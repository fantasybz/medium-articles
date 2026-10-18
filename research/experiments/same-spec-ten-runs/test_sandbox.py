from pathlib import Path
import platform
import tempfile
import unittest
from unittest.mock import patch

import sandbox


class SandboxTests(unittest.TestCase):
    def test_unsupported_os_fails_closed(self):
        with patch.object(sandbox.platform, "system", return_value="unsupported"):
            with self.assertRaises(sandbox.SandboxUnavailable):
                sandbox.profile(Path("/tmp/candidate.py"))

    def test_symlink_and_path_escape_are_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            (root / "real.py").write_text("print('ok')")
            (root / "codex_jsonl.py").symlink_to(root / "real.py")
            with self.assertRaises(sandbox.SandboxUnavailable):
                sandbox.run_candidate(root, "")
            with self.assertRaises(ValueError):
                sandbox.run_candidate(root, "", script_name="../real.py")

    @unittest.skipUnless(platform.system() == "Darwin", "actual macOS boundary")
    def test_real_boundary_denies_external_read_write_and_network(self):
        observed = sandbox.preflight()
        self.assertTrue(observed["read_denied"] and observed["write_denied"] and observed["network_denied"])

    @unittest.skipUnless(platform.system() == "Darwin", "actual macOS boundary")
    def test_streaming_probe_detects_buffer_until_eof_mutation(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            candidate = root / "codex_jsonl.py"
            candidate.write_text("import sys\nfor line in sys.stdin:\n print(line.strip(),flush=True)\n")
            self.assertTrue(sandbox.run_streaming_probe(root, "hello\n", "bye\n", "hello\n")["passed"])
            candidate.write_text("import sys\nprint(sys.stdin.read(),end='')\n")
            self.assertFalse(sandbox.run_streaming_probe(root, "hello\n", "bye\n", "hello\n", timeout_seconds=0.3)["passed"])

    @unittest.skipUnless(platform.system() == "Darwin", "actual macOS boundary")
    def test_timeout_and_output_limits(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            candidate = root / "codex_jsonl.py"
            candidate.write_text("while True: pass\n")
            result = sandbox.run_candidate(root, "", timeout_seconds=0.1)
            self.assertTrue(result.timed_out)
            self.assertNotEqual(result.returncode, 0)
            candidate.write_text("print('x'*1000000)\n")
            result = sandbox.run_candidate(root, "", max_output_bytes=2048)
            self.assertLessEqual(len(result.stdout.encode()), 2049)
            self.assertNotEqual(result.returncode, 0)


if __name__ == "__main__":
    unittest.main()
