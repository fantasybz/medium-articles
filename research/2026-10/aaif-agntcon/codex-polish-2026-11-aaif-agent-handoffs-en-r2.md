# Codex 校稿 — 2026-11-aaif-agent-handoffs/article.en.md（第 2 輪）

> model: gpt-6.1-sol, reasoning: xhigh, 2026-10-29 03:11. 原話照錄，未經摘要。

I’ll read STYLE.md first, then check the round-one fixes and dispositions before reviewing the English against the Chinese block by block. I’ll keep all access read-only and inside this repository, and report only problems that remain.
<!-- codex ran: /bin/zsh -lc 'cat STYLE.md' -->
<!-- codex ran: /bin/zsh -c 'cat .context/research/aaif-2026-10-28-polish/2026-11-aaif-agent-handoffs-en-r1-disposition.md' -->
<!-- codex ran: /bin/zsh -c 'cat research/2026-10/aaif-agntcon/codex-polish-2026-11-aaif-agent-handoffs-en-r1.md' -->
<!-- codex ran: /bin/zsh -c "wc -l 2026-11-aaif-agent-handoffs/article.en.md 2026-11-aaif-agent-handoffs/article.md; rg --files -g AGENTS.md -g style_brief.md -g '*2026-11*en*' -->
<!-- codex ran: /bin/zsh -c 'cat research/2026-10/style_brief.md' -->
<!-- codex ran: /bin/zsh -c "sed -n '1,125p' 2026-11-aaif-agent-handoffs/article.md" -->
<!-- codex ran: /bin/zsh -c "sed -n '1,170p' .context/research/aaif-2026-10-28-polish/2026-11-aaif-agent-handoffs-en-r1-disposition.md" -->
<!-- codex ran: /bin/zsh -c "sed -n '170,245p' .context/research/aaif-2026-10-28-polish/2026-11-aaif-agent-handoffs-en-r1-disposition.md" -->
<!-- codex ran: /bin/zsh -c "sed -n '1,90p' research/2026-10/style_brief.md" -->
The round-one fixes appear sound, including the simulated PR wording, work-state distinction, read permissions, and plan-version reference. I’m now checking the remaining English against the current Chinese, with particular attention to approval conditions, actor roles, and recovery states.
<!-- codex ran: /bin/zsh -c "sed -n '120,169p' .context/research/aaif-2026-10-28-polish/2026-11-aaif-agent-handoffs-en-r1-disposition.md; sed -n '125,205p' 2026-11-aaif-agent-h -->
<!-- codex ran: /bin/zsh -c "sed -n '1,110p' 2026-11-aaif-agent-handoffs/article.en.md; sed -n '111,205p' 2026-11-aaif-agent-handoffs/article.en.md" -->
<!-- codex ran: /bin/zsh -c "sed -n '206,284p' 2026-11-aaif-agent-handoffs/article.md" -->
<!-- codex ran: /bin/zsh -c "sed -n '285,365p' 2026-11-aaif-agent-handoffs/article.md" -->
<!-- codex ran: /bin/zsh -c "sed -n '366,430p' 2026-11-aaif-agent-handoffs/article.md" -->
The comparison has turned up two places where the English changes the meaning: a diagram label can read as evidence opposing the requirements, and a communication-permission example reverses who may contact whom. I’m continuing through the acceptance tests and final notes, separating those issues from optional wording preferences.
<!-- codex ran: /bin/zsh -c "sed -n '259,305p' 2026-11-aaif-agent-handoffs/article.en.md" -->
<!-- codex ran: /bin/zsh -c "sed -n '132,146p' 2026-11-aaif-agent-handoffs/article.en.md; sed -n '206,258p' 2026-11-aaif-agent-handoffs/article.en.md" -->
<!-- codex ran: /bin/zsh -c "sed -n '371,431p' 2026-11-aaif-agent-handoffs/article.en.md" -->
<!-- codex ran: /bin/zsh -c "sed -n '306,370p' 2026-11-aaif-agent-handoffs/article.en.md" -->
I’ve completed the comparison through the tables, references, methods note, and disclosure. The section references and numerical summaries line up; the remaining findings concern localized ambiguities and awkward syntax. I’m checking the proposed replacements for parity and against the rejected-item log.
<!-- codex ran: /bin/zsh -c "rg -n -F -e 'Here is how I would handle it' -e 'Evidence against requirements' -e 'who may contact me' -e 'agent\\x27s own account' -e 'reopen' -e  -->
1. **[must-fix] Series overview → Action box, “Targets and task authorization…”**  
   **Text:** “Evidence against requirements”  
   **Problem:** “Evidence against” ordinarily means evidence opposing something. The Chinese, 「符合要求的證據」, means evidence that the requirements have been met.  
   **Replacement:** “Evidence that requirements are met”

2. **[must-fix] §3 → “Check communication permission…,” “Back in the upgrade case…”**  
   **Text:** “who may contact me”  
   **Problem:** This reverses the direction of permission in the Chinese 「可以聯絡誰」. Permission for A to contact B is not interchangeable with permission for B to contact A.  
   **Replacement:** “whom I may contact”

3. **[suggested] §3 → “Semantic inspection…,” “It also matters…”**  
   **Text:** “Here is how I would handle it: when semantic judgment times out, accept no new drains, where the line that defines “new” is the moment the execution service durably registers a request, so any request not yet registered counts as new; keep tracking operations already registered; and do not accept requests that have passed the check but whose approval expires before they are durably registered.”  
   **Problem:** The nested definition interrupts a long sequence of instructions, making the registration and expiry conditions difficult to retain.  
   **Replacement:** “Here is how I would handle it: when semantic judgment times out, accept no new drains. A request counts as new until the execution service durably registers it. Keep tracking operations already registered, and do not accept requests that have passed the check but whose approval expires before they are durably registered.”

4. **[suggested] §4, “His central distinction…”**  
   **Text:** “but this task needs to get into only one meeting room”  
   **Problem:** The task becomes the person entering the room, carrying over the Chinese’s omitted actor.  
   **Replacement:** “but the engineer needs access to only one meeting room for this task”

5. **[suggested] §4 → “Shrink account capabilities…,” “The deck lists…”**  
   **Text:** “issues edited or leaked by mistake”  
   **Problem:** This makes issues themselves the leaked material. The final notes identify the leak as internal information pasted into an outside repository.  
   **Replacement:** “mistaken edits to issues or leaks of internal information”

6. **[suggested] §5 → “After remediation…,” “The contract I adopt…”**  
   **Text:** “rather than relying on the agent's own account”  
   **Problem:** In this permissions discussion, “account” can mean the agent’s login account. The Chinese 「不由 agent 自述」 means its own claims or description.  
   **Replacement:** “rather than relying on the agent's own claims”

7. **[optional] §6 → “Define the durability promise…,” “Page 7 asks…”**  
   **Text:** “Second, how much may be lost (RPO)?”; “Third, how fast is recovery (RTO)?”  
   **Problem:** Both concepts are explained, but their initials are never expanded, unlike SDK, CI, and CLI.  
   **Replacements:** “Second, how much may be lost (the recovery point objective, or RPO)?”; “Third, how fast is recovery (the recovery time objective, or RTO)?”

8. **[suggested] §7, “His starting point…”**  
   **Text:** “which needs no local user data recovered after a rebuild”  
   **Problem:** The compressed “needs … recovered” construction is awkward here and slows the definition of the harness.  
   **Replacement:** “which does not need local user data to be restored after a rebuild”

9. **[suggested] §8 → “Shared components…,” “What all three leave behind…”**  
   **Text:** “To rebuild the timeline of one procurement, from assignment through the agent's processing to the ordering service, every segment has to be instrumented in advance and the records correlated; and a timeline proves only the order of events, not an approval, so the timeline and the approval record, each on its own, leave an audit gap.”  
   **Problem:** Instrumentation, the evidentiary limit, and the resulting audit gap are compressed into one heavily coordinated sentence.  
   **Replacement:** “To rebuild the timeline of one procurement, from assignment through the agent's processing to the ordering service, every segment has to be instrumented in advance and the records correlated. A timeline proves only the order of events, not an approval. The timeline and the approval record each leave an audit gap when used on their own.”

10. **[suggested] §8 → “Shared components…,” “What all three leave behind…”**  
    **Text:** “whose permissions to use, what to delegate downstream, and how to narrow permissions at each hop still have to be built in-house.”  
    **Problem:** The grammatical subjects are questions or decisions; what teams build is the mechanism that handles them.  
    **Replacement:** “teams still have to build their own mechanisms for deciding whose permissions to use, what to delegate downstream, and how to narrow permissions at each hop.”

11. **[must-fix] §8 → “Shared components…,” “The deck gives no count…”**  
    **Text:** “Selection therefore has to include “who implements this check, and where does its data come from.””  
    **Problem:** “Where does” makes this a direct question, which requires a question mark. This is the author’s own question, not a verbatim source quotation.  
    **Replacement:** “Selection therefore has to include “Who implements this check, and where does its data come from?””

12. **[suggested] §9, “The design has three steps…”**  
    **Text:** “The design has three steps, which are also the order of the three subsections below.”  
    **Problem:** The steps correspond to the subsections; they are not themselves an order.  
    **Replacement:** “The design has three steps, presented in sequence in the three subsections below.”

13. **[suggested] §9 roadmap and subsections → “The design…,” “Next, specify…,” “The genuinely hard…”**  
    **Text:** “reopening the node to work”; “reopen the node to work”; “it may be reopened to work on the old version and marked unfinished”  
    **Problem:** “Reopen … to work” is an unnatural rendering of 「恢復接受工作」 and can suggest that the node itself resumes working.  
    **Replacements, respectively:** “allowing the node to accept workloads again”; “allow the node to accept workloads again”; “it may resume accepting workloads on the old version and be marked unfinished”

14. **[suggested] §9 → “Define the operation…,” “Next, specify…”**  
    **Text:** “This article tests only “upgrade node N” on one worker, which consists of three sub-steps:”  
    **Problem:** “Which” appears to modify “one worker,” making the worker consist of steps.  
    **Replacement:** “This article tests only “upgrade node N” on one worker. The operation consists of three sub-steps:”

15. **[suggested] §9 → “After an interruption…,” “The local summaries…”**  
    **Text:** “What this article adds is a change of successor and a multi-stage infrastructure operation.”  
    **Problem:** “A change of successor” can mean replacing an already designated successor. The Chinese means that a different agent takes over the work.  
    **Replacement:** “What this article adds is a handoff to a different agent and a multi-stage infrastructure operation.”

16. **[suggested] Sources and method, “This round did not rerun…”**  
    **Text:** “The quotations from the OpenAI Agents SDK and the Anthropic engineering article follow the online versions”  
    **Problem:** The relevant descriptions and reference annotations are paraphrases; “quotations” implies verbatim wording.  
    **Replacement:** “The material cited from the OpenAI Agents SDK documentation and the Anthropic engineering article follows the online versions”

**Counts:** must-fix **3**; suggested **12**; optional **1**. **Total: 16 findings.**

The applied round-one fixes are sound, and no rejected item needs reopening. The remaining problems are localized; the numerical summaries, table contents, and section cross-references otherwise align.

<!-- tokens: in 1228281 out 14774 -->
