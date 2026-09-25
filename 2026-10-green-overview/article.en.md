# Green Is Not Done: Testing, Review and Reliability for Agent Output

> **TL;DR** — When a team adopts coding agents and keeps seeing green CI, a growing review queue and production failures, it is worth asking whether its acceptance criteria have kept pace. If an agent writes both the implementation and its tests, without independent scrutiny of those tests, green only shows that it passed its own exam. In James Bach's terms, that is *checking*; it is not enough to complete *testing*. Three gates divide the work: the test gate assesses test effectiveness through mutation score; the review gate assigns who examines what; and the reliability gate uses constraint tests and pass^k to inform expanded authority. Section 1 sets out three positions: how humans review payment PRs, whether AI approvals count, and whether TDD can serve as a gate. Every number keeps its domain attached: SWE-Gate measured the finding that "34% of green patches violate reviewer constraints" across 75 Python repos. A 90-day blueprint closes the piece.

> Series: **Overview (this piece)** → 1. Testing (coming soon) → 2. Review (coming soon) → 3. Reliability (coming soon) → 4. Payment Walkthrough (coming soon). Related reading, the Agentic Engineering series: [Don't Build Your Own Devin](https://fantasybz.medium.com/dont-build-your-own-devin-org-strategy-and-a-90-day-blueprint-for-agentic-engineering-8187e7ec80f9) → [1. Org Design](https://fantasybz.medium.com/agentic-engineering-part-1-who-does-this-platform-plus-federation-in-practice-92343384d987) → [2. The Harness Blueprint](https://fantasybz.medium.com/agentic-engineering-part-2-the-harness-blueprint-making-your-system-legible-to-agents-3facc281f633) → [3. Evals and Unit Economics](https://fantasybz.medium.com/agentic-engineering-part-3-evals-unit-economics-and-scaling-running-agents-like-a-product-1cb1855a2046)

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

Once claims and execution results are separated, the next question is which results can support acceptance. This series distinguishes three sources; that distinction guides the discussion of acceptance evidence throughout the four parts:

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

```mermaid
---
config:
  theme: base
  themeVariables:
    fontSize: 16px
    primaryColor: "#f8f9fa"
    primaryTextColor: "#1f2933"
    primaryBorderColor: "#6b7280"
    lineColor: "#6b7280"
    secondaryColor: "#f8f9fa"
    tertiaryColor: "#ffffff"
    clusterBkg: "#ffffff"
    clusterBorder: "#9ca3af"
    edgeLabelBackground: "#ffffff"
  flowchart:
    nodeSpacing: 36
    rankSpacing: 44
    padding: 12
    htmlLabels: true
    subGraphTitleMargin:
      top: 8
      bottom: 12
    curve: basis
---
flowchart LR
    classDef own fill:#d4edda,stroke:#2e7d32,color:#1f2933
    classDef buy fill:#fff3cd,stroke:#b8860b,color:#1f2933
    classDef bad fill:#ffe0e0,stroke:#c0392b,color:#1f2933
    classDef human fill:#e3f2fd,stroke:#1565c0,color:#1f2933
    subgraph chk["Checking: mechanically verifying propositions"]
        direction TB
        C1["Green CI build<br/>coverage threshold"] ~~~ C2["Agent-written tests are executed<br/>claims still need verification"]
        C2 ~~~ C3["Mutation, constraint tests<br/>pass^k: better checks"]
    end
    subgraph tst["Testing: learning and evaluating<br/>on faith that trouble exists"]
        direction TB
        T1["Read intent and constraint report<br/>ask “where did this<br/>expected value come from”"] ~~~ T2["Exploratory testing of the output"]
        T2 ~~~ T3["Make timely business decisions<br/>merge, expand autonomy, or don't"]
    end
    chk -.->|is not| tst
    class C1,C2 buy
    class C3 own
    class T1,T2,T3 human
```

The bottom cell on the left is a reminder of something easy to forget: mutation, constraint tests and pass^k all sit on the checking side too. A better check does not complete testing on its own. It handles repeatable checks first, giving people results and open questions from which to decide what still needs investigation.

So what do today's checks miss? The next section starts with two research findings, then identifies a reliability question teams need to measure for themselves.

---

## 3. What the data says in 2026: the three layers a green build does not cover

The gaps behind a green build fall into three layers: passing functional tests does not establish that constraints are met; having tests does not establish that the relevant behavior was tested; and one success does not establish reliability. Each layer asks a different question and needs different evidence.

Every number here deliberately carries its domain, sample size and date, because research in the agent field moves fast and a number that leaves its context is easy to misuse. The first two layers each get one in-domain anchor paper — measured in the code domain itself, not borrowed from somewhere else. The third layer has no ready-made number in the code domain that I can cite, so the approach is a plain one: repeat the tasks in your own golden set and measure reliability.

SWE-Gate, in the table below, is a benchmark. What it does is hand an agent's patches to the functional tests and to the reviewer constraints at the same time, and look at how far the two results diverge. The three layers and their anchors:

| Layer | Claim | Anchor (in-domain) | More evidence |
|---|---|---|---|
| Functional tests pass ≠ constraints met | Green checked only part of what the reviewer cares about | SWE-Gate: of 644 patches that passed functional tests, 221 (34%) violated a constraint derived from real PR comments (75 Python repos, 303 tasks, September 2026) | Reliability piece |
| Has tests ≠ tested | How much of the agent-changed code the existing tests actually touch | Test Coverage of Agentic PRs: 4,882 agent PRs; the repo's existing tests touch only 61.5% (Java) and 27.0% (Python) of agent-changed lines (July 2026) | Testing piece |
| One success ≠ reliable | pass@1 and pass^k are two different numbers | Run your own golden set k times (defined in section 8) | Reliability piece |

The same three layers as a figure, this time set against the green build. What to look at is the distance between each layer and the green:

```mermaid
---
config:
  theme: base
  themeVariables:
    fontSize: 16px
    primaryColor: "#f8f9fa"
    primaryTextColor: "#1f2933"
    primaryBorderColor: "#6b7280"
    lineColor: "#6b7280"
    secondaryColor: "#f8f9fa"
    tertiaryColor: "#ffffff"
    clusterBkg: "#ffffff"
    clusterBorder: "#9ca3af"
    edgeLabelBackground: "#ffffff"
  flowchart:
    nodeSpacing: 36
    rankSpacing: 44
    padding: 12
    htmlLabels: true
    subGraphTitleMargin:
      top: 8
      bottom: 12
    curve: basis
---
flowchart TB
    classDef own fill:#d4edda,stroke:#2e7d32,color:#1f2933
    classDef buy fill:#fff3cd,stroke:#b8860b,color:#1f2933
    classDef bad fill:#ffe0e0,stroke:#c0392b,color:#1f2933
    classDef human fill:#e3f2fd,stroke:#1565c0,color:#1f2933
    G{"Green CI build"}
    subgraph layers["The three layers and their anchors"]
        direction LR
        L1["Functional pass ≠ constraints met<br/>green checked only part of<br/>what reviewers care about"] --> S1["SWE-Gate: 644 green patches<br/>34% violate a reviewer constraint<br/>75 Python repos"]
        L2["Has tests ≠ tested<br/>how much of the agent's change<br/>do the tests actually touch"] --> S2["Test Coverage of Agentic PRs<br/>existing tests reach changed lines<br/>Java 61.5%, Python 27.0%"]
        L3["One success ≠ reliable<br/>pass@1 and pass^k<br/>are two different numbers"] --> S3["Your own golden set<br/>pass@1 and pass^k, reported apart<br/>method in the reliability piece"]
    end
    G --> layers
    layers --> C["Current CI green<br/>cannot answer all three questions"]
    class G buy
    class L1,L2,L3 bad
    class S3 own
```

The final arrow is a reminder that all three layers need verification beyond the green CI result. The green light alone cannot answer those questions.

Human inspection is not a sufficient safety net either, though I had hoped it might be a fallback. In one experiment, 86 developers judged LLM-written assertions: their accuracy was 74% on correct assertions and only 49% on incorrect ones, without a corresponding drop in confidence (Poor and Overconfident Judges, July 2026). These are accuracy rates for judgments, not shares of participants divided into capable and incapable groups.

In this experiment, roughly half of the incorrect assertions were not identified correctly, and confidence did not reliably signal a need to check again. That does not describe every reviewer, but it does warn us that relying entirely on visual inspection leaves blind spots. Section 7 returns to this result when deciding what deserves human attention.

An example from my own workshop practice makes that gap concrete. It is much smaller than the studies above, but it puts the difference between "all tests green" and "the requirement was met" right in front of you. This summer, at the pattern-language-driven development workshop run by Teddy Chen (the instructor at Teddysoft), I asked an agent for a very small requirement. What it handed back came out like this: 5 tests all green, and the event-sourcing replay path never executed.

Event sourcing records state changes as events and reconstructs state from those events when needed; replay is that reconstruction path. It was central to this requirement, yet the tests never exercised it. Green only meant that the checks that ran did not fail. It said nothing about whether the untested path was correct. The testing piece tells the full story.

This example raises a more specific question than whether agents can be trusted: **the tests really ran, but they did not cover the path the requirement called for**. It makes the second layer concrete; the other two still need their own evidence.

This sounds like a new problem agents brought with them, and it isn't. The next section widens the time axis, and you will see that the same play has already run once.

---

## 4. Testing history has already run this experiment

When a new verification problem appears, I find it useful to look for similar situations in engineering history. “Don’t Build Your Own Devin” drew on DevOps in 2014–2016 to discuss organizational choices. This piece turns to testing history and the debates that preceded today’s questions.

The reason for the shift is that testing has long discussed many of the methods now used to verify agent output. Faster production creates fresh pressure to rethink the cost and division of verification work. The diagram places testing history on the left and today's verification layer on the right to show the connections:

```mermaid
---
config:
  theme: base
  themeVariables:
    fontSize: 16px
    primaryColor: "#f8f9fa"
    primaryTextColor: "#1f2933"
    primaryBorderColor: "#6b7280"
    lineColor: "#6b7280"
    secondaryColor: "#f8f9fa"
    tertiaryColor: "#ffffff"
    clusterBkg: "#ffffff"
    clusterBorder: "#9ca3af"
    edgeLabelBackground: "#ffffff"
  flowchart:
    nodeSpacing: 36
    rankSpacing: 44
    padding: 12
    htmlLabels: true
    subGraphTitleMargin:
      top: 8
      bottom: 12
    curve: basis
---
flowchart LR
    classDef own fill:#d4edda,stroke:#2e7d32,color:#1f2933
    classDef buy fill:#fff3cd,stroke:#b8860b,color:#1f2933
    classDef bad fill:#ffe0e0,stroke:#c0392b,color:#1f2933
    classDef human fill:#e3f2fd,stroke:#1565c0,color:#1f2933
    subgraph past["Testing history / CD history"]
        direction TB
        P1["1976 Fagan inspection<br/>humans read line by line"] --> P2["1978 mutation testing<br/>the cost of repeated test runs"]
        P2 --> P3["2009 Bach / Bolton<br/>checking ≠ testing"]
        P3 --> P4["2010 deployment pipeline<br/>green commit ≠ release"]
    end
    subgraph now["2026 agent verification layer"]
        direction TB
        N1["Humans read intent and constraints<br/>machines read the diff"] ~~~ N2["Diff-scoped mutation<br/>narrow scope, assess cost"]
        N2 ~~~ N3["Green is a checking result<br/>agent claims still need verification"]
        N3 ~~~ N4["test → review → reliability<br/>your 90 days install three gates"]
    end
    past --> now
    class N1 human
    class N2,N4 own
    class N3 buy
```

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

| What you want | Instruction (not a gate) | Measurement (the gate) |
|---|---|---|
| Effective tests | AGENTS.md: "please use TDD" | Mutation score ≥ threshold (agent-changed lines only) |
| Existing tests not broken | "Do not modify existing assertions" | CI check: existing assertion weakened → block; bug fix PRs also run red-then-green |
| Reviewer constraints respected | "Please follow team conventions" | Constraint tests (review comment → rule → executable check) |
| Honest reporting | "Tell me if a test is broken" | Structured escalation tool (`report_broken_test`), with evidence the team verifies |
| Reliable | "Please check carefully" | pass^k on the golden set ≥ threshold |

The right column connects each requirement to a result that can be checked. CI verifies some directly; others ask the agent to provide evidence for the team to examine. Prompts can guide behavior. Acceptance also needs a record of what actually happened and who verified the result.

The parts of the three gates have all appeared by now, scattered. The next section puts them into one figure and settles the order at the same time.

---

## 6. The three gates of the verification layer

The first five sections can now be drawn together. On the left are the code, tests and claims the agent delivers; on the right are the team's three gates for evaluating them. The gates still contain checking. The difference is that the team controls the acceptance criteria and responsibility for release:

```mermaid
---
config:
  theme: base
  themeVariables:
    fontSize: 16px
    primaryColor: "#f8f9fa"
    primaryTextColor: "#1f2933"
    primaryBorderColor: "#6b7280"
    lineColor: "#6b7280"
    secondaryColor: "#f8f9fa"
    tertiaryColor: "#ffffff"
    clusterBkg: "#ffffff"
    clusterBorder: "#9ca3af"
    edgeLabelBackground: "#ffffff"
  flowchart:
    nodeSpacing: 36
    rankSpacing: 44
    padding: 12
    htmlLabels: true
    subGraphTitleMargin:
      top: 8
      bottom: 12
    curve: basis
---
flowchart LR
    classDef own fill:#d4edda,stroke:#2e7d32,color:#1f2933
    classDef buy fill:#fff3cd,stroke:#b8860b,color:#1f2933
    classDef bad fill:#ffe0e0,stroke:#c0392b,color:#1f2933
    classDef human fill:#e3f2fd,stroke:#1565c0,color:#1f2933
    subgraph gen["The agent's side: checking"]
        direction TB
        A["Agent produces a PR"] --> B["Tests the agent wrote"]
        B --> G{"Green CI build"}
        G -.->|fail, retry| A
        G --> S["“Done, all tests pass”"]
    end
    subgraph ver["The acceptance side: three gates"]
        direction TB
        T["Test gate<br/>mutation, assertion diff"] --> R["Review gate<br/>humans read intent and constraints"]
        R --> L["Reliability gate<br/>pass^k, constraint pass rate"]
        L --> M["Merge / expand autonomy"]
    end
    gen --> ver
    class B,G,S buy
    class T,L own
    class R human
```

The figure is about the line down the middle: however well the left side does its job, it never crosses to the right on its own. The order on the right describes evidence needed before merging or expanding autonomy. It does not require people to wait for the test gate before discussing a change. Review can establish requirements and constraints earlier, then feed them back into testing. Final approval still needs the missing evidence filled in.

Each gate needs a clear question to answer, a metric to measure, and someone responsible for it:

| Gate | Question | What it checks or measures | Owner | Deep dive |
|---|---|---|---|---|
| Test gate | Can these tests catch a bug? | Mutation score, assertion-change diff, red-then-green | QA / test lead + platform | Testing piece |
| Review gate | Who should read this PR, and what should they read? | Triage matrix, reviewer heterogeneity, approval artifact | EM + seniors | Review piece |
| Reliability gate | How much autonomy can this kind of task get? | Constraint pass rate, pass^k, oversight budget | Platform + VP | Reliability piece |

One component is shared by all three gates: constraint tests. Consider a bottle of 無糖純喫綠茶, unsweetened pure green tea, with an illustrative NTD 35 order. A reviewer asks: “The payment was sent, but the screen stopped responding. Could another click charge again?” The team agrees that replaying the same attempt must not charge twice and retains an executable check. The comment now protects future changes. This is a teaching scenario, not the product's actual price.

“Constraint” describes the requirement's origin and continuing responsibility, not a test technology that excludes functional behavior. Charging the right amount and avoiding duplicate charges are both product requirements. A unit or integration test can protect a constraint the reviewer has chosen to retain. Selection depends on consequences, a decidable expected result and ownership; not every comment needs its own test.

In the accompanying [payment example](https://github.com/fantasybz/medium-articles/tree/main/examples/tea_payment), two happy-path tests detect two of seven selected mutants, for a mutation score of 28.6%. Eight tests omitting the timeout case reach 85.7% while still missing an unknown payment marked successful. All nine tests detect all seven mutants. These are measured results from sequential calls to a fake provider in one process, not evidence about concurrency, restarts or real charges.

The test gate supplies the individual results. At the review gate, someone who understands payments decides whether a surviving mutant violates a critical requirement; the percentage alone cannot authorize the change. Measuring constraint pass rate at the reliability gate changes the denominator to candidate PRs passing functional checks, then asks what share also pass every applicable constraint. One example passing nine tests does not measure an agent's long-term reliability. “Part 4 — A Payment Walkthrough: Buying Unsweetened Green Tea, from Review Constraints to Mutation Score” develops the selection decisions, implementation and arithmetic.

All three gates share one line of design philosophy: **designing the environment beats writing rules**.

One study tested that approach experimentally. It gave the agent a formal way out — a channel for saying "this test is itself broken" — and the agent's rate of reward hacking dropped to roughly a quarter. Reward hacking here means going off to make the test pass instead of fixing the bug (escalation channels, August 2026; the baseline, the full numbers and that tool's schema are in the testing piece).

Rather than infer why an agent changed a test, I want to establish whether the workflow gives it a way to raise an objection, supply evidence and wait for the team's judgment.

Measurement in the test and reliability gates can be automated, and tools can help with review triage too. The team still has to decide who examines the evidence, which concerns need further investigation, and whether to approve the change.

---

## 7. Review is the control point, not the bottleneck

On September 2 Martin Fowler reposted an article, "Maybe we shouldn't be reviewing all this code," which puts the question more directly than I have: the problem isn't that AI broke code review, it's that we've been using review to solve the wrong problem.

This piece's version: **redesigning review is not about making humans read faster; it is about deciding what deserves a human's reading.**

The "review becomes the new bottleneck" point in [“Don’t Build Your Own Devin”](https://fantasybz.medium.com/dont-build-your-own-devin-org-strategy-and-a-90-day-blueprint-for-agentic-engineering-8187e7ec80f9), section 4, is one I have to correct myself: the bottleneck is a symptom; the disease is putting humans at the wrong gate, reading the wrong thing.

This section uses two numbers, one about scale and one about association.

Scale first. A study that followed its subjects over time, across three generations (from human review to agent review) and a million PRs (From Human-Centric to Agentic Code Review, July 2026), found that agent-initiated and multi-agent review made decisions faster **under some adoption patterns**, but not better. That "under some adoption patterns" qualifier is the paper's own, not mine.

Association next. Another study tracking 182 repos (Post-merge fate of agentic code, July 2026) found that agentic code needs significantly more after-the-fact bug-fixing maintenance. The association it reports runs like this: every 10 percentage points more in unreviewed-merge rate (the share of merges with no human approve at all) goes with roughly 6% more maintenance burden.

That number has to be read carefully. The original wording is "is associated with," correlation not causation, so it cannot carry a claim like "skip review and things will rot." But it is enough to make the unreviewed-merge rate a metric that belongs in the monthly report. Unreviewed here includes merges with only an AI approve — that is what the opening section's claim 2 means by "does not count."

Maintenance burden is not the only risk. Trust but Verify, a July 2026 study, found that most genuine secret leaks in its dataset were not caught before merge. That cannot all be attributed to unreviewed merges, but it calls for examining security controls across the workflow. The review piece gives the full figures.

Draw the upside and the debt as one figure, and the diamond in the middle is the control point this section's title is about:

```mermaid
---
config:
  theme: base
  themeVariables:
    fontSize: 16px
    primaryColor: "#f8f9fa"
    primaryTextColor: "#1f2933"
    primaryBorderColor: "#6b7280"
    lineColor: "#6b7280"
    secondaryColor: "#f8f9fa"
    tertiaryColor: "#ffffff"
    clusterBkg: "#ffffff"
    clusterBorder: "#9ca3af"
    edgeLabelBackground: "#ffffff"
  flowchart:
    nodeSpacing: 96
    rankSpacing: 44
    padding: 12
    htmlLabels: true
    subGraphTitleMargin:
      top: 8
      bottom: 12
    curve: basis
---
flowchart TB
    classDef own fill:#d4edda,stroke:#2e7d32,color:#1f2933
    classDef buy fill:#fff3cd,stroke:#b8860b,color:#1f2933
    classDef bad fill:#ffe0e0,stroke:#c0392b,color:#1f2933
    classDef human fill:#e3f2fd,stroke:#1565c0,color:#1f2933
    A["PR produced by an agent"] --> R{"Review gate<br/>the organization's control point"}
    R -->|held| G1["Goal: fewer repeated errors<br/>measure the effect"]
    G1 --> G2["Review comments recycled<br/>into constraint tests"]
    R -->|let go| B1["Debt<br/>each +10pp unreviewed-merge rate<br/>≈ +6% maintenance (association)"]
    B1 --> B2["Most leaked secrets<br/>not caught before merge"]
    G2 & B2 --> M["Unreviewed-merge rate<br/>in the monthly report<br/>as a metric to manage"]
    class R human
    class G1,G2 own
    class B1,B2 bad
    class M buy
```

The right side lays out two workflow choices and the outcomes to track. Preserving comments as checks lets the same requirements be checked again; removing review can leave maintenance and security risks. This is a rationale for the design, not a causal conclusion from the associations above. After adoption, measure whether risk actually falls.

Reading payment changes line by line still has value. Relying on it as the only safety net, however, asks too much of a reviewer’s attention. I see at least two reasons to move repeatable checks into tools.

The first reason is the 49% in section 3: developers in that experiment identified incorrect assertions with roughly half accuracy. The task was assertion judgment, not a full PR review, so this is not a PR defect-detection rate. It is a reminder that time spent reading does not guarantee a correct judgment.

The second reason is to preserve what a review teaches the team. A comment may resolve the current PR without being remembered when the next change arrives. Turning its repeatable requirement into a constraint test makes that check available to later PRs and saves reviewers from having to raise the same concern again.

For PRs with a high blast radius, turn repeatable conditions found during diff review into constraint tests. Blast radius is the reach of a failure. Auth, payments, schemas and infrastructure usually warrant close attention; an internal tool must also be assessed by its permissions and the data it can affect, rather than assumed to be low risk by name.

Once constraint tests and mutation reports adequately cover that class of change, people can review the intent and reports, then inspect flagged hunks and anything still in doubt in depth. A hunk is one segment of a diff. An unflagged hunk is not necessarily safe: if the reports cannot answer a key requirement in the intent, the PR is not yet verifiable. The review piece separately addresses review obligations and sampling for regulated systems.

The triage figure below has four exits, two of which require a human to review the work in depth:

```mermaid
---
config:
  theme: base
  themeVariables:
    fontSize: 16px
    primaryColor: "#f8f9fa"
    primaryTextColor: "#1f2933"
    primaryBorderColor: "#6b7280"
    lineColor: "#6b7280"
    secondaryColor: "#f8f9fa"
    tertiaryColor: "#ffffff"
    clusterBkg: "#ffffff"
    clusterBorder: "#9ca3af"
    edgeLabelBackground: "#ffffff"
  flowchart:
    nodeSpacing: 36
    rankSpacing: 44
    padding: 12
    htmlLabels: true
    subGraphTitleMargin:
      top: 8
      bottom: 12
    curve: basis
---
flowchart TB
    classDef own fill:#d4edda,stroke:#2e7d32,color:#1f2933
    classDef buy fill:#fff3cd,stroke:#b8860b,color:#1f2933
    classDef bad fill:#ffe0e0,stroke:#c0392b,color:#1f2933
    classDef human fill:#e3f2fd,stroke:#1565c0,color:#1f2933
    P["PR opened by an agent"] --> Q1{"High blast radius?<br/>auth / payment / schema / infra"}
    Q1 -->|yes| Q2{"Do checks cover<br/>key requirements?"}
    Q1 -->|no| Q3{"Do checks cover<br/>key requirements?"}
    Q2 -->|yes| O1["Read intent + reports<br/>check hunks as needed<br/>human approves"]
    Q2 -->|no| O2["Human reads diff"]
    Q3 -->|yes| O3["Machine review<br/>human approval<br/>sampled deep review"]
    Q3 -->|no| O4["Add checks first"]
    class O1,O2 human
    class O3 own
    class O4 buy
```

The lower-right cell is an easily missed starting point: for a bounded-impact PR without verification evidence, add checks before arranging report review and approval. If key requirements remain unverified, the low-risk label does not turn a hurried approval into adequate assurance.

These four exits correspond to the triage matrix in the review piece, which develops the reviewer fleet’s responsibilities, the ban on same-session self-review, and the information an approval record needs to preserve. For now, the decision starts here: before assigning reading, establish what evidence the PR already has and which questions remain open.

The review gate determines how to assess the PR in front of us. Passing that review still leaves another question: when we hand this class of task to the agent repeatedly, is its performance consistent enough to justify broader autonomy?

---

## 8. Reliability is not capability: pass@1, pass^k and the oversight budget

A successful attempt shows what an agent can do. Deciding how much authority to give it also requires knowing whether that performance holds across repeated attempts. Those questions need separate measurements rather than one undifferentiated “pass rate”:

- **pass@1**: the per-attempt success rate of each case, estimated from k reruns.
- **pass^k**: the share of cases that succeed on all k runs.
- Both are computed case by case first, then averaged over the whole golden set. "Succeeds at least once" is pass@k; this series does not use it.

One case makes the distinction clearer. Keep the task and execution conditions fixed, start each independent attempt from the same initial state, and suppose one attempt fails:

```mermaid
---
config:
  theme: base
  themeVariables:
    fontSize: 16px
    primaryColor: "#f8f9fa"
    primaryTextColor: "#1f2933"
    primaryBorderColor: "#6b7280"
    lineColor: "#6b7280"
    secondaryColor: "#f8f9fa"
    tertiaryColor: "#ffffff"
    clusterBkg: "#ffffff"
    clusterBorder: "#9ca3af"
    edgeLabelBackground: "#ffffff"
  flowchart:
    nodeSpacing: 36
    rankSpacing: 44
    padding: 12
    htmlLabels: true
    subGraphTitleMargin:
      top: 8
      bottom: 12
    curve: basis
---
flowchart TB
    classDef own fill:#d4edda,stroke:#2e7d32,color:#1f2933
    classDef buy fill:#fff3cd,stroke:#b8860b,color:#1f2933
    classDef bad fill:#ffe0e0,stroke:#c0392b,color:#1f2933
    classDef human fill:#e3f2fd,stroke:#1565c0,color:#1f2933
    C["The same golden case<br/>run k = 5 times"]
    subgraph runs[" "]
        direction LR
        r1["run 1 pass"] ~~~ r2["run 2 pass"] ~~~ r3["run 3 pass"]
        r4["run 4 red"] ~~~ r5["run 5 pass"]
    end
    C --> runs
    runs --> P1["This case's pass@1<br/>= 4 passes / 5 runs = 80%"]
    runs --> P5["This case's pass^5 = 0<br/>one red in five is not all-pass"]
    class r1,r2,r3,r5 own
    class r4 bad
    class P5 buy
```

Both numbers describe the same set of runs. pass@1 retains the successful attempts; pass^k asks whether this case succeeded every time. One failure excludes the case from the group that passed all k attempts. The gap comes from different criteria, not conflicting reports.

To measure that gap in your own system, use the golden-set approach proposed in “Agentic Engineering: Evals, Unit Economics, and Scaling”: select 20–50 cases and run each independently at k = 5 to 10. Those measurements provide a starting point for the autonomy discussion. Another team’s benchmark can inform it, but cannot make the decision for you.

After measuring success and consistency, we still need to account for human time. A **case from outside code** illustrates why systems with similar accuracy may need different review arrangements. The reasoning is useful here; its staffing proportions cannot be transferred directly to coding agents.

READY is a qualification framework for enterprise agent deployment (September 2026). It asks, before an agent system is cleared to run, how many people it takes to reach the reliability you want. Its case is a clinical audit workflow, 16 agent systems, 750 cases. The domain is not code.

Two of those systems had autonomous accuracy only 0.3 percentage points apart (72.8% against 72.5%). With the reliability target set at the same 76% for both, their human review shares came out nearly 10 percentage points apart (39.2% against 29.6%) — the more accurate one needed more human eyes.

**A ranking by accuracy is not a ranking by human effort.**

My reading is that accuracy alone is not enough; we also need to ask whether a review policy can identify the errors. Errors concentrated in recognizable situations may be easier to allocate attention to, while less predictable errors may call for broader review. This is a possible explanation I infer from the results, not a mechanism the paper established for that difference.

The required human review share can be derived from a reliability target and compared with available capacity. This series calls that budgeting exercise the oversight budget. The reliability piece separates the required minimum, actual allocation and sustainable ceiling. First, put the two systems side by side:

```mermaid
---
config:
  theme: base
  themeVariables:
    fontSize: 16px
    primaryColor: "#f8f9fa"
    primaryTextColor: "#1f2933"
    primaryBorderColor: "#6b7280"
    lineColor: "#6b7280"
    secondaryColor: "#f8f9fa"
    tertiaryColor: "#ffffff"
    clusterBkg: "#ffffff"
    clusterBorder: "#9ca3af"
    edgeLabelBackground: "#ffffff"
  flowchart:
    nodeSpacing: 36
    rankSpacing: 44
    padding: 12
    htmlLabels: true
    subGraphTitleMargin:
      top: 8
      bottom: 12
    curve: basis
---
flowchart LR
    classDef own fill:#d4edda,stroke:#2e7d32,color:#1f2933
    classDef buy fill:#fff3cd,stroke:#b8860b,color:#1f2933
    classDef bad fill:#ffe0e0,stroke:#c0392b,color:#1f2933
    classDef human fill:#e3f2fd,stroke:#1565c0,color:#1f2933
    subgraph sa["System A: accuracy 0.3pp higher"]
        direction TB
        A1["Autonomous accuracy 72.8%<br/>(0.3pp above B)"] --> A2["Reliability target 76%<br/>(same for both systems)"] --> A3["Human review needed 39.2%<br/>(nearly 10pp more than B)"]
    end
    subgraph sb["System B: nearly 10pp less human review"]
        direction TB
        B1["Autonomous accuracy 72.5%<br/>(0.3pp below A)"] --> B2["Reliability target 76%<br/>(same for both systems)"] --> B3["Human review needed 29.6%<br/>(nearly 10pp less than A)"]
    end
    sa ~~~ sb
    class A2,B2 human
    class A3 bad
    class B3 own
```

The systems have similar autonomous accuracy but need different review shares to reach the same reliability target. For the person allocating staff, that gap cannot disappear inside an average accuracy score. Choosing a system also means checking whether the team can sustain the review work it requires.

The leadership monthly report works the same way: the single "pass rate" gives way to three numbers — the two golden-set numbers from above, plus section six's constraint pass rate:

| Number | What it answers | What it must not be used for |
|---|---|---|
| pass@1 (golden set) | Is capability improving | Deciding autonomy |
| pass^k (golden set, k = 5–10) | How much autonomy this kind of task can get | Comparing against someone else's benchmark |
| Constraint pass rate (SWE-Gate style) | What was violated beyond the green build | Replacing review |

Each metric adds evidence and has limits. pass@1 can track capability but cannot decide autonomy on its own. pass^k only supports a meaningful comparison when the task set and k are considered with it. Constraint pass rate covers only requirements that have become checks. Keeping them separate prevents an attractive overall score from hiding different risks.

These measurements feed into G2, the autonomy-expansion gate in “Agentic Engineering: Evals, Unit Economics, and Scaling.” The decision needs more than pass@1: it must also consider pass^k and escape rate, the share of defects that pass these gates and are discovered only in production.

G2 originally tracked retries, escaped defects and the champion system. This series adds four conditions: pass^k, constraint violation rate (1 minus constraint pass rate), a mutation score floor, and the oversight budget. The reliability piece brings them into one decision table, with conditions for expanding autonomy or holding it steady.

Measuring capability tells a team whether its tools are improving. Granting autonomy also requires accounting for the consequences of failure and the people who must respond.

We now have a question, evidence requirements and an owner for each gate. The next step is to look at everyday work and ask which familiar practices may be bypassing those decisions.

---

## 9. Eight anti-patterns

A workflow can look clear in a document and still give way to familiar shortcuts in a busy PR queue. The table below describes eight anti-patterns through concrete situations. Use them to examine which signals your own acceptance process treats as sufficient evidence.

| # | Anti-pattern | Where you see it |
|---|---|---|
| 1 | **Green as acceptance** | "CI passed, coverage 90%, ship it" |
| 2 | **TDD ritual** | AGENTS.md says "write the tests first"; a TDD-shaped commit history is taken as reassurance |
| 3 | **Loosened-assertion fix** | Fixing a failing test by turning `assertEqual` into `assertIn`, adding `@skip`, deleting `assertRaises` |
| 4 | **Golden that freezes a bug** | Recording the current output as a snapshot / golden file; the bug is now protected by a test |
| 5 | **Coverage as quality** | Letting agent PRs through on a coverage threshold; exclude patterns and empty assertions can both produce the number |
| 6 | **Closed-loop review** | The same model, the same session reviewing its own PR; or an AI approve counts as passing |
| 7 | **The human who reads the diff** | Seniors read agent diffs line by line, PRs queue up, and the end state is a rubber stamp |
| 8 | **Reporting only pass@1** | Telling leadership "eval pass rate 85%" and expanding autonomy on it |

One figure assigns each of the eight to the gate it belongs to:

```mermaid
---
config:
  theme: base
  themeVariables:
    fontSize: 16px
    primaryColor: "#f8f9fa"
    primaryTextColor: "#1f2933"
    primaryBorderColor: "#6b7280"
    lineColor: "#6b7280"
    secondaryColor: "#f8f9fa"
    tertiaryColor: "#ffffff"
    clusterBkg: "#ffffff"
    clusterBorder: "#9ca3af"
    edgeLabelBackground: "#ffffff"
  flowchart:
    nodeSpacing: 36
    rankSpacing: 44
    padding: 12
    htmlLabels: true
    subGraphTitleMargin:
      top: 8
      bottom: 12
    curve: basis
---
flowchart TB
    classDef own fill:#d4edda,stroke:#2e7d32,color:#1f2933
    classDef buy fill:#fff3cd,stroke:#b8860b,color:#1f2933
    classDef bad fill:#ffe0e0,stroke:#c0392b,color:#1f2933
    classDef human fill:#e3f2fd,stroke:#1565c0,color:#1f2933
    R["Green is not done<br/>eight anti-patterns"]
    subgraph gt["Test gate"]
        direction TB
        t1["TDD ritual"] ~~~ t2["Assertion-loosening fix"] ~~~ t3["Bug-freezing golden"] ~~~ t4["Coverage as quality"]
    end
    subgraph gr["Review gate"]
        direction TB
        r1["Closed-loop review"] ~~~ r2["Human reads the diff"]
    end
    subgraph gl["Reliability gate"]
        direction TB
        l1["Green as acceptance"] ~~~ l2["Report only pass@1"]
    end
    R --> gt
    R --> gr
    R --> gl
    class t1,t2,t3,t4,r1,r2,l1,l2 bad
```

The figure connects each symptom to a part of the workflow the team can improve. Loosened assertions call for checking what the test gate detects; same-session self-review calls for examining review isolation and approval. This does not absolve the agent of problems. It identifies controls the team can improve without relying solely on a model change.

In Taiwanese community discussions, I more often encounter “coverage as quality” and “closed-loop review,” entries 5 and 6. That is an observation, not a statistical finding. Adoption cost may help explain their appeal: coverage is often already available in CI, and an existing seat subscription makes reusing the same agent for review convenient. Understanding those constraints helps in designing an alternative the team can afford.

None of the studies I have read counted the share of closed-loop reviews. The available research records a different kind of pairing. An August 2026 study (AI-to-AI Code Reviews) looked at 248,641 PRs. Cross-product AI-reviews-AI — a reviewer from a different vendor reviewing agent PRs — is only about 1.6% of the total, but between Q1 and Q3 2025 grew more than 100x.

Cross-product pairing can fit the approach allowed in this series, provided generation and review contexts are separated and a human gives the final approval. Different vendors alone do not guarantee independence. Same-model, same-session self-review is a separate rate worth tracking; the paper does not measure it, so teams need their own review records.

Once the symptoms are recognizable, what's left is the decision. In the next section I put myself in the engineering VP's or QA lead's seat and write down what I would and would not approve.

---

## 10. If I were the engineering VP or QA lead, how I would decide

In a budget or workflow meeting, I would start with two questions: what evidence supports approval, and who will own the resulting responsibilities? The following proposals are illustrative examples. On the evidence they provide, I would **not** approve them:

> "Turn the QA team into a prompt team."
> "Use AI review to clear the review backlog; an AI approve is enough to merge."
> "On the strength of an 85% eval pass rate, open write tools to every team in Q4."

The first proposal leaves testing judgment without an owner. The second removes human approval. The third treats a per-attempt pass rate as sufficient evidence for broader autonomy; its write tools are permissions that let an agent change the system. The missing evidence differs, but none explains how the revised process will preserve the judgment people previously supplied.

I **would** approve four things:

1. **Turn review comments into constraint tests first.** Pull 50 review comments from the agent PRs sent back in the last 90 days, classify them, pick out the executable ones, and write the first 10 constraint tests. For a repo with no comment history, derive the first 5 from the last 5 incident postmortems instead. This is the main route, not a fallback, because every "this must never happen again" was a constraint to begin with.
2. **Pilot a mutation gate in one repo**, measuring only agent-changed lines. A team of 200+ engineers, or one with a QA lead who can regularly interpret reports, can assess adoption. Whatever the headcount, someone must own calibration, and the affected test subset must finish within 10 minutes. Start observing against **my suggested value, not an industry standard**, of mutation score ≥ 70%. Collect reports for a month before deciding whether to block. Below-threshold results should send missed behaviors and test gaps back to the agent for repair, with the owner handling exceptions and false positives.
3. **The reviewer agent must be an instance from a different vendor, or at least a different session** (switch to another vendor's model, or at least open a separate conversation to do the review), and an AI approve never counts toward required approvals. Required approvals is GitHub's setting for how many approves a PR needs before it can merge. A merge with only an AI approve counts as unreviewed in section 7's unreviewed-merge rate. GitHub offers two candidate mechanisms. One is CODEOWNERS listing humans only, plus Require review from Code Owners; the other is a required status check that counts human approves. I have not tested either on a production repo, so I will validate first with a GitHub App's approve on my own repo, to see whether either route holds up. A design draft is in the review piece.
4. **Tie approval to a person and the content that person actually reviewed.** The approval artifact should record the approver and a hash of the reviewed content; changes require renewed approval. On high-blast-radius PRs, the task assigner cannot also be the approver. Where Accountability Lives (August 2026) identifies conflicting vendor terms about who may approve an agent’s PR. That is another reason for teams to define responsibilities explicitly rather than assume that an approve button establishes accountability.

**How to think about the verification budget.** An August 2026 study (The reach of a verification tool decides its value) gave me one principle: a verification tool's value is set by its reach. Its sample is 1,116 web apps, 6 models and 8 tool configurations. The clearest illustration is the boot probe, a check that only asks whether the app starts: at about 35% of a full shell's token cost, it removed almost all startup failures; a full shell costs 2.35x.

My proposed order starts with inexpensive checks that catch common errors, then adds more costly verification. Constraints expressible as static analysis can come alongside assertion-change diff; behavioral or performance constraints still require execution. Next come red-then-green and diff-scoped mutation, followed by k repeated runs and step-rubric judges, which use an LLM to assess each step. This is a proposed ordering by cost and risk, not a ranking directly measured by that study.

The budget ratio runs like this: for every $1 the agent spends producing, budget $0.30 to $0.50 to verify it. The denominator is agent tokens plus generation-side CI, the machine cost of what the agent produces; the numerator is verification-side compute, the machine cost of verifying it. **The ratio is my provisional heuristic, to be calibrated by the pilot** — that paper supports the principle, not the ratio. **Human review time is not in this ratio**; it goes through the reliability piece's oversight budget, and the two are reported to the CFO separately.

**Planning for 50 / 200 / 1,000 engineers.** These are three adoption scenarios for extending checks from a few repos across an organization, a separate decision from G2’s autonomy expansion. The 50-person scenario assumes no capacity to maintain mutation reports. Headcount describes the setting; the real prerequisite is having someone who can own the work:

| Scale | How to install the verification layer | Who owns it |
|---|---|---|
| 50 engineers (5–10 repos) | Constraint tests + assertion-change diff only; no mutation — nobody would read the report | Platform, part-time; with no QA lead, the most senior reviewer |
| 200 engineers (30–50 repos) | All four checks in the paved-road CI template; on by default for new repos, brownfield order for old ones; the reviewer fleet defined once in a central config file | QA lead owns the test gate; EMs own the review gate's triage matrix |
| 1,000 engineers | Platform runs the test gate as a product (versions, SLA, dashboard); the reviewer fleet is managed centrally and each BU picks its configuration; each BU computes its own oversight sampling rate | Platform product owner + each BU's QA lead |

As adoption grows, the work changes beyond choosing checks: someone must maintain rules, interpret reports and handle exceptions. The paved road is the workflow the platform provides for teams to use by default. Adding checks there reduces repeated setup across repos, but central installation cannot improve quality if nobody takes responsibility for the results.

**Brownfield: which gate comes first.** Consider a concrete scenario: a 15-year-old legacy monolith, a 40-minute test suite, 30% coverage and no organized review-comment history. The sequence below is for introducing verification in that kind of repo, with each step's prerequisites listed. It does not replace the legibility sequence from section 7 of “Don’t Build Your Own Devin”: characterization tests → logs / traces → architecture rules. If there are no tests, recording existing behavior with characterization tests is step 0. Those records still need to distinguish requirements from current behavior that has not yet been validated:

| Order | Gate | Why this position | Precondition |
|---|---|---|---|
| 1 | **constraint tests** | Needs no existing tests; the raw material starts from team conventions and incident postmortems (item 1 above) | None |
| 2 | **assertion-change diff** | Static diff analysis; no need to execute the 40-minute test suite | None |
| 3 | **red-then-green (bug fix PRs)** | Runs only the affected test subset — whichever module changed, run that module's tests | Can compute the affected subset: test selection or a directory mapping |
| 4 | **diff-scoped mutation** | The most expensive, installed last; report first, block later | Affected subset runs within 10 minutes |

These four checks are just as useful on human-written PRs — loosened assertions, frozen bugs and violated team constraints were not invented by agents. **Even if the agent bet fails, none of these gates is wasted.**

---

## 11. A 90-day action blueprint for the verification layer

To act on those decisions, the team needs a sequence it can sustain. This 90-day blueprint starts with baselines and a limited pilot, then introduces blocking and autonomy decisions gradually. Each phase must leave observable results so the team can judge whether it is ready for the next step.

The starting point first. Once the gates are in, someone will ask whether things actually got better, and answering that requires knowing what things were like before adoption. The main work of month 1 is to establish a baseline: measure performance before any intervention, so there is something to compare the later results with.

There are six metrics to track. “Agentic Engineering: Evals, Unit Economics, and Scaling” introduced two: escape rate, defined in section 8, and review minutes per PR, the average human review time each PR requires. This series adds four to show how tests and acceptance evidence are changing:

- The share of PRs that weaken an existing assertion
- The share of snapshot or golden-file updates with no stated reason (a golden file records the current output as the expected answer; it is not the same thing as the golden set)
- The share of agent-changed lines that existing tests cover
- The share of new or modified test files written by the agent

The last one deserves its own note. What it measures is not quality but whether the opening section's premise holds at all. If most new tests are still human-written, the repo differs from the scenario in section 1, which can inform adoption priorities. Test independence still needs scrutiny; authorship alone does not establish it. The reason from the previous section still stands: these checks are useful on human-written PRs too. Understanding the current state helps set an adoption pace the team can sustain.

Once the baseline is established, the team can plan the pilot and compare results. Months in the table describe a suggested pace; the right-hand column states what each phase must deliver. Reaching a date does not establish readiness. The exit criteria determine whether to proceed.

| Phase | Goal | Exit criteria |
|---|---|---|
| **Month 1** | Measure the six baselines (above); the pilot repo gets the first two gates of the brownfield order — constraint tests derived from team conventions and incidents, and assertion-change diff; mutation reports only, and only on repos whose affected subset runs within 10 minutes; pull and classify 50 review comments (section 10, item 1) | The four new numbers have a baseline; the first two checks run on every PR; if mutation is on, its report appears on the PR without blocking |
| **Month 2** | The first 10 constraint tests derived from review comments enter CI; red-then-green on for bug fix PRs; the reviewer agent swapped for a heterogeneous instance; the PR template gains intent and constraint fields; **AI approve does not count toward required approvals** (validate the mechanism first, section 10, item 3); the agent gets an escalation tool | Validate constraint tests against historical violating patches; track the assertion-weakening share |
| **Month 3** | Golden set run at k = 5 to compute pass^k; mutation moves from report to gate (on the repos where it is on); one autonomy keep-or-expand decision made against the new G2 conditions; three numbers enter the leadership monthly report | The monthly report has pass@1 / pass^k / constraint pass rate columns, **and someone has made one autonomy decision on them with the reasons stated publicly** — expanding or not both count |
| **Months 4–6** | Repeat repo by repo: start with the repos with the highest share of agent PRs, in brownfield order; at 200+ engineers, put all four checks into the paved-road CI template | At least one new repo completes months 1–2 each month; the unreviewed-merge rate enters the monthly report |

Exit conditions are the easiest column to skip. They establish readiness to proceed; a calendar cannot substitute for them. If constraint tests block no PRs for a month, first check whether they cover the intended risks, including replaying past violating patches. No catches can mean compliant changes or a missed check. Do not manufacture a blocking rule merely to prove that the gate is useful.

The table answers what to do each month. The figure below takes only the first three months and lines up each month's exit criteria, to show how they converge on one decision:

```mermaid
---
config:
  theme: base
  themeVariables:
    fontSize: 16px
    primaryColor: "#f8f9fa"
    primaryTextColor: "#1f2933"
    primaryBorderColor: "#6b7280"
    lineColor: "#6b7280"
    secondaryColor: "#f8f9fa"
    tertiaryColor: "#ffffff"
    clusterBkg: "#ffffff"
    clusterBorder: "#9ca3af"
    edgeLabelBackground: "#ffffff"
  flowchart:
    nodeSpacing: 36
    rankSpacing: 44
    padding: 12
    htmlLabels: true
    subGraphTitleMargin:
      top: 8
      bottom: 12
    curve: basis
---
flowchart TB
    classDef own fill:#d4edda,stroke:#2e7d32,color:#1f2933
    classDef buy fill:#fff3cd,stroke:#b8860b,color:#1f2933
    classDef bad fill:#ffe0e0,stroke:#c0392b,color:#1f2933
    classDef human fill:#e3f2fd,stroke:#1565c0,color:#1f2933
    M1["Month 1<br/>measure baselines, pilot repo gets<br/>assertion diff, mutation report"] --> E1["Exit: four numbers have a baseline<br/>mutation report shows up on PRs"]
    M1 --> M2["Month 2<br/>10 constraint tests in CI<br/>other-vendor reviewer, AI not counted"]
    M2 --> E2["Exit: historical violations caught<br/>assertion weakening tracked"]
    M2 --> M3["Month 3<br/>golden set at k = 5 for pass^k<br/>three numbers in the monthly report"]
    M3 --> E3["Exit: three columns in the report<br/>one autonomy call, reasons published"]
    M3 --> G["G2 autonomy decision<br/>expand or hold, both count"]
    class E1,E2,E3 own
    class G buy
```

The sequence should culminate in an evidence-based autonomy decision. The owner needs to explain which results support expansion or which risks justify holding steady. Even if autonomy has not expanded after three months, a clear rationale and a clear account of the missing evidence mean the pilot has answered an important question.

Two reminders to close on, both about the places I think this most easily goes wrong:

1. **Add mutation last; report before blocking.** Observe reports in month 1 and introduce blocking in month 3 based on calibration. The team needs to understand which signals warrant stopping before it can trust the gate. Red-then-green also needs explicit scope: here it applies to changes to existing behavior. A feature PR may fail to run because a class or interface does not yet exist; that is not the behavioral difference being tested and is not a valid red.
2. **Start constraint tests with rules the team already agrees on and can check clearly.** Examples include adding no dependencies or public APIs within a particular task, or following an established log format. State their scope rather than assuming universal agreement. If “no calls across layers” has no shared definition yet, settle that boundary before encoding it in CI. Otherwise one failed check carries both a technical result and an unresolved architecture dispute, leaving the recipient unsure what to do.

Tools and staffing affect the pace; exit criteria protect the decision. When evidence is still missing, allowing the plan to take longer is preferable to expanding autonomy just to meet a date.

---

## 12. Closing

Back to the three scenarios from the opening section. With all three gates installed, how do they end?

The next time the engineer is asked whether the PR was tested, there will be concrete results to discuss together: whether the constraint report passed, which risks the mutation report identified, and what kind of review the triage matrix calls for. "The AI says it is fine" finally comes with evidence that makes a follow-up question possible.

The PR that turned `assertEqual` into `assertIn` gets caught by the assertion-change diff before merge — equality swapped for containment is a drop in strength, and it blocks outright. The tests are still green; the PR still doesn't get through.

In a workflow that previously accepted only a reviewer agent’s approve, enforced human approval and preserved records establish who reviewed which version. That cannot guarantee an incident-free release. It gives the investigation a concrete starting point: what was examined, and which risks went unrecognized.

All three changes begin with the team taking ownership of acceptance evidence: someone validates the tests, checks can be reproduced, and approval can be traced to the reviewed content and the responsible person. Better agents still help, but an organization need not wait for them to stop making mistakes before establishing these practices.

Back to Bach: checking can be automated; testing still requires human judgment. Agents make some checks easier to create and run, which gives teams a more pressing question: which unexamined problems deserve the time we have saved? That is the human effort I want to preserve: suspecting that something may be wrong, then finding a way to investigate it.

One last prediction with a date on it, so that it can be checked and so that it can be wrong. By 2027, a reliability gate will be standard in G2, and "reporting only pass@1" will draw the same frown that "only looking at coverage" does today. That is my judgment, not the conclusion of any trend report.

> **When an agent writes both implementation and tests without independent scrutiny, green means it passed its own exam. Measure the work it delivers, then reserve human time for the decisions that need judgment.**

For me, the design returns to the engineer in the opening section who is asked whether the work has been tested. The next answer should give the engineer and reviewer something they can examine together: evidence, questions and an account of what still deserves investigation. Tools handle repeatable checks so people have room to continue that work.

The four parts begin with the test, review and reliability gates, then connect constraints, tests and judgment through a payment for unsweetened green tea. To start with the PR in front of you, begin with “Reviewing the Tests an Agent Wrote” and ask what the tests that have already turned green actually protect.

---

### The series

The overview and four parts make five articles: the first three parts develop one gate each; Part 4 connects them through a payment walkthrough.

- **Overview (this piece)**
- Part 1 — Reviewing the Tests an Agent Wrote: Loosened Assertions, Frozen Bugs and Mutation Score (coming soon)
- Part 2 — Review Is the Control Point, Not the Bottleneck: Triage, Reviewer Fleets and the Closed-Loop Ban (coming soon)
- Part 3 — The 34% SWE-Gate Found Behind a Green Build: Constraint Tests, pass^k and the Gate for Expanding Autonomy (coming soon)
- Part 4 — A Payment Walkthrough: Buying Unsweetened Green Tea, from Review Constraints to Mutation Score (coming soon)

Related reading, the Agentic Engineering series: [Overview](https://fantasybz.medium.com/dont-build-your-own-devin-org-strategy-and-a-90-day-blueprint-for-agentic-engineering-8187e7ec80f9), [1. Org Design](https://fantasybz.medium.com/agentic-engineering-part-1-who-does-this-platform-plus-federation-in-practice-92343384d987), [2. The Harness Blueprint](https://fantasybz.medium.com/agentic-engineering-part-2-the-harness-blueprint-making-your-system-legible-to-agents-3facc281f633), [3. Evals and Unit Economics](https://fantasybz.medium.com/agentic-engineering-part-3-evals-unit-economics-and-scaling-running-agents-like-a-product-1cb1855a2046).

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
16. Accompanying implementation — [Tea payment, constraint tests and seven selected mutants](https://github.com/fantasybz/medium-articles/tree/main/examples/tea_payment) [section 6; measured teaching example, no real provider]

---

### On how this piece was made

The initial concept and chapter structure are the author's; the prose was drafted in collaboration with AI (Claude), then reviewed and revised section by section by the author before publication. The views and judgments are the author's own, as is responsibility for the content.

---

*Originally published in Chinese: [中文版](https://medium.com/p/582f24223eea). Also on [Medium @fantasybz](https://medium.com/@fantasybz) — if you're designing the verification layer for agent output in your organization, I'd like to hear from you.*
