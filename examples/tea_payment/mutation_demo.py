"""Execute seven hand-seeded mutants, one at a time, in disposable directories.

This is an article demonstration, not an automatic mutation engine or CI gate.
No network, gateway account, external package or real payment is involved.
"""
from pathlib import Path
import json
import subprocess
import sys
import tempfile


ROOT = Path(__file__).resolve().parent
MUTANTS = [
    ("M1", "charge 1 instead of the order amount",
     "self.gateway.charge(order.order_id, order.amount_ntd)",
     "self.gateway.charge(order.order_id, 1)"),
    ("M2", "skip the existing-attempt guard",
     "if order.order_id in self.attempts:", "if False:"),
    ("M3", "allow an idempotency key to move to another order",
     "if key in self.key_orders and self.key_orders[key] != order.order_id:", "if False:"),
    ("M4", "label a declined payment PAID",
     'replace(receipt, status="DECLINED")', 'replace(receipt, status="PAID")'),
    ("M5", "label a timed-out payment PAID",
     'replace(receipt, status="PENDING")', 'replace(receipt, status="PAID")'),
    ("M6", "put sweetened tea on the successful receipt",
     'replace(receipt, status="PAID", payment_id=payment_id)',
     'replace(receipt, status="PAID", payment_id=payment_id, sku="SWEETENED_GREEN_TEA")'),
    ("M7", "remove the pending record before the provider call",
     '        self.attempts[order.order_id] = Attempt(order, key, receipt)\n        try:',
     '        try:'),
]
EXPECTED_TESTS = {"functional": 2, "without-timeout": 8, "full": 9}
RUNNER = '''import io, json, os, sys, unittest
from pathlib import Path
sys.path.insert(0, os.getcwd())
import payment
import test_payment
if (Path(payment.__file__).resolve().parent != Path.cwd().resolve()
        or Path(test_payment.__file__).resolve().parent != Path.cwd().resolve()):
    raise SystemExit("Runner loaded modules outside the disposable directory")
suite = unittest.defaultTestLoader.loadTestsFromModule(test_payment)
tests = [test for group in suite for test in group]
timeout_id = "test_payment.ConstraintTests.test_timeout_stays_pending_without_another_charge"
if sum(test.id() == timeout_id for test in tests) != 1:
    raise SystemExit("Expected exactly one named timeout test")
if sys.argv[1] == "functional":
    tests = [test for test in tests if isinstance(test, test_payment.FunctionalTests)]
elif sys.argv[1] == "without-timeout":
    tests = [test for test in tests if test.id() != timeout_id]
result = unittest.TextTestRunner(stream=io.StringIO()).run(unittest.TestSuite(tests))
print(json.dumps({"tests": result.testsRun,
    "failures": [test.id() for test, _ in result.failures],
    "errors": [(test.id(), message) for test, message in result.errors],
    "skipped": len(result.skipped), "expected_failures": len(result.expectedFailures),
    "unexpected_successes": len(result.unexpectedSuccesses)}))
'''


def execute(source, suite):
    with tempfile.TemporaryDirectory(prefix="tea-payment-mutant-") as temp:
        folder = Path(temp)
        (folder / "payment.py").write_text(source, encoding="utf-8")
        (folder / "test_payment.py").write_text((ROOT / "test_payment.py").read_text(encoding="utf-8"), encoding="utf-8")
        process = subprocess.run([sys.executable, "-I", "-B", "-c", RUNNER, suite],
                                 cwd=folder, capture_output=True,
                                 text=True, encoding="utf-8", timeout=10)
        if process.returncode:
            raise RuntimeError(f"Runner failed, not a killed mutant:\n{process.stderr}")
        result = json.loads(process.stdout)
        if (result["errors"] or result["skipped"] or result["expected_failures"]
                or result["unexpected_successes"] or result["tests"] != EXPECTED_TESTS[suite]):
            raise RuntimeError(f"Inconclusive execution, not a killed mutant: {result}")
        return result


def main():
    source = (ROOT / "payment.py").read_text(encoding="utf-8")
    reports = []
    for suite in ("functional", "without-timeout", "full"):
        baseline = execute(source, suite)
        if baseline["failures"]:
            raise RuntimeError(f"Original program must pass first: {baseline}")
        rows = []
        for ident, description, old, new in MUTANTS:
            if source.count(old) != 1:
                raise RuntimeError(f"{ident}: mutation target is missing or ambiguous")
            result = execute(source.replace(old, new, 1), suite)
            rows.append({"id": ident, "change": description,
                         "status": "killed" if result["failures"] else "survived",
                         "failing_tests": result["failures"]})
        killed = sum(row["status"] == "killed" for row in rows)
        reports.append({"suite": suite, "baseline_tests": baseline["tests"],
                        "baseline_passed": True, "killed": killed,
                        "scored_mutants": len(rows), "excluded_mutants": 0,
                        "mutation_score": round(100 * killed / len(rows), 1),
                        "mutants": rows})
    print(json.dumps(reports, indent=2))


if __name__ == "__main__":
    main()
