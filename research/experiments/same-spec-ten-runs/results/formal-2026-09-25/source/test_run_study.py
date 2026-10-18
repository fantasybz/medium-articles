import json
import fcntl
import io
import os
from contextlib import redirect_stdout
from pathlib import Path
import tempfile
import types
import unittest
from unittest.mock import patch

import run_study as study


def trace(*, tools=None, model="model", text='{"codex_jsonl.py":"print(1)"}', terminal=True):
    events = [{"type": "system", "subtype": "init", "tools": tools or [], "mcp_servers": [],
               "model": model, "skills": [], "slash_commands": []},
              {"type": "assistant", "message": {"model": model, "content": [{"type": "text", "text": text}]}}]
    if terminal:
        events.append({"type": "result", "subtype": "success", "is_error": False, "result": text})
    return "\n".join(json.dumps(e) for e in events)


def synthetic_error_trace():
    events = [json.loads(line) for line in trace().splitlines()]
    events[1]["message"] = {"model": "<synthetic>", "content": [{"type": "text", "text": "API Error: 529"}]}
    events[2].update(subtype="error_during_execution", is_error=True, result="API Error: 529")
    return "\n".join(map(json.dumps, events))


class TraceTests(unittest.TestCase):
    def test_boundary_checks_real_exposure_and_generation_model(self):
        self.assertTrue(study.parse_trace(trace(), "model")["boundary_ok"])
        self.assertFalse(study.parse_trace(trace(tools=["Read"]), "model")["boundary_ok"])
        self.assertFalse(study.parse_trace(trace(model="different"), "model")["boundary_ok"])
        events = [json.loads(l) for l in trace().splitlines()]
        events[1]["message"]["content"].append({"type": "tool_use", "name": "Read"})
        self.assertFalse(study.parse_trace("\n".join(map(json.dumps, events)), "model")["boundary_ok"])

    def test_completed_artifact_can_survive_missing_terminal_event(self):
        parsed = study.parse_trace(trace(terminal=False), "model")
        self.assertTrue(parsed["boundary_ok"])
        self.assertEqual(parsed["result"], {})
        self.assertEqual(study.extract_code({"result": parsed["candidate_response"]}), "print(1)")

    def test_truncated_tail_never_hides_an_observed_boundary_violation(self):
        parsed = study.parse_trace(trace(tools=["Read"]) + '\n{"type":', "model")
        self.assertFalse(parsed["boundary_ok"])
        self.assertFalse(parsed["trace_valid"])
        self.assertEqual(parsed["malformed_lines"], 1)

    def test_artifact_allowlist_is_exact_and_never_strips_fences(self):
        for bad in ['{"../codex_jsonl.py":"x"}', '{"codex_jsonl.py":"x","tests.py":"x"}',
                    '{"codex_jsonl.py":"x","codex_jsonl.py":"y"}',
                    '{"codex_jsonl.py":123}', '```json\n{"codex_jsonl.py":"x"}\n```']:
            with self.subTest(bad=bad), self.assertRaises((ValueError, TypeError)):
                study.extract_code({"result": bad})

    def test_synthetic_api_error_is_operational_not_observed_drift(self):
        parsed = study.parse_trace(synthetic_error_trace(), "model")
        self.assertFalse(parsed["boundary_violation"])
        self.assertEqual(parsed["boundary_state"], "unknown")
        self.assertTrue(parsed["operational_error"])
        self.assertFalse(parsed["generation_identity_confirmed"])

    def test_missing_model_or_init_is_unknown_not_a_violation(self):
        events = [json.loads(line) for line in trace().splitlines()]
        del events[1]["message"]["model"]
        missing_model = study.parse_trace("\n".join(map(json.dumps, events)), "model")
        self.assertFalse(missing_model["boundary_violation"])
        self.assertFalse(missing_model["boundary_ok"])
        empty = study.parse_trace(b"", "model")
        self.assertEqual(empty["boundary_state"], "unknown")
        self.assertFalse(empty["boundary_violation"])

    def test_truncated_utf8_and_nested_shapes_never_erase_real_violation(self):
        raw = trace(tools=["Read"]).encode() + b'\n{"type":"assistant","message":null}\n\xe5\xaf'
        parsed = study.parse_trace(raw, "model")
        self.assertTrue(parsed["boundary_violation"])
        self.assertTrue(parsed["invalid_utf8"])
        self.assertFalse(parsed["trace_valid"])
        for message in (None, [], {"model": "model", "content": None},
                        {"model": "model", "content": [None, {"type": "text", "text": 3}]}):
            with self.subTest(message=message):
                row = json.dumps({"type": "assistant", "message": message})
                malformed = study.parse_trace(row, "model")
                self.assertFalse(malformed["trace_valid"])
                self.assertFalse(malformed["boundary_violation"])

    def test_tool_use_inside_malformed_content_is_still_a_violation(self):
        malformed = {"type": "assistant", "message": {"content": {"type": "tool_use", "name": "Read"}}}
        self.assertTrue(study.parse_trace(json.dumps(malformed), "model")["boundary_violation"])


class FreezeTests(unittest.TestCase):
    def fixture(self, source):
        (source / "seed").mkdir()
        (source / "specs").mkdir()
        (source / "seed/codex_jsonl.py").write_text("print('seed')")
        (source / "task.json").write_text(json.dumps({"seed_sha256": study.sha((source / "seed/codex_jsonl.py").read_bytes())}))
        for arm in study.ARMS:
            (source / f"specs/{arm}.md").write_text("same requirements " + arm)

    def test_schedule_is_balanced_and_post_freeze_changes_are_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            parent = Path(d)
            source = parent / "source"
            source.mkdir()
            self.fixture(source)
            dest = parent / "campaign"
            fake_cli = parent / "claude"
            fake_cli.write_text("fake CLI, never executed")
            with patch.object(study, "ROOT", source), patch("sandbox.preflight", return_value={"read_denied": True}), \
                    patch.object(study.shutil, "which", return_value=str(fake_cli)), \
                    patch.object(study.subprocess, "check_output", return_value="version\n"):
                manifest = study.freeze(dest, "formal", "model", "high", 4, 600, 5)
                self.assertEqual(len(manifest["schedule"]), 40)
                self.assertEqual((dest / "source/seed/codex_jsonl.py").read_bytes(), (source / "seed/codex_jsonl.py").read_bytes())
                for block in range(1, 11):
                    self.assertEqual({r["arm"] for r in manifest["schedule"] if r["block"] == block}, set(study.ARMS))
                self.assertEqual(study.verify(dest), manifest)
                (source / "specs/A.md").write_text("changed requirements")
                with self.assertRaisesRegex(ValueError, "Source changed"):
                    study.verify(dest)
                with self.assertRaisesRegex(ValueError, "already exists"):
                    study.freeze(dest, "formal", "model", "high", 4, 600, 5)

    def test_campaign_inside_source_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "outside"):
            study.freeze(study.ROOT / "results", "formal", "model", "high", 4, 600, 5)

    def test_halted_campaign_cannot_resume(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            (root / "HALTED.json").write_text('{}')
            with self.assertRaisesRegex(RuntimeError, "persistent halt"):
                study.run(root)

    def test_concurrent_runner_is_rejected_before_classifying_interruptions(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            with (root / ".runner.lock").open("a") as lock:
                fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
                with self.assertRaisesRegex(RuntimeError, "Another runner"):
                    study.run(root)

    def test_launcher_enters_frozen_bundle_before_verifying_source(self):
        class ExecEntered(Exception):
            pass
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            frozen = root / "source/run_study.py"
            frozen.parent.mkdir()
            frozen.write_text("# Executed by the intercepted execv, not imported here")
            with patch.object(study.sys, "argv", ["run_study.py", "run", str(root)]), \
                    patch.object(study, "verify", side_effect=AssertionError("live source verification happened")), \
                    patch.object(study.os, "execv", side_effect=ExecEntered) as execute:
                with self.assertRaises(ExecEntered):
                    study.main()
            self.assertEqual(execute.call_args.args[1][1:], [str(frozen.resolve()), "run", str(root.resolve())])

    def test_scoring_verification_never_resolves_or_invokes_cli(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source, destination = root / "source", root / "campaign"
            source.mkdir()
            self.fixture(source)
            fake_cli = root / "claude"
            fake_cli.write_text("fake CLI")
            with patch.object(study, "ROOT", source), patch("sandbox.preflight", return_value={}), \
                    patch.object(study.shutil, "which", return_value=str(fake_cli)), \
                    patch.object(study.subprocess, "check_output", return_value="version\n"):
                manifest = study.freeze(destination, "pilot", "model", "high", 1, 600, 5)
            fake_cli.unlink()
            with patch.object(study, "ROOT", source), \
                    patch.object(study.shutil, "which", side_effect=AssertionError("PATH was consulted")), \
                    patch.object(study.subprocess, "check_output", side_effect=AssertionError("CLI was invoked")):
                self.assertEqual(study.verify(destination, check_cli=False), manifest)
                with self.assertRaises(FileNotFoundError):
                    study.verify(destination, check_cli=True)

    def test_environment_records_controls_and_names_without_credentials(self):
        fake_env = {"ANTHROPIC_API_KEY": "never-record-this-value", "ANTHROPIC_BASE_URL": "private-route",
                    "CLAUDE_CODE_MAX_OUTPUT_TOKENS": "8000", "MAX_THINKING_TOKENS": "1000"}
        with patch.dict(study.os.environ, fake_env, clear=True):
            controls = study.environment_controls()
        serialized = json.dumps(controls)
        self.assertNotIn("never-record-this-value", serialized)
        self.assertNotIn("private-route", serialized)
        self.assertEqual(controls["anthropic_variable_names"], ["ANTHROPIC_API_KEY", "ANTHROPIC_BASE_URL"])
        self.assertEqual(controls["values"]["DISABLE_AUTOUPDATER"], "1")
        with patch.dict(study.os.environ, {"CLAUDE_CODE_MAX_OUTPUT_TOKENS": "9000"}, clear=True):
            self.assertEqual(study.generation_environment(controls)["CLAUDE_CODE_MAX_OUTPUT_TOKENS"], "8000")


class ScoringTests(unittest.TestCase):
    def test_resume_detects_boundary_violation_before_any_new_launch(self):
        for already_scored in (False, True):
            with self.subTest(already_scored=already_scored), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                schedule = [{"run_id": "pilot-01-" + arm, "arm": arm, "phase": "pilot", "block": 1}
                            for arm in ("A0", "C")]
                folder = root / schedule[0]["run_id"]
                folder.mkdir()
                (folder / "generation.json").write_text('{}')
                (folder / "stdout.jsonl").write_text(trace(tools=["Read"]))
                if already_scored:
                    (root / "records.jsonl").write_text(json.dumps({**schedule[0],
                        "status": "boundary_failure", "boundary_violation": True}) + "\n")
                with patch.object(study, "verify", return_value={"schedule": schedule, "model": "model"}), \
                        patch("sandbox.preflight", return_value={}), \
                        patch.object(study.subprocess, "Popen", side_effect=AssertionError("new slot launched")):
                    with self.assertRaisesRegex(RuntimeError, "boundary violation"):
                        study.run(root)
                self.assertTrue((root / "HALTED.json").exists())
                self.assertFalse((root / schedule[1]["run_id"]).exists())

    def score_fixture(self, raw, *, timed_out=False, returncode=0, evaluator=None):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        root = Path(temporary.name)
        item = {"run_id": "pilot-01-A0", "arm": "A0", "phase": "pilot", "block": 1}
        folder = root / item["run_id"]
        folder.mkdir()
        (folder / "stdout.jsonl").write_bytes(raw if isinstance(raw, bytes) else raw.encode())
        evaluator = evaluator or (lambda candidate: {"passed": True})
        with patch.dict("sys.modules", {"evaluator": types.SimpleNamespace(evaluate=evaluator)}):
            row = study.score(root, item, returncode, timed_out, 1.0, {"model": "model"})
        return root, row

    def test_trusted_evaluator_failure_is_not_recorded_as_candidate_failure(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            item = {"run_id": "formal-01-A", "arm": "A", "phase": "formal", "block": 1}
            folder = root / item["run_id"]
            folder.mkdir()
            (folder / "stdout.jsonl").write_text(trace())
            def broken_oracle(candidate):
                raise ValueError("oracle defect")
            with patch.dict("sys.modules", {"evaluator": types.SimpleNamespace(evaluate=broken_oracle)}):
                with self.assertRaisesRegex(ValueError, "oracle defect"):
                    study.score(root, item, 0, False, 1.0, {"model": "model"})
            self.assertTrue((folder / "sealed-artifact.json").exists())

    def test_synthetic_cannot_forge_a_success_terminal_but_artifact_is_separate(self):
        events = [json.loads(line) for line in trace().splitlines()]
        events[1]["message"]["model"] = "<synthetic>"
        _, row = self.score_fixture("\n".join(map(json.dumps, events)))
        self.assertFalse(row["cli_success"])
        self.assertFalse(row["accepted_completion"])
        self.assertTrue(row["artifact_success"])
        self.assertEqual(row["status"], "operational_error")

    def test_missing_generation_identity_cannot_forge_cli_success(self):
        events = [json.loads(line) for line in trace().splitlines()]
        del events[1]["message"]["model"]
        _, row = self.score_fixture("\n".join(map(json.dumps, events)))
        self.assertFalse(row["cli_success"])
        self.assertTrue(row["artifact_success"])
        self.assertEqual(row["status"], "incomplete_trace")

    def test_no_init_timeout_is_retained_without_boundary_failure(self):
        _, row = self.score_fixture(b"", timed_out=True, returncode=-15)
        self.assertEqual(row["status"], "timeout")
        self.assertEqual(row["boundary_state"], "unknown")
        self.assertFalse(row["boundary_violation"])
        self.assertFalse(row["accepted_completion"])

    def test_invalid_utf8_prevents_cli_success_without_hiding_artifact(self):
        _, row = self.score_fixture(trace().encode() + b"\n\xe5\xaf")
        self.assertFalse(row["cli_success"])
        self.assertTrue(row["artifact_success"])
        self.assertEqual(row["status"], "incomplete_trace")

    def test_evaluator_schema_and_integrity_errors_escape(self):
        with self.assertRaisesRegex(RuntimeError, "invalid scoring schema"):
            self.score_fixture(trace(), evaluator=lambda candidate: {})

        def modify(candidate):
            (candidate / "codex_jsonl.py").write_text("changed")
            return {"passed": True}

        with self.assertRaisesRegex(RuntimeError, "changed during evaluation"):
            self.score_fixture(trace(), evaluator=modify)

    def test_operational_failures_do_not_halt_or_replace_slots(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "packets").mkdir()
            schedule = [{"run_id": "pilot-01-" + arm, "arm": arm, "phase": "pilot", "block": 1}
                        for arm in ("A0", "C")]
            for arm in ("A0", "C"):
                (root / f"packets/{arm}.txt").write_text("packet")
            manifest = {"schedule": schedule, "workers": 1, "timeout_seconds": 60,
                        "model": "model", "input_packet_sha256": {"A0": "hash", "C": "hash"},
                        "invocation": ["fake-cli"], "environment_controls": study.environment_controls()}
            outputs = iter([synthetic_error_trace(), ""])
            launched = []

            def fake_process(command, **kwargs):
                launched.append(command)
                self.assertEqual(kwargs["env"]["DISABLE_AUTOUPDATER"], "1")
                kwargs["stdout"].write(next(outputs))
                return types.SimpleNamespace(returncode=1, pid=123456, poll=lambda: 1)

            with patch.object(study, "verify", return_value=manifest) as verify, \
                    patch("sandbox.preflight", return_value={}), \
                    patch.object(study.subprocess, "Popen", side_effect=fake_process), \
                    patch.dict("sys.modules", {"evaluator": types.SimpleNamespace(evaluate=lambda candidate: {"passed": True})}), \
                    redirect_stdout(io.StringIO()):
                study.run(root)
            rows = [json.loads(line) for line in (root / "records.jsonl").read_text().splitlines()]
            self.assertEqual(len(launched), 2)
            self.assertEqual([row["run_id"] for row in rows], [item["run_id"] for item in schedule])
            self.assertEqual([row["status"] for row in rows], ["operational_error", "incomplete_trace"])
            self.assertFalse((root / "HALTED.json").exists())
            self.assertTrue(all(not row["accepted_completion"] for row in rows))
            self.assertEqual(sum(call.kwargs.get("check_cli") is False for call in verify.call_args_list), 5)


if __name__ == "__main__":
    unittest.main()
