# Codex review — 2026-11-same-spec-spec/article.en.md (round 3)

> model: gpt-6.1-sol, reasoning: xhigh, 2026-10-27 01:26. Codex's own words, not summarised. Round 3; reviewing the English edition against the final Chinese article and the frozen study.

I’ll read the repository’s style standards first, then compare the English against the Chinese source and frozen study. I’ll keep this read-only and stay inside the repository.
<!-- codex ran: /bin/zsh -lc 'cat STYLE.md' -->
<!-- codex ran: /bin/zsh -lc 'cat research/2026-10/style_brief.md' -->
<!-- codex ran: /bin/zsh -lc "sed -n '1,180p' 2026-11-same-spec-spec/article.md" -->
<!-- codex ran: /bin/zsh -lc "sed -n '1,130p' 2026-10-green-payment/article.en.md" -->
<!-- codex ran: /bin/zsh -lc "sed -n '1,135p' 2026-11-aaif-agent-memory/article.en.md" -->
<!-- codex ran: /bin/zsh -lc 'wc -l 2026-11-same-spec-spec/article.md 2026-11-same-spec-spec/article.en.md 2026-10-green-payment/article.en.md 2026-11-aaif-agent-memory/article -->
<!-- codex ran: /bin/zsh -lc "sed -n '125,260p' 2026-11-same-spec-spec/article.md" -->
<!-- codex ran: /bin/zsh -lc "sed -n '85,135p' 2026-11-same-spec-spec/article.md" -->
<!-- codex ran: /bin/zsh -lc "sed -n '261,380p' 2026-11-same-spec-spec/article.md" -->
The sections read so far preserve the main evidence limits: forty passing candidates do not rank the briefs, the failures are hypothetical, and P/Q remains unrun. I’m now checking the spec quotations and later sections for wording that changes a requirement, condition, or responsibility.
<!-- codex ran: /bin/zsh -lc "sed -n '381,480p' 2026-11-same-spec-spec/article.md" -->
<!-- codex ran: /bin/zsh -lc 'cat research/experiments/same-spec-ten-runs/RESULTS.md research/experiments/same-spec-ten-runs/SPECS.md' -->
<!-- codex ran: /bin/zsh -lc 'cat research/experiments/same-spec-ten-runs/PROTOCOL.md' -->
<!-- codex ran: /bin/zsh -lc 'cat research/experiments/same-spec-ten-runs/results/formal-2026-09-25/source/specs/A0.md research/experiments/same-spec-ten-runs/results/formal-20 -->
<!-- codex ran: /bin/zsh -lc "rg -n 'English|英文|spec|規格|MAX|max|lead|Codex|288|P/Q' research/2026-10/same-spec-ten-runs/manuscripts/STATUS.md" -->
<!-- codex ran: /bin/zsh -lc "sed -n '1,80p' 2026-10-green-payment/article.en.md" -->
<!-- codex ran: /bin/zsh -lc "python3 -c 'from pathlib import Path; p=Path(\"research/experiments/same-spec-ten-runs/results/formal-2026-09-25/source/specs\"); a=(p/\"A.md\").r -->
<!-- codex ran: /bin/zsh -lc 'cat research/2026-10/same-spec-ten-runs/manuscripts/STATUS.md' -->
<!-- codex ran: /bin/zsh -lc "rg -n '288|P/Q|obligation|slot|"'^## |''^### |''^```|high|max'"' 2026-11-same-spec-overview/article.en.md 2026-11-same-spec-contract/article.en.md -->
<!-- codex ran: /bin/zsh -lc "python3 -c 'from pathlib import Path; import re,collections,json; z=Path(\"2026-11-same-spec-spec/article.md\").read_text(); e=Path(\"2026-11-same -->
<!-- codex ran: /bin/zsh -lc "sed -n '1,190p' 2026-11-same-spec-spec/article.en.md" -->
I found a provenance problem: the English note says drafting and review are recorded in `STATUS.md`, but that file still says no English manuscript was produced. The structural checks found no missing links after the required English-edition substitutions; all eight tables match in size, and neither edition has Mermaid. The six self-check questions and C’s quoted flow match the frozen originals.
<!-- codex ran: /bin/zsh -lc "sed -n '188,325p' 2026-11-same-spec-spec/article.en.md" -->
<!-- codex ran: /bin/zsh -lc "sed -n '325,430p' 2026-11-same-spec-spec/article.en.md" -->
<!-- codex ran: /bin/zsh -lc "rg -n 'the acceptance|acceptance is|qualif|deliveries|handing in|recheck with|expiry|expires|no result|complete input|slot|three ways|at a single  -->
<!-- codex ran: /bin/zsh -lc "sed -n '300,338p' 2026-11-same-spec-spec/article.en.md" -->
<!-- codex ran: /bin/zsh -lc "sed -n '455,510p' 2026-10-green-payment/article.en.md" -->
<!-- codex ran: /bin/zsh -lc "sed -n '1,95p' 2026-11-same-spec-contract/article.en.md" -->
<!-- codex ran: /bin/zsh -lc "rg -n '量尺|yardstick|grader|oracle' 2026-11-same-spec-overview/article.md 2026-11-same-spec-contract/article.md" -->
<!-- codex ran: /bin/zsh -lc 'git status --short' -->
<!-- codex ran: /bin/zsh -lc 'rg --files research/2026-10/same-spec-ten-runs/english-2026-10-26' -->
<!-- codex ran: /bin/zsh -lc "sed -n '1,100p' research/2026-10/same-spec-ten-runs/rebuild-2026-09-28/workbench/csv-transfer.md" -->
<!-- codex ran: /bin/zsh -lc 'cat research/2026-10/same-spec-ten-runs/english-2026-10-26/README.md' -->
A newer English production log does exist elsewhere in the repository. It supports Claude Code drafting at max effort, so the issue is the stale `STATUS.md` link and the claim that final checks are already recorded there. The remaining findings are narrower: input boundaries, evidence wording, maintenance responsibility, and translated phrasing.
I’ve finished the paragraph comparison. I found no dropped section, table row, code example, reference, or ending. The edits I’d prioritize are “complete input,” two sentences that turn insufficient evidence into “no result,” and wording that blurs a review obligation with expiry. The English also needs local fixes for vague actors and literal phrasing.
Read-only review completed. No missing sections, table rows, code examples, reference entries, or required links found. All eight tables match structurally; neither edition contains Mermaid. The frozen quotations, numerical results, HIGH/MAX distinction, and unexecuted P/Q status are preserved.

## Fatal

None found.

## Important

- **AI collaboration note — the linked record does not support the final sentence.**

  > “This English edition was written by Claude Code (max effort) from the final Chinese text; the paragraph-by-paragraph polish, second-model review and final checks are recorded in the same STATUS.md.”

  [STATUS.md](research/2026-10/same-spec-ten-runs/manuscripts/STATUS.md:45) still says no English manuscript was produced. The newer [English production record](research/2026-10/same-spec-ten-runs/english-2026-10-26/README.md) supports Claude Code drafting at max effort, but publication verification remains pending.

  **Fix:** Link the actual English record and distinguish completed work from pending checks:

  > “This English edition was drafted by Claude Code at max effort from the final Chinese text. Its drafting and completed reviews are documented in the English production record; final publication checks remain pending.”

- **3. Four frozen briefs: A0 is not a blank control, and C is not a Skill — “complete input” overstates the frozen boundary.**

  Chinese:

  > 同組十次收到的整包輸入（packet）完全相同，使用 `claude-opus-5-5`、high effort，也就是固定的推理投入設定；模型沒有工具，只能一次交付單一檔案。

  English adds:

  > “the complete input handed to the model (the brief together with the shared task instructions and the seed code)”

  The task packet is not the entire model context. SPECS.md separately identifies the shared system prompt; PROTOCOL.md explicitly limits what was pinned and observable.

  **Fix:**

  > “Within each group, all ten runs received exactly the same frozen task packet, containing the brief, shared task instructions and seed code. Generation used `claude-opus-5-5` at high effort, the fixed reasoning-effort setting; the model had no tools and delivered one file in a single shot.”

- **3. Four frozen briefs: A0 is not a blank control, and C is not a Skill — insufficient evidence becomes an absolute absence.**

  Chinese:

  > 本輪四組全過，也沒有提供足以證明這些增量有效的結果。

  English:

  > “With all four groups passing this round, there is no result that could show these increments effective either.”

  “沒有提供足以證明” means the results do not establish the benefit. “There is no result that could” is stronger and less precise.

  **Fix:**

  > “With all four groups passing, this round also provides insufficient evidence to establish a benefit from these additions.”

- **4. Comparing R05 sentence by sentence: the legal behavior is unchanged; what was added is reminders and a path — the same strengthening recurs.**

  Chinese:

  > 這一節把同一條要求拆成了規範、理由、自查與可選路徑，卻還沒有回答哪一種比較有效：四組都是 10/10，沒有足夠結果把成功歸給其中一段。

  English:

  > “This section has split one requirement into normative text, rationale, self-check and an optional path, but it has not answered which is more effective: all four groups scored 10/10, and there is no result that could credit the success to any one passage.”

  **Fix:**

  > “This section has separated one requirement into normative text, rationale, self-check and an optional implementation path, but it has not established which is more effective: all four groups scored 10/10, leaving insufficient evidence to attribute success to any particular passage.”

- **10. How document authors and Tech Leads divide the work: standing guidance, one-off specs and continuously maintained specs — review responsibility becomes expiry.**

  Chinese:

  > 到期責任，要在文字放進常駐指引時就寫清楚。

  English:

  > “Who reviews a passage, and when it expires, is written down at the moment the text enters the standing guidance.”

  “When it expires” suggests a predetermined expiry. The following paragraphs distinguish a review trigger from withdrawal.

  **Fix:**

  > “When a passage enters standing guidance, record who is responsible for reviewing whether it should remain.”

  The next paragraph already supplies the requirement to record the next review date.

## Minor

- **1. What “make the input handling more robust” has not yet answered — restore the plain-language introduction to “seed commit.”**

  Chinese:

  > 研究從固定的起始版本（seed commit）重現了兩個問題。

  English:

  > “The study reproduced two problems from a fixed seed commit.”

  The English drops “starting version,” leaving the technical label to explain itself.

  **Fix:**

  > “The study reproduced two problems in a fixed starting version of the parser, the seed commit.”

- **1. What “make the input handling more robust” has not yet answered — describe permission under the wording, rather than wording performing acceptance.**

  > “This piece calls a program awaiting acceptance a candidate; when we get to document changes, the recurring question will be ‘is a candidate that the old wording accepted still accepted after the change?’”

  **Fix:**

  > “This piece calls a program awaiting acceptance a candidate. When discussing document changes, I will keep asking: ‘Would a candidate permitted by the original wording still be permitted after the rewrite?’”

  This keeps the question about the legal set, distinct from what existing checks happen to accept.

- **2. Five kinds of sentence in one document: normative requirement, rationale, example, self-check and optional pattern — remove the calque around an unresolved decision.**

  > “My suggestion for review is to decide first which job a sentence is doing; if it is really searching for an answer to a decision nobody has made, label it separately as an undecided requirement.”

  **Fix:**

  > “During review, first identify what the sentence does. If it raises a behavioral choice that nobody has resolved, mark it separately as an undecided requirement.”

- **2. Five kinds of sentence in one document: normative requirement, rationale, example, self-check and optional pattern — give “update” a concrete object.**

  > “If editing a passage of ‘rationale’ turns a previously legal implementation illegal, that passage was already normative and should be handled as a requirement change: confirm with the affected callers and update the acceptance.”

  **Fix:**

  > “If editing a passage of ‘rationale’ makes a previously legal implementation illegal, treat the passage as normative and the edit as a requirement change: confirm the change with the affected callers and update the acceptance checks.”

- **3. Four frozen briefs: A0 is not a blank control, and C is not a Skill — finish the submission action.**

  > “So B's change gathers the existing requirements into one place, so they can be checked one by one before handing in.”

  **Fix:**

  > “B therefore gathers the existing requirements into one place so the implementer can check them individually before submitting the candidate.”

- **5. A sentence that looks synonymous: how A0 and A differ on the scope of new CLI options — “synonymous” needs a comparison.**

  > “A sentence that looks synonymous”

  **Fix the heading to:**

  > “5. Seemingly equivalent wording: how A0 and A differ on the scope of new CLI options”

  Also replace:

  > “Once decided, both texts are changed together, acceptance is made to check that decision, and only then is anything regenerated.”

  **With:**

  > “After the owner decides, update both texts and the acceptance checks to reflect that decision, then regenerate the candidates.”

- **7. Exploration, text, executable feedback: three interventions, three actions — the table obscures who installs which checks.**

  > “Write the mechanically decidable requirements as checks, in the environment or in acceptance”

  **Fix:**

  > “Turn mechanically decidable requirements into executable checks that the agent can run in its environment or that external acceptance can apply.”

  The owner column already assigns QA and the platform owner.

- **8. The spec change card: turning “just add the six self-check questions” into a reviewable change — state the hypothesis directly.**

  > “The card hopes the six self-check questions will reduce deliveries that fail the shared contract, and the unit of comparison is the whole checklist.”

  **Fix:**

  > “The hypothesis is that the six self-check questions will reduce submissions that fail the shared contract. The proposed comparison evaluates the checklist as a whole.”

- **9. Switching to a CSV export: how the same card is used — replace translated scaffolding with the actual decision.**

  > “Taking this over, the document author first separates the settled requirements from the open questions. Only the part this judgment needs is expanded below; it is not a complete date-conversion spec:”

  **Fix:**

  > “The document author first separates settled requirements from open questions. The draft below covers only what is needed to make that distinction; it is not a complete date-conversion spec:”

  Also replace:

  > “QA should fix the oracle that accepts only the CRLF template, keep the version, and re-score the affected candidates consistently.”

  **With:**

  > “QA should fix the oracle that accepts only the CRLF template, record its version, and consistently re-score the affected candidates.”

- **11. Closing: record why a sentence should stay, and when it should be withdrawn — make the opening question about behavior.**

  Chinese:

  > `text` 是 null、false 還是只有空白？

  English:

  > “Is `text` null, false, or whitespace only?”

  In English, this asks which value happens to be present. The surrounding argument asks what the parser should do with each value.

  **Fix:**

  > “How should the parser handle `text` when it is null, false, or whitespace only?”

  Also replace the dangling opening:

  > “Having read this far, when the question is ‘should I write one more paragraph’, my advice is to confirm first what that paragraph does.”

  **With:**

  > “When you next ask ‘Should I write another paragraph?’, my advice is to establish first what that paragraph does.”

## Suggested cuts

- **2. Five kinds of sentence in one document: normative requirement, rationale, example, self-check and optional pattern — an added qualification exceeds the Chinese definition.**

  Chinese:

  > 後文把「所有允許被接受的實作」簡稱為合法集合。

  English:

  > “From here on I call ‘the set of all implementations the contract allows to be accepted’ the legal set, whether or not the current checks recognize them correctly.”

  The final clause is an added explanatory claim. It is compatible with the argument, but unnecessary here.

  **Fix:**

  > “From here on, the legal set means all implementations permitted by the contract.”

- **10. How document authors and Tech Leads divide the work: standing guidance, one-off specs and continuously maintained specs — cut the extra announcement of an example.**

  > “Take the trigger ‘acceptance now covers this faulty version’: acceptance can catch the error, but the candidate may still have to be redone, and a self-check might reduce exactly that rework.”

  **Fix:**

  > “Acceptance can catch the error, but the candidate may still need rework; a self-check might reduce that rework.”

  No section-level cuts. The repeated examples and evidence limits otherwise correspond to the Chinese.

## Suggested additions

- **8. The spec change card: turning “just add the six self-check questions” into a reviewable change — clarify when the packets exist.**

  > “Before P and Q are built, confirm that acceptance catches the faulty version under study while accepting legal implementations; then check that this parser's two packets differ only by the original six self-check questions…”

  The opening condition can appear to govern checking packets that have not been built.

  **Fix by making the implied sequence explicit:**

  > “Before building P and Q, confirm that acceptance rejects the target faulty version and accepts legal implementations. After building the packets, verify that their only difference is the six original self-check questions.”

  Retain the subsequent cross-task checks, archival requirements and hashes. No new substantive section or evidence is needed.

## Terms still unclear

- **6. Confirm the premises before diagnosing: a wrong exit code cannot tell you what the model was thinking — introduce “slot.”**

  > “the original scheduled slot is kept rather than replaced by a new run.”

  This is the first use of an important counting unit.

  **Fix:**

  > “Retain the original slot—one scheduled generation attempt—rather than replacing it with a new run.”

- **6. Confirm the premises before diagnosing: a wrong exit code cannot tell you what the model was thinking — use the established controls terminology.**

  > “The positive-and-negative check in the table means taking examples known to satisfy the contract and examples known to violate it, and confirming first that the yardstick, the grader together with the oracle it uses, can tell them apart.”

  “Positive-and-negative check” needlessly introduces another name alongside “positive and negative controls.”

  **Fix:**

  > “Positive and negative controls are examples known to satisfy or violate the contract. They first check whether the yardstick—the grader together with its oracle—can distinguish the two.”

- **8. The spec change card: turning “just add the six self-check questions” into a reviewable change — define “qualifying deliveries.”**

  > “adoption_evidence: the difference in qualifying deliveries within the scope set in advance…”

  An English reader cannot tell whether “qualifying” means contract compliance, normal CLI completion, human approval, or the combined endpoint.

  **Fix:** Define the term at its first occurrence as:

  > “qualifying deliveries: submissions that meet the comparison’s acceptance conditions set in advance”

  Then retain that term consistently. Use “submissions that fail the shared contract” when discussing behavioral failures specifically; those are not interchangeable with operational failures.

<!-- tokens: in 1653276 out 22377 -->
