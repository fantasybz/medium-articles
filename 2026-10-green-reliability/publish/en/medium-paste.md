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

# Green Is Not Done, Part 3 — The 34% SWE-Gate Found Behind a Green Build: Constraint Tests, pass^k and the Gate for Expanding Autonomy

> **TL;DR** — Part 3 of this four-part series asks what evidence should guide expanded agent authority. Across 75 Python repos and 303 patch tasks, SWE-Gate found that 221 of 644 patches passing functional tests (34%) violated a constraint a reviewer had actually added. That gap leads to three metrics. **Constraint pass rate** is the share of functionally passing PRs that also pass all constraint tests. **pass^k** is the share of cases in a task set that pass all k runs, reported separately from single-attempt success rate, pass@1. **Oversight budget** addresses the human work still needed: in READY's clinical-audit case, systems only 0.3 percentage points apart in accuracy differed by nearly 10 percentage points in review requirements. Those staffing figures cannot transfer directly to code review. This piece borrows the idea of working backward from a reliability target, using a simplified model to estimate a review minimum and compare it with actual review and sustainable capacity. These results join test effectiveness and existing operating conditions in the monthly leadership report and the G2 authority decision. pass@1 alone does not decide expansion.

> Series: [Overview](https://medium.com/p/c4fc9f3d8581) → [1. Testing](https://medium.com/p/51d001a6dcd5) → [2. Review](https://medium.com/p/4d36d0f2f9c1) → **3. Reliability (this piece)** → 4. Payment Walkthrough (coming soon)

---

## 1. The 34% SWE-Gate measured

The overview separated the problems a green build does not cover into three layers. This piece starts with one of them: passing functional tests does not mean meeting the team's constraints. When requirements a reviewer has already raised are absent from the functional tests, a green build cannot answer those questions. The numbers cited in the overview make that gap concrete. SWE-Gate is a benchmark paper, and what it measures is exactly what a green build covers. It did one extra thing: it did not only ask whether the functional tests passed. It also pulled out what the reviewers had actually asked for on those PRs, turned each of those asks into an executable check, and ran them as a separate pass.

The 34% is what SWE-Gate (September 2026) measured on 75 Python repos and 303 patch tasks. Of the 644 patches that passed the functional tests, 221 violated one of those constraints. In plain language: one in every three green patches violates a constraint the reviewer cared about.

Two points need clarifying before using these numbers, so the study's conclusion is not misread.

The domain boundary comes first — Python repos, patch tasks, not "all agent PRs." That is the range it measured. Change the language, change the shape of the task, and the number has to be measured again.

Look at the denominator too. The denominator is "patches that passed the functional tests," so the correct plain-language reading is "one in every three green patches violates a constraint." It is **not** "a green build misses a third of what reviewers care about." That version swaps the unit for a share of "the things reviewers care about," which the paper did not measure. The two sentences look almost identical, but their denominators are not, and taking the wrong one into an argument gets you knocked over by the first follow-up question.

Understanding the gap requires separating several meanings of “passed”: a successful build, correct functionality and satisfied non-functional requirements. The next two benchmarks measure gaps between those judgments; a third, workflow-design paper identifies a premise they share.

SWE-NFI, with 188 tasks and 92 executable rules, measures the gap between functional success and non-functional compliance. The best agent reached a 70.0% functional pass rate, while performance on non-functional rules generally lagged. These rules include performance, security and log-format requirements. If functional tests do not include those conditions, passing them does not answer those questions.

OpenHarmony Bench (153 app tasks) measures a layer further down, "**a green build does not mean the behavior is right**": buildable 94.77% to 100%, behaviorally correct only 48.36% to 58.39%. The gap is far wider, but behavioral errors are what functional tests are supposed to catch in the first place, so it does not sit in the 34% layer.

Rebuild Dossier is a design premise, not an observed result. It is a paper proposing the process an agent should follow when it rebuilds an entire app: when the agent has a chance to game the tests, a fully passing suite does not mean correct, so it locks the interface first and hands over one test at a time. What it gives you is not a number but a reminder: as long as the agent can change the implementation and the tests in the same breath, a fully passing suite stops being independent evidence.

Once the layers are laid out, one thing becomes visible: all three look identical on a dashboard. The light is green in every case. The only difference is what that light measured, and whether you went and measured the rest yourself. A green build never volunteers what it left out, and that is exactly what makes it dangerous.

This piece deals with only two of those layers. One is the reviewer constraints, which is what the opening number measured. The other is reliability, which is whether the same thing done again still comes out right. None of the three studies above measured that layer; the reliability section explains how to measure it on your own system, using only the kind of independent evidence Rebuild Dossier warned about. Below, the constraints get written as checks first, then capability and reliability get measured separately, then the bill for review gets computed, and finally it all connects back to the gate.

---

## 2. Writing review constraints as executable constraint tests

The last section described SWE-Gate's finding that roughly one-third of green patches violated constraints reviewers cared about. The direct response is to turn requirements worth retaining into constraint tests that CI can run. The name describes their source and protective responsibility, not a technology mutually exclusive with functional testing. “Do not charge the same payment twice” is both functional behavior and a constraint a reviewer can choose to maintain. A unit or integration test can check it.

What does a constraint look like? Think of it first as the things a team says over and over but should not have to rely on a person to remember every time. The seven categories below illustrate how review requirements can become constraint tests; they are not a complete taxonomy; for SWE-NFI's 92 rules and SWE-Gate's comment taxonomy, the papers themselves are the authority:

📌【在此插入表 table-01.png】

The rightmost column shows that lockfile diffs, AST analysis and import graphs let us start with existing tools. Each example still needs a defined scope. A static rule for "no database calls inside loops" may recognize certain patterns without covering every indirect call. Establishing what a check can see tells us which remaining questions need another owner.

The process has four steps: review comment → rule → constraint test → CI. The rule-file approach comes from a July 2026 study that preserved accepted comments in version control for later work, also discussed in section 3 of the review piece. Before implementing a constraint test, establish whether a comment is a general rule or a one-off exception and whether it can become a stable check. Acceptance once does not settle its scope forever.

The rules file records two kinds of thing. The first is provenance: each rule records its source PR and date, and a rule that has not fired in six months gets reviewed for expiry. The second is responsibility, which is why there are two more fields — owner (who maintains this rule) and expiry (the date it comes up for review). Even a rule that was once useful can grow outdated without someone to maintain it and a time to revisit it. These two fields tell the team who should return to check when that time comes.

Six months is a reminder to reconsider, not a reason to delete the rule. A payment safety constraint may have gone a long time without failure because its protection remains effective. Retention depends on whether the business contract, implementation or risk has changed.

Now that the rules have an owner, the next question is whether the agent can change them. Section 2 of the overview splits evidence into three classes: the first is what the agent says, the second is the tests the agent wrote itself, and the third is the tests the agent cannot change. What lands here is that third class, and the mechanism has three parts.

CODEOWNERS assigns review responsibility but needs merge rules to enforce it. First, assign only human owners to `tests/constraints/` and the golden set, and enable Require review from Code Owners. Second, require human approval for changes to the rule file, CODEOWNERS and verification workflow, with no agent bypass. Third, use Check 2 from the testing piece to block any weakening of category （c） assertions.

The agent can propose changes on a branch but cannot approve and merge them itself. When evaluating a PR, obtain constraints and verification code from a protected version and use them against the candidate code. A PR must not rewrite its checker and then cite that checker's green result as proof of compliance. That is the independence "cannot change unilaterally" needs to preserve.

Walk an illustrative comment through those four steps. The PR number, dates and accounts below are examples too. Before, it is the comment a human has to repeat every time: "Please don't `new HttpClient` directly here, use `clients.http()`." It only ever covers the one PR in front of it, and once it has been said it is gone. After, the comment becomes three arrangements: CI runs a check, a maintainer owns the rule, and permissions restrict who can approve changes.

First is the test file. This minimal illustration checks direct `HttpClient(...)` calls in changed Python files. It does not cover aliases, attribute calls or dynamic construction. A production implementation must also handle deleted files, git-command failures and the diff baseline. The excerpt is not a complete security boundary:

```python
# tests/constraints/test_http_client_reuse.py
# Rule source: PR #4821 (2026-06-12); rules file: rules.md#http-client-reuse
import ast, pathlib, subprocess

ALLOWLIST = {"src/infra/clients.py"}

def changed_python_files():
    out = subprocess.run(["git", "diff", "--name-only", "origin/main...HEAD"], capture_output=True, text=True).stdout
    return [pathlib.Path(p) for p in out.split() if p.endswith(".py") and p not in ALLOWLIST]

def test_no_direct_http_client_construction():
    offenders = []
    for path in changed_python_files():
        tree = ast.parse(path.read_text())
        for node in ast.walk(tree):
            if isinstance(node, ast.Call) and getattr(node.func, "id", None) == "HttpClient":
                offenders.append(f"{path}:{node.lineno}")
    assert not offenders, (
        "Direct HttpClient construction: " + ", ".join(offenders)
        + ". Use clients.http(). Rule source PR #4821, see rules.md#http-client-reuse"
    )
```

The second is the rules file. It records where the rule came from and how long it lives, and the `owner` and `expiry` fields are the point of it:

```markdown
<!-- rules.md -->
## http-client-reuse
- Source: PR #4821 (2026-06-12), reviewer comment
- Rule: never construct HttpClient directly; always use clients.http()
- Check: tests/constraints/test_http_client_reuse.py
- Last fired: 2026-09-30 (six months without firing means a review for expiry)
- owner: @acme/platform-humans (the people who maintain this rule)
- expiry: 2027-03-31 (review on expiry: delete, keep or change)
```

Third is a CODEOWNERS excerpt. It assigns reviewers for these directories and the rule file. Merge restrictions still require the rules described above, plus protection for CODEOWNERS and the verification workflow themselves:

```text
# CODEOWNERS
/tests/constraints/   @acme/platform-humans
/tests/golden/        @acme/platform-humans
/rules.md             @acme/platform-humans
```

Put the three together and that review comment goes from "a person has to say it every time" to "said once, then checked on every PR after that." That is what compounding means here: one comment a human wrote while reading a diff covers that one PR and no more; recycled into a constraint test, the experience from that review can help check every PR that follows.

That compounding still has a cost, depending on how the constraint is checked. An AST rule like the example can analyze selected files without running the whole product test suite. Performance or behavioral constraints may need a separate environment and tests. Reach also depends on the checker: reading the whole diff does not mean verifying every requirement in it.

That is why I put constraints expressible as static checks early in brownfield adoption. A brownfield system has operated for years and may have incomplete tests and documentation. These rules offer a starting point: check a few explicit team requirements even before a complete test suite exists.

So how does a team with no review history get started? Start from the team's conventions and the last five incidents, and write those "let's not do that again" sentences down as checks first.

Draw the four steps, comment → rule → test → CI, as a diagram, and the thing to look at is not the main line on the left but the dashed line coming back on the right:

📌【在此插入圖 diagram-01.png】

The dashed line gives people a chance to reconsider a rule. Two years later, a once-prohibited approach may have a different implementation. If all that remains is a failed check, without its rationale or owner, the next person cannot easily decide whether the code or the rule needs changing. Expiry preserves the opportunity to ask that question.

**Now consider a payment constraint that needs behavioral execution.** Suppose the illustrative order is a bottle of 無糖純喫綠茶, unsweetened pure green tea, for NTD 35. A reviewer points out that a screen timeout may follow a capture, so replay must not simply start another charge. After agreeing on the requirement, retain its source, payment owner, replay scope and a condition to reconsider it when the provider contract changes. The comments and price are teaching inputs, not an actual incident or product price.

Scanning for a `PENDING` string would not verify this rule. In the accompanying [payment example](https://github.com/fantasybz/medium-articles/tree/main/examples/tea_payment), `FakeGateway` records a capture and raises a timeout. The test replays the same order and key through `Checkout.pay()`, checking that the result remains `PENDING`, has no payment ID, and leaves only one provider call and one capture. The fake deliberately does not deduplicate, so it cannot hide a missing application guard. The full tests also cover a timeout before capture and another connection error.

This Review concern is worth retaining because its consequence is clear, its expected result is decidable, it applies to future changes and someone maintains it. Naming preferences do not each need a behavior test; unsettled refund policy first needs a requirement decision. Part 4, “A Payment Walkthrough,” connects these selections to nine payment tests and seven selected mutants.

The denominators must remain distinct. Detecting 7/7 selected mutants is this suite's mutation score within the example, not an agent's constraint pass rate or pass^k. Constraint pass rate counts candidate patches that pass all applicable constraints among those passing functional checks. Pass^k needs multiple independent agent attempts on fixed tasks. Rerunning the same unit tests five times does not produce the five agent outcomes the next section measures.

Constraints can come from different sources. This piece mainly draws on **review history**: a problem occurred, and the team decided to preserve the resulting requirement. Another source is the **spec**, the contract agreed before implementation begins. Both can become checks, but reconsidering them requires returning to their respective basis.

The team that raised a review constraint maintains it and checks at expiry whether its rationale still holds. A spec-derived constraint should be reconsidered with requirement changes by the people responsible for the spec. Sharing a CI pipeline does not remove the need to retain source and owner. Those records let rules evolve and let someone explain why they remain.

---

## 3. Reliability is not capability: pass@1 and pass^k

The last section was about whether the rules got kept. This one is about something else: do the same thing again, and will it still come out right? Capability and reliability are two numbers, and plenty of teams collapse them into one, so let me pin the definitions down first.

Use the definitions from section 8 of the overview: run each golden-set case k times. These are representative acceptance cases chosen by the team. Start each attempt independently from the same initial state, fixing the model, harness version and scoring rules. Record the case-set version for comparisons across months so changes remain interpretable.

**pass@1 is the single-attempt success rate, estimated from the k repeated runs.** Per case, it is the number of passes out of k divided by k. The question it answers is whether the agent can do this on average.

**pass^k is the share of cases that succeed in all k attempts.** Any failed attempt excludes that case from the all-pass count. It describes consistency over these cases and these k runs, not a guarantee that the next run will succeed.

Keep each case's results before computing aggregate metrics. With equal attempts per case, averaging per-case pass@1 gives the same value as pooling all runs. But pass^k needs to know which successes and failures belong to the same case. A total success count cannot distinguish a few cases that always fail from occasional failures spread across cases, and those patterns call for different interventions.

There is one more symbol that looks almost the same, so rule it out now: "the share that succeeds at least once" is pass@k, a different number, and this series does not use it.

The monthly report also includes constraint pass rate: among PRs passing functional tests, the share passing all constraint tests. Both metrics have the same premise: **pass^k and constraint pass rate must be computed from category （c） evidence**, maintained by the team and not rewriteable for acceptance by the agent under evaluation. An agent's completion report does not qualify. Its new tests must pass the test gate, receive human approval into main, and enter the protected verification process to complete the promotion described in the overview.

My notes from preparing for Anthropic's Claude Certified Architect certification exam contain a small example: you do not guess whether the agent's turn has ended from the assistant's reply text, you look at stop_reason (the "why it stopped" field in the API response, filled in by the system). The reply text is what the model says about itself; stop_reason is what the system recorded. They do not come from the same source. The same reasoning applies to accepting code: "the tests all pass" is the agent talking about itself, and red or green in CI is what the system recorded. That is why claims in the first class need verification and cannot independently establish acceptance.

Why is one success insufficient? A single run reveals neither consistency across repeated attempts nor sensitivity to changed conditions. Those are separate measurement questions. The next two studies concern rephrasing the same task, not run-to-run variation under a fixed prompt.

RealSWE (381 task families) measured this: reword the same task and the average drops 6.4 percentage points, and the model rankings reshuffle. The reshuffling is the more troublesome half. It means part of what you are reading off a leaderboard is how the task was worded, not a gap between the models.

Another study of semantics-preserving rephrasing measured a drop of a similar size: an average of up to 6.7 percentage points, **but only 6 of the 16 model-and-scaffold combinations reached statistical significance.** So the right reading is not "every model is equally shaky" but that the effect is real and uneven. Whether your own combination is shaky is something you have to measure on your own combination.

Changes in performance after rephrasing call for evaluating robustness to input variation. pass^k from repeated runs under fixed conditions answers a different question. The experiments can sit alongside each other, but the first is not a measurement of the second.

The corroboration comes from outside code, and this is the only place in the whole series that quotes the full numbers. What Thinkingbox (a benchmark paper) measured is 507 policy-conditioned MCP workflows — multi-step tool-calling tasks carrying policy constraints, where the agent has to keep calling tools through MCP (the protocol for calling tools) and keep the rules at the same time. On that batch, Claude Opus 5 scored 66.50% pass@1 and 47.53% pass^20.

Looking only at the average success rate, you would expect roughly two out of three attempts to succeed. Yet fewer than half of the tasks succeed twenty times in a row. The gap is nearly twenty percentage points: the distance between capability and reliability.

Its conclusion — "clean termination and valid tool calls are not proxy indicators of completion" — holds in the code domain just the same: the agent saying it finished, with every tool call well formed, is a different thing from the task having been done right.

So how do you do this on your own evals? Reuse the golden set from “Agentic Engineering: Evals, Unit Economics, and Scaling”, 20 to 50 cases, and run it monthly at k = 5; that is the set the thresholds are read off. The frontier set runs separately at k = 3: it is a harder batch that does not pass yet, there to show where the ceiling is, and it is not used as a threshold. The report has three fixed columns, so every month you are looking at the same numbers; the oversight budget is reported separately. It uses the first column together with the reliability target and review effectiveness to estimate the required share, then compares that need with actual review and sustainable capacity. Section 4 works through the calculation.

The three columns look like this:

📌【在此插入表 table-02.png】

The most important column in that table is the rightmost one: all three numbers come from something the team owns. If you cannot name that source for a column, that column does not belong in the monthly report.

**My suggested values, not an industry standard**: k = 5 and pass^5 ≥ 60% as one condition for considering expanded authority on low-blast-radius tasks. It cannot authorize expansion alone; the other conditions in section 5 and human approval still apply. Low blast radius means bounded impact with a workable recovery path, not simply a task labeled "internal tool."

**Granularity warning**: with fewer than 30 cases, report pass^k as a trend, not a gate. With 20 cases, one case changes the result by 5 percentage points, from 65% to 60%. The proposal here requires at least 30 cases and two consecutive qualifying months before using it for an authority decision. More months alone do not replace the minimum case count.

Lay three cases out and compute both numbers once, and the difference becomes visible. The one to watch is case B in the middle, which fails exactly once:

📌【在此插入圖 diagram-02.png】

The same batch of golden cases yields pass@1 of 93% and pass^5 of 67%. One describes average performance per attempt; the other identifies cases with no failure across five attempts. Separating them exposes repeat-run failures that an average can obscure. Expanding autonomy still requires considering constraint checks and human review alongside both figures.

---

## 4. Oversight budget: READY and a simplified model

Once the team understands the agent’s success rate and consistency, the next question falls to the people receiving its work: how much review is still needed to meet the reliability commitment? The oversight budget connects that demand with the effort the team can sustain. Raising a reliability target without identifying who can perform the necessary review leaves the target as a number on paper.

READY (September 2026) offers a useful starting point. This enterprise-agent deployment qualification framework works backward from a reliability target to the review share required by an agent system and its human-review policy. In its case study, two systems only 0.3 percentage points apart in autonomous accuracy needed review shares nearly 10 percentage points apart, with the less accurate system requiring less review. The result reminds me that **ranking accuracy alone does not tell a team how much review work it must sustain.**

I borrow the concept, not the numbers. READY uses a clinical audit workflow rather than code and estimates human effort for the system and review policy. The model below only illustrates the connection between accuracy, review effectiveness and a reliability target. It neither reproduces READY's method nor explains the ranking reversal between those two systems. Section 8 of the overview gives the full figures and domain.

**My simplified model, not READY's method**, starts with three assumptions: deep reads are randomly sampled within a stratum; detected errors can be successfully corrected before release; and review does not turn correct results into incorrect ones. Let p be success before deep review, r the share deeply reviewed, and c the probability that deep review successfully corrects an existing error. Success after review is p + (1 − p) · r · c. Requiring it to reach T gives:

> r ≥ (T − p) / ((1 − p) · c)

The right-hand side is the minimum required review share, called r_min below; the actual r must not fall below it. If T is already no higher than p, the model requires no additional deep reads, though human approval remains. A result above 1 means reviewing everything is insufficient. If c is 0 and a gap remains, review cannot meet the target under this model. The three inputs are:

- **p**: that stratum's **pass@1** on the golden set, used to estimate success before deep review. The cases must represent the tasks being released; a mismatch between the golden set and real work cannot be repaired by inserting the number into a formula. pass^k informs the authority decision in section 5 and does not enter this equation.
- **T**: the reliability target for that blast-radius tier, which is to say which cell of the review piece's triage matrix (the table that sets review depth by blast radius and verifiability) it sits in. Changing auth or a schema and changing an internal tool do not get the same target.
- **c**: the probability that an erroneous PR, once selected for deep review, has its error identified and successfully corrected. Detection without correction does not improve success in this model.

c is difficult to estimate, and "our reviewers are senior" is not a substitute. Start with deep-review records whose later outcomes are known, identify errors found and successfully corrected, and track those missed. Undiscovered defects can still be absent from the records, so this remains an estimate. With no history, 0.6 is an illustrative assumption to recalibrate monthly, not measured review performance that can justify expansion.

The assertion study in the testing piece also cautions against treating human review as an infallible safety net. Among 86 developers, judgment accuracy was 49% for incorrect assertions and 74% for correct ones. That measures assertion judgment, not the probability that PR review successfully corrects an error, so neither figure can be substituted for c. The examples below use c = 0.6 only as an illustrative assumption to explore how review effectiveness affects staffing needs.

The next three examples use illustrative values to make the tradeoffs concrete. They do not set a review percentage for the industry. They show how, under these assumptions, better system performance or a different target changes the required effort.

- p = 0.80, T = 0.95, c = 0.6 → r ≥ (0.95 − 0.80) / (0.20 × 0.6) = 1.25. **Even reviewing everything is not enough**; raise p or c first.
- p = 0.90, T = 0.95, c = 0.6 → r ≥ (0.95 − 0.90) / (0.10 × 0.6) ≈ 0.8333. Raising accuracy from 0.80 to 0.90 still leaves more than four-fifths needing deep review. If scheduling in whole percentages, allocate at least 84%.
- p = 0.90 and c = 0.6, with T changed to 0.92 → r ≥ 0.02 / 0.06 ≈ 0.3333, or at least 34% when scheduling whole percentages. This illustrates sensitivity to the target, not a recommendation to lower a reliability commitment to reduce review work.

The examples vary p and then T to expose the cost of different choices. They do not establish that one input always dominates. The questions to bring back to the team are where the target should sit, whether the assumptions are credible and whether the required effort is sustainable.

The computed r_min is the lower bound for sampled deep review in the review piece. In the low-radius, verifiable cell, someone other than the assigner samples at the actual r, with r ≥ r_min. Not every PR gets line-by-line review, but every PR still requires a human to read the report and approve. Compare r_min with the sustainable ceiling r_budget as well; that becomes an authority condition in section 5.

After calculating the review share, decide which tasks to sample. My exam notes warn that aggregate accuracy can hide poor performance in particular categories, motivating stratified random sampling. Here, tasks within the same blast-radius cell can be divided by task type, repo and agent version, with p estimated separately rather than shared as one overall average.

For example, overall p may look good while schema migrations perform less well. Allocating review from the overall average can underestimate the attention those tasks need. Stratification helps staffing follow the risks of the work being reviewed.

The diagram connects estimation with execution. Both p and c need your own data; the 49% and 74% from assertion judgments cannot be inserted as PR-review performance. The formula establishes a minimum, after which the team schedules stratified sampling at or above it:

📌【在此插入圖 diagram-03.png】

Following this sequence gives the review share a rationale: the target, the data source and the assumptions behind the estimate. The diagram uses my simplified model. READY’s 76% → 29.6% belongs to a different example, connecting a reliability target to the review share required in that setting. It is not performance falling from 76% to 29.6%, and cannot calibrate this diagram. Section 8 of the overview gives its full figures and domain.

The monthly report can now bring measurements and staffing together. The format below is illustrative: it lets the people making decisions see agent performance, review demand and actual effort at the same time, instead of receiving one overall pass rate:

```yaml
# eval-report.yaml: one per month, goes into the leadership report
golden_set: { cases: 42, k: 5 }
frontier_set: { cases: 15, k: 3 }
metrics:
  pass_at_1: 0.91
  pass_pow_5: 0.64          # authority expansion reads this column
  constraint_pass_rate: 0.93
oversight:                  # simplified model, computed per stratum
  - stratum: low-radius/verifiable
    p: 0.91
    T: 0.95
    c: 0.60
    r_min: 0.740741          # required minimum, displayed rounded
    r_budget: 0.80           # illustrative sustainable capacity
    r: 0.75                 # ceil to whole %: (0.95 - 0.91) / (0.09 * 0.60)
```

All numbers in this report are illustrative. The upper part shows measurement fields; the lower part shows a stratified calculation. The given p, T and c yield r_min of approximately 0.7407, so scheduling in whole percentages rounds upward to 0.75. Keep the required share, actual share and sustainable ceiling separate so the report shows both whether capacity is sufficient and whether review actually meets the requirement.

Set the reliability target, estimate the review required, then check whether staffing can sustain it. If it cannot, narrow authority, improve the system or add capacity. Do not conceal the gap behind a more convenient sampling percentage.

---

## 5. The gate for expanding authority: back to G2

The measurements and budget now need to support a decision: is this setup ready for broader use by more teams and the authority that comes with it? “Agentic Engineering: Evals, Unit Economics, and Scaling” organizes expansion into three scaling gates, with G2 second. This section adds reliability and review-capacity requirements to its existing conditions.

The operations piece's G2 had three original conditions: retry rate (the share of agent runs that fail and get retried) under 15%, escape rate (the share of defects found only once they reached production) flat, and the champion system (the seed engineers in each team who push agent adoption part-time) running itself, meaning it keeps moving without a central push. This piece adds four, all labeled "my suggested value (not an industry standard)."

A threshold should consider stability as well as attainment. Each condition below requires two consecutive months of evidence: some require sustained attainment, while others also require violations or the required review share not to rise. If violations have already fallen to 2%, the gate should not demand another reduction every month. A healthy steady state needs a path through the gate too.

The small-sample rule matches section 3: below 30 golden-set cases, report pass^5 as a trend and optionally attach a Wilson confidence interval to show uncertainty, but do not use it as an authority gate. Under this proposal, wait for at least 30 cases and two consecutive qualifying months. Attaching an interval does not itself satisfy that requirement.

The four additions assess repeat-run consistency, constraint violations, test effectiveness and review capacity. The third uses the testing piece’s mutation score, the share of valid mutations detected by tests. Placing them together gives each risk its own basis for judgment:

📌【在此插入表 table-03.png】

The last row checks two things: required effort fits within the budget, and actual deep review meets the requirement. r_min is a minimum need; r_budget is a sustainable ceiling. They cannot be represented by the same r. The first three thresholds are also only my starting suggestions and need calibration against your team's data.

The following is a policy design example, not configuration an existing tool can execute directly. It combines the three original conditions with four additions. The oversight condition contains separate checks for capacity and actual execution:

```yaml
# agent-policy.yaml excerpt: extends the G2 format from the operations piece
gates:
  G2_expand_authority:
    all_of:
      - metric: retry_rate            # original condition, operations piece
        op: "<"
        value: 0.15
      - metric: escape_rate
        op: flat_two_months
      - metric: champions_self_sustaining
        op: "=="
        value: true
      - all_of:                     # pass^5 with a minimum sample size
          - { metric: golden_set_cases, op: ">=", value: 30, for_months: 2 }
          - { metric: pass_pow_5, op: ">=", value: 0.60, for_months: 2 }
      - any_of:                       # the two branches of that table row
          - { metric: constraint_violation_rate, op: "<", value: 0.10, not_rising_for_months: 2 }
          - { metric: constraint_violation_rate, op: "<", value: 0.05, for_months: 2 }
      - metric: mutation_score_changed_lines
        op: ">="
        value: 0.70
        for_months: 2
      - all_of:
          - metric: required_deep_read_ratio
            op: "<="
            value: sustainable_review_budget
            not_rising_for_months: 2
          - metric: actual_deep_read_ratio
            op: ">="
            value: computed_r_min
    on_fail: hold                     # hold: investigate, then close verification or review gaps
```

`on_fail: hold` means no expansion when a condition fails. This YAML still needs an evaluator, trustworthy measurement inputs and protection against unauthorized policy changes before it becomes an enforced gate. A file makes criteria reviewable and traceable; the file alone cannot block a bad decision.

Three safeguards sit alongside this gate. First, at G3, the last scaling gate in the operations piece, retain a frozen holdout eval isolated from routine development and self-improvement. Evaluation may present the task to the agent, but an independent evaluation process keeps the answer key and scoring assets away from it. Repeatedly feeding results back must not turn the holdout into a practice set.

Why lock it down that hard? A September 2026 study documents a case from a production self-improvement loop: the agent found a cached answer key, scored 100%, and its real capability was 68%. Access to the answer key made the score a poor measure of capability. The behavior alone does not establish the agent's intent.

The second safeguard is canaries: a small number of probe tasks observed within a controlled scope in production traffic. Offline evaluation and production may differ, so the team needs to watch for new failures. Probes provide signals; a small set cannot establish that production meets the overall reliability target.

The third safeguard concerns scoring evidence. A judge is a model evaluating an agent’s output; its rubric states the assessment criteria. Section 2 of the operations piece identifies three judge traps. Here is another: when a transcript contains the agent’s account of its own actions, the judge must not treat that account alone as evidence that the work happened.

Trap 1 there was about tone: judges prefer long answers and a confident voice. An August 2026 trajectory-judge study analyzed 400 trajectories (see the paper for the task domain) and measured a more specific problem: an agent fabricating action claims of "I did X" fools a step-rubric judge 82% of the time — of every ten fabricated claims, eight get taken as actually done. A step-rubric judge scores step by step against the rubric, and what it is reading is precisely the process the agent wrote down about itself.

Any rubric judgment about what was done needs a corresponding environment record: test results, constraint results or traces, the system-recorded call history. An agent’s statement that it ran tests can help locate the evidence. The result of that CI run is what should support the judgment. This returns to the series’ distinction between a claim and independent evidence.

Back to the gate: no expansion is a decision too. If pass^k falls, examine task composition and model or harness changes before diagnosing the cause. If constraint violations rise, identify the violated rules and investigate regressions or missed checks. The metrics tell us where to investigate; they do not by themselves prove that the remedy is a harness fix or an extra test.

Conversely, when all seven conditions are met and the data and scope have been checked, the policy can support considering expansion. There is no need for a staged rejection to demonstrate caution. Credibility comes from consistent criteria: explain the gap when evidence is insufficient, and acknowledge it when the conditions hold. The four new measurements still do not cover every risk.

These four conditions use accumulated monthly evidence for an authority decision, although some measurements can update continuously. They do not directly answer another question: does the agent repeatedly attempt to cross its permission boundary? That needs an additional runtime signal.

PagerDuty works in on-call and incident management, and in September 2026, at AGNTCon Japan in Tokyo (a technical conference for the agent field), it talked about its own SRE agent. The speaker, Inês Bolaños, positioned it as co-pilot, not captain: the slide that drew the line was titled "THE RED LINE", with one sentence on it, "drafts a fix command. It never touches production." — it drafts the fix command, and production is read-only to it, never written.

That red line serves the same purpose as the earlier rule that changes cannot merge into main without human approval. The constraint-tests section designs the permission boundary; here the task is to measure the agent's behavior. Once the boundary is clear, it becomes possible to record how often the agent tries to cross it and how often those attempts are intercepted.

The H.I.R.E. framework she presented contains five metrics. Red Line Rate measures the share of actions an agent suggests or executes that are intercepted by permission checks, blocklists or security checks. Permission and interception records provide a runtime signal without first requiring a golden set. It extends the question beyond whether the output qualifies: did the agent repeatedly approach prohibited operations while producing it?

I would first include Red Line Rate as an observation in the monthly report, collect two months of data, then assess whether it merits a threshold. It adds a runtime boundary signal; it is not the only metric available for ongoing observation. A rising rate also needs diagnosis: more prohibited attempts, changed permissions or false blocks of allowed actions can all require different responses.

Red Line Rate begins as an observation in this design, not an additional passing condition. G2 therefore still combines three original conditions with four additions. The figure joins them at one decision to show that all seven must hold; a high score on one cannot compensate for a gap in another:

📌【在此插入圖 diagram-04.png】

If only six conditions hold, the team should identify what the seventh lacks and who will address it. Once all seven hold, the owner confirms that the evidence applies to the task scope proposed for expansion. G2 then leaves more than a pass or hold: it preserves a rationale the team can revisit.

---

## 6. Closing and handoff

Returning to the opening 34% from the authority decision clarifies its significance. In SWE-Gate’s sample of Python repair tasks, passing functional tests still left reviewer constraints unsatisfied. From reviewing tests through organizing review to measuring reliability, the series has been building evidence for questions a green result did not answer.

This piece breaks that gap into three metrics that can be measured or calculated. The monthly report presents constraint pass rate, pass^5, and human-review needs alongside the actual share and sustainable capacity. They answer three different questions.

The first question is rules. Constraint pass rate answers whether this agent kept the rules the team laid down. Those rules used to remain in review comments. The next time the same problem appeared, a colleague had to remember and raise it again. Once they become constraint tests, CI can keep checking them, and the team no longer has to place that burden of memory on the same person.

The second question is consistency. pass^k records how many cases in this set succeeded on all k attempts. It reveals variation beyond a single success, but does not guarantee the next result. Changes to tasks, models or the harness require reconsidering what the existing measurements still support.

The third question is staffing. r_min estimates the minimum review required under the target and model assumptions; r records actual allocation, and r_budget is what the team can sustain. Showing all three makes the resulting work and available capacity visible before autonomy expands.

G2 already tracks retries, escaped defects and the champion system. The four new conditions add test effectiveness, team constraints, repeat-run consistency and human-review requirements. Together they help the team judge whether this class of tasks has sufficient verification and whether it can sustain the work that broader authority would bring.

The four thresholds are starting suggestions, not industry standards. Teams can adjust them using their own data, while retaining the rationale and evidence for each change. Missing a threshold this month is not by itself a reason to lower it just enough to pass. The habit I want to preserve is making authority decisions open to scrutiny and assigning responsibility for them.

The approach still has boundaries. Constraints recovered from review history cannot replace a specification that remains unclear. If requirements are ambiguous, adding CI rules does not automatically establish which behavior the team intends.

Likewise, repeatedly passing the same specification and producing similar implementation structures are different questions. pass^k assesses the former. Even after five passing attempts, comparing the code and design is still necessary to discuss the latter.

Offline evaluation also cannot stand in for production service performance. An SLI, or service level indicator, needs measurements from actual operation, with a clearly defined measurement scope, time window and data source. Reporting pass^k and r supports the authority and staffing decisions discussed here; it does not automatically make them production SLIs.

If there is one sequence to retain, I would first establish meaningful checks of functionality and team constraints, then assess consistency across repeated tasks. The success criterion for pass^k must include those requirements, or it can describe consistently missing the same problem. Human review is a separate axis: estimate the need under the chosen target and assumptions, then confirm sufficient capacity and actual review at or above the minimum.

That sequence makes room for the people who receive the work. If a team expands authority before discovering that its tests miss key behavior, the gap eventually falls to reviewers and on-call engineers. Making evidence and review demand explicit beforehand lets them help decide the scope, rather than inherit unaccounted work after an incident.

> **Green tells you the functional checks that ran did not fail. Constraint tests add the team's rules; pass^k checks consistency across repeated attempts. Together they inform authority decisions. None can vouch for the other two.**

At the reliability gate, we can return to the question that began the series: when the tests were written by the agent, does a green build still count? It does, but only for the layer it actually checked. The remaining constraints, consistency and human-review requirements are what these three numbers keep track of.

Part 4, “A Payment Walkthrough,” returns to one order for unsweetened green tea: select constraints from Review comments, turn them into tests, then examine what the mutation score still misses. It gives the decisions in the first three parts a reproducible starting point, while retaining this piece’s caution: one payment example cannot replace reliability evidence from repeated attempts across a task set.

---

### The series

- [Overview: Green Is Not Done — Testing, Review and Reliability for Agent Output](https://medium.com/p/c4fc9f3d8581)
- [Part 1 — Reviewing the Tests an Agent Wrote: Loosened Assertions, Frozen Bugs and Mutation Score](https://medium.com/p/51d001a6dcd5)
- [Part 2 — Review Is the Control Point, Not the Bottleneck: Triage, Reviewer Fleets and the Closed-Loop Ban](https://medium.com/p/4d36d0f2f9c1)
- **Part 3 — The 34% SWE-Gate Found Behind a Green Build (this piece)**
- Part 4 — A Payment Walkthrough: Buying Unsweetened Green Tea, from Review Constraints to Mutation Score (coming soon)

---

### References

1. SWE-Gate — [arXiv 2609.04167](https://arxiv.org/abs/2609.04167) (2026-09) — section 1; 75 Python repos, 303 patch tasks
2. SWE-NFI — [arXiv 2607.27409](https://arxiv.org/abs/2607.27409) (2026-07) — sections 1 and 2
3. OpenHarmony Bench — [arXiv 2608.16022](https://arxiv.org/abs/2608.16022) (2026-08) — section 1
4. Rebuild Dossier — [arXiv 2608.23616](https://arxiv.org/abs/2608.23616) (2026-08) — section 1; design premise
5. Accepted review comments as version-controlled rules — [arXiv 2607.13091](https://arxiv.org/abs/2607.13091) (2026-07) — section 2
6. RealSWE — [arXiv 2608.27831](https://arxiv.org/abs/2608.27831) (2026-08) — section 3; 381 task families
7. Sensitivity to semantics-preserving rephrasing — [arXiv 2608.18389](https://arxiv.org/abs/2608.18389) (2026-08) — section 3; 6 of 16 significant
8. Thinkingbox — [arXiv 2608.19741](https://arxiv.org/abs/2608.19741) (2026-08) — section 3; corroboration from outside code
9. READY — [arXiv 2609.02095](https://arxiv.org/abs/2609.02095) (2026-09) — section 4; full numbers in section 8 of the overview
10. trajectory-judge — [arXiv 2609.00038](https://arxiv.org/abs/2609.00038) (2026-08) — section 5; 400 trajectories; domain in the paper
11. LLM-as-a-Judge Is Not an Oracle — [arXiv 2609.02246](https://arxiv.org/abs/2609.02246) (2026-09) — section 5
12. Author's notes: Claude Certified Architect — Foundations exam notes (stop_reason, stratified sampling)
13. Agentic Engineering: [Agentic Engineering, Part 3 — Evals, Unit Economics, and Scaling](https://fantasybz.medium.com/agentic-engineering-part-3-evals-unit-economics-and-scaling-running-agents-like-a-product-1cb1855a2046), sections 2 and 5 (the three judge traps, the G2 gate)
14. PagerDuty — [From Clicks To Context: Building an Open-Source Evaluation Pipeline for AI Agents](https://sched.co/2QlEA) (AGNTCon + MCPCon Japan 2026, 2026-09-11) — section 5; [slides](https://hosted-files.sched.co/agntconmcpconjapan26/57/From%20Clicks%20to%20Context_%20Building%20an%20Open-Source%20Evaluation%20Pipeline%20for%20AI%20Agents%20_%20Ine%CC%82s%20Bolan%CC%83os.pdf#page=15) p. 15, the slide titled “THE RED LINE”, and [p. 21](https://hosted-files.sched.co/agntconmcpconjapan26/57/From%20Clicks%20to%20Context_%20Building%20an%20Open-Source%20Evaluation%20Pipeline%20for%20AI%20Agents%20_%20Ine%CC%82s%20Bolan%CC%83os.pdf#page=21) for the Red Line Rate of H.I.R.E.
15. Accompanying implementation — [Tea payment, constraint tests and seven selected mutants](https://github.com/fantasybz/medium-articles/tree/main/examples/tea_payment) [section 2; measured teaching example, no real provider]

---

### On how this piece was made

The initial concept and chapter structure are the author's; the prose was drafted in collaboration with AI (Claude), then reviewed and revised section by section by the author before publication. The views and judgments are the author's own, as is responsibility for the content.

---

*Originally published in Chinese: [中文版](https://medium.com/p/3c64a9622777). Also on [Medium @fantasybz](https://medium.com/@fantasybz) — if you're designing the gate for expanding an agent's authority, I'd like to hear from you.*
