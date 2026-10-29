# Codex 校稿 — 2026-11-aaif-after-tokyo/article.en.md（第 3 輪）

> model: gpt-6.1-sol, reasoning: xhigh, 2026-10-29 00:39. 原話照錄，未經摘要。

I’ll read STYLE.md first, then check the previous fixes and disposition logs before reviewing the English against the Chinese block by block. I’ll keep the repository read-only and report only problems that remain.


<!-- codex ran: /bin/zsh -lc 'cat STYLE.md' -->
<!-- codex ran: /bin/zsh -lc "cat 'research/2026-10/aaif-agntcon/codex-polish-2026-11-aaif-after-tokyo-en-r2.md'" -->
<!-- codex ran: /bin/zsh -lc "cat '.context/research/aaif-2026-10-28-polish/2026-11-aaif-after-tokyo-en-r2-disposition.md'" -->
<!-- codex ran: /bin/zsh -lc "cat 'research/2026-10/aaif-agntcon/codex-polish-2026-11-aaif-after-tokyo-en-r1.md'" -->
<!-- codex ran: /bin/zsh -lc "cat '.context/research/aaif-2026-10-28-polish/2026-11-aaif-after-tokyo-en-r1-disposition.md'" -->
<!-- codex ran: /bin/zsh -lc 'cat .context/research/aaif-2026-10-28-polish/2026-11-aaif-after-tokyo-en-r1-disposition.md' -->
<!-- codex ran: /bin/zsh -lc "sed -n '/"'^1'"\\. \\*\\*\\[must-fix\\]\\|"'^1'"\\. \\*\\*\\[suggested\\]/,"'$p'"' research/2026-10/aaif-agntcon/codex-polish-2026-11-aaif-after-t -->
<!-- codex ran: /bin/zsh -lc "sed -n '/"'^43'"\\. /,"'$p'"' research/2026-10/aaif-agntcon/codex-polish-2026-11-aaif-after-tokyo-en-r1.md" -->
<!-- codex ran: /bin/zsh -lc 'wc -l 2026-11-aaif-after-tokyo/article.en.md 2026-11-aaif-after-tokyo/article.md' -->
<!-- codex ran: /bin/zsh -lc 'cat research/2026-10/aaif-agntcon/codex-polish-2026-11-aaif-after-tokyo-en-r2.md' -->
<!-- codex ran: /bin/zsh -lc "nl -ba 2026-11-aaif-after-tokyo/article.md | sed -n '1,186p'" -->
The disposition logs account for the earlier edits. I’ll leave the rejected heading suggestions and the count-versus-rate decision closed as requested, and continue checking for remaining English ambiguity and bilingual drift.


<!-- codex ran: /bin/zsh -lc 'cat research/2026-10/style_brief.md' -->
<!-- codex ran: /bin/zsh -lc "nl -ba 2026-11-aaif-after-tokyo/article.en.md | sed -n '1,188p'" -->
<!-- codex ran: /bin/zsh -lc "sed -n '95,100p' 2026-11-aaif-after-tokyo/article.md" -->
<!-- codex ran: /bin/zsh -lc "nl -ba 2026-11-aaif-after-tokyo/article.md | sed -n '188,298p'" -->
<!-- codex ran: /bin/zsh -lc "nl -ba 2026-11-aaif-after-tokyo/article.en.md | sed -n '189,299p'" -->
<!-- codex ran: /bin/zsh -lc "sed -n '227,257p' 2026-11-aaif-after-tokyo/article.en.md" -->
<!-- codex ran: /bin/zsh -lc "nl -ba 2026-11-aaif-after-tokyo/article.md | sed -n '300,414p'" -->
The comparison through §10 is largely aligned, including the revised source-method note and the distinction between the judge and optimizer. I’m now checking §11, the closing sections, and the references, while keeping the findings limited to wording or meaning problems that warrant an edit.


<!-- codex ran: /bin/zsh -lc "nl -ba 2026-11-aaif-after-tokyo/article.md | sed -n '416,532p'" -->
<!-- codex ran: /bin/zsh -lc "nl -ba 2026-11-aaif-after-tokyo/article.en.md | sed -n '301,433p'" -->
<!-- codex ran: /bin/zsh -lc "rg -n '"'^#{1,3} |G2|G3|spec-change card|frozen holdout'"' 2026-11-same-spec-spec/article.en.md 2026-11-same-spec-variance/article.en.md 2026-10-g -->
<!-- codex ran: /bin/zsh -lc "nl -ba 2026-11-aaif-after-tokyo/article.en.md | sed -n '435,533p'" -->
<!-- codex ran: /bin/zsh -lc "sed -n '74,116p' 2026-11-aaif-after-tokyo/article.en.md" -->
<!-- codex ran: /bin/zsh -lc "sed -n '43,78p' research/2026-10/style_brief.md" -->
<!-- codex ran: /bin/zsh -lc "rg -n 'behaviour|organisation|authoris|optimis|centre|colour|catalogue|analyse|travelled|cancelled|—|“|”|‘|’' 2026-11-aaif-after-tokyo/article.en. -->
The pass through the final notes is complete. I found no new material parity or numerical discrepancies; the remaining findings concern local clarity, including “stays done,” the two model roles, and the wording of the human-effort requirement. I’m checking the drop-in replacements for unintended changes in meaning.


<!-- codex ran: /bin/zsh -lc "python3 -c 'from pathlib import Path
text = Path(\"2026-11-aaif-after-tokyo/article.en.md\").read_text()
phrases = [
\"create a PR, change a setti -->
1. **[suggested] §3 — “Why can the three…”**  
   **Exact:** “create a PR, change a setting, send a notification, and it stays done.”  
   **Problem:** “It” has no clear singular antecedent, and “stays done” blurs persistent effects with the article’s separate meaning of *done*.  
   **Replacement:** “create a PR, change a setting, or send a notification, and the effect remains.”

2. **[optional] §5, introduction — “Think of the new colleague…”**  
   **Exact:** “declaring the commit closest in time to be the root cause”  
   **Problem:** The Chinese explains *commit* here; the English postpones its explanation until §7.  
   **Replacement:** “declaring the code revision (commit) closest in time to be the root cause”

3. **[suggested] §9, 08:55 figure caption — “Marcelo Trylesinski…”**  
   **Exact:** “looking for the direction of improvement in the execution process.”  
   **Problem:** “Looking for the direction of improvement” is an awkward calque.  
   **Replacement:** “examining the execution process to identify what needs improving.”

4. **[suggested] §9, “Turn production failures into tests with explicit expectations” — “Evals prepared in advance…”**  
   **Exact:** “Use the traveler case to separate two roles:”  
   **Problem:** The following list includes two models and a person. Specify which two roles are being distinguished.  
   **Replacement:** “Use the traveler case to separate two model roles:”

5. **[suggested] §10, “Evaluate the evaluator too” — “I would require…”**  
   **Exact:** “and a classification that is confident but wrong never enters the escalation path, so high-confidence samples need human spot-checks.”  
   **Problem:** The third item under “require three more things” begins with an observation rather than the requirement it supports.  
   **Replacement:** “and high-confidence samples must receive human spot-checks, because a classification that is confident but wrong never enters the escalation path.”

6. **[suggested] §11 — “Once a quarter’s worth…”**  
   **Exact:** “Second, expanding authority has to separate "opening it to more teams" from "opening up one particular write operation," because section 5 of "Evals, Unit Economics, and Scaling" puts the former at G2 and the latter under individual review and G3, while section 5 of the reliability piece added reliability conditions to G2, so the two cannot be referred to by the same gate.”  
   **Problem:** The 63-word sentence stacks *because*, *while*, and *so* around several cross-references, making the reasoning difficult to follow in one pass.  
   **Replacement:** “Second, expanding authority has to separate "opening it to more teams" from "opening up one particular write operation." Section 5 of "Evals, Unit Economics, and Scaling" puts the former at G2 and the latter under individual review and G3. Section 5 of the reliability piece added reliability conditions to G2, so the two cannot be referred to by the same gate.”  
   **Companion adjustment:** Replace “this article offers only two sentences about them” with “this article offers only two points about them” to accommodate the sentence breaks.

7. **[suggested] §11 — “Once a quarter’s worth…”**  
   **Exact:** “All three have to record how much time colleagues spent rechecking.”  
   **Problem:** “All three” refers to the decisions, making them the actors doing the recording.  
   **Replacement:** “For each of the three decisions, record how much time colleagues spent rechecking.”

**Counts by priority:** must-fix **0**; suggested **6**; optional **1**. **Total: 7.**

**Counts by review category** (one primary category per finding): grammar **1**; punctuation/spelling **0**; readability **4**; flow **0**; terminology **1**; internal consistency/cross-references **1**; zh/en parity **0**.

The accepted earlier fixes are sound, and no rejected finding is reopened. I found no new material discrepancies in claims, numbers, or zh/en meaning; the remaining issues are local clarity edits. No files were changed.

<!-- tokens: in 1599986 out 14532 -->
