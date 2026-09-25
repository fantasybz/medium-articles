# A bottle of tea: payment, review constraints and mutation testing

This is a runnable teaching example for the **綠燈不是驗收 / Green Is Not Done** series. The fictional order is one bottle of **無糖純喫綠茶 (unsweetened pure green tea)** for **NTD 35**. The price is illustrative. No real payment provider, network request, credential or external package is used. Python 3.10 or later is required.

From the repository root:

```bash
python3 -B -m unittest discover -s examples/tea_payment -p test_payment.py -v
python3 -B examples/tea_payment/mutation_demo.py
```

`payment.py` contains the checkout boundary. `test_payment.py` supplies a fake provider, two happy-path tests, and seven review-derived constraint tests. `mutation_demo.py` applies each of seven explicit source changes to a fresh temporary copy and runs three fixed test selections. It leaves the original files untouched and emits JSON including the failing test names.

## The agreed teaching contract

- `Order` represents an authorised, immutable order loaded by the server. Clients do not supply authoritative prices or SKU changes to this boundary. The demo fixture is one bottle for 35 whole New Taiwan dollars; it does not model tax, discounts or fractional amounts.
- The payment result preserves the order ID, SKU and amount. The provider receives the server order amount. `PAID` requires a successful provider response in this model.
- The same order and idempotency key reuse the existing result without another provider call. A key cannot move to another order, and an existing order cannot restart with a new key or changed contents.
- A declined attempt remains `DECLINED`. A timeout remains `PENDING`, because a provider may have captured the money before its response was lost. A replay returns the pending result; this demo does not automatically start another charge or resolve the uncertainty. Other provider exceptions propagate to the caller, but the pre-registered pending attempt remains: replay must not call the provider again.

The fake provider deliberately has **no deduplication**. It records attempted calls and successful captures separately. The timeout test covers both a request lost before capture and a response lost after capture. Another test covers a capture followed by a non-timeout connection error. This exposes an application-side retry bug instead of letting a helpful mock hide it.

## Observed mutation experiment

The first six mutants change the charged amount (M1), skip an existing attempt (M2), allow a key to move to another order (M3), mark a decline as paid (M4), mark a timeout as paid (M5), or change the receipt to sweetened tea (M6). M7 removes the pending record written before calling the provider.

| Selected tests | Original program | Killed / scored mutants | Score | Remaining issue |
|---|---|---|---|---|
| Two happy-path tests | 2 pass | 2 / 7 | 28.6% | M2, M3, M4, M5, M7 survive |
| Everything except the timeout test | 8 pass | 6 / 7 | 85.7% | M5 survives |
| Complete teaching suite | 9 pass | 7 / 7 | 100.0% | None of these seven survive |

These are **hand-seeded, executable, non-equivalent mutants**, not all mutations a tool could generate. There are zero excluded mutants in this example. The denominator stays seven in all three runs. Each run first checks that the original program passes its selected tests. A subprocess failure, timeout, zero-test result, test execution error, skipped test, expected failure, unexpected success or unexpected test selection aborts the experiment instead of being silently counted as a kill. Normal assertion failures identify killed mutants. Results are printed, not used as an automatic merge gate.

The saved [observed-mutations.json](observed-mutations.json) contains the executed results; rerunning the command reproduces them.

The 85.7% result is deliberately incomplete: M5 violates a critical requirement despite exceeding the series' illustrative 70% threshold. The 70% comparison is illustrative: a hand-selected set cannot directly inherit a threshold for tool-generated mutants on a real diff. A team reviews the surviving failure mode rather than accepting the average. The 100% result covers only these seven mutations and these fixtures.

The empty-key input guard is not included in the seven-mutant experiment. Neither the sample's 100% nor its selected tests claim exhaustive branch or input coverage. The runner's conservative error policy also differs from tools that classify test errors or timeouts as detected mutants; compare status definitions before comparing percentages.

## Boundary of the evidence

This implementation uses process-local dictionaries and **sequential calls**. It is not safe to deploy as a payment service. A second process or restart does not share its memory; concurrent calls are not made atomic. The demo does not establish exactly-once charging in production, implement provider idempotency, reconciliation, signed webhooks, durable payment state, database transactions, authorisation, fulfilment, refunds or recovery after a decline.

Production follow-up needs separate evidence: concurrent duplicate requests against a durable shared store; crashes before and after provider capture; provider-supported idempotency and its retention limits; reconciliation and duplicate/out-of-order webhook processing; protection against cross-account order access; and an authorised new-attempt policy after a decline. A receipt SKU is not proof that the physical drink was delivered.

## Why these are constraint tests

“Constraint” describes a test's **source and role**, not a mutually exclusive test technology. Reviewers chose a durable requirement, specified its observable failure, gave it an owner, and retained a check for future changes. A normal unit or integration test can also protect such a constraint. In this demo the requirements and comments are fictional teaching inputs, not a record of a real payment incident or PR review.

See [rules.md](rules.md) for the mapping from review concerns to tests, mutants and remaining integration work. A production repository would separately protect those approved rules and the runner from unreviewed changes; this example does not configure branch protection or claim that these files are immutable.

The mutation runner has twelve separate regression tests (not included in the nine payment tests or the score denominator):

```bash
python3 -B -m unittest discover -s examples/tea_payment -p test_mutation_demo.py -v
```
