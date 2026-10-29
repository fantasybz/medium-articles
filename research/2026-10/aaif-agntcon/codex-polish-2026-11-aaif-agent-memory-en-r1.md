# Codex 校稿 — 2026-11-aaif-agent-memory/article.en.md（第 1 輪）

> model: gpt-6.1-sol, reasoning: xhigh, 2026-10-29 05:16. 原話照錄，未經摘要。

I’ll read STYLE.md first, then compare the English and Chinese block by block, including captions, tables, and final notes. I’ll keep everything read-only and report only specific problems with drop-in fixes.

<!-- codex ran: /bin/zsh -lc 'cat STYLE.md' -->
<!-- codex ran: /bin/zsh -lc 'wc -l 2026-11-aaif-agent-memory/article.en.md 2026-11-aaif-agent-memory/article.md' -->
<!-- codex ran: /bin/zsh -lc 'nl -ba 2026-11-aaif-agent-memory/article.en.md' -->
<!-- codex ran: /bin/zsh -lc 'nl -ba 2026-11-aaif-agent-memory/article.md' -->
<!-- codex ran: /bin/zsh -lc "rg --files -g 'style_brief.md' -g 'AGENTS.md' -g '*contract*' -g '*variance*' -g '*style*' -g '"'!agents/**'"' -g '"'!.claude/**'"'" -->
<!-- codex ran: /bin/zsh -lc "sed -n '105,190p' 2026-11-aaif-agent-memory/article.md" -->
The opening and graph-memory sections track the Chinese closely. I’m seeing some literal English phrasing that obscures the action or referent; I’m checking those alongside the correction workflow and tables, where small wording differences could affect the argument.

<!-- codex ran: /bin/zsh -lc "sed -n '191,270p' 2026-11-aaif-agent-memory/article.md" -->
<!-- codex ran: /bin/zsh -lc "sed -n '271,378p' 2026-11-aaif-agent-memory/article.md" -->
<!-- codex ran: /bin/zsh -lc "sed -n '160,265p' 2026-11-aaif-agent-memory/article.en.md" -->
I’ve found a few places where the English creates a stronger ambiguity than the Chinese, particularly around retries and withdrawn judgments. I’m now checking the acceptance scenarios, closing paragraphs, and notes against the earlier definitions and claims.

<!-- codex ran: /bin/zsh -lc "sed -n '1,160p' 2026-11-aaif-agent-memory/article.en.md" -->
<!-- codex ran: /bin/zsh -lc "sed -n '266,379p' 2026-11-aaif-agent-memory/article.en.md" -->
<!-- codex ran: /bin/zsh -lc "rg -n 'November 16|health check|re-verif|acceptance|oracle|Handoff|handover|hand-off|expiry|expiration|—|“|”|‘|’' 2026-11-aaif-agent-memory/articl -->
<!-- codex ran: /bin/zsh -lc "rg --files -g 'article.en.md' -g 'article.md' -g '"'!agents/**'"' -g '"'!.claude/**'"'" -->
<!-- codex ran: /bin/zsh -lc "rg -n '"'^## |''^### |oracle|third way|three .*recheck|section 8|owner|expiry|holdout|three tiers|grader'"' 2026-10-agentic-harness-blueprint/arti -->
The block comparison is complete. The substantive findings include an added publication date, “safe to upgrade” where the Chinese says only “can be upgraded,” and “re-verification” for a report check that never ran. I’m making a final pass over the replacements to preserve the author’s judgments and leave source quotations untouched.

1. **[suggested] §TL;DR, “When an agent remembers…”; also §1, “The first two articles…”**  
   **Exact:** “after a piece of experience has been carried into another environment, found to be missing a check, or formally corrected”  
   **Problem:** “A piece of experience” is a calque, and the compressed passive sequence makes the missed check difficult to interpret.  
   **Replacement:** “after prior experience is reused in a different environment, a missed check is discovered, or a formal correction is made”

2. **[suggested] §TL;DR, “When an agent remembers…”; §2 heading; §4 first subsection and its roadmap**  
   **Exact:** “what one round of work needs to read”; “what this round needs to read”  
   **Problem:** A round of work cannot read; the English carries over an omitted actor from Chinese.  
   **Replacements:** “what an agent needs to read during one round of work”; “what needs to be read this round”  
   Apply the second replacement to both headings and the quoted subsection title in §4’s roadmap.

3. **[must-fix] §Opening note, “Part 3 of my AAIF Tokyo notes…”**  
   **Exact:** “This English edition is planned for November 18, 2026, following the Chinese edition on November 16.”  
   **Problem:** The November 16 publication date is added information absent from the Chinese block.  
   **Replacement:** “This English edition is planned for November 18, 2026.”

4. **[suggested] §2, “The article recommends three countermeasures…”**  
   **Exact:** “A long run of health-check output (a health check is a short request confirming that the service can still respond; it does not prove that the report was actually produced) is condensed into a result such as ‘check passed, but the report has not been accepted.’”  
   **Problem:** The long parenthesis separates the subject from its verb and interrupts the example.  
   **Replacement:** “A long run of health-check output is condensed into a result such as ‘check passed, but the report has not been accepted.’ Here, a health check is a short request confirming that the service can still respond; it does not prove that the report was actually produced.”  
   Retain the file’s straight double quotation marks around the example.

5. **[must-fix] §2, “The earlier result came with…”**  
   **Exact:** “safe to upgrade”  
   **Problem:** “Safe” strengthens the Chinese “可以升級” and differs from the article’s recurring formulation “can be upgraded.”  
   **Replacement:** “can be upgraded”

6. **[suggested] §2 reading-map table, “Connect conclusions back to observations”; also §5 opening**  
   **Exact:** `What exactly did "upgrade successful" observe?`; “what did a remembered conclusion actually observe?”  
   **Problem:** A conclusion does not perform observations. The literal phrasing obscures the question about underlying evidence.  
   **Replacements:** `What was actually observed when the upgrade was called successful?`; “what observations underlie a remembered conclusion?”

7. **[suggested] §3 / “Put time and scope into the relationships,” “This also explains…”**  
   **Exact:** “For each relationship, record the period in which it was observed or valid separately from the time the system ingested it, because an old deployment record entered today still belongs to the old environment, and a later acquisition date does not mean the record is closer to the present state.”  
   **Problem:** The instruction and two explanations accumulate in one sentence, making the distinction between validity and ingestion hard to retain.  
   **Replacement:** “For each relationship, record the period in which it was observed or valid separately from the time the system ingested it. An old deployment record entered today still belongs to the old environment; obtaining it later does not mean it is closer to the present state.”

8. **[suggested] §3 / “Put time and scope into the relationships,” “When choosing a data structure…”**  
   **Exact:** “And switching storage does not by itself obtain the current deployment”  
   **Problem:** “Obtain the current deployment” can suggest deploying software rather than obtaining deployment information.  
   **Replacement:** “And switching storage does not by itself retrieve information about the current deployment”

9. **[suggested] §4 introduction, “For yesterday’s decisions to come back today…”**  
   **Exact:** “then looks at why the rankings from BM25, vector search, and RRF cannot decide which judgment is still valid”  
   **Problem:** BM25 and RRF appear before their explanations. The roadmap requires unfamiliar readers to interpret both acronyms.  
   **Replacement:** “then looks at why word matching, vector search, and their combined rankings cannot decide which judgment is still valid”

10. **[suggested] §4 / “First separate the experience…,” procedural-memory table row**  
    **Exact:** “a revised procedure keeps a version”  
    **Problem:** The action is unclear: a procedure does not itself keep a version.  
    **Replacement:** “a version is recorded whenever the procedure is revised”

11. **[suggested] §4 / “First separate the experience…,” figure caption, “Rohit Ghumare and Vinuja Khatode…”**  
    **Exact:** “each carry a different memory job”  
    **Problem:** “Carry a job” is an unnatural collocation carried over from Chinese.  
    **Replacement:** “each serve a different role in memory”

12. **[suggested] §4 / “First separate the experience…,” “For the ranking itself…”**  
    **Exact:** “The test uses the 500 questions of LongMemEval-S, each of which builds its search data from roughly 48 conversation sessions of its own.”  
    **Problem:** The question is incorrectly presented as the actor building the search data; “of its own” is also cumbersome.  
    **Replacement:** “The test uses 500 LongMemEval-S questions, each with search data drawn from its own set of roughly 48 conversation sessions.”

13. **[suggested] §4 / “A statement that keeps recurring…,” “Search can only find existing records…”**  
    **Exact:** “so that future work need not reread every process”  
    **Problem:** Work cannot reread, and a process is not something one reads.  
    **Replacement:** “so that later sessions need not reread every account of how the work unfolded”

14. **[optional] §4 / “A statement that keeps recurring…,” “Consolidation, forgetting, and search…”**  
    **Exact:** “semantic, memories, and observations”  
    **Problem:** These are literal collection names, but their presentation makes “semantic” look like an unattached adjective. Other implementation identifiers use code formatting.  
    **Replacement:** “`semantic`, `memories`, and `observations`”  
    Use the same formatting for subsequent references to these collection names within this paragraph.

15. **[suggested] §4 / “Updating and forgetting…,” “Nor should ‘unused for a long time’…”**  
    **Exact:** “What is new when that is applied to automatically consolidated memory is how that human review responsibility lands on the memory and its copies.”  
    **Problem:** “Responsibility lands on the memory” is a calque that obscures who is responsible for reviewing what.  
    **Replacement:** “For automatically consolidated memory, the new question is how to assign responsibility for human review of the memory and its copies.”

16. **[suggested] §4 / “Updating and forgetting…,” “Nor should ‘unused for a long time’…”**  
    **Exact:** `An "approved" in old memory serves only as a historical record and cannot become the permission for this operation`  
    **Problem:** The quoted adjective needs a noun, and “become the permission” is unnatural.  
    **Replacement:** `An "approved" status in old memory serves only as a historical record and cannot authorize the current operation`

17. **[suggested] §4 / “Updating and forgetting…,” “Go back to the hypothetical memory…”**  
    **Exact:** “none of them tells us whether this sentence could have been written from a single test rehearsal in the first place.”  
    **Problem:** “Could have been written” asks whether writing it was possible, rather than whether the evidence justified it.  
    **Replacement:** “none of them tells us whether a single test rehearsal justified that statement in the first place.”

18. **[suggested] §5 / “Decide what counts as support…,” “Page 35 then moves…”**  
    **Exact:** “Defining in advance limits changing the story afterward, and it can also miss a valuable new discovery.”  
    **Problem:** “Defining” lacks its object, and “it” awkwardly makes the act of defining responsible for missing a discovery.  
    **Replacement:** “Defining the verification method in advance limits later changes to the story, but it can also cause a valuable new discovery to be missed.”

19. **[suggested] §5 / “Decide what counts as support…,” “Page 35 then moves…”**  
    **Exact:** “which must be rerun because a necessary measurement is missing”  
    **Problem:** The grammatical antecedent is “old judgments”; judgments are re-evaluated, whereas executions are rerun.  
    **Replacement:** “which require a new run because a necessary measurement is missing”

20. **[suggested] §5 / “Let the correction travel…,” table row “Old judgment J-17”**  
    **Exact:** “cites observations O-41, node version 1.31, and O-42, health check passed”  
    **Problem:** The commas blur the boundaries between the two observation identifiers and their descriptions.  
    **Replacement:** “cites O-41 (node version 1.31) and O-42 (health check passed)”

21. **[suggested] §5 / “Let the correction travel…,” table row “Old judgment J-17”**  
    **Exact:** “Withdrawn, because the report was paused during the rehearsal and was consolidated as passed without any result”  
    **Problem:** This makes the report itself the thing consolidated. The Chinese describes an unsupported judgment that everything passed.  
    **Replacement:** “Withdrawn because the report job was paused during the rehearsal, yet the summary recorded all required functions as passed without any report result”

22. **[suggested] §5 / “Let the correction travel…,” “There is also an ordering…”**  
    **Exact:** “does not check the basis at write time”; “the check of the basis version”  
    **Problem:** “Basis” and “basis version” are compressed, undefined labels for the supporting judgment and its version.  
    **Replacements:** “does not check the supporting judgment’s version at write time”; “the check of the supporting judgment’s version”

23. **[must-fix] §5 / “Let the correction travel…,” “There is also an ordering…”**  
    **Exact:** “A retry after an interruption must not restore a withdrawn state either.”  
    **Problem:** “Restore a withdrawn state” can mean restoring the status *withdrawn*, which reverses the intended prohibition against reviving the judgment.  
    **Replacement:** “A retry after an interruption must not reinstate a withdrawn judgment either.”

24. **[must-fix] §5 / “Let the correction travel…,” “There is also an ordering…”**  
    **Exact:** “an answer that has already loaded the old context and is output later has to carry the judgment version it rests on, so that it can be recognized afterward.”  
    **Problem:** An answer cannot load context. The final “it” also leaves unclear what must be recognized.  
    **Replacement:** “an answer produced later from context loaded before that point has to carry the version of the judgment it rests on, so that its basis can be identified afterward.”

25. **[suggested] §6 heading and opening, “Now that I have read…”**  
    **Exact:** “How I would run acceptance on the next task’s memory”; `Now that I have read the three sessions this far, what I want to put through acceptance is no longer "does it still remember after a restart."`  
    **Problem:** “Run acceptance on” and “put through acceptance” are literal translations rather than idiomatic names for acceptance testing.  
    **Replacements:** “How I would run acceptance tests on memory for the next task”; “After reading these three sessions, I no longer want acceptance testing to focus on whether the agent remembers after a restart.”

26. **[suggested] §6 / “First confirm that memory saves…,” “Every trial is restored…”**  
    **Exact:** “Every trial is restored to the same starting test data, search catalog included, which means a fixed memory snapshot and index version.”; “When testing retrieval, fix the write results; only when testing the update flow are the corresponding writes enabled.”  
    **Problem:** A trial is not restored to data; the test state is restored before a trial. “Fix the write results” can mean repair them rather than hold them constant.  
    **Replacements:** “Before every trial, restore the same starting test data, including the search catalog, so that the memory snapshot and index version are fixed.”; “When testing retrieval, hold the stored results of writes fixed; enable the corresponding writes only when testing the update flow.”

27. **[suggested] §6 / “Whether a correction reaches the answer…,” “For the correction case…”**  
    **Exact:** “which required functions did service A’s last 1.31 rehearsal accept?”  
    **Problem:** “Accept” is an unnatural verb for what a rehearsal does to functions.  
    **Replacement:** “which of service A’s required functions underwent acceptance testing in its last 1.31 rehearsal?”

28. **[suggested] §6 / “Which results support widening…,” “These tests also have to avoid…”**  
    **Exact:** `without compressing them into a single "memory accuracy."`  
    **Problem:** “Accuracy” lacks the countable head noun required by “a single” here.  
    **Replacement:** `without compressing them into a single "memory accuracy" metric.`

29. **[suggested] §6 / “Which results support widening…,” “These tests also have to avoid…”**  
    **Exact:** “Each case hands over one record: the case, the expected judgment, the stored state, the tool responses, the context actually loaded, the final answer, the human checking time, and who is responsible for the failure.”  
    **Problem:** A case cannot hand something over, and the repeated “case” obscures the intended record contents.  
    **Replacement:** “For each case, provide one record containing the case description, the expected judgment, the stored state, the tool responses, the context actually loaded, the final answer, the human checking time, and who is responsible for the failure.”

30. **[suggested] §6 roadmap; §6 / “Which results support widening…,” acceptance card and “These scenarios are a diagnostic pilot…”**  
    **Exact:** “three-stage exit from a diagnostic pilot to wider use”; “Human exits”; “The exits therefore come in three stages.”  
    **Problem:** “Exit” is used as an unexplained translation of 出口. In English, these passages describe progression, decision authority, and backup responsibility.  
    **Replacements:** “three stages for moving from a diagnostic pilot to wider use”; “Human authority and backup”; “Moving toward wider use therefore has three stages.”

31. **[suggested] §6 / “Which results support widening…,” “Two other boundaries mark…”**  
    **Exact:** “a question set that passes in full can only catch regressions and gives no signal for improvement.”  
    **Problem:** The agent passes the questions; the question set itself does not pass.  
    **Replacement:** “once the agent passes every question in a set, that set can only catch regressions and gives no signal for improvement.”

32. **[suggested] §6 / “Which results support widening…,” “These scenarios are a diagnostic pilot…”**  
    **Exact:** “Only with evidence of benefit and maintenance from representative work does expansion come up for discussion.”  
    **Problem:** “Evidence of maintenance” is unclear; the preceding sentence identifies maintenance costs as the evidence to collect.  
    **Replacement:** “Only after representative work provides evidence about benefits and maintenance effort does expansion come up for discussion.”

33. **[must-fix] §7, “My Facebook post saying farewell…”**  
    **Exact:** `the photograph below shows SHIBUYA SKY's "天空夢祭" exhibition, taken the evening before.`  
    **Problem:** “Taken the evening before” attaches grammatically to “exhibition” rather than “photograph.”  
    **Replacement:** `the photograph below, taken the evening before, shows SHIBUYA SKY's "天空夢祭" exhibition.`

34. **[must-fix] §7, “This checking changed…”; also §4 / “A statement that keeps recurring…,” “Search can only find…”**  
    **Exact:** “The re-verification of the report and the compatibility confirmation for production become preconditions for release”; “later re-verification”  
    **Problem:** The Chinese says 補驗: completing a missing check. “Re-verification” implies an earlier verification, contradicting the example’s central fact that the report check never ran.  
    **Replacements:** “Completing the missing report verification and confirming compatibility for production become preconditions for release”; “later verification to fill the gaps”

35. **[suggested] §Sources and method, “The Anthropic engineering article…”**  
    **Exact:** “The four official slides keep their full pages, and the two Agent Memory slides were rendered from the official PPTX.”  
    **Problem:** Slides do not “keep their full pages”; this is a literal translation of the statement about uncropped images.  
    **Replacement:** “The four official slide images each show a complete page; the two Agent Memory slides were rendered from the official PPTX.”

**Counts:** must-fix **6**; suggested **28**; optional **1**. **Total: 35 findings.**

This version needs another correction pass before press. The principal risks are the added date, the stronger upgrade wording, and ambiguity around withdrawn judgments and the report check that never ran.

<!-- tokens: in 737880 out 21459 -->
