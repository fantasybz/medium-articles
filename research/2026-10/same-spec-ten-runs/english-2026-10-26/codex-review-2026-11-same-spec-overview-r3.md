# Codex review — 2026-11-same-spec-overview/article.en.md (round 3)

> model: gpt-6.1-sol, reasoning: xhigh, 2026-10-27 01:17. Codex's own words, not summarised. Round 3; reviewing the English edition against the final Chinese article and the frozen study.

I’ll read the writing standards first, then compare the English against the Chinese and frozen study files. I’ll stay inside this repository, treat it as read-only, and avoid the prohibited skill directories.
<!-- codex ran: /bin/zsh -lc 'cat STYLE.md' -->
<!-- codex ran: /bin/zsh -lc 'cat research/2026-10/style_brief.md' -->
<!-- codex ran: /bin/zsh -lc 'nl -ba 2026-11-same-spec-overview/article.md' -->
<!-- codex ran: /bin/zsh -lc 'cat research/experiments/same-spec-ten-runs/RESULTS.md' -->
<!-- codex ran: /bin/zsh -lc 'cat research/experiments/same-spec-ten-runs/SPECS.md' -->
<!-- codex ran: /bin/zsh -lc 'cat research/experiments/same-spec-ten-runs/PROTOCOL.md' -->
<!-- codex ran: /bin/zsh -lc 'nl -ba 2026-11-same-spec-overview/article.en.md' -->
<!-- codex ran: /bin/zsh -lc "sed -n '130,285p' 2026-11-same-spec-overview/article.md" -->
The main study limits are preserved so far: the English does not rank the four briefs, claim equivalence, or present the CSV replay as a trial. I’m checking smaller shifts in definitions, spec quotations, and the proposed comparison’s decision rules.
<!-- codex ran: /bin/zsh -lc 'cat research/experiments/same-spec-ten-runs/results/formal-2026-09-25/source/specs/A0.md' -->
<!-- codex ran: /bin/zsh -lc "sed -n '286,470p' 2026-11-same-spec-overview/article.md" -->
<!-- codex ran: /bin/zsh -lc 'cat research/experiments/same-spec-ten-runs/results/formal-2026-09-25/source/specs/C.md' -->
<!-- codex ran: /bin/zsh -lc "sed -n '390,480p' 2026-11-same-spec-overview/article.md" -->
<!-- codex ran: /bin/zsh -lc 'cat research/experiments/same-spec-ten-runs/RESULTS.md' -->
<!-- codex ran: /bin/zsh -lc "sed -n '1,150p' 2026-11-aaif-agent-memory/article.en.md" -->
<!-- codex ran: /bin/zsh -lc "sed -n '1,130p' 2026-10-green-payment/article.en.md" -->
<!-- codex ran: /bin/zsh -lc "sed -n '1,38p' research/experiments/same-spec-ten-runs/results/formal-2026-09-25/source/specs/A0.md" -->
<!-- codex ran: /bin/zsh -lc "rg -n -i 'english|英文|overview|總論|MAX|HIGH|288|review' research/2026-10/same-spec-ten-runs/manuscripts/STATUS.md" -->
<!-- codex ran: /bin/zsh -lc "python3 -B -c 'from pathlib import Path
import re
base=Path('\\''.'\\'')
z=(base/'\\''2026-11-same-spec-overview/article.md'\\'').read_text()
e=(b -->
<!-- codex ran: /bin/zsh -lc 'cat research/2026-10/same-spec-ten-runs/manuscripts/STATUS.md' -->
<!-- codex ran: /bin/zsh -lc "python3 -B -c 'from pathlib import Path
import re
z=Path('\\''2026-11-same-spec-overview/article.md'\\'').read_text()
e=Path('\\''2026-11-same-spe -->
<!-- codex ran: /bin/zsh -lc "rg -n '288|48|interval|cluster|bootstrap|percentage|human|qualifying|gate|fee|cost' research/2026-10/same-spec-ten-runs/rebuild-2026-09-28/compari -->
<!-- codex ran: /bin/zsh -lc "rg --files research/2026-10/same-spec-ten-runs 2026-11-same-spec-overview | rg -i 'english|\\.en\\.|review|draft|STATUS'" -->
I found a concrete problem in the AI collaboration note: it says STATUS.md records the English edition’s review and final checks, but that file still says the English manuscripts have not been produced. The structural checks match: six tables retain their rows and columns, the example blocks are unchanged, and the Mermaid IDs and configuration are intact.
<!-- codex ran: /bin/zsh -lc 'cat research/2026-10/same-spec-ten-runs/english-2026-10-26/codex-review-2026-11-same-spec-overview-r3.md' -->
<!-- codex ran: /bin/zsh -lc 'cat research/2026-10/same-spec-ten-runs/rebuild-2026-09-28/comparison-plan-example.md' -->
<!-- codex ran: /bin/zsh -lc 'cat research/2026-10/same-spec-ten-runs/rebuild-2026-09-28/document-change-proposal.md' -->
<!-- codex ran: /bin/zsh -lc "rg -n '空欄|empty column|thorough|all the work|claim|below|same STATUS|original final|share of|supports exceeding|on their own|optional' 2026-11-sam -->
<!-- codex ran: /bin/zsh -lc 'cat research/2026-10/same-spec-ten-runs/english-2026-10-26/codex-review-2026-11-same-spec-overview-r3.md' -->
<!-- codex ran: /bin/zsh -lc "sed -n '1,90p' 2026-11-aaif-agent-memory/article.en.md" -->
<!-- codex ran: /bin/zsh -lc "python3 -B -c 'from pathlib import Path
import re
z=Path('\\''2026-11-same-spec-overview/article.md'\\'').read_text()
e=Path('\\''2026-11-same-spe -->
<!-- codex ran: /bin/zsh -lc "python3 -B -c 'from pathlib import Path
z=Path('\\''2026-11-same-spec-overview/article.md'\\'').read_text().split('\\''\\n\\n'\\'')
e=Path('\\''20 -->
Two wording problems affect the technical argument: “every output looks the same” blurs program structure with observable output, and “empty column” should be “empty field” in the CSV example. I’m also checking whether “packet, the complete input” overstates what the archive contains, since it stores a separate system prompt.
<!-- codex ran: /bin/zsh -lc "python3 -B -c 'from pathlib import Path
z=Path('\\''2026-11-same-spec-overview/article.md'\\'').read_text().split('\\''\\n\\n'\\'')
e=Path('\\''20 -->
<!-- codex ran: /bin/zsh -lc "python3 -B -c 'from pathlib import Path
z=Path('\\''2026-11-same-spec-overview/article.md'\\'').read_text().split('\\''\\n\\n'\\'')
e=Path('\\''20 -->
<!-- codex ran: /bin/zsh -lc 'cat research/experiments/same-spec-ten-runs/results/formal-2026-09-25/system.txt' -->
<!-- codex ran: /bin/zsh -lc "sed -n '188,210p' 2026-11-same-spec-overview/article.en.md" -->
<!-- codex ran: /bin/zsh -lc "sed -n '1,42p' research/experiments/same-spec-ten-runs/results/formal-2026-09-25/packets/A0.txt" -->
<!-- codex ran: /bin/zsh -lc "rg -n 'spec change card|change card|obligation table|brief|yardstick|oracle' 2026-11-same-spec-spec/article.en.md 2026-11-same-spec-contract/artic -->
The paragraph-by-paragraph comparison is complete. I found no missing sections, table rows, examples, reference entries, or closure steps. The remaining findings concern specific meaning shifts, the unsupported STATUS.md claim, English-only elaborations, and wording that leaves actions or terms unclear.
## Fatal

None found.

## Important

1. **AI collaboration note — the English review record is misrepresented.**

   > “This English edition was written by Claude Code (max effort) from the final Chinese text; the paragraph-by-paragraph polish, second-model review and final checks are recorded in the same STATUS.md.”

   The Chinese says:

   > 「本稿的主寫、代理審稿、逐段潤飾與語言檢查紀錄，見 STATUS.md。」

   That refers to the Chinese manuscript. The linked [STATUS.md](research/2026-10/same-spec-ten-runs/manuscripts/STATUS.md:45) still lists the English manuscripts, polish and publication work as unfinished. English review files exist elsewhere, but this sentence points to the wrong record and claims that final checks are documented there.

   **Fix:** “The Chinese manuscript’s writing and review history is recorded in STATUS.md. That file has not yet been updated to document this English edition.”

   Retain the Claude Code/max-effort authorship statement only where its generation record supports it.

2. **7. After everything passes: legitimate variation, the ceiling, and regression assets — “output” changes the object of the argument.**

   > “Until then, ‘every output looks the same’ cannot serve as a quality goal.”

   Chinese:

   > 「如果團隊真的重視程式結構，就要把結構寫成有來歷、有驗收的架構要求；在那之前，『每次產出都一樣』不能當作品質目標。」

   This paragraph concerns generated **program structure**. “Output” can mean stdout, whose contents the contract does constrain.

   **Fix:** “If the team genuinely requires a particular program structure, it must record that structure as an architectural requirement, with its source and a matching acceptance check. Until then, requiring every generated program to look the same cannot serve as a quality goal.”

3. **9. A one-page proposal: turning “write it more clearly” into a claim that can be reviewed — the trace limitation is strengthened.**

   > “But even with the tool calls and the execution record (the trace) preserved, they do not reveal why the model did what it did.”

   Chinese:

   > 「但即使保留了工具呼叫與執行過程的紀錄（trace），也不能從中讀出模型的心理成因。」

   The Chinese excludes inference about the model’s internal reasons. The English excludes explanations generally, including observable execution mechanisms discussed immediately before it.

   **Fix:** “Even a preserved trace of tool calls and execution steps does not establish the model’s internal reasons for choosing them.”

4. **4. Three layers of question; 5. Example Mapping; 8. Triaging the CSV case — translate 空欄 as “empty field.”**

   Repeated wording includes:

   > “a `null` date produces an empty column”  
   > “its date is an empty column”

   A column spans records. The example leaves one record’s date **field** empty. Correct all seven occurrences:

   | Section | Chinese source | Corrected English |
   |---|---|---|
   | 4 | 「例如，需求已決定日期是 `null` 時輸出空欄，檢查工具就可以據此核對結果；如果需求還沒決定，檢查工具本身沒有權力選答案。」 | “If the requirements specify an empty field for a `null` date, the checking tool can compare the result against that rule; if the policy is undecided, the tool has no authority to choose an answer.” |
   | 4 | 「一份排版完整的規格，不會自動決定空日期該輸出空欄還是拒絕；一份通過驗收的候選，也不能證明產生它的交代方式比較好；即使方法比較設計得很嚴謹，也無法補上一條沒人決定過的需求。」 | “A neatly formatted spec does not decide whether to export an empty date field or reject the input; a candidate that passes acceptance does not prove that its brief is better; and even a rigorous method comparison cannot supply a requirement nobody has decided.” |
   | 5 | 「假設某個 CSV 匯出工具要新增日期欄格式化，呼叫端已要求保留輸入列的順序與重複列，但還沒決定空日期要輸出空欄還是拒絕。」 | “Suppose a CSV export tool needs date formatting. The caller already requires input row order and duplicate rows to be preserved, but nobody has decided whether a missing date should produce an empty field or cause rejection.” |
   | 5, table | 「缺日期時，輸出空欄還是拒絕整份輸入？」 | “When the date is missing, output an empty field or reject the whole input?” |
   | 5 | 「它可能選擇輸出空欄，也可能選擇拒絕。」 | “It might output an empty field, or it might reject the input.” |
   | 8 | 「假設 owner 決定 null 日期輸出空欄，並和 QA owner 確認三個格式條件：欄位標題（header）的名稱與順序固定為 `name,date,note`；每筆完整資料（record）可以用 LF 或 CRLF 這兩種換行表示結束；欄位內容裡的逗號與換行都要保留。」 | “Suppose the owner decides that a `null` date produces an empty field and confirms three formatting conditions with the QA owner: the header names and order are fixed as `name,date,note`; each record may end with LF or CRLF; and commas and line breaks within fields must be preserved.” |
   | 8 | 「第一筆的姓名仍含逗號，日期是空欄，備註仍保留欄位內的換行；後面兩筆完全相同的『李』都要保留。」 | “The first record’s name retains its comma, its date field is empty, and its note retains the embedded line break; both identical ‘李’ records that follow are preserved.” |

5. **6. A narrow case: four briefs, forty candidates, all 103 checks passed — “the complete input” overstates packet scope.**

   > “The study calls the task description and starting code sent to the model in one go a packet, the complete input.”

   Chinese:

   > 「研究把一次送給模型的任務說明與起始程式碼合稱為 packet，也就是整包輸入。」

   This ambiguity is inherited from the Chinese. The archive separately preserves a shared [system prompt](research/experiments/same-spec-ten-runs/results/formal-2026-09-25/system.txt). The packet is not the model’s entire input.

   **Fix:** “The study calls the task instructions and starting code sent together a task packet. Each packet was supplied alongside the same archived system prompt.”

6. **10. Three exits: dry-run the process first, run a small trial, or adopt as a default — purpose becomes a guaranteed result.**

   > “This confirms that the requirements, the positive and negative controls, the grader and the recording flow actually work.”

   Chinese:

   > 「先試走流程，也就是診斷 pilot 用來確認要求、正反對照、grader 與紀錄流程是否能正常運作。」

   A diagnostic pilot checks **whether** these work; it can reveal that they do not.

   **Fix:** “Use the diagnostic pilot to check whether the requirements, positive and negative controls, grader and recording process work as intended.”

7. **11. Closing: who maintains that paragraph, and when it is withdrawn — restore the final sentence’s optionality.**

   > “While the evidence is still insufficient, fill in the requirements, fix the acceptance, or run a limited trial under the original approval first.”

   Chinese:

   > 「證據還不夠時，可以先補需求、修驗收，或在原核准下有限試行。」

   The imperative drops 可以. These are available next steps, not a requirement to perform one regardless of the remaining problem.

   **Fix:** “While evidence is insufficient, the team can first fill in missing requirements, repair acceptance checks, or run a limited trial under the existing approval rules.”

## Minor

These are English repairs, not requests to compress the reasoning.

- **1. After the workshop gap, the question turned to the brief**

  > “the responsibility of review”

  **Fix:** “who is accountable for review.”

  > “tests have not loosened a requirement they were supposed to hold”

  **Fix:** “tests have not weakened a requirement they were supposed to enforce.”

- **2. After one success, who bears the cost of a default?**

  > “Sometimes finding the right responsible person, or fixing the way right and wrong are judged, is all the work in front of you needs.”

  “The right responsible person” and the ending both sound translated.

  **Fix:** “Sometimes the team can resolve the current task simply by finding the right owner or fixing how results are judged.”

- **3. Book anchor: Lamport’s blueprints preserve the choices already made**

  > “Book anchor”

  This is an editorial calque, and the source discussed is an essay.

  **Fix heading:** “3. What a spec preserves—and what it leaves to verification.”

  > “only the subtle or critical parts earn more precise methods and tools”

  **Fix:** “only subtle or critical behavior justifies more precise methods and tools.”

- **4. Three layers of question: first establish which kind of evidence is missing**

  > “Three layers of question”

  **Fix:** “Three layers of questions.” Correct the same phrase in section 3’s body.

- **5. Example Mapping: a model cannot fill in a policy nobody has decided**

  > “a line like ‘handle the formatting properly’ looks as if it has briefed the work”

  **Fix:** “‘Handle the formatting properly’ can sound like a complete instruction while leaving the handling of empty values undecided.”

- **6. A narrow case: four briefs, forty candidates, all 103 checks passed**

  > “comes from a round of study”

  **Fix:** “comes from a study.” Likewise, replace “This round of study” with “This study.”

  > “Two problems reproduce on that version.”

  **Fix:** “Two problems can be reproduced on that version.”

  > “That is not a bill, and it excludes the study, the pilots, the writing and the human cost.”

  Chinese:

  > 「這不是帳單，也不包含研究、pilot、寫作或人工成本。」

  “Excludes the study” is confusing because the forty generations belong to the study.

  **Fix:** “This is a list-price estimate for the forty formal generations, not a bill. It excludes research and review work outside those generations, pilot runs, writing and human labor.”

  > “Cost rises as the document gets longer”

  **Fix:** “In these four groups, longer briefs had higher reported generation costs.” Keep the observation scoped to these groups.

- **7. After everything passes: legitimate variation, the ceiling, and regression assets**

  > “even when the two programs execute in a different order”

  Chinese:

  > 「假如兩份程式的判斷與呼叫次數很接近，分數就可能接近，即使它們執行的順序不同。」

  The English can mean running program A before B.

  **Fix:** “even when operations occur in different orders within the two programs.”

- **8. Triaging the CSV case: fix the oracle, and the existing acceptance is restored**

  > “The narrow case showed how far the study can answer.”

  **Fix:** “The parser case established the limits of what this study can tell us.”

  > “The replay can be checked for yourself.”

  **Fix:** “You can inspect the replay yourself.”

  > “The diagram’s final ‘No’ thus becomes a closure with a reason behind it.”

  **Fix:** “The final ‘No’ now gives the team a reason to close the task.”

- **9. A one-page proposal: turning “write it more clearly” into a claim that can be reviewed**

  > “Below is a demonstration against the parser’s background.”

  **Fix:** “Here is a proposal using the parser as the example.”

  > “The cost’s numerator and denominator have to correspond.”

  **Fix:** “When calculating cost per qualifying delivery, the numerator and denominator must cover the same work.”

  > “a rescue burden beyond what can be carried”

  **Fix:** “a repair burden beyond what the team can sustain.”

- **10. Three exits: dry-run the process first, run a small trial, or adopt as a default**

  > “The piece of brief the team wants to try can first run as a limited-deployment trial”

  **Fix:** “The team can first try the proposed passage on a few work items under a limited-deployment trial.”

- **11. Closing: who maintains that paragraph, and when it is withdrawn**

  > “Answering in order, if the first two layers still have gaps, deal with the requirements and the acceptance in front of you first.”

  **Fix:** “If either of the first two layers still has a gap, resolve the current requirements and acceptance issues first.”

  > “Maintenance also has to tell apart what changed.”

  **Fix:** “The owner must also identify which component changed.”

## Suggested cuts

1. **4. Three layers of question — remove the English-only definitional equation.**

   > “The oracle and the grader together are the yardstick this piece keeps referring to.”

   The Chinese moves directly from defining the grader to:

   > 「好比答案與批改步驟：答案正確，仍可能批改錯誤；批改忠實，也可能照著一份錯誤答案判分。」

   The added definition is reasonable, but it is an English-only claim. **Delete it** for strict cross-edition fidelity. The answer-key analogy already carries the distinction.

2. **5. Example Mapping — replace the R05 quotation chain with the Chinese’s explanatory prose.**

   > “In the frozen spec’s own words …”

   The quotations reproduce A0’s wording, but the chain is harder to follow than the Chinese and adds the explicit “plus one newline” detail.

   Chinese:

   > 「它規定：缺值、`null` 與空字串都不輸出，也不記為發言；非空字串要原樣印出，立刻把暫存的內容送到輸出端（flush），不能等整批工作結束才讓下一個程式讀到。」  
   > 「只有空白的字串也算有效；其餘非字串值，包括 `false`、`0`、陣列與物件，都屬於格式錯誤，後文稱為 malformed。」

   **Replacement:** “Missing `text`, `null` and the empty string produce no output and do not count as a message. A nonempty string must be printed unchanged, with buffered content sent to the output immediately (flushed), so the next program can read it before the batch ends. Whitespace-only strings are valid. Other non-string values, including `false`, `0`, arrays and objects, are format errors, called malformed here.”

3. **7. After everything passes — trim the additional handler-result explanation.**

   > “describing the output and the flags”

   Chinese:

   > 「C 的 pattern 甚至明白列出兩種合法做法：可以由 handler 回傳一份小結果，也可以保留 if 分支，在各分支中就地驗證。」

   Those additional fields are supported by C, but absent from this Chinese sentence. **Delete the phrase**; retain both implementation alternatives and the separate top-level-error rule.

No whole-paragraph cuts are justified by fidelity.

## Suggested additions

- **4. Three layers of question — explain controls before their first table appearance.**

  First use:

  > “An oracle checked with positive and negative controls”

  The concrete explanation arrives three paragraphs later:

  > 「後文說的『正反對照』，就是事先準備已核對的合法版本與錯誤版本，確認檢查不會把這兩類弄反。」

  **Move that explanation before the table**, using: “Prepare a verified conforming implementation that should pass and a known faulty implementation that should fail. These are the positive and negative controls used to check the yardstick.”

  This relocates existing meaning; it adds no result or experience.

## Terms still unclear

- **9. A one-page proposal — “original final candidate.”**

  > “Each scheduled slot’s original final candidate passes external acceptance”

  “Original” and “final” need an explicit reference point.

  **Fix:** “The candidate submitted at the end of each scheduled session, before any human repair, passes external acceptance.”

  Keep the separate operating-condition requirement.

- **9. A one-page proposal — “takeover time.”**

  > “Record actual takeover time for every piece of work”

  This can mean delay until a reviewer starts, rather than labor spent reviewing and repairing.

  **Fix:** “For every work item, record human effort after the session ends, separating active work time from elapsed time.”

  Apply the same wording to the later “takeover time actually spent” sentence.

- **9. A one-page proposal — “qualifying delivery.”**

  > “added human time per qualifying delivery”

  Make clear that this denominator concerns final deliveries, potentially after limited human repair, whereas the primary outcome concerns the original candidate.

  **Fix:** “additional human time per final delivery that passes acceptance, including all effort spent on failed attempts and limited human repairs.”

- **5. Example Mapping; 6. A narrow case — “utterance” versus “message.”**

  > “Counting a whitespace-only string as a valid utterance is a decision”

  **Fix:** “Counting a whitespace-only string as an agent message is a decision.”

  Use “counts as an agent message” consistently for the R05 count. “Utterance,” “spoken message” and “actual message” unnecessarily suggest different categories.

<!-- tokens: in 2125440 out 27811 -->
