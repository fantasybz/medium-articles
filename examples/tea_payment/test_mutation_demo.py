"""Keep runner/selection failures from masquerading as mutation evidence."""
from contextlib import redirect_stdout
from pathlib import Path
import io
import json
import os
import subprocess
import tempfile
import unittest
from unittest.mock import patch

import mutation_demo


class MutationEvidenceTests(unittest.TestCase):
    def setUp(self):
        self.source = (mutation_demo.ROOT / "payment.py").read_text(encoding="utf-8")

    def test_python_environment_cannot_select_the_unmutated_module(self):
        mutant = self.source.replace(
            "self.gateway.charge(order.order_id, order.amount_ntd)",
            "self.gateway.charge(order.order_id, 1)", 1)
        with patch.dict(os.environ, {"PYTHONPATH": str(mutation_demo.ROOT),
                                     "PYTHONSAFEPATH": "1"}):
            result = mutation_demo.execute(mutant, "functional")
        self.assertEqual(result["failures"], [
            "test_payment.FunctionalTests.test_provider_captures_exactly_35_ntd"])

    def test_import_failure_is_not_a_killed_mutant(self):
        with self.assertRaisesRegex(RuntimeError, "Runner failed, not a killed mutant"):
            mutation_demo.execute("import missing_tea_payment_demo_module\n", "functional")

    def altered_tests(self, old, new, suite, message):
        original = (mutation_demo.ROOT / "test_payment.py").read_text(encoding="utf-8")
        self.assertEqual(original.count(old), 1)
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            (root / "test_payment.py").write_text(original.replace(old, new, 1), encoding="utf-8")
            with patch.object(mutation_demo, "ROOT", root):
                with self.assertRaisesRegex(RuntimeError, message):
                    mutation_demo.execute(self.source, suite)

    def test_renamed_timeout_test_cannot_silently_change_selection(self):
        self.altered_tests("def test_timeout_stays_pending_without_another_charge(self):",
                           "def test_timeout_renamed(self):", "without-timeout", "Runner failed")

    def test_skipped_test_cannot_be_reported_as_a_clean_baseline(self):
        self.altered_tests("    def test_provider_captures_exactly_35_ntd(self):",
                           '    @unittest.skip("would hide a missing check")\n'
                           "    def test_provider_captures_exactly_35_ntd(self):",
                           "functional", "Inconclusive execution")

    def test_execution_error_is_not_a_killed_mutant(self):
        signature = "    def test_provider_captures_exactly_35_ntd(self):"
        self.altered_tests(signature,
                           signature + '\n        raise RuntimeError("broken test fixture")',
                           "functional", "Inconclusive execution")

    def test_expected_failure_cannot_be_reported_as_clean_evidence(self):
        signature = "    def test_provider_captures_exactly_35_ntd(self):"
        self.altered_tests(signature,
                           "    @unittest.expectedFailure\n" + signature
                           + '\n        self.fail("known failing fixture")',
                           "functional", "Inconclusive execution")

    def test_unexpected_success_cannot_be_reported_as_clean_evidence(self):
        signature = "    def test_provider_captures_exactly_35_ntd(self):"
        self.altered_tests(signature, "    @unittest.expectedFailure\n" + signature,
                           "functional", "Inconclusive execution")

    def test_selection_count_drift_cannot_be_reported_as_clean_evidence(self):
        signature = "    def test_provider_captures_exactly_35_ntd(self):"
        replacements = {
            "missing": "    def helper_no_longer_selected(self):",
            "extra": "    def test_extra_selection_member(self):\n        pass\n\n" + signature,
        }
        for change, replacement in replacements.items():
            with self.subTest(change=change):
                self.altered_tests(signature, replacement,
                                   "functional", "Inconclusive execution")

    def assert_main_aborts(self, message, *, source=None, tests=None):
        if tests is None:
            tests = (mutation_demo.ROOT / "test_payment.py").read_text(encoding="utf-8")
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            (root / "payment.py").write_text(self.source if source is None else source,
                                             encoding="utf-8")
            (root / "test_payment.py").write_text(tests, encoding="utf-8")
            output = io.StringIO()
            with patch.object(mutation_demo, "ROOT", root), redirect_stdout(output):
                with self.assertRaisesRegex(RuntimeError, message):
                    mutation_demo.main()
            self.assertEqual(output.getvalue(), "", "Invalid evidence produced a report")

    def test_failing_original_baseline_aborts_without_a_report(self):
        original = (mutation_demo.ROOT / "test_payment.py").read_text(encoding="utf-8")
        signature = "    def test_provider_captures_exactly_35_ntd(self):"
        self.assertEqual(original.count(signature), 1)
        tests = original.replace(signature,
                                 signature + '\n        self.fail("baseline fixture failure")', 1)
        self.assert_main_aborts("Original program must pass first", tests=tests)

    def test_missing_or_ambiguous_mutation_target_aborts_without_a_report(self):
        target = "self.gateway.charge(order.order_id, order.amount_ntd)"
        self.assertEqual(self.source.count(target), 1)
        sources = {
            "missing": self.source.replace(target,
                                           "self.gateway.charge(order.order_id, (order.amount_ntd))", 1),
            "ambiguous": self.source + f"\n# A second textual match: {target}\n",
        }
        for change, source in sources.items():
            with self.subTest(change=change):
                self.assert_main_aborts("M1: mutation target is missing or ambiguous",
                                        source=source)

    def test_subprocess_timeout_aborts_without_a_report(self):
        output = io.StringIO()
        with patch.object(mutation_demo.subprocess, "run",
                          side_effect=subprocess.TimeoutExpired("payment test runner", 10)) as run:
            with redirect_stdout(output), self.assertRaises(subprocess.TimeoutExpired):
                mutation_demo.main()
        self.assertGreater(run.call_args.kwargs["timeout"], 0)
        self.assertEqual(output.getvalue(), "", "Timed-out evidence produced a report")

    def test_complete_report_preserves_the_observed_experiment(self):
        output = io.StringIO()
        with redirect_stdout(output):
            mutation_demo.main()
        reports = json.loads(output.getvalue())
        expected = [
            ("functional", 2, {"M1", "M6"}, 28.6),
            ("without-timeout", 8, {"M1", "M2", "M3", "M4", "M6", "M7"}, 85.7),
            ("full", 9, {"M1", "M2", "M3", "M4", "M5", "M6", "M7"}, 100.0),
        ]
        self.assertEqual([report["suite"] for report in reports],
                         [suite for suite, _, _, _ in expected])
        for report, (suite, count, killed, score) in zip(reports, expected):
            with self.subTest(suite=suite):
                self.assertTrue(report["baseline_passed"])
                self.assertEqual(report["baseline_tests"], count)
                self.assertEqual(report["killed"], len(killed))
                self.assertEqual(report["scored_mutants"], 7)
                self.assertEqual(report["excluded_mutants"], 0)
                self.assertEqual(report["mutation_score"], score)
                self.assertEqual(len(report["mutants"]), 7)
                self.assertEqual({row["id"] for row in report["mutants"]},
                                 {"M1", "M2", "M3", "M4", "M5", "M6", "M7"})
                for row in report["mutants"]:
                    detected = row["id"] in killed
                    self.assertEqual(row["status"], "killed" if detected else "survived")
                    self.assertEqual(bool(row["failing_tests"]), detected)


if __name__ == "__main__":
    unittest.main()
