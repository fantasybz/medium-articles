# Codex review — 2026-11-same-spec-overview/article.en.md (round 1)

> model: gpt-6.1-sol, reasoning: xhigh, 2026-10-26 20:52. Codex's own words, not summarised. Round 1; reviewing the English edition against the final Chinese article and the frozen study.

I’ll read the two writing standards first, then compare the editions and frozen study records. I’ll keep the repository read-only and avoid the excluded paths.
<!-- codex ran: /bin/zsh -lc 'cat STYLE.md' -->
<!-- codex ran: /bin/zsh -lc 'cat research/2026-10/style_brief.md' -->
<!-- codex ran: /bin/zsh -lc 'wc -l 2026-11-same-spec-overview/article.md 2026-11-same-spec-overview/article.en.md 2026-10-green-payment/article.en.md 2026-11-aaif-agent-memory -->
<!-- codex ran: /bin/zsh -lc 'cat 2026-11-same-spec-overview/article.md' -->
<!-- codex ran: /bin/zsh -lc "sed -n '145,245p' 2026-11-same-spec-overview/article.md" -->
<!-- codex ran: /bin/zsh -lc "sed -n '246,337p' 2026-11-same-spec-overview/article.md" -->
<!-- codex ran: /bin/zsh -lc 'cat research/experiments/same-spec-ten-runs/PROTOCOL.md' -->
<!-- codex ran: /bin/zsh -lc "sed -n '134,145p' 2026-11-same-spec-overview/article.md" -->
<!-- codex ran: /bin/zsh -lc 'cat research/experiments/same-spec-ten-runs/RESULTS.md research/experiments/same-spec-ten-runs/SPECS.md' -->
The main evidence limits survive the translation. I’ve found added Lamport quotations and several places where the English presents paraphrases as exact spec text. I’m checking the frozen wording and the remaining sections before grading their severity.
<!-- codex ran: /bin/zsh -lc 'cat research/2026-10/same-spec-ten-runs/manuscripts/STATUS.md' -->
<!-- codex ran: /bin/zsh -lc 'cat research/experiments/same-spec-ten-runs/results/formal-2026-09-25/source/specs/A0.md research/experiments/same-spec-ten-runs/results/formal-20 -->
<!-- codex ran: /bin/zsh -lc 'cat research/experiments/same-spec-ten-runs/results/formal-2026-09-25/source/specs/B.md research/experiments/same-spec-ten-runs/results/formal-202 -->
<!-- codex ran: /bin/zsh -lc "sed -n '1,170p' 2026-10-green-payment/article.en.md" -->
<!-- codex ran: /bin/zsh -lc "sed -n '1,150p' 2026-11-aaif-agent-memory/article.en.md" -->
<!-- codex ran: /bin/zsh -lc "sed -n '135,175p' research/experiments/same-spec-ten-runs/results/formal-2026-09-25/source/specs/B.md; sed -n '152,173p' research/experiments/same -->
<!-- codex ran: /bin/zsh -lc "rg -n 'English|英文|second.model|max effort|MAX' research/2026-10/same-spec-ten-runs/manuscripts research/2026-10/same-spec-ten-runs/*2026-10-26* 20 -->
<!-- codex ran: /bin/zsh -lc "python3 -c 'from pathlib import Path; import re; p=Path(\"2026-10-green-payment/article.en.md\"); s=p.read_text(); s=re.sub(r\""'```.*?```", "[cod -->
<!-- codex ran: /bin/zsh -lc "rg --files research/2026-10/same-spec-ten-runs/english-2026-10-26 .context -g '*english*' -g '*overview*' -g '*STATUS*' -g '*manifest*' -g '*meta* -->
<!-- codex ran: /bin/zsh -lc "python3 -c 'from pathlib import Path; import re; s=Path(\"2026-11-aaif-agent-memory/article.en.md\").read_text(); s=re.sub(r\""'```.*?```", "[code -->
<!-- codex ran: /bin/zsh -lc "rg --files .context/same-spec-en-2026-10-26 research/2026-10/same-spec-ten-runs/english-2026-10-26 -g '"'!codex-review-*'"' -g '"'!codex-*'"' -g ' -->
<!-- codex ran: /bin/zsh -lc "python3 -c 'from pathlib import Path; import re,json; z=Path(\"2026-11-same-spec-overview/article.md\").read_text(); e=Path(\"2026-11-same-spec-ov -->
The table dimensions, Mermaid structure and config, reference numbers and back-pointers match. Earlier-series links use the requested English IDs. Two issues need attention: §9 changes work that cannot yet be evaluated into “unacceptable” work, and the AI note points to a status page that still says the English drafts have not been produced.
<!-- codex ran: /bin/zsh -lc "python3 -c 'from pathlib import Path; import re; dirs=[\"2026-11-same-spec-spec\",\"2026-11-same-spec-contract\",\"2026-11-same-spec-variance\"];  -->
<!-- codex ran: /bin/zsh -lc "python3 -c 'from pathlib import Path; import re; z=Path(\"2026-11-same-spec-overview/article.md\").read_text(); e=Path(\"2026-11-same-spec-overvie -->
<!-- codex ran: /bin/zsh -lc "sed -n '1,140p' research/2026-10/same-spec-ten-runs/rebuild-2026-09-28/document-change-proposal.md; sed -n '1,105p' research/2026-10/same-spec-ten -->
<!-- codex ran: /bin/zsh -lc "sed -n '328,375p' 2026-11-same-spec-overview/article.en.md" -->
<!-- codex ran: /bin/zsh -lc "rg --files 2026-11-same-spec-overview .context/same-spec-en-2026-10-26 -g '*svg' -g '*png' -g '*metadata.json' -g '*manifest.json' -g '*render*' - -->
<!-- codex ran: /bin/zsh -lc "sed -n '1,95p' .context/same-spec-en-2026-10-26/brief.md" -->
<!-- codex ran: /bin/zsh -lc "sips -g pixelWidth -g pixelHeight 2026-11-same-spec-overview/publish/en/images/diagram-01.png 2026-11-same-spec-overview/publish/en/images/table-0 -->
<!-- codex ran: /bin/zsh -lc "python3 -c 'from pathlib import Path; import re; s=Path(\"2026-11-aaif-agent-memory/article.en.md\").read_text(); print(s[s.index(\"## 6.\"):])'" -->
The R05, R13 and C quotations match the frozen specs; I’m not flagging them as misquotations. The Mermaid render is readable and its structure is unchanged. The remaining findings concern the Lamport expansion, a few shifts in meaning and wording, and the unsupported English-review record.
## Fatal

None found in the study’s reported numbers or principal evidence limits. No files changed.

## Important

1. **AI collaboration note — the claimed English review record is absent from the linked page.**

   > “This English edition was written by Claude Code (max effort) from the final Chinese text; the paragraph-by-paragraph polish, second-model review and final checks are recorded in the same STATUS.md.”

   [STATUS.md](research/2026-10/same-spec-ten-runs/manuscripts/STATUS.md:45) still says the English manuscripts have not been produced and their writing requests were rejected by the quota limit. That may be stale, but it does not substantiate this sentence.

   **Fix:** retain the writer and effort attribution only where the generation record supports it. Remove the claim that completed English checks are recorded there until the page actually identifies those checks and the manuscript version they covered.

2. **3. Book anchor: Lamport’s blueprints, which preserve the choices made — the English expands and strengthens the Chinese.**

   Chinese:

   > 「第一，寫下規格，會迫使作者在修改程式之前先說清楚程式應該做什麼；很多沒想清楚的地方，要試著寫下來時才會浮現。」

   English:

   > “First, writing a spec forces the author to say what the program is supposed to do before touching the code: ‘Before we start to write any piece of code, we should understand what that code is supposed to do.’”

   > “Many of the places we have not thought through only surface when we try to write them down; Lamport borrows the cartoonist Dick Guindon’s line, ‘Writing is nature’s way of letting you know how sloppy your thinking is.’”

   “Before modifying code” becomes “before touching the code.” The Guindon attribution and quotation are English-only additions.

   Chinese:

   > 「第二，規格把使用介面所需的知識從實作中抽出來，寫成一份可以維護的說明，讓使用者不必讀懂程式碼也能正確呼叫。」

   The added quotation ends with:

   > “After the code has been written and debugged, no one should ever have to read it.”

   The Chinese makes a claim about callers using an interface correctly. The English introduces a substantially broader formulation.

   Chinese:

   > 「第三，描述需要多精密，取決於問題：簡單行為可以用一般文字說清楚，微妙或關鍵的部分，才值得採用更精密的方法與工具。」

   English adds:

   > “In his words, ‘we wouldn’t draw the kind of blueprints needed for a skyscraper when building a toolshed, nor should we write formal specs for most software.’”

   “Most software” is a population-level claim absent from the Chinese.

   **Replace the three-point explanation with:**

   > “The essay makes three points relevant to this question. First, writing a spec forces its author to explain what the program should do before modifying the code; trying to write that explanation often exposes what remains unclear. Second, a spec moves the knowledge needed to use an interface out of its implementation and into a maintainable description, so callers can use it correctly without understanding the code. Third, the precision needed depends on the problem: ordinary prose can describe simple behavior, while subtle or critical parts may justify more precise methods and tools.”

   Keep the following paragraph’s limit on what specifications can establish.

3. **9. A one-page proposal: turning “write it more clearly” into a claim that can be reviewed — inability to evaluate becomes an adverse verdict.**

   Chinese YAML:

   > 「target_work: 固定期間內進來的全部合格修補工作；保留未完成、尚無法驗收與排除的理由」

   English:

   > “target_work: All qualifying patch work arriving in a fixed period; keep the reasons for work that is unfinished, not yet acceptable or excluded”

   Chinese prose:

   > 「提案要保留固定期間內進來的全部合格工作清單，同時記錄未完成、無法驗收與排除的理由。」

   English:

   > “The proposal keeps the full inventory of qualifying work that arrived in the fixed period, and records the reasons for anything unfinished, unacceptable or excluded.”

   **“Cannot yet be evaluated for acceptance” does not mean “unacceptable.”** This changes the inventory’s recorded states and blurs missing evaluation with observed failure.

   **Fix the YAML:**

   > “target_work: All eligible patch work arriving during a fixed period; record why any work is unfinished, cannot yet be evaluated for acceptance, or is excluded”

   **Fix the prose:**

   > “The proposal retains the full inventory of eligible work arriving during the fixed period, including the reasons any work remains unfinished, cannot be evaluated for acceptance, or is excluded.”

4. **9. A one-page proposal: turning “write it more clearly” into a claim that can be reviewed — “tampered with” changes the pause condition.**

   Chinese:

   > 「至於越權、驗收被改動、補救負擔超出可承擔範圍等方法層級的必要條件與暫停規則，owner 要在看到結果之前另外定好，而且不能被平均改善抵銷。」

   English:

   > “Method-level necessary conditions and pause rules, such as exceeding authority, acceptance being tampered with, or a rescue burden beyond what can be carried, are something the owner sets separately before seeing the results, and they cannot be offset by an average improvement.”

   “Tampered with” implies improper interference. The Chinese says acceptance was changed, without making that additional allegation.

   **Fix:**

   > “Before seeing the results, the owner must separately define the method-level necessary conditions and pause rules, including acting beyond granted authority, changes to acceptance checks, or an unmanageable rescue burden. An average improvement cannot override those conditions.”

## Minor

1. **1. After that gap at the workshop, the question changed its target — several metaphors sound translated.**

   > “What it reminded me of, in the Green Is Not Done series, is that between all tests green and meeting the requirements there can be a full six requirements’ worth of distance.”

   **Fix:**

   > “The lesson I carried into Green Is Not Done was that every test can pass while six requirements remain unmet.”

   > “All of that work eventually arrives at the same entrance: the next time we hand out a task, how do we intend to brief it?”

   **Fix:**

   > “All of that work brings us back to one question: how will we brief the next task?”

   The heading also reads literally. **Use:** “1. The workshop gap led to a different question”.

2. **2. After one success, who bears the cost of a default? — “permanently” overstates the document’s status.**

   Chinese:

   > 「原本它只屬於一次任務，任務結束後就可以放下；成為預設之後，它會常駐在 repo 或範本裡，每次派工都會帶上，每位 reviewer 也得判斷候選有沒有照做。」

   English:

   > “Originally it belonged to a single task and could be set aside once the task ended; as a default it lives permanently in the repo or the template, goes out with every assignment, and every reviewer has to judge whether the candidate followed it.”

   The closing section explicitly allows withdrawal.

   **Fix:**

   > “Originally it belonged to one task and could be set aside when that task ended. As a default, it becomes standing guidance in the repo or template, accompanies every assignment, and gives every reviewer another obligation to check.”

3. **3. Book anchor: Lamport’s blueprints, which preserve the choices made — “Book anchor” exposes an editorial label.**

   > “Book anchor: Lamport’s blueprints, which preserve the choices made”

   **Fix:** “3. What Lamport’s blueprint preserves”.

4. **4. Three layers of question: first establish which kind of evidence you lack — the heading and implementation language need ordinary English.**

   > “Three layers of question: first establish which kind of evidence you lack”

   **Fix:** “4. Three layers: which kind of evidence is missing?”

   > “So a good yardstick has to do two things at once: reject known faults, and accept writing that is different but legitimate.”

   **Fix:**

   > “A good yardstick must reject known faults and accept different implementations that meet the contract.”

   Apply the same terminology in **11. Closing: who maintains that paragraph, and when it is withdrawn**, where “legitimate different writing” should become **“different implementations that meet the contract.”**

5. **4. Three layers of question: first establish which kind of evidence you lack — the Mermaid approval label is awkward.**

   > “Handle this candidate / under the existing / approval responsibility”

   **Fix the label only:**

   ```text
   Handle this candidate<br/>Keep approval<br/>responsibility unchanged
   ```

   The existing diagram fits the prescribed width and is readable. Its node IDs, edges and configuration match the Chinese; no layout change is needed.

6. **7. After everything passes: legitimate variation, the ceiling, and regression assets — distinguish holding material constant from recording conditions.**

   > “What is regressed”

   **Fix:** “What regression testing checks”.

   > “Fix the positive and negative fixtures with verified behavior; change the grader version”

   “Fix” can mean repair.

   Chinese:

   > 「固定已核對行為的正反 fixtures，換 grader 版本」

   **Fix:**

   > “Hold the verified valid and faulty fixtures constant; change the grader version.”

   Likewise, replace “Fix the same contract cases” with **“Hold the contract cases constant.”**

   Chinese method row:

   > 「取得新的生成結果，保存 task／trial 分布與 policy 版本」

   English:

   > “Obtain new generation results; keep the task/trial distribution and the policy version”

   “Keep” under this column heading can imply holding those conditions unchanged rather than preserving their records.

   **Fix:**

   > “Obtain fresh generation results; record the task/trial distribution and the policy version.”

7. **8. Triaging the CSV case: fix the oracle, and the existing acceptance comes back — the framing is unnatural.**

   > “Next, I use a different task to walk the triage diagram from section 4 for real.”

   The following sentence identifies a teaching hypothetical. “For real” adds avoidable friction.

   **Fix:**

   > “Next, I use another example to work through the triage diagram from section 4.”

   **Use this heading:** “8. Triaging the CSV case: repair the oracle, then resume acceptance”.

8. **8. Triaging the CSV case: fix the oracle, and the existing acceptance comes back — the idempotency explanation remains difficult to parse.**

   > “The parser case works the same way: R13 requires that repeated messages and repeated completions be accepted (in the spec’s words, repeated identical agent messages ‘are printed/count separately’), which neither permits deduplication nor means that replaying the same batch of events may only produce the first run’s effect; the latter is what idempotent handling would mean here.”

   Chinese:

   > 「parser 的案例也是同樣道理：R13 要求接受重複訊息與重複完成，並不代表可以去重，也不代表重播同一批事件時只能產生第一次的效果；後者才是這裡說的冪等處理。」

   **Fix:**

   > “The parser case works the same way. R13 requires repeated messages and completions to remain accepted, with repeated identical messages printed and counted separately. It does not permit deduplication, and it does not require replaying an event batch to have no additional effect. That latter guarantee would be idempotent handling.”

   This preserves the distinction without making readers untangle “may only produce the first run’s effect.”

9. **8. Triaging the CSV case: fix the oracle, and the existing acceptance comes back — “protective power” is a calque.**

   > “The same programs, placed under acceptance with different protective power, received different verdicts.”

   **Fix:**

   > “The same programs received different verdicts when the acceptance checks became better at detecting faults.”

   Use **“fault-detection ability”** consistently for this meaning, including the evidence list in section 10.

10. **9. A one-page proposal: turning “write it more clearly” into a claim that can be reviewed — repair the incomplete constructions.**

   > “If both lower layers are sound and the team genuinely has to decide whether to make a piece of brief a default, I would ask the proposer to write a one-page proposal first.”

   **Fix:**

   > “If the first two layers are sound and the team needs to decide whether to make a passage from a brief part of its default template, I would ask the proposer to write a one-page proposal first.”

   > “`task_id` records which original requirement and starting repo; `work_id` gives each of the six pieces of work its own number.”

   **Fix:**

   > “`task_id` identifies the original requirement and starting repository version; `work_id` identifies each of the six scheduled attempts.”

11. **10. Three exits: walk the process first, run a small trial, or adopt as a default — the bold openings sound like translated labels.**

   > “Walking the process first, the diagnostic pilot, confirms that the requirements, the positive and negative cases, the grader and the recording flow actually work.”

   **Fix:**

   > “A diagnostic pilot walks through the process to confirm that the requirements, verified valid and faulty cases, grader and recording procedures work.”

   > “A small-scale trial, the limited-deployment trial, keeps the original human approval…”

   **Fix the opening:** “A limited-deployment trial retains the original human approval…”

12. **11. Closing: who maintains that paragraph, and when it is withdrawn — “product” and “taken over” obscure the concrete handoff.**

   > “That gap made me ask, in Green Is Not Done, what else has to be looked at beyond a green light before a product can be taken over.”

   **Fix:**

   > “That gap led me to ask, in Green Is Not Done, what else we must examine before taking responsibility for a delivered program.”

   Also replace **“product”** with **“candidate”**, **“program”** or **“artifact”** where the article means a generated deliverable. In section 4’s table, “Did this product do it?” should be **“Did this candidate implement the required behavior?”**

## Suggested cuts

- **3. Book anchor: Lamport’s blueprints, which preserve the choices made** — cut the English-only Guindon attribution and the quotation expansions identified above. They add authority and length without carrying another step from the Chinese argument. Preserve the three points and Lamport’s stated limit.
- No other paragraph-level cuts. The repeated distinctions about requirements, candidate acceptance, method comparison and human effort also exist in the Chinese; deleting them selectively would reduce fidelity.

## Suggested additions

- **AI collaboration note** — add the actual English-edition provenance record before claiming that polishing, second-model review and final checks are documented. Identify the reviewed manuscript version.
- No additional studies, anecdotes, results or examples are needed. The references, section back-pointers, earlier-series English URLs, table dimensions, example data and final closure are carried across. The R05, R13 and C quotations match the frozen English specifications.

## Terms still unclear

- **6. A narrow case: four briefs, forty candidates, all 103 checks passed**

  > “The forty slots were scheduled in advance…”

  Define the unit immediately: **“The forty generation slots—one planned attempt per slot—were scheduled in advance…”** Section 9 later explains sessions, but section 6 already relies on this denominator.

- **9. A one-page proposal: turning “write it more clearly” into a claim that can be reviewed**

  > “The parser’s six questions involve rules about EOF, tokens and error events…”

  **Fix:** “The parser’s six questions involve rules about EOF, token-count fields and error events…” This identifies the actual fields governed by R08.

- **9. A one-page proposal: turning “write it more clearly” into a claim that can be reviewed**

  > “All qualifying patch work…”  
  > “Each scheduled slot’s original final candidate…”  
  > “per final qualifying delivery…”

  These refer to three different statuses. Use **“eligible task”** for inventory inclusion, **“accepted original candidate”** for the agent outcome, and **“final qualifying delivery”** for the delivery after any recorded human repair. Keep those denominators visibly distinct.

<!-- tokens: in 1657459 out 20543 -->
