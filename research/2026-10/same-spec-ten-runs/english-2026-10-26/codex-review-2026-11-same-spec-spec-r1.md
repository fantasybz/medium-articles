# Codex review — 2026-11-same-spec-spec/article.en.md (round 1)

> model: gpt-6.1-sol, reasoning: xhigh, 2026-10-27 01:01. Codex's own words, not summarised. Round 1; reviewing the English edition against the final Chinese article and the frozen study.

I’ll read the writing standards first, then compare the English against the Chinese and frozen study records. I’ll stay inside the repository, read only, and leave all files unchanged.
<!-- codex ran: /bin/zsh -lc 'cat STYLE.md' -->
<!-- codex ran: /bin/zsh -lc 'cat research/2026-10/style_brief.md' -->
<!-- codex ran: /bin/zsh -lc 'cat research/experiments/same-spec-ten-runs/RESULTS.md research/experiments/same-spec-ten-runs/PROTOCOL.md' -->
<!-- codex ran: /bin/zsh -lc 'cat 2026-11-same-spec-spec/article.md' -->
<!-- codex ran: /bin/zsh -lc "wc -l 2026-11-same-spec-spec/article.md 2026-11-same-spec-spec/article.en.md 2026-10-green-payment/article.en.md 2026-11-aaif-agent-memory/article -->
<!-- codex ran: /bin/zsh -lc "sed -n '100,300p' 2026-11-same-spec-spec/article.md" -->
<!-- codex ran: /bin/zsh -lc "sed -n '301,469p' 2026-11-same-spec-spec/article.md" -->
The section structure and argument track the Chinese closely so far. I’m checking the restored English quotations against the frozen specs next; several passages presented as quotations need exact source matching.
<!-- codex ran: /bin/zsh -lc 'cat research/experiments/same-spec-ten-runs/SPECS.md research/experiments/same-spec-ten-runs/results/formal-2026-09-25/source/specs/A0.md research -->
<!-- codex ran: /bin/zsh -lc 'cat research/experiments/same-spec-ten-runs/results/formal-2026-09-25/source/specs/B.md research/experiments/same-spec-ten-runs/results/formal-202 -->
<!-- codex ran: /bin/zsh -lc "sed -n '1,100p' research/experiments/same-spec-ten-runs/RESULTS.md; cat research/2026-10/same-spec-ten-runs/manuscripts/STATUS.md" -->
<!-- codex ran: /bin/zsh -lc "sed -n '1,100p' 2026-10-green-payment/article.en.md; sed -n '1,110p' 2026-11-aaif-agent-memory/article.en.md" -->
<!-- codex ran: /bin/zsh -lc "nl -ba 2026-11-same-spec-spec/article.en.md | sed -n '1,190p'" -->
<!-- codex ran: /bin/zsh -lc "nl -ba 2026-11-same-spec-spec/article.en.md | sed -n '190,470p'" -->
I found one concrete record problem: the AI note says the English review and final checks are recorded in STATUS.md, but that file still says the English drafts have not been produced. I also found smaller meaning shifts involving optionality, advance planning versus preregistration, and “slot” being used for both a study run and a checklist position.
<!-- codex ran: /bin/zsh -lc "sed -n '312,340p' 2026-11-same-spec-spec/article.en.md; sed -n '1,80p' 2026-11-aaif-agent-memory/article.en.md; sed -n '330,430p' 2026-10-green-pa -->
<!-- codex ran: /bin/zsh -lc "rg -n '"'^#|P/Q|P／Q|288|not|尚未|未執行|重播|試驗|self-check|正例|陰|陽|負例'"' research/2026-10/same-spec-ten-runs/rebuild-2026-09-28/document-change-proposal.m -->
<!-- codex ran: /bin/zsh -lc "python3 -c 'from pathlib import Path; import re,collections,json
root=Path(\".\")
zh=(root/\"2026-11-same-spec-spec/article.md\").read_text(); en= -->
<!-- codex ran: /bin/zsh -lc "python3 -c 'from pathlib import Path; import re
z=Path(\"2026-11-same-spec-spec/article.md\").read_text();e=Path(\"2026-11-same-spec-spec/article. -->
The tables match in row and column counts, the reference numbering and back-pointers match, and the earlier-series links use the supplied English post IDs. There is no Mermaid in this piece. The remaining findings concern translation precision and English phrasing, especially wording that could imply text is executed or a policy decision can be automated.
<!-- codex ran: /bin/zsh -lc "rg -n '英文版維持|四篇英文主稿|288|全體任務|本輪也尚未|不是必須照抄|要求可以機械|原本只能閱讀文字|事前範圍|六個位置|對應位置|日期範圍|兩種缺口|第三部分特別|先把比較情境固定|多寫一段之前' research/2026-10/same-spec-ten-runs/man -->
Read-only audit against the repository copies. No whole Chinese paragraph, table row, code example, reference entry or section back-pointer is missing. All eight tables retain their dimensions. The earlier-series links use the supplied English IDs. There is no Mermaid in this article.

## Fatal

1. **AI collaboration note — the claimed English audit trail is unsupported.**

   > “This English edition was written by Claude Code (max effort) from the final Chinese text; the paragraph-by-paragraph polish, second-model review and final checks are recorded in the same STATUS.md.”

   This is an English-only addition. The repository’s [STATUS.md](research/2026-10/same-spec-ten-runs/manuscripts/STATUS.md:45) instead says all four English requests were rejected by the weekly limit and produced no manuscript. It contains no completed English review record.

   **Fix:** cite an actual English production and review record before making this assertion. Until then:

   > “This English edition translates the final Chinese manuscript. The linked STATUS.md documents the Chinese manuscript; it does not yet document this English edition’s production and review.”

   Retain the Claude/max attribution only if its generation record supports it. A stale status page does not establish that attribution is false, but it cannot substantiate the published claim.

## Important

1. **1. What “make the input handling more robust” has not yet answered — the comparison premise accidentally excludes the fault being compared.**

   Chinese:

   > 「先把比較情境固定：收到一則帶有 `text` 的訊息後，只再收到一個有效完成事件，沒有其他發言、明確失敗或格式錯誤。」

   English:

   > “after one message carrying a `text` value, exactly one valid completion event arrives, with no other message, no explicit failure and no format error.”

   “No format error” conflicts with the following `false`, `0` and `123` rows. Preserve the scope of “other.”

   **Fix:**

   > “For each row, the input contains one agent-message event with the listed `text` value, followed by one valid completion event. There are no other messages or malformed events, and no explicit failure.”

2. **1. What “make the input handling more robust” has not yet answered — blanket diagnosis becomes a prohibition on either diagnosis.**

   Chinese:

   > 「兩種缺口不能都靠實作者猜測，也不能一概診斷成需求未決。」

   English:

   > “Neither gap may be left to the implementer’s guess, and neither may be diagnosed wholesale as an undecided requirement.”

   One gap genuinely *is* an undecided requirement. The Chinese rejects classifying every gap that way.

   **Fix:**

   > “Neither gap should be left to the implementer’s guess, and the two must not be classified indiscriminately as undecided requirements.”

3. **3. Four frozen briefs: A0 is not a blank control, and C is not a Skill — optional copying becomes discouraged copying.**

   Chinese:

   > 「下面的虛擬流程是我的節譯；它像寫給實作者的路線草圖，用來說明處理順序，不是必須照抄的程式：」

   English:

   > “The pseudo-flow below is quoted from C’s original plain text; it reads like a route sketch for the implementer, there to explain the order of processing, not a program to be copied:”

   Restoring the original English is appropriate: the flow matches C. But “not a program to be copied” drops **必須**.

   **Fix:**

   > “The pseudo-flow below reproduces C’s original English. It sketches one possible processing order; implementations need not follow it verbatim.”

4. **6. Confirm the premises before diagnosing — the nonexecution disclaimer becomes article-wide.**

   Chinese:

   > 「表中的結果都依契約推導，沒有在本文中執行。」

   English:

   > “Every result in it is derived from the contract; nothing was executed for this piece.”

   “Nothing” broadens a disclaimer about this hypothetical example and invites confusion with the actual CSV teaching replay.

   **Fix:**

   > “The outcomes in this table are derived rather than observed; this hypothetical candidate was not executed.”

5. **7. Exploration, text, executable feedback — the text appears to become executable.**

   Chinese:

   > 「原本只能閱讀文字，現在還能執行並取得回饋，作用途徑已經不同。」

   English:

   > “Where before the text could only be read, now it can be executed and its feedback obtained; the pathway is different.”

   The referent of “it” is **the text**. The agent executes checks, not the self-check prose.

   **Fix:**

   > “With tools, the agent can also run the checks and receive feedback, so the mechanism is different.”

6. **7. Exploration, text, executable feedback — checking compliance becomes deciding a requirement.**

   Chinese:

   > 「要求可以機械判定時，先考慮把它寫成檢查；這可能比多寫一段文字更直接，但這只是推論，本輪沒有比較兩者。」

   English:

   > “If the requirement can be decided mechanically, consider writing it as a check first; that may be more direct than another paragraph, but this is an inference, and this round did not compare the two.”

   “Decided” suggests automating the owner’s policy decision—the distinction this article repeatedly protects.

   **Fix:**

   > “If compliance with a requirement can be checked mechanically, consider writing that check first. This may be more direct than adding another paragraph, but that is an inference; this round did not compare the two.”

7. **8. The spec change card — advance planning becomes preregistration.**

   Chinese:

   > `adoption_evidence: 事前範圍內的合格交付差距、各 requirement 的失敗、全部嘗試的費用與人工投入`

   English:

   > `adoption_evidence: the gap in qualified deliveries within the pre-registered scope, failures per requirement, cost and human effort of every attempt`

   “Pre-registered” adds a methodological commitment absent from **事前**. Elsewhere, the record carefully distinguishes a local freeze from third-party registration.

   **Fix:**

   > `adoption_evidence: the difference in qualifying deliveries within the scope set in advance, failures per requirement, and the cost and human effort of every attempt`

8. **8. The spec change card; 9. Switching to a CSV export — “slot” acquires two incompatible meanings.**

   Chinese:

   > 「每道自查只能指回該任務 P 已有的要求；六個位置依事前規則改寫，無對應義務的位置標成不適用，不另加問題湊滿六題。」

   English:

   > “the six slots are rewritten under rules fixed in advance, a slot with no corresponding obligation is marked not applicable”

   These are checklist **positions**, not scheduled generation slots.

   **Fix:**

   > “Rewrite the six checklist positions under rules fixed in advance. Mark a position with no corresponding obligation ‘not applicable’; do not invent a question merely to reach six.”

   Section 9 repeats the collision:

   Chinese:

   > 「在跨任務的自查範本裡，對應位置應依事前規則標成不適用。」

   English:

   > “In the cross-task self-check template, the corresponding slot is marked not applicable under the rules set in advance.”

   **Fix:** replace “slot” with “checklist position.” Reserve **slot** for a scheduled study run.

9. **9. Switching to a CSV export — “date ranges” implies an unestablished numerical-range policy.**

   Chinese:

   > 「走到這裡，文件已能支持下一步：QA 依核定的輸出義務修正 oracle，再重評候選；尚未決定的日期範圍由 owner 補齊。」

   English:

   > “QA fixes the oracle to the approved output obligations and re-scores the candidates; the date ranges not yet decided are filled in by the owner.”

   The Chinese is loose here. English “date ranges” specifically suggests earliest/latest permitted dates, whereas the example concerns unresolved date-handling policies.

   **Fix:**

   > “QA updates the oracle to reflect the approved output obligations and re-scores the candidates; the owner resolves the remaining questions about date handling.”

## Minor

1. **1. What “make the input handling more robust” has not yet answered — an emphasis becomes a ranking.**

   Chinese:

   > 「對這支 parser 來說，第三部分特別重要：既有診斷、exit 優先序與重複事件的處理，都是修補時必須保住的行為。」

   English:

   > “For this parser the third part matters most…”

   **特別重要** means especially important, not most important.

   **Fix:**

   > “For this parser, the third part is especially important: the fix must preserve the existing diagnostics, exit precedence and handling of duplicate events.”

2. **5. A sentence that looks synonymous — incomplete inspection becomes no inspection.**

   Chinese:

   > 「本輪也尚未針對這一點全面檢查保存的候選；即使補做檢查，仍不能單憑某份候選新增了什麼，就把原因歸給這一句話。」

   English:

   > “This round has not yet gone through the archived candidates for this point either…”

   Restore **全面**.

   **Fix:**

   > “The archived candidates have not yet been comprehensively checked for this point; even such a check could not, by itself, attribute an added option to this sentence.”

3. **2. Five kinds of sentence — “delivery” and “handing in” repeatedly sound translated.**

   > “What must the delivery do, and not do?”

   **Fix:**

   > “What must the delivered program do, and what must it avoid?”

   > “Which easily missed requirement should be rechecked before handing in?”

   **Fix:**

   > “Which easily missed requirement should the implementer recheck before submitting the candidate?”

   Apply **before submission** or **before submitting the candidate** consistently where “before handing in” otherwise lacks an object.

4. **3. Four frozen briefs — awkward agency and an overloaded comparison sentence.**

   > “Each of the four documents generated ten candidates.”

   **Fix:** “The model generated ten candidates from each brief.”

   > “Comparing A0 with A requirement by requirement across R01–R13, then reading the sections B and C each append, finds the differences more easily than rereading all four documents from the top.”

   **Fix:**

   > “To find the differences, compare A0 and A requirement by requirement across R01–R13, then read the sections appended by B and C. This is easier than rereading all four documents from the beginning.”

5. **6. Confirm the premises before diagnosing — a table does not “meet” an error.**

   > “It also meets another kind of error: the contract allows different explanatory wording, but the check insists on matching the reference program word for word.”

   **Fix:**

   > “The table also covers another error: the contract allows different explanatory wording, but the check requires a word-for-word match with the reference program.”

6. **7. Exploration, text, executable feedback — Chinese sentence structure survives.**

   > “B’s sixth question reminds in exactly the opposite direction: do not add sequence rules.”

   **Fix:**

   > “B’s sixth question gives the opposite reminder: do not add sequence rules.”

7. **8. The spec change card — notes intrude into finished prose.**

   > “The nature of the card first…”

   **Fix:** “First, establish what this card represents…”

   > “the reviewer who takes over records how long understanding, fixing and reviewing each took.”

   “Each” has no clear object.

   **Fix:**

   > “The reviewer records the time spent understanding, fixing and reviewing each candidate.”

8. **9. Switching to a CSV export — the hand-off is a calque.**

   > “Following the Overview’s subsequent assumption, the owner decides…”

   **Fix:**

   > “Continue the hypothetical scenario from the Overview: the owner decides…”

   > “The document author then moves the null answer into the requirements…”

   **Fix:**

   > “The document author then records the null-date policy as a requirement…”

9. **10. How document authors and Tech Leads divide the work — responsibility is obscured by abstract nouns.**

   > “Expiry responsibility is written down at the moment text enters the standing guidance.”

   **Fix:**

   > “When adding standing guidance, name who will review it and decide when it should be withdrawn.”

   > “whether the failures and the takeover burden after removing it are acceptable.”

   **Fix:**

   > “whether removing it would leave an acceptable number of failures and an acceptable workload for whoever takes over.”

10. **11. Closing — the heading and final hand-off need natural English.**

   > “Closing: leave a reason that can keep a sentence, and can withdraw it”

   **Fix:**

   > “Closing: record why a sentence should stay, and when it should be withdrawn”

   > “given a program, how do I know it did it?”

   **Fix:**

   > “Given a program, how do I know it meets the requirements?”

11. **11. Closing — the final sentence preserves ownership but blurs which decision must be identified.**

   Chinese:

   > 「多寫一段之前，先確認它要替誰解決哪個選擇；寫下它的同時，也寫下它何時應該撤回。」

   English:

   > “Before writing one more paragraph, confirm whose choice it is meant to settle; and as you write it, write down when it should be withdrawn.”

   **Fix:**

   > “Before adding a paragraph, identify the choice it is meant to resolve and whose decision it is; as you write it, record when it should be withdrawn.”

## Suggested cuts

1. **3. Four frozen briefs — shorten the additional quotation without removing the execution boundary.**

   > “C itself says it is ‘an optional plain-text implementation pattern, not a runtime skill, installed plugin, hook or tool invocation’, so the pattern here is not a native Skill, plugin or hook that an agent can load and use.”

   The preceding sentence already says the text installs nothing and executes nothing. The Chinese does not contain this additional quotation.

   **Replace with:**

   > “The pattern is therefore not a native Skill, plugin or hook an agent can load and use.”

2. **4. Comparing R05 sentence by sentence — remove unnecessary quotation-management prose.**

   > “The wording below paraphrases A0’s R05 and keeps its terms.”

   **Cut this sentence.** Retain the complete rule and its explanations. The Chinese proceeds directly from introducing R05 to explaining it.

   Do not cut the later limitations merely because they recur: their Chinese counterparts are present and qualify different decisions.

## Suggested additions

1. **3. Four frozen briefs — name the interval and scope its assumptions to each group.**

   > “Assuming the runs are independent, identically distributed and share one success probability, each group’s 10/10 gives an exact two-sided 95% Clopper–Pearson interval…”

   **Replace with:**

   > “Within each group, assuming the ten runs are independent Bernoulli trials with a common success probability, 10/10 yields an exact two-sided 95% confidence interval of about 69.15% to 100%.”

   This clarifies the existing condition without implying that all four groups share one probability.

2. **8. The spec change card — distinguish message output from total stdout.**

   > `legal_cases: null and "" produce no output; " " is printed unchanged and counts as spoken`

   Chinese likewise abbreviates this as:

   > `legal_cases: null 與 "" 不輸出；" " 原樣印出並算發言`

   **Replace with:**

   > `legal_cases: null and "" produce no agent-message output; " " is printed unchanged and counts as an agent message`

   A subsequent valid completion still produces its token comment. The change prevents readers from interpreting “no output” as empty stdout for the entire stream.

## Terms still unclear

1. **3. Four frozen briefs — brief / spec / packet need one explicit relationship.**

   > “The ten runs in a group received exactly the same packet, the complete bundle of input…”

   The reader knows a packet is complete, but not precisely how it differs from the document being compared.

   **Fix the definition:**

   > “The brief is the spec text. The packet is the complete input, including that brief and the seed code.”

2. **6. Confirm the premises before diagnosing — yardstick / oracle / grader / acceptance should not drift into interchangeable names.**

   > “The positive-and-negative check in the table means taking known-legal and known-faulty examples and confirming first that the yardstick can tell them apart.”

   **Clarify once:**

   > “Here, ‘yardstick’ means the acceptance checks as a whole. The grader runs them; the oracle supplies the expected result or judgment rule.”

   Use **acceptance check**, rather than “an acceptance,” when referring to an individual executable check.

3. **1. What “make the input handling more robust” has not yet answered; 8. The spec change card — qualified / legal / passed describe different judgments.**

   > “is a candidate that qualified before the change still qualified after it?”

   For the semantic comparison, **qualified** obscures whether this means permitted by the wording or observed to pass tests.

   **Fix:**

   > “Would an implementation permitted by the old wording still be permitted after the change?”

   Reserve **passes the frozen checks** for observed study results. Use **permitted by the spec** for the legal-set argument. This keeps the 103-check result from quietly becoming proof of complete contract compliance.

<!-- tokens: in 1408728 out 19554 -->
