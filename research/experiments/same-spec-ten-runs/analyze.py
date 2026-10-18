#!/usr/bin/env python3
"""Validate a frozen run ledger and recompute descriptive experiment reports.

No candidate code is imported or executed. Formal analyses require the entire
prescheduled 10-block, four-arm cohort, including failed and timed-out runs.
AST similarities are conditional descriptions of available parsed artifacts.
"""

from __future__ import annotations

import argparse
import ast
from collections import Counter
import copy
import hashlib
import itertools
import json
import math
import os
from pathlib import Path
import platform
import statistics
import sys
import tempfile
from typing import Any


ARMS = ("A0", "A", "B", "C")
ANALYSIS_VERSION = "same-spec-ten-runs-analysis-v1"
AST_METRIC = "python-ast-node-type-multiset-cosine-v1"
NORMALIZED_AST_METRIC = "python-identifier-normalized-ast-sha256-v1"
TOKEN_FIELDS = {
    "input_tokens": ("input_tokens",),
    "output_tokens": ("output_tokens",),
    "cache_read_input_tokens": ("cache_read_input_tokens", "cache_read_tokens"),
    "cache_creation_input_tokens": (
        "cache_creation_input_tokens", "cache_write_tokens", "cache_creation_tokens"
    ),
}


class AnalysisError(ValueError):
    """The input ledger cannot support the requested analysis."""


def _reject_constant(value: str) -> None:
    raise AnalysisError(f"Non-finite JSON constant: {value}")


def _unique_keys(pairs: list[tuple[str, Any]]) -> dict:
    result = {}
    for key, value in pairs:
        if key in result:
            raise AnalysisError(f"Duplicate JSON object key: {key}")
        result[key] = value
    return result


def _json(text: str, label: str) -> Any:
    try:
        return json.loads(text, parse_constant=_reject_constant,
                          object_pairs_hook=_unique_keys)
    except (json.JSONDecodeError, AnalysisError) as exc:
        raise AnalysisError(f"{label}: {exc}") from exc


def _number(value: Any, label: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise AnalysisError(f"{label} must be a nonnegative finite number")
    if not math.isfinite(value) or value < 0:
        raise AnalysisError(f"{label} must be a nonnegative finite number")
    return value


def _run_fields(item: dict, label: str, default_phase: str | None = None) -> dict:
    if not isinstance(item, dict):
        raise AnalysisError(f"{label} must be an object")
    run_id = item.get("run_id")
    arm = item.get("arm")
    block = item.get("block")
    phase = item.get("phase", default_phase)
    if not isinstance(run_id, str) or not run_id.strip():
        raise AnalysisError(f"{label}.run_id must be a nonempty string")
    if arm not in ARMS:
        raise AnalysisError(f"{label}.arm must be one of {ARMS}")
    if type(block) is not int or block < 0:
        raise AnalysisError(f"{label}.block must be a nonnegative integer")
    if phase not in ("formal", "pilot"):
        raise AnalysisError(f"{label}.phase must be formal or pilot")
    return {"run_id": run_id, "arm": arm, "block": block, "phase": phase}


def _usage_value(usage: dict, canonical: str, run_id: str) -> float | None:
    found = [(key, usage[key]) for key in TOKEN_FIELDS[canonical]
             if key in usage and usage[key] is not None]
    if not found:
        return None
    for key, value in found:
        _number(value, f"{run_id}.usage.{key}")
    if any(value != found[0][1] for _, value in found):
        raise AnalysisError(f"{run_id}: conflicting aliases for {canonical}")
    return found[0][1]


def validate_inputs(manifest: dict, records: list[dict]) -> tuple[str, list[dict]]:
    """Return phase and ordered rows; never silently drop ledger rows."""
    if not isinstance(manifest, dict):
        raise AnalysisError("manifest.json must contain an object")
    phase = manifest.get("phase", "formal")
    if phase not in ("formal", "pilot"):
        raise AnalysisError("manifest.phase must be formal or pilot")
    schedule = manifest.get("schedule")
    if not isinstance(schedule, list) or not schedule:
        raise AnalysisError("manifest.schedule must be a nonempty list")
    expected = {}
    for index, item in enumerate(schedule):
        fields = _run_fields(item, f"schedule[{index}]", phase)
        run_id = fields["run_id"]
        if run_id in expected:
            raise AnalysisError(f"Duplicate scheduled run_id: {run_id}")
        expected[run_id] = fields

    selected = [item for item in expected.values() if item["phase"] == phase]
    if not selected:
        raise AnalysisError(f"No {phase} entries in manifest.schedule")
    if phase == "formal":
        arm_counts = Counter(item["arm"] for item in selected)
        if len(selected) != 40 or any(arm_counts[arm] != 10 for arm in ARMS):
            raise AnalysisError("Formal schedule must contain exactly 10 runs per arm (40 total)")
        blocks = {}
        for item in selected:
            blocks.setdefault(item["block"], []).append(item["arm"])
        if len(blocks) != 10 or any(Counter(arms) != Counter(ARMS)
                                    for arms in blocks.values()):
            raise AnalysisError("Formal schedule requires 10 blocks, each containing every arm once")

    actual = {}
    for index, row in enumerate(records):
        fields = _run_fields(row, f"records[{index}]")
        run_id = fields["run_id"]
        if run_id in actual:
            raise AnalysisError(f"Duplicate record run_id: {run_id}")
        if run_id not in expected:
            raise AnalysisError(f"Unknown record run_id: {run_id}")
        if fields != expected[run_id]:
            raise AnalysisError(f"Record assignment does not match schedule: {run_id}")
        if not isinstance(row.get("status"), str) or not row["status"].strip():
            raise AnalysisError(f"{run_id}.status must be a nonempty string")
        if row.get("boundary_violation") is True or row["status"] == "boundary_failure":
            raise AnalysisError(f"{run_id}: observed boundary violation; report campaign status, not outcome intervals")
        for field in ("cli_success", "artifact_success", "accepted_completion"):
            if type(row.get(field)) is not bool:
                raise AnalysisError(f"{run_id}.{field} must be a boolean")
        if row["accepted_completion"] != (row["cli_success"] and row["artifact_success"]):
            raise AnalysisError(f"{run_id}: accepted_completion must equal cli_success AND artifact_success")
        if "wall_seconds" not in row:
            raise AnalysisError(f"{run_id}.wall_seconds is required (null if unknown)")
        if row["wall_seconds"] is not None:
            _number(row["wall_seconds"], f"{run_id}.wall_seconds")
        if "total_cost_usd" not in row:
            raise AnalysisError(f"{run_id}.total_cost_usd is required (null if unknown)")
        if row["total_cost_usd"] is not None:
            _number(row["total_cost_usd"], f"{run_id}.total_cost_usd")
        usage = row.get("usage")
        if not isinstance(usage, dict):
            raise AnalysisError(f"{run_id}.usage must be an object")
        for field in TOKEN_FIELDS:
            _usage_value(usage, field, run_id)
        if "code_path" not in row or "artifact_sha256" not in row:
            raise AnalysisError(f"{run_id}: code_path and artifact_sha256 are required")
        path, digest = row["code_path"], row["artifact_sha256"]
        if path is None:
            if digest is not None or row["artifact_success"]:
                raise AnalysisError(f"{run_id}: absent code cannot have a hash or artifact_success")
        else:
            if not isinstance(path, str) or not path.strip():
                raise AnalysisError(f"{run_id}.code_path must be a nonempty relative path or null")
            if (not isinstance(digest, str) or len(digest) != 64
                    or any(c not in "0123456789abcdefABCDEF" for c in digest)):
                raise AnalysisError(f"{run_id}.artifact_sha256 must be a SHA-256 hex digest")
        actual[run_id] = row

    missing = [run_id for run_id in expected if run_id not in actual]
    if missing:
        raise AnalysisError(f"Missing scheduled records: {', '.join(missing)}")
    return phase, [actual[item["run_id"]] for item in selected]


def clopper_pearson(successes: int, total: int, alpha: float = 0.05) -> tuple[float, float]:
    """Two-sided exact binomial bounds, inverted with stdlib bisection."""
    if (type(successes) is not int or type(total) is not int or total <= 0
            or successes < 0 or successes > total or not 0 < alpha < 1):
        raise ValueError("Require integer 0 <= successes <= total, total > 0, 0 < alpha < 1")
    target = alpha / 2.0

    def probability(p: float, start: int, end: int) -> float:
        return math.fsum(math.comb(total, k) * p ** k * (1 - p) ** (total - k)
                         for k in range(start, end + 1))

    lower = 0.0
    if successes:
        low, high = 0.0, 1.0
        for _ in range(90):
            mid = (low + high) / 2.0
            if probability(mid, successes, total) < target:
                low = mid
            else:
                high = mid
        lower = (low + high) / 2.0
    upper = 1.0
    if successes < total:
        low, high = 0.0, 1.0
        for _ in range(90):
            mid = (low + high) / 2.0
            if probability(mid, 0, successes) > target:
                low = mid
            else:
                high = mid
        upper = (low + high) / 2.0
    return lower, upper


def _outcome(rows: list[dict], field: str) -> dict:
    n, k = len(rows), sum(row[field] for row in rows)
    bounds = clopper_pearson(k, n) if n else (None, None)
    return {
        "successes": k, "total": n, "rate": k / n if n else None,
        "ci95": {"lower": bounds[0], "upper": bounds[1],
                 "method": "two-sided Clopper-Pearson", "confidence": 0.95},
    }


def describe(values: list[float | None], *, include_total: bool = True) -> dict:
    present = sorted(value for value in values if value is not None)
    n = len(present)

    def quantile(q: float) -> float | None:
        if not n:
            return None
        index = (n - 1) * q
        left, right = math.floor(index), math.ceil(index)
        return present[left] + (present[right] - present[left]) * (index - left)

    q25, q75 = quantile(0.25), quantile(0.75)
    result = {
        "observed": n, "missing": len(values) - n,
        "min": present[0] if n else None,
        "q25": q25, "median": statistics.median(present) if n else None,
        "q75": q75, "max": present[-1] if n else None,
        "mean": statistics.fmean(present) if n else None,
        "iqr": q75 - q25 if n else None,
    }
    if include_total:
        result["total_observed"] = math.fsum(present) if n else None
    return result


def _normalized_ast_sha(tree: ast.AST) -> str:
    """Collapse selected identifier fields; this is not semantic equivalence."""
    normalized = copy.deepcopy(tree)
    for node in ast.walk(normalized):
        if isinstance(node, ast.Name):
            node.id = "__ID__"
        elif isinstance(node, ast.arg):
            node.arg = "__ID__"
        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            node.name = "__ID__"
        elif isinstance(node, (ast.Global, ast.Nonlocal)):
            node.names = ["__ID__"] * len(node.names)
        elif isinstance(node, ast.ExceptHandler) and node.name is not None:
            node.name = "__ID__"
        elif isinstance(node, ast.alias) and node.asname is not None:
            node.asname = "__ID__"
        elif isinstance(node, (ast.MatchAs, ast.MatchStar)) and node.name is not None:
            node.name = "__ID__"
        elif isinstance(node, ast.MatchMapping) and node.rest is not None:
            node.rest = "__ID__"
    representation = ast.dump(normalized, annotate_fields=True, include_attributes=False)
    return hashlib.sha256(representation.encode("utf-8")).hexdigest()


def _artifact(campaign: Path, row: dict) -> tuple[dict, Counter | None]:
    result = {
        "run_id": row["run_id"], "arm": row["arm"], "block": row["block"],
        "code_path": row["code_path"], "artifact_sha256": row["artifact_sha256"],
        "parsed": False, "na_reason": "no_code_produced",
        "identifier_normalized_ast_sha256": None,
        "function_count": None, "async_function_count": None, "class_count": None,
        "ast_node_type_counts": None,
    }
    if row["code_path"] is None:
        return result, None
    relative = Path(row["code_path"])
    if relative.is_absolute() or ".." in relative.parts:
        raise AnalysisError(f"{row['run_id']}: code_path must remain inside campaign directory")
    path = campaign
    for part in relative.parts:
        path = path / part
        if path.is_symlink():
            raise AnalysisError(f"{row['run_id']}: symlink in sealed code_path")
    if not path.is_file():
        raise AnalysisError(f"{row['run_id']}: sealed code file is missing: {relative}")
    if not path.resolve().is_relative_to(campaign.resolve()):
        raise AnalysisError(f"{row['run_id']}: code_path escapes campaign directory")
    source = path.read_bytes()
    digest = hashlib.sha256(source).hexdigest()
    if digest != row["artifact_sha256"].lower():
        raise AnalysisError(f"{row['run_id']}: artifact SHA-256 mismatch")
    try:
        tree = ast.parse(source, filename=str(relative))
        if not tree.body:
            result["na_reason"] = "empty_module"
            return result, None
        nodes = list(ast.walk(tree))
        counts = Counter(type(node).__name__ for node in nodes)
        normalized_sha = _normalized_ast_sha(tree)
    except (SyntaxError, ValueError, UnicodeError, RecursionError) as exc:
        result["na_reason"] = f"parse_error:{type(exc).__name__}"
        if isinstance(exc, SyntaxError):
            result["syntax_error_line"] = exc.lineno
        return result, None
    result.update({
        "parsed": True, "na_reason": None,
        "identifier_normalized_ast_sha256": normalized_sha,
        "function_count": sum(isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
                              for node in nodes),
        "async_function_count": sum(isinstance(node, ast.AsyncFunctionDef) for node in nodes),
        "class_count": sum(isinstance(node, ast.ClassDef) for node in nodes),
        "ast_node_type_counts": dict(sorted(counts.items())),
    })
    return result, counts


def _cosine(left: Counter, right: Counter) -> float:
    dot = sum(value * right.get(key, 0) for key, value in left.items())
    norm = math.sqrt(sum(value * value for value in left.values())
                     * sum(value * value for value in right.values()))
    return min(1.0, max(0.0, dot / norm))


def _seed_reference(campaign: Path, manifest: dict) -> tuple[dict, Counter | None]:
    """Read only the provenance-identified frozen seed; never infer a baseline."""
    result = {
        "status": "not_available", "na_reason": "seed_provenance_not_recorded",
        "reference_path": None, "sha256": None, "ast_node_type_counts": None,
        "metric": AST_METRIC,
    }
    provenance = manifest.get("task_provenance")
    if provenance is None:
        return result, None
    if not isinstance(provenance, dict):
        raise AnalysisError("manifest.task_provenance must be an object")
    expected = provenance.get("seed_sha256")
    if (not isinstance(expected, str) or len(expected) != 64
            or any(c not in "0123456789abcdefABCDEF" for c in expected)):
        raise AnalysisError("manifest.task_provenance.seed_sha256 must be a SHA-256 hex digest")
    relative = Path("source/seed/codex_jsonl.py")
    path = campaign
    for part in relative.parts:
        path = path / part
        if path.is_symlink():
            raise AnalysisError("Symlink in frozen seed reference path")
    if not path.is_file():
        raise AnalysisError("Frozen seed declared by task_provenance is missing")
    if not path.resolve().is_relative_to(campaign.resolve()):
        raise AnalysisError("Frozen seed reference escapes campaign directory")
    source = path.read_bytes()
    actual = hashlib.sha256(source).hexdigest()
    if actual != expected.lower():
        raise AnalysisError("Frozen seed SHA-256 does not match task_provenance")
    result.update(reference_path=relative.as_posix(), sha256=actual)
    try:
        tree = ast.parse(source, filename=str(relative))
        if not tree.body:
            result["na_reason"] = "empty_seed_module"
            return result, None
        counts = Counter(type(node).__name__ for node in ast.walk(tree))
    except (SyntaxError, ValueError, UnicodeError, RecursionError) as exc:
        result["na_reason"] = f"seed_parse_error:{type(exc).__name__}"
        return result, None
    result.update(status="available", na_reason=None,
                  ast_node_type_counts=dict(sorted(counts.items())))
    return result, counts


def analyze_campaign(campaign: Path | str) -> dict:
    if sys.version_info < (3, 10):
        raise AnalysisError("Python 3.10+ is required for the frozen AST metric; select an explicit interpreter")
    campaign = Path(campaign)
    if (campaign / "HALTED.json").exists():
        raise AnalysisError("Halted campaign: report campaign_status.py; no outcome intervals")
    try:
        manifest_bytes = (campaign / "manifest.json").read_bytes()
        records_bytes = (campaign / "records.jsonl").read_bytes()
        manifest = _json(manifest_bytes.decode("utf-8"), "manifest.json")
        records = [_json(line, f"records.jsonl:{index}")
                   for index, line in enumerate(records_bytes.decode("utf-8").splitlines(), 1)
                   if line.strip()]
    except (OSError, UnicodeError) as exc:
        raise AnalysisError(f"Cannot read campaign inputs: {exc}") from exc
    phase, rows = validate_inputs(manifest, records)
    seed_reference, seed_vector = _seed_reference(campaign, manifest)
    artifacts, vectors = [], {}
    for row in rows:
        artifact, vector = _artifact(campaign, row)
        artifact["seed_ast_node_type_cosine"] = (
            _cosine(vector, seed_vector) if vector is not None and seed_vector is not None else None
        )
        artifact["seed_similarity_na_reason"] = (
            artifact["na_reason"] if vector is None else seed_reference["na_reason"]
        )
        artifacts.append(artifact)
        if vector is not None:
            vectors[row["run_id"]] = vector
    arm_summaries = {}
    pair_rows = []
    for arm in ARMS:
        group = [row for row in rows if row["arm"] == arm]
        arm_artifacts = [item for item in artifacts if item["arm"] == arm]
        parsed = [item for item in arm_artifacts if item["parsed"]]
        similarities = []
        for left, right in itertools.combinations(parsed, 2):
            similarity = _cosine(vectors[left["run_id"]], vectors[right["run_id"]])
            similarities.append(similarity)
            pair_rows.append({
                "arm": arm, "run_id_left": left["run_id"], "run_id_right": right["run_id"],
                "metric": AST_METRIC, "cosine": similarity,
                "normalized_ast_equal": (left["identifier_normalized_ast_sha256"]
                                         == right["identifier_normalized_ast_sha256"]),
            })
        arm_summaries[arm] = {
            "planned_runs": len(group), "recorded_runs": len(group),
            "accepted_completion": _outcome(group, "accepted_completion"),
            "artifact_success": _outcome(group, "artifact_success"),
            "cli_success": _outcome(group, "cli_success"),
            "status_counts": dict(sorted(Counter(row["status"] for row in group).items())),
            "wall_seconds_observed": describe([row["wall_seconds"] for row in group]),
            "reported_cost_usd": describe([row["total_cost_usd"] for row in group]),
            "reported_usage": {
                field: describe([_usage_value(row["usage"], field, row["run_id"])
                                 for row in group]) for field in TOKEN_FIELDS
            },
            "ast_similarity": {
                "metric": AST_METRIC,
                "conditional_on": "produced, hash-verified, nonempty, parsed artifacts",
                "planned_artifacts": len(group),
                "produced_artifacts": sum(item["code_path"] is not None for item in arm_artifacts),
                "parsed_artifacts": len(parsed),
                "unavailable_reasons": dict(sorted(Counter(item["na_reason"] for item in arm_artifacts
                                                          if not item["parsed"]).items())),
                "possible_pairs_if_all_parsed": len(group) * (len(group) - 1) // 2,
                "observed_pairs": len(similarities),
                "distribution": describe(similarities, include_total=False),
                "unique_normalized_ast_hashes": len({item["identifier_normalized_ast_sha256"]
                                                     for item in parsed}),
                "seed_ast_node_type_cosine": describe(
                    [item["seed_ast_node_type_cosine"] for item in arm_artifacts], include_total=False
                ),
            },
        }

    return {
        "analysis_version": ANALYSIS_VERSION, "phase": phase,
        "formal_evidence": phase == "formal",
        "manifest_sha256": hashlib.sha256(manifest_bytes).hexdigest(),
        "records_sha256": hashlib.sha256(records_bytes).hexdigest(),
        "analyzer_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "python_version": platform.python_version(),
        "primary_outcome": "accepted_completion = cli_success AND artifact_success",
        "planned_runs": len(rows), "recorded_runs": len(rows),
        "other_phase_records_excluded": len(records) - len(rows),
        "arms": arm_summaries,
        "artifacts": artifacts, "pairwise_ast_similarity": pair_rows,
        "seed_ast_reference": seed_reference,
        "normalized_ast_metric": NORMALIZED_AST_METRIC,
        "normalized_ast_definition": (
            "ast.dump with locations omitted; Name.id, arg.arg, function/class names, "
            "global/nonlocal names, exception targets, import aliases and match bindings "
            "collapse to __ID__. Attribute names, import paths, constants and tree order remain. "
            "Not binding-aware or a test of semantic equivalence."
        ),
        "limitations": [
            "All prescheduled run outcomes remain in the primary denominator, including failures.",
            "Ledger completeness does not verify preregistration timing, model pinning, sandbox enforcement or oracle validity; these need separate audit artifacts.",
            "Exact binomial intervals assume a common Bernoulli success probability; provider drift or dependence may violate this.",
            "Ten successes do not establish production reliability or a pass^10 probability.",
            "AST cosine ignores order, identifiers and literal values; similarity is not correctness or maintainability.",
            "Shared source scaffolding may drive high within-arm similarity. Seed-relative cosine is supplemental and does not subtract common code or resolve that ceiling effect.",
            "Pairwise similarities share runs and are not independent observations; no pair bootstrap or significance test is used.",
            "Similarity is conditional on available parsed artifacts, including failed artifacts, and may be selected by missingness.",
            "Reported CLI cost is not a billing invoice. Unknown usage or cost remains missing, not zero.",
            "Observed durations and token use include capped runs; they are not uncensored time-to-completion estimates.",
            "No human review time, human calibration or production authorization is inferred.",
        ],
    }


def render_report(summary: dict) -> str:
    def percent(value: float | None) -> str:
        return "NA" if value is None else f"{100 * value:.2f}%"

    def amount(value: float | None, digits: int = 3) -> str:
        return "NA" if value is None else f"{value:.{digits}f}"

    lines = [
        "# Same-spec controlled generation: descriptive report", "",
        f"Phase: **{summary['phase']}**. Planned and recorded: **{summary['planned_runs']}**.", "",
        "Primary outcome: `accepted_completion = cli_success AND artifact_success`.",
        "All prescheduled failures remain in the denominator. Intervals are two-sided 95% Clopper–Pearson.", "",
        "| Arm | Accepted / planned | Exact 95% CI | Artifact successes | CLI successes |",
        "|---|---:|---|---:|---:|",
    ]
    if not summary["formal_evidence"]:
        lines.insert(4, "Pilot data are development evidence and are excluded from any formal cohort.")
    for arm in ARMS:
        data = summary["arms"][arm]
        primary = data["accepted_completion"]
        bounds = primary["ci95"]
        lines.append(f"| {arm} | {primary['successes']}/{primary['total']} | "
                     f"{percent(bounds['lower'])}–{percent(bounds['upper'])} | "
                     f"{data['artifact_success']['successes']}/{primary['total']} | "
                     f"{data['cli_success']['successes']}/{primary['total']} |")
    lines += ["", "## Observed resources", "",
              "Costs are reported CLI estimates, not billing invoices. Missing values are not zero; capped and failed runs remain included.", "",
              "| Arm | Wall seconds, median (observed/planned) | Reported USD total | Cost observed / planned | Input tokens total | Output tokens total | Cache read / creation totals |",
              "|---|---:|---:|---:|---:|---:|---:|"]
    for arm in ARMS:
        data = summary["arms"][arm]
        cost, usage = data["reported_cost_usd"], data["reported_usage"]
        token = lambda field: amount(usage[field]["total_observed"], 0) + f" ({usage[field]['observed']}/{data['planned_runs']})"
        wall = data["wall_seconds_observed"]
        lines.append(f"| {arm} | {amount(wall['median'])} ({wall['observed']}/{data['planned_runs']}) | "
                     f"{amount(cost['total_observed'], 6)} | {cost['observed']}/{data['planned_runs']} | "
                     f"{token('input_tokens')} | {token('output_tokens')} | "
                     f"{token('cache_read_input_tokens')} / {token('cache_creation_input_tokens')} |")
    lines += ["", "## Exploratory AST description", "",
              "Metric: AST node-type multiset cosine. This ignores order and many semantic differences. Only produced, hash-verified, nonempty parsed artifacts contribute; unsuccessful runs can contribute artifacts.", "",
              "| Arm | Produced / planned | Parsed / planned | Pairs observed / possible | Median cosine | Min cosine | Unique normalized AST hashes | Seed cosine: median [min, max]; observed/planned |",
              "|---|---:|---:|---:|---:|---:|---:|---|"]
    for arm in ARMS:
        metric = summary["arms"][arm]["ast_similarity"]
        n = metric["planned_artifacts"]
        seed = metric["seed_ast_node_type_cosine"]
        seed_text = (f"{amount(seed['median'])} [{amount(seed['min'])}, {amount(seed['max'])}]; "
                     f"{seed['observed']}/{n}")
        lines.append(f"| {arm} | {metric['produced_artifacts']}/{n} | {metric['parsed_artifacts']}/{n} | "
                     f"{metric['observed_pairs']}/{metric['possible_pairs_if_all_parsed']} | "
                     f"{amount(metric['distribution']['median'])} | {amount(metric['distribution']['min'])} | "
                     f"{metric['unique_normalized_ast_hashes']} | {seed_text} |")
    reference = summary["seed_ast_reference"]
    if reference["status"] == "available":
        lines += ["", "Seed-relative cosine uses `source/seed/codex_jsonl.py`, verified against "
                  "`manifest.task_provenance.seed_sha256`. High similarity can reflect shared seed scaffolding; "
                  "this description does not subtract shared code or support an inferential conclusion."]
    else:
        lines += ["", f"Seed-relative cosine is unavailable: `{reference['na_reason']}`. No baseline is inferred."]
    lines += ["", "Pairs share runs; 45 pairs are not 45 independent observations. No pair bootstrap, significance, equivalence, human-calibration or review-cost claim is made.", "",
              "## Completion status", ""]
    for arm in ARMS:
        statuses = summary["arms"][arm]["status_counts"]
        lines.append(f"- {arm}: " + (", ".join(f"{key}={value}" for key, value in statuses.items()) or "no runs"))
    lines += ["", "Ten accepted results do not establish production reliability or a pass^10 probability. Binomial intervals depend on stability and independence assumptions. This tool-free task snapshot does not measure a native agent tool loop or runtime skill enforcement.", "",
              "Complete ledger validation does not establish preregistration timing, model pinning, sandbox enforcement or oracle validity; audit those separately.", "",
              "Per-run AST hashes/counts, every pair, resource missingness and input hashes are in `summary.json`.", ""]
    return "\n".join(lines)


def _atomic_write(path: Path, content: str) -> None:
    handle = tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", dir=path.parent,
                                         prefix=f".{path.name}.", suffix=".tmp", delete=False)
    temporary = Path(handle.name)
    try:
        with handle:
            handle.write(content)
        os.replace(temporary, path)
    finally:
        temporary.unlink(missing_ok=True)


def write_outputs(campaign: Path | str, summary: dict) -> None:
    campaign = Path(campaign)
    _atomic_write(campaign / "summary.json", json.dumps(summary, indent=2, sort_keys=True,
                                                       ensure_ascii=False, allow_nan=False) + "\n")
    _atomic_write(campaign / "report.md", render_report(summary))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("campaign", nargs="?", type=Path)
    parser.add_argument("--campaign", dest="campaign_option", type=Path)
    args = parser.parse_args(argv)
    if (args.campaign is None) == (args.campaign_option is None):
        parser.error("Supply exactly one campaign directory, positionally or with --campaign")
    campaign = args.campaign if args.campaign is not None else args.campaign_option
    try:
        summary = analyze_campaign(campaign)
        write_outputs(campaign, summary)
    except (AnalysisError, OSError) as exc:
        print(f"Analysis refused: {exc}", file=sys.stderr)
        return 2
    print(f"Wrote {campaign / 'summary.json'} and {campaign / 'report.md'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
