import json
from pathlib import Path
import tempfile
import unittest

from campaign_status import status


class StatusTests(unittest.TestCase):
    def test_recorded_violation_is_incomplete_even_without_halt_marker(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            (root / "manifest.json").write_text('{"schedule":[{"run_id":"a"}]}')
            (root / "records.jsonl").write_text('{"run_id":"a","status":"boundary_failure"}\n')
            result = status(root)
            self.assertFalse(result["complete"])
            self.assertTrue(result["halted"])
            self.assertFalse(result["halt_marker_present"])
            self.assertTrue(result["boundary_violation_in_ledger"])

    def test_partial_campaign_preserves_unstarted_without_inventing_failures(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            (root / "manifest.json").write_text(json.dumps({"schedule": [{"run_id": "a"}, {"run_id": "b"}]}))
            (root / "a").mkdir()
            (root / "a/generation.json").write_text('{}')
            (root / "HALTED.json").write_text('{}')
            result = status(root)
            self.assertFalse(result["complete"])
            self.assertEqual(result["counts"], {"generated_not_scored": 1, "not_started": 1})
            self.assertEqual(result["recorded"], 0)

    def test_unknown_or_duplicate_rows_are_not_silently_collapsed(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            (root / "manifest.json").write_text('{"schedule":[{"run_id":"a"}]}')
            for data in ['{"run_id":"unknown","status":"completed"}',
                         '{"run_id":"a","status":"completed"}\n{"run_id":"a","status":"completed"}']:
                (root / "records.jsonl").write_text(data)
                with self.assertRaises(ValueError):
                    status(root)


if __name__ == "__main__":
    unittest.main()
