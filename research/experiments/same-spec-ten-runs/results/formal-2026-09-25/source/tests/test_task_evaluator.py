"""Offline apparatus checks, including real-OS-sandbox fixture/mutation checks.

AI reference and intentionally broken fixtures are never study runs or human
baselines. Pure grading tests use a stub result only; isolation tests explicitly
call sandbox.preflight and never substitute an unsandboxed subprocess.
"""
import ast
from dataclasses import replace
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import sys
import tempfile
from types import SimpleNamespace
import unittest
from unittest import mock

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT))
import evaluator
import sandbox


class TestSpecificationManifest(unittest.TestCase):
    def test_all_arms_have_same_normative_ids_and_guidance_is_appended(self):
        manifest = json.loads((ROOT / "requirements.json").read_text())
        required = {row["id"] for row in manifest["requirements"]}
        self.assertEqual(required, {f"R{i:02d}" for i in range(1, 14)})
        texts = {arm: (ROOT / "specs" / f"{arm}.md").read_text()
                 for arm in ("A0", "A", "B", "C")}
        for arm, text in texts.items():
            with self.subTest(arm=arm):
                headings = re.findall(r"^### (R\d+) —", text, flags=re.M)
                self.assertEqual(set(headings), required)
                self.assertEqual(len(headings), len(required))
        self.assertTrue(texts["B"].startswith(texts["A"]))
        self.assertTrue(texts["C"].startswith(texts["B"]))
        self.assertEqual(hashlib.sha256((ROOT / "seed/codex_jsonl.py").read_bytes()).hexdigest(),
                         manifest["source_sha256"])

    def test_external_cases_cover_all_requirements_without_duplicate_ids(self):
        cases = evaluator.cases()
        self.assertEqual(len(cases), len({row.case_id for row in cases}))
        self.assertEqual({rid for case in cases for rid in case.requirements},
                         {f"R{i:02d}" for i in range(1, 14)})
        self.assertEqual(len([case for case in cases if case.group == "legacy"]), 16)
        self.assertTrue(any(case.c_locale for case in cases))

    def test_seed_is_exact_fixed_repository_baseline(self):
        # Only a file hash, never the current mutable production implementation.
        self.assertEqual(hashlib.sha256((ROOT / "seed/codex_jsonl.py").read_bytes()).hexdigest(),
                         "4949ff55184cbfd3cbd0c8add632a6382ec4b5e6ec2240ca88018443370e6afb")


class TestPureGrading(unittest.TestCase):
    """Stub result objects test grading only; these tests do not prove isolation."""

    def case(self, name="wrong-root-list"):
        return next(case for case in evaluator.cases() if case.case_id == name)

    def result(self, case, **changes):
        fields = dict(returncode=case.returncode, stdout=case.stdout,
                      stderr=evaluator.expected_stderr_description(case.stderr).replace(
                          "<nonempty reason>", "bad object"),
                      timed_out=False, sandbox=evaluator.VERIFIED_SANDBOX)
        fields.update(changes)
        return SimpleNamespace(**fields)

    def test_exact_stdout_exit_and_malformed_line_marker_are_required(self):
        case = self.case()
        self.assertTrue(evaluator._grade(case, self.result(case), max_output_bytes=65536)["passed"])
        for changes in [dict(returncode=0), dict(stdout=case.stdout + "debug\n"),
                        dict(stderr="[codex malformed event] line 2: wrong\n"),
                        dict(stderr="[codex malformed event] line 1: \n"),
                        dict(stderr="[codex malformed event] line 1: bad\nTraceback\n")]:
            with self.subTest(changes=changes):
                self.assertFalse(evaluator._grade(case, self.result(case, **changes),
                                                  max_output_bytes=65536)["passed"])

    def test_timeout_output_bound_and_unknown_sandbox_fail(self):
        case = self.case()
        self.assertEqual(evaluator._grade(case, self.result(case, timed_out=True),
                                         max_output_bytes=65536)["failure"], "timeout")
        self.assertEqual(evaluator._grade(case, self.result(case, stdout="x" * 20),
                                         max_output_bytes=10)["failure"], "output_limit")
        with self.assertRaises(evaluator.EvaluationUnavailable):
            evaluator._grade(case, self.result(case, sandbox="none"), max_output_bytes=65536)

    def test_incomplete_preflight_cannot_execute_a_candidate(self):
        with mock.patch.object(sandbox, "preflight", return_value={"sandbox": evaluator.VERIFIED_SANDBOX}), \
             mock.patch.object(sandbox, "run_candidate") as run:
            with self.assertRaises(evaluator.EvaluationUnavailable):
                evaluator._boundary()
            run.assert_not_called()

    def test_unsupported_sandbox_fails_closed(self):
        with mock.patch.object(sandbox, "preflight", side_effect=sandbox.SandboxUnavailable("unsupported")), \
             mock.patch.object(sandbox, "run_candidate") as run:
            with self.assertRaises(evaluator.EvaluationUnavailable):
                evaluator._boundary()
            run.assert_not_called()

    def test_extra_candidate_files_and_symlinks_are_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "codex_jsonl.py"
            source.write_text("pass\n")
            self.assertEqual(evaluator._check_candidate_layout(root), source.resolve())
            (root / "test_evil.py").write_text("raise RuntimeError('do not run')\n")
            with self.assertRaises(evaluator.CandidateLayoutError):
                evaluator._check_candidate_layout(root)
            (root / "test_evil.py").unlink()
            source.unlink()
            source.symlink_to(ROOT / "seed/codex_jsonl.py")
            with self.assertRaises(evaluator.CandidateLayoutError):
                evaluator._check_candidate_layout(root)


class TestRealSandboxFixtures(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # An unsupported machine fails this requested verification. No stub,
        # skip-on-error, or direct subprocess can turn it into a green check.
        cls.isolation = sandbox.preflight()
        cls.reference = (HERE / "fixtures/parser_reference.py").read_text()
        cls.by_id = {case.case_id: case for case in evaluator.cases()}

    def candidate(self, source):
        directory = tempfile.TemporaryDirectory(prefix="parser-fixture-")
        self.addCleanup(directory.cleanup)
        root = Path(directory.name)
        (root / "codex_jsonl.py").write_text(source)
        return root

    def test_ai_reference_passes_all_cases_and_real_streaming_probe(self):
        result = evaluator.evaluate(self.candidate(self.reference))
        failed = [row for row in result["cases"] if not row["passed"]]
        self.assertTrue(result["passed"], json.dumps(failed, ensure_ascii=False, indent=2))
        self.assertTrue(result["sandbox"]["read_denied"])
        self.assertTrue(result["sandbox"]["write_denied"])
        self.assertTrue(result["sandbox"]["network_denied"])

    def test_unchanged_real_seed_passes_legacy_and_fails_new_type_cases(self):
        root = self.candidate((ROOT / "seed/codex_jsonl.py").read_text())
        legacy = [case for case in evaluator.cases() if case.group == "legacy"]
        for case in legacy:
            with self.subTest(case=case.case_id):
                result = evaluator._run_case(case, root, sandbox, timeout_seconds=3, max_output_bytes=65536)
                self.assertTrue(result["passed"], result)
        for name in ("wrong-root-list", "wrong-usage-null", "wrong-agent_message-number"):
            with self.subTest(known_bug=name):
                result = evaluator._run_case(self.by_id[name], root, sandbox,
                                              timeout_seconds=3, max_output_bytes=65536)
                self.assertFalse(result["passed"], "Baseline bug must remain detectable")

    def test_known_fault_mutations_are_detected(self):
        mutations = [
            ("skip-decoded-scalar", 'raise MalformedEvent("event must be an object")',
             "continue", "wrong-root-list"),
            ("accept-bool-token", "type(value) is not int", "not isinstance(value, int)",
             "wrong-input_tokens-bool"),
            ("coerce-nontext-agent", 'raise MalformedEvent(field + " must be a string or null")',
             "return str(value)", "wrong-agent_message-number"),
            ("disconnect-before-malformed", "if malformed:\n        return 6", "if malformed and done > 0:\n        return 6",
             "malformed-outranks-disconnect"),
            ("malformed-before-remote-error", "    if failed:\n", "    if malformed:\n        return 6\n    if failed:\n",
             "later-error-outranks-malformed"),
            ("drop-malformed-failed-turn", "failed = True  # A failed-turn event retains failure even if its payload is malformed.",
             "failed = False  # intentionally broken mutation", "wrong-failed-error-envelope-number"),
            ("stop-reading-after-malformed", "        except MalformedEvent as exc:\n            malformed = True\n            bad(line_number, str(exc))",
             "        except MalformedEvent as exc:\n            malformed = True\n            bad(line_number, str(exc))\n            return 6",
             "wrong-root-list"),
        ]
        for name, before, after, case_id in mutations:
            with self.subTest(mutation=name):
                self.assertEqual(self.reference.count(before), 1, "Mutation point must be unique")
                mutant = self.reference.replace(before, after, 1)
                ast.parse(mutant)  # A syntax error is not meaningful mutation detection.
                result = evaluator._run_case(self.by_id[case_id], self.candidate(mutant), sandbox,
                                              timeout_seconds=3, max_output_bytes=65536)
                self.assertFalse(result["passed"], name)
                self.assertNotIn("SyntaxError", result.get("actual_stderr", ""))

    def test_whole_input_buffering_mutation_is_detected_before_eof(self):
        before = "for line_number, line in enumerate(sys.stdin, 1):"
        after = "for line_number, line in enumerate(sys.stdin.read().splitlines(True), 1):"
        self.assertEqual(self.reference.count(before), 1)
        mutant = self.reference.replace(before, after, 1)
        ast.parse(mutant)
        result = evaluator._streaming_case(self.candidate(mutant), sandbox, timeout_seconds=0.6)
        self.assertFalse(result["passed"])
        self.assertFalse(result["observed_before_eof"])


if __name__ == "__main__":
    unittest.main()
