"""External oracle for the real repository codex_jsonl.py maintenance task.

The candidate receives public R01--R13 but not these exact cases or expected
outputs. Cases introduce no extra requirements. Only the verified OS sandbox
executes candidates; candidate tests are never discovered or run. Synthetic
reference/mutation fixtures validate the apparatus, not a human baseline.
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass
import hashlib
import json
from pathlib import Path
import re
import sys
import time
from typing import Any

HERE = Path(__file__).resolve().parent
VERIFIED_SANDBOX = "macos-seatbelt-v1"
SCRIPT_NAME = "codex_jsonl.py"
FAILED_SUMMARY = "[codex] the turn failed (reason above); no review was produced.\n"
DISCONNECT_SUMMARY = "[codex] no turn.completed event: possible mid-stream disconnect.\n"
SILENT_SUMMARY = "[codex] the turn completed without an agent message; no review was produced.\n"
TOKENS = "\n<!-- tokens: in 10 out 5 -->\n"
DONE = {"type": "turn.completed", "usage": {"input_tokens": 10, "output_tokens": 5}}


class EvaluationUnavailable(RuntimeError):
    """No verified boundary; fail closed without running a candidate."""


class CandidateLayoutError(ValueError):
    pass


@dataclass(frozen=True)
class Malformed:
    line: int


@dataclass(frozen=True)
class Case:
    case_id: str
    requirements: tuple[str, ...]
    input_text: str
    returncode: int
    stdout: str
    stderr: tuple[str | Malformed, ...] = ()
    group: str = "hardening"
    c_locale: bool = False


def jsonl(*events: Any) -> str:
    return "".join(json.dumps(event, ensure_ascii=False) + "\n" for event in events)


def message(text: Any) -> dict:
    return {"type": "item.completed", "item": {"type": "agent_message", "text": text}}


def item(kind: str, **fields: Any) -> dict:
    return {"type": "item.completed", "item": {"type": kind, **fields}}


def cases() -> tuple[Case, ...]:
    """Hand-specified expected behavior, independent of all candidate code."""
    rows: list[Case] = []

    def add(name, reqs, text, code, out, err=(), *, group="hardening", c_locale=False):
        rows.append(Case(name, tuple(reqs), text, code, out, tuple(err), group, c_locale))

    # All eleven existing TestCodexJsonl methods and their distinct branches.
    add("legacy-multiple-messages", ("R01", "R05", "R08"),
        jsonl(message("first"), message("second"), DONE), 0, "first\nsecond\n" + TOKENS, group="legacy")
    add("legacy-cjk-c-locale", ("R01", "R05"),
        jsonl(message("審查：沒問題"), DONE), 0, "審查：沒問題\n" + TOKENS,
        group="legacy", c_locale=True)
    command = "grep -rn " + "x" * 200
    add("legacy-command-truncation", ("R06",),
        jsonl(item("command_execution", command=command), message("ok"), DONE), 0,
        "<!-- codex ran: " + command[:160] + " -->\nok\n" + TOKENS, group="legacy")
    add("legacy-ignored-lines-and-types", ("R02", "R04", "R05", "R06", "R13"),
        "\n\nnot json\n{}\n" + jsonl(
            {"type": "item.started", "item": {"type": "agent_message", "text": "partial"}},
            item("agent_message"), item("reasoning", text="hidden"), item("command_execution"),
            message("ok"), DONE), 0, "ok\n" + TOKENS, group="legacy")
    add("legacy-missing-usage", ("R08",),
        jsonl(message("ok"), {"type": "turn.completed"}), 0,
        "ok\n\n<!-- tokens: in 0 out 0 -->\n", group="legacy")
    add("legacy-item-error", ("R07", "R11"),
        jsonl(item("error", message="tool blew up"), message("ok"), DONE), 0,
        "ok\n" + TOKENS, ("[codex item error] tool blew up\n",), group="legacy")
    add("legacy-turn-failed", ("R10", "R11", "R12"),
        jsonl(message("partial"), {"type": "turn.failed", "error": {"message": "usage limit reached"}}),
        3, "partial\n", ("[codex turn FAILED] usage limit reached\n", FAILED_SUMMARY), group="legacy")
    add("legacy-turn-failed-missing", ("R10", "R11", "R12"),
        jsonl({"type": "turn.failed"}), 3, "", ("[codex turn FAILED] no message\n", FAILED_SUMMARY), group="legacy")
    add("legacy-error-before-completion", ("R09", "R11", "R12"),
        jsonl({"type": "error", "message": "refused"}, message("ok"), DONE), 3,
        "ok\n" + TOKENS, ("[codex error] refused\n", FAILED_SUMMARY), group="legacy")
    add("legacy-missing-completion", ("R11", "R12"),
        jsonl(message("looks complete")), 4, "looks complete\n", (DISCONNECT_SUMMARY,), group="legacy")
    add("legacy-empty-input", ("R11", "R12"), "", 4, "", (DISCONNECT_SUMMARY,), group="legacy")
    add("legacy-completed-silent", ("R08", "R11", "R12"),
        jsonl(DONE), 5, TOKENS, (SILENT_SUMMARY,), group="legacy")
    add("legacy-command-is-not-speech", ("R06", "R11", "R12"),
        jsonl(item("command_execution", command="ls"), DONE), 5,
        "<!-- codex ran: ls -->\n" + TOKENS, (SILENT_SUMMARY,), group="legacy")
    add("legacy-empty-text-is-not-speech", ("R05", "R11", "R12"),
        jsonl(message(""), DONE), 5, TOKENS, (SILENT_SUMMARY,), group="legacy")
    add("legacy-error-outranks-silence", ("R09", "R11", "R12"),
        jsonl({"type": "error", "message": "refused"}, DONE), 3,
        TOKENS, ("[codex error] refused\n", FAILED_SUMMARY), group="legacy")
    add("legacy-incomplete-command", ("R06", "R11", "R12"),
        jsonl(item("command_execution", command="ls")), 4,
        "<!-- codex ran: ls -->\n", (DISCONNECT_SUMMARY,), group="legacy")

    # Compatibility edge cases explicitly enumerated in the public contract.
    add("compat-duplicate-messages-and-completions", ("R05", "R08", "R13"),
        jsonl(message("same"), DONE, message("same"), DONE), 0,
        "same\n" + TOKENS + "same\n" + TOKENS)
    add("compat-error-after-completion", ("R09", "R11", "R13"),
        jsonl(message("ok"), DONE, {"type": "error", "message": "late"}), 3,
        "ok\n" + TOKENS, ("[codex error] late\n", FAILED_SUMMARY))
    add("compat-whitespace-text", ("R05",), jsonl(message(" \t "), DONE), 0, " \t \n" + TOKENS)
    add("compat-embedded-newline", ("R05",), jsonl(message("a\nb"), DONE), 0, "a\nb\n" + TOKENS)
    add("compat-unicode-command-characters", ("R01", "R06"),
        jsonl(item("command_execution", command="檢" * 170), message("ok"), DONE), 0,
        "<!-- codex ran: " + "檢" * 160 + " -->\nok\n" + TOKENS)
    add("compat-unknown-payloads-not-inspected", ("R02", "R04", "R13"),
        jsonl({"type": "future.event", "usage": None, "item": 123},
              item("future_item", text=123, command=[], message=False),
              {"unrelated": None}, {"type": "item.completed"},
              {"type": "item.completed", "item": {}}, message("ok"), DONE),
        0, "ok\n" + TOKENS)
    add("compat-extra-fields", ("R01", "R13"),
        jsonl({"type": "item.completed", "extra": [], "item": {
            "type": "agent_message", "text": "ok", "extra": None}},
            {"type": "turn.completed", "usage": {"input_tokens": 1, "extra": []}, "extra": False}),
        0, "ok\n\n<!-- tokens: in 1 out 0 -->\n")
    add("compat-optional-null-empty", ("R04", "R05", "R06", "R07", "R08"),
        jsonl(message(None), item("command_execution", command=None),
              item("command_execution", command=""), item("error"),
              item("error", message=None), item("error", message=""),
              message("ok"), {"type": "turn.completed", "usage": {"output_tokens": 7}}),
        0, "ok\n\n<!-- tokens: in 0 out 7 -->\n")
    for label, value in [("null", None), ("empty-object", {}), ("null-message", {"message": None}),
                         ("empty-message", {"message": ""})]:
        add("compat-turn-failed-" + label, ("R10", "R11", "R12"),
            jsonl({"type": "turn.failed", "error": value}), 3, "",
            ("[codex turn FAILED] no message\n", FAILED_SUMMARY))
    for label, value in [("null", None), ("number", 123), ("list", []), ("object", {"detail": 2}), ("bool", False)]:
        add("compat-top-error-converts-" + label, ("R09", "R11", "R12"),
            jsonl({"type": "error", "message": value}, message("ok"), DONE), 3,
            "ok\n" + TOKENS, ("[codex error] " + str(value) + "\n", FAILED_SUMMARY))
    add("compat-top-error-missing-message", ("R09", "R11"),
        jsonl({"type": "error"}), 3, "", ("[codex error] \n", FAILED_SUMMARY))

    # Malformed lines must not prevent the following valid review from streaming.
    wrong_values = [("null", None), ("list", []), ("number", 123),
                    ("string", "decoded string"), ("bool", False)]
    for label, value in wrong_values:
        add("wrong-root-" + label, ("R02", "R03", "R11"),
            jsonl(value, message("after"), DONE), 6, "after\n" + TOKENS, (Malformed(1),))
    for label, value in [("null", None), ("number", 123), ("list", []), ("bool", False)]:
        add("wrong-event-type-" + label, ("R02", "R03"),
            jsonl({"type": value}, message("after"), DONE), 6, "after\n" + TOKENS, (Malformed(1),))
    for label, value in wrong_values:
        add("wrong-item-envelope-" + label, ("R03", "R04"),
            jsonl({"type": "item.completed", "item": value}, message("after"), DONE),
            6, "after\n" + TOKENS, (Malformed(1),))
    for label, value in [("null", None), ("number", 123), ("list", []), ("bool", False)]:
        add("wrong-item-type-" + label, ("R03", "R04"),
            jsonl({"type": "item.completed", "item": {"type": value}}, message("after"), DONE),
            6, "after\n" + TOKENS, (Malformed(1),))
    wrong_text_values = [("number", 123), ("zero", 0), ("bool", False), ("list", []), ("object", {})]
    for kind, field, rid in [("agent_message", "text", "R05"),
                             ("command_execution", "command", "R06"), ("error", "message", "R07")]:
        for label, value in wrong_text_values:
            add("wrong-" + kind + "-" + label, ("R03", rid),
                jsonl(item(kind, **{field: value}), message("after"), DONE),
                6, "after\n" + TOKENS, (Malformed(1),))
    for label, value in wrong_values:
        add("wrong-usage-" + label, ("R03", "R08"),
            jsonl(message("before"), {"type": "turn.completed", "usage": value}, message("after")),
            6, "before\nafter\n", (Malformed(2),))
    invalid_tokens = [("null", None), ("negative", -1), ("bool", True), ("float", 1.0),
                      ("string", "1"), ("list", []), ("object", {})]
    for field in ("input_tokens", "output_tokens"):
        for label, value in invalid_tokens:
            add("wrong-" + field + "-" + label, ("R03", "R08"),
                jsonl(message("ok"), {"type": "turn.completed", "usage": {field: value}}),
                6, "ok\n", (Malformed(2),))
    add("wrong-both-token-fields-one-diagnostic", ("R03", "R08"),
        jsonl({"type": "turn.completed", "usage": {"input_tokens": True, "output_tokens": None}}),
        6, "", (Malformed(1),))
    add("valid-zero-and-large-tokens", ("R08",),
        jsonl(message("ok"), {"type": "turn.completed", "usage": {"input_tokens": 0, "output_tokens": 10**30}}),
        0, "ok\n\n<!-- tokens: in 0 out 1000000000000000000000000000000 -->\n")
    for label, value in [("number", 123), ("false", False), ("list", []), ("string", "bad")]:
        add("wrong-failed-error-envelope-" + label, ("R03", "R10", "R11"),
            jsonl({"type": "turn.failed", "error": value}, message("after"), DONE),
            3, "after\n" + TOKENS, (Malformed(1), "[codex turn FAILED] no message\n", FAILED_SUMMARY))
    for label, value in wrong_text_values:
        add("wrong-failed-message-" + label, ("R03", "R10", "R11"),
            jsonl({"type": "turn.failed", "error": {"message": value}}),
            3, "", (Malformed(1), "[codex turn FAILED] no message\n", FAILED_SUMMARY))
    add("physical-line-numbers-and-continuation", ("R02", "R03", "R11"),
        "\nnot json\n" + jsonl([], message("kept"), {"type": "item.completed", "item": None}, DONE),
        6, "kept\n" + TOKENS, (Malformed(3), Malformed(5)))
    add("malformed-outranks-disconnect", ("R03", "R11"), jsonl([]), 6, "", (Malformed(1),))
    add("malformed-outranks-silence", ("R03", "R11"), jsonl([], DONE), 6, TOKENS, (Malformed(1),))
    add("later-error-outranks-malformed", ("R03", "R09", "R11", "R12"),
        jsonl([], {"type": "error", "message": "refused"}, message("after"), DONE),
        3, "after\n" + TOKENS, (Malformed(1), "[codex error] refused\n", FAILED_SUMMARY))
    add("earlier-error-outranks-malformed", ("R03", "R09", "R11", "R12"),
        jsonl({"type": "error", "message": "refused"}, [], message("after"), DONE),
        3, "after\n" + TOKENS, ("[codex error] refused\n", Malformed(2), FAILED_SUMMARY))
    assert len(rows) == len({row.case_id for row in rows})
    return tuple(rows)


def stderr_matches(actual: str, expected: tuple[str | Malformed, ...]) -> bool:
    parts = []
    for fragment in expected:
        if isinstance(fragment, Malformed):
            parts.append(re.escape(f"[codex malformed event] line {fragment.line}: ") + r"[^\r\n]+\n")
        else:
            parts.append(re.escape(fragment))
    return re.fullmatch("".join(parts), actual) is not None


def expected_stderr_description(expected) -> str:
    return "".join(f"[codex malformed event] line {part.line}: <nonempty reason>\n"
                   if isinstance(part, Malformed) else part for part in expected)


def _check_candidate_layout(candidate_dir: Path) -> Path:
    root = Path(candidate_dir)
    if root.is_symlink() or not root.is_dir():
        raise CandidateLayoutError("Candidate must be a real directory")
    entries = list(root.iterdir())
    if len(entries) != 1 or entries[0].name != SCRIPT_NAME:
        raise CandidateLayoutError("Candidate must contain only codex_jsonl.py, no tests or helpers")
    if entries[0].is_symlink() or not entries[0].is_file():
        raise CandidateLayoutError("codex_jsonl.py must be a regular file, not a symlink")
    return entries[0].resolve()


def _boundary():
    try:
        import sandbox
    except ImportError as exc:
        raise EvaluationUnavailable("Trusted sandbox helper is unavailable; no candidate executed") from exc
    try:
        verified = sandbox.preflight()
    except sandbox.SandboxUnavailable as exc:
        raise EvaluationUnavailable(str(exc)) from exc
    if (verified.get("sandbox") != VERIFIED_SANDBOX or
            any(verified.get(k) is not True for k in ("read_denied", "write_denied", "network_denied"))):
        raise EvaluationUnavailable("Sandbox isolation evidence is missing or unrecognized")
    return sandbox, verified


def _grade(case: Case, run: Any, *, max_output_bytes: int) -> dict:
    if run.sandbox != VERIFIED_SANDBOX:
        raise EvaluationUnavailable("Execution did not identify the verified sandbox")
    record = {"case_id": case.case_id, "requirements": list(case.requirements),
              "group": case.group, "passed": False, "returncode": run.returncode,
              "sandbox": run.sandbox, "c_locale": case.c_locale}
    if run.timed_out:
        record["failure"] = "timeout"
    elif len(run.stdout.encode()) > max_output_bytes or len(run.stderr.encode()) > max_output_bytes:
        record["failure"] = "output_limit"
    else:
        failures = []
        if run.returncode != case.returncode:
            failures.append("returncode")
        if run.stdout != case.stdout:
            failures.append("stdout")
        if not stderr_matches(run.stderr, case.stderr):
            failures.append("stderr")
        record["passed"] = not failures
        if failures:
            record.update(failure="mismatch", mismatches=failures,
                          actual_stdout=run.stdout, actual_stderr=run.stderr,
                          expected_returncode=case.returncode, expected_stdout=case.stdout,
                          expected_stderr=expected_stderr_description(case.stderr))
    return record


def _run_case(case: Case, candidate_dir: Path, boundary: Any, *,
              timeout_seconds: float, max_output_bytes: int) -> dict:
    kwargs = {"timeout_seconds": timeout_seconds, "max_output_bytes": max_output_bytes,
              "script_name": SCRIPT_NAME}
    if case.c_locale:
        kwargs["c_locale"] = True
    started = time.monotonic()
    run = boundary.run_candidate(candidate_dir, case.input_text, **kwargs)
    record = _grade(case, run, max_output_bytes=max_output_bytes)
    record["duration_seconds"] = round(time.monotonic() - started, 6)
    return record


def _streaming_case(candidate_dir: Path, boundary: Any, timeout_seconds: float) -> dict:
    probe = boundary.run_streaming_probe(candidate_dir, jsonl(message("stream-before-eof")),
                                         jsonl(DONE), "stream-before-eof\n",
                                         timeout_seconds=timeout_seconds)
    if probe.get("sandbox") != VERIFIED_SANDBOX:
        raise EvaluationUnavailable("Streaming probe did not use the verified sandbox")
    passed = (probe.get("passed") is True and probe.get("observed_before_eof") is True
              and probe.get("returncode") == 0 and probe.get("early_stdout") == "stream-before-eof\n")
    return {"case_id": "streaming-before-eof", "requirements": ["R01"], "group": "streaming",
            **probe, "passed": passed}


def evaluate(candidate_dir: Path, *, timeout_seconds: float = 3.0,
             max_output_bytes: int = 65536) -> dict:
    """Fail-closed external evaluation; no agent-supplied test code is executed."""
    if timeout_seconds <= 0 or max_output_bytes <= 0:
        raise ValueError("Positive timeout and output bounds required")
    candidate = _check_candidate_layout(candidate_dir)
    candidate_sha = hashlib.sha256(candidate.read_bytes()).hexdigest()
    boundary, verified = _boundary()
    all_cases = cases()
    try:
        records = [_run_case(case, candidate.parent, boundary, timeout_seconds=timeout_seconds,
                             max_output_bytes=max_output_bytes) for case in all_cases]
        records.append(_streaming_case(candidate.parent, boundary, timeout_seconds))
    except boundary.SandboxUnavailable as exc:
        raise EvaluationUnavailable(str(exc)) from exc
    if hashlib.sha256(candidate.read_bytes()).hexdigest() != candidate_sha:
        raise EvaluationUnavailable("Candidate changed during evaluation; discard the measurements")
    failed = [record for record in records if not record["passed"]]
    coverage = {}
    for record in records:
        for rid in record["requirements"]:
            coverage.setdefault(rid, []).append(record["case_id"])
    return {"schema_version": 1, "task_id": "codex-jsonl-type-safety-v1",
            "candidate_sha256": candidate_sha,
            "evaluator_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            "requirements_sha256": hashlib.sha256((HERE / "requirements.json").read_bytes()).hexdigest(),
            "sandbox": verified, "case_count": len(records),
            "passed_count": len(records) - len(failed), "failed_count": len(failed),
            "passed": not failed, "all_passed": not failed,
            "failed_requirements": sorted({rid for row in failed for rid in row["requirements"]}),
            "requirement_coverage": coverage, "cases": records}


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--candidate", type=Path, required=True)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--timeout-seconds", type=float, default=3.0)
    parser.add_argument("--max-output-bytes", type=int, default=65536)
    args = parser.parse_args(argv)
    if args.output is not None and args.output.resolve().is_relative_to(args.candidate.resolve()):
        parser.error("The report must stay outside the candidate directory")
    try:
        result = evaluate(args.candidate, timeout_seconds=args.timeout_seconds,
                          max_output_bytes=args.max_output_bytes)
    except (CandidateLayoutError, EvaluationUnavailable, ValueError) as exc:
        print(json.dumps({"status": "evaluation_unavailable", "error": str(exc)}), file=sys.stderr)
        return 2
    rendered = json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False) + "\n"
    if args.output is None:
        sys.stdout.write(rendered)
    else:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered)
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
