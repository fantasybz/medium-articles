# Codex 校稿 — 2026-11-aaif-agent-handoffs/article.en.md（第 1 輪）

> model: gpt-6.1-sol, reasoning: xhigh, 2026-10-29 02:30. 原話照錄，未經摘要。

I’ll read STYLE.md first, then compare the English and Chinese block by block, including captions, tables, and notes. I’ll keep the repository read-only and report localized fixes only.
<!-- codex ran: /bin/zsh -lc 'cat STYLE.md' -->
<!-- codex ran: /bin/zsh -lc 'nl -ba 2026-11-aaif-agent-handoffs/article.en.md' -->
<!-- codex ran: /bin/zsh -lc 'nl -ba 2026-11-aaif-agent-handoffs/article.md' -->
<!-- codex ran: /bin/zsh -lc "wc -l 2026-11-aaif-agent-handoffs/article.md 2026-11-aaif-agent-handoffs/article.en.md; rg --files -g 'AGENTS.md' -g '*style_brief*' -g '*2026-11* -->
<!-- codex ran: /bin/zsh -lc "sed -n '118,205p' 2026-11-aaif-agent-handoffs/article.md" -->
<!-- codex ran: /bin/zsh -lc 'cat research/2026-10/style_brief.md' -->
<!-- codex ran: /bin/zsh -lc "sed -n '200,285p' 2026-11-aaif-agent-handoffs/article.md" -->
The approval, recovery, and takeover distinctions largely match so far. I’m checking places where the English may shift an actor, condition, or claim, alongside sentences that take more than one pass to parse.
<!-- codex ran: /bin/zsh -lc "sed -n '285,375p' 2026-11-aaif-agent-handoffs/article.md" -->
<!-- codex ran: /bin/zsh -lc "sed -n '376,430p' 2026-11-aaif-agent-handoffs/article.md" -->
<!-- codex ran: /bin/zsh -lc "sed -n '1,120p' 2026-11-aaif-agent-handoffs/article.en.md" -->
I’ve reached the final notes. The main issues are localized: wording that blurs simulated PR creation, a sentence that narrows work state to conversation state, a read/write ambiguity in the `safe-gh` description, and several calques in the recovery sections. I’m checking that each replacement preserves the Chinese meaning and the author’s level of certainty.
<!-- codex ran: /bin/zsh -lc "sed -n '121,245p' 2026-11-aaif-agent-handoffs/article.en.md" -->
The full comparison is complete, including the diagram labels, captions, both tables, references, and disclosure. I’m consolidating repeated wording issues and separating corrections needed for meaning or correctness from optional style changes.
1. **[optional] TL;DR and §1, “On what grounds…” / “Once I laid…”**  
   **Text:** “obtain the right to take over, and decide whether to continue, redo, or stop”  
   **Problem:** The comma unnecessarily separates coordinated verbs.  
   **Replacement:** “obtain the right to take over and decide whether to continue, redo, or stop”

2. **[must-fix] §1, “When I reread…”**  
   **Text:** “the engineering agent first completes a mock operation that creates a pull request (PR)”  
   **Problem:** “That creates” leaves room for an actual PR to have been created. The Chinese specifies simulated PR creation, an important evidence limitation.  
   **Replacement:** “the engineering agent first completes an operation that simulates creating a pull request (PR)”

3. **[suggested] §1, “When I reread…”**  
   **Text:** “a constraint the speaker was trying to solve”  
   **Problem:** A problem is solved; a constraint is addressed or worked within.  
   **Replacement:** “a constraint the speaker was trying to address”

4. **[must-fix] §2, “Put these kinds…”**  
   **Text:** “the conversation and its state”  
   **Problem:** “Its” restricts state to conversational state. The Chinese says “對話與狀態,” encompassing the state of the work.  
   **Replacement:** “the conversation and the state of the work”

5. **[suggested] §2, “One concrete task…”**  
   **Text:** “What is handed over at first is only the assessment; changing any node is not allowed.”  
   **Problem:** “The assessment” can sound like a completed report being transferred. The Chinese describes the initial assignment’s scope.  
   **Replacement:** “The initial assignment is assessment only; changing any node is not allowed.”

6. **[suggested] §3 → “Check communication permission…,” “Back in the upgrade case…”**  
   **Text:** “That request does not authorize the execution agent to drain a node, that is, to move whatever application workloads can be moved off that machine first, so that the machine can be maintained.”  
   **Problem:** The definition interrupts the main statement with several layers of qualification.  
   **Replacement:** “That request does not authorize the execution agent to drain a node. Draining means moving workloads off the machine, where possible, before maintenance.”

7. **[suggested] §3 → “Semantic inspection…,” SoftBank page 15 caption**  
   **Text:** “streamed content first needs enough context to build up”  
   **Problem:** The wording makes the relationship between content, context, and judgment difficult to parse.  
   **Replacement:** “enough context must first accumulate before streamed content can be judged”

8. **[must-fix] §3 → “Semantic inspection…,” “So I would not only ask…”**  
   **Text:** “and which kind of error justifies which kind of cost.”  
   **Problem:** This closes a series of direct questions and needs a question mark.  
   **Replacement:** “and which kind of error justifies which kind of cost?”

9. **[suggested] §3, closing bold statement**  
   **Text:** “an “approved” in the message is only where the check begins”  
   **Problem:** The quoted adjective needs a noun here for natural English.  
   **Replacement:** “an “approved” label in the message is only where the check begins”

10. **[optional] §4 → “Shrink account capabilities…,” “The deck lists…”**  
    **Text:** “a process called CI”  
    **Problem:** The process is explained, but the acronym is never expanded.  
    **Replacement:** “a process called continuous integration (CI)”

11. **[suggested] §4 → “Shrink account capabilities…,” “The deck lists…”**  
    **Text:** “An agent that can push can therefore change the CI configuration in passing and have CI do for it whatever CI's account, and the passwords or API keys CI needs to log into other systems (its secrets), allow: while fixing code, the agent changes the process that checks its own work.”  
    **Problem:** The long insertion separates “whatever” from “allow,” obscuring the grammatical structure.  
    **Replacement:** “An agent that can push can therefore change the CI configuration in passing and have CI act on its behalf with the permissions available through CI's own account and secrets. These secrets are the passwords or API keys CI needs to log into other systems. While fixing code, the agent changes the process that checks its own work.”

12. **[suggested] §4 → “Shrink account capabilities…,” “His countermeasures…”**  
    **Text:** “His countermeasures are a handful of CLI wrapper tools, that is, a layer of checking wrapped around the original command, which the same command passes through before it is sent.”  
    **Problem:** The definition repeats “command” and leaves the relative clause awkwardly attached.  
    **Replacement:** “His countermeasures are a handful of command-line interface (CLI) wrappers that check each command before it is sent to the original tool.”

13. **[must-fix] §4 → “Shrink account capabilities…,” “His countermeasures…”**  
    **Text:** “`safe-gh` allows only reads against allowlisted organizations, and in the demo the issue-editing rule”  
    **Problem:** “Allows only reads” appears to prohibit the editing described immediately afterward. The restriction on read targets needs to be distinguished from the editing rule.  
    **Replacement:** “`safe-gh` restricts reads to allowlisted organizations; in the demo, the issue-editing rule”

14. **[must-fix] §4 → “Shrink account capabilities…,” “Back in the upgrade case…”**  
    **Text:** “the assessment may read cluster versions and resources”  
    **Problem:** The actor is missing: an assessment cannot read resources or hold permissions.  
    **Replacement:** “the assessment agent may read cluster versions and resources”

15. **[suggested] §5, “Their demonstration environment…”**  
    **Text:** “with the model served through a local Ollama”  
    **Problem:** The indefinite article needs an instance noun after the product name.  
    **Replacement:** “with the model served through a local Ollama instance”

16. **[suggested] §5 → “An assessment that says feasible…,” “Page 21 parses…”**  
    **Text:** “`CONDITIONAL` needs remediation first, or a person accepting an explicit, bounded risk”; “`UNKNOWN`, which likewise may not proceed”  
    **Problem:** The first fragment has awkward parallelism; the second makes the state itself the entity that proceeds.  
    **Replacements:** “`CONDITIONAL` requires remediation first or human acceptance of an explicit, bounded risk”; “`UNKNOWN`, which likewise blocks execution”

17. **[suggested] §5 → “After remediation…,” “The environment keeps changing…”**  
    **Text:** “need only be recorded; variation within the pre-approved bounds”; “the approved targets and steps carry over; and variation beyond the bounds”  
    **Problem:** The three-category sentence is too long to retain comfortably in one pass. Split it at the category boundaries.  
    **Replacements:** “need only be recorded. The second kind is variation within the pre-approved bounds”; “the approved targets and steps carry over. The third kind is variation beyond the bounds”

18. **[must-fix] §5 → “Accept layer by layer…,” “Finally, infrastructure checks…”**  
    **Text:** “; and the four are tested separately.”  
    **Problem:** The Chinese says these four aspects must be tested separately. The English’s declarative tense can imply testing already takes place.  
    **Replacement:** “. All four must be tested separately.”

19. **[must-fix] §5 → “Accept layer by layer…,” “At this point…”**  
    **Text:** “which of that evidence can still be found?”  
    **Problem:** “Evidence” is uncountable; “which of” needs a countable unit here.  
    **Replacement:** “which pieces of that evidence can still be found?”

20. **[suggested] §6 → “First separate…,” “Putting control state…”; §7 → “Each file…,” “Here the execution service…”**  
    **Text:** “it stops at pending confirmation”; “new ones stop at pending confirmation”  
    **Problem:** “Stop at pending confirmation” carries over the Chinese construction awkwardly.  
    **Replacements:** “it pauses pending confirmation”; “new operations remain pending confirmation”

21. **[suggested] §6 → “Define the durability promise…,” “Page 7 asks…”**  
    **Text:** “assume every remote replica has completed”  
    **Problem:** The action completed by each replica is left unstated.  
    **Replacement:** “assume every remote replica has completed the write”

22. **[suggested] §7 heading, “No file was overwritten…”**  
    **Text:** “No file was overwritten, and the work can still conflict”  
    **Problem:** The past tense suggests a particular incident, while the section states a general principle.  
    **Replacement:** “Work can still conflict even when no file is overwritten”

23. **[suggested] §7 → “A version check…,” “The conflict handled…”**  
    **Text:** “the write is refused, and the failed file stays on the side whose write failed”  
    **Problem:** The write fails, not the file; “the side” also obscures which client retains the edit.  
    **Replacement:** “the write is refused, and the local edit remains with the client whose write failed”

24. **[suggested] §8 → “Shared components…,” “The deck gives no count…”**  
    **Text:** “so that an incomplete set of conditions never reaches an orderable state”  
    **Problem:** The workflow reaches a state; the conditions determine whether it may do so.  
    **Replacement:** “so that the workflow cannot reach an orderable state until all conditions are met”

25. **[suggested] §8 → “Link the task…,” “One assignment…”**  
    **Text:** “A record that can be traced to a person is still not the same as someone taking the case.”  
    **Problem:** The comparison between a record and a person’s action is awkward, and “taking the case” is a calque.  
    **Replacement:** “Being able to trace a record to a person does not mean someone has taken responsibility for the case.”

26. **[suggested] §8 → “Link the task…,” “What holds for procurement…”**  
    **Text:** “so a late request from the predecessor finds nothing to attach itself to”  
    **Problem:** The metaphor obscures the concrete check against the current handover record.  
    **Replacement:** “so a late request from the predecessor fails the check against the current handover record”

27. **[suggested] §9 heading and introduction; “Which results…,” “The expectations…”**  
    **Text:** “If I were doing the acceptance now”; “run acceptance on only one kind of limited operation”; “The expectations in this acceptance”  
    **Problem:** These uses of bare “acceptance” sound translated. The intended activity is acceptance testing.  
    **Replacements:** “If I were running acceptance tests now”; “run acceptance tests on only one kind of limited operation”; “The expected outcomes in these acceptance tests”

28. **[suggested] §9 → “Define the operation…,” “Before starting…”**  
    **Text:** “may not read the moment of failure the test apparatus privately recorded”  
    **Problem:** A recorded time can be read; the moment itself cannot.  
    **Replacement:** “may not read the failure time privately recorded by the test apparatus”

29. **[suggested] §9 → “Which results…,” table, “Drain completed, upgrade failed”**  
    **Text:** “One of three by the state found:”  
    **Problem:** The compressed wording is unnatural and makes the decision rule harder to scan.  
    **Replacement:** “Choose among three responses according to the observed state:”

30. **[must-fix] §9 → “Which results…,” table, “Normal, approval valid”**  
    **Text:** “Approval record v8”  
    **Problem:** Earlier, v8 identifies the plan; the approval source is CR-204. This cell conflates the plan version with the approval record.  
    **Replacement:** “Approval for plan v8”

31. **[suggested] §9 → “Which results…,” table, “Result temporarily unqueryable”; Further reading, organization entry**  
    **Text:** “The case-taking rule”; “the case-taking split in Section 8”  
    **Problem:** “Case-taking” is an unnatural rendering of 接案 in both contexts.  
    **Replacements:** “The rule for assigning cases”; “the division of responsibility for handling cases in Section 8”

32. **[suggested] §9 → “Which results…,” “A safe stop…”**  
    **Text:** “A Staff engineer on the platform”  
    **Problem:** The generic job title should be lowercase, consistent with the other roles. “Platform team” also makes the affiliation explicit.  
    **Replacement:** “A staff engineer on the platform team”

33. **[suggested] §10, “A good handoff…”**  
    **Text:** “it keeps the effects already produced”  
    **Problem:** A handoff preserves information about external effects; it does not preserve the effects themselves.  
    **Replacement:** “it records the effects already produced”

34. **[suggested] §10, “I will start…”**  
    **Text:** “that record is exactly the capability a recoverable system still has to add”  
    **Problem:** A record is an artifact, whereas maintaining it is a capability.  
    **Replacement:** “maintaining that record is exactly the capability a recoverable system still has to add”

35. **[suggested] References, entry 3, “OpenAI…”**  
    **Text:** “input filters; and authorization checks, which belong in the handoff callback.”  
    **Problem:** The list switches from complete clauses to noun fragments.  
    **Replacement:** “developers can filter inputs; and authorization checks belong in the handoff callback.”

36. **[suggested] Sources and method, “This article analyzes…”**  
    **Text:** “so the official decks are attached for comparison in the meantime.”  
    **Problem:** The article supplies links, rather than attaching the decks themselves.  
    **Replacement:** “so the official decks are linked for comparison in the meantime.”

**Counts:** must-fix **8**; suggested **26**; optional **2**. Total: **36 findings**.

The English is broadly faithful to the Chinese and preserves the author’s judgments and first-person voice. Before pre-press sign-off, resolve the ambiguities concerning simulated operations, work state, read/write permissions, and record versions, along with the localized grammar and punctuation errors.

<!-- tokens: in 712122 out 18968 -->
