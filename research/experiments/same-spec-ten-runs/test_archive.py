"""Integrity and privacy regression checks; fixtures are not experiment results."""
import hashlib
import json
from pathlib import Path
import shutil
import sys
import tempfile
import unittest
from unittest import mock

import archive
import run_study

HERE = Path(__file__).resolve().parent


class ArchiveTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.campaign = self.root / "campaign"
        self.campaign.mkdir()
        self.source = self.campaign / "source"
        self.source.mkdir()
        names = ["archive.py", "analyze.py", "run_study.py", "evaluator.py", "sandbox.py", "requirements.json"]
        for name in names:
            shutil.copyfile(HERE / name, self.source / name)
        (self.campaign / "packets").mkdir()
        for arm in ("A0", "A", "B", "C"):
            (self.campaign / "packets" / f"{arm}.txt").write_text("fixture prompt " + arm)
        (self.campaign / "system.txt").write_text("fixture system")
        self.schedule = [{"run_id": f"formal-{block:02d}-{arm}", "block": block, "arm": arm, "phase": "formal"}
                         for block in range(1, 11) for arm in ("A0", "A", "B", "C")]
        self.manifest = {"phase": "formal", "schedule": self.schedule, "python_version": sys.version,
                         "platform": sys.platform, "model": "fixture-model",
                         "source_sha256": {name: archive.sha((self.source / name).read_bytes()) for name in names},
                         "input_packet_sha256": {arm: archive.sha((self.campaign / "packets" / f"{arm}.txt").read_bytes())
                                                  for arm in ("A0", "A", "B", "C")},
                         "system_input_sha256": archive.sha((self.campaign / "system.txt").read_bytes())}
        self.rows = [{**item, "status": "interrupted", "cli_success": False, "artifact_success": False,
                      "accepted_completion": False, "code_path": None, "artifact_sha256": None,
                      "usage": {}, "wall_seconds": None, "total_cost_usd": None} for item in self.schedule]
        self.save_manifest()
        self.save_records()
        (self.campaign / "launch-preflight.json").write_text('{}\n')

    def save_manifest(self):
        data = archive.encoded(self.manifest)
        (self.campaign / "manifest.json").write_bytes(data)
        (self.campaign / "manifest.sha256").write_text(archive.sha(data) + "\n")

    def save_records(self):
        (self.campaign / "records.jsonl").write_text("".join(json.dumps(row) + "\n" for row in self.rows))

    def test_manifest_and_source_tampering_refuse_before_loading(self):
        (self.campaign / "manifest.json").write_bytes((self.campaign / "manifest.json").read_bytes() + b" ")
        with mock.patch.object(archive, "load_frozen", side_effect=AssertionError("must not execute")):
            with self.assertRaisesRegex(archive.ArchiveError, "manifest.json"):
                archive.verify_campaign(self.campaign)
        self.save_manifest()
        (self.source / "evaluator.py").write_text("raise RuntimeError('tampered source must not run')")
        with mock.patch.object(archive, "load_frozen", side_effect=AssertionError("must not execute")):
            with self.assertRaisesRegex(archive.ArchiveError, "evaluator.py"):
                archive.verify_campaign(self.campaign)

    @unittest.skipUnless(sys.platform == "darwin", "formal runtime is macOS-only")
    def test_missing_slot_and_pilot_cannot_export(self):
        self.rows.pop()
        self.save_records()
        with self.assertRaisesRegex(ValueError, "Missing scheduled records"):
            archive.export_campaign(self.campaign, self.root / "public")
        self.assertFalse((self.root / "public").exists())
        self.manifest["phase"] = "pilot"
        self.save_manifest()
        with self.assertRaisesRegex(archive.ArchiveError, "pilot"):
            archive.verify_source(self.campaign)

    @unittest.skipUnless(sys.platform == "darwin", "formal runtime is macOS-only")
    def test_candidate_tampering_detected_before_evaluation(self):
        row = self.rows[0]
        name = f"{row['run_id']}/candidate/codex_jsonl.py"
        candidate = self.campaign / name
        candidate.parent.mkdir(parents=True)
        candidate.write_text("print('original')\n")
        row.update(code_path=name, artifact_sha256=archive.sha(candidate.read_bytes()))
        self.save_records()
        candidate.write_text("print('changed')\n")
        with self.assertRaisesRegex(ValueError, "artifact SHA-256 mismatch"):
            archive.verify_campaign(self.campaign)

    def test_halted_campaign_is_refused_even_with_all_40_records(self):
        (self.campaign / "HALTED.json").write_text('{"reason":"boundary breach on last slot"}')
        with self.assertRaisesRegex(archive.ArchiveError, "Halted"):
            archive.verify_campaign(self.campaign)

    def test_projection_removes_private_metadata_and_keeps_boundary_evidence(self):
        events = [
            {"type": "system", "subtype": "init", "model": "fixture-model", "tools": [], "skills": [],
             "mcp_servers": [], "slash_commands": [], "cwd": "PRIVATE-CWD", "session_id": "PRIVATE-SESSION",
             "claude_code_version": "2.1.0", "apiKeySource": "PRIVATE-AUTH", "messaging_socket_path": "PRIVATE-SOCKET"},
            {"type": "assistant", "uuid": "PRIVATE-UUID", "request_id": "PRIVATE-REQUEST",
             "message": {"model": "fixture-model", "content": [
                 {"type": "thinking", "thinking": "PRIVATE-THOUGHT", "signature": "PRIVATE-SIGNATURE"},
                 {"type": "text", "text": '{"codex_jsonl.py":"print(1)\\n"}'}]}},
            {"type": "result", "subtype": "success", "is_error": False,
             "result": '{"codex_jsonl.py":"print(1)\\n"}', "total_cost_usd": 0.1,
             "usage": {"input_tokens": 12, "output_tokens": 24, "auth": "PRIVATE-NESTED-AUTH"},
             "modelUsage": {"fixture-model": {"costUSD": 0.1, "request_id": "PRIVATE-NESTED-ID"}}},
        ]
        raw = ("".join(json.dumps(event) + "\n" for event in events)).encode()
        projected, metadata = archive.project_trace(raw, "fixture-model", run_study.parse_trace)
        self.assertNotIn(b"PRIVATE-", projected)
        self.assertNotIn(b'"thinking"', projected)
        self.assertNotIn(b"PRIVATE-", archive.encoded(metadata))
        original = run_study.parse_trace(raw, "fixture-model")
        public = run_study.parse_trace(projected, "fixture-model")
        for key in ("boundary_ok", "candidate_response", "trace_valid", "generation_models", "candidate_source"):
            self.assertEqual(original[key], public[key], key)
        self.assertTrue(public["boundary_ok"])
        self.assertEqual(public["result"]["usage"]["output_tokens"], 24)
        self.assertEqual(metadata["raw_sha256"], hashlib.sha256(raw).hexdigest())
        self.assertEqual(metadata["projection_sha256"], hashlib.sha256(projected).hexdigest())
        # A tool call hidden in a discarded thinking envelope must remain observable.
        events[1]["message"]["content"][0]["nested"] = {"type": "tool_use", "input": {"auth": "PRIVATE-TOOL"}}
        bad = ("".join(json.dumps(event) + "\n" for event in events)).encode()
        projected, _ = archive.project_trace(bad, "fixture-model", run_study.parse_trace)
        self.assertNotIn(b"PRIVATE-", projected)
        audit = run_study.parse_trace(projected, "fixture-model")
        self.assertEqual(audit["tool_call_count"], 1)
        self.assertTrue(audit["boundary_violation"])

    def test_projection_preserves_malformed_lines_and_records_encoding_loss(self):
        raw = b'not-json\n[]\n{"type":"assistant","message":false}\n\xff\n'
        projected, metadata = archive.project_trace(raw, "fixture-model", run_study.parse_trace)
        self.assertEqual(run_study.parse_trace(projected, "fixture-model")["malformed_lines"], 3)
        self.assertTrue(metadata["original_parser_observations"]["invalid_utf8"])
        self.assertFalse(metadata["projection_parser_observations"]["invalid_utf8"])

    @unittest.skipUnless(sys.platform == "darwin", "formal runtime is macOS-only")
    def test_export_index_has_no_self_cycle_and_refuses_overwrite(self):
        destination = self.root / "public"
        index = archive.export_campaign(self.campaign, destination)
        self.assertEqual(index["slots"], 40)
        self.assertNotIn("archive.json", index["files_sha256"])
        self.assertNotIn("archive.sha256", index["files_sha256"])
        for name, expected in index["files_sha256"].items():
            self.assertEqual(archive.sha((destination / name).read_bytes()), expected)
        self.assertEqual((destination / "archive.sha256").read_text().strip(), archive.sha((destination / "archive.json").read_bytes()))
        with self.assertRaisesRegex(archive.ArchiveError, "new"):
            archive.export_campaign(self.campaign, destination)
        records = destination / "records.jsonl"
        records.write_bytes(records.read_bytes() + b" ")
        with self.assertRaisesRegex(archive.ArchiveError, "records.jsonl"):
            archive.verify_source(destination)
        with self.assertRaisesRegex(archive.ArchiveError, "outside"):
            archive.rescore_campaign(self.campaign, self.campaign / "rescore.json")

    @unittest.skipUnless(sys.platform == "darwin", "formal runtime is macOS-only")
    def test_trusted_preflight_exception_never_writes_completed_rescore(self):
        original_loader = archive.load_frozen
        def loader(campaign, filename, name):
            if filename == "sandbox.py":
                return mock.Mock(preflight=mock.Mock(side_effect=RuntimeError("probe unavailable")))
            return original_loader(campaign, filename, name)
        output = self.root / "rescore.json"
        with mock.patch.object(archive, "load_frozen", side_effect=loader):
            with self.assertRaisesRegex(RuntimeError, "probe unavailable"):
                archive.rescore_campaign(self.campaign, output)
        self.assertFalse(output.exists())


if __name__ == "__main__":
    unittest.main()
