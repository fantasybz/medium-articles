# Codex review — 2026-11-same-spec-contract/article.en.md (round 1)

> model: gpt-6.1-sol, reasoning: xhigh, 2026-10-26 20:54. Codex's own words, not summarised. Round 1; reviewing the English edition against the final Chinese article and the frozen study.

I’ll read the two style guides first, then compare the English against the Chinese and frozen study records. I’ll stay inside the repository and make no changes.
<!-- codex ran: /bin/zsh -lc 'cat STYLE.md' -->
<!-- codex ran: /bin/zsh -lc 'cat research/2026-10/style_brief.md' -->
<!-- codex ran: /bin/zsh -lc 'cat research/experiments/same-spec-ten-runs/RESULTS.md research/experiments/same-spec-ten-runs/SPECS.md research/experiments/same-spec-ten-runs/PR -->
<!-- codex ran: /bin/zsh -lc 'wc -l 2026-11-same-spec-contract/article.md 2026-11-same-spec-contract/article.en.md 2026-10-green-payment/article.en.md 2026-11-aaif-agent-memory -->
<!-- codex ran: /bin/zsh -lc "sed -n '1,220p' 2026-11-same-spec-contract/article.md" -->
<!-- codex ran: /bin/zsh -lc 'cat research/experiments/same-spec-ten-runs/RESULTS.md' -->
<!-- codex ran: /bin/zsh -lc "sed -n '210,430p' 2026-11-same-spec-contract/article.md" -->
I’m checking fidelity and evidence scope separately. The opening preserves the study’s main limits; the detailed pass is now checking rule wording, replay claims, and the English collaboration note.
<!-- codex ran: /bin/zsh -lc 'cat research/experiments/same-spec-ten-runs/results/formal-2026-09-25/source/specs/A0.md research/experiments/same-spec-ten-runs/results/formal-20 -->
<!-- codex ran: /bin/zsh -lc "sed -n '170,212p' 2026-11-same-spec-contract/article.md; sed -n '430,637p' 2026-11-same-spec-contract/article.md" -->
<!-- codex ran: /bin/zsh -lc "sed -n '1,100p' 2026-10-green-payment/article.en.md; sed -n '1,100p' 2026-11-aaif-agent-memory/article.en.md; tail -n 65 2026-11-aaif-agent-memory -->
<!-- codex ran: /bin/zsh -lc "sed -n '525,637p' 2026-11-same-spec-contract/article.md" -->
<!-- codex ran: /bin/zsh -lc 'cat research/experiments/same-spec-ten-runs/results/formal-2026-09-25/source/specs/A0.md research/experiments/same-spec-ten-runs/results/formal-20 -->
<!-- codex ran: /bin/zsh -lc 'cat research/2026-10/same-spec-ten-runs/manuscripts/STATUS.md' -->
<!-- codex ran: /bin/zsh -lc 'cat research/experiments/same-spec-ten-runs/results/formal-2026-09-25/source/requirements.json; tail -n 60 research/experiments/same-spec-ten-runs -->
<!-- codex ran: /bin/zsh -lc "sed -n '1,80p' 2026-10-green-payment/article.en.md; sed -n '415,452p' 2026-10-green-payment/article.en.md" -->
<!-- codex ran: /bin/zsh -lc "sed -n '1,38p' 2026-11-aaif-agent-memory/article.en.md; sed -n '120,149p' 2026-11-aaif-agent-memory/article.en.md" -->
<!-- codex ran: /bin/zsh -lc "rg -n '"'^#|Clopper|69'"\\.15|288|P.?Q|brief|change card|packet|oracle|self-check|yardstick' 2026-11-same-spec-overview/article.en.md 2026-11-same -->
<!-- codex ran: /bin/zsh -lc 'cat research/2026-10/same-spec-ten-runs/rebuild-2026-09-28/workbench/RESULTS.md; cat research/2026-10/same-spec-ten-runs/rebuild-2026-09-28/workbe -->
I found a meaning reversal in section 2: “part of what must be accepted” turns required rejection tests into a suggestion to accept invalid inputs. The AI note also claims English review records exist in STATUS.md, but that file still says the English drafts have not been produced. I’m checking the remaining text and structural details.
<!-- codex ran: /bin/zsh -lc "python3 -B -c 'from pathlib import Path
import re, ast
root=Path('\\''2026-11-same-spec-contract'\\'')
zh=(root/'\\''article.md'\\'').read_text(); -->
<!-- codex ran: /bin/zsh -lc "python3 -B -c 'from pathlib import Path
import re, ast
root=Path('\\''2026-11-same-spec-contract'\\'')
zh=(root/'\\''article.md'\\'').read_text(); -->
<!-- codex ran: /bin/zsh -lc "rg --files research/2026-10/same-spec-ten-runs 2026-11-same-spec-contract -g '*en*' -g '*review*' -g '*quality*' -g '*STATUS*' -g '"'!agents/**'"' -->
<!-- codex ran: /bin/zsh -lc "rg --files research/2026-10/same-spec-ten-runs/english-2026-10-26; sed -n '1,36p' 2026-11-aaif-agent-memory/article.en.md" -->
<!-- codex ran: /bin/zsh -lc "python3 -B -c 'from pathlib import Path
import re
zh=Path('\\''2026-11-same-spec-contract/article.md'\\'').read_text()
en=Path('\\''2026-11-same-s -->
<!-- codex ran: /bin/zsh -lc "rg --files 2026-11-same-spec-contract -g '"'!agents/**'"' -g '"'!**/agents/**'"' -g '"'!.claude/**'"' -g '"'!**/.claude/**'"'; rg -n 'stream|obser -->
<!-- codex ran: /bin/zsh -lc "cat 2026-11-same-spec-contract/publish/en/figures.json; sed -n '220,278p' research/2026-10/same-spec-ten-runs/rebuild-2026-09-28/workbench/workben -->
The code and structure checks found no omitted blocks: all 16 fenced blocks retain their executable content, all six tables keep the Chinese rows and columns, and the Mermaid configuration and node IDs are unchanged. The remaining issues are wording, a table entry that conflicts with R01’s entry-point requirement, and English phrases that leave the actor or action unclear.
<!-- codex ran: /bin/zsh -lc "python3 -B -c 'from pathlib import Path
import re
for d in ['\\''2026-11-same-spec-overview'\\'','\\''2026-11-same-spec-spec'\\'','\\''2026-11-sam -->
<!-- codex ran: /bin/zsh -lc "python3 -B -c 'from pathlib import Path
import re
zh=Path('\\''2026-11-same-spec-contract/article.md'\\'').read_text().split('\\''### References\\ -->
<!-- codex ran: /bin/zsh -lc "sed -n '142,176p' 2026-11-same-spec-contract/article.md; sed -n '509,528p' 2026-11-same-spec-contract/article.md; rg -n 'part of what must be acce -->
The reference numbering, URLs, and section back-pointers match the Chinese, and the older-series links use the required English post IDs. I found no blurred claims about the unrun P/Q comparison or the teaching replays. I’m finishing the report, separating mistranslations from ambiguities already present in the Chinese.
## Fatal

None identified. No section, table row, code block, reference, or closing argument is missing. All 16 fenced blocks retain their executable content; the six tables preserve their dimensions; Mermaid IDs and configuration are unchanged. References 1–13 preserve their URLs and section back-pointers. The earlier-series links use the required English post IDs.

## Important

1. **2. The oracle: who judges right from wrong, on what basis, and where it can misjudge — “accepted” reverses the requirement.**

   Chinese: “放到 parser 上，`false`、`0` 與陣列這些看起來「不合法」的 `text`，正好落在契約指定的拒絕路徑上，屬於要驗收的內容。”

   English: “Applied to the parser, `text` values that look ‘invalid,’ such as `false`, `0` and arrays, fall exactly on the rejection path the contract specifies, and so are part of what must be accepted.”

   The Chinese requires testing their rejection. The English suggests accepting them.

   **Fix:** “For this parser, apparently ‘invalid’ `text` values such as `false`, `0` and arrays belong to the rejection path specified by the contract. Acceptance testing must therefore verify their rejection.”

2. **3. Read the rules first, then derive once: after `false` there is still `after` — specify which output is absent.**

   Chinese: “依 R03，stderr 留下一則 `line 1` 的診斷；這一行不輸出、不算發言，程式繼續讀下一行。”

   English: “Under R03, stderr gets one `line 1` diagnostic; this line produces no output and no spoken message, and the program continues with the next line.”

   “No output” contradicts the diagnostic immediately preceding it. The Chinese leaves stdout implicit; English needs the object stated.

   **Fix:** “Under R03, the parser writes one `line 1` diagnostic to stderr. The event contributes no stdout and does not count as a spoken agent message; processing continues with the next line.”

3. **4. Watching only one channel: which kind of error gets through — distinguish checking for success from comparing an expected exit code.**

   Chinese: “回到開場，seed 的 `123` bug 能同時通過「只看 exit」與「只看 stdout 有沒有內容」兩種檢查，也是這個緣故。”

   English: “Back at the opening, this is also why the seed’s `123` bug could pass both ‘look only at exit’ and ‘look only at whether stdout has content.’”

   This ambiguity is already in the Chinese. Comparing the actual exit against the contract-derived **6** catches this bug. Merely treating **0** as success misses it. The preceding table depends on that distinction.

   **Fix:** “The seed’s `123` bug passed checks that merely looked for exit 0 or any stdout content. Comparing its exit code with the contract-derived 6 would have caught it.”

4. **9. The obligation table: handing derivations, gaps and owners to the next person who takes over — the implementation freedom is overstated.**

   Chinese table cell: “不限函式名稱與程式結構”

   English: “Function names and program structure unrestricted”

   This is inherited from the Chinese, rather than introduced by translation. Nevertheless, frozen R01 requires retaining the CLI/main entrypoint. The grader’s incomplete inspection of that requirement does not remove it.

   **Fix the cell:** “Internal helper names and structure unrestricted; retain the existing CLI/main entrypoint.”

   This keeps the table’s rows and columns intact while separating implementation freedom from an unchecked obligation.

5. **AI collaboration note — the English production claim is unsupported by its linked record.**

   English: “This English edition was written by Claude Code (max effort) from the final Chinese text; the paragraph-by-paragraph polish, second-model review and final checks are recorded in the same STATUS.md.”

   The Chinese says: “本輪寫作、逐段修訂、語言與發布包檢查紀錄見 STATUS.md。”

   The English extends that record claim to this edition. However, [STATUS.md](research/2026-10/same-spec-ten-runs/manuscripts/STATUS.md:45) still says the English requests produced no manuscripts because of the weekly limit. That makes the linked disclosure inaccurate as it stands. It does **not** establish that Claude did not write this draft.

   **Immediately supportable replacement:** “This English edition translates the final Chinese manuscript.”

   Restore the writer/model/effort attribution and completed-review claims only with the corresponding English production record. Update the linked status before publication.

## Minor

1. **1. Two green lights, and what each one leaves out — unnatural requirement wording.**

   Quote: “The program did return 0, but it failed to hold one key requirement: a number is not a legitimate message.”

   **Fix:** “The program returned 0 while violating a key requirement: a number is not valid message text.”

   Also change “a `text` which is neither a string nor null” to “a `text` value that is neither a string nor null.”

2. **2. The oracle: who judges right from wrong, on what basis, and where it can misjudge — the checking explanation sounds translated.**

   Quote: “The Overview of Green Is Not Done borrowed James Bach’s distinction and treated checking as a process that compares written propositions against answers, one that can be handed to a machine.”

   “Compares written propositions against answers” leaves the reader reconstructing the action.

   **Fix:** “The Green Is Not Done overview borrowed James Bach’s distinction: checking uses explicit propositions to assess results and can be delegated to a machine.”

3. **2. The oracle: who judges right from wrong, on what basis, and where it can misjudge — replace “protective power.”**

   Quote: “The same programs, given to acceptance checks with different protective power, led to different conclusions.”

   “Protective power” is a calque of 保護力. The approved payment article uses the clearer “fault-detection ability.”

   **Fix:** “When the test suite detected more faults, the same programs received different verdicts.”

   Use “ability to detect faults” where this meaning recurs.

4. **3. Read the rules first, then derive once: after `false` there is still `after` — complete the actors and actions.**

   Quote: “A ‘physical line number’ counts the actual input line by line, with a blank line taking a number too…”

   **Fix:** “The parser counts physical input lines from 1, including blank lines…”

   Quote: “Only exits 3, 4 and 5 append the legacy end summary; 0 and 6 do not.”

   **Fix:** “For exit codes 3, 4 and 5, the parser appends the legacy summary to stderr; for 0 and 6, it appends none.”

5. **5. The batch end state is all correct, yet the output before EOF is missing — shorten the diagram labels.**

   Quotes: “Completion event and EOF / all channels as expected” and “Completion event and EOF / all channels identical.”

   The existing English render becomes text-heavy near 500 px. B1 also occupies two lines while A1 occupies one, misaligning corresponding observation boxes.

   **Fix labels only:**

   - A1: `Valid message arrives`
   - B1: `Same message arrives`
   - A2: `stdin open<br/>message readable`
   - B2: `stdin open<br/>no output in window`
   - A3: `Completion + EOF<br/>all three as expected`
   - B3: `Completion + EOF<br/>same final results`

   Keep the IDs, edges, classes and configuration unchanged.

6. **6. From one problem to more: which results should stay the same, and which must change — “problem” repeatedly means a test exercise.**

   Quote: “From one problem to more…”

   **Fix heading:** “6. Deriving more test cases: which results should stay the same, and which must change”

   In section 3, “This problem has two places where the derivation easily goes wrong” should become “Two steps in this derivation are easy to get wrong.” Use **exercise** for the reader’s derivation task and **case** for an input being tested.

7. **6. From one problem to more: which results should stay the same, and which must change — a fault does not itself ‘go wrong.’**

   Quote: “…the truthiness fault of sections 3 and 4 goes wrong on exactly those values.”

   **Fix:** “Those are exactly the values the truthiness bug in sections 3 and 4 mishandles.”

8. **7. Verify the yardstick first: positive and negative controls, surviving changes, and inconclusive results — avoid implying that every proposed check was performed.**

   Quote: “Before using it to judge candidates, I check it with four kinds of input…”

   The Chinese’s “我會先……” and section 12’s description of recommended practices support a proposed workflow. The present habitual wording sounds like an established, fully exercised procedure, including inconclusive-result handling.

   **Fix:** “Before using it to judge candidates, I would first check it with four kinds of input…”

9. **7. Verify the yardstick first: positive and negative controls, surviving changes, and inconclusive results — the link promises both records but opens only the initial one.**

   Quote: “Both versions’ records are kept in the attachment…”

   This navigation problem also exists in the Chinese.

   **Fix:** “The initial 23-check record and the current 26-check record are both archived.”

   Link “initial 23-check record” to `runs/initial-results.json` and “current 26-check record” to `observed-results.json`. Both destinations already appear elsewhere in the article.

10. **10. Understand the yardstick first, then talk about isolation, freezing and grader versions — replace the abstract verb.**

    Quote: “Only once you know what the yardstick has to hold can you know what must be kept apart.”

    **Fix:** “First identify the obligations the yardstick must enforce. Then decide what information must be isolated.”

11. **10. Understand the yardstick first, then talk about isolation, freezing and grader versions — identify what fixed the standard.**

    Quote: “The point of arranging it this way is to fix the definition of ‘pass’ before any candidate is seen…”

    The nearest antecedent is evaluating after generation. The pre-execution freeze fixed the definition; delayed evaluation alone would not do that. This ambiguity is shared with the Chinese.

    **Fix:** “The pre-execution freeze fixed the definition of ‘pass’ before formal candidates were available. After generation finished, external acceptance used that frozen grader.”

12. **11. Fix the oracle, reject the candidate, or go back to the requirements owner — ‘keep every assigned job’ needs a mathematical object.**

    Quote: “When computing the overall delivery rate, keep every assigned job; when computing the results of completed checks, also list separately the number of observations actually completed.”

    **Fix:** “Use all assigned jobs as the denominator for the overall delivery rate. When reporting completed-check results, give the number of completed observations as a separate denominator.”

## Suggested cuts

- **9. The obligation table: handing derivations, gaps and owners to the next person who takes over.**

  Quote: “handing derivations, gaps and owners to the next person who takes over”

  **Shorten to:** “handing over derivations, gaps and owners.”

  Throughout the piece, shorten repeated instances of “the next person who takes over” to “whoever takes over” where the responsibility remains clear.

- **10. Understand the yardstick first, then talk about isolation, freezing and grader versions.**

  Quote: “The third, and the one most easily confused: after the grader changes version, what exactly has to be redone?”

  **Shorten to:** “Third, what needs to be redone when the grader changes?”

- **12. Closing: before the green light comes on, say what it can see.**

  Quote: “Until then, the next time I see ‘all passed,’ I will first ask whoever wrote the tests to bring out the obligation table…”

  Retain this handoff and the final blockquote. They carry the Chinese closure. No substantive English-only padding warrants deleting a paragraph; the excess is mostly phrasing.

## Suggested additions

- **10. Understand the yardstick first, then talk about isolation, freezing and grader versions — identify A0/A/B/C when they become necessary.**

  Quote: “On new CLI arguments, A0 says only that no new ones ‘are required’; A’s R13 goes further…”

  A standalone reader has encountered “four briefs” but has not been told which labels identify which documents.

  **Minimal clarification:** “A0, the compact brief, says only that no new CLI arguments are required. A, the expanded brief, goes further in R13; B and C include A’s wording.”

  Link the labels to the frozen specs or the existing `SPECS.md` guide. This addresses a gap shared with the Chinese; it is not a missing translated passage.

## Terms still unclear

- **7. Verify the yardstick first: positive and negative controls, surviving changes, and inconclusive results — oracle versus its implementation.**

  Quote: “The oracle is itself a program…”

  Section 2 defines an oracle as the basis for judgment and includes human judgment among its sources. This sentence abruptly makes every oracle software.

  **Fix:** “The comparison program implementing the oracle can also be wrong.”

- **10. Understand the yardstick first, then talk about isolation, freezing and grader versions — brief/spec versus packet.**

  Quote: “a new full packet”

  **Fix:** “a new task packet—the brief, seed code and shared task and response instructions.”

  Use **brief/spec** for the requirements document and **packet** for the assembled task input.

- **10. Understand the yardstick first, then talk about isolation, freezing and grader versions — slot.**

  Quote: “only when both held was a slot counted as accepted.”

  **Fix:** “A slot is one preassigned generation opportunity. It counted as accepted only when both conditions held.”

  This preserves the distinction between an allocated opportunity and the candidate it produces.

- **6. From one problem to more: which results should stay the same, and which must change — negative input domain.**

  Quote: “So `10.0` belongs in the negative input domain…”

  This can sound like inputs outside the contract, despite section 2’s explanation that specified rejection behavior belongs inside acceptance.

  **Fix:** “So `10.0` must be included among the inputs expected to be rejected; R08 already settles its treatment.”

- **7. Verify the yardstick first: positive and negative controls, surviving changes, and inconclusive results — self-check has two uses.**

  Quote: “26 checks in total” / “26 self-checks”

  Reserve **self-check** for the instruction added to the brief. Call the tooling count **26 workbench checks**, consistently distinguishing it from the **3 oracle unit tests** and **11 CSV self-tests**.

<!-- tokens: in 2575913 out 28071 -->
