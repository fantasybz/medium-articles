# Codex 校稿 — 2026-11-aaif-after-tokyo/article.en.md（第 2 輪）

> model: gpt-6.1-sol, reasoning: xhigh, 2026-10-29 00:17. 原話照錄，未經摘要。

I’ll read STYLE.md first, then check the round-one fixes and disposition log before reviewing both editions block by block. I’ll keep all access inside this repository and make no changes.
<!-- codex ran: /bin/zsh -lc 'cat STYLE.md' -->
<!-- codex ran: /bin/zsh -lc 'cat .context/research/aaif-2026-10-28-polish/2026-11-aaif-after-tokyo-en-r1-disposition.md' -->
<!-- codex ran: /bin/zsh -lc 'cat research/2026-10/aaif-agntcon/codex-polish-2026-11-aaif-after-tokyo-en-r1.md' -->
<!-- codex ran: /bin/zsh -lc 'wc -l 2026-11-aaif-after-tokyo/article.en.md 2026-11-aaif-after-tokyo/article.md
cat research/2026-10/style_brief.md' -->
<!-- codex ran: /bin/zsh -lc 'cat .context/research/aaif-2026-10-28-polish/2026-11-aaif-after-tokyo-en-r1-disposition.md' -->
<!-- codex ran: /bin/zsh -lc "sed -n '300,390p' research/2026-10/aaif-agntcon/codex-polish-2026-11-aaif-after-tokyo-en-r1.md
wc -l 2026-11-aaif-after-tokyo/article.en.md 2026-1 -->
<!-- codex ran: /bin/zsh -lc "nl -ba 2026-11-aaif-after-tokyo/article.md | sed -n '1,170p'" -->
The round-one fixes are present, including the clarified approval question and rollout-state wording. I’m leaving the two rejected heading suggestions closed and checking the remaining prose and tables for ambiguity and bilingual drift.
<!-- codex ran: /bin/zsh -lc "nl -ba 2026-11-aaif-after-tokyo/article.md | sed -n '170,310p'" -->
<!-- codex ran: /bin/zsh -lc "nl -ba 2026-11-aaif-after-tokyo/article.md | sed -n '310,448p'" -->
<!-- codex ran: /bin/zsh -lc "nl -ba 2026-11-aaif-after-tokyo/article.en.md | sed -n '1,190p'" -->
<!-- codex ran: /bin/zsh -lc "nl -ba 2026-11-aaif-after-tokyo/article.md | sed -n '450,532p'" -->
One consistency issue remains in the decision table: §4 defines the comparison as crashes per thousand sessions, but the later criterion says only that crashes stop rising. I’m also checking a few pronouns and translated phrases that blur the intended actor or action.
<!-- codex ran: /bin/zsh -lc "nl -ba 2026-11-aaif-after-tokyo/article.en.md | sed -n '191,352p'" -->
<!-- codex ran: /bin/zsh -lc "nl -ba 2026-11-aaif-after-tokyo/article.en.md | sed -n '353,433p'" -->
<!-- codex ran: /bin/zsh -lc "nl -ba 2026-11-aaif-after-tokyo/article.en.md | sed -n '435,483p'" -->
<!-- codex ran: /bin/zsh -lc "nl -ba 2026-11-aaif-after-tokyo/article.en.md | sed -n '484,533p'" -->
<!-- codex ran: /bin/zsh -lc "rg -n '"'^#{1,3} |G2|G3|frozen holdout|spec-change card'"' 2026-11-same-spec-spec/article.en.md 2026-11-same-spec-variance/article.en.md 2026-10-g -->
The bilingual pass is complete through the disclosure and source notes. I’ve found a few remaining wording issues, including servers being described as procedures and an incomplete expansion of API. I’m checking the replacements now to keep them local and preserve the author’s claims.
<!-- codex ran: /bin/zsh -lc "sed -n '93,118p' 2026-11-aaif-after-tokyo/article.en.md
sed -n '260,287p' 2026-11-aaif-after-tokyo/article.en.md" -->
<!-- codex ran: /bin/zsh -lc "rg -n 'read, write and|effectiveness, cost and|gave up, expressed frustration or|stays done|needs compensating|programming interface|override a tr -->
1. **[suggested] §2, “After a rate limit…” — “Failover handles…”**  
   **Exact:** “the group the regional notifications belong to is not bound by this rule.”  
   **Problem:** The notifications are not group members. The Chinese assigns membership to the agent handling them.  
   **Replacement:** “the sales-support agent's group is not bound by this rule.”

2. **[optional] §3, reading-map table, and §10, metrics table**  
   **Exact → replacement:**
   - “read, write and connection records” → “read, write, and connection records”
   - “effectiveness, cost and correctness” → “effectiveness, cost, and correctness”
   - “gave up, expressed frustration or asked for a human” → “gave up, expressed frustration, or asked for a human”

   **Problem:** These cells retain the earlier punctuation convention, while the file now predominantly uses serial commas.

3. **[suggested] §4, “Make feedback able to recognize a real improvement” — “Even after grouping…”**  
   **Exact:** “After a pause, there may be no exposure under the same trigger condition at all; with a denominator of zero, there is no way to tell whether errors under the same conditions became rarer, and so the patch cannot be judged effective; a controlled observation has to be arranged instead.”  
   **Problem:** Two semicolons join three reasoning steps, making the expanded zero-denominator explanation harder to absorb in one pass.  
   **Replacement:** “After a pause, there may be no exposure under the same trigger condition at all. With a denominator of zero, there is no way to tell whether errors under the same conditions became rarer, so the patch cannot be judged effective. A controlled observation has to be arranged instead.”

4. **[must-fix] §5, “Check the source together with the content” — “Once the procedure…”**  
   **Exact:** “two servers both offering something named "crash-investigation" cannot be treated as the same procedure on the name alone.”  
   **Problem:** This compares servers with a procedure. The Chinese compares the procedures offered by different servers.  
   **Replacement:** “two procedures offered by different servers under the name "crash-investigation" cannot be treated as the same procedure on the name alone.”

5. **[suggested] §6, “Errors need a location, and caches need a way to expire” — “She also gives numbers…”**  
   **Exact:** “so it has to learn each provider one by one.”  
   **Problem:** “Learn each provider” is an unnatural rendering of learning how each provider behaves.  
   **Replacement:** “so it has to learn how each provider behaves.”

6. **[must-fix] §7, “Private deployment redistributes operational responsibility” — “The benefit…”**  
   **Exact:** “a shared programming interface (API)”  
   **Problem:** The expansion of API is incomplete.  
   **Replacement:** “a shared application programming interface (API)”

7. **[suggested] §7, “Data boundaries must take effect at reads, writes, and connections” — “The final human review…”**  
   **Exact:** “whether it can be reversed”  
   **Problem:** “It” refers grammatically to the tool; the intended question concerns reversing its effects.  
   **Replacement:** “whether its effects can be reversed”

8. **[suggested] §8, “From a lead to a fix…” — “Moving toward a fix…”**  
   **Exact:** “a problem that appeared only on the weak network near an airport”; “recreate the network strength and the feature-flag state”  
   **Problem:** “On the weak network” and “recreate the network strength” are awkward renderings of the network conditions being reproduced.  
   **Replacements:** “a problem that appeared only when network connectivity was poor near an airport”; “recreate those network conditions and the feature-flag state”

9. **[suggested] §8, “Hand over the validation evidence…” — “The numbers also…”**  
   **Exact:** “compared against the engineers' final fixes, 50% RCA accuracy”  
   **Problem:** The opening modifier appears to attach to “accuracy”; the analyses are what were compared with the fixes.  
   **Replacement:** “50% RCA accuracy when the analyses were compared against the engineers' final fixes”

10. **[suggested] §9, “First separate a relaxed requirement from a wrong tool parameter” — “The proposal screen…”**  
    **Exact:** “the default fifteen-minute arrival tolerance may not override a traveler who has explicitly said they are unwilling to relax the requirement.”  
    **Problem:** The tolerance overrides a requirement, rather than a traveler. The Chinese names the requirement as the object.  
    **Replacement:** “the default fifteen-minute arrival tolerance may not override the requirement of a traveler who has explicitly said they are unwilling to relax it.”

11. **[suggested] §9, “First separate a relaxed requirement from a wrong tool parameter” — “If the traveler…”**  
    **Exact:** “the first case improves while the second loses a choice it was originally allowed.”  
    **Problem:** “The second” grammatically refers to the test case, attributing the traveler’s choice and permission to it.  
    **Replacement:** “the first case improves while the second traveler loses a choice they were originally allowed.”

12. **[suggested] §9, “Rolling back the instructions still leaves external state to check” — “From 13:29…”**  
    **Exact:** “it cannot recall a notification already sent or a flag already changed.”  
    **Problem:** “Recall” works for the notification but does not express undoing a flag change.  
    **Replacement:** “it cannot recall a notification already sent or undo a change already made to a flag.”

13. **[must-fix] §11, decision table, “Pause the rollout” row; and “On Monday you can also…”**  
    **Exact, table:** “Exposure stays at the approved share, and crashes under the same trigger condition stop rising”  
    **Exact, paragraph:** “an operation that succeeded while crashes under the same trigger condition are still rising”  
    **Problem:** Both revert to an unspecified crash count. §4 explicitly requires crashes **per thousand sessions**, within the same version and trigger condition, because totals can change with exposure. This remains pending in the disposition log, and the same omission remains in Chinese; both editions need alignment.  
    **Replacement, table:** “Exposure stays at the approved share, and crashes per thousand sessions within the same version and under the same trigger condition stop rising”  
    **Replacement, paragraph:** “an operation that succeeded while crashes per thousand sessions within the same version and under the same trigger condition are still rising”

14. **[suggested] §11 — “Once a quarter's worth…”**  
    **Exact:** “What the body of this article actually has to count is the cost of people taking over:”  
    **Problem:** “Has to count” reads as literal tallying; the Chinese means that the cost must be included in the accounting.  
    **Replacement:** “What the body of this article needs to account for is the cost of people taking over:”

**Counts:** 3 must-fix; 10 suggested; 1 optional. **Total: 14 findings.**

The round-one fixes are sound, and neither rejected heading suggestion is reopened. The remaining issues are local; the crash-rate criterion requires correction in both editions before publication.

<!-- tokens: in 1345220 out 14215 -->
