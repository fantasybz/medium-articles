#!/usr/bin/env python3
"""Export a verified formal cohort or rescore it with its frozen external oracle.

Usage: python3 archive.py export CAMPAIGN NEW_DIRECTORY
       python3 archive.py rescore CAMPAIGN --output NEW_FILE

The CLI validates the frozen bundle before executing its archive.py. Rescoring
requires the original Python build on macOS and never requires Claude CLI.
Public traces are projections, not raw traces: thinking/signatures and transport
identifiers are omitted. Candidate text remains verbatim. Raw trace hashes are
commitments, not proof that withheld traces had particular contents. A local
manifest hash is an integrity check, not a signed preregistration timestamp.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
import math
import os
from pathlib import Path
import re
import shutil
import sys
import tempfile
import types


class ArchiveError(ValueError):
    """Incomplete, changed, or unsupported evidence; do not publish or rescore."""


def sha(data):
    return hashlib.sha256(data).hexdigest()


def encoded(value):
    return (json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False) + "\n").encode()


def strict_json(data, label):
    def unique(pairs):
        obj = {}
        for key, value in pairs:
            if key in obj:
                raise ArchiveError(f"{label}: duplicate JSON key {key}")
            obj[key] = value
        return obj

    def constant(value):
        raise ArchiveError(f"{label}: non-finite JSON value {value}")

    try:
        return json.loads(data, object_pairs_hook=unique, parse_constant=constant)
    except (ValueError, UnicodeError, RecursionError) as exc:
        raise ArchiveError(f"{label}: invalid JSON: {exc}") from exc


def safe_file(root, name):
    relative = Path(name)
    if (not isinstance(name, str) or not name or relative.is_absolute()
            or any(p in (".", "..") for p in name.split("/"))):
        raise ArchiveError(f"Unsafe relative path: {name!r}")
    path = root
    for part in relative.parts:
        path = path / part
        if path.is_symlink():
            raise ArchiveError(f"Symlink in evidence path: {name}")
    if not path.is_file() or not path.resolve().is_relative_to(root.resolve()):
        raise ArchiveError(f"Missing or non-file evidence: {name}")
    return path


def checked(root, name, expected):
    data = safe_file(root, name).read_bytes()
    if not isinstance(expected, str) or sha(data) != expected:
        raise ArchiveError(f"SHA-256 mismatch: {name}")
    return data


def verify_source(campaign):
    """No frozen Python executes until every declared source byte is checked."""
    data = safe_file(campaign, "manifest.json").read_bytes()
    expected = safe_file(campaign, "manifest.sha256").read_text().strip()
    if sha(data) != expected:
        raise ArchiveError("SHA-256 mismatch: manifest.json")
    # A public archive has an additional immutable ledger covering records and
    # derived results; verify it before any bundled code is loaded.
    if (campaign / "archive.json").exists():
        index_bytes = safe_file(campaign, "archive.json").read_bytes()
        if sha(index_bytes) != safe_file(campaign, "archive.sha256").read_text().strip():
            raise ArchiveError("SHA-256 mismatch: archive.json")
        index = strict_json(index_bytes, "archive.json")
        hashes = index.get("files_sha256") if isinstance(index, dict) else None
        if (not isinstance(hashes, dict) or "records.jsonl" not in hashes
                or {"archive.json", "archive.sha256"} & set(hashes)):
            raise ArchiveError("Invalid or self-referential archive hash inventory")
        for name, digest in hashes.items():
            checked(campaign, name, digest)
    manifest = strict_json(data, "manifest.json")
    if not isinstance(manifest, dict) or manifest.get("phase") != "formal":
        raise ArchiveError("Only a formal campaign can be exported or rescored; pilot is excluded")
    sources = manifest.get("source_sha256")
    required = {"archive.py", "analyze.py", "run_study.py", "evaluator.py", "sandbox.py", "requirements.json"}
    if not isinstance(sources, dict) or not required.issubset(sources):
        raise ArchiveError("Frozen source bundle lacks required archive/oracle files")
    source = campaign / "source"
    if source.is_symlink():
        raise ArchiveError("Frozen source directory must not be a symlink")
    actual = set()
    for path in source.rglob("*"):
        if path.is_symlink():
            raise ArchiveError("Symlink in frozen source bundle")
        if path.is_file() and "__pycache__" not in path.relative_to(source).parts:
            actual.add(path.relative_to(source).as_posix())
    if actual != set(sources):
        raise ArchiveError("Frozen source inventory differs from manifest")
    for name, digest in sources.items():
        checked(source, name, digest)
    if sys.version != manifest.get("python_version") or sys.platform != manifest.get("platform"):
        raise ArchiveError("Original Python build/platform required; refusing a different AST/evaluation runtime")
    if sys.platform != "darwin":
        raise ArchiveError("This archive/evaluation protocol supports macOS only")
    packets = manifest.get("input_packet_sha256")
    if not isinstance(packets, dict) or set(packets) != {"A0", "A", "B", "C"}:
        raise ArchiveError("All four frozen input packets are required")
    for arm, digest in packets.items():
        checked(campaign, f"packets/{arm}.txt", digest)
    checked(campaign, "system.txt", manifest.get("system_input_sha256"))
    schedule = manifest.get("schedule")
    if (not isinstance(schedule, list) or len(schedule) != 40
            or any(not isinstance(row, dict) or row.get("phase") != "formal" for row in schedule)):
        raise ArchiveError("Exactly 40 formal scheduled slots are required")
    for item in schedule:
        if not isinstance(item.get("run_id"), str) or not re.fullmatch(r"[A-Za-z0-9_-]+", item["run_id"]):
            raise ArchiveError("Unsafe scheduled run_id")
    return manifest


def load_frozen(campaign, filename, name):
    """Compile verified source bytes directly; never trust stale bytecode caches."""
    path = safe_file(campaign, "source/" + filename)
    module = types.ModuleType(name)
    module.__file__ = str(path)
    module.__package__ = ""
    sys.modules[name] = module
    exec(compile(path.read_bytes(), str(path), "exec"), module.__dict__)
    return module


def evaluation_outcomes(value, label):
    if not isinstance(value, dict) or type(value.get("passed")) is not bool:
        raise ArchiveError(f"{label}: invalid evaluation envelope")
    cases = value.get("cases")
    if not isinstance(cases, list) or not cases:
        raise ArchiveError(f"{label}: missing case outcomes")
    outcomes = {}
    for case in cases:
        if (not isinstance(case, dict) or not isinstance(case.get("case_id"), str)
                or not case["case_id"] or type(case.get("passed")) is not bool
                or case["case_id"] in outcomes):
            raise ArchiveError(f"{label}: malformed/duplicate case outcome")
        outcomes[case["case_id"]] = case["passed"]
    if (value.get("case_count") != len(outcomes)
            or value.get("passed_count") != sum(outcomes.values())
            or value.get("failed_count") != len(outcomes) - sum(outcomes.values())
            or value["passed"] != all(outcomes.values())):
        raise ArchiveError(f"{label}: inconsistent evaluation totals")
    return outcomes


def verify_campaign(campaign):
    if (campaign / "HALTED.json").exists() or (campaign / "HALTED.json").is_symlink():
        raise ArchiveError("Halted campaigns cannot be published or rescored as a complete formal cohort")
    manifest = verify_source(campaign)
    analyzer = load_frozen(campaign, "analyze.py", "_archive_analyze")
    raw_records = safe_file(campaign, "records.jsonl").read_bytes()
    rows = [strict_json(line, f"records.jsonl:{i}")
            for i, line in enumerate(raw_records.splitlines(), 1) if line.strip()]
    _, rows = analyzer.validate_inputs(manifest, rows)
    summary = analyzer.analyze_campaign(campaign)
    if summary["recorded_runs"] != 40 or summary["other_phase_records_excluded"]:
        raise ArchiveError("Archive must contain exactly the complete 40-slot formal cohort")
    evaluator = load_frozen(campaign, "evaluator.py", "_archive_evaluator")
    expected_cases = {case.case_id for case in evaluator.cases()} | {"streaming-before-eof"}
    originals = {}
    for row in rows:
        run_id = row["run_id"]
        if row["code_path"] is None:
            if (campaign / run_id / "candidate").exists() or (campaign / run_id / "evaluation.json").exists():
                raise ArchiveError(f"{run_id}: unrecorded candidate/evaluation")
            continue
        expected_path = f"{run_id}/candidate/codex_jsonl.py"
        if row["code_path"] != expected_path:
            raise ArchiveError(f"{run_id}: noncanonical candidate path")
        checked(campaign, expected_path, row["artifact_sha256"])
        if {p.name for p in (campaign / run_id / "candidate").iterdir()} != {"codex_jsonl.py"}:
            raise ArchiveError(f"{run_id}: unexpected candidate files")
        seal = strict_json(safe_file(campaign, f"{run_id}/sealed-artifact.json").read_bytes(), run_id + " seal")
        if seal != {"code_path": expected_path, "sha256": row["artifact_sha256"]}:
            raise ArchiveError(f"{run_id}: sealed candidate hash differs from ledger")
        old = strict_json(safe_file(campaign, f"{run_id}/evaluation.json").read_bytes(), run_id + " evaluation")
        outcomes = evaluation_outcomes(old, run_id)
        if (set(outcomes) != expected_cases or old["passed"] != row["artifact_success"]
                or old.get("candidate_sha256") != row["artifact_sha256"]
                or old.get("evaluator_sha256") != manifest["source_sha256"]["evaluator.py"]
                or old.get("requirements_sha256") != manifest["source_sha256"]["requirements.json"]):
            raise ArchiveError(f"{run_id}: original evaluation does not match frozen evidence")
        originals[run_id] = old
    return manifest, rows, summary, analyzer, evaluator, originals


# Explicit usage schema: no arbitrary metadata subtrees or identifiers are copied.
USAGE_KEYS = {
    "input_tokens", "output_tokens", "cache_read_input_tokens", "cache_creation_input_tokens",
    "cache_read_tokens", "cache_write_tokens", "cache_creation_tokens", "thinking_tokens",
    "ephemeral_1h_input_tokens", "ephemeral_5m_input_tokens", "web_search_requests", "web_fetch_requests",
    "inputTokens", "outputTokens", "cacheReadInputTokens", "cacheCreationInputTokens", "thinkingTokens",
    "webSearchRequests", "costUSD", "contextWindow", "maxOutputTokens",
}
USAGE_CONTAINERS = {"cache_creation", "output_tokens_details", "server_tool_use", "iterations"}
USAGE_ENUMS = {"service_tier", "inference_geo", "speed", "type", "canonicalModel", "provider", "costBasis"}


def public_usage(value):
    if isinstance(value, list):
        return [public_usage(item) for item in value if isinstance(item, dict)]
    if not isinstance(value, dict):
        return {}
    result = {}
    for key, item in value.items():
        if key in USAGE_KEYS and type(item) in (int, float) and math.isfinite(item):
            result[key] = item
        elif key in USAGE_CONTAINERS and isinstance(item, (dict, list)):
            result[key] = public_usage(item)
        elif key in USAGE_ENUMS and isinstance(item, str) and re.fullmatch(r"[A-Za-z0-9_.:-]{1,100}", item):
            result[key] = item
    return result


def tool_count(value):
    count, pending = 0, [value]
    while pending:
        item = pending.pop()
        if isinstance(item, dict):
            count += item.get("type") == "tool_use"
            pending.extend(item.values())
        elif isinstance(item, list):
            pending.extend(item)
    return count


def project_trace(raw, expected_model, parse_trace):
    """Whitelist projection, retaining parser evidence without thinking payloads.

    Malformed lines become JSON null (still malformed to parse_trace). Invalid
    UTF-8 is recorded in the sidecar; the valid UTF-8 projection cannot preserve
    that encoding defect. Every other parser decision must remain identical.
    """
    before = parse_trace(raw, expected_model)
    projected = []
    for line in raw.decode("utf-8", errors="replace").splitlines():
        if not line.strip():
            continue
        try:
            event = json.loads(line)
        except (ValueError, RecursionError):
            projected.append(None)
            continue
        if not isinstance(event, dict):
            projected.append(None)
            continue
        event_type = event.get("type")
        out = {"type": event_type if event_type in ("system", "assistant", "result", "error") else "projection_omitted_event"}
        for flag in ("is_error", "isApiErrorMessage"):
            if event.get(flag) is True:
                out[flag] = True
        if event_type == "system" and event.get("subtype") == "init":
            out["subtype"] = "init"
            out["model"] = event.get("model") if isinstance(event.get("model"), str) else None
            for field in ("tools", "mcp_servers", "skills", "slash_commands"):
                value = event.get(field)
                # Empty/nonempty exposure is the exact parser evidence; redact server config.
                out[field] = (["exposed-entry" for _ in value] if value else []) if isinstance(value, list) else None
            for field in ("claude_code_version", "cli_version"):
                if isinstance(event.get(field), str) and re.fullmatch(r"[A-Za-z0-9 ._()+-]{1,100}", event[field]):
                    out[field] = event[field]
        elif event_type == "assistant":
            msg = event.get("message")
            if not isinstance(msg, dict):
                out["message"] = None
            else:
                public = {"model": msg.get("model") if isinstance(msg.get("model"), str) else None}
                if msg.get("is_error") is True or msg.get("error"):
                    public["is_error"] = True
                content = msg.get("content")
                public["content"] = None
                if isinstance(content, list):
                    public["content"] = []
                    for block in content:
                        if not isinstance(block, dict):
                            public["content"].append(None)
                        elif block.get("type") == "text":
                            public["content"].append({"type": "text", "text": block.get("text") if isinstance(block.get("text"), str) else None})
                out["message"] = public
        elif event_type == "result":
            for field in ("subtype", "result"):
                if isinstance(event.get(field), str):
                    out[field] = event[field]
            if type(event.get("is_error")) is bool:
                out["is_error"] = event["is_error"]
            for field in ("total_cost_usd", "duration_ms", "duration_api_ms", "num_turns"):
                if type(event.get(field)) in (int, float) and math.isfinite(event[field]):
                    out[field] = event[field]
            if isinstance(event.get("usage"), dict):
                out["usage"] = public_usage(event["usage"])
            if isinstance(event.get("modelUsage"), dict):
                out["modelUsage"] = {model: public_usage(usage) for model, usage in event["modelUsage"].items()
                                     if re.fullmatch(r"[A-Za-z0-9_.:-]{1,160}", model)}
        count = tool_count(event) - tool_count(out)
        if count < 0:
            raise ArchiveError("Projection introduced tool-use evidence")
        if count:
            out["projection_tool_use_evidence"] = [{"type": "tool_use"} for _ in range(count)]
        projected.append(out)
    data = ("".join(json.dumps(e, ensure_ascii=False, allow_nan=False) + "\n" for e in projected)).encode()
    after = parse_trace(data, expected_model)
    excluded = {"init", "result", "model_usage", "trace_valid", "invalid_utf8"}
    before_observations = {k: v for k, v in before.items() if k not in excluded and k != "candidate_response"}
    after_observations = {k: v for k, v in after.items() if k not in excluded and k != "candidate_response"}
    if before_observations != after_observations or before["candidate_response"] != after["candidate_response"]:
        raise ArchiveError("Projection changed a parser decision; refusing misleading trace evidence")
    for key in ("trace_valid", "invalid_utf8"):
        before_observations[key] = before[key]
        after_observations[key] = after[key]
    metadata = {"format": "parse-trace-whitelist-projection-v1", "is_raw_trace": False,
                "raw_sha256": sha(raw), "projection_sha256": sha(data),
                "original_parser_observations": before_observations,
                "projection_parser_observations": after_observations,
                "redactions": ["thinking/signature blocks", "transport/session/request identifiers",
                               "cwd/socket/auth/config metadata", "exposure entry details", "unlisted metadata"],
                "encoding_note": "Projection is valid UTF-8; original invalid_utf8 and trace_valid are preserved above, not inferred from projection.",
                "text_note": "Assistant text and terminal result text remain verbatim; this is not general-purpose secret removal from generated code."}
    return data, metadata


def new_external_path(campaign, target):
    target = target.expanduser().absolute()
    if target.exists() or target.is_symlink():
        raise ArchiveError("Destination must be new; existing output is never overwritten")
    if target.resolve().is_relative_to(campaign.resolve()):
        raise ArchiveError("Output must be outside the immutable campaign")
    if not target.parent.is_dir():
        raise ArchiveError("Destination parent must already exist")
    return target


def export_campaign(campaign, destination):
    destination = new_external_path(campaign, destination)
    manifest, rows, summary, analyzer, _, _ = verify_campaign(campaign)
    runner = load_frozen(campaign, "run_study.py", "_archive_runner")
    files = {}

    def include(name):
        files[name] = safe_file(campaign, name).read_bytes()

    for name in ("manifest.json", "manifest.sha256", "system.txt", "records.jsonl", "launch-preflight.json"):
        include(name)
    for name in manifest["source_sha256"]:
        include("source/" + name)
    for arm in ("A0", "A", "B", "C"):
        include(f"packets/{arm}.txt")
    report = analyzer.render_report(summary)
    for name, generated in (("summary.json", encoded(summary)), ("report.md", report.encode())):
        original = campaign / name
        if original.exists():
            data = safe_file(campaign, name).read_bytes()
            matches = strict_json(data, name) == summary if name.endswith(".json") else data == generated
            if not matches:
                raise ArchiveError(f"{name}: existing analysis differs from frozen recomputation")
            files[name] = data
        else:
            files[name] = generated
    for name in ("preflight.json", "HALTED.json"):
        if (campaign / name).exists():
            include(name)
    projections = {}
    for row in rows:
        run_id = row["run_id"]
        for name in ("launch.json", "generation.json"):
            relative = f"{run_id}/{name}"
            if (campaign / relative).exists():
                include(relative)
            elif row["status"] != "interrupted":
                raise ArchiveError(f"Missing run evidence: {relative}")
        if row["code_path"] is not None:
            for relative in (row["code_path"], f"{run_id}/evaluation.json", f"{run_id}/sealed-artifact.json"):
                include(relative)
        raw_path = campaign / run_id / "stdout.jsonl"
        if raw_path.exists():
            projection, metadata = project_trace(safe_file(campaign, f"{run_id}/stdout.jsonl").read_bytes(),
                                                 manifest["model"], runner.parse_trace)
            files[f"{run_id}/trace-public.jsonl"] = projection
            files[f"{run_id}/trace-projection.json"] = encoded(metadata)
            projections[run_id] = metadata
        elif row["status"] == "interrupted":
            projections[run_id] = {"status": "raw_trace_absent_for_interrupted_slot"}
        else:
            raise ArchiveError(f"{run_id}: missing private raw trace")
    # Reverify inputs after reading every artifact and before creating public output.
    verify_campaign(campaign)
    index = {"format": "same-spec-ten-runs-public-archive-v1", "phase": "formal", "slots": 40,
             "created_at_utc": datetime.now(timezone.utc).isoformat(),
             "manifest_sha256": sha(files["manifest.json"]), "records_sha256": sha(files["records.jsonl"]),
             "python_version": sys.version, "platform": sys.platform,
             "files_sha256": {name: sha(data) for name, data in sorted(files.items())},
             "trace_projections": projections,
             "omitted_private_files": ["stdout.jsonl", "stderr.txt", "trace-audit.json"],
             "hash_scope": "files_sha256 excludes archive.json and archive.sha256; archive.sha256 hashes archive.json only.",
             "raw_trace_notice": "Only a redacted projection is public. Original raw traces remain in the private campaign."}
    staging = Path(tempfile.mkdtemp(prefix=".archive-stage-", dir=destination.parent))
    try:
        for name, data in files.items():
            path = staging / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(data)
        index_bytes = encoded(index)
        (staging / "archive.json").write_bytes(index_bytes)
        (staging / "archive.sha256").write_text(sha(index_bytes) + "\n")
        # mkdir reserves the new destination atomically; do not replace another directory.
        destination.mkdir()
        try:
            for child in staging.iterdir():
                shutil.move(str(child), str(destination / child.name))
        except BaseException:
            shutil.rmtree(destination)
            raise
    finally:
        shutil.rmtree(staging)
    return index


def rescore_campaign(campaign, output):
    output = new_external_path(campaign, output)
    manifest, rows, _, _, evaluator, originals = verify_campaign(campaign)
    sandbox = load_frozen(campaign, "sandbox.py", "sandbox")
    preflight = sandbox.preflight()
    if (preflight.get("sandbox") != "macos-seatbelt-v1"
            or any(preflight.get(k) is not True for k in ("read_denied", "write_denied", "network_denied"))):
        raise ArchiveError("Real sandbox preflight did not verify all three boundaries")
    results = []
    for row in rows:
        run_id = row["run_id"]
        if row["code_path"] is None:
            results.append({"run_id": run_id, "status": "no_candidate", "original_status": row["status"],
                            "original_artifact_success": row["artifact_success"], "matches_original": None})
            continue
        checked(campaign, row["code_path"], row["artifact_sha256"])
        fresh = evaluator.evaluate((campaign / row["code_path"]).parent)
        outcomes = evaluation_outcomes(fresh, run_id + " rescore")
        old = originals[run_id]
        old_outcomes = evaluation_outcomes(old, run_id + " original")
        if (fresh.get("candidate_sha256") != row["artifact_sha256"]
                or fresh.get("evaluator_sha256") != manifest["source_sha256"]["evaluator.py"]
                or fresh.get("requirements_sha256") != manifest["source_sha256"]["requirements.json"]):
            raise ArchiveError(f"{run_id}: rescoring provenance changed")
        matches = fresh["passed"] == old["passed"] and outcomes == old_outcomes
        results.append({"run_id": run_id, "status": "rescored", "matches_original": matches,
                        "original_passed": old["passed"], "rescored_passed": fresh["passed"],
                        "case_outcome_changes": [case for case in sorted(set(old_outcomes) | set(outcomes))
                                                 if old_outcomes.get(case) != outcomes.get(case)],
                        "evaluation": fresh})
    verify_campaign(campaign)
    result = {"format": "same-spec-ten-runs-rescore-v1", "phase": "formal", "slots": 40,
              "manifest_sha256": sha(safe_file(campaign, "manifest.json").read_bytes()),
              "records_sha256": sha(safe_file(campaign, "records.jsonl").read_bytes()),
              "python_version": sys.version, "platform": sys.platform,
              "sandbox_preflight": preflight, "completed_at_utc": datetime.now(timezone.utc).isoformat(),
              "rescored_candidates": sum(row["status"] == "rescored" for row in results),
              "all_available_candidates_match": all(row["matches_original"] is not False for row in results),
              "runs": results}
    # A trusted exception above leaves no apparently completed report behind.
    with output.open("xb") as stream:
        stream.write(encoded(result))
    return result


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    export = commands.add_parser("export")
    export.add_argument("campaign", type=Path)
    export.add_argument("destination", type=Path)
    rescore = commands.add_parser("rescore")
    rescore.add_argument("campaign", type=Path)
    rescore.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)
    campaign = args.campaign.expanduser().resolve()
    try:
        verify_source(campaign)
        frozen = safe_file(campaign, "source/archive.py")
        if Path(__file__).resolve() != frozen.resolve():
            tail = ["export", str(campaign), str(args.destination.expanduser().absolute())] if args.command == "export" else ["rescore", str(campaign), "--output", str(args.output.expanduser().absolute())]
            os.execv(sys.executable, [sys.executable, "-B", str(frozen), *tail])
        sys.dont_write_bytecode = True
        result = export_campaign(campaign, args.destination) if args.command == "export" else rescore_campaign(campaign, args.output)
        print(json.dumps({"command": args.command, "slots": result["slots"], "status": "complete"}))
        return 1 if result.get("all_available_candidates_match") is False else 0
    except Exception as exc:
        print(f"Archive refused: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
