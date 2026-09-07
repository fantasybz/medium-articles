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

# Green Is Not Done, Part 1 — Reviewing the Tests an Agent Wrote: Loosened Assertions, Frozen Bugs and Mutation Score

> **TL;DR** — The overview's point: when the agent wrote the tests, a green build is checking, not acceptance. This piece is about the tooling for the test gate. Tests are the agent's acceptance criteria for itself — it sets the exam and sits it — so tests need review more than code does. Agent-written tests go wrong in four places: assertions get loosened, current bugs get recorded as goldens, tests never go red or take a path the spec didn't ask for, and coverage gets mistaken for quality. Human eyes can't catch these — in one experiment with 86 developers, judging the LLM-written assertions that were wrong was only 49% accurate, and confidence didn't drop — so lean on three cheap checks: **assertion-change diff, red-then-green, and diff-scoped mutation score**. In the agent era, mutation testing has an economic case as a gate for the first time, but it has to be a gate, not a ritual. At the end: a ten-question checklist for a tester reviewing an agent's tests, and an example I ran myself at a pattern-language workshop — all tests green, replay never executed — which happens to prove that none of the three gates can be skipped, and tells you which one was missing.

> Series: [Overview](https://medium.com/p/c4fc9f3d8581) → **1. Testing (this piece)** → 2. Review (coming soon) → 3. Reliability (coming soon)

---

## 1. After "the AI said it's fine": the tester's new job

The overview used James Bach's language to split checking from testing: a green CI build is checking, and an agent saying "all tests pass" is checking too; acceptance is testing, a human judgment. The overview also used SWE-Gate's 34% to show that a green build doesn't measure reviewer constraints. This piece covers only the first of the three gates — the test gate — which is the other layer a green build can't measure: whether the tests themselves are any good.

First, why tests need review more than code does. Scrum Community in Taiwan reshared a line from Lada Kesseler, to the effect that she trusts AI-written tests even less than AI-written code. The reason is direct: tests are the agent's acceptance criteria for itself, and the one setting the exam is the one sitting it. For the three-way split, and the promotion rule for when an agent-written test becomes the team's test, see section 2 of the overview.

Bach says a tester's core skill is rapid learning. In the agent era that has a concrete form: reading the tests an agent left behind tells you faster than reading its code what it understood and what it didn't. Tests are the agent's translation of the requirements; where the translation is wrong, the tests give it away first.

The discussion that actually caught fire in Taiwan was the DevOps Taiwan thread on Uncle Bob's position of not reading the agent's code and looking only at the tests and quality metrics — someone half-jokingly asked him to list every test that ought to be run. He had, in fact, already listed them ([2026-07-26](https://x.com/unclebobmartin/status/2081332683582427641)): agents write fast, so spend the time saved on unit, acceptance, property, torture, mutation and QA tests. This piece is my answer to that thread, but the answer isn't a list of test types; it's three checks and their thresholds.

---

## 2. Where agent-written tests go wrong: four patterns

📌【在此插入表 table-01.png】

A fifth doesn't get its own row but needs mentioning: **red for the wrong reason**. LeSS in Action, when teaching A-TDD, has a discipline: pay attention to the error message, and the error message has to match what you expected. The red in red-then-green needs checking too: it should be the expected assertion failing, not an import error.

The workshop example in section 7 is a variant of the third row: not "never goes red" but "tests the wrong thing" — the tests take the in-memory path, and the spec wants the replay path. None of the four checks can measure "what should have been written wasn't"; that section explains why.

📌【在此插入圖 diagram-01.png】

Each of the four failure patterns has a cheap check; nobody has to read the tests line by line.

---

## 3. Human eyes aren't enough: 49%

One experiment had 86 developers judge whether LLM-generated assertions were correct (Poor and Overconfident Judges, July 2026). They recognized correct assertions 74% of the time; incorrect ones only 49% — about a coin flip — and their confidence was equally high in both cases. Attaching explanations didn't help; low-quality explanations actually hurt. Note what this experiment measures: "judging whether an LLM-generated assertion is correct", not "judging an existing assertion the agent loosened"; I keep the two apart, but they point the same way.

An eye-tracking study adds the second cut: code labeled as LLM-generated gets looked at longer by reviewers, but not more thoroughly.

The inference is direct: "have a senior look carefully at the tests" is not a strategy. What humans should look at is **the tools' report** — which assertions were weakened, which mutants survived, which new tests didn't go red against the old code — not the tests themselves.

📌【在此插入表 table-02.png】

---

## 4. Mutation testing: a gate, not a ritual

Mutation testing works by breaking the code a little — swap an operator, change a constant, flip a condition — and seeing whether the tests go red. If they do, the mutant is killed; if they don't, the mutant survives, which means the tests weren't guarding that spot. The mutation score is the share of mutants killed.

Uncle Bob's gate combination is coverage, CRAP score and mutation tests — TDD, he says, is a human discipline; he doesn't expect agents to follow it and only measures the result ([2026-07-30](https://x.com/unclebobmartin/status/2082850576832905657)). DevOps Taiwan's summary of his position: once the agent's code passes unit, Gherkin, mutation and the quality metrics, he stops reading the code. This piece doesn't go that far — the Review piece will argue that humans still have to read intent and constraints — but it agrees that mutation is the core of the test gate.

Why didn't it pay off before, and why does it now? Mutation is slow, because it runs the tests N times over. The agent era changed two things: the volume of tests has outgrown what people can read, so "are the tests any good" becomes the only question worth money; and **diff-scoped mutation**, which counts only the lines the agent changed, brings the cost down to something acceptable. Section 10 of the overview said the value of a verification tool is set by its reach; diff-scoped mutation's reach is exactly the place the agent just changed.

What it can't measure has to be said up front too: mutation only measures whether code that has been written is guarded by tests; it can't measure "what should have been written wasn't". Section 7 will use this sentence — it's exactly the proof that mutation is a better check, not testing.

The brownfield reality: on a 40-minute test suite, diff-scoped mutation still has to run the affected tests N times. So it's the **last** of the four checks to install, and only on repos where the affected subset finishes within 10 minutes; the install order is in section 10 of the overview and isn't repeated here.

**The ritual version versus the gate version.** Thoughtworks' Birgitta Böckeler asked "TDD inside the agent loop—theater or actual value?" (reshared by Fowler, [2026-08-11](https://x.com/martinfowler/status/2087173563144912985)); Uncle Bob's negative test experiment of August 17 is the other face of the same question — programs written under four test disciplines all passed the acceptance tests, and the programs were different ([2026-08-17](https://x.com/unclebobmartin/status/2089449442089025936); the overview quoted the numbers). Telling an agent to "run mutation, then add tests until you hit 100%" is the ritual version: you get tests written specifically to kill mutants — another kind of tautology. The gate version is CI reporting the surviving mutants to a human, and the human deciding which need a test and which are equivalent mutants.

The threshold is my recommended value, not an industry standard: mutation score on the agent's changed lines ≥ 70% before the PR enters review, and report for a month before blocking. The number is Uncle Bob's practice plus my own rough estimate; I'll add my own data in November. On tooling, the JVM has PIT, JS and TS have Stryker, Python has mutmut; how far each can be confined to the diff varies, so check how your stack does it before you start.

📌【在此插入表 table-03.png】

---

## 5. Three checks on the diff: a reference implementation

**Check 1: red-then-green.** Scope first. It runs only on PRs that change existing behavior — bug fixes, behavior changes. A feature PR's new tests always go red on the base branch, and they do so because a class doesn't exist, which is the wrong reason; producing noise on every feature PR is exactly what triggers the overview's warning that a gate which blocks outright gets torn down. So a feature PR's new tests go to Check 3.

**The classification must not come from the PR's author.** If the label is set by the agent that opened the PR, an agent driven by the "make the tests pass" reward quickly learns: label every PR a feature and never get checked. The scope of a gate can't be decided by the party being checked — this is the same thing as the series' "measure output, not process". In practice: bring it in from the issue or ticket's type field (set by a human) or the harness's task type, which the agent can't change; with no source, judge from the diff — if the PR modified any existing non-test file, treat it as a behavior change and run the check; only PRs that add files skip it.

The CI job checks out the tests the PR added onto the base branch and runs them; the output falls into three classes: a) didn't go red — flagged `test-never-fails`, the only class that gets flagged; b) red for the right reason — the expected assertion failed — pass; c) red for the wrong reason — import error, missing fixture — not flagged, only listed in the report, because it's mostly a signal of a feature mixed into a fix, not of the agent cheating.

📌【在此插入圖 diagram-02.png】

red-then-green runs only on PRs that change existing behavior; of the three exits, only "didn't go red" is a bad signal.

**Check 2: assertion-change diff.** When an existing assertion is modified, grade it into four classes:

- a) **A step down the strength ladder**: equality → containment → truthy. Block.
- b) **Count or precision relaxed**: call count, tolerance, timeout. Block.
- c) **Removal**: assertion deleted, `assertRaises` deleted. Always block.
- d) **Disabling**: `skip`, `xfail`, `.only`, test file deleted. Always block.

Any other change to an existing assertion gets `needs-human-test-review`. For tests already promoted to team ownership (the third category in section 2 of the overview), any weakening blocks outright. Don't use "the same PR changes both code and tests" as a signal — a normal behavior-change PR changes both anyway, so that ratio will sit near 100% and measure nothing.

**Check 3: diff-scoped mutation.** Generate mutants only for the files the agent changed, and report only the survivors on the changed lines — most tools work per file, and whether they can be confined to lines varies (section 4); if yours can't, filter the survivors yourself. A feature PR's new tests rely on this one.

Three jobs fan out from the same PR and come back as one report:

📌【在此插入圖 diagram-03.png】

Three jobs run in parallel and produce a report for humans to read; for the first month, nothing blocks.

This is the series' only "instruction vs. measurement" Before / After — Uncle Bob's version is that you can't tell an agent to write clean code, you can only measure whether it did and then tell it to fix it ([2026-07-29](https://x.com/unclebobmartin/status/2082497764223492161)). Before is what most teams have in AGENTS.md today:

```text
# Before: instructions (the agent reads them, and nothing changes)
Always use TDD. Do not modify existing tests.
```

After is three jobs in CI plus a `classify` job that decides the scope (excerpt; every diff is against the base branch, and the five scripts under `tools/` — one for `classify`, one per check, one that posts the report — are the part you write yourself; their behavior is the definition of the three checks above):

```yaml
# .github/workflows/test-gate.yml (excerpt) — first month: comment only, no blocking
on: pull_request
jobs:
  classify:              # classification not by the PR author: read the linked issue's type field; failing that, check whether existing non-test files changed
    outputs:
      kind: ${{ steps.kind.outputs.kind }}
    steps:
      - uses: actions/checkout@v4
        with: { fetch-depth: 0 }
      - id: kind
        run: python tools/classify_pr.py --base origin/${{ github.base_ref }} >> "$GITHUB_OUTPUT"
  assertion-diff:        # all PRs: pure diff analysis, zero run cost
    steps:
      - uses: actions/checkout@v4
        with: { fetch-depth: 0 }
      - run: python tools/assertion_strength.py --base origin/${{ github.base_ref }} --report weakened.json
  red-then-green:        # fix / behavior-change only
    needs: classify
    if: ${{ needs.classify.outputs.kind != 'feature' }}
    steps:
      - uses: actions/checkout@v4
        with: { fetch-depth: 0 }
      - run: git checkout origin/${{ github.base_ref }} -- src/   # pre-fix code; the tests stay at the PR's version
      - run: pytest $(git diff --name-only --diff-filter=A origin/${{ github.base_ref }}...HEAD -- tests/) || true
      - run: python tools/red_then_green.py --classify-red --report never_fails.json   # no red / right-reason red / wrong-reason red
  mutation-diff:         # only on repos whose affected subset runs in < 10 minutes
    steps:
      - uses: actions/checkout@v4
        with: { fetch-depth: 0 }
      # mutation tools generate mutants per file; confining to "lines the agent changed" means filtering the survivors yourself
      - run: python tools/mutation_diff.py --base origin/${{ github.base_ref }} --report survivors.json
  report:
    needs: [assertion-diff, red-then-green, mutation-diff]
    if: ${{ always() }}  # the report must still go out when red-then-green is skipped
    steps:
      - run: python tools/post_pr_comment.py weakened.json never_fails.json survivors.json
```

**The agent-side counterpart.** One study (escalation channels, August 2026) gave agents a structured "report a broken test" tool; reward hacking fell from 23.6% to 5.3% (odds ratio 9.2), and disappeared entirely in 6 of 8 frontier models; 98.7% of escalations involved no cheating, and defect-detection coverage rose by 10.1 percentage points. Landing it takes two steps:

```json
{
  "name": "report_broken_test",
  "description": "Call this when you believe an existing test is itself wrong. Do not change the assertion.",
  "parameters": {
    "test_id": "tests/test_pool.py::test_timeout",
    "reason": "expected value contradicts the spec in docs/pool.md §3",
    "evidence": "spec says 30s; test asserts 3s"
  }
}
```

AGENTS.md gets one added line: "If you believe a test is wrong, call `report_broken_test`; do not change the assertion." This is "changing the environment beats writing rules" landing in the testing piece — the agent isn't trying to deceive you; you only gave it one road.

One last small thing: add a "golden source" field to the PR template. Where did the new snapshot or golden file come from — the spec, actual production output, or "this is what it produces right now" — required. The third answer isn't forbidden, but it has to be written down where the reviewer can see it.

---

## 6. Coverage is an assertion that can be edited away

Test Coverage of Agentic PRs measured 4,882 agent PRs: the repo's existing tests touched only 61.5% of the executable lines the agent changed in Java, and only 27.0% in Python. The repo-wide coverage number won't tell you this — whatever your repo's overall coverage is, on the Python side nearly three quarters of the lines the agent just changed have no existing test passing through them.

All three ways to game it are cheap: add a line to the exclude pattern; call without asserting; move the hard-to-test logic into an excluded file.

Three prescriptions: measure coverage on the agent's changed lines only; read it paired with the mutation score; route exclude-pattern changes through human review.

In one line: **coverage tells you where the tests ran; mutation tells you where the tests hold.**

---

## 7. A first-hand example: all tests green, replay never executed

This August, at a pattern-language workshop, I ran two approaches on the same requirement — a Product aggregate plus a CreateProduct use case — each in its own worktree. What Approach A delivered looked beautiful: 25 files, zero compiler warnings, 5 tests all green, clean layering, complete Javadoc.

The problem was the path the tests took. The spec asked for event sourcing: the aggregate's state has to be replayable from its events. Approach A's Product wasn't event sourcing at all — it didn't extend `EventSourcedAggregate` — and the tests read `getDomainEvents()` straight off the in-memory aggregate, never going through the replay path. It also lacked `@DirtiesContext`, so CI would go red intermittently. My note at the time: A's 10/16 (10 of the 16 items on the compliance checklist) wasn't "nearly there"; it was "hasn't blown up yet at a toy scale with a single InMemory use case".

Scope first: this is an instance of "green but not accepted" and "testing the wrong thing", not variance data — N equals 1, and what was measured is compliance. The variance question waits for November.

Mapping this example onto the checks has to be done right; a staff engineer would catch it at a glance:

- **red-then-green doesn't apply**: this is a feature PR, and the new tests would go red against the old code because the class doesn't exist.
- **mutation can't catch it either**: Product isn't event sourcing at all, so there's no replay path in the code, so there's no "replay-path mutant" that could survive — and the in-memory aggregate's mutation score is quite possibly still beautiful. This is exactly the sentence from section 4 — it can't measure "what should have been written wasn't"; it's a better check, not testing.
- **What does catch it is two things**: a constraint test — the aggregate must extend `EventSourcedAggregate`, or at least one test must construct the aggregate via rehydrate, the "architecture rule" kind that section 2 of the Reliability piece describes — and a human reading the intent: "is this event sourcing?"

So none of the three gates can be skipped, and this example tells you which one was missing: the test gate passed, no constraint test was installed, and no human read the intent.

📌【在此插入圖 diagram-04.png】

5 tests all green; the replay path the spec asked for was never executed.

Thanks to Teddy, whose workshop produced this example.

---

## 8. The tester's role: from box-ticker to test-suite reviewer

Ten questions for reviewing a test suite an agent wrote:

📌【在此插入表 table-04.png】

Tools answer the first eight; only a human can answer the last two. That is the tester's position at the test gate: not a box-ticker, but a test-suite reviewer. *Testing Extreme Programming* says everyone is a tester; the agent-era version of that line is: everyone who merges an agent PR is reviewing a test suite.

---

## 9. Closing

There's one more piece of testing that Bach says can't be automated: exploratory testing of what the agent produced — not reading its tests, but using the thing it built. That's a topic for another article; here I only point at it.

> **An agent's tests are its acceptance criteria for itself; reviewing its tests is reviewing what it believes "correct" means.**

Next is the Review piece: once the test gate passes, who reads this PR, what they read, who reviews whom, and when AI reviewing AI should be banned.

---

### The series

1. [Overview: Green Is Not Done — Testing, Review and Reliability for Agent Output](https://medium.com/p/c4fc9f3d8581)
2. **1. Testing (this piece)**
3. 2. Review: Review Is the Control Point, Not the Bottleneck — Triage, Reviewer Fleets and the Closed-Loop Ban (coming soon)
4. 3. Reliability: The 34% SWE-Gate Found Behind a Green Build — Constraint Tests, pass^k and the Gate for Expanding Autonomy (coming soon)

---

### References

1. Programmers Are Poor and Overconfident Judges of LLM-Generated Assertions — [arXiv 2607.08885](https://arxiv.org/abs/2607.08885) (2026-07-09). Section 3.
2. Same Scrutiny, More Time: Eye Tracking on Reviewing LLM-Labelled Code — [arXiv 2606.26505](https://arxiv.org/abs/2606.26505) (2026-06-25). Section 3.
3. Test Coverage Analysis of Agentic Pull Requests — [arXiv 2607.18057](https://arxiv.org/abs/2607.18057) (2026-07-20). Sections 2 and 6.
4. Can escalation channels redirect reward hacking toward defect disclosure? — [arXiv 2608.29460](https://arxiv.org/abs/2608.29460) (2026-08-29). Section 5.
5. SWE-Gate — [Passing Functional Tests Is Not Enough for Software Engineering Agents](https://arxiv.org/abs/2609.04167) (arXiv 2609.04167, 2026-09-03). Section 3 of the overview; one sentence in section 1 here.
6. Robert C. Martin (@unclebobmartin) — [2026-07-26, the kinds of tests](https://x.com/unclebobmartin/status/2081332683582427641) (section 1); [2026-07-29, measure cleanliness rather than asking for it](https://x.com/unclebobmartin/status/2082497764223492161) (section 5); [2026-07-30, TDD is a human discipline](https://x.com/unclebobmartin/status/2082850576832905657) (section 4); [2026-08-17, the negative test experiment](https://x.com/unclebobmartin/status/2089449442089025936) (section 4)
7. Martin Fowler (@martinfowler) — [2026-08-11, TDD inside the agent loop](https://x.com/martinfowler/status/2087173563144912985) (section 4)
8. Community discussions: Scrum Community in Taiwan (the Lada Kesseler reshare; "the AI said it's fine"); DevOps Taiwan (the Uncle Bob mutation-gate thread)
9. Author's notes: A-TDD course notes from LeSS in Action; the A/B implementation log from the pattern-language-driven development workshop (2026-08) (section 7); reading notes on *Testing Extreme Programming* (section 8)
10. Last season: [Part 2, The Harness Blueprint](https://fantasybz.medium.com/agentic-engineering-part-2-the-harness-blueprint-making-your-system-legible-to-agents-3facc281f633), section 5 (flaky quarantine)

---

### On how this piece was made

The initial concept and chapter structure are the author's; the prose was drafted in collaboration with AI (Claude), then reviewed and revised section by section by the author before publication. The views and judgments are the author's own, as is responsibility for the content.

---

*Originally published in Chinese: [中文版](https://medium.com/p/b01055139451). Also on [Medium @fantasybz](https://medium.com/@fantasybz) — if you're installing your team's first test gate, I'd like to hear from you.*
