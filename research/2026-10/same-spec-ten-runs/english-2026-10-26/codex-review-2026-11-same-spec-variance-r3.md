# Codex review — 2026-11-same-spec-variance/article.en.md (round 3)

> model: gpt-6.1-sol, reasoning: xhigh, 2026-10-27 01:36. Codex's own words, not summarised. Round 3; reviewing the English edition against the final Chinese article and the frozen study.

I’ll read the writing standards first, then compare the English against the Chinese source and frozen study. I’ll keep the review read-only and stay inside this repository.
<!-- codex ran: /bin/zsh -lc 'cat research/2026-10/style_brief.md' -->
<!-- codex ran: /bin/zsh -lc 'cat STYLE.md' -->
<!-- codex ran: /bin/zsh -lc "sed -n '45,220p' research/2026-10/style_brief.md" -->
<!-- codex ran: /bin/zsh -lc 'wc -l 2026-11-same-spec-variance/article.md 2026-11-same-spec-variance/article.en.md research/experiments/same-spec-ten-runs/RESULTS.md research/e -->
<!-- codex ran: /bin/zsh -lc "rg --files -g 'AGENTS.md' -g '"'!agents/**'"' -g '"'!.claude/**'"' -g '"'!**/.claude/skills/**'"' -g '*same-spec*' -g '*source-ledger*' -g '*STATU -->
<!-- codex ran: /bin/zsh -lc 'cat research/experiments/same-spec-ten-runs/RESULTS.md research/experiments/same-spec-ten-runs/SPECS.md' -->
<!-- codex ran: /bin/zsh -lc "sed -n '1,120p' 2026-10-green-payment/article.en.md" -->
<!-- codex ran: /bin/zsh -lc "sed -n '1,135p' 2026-11-aaif-agent-memory/article.en.md" -->
<!-- codex ran: /bin/zsh -lc "nl -ba 2026-11-same-spec-variance/article.md | sed -n '1,154p'" -->
<!-- codex ran: /bin/zsh -lc "nl -ba 2026-11-same-spec-variance/article.md | sed -n '112,257p'" -->
The opening sections preserve the main evidence limits: 40/40 does not establish equivalence, and P/Q remains unexecuted. I’m now checking the spec quotations and later decision rules for shifts in scope or meaning.
<!-- codex ran: /bin/zsh -lc "nl -ba 2026-11-same-spec-variance/article.md | sed -n '259,442p'" -->
<!-- codex ran: /bin/zsh -lc 'cat research/experiments/same-spec-ten-runs/RESULTS.md research/experiments/same-spec-ten-runs/SPECS.md research/experiments/same-spec-ten-runs/PR -->
<!-- codex ran: /bin/zsh -lc "python3 -c 'from pathlib import Path; s=Path(\"research/experiments/same-spec-ten-runs/results/formal-2026-09-25/source/specs\"); files={a:(s/(a+\ -->
<!-- codex ran: /bin/zsh -lc "sed -n '125,255p' 2026-10-green-payment/article.en.md" -->
<!-- codex ran: /bin/zsh -lc "nl -ba 2026-11-same-spec-variance/article.en.md | sed -n '1,161p'" -->
<!-- codex ran: /bin/zsh -lc "rg -n 'English|英文|variance|變異|Claude|Codex|MAX|max|round|三輪|三回' research/2026-10/same-spec-ten-runs/manuscripts/STATUS.md" -->
<!-- codex ran: /bin/zsh -lc "python3 -c 'from pathlib import Path; import re,collections; z=Path(\"2026-11-same-spec-variance/article.md\").read_text(); e=Path(\"2026-11-same- -->
<!-- codex ran: /bin/zsh -lc "sed -n '1,160p' research/2026-10/same-spec-ten-runs/rebuild-2026-09-28/comparison-plan-example.md" -->
<!-- codex ran: /bin/zsh -lc 'cat research/2026-10/same-spec-ten-runs/english-2026-10-26/README.md' -->
<!-- codex ran: /bin/zsh -lc "rg -n '"'^# |''^> Series:|''^### Series|''^### AI|''^### References|''^'"\\*Kochi|"'^- '"' 2026-11-same-spec-overview/article.en.md 2026-11-same-s -->
The seven tables have matching dimensions, and the link differences are limited to the requested English-edition substitutions and Chinese-edition links. The spec wording checks out. The English also adds two disclosed technical clarifications in section 7; I’ll distinguish those from translation drift. The remaining issues are mainly wording and terminology.
<!-- codex ran: /bin/zsh -lc "python3 -c 'from pathlib import Path; import re,ast,hashlib; base=Path(\"research/experiments/same-spec-ten-runs/results/formal-2026-09-25\"); z=P -->
I found three wording issues worth fixing: the cost paragraph shifts from describing a measurement scale to describing how costs vary; the oracle definition loses the comparison procedure; and the architecture paragraph drops the authority part of the Chinese’s “權責.” I’m separating those from smaller prose edits in the review.
## Fatal

None found. The English preserves the conditional Clopper–Pearson interval, the limits of 40/40, the unexecuted P/Q design, the teaching-aid exclusions, and the HIGH-generation/MAX-writing distinction.

## Important

1. **3. Four arms at 10/10: identical observed results do not establish equivalence — cost dispersion.**

   Chinese:
   > 成本本身也會隨重複執行而變動：前一節提到的 SWE-bench 研究中，同一種規格與 effort 重複執行時，研究以幾何標準差（geometric SD）描述成本的倍數散布，其中位數為 ×1.34；這種量尺用倍數而非相差幾美元表示離散程度（arXiv 2608.25399v1，§4.3）。

   English:
   > “repeated runs of the same specification and effort varied in cost multiplicatively rather than by a fixed dollar amount”

   This shifts a description of the **measurement scale** into a stronger claim about how costs vary.

   **Fix:**
   > For repeated runs of the same specification and effort, the study summarized cost dispersion using geometric standard deviation (geometric SD), with a median of ×1.34. This measure expresses dispersion as a multiplicative factor rather than a dollar difference.

2. **5. Both at 10/20, and it still matters which tasks failed — the oracle’s comparison procedure disappears.**

   Chinese:
   > 我會先查這五題是否碰到共同的義務、量尺或工作類型：需求是否仍未決定，判斷對錯的依據與比對方式（oracle）是否誤拒合法寫法，或者目前做法是否在某類工作上較常失敗。

   English:
   > “whether a legitimate way of writing the program is being wrongly rejected by the rule used to judge right from wrong, the oracle”

   “Rule” drops the explicit **comparison procedure**. That matters to this series: the expected behavior can be correct while byte comparison wrongly rejects valid output.

   **Fix:**
   > I would first check whether those five tasks share an obligation, an acceptance yardstick or a type of work: whether a requirement remains undecided, whether the oracle’s basis for the expected result or its comparison procedure wrongly rejects a valid implementation, or whether the current approach fails more often on that type of work.

   The English also introduces this narrower definition in **3. Four arms at 10/10…**:
   > “‘No failure observed’ covers only what the yardstick can see: the rules that define the expected behavior (the oracle) and the grader that applies them.”

   Chinese:
   > 所謂「沒有觀察到失敗」，只涵蓋量尺看得見的範圍。

   That explanatory tail is English-only. **Cut it**, retain the Chinese’s sentence, and introduce the oracle through the concrete diagnostic question in section 5.

3. **7. Two candidates that both passed: which review action does the difference point to? — authority is lost.**

   Chinese:
   > 第三，如果團隊是以降低理解或修改成本為理由，想選定一種共同架構，就要另外設計比較；已成立的相容與架構義務，仍依原本的權責執行。

   English:
   > “the compatibility and architectural obligations already in force are still carried out under their original responsibilities”

   “Under their original responsibilities” is unclear English and loses **權**: who has authority over those obligations.

   **Fix:**
   > Third, a team that wants to standardize an architecture to reduce comprehension or modification time needs a separate comparison. The people already authorized and responsible for enforcing existing compatibility and architectural obligations must continue to enforce them.

## Minor

1. **1. All four groups passed ten out of ten, so where does the next budget go? — agreement.**

   > “Each proposal costs money, but they buy different evidence and answer different questions.”

   **Fix:**
   > Each proposal costs money, buys different evidence and answers a different question.

2. **2. First, identify what changed this time: three kinds of variation, three units of comparison — tasks do not prepare documents.**

   > “each task still prepares its documents according to its own requirements”

   **Fix:**
   > The documents for each task still have to be prepared from that task’s own requirements.

3. **3. Four arms at 10/10: identical observed results do not establish equivalence — counts do not split text.**

   > “Word counts split on whitespace, include headings and code, exclude the starting code, and are not the token count the model processes.”

   **Fix:**
   > These counts use whitespace-separated words. They include headings and code, exclude the starting code, and differ from the model’s token counts.

4. **4. The same success rate, different usage policies — awkward sentence construction.**

   > “How reliable the yardstick is, is exactly the question the Contract part deals with.”

   **Fix:**
   > Part 2, Contract asks how reliable that yardstick is.

5. **7. Two candidates that both passed: which review action does the difference point to? — cumbersome action.**

   > “For a reviewer, the next step is to go looking for the implementation with one requirement in hand: where does this difference oblige me to look more closely?”

   **Fix:**
   > A reviewer can now trace one requirement through each implementation and ask: where does this difference require closer inspection?

6. **7. Two candidates that both passed… — retain the disclosed technical correction.**

   Chinese:
   > R03 接著要求：每個壞行只留一則診斷，仍要繼續讀後面的輸入。

   English:
   > “R03 then requires that each malformed line leave exactly one malformed-event diagnostic on stderr, and that the parser ‘continue reading’ the input that follows (a malformed `turn.failed` additionally keeps its R10 failure diagnostic).”

   This adds an exception absent from that Chinese sentence. The frozen R03/R10 supports it, and the AI note discloses it. **Do not remove it to force literal parity.** Tighten it:

   > R03 requires exactly one malformed-event diagnostic per malformed line and continued processing. A malformed `turn.failed` also emits its legacy failure diagnostic under R10.

   Likewise, retain the disclosed `if not text: return` clarification; reverting to the Chinese’s isolated `if text:` would make the example less precise.

7. **AI collaboration note — an edition cannot be reviewed “by a review.”**

   > “reviewed by an independent Claude reader review and three rounds of Codex review”

   **Fix:**
   > reviewed by a separate Claude reader agent and in three Codex review rounds against the Chinese text and frozen study

   The recorded workflow supports the attribution. This is a grammar fix, not grounds for claiming independent human verification.

## Suggested cuts

1. **1. All four groups passed ten out of ten, so where does the next budget go? — premature English-only definition.**

   > “its reading of pass^k, the chance that all k deliveries in a row succeed, is restated with an example in section 4.”

   Chinese:
   > 那篇關心多次交付是否都能成功，以及人工複核要保留多少預算；其中 pass^k 的讀法，第四節會用例子重說一次。

   **Fix:**
   > That piece examined whether repeated deliveries all succeed and how much budget to retain for human re-checking. Section 4 revisits pass^k through an example.

   Let section 4’s example introduce the definition. Also remove section 3’s added oracle/grader gloss as noted above.

   No broader cuts: deleting the Chinese-supported limitations, derivations or final closure would reduce fidelity.

## Suggested additions

None. The missing comparison procedure and authority language need restoration, not additional studies, examples or data.

## Terms still unclear

1. **6. Work backward from the question to the next piece of evidence — “Behavior is not equivalent.”**

   > “Behavior is not equivalent”

   This table label and bold subsection lead-in can sound like an observed behavioral difference. The paragraph establishes a difference in **documented requirements**; its effect remains unknown. It also risks confusion with section 3’s statistical equivalence discussion.

   **Fix both occurrences:**
   > Requirements differ between conditions

2. **4. The same success rate, different usage policies — which policy differs?**

   > “What is compared is each policy’s final results, together with the budget spent to obtain them.”

   Here “policy” can mean the session rules or the self-check intervention. Section 9 requires the session rules to remain the same.

   **Fix:**
   > The comparison records the final results under P and Q and the budget each used, with the same session policy in both conditions.

Mechanical checks found no missing table rows or columns: all seven tables match. Python logic and YAML keys match; neither edition contains Mermaid. References 1–13 retain their URLs and section back-pointers. The Series blocks, earlier-series English IDs and Chinese-edition signature link match the requested mapping.

<!-- tokens: in 1254045 out 14673 -->
