# Codex 校稿 — 2026-11-aaif-agent-handoffs/article.en.md（第 3 輪）

> model: gpt-6.1-sol, reasoning: xhigh, 2026-10-29 03:33. 原話照錄，未經摘要。

I’ll read STYLE.md first, then check the prior fixes and disposition logs before comparing the English and Chinese block by block. I’ll keep everything read-only and report only remaining problems.

<!-- codex ran: /bin/zsh -lc 'cat STYLE.md' -->
<!-- codex ran: /bin/zsh -lc "cat '.context/research/aaif-2026-10-28-polish/2026-11-aaif-agent-handoffs-en-r2-disposition.md'" -->
<!-- codex ran: /bin/zsh -lc "cat 'research/2026-10/aaif-agntcon/codex-polish-2026-11-aaif-agent-handoffs-en-r2.md'" -->
<!-- codex ran: /bin/zsh -lc "cat 'research/2026-10/style_brief.md'" -->
<!-- codex ran: /bin/zsh -lc "cat 'research/2026-10/aaif-agntcon/codex-polish-2026-11-aaif-agent-handoffs-en-r1.md'" -->
<!-- codex ran: /bin/zsh -lc "cat '.context/research/aaif-2026-10-28-polish/2026-11-aaif-agent-handoffs-en-r1-disposition.md'" -->
<!-- codex ran: /bin/zsh -lc 'cat .context/research/aaif-2026-10-28-polish/2026-11-aaif-agent-handoffs-en-r2-disposition.md' -->
<!-- codex ran: /bin/zsh -lc 'cat .context/research/aaif-2026-10-28-polish/2026-11-aaif-agent-handoffs-en-r1-disposition.md' -->
<!-- codex ran: /bin/zsh -lc 'cat research/2026-10/aaif-agntcon/codex-polish-2026-11-aaif-agent-handoffs-en-r2.md' -->
<!-- codex ran: /bin/zsh -lc "nl -ba 2026-11-aaif-agent-handoffs/article.md | sed -n '1,164p'" -->
<!-- codex ran: /bin/zsh -lc "nl -ba 2026-11-aaif-agent-handoffs/article.en.md | sed -n '1,180p'" -->
The round-two fixes read correctly, and the diagram correction and parity updates flagged in the logs are now present. I’m continuing through the bilingual comparison, checking whether the English preserves the same actors, conditions, and limits.

<!-- codex ran: /bin/zsh -lc "nl -ba 2026-11-aaif-agent-handoffs/article.md | sed -n '134,222p'" -->
<!-- codex ran: /bin/zsh -lc "nl -ba 2026-11-aaif-agent-handoffs/article.md | sed -n '222,304p'" -->
<!-- codex ran: /bin/zsh -lc "nl -ba 2026-11-aaif-agent-handoffs/article.en.md | sed -n '181,282p'" -->
<!-- codex ran: /bin/zsh -lc "nl -ba 2026-11-aaif-agent-handoffs/article.md | sed -n '304,376p'" -->
The remaining candidates are mostly local wording issues, including a few sentences whose grammatical subject does not match the action. I’m checking the acceptance tables and closing notes now, and screening out items already rejected in earlier rounds.

<!-- codex ran: /bin/zsh -lc "nl -ba 2026-11-aaif-agent-handoffs/article.md | sed -n '377,435p'" -->
<!-- codex ran: /bin/zsh -lc "nl -ba 2026-11-aaif-agent-handoffs/article.en.md | sed -n '283,373p'" -->
<!-- codex ran: /bin/zsh -lc "nl -ba 2026-11-aaif-agent-handoffs/article.en.md | sed -n '374,435p'" -->
<!-- codex ran: /bin/zsh -c "rg --files -g 'article.en.md' -g '"'!agents/**'"' -g '"'!.claude/**'"'" -->
<!-- codex ran: /bin/zsh -c "rg -n '"'^## |''^### |G2|pre-approved|[Aa]uthority is|checker itself|retention|restart'"' 2026-10-green-overview/article.en.md 2026-10-green-testin -->
<!-- codex ran: /bin/zsh -c "rg -n '"'^## |''^### |RACI|[Rr]egistry|broker|secret|egress|more teams|high-risk|obligation'"' 2026-10-agentic-harness-blueprint/article.en.md 2026 -->
<!-- codex ran: /bin/zsh -c "rg -n -i -e 'Quartic' -e 'first node' -e 'control plane' -e 'worker' -e 'checker' 2026-10-green-testing/article.en.md; rg -n -e '"'^## 2'"\\.' -e ' -->
I’ve completed the comparison through the disclosure and checked the cross-references against the other articles in the repository. I’m making the final pass over the remaining findings and their drop-in replacements; no rejected item needs reopening.

1. **[suggested] §5 → subsection heading and roadmap, “An assessment that says feasible…”**  
   **Exact text:** “An assessment that says feasible still needs approval to execute”  
   **Problem:** The grammatical subject makes the assessment itself the entity seeking permission to execute. The Chinese distinguishes a favorable assessment from authorization for execution.  
   **Drop-in replacement:** “Even when the assessment finds the upgrade feasible, execution still needs approval”

2. **[suggested] §5 → “An assessment that says feasible…,” “The data collector…”**  
   **Exact text:** “An upgrade has to confirm beforehand that these interdependent components can still work together.”  
   **Problem:** The upgrade is made the actor performing the confirmation. The Chinese says this compatibility must be confirmed before upgrading.  
   **Drop-in replacement:** “Before the upgrade, it is necessary to confirm that these interdependent components can still work together.”

3. **[suggested] §5 → “An assessment that says feasible…,” “Page 21 parses…”**  
   **Exact text:** “y executes, and n stops the upgrade.”  
   **Problem:** “Y executes” is compressed interface shorthand rather than natural explanatory prose.  
   **Drop-in replacement:** “answering y starts the upgrade, and answering n stops it.”

4. **[suggested] §5 → “Accept layer by layer…,” “Finally, infrastructure checks…”**  
   **Exact text:** “It must not erase effects that were legitimately accepted before expiry and confirmed complete only afterward”  
   **Problem:** The execution service accepts operations; their effects occur as a result. Calling the effects “accepted” blurs the distinction this paragraph establishes.  
   **Drop-in replacement:** “It must not erase the effects of operations that were legitimately accepted before expiry and confirmed complete only afterward”

5. **[suggested] §6 → “Define the durability promise…,” “This also changes…”**  
   **Exact text:** “and lists the failures to inject:”  
   **Problem:** The ensuing list includes confirming that secrets never enter snapshots, which is a verification activity rather than a failure to inject.  
   **Drop-in replacement:** “and lists the checks to perform:”

6. **[suggested] §7 → “A version check keeps…” and “In terms of the upgrade plan…”**  
   **Exact text:** “A version check keeps the edit, and keeps the chance to handle the conflict”; “keeps the chance to recognize the conflict”  
   **Problem:** “Keeps the chance” is an awkward calque of 保留機會.  
   **Drop-in replacements, respectively:** “A version check preserves the edit and the opportunity to handle the conflict”; “preserves the opportunity to recognize the conflict”

7. **[suggested] §9 → roadmap, “The design has three steps…”**  
   **Exact text:** “the execution service restarting itself”  
   **Problem:** “Restarting itself” suggests that the service initiates its own restart. The Chinese identifies the service itself as the component being restarted; the subsection describes an injected interruption.  
   **Drop-in replacement:** “a restart of the execution service itself”

8. **[suggested] §9 → “After an interruption…,” “The local summaries…”**  
   **Exact text:** “when the payment screen freezes and the same request is sent again, it should get back the original result, not charge a second time.”  
   **Problem:** “It” has no clear actor: the nearest referent is the request, while “get back” and “charge” imply different actors.  
   **Drop-in replacement:** “when the payment screen freezes, resending the same request should return the original result, not cause a second charge.”

9. **[suggested] §10 → closing, “I will start…”**  
   **Exact text:** “Then I will fill in, item by item, the evidence that recovery could not find”  
   **Problem:** “Fill in the evidence” is an unnatural collocation; evidence is supplied, while gaps or fields are filled in.  
   **Drop-in replacement:** “Then I will supply, item by item, the evidence that could not be found during recovery”

**Counts:** must-fix **0**; suggested **9**; optional **0**. **Total: 9 findings.**

The applied fixes from the previous rounds are sound, and no rejected item needs reopening. The remaining issues are localized wording and grammatical ambiguities; the numerical summaries, section references, captions, tables, and substantive zh/en coverage otherwise align.

<!-- tokens: in 1676181 out 9891 -->
