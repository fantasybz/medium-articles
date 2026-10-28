# Codex 校稿 — 2026-11-aaif-agent-memory/article.en.md（第 3 輪）

> model: gpt-6.1-sol, reasoning: xhigh, 2026-10-29 05:59. 原話照錄，未經摘要。

I’ll read STYLE.md first, then check the earlier findings and disposition logs before comparing the English and Chinese block by block. I’ll keep the review read-only and report only problems that remain.
<!-- codex ran: /bin/zsh -lc 'cat STYLE.md' -->
<!-- codex ran: /bin/zsh -lc 'cat research/2026-10/aaif-agntcon/codex-polish-2026-11-aaif-agent-memory-en-r2.md' -->
<!-- codex ran: /bin/zsh -lc 'cat research/2026-10/aaif-agntcon/codex-polish-2026-11-aaif-agent-memory-en-r1.md' -->
<!-- codex ran: /bin/zsh -lc 'cat .context/research/aaif-2026-10-28-polish/2026-11-aaif-agent-memory-en-r1-disposition.md' -->
<!-- codex ran: /bin/zsh -lc 'cat .context/research/aaif-2026-10-28-polish/2026-11-aaif-agent-memory-en-r2-disposition.md' -->
<!-- codex ran: /bin/zsh -lc 'cat .context/research/aaif-2026-10-28-polish/2026-11-aaif-agent-memory-en-r1-disposition.md' -->
<!-- codex ran: /bin/zsh -lc "sed -n '195,285p' research/2026-10/aaif-agntcon/codex-polish-2026-11-aaif-agent-memory-en-r1.md" -->
<!-- codex ran: /bin/zsh -lc "nl -ba 2026-11-aaif-agent-memory/article.en.md | sed -n '1,170p'" -->
<!-- codex ran: /bin/zsh -lc "nl -ba 2026-11-aaif-agent-memory/article.md | sed -n '1,170p'" -->
<!-- codex ran: /bin/zsh -lc 'cat research/2026-10/style_brief.md' -->
The round 2 edits are present and read correctly, including the revised test for a stale summary write. I’ll respect the earlier decision to retain the publication-date note and continue checking the correction workflow, tables, and final notes for remaining English issues or differences in meaning.
<!-- codex ran: /bin/zsh -lc "nl -ba 2026-11-aaif-agent-memory/article.md | sed -n '145,265p'" -->
<!-- codex ran: /bin/zsh -lc "nl -ba 2026-11-aaif-agent-memory/article.md | sed -n '266,410p'" -->
<!-- codex ran: /bin/zsh -lc "nl -ba 2026-11-aaif-agent-memory/article.en.md | sed -n '1,145p'" -->
<!-- codex ran: /bin/zsh -lc "nl -ba 2026-11-aaif-agent-memory/article.en.md | sed -n '146,265p'" -->
<!-- codex ran: /bin/zsh -lc "nl -ba 2026-11-aaif-agent-memory/article.en.md | sed -n '266,410p'" -->
The comparison through the final notes shows no new substantive translation mismatch so far. The remaining candidates are local wording issues; I’m checking the section references and proposed replacements to make sure they preserve the author’s meaning.
<!-- codex ran: /bin/zsh -lc "rg -n '—|“|”|‘|’|behaviour|behaviors|organisation|organis|colour|color|licence|license|analyse|analyz|centre|center|cancelled|canceled' 2026-11-aa -->
<!-- codex ran: /bin/zsh -lc "sed -n '447,470p' 2026-11-same-spec-variance/article.en.md" -->
<!-- codex ran: /bin/zsh -lc "rg --files 2026-10-agentic-* -g 'article.en.md'" -->
<!-- codex ran: /bin/zsh -lc "rg -n '"'^## (1'"\\.|2\\.|7\\.)' 2026-10-green-review/article.en.md 2026-10-green-testing/article.en.md 2026-10-agentic-harness-blueprint/article. -->
<!-- codex ran: /bin/zsh -lc "rg -n '"'^## (2'"\\.|8\\.|10\\.)|third way|three kinds of recheck' 2026-11-same-spec-contract/article.en.md 2026-11-same-spec-variance/article.en. -->
<!-- codex ran: /bin/zsh -lc "sed -n '232,253p' 2026-11-same-spec-variance/article.en.md" -->
<!-- codex ran: /bin/zsh -lc "sed -n '368,394p' 2026-11-same-spec-overview/article.en.md" -->
<!-- codex ran: /bin/zsh -lc "sed -n '34,53p' 2026-11-same-spec-contract/article.en.md" -->
<!-- codex ran: /bin/zsh -lc "rg --files 2026-10-* -g 'article.en.md'" -->
1. **[suggested] §5 roadmap, “This section follows one claim…”; also §5 / “Let the correction travel along the citations into the next summary,” “I would borrow…”**

   **Exact:** “fills the correction in as three records”; “the report case is filled in as three records”

   **Problem:** These are literal constructions. The records present the correction; “fill in” suggests completing missing information.

   **Replacements:** “sets out the correction in three records”; “the report case is set out in three records”

2. **[suggested] §5 / “Decide what counts as support before the results appear,” “Page 35 then moves…”**

   **Exact:** “Page 35 then moves the method of checking to before the research begins.”

   **Problem:** “Moves the method … to before” is awkward and momentarily obscures whether the method is chosen beforehand or the checking happens beforehand.

   **Replacement:** “Page 35 then turns to choosing the verification method before the research begins.”

3. **[suggested] §5 / “Let the correction travel along the citations into the next summary,” table row “New judgment J-18”**

   **Exact:** “marks the missing verification of the report's run and output”

   **Problem:** The job executes and produces the report. This cell retains the ambiguity corrected in round 2’s §6 wording.

   **Replacement:** “notes that verification of the report job's execution and output is missing”

4. **[suggested] §5 / “Let the correction travel along the citations into the next summary,” “The three records are hypothetical data…”**

   **Exact:** “Whether they are of any use will show only when”

   **Problem:** “Will show” is unidiomatic here; the intended meaning is that their usefulness will become apparent.

   **Replacement:** “Whether they are of any use will become clear only when”

5. **[suggested] §6 / “Whether a correction reaches the answer has to be checked layer by layer,” acceptance-table row “Two sources conflict…”**

   **Exact:** “Two sources conflict, and the data to tell them apart is missing”

   **Problem:** “Tell them apart” suggests distinguishing the sources’ identities rather than resolving their conflicting claims.

   **Replacement:** “Two sources conflict, and the data needed to resolve the conflict is missing”

**Counts:** must-fix **0**; suggested **5**; optional **0**. **Total: 5 findings**, grouping repeated wording.

Round 2’s fixes are correctly applied and introduce no new problems. I found no further substantive zh/en divergence or incorrect section reference; the remaining findings concern local phrasing and terminology.

<!-- tokens: in 1194603 out 11146 -->
