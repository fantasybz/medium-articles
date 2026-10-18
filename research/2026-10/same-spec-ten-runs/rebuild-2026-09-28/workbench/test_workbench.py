"""驗證教學 oracle 不會自行放寬或新增 R03 的要求。"""

import unittest

from workbench import Expected, Observed, grade


class ContractOracleTests(unittest.TestCase):
    def test_accepts_different_nonempty_reasons(self):
        expected = Expected("", (3,), 6)
        for reason in ("bad text", "必須提供字串", "value 0 is invalid"):
            with self.subTest(reason=reason):
                observed = Observed("", f"[codex malformed event] line 3: {reason}\n", 6)
                self.assertTrue(grade(expected, observed)["passed"])

    def test_rejects_missing_extra_empty_multiline_and_wrong_line_diagnostics(self):
        expected = Expected("", (3,), 6)
        invalid = ("", "[codex malformed event] line 3: \n",
                   "[codex malformed event] line 1: bad\n",
                   "[codex malformed event] line 3: bad\nextra\n",
                   "[codex malformed event] line 3: bad\rreason\n")
        for stderr in invalid:
            with self.subTest(stderr=stderr):
                self.assertEqual(grade(expected, Observed("", stderr, 6))["mismatches"], ["stderr"])

    def test_every_outlet_can_fail_independently(self):
        expected = Expected("review\n", (), 0)
        observations = ((Observed("debug\nreview\n", "", 0), "stdout"),
                        (Observed("review\n", "unexpected\n", 0), "stderr"),
                        (Observed("review\n", "", 6), "returncode"))
        for observed, channel in observations:
            with self.subTest(channel=channel):
                self.assertEqual(grade(expected, observed)["mismatches"], [channel])


if __name__ == "__main__":
    unittest.main()
