#!/usr/bin/env python3
"""Freeze, run and audit a tool-free coding experiment. Python stdlib only."""
import argparse
from datetime import datetime, timezone
import fcntl
import hashlib
import json
import os
from pathlib import Path
import random
import shutil
import signal
import subprocess
import sys
import tempfile
import time

ROOT = Path(__file__).resolve().parent
ARMS = ("A0", "A", "B", "C")
NONSECRET_ENV_CONTROLS = ("CLAUDE_CODE_MAX_OUTPUT_TOKENS", "MAX_THINKING_TOKENS")
SYSTEM = ("You implement a Python program from the supplied repository snapshot and specification. "
          "You have no tools or external files. Return exactly one JSON object with exactly one key "
          "codex_jsonl.py whose value is the complete UTF-8 source code. No markdown fences or commentary.")


def sha(data):
    return hashlib.sha256(data).hexdigest()


def now():
    return datetime.now(timezone.utc).isoformat()


def write_json(path, value):
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False, allow_nan=False) + "\n")


def packet(arm, root=None):
    root = ROOT if root is None else root
    if arm not in ARMS:
        raise ValueError("Unknown arm")
    return ("Implement the supplied task. The implementation must satisfy every stated requirement.\n\n"
            "Repository: medium-articles. Target: research/scripts/codex_jsonl.py.\n"
            "<seed path=\"research/scripts/codex_jsonl.py\">\n" + (root / "seed/codex_jsonl.py").read_text() + "\n</seed>\n\n"
            "<specification>\n" + (root / f"specs/{arm}.md").read_text() + "\n</specification>\n\n"
            "Return {\"codex_jsonl.py\": \"complete Python source\"}. The evaluator is external; "
            "you cannot run tests or revise after receiving feedback.")


def inputs():
    paths = sorted(p for p in ROOT.rglob("*") if p.is_file()
                   and ".git" not in p.parts and "__pycache__" not in p.parts
                   and p.relative_to(ROOT).parts[0] != "results"
                   and p.suffix in (".py", ".md", ".json", ".txt"))
    return {str(p.relative_to(ROOT)): sha(p.read_bytes()) for p in paths}


def environment_controls():
    values = {"DISABLE_AUTOUPDATER": "1"}
    for name in NONSECRET_ENV_CONTROLS:
        if name in os.environ:
            value = os.environ[name]
            if not value.isascii() or not value.isdigit():
                raise ValueError(f"{name} must be a numeric token limit before freezing")
            values[name] = value
    controls = {"values": values,
                "anthropic_variable_names": sorted(name for name in os.environ if name.startswith("ANTHROPIC_")),
                "unobserved_context": "Other environment values and provider/CLI context are inherited, not recorded or fully pinned. ANTHROPIC_* values are never stored."}
    controls["sha256"] = sha(json.dumps(controls, sort_keys=True, separators=(",", ":")).encode())
    return controls


def generation_environment(controls):
    env = os.environ.copy()
    for name in NONSECRET_ENV_CONTROLS:
        env.pop(name, None)
    env.update(controls["values"])
    env["DISABLE_AUTOUPDATER"] = "1"
    return env


def freeze(destination, phase, model, effort, workers, timeout, budget):
    from sandbox import preflight
    if destination.is_relative_to(ROOT):
        raise ValueError("Campaigns must be outside the frozen source directory")
    if destination.exists():
        raise ValueError("Campaign directory already exists; a freeze is immutable")
    isolation = preflight()
    controls = environment_controls()
    invocation = cli_args(model, effort, budget)
    executable = invocation[0]
    version = subprocess.check_output([executable, "--version"], text=True, timeout=10,
                                      env=generation_environment(controls)).strip()
    provenance = json.loads((ROOT / "task.json").read_text())
    if sha((ROOT / "seed/codex_jsonl.py").read_bytes()) != provenance["seed_sha256"]:
        raise ValueError("Seed differs from recorded repository provenance")
    source_hashes = inputs()
    schedule = []
    rng = random.Random(20260925)
    for block in range(1, 11 if phase == "formal" else 2):
        arms = list(ARMS) if phase == "formal" else ["A0", "C"]
        rng.shuffle(arms)
        for arm in arms:
            schedule.append({"run_id": f"{phase}-{block:02d}-{arm}", "arm": arm, "block": block, "phase": phase})
    destination.mkdir(parents=True)
    frozen_source = destination / "source"
    for name, digest in source_hashes.items():
        data = (ROOT / name).read_bytes()
        if sha(data) != digest:
            raise ValueError("Source changed while freezing")
        target = frozen_source / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
    (destination / "packets").mkdir()
    packet_hashes = {}
    for arm in ARMS:
        data = packet(arm, frozen_source).encode()
        (destination / f"packets/{arm}.txt").write_bytes(data)
        packet_hashes[arm] = sha(data)
    (destination / "system.txt").write_text(SYSTEM)
    manifest = {"schema": 1, "phase": phase, "frozen_at_utc": now(), "schedule_seed": 20260925,
                "schedule": schedule, "model": model, "effort": effort, "workers": workers,
                "timeout_seconds": timeout, "max_budget_usd": budget, "cli_version": version,
                "cli_binary_sha256": sha(Path(executable).read_bytes()),
                "environment_controls": controls,
                "python_version": sys.version, "platform": sys.platform,
                "input_packet_sha256": packet_hashes, "system_input_sha256": sha(SYSTEM.encode()),
                "source_sha256": source_hashes, "isolation_preflight": isolation,
                "task_provenance": provenance,
                "primary_endpoint": "accepted_completion", "invocation": invocation}
    write_json(destination / "manifest.json", manifest)
    (destination / "manifest.sha256").write_text(sha((destination / "manifest.json").read_bytes()) + "\n")
    return manifest


def cli_args(model, effort, budget, executable=None):
    if executable is None:
        executable = shutil.which("claude")
        if executable is None:
            raise ValueError("Claude CLI is unavailable")
        executable = str(Path(executable).resolve())
    elif not Path(executable).is_absolute():
        raise ValueError("Frozen CLI executable must be absolute")
    executable = str(executable)
    return [executable, "-p", "--model", model, "--effort", effort,
            "--output-format", "stream-json", "--verbose", "--tools", "",
            "--disable-slash-commands", "--safe-mode", "--strict-mcp-config", "--setting-sources", "",
            "--no-chrome", "--no-session-persistence", "--permission-mode", "dontAsk",
            "--system-prompt", SYSTEM, "--max-budget-usd", str(budget)]


def verify(destination, check_cli=True):
    data = (destination / "manifest.json").read_bytes()
    if sha(data) != (destination / "manifest.sha256").read_text().strip():
        raise ValueError("Manifest changed after freeze")
    manifest = json.loads(data)
    if inputs() != manifest["source_sha256"]:
        raise ValueError("Source changed after freeze; create a new campaign, never amend a running one")
    for arm, expected in manifest["input_packet_sha256"].items():
        if sha((destination / f"packets/{arm}.txt").read_bytes()) != expected:
            raise ValueError("Packet changed after freeze")
    if sha((destination / "system.txt").read_bytes()) != manifest["system_input_sha256"]:
        raise ValueError("System input changed after freeze")
    executable = manifest["invocation"][0]
    if not Path(executable).is_absolute():
        raise ValueError("Frozen CLI executable must be absolute")
    if manifest["invocation"] != cli_args(manifest["model"], manifest["effort"], manifest["max_budget_usd"], executable=executable):
        raise ValueError("Invocation differs from frozen executable policy")
    controls = manifest["environment_controls"]
    public_controls = {key: value for key, value in controls.items() if key != "sha256"}
    if sha(json.dumps(public_controls, sort_keys=True, separators=(",", ":")).encode()) != controls["sha256"]:
        raise ValueError("Recorded environment controls hash is invalid")
    if (controls.get("values", {}).get("DISABLE_AUTOUPDATER") != "1"
            or set(controls["values"]) - {"DISABLE_AUTOUPDATER", *NONSECRET_ENV_CONTROLS}):
        raise ValueError("Environment controls differ from the frozen policy")
    if check_cli:
        if sha(Path(executable).read_bytes()) != manifest["cli_binary_sha256"]:
            raise ValueError("CLI binary changed after freeze")
        if subprocess.check_output([executable, "--version"], text=True, timeout=10,
                                   env=generation_environment(controls)).strip() != manifest["cli_version"]:
            raise ValueError("CLI version changed after freeze")
        if sorted(name for name in os.environ if name.startswith("ANTHROPIC_")) != controls["anthropic_variable_names"]:
            raise ValueError("ANTHROPIC environment variable names changed after freeze; values remain unrecorded")
    if sys.version != manifest["python_version"] or sys.platform != manifest["platform"]:
        raise ValueError("Evaluation runtime changed after freeze")
    return manifest


def parse_trace(raw, expected_model):
    invalid_utf8 = False
    if isinstance(raw, bytes):
        try:
            raw.decode("utf-8")
        except UnicodeDecodeError:
            invalid_utf8 = True
        raw = raw.decode("utf-8", errors="replace")
    events = []
    malformed_lines = 0
    malformed_fields = 0
    for line in raw.splitlines():
        if line.strip():
            try:
                event = json.loads(line)
                if not isinstance(event, dict):
                    raise ValueError("Event must be an object")
                events.append(event)
            except (ValueError, RecursionError):
                malformed_lines += 1
    init = [e for e in events if e.get("type") == "system" and e.get("subtype") == "init"]
    results = [e for e in events if e.get("type") == "result"]
    violations = []
    exposed_fields = ("tools", "mcp_servers", "skills", "slash_commands")
    for event in init:
        for field in exposed_fields:
            value = event.get(field)
            if isinstance(value, list) and value:
                violations.append("exposed_" + field)
            elif not isinstance(value, list):
                malformed_fields += 1
        model = event.get("model")
        if isinstance(model, str) and model and model not in (expected_model, "<synthetic>"):
            violations.append("different_init_model:" + model)
    # Inspect nested dictionaries even when a malformed message/content envelope
    # surrounds a real tool call; malformed tails cannot erase observed evidence.
    tool_call_count = 0
    pending = list(events)
    while pending:
        value = pending.pop()
        if isinstance(value, dict):
            tool_call_count += value.get("type") == "tool_use"
            pending.extend(value.values())
        elif isinstance(value, list):
            pending.extend(value)
    if tool_call_count:
        violations.append("observed_tool_use")
    generated = set()
    assistant_count = 0
    unknown_model_messages = 0
    synthetic_messages = 0
    operational_error = any(e.get("type") == "error" or e.get("is_error") is True
                            or e.get("isApiErrorMessage") is True for e in events)
    messages = []
    real_messages = []
    for event in events:
        if event.get("type") != "assistant":
            continue
        assistant_count += 1
        message = event.get("message")
        if not isinstance(message, dict):
            malformed_fields += 1
            unknown_model_messages += 1
            continue
        model = message.get("model")
        if model == "<synthetic>":
            synthetic_messages += 1
            operational_error = True
        elif not isinstance(model, str) or not model:
            unknown_model_messages += 1
        else:
            generated.add(model)
            if model != expected_model:
                violations.append("different_generation_model:" + model)
        if message.get("is_error") is True or message.get("error"):
            operational_error = True
        content = message.get("content")
        if not isinstance(content, list):
            malformed_fields += 1
            continue
        pieces = []
        for block in content:
            if not isinstance(block, dict):
                malformed_fields += 1
            elif block.get("type") == "text":
                if isinstance(block.get("text"), str):
                    pieces.append(block["text"])
                else:
                    malformed_fields += 1
        text = "".join(pieces)
        if text:
            messages.append(text)
            if model == expected_model:
                real_messages.append(text)
    init_confirmed = (len(init) == 1 and init[0].get("model") == expected_model
                      and all(init[0].get(field) == [] for field in exposed_fields))
    generation_identity_confirmed = (assistant_count > 0 and generated == {expected_model}
                                     and not unknown_model_messages and not synthetic_messages)
    boundary_violation = bool(violations)
    boundary_ok = init_confirmed and generation_identity_confirmed and not boundary_violation
    result = results[-1] if len(results) == 1 else {}
    if result and (result.get("is_error") is True or result.get("subtype") != "success"):
        operational_error = True
    used_models = result.get("modelUsage") if isinstance(result.get("modelUsage"), dict) else {}
    terminal_text = result.get("result") if isinstance(result.get("result"), str) else ""
    if terminal_text and result.get("subtype") == "success" and result.get("is_error") is False:
        candidate_response, candidate_source = terminal_text, "terminal_success_result"
    elif real_messages:
        candidate_response, candidate_source = real_messages[-1], "last_real_assistant_text"
    elif messages:
        candidate_response, candidate_source = messages[-1], "last_assistant_text"
    else:
        candidate_response, candidate_source = terminal_text, "terminal_error_result" if terminal_text else "none"
    return {"boundary_ok": boundary_ok, "init": init[0] if init else {}, "result": result,
            "boundary_violation": boundary_violation, "boundary_violations": sorted(set(violations)),
            "boundary_state": "violation" if boundary_violation else ("confirmed" if boundary_ok else "unknown"),
            "generation_identity_confirmed": generation_identity_confirmed,
            "operational_error": operational_error, "synthetic_messages": synthetic_messages,
            "unknown_model_messages": unknown_model_messages, "result_count": len(results),
            "candidate_response": candidate_response, "candidate_source": candidate_source,
            "tool_call_count": tool_call_count,
            "generation_models": sorted(generated), "model_usage": used_models,
            "trace_valid": not invalid_utf8 and malformed_lines == 0 and malformed_fields == 0,
            "malformed_lines": malformed_lines, "malformed_fields": malformed_fields,
            "invalid_utf8": invalid_utf8}


def extract_code(result):
    def unique_keys(pairs):
        value = {}
        for key, item in pairs:
            if key in value:
                raise ValueError("Duplicate JSON output key")
            value[key] = item
        return value
    payload = json.loads(result.get("result", ""), object_pairs_hook=unique_keys)
    if not isinstance(payload, dict) or set(payload) != {"codex_jsonl.py"}:
        raise ValueError("Expected exactly codex_jsonl.py")
    code = payload["codex_jsonl.py"]
    if not isinstance(code, str) or not code.strip() or len(code.encode()) > 200000:
        raise ValueError("Missing or oversized source")
    return code


def score(destination, item, returncode, timed_out, wall_seconds, manifest):
    from evaluator import evaluate
    folder = destination / item["run_id"]
    record = {**item, "returncode": returncode, "timed_out": timed_out, "wall_seconds": wall_seconds,
              "cli_success": False, "artifact_success": False, "accepted_completion": False,
              "artifact_sha256": None, "code_path": None, "status": "invalid_trace", "usage": {},
              "total_cost_usd": None, "completed_at_utc": now()}
    try:
        trace = parse_trace((folder / "stdout.jsonl").read_bytes(), manifest["model"])
    except (ValueError, TypeError, KeyError, AttributeError) as exc:
        record["error"] = f"Invalid trace: {type(exc).__name__}: {exc}"
        return record
    result = trace["result"]
    write_json(folder / "trace-audit.json", {k: v for k, v in trace.items() if k not in ("result", "candidate_response")})
    record.update(usage=result.get("usage") if isinstance(result.get("usage"), dict) else {},
                  total_cost_usd=result.get("total_cost_usd"), model_usage=trace["model_usage"],
                  boundary_ok=trace["boundary_ok"], boundary_state=trace["boundary_state"],
                  boundary_violation=trace["boundary_violation"],
                  operational_error=trace["operational_error"])
    record["cli_success"] = (returncode == 0 and not timed_out and trace["boundary_ok"]
                              and trace["trace_valid"] and result.get("subtype") == "success"
                              and result.get("is_error") is False and not trace["operational_error"])
    if timed_out:
        record["status"] = "timeout"
    elif trace["operational_error"]:
        record["status"] = "operational_error"
    elif trace["boundary_state"] == "unknown" or not trace["trace_valid"] or trace["result_count"] != 1:
        record["status"] = "incomplete_trace"
    else:
        record["status"] = "completed" if record["cli_success"] else "cli_failure"
    if trace["boundary_violation"]:
        record["status"] = "boundary_failure"
        return record
    try:
        code = extract_code({"result": trace["candidate_response"]})
    except (ValueError, TypeError, KeyError) as exc:
        record["artifact_error"] = str(exc)
        return record
    candidate = folder / "candidate"
    candidate.mkdir()
    code_path = candidate / "codex_jsonl.py"
    code_path.write_text(code)
    before = sha(code_path.read_bytes())
    record.update(artifact_sha256=before, code_path=str(code_path.relative_to(destination)))
    write_json(folder / "sealed-artifact.json", {"code_path": record["code_path"], "sha256": before})
    # Trusted evaluator failures are measurement errors, never candidate failures.
    evaluation = evaluate(candidate)
    if not isinstance(evaluation, dict) or type(evaluation.get("passed")) is not bool:
        raise RuntimeError("Evaluator returned an invalid scoring schema")
    write_json(folder / "evaluation.json", evaluation)
    if before != sha(code_path.read_bytes()):
        raise RuntimeError("Sealed artifact changed during evaluation")
    record["artifact_success"] = evaluation["passed"]
    record["accepted_completion"] = record["cli_success"] and record["artifact_success"]
    return record


def run_locked(destination):
    from sandbox import preflight
    if (destination / "HALTED.json").exists():
        raise RuntimeError("Campaign has a persistent halt; it cannot resume")
    manifest = verify(destination, check_cli=False)
    isolation = preflight()
    write_json(destination / "launch-preflight.json", {"at_utc": now(), **isolation})
    records = destination / "records.jsonl"
    done = {}
    if records.exists():
        for line in records.read_text().splitlines():
            row = json.loads(line)
            if row["run_id"] in done:
                raise ValueError("Duplicate record")
            done[row["run_id"]] = row
            if row.get("boundary_violation") or row.get("status") == "boundary_failure":
                reason = "Previously recorded boundary violation; campaign halted on resume"
                write_json(destination / "HALTED.json", {"at_utc": now(), "reason": reason,
                                                        "active_run_ids": []})
                raise RuntimeError(reason)
    queue = [item for item in manifest["schedule"] if item["run_id"] not in done]
    # No reruns: a started folder without a result is an interrupted slot.
    for item in list(queue):
        folder = destination / item["run_id"]
        if folder.exists():
            if (folder / "generation.json").is_file():
                trace = parse_trace((folder / "stdout.jsonl").read_bytes(), manifest["model"])
                if trace["boundary_violation"]:
                    reason = "Previously generated boundary violation; campaign halted before new launches"
                    write_json(destination / "HALTED.json", {"at_utc": now(), "reason": reason,
                                                            "active_run_ids": []})
                    raise RuntimeError(reason)
                queue.remove(item)
                continue
            row = {**item, "status": "interrupted", "cli_success": False, "artifact_success": False,
                   "accepted_completion": False, "artifact_sha256": None, "code_path": None,
                   "usage": {}, "total_cost_usd": None, "wall_seconds": None}
            with records.open("a") as f:
                f.write(json.dumps(row) + "\n")
            queue.remove(item)
    active = []
    try:
        while queue or active:
            while queue and len(active) < manifest["workers"]:
                verify(destination)
                item = queue.pop(0)
                folder = destination / item["run_id"]
                folder.mkdir()
                workspace = tempfile.TemporaryDirectory(prefix="same-spec-cli-")
                out = (folder / "stdout.jsonl").open("w")
                err = (folder / "stderr.txt").open("w")
                prompt = (destination / f"packets/{item['arm']}.txt").open("r")
                write_json(folder / "launch.json", {**item, "started_at_utc": now(),
                           "input_sha256": manifest["input_packet_sha256"][item["arm"]],
                           "environment_controls_sha256": manifest["environment_controls"]["sha256"]})
                process = subprocess.Popen(manifest["invocation"], stdin=prompt, stdout=out, stderr=err,
                                           cwd=workspace.name, start_new_session=True,
                                           env=generation_environment(manifest["environment_controls"]))
                active.append({"item": item, "process": process, "workspace": workspace,
                               "handles": (out, err, prompt), "start": time.monotonic()})
                print(f"START {item['run_id']}", flush=True)
            for job in active[:]:
                proc = job["process"]
                elapsed = time.monotonic() - job["start"]
                timed_out = elapsed >= manifest["timeout_seconds"]
                if timed_out and proc.poll() is None:
                    os.killpg(proc.pid, signal.SIGTERM)
                    try:
                        proc.wait(timeout=5)
                    except subprocess.TimeoutExpired:
                        os.killpg(proc.pid, signal.SIGKILL)
                        proc.wait()
                if proc.poll() is not None:
                    for handle in job["handles"]:
                        handle.close()
                    job["workspace"].cleanup()
                    folder = destination / job["item"]["run_id"]
                    generation = {"returncode": proc.returncode, "timed_out": timed_out,
                                  "wall_seconds": elapsed, "observed_complete_at_utc": now()}
                    write_json(folder / "generation.json", generation)
                    trace = parse_trace((folder / "stdout.jsonl").read_bytes(), manifest["model"])
                    active.remove(job)
                    print(f"GENERATED {job['item']['run_id']} timeout={timed_out}", flush=True)
                    if trace["boundary_violation"]:
                        row = score(destination, job["item"], proc.returncode, timed_out, elapsed, manifest)
                        with records.open("a") as f:
                            f.write(json.dumps(row) + "\n")
                        raise RuntimeError("Observed model/tool boundary drift; campaign halted, no replacement slots")
            if active:
                time.sleep(0.5)
        # Evaluation cannot delay timeout supervision for still-generating slots.
        known = {json.loads(line)["run_id"] for line in records.read_text().splitlines()} if records.exists() else set()
        for item in manifest["schedule"]:
            if item["run_id"] in known:
                continue
            verify(destination, check_cli=False)
            generation = json.loads((destination / item["run_id"] / "generation.json").read_text())
            row = score(destination, item, generation["returncode"], generation["timed_out"], generation["wall_seconds"], manifest)
            verify(destination, check_cli=False)
            with records.open("a") as f:
                f.write(json.dumps(row, ensure_ascii=False, allow_nan=False) + "\n")
                f.flush()
                os.fsync(f.fileno())
            print(f"SCORED {row['run_id']} {row['status']} accepted={row['accepted_completion']}", flush=True)
            if row.get("boundary_violation"):
                raise RuntimeError("Observed boundary violation during scoring; campaign halted")
    except BaseException as exc:
        write_json(destination / "HALTED.json", {"at_utc": now(), "reason": f"{type(exc).__name__}: {exc}",
                                               "active_run_ids": [j["item"]["run_id"] for j in active]})
        raise
    finally:
        for job in active:
            proc = job["process"]
            if proc.poll() is None:
                os.killpg(proc.pid, signal.SIGKILL)
                proc.wait()
            for handle in job["handles"]:
                handle.close()
            job["workspace"].cleanup()


def run(destination):
    with (destination / ".runner.lock").open("a") as lock:
        try:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError as exc:
            raise RuntimeError("Another runner owns this campaign") from exc
        run_locked(destination)


def main():
    if sys.version_info < (3, 10):
        raise SystemExit("Python 3.10+ is required; select an explicit interpreter")
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    new = sub.add_parser("freeze")
    new.add_argument("destination", type=Path)
    new.add_argument("--phase", choices=("pilot", "formal"), required=True)
    new.add_argument("--model", default="claude-opus-5-5")
    new.add_argument("--effort", choices=("low", "medium", "high", "xhigh", "max"), default="high")
    new.add_argument("--workers", type=int, default=4)
    new.add_argument("--timeout", type=float, default=600)
    new.add_argument("--budget", type=float, default=5)
    execute = sub.add_parser("run")
    execute.add_argument("destination", type=Path)
    args = parser.parse_args()
    if args.command == "freeze":
        if not 1 <= args.workers <= 4 or args.timeout <= 0 or args.budget <= 0:
            parser.error("workers must be 1..4 and timeout/budget positive")
        m = freeze(args.destination.resolve(), args.phase, args.model, args.effort, args.workers, args.timeout, args.budget)
        print(f"Frozen {len(m['schedule'])} {args.phase} slots")
    else:
        destination = args.destination.resolve()
        frozen_script = destination / "source/run_study.py"
        if ROOT != frozen_script.parent:
            if not frozen_script.is_file() or frozen_script.is_symlink():
                raise ValueError("Frozen executable bundle is missing")
            os.execv(sys.executable, [sys.executable, str(frozen_script), "run", str(destination)])
        run(destination)


if __name__ == "__main__":
    main()
