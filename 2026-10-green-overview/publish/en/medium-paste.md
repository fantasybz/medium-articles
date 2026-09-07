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

# Green Is Not Done: Testing, Review and Reliability for Agent Output

> **TL;DR** — Six months after adopting coding agents, most teams run into the same set of symptoms: CI is green, review is queued, production breaks. The three are one problem — when the agent also wrote the tests, a green build only proves it passed the questions it set for itself; in James Bach's words, that is *checking*, not *testing*. The verification layer has three gates: the test gate measures what the tests leave behind (mutation score), the review gate decides what deserves a human's reading and who reviews whom, and the reliability gate uses constraint tests and pass^k to decide whether autonomy can expand. Three claims you may disagree with — what a human reads on a payment PR, whether an AI approve counts, whether TDD can be a gate — are written out in one sentence at the end of section 1. Every number carries its domain: "34% of green patches violate a reviewer constraint" is what SWE-Gate measured on 75 Python repos. A 90-day blueprint is at the end.

> Series: **Overview (this piece)** → 1. Testing (coming soon) → 2. Review (coming soon) → 3. Reliability (coming soon). Last season: [Don't Build Your Own Devin](https://fantasybz.medium.com/dont-build-your-own-devin-org-strategy-and-a-90-day-blueprint-for-agentic-engineering-8187e7ec80f9) → [1. Org Design](https://fantasybz.medium.com/agentic-engineering-part-1-who-does-this-platform-plus-federation-in-practice-92343384d987) → [2. The Harness Blueprint](https://fantasybz.medium.com/agentic-engineering-part-2-the-harness-blueprint-making-your-system-legible-to-agents-3facc281f633) → [3. Evals and Unit Economics](https://fantasybz.medium.com/agentic-engineering-part-3-evals-unit-economics-and-scaling-running-agents-like-a-product-1cb1855a2046)

---

## 1. The question every engineering VP is asking: after "the AI said it's fine," what should I trust?

Three scenarios; most teams have lived through at least one.

First: you ask an engineer whether this PR was tested, and the answer is "the AI said it's fine." A post in the Scrum Community in Taiwan group was about exactly this — the person answering isn't lazy; they don't know what else there is to look at besides trusting the agent.

Second: you ask an agent to fix a failing test, and it does. Then you look at the diff: `assertEqual` became `assertIn`, `== 3` became `>= 1`. The test is green; the bug is still there.

Third: production breaks, you go back to the PR, and the approve came from a reviewer agent. No human ever read it.

They share exactly one thing: **the only evidence came from the agent itself** — the tests it wrote, the things it said, the approve it gave are all its checking of questions it set for itself, and the organization took them as acceptance.

The premise first. A green CI build is a measurement of the environment, not a statement by the agent; only when the tests were written or modified by the agent itself — examiner and examinee are the same — does it turn into self-report. None of the research I have read measured what share of agent PRs contain agent-written tests, so "**most of the tests are agent-written**" is a premise in this series, not a fact: repos where the condition doesn't hold are out of scope; measure it in month 1.

The one-sentence answer, written deliberately in a shape you can disagree with:

> **Green is checking. Acceptance is testing.** So on a PR that touches payment, once constraint tests and a mutation report are in place, a human no longer reads the diff line by line — they read the intent, the constraint report and the mutation report, and only the hunks flagged red; until then, every comment a human leaves while reading the diff gets recycled into a constraint test. An AI approve does not count toward branch protection, whichever vendor it comes from. Writing TDD into AGENTS.md is fine; using the shape of TDD as a gate is not.

---

## 2. The book anchor: Bach's testing and checking

James Bach's *Taking Testing Seriously* — I quoted one line from it on my Facebook page: "Testing is the opposite of faith in the product. Testing begins with faith in the existence of trouble." A reader replied that testers now use vibe coding to build throwaway test tools — which is exactly this series' position: the agent is the tester's tool, not the tester's replacement.

Bach's definition of *checking*: "Checking is the mechanistic process of verifying propositions… testing cannot be automated, but checking can." CI is checking, automated; an agent saying "all tests pass" is its checking of its own propositions — and it wrote the propositions too.

**The three kinds of evidence**, used throughout the three deep dives:

- a) **The agent's statements**: "done," "all tests pass," "LGTM."
- b) **Tests the agent wrote or modified**: green only proves it passed the questions it set for itself.
- c) **Team-owned tests and constraint tests**: a measurement of the environment the agent cannot alter.

Only c) counts as evidence; the difference between a) and b) is only that b) has CI pressing enter for it. One objection: the agent has write access to the repo, so what makes c) something it cannot alter? Two mechanisms. **The promotion rule**: a test the agent wrote passes the test gate (no weakened assertions, real mutation kill power) **and is approved into main by a human** — only then does it move from b) to c); the classification looks at who has taken responsibility for it, not who typed it. **Cannot alter**: CODEOWNERS for `tests/constraints/` and the golden set directory lists humans only, and any weakening of a c) test blocks outright; the implementation is in the reliability piece.

The vocabulary gets fixed here too: mutation score, constraint tests and pass^k are all **better checks**; testing — looking with the belief that there must be trouble — remains human work.

I have not finished the book; the quotations come from the chapter that defines testing and checking, and from one interview.

📌【在此插入圖 diagram-01.png】

---

## 3. What the data says in 2026: the three layers a green build cannot measure

Every number carries its domain, sample size and date; the first two layers each get one in-domain anchor paper, and the third has no ready-made number in the code domain — measure it with your own golden set.

📌【在此插入表 table-01.png】

📌【在此插入圖 diagram-02.png】

Human eyes are not the safety net either: 86 developers judging LLM-written assertions recognized the correct ones 74% of the time and the incorrect ones only 49%, with no drop in confidence (Poor and Overconfident Judges, July 2026). Section 7 uses this number.

One first-hand case on top: an example from a pattern-language workshop — 5 tests all green, and the event-sourcing replay path never executed; details in the testing piece.

The conclusion is not "agents can't be trusted." It is that **what you measure today cannot measure these three layers**.

---

## 4. Testing history has already run this experiment

Last season's historical through-line was DevOps 2014–2016; this season it is the history of testing.

📌【在此插入圖 diagram-03.png】

Two points. First, Humble and Farley's deployment pipeline said long ago that a green commit stage is not a release; the agent era merely reinvents the later stages as three gates. Second, the economic case that mutation testing waited forty years for, agents supplied — once "writing tests" is free, "do the tests do anything" becomes the only question worth money.

In one line: **history taught us nothing new; it just mailed the bill for the stages we skipped.**

---

## 5. Don't teach the agent how to test; measure what it leaves behind

Uncle Bob settled his position on X this summer: TDD is a human discipline and he does not expect agents to follow it (July 30); you can't tell an agent to "stay clean," you can only measure how clean it is and then tell it to fix that (July 29).

Böckeler (reposted by Fowler on August 11) framed "TDD inside the agent loop — theater or actual value?" as an empirical question. This piece's answer is the third claim: the ritual's value is not zero — it changes the agent's exploration path — so writing "please use TDD" in AGENTS.md is fine; but **the shape of TDD cannot be the gate**; the gate measures only output.

Uncle Bob's negative test experiment of August 17: 8 runs, four test disciplines, with and without a CRAP threshold — **all passed the same 25 acceptance cases, and the programs that came out were different**. Acceptance tests all green cannot tell quality apart — SWE-Gate, personal edition.

The Taiwanese discussion has reached the same point — a post in the Scrum Community in Taiwan group argued that demanding human "values" of an AI is right, and forcing human "work habits" onto it is wrong. What's missing is that nobody has written the gate yet.

📌【在此插入表 table-02.png】

Every cell in the right column is a check, not a prompt.

---

## 6. The three gates of the verification layer

The first five sections collapse into one figure: on the left, everything on the agent's side is checking; on the right, three gates — merge and expanded autonomy exit only from the right.

📌【在此插入圖 diagram-04.png】

One question, one measurement and one owner per gate:

📌【在此插入表 table-03.png】

Constraint tests are installed and maintained by the test gate's owner; the reliability gate only consumes their constraint pass rate.

The design philosophy behind all three gates is one sentence: **designing the environment beats writing rules**. Give the agent a formal way out — "report a broken test" — and its rate of reward hacking (making the test pass instead of fixing the bug) drops to roughly a quarter (escalation channels, August 2026; the full numbers and the tool schema are in the testing piece). The agent isn't trying to deceive you; you gave it only one road.

---

## 7. Review is the control point, not the bottleneck

On September 2 Martin Fowler reposted "Maybe we shouldn't be reviewing all this code": the problem isn't that AI broke code review, it's that we've been using review to solve the wrong problem. This piece's version: **redesigning review is not about making humans read faster; it is about deciding what deserves a human's reading.** The "review becomes the new bottleneck" point in [last season's overview](https://fantasybz.medium.com/dont-build-your-own-devin-org-strategy-and-a-90-day-blueprint-for-agentic-engineering-8187e7ec80f9), section 4, needs a correction: the bottleneck is a symptom; the disease is putting humans at the wrong gate, reading the wrong thing.

Two numbers. Scale: a longitudinal study across three generations and a million PRs (From Human-Centric to Agentic Code Review, July 2026) found that agent-initiated and multi-agent review made decisions faster **under some adoption patterns**, but not better. Association: another longitudinal study tracking 182 repos (Post-merge fate of agentic code, July 2026) found that agentic code needs significantly more corrective maintenance; every 10 percentage points more in unreviewed-merge rate goes with roughly 6% more maintenance burden — the original wording is "is associated with," correlation not causation, but enough to put the unreviewed-merge rate into the monthly report; a merge with only an AI approve counts as unreviewed in this metric — that is what claim 2's "does not count" means. Another July 2026 study also found that most real leaked secrets were not caught before merge — the numbers are in the review piece.

So why isn't a human reading the payment diff line by line the safety net? Two reasons. First, section 3's 49% — it measured judging assertions, not reviewing PRs, but the direction is the same. Second, compounding: a comment a human leaves while reading a diff reviews this one PR; recycled into a constraint test, it checks every PR that follows. So in the high-blast-radius cells, what a human catches reading the diff gets recycled into constraint tests; the day the reports are in place, the human switches to reading intent and reports, and only the hunks flagged red (the sampling rule for regulated systems is in the review piece). Humans read in only two cells:

📌【在此插入圖 diagram-05.png】

📌【在此插入圖 diagram-06.png】

The four exits are the four cells of the review piece's triage matrix; the full table, the reviewer fleet, the closed-loop ban and the approval artifact are all in that piece.

---

## 8. Reliability is not capability: pass@1, pass^k and the oversight budget

Definitions:

- **pass@1**: the per-attempt success rate of each case, estimated from k reruns.
- **pass^k**: the share of cases that succeed on all k runs.
- Both are computed per case first, then aggregated over the golden set. "Succeeds at least once" is pass@k; this series does not use it.

📌【在此插入圖 diagram-07.png】

The two can differ a lot; run the operations piece's 20–50 golden cases at k = 5 to 10 and measure your own.

The third number is human effort, borrowed from **a corroborating case outside code** — the concept transfers, the numbers do not. READY is a qualification framework for enterprise agent deployment (September 2026); its case is a clinical audit workflow, 16 agent systems, 750 cases: two systems had autonomous accuracy of 72.8% and 72.5%, only 0.3 percentage points apart; for the same 76% reliability target, their human review shares were 39.2% and 29.6% — the more accurate one needed more human eyes. **A ranking by accuracy is not a ranking by human effort.** The human review share is derived backwards from the reliability target; this series calls it the oversight budget, and the algorithm is in the reliability piece:

📌【在此插入圖 diagram-08.png】

In the leadership monthly report, three numbers replace the single "pass rate":

📌【在此插入表 table-04.png】

Back to the operations piece's G2: autonomy expansion looks at pass^k and escape rate, not pass@1; this season gives G2 four measurable conditions — pass^k, constraint violation rate, mutation score floor, oversight budget — the full table is in the reliability piece.

---

## 9. Eight anti-patterns

The symptom list:

📌【在此插入表 table-05.png】

📌【在此插入圖 diagram-09.png】

Closed-loop review comes with a scale number: cross-product AI-reviews-AI — a reviewer from a different vendor reviewing agent PRs — is only about 1.6% of the total, but grew more than 100x from Q1 to Q3 2025 (AI-to-AI Code Reviews, 248,641 PRs, August 2026). How large the same-model, same-session loop is, the paper did not measure; you will have to measure it yourself.

In Taiwanese communities I see 5 and 6 most often — an observation, not a statistic: coverage is the threshold easiest to bolt onto existing CI, and seat-based subscriptions make "review yourself on the same subscription" the cheapest option.

---

## 10. If I were the engineering VP or QA lead, how I would decide

I would **not** approve:

> "Turn the QA team into a prompt team."
> "Use AI review to clear the review backlog; an AI approve is enough to merge."
> "On the strength of an 85% eval pass rate, open write tools to every team in Q4."

I **would** approve four things:

1. Pull 50 review comments from the agent PRs sent back in the last 90 days, classify them, pick out the executable ones, and write the first 10 constraint tests. For a repo with no comment history, derive the first 5 from the last 5 incident postmortems — this is the main route, not a fallback: every "this must never happen again" was a constraint to begin with.
2. Install a mutation gate on one pilot repo, counting only the lines the agent changed; the conditions are 200+ engineers or a QA lead who reads the report, and the affected test subset finishing within 10 minutes — at 50 people, don't turn it on, see the table below. The threshold is **my suggested value (not an industry standard)**: mutation score ≥ 70%; below that, the PR goes back to the agent for more tests, not to a human to read; report only for a month, then block.
3. The reviewer agent must be an instance from **a different vendor, or at least a different session**; an AI approve never counts toward required approvals — a merge with only an AI approve counts as unreviewed in section 7's unreviewed-merge rate. GitHub offers two candidate mechanisms — CODEOWNERS listing humans only plus Require review from Code Owners, or a required status check that counts human approves — I have not tested either on a production repo; validate it first with a GitHub App's approve on your own repo; a design draft is in the review piece.
4. The approval artifact binds a human identity to the hash of what was reviewed; on high-blast-radius PRs, whoever assigned the task cannot approve. Vendor terms contradict one another on "who may approve an agent's PR" (Where Accountability Lives, August 2026); the details go to December's accountability piece.

**How to think about the verification budget.** A study of 1,116 web apps, 6 models and 8 tool configurations (The reach of a verification tool decides its value, August 2026) gave me one principle: a verification tool's value is set by its reach — a boot probe that only checks whether the app starts, at about 35% of a shell's token cost, removed almost all startup failures; a full shell costs 2.35x. So buy the check with the widest reach first (constraint tests, assertion-change diff), then the ones that have to execute tests (red-then-green, mutation), and only last the expensive ones (k reruns, step-rubric judges).

**The ratio is my provisional heuristic, to be calibrated by the pilot** — that paper supports the principle, not the ratio: for every $1 of agent tokens plus generation-side CI (the denominator: the machine cost of what the agent produces), budget $0.30 to $0.50 of verification-side compute (the numerator: the machine cost of verifying it). **Human review time is not in this ratio**; it goes through the reliability piece's oversight budget, and the two are reported to the CFO separately.

**Installing at 50 / 200 / 1,000 engineers.** G2 is about expanding autonomy, not about rolling a gate from one repo to forty:

📌【在此插入表 table-06.png】

**Brownfield: which gate first.** The reality for most readers in Taiwan is a 15-year-old legacy monolith: a 40-minute test suite, 30% coverage, no review-comment history to mine. Below is the installation order for the verification layer; each step depends only on the precondition in its own row. It does not replace the legibility order from last season's overview, section 7 (characterization tests → logs / traces → architecture rules); a repo with no tests at all adds characterization tests first, as step 0:

📌【在此插入表 table-07.png】

These four checks are just as useful on human-written PRs — loosened assertions, frozen bugs and violated team constraints were not invented by agents. **Even if the agent bet fails, none of these gates is wasted.**

---

## 11. A 90-day action blueprint for the verification layer

Month 1 has six baselines to measure: the escape rate and review minutes per PR that last season already measured, plus four new numbers — the share of PRs that weaken an existing assertion, the share of snapshot or golden-file updates with no stated reason, the share of agent-changed lines that existing tests cover, and the share of new or modified test files written by the agent (the last one measures this series' premise).

📌【在此插入表 table-08.png】

📌【在此插入圖 diagram-10.png】

Two reminders:

1. **Mutation goes in last, report first, block later**: month 1 reports only, month 3 blocks — a gate that blocks from day one gets ripped out. Likewise, red-then-green is on only for PRs that change existing behavior; turn it on for feature PRs too and every one goes red on "class does not exist," and it gets ripped out the same way — the new tests on feature PRs are mutation's job.
2. **Start constraint tests from the rules that are executable and least contested**: no new dependencies, no new public API, log format; do not start with architecture rules.

---

## 12. Closing

Back to Bach: checking can be automated, testing cannot. Agents have pushed the cost of checking close to zero, and in doing so made testing the scarcest thing in the organization. One dated prediction: by 2027, a reliability gate will be standard in G2, and "reporting only pass@1" will draw the same frown that "only looking at coverage" does today.

> **When the agent wrote the tests, green only means it passed the questions it set for itself. Don't teach it how to test; measure what it left behind — then put humans where they should be reading.**

November's theme, "the same spec, run ten times," pushes pass^k one step further, into the harness's variance.

---

### The series

Three deep dives, one gate each:

1. **Overview (this piece)**
2. Part 1 — Reviewing the Tests an Agent Wrote: Loosened Assertions, Frozen Bugs and Mutation Score (coming soon)
3. Part 2 — Review Is the Control Point, Not the Bottleneck: Triage, Reviewer Fleets and the Closed-Loop Ban (coming soon)
4. Part 3 — The 34% SWE-Gate Found Behind a Green Build: Constraint Tests, pass^k and the Gate for Expanding Autonomy (coming soon)

Last season's Agentic Engineering series: [Overview](https://fantasybz.medium.com/dont-build-your-own-devin-org-strategy-and-a-90-day-blueprint-for-agentic-engineering-8187e7ec80f9), [1. Org Design](https://fantasybz.medium.com/agentic-engineering-part-1-who-does-this-platform-plus-federation-in-practice-92343384d987), [2. The Harness Blueprint](https://fantasybz.medium.com/agentic-engineering-part-2-the-harness-blueprint-making-your-system-legible-to-agents-3facc281f633), [3. Evals and Unit Economics](https://fantasybz.medium.com/agentic-engineering-part-3-evals-unit-economics-and-scaling-running-agents-like-a-product-1cb1855a2046).

---

### References

1. James Bach — *Taking Testing Seriously* (book); Bach / Bolton — Testing and Checking (satisfice.com)
2. SWE-Gate — [Passing Functional Tests Is Not Enough for Software Engineering Agents](https://arxiv.org/abs/2609.04167) (2026-09-03)
3. arXiv — [Test Coverage Analysis of Agentic Pull Requests](https://arxiv.org/abs/2607.18057) (2026-07-20)
4. arXiv — [Programmers Are Poor and Overconfident Judges of LLM-Generated Assertions](https://arxiv.org/abs/2607.08885) (2026-07-09)
5. arXiv — [Can escalation channels redirect reward hacking toward defect disclosure?](https://arxiv.org/abs/2608.29460) (2026-08-29)
6. arXiv — [READY or Not: Reliable Enterprise Agent Deployment](https://arxiv.org/abs/2609.02095) (2026-09-02)
7. arXiv — [From Human-Centric to Agentic Code Review: three generations of GenAI and review quality](https://arxiv.org/abs/2607.13196) (2026-07-14)
8. arXiv — [Do These Violent Delights Have Violent Ends? Post-merge fate of agentic code](https://arxiv.org/abs/2607.09902) (2026-07-10)
9. arXiv — [Trust but Verify? Security debt of autonomous coding agents](https://arxiv.org/abs/2607.12428) (2026-07-14)
10. arXiv — [AI-to-AI Code Reviews of GitHub Pull Requests](https://arxiv.org/abs/2608.21311) (2026-08-21)
11. arXiv — [Where Accountability Lives: mapping human responsibility to workflow artifacts](https://arxiv.org/abs/2608.15678) (2026-08-16)
12. arXiv — [The reach of a verification tool decides its value](https://arxiv.org/abs/2608.28795) (2026-08-28)
13. Robert C. Martin (@unclebobmartin) — [2026-07-26 kinds of tests](https://x.com/unclebobmartin/status/2081332683582427641), [2026-07-29 measure cleanliness](https://x.com/unclebobmartin/status/2082497764223492161), [2026-07-30 TDD is a human discipline](https://x.com/unclebobmartin/status/2082850576832905657), [2026-08-05 deterministic tools](https://x.com/unclebobmartin/status/2085104553746190372), [2026-08-17 negative test experiment](https://x.com/unclebobmartin/status/2089449442089025936)
14. Martin Fowler (@martinfowler) — [2026-08-11 TDD inside the agent loop (Birgitta Böckeler)](https://x.com/martinfowler/status/2087173563144912985), [2026-09-02 Maybe we shouldn't be reviewing all this code](https://x.com/martinfowler/status/2095147242986373485)
15. Community discussion: public posts in the Scrum Community in Taiwan group ("the AI said it's fine"; "demanding human values of an AI is right")

---

### On how this piece was made

The initial concept and chapter structure are the author's; the prose was drafted in collaboration with AI (Claude), then reviewed and revised section by section by the author before publication. The views and judgments are the author's own, as is responsibility for the content.

---

*Originally published in Chinese: [中文版](https://medium.com/p/582f24223eea). Also on [Medium @fantasybz](https://medium.com/@fantasybz) — if you're designing the verification layer for agent output in your organization, I'd like to hear from you.*
