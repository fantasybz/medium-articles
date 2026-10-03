<!--
Medium 發布指南（此註解區塊不要貼進 Medium）

自動化：`./tools/medium_draft.sh <article-dir> en` 會建好草稿並比對內容，停在發布前一步。
細節見 repo 根目錄的 PUBLISHING.md。以下是手動流程與發布後必做的收尾。

【系列狀態】以各篇 publish/PUBLISHED.md 為準。Medium 限制同一作者 24 小時內最多發布或排程 2 篇，
見 PUBLISHING.md 的〈發文數量上限〉。

【手動流程】
1. 開新 story：https://medium.com/new-story
2. 貼上下方內容（從標題那行開始，不含本註解）。
3. 看到 📌【在此插入…】的行：刪掉該行，按 + 插入同目錄 images/ 裡對應的 PNG。
4. code block：在 Medium 選取後按 ``` 轉成 code block。
5. 封面圖選流程圖，不要選表格截圖（縮到卡片尺寸看不清）。
6. Tags 建議：AI, Software Engineering, Engineering Management, Agentic AI, DevOps

【發布後收尾—不做的話系列會斷】
7. 記下本篇 Medium URL，補進 repo 的 README 索引與 publish/PUBLISHED.md。
8. 把本篇兩處的系列連結換成真正的 Medium URL：
   (a) 開頭「系列導覽」那一行
   (b) 文末「系列文章」清單
   （尚未發布的篇在這裡是純文字「（即將發布）」，不是相對路徑；上線後換成真正的 URL）
9. 回頭編輯已發布的其他篇，把指向本篇的連結補上。
-->

# Green Is Not Done, Part 4 — A Payment Walkthrough: Buying Unsweetened Green Tea, from Review Constraints to Mutation Score

> **TL;DR** — You want to buy a bottle of unsweetened pure green tea, but the payment screen has stopped responding. Will pressing again charge you twice? Starting with an illustrative NTD 35 order, this walkthrough follows human review, constraint selection, test design and interpretation of results. Deliberately breaking the payment code to see whether tests fail is mutation testing: a way to examine their fault-detection ability. The runnable Python example explains why 85.7% can still miss a critical error, and what 100% actually supports. We then return the evidence to the reviewer and identify the verification still needed for a real payment service.

> Series: [Overview: Green Is Not Done](https://medium.com/p/c4fc9f3d8581) → [1. Testing](https://medium.com/p/51d001a6dcd5) → [2. Review](https://medium.com/p/4d36d0f2f9c1) → [3. Reliability](https://medium.com/p/4b6d147bff0d) → **4. Payment Walkthrough (this piece)**. This article stands on its own; the overview and first three parts provide the research background and organizational design.

---

## 1. First, agree on what buying that bottle means

Imagine a small, familiar situation. You choose a bottle of 無糖純喫綠茶, unsweetened pure green tea, check the amount and press Pay. The screen spins for a while. It reports neither success nor a clear failure. Your finger hovers over the button. Would another press retrieve the previous result, or start a second payment?

This is a teaching scenario, not an incident from my work or a description of a particular merchant. The **NTD 35 price is illustrative**, not a claim about the product's actual price. Amounts are integer New Taiwan dollars; discounts, tax, other currencies and change are outside this example.

I want this bottle of tea to make the abstract terms observable. The buyer's expectations are concrete: the order contains unsweetened tea, the amount is NTD 35, pressing Pay again does not charge them twice, and the merchant does not issue a successful receipt while the payment result remains unknown.

When a payment request receives no response and is sent again, we want the code to find the original attempt and return its saved result without sending another charge. This is the idempotency requirement protected in this example. The code first needs a way to recognize the same operation: the SKU identifies which tea, `order_id` identifies the order, and `key` identifies this payment attempt, hence the name idempotency key. The key supplies identity; the code must still check and reuse its records to prevent another charge. The example begins with an authorized order loaded by the server. An arbitrary price submitted by the browser is not authoritative input to this boundary.

Pressing the button again can also mean buying another bottle. Resending a request that received no response should retain the original order and key; another purchase needs another order and payment attempt. Both purchases can have the same SKU and NTD 35 amount, so product and price alone cannot identify a replay. Conversely, a system that looks only at the key could mistake a retry for a new payment if every click generates a new key. This example therefore also checks the order: an order with an existing attempt cannot restart by changing its key. Section 3 labels these requirements so we can connect the agreements with their tests.

```python
# Illustrative data: an authorized, immutable server-loaded order.
# Full code: examples/tea_payment/. No real provider is called.
order = Order(
    order_id="tea-001",
    sku="UNSWEETENED_PURE_GREEN_TEA",
    amount_ntd=35,
)
key = "buy-tea-001"
```

The payment contract is this set of agreed outcomes: people establish what each operation should do before asking the agent to implement it. A normal payment sends the order amount to the payment service provider and returns `PAID` after a successful response. The receipt preserves the order, SKU, amount and payment identifier. Repeating the same order and key returns the existing result without another charge request. A key cannot move to another order. An order with an existing attempt cannot start again by changing its key or contents.

A decline and a timeout mean different things. An explicit decline is `DECLINED`. A timeout means a definite response did not arrive; the provider might already have captured the money, so the result remains `PENDING`. This demo does not automatically charge again after a timeout or implement lookup and reconciliation. Those need a separately designed and verified recovery path.

The example also specifies that unclassified provider exceptions propagate to the caller. Checkout must not turn them into a claim of payment success or failure. The recorded attempt remains `PENDING`, so replay does not call the provider again. Later tests protect this agreement alongside the timeout behavior, preserving both the error that needs investigation and the record needed for replay. The caller's error presentation and recovery flow are outside this implementation.

These are the example's agreed behaviors, not universal payment API state names. [Stripe's error-handling documentation](https://docs.stripe.com/error-handling#connection-errors) likewise treats connection errors as indeterminate, but its idempotency contract permits safe retries with the same key. This demo has no provider-side idempotency implementation, so it retains a pending result. The distinction is the guarantee supporting the retry. The conservative teaching policy should not become a blanket rule that real payment systems must never retry.

---

## 2. Choose the reviewers, then decide where they need to read deeply

Suppose an agent submits a change for merging into the project, a pull request or PR, saying: “The payment API now supports retries; identical requests receive the existing result.” That statement describes the change's intent. The reviewer's next task is to examine whether the code and tests support that promise. Knowing what the author wanted to do does not establish that the implementation does it.

I would first identify the responsibilities touched by the change: order identity, amount, provider calls, payment state and the tests used to accept them. Shared payment logic can affect many orders. The fact that this bottle costs only NTD 35 does not make the change low risk. Conversely, a documentation-only correction that does not affect the payment path should not require the same scrutiny merely because its directory is named `payment`.

Here is my suggested allocation for this payment-logic PR. The payment owner confirms the agreement. The test reviewer examines the prepared orders and scenarios (fixtures), the statements judging results (assertions), and whether deliberately faulty versions (mutants) are detected. The integration reviewer checks how far that evidence extends to a real service. A person with the relevant competence may cover more than one role; the aim is clear responsibility, not a quota of job titles.

📌【在此插入表 table-01.png】

A reviewer agent can organize the diff, locate charge calls and exception handling, or propose counterexamples. It cannot approve the payment contract on its own or turn its own approval into human authorization. Following the Review article's recommendation, high-risk payment logic needs approval from a responsible, qualified person other than the task assigner.

At the code level, a diff shows what changed, and a hunk is one block of those changes. I would prioritize the existing-attempt check, the amount sent to the provider, the conversion of exceptions into payment states, and connected callers. For example, the condition that returns early when an attempt already exists is a guard against another charge. Moving it after the charge would make it too late to protect the payment, even if the condition itself were unchanged. Reading only the highlighted line is therefore insufficient: inspect the check's position, the value's source and the handling of exceptions. Review test and verification-configuration changes as well, so weakened assertions cannot manufacture a green result.

Consider the timeout branch. The reviewer sees an exception handler, then needs to work out what that exception establishes. First, look outward: does a timeout from `charge()` guarantee that no money was captured? This example provides no such guarantee. Next, look inward: if the code assigned `PAID` here, what evidence would support it, and did it receive a payment identifier? Without a successful response and payment identifier, “paid” promises more than the application knows. Only then return to the tests: does any case produce this uncertain outcome and check the reported state? Following that path reveals a missing scenario, rather than a need for more assertions on the happy path.

The three review responsibilities now connect. The payment owner confirms that an unknown result stays `PENDING`. The QA reviewer makes loss of the response before or after capture observable in a test. The integration reviewer asks how the real provider's result will be recovered and who handles payments that remain unresolved. Those judgments can emerge in one discussion. Recording only “tests passed” would leave the next person guessing which questions were actually settled.

[Google's Code Review guidance](https://google.github.io/eng-practices/review/reviewer/looking-for.html) asks reviewers to understand their assigned code, read wider context when needed and involve qualified reviewers for specialized concerns. The three responsibilities above are my application to this payment case, not a Google requirement to assemble three people. The approval record should say who reviewed the tests and who checked the payment-state decisions.

If the only evidence is happy-path testing, I would begin with a close review of the relevant diff and identify missing constraints. Once reports actually cover those requirements, there is a basis for adjusting future review depth. Removing that attention first leaves the score trying to stand in for questions nobody has answered.

---

## 3. Which Review comments deserve a lasting test?

Now imagine several reviewer comments. These are teaching inputs, not comments copied from a real PR.

One asks whether clicking twice on the same order could send two charge requests. Another asks what happens if a retry regenerates the key or reuses it for another order. A third points out that money might have been captured before the timeout. Two more suggest renaming a local variable and ask whether the campaign should offer refunds.

All may be useful, but they call for different next steps. I would ask what consequence a comment identifies, whether the requirement must survive later changes, who can confirm the expected result, and whether a stable, maintainable test can observe it. Those questions matter more than comment length, popularity or whether an incident has already occurred. The table labels the retained payment requirements C1 through C4 so we can connect the comments, tests and later experiment. These are rule labels for this example, not four built-in kinds of test.

📌【在此插入表 table-02.png】

A consequential requirement can deserve protection the first time it appears. There is no reason to wait for a second incorrect charge before calling it a recurring rule. A temporary migration restriction, by contrast, may need a check with an expiry condition rather than a permanent place in CI.

A selected comment also needs a traceable rule record. For C4, the source is the lost-response risk in this illustrative Review. Its scope is the payment attempt and its replay. Its requirement is to retain an unknown result after timeout, without reporting success or automatically sending a new charge. The timeout test is `test_timeout_stays_pending_without_another_charge`. C4 also includes the unclassified-exception behavior specified in section 1: `test_unexpected_provider_error_preserves_pending_attempt` checks propagation, retention of the early record and replay without another charge. A payment owner maintains the rule, and a change to the provider contract or reconciliation design triggers reconsideration.

A real team should attach the actual PR, requirement or incident. An owner field lets the next reviewer find someone who can explain or change the expected result. A long period without failures is not, by itself, a reason to remove a payment safety rule. The rule's continuing protection may be why the mistake has stayed out.

The most consequential step from comment to rule is defining the expected result. “Please handle timeouts” leaves several answers open: report failure, charge again or wait for a lookup. An agent could plausibly implement any of them. C4 needs to specify that the first timed-out call returns `PENDING` without a successful payment identifier; replay returns the same result and the provider-call count remains one. That gives everyone an answer they can inspect together.

Keep both timeout scenarios. Timeout before capture prevents us from treating uncertainty as proof that money moved. Timeout after capture prevents us from treating an exception as proof that nothing happened. Both produce the same application state because the application has the same information, even though the provider's internal outcomes differ. If lookup is added later, the owner should define which new evidence permits `PENDING` to become a definite result and add the corresponding tests. The rule can evolve with the contract, with the reason for the change preserved.

---

## 4. Turn the constraints into tests that distinguish incorrect behavior

The preceding section established that replaying a payment must not charge it again. The next step is to check that later changes continue to honor that requirement. A repeatable test retaining that agreement is what this article calls a constraint test. **The name describes the constraint it comes from and the behavior it preserves, not a technology mutually exclusive with functional testing.** Preventing a duplicate charge is also product functionality. A unit test can examine payment logic in isolation; an integration test can connect it with components such as storage and the provider interface. Choose the method according to the evidence needed. Reporting the tests separately helps trace the retained review requirement and its maintenance responsibility; it does not mean they protect disjoint behavior.

To compare test selections, begin with the example's two happy-path tests: the receipt preserves the unsweetened SKU, NTD 35 and payment identifier; the fake provider receives and captures exactly NTD 35. Then include seven more test methods covering C1's replay, C2's three identity conflicts, and C3/C4's decline, timeout and unclassified exception, represented here by ConnectionError. One rule can require several test methods; rule count and test count need not match.

The tests do not charge a real card. They give the payment code a fake provider, `FakeGateway`, whose behavior the test controls; an object standing in for an external service this way is a test double. It can return success, decline the payment or simulate a lost response. The prepared order and provider scenario form the fixture for this test. The fake records attempted `calls` separately from successful `captures`, because receiving a request does not establish that money was captured. It **deliberately does not deduplicate**: if the fake suppressed a second request on its own, the test might conceal a missing application check.

This first excerpt from `ConstraintTests` calls the payment code, `Checkout.pay()`, twice with the same order and key. The following `assertEqual` statements are assertions: they compare the actual result with the agreed answer and fail the test when the two differ. The test examines both the receipts and the side effects of paying: whether an additional charge request or capture was recorded. The expected NTD 35 comes directly from the agreed example, without asking the system under test to calculate its own expected answer.

```python
def test_same_attempt_is_not_charged_twice(self):
    gateway = FakeGateway()
    checkout = Checkout(gateway)
    first = checkout.pay(tea_order(), "buy-tea-001")
    second = checkout.pay(tea_order(), "buy-tea-001")
    self.assertEqual(second, first)
    self.assertEqual(gateway.calls, [("tea-001", 35)])
    self.assertEqual(gateway.captures, [("pay-1", "tea-001", 35)])
```

Equal receipts alone would be weak evidence. Code could charge again and then return the old receipt. Checking calls and captures detects that side effect. An assertion such as `assert checkout.pay(...)` would be weaker still: any nonempty result could pass without preserving the behavior that matters.

The next test protects the key boundary. A second order is not a replay of the first. The conflict must be rejected before another charge is sent.

```python
def test_key_cannot_move_to_another_order(self):
    gateway = FakeGateway()
    checkout = Checkout(gateway)
    checkout.pay(tea_order(), "buy-tea-001")
    with self.assertRaises(PaymentConflict):
        checkout.pay(tea_order("tea-002"), "buy-tea-001")
    self.assertEqual(gateway.calls, [("tea-001", 35)])
```

The timeout fixture deserves particular attention. The complete test covers both a timeout before capture and **a successful capture followed by a lost response**. The following version isolates the latter, simplified from the full test, which uses `subTest` for both cases. Because the application cannot know whether capture completed, it returns `PENDING`. Replaying the request finds the same pending result without another charge.

```python
def test_timeout_stays_pending_without_another_charge(self):
    gateway = FakeGateway("timeout_after_capture")
    checkout = Checkout(gateway)
    first = checkout.pay(tea_order(), "buy-tea-001")
    second = checkout.pay(tea_order(), "buy-tea-001")
    self.assertEqual(first.status, "PENDING")
    self.assertIsNone(first.payment_id)
    self.assertEqual(second, first)
    self.assertEqual(gateway.calls, [("tea-001", 35)])
    self.assertEqual(gateway.captures, [("pay-1", "tea-001", 35)])
```

One capture but no payment ID in the receipt is an intentional asymmetry. The test can inspect the fake's internals; the application can only act on the response it receives. Knowing the fixture captured money does not justify asking the application to claim success after losing that response.

Start by checking whether the arranged scenario reaches the payment code: both requests pass through `Checkout.pay()`. Then confirm that the expected answer comes from the agreed C4 contract, independently of the implementation's current return value. Finally, examine how the assertions observe the promise and the side effect. They check `PENDING`, the absent payment identifier, the unchanged replay result and the single provider call. Omitting either side can leave part of the requirement unprotected.

For example, comparing `first.status` with `second.status` also appears to test replay, but it passes if both incorrectly return `PAID`. The expected value needs an independent source. Likewise, if the fake silently returns an old result on a second call, `captures` may still contain one entry even though the application called twice. Recording `calls` separately from `captures` lets that mistake become visible before the test judges it.

---

## 5. Read the payment response logic before deliberately breaking it

The example stores payment attempts in memory. It first checks whether a key belongs to another order, then whether this order already has an attempt. An existing attempt requires matching key and order contents and returns the saved result. Only a new, valid attempt calls the provider, after first recording `PENDING`.

The excerpt below handles the charge and its outcome; the linked implementation contains the guards and data structures. These lines deserve close review because a convenient exception handler can turn “unknown” into “paid.”

```python
try:
    payment_id = self.gateway.charge(order.order_id, order.amount_ntd)
except Declined:
    receipt = replace(receipt, status="DECLINED")
except TimeoutError:
    receipt = replace(receipt, status="PENDING")
else:
    receipt = replace(receipt, status="PAID", payment_id=payment_id)
```

Follow the different responses through this diagram. It shows what this example can know at the payment boundary, not the provider's entire transaction lifecycle.

📌【在此插入圖 diagram-01.png】

The branch that retains `PENDING` has no direct arrow to `PAID`. Lookup and reconciliation require new evidence, and this demo does not implement them. Saving a pending attempt gives recovery a defined starting point. Leaving it unresolved forever would not complete the payment flow.

Now follow capture followed by a lost response in time. Checkout records the attempt, then calls the provider. The fake records a successful capture and raises `TimeoutError`; Checkout returns `PENDING`. When the same request arrives again, the existing attempt is found before another provider call. Safe replay depends on what has already been recorded and where that record is checked.

One detail is easy to miss. For the handled `TimeoutError`, the code also writes the attempt after exception handling. Removing the pre-call record can therefore leave timeout-only checks green. To protect the requirement that the record exists before the call, we need an exception that skips the later write. The full example uses `error_after_capture`: the fake records a capture, then raises `ConnectionError`, which neither of the two handlers catches.

The first call propagates that `ConnectionError`, which the test explicitly expects. On the second call with the same order and key, the early record still exists, so Checkout returns `PENDING` without calling the provider. Remove that record and the second call reaches the charge again, allowing the test to distinguish the change. This case protects a requirement that must survive an interruption to control flow.

This part is grounded in the example's development record. An independent Claude Code review identified the missing non-timeout exception test for the early `PENDING` record; the subsequent revision added that case and M7, the mutation that removes the pre-call record. The initial tests and mutants had not fully exposed the risk. Independent Review contributed a question the original selection had missed, and an executable test retained the resulting requirement. The requirement comes from the teaching contract stated in section 1; a real team still needs its responsible people to confirm that contract. The model identified the testing gap. Execution then established the test's ability to distinguish this contract violation, M7, rather than establishing that the contract itself was appropriate.

Having tests still leaves a question: would they object to incorrect behavior? If we deliberately change the timeout result from `PENDING` to `PAID`, will the test protecting an unknown outcome fail? Making one change in a copy of the program and checking whether the tests notice is mutation testing; the changed version is a mutant. First verify that the original program passes, then change one thing and run the same tests. A failure of the expected behavioral assertion now means that the tests detected the selected error, called a killed mutant. Discard the copy afterward, leaving the original code intact.

The program that creates the copies, executes the tests and assembles the results is the runner. This simplified runner labels every undetected mutant survived. That says only that the selected tests did not detect it. Because the runner does not measure code coverage, it also includes branches the tests never execute. Tools with coverage information can distinguish NoCoverage from Survived, meaning executed but undetected. Keep that classification limit attached to the scores that follow.

---

## 6. Select mutation scope from the Review risks

The third selection is deciding which code and mutations deserve execution. I start with the agreed payment requirements and locate the code that enforces them: charge amount, existing-attempt guard, key binding, exception handling and receipt contents.

Only `payment.py` is mutated. Assertions, fixtures, `FakeGateway` and the mutation runner remain unchanged. Changing the question or the judge at the same time would undermine the experiment. If a real PR changes a shared payment helper, affected tests must follow its callers. “Diff-scoped” does not mean the surrounding behavior no longer matters.

Earlier industrial research offers a reference for this approach to controlling scope. Google's [Practical Mutation Testing at Scale](https://research.google/pubs/practical-mutation-testing-at-scale-a-view-from-google/) (2021) describes mutation during Code Review on changed code, filtering less useful mutants and selecting operators using historical performance. It supports considering cost and actionable results together. It does not validate this article's seven mutants or a 70% threshold.

For an experiment the reader can inspect individually, this example **hand-seeds seven mutants**. They are executed changes, not a complete set automatically generated by Stryker, PIT or mutmut, and they do not cover every possible payment defect.

📌【在此插入表 table-03.png】

Each selected change has an operation that exposes a behavior difference: for example, M5 returns a different state from the original program after a timeout. Some code changes can instead preserve every observable behavior within the agreed input domain. Those are equivalent mutants; failure to find a difference with the current tests does not establish equivalence. None of these seven falls into that category, so no equivalent mutants are excluded here. With a full tool, record its version, the mutation operators defining which changes it makes, file scope and test selection. Separate compile failures, no coverage, timeouts and confirmed equivalence. For example, [Stryker's metrics](https://stryker-mutator.io/docs/mutation-testing-elements/mutant-states-and-metrics/) count both killed mutants and timeouts as detected, while valid mutants with no coverage remain in the ordinary mutation-score denominator. Dropping both timeouts and uncovered mutants as “invalid” would change the meaning of a comparison.

Both selecting mutations and interpreting survivors require an operation that distinguishes the original program from the incorrect version. M2 needs two calls on the same order, with an observation of whether a charge happens again. M5 needs the provider to raise a timeout, followed by a check that the receipt remains pending. The complete test includes timeouts before and after capture, so uncertainty does not silently become proof that money moved. These defects need different inputs and assertions. Five more `PAID` assertions on a normal purchase would reach neither.

A survivor does not always mean “add a test immediately,” either. First establish whether the behavior belongs to the promised scope and whether a person has confirmed the expected result. If refund policy remains undecided, a test would merely freeze an answer nobody has agreed on. C4 already has a clear contract, so M5's survival points directly to missing verification. Review supplies the basis for interpreting the mutation result and deciding what to do with it.

When no counterexample is apparent, distinguish undefined requirements, unreachable inputs, test gaps and actual behavioral equivalence. “We do not test that input” is not an equivalence proof. [Stryker's equivalent-mutant guidance](https://stryker-mutator.io/docs/mutation-testing-elements/equivalent-mutants/) also explains the limits of automatic determination. Any exclusion needs its input domain, reason and review recorded. A consequential surviving mutation must be resolved or explicitly accepted before approval, not hidden inside the average.

---

## 7. Follow the 85.7% green result to a test that actually fails

All seven mutated programs are executable and non-equivalent, so this experiment keeps a denominator of seven. Its mutation score is the number detected by tests divided by seven, multiplied by 100%. The denominator counts mutants, not tests. It is not the probability that the product has no bugs.

The accompanying `mutation_demo.py` was executed with three test selections. The original program passed each selection before the mutations ran. Start with the overall results, then follow M5 in the second row to the missing evidence.

📌【在此插入表 table-04.png】

The first two tests are real and exercise payment. They simply do not demand correct handling of replay, key conflicts, declines or timeouts. The locations changed by M2, M3 and M7 execute without the tests distinguishing the defects. That is the extra question mutation asks beyond “did this line run?” M4 and M5 never enter their exception branches; branch coverage alone could also reveal those gaps.

The second row detects six mutants. If a team used only the Testing article's suggested 70% starting threshold, 85.7% would clear it. Yet the surviving M5 changes exactly the behavior C4 protects. Here is its actual single-line replacement; the rest of the program and tests remain unchanged:

```diff
 except TimeoutError:
-    receipt = replace(receipt, status="PENDING")
+    receipt = replace(receipt, status="PAID")
```

All eight tests still pass for a straightforward reason: none arranges a provider timeout, so execution never enters that branch. Read their green result again with this in mind. They confirm their arranged cases. They do not answer whether an unknown payment will be reported as successful. Execution without an error cannot answer a question the suite never asked. A full tool with coverage information would classify this as NoCoverage; under the Stryker definition discussed earlier, it remains in the ordinary mutation-score denominator. The lesson is that someone still needs to examine this unanswered question after the aggregate clears its threshold.

Now restore the timeout test from section 4 and use that same test against M5 and the original program. A separate isolated run executed only that test method. The following excerpt omits the full test-name prefixes, tracebacks and elapsed time, and shows the identical assertion message only once. It retains both scenarios and the counts:

```text
# M5: two subTests arrange timeout before and after capture
(outcome='timeout_before_capture') ... FAIL
(outcome='timeout_after_capture') ... FAIL
AssertionError: 'PAID' != 'PENDING'
Ran 1 test
FAILED (failures=2)

# Same test, original payment.py restored
Ran 1 test
OK
```

This is **one test method with two failing subTests**, not two additional payment tests. The full suite still contains nine methods. The failure is the assertion on `first.status`: the changed program returns `PAID`, while the contract requires `PENDING`. It is not an import error, a broken environment or a failure to collect the test. The same method passes against the original program. We can now trace the requirement, input and assertion that distinguish M5.

This checks a test's ability to identify a known incorrect version. It does not establish a historical TDD sequence for the feature PR. Running the full nine-test suite detects all seven specified mutants, producing 100%. The supported conclusion remains specific: the selected tests detect those seven changes. Concurrency, restarts and provider integration still require their own cases and evidence.

**Clearing an aggregate threshold cannot offset an unverified payment constraint.** The 70% comparison illustrates what an aggregate can hide. Seven hand-selected mutants differ from the set a full tool generates across changed code; this small denominator cannot calibrate a universal threshold for a real repository.

### Why read individual results even at 100%?

The next table is derived from the full experiment's JSON. Each row represents one test method. A dot means at least one assertion or subTest in that method failed for the mutant; a dash means it did not distinguish the change. This is a failure matrix, not a coverage measurement. A dash does not necessarily mean the changed code was never executed.

📌【在此插入表 table-05.png】

Follow the M5 column first. Only the timeout method detects it, which explains the gap when that method is omitted. Now look at M2. Several methods detect it: although they check declines, replay or exceptions, they all encounter the existing-attempt guard. If one constraint test loses its assertions, another can still detect M2 and keep the aggregate unchanged.

This was also tested, rather than inferred only from the table. In an isolated copy, the C1 replay method and the C2 methods labeled “Reject new key on same order” and “Preserve order during replay” were replaced with empty `pass` bodies. The three scores remained 28.6%, 85.7% and 100%. The official example retains its assertions. This counterexample exposes a limit of the aggregate: unittest still counts empty methods, and other cases still detect M2, so neither “nine tests” nor “100%” reveals that three methods have lost their content.

After receiving the report, a reviewer therefore still needs to inspect the input and assertions for the particular constraint. Where necessary, isolate the method as in the M5 check: confirm that it fails for a violation and passes against the original program. If no suitable counterexample has been established, record that evidence gap. An unknown result need not be reported as verified to preserve an attractive score.

### The report's construction must be inspectable too

This runner first checks that the original program passes, verifies the selected test count and the timeout test's name, then executes each mutant in a separate temporary directory. It separates assertion failures from execution errors and lists failing test names. It does not pin every test identity or include assertion messages in its JSON, which is why the earlier failure message comes from a separate single-method run.

An import or execution error, an unexpected test count or an execution timeout aborts the demonstration rather than silently counting as a kill. That is this tutorial's conservative policy. M5 models the payment code receiving `TimeoutError`; the test process completes normally. A mutation tool's execution timeout means its test process exceeded a time limit. Stryker counts that latter outcome as detected, while this runner aborts. Establish which definition applies before interpreting the report.

The three suites are an experiment in test selection. A real acceptance process must fix the scope, protect its rules and runner, and review changes to them separately. If a PR author can remove unfavorable tests and return a new green result, the score no longer has a shared basis.

---

## 8. Return the evidence to Review before discussing reliability

Return to the PR in section 2 that promises payment replay. The reviewer now knows the commitment and has seen M5's counterexample. The decision is whether the change has sufficient evidence for approval, and what that approval covers.

If the submission still contained the 85.7% result, I would leave a comment like this. It is a teaching example, not an actual team's approval record:

> Approval withheld. M5 changes a timeout result to `PAID`, yet all eight selected tests pass. C4's unknown payment outcome remains unverified. Add timeout cases before and after capture, checking state, payment identifier and replay side effects through `Checkout.pay()`. Provide the test failing against M5 and passing against the original program, then request the payment owner's review. This review covers the sequential, single-process teaching implementation; production recovery and integration require separate evidence.

The comment connects the reason for withholding approval to the conditions for reconsidering it. The author need not guess whether the issue is a score or a naming preference. The next reviewer knows what to examine. A test that compares a string stored inside the fake without exercising the payment code would not meet the condition. The same product path must show an explainable difference between correct and incorrect versions.

A PR evidence package can be concise while preserving those connections. Here is a completed teaching template with fields for the actual revision, rule version and report links. It is a review-record format, not an implemented automatic approval tool.

```text
Intent:
  Replay of the same payment attempt returns the saved result
  without another provider call.
Constraints honoured:
  C1 replay; C2 order/key boundaries; C3 decline;
  C4 unknown outcomes and unclassified exceptions.
Evidence:
  Original program passes 9 payment tests.
  All 7 specified mutants detected; 0 excluded.
  The isolated C4 timeout method fails against M5 and passes against the original.
Revision / rule version / report:
  [Link actual reviewed revision, protected rule version and run results.]
Remaining scope:
  Persistence, concurrency, restarts, provider integration and authorization.
Decision / approver:
  [Responsible person records scope, decision and identity.]
```

With that evidence, the payment owner can judge whether the teaching implementation meets C1 through C4. The QA reviewer checks the relationship between tests and mutants. The integration reviewer records the remaining deployment scope. If the decision is to merge a teaching example into an article repository, those boundaries can be explicitly accepted. If it is to deploy a real payment service, the same report is insufficient. The decision changes because the commitment changes.

Rules and candidate code also need independence. A candidate PR may propose a constraint change, but cannot weaken the tests and use its revised green result to authorize itself. A real process needs human approval of rule changes, evaluation against protected rule and runner versions, and an approval record tied to the reviewed revision. A later change to the payment branch requires relevant evidence for the new revision. A directory named `constraints/` does not establish those permissions or version protections.

So far we have asked whether the tests for this payment implementation detect selected errors. Asking how often an agent's submitted changes honor the team's requirements changes what we count. Each agent-produced change awaiting acceptance is a candidate patch. Constraint pass rate is the share of functionally passing candidate patches that also satisfy all applicable constraints. Fix the task set, functional requirements and constraints, then record each candidate's result so the denominator is clear. Here, one implementation passes nine tests, seven of which retain Review constraints. Those seven tests cannot be counted as seven successful agent deliveries.

Asking whether the same task can be completed repeatedly needs a pass^k experiment. For pass^5, for example, the agent independently produces five results for the same task, each checked against fixed functional and constraint requirements. That task counts as successful across all five attempts only if every attempt succeeds. We can then examine the share of tasks in the fixed task set that meet this condition. Rerunning the same deterministic unittest suite five times examines one implementation; it does not provide five independently generated agent outputs. This article did not run that experiment and reports no pass^5 value. A team considering broader task authorization should first collect the evidence using the Reliability article's approach.

The three gates now have a concrete handoff. The test gate supplies evidence of tests' ability to distinguish errors. The review gate evaluates requirements, evidence and remaining risk. The reliability gate examines repeated outputs across a fixed task set. Each step receives the preceding evidence, and the person taking over must ask which part of the present decision that evidence can support.

---

## 9. From reproducing the example to arranging the next evidence

The implementation, nine payment tests, seven mutants and rule mapping are in [examples/tea_payment](https://github.com/fantasybz/medium-articles/tree/main/examples/tea_payment). With Python 3.10 or later, run these commands from the repository root:

```bash
python3 -B -m unittest discover -s examples/tea_payment -p test_payment.py -v
python3 -B examples/tea_payment/mutation_demo.py
```

The first command runs nine tests. The second prints JSON for the three experiments. Read each suite's `baseline_passed` and `baseline_tests` first, then its `scored_mutants`, `excluded_mutants` and individual `failing_tests`. Looking only at `mutation_score` would repeat the reading habit this article is trying to change.

Start with M5 under `without-timeout`: it is marked survived, with an empty failing-test list. Find M5 under `full` and the list names both timeout subTests. Those records connect section 7's interpretation to the executed results. For each run, the runner copies the original source into a fresh temporary directory and inserts one mutant into that copy. It uses the standard library and local files, makes no real charge and leaves the official `payment.py` unchanged.

The directory also has twelve runner regression tests covering selected cases such as import failures, anomalous test outcomes, changed test counts and a missing timeout test, along with the expected sets of detected mutants. These are outside the nine payment tests and the seven-mutant denominator. Discovering `test_*.py` runs 21 tests in total. That total checks some behavior of the experimental tooling; it cannot be added to a payment service's coverage or reliability measure.

### Hand unresolved outcomes to someone equipped to resolve them

This implementation keeps attempts in a dictionary owned by the running program and verifies **sequential calls within one process**: one `pay()` finishes before the next starts. In a real service, two requests handled at the same time might both see no existing attempt before either records one. That is a concurrency scenario needing separate verification; this example did not run it. Separate service processes also do not share this memory, and a restart loses it. Following an interruption scenario next helps locate the evidence needed to carry the same requirements into a real service.

Suppose the provider captures the payment, but the service stops before saving the final result. After restart, code that sees only an unfinished order may charge again, mistaking “no recorded result” for “no previous capture.” Replacing the dictionary with a database still leaves decisions about when to record an attempt, which operations are atomic, and how to recover when the external charge completes but the local result is not saved. Atomicity means a group of updates either takes effect together or does not take effect at all. For example, a local transaction could record the payment attempt and mark the order as processing together, avoiding a half-completed update. That database transaction does not automatically include the external provider's charge.

These are follow-up design questions derived from the code's boundaries. This article neither implements nor measures production exactly-once guarantees, under which the same payment takes effect only once. The table connects the missing evidence to the review responsibilities from section 2. Each row should become verifiable work, rather than an unexplained “handle before launch” note at the bottom of a PR.

📌【在此插入表 table-06.png】

Take the lost response in the third row. A lookup asks the provider for the current result of that payment. Reconciliation compares the provider's records with the application's order and payment records to find differences that need action. Naming the state `PENDING` is only the beginning: the owner must decide which process obtains those records, what evidence permits a state change, and who takes over when an attempt remains unresolved too long. A webhook in the fourth row is a system notification sent by the provider. It can arrive more than once or arrive late, so receiving a notification cannot by itself mean a new payment occurred. These recovery processes still need design and verification; the example does not implement them.

The buyer's screen should describe the current state and next step according to capabilities that actually exist. A service without a notification process cannot promise a later notification. Retaining an unknown result should support recovery, rather than leave the buyer responsible for managing the uncertainty.

Identifier lifetimes need deliberate design too. The [AWS Builders' Library](https://aws.amazon.com/builders-library/making-retries-safe-with-idempotent-APIs/) discusses a repeated request ID with different intent and late-arriving requests. [Stripe's idempotency documentation](https://docs.stripe.com/api/idempotent_requests) says keys may be removed after they are at least 24 hours old; reuse after pruning creates a new request. An application must account for the provider's retention and retry contract, as well as remembering that it once used the key. An order ID, payment-attempt key and webhook event ID protect different boundaries; one cannot stand in for all of them.

Authorization also requires evidence from the real service. This fixture begins with an authorized order and does not test rejection of cross-account access or payment. A correct receipt SKU does not establish correct warehouse fulfillment either. These are explicit handoff tasks. Detecting all seven mutants does not complete them.

### A team can start with one PR

To introduce this approach, I would choose a change with clear consequences that the team can understand fully, then identify one consequential requirement whose expected result is settled. A reviewer explains its source, the implementer adds a case, and a corresponding incorrect version is seeded by hand to check whether the test distinguishes it. Completing one chain of evidence helps the team discover what its rule records, tests and review notes need to preserve.

Then observe the maintenance cost. When the rule fails, can its owner distinguish an implementation regression from a changed contract or an unsuitable fixture? An implementation regression calls for a code fix and renewed verification against the existing requirement. A changed contract calls for the rule, counterexample and approval record to be updated together. A fixture that no longer represents the agreed scenario needs correction and another check of its ability to distinguish errors. An environment failure that prevents execution is a separate problem: repair it and obtain a result before counting anything for or against the requirement. Experience with those judgments gives the team a basis for expanding scope and automation, with a better chance of sustaining it than a large initial collection of ownerless constraints.

---

## 10. Return to the person waiting for a payment result

Return to the payment screen at the start. The buyer's questions are still concrete: did the payment go through, is it safe to press Pay again, and whose response should they wait for? Having read the code and reports, we are better equipped to examine how a system handles those questions. But 100% in this demonstration has not determined the outcome of a real transaction. For the screen's message to deserve trust, the team still has to connect its verification results to an actual process for handling the payment.

I want to hold on to the 85.7% result in Section 7. It gives a reviewer a reason they can explain for withholding approval: the eight tests never arrange a timeout, so none objects when M5 changes an unknown outcome into success. The reviewer uses the payment contract to identify that difference, then asks for a test that fails against the faulty version and passes against the original. The implementer now knows what evidence to add, and the reviewer knows what to reconsider. The gap is unverified timeout behavior; merely raising the score threshold does not explain how to close it.

Judgment continues at 100%. Detecting all seven selected mutants supports the tests' ability to distinguish those changes. The empty-test counterexample also shows how an aggregate can conceal a constraint losing its assertions. The next reviewer therefore needs to see how requirements, cases and individual results connect, so they can distinguish protection that exists from a report that only looks complete. Preserving those reasons gives the work invested in one review a chance to remain useful in the next change.

This connects the questions from the preceding parts. The testing part asks whether the tests' idea of “correct” matches the original requirements. The review part assigns people with the competence and responsibility to judge whether the evidence supports this approval. The reliability part then widens the question to repeated outputs across a set of tasks, and whether the team can sustain the necessary human review. This payment example supplies a reproducible starting point. A green result for one program cannot be converted directly into an agent's long-term reliability.

The people making those judgments need support, too. Suppose a different colleague changes the payment flow later. They should not inherit only a rule saying that timeouts must remain PENDING, with no explanation of why that agreement was made. If the rule is connected to the provider's guarantees, the way the tests arrange unknown outcomes, and the recovery work still unfinished, the colleague can judge whether to fix the implementation or reopen the contract. Keeping the reasoning reduces the need to find the original reviewer for another explanation. It also helps prevent old tests from becoming rules nobody dares change after the requirements have moved on.

The same record should make unfinished responsibilities visible. A reviewer can use the preceding evidence to judge whether this teaching example meets C1 through C4 and can be merged into the article repository. Deploying a real payment service still requires evidence for persistence, concurrency, provider integration and recovery. Labeling them “follow-up work” is insufficient: someone must take responsibility and state what results would allow the team to reconsider deployment. Until those arrangements exist, withholding approval has both an explicit reason and conditions under which the work can move forward.

To bring this into a team, I would start with a PR that is already green and follow one promise it makes to a user. Which requirement defines that promise? Which test actually passes through the product path? Which version that violates the requirement would make that test fail? Who judges whether the evidence is sufficient? Wherever the chain stops, leave a concrete question for the next review. The rule cards, mutation reports and approval records discussed earlier help people make that judgment. Their value lies in enabling a colleague to take over with understanding, rather than adding another document nobody knows how to use.

At the end of these four parts, this is the working habit I hope to leave with the reader: explain what has been established, put unanswered questions in the hands of people who can pursue them, and keep approval decisions connected to their evidence. An agent can help produce code, find counterexamples and organize reports. The team must continue to decide which promises those results support, and which promises it is not yet ready to make.

The person waiting to buy tea will not read our test names and does not need to know what M5 means. They have entrusted a payment to the system and want a result it has grounds to give. If the outcome is still unknown, they want to know what they can do next. Our discussions of testing, review and reliability should help the team meet that expectation. Leaving both the reasons for our judgments and the unfinished responsibilities visible gives engineering care a chance to become reassurance the user can actually feel.

---

### Series

- [Overview: Green Is Not Done](https://medium.com/p/c4fc9f3d8581): three gates and their adoption order.
- [1. Testing](https://medium.com/p/51d001a6dcd5): checking whether tests distinguish incorrect behavior.
- [2. Review](https://medium.com/p/4d36d0f2f9c1): human judgment, risk triage and approval responsibility.
- [3. Reliability](https://medium.com/p/4b6d147bff0d): retaining reviewer constraints and measuring candidate patches and repeated attempts.
- **4. Payment Walkthrough (this piece)**: connecting selection, tests and evidence through one bottle of tea.

### References

1. Accompanying implementation — [Payment, constraint tests and seven selected mutants](https://github.com/fantasybz/medium-articles/tree/main/examples/tea_payment) [§§4–9; a teaching example, not a production system]
2. Stryker documentation — [Mutant states and metrics](https://stryker-mutator.io/docs/mutation-testing-elements/mutant-states-and-metrics/) [§§6–7; tool states and score definitions]
3. Stripe documentation — [Idempotent requests](https://docs.stripe.com/api/idempotent_requests) [§§1, 9; provider-contract comparison; the demo does not integrate Stripe]
4. Stripe documentation — [Handle errors](https://docs.stripe.com/error-handling) [§1; indeterminate outcomes and same-key retries]
5. Google — [What to look for in a code review](https://google.github.io/eng-practices/review/reviewer/looking-for.html) [§2; scope, context and reviewer competence]
6. Petrović et al. — [Practical Mutation Testing at Scale: A view from Google](https://research.google/pubs/practical-mutation-testing-at-scale-a-view-from-google/) (2021) [§6; incremental execution, filtering and selection]
7. Stryker documentation — [Equivalent mutants](https://stryker-mutator.io/docs/mutation-testing-elements/equivalent-mutants/) [§6; limits of equivalence determination]
8. AWS Builders' Library — [Making retries safe with idempotent APIs](https://aws.amazon.com/builders-library/making-retries-safe-with-idempotent-APIs/) [§9; identifiers, different intent and late requests]

### AI collaboration note

AI assisted with organization, writing, translation and review of this article and its code. The payment scenario and Review comments are explicitly illustrative. Test and mutation figures come from executing the accompanying code, not from fictional production outcomes.

*Kochi Chuang, 榮民叔叔的藏書筆記. Chinese edition: [中文版](https://medium.com/p/46377fd460fe).*
