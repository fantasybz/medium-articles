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

> **TL;DR** — The overview argues that when an agent writes both code and tests, and those tests have not been independently reviewed, green is insufficient for acceptance. This piece develops the test gate. Tests record the agent's understanding of the requirements, so they need review too. Four common risks are weakened assertions, existing bugs recorded as golden outputs, tests that fail to detect faults or exercise the wrong path, and coverage mistaken for quality. Human inspection alone is unreliable: in an experiment with 86 developers, accuracy on incorrect LLM-written assertions was only 49%, without lower confidence. **Assertion-change diff, red-then-green and diff-scoped mutation score** help identify these risks, each with costs and limits. The piece ends with a ten-question checklist and my workshop example of "all tests green, replay never executed." That example made the remaining task clear: beyond test effectiveness, someone must establish whether the implementation answers the original requirement.

> Series: [Overview](https://medium.com/p/c4fc9f3d8581) → **1. Testing (this piece)** → 2. Review (coming soon) → 3. Reliability (coming soon) → 4. Payment Walkthrough (draft ready; unscheduled)

---

## 1. After "the AI said it's fine": the tester's new job

James Bach is the author of the Context-Driven Testing and Rapid Software Testing methodologies. The overview borrowed his language to separate two things that usually get mixed together: checking is comparing an answer against a rule you already know, and testing is a person judging whether the thing is any good.

On that distinction, CI performs checking. An agent saying "all tests passed" is reporting a result that still needs to be checked against execution records. Deciding whether those checks are sufficient for acceptance remains a matter of the human judgment involved in testing.

The overview also put the first number on that line. SWE-Gate is a benchmark that, on patching tasks across a set of Python repos, runs a patch's functional tests separately from the constraints its reviewer stated. Among the patches that passed the functional tests, 34% violated a constraint. A green build does not cover those requirements the reviewer actually cares about.

That is one layer a green build does not cover. This piece is about the layer in front of it: whether the tests themselves are any good. That is the first of the three gates, the test gate. The first three parts develop one gate each: the test gate here, the review gate in the Review piece, and the reliability gate in the Reliability piece. Part 4, “A Payment Walkthrough,” uses one order to carry those decisions into code and tests.

For the three-way split (the overview sorts evidence into three categories: the agent's statements, agent-written tests, and team-owned tests), and the promotion rule for when an agent-written test becomes the team's test, see section 2 of the overview; it isn't repeated here.

First, why tests need review more than code does. Scrum Community in Taiwan reshared a line from Lada Kesseler, short enough to be a slogan, to the effect of "I trust the tests an AI writes even less than the code it writes."

The reason is direct: tests are the agent's acceptance criteria for itself, and the one setting the exam is the one sitting it. When the code is wrong, the tests still get a chance to stop it. If the requirements in the tests are weakened too, the defense that was supposed to catch the error loses its purpose.

There is a second reason tests need review more than code does. Bach says a tester's core skill is rapid learning. In the agent era that has a concrete form: reading the tests an agent left behind tells you faster than reading its code what it understood and what it didn't.

The reason is that tests are the agent's translation of the requirements. The code only tells you what it did; the tests tell you what it thought the requirements were. Where the translation is wrong, the assertions, the fixtures (the data and environment set up before a test runs) and the test names give it away first.

Back to Lada Kesseler's line. It leans toward trusting less; where the question actually caught fire in Taiwan was on DevOps Taiwan, and what burned there was the position leaning the other way. Uncle Bob (Robert C. Martin) is TDD's main popularizer, and he holds that you don't read the agent's code; you look only at the tests and the quality metrics. Someone posted that position, the thread ran long, and someone half-jokingly asked him to list every test that ought to be run.

He did list them ([2026-07-26](https://x.com/unclebobmartin/status/2081332683582427641)): agents write quickly, so spend the saved time on unit, acceptance, property, torture, mutation and QA testing. Property testing checks expected properties using generated inputs; torture testing pushes inputs, load or concurrency beyond normal conditions to find where the system fails. Each has its place. This piece concentrates on mutation because it directly asks whether existing tests can detect deliberately introduced changes in the code.

I want to respond to that discussion by going beyond a list of test types and explaining three checks and their thresholds. The order is: where agent-written tests go wrong, why human eyes don't catch it, mutation as the threshold and the three checks on the diff, why coverage can't be that threshold, an example from my own implementation to draw their boundaries, and the ten-question checklist a tester works from. Before the checks, though, it helps to know what each of them is there to stop.

---

## 2. Where agent-written tests go wrong: four patterns

Agent-written tests can lose their protective value in different ways. This piece groups four useful starting points for inspection: weakened assertions, existing bugs recorded as golden files, tests unable to distinguish faults, and coverage mistaken for quality. This is a starting point for investigation, not an exhaustive taxonomy.

On CI all four look identical, because all four are green. The table names the check for each; how each is built waits for the reference implementation. The mutant the table mentions is a copy of the code deliberately broken; the mutation-testing section covers it:

📌【在此插入表 table-01.png】

Read the third column as possible mechanisms, not claims about an agent's intentions. If feedback rewards only passing tests, fixing the product and weakening the tests may receive the same success signal. The workflow needs to distinguish them, so CI can report changes to test requirements as well as whether the tests passed.

Related risks appear in other taxonomies too. Bojie Li, Pine AI's chief scientist and author of *AI Agents in Depth*, discusses failure attribution in chapter 7: tracing an execution record to where an error began. One category is hacking the verification environment: changing assertions, adding skips, mocking away the behavior under test, or claiming tests passed without an execution record.

The first three all have a place among the four above; the fourth doesn't, because no test ran at all — there was only the claim. He also notes that the taxonomy will continue to grow. This piece uses only the part relevant to testing.

The fourth item doesn't even amount to checking: CI can check that claim by actually running the tests once. What the four patterns have in common is that the tests ran and were green; this one happens before the green build, which is why this piece doesn't list it as a fifth pattern.

There is one more, and it doesn't go in the table, because it isn't the test going wrong. It's the pothole the red-then-green check itself can fall into: **red for the wrong reason**.

LeSS in Action, when teaching A-TDD — acceptance test-driven development, where the acceptance test is written before the implementation — has a discipline: pay attention to the error message, and the error message has to match what you expected. The red in red-then-green takes the same discipline. You want to see the expected assertion fail, not an import error, which is the kind of red that means the test never ran at all.

A harder case appears in the workshop example in section 7. The tests can fail and their assertions are real, but they exercise the wrong path: reading objects in memory when the requirement is to reconstruct state by replaying events. Running these three checks over the existing implementation may not reveal an entirely omitted requirement path. Constraints derived from the requirement are also needed.

Line the four failure patterns up against their checks and you see that although there are four ways to break, there are only two things a human has to guard against: tests being weakened, and tests that miss.

📌【在此插入圖 diagram-01.png】

The four risks each have a starting point for inspection: three checks and a PR-template field recording the origin of golden outputs. Their costs differ, and mutation in particular needs a controlled execution scope.

A machine can detect bad smells in the tests, but it cannot clarify the intent of a requirement for a person. These checks first collect the problems that can be recognized automatically, leaving people time to ask whether the tests really verify the behavior the requirement calls for.

---

## 3. Human eyes aren't enough: 49%

Everything the last section prescribed points at a tool. Nothing points at "a more careful human". There is a reason for that.

An experiment asked 86 developers to judge LLM-generated assertions (Poor and Overconfident Judges, July 2026). Accuracy was 74% for correct assertions and only 49% for incorrect ones. These are proportions of correct judgments, not a claim that only a particular subset of participants could recognize errors.

Confidence was similar in the two conditions. In this experiment, inaccurate judgments did not reliably come with lower confidence. We therefore cannot count on a reviewer's feeling that something is wrong to consistently signal when another check is needed.

The experiment tried one further condition: attach the LLM's own explanation next to the assertion and see whether people judge more accurately. The answer is that attaching explanations didn't help, and low-quality explanations actually hurt.

Scope it first. What this experiment measures is "judging whether an LLM-generated assertion is correct", not "judging an existing assertion the agent loosened". This piece handles the two separately: this section takes the first, and the reference implementation's assertion-change diff takes the second; they point the same way.

Would labeling the code as AI-written improve scrutiny? A separate eye-tracking study observed that reviewers spent longer on code labeled as LLM-generated, without a corresponding increase in scrutiny. In that study, extra time did not bring the expected change.

The studies use different tasks, so their results cannot be combined into one defect-detection rate. Their shared warning is narrower: longer reading time and an AI label do not by themselves establish improved quality.

So "ask a senior to read the tests carefully" is not a complete strategy. Let tools first identify weakened assertions, new tests that do not fail on old code, and surviving mutants. People can then return to the tests and requirements with concrete questions, instead of starting at the first line and guessing where trouble might be. The next section explains mutants.

Lay the four failure patterns out and compare what human eyes and tools can each do, row by row:

📌【在此插入表 table-02.png】

The "human eyes" column has one thing in common all the way down: not one of those cells is about a person not trying hard enough. Some of the signals simply aren't visually salient — a deleted assertion is one red line in a diff, and it looks exactly like the other few hundred red lines. Other problems appear only when the tests actually execute; reading the code carefully cannot reveal them on its own.

---

## 4. Mutation testing: a gate, not a ritual

Mutation testing deliberately changes code, for example by replacing an operator, changing a constant or reversing a condition, then runs the tests. A failing test has caught, or "killed," the mutant. Otherwise the mutant survives. Survival may reveal a test gap, or it may mean the change did not alter observable behavior; it needs interpretation. Mutation score is the share of scored mutants killed by the tests.

What it does to your tests is the same idea chaos engineering applies to production: break the thing yourself once, and see whether the alarm goes off. The only difference is that here what gets broken is the code, and what should go off is the tests.

Mutation as a gate isn't my idea first. Uncle Bob's gate combination is coverage, CRAP score and mutation tests. CRAP score — Change Risk Anti-Patterns — folds complexity and coverage into one number, and a function that is both complex and untested scores highest.

This combination and the reasoning behind it come from one of his posts ([2026-07-30](https://x.com/unclebobmartin/status/2082850576832905657)): TDD is a human discipline, he doesn't expect agents to follow it, and he measures the result instead.

This is the "don't read the agent's code" position from the opening section. The list attached to DevOps Taiwan's retelling of it (unit, Gherkin — the Given/When/Then syntax acceptance tests are written in — mutation and the quality metrics) isn't quite the one in this post, but both lists have mutation, and the conclusion is the same: once it passes, he doesn't read the code.

This piece doesn't go that far. The Review piece will argue that humans still have to review intent and constraint reports, but it agrees that mutation is the core of the test gate.

Mutation testing is not new, but execution cost remains an adoption concern. Generating N mutants means repeatedly running tests against those variants. Test selection can reduce the scope of each run, but it does not remove that cost.

Agents make tests arrive faster and individual manual inspection harder to sustain, increasing the need to assess test effectiveness. One way to control cost is **diff-scoped mutation** over the agent's changes, reducing the mutants generated and executed. Scope restriction did not begin with agents and does not guarantee low cost; the runtime of the affected tests still determines whether it is practical.

Section 10 of the overview said the value of a verification tool is set by its reach. Diff-scoped mutation's reach is exactly the lines the agent just changed.

Its limits need to be clear too. Mutation measures whether tests protect the code that has been written; it cannot detect a requirement that was never implemented at all.

More concretely, it will tell you that flipping this condition made no test go red. It won't tell you that the module is missing an architecture rule, or a business constraint, or that the path the spec asked for doesn't exist at all. The example in section 7 is that last kind.

Back to cost. Most people installing this check are looking at a brownfield: an existing system that has been running for years, with a test suite that is big and slow. The brownfield reality is that on a 40-minute test suite, diff-scoped mutation still has to run the affected tests N times.

So it's the **last** of the four checks to install, and only on repos where the affected subset finishes within 10 minutes. Why that order, section 10 of the overview covers; it isn't repeated here.

**The ritual version versus the gate version.** The question was asked twice this summer. The first time was Thoughtworks' Birgitta Böckeler, who asked "TDD inside the agent loop—theater or actual value?" (reshared by Martin Fowler, [2026-08-11](https://x.com/martinfowler/status/2087173563144912985)).

The second time was Uncle Bob's August 17 experiment (the negative test experiment), which asked the other face of the same question: he had four test disciplines each write the same program, the acceptance tests all passed, and the programs were different ([2026-08-17](https://x.com/unclebobmartin/status/2089449442089025936); the overview covered the design and the results).

These discussions bring me back to one question: a process can have the right shape while its protective value remains unexamined. Telling an agent to run mutation and keep adding tests until it reaches 100% can encourage tests tailored too closely to the mutation operators. Those tests are not necessarily tautologies, but they may still miss requirements that were never implemented.

The gate version starts with CI listing surviving mutants, then distinguishes test gaps from equivalent mutants. Equivalent mutants preserve observable behavior, so tests cannot distinguish them from the original. Exclude confirmed equivalents with a recorded reason, have the agent add tests for the remaining gaps, and reserve human attention for cases requiring judgment. That avoids handing every entire report back to a reviewer.

The threshold is my recommendation, not an industry standard: start with a mutation score of ≥ 70% on agent-changed lines as a pre-merge reference, reporting for a month before blocking PRs that fall short. The number draws on Uncle Bob's practice and my initial estimate. It needs calibration against my own pilot data, rather than being a validated universal threshold. Review can establish specifications and select tests earlier; even an above-threshold score still needs examination of critical risks.

**A payment makes the percentage's limits visible.** The accompanying [runnable example](https://github.com/fantasybz/medium-articles/tree/main/examples/tea_payment) buys a bottle of 無糖純喫綠茶, unsweetened pure green tea, at an illustrative NTD 35. A fake provider records a capture and then raises a timeout. The application only knows that the response was lost, so it must retain `PENDING`. A reviewer preserves the requirement that an unknown outcome must not appear successful and replay must not charge again. That constraint test also protects functional behavior; the terms are not mutually exclusive.

The test calls `Checkout.pay()` twice with the same order and key, checks that the result remains `PENDING` without a payment ID, and verifies there was only one provider call. The full version also covers a timeout before capture, so “unknown” does not become “definitely charged.” Its oracle, the expected result used to judge correctness, comes from the agreed payment requirement, not from asking the implementation to calculate its own answer.

M5 deliberately breaks that branch:

```python
# Original payment code
except TimeoutError:
    receipt = replace(receipt, status="PENDING")

# M5: the intentionally incorrect variant
except TimeoutError:
    receipt = replace(receipt, status="PAID")
```

The experiment keeps seven hand-seeded, executable, non-equivalent mutants, with no exclusions. Two happy-path tests detect 2/7, or 28.6%. Adding the other constraints but omitting the timeout test detects 6/7, or 85.7%, while M5 survives. Restoring that test brings the nine-test suite to 7/7, or 100.0%. Each selection first passes on the original program, then runs against every mutant.

The 70% comparison is illustrative; seven hand-selected mutants cannot directly inherit a threshold for tool-generated mutants on a real diff. Even though 85.7% exceeds 70%, it cannot justify approving this payment change: a critical constraint remains unprotected. The 100% result only describes these seven mutants. It does not verify real providers, concurrency or restarts. The demo uses sequential calls and a fake provider in one process. The unscheduled draft of “Part 4 — A Payment Walkthrough: Buying Unsweetened Green Tea, from Review Constraints to Mutation Score” develops the code, Review selections and denominator in full.

On tooling, the JVM has PIT, JS and TS have Stryker, Python has mutmut. How far each can be confined to the diff varies, so check how your stack does it before you start.

Put this section's two thresholds next to the thresholds for the other two checks and you have the whole table of recommended values for this piece:

📌【在此插入表 table-03.png】

The easiest thing to skip in that table is the first row of the notes column: provide reports for a month before blocking PRs that fall short. The team needs to see the problems in those reports before it can understand why this gate is worth stopping for. Reverse that order, and the first blocked agent PR may prompt someone to remove the whole mechanism. A gate earns credibility through that experience of using it.

---

## 5. Three checks on the diff: a reference implementation

The earlier sections explained the reasoning. This one turns it into checks that CI can execute. Each check addresses a different problem, and each has conditions to confirm before adopting it.

All three are automated checks in CI. Start by establishing the first two, then add the more expensive mutation check.

**Check 1: red-then-green.** This one asks the most basic question there is: would this new test have failed while the bug was still there? If it would, it has earned the right to claim it catches that bug.

The scope comes first. The red-then-green gate proposed here applies to changes to existing behavior: bug fixes and behavior changes. A feature PR may depend on classes or interfaces absent from the base branch, producing a loading failure rather than the intended behavioral difference.

That is why this proposal does not apply red-then-green to every feature PR: excluding incomparable situations keeps red meaningful as a behavioral difference. Use Check 3 to help assess new feature tests, then return to the requirement to confirm that they test the right thing.

**Classification must be independent of the PR author.** If the agent opening a PR can assign its own label, it may classify a fix as a feature and bypass red-then-green. The design should close that route without assuming the agent will inevitably take it.

Classification is part of verification. Protecting its inputs lets the team trust that “this check does not apply” is a supported decision rather than an exemption the author granted itself.

There are three sources for the classification, taken in order. The first is the type field on the issue or ticket, which a human set. The second is the task type from the harness (the layer between the agent and the engineering system, which “The Harness Blueprint” was about). With neither available, judge from the diff: if the PR modified any existing non-test file, treat it as a behavior change and run the check; only PRs that just add files skip it.

The first two sources must be maintained by people or protected harness configuration, so the agent cannot change its own classification. The third is only a conservative fallback when task metadata is absent: it detects changes to existing files, not whether the requirement is complete. A fix that only adds files can still escape it, so classifications need spot checks.

The CI job checks out the tests the PR added onto the base branch and runs them once. The output falls into three classes.

a) The test does not fail. Flag it `test-never-fails`; this is the only class that receives that flag.

(b) The test fails for the expected behavioral difference. For a bug fix, it reproduces the original defect; for a behavior change, it distinguishes the old requirement from the new one. This establishes red only. The same test must also pass after the patch to establish green.

（c） The test fails for an unexpected reason, such as an import error or a missing fixture. Do not label it `test-never-fails`, but do not count it as successful verification either. Record the cause, determine whether the PR needs splitting, the environment needs fixing or the classification needs correcting, then run the check again.

Draw the scope and the three exits as one diagram and you can see it's really a router:

📌【在此插入圖 diagram-02.png】

red-then-green runs only on PRs that change existing behavior. Of these three outcomes, only "the test does not fail" receives the `test-never-fails` flag.

The three outcomes mean different things. No failure calls for investigating the test's ability to distinguish behavior. Expected failure must be followed by a passing run after the patch. Unexpected failure leaves verification unresolved. Keeping "unresolved" separate from "passed" prevents an error-filled report from being mistaken for clearance.

**Check 2: assertion-change diff.** This one handles a quieter risk: the test file is still there, the test name hasn't changed, but the assertion that used to catch the bug has been weakened. CI is still all green, and on the diff it's just a few interleaved red and green lines.

When an existing assertion is modified, don't ask the agent why yet. Grade it into four classes first:

- a) **A step down the strength ladder**: equality → containment → truthy. Block the PR.
- b) **Count or precision relaxed**: call count, tolerance, timeout. Block the PR.
- c) **Removal**: assertion deleted, `assertRaises` deleted. Always block the PR.
- d) **Disabling**: `skip`, `xfail`, `.only`, test file deleted. Always block the PR.

A hypothetical, to make that concrete. A PR says it fixed a serialization bug, and one line in its diff turns `toEqual` into `toMatchObject`. Functionally the PR may well have fixed the bug, but that one line means the test will never check the other fields again. That is class a), so the PR is blocked.

Any other change to an existing assertion gets `needs-human-test-review`. For tests already promoted to team ownership (the third category in section 2 of the overview), any weakening blocks outright.

Do not treat changes to both code and tests in one PR as evidence of weakening on their own. Legitimate behavior changes may require both. Identifying the risk still requires comparing what the assertions checked before and after the change.

**Check 3: diff-scoped mutation.** This one isn't a health check on the whole repo. It asks one thing: are the lines the agent just changed actually held by tests?

Generate mutants for files the agent changed, then report and score the results on changed lines. Mutants that remain alive are called survivors. Many tools work at file granularity. If you filter to lines yourself, apply the same filter to killed and surviving mutants so the numerator and denominator cover the same scope; filtering survivors alone is insufficient.

A feature PR's new tests are outside red-then-green's scope. This check assesses whether they protect the newly written code.

The same PR starts three jobs, whose results are collected into one report:

📌【在此插入圖 diagram-03.png】

The three jobs can run in parallel and feed one report, with classification deciding whether red-then-green runs. This excerpt illustrates the initial reporting phase: PRs are not blocked during the first month. It does not yet enforce the gates described above.

Keeping the first month in reporting mode gives the people receiving the results time to understand them. Each warning needs examination: does it identify a test gap, or an incomplete classification or environment setup? Once the owner can explain those differences, reliable checks can become blocking conditions. The team then knows why a PR stopped and what needs fixing.

The instructions in AGENTS.md (the project instruction file an agent reads before it starts work), set against the measurements on CI, form an "instruction vs. measurement" Before / After. Uncle Bob's version is that you can't tell an agent to write clean code; you can only measure whether it did and then tell it to fix it ([2026-07-29](https://x.com/unclebobmartin/status/2082497764223492161)).

Before illustrates an AGENTS.md with instructions that have not been connected to checks:

```text
# Before: instructions (no CI check has been added)
Always use TDD. Do not modify existing tests.
```

Both of those sentences are true, and both of them are instructions. Once the agent has read them, CI still has no new executable check.

After shows the relationship between three check jobs, a classification job and a reporting job. This is a design excerpt, not a workflow ready to paste into GitHub Actions: runner configuration, dependency installation, artifact transfer between jobs and permissions still need implementation. Every diff uses the base branch.

The five scripts under `tools/` are the part you write yourself — one for `classify`, one per check, one that posts the report — and their behavior is the definition of the three checks above:

```yaml
# test-gate.yml (design excerpt, not a runnable workflow)
# First month: reports only; runners, setup and cross-job artifacts omitted
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
  assertion-diff:        # all PRs: analyze the diff without executing product tests
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
      # Compare base and PR in isolation: record the reason for red, then verify green on the PR
      - run: python tools/red_then_green.py --base origin/${{ github.base_ref }} --head HEAD --report red_green.json
  mutation-diff:         # only on repos whose affected subset runs in < 10 minutes
    steps:
      - uses: actions/checkout@v4
        with: { fetch-depth: 0 }
      # Filter killed and surviving mutants to the same changed lines before scoring
      - run: python tools/mutation_diff.py --base origin/${{ github.base_ref }} --report survivors.json
  report:
    needs: [assertion-diff, red-then-green, mutation-diff]
    if: ${{ always() }}  # the report must still go out when red-then-green is skipped
    steps:
      - run: python tools/post_pr_comment.py weakened.json red_green.json survivors.json
```

In the implementation, `red_then_green.py` must retain output and exit codes from both runs, distinguishing expected failure, unexpected failure and failure after the patch. A red classification alone is insufficient. The reporting job must retrieve artifacts from each job and distinguish skipped, failed and completed checks; a missing file is not a pass.

Two decisions in the configuration matter. Because `red-then-green` reads `classify` through an `if`, classification must use protected inputs rather than merely repeat the author’s label. And `report` uses `if: always()` so skipped or failed checks still leave a report. A reader should be able to distinguish “not applicable,” “incomplete” and “passed” without guessing what a missing result means.

Even with those states made explicit, YAML cannot tell us whether the verifier covers everything it claims to check. At AGNTCon Japan in Tokyo in September 2026, the agent conference organized by the Agentic AI Foundation under the Linux Foundation, two SREs from Quartic.ai described just such a gap in their work on agent-driven production Kubernetes upgrades.

Kubernetes only moves one minor version at a time, and each version is one hop. They told the room themselves how their first version missed: the verifier checked only the first node after each hop, so the control plane reached 1.31, the worker nodes stayed on 1.30, and the hop was still marked successful.

The fix was to enumerate every node by role and refuse to start the next hop until all of them matched the version. They folded the lesson into one sentence: "A cluster upgrade succeeds only when the whole cluster has crossed the version boundary."

Checking only some nodes yields a result that represents only those nodes. Whether the whole cluster has completed the upgrade remains unverified.

Returning to this design, two places deserve the same scrutiny. If `mutation_diff` filters file-level results down to lines, verify that it does not omit mutants that belong in the score. When task information is missing, `classify` infers a behavior change from modifications to existing non-test files; that inference cannot establish requirement completeness. Reports need to state those boundaries so “diff” and “classification” do not promise more than the checks deliver.

Quartic.ai's demo ran on a kind cluster (Kubernetes simulated on a local machine); what that lesson cost in production, the slides don't say.

When calibrating a report, I would check execution success separately from inspection completeness. One asks whether the job finished normally; the other compares the intended scope with what was actually inspected. Quartic.ai’s example makes the distance between those questions concrete.

**The agent-side counterpart.** The three checks inspect output in CI. If an agent believes an existing test is wrong, what can the workflow offer beyond repeated attempts or changing the assertion?

An August 2026 study on escalation channels added another route: a structured tool for reporting a broken test, so agents could present evidence of a suspected test defect instead of changing the assertion. It can complement CI enforcement. Here reward hacking means distorting verification to obtain a passing signal. An odds ratio compares the odds of that behavior between groups and must be read with the comparison direction and study setup. Frontier models are the leading models at the time of the study.

Across 8 frontier models, reward hacking fell from 23.6% to 5.3%; the paper separately reports an odds ratio of 9.2. The behavior disappeared from the tested samples for 6 models. Of escalations, 98.7% involved no hacking, while defect-detection coverage increased by 10.1 percentage points.

The last two figures make the approach worth trying: in the tested setting, most reports involved no hacking, and more defects were identified. It does not guarantee future honesty. It gives the agent a usable route for raising a problem that can be checked. Introducing it has two parts.

**Step one: register the tool in the harness.** Its call format is:

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

`reason` explains the suspected problem in the test; `evidence` supplies something reproducible. Together they let the recipient check the claim, request more information or reject the proposed change. Filled fields are not proof: someone still needs to assess their contents.

**Step two: tell the agent in AGENTS.md that the road exists.** AGENTS.md gets one added line: "If you believe a test is wrong, call `report_broken_test`; do not change the assertion." Registration also needs instructions about when to use the tool, what evidence to supply and who handles the report afterward.

This makes the environmental change concrete: restrict unilateral assertion changes while providing a channel for objections. The team then needs to confirm that reports are handled, not merely that the tool was called.

One practical addition to the PR template is to ask where a snapshot or golden file’s expected values came from. Were they derived from the spec, taken from production output, or simply recorded from the current implementation? Naming the source tells the reviewer what evidence to examine next.

Recording current behavior has a purpose, such as establishing characterization tests for legacy code. It must not become the correct answer without scrutiny, and production output may contain defects too. Separating observed behavior from required behavior keeps a convenient golden file from becoming evidence in defense of a bug.

---

## 6. Coverage is an assertion that can be edited away

Even as these reports become available, a team may still reach first for the familiar coverage percentage. To judge whether it supports the current PR, start by asking what it measures: the entire repo, or the code that actually changed?

One study (Test Coverage of Agentic PRs) measured 4,882 agent PRs, and the question it asked is a narrow one: do the repo's existing tests run through the executable lines the agent changed? In Java the answer is only 61.5%, and in Python only 27.0%.

The denominator is the executable lines changed by agents in the study sample, not all Python repos and not total repository coverage. The finding warns that newly changed regions may lack protection from existing tests even when overall coverage looks respectable.

To assess the PR in front of you, inspect coverage over its changes as well. Keep the overall figure, but do not let it answer questions about a change it may barely reflect.

Scope is only part of the problem. Both the coverage configuration and the tests themselves can change, so a higher percentage need not mean that more behavior is protected.

Adding a file to an exclude pattern removes its lines from the denominator. Calling code without assertions can execute more lines without checking the result. Moving difficult logic into an excluded file also changes what the percentage represents. Each change needs review together with its rationale.

The person making such a change may be short of time or struggling with tightly coupled legacy code. Understanding that difficulty helps the team decide how to improve the tests. It still cannot count an increase caused by a changed measurement scope as an improvement in test quality.

This does not require an immediate rebuild of the whole coverage system. For agent PRs, start with three additions to the existing review process:

First, show coverage of agent-changed lines separately so the reviewer can see the scope of testing for this change. Continue tracking total coverage, but do not use it as a substitute.

Second, interpret coverage together with mutation score. Executing a line does not mean an assertion protects its behavior; mutation adds that check.

Third, have a human review exclude-pattern changes, including the reason for exclusion, the scope no longer measured and any checks that compensate. The aim is to protect the meaning of the measurement, not merely its configuration file.

**Coverage shows where tests executed; mutation checks whether they detect deliberate changes to that code.** Together they still share a limit: when required behavior was never implemented, the numbers may remain reassuring. The workshop experience below made that gap concrete for me.

---

## 7. A first-hand example: all tests green, replay never executed

This August, at the pattern-language workshop run by Teddy Chen (author of the Taiwanese software blog 搞笑談軟工), I implemented the same requirement using two approaches, each in its own git worktree (a separate working directory under the same repo): Approach A gave the agent a bare prompt and nothing else; Approach B added the workflow the workshop supplied. The requirement itself was small: a Product aggregate (an aggregate, in domain-driven design, is a group of objects that has to stay consistent as a unit) plus a CreateProduct use case.

Below I'll stay with Approach A, because that's where the problem worth talking about is. Judged only by the delivery checklist, Approach A looked reassuring: 25 files, zero compiler warnings, 5 tests all green, clean layering, complete Javadoc.

The problem was the path the tests took. The spec asked for event sourcing: the aggregate doesn't store its state directly. It stores only the events that happened, and the state is replayed back from them one at a time when it's needed.

Approach A's Product wasn't event sourcing at all. It didn't extend `EventSourcedAggregate`, and the tests called `getDomainEvents()` to read events straight from the in-memory aggregate, never going through the replay path.

My note at the time: A's 10/16 (10 of the 16 items on the workshop's compliance checklist) wasn't "nearly there"; it was "hasn't blown up yet at a toy scale with a single InMemory use case".

There was another gap unrelated to replay: the tests lacked `@DirtiesContext`. Spring uses that annotation to remove a contaminated test context from the cache so later tests can rebuild it. If tests alter shared state without appropriate reset or isolation, they can interfere with one another. Retrying until green does not resolve that issue, which is why section 8 asks how flaky tests are handled.

This example illustrates a green build that has not met acceptance requirements, with tests following a different path from the spec. But the evidence here is one implementation from Approach A: N equals 1, and the measurement is compliance. Understanding variation across repeated attempts on the same spec requires a separate experiment; this result cannot establish it.

Looking back at this example, what I want to understand is where each check helps and where it stops. Spelling out their capabilities and limits makes it possible to see what evidence is still missing beyond the green build:

- **red-then-green doesn't apply**: this is a feature PR, and the new tests would go red against the old code because the class doesn't exist.
- **mutation cannot directly verify the missing replay path**: without that path in the code, there is no corresponding code from which to generate mutants.
- **Closing the gap starts with the requirement**: a person reviews intent, identifies the missing behavior, and turns the repeatable requirement into a constraint test.

Approach A’s mutation score was not measured here, so a possibly high score is not a finding. The point is narrower: even if tests detect mutations in the existing in-memory aggregate, that does not establish that replay was implemented. Mutation evaluates the code supplied to it.

The constraint test would read like this: the aggregate must extend `EventSourcedAggregate`, or at least one test must construct the aggregate via rehydrate. Rehydrate is the act of rebuilding the aggregate from its events, which is the path the spec actually wanted. It's the "architecture rule" kind that section 2 of the Reliability piece describes.

A human reviewing intent can start with one question: "is this event sourcing?"

This example did not run the test gate proposed here or compare the effects of all three gates. What it clearly shows is that all existing tests passed without verifying the required path. Closing that gap starts with a person identifying the difference between requirement and implementation, then turning the repeatable part into constraint tests.

Draw the path the spec wanted and the path the tests took in the same diagram:

📌【在此插入圖 diagram-04.png】

Placed side by side, the paths explain why 5 green tests and an unexecuted replay path can coexist: the tests completed the checks they contained, but those checks did not cover the required behavior.

The dashed line marks that gap. A review that follows only the existing implementation and tests can keep confirming details along the same path without asking where the other path required by the spec went. That is a question I want the acceptance process to preserve.

Once the missing requirement is recognized, parts of it can become new checks. The person’s role is not to repeat every tool’s work forever, but to identify requirements the current checks have not yet expressed.

Thanks to Teddy's workshop, a gap that is easy to leave as an abstract idea became an implementation experience I can return to and examine.

---

## 8. The tester's role: from box-ticker to test-suite reviewer

The workshop example gives the following checklist a purpose: helping testers find questions worth pursuing in the reports, then return to the requirements. It provides a reading order, not a substitute for checking that tests and implementation agree. Some questions still require opening both and reading closely.

Ten questions for reviewing a test suite an agent wrote:

📌【在此插入表 table-04.png】

Tools can supply initial evidence for the first eight questions; the last two need more direct judgment about requirements. Keep the final question in particular: which behavior loses protection if this test is removed? No clear answer may indicate an ineffective test, or simply overlapping coverage. Investigate its purpose before declaring that it can never fail.

At the test gate, the tester examines how the suite interprets requirements as well as whether it finished running. Reports can organize assertion changes, surviving mutants and unverified areas. The tester uses that evidence to decide where tests need improving, which requirements need clarification and which questions deserve exploratory testing.

Lisa Crispin and Tip House’s *Testing Extreme Programming* says everyone is a tester. My reading here is that anyone merging an agent PR also has responsibility for its acceptance evidence. Tools can collect results, but the agent that produced the tests cannot be left to decide on its own why they are sufficient.

---

## 9. Closing

Go back to Approach A and its green build at the workshop. For me, what makes that implementation worth keeping is precisely how free of problems it appeared. Not one of A's tests was fake. Every one of them really ran and really asserted; they just all went around the path the spec asked for. That green build didn't lie. It had simply never promised to cover what you assumed it covered.

The three checks in this piece do one thing only: take the parts of what green never promised that machines can measure or check, and present them item by item in a report. assertion-change diff checks for weakened assertions, red-then-green verifies whether new tests distinguish behavior before and after the fix, and diff-scoped mutation checks whether tests detect mutations in the changed code. Those checks may not reveal the requirement path missing from approach A. That also needs a requirement-derived constraint test and human review of intent. All three are better checks, not acceptance.

> **An agent's tests are its acceptance criteria for itself; reviewing its tests is reviewing what it believes "correct" means.**

Reviewing the test suite this way gives the team firmer ground for the next question: who still needs to examine the PR, what should they read, and who gives final approval? “Review Is the Control Point, Not the Bottleneck” develops those arrangements. For the work in front of us, we can start with an already-green suite and ask: does it verify what we originally set out to build?

---

### The series

- [Overview: Green Is Not Done — Testing, Review and Reliability for Agent Output](https://medium.com/p/c4fc9f3d8581)
- **Part 1 — Testing (this piece)**
- Part 2 — Review: Review Is the Control Point, Not the Bottleneck — Triage, Reviewer Fleets and the Closed-Loop Ban (coming soon)
- Part 3 — Reliability: The 34% SWE-Gate Found Behind a Green Build — Constraint Tests, pass^k and the Gate for Expanding Autonomy (coming soon)
- Part 4 — A Payment Walkthrough: Buying Unsweetened Green Tea, from Review Constraints to Mutation Score (draft ready; unscheduled)

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
10. Related reading, the Agentic Engineering series: [Part 2, The Harness Blueprint](https://fantasybz.medium.com/agentic-engineering-part-2-the-harness-blueprint-making-your-system-legible-to-agents-3facc281f633), section 5 (flaky quarantine)
11. Bojie Li, *AI Agents in Depth: Design Principles and Engineering Practice* v2.0 — [Chapter 7, Evaluating Agents](https://bojieli.github.io/ai-agent-book/book-en/chapter7/) (2026-09-06; §7.5.2, the coding-agent failure-attribution table). Section 2.
12. Quartic.ai — [Letting an Agent Upgrade Production Kubernetes — Without Getting Paged at 3 AM](https://sched.co/2QlD9) (AGNTCon + MCPCon Japan 2026, 2026-09-10; [slides](https://hosted-files.sched.co/agntconmcpconjapan26/d9/AGNTCon-MCPCon-Japan-2026_Abhijeet_Sanskar_final.pdf#page=29), slide 29). Section 5.
13. Spring Framework documentation — [@DirtiesContext](https://docs.spring.io/spring-framework/reference/testing/annotations/integration-spring/annotation-dirtiescontext.html), explaining context invalidation, removal and rebuilding (section 7).
14. Accompanying implementation — [Tea payment, constraint tests and seven selected mutants](https://github.com/fantasybz/medium-articles/tree/main/examples/tea_payment) [section 4; measured teaching example, no real provider]

---

### On how this piece was made

The initial concept and chapter structure are the author's; the prose was drafted in collaboration with AI (Claude), then reviewed and revised section by section by the author before publication. The views and judgments are the author's own, as is responsibility for the content.

---

*Originally published in Chinese: [中文版](https://medium.com/p/b01055139451). Also on [Medium @fantasybz](https://medium.com/@fantasybz) — if you're installing your team's first test gate, I'd like to hear from you.*
