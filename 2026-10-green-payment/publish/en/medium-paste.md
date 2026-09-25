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

> **TL;DR** — You want to buy a bottle of unsweetened pure green tea, but the payment screen has stopped responding. Will pressing the button again charge you twice? This walkthrough uses a fictional NTD 35 order to connect the series' three gates: assign reviewers and reading depth by risk, select durable constraints from Review comments, turn them into tests, then choose relevant code for mutation testing. The runnable Python example executes seven explicitly selected mutants. Two happy-path tests kill two of them, for a score of 28.6%. Eight tests, omitting only the timeout case, reach 85.7% while still missing a payment incorrectly marked successful. All nine payment tests detect all seven mutants. That 100% describes the selected scope; it says nothing by itself about concurrency, restarts or a real provider integration.

> Series: [Overview: Green Is Not Done](https://medium.com/p/c4fc9f3d8581) → [1. Testing](https://medium.com/p/51d001a6dcd5) → [2. Review](https://medium.com/p/4d36d0f2f9c1) → [3. Reliability](https://medium.com/p/4b6d147bff0d) → **4. Payment Walkthrough (this piece)**. This article stands on its own; the overview and first three parts provide the research background and organizational design.

---

## 1. First, agree on what buying that bottle means

Imagine a small, familiar situation. You choose a bottle of 無糖純喫綠茶, unsweetened pure green tea, check the amount and press Pay. The screen spins for a while. It reports neither success nor a clear failure. Your finger hovers over the button. Would another press retrieve the previous result, or start a second payment?

This is a teaching scenario, not an incident from my work or a description of a particular merchant. The **NTD 35 price is illustrative**, not a claim about the product's actual price. Amounts are integer New Taiwan dollars; discounts, tax, other currencies and change are outside this example.

I want this bottle of tea to make the abstract terms observable. The buyer's expectations are concrete: the order contains unsweetened tea, the amount is NTD 35, pressing Pay again does not charge them twice, and the merchant does not issue a successful receipt while the payment result remains unknown.

The example starts with an authorized order loaded by the server. The SKU identifies the product, `order_id` identifies the order, and `key` is the idempotency key for this payment attempt, allowing repeated requests to refer to the same operation. These identifiers serve different purposes. An arbitrary price submitted by the browser is not authoritative input to this boundary.

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

People should agree on the payment contract before asking an agent to implement it. A normal payment sends the order amount to the provider and returns `PAID` after a successful response. The receipt preserves the order, SKU, amount and payment identifier. Repeating the same order and key returns the existing result without another charge request. A key cannot move to another order. An order with an existing attempt cannot start again by changing its key or contents.

A decline and a timeout mean different things. An explicit decline is `DECLINED`. A timeout means a definite response did not arrive; the provider might already have captured the money, so the result remains `PENDING`. This demo does not automatically charge again after a timeout or implement lookup and reconciliation. Those need a separately designed and verified recovery path.

These are the example's agreed behaviors, not universal payment API state names. [Stripe's error-handling documentation](https://docs.stripe.com/error-handling#connection-errors) likewise treats connection errors as indeterminate, but its idempotency contract permits safe retries with the same key. This demo has no provider-side idempotency implementation, so it retains a pending result. The distinction is the guarantee supporting the retry. The conservative teaching policy should not become a blanket rule that real payment systems must never retry.

---

## 2. Choose the reviewers, then decide where they need to read deeply

Suppose an agent submits a PR saying: “The payment API now supports retries; identical requests receive the existing result.” That intent tells a reviewer what the change is trying to accomplish. It does not establish that the implementation accomplishes it.

I would first identify the responsibilities touched by the change: order identity, amount, provider calls, payment state and the tests used to accept them. Shared payment logic can affect many orders. The fact that this bottle costs only NTD 35 does not make the change low risk. Conversely, a documentation-only correction that does not affect the payment path should not require the same scrutiny merely because its directory is named `payment`.

Here is my suggested allocation for this payment-logic PR. One qualified person may cover several roles. The point is responsibility and competence, not filling three job titles.

📌【在此插入表 table-01.png】

A reviewer agent can organize the diff, locate charge calls and exception handling, or propose counterexamples. It cannot approve the payment contract on its own or turn its own approval into human authorization. Following the Review article's recommendation, high-risk payment logic needs approval from a responsible, qualified person other than the task assigner.

When selecting hunks, the blocks of changes in a diff, I would prioritize the existing-attempt check, the amount passed to the provider, the conversion of exceptions into payment states, and connected callers. Reading only the highlighted line is insufficient. A guard's position, the origin of a value or an exception swallowed nearby may determine the behavior. Changes to tests and verification configuration belong in the same review, so a weaker assertion cannot quietly manufacture a green result.

[Google's Code Review guidance](https://google.github.io/eng-practices/review/reviewer/looking-for.html) asks reviewers to understand their assigned code, read wider context when needed and involve qualified reviewers for specialized concerns. The three responsibilities above are my application to this payment case, not a Google requirement to assemble three people. The approval record should say who reviewed the tests and who checked the payment-state decisions.

If the only evidence is happy-path testing, I would begin with a close review of the relevant diff and identify missing constraints. Once reports actually cover those requirements, there is a basis for adjusting future review depth. Removing that attention first leaves the score trying to stand in for questions nobody has answered.

---

## 3. Which Review comments deserve a lasting test?

Now imagine several reviewer comments. These are teaching inputs, not comments copied from a real PR.

One asks whether clicking twice on the same order could send two charge requests. Another asks what happens if a retry regenerates the key or reuses it for another order. A third points out that money might have been captured before the timeout. Two more suggest renaming a local variable and ask whether the campaign should offer refunds.

All may be useful, but they call for different next steps. I would not select comments by length, popularity or whether they already describe an incident. I would ask what consequence the comment identifies, whether the requirement will outlive this PR, who can confirm the expected result, and whether a stable, maintainable test can observe it.

📌【在此插入表 table-02.png】

A consequential requirement can deserve protection the first time it appears. There is no reason to wait for a second incorrect charge before calling it a recurring rule. A temporary migration restriction, by contrast, may need a check with an expiry condition rather than a permanent place in CI.

A selected comment also needs a traceable rule record. For C4, the source is the lost-response risk in this illustrative Review. Its scope is the payment attempt and its replay. Its requirement is to retain an unknown result after timeout, without reporting success or automatically sending a new charge. The test is `test_timeout_stays_pending_without_another_charge`; a payment owner maintains it, and a change to the provider contract or reconciliation design triggers reconsideration.

A real team should attach the actual PR, requirement or incident. An owner field lets the next reviewer find someone who can explain or change the expected result. A long period without failures is not, by itself, a reason to remove a payment safety rule. The rule's continuing protection may be why the mistake has stayed out.

---

## 4. Turn the constraints into tests that distinguish incorrect behavior

**“Constraint test” describes a test's origin and responsibility, not a technology mutually exclusive with functional testing.** Preventing a duplicate payment is both product behavior and a constraint a reviewer has chosen to retain. It can be checked by a unit test, integration test or another suitable mechanism. Reporting those responsibilities separately can help accountability without implying that they protect disjoint worlds.

The example begins with two happy-path tests: the receipt preserves the unsweetened SKU, NTD 35 and payment identifier; the fake provider receives and captures exactly NTD 35. Seven more test methods cover C1's replay, C2's three identity conflicts, and C3/C4's decline, timeout and other connection error. One rule can require several test methods; rule count and test count need not match.

`FakeGateway` is a test double. It records attempted charge `calls` separately from successful `captures`, and **deliberately does not deduplicate**. If a helpful fake silently removed duplicate requests, a missing application guard might leave every test green.

This first excerpt from `ConstraintTests` makes two calls with the same order and key, then checks both results and side effects. The expected NTD 35 comes directly from the agreed example, without asking the system under test to calculate its own expected answer.

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

Other provider exceptions propagate out of the method, but the pending record written before the call remains. A replay therefore does not send another charge. That early record needs its own protection. While developing the example, an independent Claude Code review identified this testing gap. The example was extended with a capture followed by a non-timeout connection error, plus M7, which removes the early record. Review identified a risk the initial selection had missed; mutation then checked whether the added test protected it.

Mutation testing begins with a passing original program. Change one thing, run the selected tests and discard that mutated copy. An assertion failure caused by the changed behavior identifies a killed mutant. This simple runner labels every undetected mutant survived. It does not measure coverage, so that label also includes branches the selected tests never execute. Full tools distinguish NoCoverage from Survived, meaning executed but undetected; keep that distinction in mind when reading the tables.

---

## 6. Select mutation scope from the Review risks

The third selection is deciding which code and mutations deserve execution. I start with the agreed payment requirements and locate the code that enforces them: charge amount, existing-attempt guard, key binding, exception handling and receipt contents.

Only `payment.py` is mutated. Assertions, fixtures, `FakeGateway` and the mutation runner remain unchanged. Changing the question or the judge at the same time would undermine the experiment. If a real PR changes a shared payment helper, affected tests must follow its callers. “Diff-scoped” does not mean the surrounding behavior no longer matters.

There is earlier industrial research behind this approach to controlling scope. Google's [Practical Mutation Testing at Scale](https://research.google/pubs/practical-mutation-testing-at-scale-a-view-from-google/) (2021) describes mutation during Code Review on changed code, filtering less useful mutants and selecting operators using historical performance. It supports considering cost and actionable results together. It does not validate this article's seven mutants or a 70% threshold.

For an experiment the reader can inspect individually, this example **hand-seeds seven mutants**. They are executed changes, not a complete set automatically generated by Stryker, PIT or mutmut, and they do not cover every possible payment defect.

📌【在此插入表 table-03.png】

Each has a demonstrable behavior difference; no equivalent mutants are excluded here. With a full mutation tool, record its version, operators, file scope and test selection, and separate compile failures, no coverage, timeouts and confirmed equivalence. For example, [Stryker's metrics](https://stryker-mutator.io/docs/mutation-testing-elements/mutant-states-and-metrics/) count both killed mutants and timeouts as detected, while valid mutants with no coverage remain in the ordinary mutation-score denominator. Dropping both timeouts and uncovered mutants as “invalid” would change the meaning of a comparison.

A surviving mutant does not automatically prescribe an assertion. Read the change and find an input and side effect that expose it. M2 needs a second call; M5 needs a timeout. The complete test includes timeouts before and after capture, so “unknown” does not quietly become “definitely charged.” Five more `PAID` assertions on a normal purchase would reach none of these situations.

When no counterexample is apparent, distinguish undefined requirements, unreachable inputs, test gaps and actual behavioral equivalence. “We do not test that input” is not an equivalence proof. [Stryker's equivalent-mutant guidance](https://stryker-mutator.io/docs/mutation-testing-elements/equivalent-mutants/) also explains the limits of automatic determination. Any exclusion needs its input domain, reason and review recorded. A consequential surviving mutation must be resolved or explicitly accepted before approval, not hidden inside the average.

---

## 7. Calculate the score, then state what it leaves unanswered

All seven mutated programs are executable and non-equivalent, so this experiment keeps a denominator of seven. Its mutation score is the number detected by tests divided by seven, multiplied by 100%. The denominator counts mutants, not tests. It is not the probability that the product has no bugs.

The accompanying `mutation_demo.py` was executed with three test selections. The original program passed each selection before the mutations ran:

📌【在此插入表 table-04.png】

The first two tests are real tests that exercise payment. They simply do not require the program to handle replay, key conflicts, declines or timeouts. The locations changed by M2, M3 and M7 execute, yet the tests do not detect the behavioral differences: mutation asks more than whether a line ran. M4 and M5 never reach their exception branches, a gap branch coverage could also reveal.

The second row deserves a pause. A team using only the Testing article's proposed starting threshold of 70% would see 85.7% as enough. Yet C4 remains partly unprotected: M5 changes `PENDING` to `PAID`, but none of these eight tests executes the timeout branch, so they cannot detect that error. **An aggregate score above the threshold cannot compensate for an unverified critical payment constraint.** This PR needs the timeout case and evidence that it fails against M5.

The 70% comparison illustrates how an aggregate can hide a critical survivor. Seven manually selected mutants differ from the set a tool generates on changed lines, and the score depends on that selection. This small denominator cannot calibrate, or directly inherit, a real repository's threshold.

The third row restores that timeout test and detects all seven mutants. It supports the claim that these nine tests catch these seven selected changes. It does not make the payment service “100% reliable.” Concurrency, restarts and provider integration do not acquire evidence merely because every mutant in this denominator was detected.

Nor does 100% prove that every test is individually effective. M2 fails several tests at once. In an isolated copy, replacing C1’s replay test and C2’s new-key and changed-order tests with empty `pass` bodies still produced 28.6%, 85.7% and 100%. Other tests continued to detect M2, hiding three tests that had lost their assertions. This counterexample was executed; the original example retains its tests. Review must also inspect assertions and individual failing-test results. Where needed, run a constraint’s test alone against a version that violates its requirement.

The report must also explain its classification. This runner checks a passing baseline, each selection’s test count and the timeout test’s name. It executes each mutant in a separate temporary directory, distinguishes assertion failures from execution errors and reports failing test names. It does not lock every test’s identity or include assertion messages in the JSON. Import errors, execution errors, missing tests or execution timeouts abort the experiment instead of quietly counting as kills. This is a conservative convention for the teaching runner, not a claim about every production mutation tool's default classification.

There are two different levels of timeout here. M5 changes how the payment code handles `TimeoutError`; its tests finish normally. A mutation tool's execution timeout means the mutant's test process exceeded a time limit. Stryker counts the latter as detected, while this runner aborts. Neither means that every payment timeout counts as a detected bug.

Putting three selections side by side compares test effectiveness. It is not a CI option allowing PR authors to remove inconvenient tests. A real acceptance process fixes and protects its test scope, rules and runner, and separately reviews changes to that evidence.

---

## 8. Return the evidence to Review before discussing reliability

At this point, a reviewer should receive more than a percentage. The payment PR needs its intended replay behavior, C1–C4 with sources and owners, results from nine tests, individual statuses for seven mutants, and the system boundaries that remain unverified.

The human judgment at 85.7% is specific: M5 reports an unknown payment as successful, and C4 lacks its timeout test, so the aggregate score does not justify approval. After adding the test, its oracle still deserves review. A test that only checks a string returned directly by the fake, without passing through `Checkout.pay()`, would not protect the application's state handling.

Rules also need independence from the candidate implementation. A PR may propose changing a constraint, but it cannot weaken the acceptance test and use the resulting green run to authorize itself. A production workflow should require human approval for rule changes, evaluate candidate code with protected rule and runner revisions, and bind approval to the revision actually reviewed. A directory named `constraints/` creates none of that protection on its own.

The nine tests describe one candidate program in selected scenarios. To measure an agent's constraint pass rate, the unit changes to candidate patches: among patches passing functional checks, how many also pass every applicable constraint? One patch passing seven constraint tests does not measure the agent's long-term pass rate.

Likewise, pass^k involves independent agent attempts at the same task, each evaluated against requirements fixed in advance. It does not mean rerunning the same deterministic unit tests five times or running once against each mutant. This article performs no repeated-agent experiment and therefore reports no invented pass^5 figure.

That is how the three gates divide the work around this bottle of tea. The test gate supplies evidence about test protection. The review gate judges requirements, evidence and outstanding risk. The reliability gate uses repeated outcomes on a fixed task set to inform authorization. Evidence can move between stages without changing what its denominator means.

---

## 9. What readers can reproduce, and what deployment still needs

The implementation, nine payment tests, seven mutants and rule mapping are in [examples/tea_payment](https://github.com/fantasybz/medium-articles/tree/main/examples/tea_payment). With Python 3.10 or later, run these commands from the repository root:

```bash
python3 -B -m unittest discover -s examples/tea_payment -p test_payment.py -v
python3 -B examples/tea_payment/mutation_demo.py
```

The first command runs nine tests. The second emits JSON for the three experiments, including baseline counts, kills, the fixed denominator and failing test names for each mutant. It uses only the standard library and local temporary files, with no real account or charge.

The directory also contains twelve runner regression tests, checking that loading failures, abnormal test outcomes and selection drift cannot produce a trustworthy-looking report. They are outside both the nine payment tests and the seven-mutant denominator. Discovering `test_*.py` across the directory therefore runs 21 tests.

Payment attempts live in process-local dictionaries. The evidence covers **sequential calls in one process**. Two service processes do not share that memory, and a restart loses it. Blocking repeated calls in the demo does not establish exactly-once charging in production.

Taking these requirements into a real service would need shared durable payment state, database uniqueness and transaction boundaries, plus concurrent-request tests for races. It would need crashes before and after capture, recovery after restart, and provider-contract tests for idempotency, lookup, reconciliation and duplicate or out-of-order webhooks. An authorized new attempt after a decline needs a separate policy. None of those are included in this example's 100%.

The identifier's lifecycle matters too. [AWS Builders' Library](https://aws.amazon.com/builders-library/making-retries-safe-with-idempotent-APIs/) discusses different intent under the same request ID and late-arriving requests. [Stripe's idempotency documentation](https://docs.stripe.com/api/idempotent_requests) says keys can be pruned once they are at least 24 hours old; reuse after pruning creates a new request. An application cannot merely remember that it once used a key without establishing whether the provider still remembers it. An in-memory dictionary cannot substitute for that integration evidence.

Authorization is another boundary the fixture cannot establish. A real service must reject cross-account access to orders. A correct receipt SKU also does not prove the warehouse delivered the unsweetened drink. Naming these boundaries gives the next person a concrete place to continue gathering evidence.

---

## 10. Return to the person waiting for a payment result

The person at the start only wanted a bottle of tea. They do not need to understand a mutation-score denominator, and they should not have to guess whether pressing Pay again is safe. Those decisions belong in the requirements, implementation and acceptance process.

For the engineering team, the example connects three selections: choose reviewers and close reading by payment risk; retain comments that identify durable, observable requirements with an owner; then locate the enforcing code and choose mutations that test its protection. Each choice needs a reason the next person can understand and examine.

I would not turn 100% into a new acceptance slogan. The number I want to leave with the reader is 85.7%. It looks reassuring, yet the payment outcome can still be reported incorrectly. A reviewer who can name the missing scenario, rule and mutant has evidence with which to act.

The four parts bring us back to the person waiting for a payment result. The tea's price is just an illustration. What deserves care is that someone entrusted a payment to this system. The team needs to explain what it has checked and which questions still need verification.

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

*Kochi Chuang, 榮民叔叔的藏書筆記.*
