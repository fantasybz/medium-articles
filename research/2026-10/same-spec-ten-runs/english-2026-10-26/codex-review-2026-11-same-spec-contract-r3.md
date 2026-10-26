# Codex review — 2026-11-same-spec-contract/article.en.md (round 3)

> model: gpt-6.1-sol, reasoning: xhigh, 2026-10-27 01:15. Codex's own words, not summarised. Round 3; reviewing the English edition against the final Chinese article and the frozen study.

I’ll read the writing standards first, then check the English against the Chinese source, frozen study files, and approved voice samples. I’ll keep the review read-only and stay inside the repository.
<!-- codex ran: /bin/zsh -lc 'cat STYLE.md' -->
<!-- codex ran: /bin/zsh -lc 'cat research/2026-10/style_brief.md' -->
<!-- codex ran: /bin/zsh -lc 'nl -ba 2026-11-same-spec-contract/article.md' -->
<!-- codex ran: /bin/zsh -lc 'wc -l 2026-11-same-spec-contract/article.en.md 2026-10-green-payment/article.en.md 2026-11-aaif-agent-memory/article.en.md research/experiments/sa -->
<!-- codex ran: /bin/zsh -lc "rg --files research/experiments/same-spec-ten-runs/results/formal-2026-09-25/source research/2026-10/same-spec-ten-runs -g '"'!agents/**'"' -g '"' -->
<!-- codex ran: /bin/zsh -lc "sed -n '150,335p' 2026-11-same-spec-contract/article.md" -->
<!-- codex ran: /bin/zsh -lc 'cat research/experiments/same-spec-ten-runs/RESULTS.md research/experiments/same-spec-ten-runs/SPECS.md' -->
The English keeps the main evidence limits in the opening: the teaching fixtures are separate from the forty candidates, and “all passed” does not rank the briefs. I’m now checking the rule paraphrases, later sections, tables, and publishing notes for smaller shifts.
<!-- codex ran: /bin/zsh -lc 'cat research/experiments/same-spec-ten-runs/results/formal-2026-09-25/source/specs/A0.md research/experiments/same-spec-ten-runs/results/formal-20 -->
<!-- codex ran: /bin/zsh -lc 'cat research/experiments/same-spec-ten-runs/PROTOCOL.md' -->
<!-- codex ran: /bin/zsh -lc "sed -n '336,510p' 2026-11-same-spec-contract/article.md" -->
<!-- codex ran: /bin/zsh -lc "sed -n '505,637p' 2026-11-same-spec-contract/article.md" -->
<!-- codex ran: /bin/zsh -lc 'cat research/experiments/same-spec-ten-runs/PROTOCOL.md' -->
<!-- codex ran: /bin/zsh -lc 'cat research/experiments/same-spec-ten-runs/results/formal-2026-09-25/source/specs/B.md research/experiments/same-spec-ten-runs/results/formal-202 -->
<!-- codex ran: /bin/zsh -lc "sed -n '1,150p' 2026-10-green-payment/article.en.md" -->
<!-- codex ran: /bin/zsh -lc "sed -n '/"'^## Non-normative implementation pattern/,$p'"' research/experiments/same-spec-ten-runs/results/formal-2026-09-25/source/specs/C.md" -->
<!-- codex ran: /bin/zsh -lc "sed -n '1,120p' 2026-11-aaif-agent-memory/article.en.md" -->
<!-- codex ran: /bin/zsh -lc 'cat research/experiments/same-spec-ten-runs/results/formal-2026-09-25/source/requirements.json' -->
<!-- codex ran: /bin/zsh -lc "rg -n 'English|english|contract|契約|MAX|max|polish|final|review|審|en\\.md|EN' research/2026-10/same-spec-ten-runs/manuscripts/STATUS.md" -->
<!-- codex ran: /bin/zsh -lc "rg --files research/2026-10/same-spec-ten-runs/english-2026-10-26 -g '"'!agents/**'"' -g '"'!**/.claude/**'"'" -->
<!-- codex ran: /bin/zsh -lc "sed -n '165,270p' 2026-11-aaif-agent-memory/article.en.md" -->
<!-- codex ran: /bin/zsh -lc 'cat research/2026-10/same-spec-ten-runs/manuscripts/STATUS.md' -->
I found a publishing-note mismatch: the English says its revision and final-check records are in `STATUS.md`, but that file still says the English drafts have not been produced. The CLI wording caveat matches the frozen specs. I’m finishing the code, table, diagram, and sentence-level checks.
<!-- codex ran: /bin/zsh -lc "python3 -I -B - <<'PY'
from pathlib import Path
import re, tokenize, io
root = Path('.')
z = (root/'2026-11-same-spec-contract/article.md').read_t -->
<!-- codex ran: /bin/zsh -lc "python3 -I -B -c 'from pathlib import Path
import re, tokenize, io
from collections import Counter
root = Path('\\''.'\\'')
z = (root/'\\''2026-11 -->
<!-- codex ran: /bin/zsh -lc 'cat research/2026-10/same-spec-ten-runs/rebuild-2026-09-28/workbench/RESULTS.md research/2026-10/same-spec-ten-runs/rebuild-2026-09-28/workbench/c -->
<!-- codex ran: /bin/zsh -lc "rg --files 2026-11-same-spec-contract -g '"'!agents/**'"' -g '"'!**/.claude/**'"'" -->
<!-- codex ran: /bin/zsh -lc "rg -n 'P／Q|P/Q|288|共同要求|共同需求|clopper|Clopper|69\\.15|high|max|self-check|change card|obligation table|task packet' 2026-11-same-spec-overview/arti -->
<!-- codex ran: /bin/zsh -lc 'cat 2026-11-same-spec-contract/publish/en/figures.json' -->
<!-- codex ran: /bin/zsh -lc "rg -n 'all channels|designated case|observational|shared requirements|MAX|max effort|This English edition|should pass|keyword' 2026-11-same-spec-c -->
<!-- codex ran: /bin/zsh -lc "nl -ba 2026-11-same-spec-contract/article.en.md | sed -n '1,180p'" -->
<!-- codex ran: /bin/zsh -lc "rg -n 'designated|channel|matrix|mutant|wrong-priority|false-text|continue-after-malformed|compile|unit' research/2026-10/same-spec-ten-runs/rebui -->
<!-- codex ran: /bin/zsh -lc "sed -n '1,100p' 2026-11-same-spec-contract/publish/en/medium-paste.md" -->
The six tables retain the Chinese rows and columns. The code retains the executable tokens, and the Mermaid retains its node IDs and configuration. The English publishing package is stale, though: its paste file and rendered figures still contain wording that the current manuscript has already replaced. I’m separating those publishing issues from the remaining prose fixes.
<!-- codex ran: /bin/zsh -lc "python3 -I -B -c 'from pathlib import Path
import re,json,difflib
a=Path('\\''2026-11-same-spec-contract/article.en.md'\\'').read_text()
p=Path('\ -->
## Fatal

None found in the supplied edition’s technical argument, numerical claims, or derivations.

## Important

1. **“AI collaboration note” — the English verification claim is unsupported by its citation.**

   > “This English edition was written by Claude Code (max effort) from the final Chinese text; the paragraph-by-paragraph polish, second-model review and final checks are recorded in the same STATUS.md.”

   This is an English-only provenance claim. The linked [STATUS.md](research/2026-10/same-spec-ten-runs/manuscripts/STATUS.md:3) still says:

   > 「英文版維持 Claude Code max 主寫，因週額度限制尚未產出。」

   It also lists English drafting, polishing, figures and scheduling as unfinished. That record may be stale; it does not substantiate the sentence.

   **Fix:** Link the actual English workflow record. Until then, replace the verification clause with: “The linked STATUS.md documents the Chinese manuscript workflow; it does not yet contain this edition’s review and final-check records.” Retain the authorship and effort claim only with supporting generation records.

2. **2. “The oracle: who judges right from wrong, on what basis, and where it can misjudge” — the publishing package restores an already-corrected meaning error.**

   The supplied manuscript says:

   > “…and so are part of what acceptance has to check.”

   But [publish/en/medium-paste.md](2026-11-same-spec-contract/publish/en/medium-paste.md) still says:

   > “…and so are part of what must be accepted.”

   Chinese:

   > 「放到 parser 上，`false`、`0` 與陣列這些看起來『不合法』的 `text`，正好落在契約指定的拒絕路徑上，屬於要驗收的內容。」

   “Must be accepted” reverses the point: these inputs belong in acceptance testing, with rejection behavior checked.

   **Fix:** Regenerate the English publishing package from the corrected manuscript after review. Its figure metadata also retains older wording in tables 3, 5 and 6 and the streaming diagram. Do not publish the existing paste file and PNG set as the reviewed edition.

3. **1. “Two green lights, and what each one leaves out” — “fixed” obscures the freeze timeline.**

   > “But the behavioral agreement the study later fixed…”

   Chinese:

   > 「但研究後來固定的行為約定，也就是本文所說的契約，要求非字串、非 null 的 `text` 視為格式錯誤，後文稱為 malformed。」

   In English, “fixed” readily means repaired. Here it means settled and frozen before formal generation.

   **Fix:** “The study later froze a behavioral agreement, called the contract here. It requires any `text` value that is neither a string nor null to be treated as a format error, or malformed.”

## Minor

1. **1. “Two green lights, and what each one leaves out” — the introductory definitions sound translated.**

   > “This parsing tool, the parser, has to recognize the lines one by one and hand the results on to the next program, the caller.”

   **Fix:** “The tool, a parser, recognizes each line and passes the results to the next program, the caller.”

   > “From each of the four briefs, the four documents handed to the model, ten patched programs were generated…”

   **Fix:** “The model generated ten patched programs from each of four task documents, or briefs. This article calls each program awaiting acceptance a candidate.”

2. **2. “The oracle: who judges right from wrong, on what basis, and where it can misjudge” — a stated approach becomes a general preference.**

   > “So I prefer to derive expectations independently from the contract…”

   Chinese:

   > 「所以本篇優先從契約獨立推導預期，讓每個答案都能追到依據，再請人複核推導。」

   **Fix:** “The approach here is to derive expected values independently from the contract so each answer has a traceable basis, then have another person check the derivation.”

3. **2. “The oracle: who judges right from wrong, on what basis, and where it can misjudge” — incomplete action and awkward comparison.**

   > “…output before EOF additionally needs its own observation point arranged.”

   **Fix:** “To check output before EOF, the test author must also arrange when the driver will read it.”

   > “The same programs, given to acceptance checks with different ability to detect faults, led to different conclusions.”

   **Fix:** “Acceptance checks with different abilities to detect faults produced different conclusions about the same programs.”

4. **3. “Read the rules first, then derive once: after `false` there is still `after`” — the heading omits what is derived.**

   Chinese:

   > 「先讀規則，再推一次：`false` 之後還有 `after`」

   **Fix:** “Read the rules, then derive the expected result: `after` still follows `false`.”

   Also:

   > “The completion event’s usage field records consumption…”

   **Fix:** “The completion event’s `usage` field records token usage…”

5. **7. “Verify the yardstick first: positive and negative controls, surviving changes, and inconclusive results” — clarify why exit 3 remains possible.**

   > “Once R11 sees a malformed event it stops at 3 or 6…”

   Chinese:

   > 「R11 一旦看到 malformed，就會停在 3 或 6，輪不到由『是否發言』決定 exit；R12 的固定摘要也沒有發言數，exit 6 更沒有摘要。」

   The conclusion is correct, but the wording makes malformed status appear to select exit 3.

   **Fix:** “At EOF, explicit failure selects exit 3; otherwise the malformed flag selects exit 6. Either way, the spoken-message flag cannot affect the exit code. R12’s fixed summaries contain no message count, and exit 6 has no summary.”

6. **7. “Verify the yardstick first: positive and negative controls, surviving changes, and inconclusive results” — the mutant definition interrupts its sentence.**

   > “It is a derived example; no program carrying this change, a mutant, was written.”

   **Fix:** “This example was derived from the contract; no mutant implementing this change was written.”

7. **9. “The obligation table: handing derivations, gaps and owners to whoever takes over next” — two calques weaken otherwise concrete responsibilities.**

   > “…it needs targeted reading or added cases…”

   **Fix:** “…it needs a focused review of the relevant code or additional test cases…”

   > “One person can carry these responsibilities, but none of them can be skipped in favor of another.”

   **Fix:** “One person may hold all three responsibilities, but each still has to be fulfilled.”

8. **11. “Fix the oracle, reject the candidate, or go back to the requirements owner” — distinguish unsupported attribution from investigating causes.**

   > “When rejecting, record which obligation was violated, but do not supply a cause for it…”

   Chinese:

   > 「拒絕時要記下違反的是哪一條義務，但不要替它補上成因：從輸出差異看不出模型是漏讀、誤解，還是選錯了寫法。」

   “Do not supply a cause” sounds like a prohibition on explaining the failure even when further evidence exists.

   **Fix:** “When rejecting the candidate, record which obligation it violated, but do not infer the cause from the output difference alone.”

## Suggested cuts

1. **3. “Read the rules first, then derive once: after `false` there is still `after`”**

   > “(the spec’s term for a message that counts as the agent actually having said something)”

   Delete this English-only parenthesis. It explains “spoken message” with another version of “spoken message”; the following sentence supplies the actual rule.

2. **11. “Fix the oracle, reject the candidate, or go back to the requirements owner”**

   > “…where P contains only the shared requirements, while Q also includes a written self-check asking the implementer to revisit those requirements; that comparison has not been run.”

   Once self-check is explained at its first occurrence, shorten this to:

   **“P contains the shared requirements; Q appends the self-check. The comparison has not been run.”**

   Keep the Chinese reasoning, counterexamples and evidence limits. No substantive deletion is warranted merely to shorten this edition.

## Suggested additions

None beyond the inline clarifications below. No additional study results or hypothetical experiences are needed.

## Terms still unclear

1. **8. “Change the task: a semantic oracle for CSV export” — self-check first appears before its meaning is established.**

   > “…nor can it prove that adding a self-check section would improve the result.”

   Explain the intervention here, rather than waiting until section 11.

   **Fix:** “Nor can it prove that adding questions asking the implementer to recheck the existing requirements—a written self-check—would improve the result.”

2. **5. “The batch end state is all correct, yet the output before EOF is missing” — “commands” can suggest that this parser executes them.**

   > “…whether later messages, commands, the token comment or stderr are output promptly…”

   Chinese:

   > 「它只檢查第一則有效訊息，沒有驗證後續訊息、command、token 註記或 stderr 是否即時輸出；stdout 與 stderr 也是分開比對，沒有量測兩者之間的交錯順序。」

   R06 concerns emitted command comments, not command execution by the parser.

   **Fix:** “…whether later messages, command comments, the token comment or stderr are output promptly…”

No files changed.

<!-- tokens: in 2712902 out 19138 -->
