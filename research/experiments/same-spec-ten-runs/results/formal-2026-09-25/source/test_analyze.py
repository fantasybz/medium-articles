"""Meaningful integrity and small-sample checks for the experiment analyzer."""

import hashlib
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch


_SPEC = importlib.util.spec_from_file_location("variance_analyze", Path(__file__).with_name("analyze.py"))
analyze = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(analyze)


class ExactIntervalTests(unittest.TestCase):
    def test_ten_successes_are_not_certainty(self):
        low, high = analyze.clopper_pearson(10, 10)
        self.assertAlmostEqual(low, 0.6915028921812392, places=12)
        self.assertEqual(high, 1.0)

    def test_zero_successes_use_two_sided_upper_bound(self):
        low, high = analyze.clopper_pearson(0, 10)
        self.assertEqual(low, 0.0)
        self.assertAlmostEqual(high, 0.30849710781876083, places=12)

    def test_interval_is_symmetric_at_five_successes(self):
        low, high = analyze.clopper_pearson(5, 10)
        self.assertAlmostEqual(low + high, 1.0, places=12)
        self.assertLess(low, 0.5)
        self.assertGreater(high, 0.5)


class CampaignTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        schedule = [{"run_id": f"b{block:02d}-{arm}", "arm": arm, "block": block}
                    for block in range(1, 11) for arm in analyze.ARMS]
        self.manifest = {"phase": "formal", "schedule": schedule}
        self.records = [{**item, "phase": "formal", "status": "no_output",
                         "cli_success": False, "artifact_success": False,
                         "accepted_completion": False, "artifact_sha256": None,
                         "code_path": None, "wall_seconds": 1.0, "usage": {},
                         "total_cost_usd": None} for item in schedule]

    def save(self):
        (self.root / "manifest.json").write_text(json.dumps(self.manifest), encoding="utf-8")
        (self.root / "records.jsonl").write_text(
            "".join(json.dumps(row) + "\n" for row in self.records), encoding="utf-8")

    def candidate(self, index, source, *, cli=False, artifact=False, status="candidate"):
        row = self.records[index]
        path = self.root / row["run_id"] / "candidate.py"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(source.encode("utf-8"))
        row.update({"code_path": str(path.relative_to(self.root)),
                    "artifact_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
                    "cli_success": cli, "artifact_success": artifact,
                    "accepted_completion": cli and artifact, "status": status})
        return path

    def seed(self, source):
        path = self.root / "source/seed/codex_jsonl.py"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(source.encode("utf-8"))
        self.manifest["task_provenance"] = {
            "seed_sha256": hashlib.sha256(path.read_bytes()).hexdigest()
        }
        return path

    def result(self):
        self.save()
        return analyze.analyze_campaign(self.root)

    def test_missing_record_refuses_incomplete_cohort(self):
        self.records.pop()
        with self.assertRaisesRegex(analyze.AnalysisError, "Missing scheduled"):
            self.result()

    def test_halt_refuses_intervals_even_with_all_forty_records(self):
        (self.root / "HALTED.json").write_text('{}')
        with self.assertRaisesRegex(analyze.AnalysisError, "Halted campaign"):
            self.result()

    def test_recorded_boundary_violation_refuses_intervals_without_halt_marker(self):
        # A hard kill may occur after the final ledger append but before HALTED.json.
        self.records[-1].update(status="boundary_failure", boundary_violation=True)
        with self.assertRaisesRegex(analyze.AnalysisError, "observed boundary violation"):
            self.result()

    def test_unsupported_python_has_clear_error_before_ast_work(self):
        with patch.object(analyze.sys, "version_info", (3, 9, 0)):
            with self.assertRaisesRegex(analyze.AnalysisError, "Python 3.10\\+"):
                self.result()

    def test_duplicate_record_is_not_an_extra_sample(self):
        self.records.append(dict(self.records[0]))
        with self.assertRaisesRegex(analyze.AnalysisError, "Duplicate record"):
            self.result()

    def test_unknown_record_is_not_silently_dropped(self):
        self.records.append({**self.records[0], "run_id": "unscheduled"})
        with self.assertRaisesRegex(analyze.AnalysisError, "Unknown record"):
            self.result()

    def test_assignment_mismatch_is_not_repaired(self):
        self.records[0]["arm"] = "C"
        with self.assertRaisesRegex(analyze.AnalysisError, "does not match"):
            self.result()

    def test_formal_schedule_requires_complete_randomization_blocks(self):
        self.manifest["schedule"][0]["block"] = 2
        with self.assertRaisesRegex(analyze.AnalysisError, "10 blocks"):
            self.result()

    def test_primary_and_artifact_outcomes_remain_distinct(self):
        self.candidate(0, "x = 1\n", cli=False, artifact=True, status="transport_error")
        self.records[4]["cli_success"] = True
        self.records[4]["status"] = "invalid_json"
        group = self.result()["arms"]["A0"]
        self.assertEqual(group["accepted_completion"]["successes"], 0)
        self.assertEqual(group["artifact_success"]["successes"], 1)
        self.assertEqual(group["cli_success"]["successes"], 1)
        self.assertEqual(group["accepted_completion"]["total"], 10)

    def test_report_contains_only_per_arm_outcomes(self):
        summary = self.result()
        self.assertEqual(summary["primary_outcome"],
                         "accepted_completion = cli_success AND artifact_success")
        self.assertNotIn("contrasts", summary)
        rendered = analyze.render_report(summary)
        self.assertNotIn("Prescheduled block contrasts", rendered)
        self.assertNotIn("percentage points", rendered)

    def test_inconsistent_success_flags_are_refused(self):
        self.records[0]["accepted_completion"] = True
        with self.assertRaisesRegex(analyze.AnalysisError, "must equal"):
            self.result()

    def test_pair_denominator_uses_only_two_parsed_artifacts(self):
        self.candidate(0, "def f(x):\n    return x + 1\n")
        self.candidate(4, "def g(y):\n    return y + 1\n")
        self.candidate(8, "def broken(:\n")
        summary = self.result()
        metric = summary["arms"]["A0"]["ast_similarity"]
        self.assertEqual(metric["produced_artifacts"], 3)
        self.assertEqual(metric["parsed_artifacts"], 2)
        self.assertEqual(metric["observed_pairs"], 1)
        self.assertEqual(metric["possible_pairs_if_all_parsed"], 45)
        self.assertEqual(metric["unavailable_reasons"]["parse_error:SyntaxError"], 1)
        pair = summary["pairwise_ast_similarity"][0]
        self.assertEqual(pair["cosine"], 1.0)
        self.assertTrue(pair["normalized_ast_equal"])
        self.assertEqual(summary["artifacts"][0]["function_count"], 1)

    def test_three_parsed_artifacts_produce_three_pairs(self):
        for index in (0, 4, 8):
            self.candidate(index, "x = 1\n")
        self.assertEqual(self.result()["arms"]["A0"]["ast_similarity"]["observed_pairs"], 3)

    def test_seed_cosine_reports_scaffolding_with_explicit_denominator(self):
        self.seed("def seed(x):\n    return x + 1\n")
        self.candidate(0, "def renamed(y):\n    return y + 1\n")
        self.candidate(4, "class Changed:\n    value = 7\n")
        self.candidate(8, "def broken(:\n")
        summary = self.result()
        self.assertEqual(summary["seed_ast_reference"]["status"], "available")
        self.assertEqual(summary["artifacts"][0]["seed_ast_node_type_cosine"], 1.0)
        self.assertLess(summary["artifacts"][4]["seed_ast_node_type_cosine"], 1.0)
        self.assertIsNone(summary["artifacts"][8]["seed_ast_node_type_cosine"])
        self.assertEqual(summary["artifacts"][8]["seed_similarity_na_reason"], "parse_error:SyntaxError")
        seed = summary["arms"]["A0"]["ast_similarity"]["seed_ast_node_type_cosine"]
        self.assertEqual(seed["observed"], 2)
        self.assertEqual(seed["missing"], 8)
        self.assertEqual(seed["max"], 1.0)
        self.assertGreater(seed["median"], seed["min"])
        self.assertIn("shared seed scaffolding", analyze.render_report(summary))

    def test_legacy_manifest_does_not_guess_a_seed(self):
        self.candidate(0, "x = 1\n")
        summary = self.result()
        self.assertEqual(summary["seed_ast_reference"]["status"], "not_available")
        self.assertIsNone(summary["artifacts"][0]["seed_ast_node_type_cosine"])
        self.assertEqual(summary["artifacts"][0]["seed_similarity_na_reason"], "seed_provenance_not_recorded")
        self.assertEqual(summary["arms"]["A0"]["ast_similarity"]["seed_ast_node_type_cosine"]["observed"], 0)

    def test_missing_declared_seed_refuses_analysis(self):
        self.seed("x = 1\n").unlink()
        with self.assertRaisesRegex(analyze.AnalysisError, "Frozen seed.*missing"):
            self.result()

    def test_changed_seed_refuses_analysis(self):
        self.seed("x = 1\n").write_text("x = 2\n", encoding="utf-8")
        with self.assertRaisesRegex(analyze.AnalysisError, "Frozen seed SHA-256"):
            self.result()

    def test_seed_symlink_is_not_followed(self):
        path = self.seed("x = 1\n")
        real = path.with_name("real.py")
        path.rename(real)
        path.symlink_to(real)
        with self.assertRaisesRegex(analyze.AnalysisError, "Symlink in frozen seed"):
            self.result()

    def test_empty_source_has_no_similarity_value(self):
        self.candidate(0, "# no implementation\n")
        group = self.result()["arms"]["A0"]["ast_similarity"]
        self.assertEqual(group["parsed_artifacts"], 0)
        self.assertIsNone(group["distribution"]["median"])
        self.assertEqual(group["unavailable_reasons"]["empty_module"], 1)

    def test_hash_mismatch_refuses_changed_sealed_artifact(self):
        path = self.candidate(0, "x = 1\n")
        path.write_text("x = 2\n", encoding="utf-8")
        with self.assertRaisesRegex(analyze.AnalysisError, "SHA-256 mismatch"):
            self.result()

    def test_missing_artifact_is_an_integrity_error(self):
        path = self.candidate(0, "x = 1\n")
        path.unlink()
        with self.assertRaisesRegex(analyze.AnalysisError, "sealed code file is missing"):
            self.result()

    def test_symlink_is_not_followed(self):
        path = self.candidate(0, "x = 1\n")
        real = path.with_name("real.py")
        path.rename(real)
        path.symlink_to(real)
        with self.assertRaisesRegex(analyze.AnalysisError, "symlink"):
            self.result()

    def test_parent_path_is_refused_before_reading(self):
        self.candidate(0, "x = 1\n")
        self.records[0]["code_path"] = "../outside.py"
        with self.assertRaisesRegex(analyze.AnalysisError, "inside campaign"):
            self.result()

    def test_failures_contribute_cost_and_missing_stays_unknown(self):
        self.records[0].update({"status": "timeout", "total_cost_usd": 1.25,
                                "wall_seconds": 900.0,
                                "usage": {"input_tokens": 42, "cache_read_input_tokens": 10}})
        self.records[4]["total_cost_usd"] = 0.0
        group = self.result()["arms"]["A0"]
        self.assertEqual(group["reported_cost_usd"]["total_observed"], 1.25)
        self.assertEqual(group["reported_cost_usd"]["observed"], 2)
        self.assertEqual(group["reported_cost_usd"]["missing"], 8)
        self.assertEqual(group["reported_usage"]["input_tokens"]["total_observed"], 42)
        self.assertIsNone(group["reported_usage"]["output_tokens"]["total_observed"])
        self.assertEqual(group["wall_seconds_observed"]["max"], 900.0)

    def test_conflicting_usage_aliases_refused(self):
        self.records[0]["usage"] = {"cache_read_input_tokens": 10, "cache_read_tokens": 20}
        with self.assertRaisesRegex(analyze.AnalysisError, "conflicting aliases"):
            self.result()

    def test_interrupted_slot_retains_primary_denominator_and_missing_time(self):
        self.records[0].update({"status": "interrupted", "wall_seconds": None})
        summary = self.result()
        group = summary["arms"]["A0"]
        self.assertEqual(group["accepted_completion"]["total"], 10)
        self.assertEqual(group["accepted_completion"]["successes"], 0)
        self.assertEqual(group["wall_seconds_observed"]["observed"], 9)
        self.assertEqual(group["wall_seconds_observed"]["missing"], 1)
        self.assertEqual(group["wall_seconds_observed"]["total_observed"], 9.0)
        self.assertIn("1.000 (9/10)", analyze.render_report(summary))

    def test_scheduled_pilot_is_excluded_from_formal_counts(self):
        pilot = {"run_id": "pilot-1", "arm": "A", "block": 0, "phase": "pilot"}
        self.manifest["schedule"].append(pilot)
        self.records.append({**self.records[0], **pilot})
        summary = self.result()
        self.assertEqual(summary["planned_runs"], 40)
        self.assertEqual(summary["other_phase_records_excluded"], 1)
        self.assertEqual(summary["arms"]["A"]["planned_runs"], 10)

    def test_pilot_campaign_does_not_pretend_to_be_formal(self):
        self.manifest = {"phase": "pilot", "schedule": self.manifest["schedule"][:2]}
        self.records = self.records[:2]
        for row in self.records:
            row["phase"] = "pilot"
        summary = self.result()
        self.assertFalse(summary["formal_evidence"])
        self.assertEqual(summary["planned_runs"], 2)
        self.assertIsNone(summary["arms"]["C"]["accepted_completion"]["rate"])
        self.assertIn("Pilot data", analyze.render_report(summary))

    def test_outputs_are_deterministic_and_show_exact_interval(self):
        for index in range(0, 40, 4):
            self.candidate(index, "x = 1\n", cli=True, artifact=True, status="completed")
        summary = self.result()
        analyze.write_outputs(self.root, summary)
        first = (self.root / "summary.json").read_bytes()
        self.assertIn("69.15%–100.00%", (self.root / "report.md").read_text())
        analyze.write_outputs(self.root, analyze.analyze_campaign(self.root))
        self.assertEqual(first, (self.root / "summary.json").read_bytes())


if __name__ == "__main__":
    unittest.main()
