# Review-derived constraints for the teaching case

All comments and owners below are **illustrative roles**, not historical PR evidence. “Owner” means a human payment-domain maintainer would approve and maintain the rule in a real team. Revisit a rule when its payment contract, provider behaviour or retry/reconciliation design changes; absence of recent failures alone does not make a safety rule obsolete.

| Rule | Accepted concern and observable requirement | Check in `test_payment.py` | Targeted mutant | Human responsibility |
|---|---|---|---|---|
| C1 | Replaying an existing order/key must not create another provider call or capture; reuse the result | `test_same_attempt_is_not_charged_twice` | M2 | Payment owner approves retry semantics |
| C2 | Reject rebinding a key to another order, a new key to an existing order, or changed order contents before another provider call | `test_key_cannot_move_to_another_order`, `test_new_key_cannot_restart_the_same_order`, `test_order_contents_cannot_change_during_replay` | M3 exercises cross-order rebinding; M2 also exposes skipped existing-order validation | Payment owner owns the identity boundary; security reviewer examines account authorisation separately |
| C3 | A provider decline must not produce a paid result or an additional provider call | `test_declined_payment_is_not_paid` | M4; M2 causes another provider call | Payment owner defines declined-attempt recovery outside this demo |
| C4 | A timeout before/after capture or an uncaught provider error preserves a pending attempt; replay must not send another charge | `test_timeout_stays_pending_without_another_charge`, `test_unexpected_provider_error_preserves_pending_attempt` | M5; M2 causes another charge; M7 loses the pending record on an uncaught provider error | Payment owner and operations owner define durable reconciliation before deployment |

The two functional tests check the purchased SKU/receipt and actual captured amount (M6 and M1). Those are also durable business requirements. The separate test classes make the narrative easier to follow; they do not imply functional requirements and constraints cannot overlap.

The mapping above identifies relevant mutations, not independent proof for every test. M2 is killed by multiple tests. Replacing C1’s replay test and C2’s new-key/changed-order tests with empty bodies in an isolated copy leaves all three aggregate scores unchanged. A 7/7 result therefore cannot establish that those individual assertions are effective. Review the assertions and failing-test mapping, and isolate a constraint test against a known violating version when that evidence is needed.

## Choosing from review comments

Retain a test when the comment identifies a consequential failure, describes a requirement expected to survive this PR, has a stable observable oracle and a maintainable test boundary, and has a human owner. Do not require an incident to happen twice before retaining a high-impact rule.

- “Could a second click charge the order twice?” becomes C1, with two calls and a one-capture expectation.
- “Could the retry key accidentally be regenerated or reused?” becomes C2, with explicit conflict and no new provider call.
- “Can a timeout already have charged the customer?” becomes C4, covering both capture-then-timeout and a timeout before any side effect.
- “Rename this local variable” remains ordinary code feedback unless an established convention belongs in a formatter/linter.
- “Should this campaign offer refunds?” first needs a product/payment policy decision. An agent cannot manufacture the expected answer and then call it an approved constraint.

Select mutation targets from the implementation that enforces these risks. Mutate `payment.py`, not the test assertions, fake provider or mutation runner. Keep the candidate program, fixtures, scope and seven-mutant denominator fixed while comparing the three test selections. A surviving mutant requires a concrete counterexample or a justified equivalence analysis; “we do not test that input yet” is not proof of equivalence.
