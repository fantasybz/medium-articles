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

> **TL;DR** — When a team adopts coding agents and keeps seeing green CI, a growing review queue and production failures, it is worth asking whether its acceptance criteria have kept pace. If an agent writes both the implementation and its tests, without independent scrutiny of those tests, green only shows that it passed its own exam. In James Bach's terms, that is *checking*; it is not enough to complete *testing*. Three gates divide the work: the test gate assesses test effectiveness through mutation score; the review gate assigns who examines what; and the reliability gate uses constraint tests and pass^k to inform expanded authority. Section 1 sets out three positions: how humans review payment PRs, whether AI approvals count, and whether TDD can serve as a gate. Every number keeps its domain attached: SWE-Gate measured the finding that "34% of green patches violate reviewer constraints" across 75 Python repos. A 90-day blueprint closes the piece.

> Series: **Overview (this piece)** → 1. Testing (coming soon) → 2. Review (coming soon) → 3. Reliability (coming soon). Last season: [Don't Build Your Own Devin](https://fantasybz.medium.com/dont-build-your-own-devin-org-strategy-and-a-90-day-blueprint-for-agentic-engineering-8187e7ec80f9) → [1. Org Design](https://fantasybz.medium.com/agentic-engineering-part-1-who-does-this-platform-plus-federation-in-practice-92343384d987) → [2. The Harness Blueprint](https://fantasybz.medium.com/agentic-engineering-part-2-the-harness-blueprint-making-your-system-legible-to-agents-3facc281f633) → [3. Evals and Unit Economics](https://fantasybz.medium.com/agentic-engineering-part-3-evals-unit-economics-and-scaling-running-agents-like-a-product-1cb1855a2046)

---

## 1. The question every engineering VP is asking: after "the AI said it's fine," what should I trust?

Before getting to acceptance gates, I want to start with a few moments a team may encounter after adopting coding agents. The tool has delivered something, but the person taking it over still has to answer: what gives me reason to trust it?

The three situations below include a community account and examples used to explain the risks. They may not all have happened in your repo, but they point to the same question.

The first comes up in a routine progress check. You ask a developer whether the PR has been tested; the answer is, "The AI says it is fine." A post in Scrum Community, a Taiwanese Scrum Facebook group, describes this situation. Before dismissing the answer as laziness, ask what evidence the team has made available for the developer to check beyond the agent's own account.

The second one shows up while fixing a bug. You ask an agent to fix a failing test. It reports success, and CI goes green too. Then you look at the diff: `assertEqual` became `assertIn`, `== 3` became `>= 1`. The test is green; the bug is still there. What it fixed was not the code. It was the assertion that had been complaining.

The third one shows up afterwards. Production breaks, you go back to the PR, and the approve came from a reviewer agent. No human ever read it. Suppose this had to be written up as a postmortem: the hardest field to fill in would be "who looked at this change," and no name would go in it.

The common thread is that **the team has not independently established whether its grounds for acceptance are reliable**. An agent's account, tests it has modified, and a reviewer agent's approval are different signals, yet each is being treated as sufficient reason to proceed.

This series focuses on a particular situation: agents write much of both the implementation and the tests, and the team needs to re-examine how one verifies the other.

A green CI result comes from checks executed by the environment, not from the agent's account. The problem arises when the agent changes both the implementation and the tests used to accept it, without independent scrutiny of those tests. The same party sets the exam and takes it. Green remains a real result; it is simply insufficient to establish that the original requirements have been met.

There is one question I still cannot answer. None of the studies I have read measures what share of agent-authored PRs includes agent-written tests. So **most tests are agent-written** is a premise for this discussion, not an established fact about all teams. In month 1, count what share of added or modified test files was written by agents. That share helps set adoption priorities; test independence and effectiveness still matter in other repos.

I want to put forward three claims to discuss in response to those scenarios. Disagreeing is fine; they still give you something to take back and compare with your own branch protection (GitHub's setting for what a PR must satisfy before it may merge), review policy and agent workflow.

Before stating the claims, a few terms need explaining. Payment means the code that handles payments. It is the example here because an error can affect payment correctness; auth and schema changes also often need close attention. Constraint tests turn checkable requirements raised by reviewers into checks executed by CI. A mutation report is the result of deliberately breaking the code and seeing whether the tests go red. Intent is the part of the PR description that says what is being changed and why. AGENTS.md is the project file that lives in the repo and is written for agents to read. Constraint tests and the mutation report each get a section of their own later:

> **Green is checking. Acceptance is testing.** For a PR that touches payment, first establish that constraint tests and the mutation report cover key requirements. A human can then start with intent and reports, inspecting flagged hunks and anything still in doubt. Until that evidence exists, line-by-line review remains the default. Turn review requirements that can be checked repeatedly into constraint tests. An AI approve does not count toward branch protection, whichever vendor it comes from. Writing TDD into AGENTS.md is fine; using the shape of TDD as a gate is not.

These three positions are my proposals for workflow design. The distinction between testing and checking comes from James Bach. The next section establishes that vocabulary, then the data and testing history explain why green is insufficient for acceptance. From there, I develop the three gates and turn them into a decision list and an action plan.

---

## 2. The book anchor: Bach's testing and checking

To explain why these three gates are needed, I want to return to a book about testing. James Bach is the author of context-driven testing (deciding how to test from the situation rather than following a fixed procedure) and of the Rapid Software Testing methodology, and this section's book anchor is his *Taking Testing Seriously*. The work of his career has been to keep "testing" separate from "ticking boxes off a list."

There is a line in the book that I quoted on my own Facebook page: "Testing is the opposite of faith in the product. Testing begins with faith in the existence of trouble." The second half is what matters to me. Testing does not start from believing the product is fine. It starts from believing that trouble is waiting somewhere.

A note on where I am in the reading: I have not finished the book; the quotations come from the chapter that defines testing and checking, and from one interview.

So what is checking? Bach's definition reads: "Checking is the mechanistic process of verifying propositions… testing cannot be automated, but checking can."

In plain language, checking takes a set of propositions someone has already written down and marks them against the answer key: matching is green, not matching is red, and a machine does that faster and more consistently than a person. Testing is a person going in with judgment to ask whether the thing actually works, and Bach says that cannot be automated.

There is nothing wrong with CI automating checking. What we need to distinguish is what CI actually executed, who validated the propositions in the tests, and how the agent described the result afterward. The words "all tests passed" are themselves only a claim.

Once claims and execution results are separated, the next question is which results can support acceptance. This series distinguishes three sources, using the same labels in the three deep dives:

- a) **The agent's statements**: "done," "all tests pass," "LGTM."
- b) **Tests the agent wrote or modified**: green only proves it passed the questions it set for itself.
- c) **Team-owned tests and constraint tests**: a measurement of the environment the agent cannot alter.

Only （c） qualifies as independent acceptance evidence for the gates proposed here. Category (a) can point to what needs checking, and (b) supplies actual execution results. But until the team has validated the tests themselves, neither is sufficient on its own to justify acceptance.

A natural objection comes up here. The agent has write access to the repo, so what makes c) something it cannot alter? Answering that takes two mechanisms — one that decides how a test gets promoted, and one that decides who can touch it afterwards.

**The promotion rule**: a test the agent wrote passes the test gate (no weakened assertions, real mutation kill power) **and is approved into main by a human** — only then does it move from b) to c). The classification looks at who has taken responsibility for it, not who typed it.

**Cannot change them unilaterally**: list only humans as CODEOWNERS for `tests/constraints/` and the golden set, and enforce code-owner approval in the merge rules. Block any weakening of category （c） tests. The golden set is a fixed collection of representative tasks used to evaluate the same agent setup repeatedly. "Cannot change" means the agent cannot approve and merge the changes on its own; it can still propose changes on a branch. Checks also need a protected version of the tests, so a PR cannot rewrite its exam and then use that exam to certify itself. The reliability piece explains the implementation and its limits.

Mutation in the promotion rule means deliberately changing the code and checking whether a test fails. If the mutation changes behavior but the tests stay green, investigate which requirement lacks an effective assertion. Mutation score measures the share of valid mutations caught by the tests. It assesses sensitivity to those changes, rather than merely which lines were executed.

That distinction also makes the vocabulary clearer. Mutation score, constraint tests and pass^k (the share that passes all k runs) are all **better checks**, not substitutes for testing. Testing is looking at the system with the belief that there must be trouble in it, and that remains human work.

People on the ground are already doing this. Under the Facebook post where I quoted that line, a reader replied that testers now use vibe coding (having the agent write it, looking only at the result and never at the code) to build throwaway test tools. Throwaway means written and then discarded, built only to answer the one question in front of you. That is exactly this series' position: the agent is the tester's tool, not the tester's replacement.

Laying checking and testing out in two columns makes the line clearer than prose does. The left column is what a machine can do; the right column is what only a person can do:

📌【在此插入圖 diagram-01.png】

The bottom cell on the left is a reminder of something easy to forget: mutation, constraint tests and pass^k all sit on the checking side too. A better check does not complete testing on its own. It handles repeatable checks first, giving people results and open questions from which to decide what still needs investigation.

So what do today's checks miss? The next section starts with two research findings, then identifies a reliability question teams need to measure for themselves.

---

## 3. What the data says in 2026: the three layers a green build does not cover

The gaps behind a green build fall into three layers: passing functional tests does not establish that constraints are met; having tests does not establish that the relevant behavior was tested; and one success does not establish reliability. Each layer asks a different question and needs different evidence.

Every number here deliberately carries its domain, sample size and date, because research in the agent field moves fast and a number that leaves its context is easy to misuse. The first two layers each get one in-domain anchor paper — measured in the code domain itself, not borrowed from somewhere else. The third layer has no ready-made number in the code domain that I can cite, so the approach is a plain one: repeat the tasks in your own golden set and measure reliability.

SWE-Gate, in the table below, is a benchmark. What it does is hand an agent's patches to the functional tests and to the reviewer constraints at the same time, and look at how far the two results diverge. The three layers and their anchors:

📌【在此插入表 table-01.png】

The same three layers as a figure, this time set against the green build. What to look at is the distance between each layer and the green:

📌【在此插入圖 diagram-02.png】

The final arrow is a reminder that all three layers need verification beyond the green CI result. The green light alone cannot answer those questions.

Human inspection is not a sufficient safety net either, though I had hoped it might be a fallback. In one experiment, 86 developers judged LLM-written assertions: their accuracy was 74% on correct assertions and only 49% on incorrect ones, without a corresponding drop in confidence (Poor and Overconfident Judges, July 2026). These are accuracy rates for judgments, not shares of participants divided into capable and incapable groups.

In this experiment, roughly half of the incorrect assertions were not identified correctly, and confidence did not reliably signal a need to check again. That does not describe every reviewer, but it does warn us that relying entirely on visual inspection leaves blind spots. Section 7 returns to this result when deciding what deserves human attention.

An example from my own workshop practice makes that gap concrete. It is much smaller than the studies above, but it puts the difference between "all tests green" and "the requirement was met" right in front of you. This summer, at the pattern-language-driven development workshop run by Teddy Chen (the instructor at Teddysoft), I asked an agent for a very small requirement. What it handed back came out like this: 5 tests all green, and the event-sourcing replay path never executed.

Event sourcing records state changes as events and reconstructs state from those events when needed; replay is that reconstruction path. It was central to this requirement, yet the tests never exercised it. Green only meant that the checks that ran did not fail. It said nothing about whether the untested path was correct. The testing piece tells the full story.

This example raises a more specific question than whether agents can be trusted: **the tests really ran, but they did not cover the path the requirement called for**. It makes the second layer concrete; the other two still need their own evidence.

This sounds like a new problem agents brought with them, and it isn't. The next section widens the time axis, and you will see that the same play has already run once.

---

## 4. Testing history has already run this experiment

A new verification problem is usually an old one in different clothes. Last season's historical through-line was DevOps 2014–2016; this season it is the history of testing.

The reason for the shift is that testing has long discussed many of the methods now used to verify agent output. Faster production creates fresh pressure to rethink the cost and division of verification work. The diagram places testing history on the left and today's verification layer on the right to show the connections:

📌【在此插入圖 diagram-03.png】

Two points in that figure are worth going into.

The first is in the timeline on the left. That line starts with Fagan inspection, the formal review where a group of people sits down and reads the code line by line; it ends with the deployment pipeline of Humble and Farley (the two authors of *Continuous Delivery*), which said long ago that a green commit stage is not a release. The agent era did not overturn that; it merely reinvents the later stages as three gates.

The second connection is on the right. Mutation testing still costs repeated test execution; agents have not made that computation disappear. They change the other side of the equation: tests arrive faster, inspecting each one by hand becomes harder to sustain, and evaluating their effectiveness matters more. Restricting mutation to the changed code offers a way to balance cost and protection.

**The methods from testing history are still available. What teams need to reconsider is where to spend their verification time and budget.**

The next section starts with tests. If agents write those too, where can instructions help, and which results still need separate measurement?

---

## 5. Don't teach the agent how to test; measure the work it delivers

Start with the last person in this industry you would expect to give up on TDD: Uncle Bob (Robert C. Martin), its main promoter. He settled his position on X this summer, which is what makes it worth reading. On July 29 he said you can't tell an agent to "stay clean," you can only measure the quality of its code and ask it to make corrections based on the results. The next day (July 30) he put it more bluntly: TDD is a human discipline and he does not expect agents to follow it.

When TDD's own promoter hands the agent's discipline problem over to measurement, that is where this section's title starts.

Another angle comes from Birgitta Böckeler, who leads AI-assisted software delivery at Thoughtworks. Böckeler framed "TDD inside the agent loop — theater or actual value?" as an empirical question: is that a ritual performed for an audience, or does it do something real? The piece was reposted on August 11 by her Thoughtworks colleague Martin Fowler, the author of *Refactoring*.

The answer is the third position from section 1. TDD steps may affect how an agent explores a task, so asking for TDD in AGENTS.md is reasonable. Whether it improves quality must still be assessed in the output. **The shape of TDD cannot serve as the gate**: following the sequence of tests and implementation does not by itself establish that the requirements were met.

Uncle Bob ran a small experiment on August 17; this piece calls it the negative test experiment, after that post. The design is simple: the same problem, four different test disciplines, each with and without a CRAP threshold, to see whether the programs that come out look the same — 8 runs in all. CRAP is Change Risk Anti-Patterns, a risk score that combines cyclomatic complexity (how many branches the code has) with coverage; the higher it goes, the more that code is both complicated and untested.

The result: **all runs passed the same 25 acceptance cases, yet produced different programs**. The same acceptance suite therefore permits different implementation structures; deciding which is better requires additional quality criteria. Both this experiment and SWE-Gate remind us that green has limits, but one observes implementation differences and the other measures constraint violations. They are not interchangeable evidence.

The Taiwanese discussion has landed in the same place. A post in the Scrum Community in Taiwan group argued that demanding human "values" of an AI is right, and forcing human "work habits" onto it is wrong. I agree with where that line is drawn, with one thing to add: what's missing is not the agreement, it's that nobody has written the gate yet.

The table below puts the instruction approach and the measurement approach side by side. The left column is the outcome you want, the middle relies on instructions alone, and the right is what can actually serve as a gate:

📌【在此插入表 table-02.png】

The right column connects each requirement to a result that can be checked. CI verifies some directly; others ask the agent to provide evidence for the team to examine. Prompts can guide behavior. Acceptance also needs a record of what actually happened and who verified the result.

The parts of the three gates have all appeared by now, scattered. The next section puts them into one figure and settles the order at the same time.

---

## 6. The three gates of the verification layer

The first five sections can now be drawn together. On the left are the code, tests and claims the agent delivers; on the right are the team's three gates for evaluating them. The gates still contain checking. The difference is that the team controls the acceptance criteria and responsibility for release:

📌【在此插入圖 diagram-04.png】

The figure is about the line down the middle: however well the left side does its job, it never crosses to the right on its own. The three gates on the right are ordered, and if the previous one hasn't passed, there is nothing to discuss about the next.

Each gate needs a clear question to answer, a metric to measure, and someone responsible for it:

📌【在此插入表 table-03.png】

One part in that table is shared by all three gates: constraint tests. The other terms get defined in the section that uses them; this one comes first. Take a hypothetical. A reviewer once left "don't open a new HTTP client every time here" on some PR, and that sentence gets written up as a rule CI runs on every PR. It has just turned from a comment into a check.

Constraint tests are installed and maintained by the test gate's owner, and the reliability gate only consumes the constraint pass rate computed from them (of the PRs that passed the functional tests, the share that also pass every constraint test).

All three gates share one line of design philosophy: **designing the environment beats writing rules**.

One study tested that approach experimentally. It gave the agent a formal way out — a channel for saying "this test is itself broken" — and the agent's rate of reward hacking dropped to roughly a quarter. Reward hacking here means going off to make the test pass instead of fixing the bug (escalation channels, August 2026; the baseline, the full numbers and that tool's schema are in the testing piece).

Rather than infer why an agent changed a test, I want to establish whether the workflow gives it a way to raise an objection, supply evidence and wait for the team's judgment.

Measurement in the test and reliability gates can be automated, and tools can help with review triage too. The team still has to decide who examines the evidence, which concerns need further investigation, and whether to approve the change.

---

## 7. Review is the control point, not the bottleneck

On September 2 Martin Fowler reposted an article, "Maybe we shouldn't be reviewing all this code," which puts the question more directly than I have: the problem isn't that AI broke code review, it's that we've been using review to solve the wrong problem.

This piece's version: **redesigning review is not about making humans read faster; it is about deciding what deserves a human's reading.**

The "review becomes the new bottleneck" point in [last season's overview](https://fantasybz.medium.com/dont-build-your-own-devin-org-strategy-and-a-90-day-blueprint-for-agentic-engineering-8187e7ec80f9), section 4, is one I have to correct myself: the bottleneck is a symptom; the disease is putting humans at the wrong gate, reading the wrong thing.

This section uses two numbers, one about scale and one about association.

Scale first. A study that followed its subjects over time, across three generations (from human review to agent review) and a million PRs (From Human-Centric to Agentic Code Review, July 2026), found that agent-initiated and multi-agent review made decisions faster **under some adoption patterns**, but not better. That "under some adoption patterns" qualifier is the paper's own, not mine.

Association next. Another study tracking 182 repos (Post-merge fate of agentic code, July 2026) found that agentic code needs significantly more after-the-fact bug-fixing maintenance. The association it reports runs like this: every 10 percentage points more in unreviewed-merge rate (the share of merges with no human approve at all) goes with roughly 6% more maintenance burden.

That number has to be read carefully. The original wording is "is associated with," correlation not causation, so it cannot carry a claim like "skip review and things will rot." But it is enough to make the unreviewed-merge rate a metric that belongs in the monthly report. Unreviewed here includes merges with only an AI approve — that is what the opening section's claim 2 means by "does not count."

Maintenance burden is not the only risk. Trust but Verify, a July 2026 study, found that most genuine secret leaks in its dataset were not caught before merge. That cannot all be attributed to unreviewed merges, but it calls for examining security controls across the workflow. The review piece gives the full figures.

Draw the upside and the debt as one figure, and the diamond in the middle is the control point this section's title is about:

📌【在此插入圖 diagram-05.png】

The right side lays out two workflow choices and the outcomes to track. Preserving comments as checks lets the same requirements be checked again; removing review can leave maintenance and security risks. This is a rationale for the design, not a causal conclusion from the associations above. After adoption, measure whether risk actually falls.

So why isn't a human reading the payment diff line by line the safety net? I have two reasons.

The first reason is the 49% in section 3: developers in that experiment identified incorrect assertions with roughly half accuracy. The task was assertion judgment, not a full PR review, so this is not a PR defect-detection rate. It is a reminder that time spent reading does not guarantee a correct judgment.

The second is compounding. A comment a human leaves while reading a diff reviews this one PR, and it is over once that PR merges. The same comment recycled into a constraint test checks every PR that follows.

For PRs with a high blast radius, turn repeatable conditions found during diff review into constraint tests. Blast radius is the reach of a failure. Auth, payments, schemas and infrastructure usually warrant close attention; an internal tool must also be assessed by its permissions and the data it can affect, rather than assumed to be low risk by name.

Once constraint tests and mutation reports adequately cover that class of change, people can review the intent and reports, then inspect flagged hunks and anything still in doubt in depth. A hunk is one segment of a diff. An unflagged hunk is not necessarily safe: if the reports cannot answer a key requirement in the intent, the PR is not yet verifiable. The review piece separately addresses review obligations and sampling for regulated systems.

The triage figure below has four exits, two of which require a human to review the work in depth:

📌【在此插入圖 diagram-06.png】

The lower-right cell is an easily missed starting point: for a bounded-impact PR without verification evidence, add checks before arranging report review and approval. If key requirements remain unverified, the low-risk label does not turn a hurried approval into adequate assurance.

The four exits are the four cells of the review piece's triage matrix. The full table is in that piece, and so are the reviewer fleet (layers of reviewers each looking at one part), the closed-loop ban and the approval artifact.

Review decides who reads what. The next section changes the question: how much autonomy can this kind of task actually be given?

---

## 8. Reliability is not capability: pass@1, pass^k and the oversight budget

Reliability is not capability, and that is this section's whole position. How strong an agent is and whether you dare hand it a whole class of tasks are two different things. Separating them takes two definitions:

- **pass@1**: the per-attempt success rate of each case, estimated from k reruns.
- **pass^k**: the share of cases that succeed on all k runs.
- Both are computed case by case first, then averaged over the whole golden set. "Succeeds at least once" is pass@k; this series does not use it.

One case makes the distinction clearer. Keep the task and execution conditions fixed, start each independent attempt from the same initial state, and suppose one attempt fails:

📌【在此插入圖 diagram-07.png】

The gap between the two boxes on the right is what to take from the figure: same case, same set of runs, and the two numbers reach completely different conclusions. One red is enough for "right every time" to be false.

The gap can be large. To measure it on your own system, repeat the 20–50 cases in last season's operations-piece golden set at k = 5 to 10 and compare the results. Those measurements should inform how far you expand autonomy; somebody else's benchmark cannot make that decision for you.

The third number is human effort. Here I borrow **a corroborating case outside code** — the concept transfers, the numbers do not.

READY is a qualification framework for enterprise agent deployment (September 2026). It asks, before an agent system is cleared to run, how many people it takes to reach the reliability you want. Its case is a clinical audit workflow, 16 agent systems, 750 cases. The domain is not code.

Two of those systems had autonomous accuracy only 0.3 percentage points apart (72.8% against 72.5%). With the reliability target set at the same 76% for both, their human review shares came out nearly 10 percentage points apart (39.2% against 29.6%) — the more accurate one needed more human eyes.

**A ranking by accuracy is not a ranking by human effort.**

My reading is that accuracy alone is not enough; we also need to ask whether a review policy can identify the errors. Errors concentrated in recognizable situations may be easier to allocate attention to, while less predictable errors may call for broader review. This is a possible explanation I infer from the results, not a mechanism the paper established for that difference.

The required human review share can be derived from a reliability target and compared with available capacity. This series calls that budgeting exercise the oversight budget. The reliability piece separates the required minimum, actual allocation and sustainable ceiling. First, put the two systems side by side:

📌【在此插入圖 diagram-08.png】

The two systems in the figure start out almost identical and end up far apart, and the only thing they share in between is that reliability target. An autonomy decision cannot be made on an accuracy number alone, and this figure is the reason.

The leadership monthly report works the same way: the single "pass rate" gives way to three numbers — the two golden-set numbers from above, plus section six's constraint pass rate:

📌【在此插入表 table-04.png】

The column that matters most in that table is the last one. "What it must not be used for" is not filler; it blocks the three most common misuses — deciding autonomy on a capability number, comparing your own numbers against someone else's benchmark, and treating a constraint pass rate as a reason to skip review.

These three numbers connect back to last season's operations-piece gate that decides whether autonomy gets opened wider (G2): autonomy expansion looks at pass^k and escape rate, not pass@1; escape rate is the share of defects that slip past these gates and are only found in production afterwards.

G2 originally tracked retries, escaped defects and the champion system. This season adds four measurable conditions — pass^k, the complement of constraint pass rate (constraint violation rate, or 1 minus the pass rate), a mutation score floor and oversight budget — and the full table is in the reliability piece.

Whether capability is improving and whether you can let go were always two different questions.

The question, the measurement and the owner for each of the three gates are now in place. The next section walks it backwards: what you see on the ground when none of this is installed.

---

## 9. Eight anti-patterns

Everything so far has been about what to do. This section turns it around into eight anti-patterns, because on the ground the thing recognized first is usually not the correct practice, it's the symptom. Every line in the right column below is something you can match yourself against directly:

📌【在此插入表 table-05.png】

One figure assigns each of the eight to the gate it belongs to:

📌【在此插入圖 diagram-09.png】

The assignment itself is the takeaway: not one of the eight is "the agent's problem." Every one of them maps to a gate that hasn't been installed yet.

Of the eight, in Taiwanese communities I see "coverage as quality" and "closed-loop review" most often — 5 and 6 in the table; an observation, not a statistic. The reasons are practical in both cases: coverage is the threshold easiest to bolt onto existing CI, with the number already there and no process to change, and seat-based subscriptions make "review yourself on the same subscription" the cheapest option.

None of the studies I have read counted the share of closed-loop reviews. The available research records a different kind of pairing. An August 2026 study (AI-to-AI Code Reviews) looked at 248,641 PRs. Cross-product AI-reviews-AI — a reviewer from a different vendor reviewing agent PRs — is only about 1.6% of the total, but between Q1 and Q3 2025 grew more than 100x.

Cross-product pairing can fit the approach allowed in this series, provided generation and review contexts are separated and a human gives the final approval. Different vendors alone do not guarantee independence. Same-model, same-session self-review is a separate rate worth tracking; the paper does not measure it, so teams need their own review records.

Once the symptoms are recognizable, what's left is the decision. In the next section I put myself in the engineering VP's or QA lead's seat and write down what I would and would not approve.

---

## 10. If I were the engineering VP or QA lead, how I would decide

The previous nine sections turn into a decision list here. The three lines below are written as realistic proposals, because that is usually how they get said out loud. I would **not** approve:

> "Turn the QA team into a prompt team."
> "Use AI review to clear the review backlog; an AI approve is enough to merge."
> "On the strength of an 85% eval pass rate, open write tools to every team in Q4."

The write tools in the third line are the tool permissions that let an agent change a system by itself. All three are blocked for the same reason: each of them wants an unmeasured number or process to stand in for a gate that isn't installed yet.

I **would** approve four things:

1. **Turn review comments into constraint tests first.** Pull 50 review comments from the agent PRs sent back in the last 90 days, classify them, pick out the executable ones, and write the first 10 constraint tests. For a repo with no comment history, derive the first 5 from the last 5 incident postmortems instead. This is the main route, not a fallback, because every "this must never happen again" was a constraint to begin with.
2. **Install a mutation gate on one pilot repo**, counting only the lines the agent changed. There are two conditions for turning it on: 200+ engineers or a QA lead who will read the report, and the affected test subset finishing within 10 minutes — at 50 people, don't turn it on, and the reason is in the table below. The threshold is **my suggested value (not an industry standard)**: mutation score ≥ 70%. Below the threshold, the PR goes back to the agent for more tests, not to a human to read. The rollout order is report only for a month, then block.
3. **The reviewer agent must be an instance from a different vendor, or at least a different session** (switch to another vendor's model, or at least open a separate conversation to do the review), and an AI approve never counts toward required approvals. Required approvals is GitHub's setting for how many approves a PR needs before it can merge. A merge with only an AI approve counts as unreviewed in section 7's unreviewed-merge rate. GitHub offers two candidate mechanisms. One is CODEOWNERS listing humans only, plus Require review from Code Owners; the other is a required status check that counts human approves. I have not tested either on a production repo, so I will validate first with a GitHub App's approve on my own repo, to see whether either route holds up. A design draft is in the review piece.
4. **The approval artifact binds a human identity to the hash of what was reviewed.** An approval artifact records who pressed approve on exactly what content; change the content and the record is void. On high-blast-radius PRs, whoever assigned the task cannot approve. There is a second reason to bind it to a person. Vendor terms contradict one another on "who may approve an agent's PR" (Where Accountability Lives, August 2026); the details go to December's accountability piece.

**How to think about the verification budget.** An August 2026 study (The reach of a verification tool decides its value) gave me one principle: a verification tool's value is set by its reach. Its sample is 1,116 web apps, 6 models and 8 tool configurations. The clearest illustration is the boot probe, a check that only asks whether the app starts: at about 35% of a full shell's token cost, it removed almost all startup failures; a full shell costs 2.35x.

My proposed order starts with inexpensive checks that catch common errors, then adds more costly verification. Constraints expressible as static analysis can come alongside assertion-change diff; behavioral or performance constraints still require execution. Next come red-then-green and diff-scoped mutation, followed by k repeated runs and step-rubric judges, which use an LLM to assess each step. This is a proposed ordering by cost and risk, not a ranking directly measured by that study.

The budget ratio runs like this: for every $1 the agent spends producing, budget $0.30 to $0.50 to verify it. The denominator is agent tokens plus generation-side CI, the machine cost of what the agent produces; the numerator is verification-side compute, the machine cost of verifying it. **The ratio is my provisional heuristic, to be calibrated by the pilot** — that paper supports the principle, not the ratio. **Human review time is not in this ratio**; it goes through the reliability piece's oversight budget, and the two are reported to the CFO separately.

**Installing at 50 / 200 / 1,000 engineers.** This is about rolling a gate from one repo to forty; the autonomy expansion G2 talks about is a different thing:

📌【在此插入表 table-06.png】

What is worth looking at in that table is the gap between the middle column and the right one: the set of checks only shrinks at the smallest scale, but who owns the gate changes on every row. The shrink has exactly one reason: at a scale where nobody would read the report, mutation stays off. The paved road in the table is the path the platform has laid in advance and that works by default.

**Brownfield: which gate comes first.** Consider a concrete scenario: a 15-year-old legacy monolith, a 40-minute test suite, 30% coverage and no organized review-comment history. The sequence below is for introducing verification in that kind of repo, with each step's prerequisites listed. It does not replace the legibility sequence from section 7 of last season's overview: characterization tests → logs / traces → architecture rules. If there are no tests, recording existing behavior with characterization tests is step 0. Those records still need to distinguish requirements from current behavior that has not yet been validated:

📌【在此插入表 table-07.png】

These four checks are just as useful on human-written PRs — loosened assertions, frozen bugs and violated team constraints were not invented by agents. **Even if the agent bet fails, none of these gates is wasted.**

---

## 11. A 90-day action blueprint for the verification layer

The previous section listed what I would and would not approve, but a list on its own has no order. This section lays it out on a timeline: which gate goes in which month, and what has to be visible at the end of each month before it is reasonable to move on.

The starting point first. Once the gates are in, someone will ask whether things actually got better, and answering that requires knowing what things were like before adoption. The main work of month 1 is to establish a baseline: measure performance before any intervention, so there is something to compare the later results with.

There are six metrics to track. The first two were already being measured last season: escape rate, defined in section eight, and review minutes per PR, the average human review minutes each PR consumes. The other four are new this season:

- The share of PRs that weaken an existing assertion
- The share of snapshot or golden-file updates with no stated reason (a golden file records the current output as the expected answer; it is not the same thing as the golden set)
- The share of agent-changed lines that existing tests cover
- The share of new or modified test files written by the agent

The last one deserves its own note. What it measures is not quality but whether the opening section's premise holds at all. If most new tests are still human-written, the repo differs from the scenario in section 1, which can inform adoption priorities. Test independence still needs scrutiny; authorship alone does not establish it. The reason from the previous section still stands: these checks are useful on human-written PRs too. Understanding the current state helps set an adoption pace the team can sustain.

With the six numbers in hand, what's left is the schedule. Each row of the table below is one phase: the middle column is that month's work, and the right column is the exit criteria — the bar for moving on to the next month.

📌【在此插入表 table-08.png】

Exit conditions are the easiest column to skip. They establish readiness to proceed; a calendar cannot substitute for them. If constraint tests block no PRs for a month, first check whether they cover the intended risks, including replaying past violating patches. No catches can mean compliant changes or a missed check. Do not manufacture a blocking rule merely to prove that the gate is useful.

The table answers what to do each month. The figure below takes only the first three months and lines up each month's exit criteria, to show how they converge on one decision:

📌【在此插入圖 diagram-10.png】

The main line runs straight down and lands on the node at the bottom right. The end of three months is not "all four checks are installed," it is that someone has taken these numbers and made one keep-or-expand call on autonomy, with the reasons said out loud. Expanding and holding both count; nobody deciding is the failure.

Two reminders to close on, both about the places I think this most easily goes wrong:

1. **Add mutation last; report before blocking.** Observe reports in month 1 and introduce blocking in month 3 based on calibration. The team needs to understand which signals warrant stopping before it can trust the gate. Red-then-green also needs explicit scope: here it applies to changes to existing behavior. A feature PR may fail to run because a class or interface does not yet exist; that is not the behavioral difference being tested and is not a valid red.
2. **Start constraint tests from the rules that are executable and least contested.** What do those look like? No new dependencies, no new public API, a consistent log format. What they have in common is that right and wrong are obvious, and writing them as a CI check starts no arguments. Do not start with architecture rules. Suppose the first rule you write is "no calls across layers": that rule sets off an architecture debate inside review, and the whole constraint-tests effort stalls before it has run once.

Whether three months is enough has less to do with how good the tools are than with whether anyone is willing to stop when the exit criteria haven't been met.

---

## 12. Closing

Back to the three scenarios from the opening section. With all three gates installed, how do they end?

The next time the engineer is asked whether the PR was tested, there will be concrete results to discuss together: whether the constraint report passed, which risks the mutation report identified, and what kind of review the triage matrix calls for. "The AI says it is fine" finally comes with evidence that makes a follow-up question possible.

The PR that turned `assertEqual` into `assertIn` gets caught by the assertion-change diff before merge — equality swapped for containment is a drop in strength, and it blocks outright. The tests are still green; the PR still doesn't get through.

As for the one that broke production and turned out to have only a reviewer agent's approve, the "who looked at this change" field in the postmortem will have a name in it, because an AI approve never counted in the first place.

Not one of the three came from the agent getting better. All they did was move the source of evidence out of the agent's own hands and into measurements the organization owns.

Back to Bach: checking can be automated; testing still requires human judgment. Agents make some checks easier to create and run, which gives teams a more pressing question: which unexamined problems deserve the time we have saved? That is the human effort I want to preserve: suspecting that something may be wrong, then finding a way to investigate it.

One last prediction with a date on it, so that it can be checked and so that it can be wrong. By 2027, a reliability gate will be standard in G2, and "reporting only pass@1" will draw the same frown that "only looking at coverage" does today. That is my judgment, not the conclusion of any trend report.

> **When an agent writes both implementation and tests without independent scrutiny, green means it passed its own exam. Measure the work it delivers, then reserve human time for the decisions that need judgment.**

Turning some measurements into checks in CI is engineering work a team can build up gradually. The next decision is a shared one: what should human time be reserved for? Acknowledging that reviewer time is finite makes room to discuss which work machines can handle and which still needs a person to look closely.

One piece per gate, starting with the testing piece. Further out, November's theme, "the same spec, run ten times," pushes pass^k one step further, into the variance of the harness (the layer last season's technical piece covered: the tools and process around the agent). How consistent the results are when the same task is repeated is mostly treated today as a question about the model. What I want to talk about is how much of it the harness decides.

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
