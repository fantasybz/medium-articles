# Codex 校稿 — 2026-11-aaif-agent-memory/article.en.md（第 2 輪）

> model: gpt-6.1-sol, reasoning: xhigh, 2026-10-29 05:49. 原話照錄，未經摘要。

I’ll read STYLE.md first, check the round 1 fixes and dispositions, then compare the English and Chinese block by block. I’ll keep the repository read-only and report only problems that remain.
<!-- codex ran: /bin/zsh -lc 'cat STYLE.md' -->
<!-- codex ran: /bin/zsh -lc 'cat research/2026-10/aaif-agntcon/codex-polish-2026-11-aaif-agent-memory-en-r1.md' -->
<!-- codex ran: /bin/zsh -lc 'cat .context/research/aaif-2026-10-28-polish/2026-11-aaif-agent-memory-en-r1-disposition.md' -->
<!-- codex ran: /bin/zsh -lc "wc -l 2026-11-aaif-agent-memory/article.en.md 2026-11-aaif-agent-memory/article.md; rg --files research/2026-11 research/2026-10 -g '*style*' -g ' -->
<!-- codex ran: /bin/zsh -lc "sed -n '1,155p' .context/research/aaif-2026-10-28-polish/2026-11-aaif-agent-memory-en-r1-disposition.md" -->
<!-- codex ran: /bin/zsh -lc "nl -ba 2026-11-aaif-agent-memory/article.md | sed -n '1,170p'" -->
<!-- codex ran: /bin/zsh -lc "sed -n '245,340p' research/2026-10/aaif-agntcon/codex-polish-2026-11-aaif-agent-memory-en-r1.md; cat research/2026-10/style_brief.md" -->
<!-- codex ran: /bin/zsh -lc "nl -ba 2026-11-aaif-agent-memory/article.en.md | sed -n '1,170p'" -->
<!-- codex ran: /bin/zsh -lc "sed -n '1,145p' 2026-11-aaif-agent-memory/article.md" -->
<!-- codex ran: /bin/zsh -lc "sed -n '146,265p' 2026-11-aaif-agent-memory/article.md" -->
The accepted round 1 fixes are present, including the reconciled headings and table cells. I’m leaving the deliberately retained publication-date note alone; I’m now checking the correction workflow and acceptance scenarios for remaining ambiguities and translation differences.
<!-- codex ran: /bin/zsh -lc "sed -n '266,378p' 2026-11-aaif-agent-memory/article.md" -->
<!-- codex ran: /bin/zsh -lc "sed -n '170,265p' 2026-11-aaif-agent-memory/article.en.md" -->
<!-- codex ran: /bin/zsh -lc "sed -n '266,379p' 2026-11-aaif-agent-memory/article.en.md" -->
<!-- codex ran: /bin/zsh -lc "cat research/2026-10/style_brief.md; sed -n '195,265p' research/2026-10/aaif-agntcon/codex-polish-2026-11-aaif-agent-memory-en-r1.md" -->
<!-- codex ran: /bin/zsh -lc "rg --files -g 'article.en.md' -g 'article.md' -g '"'!agents/**'"' -g '"'!.claude/**'"'; rg -n '—|“|”|‘|’|colour|behavior|behaviour|organis|organiz -->
<!-- codex ran: /bin/zsh -lc "rg -n '"'^## |''^### |oracle|third |owner|expiry|holdout|grader|three .*recheck|three tiers|domain'"' 2026-11-same-spec-contract/article.en.md 202 -->
The captions, table figures, and revised test-cluster scope agree across the two editions. The remaining candidates are mostly local wording and punctuation issues; I’m checking the cross-references and final notes before selecting the findings.
<!-- codex ran: /bin/zsh -lc "sed -n '1,120p' .context/research/aaif-2026-10-28-polish/memory-flags-decisions.md" -->
<!-- codex ran: /bin/zsh -lc "rg -n '"'^## '"' 2026-11-same-spec-contract/article.en.md 2026-11-same-spec-variance/article.en.md 2026-11-same-spec-overview/article.en.md 2026-1 -->
<!-- codex ran: /bin/zsh -lc "sed -n '63,71p' 2026-10-agentic-harness-blueprint/article.en.md; sed -n '9,25p' 2026-10-green-review/article.en.md; rg -n 'three kinds|yardstick|g -->
<!-- codex ran: /bin/zsh -lc "rg -n 'compares whether|no longer latest|for every kind of result|keeping every version never|The venue as photographed|let it write back|results  -->
The comparison is complete. I found no further substantive translation mismatch or incorrect section reference. I’m limiting the report to remaining article usage, question punctuation, and specific passages where the English obscures the action.
1. **[suggested] §3–§6, quoted questions at the locations below**

   **Problem:** These are the author's questions, but they end with commas or periods instead of question marks. The test questions later in §6 already use question marks.

   | Location and opening words | Exact text | Drop-in replacement |
   |---|---|---|
   | §3 / “Similarity finds the material…”; “If I ask…” | `"what problems did the last upgrade run into,"` | `"what problems did the last upgrade run into?"` |
   | Same subsection; “If the question is only…” | `"which plugin version does the production inventory record,"` | `"which plugin version does the production inventory record?"` |
   | Same subsection; “It is the next question…” | `"has matching compatibility evidence been found for the plugin that service A uses,"` | `"has matching compatibility evidence been found for the plugin that service A uses?"` |
   | §3 / “Put time and scope…”; “When choosing a data structure…” | `"B's compatibility document has changed; which services' upgrade assessments need another look,"` | `"B's compatibility document has changed; which services' upgrade assessments need another look?"` |
   | §4 / “First separate the experience…”; “For the ranking itself…” | `"can the relevant material be found."` | `"can the relevant material be found?"` |
   | §6 opening; “Now that I have read…” | `"does it still remember after a restart."` | `"does it still remember after a restart?"` |

2. **[suggested] §3 / “Similarity finds the material…”; “If I ask…”**

   **Exact:** “a search compares whether the representation of the question and that of a note are close”

   **Problem:** “Compares whether” is an unnatural construction: the representations are compared; their closeness is assessed.

   **Replacement:** “a search compares the question's representation with that of a note to see whether they are close”

3. **[suggested] §4 / “First separate the experience…”; “For the ranking itself…”**

   **Exact:** “Strings such as the plugin name `plugin-c` or the error message `CrashLoopBackOff` can be hit directly by word matching and ranked by lexical relevance”

   **Problem:** “Can be hit directly” is a calque. The construction also makes the strings themselves, rather than matching records, the objects being ranked.

   **Replacement:** “Word matching can directly find strings such as the plugin name `plugin-c` or the error message `CrashLoopBackOff` and rank the matching records by lexical relevance”

4. **[must-fix] §4 / “A statement that keeps recurring…”; “Consolidation, forgetting, and search…”; also / “Updating and forgetting…”; “Updating also has a shortcut…”**

   **Exact:** “marks the older record as no longer latest”; “marks the earlier-created one as no longer latest”

   **Problem:** “Latest” needs the definite article here.

   **Replacements:** “marks the older record as no longer the latest”; “marks the earlier-created one as no longer the latest”

5. **[suggested] §5 / “Decide what counts as support…”; “Page 35 then moves…”**

   **Exact:** “makes it easy for every kind of result to find an account that looks like success”

   **Problem:** The literal phrasing makes a result the actor finding an explanation.

   **Replacement:** “makes it easy to frame any kind of result as a success”

6. **[suggested] §5 / “Decide what counts as support…”; “Page 35 then moves…”**

   **Exact:** “otherwise, keeping every version never turns into a maintenance decision”

   **Problem:** Keeping versions does not itself “turn into” a decision. The intended connection to choosing the necessary maintenance action is obscured.

   **Replacement:** “otherwise, keeping every version still does not tell us which maintenance action to take”

7. **[suggested] §5 / “The observations have not changed…”; figure caption beginning “The venue as photographed…”**

   **Exact:** “The venue as photographed by the author on September 10, 2026, corresponding to page 40 of Wataru Kumagai's deck:”

   **Problem:** “Corresponding to page 40” appears to modify the venue rather than the photographed slide.

   **Replacement:** “The author's photograph, taken at the venue on September 10, 2026, shows the slide on page 40 of Wataru Kumagai's deck:”

8. **[optional] §6 / “Whether a correction reaches the answer…”; “For the correction case…”**

   **Exact:** “let it write back after the withdrawal completes, and check whether the write is blocked”

   **Problem:** “Let it write back” can imply that the write succeeds, although the test checks whether it is blocked.

   **Replacement:** “let it attempt to write back after the withdrawal completes, and check whether the write is blocked”

9. **[suggested] §6 / “Whether a correction reaches the answer…”; “After the update…”**

   **Exact:** “ask the service owner to supply the results of running the report and its output”

   **Problem:** “Running the report” blurs the distinction between the report job and its output; “results … and its output” is also awkwardly coordinated.

   **Replacement:** “ask the service owner to supply the report job's execution results and output”

10. **[suggested] §6 / “Which results support widening…”; “These scenarios are a diagnostic pilot…”**

    **Exact:** “and the reading of conflicts goes to the owner”

    **Problem:** “The reading of conflicts goes to” is a calque that obscures the assigned action.

    **Replacement:** “and the owner interprets conflicting evidence”

11. **[suggested] §6 / “Which results support widening…”; “These scenarios are a diagnostic pilot…”**

    **Exact:** “Once the diagnostic cases pass, move to a small trial that keeps human approval: it is limited to this kind of upgrade assessment, each use is approved by the service owner, it stops as soon as a correction fails to reach the answer, it is owned by the maintainer of the memory system, and the actual handover and maintenance costs are recorded.”

    **Problem:** Five clauses after the colon make the scope, approval, stopping condition, ownership, and recordkeeping difficult to retain in one pass.

    **Replacement:** “Once the diagnostic cases pass, move to a small trial that retains human approval and is limited to this kind of upgrade assessment. Each use is approved by the service owner, and the trial stops as soon as a correction fails to reach the answer. The trial is owned by the maintainer of the memory system, and the actual handover and maintenance costs are recorded.”

12. **[suggested] §7; “This checking changed…”**

    **Exact:** “The evidence still missing has to be stated too: a comparison of storage, tool responses, context, and answers from before and after a correction, for which this article has only static checks and a test design.”

    **Problem:** The trailing “for which” blurs the distinction between the missing comparison and the static work actually completed. The Chinese states these separately.

    **Replacement:** “The evidence still missing has to be stated too: a comparison of storage, tool responses, context, and answers from before and after a correction. This article has only static checks and a test design.”

**Counts:** must-fix **1**; suggested **10**; optional **1**. **Total: 12 findings**, grouping repeated occurrences.

Round 1's accepted corrections hold, and I found no further substantive zh/en divergence or incorrect section reference. The remaining issues are local copy edits.

<!-- tokens: in 1220126 out 16066 -->
