# Codex review — 2026-11-same-spec-variance/article.en.md (round 2)

> model: gpt-6.1-sol, reasoning: xhigh, 2026-10-27 01:22. Codex's own words, not summarised. Round 2; reviewing the English edition against the final Chinese article and the frozen study.

I’ll read the writing standards, then compare the editions paragraph by paragraph against the frozen study. I’ll keep all reads inside this repository and make no changes.
<!-- codex ran: /bin/zsh -lc 'cat STYLE.md' -->
<!-- codex ran: /bin/zsh -lc 'cat research/2026-10/style_brief.md' -->
<!-- codex ran: /bin/zsh -lc 'wc -l 2026-11-same-spec-variance/article.md 2026-11-same-spec-variance/article.en.md research/experiments/same-spec-ten-runs/RESULTS.md research/e -->
<!-- codex ran: /bin/zsh -lc "sed -n '1,180p' 2026-11-same-spec-variance/article.md" -->
<!-- codex ran: /bin/zsh -lc 'cat research/experiments/same-spec-ten-runs/RESULTS.md' -->
<!-- codex ran: /bin/zsh -lc "rg --files -g '*SKILL.md' -g '"'!agents/**'"' -g '"'!.claude/**'"' -g '"'!**/agents/**'"' -g '"'!**/.claude/**'"' -g '*source-ledger*' -g '*STATUS -->
<!-- codex ran: /bin/zsh -lc "sed -n '145,300p' 2026-11-same-spec-variance/article.md" -->
The draft keeps the main evidence limits intact: 40/40 does not establish equivalence, and P/Q remains unexecuted. I found a few changes around the contract examples that need checking against the frozen English specs, including an added R03 exception and a rewritten truthiness example.
<!-- codex ran: /bin/zsh -lc "sed -n '300,455p' 2026-11-same-spec-variance/article.md" -->
<!-- codex ran: /bin/zsh -lc 'cat research/experiments/same-spec-ten-runs/results/formal-2026-09-25/source/specs/A0.md research/experiments/same-spec-ten-runs/results/formal-20 -->
<!-- codex ran: /bin/zsh -lc 'cat research/experiments/same-spec-ten-runs/SPECS.md research/experiments/same-spec-ten-runs/PROTOCOL.md' -->
<!-- codex ran: /bin/zsh -lc "sed -n '1,170p' 2026-10-green-payment/article.en.md" -->
<!-- codex ran: /bin/zsh -lc "sed -n '1,170p' 2026-11-aaif-agent-memory/article.en.md" -->
<!-- codex ran: /bin/zsh -lc "sed -n '107,142p' 2026-11-same-spec-variance/article.md" -->
<!-- codex ran: /bin/zsh -lc "rg -n 'English|英文|variance|變異|Claude|Codex|MAX|max|審查|完成' research/2026-10/same-spec-ten-runs/manuscripts/STATUS.md" -->
<!-- codex ran: /bin/zsh -lc 'tail -n 45 research/experiments/same-spec-ten-runs/results/formal-2026-09-25/source/specs/C.md' -->
<!-- codex ran: /bin/zsh -lc 'tail -n 49 research/experiments/same-spec-ten-runs/results/formal-2026-09-25/source/specs/B.md' -->
<!-- codex ran: /bin/zsh -lc "python3 -c 'from pathlib import Path
import re
for name in [\"2026-11-same-spec-variance/article.md\",\"2026-11-same-spec-variance/article.en.md\" -->
<!-- codex ran: /bin/zsh -lc 'cat research/2026-10/same-spec-ten-runs/manuscripts/STATUS.md' -->
<!-- codex ran: /bin/zsh -lc 'cat research/2026-10/same-spec-ten-runs/rebuild-2026-09-28/self-check-transfer-policy.md' -->
<!-- codex ran: /bin/zsh -lc "sed -n '60,135p' research/experiments/same-spec-ten-runs/results/formal-2026-09-25/formal-01-A0/candidate/codex_jsonl.py" -->
<!-- codex ran: /bin/zsh -lc 'cat research/2026-10/same-spec-ten-runs/rebuild-2026-09-28/comparison-plan-example.md' -->
The tables match row for row, and the reference URLs match apart from the requested English-series substitutions and Chinese-edition links. The collaboration note has a documentation problem: it says the English checks are recorded in `STATUS.md`, but that file still says the English manuscripts have not been produced.
<!-- codex ran: /bin/zsh -lc "sed -n '1,110p' research/experiments/same-spec-ten-runs/results/formal-2026-09-25/formal-02-A0/candidate/codex_jsonl.py" -->
<!-- codex ran: /bin/zsh -lc "sed -n '215,255p' research/experiments/same-spec-ten-runs/results/formal-2026-09-25/formal-02-A0/candidate/codex_jsonl.py" -->
<!-- codex ran: /bin/zsh -lc "sed -n '180,240p' research/experiments/same-spec-ten-runs/results/formal-2026-09-25/formal-01-A0/candidate/codex_jsonl.py" -->
<!-- codex ran: /bin/zsh -lc 'cat research/2026-10/same-spec-ten-runs/rebuild-2026-09-28/reliability-source-ledger.json' -->
<!-- codex ran: /bin/zsh -lc "rg -n '"'^#|''^##|''^###|comparison|對照|note|英文|English'"' 2026-11-same-spec-overview/article.en.md 2026-11-same-spec-spec/article.en.md 2026-11-sa -->
<!-- codex ran: /bin/zsh -lc "python3 -c 'from pathlib import Path
import re,hashlib,json
base=Path(\"research/experiments/same-spec-ten-runs/results/formal-2026-09-25\")
spec= -->
<!-- codex ran: /bin/zsh -lc "rg --files --hidden .context research/2026-10/same-spec-ten-runs 2026-11-same-spec-variance -g '"'!**/agents/**'"' -g '"'!**/.claude/**'"' -g '"'! -->
<!-- codex ran: /bin/zsh -lc "rg --files --hidden .context/same-spec-en-2026-10-26 research/2026-10/same-spec-ten-runs/english-2026-10-26 -g '"'!**/agents/**'"' -g '"'!**/.clau -->
<!-- codex ran: /bin/zsh -lc 'cat research/2026-10/same-spec-ten-runs/english-2026-10-26/README.md' -->
The English-edition record confirms max-effort drafting and completed review rounds, so the provenance issue is the stale `STATUS.md` pointer. It also documents the R03 exception and truthiness rewrite as deliberate technical clarifications. The remaining issues are mostly translation stiffness and a few phrases that imply more than the Chinese states.
Read-only review; no files changed. All seven tables retain the Chinese rows and columns. The Python calculations and YAML field names match. Neither edition contains Mermaid. References 1–13 preserve their numbering, URLs and section back-pointers. The earlier-series links use the required English Post IDs.

## Fatal

None found. The draft preserves the statistical assumptions, the limits of 40/40, the unexecuted P/Q design, the hypothetical calculations, and the distinction between HIGH generation effort and MAX manuscript effort.

## Important

1. **AI collaboration note — the English audit pointer is wrong.**

   > “This English edition was written by Claude Code (max effort) from the final Chinese text; the paragraph-by-paragraph polish, second-model review and final checks are recorded in the same STATUS.md.”

   The repository’s `STATUS.md` still says the English manuscripts have not been produced. The newer [English-edition record](research/2026-10/same-spec-ten-runs/english-2026-10-26/README.md) documents drafting and review rounds, while publication checks remain pending. The drafting claim has support; the stated location and final-check implication do not.

   **Fix:** Point the English note to that record and write:

   > “This English edition was drafted by Claude Code at max effort from the final Chinese text. The English-edition record documents drafting and completed review rounds; final publication checks remain pending.”

   Make the preceding `STATUS.md` bullet explicitly about the **Chinese manuscript**.

2. **7. Two candidates that both passed: which review action does the difference point to? — added personal attribution.**

   Chinese:

   > 「下面實際讀兩份，看看這個問題怎麼問。」

   English:

   > “Below, I actually read two candidates to see how that question is asked.”

   The English explicitly attributes the code reading to Kochi. The Chinese leaves the walkthrough’s agency unstated; the collaboration disclosures establish AI-assisted analysis, not this personal action.

   **Fix:**

   > “The following static walkthrough reads two candidates against that question.”

3. **8. Keeping the old results: what to recheck when the yardstick, the program or the method changes — plural “tasks” muddies the denominator.**

   Chinese:

   > 「這批題目、答案與評分資料，已在研究與成稿過程中揭露，並整理成可查核附件。」

   English:

   > “This batch of tasks, answers and scoring data has been disclosed during the research and writing, and organized into verifiable attachments.”

   There was **one task**, forty generations and 103 checks per candidate. English forces a plural reading that the study does not support.

   **Fix:**

   > “The study task, its answers and its grading data were disclosed during research and writing and organized into verifiable attachments.”

   The same correction is needed in **11. The decision record: joint conditions, and the exit when data falls short**, first table row:

   Chinese:

   > 「四組各 10/10，通過 103 項檢查；題目與答案已在研究／成稿過程揭露」

   English:

   > “Four arms at 10/10, passing 103 checks; the tasks and answers were disclosed during research and writing”

   **Fix:** Change “the tasks and answers” to **“the study task and its answers.”**

## Minor

1. **1. All four briefs passed ten out of ten, so where does the next budget go? — briefs do not pass acceptance.**

   > “All four briefs passed ten out of ten…”

   **Fix the heading:**

   > “Four groups, ten passes each: where should the next budget go?”

   Also:

   > “This piece takes over the third layer…”

   “Takes over” is a calque here.

   **Fix:**

   > “This piece addresses the third question…”

2. **2. Say first what changed this time: three kinds of variation, three units of comparison — unnatural heading syntax.**

   > “Say first what changed this time…”

   **Fix:**

   > “First, identify what changed: three kinds of variation, three units of comparison”

3. **2. Say first what changed this time: three kinds of variation, three units of comparison — incomplete action.**

   > “Same task, same brief, same model settings and execution policy, delivered once more, letting the parts of the generation process that cannot be pinned down vary on their own.”

   What is delivered, and by whom?

   **Fix:**

   > “The model generates another candidate for the same task, using the same brief, model settings and execution policy, while the uncontrolled parts of generation vary.”

4. **3. Four arms at 10/10: identical observed results do not establish equivalence — abstract translation before the explanation.**

   > “A statistical interval deals with exactly the uncertainty that remains even when every observation came out the same.”

   **Fix:**

   > “Even identical observed results leave uncertainty about the underlying success probability. A confidence interval describes that sampling uncertainty.”

   Retain the following independence and common-probability assumptions unchanged.

5. **3. Four arms at 10/10: identical observed results do not establish equivalence — “median” has an unclear referent.**

   > “…the researchers described the multiplicative spread of cost with a geometric standard deviation (geometric SD), with a median of ×1.34…”

   **Fix:**

   > “Repeated-run cost can vary multiplicatively rather than by a fixed dollar amount. The researchers measured that spread with geometric standard deviation (geometric SD); the median geometric SD was ×1.34.”

   This also puts the problem before the term.

6. **9. The next comparison card: how to assign work, how to count, where to draw tasks from (not yet executed) — use obligation language for unfinished preparation.**

   Chinese:

   > 「每題都要核對完整 P／Q、diff、條文映射與不適用理由，並在試行前封存版本與內容雜湊值。」

   English:

   > “For every task, the complete P and Q, the diff, the clause mapping and the not-applicable reasons are checked, and the version and content hashes are archived before any trial.”

   The surrounding caveats prevent a false completion claim, but “are checked” weakens the Chinese requirement.

   **Fix:**

   > “For every task, the complete P and Q, their diff, the clause mapping and the not-applicable reasons must be checked, and the version and content hashes must be archived before any trial.”

7. **10. Human takeover and scale: what 288 slots cannot buy — the precision paragraph reads like translated exposition.**

   > “Put these two rough numbers next to the 5-percentage-point threshold and a result that should be known in advance appears…”

   **Fix:**

   > “Compared with a 5-percentage-point threshold, these rough half-widths suggest that a true gain of five or six percentage points will very likely remain ‘undetermined’ at this scale.”

   Keep the preceding warning that this is **not** the design’s power analysis.

8. **11. The decision record: joint conditions, and the exit when data falls short — “exit” is proposal vocabulary rather than reader-facing English.**

   **Fix the heading:**

   > “11. The decision record: adoption conditions and what to do when evidence falls short”

## Suggested cuts

No whole-section cuts. Most repetition is also present in the Chinese; removing it only from English would reduce fidelity.

1. **1. All four briefs passed ten out of ten, so where does the next budget go? — remove verbal bulk from the roadmap.**

   > “It then places one and the same success rate inside two ways of working, to see why the number changes…”

   **Fix:**

   > “It then shows how the same per-run success rate produces different workflow success rates…”

   “One and the same” adds emphasis without information.

2. **7. Two candidates that both passed: which review action does the difference point to? — untangle the selection sentence.**

   > “To answer it, this static reading, done after the study was complete, first selected the two A0 candidates that come earliest in the frozen execution order…”

   **Fix:**

   > “For this post-study static reading, the first two A0 candidates in the frozen execution order were selected before their code was read.”

   Keep the following qualifications about post hoc selection and representativeness.

3. **6. Work backward from the question to the next piece of evidence — trim theatrical emphasis.**

   > “…what effect this difference had remains unknown to this day.”

   **Fix:**

   > “…the effect of this difference remains unknown.”

## Suggested additions

1. **7. Two candidates that both passed: which review action does the difference point to? / AI collaboration note — disclose the two documented technical clarifications.**

   These are departures from literal translation, but the frozen contract supports them. The English-edition record already explains their editorial basis.

   **R03 clarification**

   Chinese:

   > 「R03 接著要求：每個壞行只留一則診斷，仍要繼續讀後面的輸入。」

   English:

   > “R03 then requires that each malformed line leave exactly one malformed-event diagnostic on stderr, and that the parser ‘continue reading’ the input that follows (a malformed `turn.failed` additionally keeps its R10 failure diagnostic).”

   The parenthetical adds a qualification absent from the Chinese sentence. Frozen R03 and R10 explicitly support it. **Keep the qualification.**

   **Truthiness clarification**

   Chinese:

   > 「這個順序本身沒有錯，卻讓第一個判斷成為關鍵：如果那一行用 `if text:` 判斷值是真還是假（truthiness），把所有『看起來是空的』值一起放行，`false` 與 `0` 就會被當成沒有訊息，直接略過。」

   English changes the example to:

   > “…if that guard were written as a truthiness test, `if not text: return`…”

   That makes the intended silent early return explicit. It preserves the intended warning but changes the code expression.

   **Concrete addition to the collaboration note:**

   > “The English edition clarifies the malformed-`turn.failed` diagnostic exception and makes the truthiness example’s early return explicit; both clarifications are documented in the English-edition record.”

   Do not revert accurate contract wording merely to reproduce the Chinese simplification.

## Terms still unclear

1. **3. Four arms at 10/10: identical observed results do not establish equivalence — “accepted” needs an explicit conjunction.**

   > “Operational conditions were checked separately, and a candidate counted as accepted only when both held.”

   “Both” requires the reader to reconstruct two unlike conditions.

   **Fix:**

   > “A candidate counted as accepted only if the CLI completed normally with the generation boundary intact and the file passed all 103 checks.”

   This matches the frozen endpoint.

2. **3. Four arms at 10/10: identical observed results do not establish equivalence — distinguish yardstick, oracle and grader.**

   > “‘No failure observed’ covers only what the yardstick, the acceptance checks and the program that scores them, can see.”

   The apposition is cumbersome and does not establish the distinctions used later.

   **Fix:**

   > “‘No failure observed’ covers only what the yardstick can detect: the rules defining expected behavior and the grader that applies them.”

3. **5. Both at 10/20, and it still matters which tasks failed — introduce the oracle through its possible error.**

   > “…whether the basis and method for judging right from wrong, the oracle, wrongly rejects a legitimate way of writing the program…”

   The definition interrupts the diagnostic question.

   **Fix:**

   > “…whether a legitimate implementation is being rejected by the rule used to judge correctness—the oracle…”

   The reader encounters the problem before its name.

4. **9. The next comparison card: how to assign work, how to count, where to draw tasks from (not yet executed) — bare “reference.”**

   > “…to check that the reference, the positive and negative controls, the grader and the execution script (runner) behave.”

   Reference document, expected output or implementation?

   **Fix:**

   > “…to check that the reference implementation, positive and negative controls, grader and execution script behave as intended.”

5. **10. Human takeover and scale: what 288 slots cannot buy — “qualifying delivery.”**

   > “When computing human effort per qualifying delivery…”

   The phrase is central to the cost denominator but sounds like an unexplained eligibility category.

   **Fix its first occurrence:**

   > “When computing human effort per final delivery that meets the agreed requirements—a qualifying delivery…”

   Continue using **qualifying delivery** afterward.

6. **11. The decision record: joint conditions, and the exit when data falls short — “incoming list.”**

   > “What is needed is an incoming list of export-type work…”

   **Fix:**

   > “What is needed is a list of incoming export-related tasks…”

   Use **incoming work** consistently; “incoming” alone should not become another named artifact.

<!-- tokens: in 1869370 out 22715 -->
