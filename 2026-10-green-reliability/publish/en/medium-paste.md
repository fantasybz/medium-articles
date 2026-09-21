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

> **TL;DR** — The final part of the trilogy, on the reliability gate: which numbers decide whether an agent's authority gets expanded. SWE-Gate measured it on 75 Python repos and 303 patch tasks: of the 644 patches that passed the functional tests, 221 (34%) violated a constraint a reviewer had actually added — one in every three green patches broke a constraint the reviewer cared about. This piece is about three numbers only. **Constraint pass rate**: write review constraints as executable constraint tests (review comment → rule → check), so that "what the reviewer cares about" becomes part of CI. **pass^k**: reliability is not capability — pass@1 is each case's single-attempt success rate, pass^k is the share of cases that pass all k times; report them separately. **Oversight budget**: two systems 0.3 percentage points apart in accuracy can differ by nearly 10 percentage points in the human review they need (READY), so "how many people have to look" is a budget derived backward from your reliability target, not "look as much as you can" — this piece gives a simplified model so you can compute your own. The three numbers go into the monthly leadership report and connect back to the G2 gate of the operations piece: expanding authority looks at pass^k, constraint pass rate and escape rate, not at pass@1.

> Series: [Overview](https://medium.com/p/c4fc9f3d8581) → [1. Testing](https://medium.com/p/51d001a6dcd5) → [2. Review](https://medium.com/p/4d36d0f2f9c1) → **3. Reliability (this piece)**

---

## 1. The 34% SWE-Gate measured

Start with a number that anchors the gap this piece is about. The overview used this number too, in its table of the three layers a green build cannot measure, and the layer where functional tests pass but the constraints are not met was left to this piece. SWE-Gate is a benchmark paper, and what it measures is exactly what a green build covers. It did one extra thing: it did not only ask whether the functional tests passed. It also pulled out what the reviewers had actually asked for on those PRs, turned each of those asks into an executable check, and ran them as a separate pass.

The 34% is what SWE-Gate (September 2026) measured on 75 Python repos and 303 patch tasks. Of the 644 patches that passed the functional tests, 221 violated one of those constraints. In plain language: one in every three green patches violates a constraint the reviewer cared about.

There are two ways to misread that number, so let me block both first.

The domain boundary comes first — Python repos, patch tasks, not "all agent PRs." That is the range it measured. Change the language, change the shape of the task, and the number has to be measured again.

Look at the denominator too. The denominator is "patches that passed the functional tests," so the correct plain-language reading is "one in every three green patches violates a constraint." It is **not** "a green build misses a third of what reviewers care about." That version swaps the unit for a share of "the things reviewers care about," which the paper did not measure. The two sentences look almost identical, but their denominators are not, and taking the wrong one into an argument gets you knocked over by the first follow-up question.

A green build has layers, and each layer has evidence from the same domain: measured on a language and a shape of task close to yours, not numbers borrowed from somewhere else. Of the three studies below, the first two sit one on each layer, and the third gives the premise all those layers share.

SWE-NFI (188 tasks, 92 executable rules) measures "passing functionally does not mean the non-functional rules are satisfied": the best agent passed 70.0% functionally and fell short on the non-functional rules across the board. Non-functional rules are things like performance, security and log format — requirements that never turn a functional test red, and that the team cares about all the same.

OpenHarmony Bench (153 app tasks) measures a layer further down, "**a green build does not mean the behavior is right**": buildable 94.77% to 100%, behaviorally correct only 48.36% to 58.39%. The gap is far wider, but behavioral errors are what functional tests are supposed to catch in the first place, so it does not sit in the 34% layer.

Rebuild Dossier is a design premise, not an observed result. It is a paper proposing the process an agent should follow when it rebuilds an entire app: when the agent has a chance to game the tests, a fully passing suite does not mean correct, so it locks the interface first and hands over one test at a time. What it gives you is not a number but a reminder: as long as the agent can change the implementation and the tests in the same breath, a fully passing suite stops being independent evidence.

Once the layers are laid out, one thing becomes visible: all three look identical on a dashboard. The light is green in every case. The only difference is what that light measured, and whether you went and measured the rest yourself. A green build never volunteers what it left out, and that is exactly what makes it dangerous.

This piece deals with only two of those layers. One is the reviewer constraints, which is what the opening number measured. The other is reliability, which is whether the same thing done again still comes out right. None of the three studies above measured that layer; this piece measures it itself in the reliability section, and when it does, it only accepts the kind of independent evidence Rebuild Dossier warned about. Below, the constraints get written as checks first, then capability and reliability get measured separately, then the bill for review gets computed, and finally it all connects back to the gate.

---

## 2. Writing review constraints as executable constraint tests

The last section said one in every three green patches violates a constraint the reviewer cared about. This section is the most direct answer to that: write those constraints as checks CI can run. Checks like these have a name — constraint tests. They do not verify that the functionality is right, which is what functional tests are for. They verify one thing only: whether this PR stepped on a rule the team has already stated out loud.

What does a constraint look like? Think of it first as the things a team says over and over but should not have to rely on a person to remember every time. The seven categories below are what I distilled from my teams' review comments, meant to show where constraint tests can grow from, not to be a complete taxonomy; for SWE-NFI's 92 rules and SWE-Gate's comment taxonomy, the papers themselves are the authority:

📌【在此插入表 table-01.png】

The column worth looking at in that table is the rightmost one. Seven kinds of constraint, seven ways to check them, and not one of them needs an LLM to judge anything: lockfile diffs, AST (the syntax tree of the code) scans and import graphs are all old tools. Turning review constraints into checks has a lower bar than most people assume.

The pipeline is four steps: review comment → rule → constraint test → CI. The rules file (one file in the repo that records every rule) has its shape borrowed from a July 2026 study: every accepted review comment becomes one entry in that rules file under version control (section 3 of the review piece reuses that same file). The reason for borrowing it is simple: a comment that got accepted means the team has already agreed to that rule, and there is no reason to make a person say it again on the next PR.

The rules file records two kinds of thing. The first is provenance: each rule records its source PR and date, and a rule that has not fired in six months gets reviewed for expiry. The second is responsibility, which is why there are two more fields — owner (who maintains this rule) and expiry (the date it comes up for review). Rules rot precisely because nobody owns them and nothing expires, and these two fields are the mechanism that keeps them from rotting.

Now that the rules have an owner, the next question is whether the agent can change them. Section 2 of the overview splits evidence into three classes: the first is what the agent says, the second is the tests the agent wrote itself, and the third is the tests the agent cannot change. What lands here is that third class, and the mechanism has three parts.

First, `tests/constraints/` and the golden set directory go into CODEOWNERS, listing humans only. CODEOWNERS is the file GitHub uses to specify which directories need approval from whom; the golden set is the batch of acceptance cases the team picked itself, defined in the next section. Second, changes to the rules file need human approval. Third, any weakening of an assertion in a test of the third class is blocked outright by Check 2 from the testing piece.

The agent has write access to the repo, but a change to these three paths does not reach main without a human approval. "Cannot change it" does not mean the agent is forbidden to touch them; it means touching them gets it nowhere.

Walk one real comment through those four steps. Before, it is the comment a human has to repeat every time: "Please don't `new HttpClient` directly here, use `clients.http()`." It only ever covers the one PR in front of it, and once it has been said it is gone. After, it becomes three things: an executable check, a rule with an owner, and a door the agent cannot move.

The first is the test file. It only scans the Python files this PR touched, so it runs in seconds:

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

The third is CODEOWNERS. The first two make the rule exist; this one makes it unchangeable:

```text
# CODEOWNERS
/tests/constraints/   @acme/platform-humans
/tests/golden/        @acme/platform-humans
/rules.md             @acme/platform-humans
```

Put the three together and that review comment goes from "a person has to say it every time" to "said once, then checked on every PR after that." That is what compounding means here: one comment a human wrote while reading a diff covers that one PR and no more; recycled into a constraint test, it covers every PR not yet written.

How cheap that compounding is can be put plainly too. Constraint tests are deterministic (rule-based, the same result on every run), run in seconds, and their reach is the whole PR. "Reach" is the word section 10 of the overview uses for how much code one check covers in a single run: a unit test covers only the lines that got called, while a constraint test covers the whole diff.

By that principle, they are the cheapest verification there is, and the first gate for a brownfield system. Brownfield means an existing system that has been running for years, with incomplete tests and incomplete documentation. What such a system fears most is "you need tests before you can start," and constraint tests need no existing tests.

So how does a team with no review history get started? Start from the team's conventions and the last five incidents, and write those "let's not do that again" sentences down as checks first.

Draw the four steps, comment → rule → test → CI, as a diagram, and the thing to look at is not the main line on the left but the dashed line coming back on the right:

📌【在此插入圖 diagram-01.png】

What to take from this diagram is that dashed line: a rule is not settled once it is written. A rule base with no expiry loop turns, two years on, into a pile of checks nobody dares delete and nobody believes, and then the whole mechanism gets routed around.

Before this section closes, the boundary with November's contracts piece has to be drawn, or the two kinds of constraint blur into one. The constraints in this piece come from **review history**: accumulated after the fact, empirical. The contracts piece's constraints come from the **spec**: agreed up front, normative.

Both go into CI, but they have different owners and different lifespans. A review constraint is owned by the team that raised the comment in the first place, and its lifespan is set by its expiry — when that date arrives, somebody has to confirm it still holds. A spec constraint follows the spec: as long as the spec is there, so is the constraint.

---

## 3. Reliability is not capability: pass@1 and pass^k

The last section was about whether the rules got kept. This one is about something else: do the same thing again, and will it still come out right? Capability and reliability are two numbers, and plenty of teams collapse them into one, so let me pin the definitions down first.

The definitions follow section 8 of the overview: run every case in the golden set k times. The golden set is the batch of acceptance cases the team picked itself and reruns unchanged every month.

**pass@1 is the single-attempt success rate, estimated from the k repeated runs.** Per case, it is the number of passes out of k divided by k. The question it answers is whether the agent can do this on average.

**pass^k is the share of cases that succeed on all k runs.** One failure anywhere in a case and the whole case does not count. The question it answers is whether the agent can do this every time.

Both are computed per case first, then aggregated over the whole golden set. This step is easy to get wrong: pool all the runs together and average them, and "one case that fails every time" comes out looking exactly like "every case failing once in a while" — and those two call for completely different responses.

There is one more symbol that looks almost the same, so rule it out now: "the share that succeeds at least once" is pass@k, a different number, and this series does not use it.

Besides pass^k, the monthly report has one more column, constraint pass rate: among the PRs that passed the functional tests, the share that also pass every constraint test. With the two numbers side by side, the next sentence is load-bearing: **pass^k and constraint pass rate can only be computed from the third class of evidence** — only from the tests the team owns and the constraint tests. The agent's closing report does not count, and neither do the tests it added itself that have not yet been promoted. Promoted means a human has looked at that test, moved it into a directory the team owns, and put it under CODEOWNERS.

My notes from preparing for Anthropic's Claude Certified Architect certification exam hold the smallest possible example: you do not guess whether the agent's turn has ended from the assistant's reply text, you look at stop_reason (the "why it stopped" field in the API response, filled in by the system). The reply text is what the model says about itself; stop_reason is what the system recorded. They do not come from the same source. Moved to code it is the same thing: "the tests all pass" is the agent talking about itself, and red or green in CI is what the system recorded. That is what "the first class of evidence is not evidence" means.

Why run code k times instead of trusting a single run? Because the agent's score wobbles with how the task is worded, and anything that wobbles cannot be measured just once. The evidence is two studies of rephrasing sensitivity.

RealSWE (381 task families) measured this: reword the same task and the average drops 6.4 percentage points, and the model rankings reshuffle. The reshuffling is the more troublesome half. It means part of what you are reading off a leaderboard is how the task was worded, not a gap between the models.

Another study of semantics-preserving rephrasing measured a drop of a similar size: an average of up to 6.7 percentage points, **but only 6 of the 16 model-and-scaffold combinations reached statistical significance.** So the right reading is not "every model is equally shaky" but that the effect is real and uneven. Whether your own combination is shaky is something you have to measure on your own combination.

Ask the same thing in different words and get a different result: that is a reliability problem.

The corroboration comes from outside code, and this is the only place in the whole series that quotes the full numbers. What Thinkingbox (a benchmark paper) measured is 507 policy-conditioned MCP workflows — multi-step tool-calling tasks carrying policy constraints, where the agent has to keep calling tools through MCP (the protocol for calling tools) and keep the rules at the same time. On that batch, Claude Opus 5 scored 66.50% pass@1 and 47.53% pass^20. You would expect two out of three attempts to come out right, and yet fewer than half of the tasks come out right twenty times in a row.

The two numbers sit nearly twenty percentage points apart, and that gap is what separates capability from reliability.

Its conclusion — "clean termination and valid tool calls are not proxy indicators of completion" — holds in the code domain just the same: the agent saying it finished, with every tool call well formed, is a different thing from the task having been done right.

So how do you do this on your own evals? Reuse the operations piece's golden set, 20 to 50 cases, and run it monthly at k = 5; that is the set the thresholds are read off. The frontier set runs separately at k = 3: it is a harder batch that does not pass yet, there to show where the ceiling is, and it is not used as a threshold. The report has three fixed columns, so every month you are looking at the same numbers; the third number from the opening, the oversight budget's r, is a policy derived from those three columns, and the oversight-budget section is where it gets computed.

The three columns look like this:

📌【在此插入表 table-02.png】

The most important column in that table is the rightmost one: all three numbers come from something the team owns. If you cannot name that source for a column, that column does not belong in the monthly report.

The source comes before the threshold. **My suggested value (not an industry standard)**: k = 5, and pass^5 ≥ 60% before anything counts as "allowed to run autonomously at low blast radius," meaning the class of PR where a bad change can still be taken back.

**Granularity warning**: with fewer than 30 cases in the golden set, report pass^k as a trend only, not as a threshold — 20 cases give a granularity of 5 percentage points, one case flipping takes you from 65% to 60%, and month-to-month noise dominates. If you really want it as a threshold, it has to be met two months in a row.

Lay three cases out and compute both numbers once, and the difference becomes visible. The one to watch is case B in the middle, which fails exactly once:

📌【在此插入圖 diagram-02.png】

One sentence to take from this diagram: on the same batch of golden cases, pass@1 of 93% and pass^5 of 67% are two different numbers, not two ways of writing the same one. The first says it is good on average; the second says you cannot let go yet. Authority looks at the latter.

---

## 4. Oversight budget: READY and a simplified model

The last section gave you two numbers; this one deals with their bill: the oversight budget, which is "how much human effort am I planning to spend on review this month." The higher the reliability target, the more people you have to pay to read.

How to estimate that budget: start with a study that actually computed it. READY is a qualification framework for enterprise agent deployment (September 2026). One idea in it is especially useful here: do not look only at the agent's accuracy, work backward from a reliability target to how much human review an "agent plus human-review policy" needs. What it measured is counterintuitive: two systems only 0.3 percentage points apart in accuracy had human-review requirements that differed by nearly 10 percentage points, and it was the less accurate one that needed fewer people. In this piece READY is used to prove exactly one thing: **the ranking by accuracy is not the ranking by human effort.**

Let me be clear about what is borrowed and what is not. Its case is a clinical-audit workflow, not code — only the concept is borrowed here, and none of the numbers transfer. Its reversal, the less accurate system needing fewer people, is not something the simplified model below reproduces either; what I borrow is the sensitivity alone. The full numbers and the domain caveat are in section 8 of the overview. I make no promise of reproducing its numbers, and its method certainly accounts for more than the simplified model below does.

**My simplified model (not READY's method)**, which turns "the share of PRs under human review" into something you can compute:

> r ≥ (T − p) / ((1 − p) · c)

Read plainly, the formula says this: the gap between the target and where you are has to be closed by human eyes, and human eyes only close c of it. The wider the gap and the less reliable the eyes, the larger the share you have to deep-read. The three inputs are:

- **p**: that stratum's **pass@1** on the golden set. Reviewing a single PR uses per-attempt accuracy, not the all-k pass rate. pass^k is reserved for the authority expansion in section 5 and stays out of this formula.
- **T**: the reliability target for that blast-radius tier, which is to say which cell of the review piece's triage matrix (the table that sets review depth by blast radius and verifiability) it sits in. Changing auth or a schema and changing an internal tool do not get the same target.
- **c**: the probability that human review catches an error.

Of the three, c is the one most likely to get skipped, and it is the one that decides the most. Compute c from your own history of sampled deep reads: of the deep-read PRs later confirmed to have a defect, what share was caught during the deep read itself. With no history, start at 0.6 and recalibrate monthly.

The human eye is not a safety net, and the testing piece has the numbers: 86 developers judging LLM-written assertions, only 49% of the wrong ones caught and 74% of the right ones recognized. Put a wrong assertion in front of a person, in other words, and there is a one-in-two chance it gets waved through. Those figures measure judging assertions, not catching defects in PR review, and they cannot be used as c directly. Here they are only a warning: the human eye cannot be assumed to be 100%. The c = 0.6 in the worked examples below is that starting value. The human catch rate directly decides how much human effort you pay for.

Below I work through it with numbers of my own. The point is not to memorize the formula, but to feel one thing first: the share of human review that comes out is usually much higher than intuition suggests.

- p = 0.80, T = 0.95, c = 0.6 → r ≥ (0.95 − 0.80) / (0.20 × 0.6) = 1.25. **Even reviewing everything is not enough**; raise p or c first.
- p = 0.90, T = 0.95, c = 0.6 → r ≥ (0.95 − 0.90) / (0.10 × 0.6) = 0.83. Raising accuracy from 0.80 to 0.90 only turns "even everything is not enough" into "review eighty percent."
- p = 0.90, c = 0.6, with T lowered to 0.92 → r ≥ 0.02 / 0.06 = 0.33. The target dropped by only three percentage points, and the human effort fell from eighty percent to thirty.

Put the three examples side by side: p changes first, then T. The first time you run the numbers you will probably find that which cell the reliability target sits in decides human effort more than the agent's accuracy does.

Where does the r you computed go? Into the review piece's triage matrix. The low-radius, verifiable cell has an item called "deep-read sampling by someone other than the assignee" (someone not assigned to this PR samples it and reads it line by line), and its share is the r computed here. Every cell still has a human reading the report and approving; r only decides what share of those get read line by line.

The sampling has to be stratified as well. Another line from my exam notes: aggregate accuracy hides low performance on particular categories, so use stratified random sampling. Moved to code, there is one more cut inside the same blast-radius cell: task type, repo and agent version, with p computed separately for each.

Suppose a team's p looks fine overall, but comes out a good deal lower when schema migrations are counted on their own. Look only at the aggregate and you staff to the flattering number, then pull people away from the very category that needed more of them.

Draw the whole path as one diagram. The 49% and 74% written in the c box are the two numbers of the warning above; they give an order of magnitude, not a measured value of c: the human eye is not 100%. The box to look at is the bottom one: r is not the end of it; stratified sampling still has to catch it:

📌【在此插入圖 diagram-03.png】

What to take from this diagram is the direction of the arrows: the human-review share is a budget derived backward from the reliability target, not a constant. The worked example in the diagram is mine; compute your own numbers. READY's own worked example is 76% → 29.6%, where the first is a reliability target and the second is the human-review share computed under that target, not a drop along one axis; the full numbers are in the overview.

Three numbers plus a budget: put them together and you have the report that gets handed over every month. It looks like this:

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
    r: 0.74                 # (0.95 - 0.91) / (0.09 * 0.60)
```

The part of that report to look at is the last block. Oversight is written per stratum, not as one company-wide number: each stratum has its own p, so it has its own r. The metrics above are measured facts, the block below is the policy you derived from them, and putting both in the same file is the only way to see whether the policy is actually tracking the numbers.

What this section is really for is an ordering: set the reliability target first, then compute how much human review you have to pay for. Not count the reviewers you happen to have, then work backward to how much you dare hand the agent.

---

## 5. The gate for expanding authority: back to G2

The four sections so far have given you numbers and a budget. This one connects them to a place where they actually change behavior: whether authority gets expanded to the next batch of teams. That gate already exists in the operations piece: the operations piece has three scaling gates, and this is the second. What this section does is add the reliability side of it.

The operations piece's G2 had three original conditions: retry rate (the share of agent runs that fail and get retried) under 15%, escape rate (the share of defects found only once they reached production) flat, and the champion system (the seed engineers in each team who push agent adoption part-time) running itself, meaning it keeps moving without a central push. This piece adds four, all labeled "my suggested value (not an industry standard)."

Every threshold uses the same sentence form, "met, and not rising / not falling for two consecutive months," never "falling for consecutive months" — once a steady state gets down to 2% there is nothing left to fall, and the gate can never pass again. Demanding that a metric keep dropping forever amounts to designing the gate to jam at the healthiest moment, and then the whole thing gets torn out.

The small-sample rule is the granularity warning of section 3. With fewer than 30 cases in the golden set, the single number for pass^5 (the point estimate) is not a threshold. Either report it together with its Wilson interval, or wait for "two consecutive months plus at least 30 cases" before using it as a gate. A Wilson interval is a confidence interval for a proportion from a small sample; it turns "I only have twenty-odd cases" into a width you can see on the report.

The four new conditions are below, and the rightmost column is what each of them is there to block. The mutation score in the third comes from the testing piece (break the code on purpose and see whether the tests go red; the share that do is the score):

📌【在此插入表 table-03.png】

The row worth looking at is the last one. The thresholds in the first three you can copy; that one you cannot. Its threshold is the r you computed yourself with the formula in the previous section, and it comes out different for every team.

Written into the policy file it looks like this, with every entry matching a row in that table:

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
      - metric: pass_pow_5            # added in this piece
        op: ">="
        value: 0.60
        for_months: 2
      - any_of:                       # the two branches of that table row
          - { metric: constraint_violation_rate, op: "<", value: 0.10, not_rising_for_months: 2 }
          - { metric: constraint_violation_rate, op: "<", value: 0.05, for_months: 2 }
      - metric: mutation_score_changed_lines
        op: ">="
        value: 0.70
        for_months: 2
      - metric: deep_read_ratio
        op: "<="
        value: computed_r             # section 4's simplified model
        not_rising_for_months: 2
    on_fail: hold                     # no expansion: fix the harness or add constraint tests first
```

The line to look at in that excerpt is the last one. `on_fail: hold` means a failed gate is no expansion, not "expand now and fix it later." Writing the gate as a file instead of a slide is exactly what this buys: a file cannot be talked round in a meeting room.

Beyond this gate, three more things have to be added together. The first goes on the gate above this one, against the eval being contaminated by the system itself. G3 (the last of the operations piece's three scaling gates) gets one more condition: the frozen holdout eval must not be touched by the agent or the harness (the layer of interface between the agent and the engineering system, from the harness piece). A frozen holdout eval is a batch of tasks locked away where neither the agent nor the harness can see them, and the only reason it exists is not to be optimized against.

Why lock it down that hard? A September 2026 study documents a case from a production self-improvement loop: the agent found a cached answer key, scored 100%, and its real capability was 68%. It was not trying to deceive anyone. It found a shorter path, and that path was one you had not blocked off.

The second is canaries: a small set of probe tasks mixed into production traffic, there to confirm that the numbers from the lab still hold in the real environment.

The third is the judge trap. A judge is one model scoring another agent's output, and the rubric is the scoring sheet you hand it. Section 2 of the operations piece listed three traps; the fourth one goes here: do not let the transcript (the execution record the agent writes about itself) prove itself.

Trap 1 there was about tone: judges prefer long answers and a confident voice. An August 2026 trajectory-judge study read 400 trajectories (see the paper for the task domain) and measured a more specific layer: an agent fabricating action claims of "I did X" fools a step-rubric judge 82% of the time — of every ten fabricated claims, eight get taken as actually done. A step-rubric judge scores step by step against the rubric, and what it is reading is precisely the process the agent wrote down about itself.

So the factual items a rubric binds to have to be verifiable from the environment — test results, constraint results, traces (the call trail the system recorded) — not from the transcript. The agent saying it ran the tests, and that run actually appearing in the CI record, are two things you can check against each other. The first is the agent talking about itself; the second is not.

Back to the gate. "No expansion" is also a decision. If pass^k drops, go back and fix the harness first (see the harness piece), and do not push through. If constraint violations rise, add constraint tests first, and do not push through there either. How much verification to buy, and which to buy first, is section 10 of the overview.

But when the numbers are all good, expand — do not stage a fake no just to "prove the gate works." A gate earns its credibility by moving in both directions: it holds, and it also lets things past. But these four new conditions share one blind spot.

All four new conditions have to wait for a PR to come in and the monthly report to come out before they can be computed at all. What do you look at in between two reports? Not one of the four answers that.

PagerDuty works in on-call and incident management, and in September 2026, at AGNTCon Japan in Tokyo (a technical conference for the agent field), it talked about its own SRE agent. The speaker, Inês Bolaños, positioned it as co-pilot, not captain: the slide that drew the line was titled "THE RED LINE", with one sentence on it, "drafts a fix command. It never touches production." — it drafts the fix command, and production is read-only to it, never written.

That red line is the same line as "touching them gets it nowhere" in the constraint-tests section. The difference is that there it is design and here it is measurement: only once the line is drawn hard can you measure how often the agent runs into it.

The H.I.R.E. evaluation framework she presented has one metric that measures exactly this, Red Line Rate: the share of actions the agent suggests or executes that a permission check, a blocklist or a security check rejects. The permission layer emits it directly, it needs no golden set, and it does not wait for a PR or a monthly report — the reliability section's rule, that a column you cannot name a source for does not belong in the monthly report, is one this metric can answer.

For me it is an observation for now, not a threshold: this gate only takes numbers with two months of baseline behind them, and Red Line Rate does not have that yet. It goes into the monthly report first, and once two months have accumulated we can talk about the gate. That makes it the one number outside the gate that moves before an expansion happens: no waiting for the month to close, you can look at it any time.

The gate itself is still seven conditions. Stack the original conditions and the new ones together and you have the gate as it now stands. The thing to look at is the diamond in the middle: it is an and, not a vote:

📌【在此插入圖 diagram-04.png】

What to take from this diagram is the shape G2 now has: three original conditions plus four new ones, and all seven have to pass. Six is not a pass. This gate has no cell for "close enough."

---

## 6. Closing and handoff

The last section wrote the four new conditions into that gate, and with that everything this piece had to hand over is handed over. What is left is to go back to the gap in the opening. What SWE-Gate measured is not that agents cannot write code; it is that "the tests are green" never promised what you took it to promise. The trilogy went from the testing piece through the review piece to this one, and all three are working on the same gap. A green build is a check, and a check does not volunteer what it did not measure.

This piece breaks that gap into three things you can measure. Three numbers go into the monthly report: constraint pass rate, pass^5, and the oversight budget's r. They are not three views of one thing; they are three different questions.

The first question is rules. Constraint pass rate answers whether this agent kept the rules the team laid down. Those rules used to live only in review comments, kept alive by somebody remembering and saying them again. Written as constraint tests, they live in CI instead, and no person has to be that memory any more.

The second question is steadiness. pass^k answers whether what it managed this time it will still manage next time. Between succeeding once and succeeding several times in a row sits the question of whether you dare let go.

The third question is the bill. r answers how much human effort you pay to cover the part that steadiness does not cover on its own. It is derived backward from the reliability target, not called out by feel.

On the gate side, G2 gains four conditions. The point of adding them is not to pile the bar higher but to change what is being judged. The old question was whether the agent finished the task; the new one is whether it can finish it verifiably, steadily, and at a review cost you can afford. Those three adjectives are the three numbers above, in the same order.

All four are my suggested values, not an industry standard, and the thresholds themselves should be rewritten by your own data. What I want to leave behind is not the numbers but the habit of arguing about expanded authority against numbers at all.

Next month's contracts piece picks up the other half of the split made earlier here: the constraints that come from the spec. How two kinds of constraint with different origins sit in the same CI, and how their owners and expiry dates get arranged, is left to that piece.

November also turns pass^k over to its other side: pass^k is the outcome side of "run the same spec N times"; November measures the variance side, the structure of the implementations. Five runs of the same spec all passing does not mean the code came out the same way five times, and that is a different kind of variance.

There is one more thing at the end of the year. The two numbers pass^k and r do not stop at the monthly report — they become SLIs in December. An SLI is a service level indicator, the number actually measured behind the level a service promises to the outside. When a number goes from the monthly report to an SLI, it goes from a number you look at yourself to a number you are answerable to someone else for. That is why granularity, sample size and the handling of small samples have to be spelled out now.

If there is only one thing to take away, it is the order of the three layers below: a green build at the bottom, constraint tests in the middle, pass^k on top. r is not on that axis — it is the bill that comes due once all three have been computed. I do not think they can be swapped, because each layer above assumes the one below it already holds.

It is not hard to picture what the reverse order looks like. A team sees that the agent writes well, so it loosens authority first, goes back to fill in the team's rules afterward, and only then finds out that the functional tests were never measuring what they should have been. Every step on that path looks reasonable on its own; put together, they leave the weakest layer holding everything else up.

> **A green build tells you the agent did not break the functionality; constraint tests tell you whether it kept the team's rules; pass^k tells you whether you can let go. You need all three, and the order cannot be reversed.**

That is the end of the trilogy. It started from one question: when the tests were written by the agent, does a green build still count? It does, but only for the layer it measured. Everything it left out is where these three numbers take over.

---

### The series

1. [Overview: Green Is Not Done — Testing, Review and Reliability for Agent Output](https://medium.com/p/c4fc9f3d8581)
2. [1. Reviewing the Tests an Agent Wrote: Loosened Assertions, Frozen Bugs and Mutation Score](https://medium.com/p/51d001a6dcd5)
3. [2. Review Is the Control Point, Not the Bottleneck: Triage, Reviewer Fleets and the Closed-Loop Ban](https://medium.com/p/4d36d0f2f9c1)
4. **3. The 34% SWE-Gate Found Behind a Green Build (this piece)**

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
13. Last season's operations piece: [Agentic Engineering, Part 3 — Evals, Unit Economics, and Scaling](https://fantasybz.medium.com/agentic-engineering-part-3-evals-unit-economics-and-scaling-running-agents-like-a-product-1cb1855a2046), sections 2 and 5 (the three judge traps, the G2 gate)
14. PagerDuty — [From Clicks To Context: Building an Open-Source Evaluation Pipeline for AI Agents](https://sched.co/2QlEA) (AGNTCon + MCPCon Japan 2026, 2026-09-11) — section 5; [slides](https://hosted-files.sched.co/agntconmcpconjapan26/57/From%20Clicks%20to%20Context_%20Building%20an%20Open-Source%20Evaluation%20Pipeline%20for%20AI%20Agents%20_%20Ine%CC%82s%20Bolan%CC%83os.pdf#page=21) p. 21; the Red Line Rate of H.I.R.E.

---

### On how this piece was made

The initial concept and chapter structure are the author's; the prose was drafted in collaboration with AI (Claude), then reviewed and revised section by section by the author before publication. The views and judgments are the author's own, as is responsibility for the content.

---

*Originally published in Chinese: [中文版](https://medium.com/p/3c64a9622777). Also on [Medium @fantasybz](https://medium.com/@fantasybz) — if you're designing the gate for expanding an agent's authority, I'd like to hear from you.*
