# Codex review — 2026-11-same-spec-spec/article.en.md (round 2)

> model: gpt-6.1-sol, reasoning: xhigh, 2026-10-27 01:14. Codex's own words, not summarised. Round 2; reviewing the English edition against the final Chinese article and the frozen study.

I’ll read the standards first, then compare the editions against the frozen study and approved English samples. I’ll keep the review read-only and stay inside this repository.
<!-- codex ran: /bin/zsh -lc 'cat STYLE.md' -->
<!-- codex ran: /bin/zsh -lc 'cat research/2026-10/style_brief.md' -->
<!-- codex ran: /bin/zsh -lc "sed -n '1,190p' 2026-11-same-spec-spec/article.md" -->
<!-- codex ran: /bin/zsh -lc "sed -n '1,160p' 2026-11-aaif-agent-memory/article.en.md" -->
<!-- codex ran: /bin/zsh -lc "sed -n '1,150p' 2026-10-green-payment/article.en.md" -->
<!-- codex ran: /bin/zsh -lc 'wc -l 2026-11-same-spec-spec/article.md 2026-11-same-spec-spec/article.en.md 2026-10-green-payment/article.en.md 2026-11-aaif-agent-memory/article -->
<!-- codex ran: /bin/zsh -lc "nl -ba 2026-11-same-spec-spec/article.md | sed -n '90,215p'" -->
<!-- codex ran: /bin/zsh -lc "nl -ba 2026-11-same-spec-spec/article.md | sed -n '217,360p'" -->
The editions follow nearly the same paragraph structure. I’m checking where translation choices alter the meaning, with particular attention to spec quotations, evidence limits, and the English edition’s provenance note.
<!-- codex ran: /bin/zsh -lc "nl -ba 2026-11-same-spec-spec/article.md | sed -n '360,490p'" -->
<!-- codex ran: /bin/zsh -lc 'cat research/experiments/same-spec-ten-runs/RESULTS.md research/experiments/same-spec-ten-runs/SPECS.md' -->
<!-- codex ran: /bin/zsh -lc 'cat research/experiments/same-spec-ten-runs/PROTOCOL.md' -->
<!-- codex ran: /bin/zsh -lc 'cat research/experiments/same-spec-ten-runs/results/formal-2026-09-25/source/specs/A0.md research/experiments/same-spec-ten-runs/results/formal-20 -->
<!-- codex ran: /bin/zsh -lc "sed -n '70,150p' research/experiments/same-spec-ten-runs/PROTOCOL.md;" -->
<!-- codex ran: /bin/zsh -lc "sed -n '130,180p' research/experiments/same-spec-ten-runs/results/formal-2026-09-25/source/specs/C.md" -->
<!-- codex ran: /bin/zsh -lc 'cat research/2026-10/same-spec-ten-runs/manuscripts/STATUS.md' -->
<!-- codex ran: /bin/zsh -lc "sed -n '1,100p' 2026-10-green-payment/article.en.md" -->
<!-- codex ran: /bin/zsh -lc "sed -n '245,347p' 2026-11-aaif-agent-memory/article.en.md" -->
<!-- codex ran: /bin/zsh -lc "nl -ba 2026-11-same-spec-spec/article.en.md | sed -n '1,172p'" -->
<!-- codex ran: /bin/zsh -lc "rg -n --glob '*.md' 'English edition|英文.*(max|主稿|主寫|Opus)|Specification.*English|spec.*English|English.*spec' research/2026-10/same-spec-ten-runs  -->
<!-- codex ran: /bin/zsh -lc "python3 -c 'from pathlib import Path
import re
base=Path(\".\")
zh=(base/\"2026-11-same-spec-spec/article.md\").read_text()
en=(base/\"2026-11-sam -->
The eight tables match in size, the six B questions and C pseudo-flow match the frozen English, and the reference links and back-pointers align. One publication claim is unsupported: the AI note says English production and review are recorded in STATUS.md, but that page still lists them as unfinished. That shows a record mismatch, not that the authorship claim is false.
<!-- codex ran: /bin/zsh -lc "nl -ba 2026-11-same-spec-spec/article.en.md | sed -n '308,340p'" -->
<!-- codex ran: /bin/zsh -lc "nl -ba 2026-11-same-spec-spec/article.en.md | sed -n '217,280p'" -->
<!-- codex ran: /bin/zsh -lc "rg -n '"'^## |''^### |''^> Series|''^> '"\\*\\*TL;DR|"'^'"\\*Kochi|"'^The (model|ten|formal)|''^All forty|''^.*288|''^.*P/Q'"' 2026-11-same-spec-{ -->
<!-- codex ran: /bin/zsh -lc "sed -n '1,16p' research/experiments/same-spec-ten-runs/results/formal-2026-09-25/packets/A.txt" -->
<!-- codex ran: /bin/zsh -lc 'tail -n 10 research/experiments/same-spec-ten-runs/results/formal-2026-09-25/packets/A.txt' -->
<!-- codex ran: /bin/zsh -lc "nl -ba research/2026-10/same-spec-ten-runs/manuscripts/STATUS.md | sed -n '41,53p'" -->
The remaining problems are wording and attribution: the packet definition omits shared instructions, “fixing” the rewrite policy obscures the requirement to freeze it, and several sentences give the candidate program actions that belong to the model or agent. Some of those ambiguities also exist in the Chinese; I’ll distinguish them from translation errors.
The pasted edition retains the main evidence limits. All eight tables match in dimensions; the six B questions and C’s pseudo-flow match the frozen English. Reference numbering, URLs and back-pointers align, including the required English links to earlier articles. There is no Mermaid. No missing reasoning paragraph or closing passage surfaced.

## Fatal

- **AI collaboration note — unsupported claim of completed English documentation.**

  > “This English edition was written by Claude Code (max effort) from the final Chinese text; the paragraph-by-paragraph polish, second-model review and final checks are recorded in the same STATUS.md.”

  This is an English-only provenance claim. [STATUS.md:45](research/2026-10/same-spec-ten-runs/manuscripts/STATUS.md:45) still says the English manuscripts and checks are unfinished and that the attempted drafting requests produced no manuscript. It does **not** establish that Claude did not write this draft; it does establish that the linked page does not substantiate this sentence.

  **Supportable replacement:** “This English edition translates the final Chinese manuscript. The linked STATUS.md documents the Chinese manuscript workflow; this edition’s production and review records have not yet been added there.”

  Restore the specific authorship and completed-check claims only when their records support them.

## Important

- **3. Four frozen briefs: A0 is not a blank control, and C is not a Skill — the added packet definition is incomplete.**

  Chinese:

  > 「同組十次收到的整包輸入（packet）完全相同，使用 `claude-opus-5-5`、high effort，也就是固定的推理投入設定；模型沒有工具，只能一次交付單一檔案。」

  English:

  > “The ten runs in a group received exactly the same packet, the complete input made up of that brief and the seed code, using `claude-opus-5-5` at high effort, a fixed setting for reasoning investment; the model had no tools and could only deliver a single file in one pass.”

  The Chinese does not supply that component list. The English adds one while omitting shared task instructions and the required return format. The system prompt is also archived separately; “complete input” risks conflating these boundaries.

  **Fix:** “The ten runs in each group received the same frozen task packet, containing shared task instructions, the brief, the seed code and the required return format. They used `claude-opus-5-5` at high effort, a fixed reasoning setting, with no tools and one generation pass to return a single file.”

- **8. The spec change card: turning “just add the six self-check questions” into a reviewable change — “fixing” obscures the required freeze.**

  Chinese:

  > 「跨到其他任務時，還要先固定自查改寫政策。」

  English:

  > “Crossing to other tasks also requires fixing the self-check rewrite policy first.”

  “Fixing” commonly means repairing. The source means establishing and freezing the policy before applying it.

  **Fix:** “Before applying the checklist to other tasks, freeze the self-check rewrite policy.”

- **6. Confirm the premises before diagnosing: a wrong exit code cannot tell you what the model was thinking — the candidate becomes the author.**

  > “The candidate kept the old code’s truthiness structure; the candidate wrote a helper that treats every false-like value as missing; or the candidate understood R05 and got something else wrong.”

  The article defined *candidate* as the generated program. Programs do not write helpers or understand requirements.

  This ambiguity is inherited from the Chinese:

  > 「這個推論缺乏依據，至少還有三種可能：候選沿用了舊程式的 truthiness 結構；候選寫了一個把假值都當成缺值的 helper；或者候選理解了 R05，卻在其他地方寫錯。」

  **Fix:** “There are at least three other possibilities: the generated code retained the old truthiness check; the model wrote a helper that treats all falsy values as missing; or the model understood R05 but introduced an error elsewhere.”

  Keep these explicitly hypothetical.

- **7. Exploration, text, executable feedback: three interventions, three actions — distinguish the agent from its artifact.**

  > “If nobody knows yet what to do with an empty value, find someone to decide; if the answer exists but is easy to misread, improve the explanation; if the program can run checks itself, let it see its errors before delivery.”

  The table repeats the ambiguity:

  > “Can the candidate find its own errors before delivery?”

  The Chinese also uses this shorthand:

  > 「還不知道空值該怎麼辦，就找人決定；已經有答案卻容易誤讀，可以改善說明；程式能自己執行檢查，則可以讓它在交付前看見錯誤。」

  **Fix the sentence:** “…if the agent can run checks, let it inspect failures before submitting its candidate.”

  **Fix the table cell:** “Can the agent detect errors in its candidate before delivery?”

  This matters because the section’s argument concerns feedback reaching the agent during its session.

## Minor

- **TL;DR — the central instruction becomes a terminology list.**

  > “First recover the requirements that already exist; hand what is genuinely undecided to whoever has the authority to decide; then separate the normative requirements that must be followed from the rationale and examples that explain them, the self-check before handing in, and the optional implementation suggestions.”

  **Fix:** “First recover existing requirements and refer genuinely undecided questions to whoever can decide them. Then distinguish what the implementation must do from explanations, examples, pre-submission self-checks and optional implementation suggestions.”

  This preserves the categories while letting the opening use ordinary English.

- **1. What “make the input handling more robust” has not yet answered — mismatched comparison.**

  > “The effect of these decisions on the caller is more direct than whether the code looks good.”

  **Fix:** “These decisions affect the caller more directly than code style does.”

- **3. Four frozen briefs: A0 is not a blank control, and C is not a Skill — counts do not split text.**

  > “The English word counts split on whitespace and include headings and code blocks; they exclude the seed code, and they are not the token counts the model uses to process text.”

  **Fix:** “The word counts use whitespace-separated units and include headings and code blocks. They exclude the seed code and are not model token counts.”

- **3. Four frozen briefs: A0 is not a blank control, and C is not a Skill — translated abstraction obscures the comparison.**

  > “B versus C could in principle compare the increment of the whole pattern section, but it still cannot separate which suggestion inside it worked, let alone infer the model’s inner reasoning from the result.”

  **Fix:** “Comparing B with C could in principle estimate the effect of adding the pattern section as a whole. It could not isolate the effect of individual suggestions or reveal the model’s reasoning.”

- **4. Comparing R05 sentence by sentence: the legal behavior is unchanged; what was added is reminders and a path — cumbersome heading.**

  **Fix the heading:** “4. R05 permits the same behavior; the added text supplies reminders and an implementation path”

- **4. Comparing R05 sentence by sentence: the legal behavior is unchanged; what was added is reminders and a path — history does not change.**

  > “The three treatments belong to three kinds of content, and each has its own maintenance: rationale has to be updated as the history changes, a self-check has to follow the clauses, and a helper suggestion must always carry its exception with it.”

  **Fix:** “Each treatment needs its own maintenance: keep the rationale consistent with the implementation history, update the self-check when its referenced clauses change, and preserve the exception whenever the helper suggestion is copied.”

  The source is similarly loose here; this clarifies its maintenance instruction without adding an outcome.

- **5. A sentence that looks synonymous: how A0 and A differ on the scope of new CLI options — “synonymous” needs a counterpart.**

  **Fix the heading:** “5. The CLI-scope sentence that makes A narrower than A0”

- **8. The spec change card: turning “just add the six self-check questions” into a reviewable change — the sample is not the estimate.**

  > “…the yardstick’s discriminating power, the representativeness of the tasks, or the precision of the sample.”

  **Fix:** “…the yardstick’s ability to distinguish outcomes, the representativeness of the tasks, or the precision of the estimate given the sample size.”

- **9. Switching to a CSV export: how the same card is used — unclear action.**

  > “At this point the document can support the next step: QA fixes the oracle to the approved output obligations and re-scores the candidates; the parts of the date policy not yet decided are filled in by the owner.”

  **Fix:** “The document now supports the next step: QA updates the oracle to match the approved output obligations and re-scores the candidates; the owner resolves the remaining date-policy questions.”

## Suggested cuts

- **4. Comparing R05 sentence by sentence: the legal behavior is unchanged; what was added is reminders and a path — remove added editorial scaffolding.**

  > “The wording below paraphrases A0’s R05 and keeps its terms.”

  **Cut it.** The preceding sentence already announces the rule, and the original-text links establish where to verify it. Keep the actual requirements and explanations.

- **11. Closing: record why a sentence should stay, and when it should be withdrawn — no substantive cut.**

  > “All 40 formal candidates passed, but that result cannot rank the documents; the P-versus-Q comparison has not been run; CSV is a hypothetical requirement paired with a fixed-data replay…”

  **Retain it.** This repetition exists in the Chinese and supplies the closing decision’s evidence boundaries. Removing it merely to shorten the English would weaken the twin.

## Suggested additions

- **3. Four frozen briefs: A0 is not a blank control, and C is not a Skill — name the interval precisely.**

  > “…10/10 gives an exact two-sided 95% Clopper–Pearson interval…”

  **Add one word:** “…an exact two-sided 95% Clopper–Pearson **confidence** interval…”

  The i.i.d., common-probability assumptions and numerical bounds are already present. No additional statistical claim is needed.

- **6. Confirm the premises before diagnosing: a wrong exit code cannot tell you what the model was thinking — define “slot” locally.**

  > “…and no replacement slot is opened.”

  **Fix:** “…and the original scheduled attempt is retained rather than replaced by a new run.”

  Part 3 can provide the detailed counting rules. This piece still needs that sentence to stand alone.

## Terms still unclear

- **2. Five kinds of sentence in one document: normative requirement, rationale, example, self-check and optional pattern — “legal set.”**

  > “From here on I call ‘the set of all implementations allowed to be accepted’ the legal set.”

  This definition is circular around acceptance, which the article later distinguishes from contractual permission.

  **Fix:** “The set of permitted implementations contains every implementation the contract allows, whether or not the current checks recognize it correctly.”

  That makes the later false-rejection argument easier to follow.

- **6. Confirm the premises before diagnosing: a wrong exit code cannot tell you what the model was thinking — countable “acceptance.”**

  > “That stdout agrees on both sides is itself a warning: an acceptance that checks only stdout would pass this candidate.”

  **Fix:** “The matching stdout is a warning: an acceptance check that inspects only stdout would pass this candidate.”

  Use *acceptance check*, *acceptance suite*, *acceptance criteria* or *acceptance process* according to the action. Bare “acceptance” currently carries all four meanings.

- **6. Confirm the premises before diagnosing: a wrong exit code cannot tell you what the model was thinking — “positive-and-negative check.”**

  > “The positive-and-negative check in the table means taking known-legal and known-faulty examples and confirming first that the yardstick, the grader together with the oracle it uses, can tell them apart.”

  **Fix:** “First check the grader and its oracle against examples known to satisfy the contract and examples known to violate it. They must distinguish the two.”

  Preserve the distinction between a deliberately malformed **input** and a faulty **implementation**: a compliant implementation should handle malformed input correctly.

<!-- tokens: in 1440253 out 20163 -->
