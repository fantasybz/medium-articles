# Codex 校稿 — 2026-11-aaif-after-tokyo/article.en.md（第 1 輪）

> model: gpt-6.1-sol, reasoning: xhigh, 2026-10-28 23:34. 原話照錄，未經摘要。

I’ll read `STYLE.md` first, then compare the English and Chinese block by block, including captions, tables, references, and final notes. I’ll keep the review read-only and stay inside the repository.
<!-- codex ran: /bin/zsh -lc 'cat STYLE.md' -->
<!-- codex ran: /bin/zsh -lc 'wc -l 2026-11-aaif-after-tokyo/article.en.md 2026-11-aaif-after-tokyo/article.md' -->
<!-- codex ran: /bin/zsh -lc "sed -n '1,220p' 2026-11-aaif-after-tokyo/article.en.md" -->
<!-- codex ran: /bin/zsh -lc "sed -n '1,220p' 2026-11-aaif-after-tokyo/article.md" -->
<!-- codex ran: /bin/zsh -lc "rg --files -g 'AGENTS.md' -g 'style_brief.md' -g '*voice*' -g '"'!agents/**'"' -g '"'!.claude/**'"' -g '"'!**/agents/**'"'" -->
<!-- codex ran: /bin/zsh -lc "sed -n '165,290p' 2026-11-aaif-after-tokyo/article.md" -->
<!-- codex ran: /bin/zsh -lc "sed -n '130,168p' 2026-11-aaif-after-tokyo/article.md" -->
<!-- codex ran: /bin/zsh -lc "sed -n '290,410p' 2026-11-aaif-after-tokyo/article.md" -->
The comparison has turned up a clear parity error: “In another session” in §3 can read as another conference talk, where the Chinese means another agent run. I’m also checking the rollout-state example and the later cross-references for consistency.
<!-- codex ran: /bin/zsh -lc "sed -n '410,532p' 2026-11-aaif-after-tokyo/article.md" -->
<!-- codex ran: /bin/zsh -lc "rg --files -g '*.md' -g '"'!agents/**'"' -g '"'!.claude/**'"' -g '"'!**/agents/**'"' -g '"'!**/node_modules/**'"' -g '"'!**/.git/**'"'" -->
<!-- codex ran: /bin/zsh -lc "nl -ba 2026-11-aaif-after-tokyo/article.en.md | sed -n '220,355p'" -->
<!-- codex ran: /bin/zsh -lc "rg -n '"'^#{1,3} |comparison slots|handover|handing over|takeover|human|名額|接手'"' 2026-11-same-spec-spec/article.en.md 2026-11-same-spec-variance/a -->
<!-- codex ran: /bin/zsh -lc "rg -n '"'^#{1,3} |G2|G3|golden|frozen|constraint'"' 2026-10-green-reliability/article.en.md 2026-11-agentic-eval-economics/article.en.md 2026-10-g -->
<!-- codex ran: /bin/zsh -lc "sed -n '312,334p' 2026-11-same-spec-variance/article.en.md" -->
<!-- codex ran: /bin/zsh -lc "rg -n '"'^#{1,3} '"' 2026-11-same-spec-spec/article.en.md 2026-11-same-spec-variance/article.en.md 2026-10-green-reliability/article.en.md 2026-11 -->
I’ve completed the bilingual pass through the final notes. Most findings are local wording fixes, but a few affect meaning: §5 drops who approved the procedure, §11 says a pause reduced exposure despite the earlier hold-at-10% definition, and the source note’s “seven talks cited here” needs a narrower scope. I’m now checking the replacements against the surrounding text.
<!-- codex ran: /bin/zsh -lc "sed -n '512,533p' 2026-11-aaif-after-tokyo/article.en.md" -->
<!-- codex ran: /bin/zsh -lc "sed -n '392,465p' 2026-11-aaif-after-tokyo/article.en.md" -->
<!-- codex ran: /bin/zsh -lc "rg -n '11.?09|11.?9|11.?11|11.?16|11.?18|English|英文|週三|Wednesday' research/2026-10/aaif-agntcon/publication.md 2026-11-aaif-agent-handoffs/publish -->
The final check is complete. I’ve kept the replacements to local edits and left the quoted material intact. Findings shared by both languages are marked so they can be corrected together.
1. **[must-fix] §TL;DR — “My judgment”**  
   **Exact:** “a piece of evidence whose criteria have been confirmed, whose scope of observation is clear, and which the agent cannot relax or approve on its own”  
   **Problem:** The final relative clause makes *evidence* the object of “relax.” The criteria and approval authority need distinct objects.  
   **Replacement:** “a piece of evidence with confirmed criteria and a clear scope of observation, with no authority for the agent to relax those criteria or approve the result on its own”

2. **[suggested] §1 — “By the time I left”**  
   **Exact:** “what I wrote was still”  
   **Problem:** A calque that delays the subject and action.  
   **Replacement:** “I was still writing”

3. **[optional] §2 — “On September 10”**  
   **Exact:** “tried its three scenarios — the full workflow, failover and cost control — and”  
   **Problem:** Paired em dashes interrupt the main action; parentheses would follow the requested sparing use of em dashes.  
   **Replacement:** “tried its three scenarios (the full workflow, failover and cost control) and”

4. **[suggested] §2 — “This section therefore”**  
   **Exact:** “what still has to be checked once it has been”  
   **Problem:** The suspended passive requires the reader to reconstruct “passed to a fallback model.”  
   **Replacement:** “what still has to be checked after the switch”

5. **[suggested] §2, “Failover only answers who responds” — “In that day's post”**  
   **Exact:** “a request that is being served again should not simply rejoin the original steps”  
   **Problem:** A request cannot naturally “rejoin” a sequence of work steps.  
   **Replacement:** “work should not simply resume from where it stopped once requests can be served again”

6. **[suggested] §2, “After a rate limit…” — “Failover handles”**  
   **Exact:** “The token here is the unit models are billed in”  
   **Problem:** Models themselves are not billed; the sentence also introduces the generic term awkwardly.  
   **Replacement:** “Here, a token is a unit used to bill for model usage”

7. **[suggested] §3 — “The same conference”**  
   **Exact:** “yet only five agent work sessions actually succeeded; the one that failed was a run in which”  
   **Problem:** The already long sentence adds another nested explanation after the semicolon. A sentence break separates the result from the explanation.  
   **Replacement:** “yet only five agent work sessions actually succeeded. The one that failed was a run in which”

8. **[must-fix] §3 — “The same conference”**  
   **Exact:** “In another session”  
   **Problem:** In a conference article, this can mean another talk. The Chinese means another agent work session within the NTT study.  
   **Replacement:** “In another agent work session”

9. **[suggested] §3, reading-map table, MCP keynote row**  
   **Exact:** “on whose behalf, and for which task, it is acting right now”  
   **Problem:** “It” has no clear antecedent in this cell; the nearby nouns are feedback and judgment.  
   **Replacement:** “on whose behalf, and for which task, the agent is acting right now”

10. **[suggested] §3, reading-map table, Logfire row**  
    **Exact:** “regression on held-out cases”  
    **Problem:** “Regression” can mean deterioration rather than the missing verification activity.  
    **Replacement:** “regression testing on held-out cases”

11. **[suggested] §4, heading — “Code has compilers”**  
    **Exact:** “What tells other work it went wrong?”  
    **Problem:** “Work” is awkwardly treated as the recipient of feedback.  
    **Replacement:** “What provides feedback when other work goes wrong?”

12. **[suggested] §4, closing judgment — “Once the tools”**  
    **Exact:** “keep both task progress and the authority to act on verifiable grounds”  
    **Problem:** “Task progress” does not naturally rest “on grounds.” The Chinese asks for evidence by which both can be checked.  
    **Replacement:** “make both task progress and the authority to act verifiable”

13. **[must-fix] §5, introduction — “Ola Hungerford”**  
    **Exact:** “which approved version of the procedure did the agent actually receive?”  
    **Problem:** The Chinese explicitly asks *who approved* the version received. That ownership question disappears in English.  
    **Replacement:** “who approved the version of the procedure the agent actually received?”

14. **[optional] §5 — “Think of the new colleague”**  
    **Exact:** “an SOP folder”  
    **Problem:** SOP appears without expansion, despite the article’s otherwise careful introduction of terms.  
    **Replacement:** “a standard operating procedure (SOP) folder”

15. **[must-fix] §5, “Check the source together with the content” — “In section 2”**  
    **Exact:** “the automated build pipeline (CI)”  
    **Problem:** This does not expand CI correctly and differs from the full term supplied in Chinese and later in §7.  
    **Replacement:** “the continuous integration (CI) pipeline”

16. **[suggested] §5, “When validating an update…” — “What the research measures”**  
    **Exact:** “What the research measures is the difference in benefit; it does not vouch for the validation of an authorization change, but it does support checking item by item.”  
    **Problem:** “Vouch for the validation” obscures what the research does and does not support.  
    **Replacement:** “The research measures differences in benefit; it does not validate changes to authorization requirements, but it does support checking results item by item.”

17. **[suggested] §6, closing judgment — “Whether to retry”**  
    **Exact:** “Whether to retry should be decided jointly by”  
    **Problem:** The following items are grounds for a decision, not parties making it.  
    **Replacement:** “The decision to retry should rest on”

18. **[suggested] §7, “Data boundaries…” — “The speaker lists”**  
    **Exact:** “at what moment each of these controls sits”  
    **Problem:** An unnatural translation of the controls’ position in the workflow.  
    **Replacement:** “where in the workflow each of these controls takes effect”

19. **[must-fix] §7, “Verify at the same time…” — “Continuing the crash case”**  
    **Exact:** “only the designated directory can be written”  
    **Problem:** The intended meaning requires “written to”; a directory is not the content being written.  
    **Replacement:** “only the designated directory can be written to”

20. **[suggested] §7, “Verify at the same time…” — “The two sets of results”**  
    **Exact:** “At the end of the recording, the build result is still being confirmed, and the frame at 28:00 shows a compilation error.”  
    **Problem:** The paragraph abruptly switches from the author’s proposed acceptance case to the recorded demonstration. The Chinese explicitly marks this return.  
    **Replacement:** “In the talk itself, the build result is still being confirmed at the end of the recording, and the frame at 28:00 shows a compilation error.”

21. **[suggested] §8, subsection heading — “Fix the data-collection path”**  
    **Exact:** “Fix the data-collection path, and leave judgment to the steps that need reasoning”  
    **Problem:** In this context, “fix” readily means repair. The Chinese means establish a fixed workflow.  
    **Replacement:** “Use a fixed data-collection path, and leave judgment to the steps that need reasoning”

22. **[suggested] §8, “Fix the data-collection path…” — “On top of those sources”**  
    **Exact:** “missing data must not keep flowing into the RCA”  
    **Problem:** Missing data cannot flow; the intended prohibition concerns continuing analysis without it.  
    **Replacement:** “RCA must not continue with missing data”

23. **[suggested] §8, “From a lead to a fix…” — “Moving toward a fix”**  
    **Exact:** “then built and tested repeatedly until it passed or hit the retry limit”  
    **Problem:** “It” could refer to the simulator, feature-flag state, build, or test.  
    **Replacement:** “then repeated the build-and-test cycle until the tests passed or the retry limit was reached”

24. **[suggested] §8, “From a lead to a fix…” — “Start with an example”**  
    **Exact:** “another patch keeps the error and the retry entry point, and does not crash either”  
    **Problem:** “Keeps the error” can suggest preserving the defect; “retry entry point” is an awkward rendering of the user’s retry option.  
    **Replacement:** “another patch preserves the error state and the option to retry while also preventing the crash”

25. **[suggested] §8, subsection heading — “Hand over the validation evidence”**  
    **Exact:** “the PR becomes something another engineer can take”  
    **Problem:** The intended phrasal verb is “take over,” consistent with the article’s central handoff terminology.  
    **Replacement:** “the PR becomes something another engineer can take over”

26. **[suggested] §8, “Hand over the validation evidence…” — “The workflow is packaged”**  
    **Exact:** “the same series'”  
    **Problem:** The most recently named series is Green Is Not Done, whereas the organization piece belongs to Agentic Engineering.  
    **Replacement:** “the Agentic Engineering series'”

27. **[suggested] §8, “Hand over the validation evidence…” — “The numbers also”**  
    **Exact:** “According to the slides and the spoken talk:”  
    **Problem:** The colon follows an introductory prepositional phrase rather than a complete lead-in.  
    **Replacement:** “The slides and the talk report the following:”

28. **[suggested] §9, “First separate a relaxed requirement…” — “The second kind of error”**  
    **Exact:** “The second kind of error is very cheap to prevent.”  
    **Problem:** The Chinese identifies one inexpensive preventive method; English generalizes the inexpensive prevention to the error category itself.  
    **Replacement:** “There is a very cheap way to prevent the second kind of error.”

29. **[suggested] §9, “Turn production failures into tests…” — “Evals prepared in advance”**  
    **Exact:** “mixing the source of the criteria with the role”  
    **Problem:** “The role” is unspecified, leaving the central separation unclear.  
    **Replacement:** “combining the role that sets the criteria with the role that judges the result”

30. **[suggested] §10, “Five metrics…” — “She argues”**  
    **Exact:** “each corresponding to one kind of user reaction”  
    **Problem:** The last item, the agent crossing the line, is agent behavior rather than a user reaction. This mismatch also occurs in Chinese.  
    **Replacement:** “each capturing an aspect of the interaction”

31. **[suggested] §10, metrics table, Ping Pong Rate row**  
    **Exact:** “The turn at which the first resolution occurred, averaged”  
    **Problem:** Unlike the other cells under “Numerator over denominator,” this leaves the denominator implicit.  
    **Replacement:** “Sum of the turn numbers at first resolution, divided by the number of resolved conversations”

32. **[suggested] §11, introduction — “Now let the hypothetical”**  
    **Exact:** “a scorer counts only once it has been calibrated”  
    **Problem:** Beside metrics and counting, “counts” can mean that the scorer starts tallying only after calibration. The intended meaning concerns whether its judgments count as evidence.  
    **Replacement:** “a scorer's judgments count only once it has been calibrated”

33. **[suggested] §11 — “The second moment”**  
    **Exact:** “the engineer deciding how far this patch deserves to be accepted”  
    **Problem:** “How far … deserves to be accepted” is not idiomatic English.  
    **Replacement:** “the engineer deciding what level of acceptance this patch warrants”

34. **[suggested] §11, second decision and decision table, Accept the fix row**  
    **Exact:** “the relevant regression checks do not get worse”; “regressions do not get worse”  
    **Problem:** The intended comparison concerns check results. “Regressions do not get worse” could instead permit existing regressions to remain.  
    **Replacements:** “results on the relevant regression checks do not get worse”; “results on the regression checks do not get worse”

35. **[must-fix] §11 — “The second moment”**  
    **Exact:** “if pausing the rollout has already reduced traffic on the new version”  
    **Problem:** §3 explicitly defines pausing as holding exposure at 10%, not withdrawing exposure. This clause attributes a traffic reduction to that pause. The same inconsistency occurs in Chinese; both editions need alignment.  
    **Replacement:** “if traffic on the new version has already fallen”

36. **[suggested] §11 — “The third moment”**  
    **Exact:** “section 8 of the spec piece in "The Same Spec, Ten Runs"”; “Sections 10 and 11 of the variance piece”  
    **Problem:** These informal labels do not match the named English parts, making the cross-references harder to locate.  
    **Replacements:** “section 8 of the Specification part of "The Same Spec, Ten Runs"”; “Sections 10 and 11 of the Variance part of "The Same Spec, Ten Runs"”

37. **[suggested] §11 — “The third moment”**  
    **Exact:** “more comparison runs do not pay for the cost of a person taking over”  
    **Problem:** The translated metaphor sounds like a statement about who pays the bill. The referenced discussion concerns the separate evidence needed to establish human effort.  
    **Replacement:** “more comparison runs do not establish the cost of a person taking over”

38. **[must-fix] §11 — “The second and third rows”**  
    **Exact:** “The second and third rows are unaffected by this timeout”  
    **Problem:** This is broader than the explanation that follows: the paragraph itself says the flag’s state affects reproduction conditions. What remains unaffected is the acceptance criteria. The Chinese shares this overstatement.  
    **Replacement:** “The acceptance criteria in the second and third rows are unaffected by this timeout”

39. **[suggested] §11 — “Once a quarter's worth”**  
    **Exact:** “whether what the agent saves is data collection, setting up the reproduction environment, or fixing time”  
    **Problem:** The list mixes activities with time saved; “fixing time” is also ambiguous.  
    **Replacement:** “whether the agent saves time on collecting data, setting up the reproduction environment, or fixing the defect”

40. **[suggested] §12 — “When I look back”**  
    **Exact:** “asking the three questions apart”  
    **Problem:** A calque; English asks questions “separately.”  
    **Replacement:** “asking the three questions separately”

41. **[must-fix] §12 — “When I look back”**  
    **Exact:** “the paused flag is the target state confirmed by the remote check”  
    **Problem:** A flag is not itself a state, and the article’s defined action is pausing the rollout. The wording blurs the distinction established in §3.  
    **Replacement:** “the rollout is paused, as confirmed by the remote check”

42. **[suggested] §12 — “Open-source contribution”**  
    **Exact:** “AAIF's shared projects gain one more ambiguity found in real use”  
    **Problem:** The projects appear to acquire more ambiguity, rather than receive evidence exposing an ambiguity.  
    **Replacement:** “AAIF's shared projects gain a report of another ambiguity encountered in real use”

43. **[suggested] §12 — “So I would start”**  
    **Exact:** “In that way the invitation extends beyond the conference: organizing”  
    **Problem:** The gerund after the colon leaves the author’s action unattached to a clear actor.  
    **Replacement:** “In that way I carry the invitation beyond the conference by organizing”

44. **[suggested] §Final notes, “How the recordings and documents were checked” — “The five Tokyo talks”**  
    **Exact:** “; PagerDuty's recording”; “; Mazin Gilbert's keynote”; “; the NTT DOCOMO session”  
    **Problem:** One sentence carries four distinct verification methods and their qualifications. Sentence breaks make the source boundaries easier to retain.  
    **Replacements:** “. PagerDuty's recording”; “. Mazin Gilbert's keynote”; “. The NTT DOCOMO session”

45. **[must-fix] §Final notes, “How the recordings and documents were checked” — “As of 2026-10-25”**  
    **Exact:** “the recordings of all seven talks cited here are among them”  
    **Problem:** More than seven talks are cited, including Mazin Gilbert’s keynote and the NTT session; the preceding text says no matching NTT recording has been confirmed. Seven refers to the talks analyzed in §§4–10. The Chinese needs the same scope clarification.  
    **Replacement:** “the recordings of the seven talks analyzed in sections 4–10 are among them”

46. **[must-fix] §Final notes, “AI collaboration disclosure” — “Codex assisted”**  
    **Exact:** “re-argued”  
    **Problem:** The Chinese says the argument was reorganized, not argued again.  
    **Replacement:** “reorganized”

**Counts by priority:** must-fix **10**; suggested **34**; optional **2**. Total: **46**.

**Counts by review category** (one primary category per finding): grammar/syntax **3**; punctuation **2**; readability **24**; flow **1**; terminology **4**; internal consistency/cross-references **8**; zh/en parity **4**.

The remaining pre-press risks are localized ambiguity, several translation shifts, and imprecise statements about rollout state and evidence. Resolve the must-fix items, with corresponding Chinese corrections where noted, before final sign-off.

<!-- tokens: in 912313 out 24774 -->
