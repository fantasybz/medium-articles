#!/usr/bin/env python3
"""Render F2 from a complete, hash-consistent FORMAL campaign only.

Reads JSON and source bytes for integrity checks; never imports or executes a
candidate. No success filtering, fitted effects, significance tests, random
jitter, pilot fallback, or synthetic data. Requires the pinned matplotlib stack
in requirements-figures.txt. See --help for invocation.
"""
from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import importlib.metadata
import itertools
import json
import math
import os
from pathlib import Path
import platform
import re
import sys
import tempfile
from typing import Any

ARMS = ("A0", "A", "B", "C")
RENDERER_VERSION = "same-spec-f2-v1"
ANALYSIS_VERSION = "same-spec-ten-runs-analysis-v1"
METRIC = "python-ast-node-type-multiset-cosine-v1"
REQUIREMENTS = Path(__file__).with_name("requirements-figures.txt")


class RenderRefused(ValueError):
    pass


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise RenderRefused(f"Duplicate JSON key: {key}")
        result[key] = value
    return result


def _reject_constant(value):
    raise RenderRefused(f"Non-finite JSON constant: {value}")


def _json(data: bytes, label: str):
    try:
        return json.loads(data.decode("utf-8"), object_pairs_hook=_unique_object,
                          parse_constant=_reject_constant)
    except (UnicodeError, json.JSONDecodeError) as exc:
        raise RenderRefused(f"Cannot decode {label}: {exc}") from exc


def _require(condition, message):
    if not condition:
        raise RenderRefused(message)


def _regular_file(campaign: Path, relative: str) -> Path:
    path = Path(relative)
    _require(not path.is_absolute() and ".." not in path.parts, "Unsafe campaign-relative path")
    current = campaign
    for part in path.parts:
        current = current / part
        _require(not current.is_symlink(), f"Symlink is not allowed: {relative}")
    _require(current.is_file(), f"Missing regular file: {relative}")
    _require(current.resolve().is_relative_to(campaign.resolve()), "Path escapes campaign")
    return current


def _cosine(value, label):
    _require(type(value) in (int, float) and 0 <= value <= 1 and math.isfinite(value),
             f"{label} must be a finite number in [0, 1]")
    return float(value)


def load_formal(campaign: Path) -> dict:
    """Check provenance, completeness, all-artifact pair coverage, and plot values."""
    campaign = Path(campaign)
    _require(campaign.is_dir() and not campaign.is_symlink(), "Campaign must be a real directory")
    _require(not (campaign / "HALTED.json").exists(), "Halted campaign: results rendering refused")
    checked = {}

    def read(relative):
        path = _regular_file(campaign, relative)
        data = path.read_bytes()
        checked[relative] = sha(data)
        return data

    manifest_bytes = read("manifest.json")
    manifest = _json(manifest_bytes, "manifest.json")
    _require(isinstance(manifest, dict) and manifest.get("phase") == "formal",
             "Only formal campaigns are accepted; pilot data must not be rendered")
    sidecar = read("manifest.sha256").decode("ascii").strip()
    _require(sidecar == sha(manifest_bytes), "manifest.sha256 does not match manifest.json")
    summary_bytes = read("summary.json")
    records_bytes = read("records.jsonl")
    summary = _json(summary_bytes, "summary.json")
    _require(isinstance(summary, dict) and summary.get("phase") == "formal"
             and summary.get("formal_evidence") is True, "Summary is not formal evidence")
    _require(summary.get("analysis_version") == ANALYSIS_VERSION, "Unsupported analysis schema")
    _require(summary.get("manifest_sha256") == sha(manifest_bytes), "Summary manifest hash mismatch")
    _require(summary.get("records_sha256") == sha(records_bytes), "Summary records hash mismatch")
    _require(summary.get("planned_runs") == 40 and summary.get("recorded_runs") == 40,
             "Formal summary must contain all forty scheduled records")
    _require(summary.get("other_phase_records_excluded") == 0, "Mixed-phase input ledger refused")

    source_hashes = manifest.get("source_sha256")
    _require(isinstance(source_hashes, dict), "Manifest has no frozen source hashes")
    analyzer_hash = sha(read("source/analyze.py"))
    _require(analyzer_hash == source_hashes.get("analyze.py") == summary.get("analyzer_sha256"),
             "Frozen analyzer and summary analyzer hash differ")
    renderer_hash = sha(Path(__file__).read_bytes())
    _require(source_hashes.get("render_results.py") == renderer_hash,
             "Use the exact renderer included in this campaign's frozen source bundle")
    frozen_renderer_hash = sha(read("source/render_results.py"))
    _require(frozen_renderer_hash == renderer_hash, "Frozen renderer file differs from executing renderer")
    _require(REQUIREMENTS.is_file(), "Pinned requirements-figures.txt is missing beside the renderer")
    dependency_hash = sha(REQUIREMENTS.read_bytes())
    _require(source_hashes.get("requirements-figures.txt") == dependency_hash
             and sha(read("source/requirements-figures.txt")) == dependency_hash,
             "Figure dependency pins differ from the frozen source bundle")

    schedule = manifest.get("schedule")
    _require(isinstance(schedule, list) and len(schedule) == 40, "Expected a forty-slot schedule")
    expected = {}
    blocks = {}
    for item in schedule:
        _require(isinstance(item, dict), "Scheduled slot is not an object")
        run_id, arm, block = item.get("run_id"), item.get("arm"), item.get("block")
        _require(isinstance(run_id, str) and run_id and run_id not in expected, "Invalid/duplicate scheduled ID")
        _require(arm in ARMS and type(block) is int and 1 <= block <= 10
                 and item.get("phase") == "formal", "Invalid formal slot assignment")
        expected[run_id] = {"run_id": run_id, "arm": arm, "block": block, "phase": "formal"}
        blocks.setdefault(block, []).append(arm)
    _require(len(blocks) == 10 and all(Counter(arms) == Counter(ARMS) for arms in blocks.values()),
             "Each of ten blocks must contain A0, A, B and C exactly once")

    rows = {}
    for line_number, line in enumerate(records_bytes.splitlines(), 1):
        if not line.strip():
            continue
        row = _json(line, f"records.jsonl:{line_number}")
        _require(isinstance(row, dict), "Ledger row is not an object")
        run_id = row.get("run_id")
        _require(isinstance(run_id, str) and run_id in expected and run_id not in rows,
                 "Unknown/duplicate ledger ID")
        _require(all(row.get(k) == value for k, value in expected[run_id].items()), "Ledger assignment differs from schedule")
        for field in ("cli_success", "artifact_success", "accepted_completion"):
            _require(type(row.get(field)) is bool, f"{run_id}: invalid {field}")
        _require(row["accepted_completion"] == (row["cli_success"] and row["artifact_success"]),
                 "Inconsistent accepted-completion record")
        rows[run_id] = row
    _require(set(rows) == set(expected), "Incomplete formal ledger; no result figure may be rendered")

    artifact_list = summary.get("artifacts")
    _require(isinstance(artifact_list, list) and len(artifact_list) == 40, "Expected forty artifact descriptors")
    artifacts = {}
    for artifact in artifact_list:
        _require(isinstance(artifact, dict), "Artifact descriptor is not an object")
        run_id = artifact.get("run_id")
        _require(isinstance(run_id, str) and run_id in expected and run_id not in artifacts,
                 "Unknown/duplicate artifact ID")
        _require(artifact.get("arm") == expected[run_id]["arm"]
                 and artifact.get("block") == expected[run_id]["block"], "Artifact assignment mismatch")
        _require(type(artifact.get("parsed")) is bool, "Artifact parsed flag must be boolean")
        _require(artifact.get("code_path") == rows[run_id].get("code_path")
                 and artifact.get("artifact_sha256") == rows[run_id].get("artifact_sha256"),
                 "Artifact provenance differs from ledger")
        if artifact.get("code_path") is not None:
            _require(isinstance(artifact["code_path"], str), "Artifact path must be a string")
            # Integrity only: source bytes are never imported, parsed or executed here.
            _require(sha(read(artifact["code_path"])) == artifact.get("artifact_sha256"),
                     "Sealed candidate source hash mismatch")
        else:
            _require(artifact.get("artifact_sha256") is None and not artifact["parsed"],
                     "Missing source cannot be a parsed artifact")
        value = artifact.get("seed_ast_node_type_cosine")
        if value is not None:
            _require(artifact["parsed"], "Unparseable artifact cannot have seed cosine")
            _cosine(value, f"{run_id}.seed cosine")
        else:
            _require(isinstance(artifact.get("seed_similarity_na_reason"), str)
                     and artifact["seed_similarity_na_reason"], "Missing seed value needs an explicit reason")
        artifacts[run_id] = artifact

    reference = summary.get("seed_ast_reference")
    provenance = manifest.get("task_provenance")
    _require(isinstance(reference, dict) and isinstance(provenance, dict), "Missing seed provenance")
    _require(reference.get("status") == "available", "Verified seed reference must be available")
    _require(reference.get("metric") == METRIC, "Seed cosine metric mismatch")
    _require(reference.get("reference_path") == "source/seed/codex_jsonl.py", "Unexpected seed reference path")
    seed_hash = sha(read("source/seed/codex_jsonl.py"))
    _require(seed_hash == reference.get("sha256") == provenance.get("seed_sha256"), "Seed hash mismatch")
    _require(all(not artifact["parsed"] or artifact["seed_ast_node_type_cosine"] is not None
                 for artifact in artifacts.values()), "Parsed artifact is missing its available seed reference value")

    pair_list = summary.get("pairwise_ast_similarity")
    _require(isinstance(pair_list, list), "Pairwise similarity must be a list")
    actual_pairs = {}
    for pair in pair_list:
        _require(isinstance(pair, dict) and pair.get("metric") == METRIC, "Invalid pair metric")
        left, right, arm = pair.get("run_id_left"), pair.get("run_id_right"), pair.get("arm")
        _require(isinstance(left, str) and isinstance(right, str) and left < right, "Pair IDs must be distinct and ordered")
        _require(left in artifacts and right in artifacts and arm in ARMS, "Pair references unknown artifacts")
        _require(artifacts[left]["parsed"] and artifacts[right]["parsed"]
                 and artifacts[left]["arm"] == arm == artifacts[right]["arm"], "Pair violates parsed/arm inclusion")
        key = (arm, left, right)
        _require(key not in actual_pairs, "Duplicate pair")
        actual_pairs[key] = _cosine(pair.get("cosine"), "pair cosine")

    arms = summary.get("arms")
    _require(isinstance(arms, dict) and set(arms) == set(ARMS), "Missing/extra arm summary")
    groups = {}
    expected_pair_keys = set()
    for arm in ARMS:
        arm_artifacts = sorted((a for a in artifacts.values() if a["arm"] == arm), key=lambda a: a["run_id"])
        parsed_ids = [a["run_id"] for a in arm_artifacts if a["parsed"]]
        keys = [(arm, left, right) for left, right in itertools.combinations(parsed_ids, 2)]
        expected_pair_keys.update(keys)
        arm_data = arms[arm]
        _require(isinstance(arm_data, dict) and arm_data.get("planned_runs") == 10
                 and arm_data.get("recorded_runs") == 10, "Arm is incomplete")
        metric = arm_data.get("ast_similarity")
        _require(isinstance(metric, dict) and metric.get("metric") == METRIC, "Arm metric mismatch")
        _require(metric.get("planned_artifacts") == 10 and metric.get("parsed_artifacts") == len(parsed_ids)
                 and metric.get("possible_pairs_if_all_parsed") == 45
                 and metric.get("observed_pairs") == len(keys), "Arm pair/artifact denominators disagree")
        groups[arm] = {"artifacts": arm_artifacts, "parsed_ids": parsed_ids, "pair_keys": keys}
    _require(set(actual_pairs) == expected_pair_keys,
             "Pair list is incomplete or filtered; all parseable artifacts must contribute")
    for group in groups.values():
        group["pairs"] = [{"left": key[1], "right": key[2], "cosine": actual_pairs[key]}
                          for key in group.pop("pair_keys")]
    return {"campaign": campaign, "groups": groups, "checked_sha256": checked,
            "renderer_sha256": renderer_hash, "requirements_sha256": dependency_hash,
            "manifest_sha256": sha(manifest_bytes), "summary_sha256": sha(summary_bytes),
            "records_sha256": sha(records_bytes), "analyzer_sha256": analyzer_hash,
            "seed_sha256": seed_hash, "model": manifest.get("model"), "effort": manifest.get("effort")}


def offsets(count: int, half_span: float) -> list[float]:
    """Lexicographic ID rank receives a fixed vertical offset, never random jitter."""
    if count <= 1:
        return [0.0] * count
    return [-half_span + 2 * half_span * index / (count - 1) for index in range(count)]


def _dependency_versions():
    _require(REQUIREMENTS.is_file(), "Pinned figure dependencies are missing")
    versions = {}
    for raw in REQUIREMENTS.read_text().splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        _require(re.fullmatch(r"[A-Za-z0-9_.-]+==[A-Za-z0-9_.+-]+", line), "Only exact dependency pins are supported")
        package, expected = line.split("==")
        try:
            observed = importlib.metadata.version(package)
        except importlib.metadata.PackageNotFoundError as exc:
            raise RenderRefused(f"Install pinned figure dependencies: missing {package}") from exc
        _require(observed == expected, f"Dependency mismatch: {package} is {observed}, expected {expected}")
        versions[package] = observed
    _require("matplotlib" in versions, "Figure dependency lock has no matplotlib")
    return versions


def render(inputs: dict, output_dir: Path, *, prefix: str = "F2", overwrite: bool = False) -> dict:
    versions = _dependency_versions()
    # Matplotlib is imported only after the formal-data and provenance checks pass.
    import matplotlib
    matplotlib.use("Agg")
    from matplotlib import pyplot as plt, font_manager, ft2font

    _require(re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_-]{0,63}", prefix), "Invalid output prefix")
    output_dir = Path(output_dir).resolve()
    campaign = inputs["campaign"].resolve()
    _require(not output_dir.is_relative_to(campaign / "source"), "Do not write into the frozen source bundle")
    for group in inputs["groups"].values():
        for artifact in group["artifacts"]:
            if artifact["code_path"] is not None:
                _require(not output_dir.is_relative_to((campaign / artifact["code_path"]).parent),
                         "Do not write into a sealed candidate directory")
    outputs = {kind: output_dir / f"{prefix}.{kind}" for kind in ("svg", "png", "metadata.json")}
    _require(overwrite or not any(path.exists() for path in outputs.values()),
             "Output exists; choose another directory or explicitly use --overwrite")
    output_dir.mkdir(parents=True, exist_ok=True)
    plot_data = {"pair_points": [], "seed_points": [], "missing_seed_values": [], "arm_counts": {}}
    rc = {"font.family": "DejaVu Sans", "font.size": 11,
          "axes.labelsize": 11, "axes.titlesize": 13, "xtick.labelsize": 10,
          "ytick.labelsize": 10.5, "svg.fonttype": "path",
          "svg.hashsalt": RENDERER_VERSION + ":" + inputs["summary_sha256"],
          "figure.facecolor": "white", "axes.facecolor": "white",
          "savefig.facecolor": "white", "axes.unicode_minus": False}
    with plt.rc_context(rc):
        fig, axes = plt.subplots(2, 1, figsize=(9.6, 9.1), sharex=True)
        fig.subplots_adjust(left=0.31, right=0.965, top=0.87, bottom=0.17, hspace=0.48)
        fig.suptitle("Same spec, ten runs: structural descriptions", x=0.035, y=0.965,
                     ha="left", fontsize=17, fontweight="bold", color="#1f2933")
        fig.text(0.035, 0.923, "Formal cohort. All parseable artifacts, regardless of acceptance.",
                 ha="left", fontsize=11, color="#475569")
        for axis, title in zip(axes, ("A. Within-arm pairs", "B. Each artifact versus the frozen seed")):
            axis.set_title(title, loc="left", pad=13, fontweight="bold")
            axis.set_xlim(0, 1)
            axis.set_ylim(-0.6, 3.6)
            axis.set_xticks([0, 0.25, 0.5, 0.75, 1], ["0", "0.25", "0.50", "0.75", "1"])
            axis.tick_params(axis="x", labelbottom=True, length=0, pad=7)
            axis.tick_params(axis="y", length=0, pad=10)
            axis.set_xlabel("AST node-type cosine (fixed 0-1 axis)", labelpad=8)
            axis.grid(axis="x", color="#d7dde4", linewidth=0.7, zorder=0)
            for spine in ("top", "left", "right"):
                axis.spines[spine].set_visible(False)
            axis.spines["bottom"].set_color("#94a3b8")
        top_labels, bottom_labels = [], []
        for index, arm in enumerate(ARMS):
            center = 3 - index
            group = inputs["groups"][arm]
            pairs = group["pairs"]
            pair_offsets = offsets(len(pairs), 0.25)
            top_labels.append(f"{arm}  artifacts {len(group['parsed_ids'])}/10\n"
                              f"pairs {len(pairs)}/45 (missing {45-len(pairs)})")
            pair_x = [p["cosine"] for p in pairs]
            pair_y = [center + shift for shift in pair_offsets]
            axes[0].scatter(pair_x, pair_y, s=15, alpha=0.72, color="#355f7c",
                            edgecolors="none", zorder=3, clip_on=False)
            for pair, y in zip(pairs, pair_y):
                plot_data["pair_points"].append({"arm": arm, **pair, "y": y})
            seed_artifacts = [a for a in group["artifacts"] if a["seed_ast_node_type_cosine"] is not None]
            missing = [a for a in group["artifacts"] if a["seed_ast_node_type_cosine"] is None]
            seed_offsets = offsets(len(seed_artifacts), 0.23)
            seed_y = [center + shift for shift in seed_offsets]
            axes[1].scatter([a["seed_ast_node_type_cosine"] for a in seed_artifacts], seed_y,
                            s=24, marker="D", alpha=0.85, color="#355f7c",
                            edgecolors="none", zorder=3, clip_on=False)
            bottom_labels.append(f"{arm}  seed values {len(seed_artifacts)}/10\nmissing {len(missing)}")
            for artifact, y in zip(seed_artifacts, seed_y):
                plot_data["seed_points"].append({"arm": arm, "run_id": artifact["run_id"],
                                                  "cosine": artifact["seed_ast_node_type_cosine"], "y": y})
            plot_data["missing_seed_values"].extend({"arm": arm, "run_id": a["run_id"],
                                                       "reason": a["seed_similarity_na_reason"]} for a in missing)
            plot_data["arm_counts"][arm] = {"planned_artifacts": 10, "parsed_artifacts": len(group["parsed_ids"]),
                                             "observed_pairs": len(pairs), "possible_pairs": 45,
                                             "seed_observed": len(seed_artifacts), "seed_missing": len(missing)}
            for axis, count in ((axes[0], len(pairs)), (axes[1], len(seed_artifacts))):
                if not count:
                    axis.text(0.04, center, "No observed values", va="center", color="#64748b", fontsize=10)
        axes[0].set_yticks([3, 2, 1, 0], top_labels)
        axes[1].set_yticks([3, 2, 1, 0], bottom_labels)
        fig.text(0.035, 0.102, "Artifacts means hash-verified, nonempty, parseable source. Missing values are not zero.",
                 ha="left", fontsize=9.5, color="#475569")
        fig.text(0.035, 0.078, "Pair dots share artifacts; they are not independent observations. Vertical spacing follows ID order.",
                 ha="left", fontsize=9.5, color="#475569")
        fig.text(0.035, 0.054, "Similarity does not measure correctness or maintainability. A shared seed can produce a ceiling effect.",
                 ha="left", fontsize=9.5, color="#475569")
        font_path = Path(font_manager.findfont("DejaVu Sans", fallback_to_default=False))
        metadata = {"schema_version": 1, "renderer_version": RENDERER_VERSION,
                    "phase": "formal", "metric": METRIC,
                    "source_sha256": {key: inputs[key] for key in
                                      ("manifest_sha256", "records_sha256", "summary_sha256", "analyzer_sha256", "seed_sha256")},
                    "renderer_sha256": inputs["renderer_sha256"], "requirements_sha256": inputs["requirements_sha256"],
                    "checked_campaign_files": inputs["checked_sha256"],
                    "python_version": platform.python_version(), "platform": sys.platform,
                    "dependencies": versions, "backend": "Agg", "freetype_version": ft2font.__freetype_version__,
                    "font": {"family": "DejaVu Sans", "sha256": sha(font_path.read_bytes())},
                    "figure_inches": [9.6, 9.1], "png_dpi": 240, "svg_fonttype": "path",
                    "x_axis": {"min": 0, "max": 1, "shared_by_both_panels": True},
                    "vertical_layout": "Lexicographic IDs, evenly spaced: pair +/-0.25; artifact +/-0.23; no random jitter",
                    "inclusion": "All hash-verified nonempty parseable artifacts; accepted status is not a filter",
                    "plot_data": plot_data}
        with tempfile.TemporaryDirectory(prefix="f2-stage-", dir=output_dir) as temporary:
            stage = Path(temporary)
            try:
                fig.savefig(stage / f"{prefix}.svg", format="svg",
                            metadata={"Date": None, "Creator": RENDERER_VERSION,
                                      "Description": "Descriptive AST cosine; all parseable formal artifacts; fixed 0-1 axes."})
                fig.savefig(stage / f"{prefix}.png", format="png", dpi=240,
                            metadata={"Software": RENDERER_VERSION, "Description": "Descriptive AST cosine; fixed 0-1 axes."})
            finally:
                plt.close(fig)
            # A writer changing a campaign while we render invalidates the artifact.
            _require(not (campaign / "HALTED.json").exists(), "Campaign halted during rendering")
            for relative, expected_hash in inputs["checked_sha256"].items():
                _require(sha(_regular_file(campaign, relative).read_bytes()) == expected_hash,
                         f"Input changed during rendering: {relative}")
            metadata["outputs"] = {kind: {"filename": outputs[kind].name,
                                         "sha256": sha((stage / outputs[kind].name).read_bytes())}
                                   for kind in ("svg", "png")}
            metadata_path = stage / outputs["metadata.json"].name
            metadata_path.write_text(json.dumps(metadata, ensure_ascii=False, indent=2, sort_keys=True,
                                                 allow_nan=False) + "\n")
            for kind in ("svg", "png", "metadata.json"):
                os.replace(stage / outputs[kind].name, outputs[kind])
    return {"outputs": {kind: str(path) for kind, path in outputs.items()},
            "phase": "formal", "manifest_sha256": inputs["manifest_sha256"],
            "summary_sha256": inputs["summary_sha256"], "renderer_sha256": inputs["renderer_sha256"]}


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("campaign", type=Path, help="Formal campaign with a complete frozen summary.json")
    parser.add_argument("--output-dir", type=Path, help="SVG/PNG/metadata destination; never a sealed source/candidate directory")
    parser.add_argument("--prefix", default="F2")
    parser.add_argument("--validate-only", action="store_true", help="Check formal provenance/completeness, without importing matplotlib or drawing")
    parser.add_argument("--overwrite", action="store_true", help="Explicitly replace existing figure outputs")
    args = parser.parse_args(argv)
    if not args.validate_only and args.output_dir is None:
        parser.error("--output-dir is required unless --validate-only is used")
    try:
        inputs = load_formal(args.campaign)
        if args.validate_only:
            print(json.dumps({"status": "valid_formal_inputs", "summary_sha256": inputs["summary_sha256"],
                              "renderer_sha256": inputs["renderer_sha256"]}))
        else:
            print(json.dumps(render(inputs, args.output_dir, prefix=args.prefix, overwrite=args.overwrite)))
    except (RenderRefused, OSError, ImportError, KeyError, TypeError, UnicodeError) as exc:
        print(f"Rendering refused: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
