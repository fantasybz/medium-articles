# Codex review — 2026-11-same-spec-contract/article.en.md (round 2)

> model: gpt-6.1-sol, reasoning: xhigh, 2026-10-27 01:05. Codex's own words, not summarised. Round 2; reviewing the English edition against the final Chinese article and the frozen study.

I’ll read the writing standards first, then compare the English line by line with the Chinese and frozen study files. I’ll keep the review read-only and inside this repository.
<!-- codex ran: /bin/zsh -lc 'cat STYLE.md' -->
<!-- codex ran: /bin/zsh -lc 'cat research/2026-10/style_brief.md' -->
<!-- codex ran: /bin/zsh -lc 'cat research/experiments/same-spec-ten-runs/RESULTS.md research/experiments/same-spec-ten-runs/SPECS.md research/experiments/same-spec-ten-runs/PR -->
<!-- codex ran: /bin/zsh -lc "sed -n '1,180p' 2026-11-same-spec-contract/article.md" -->
<!-- codex ran: /bin/zsh -lc 'wc -l 2026-11-same-spec-contract/article.md 2026-11-same-spec-contract/article.en.md 2026-10-green-payment/article.en.md 2026-11-aaif-agent-memory -->
<!-- codex ran: /bin/zsh -lc 'rg --files research/experiments/same-spec-ten-runs/results/formal-2026-09-25/source/specs research/2026-10/same-spec-ten-runs/manuscripts 2026-11- -->
<!-- codex ran: /bin/zsh -lc 'cat research/experiments/same-spec-ten-runs/RESULTS.md research/experiments/same-spec-ten-runs/SPECS.md' -->
<!-- codex ran: /bin/zsh -lc 'cat research/experiments/same-spec-ten-runs/PROTOCOL.md' -->
<!-- codex ran: /bin/zsh -lc "sed -n '1,125p' 2026-10-green-payment/article.en.md" -->
<!-- codex ran: /bin/zsh -lc 'cat research/experiments/same-spec-ten-runs/results/formal-2026-09-25/source/specs/A0.md research/experiments/same-spec-ten-runs/results/formal-20 -->
<!-- codex ran: /bin/zsh -lc "sed -n '1,125p' 2026-11-aaif-agent-memory/article.en.md" -->
The opening preserves the Chinese’s evidence limits: 40 candidates, 103 checks, no ranking of the briefs, and no added study samples from the teaching material. I’m checking the derivations and later sections for narrower wording shifts, especially the CLI restriction and observation failures.
<!-- codex ran: /bin/zsh -lc "sed -n '175,360p' 2026-11-same-spec-contract/article.md" -->
<!-- codex ran: /bin/zsh -lc "sed -n '360,520p' 2026-11-same-spec-contract/article.md" -->
<!-- codex ran: /bin/zsh -lc "sed -n '520,660p' 2026-11-same-spec-contract/article.md" -->
<!-- codex ran: /bin/zsh -lc 'cat 2026-11-same-spec-contract/publish/en/figures.json' -->
<!-- codex ran: /bin/zsh -lc 'cat research/experiments/same-spec-ten-runs/results/formal-2026-09-25/source/requirements.json' -->
<!-- codex ran: /bin/zsh -lc 'cat research/experiments/same-spec-ten-runs/results/formal-2026-09-25/source/specs/B.md research/experiments/same-spec-ten-runs/results/formal-202 -->
<!-- codex ran: /bin/zsh -lc "python3 -B -c 'from pathlib import Path
import re, json, io, tokenize
root=Path(\".\")
z=(root/\"2026-11-same-spec-contract/article.md\").read_tex -->
<!-- codex ran: /bin/zsh -lc "sed -n '1,100p' research/2026-10/same-spec-ten-runs/manuscripts/STATUS.md" -->
<!-- codex ran: /bin/zsh -lc "sed -n '280,350p' 2026-11-aaif-agent-memory/article.en.md" -->
<!-- codex ran: /bin/zsh -lc 'cat research/2026-10/same-spec-ten-runs/rebuild-2026-09-28/workbench/RESULTS.md research/2026-10/same-spec-ten-runs/rebuild-2026-09-28/workbench/c -->
<!-- codex ran: /bin/zsh -lc "rg -n '"'^# |''^### |69'"\\.15|288|P/Q|P／Q|self-check|change card|brief|packet|acceptance|yardstick' 2026-11-same-spec-overview/article.en.md 2026 -->
<!-- codex ran: /bin/zsh -lc "sed -n '1,110p' research/2026-10/same-spec-ten-runs/rebuild-2026-09-28/workbench/RESULTS.md" -->
<!-- codex ran: /bin/zsh -lc "rg -n '"'^# |''^### Series|''^This series|The Same Spec, Ten Runs'"' 2026-11-same-spec-overview/article.en.md 2026-11-same-spec-spec/article.en.md -->
<!-- codex ran: /bin/zsh -lc "rg -n 'English|英文|contract|Opus|max|review' .context/README.md 2026-11-same-spec-contract/outline.md research/2026-10/same-spec-ten-runs/manuscrip -->
The structural comparison found no missing code blocks or table rows; the executable code and Mermaid config/node IDs are unchanged. One concrete problem is in the AI note: it says the English review and final checks are recorded in STATUS.md, but that file still says the English drafts have not been produced. I’m finishing the wording and terminology pass.
<!-- codex ran: /bin/zsh -lc "python3 -B -c 'from pathlib import Path
import json, re, struct
base=Path(\"research/2026-10/same-spec-ten-runs/rebuild-2026-09-28/workbench\")
fo -->
The remaining edits are mostly English phrasing and a few precision issues: “missed the requirement” better preserves 漏讀, “null date” avoids conflating it with an empty string, and “agent message” is clearer than “spoken message.” I found no missing derivation or closing argument. The publication note’s claim about completed English checks is the main issue.
## Fatal

None found. No paragraph, derivation, code block, table row or closing argument is missing. The six tables retain their dimensions; executable code and Mermaid config/node IDs are unchanged. Reference numbering, URLs and section back-pointers match, allowing for the required English-edition links.

The study’s main evidence limits survive: no ranking or equivalence claim, no teaching fixtures counted as trials, P/Q remains unexecuted, and HIGH generation effort remains separate from MAX manuscript effort.

## Important

1. **AI collaboration note — unsupported English-workflow claim.**

   > “This English edition was written by Claude Code (max effort) from the final Chinese text; the paragraph-by-paragraph polish, second-model review and final checks are recorded in the same STATUS.md.”

   This is an English-only provenance claim. The repository’s [STATUS.md](research/2026-10/same-spec-ten-runs/manuscripts/STATUS.md:45) still lists English drafting and polishing as unfinished and says the attempted requests produced no manuscript. That historical record does not substantiate the current claim.

   **Fix:** Retain the Claude/MAX attribution only if the generation record confirms it. Replace the last clause with:

   > “The linked STATUS.md documents the Chinese manuscript workflow; this English edition’s review and publishing checks have not yet been recorded there.”

   Also change the preceding bullet’s “this round’s writing” to “the Chinese manuscript’s writing” so its scope is explicit.

## Minor

1. **8. “Change the task: a semantic oracle for CSV export”; 11. “Fix the oracle, reject the candidate, or go back to the requirements owner” — preserve 漏讀.**

   Chinese §8:

   > 「從輸出差異本身，看不出模型是漏讀、誤解，還是選錯了 helper；也不能據此證明補一段自查就會改善結果。」

   English:

   > “The output difference by itself cannot show whether the model misread, misunderstood, or chose the wrong helper; nor can it prove that adding a self-check section would improve the result.”

   “Misread” blurs the distinction between missing a requirement and misunderstanding it.

   **Fix:**

   > “The output difference alone cannot tell us whether the model missed the requirement, misunderstood it, or chose the wrong helper; nor can it show that adding a self-check would improve the result.”

   Chinese §11:

   > 「但不要替它補上成因：從輸出差異看不出模型是漏讀、誤解，還是選錯了寫法。」

   English:

   > “When rejecting, record which obligation was violated, but do not supply a cause for it: the output difference cannot show whether the model misread, misunderstood, or chose the wrong way of writing it.”

   **Fix:**

   > “When rejecting a candidate, record the violated obligation without inferring its cause: the output alone cannot tell us whether the model missed the requirement, misunderstood it, or chose the wrong implementation approach.”

2. **2. “The oracle: who judges right from wrong, on what basis, and where it can misjudge” — awkward attribution of agency.**

   > “So this piece prefers to derive expectations independently from the contract, so that every answer can be traced to its basis, and then has a person re-check the derivation.”

   An article cannot “have a person” perform a check.

   **Fix:**

   > “My approach here is to derive expectations independently from the contract, trace each answer to its basis, and then ask someone to check the derivation.”

3. **2. — calque in the EvalPlus transition.**

   > “EvalPlus shows from the other direction that a yardstick's protective power changes the verdict.”

   **Fix:**

   > “EvalPlus shows that the checks’ ability to detect faults can change the verdict.”

   “Protective power” is less precise than the approved English edition’s “fault-detection ability.”

4. **3. “Read the rules first, then derive once: after `false` there is still `after`” — wrong grammatical subject.**

   > “The first line is a nonempty string, so stdout prints `ok` plus a newline, and it counts as a spoken message.”

   The event is an object; its `text` field is the nonempty string. The parser writes to stdout.

   **Fix:**

   > “The first event’s `text` is a nonempty string, so the parser writes `ok` followed by a newline to stdout and counts it as an agent message.”

   Apply the same subject correction to “stdout prints” elsewhere in this derivation.

5. **3. — unnatural case description.**

   > “This problem tells two common ways of writing the code apart.”

   **Fix:**

   > “This case distinguishes two common implementation mistakes.”

6. **3., 5. and 6. — headings retain Chinese syntax.**

   > “Read the rules first, then derive once: after `false` there is still `after`”

   **Fix:** “Read the rules, then derive the result: processing must continue after `false`”

   > “The batch end state is all correct, yet the output before EOF is missing”

   **Fix:** “All final results match, but nothing arrives before EOF”

   > “From one case to more: which results should stay the same, and which must change”

   **Fix:** “Generate related cases: what stays the same, and what must change?”

7. **5. — Mermaid B3 has an ambiguous comparison.**

   > “all channels identical”

   This can mean stdout, stderr and the exit code are identical to one another. The intended comparison is with the reference.

   **Fix the label only:**

   ```text
   Completion + EOF<br/>all three match reference
   ```

   Keep the node ID and configuration unchanged. No clipping is apparent in the existing PNG.

8. **7. “Verify the yardstick first: positive and negative controls, surviving changes, and inconclusive results” — abstract paragraph hand-off.**

   > “The previous section widened ‘which inputs to ask with.’ This section turns back to check ‘whether the judge itself can misjudge’; the two have to be done together for added cases to mean anything.”

   **Fix:**

   > “Section 6 widened the input set. Those additional cases help only if the oracle judges their results correctly, so this section checks the oracle itself.”

9. **9. “The obligation table: handing derivations, gaps and owners to whoever takes over next” — “spoken assumption” is the wrong emphasis.**

   > “If the two of you need to add a spoken assumption before you reach the same answer, return that assumption to the spec owner.”

   The problem is an unstated assumption, whether spoken or written.

   **Fix:**

   > “If reaching the same answer requires an assumption absent from the requirements, return that assumption to the spec owner.”

10. **10. “Understand the yardstick first, then talk about isolation, freezing and grader versions” — cumbersome holdout definition.**

    > “They can continue to serve as regression assets, but saving another copy will not turn them back into a holdout, problems never touched while the method was being designed and kept for the end.”

    **Fix:**

    > “They remain useful regression assets, but copying them cannot make them a holdout again: a set kept untouched during method development and reserved for final evaluation.”

11. **11. — sentence fragment at the denominator recommendation.**

    > “The practice I extend from that classification: a run stopped because its budget ran out can count as ‘not completed’ in the delivery analysis, but it must not be treated as a completed semantic test that failed.”

    **Fix:**

    > “From that classification, I would adopt this practice: count a budget-stopped run as ‘not completed’ in delivery analysis, while keeping it separate from completed semantic checks that failed.”

## Suggested cuts

1. **7. — compress the opening qualification.**

   > “The oracle, once written down as a comparison program, is itself code, and it too can be wrong.”

   **Replace with:**

   > “The code implementing an oracle can be wrong too.”

   This also preserves §2’s distinction between the oracle’s basis and the program implementing it.

2. **8. — remove translation scaffolding.**

   > “Below, csv-transfer's way of judging is organized into a code sketch; it is not the teaching replay's source code, and this article did not execute it.”

   **Replace with:**

   > “The sketch below follows csv-transfer’s comparison method. It is not the replay’s source code and has not been executed.”

3. **AI collaboration note — remove “meta-teaching material.”**

   > “are both meta-teaching material added on 2026-09-28”

   **Replace with:**

   > “are both teaching materials added on 2026-09-28”

   No section-level cuts are justified by English-only padding. Cutting the repeated evidence limits would remove qualifications present in the Chinese.

## Suggested additions

1. **1. “Two green lights, and what each one leaves out” — make the denominator immediate.**

   > “In total, 103 checks.”

   **Replace with:**

   > “Each candidate faced 103 checks: 102 batch cases and one pre-EOF streaming probe.”

   This prevents readers from briefly interpreting 103 as the total across all forty candidates.

## Terms still unclear

1. **2.; 8. “Requirements and decisions,” code comment and self-test discussion — “empty date.”**

   > “when the Overview's hypothetical CSV tool meets an empty date”

   Later:

   > “preserves commas, newlines inside fields, empty dates and duplicate data”

   The Chinese explicitly limits the policy:

   > 「本例只決定 null 日期如何輸出，沒有替缺欄、空字串等其他輸入定義行為」

   **Fix:** Use **“null date”** for the input and **“empty field”** for the output. Reserve “empty string” and “missing column” for the explicitly uncovered inputs. Update the code comment accordingly.

2. **3.; 7. — “spoken message.”**

   > “counts as a spoken message”

   > “was a message spoken”

   This sounds like audio or conversational speech.

   **Fix:** Use **“counts as an agent message”** and **“whether a valid nonempty agent message was seen.”** Preserve the distinction between emitting a command comment and counting an agent message.

3. **11. — “self-check” could mean another automated test.**

   > “P has only the shared requirements and Q adds the self-check on top”

   **Fix:**

   > “P contains only the shared requirements; Q also includes a written self-check asking the implementer to revisit those requirements.”

   Keep the following statement that the comparison has not been run.

<!-- tokens: in 1814443 out 17685 -->
