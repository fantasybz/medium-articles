# Codex review — 2026-11-same-spec-variance/article.en.md (round 1)

> model: gpt-6.1-sol, reasoning: xhigh, 2026-10-27 01:08. Codex's own words, not summarised. Round 1; reviewing the English edition against the final Chinese article and the frozen study.

I’ll read the repository’s writing standards first, then compare the English against the Chinese and frozen study files. I’ll keep the review read-only and stay inside the repository.
<!-- codex ran: /bin/zsh -lc 'cat STYLE.md' -->
<!-- codex ran: /bin/zsh -lc 'cat research/2026-10/style_brief.md' -->
<!-- codex ran: /bin/zsh -lc 'cat research/experiments/same-spec-ten-runs/SPECS.md' -->
<!-- codex ran: /bin/zsh -lc "sed -n '1,180p' 2026-11-same-spec-variance/article.md" -->
<!-- codex ran: /bin/zsh -lc 'wc -l 2026-11-same-spec-variance/article.md 2026-11-same-spec-variance/article.en.md research/experiments/same-spec-ten-runs/{RESULTS,SPECS,PROTOC -->
<!-- codex ran: /bin/zsh -lc 'cat research/experiments/same-spec-ten-runs/RESULTS.md research/experiments/same-spec-ten-runs/PROTOCOL.md' -->
<!-- codex ran: /bin/zsh -lc "sed -n '181,330p' 2026-11-same-spec-variance/article.md" -->
<!-- codex ran: /bin/zsh -lc "sed -n '1,115p' 2026-10-green-payment/article.en.md
sed -n '1,120p' 2026-11-aaif-agent-memory/article.en.md" -->
<!-- codex ran: /bin/zsh -lc 'cat research/experiments/same-spec-ten-runs/RESULTS.md' -->
<!-- codex ran: /bin/zsh -lc "sed -n '291,442p' 2026-11-same-spec-variance/article.md" -->
The main evidence limits are preserved so far: the English does not rank the four briefs, and it keeps P/Q and the 288 slots explicitly unexecuted. I’m checking the exact spec wording next, along with sentence-level shifts and the English edition’s collaboration note.
<!-- codex ran: /bin/zsh -lc 'cat research/experiments/same-spec-ten-runs/PROTOCOL.md' -->
<!-- codex ran: /bin/zsh -lc 'cat research/experiments/same-spec-ten-runs/results/formal-2026-09-25/source/specs/A0.md research/experiments/same-spec-ten-runs/results/formal-20 -->
<!-- codex ran: /bin/zsh -lc 'cat research/2026-10/same-spec-ten-runs/manuscripts/STATUS.md' -->
<!-- codex ran: /bin/zsh -lc "sed -n '1,65p' 2026-10-green-payment/article.en.md
rg -n '"'^(#|> Series|### AI)|written by|English edition'"' 2026-11-same-spec-{overview,spec,co -->
<!-- codex ran: /bin/zsh -lc "sed -n '30,67p' 2026-11-same-spec-contract/article.en.md
sed -n '74,142p' 2026-11-same-spec-spec/article.en.md
sed -n '225,247p' 2026-11-same-spec -->
<!-- codex ran: /bin/zsh -lc "sed -n '262,292p' 2026-11-same-spec-variance/article.md
rg -n 'English|英文|variance|變異' research/2026-10/same-spec-ten-runs/manuscripts --glob '*.m -->
<!-- codex ran: /bin/zsh -lc "python3 -c 'from pathlib import Path
root=Path(\"research/experiments/same-spec-ten-runs/results/formal-2026-09-25/source/specs\")
a,b,c=(root.joi -->
<!-- codex ran: /bin/zsh -lc "python3 -c 'from pathlib import Path
import re,collections
z=Path(\"2026-11-same-spec-variance/article.md\").read_text(); e=Path(\"2026-11-same-sp -->
The mechanical checks found no missing table rows, changed Python instructions or YAML fields. The links differ only where expected for English editions, and this article has no Mermaid blocks. Two issues need attention: the linked STATUS.md has no English-review records despite the note claiming it does, and the R03 summary omits R10’s additional failure diagnostic.
<!-- codex ran: /bin/zsh -lc 'cat research/2026-10/same-spec-ten-runs/rebuild-2026-09-28/static-review-walkthrough.md' -->
<!-- codex ran: /bin/zsh -lc "nl -ba 2026-11-same-spec-variance/article.en.md | sed -n '1,145p'" -->
<!-- codex ran: /bin/zsh -lc "cat research/2026-10/same-spec-ten-runs/rebuild-2026-09-28/workbench/README.md
sed -n '1,165p' research/2026-10/same-spec-ten-runs/rebuild-2026-09 -->
<!-- codex ran: /bin/zsh -lc "nl -ba 2026-11-same-spec-variance/article.en.md | sed -n '145,232p'" -->
<!-- codex ran: /bin/zsh -lc "sed -n '70,102p' research/experiments/same-spec-ten-runs/results/formal-2026-09-25/formal-02-A0/candidate/codex_jsonl.py
sed -n '106,130p' researc -->
<!-- codex ran: /bin/zsh -lc "nl -ba 2026-11-same-spec-variance/article.en.md | sed -n '258,395p'" -->
<!-- codex ran: /bin/zsh -lc "rg -n '英文版維持|四篇英文主稿|逐段修訂|This English edition|same on paper|nothing counts|exactly one stderr diagnostic|if that line used|Human cost that|human c -->
One technical example is wrong in both editions: replacing the first guard in `formal-02-A0` with `if text:` would return early for valid nonempty strings. Skipping `false` and `0` would require a false-like guard such as `if not text: return`. I’ll distinguish inherited source issues from translation errors in the review.
<!-- codex ran: /bin/zsh -lc "rg -n 'proxy review|代理 review|proxy_review|review proxy|qualified delivery|三個出口' research/2026-10/same-spec-ten-runs/rebuild-2026-09-28/{compariso -->
<!-- codex ran: /bin/zsh -lc "rg --files --hidden research/2026-10/same-spec-ten-runs .context -g '*english*' -g '*provenance*' -g '*en-*' -g '*en.*' -g '"'!**/.claude/**'"' -g -->
<!-- codex ran: /bin/zsh -lc "rg --files --hidden .context/same-spec-en-2026-10-26 -g '"'!**/.claude/**'"' -g '"'!**/agents/**'"' -g '"'!**/skills/**'"'" -->
The remaining findings concern wording: “same on paper” obscures that 10/10 was observed, “nothing counts as a spoken message” has unclear scope, and “supply … the yardstick’s blind spots” weakens the closing argument. The English-only yardstick definitions can also be cut without losing anything in the Chinese.
## Fatal

None found in the central study claims. The English preserves the conditional Clopper–Pearson interpretation, the limits of 40/40, HIGH generation versus MAX writing, and the unexecuted P/Q design.

Mechanical checks: all seven tables retain their rows and columns; Python instructions and YAML fields match; there is no Mermaid. References 1–13 preserve numbering, URLs and section back-pointers. Earlier-series links use the supplied English IDs. The Chinese-edition links are present.

## Important

1. **AI collaboration note — the claimed English audit trail is missing from STATUS.md.**

   > “This English edition was written by Claude Code (max effort) from the final Chinese text; the paragraph-by-paragraph polish, second-model review and final checks are recorded in the same STATUS.md.”

   The repository’s [STATUS.md](research/2026-10/same-spec-ten-runs/manuscripts/STATUS.md:45) still says the English drafts were not produced and lists their drafting and polishing as unfinished. English drafts and review logs exist under `.context/same-spec-en-2026-10-26/`, so this is an outdated public record, not proof that the work never happened.

   **Fix:** replace the recorded-checks assertion until the public record supports it:

   > “This English edition follows the final Chinese manuscript. Its English-specific drafting and review records have not yet been added to STATUS.md.”

   Retain the Claude Code/MAX attribution only against an actual execution record.

2. **7. “Two candidates that both passed” — the truthiness counterfactual is technically wrong in both editions.**

   > “if that line used `if text:` … `false` and `0` would be treated as no message and simply skipped.”

   Chinese:

   > 「這個順序本身沒有錯，卻讓第一個判斷成為關鍵：如果那一行用 `if text:` 判斷值是真還是假（truthiness），把所有『看起來是空的』值一起放行，`false` 與 `0` 就會被當成沒有訊息，直接略過。」

   In the actual `formal-02-A0`, that condition guards a `return`. Replacing its condition with `if text:` would skip valid nonempty strings; `false` and `0` would reach the following type check and be rejected.

   **Fix:**

   > “If that guard were replaced with `if not text: return`, it would silently skip `false` and `0` along with null and the empty string.”

   This is an inherited source error. Resolve it explicitly rather than silently treating it as a translation correction.

3. **7. R03 summary — “exactly one stderr diagnostic” omits the R10 exception.**

   > “R03 then requires that each bad line leave exactly one stderr diagnostic…”

   Chinese:

   > 「R03 接著要求：每個壞行只留一則診斷，仍要繼續讀後面的輸入。」

   Frozen R03 requires exactly one **malformed-event** diagnostic. A malformed `turn.failed` also emits its legacy R10 failure diagnostic.

   **Fix:**

   > “R03 requires exactly one malformed-event diagnostic per malformed line and continued processing. A `turn.failed` event also retains its R10 failure diagnostic, even when malformed.”

   This qualification is also missing from the Chinese summary.

4. **2. “Say first what changed this time” — one generation per candidate becomes one generation for the study.**

   > “The formal study was a single generation without tools…”

   Chinese:

   > 「正式研究是無工具的一次生成，模型不會安裝套件、建置專案或執行測試。」

   The English singular is especially easy to misread against forty generations.

   **Fix:**

   > “Each of the formal study’s forty candidates came from one generation without tools; the model did not install packages, build the project or run tests.”

5. **7. R05 summary — “nothing counts” loses the scope of the condition.**

   > “when `text` is missing, `null` or the empty string, it means no message and produces nothing, and nothing counts as a spoken message”

   Chinese:

   > 「R05 是訊息欄位的要求編號：`text` 缺值、為 `null` 或空字串時，不輸出，也不算發言；非空字串要原樣印出，立即送給呼叫端（flush），只有空白的字串也有效。」

   **Fix:**

   > “R05 governs agent-message text. Missing `text`, null and the empty string produce no output and do not count as spoken messages. Nonempty strings are printed unchanged and flushed immediately; whitespace-only strings remain valid.”

   In the following worked example, replace “prints nothing” with **“emits nothing on stdout”** so it does not appear to contradict the stderr diagnostic.

6. **6. Decision table, “Observations cannot discriminate” — the quantifiers permit a discriminating result.**

   > “Every arm passes or fails in full”

   Chinese cell:

   > 「各組都全過或全敗」

   The English permits one arm passing everything while another fails everything.

   **Fix:**

   > “All arms pass every trial, or all arms fail every trial.”

## Minor

1. **3. Heading — “on paper” shifts an observed result toward a theoretical or nominal one.**

   > “Four arms at 10/10: the same on paper, not equivalent”

   Chinese:

   > 「四組 10/10：結果字面相同，不代表等效」

   **Fix:**

   > “Four arms at 10/10: identical observed results do not establish equivalence”

2. **1. Opening — conspicuous translation phrasing.**

   > “The place that deserves the real question is the next assignment…”

   **Fix:**

   > “The real question arises with the next assignment: will these six questions keep helping, or did they merely appear alongside this one success?”

   Also complete:

   > “decides whether to adopt, keep or withdraw”

   **Fix:**

   > “decides whether to adopt the self-check, maintain the current policy or withdraw it.”

3. **2. and 9. — “read/written backward” is repeatedly calqued.**

   > “These studies cannot be read backward into the causes in this series.”

   **Fix:**

   > “These studies do not establish what caused the differences observed in this series.”

   In **9., opening**, replace:

   > “it cannot be written backward as a continuation of that round”

   with:

   > “it must not be retrospectively presented as a continuation of that study.”

   In **9., “Assignment and environment,”** replace:

   > “it cannot be written backward as having already controlled for time”

   with:

   > “the study must not be retrospectively described as having controlled for time.”

4. **3. Cost discussion — the EM needs information, not cost.**

   > “the human cost that an EM needs most … was not measured”

   **Fix:**

   > “The human-cost data an EM needs most were not collected: time spent reading code, making corrections, approving changes and maintaining documents.”

   Also replace:

   > “Four arms with the same wide interval still have not identified their unknown success rates as one and the same value.”

   with:

   > “Identical wide intervals do not establish that the four arms have the same unknown success probability.”

5. **4. Usage policies — “takes two discounts” suggests numerical adjustments.**

   > “The 99.2% figure takes two discounts.”

   **Fix:**

   > “The 99.2% figure needs two qualifications.”

   Use “qualification” for the feedback paragraph too. Neither paragraph computes a discount.

   Also:

   > “The original study is a simulated customer service for retail and airlines…”

   **Fix:**

   > “The original study uses simulated customer-service tasks in retail and aviation…”

6. **5. Task-level results — awkward observation language and ambiguous agency.**

   > “a few tasks improved a great deal in observation”

   **Fix:**

   > “a few tasks showed much better observed results”

   And:

   > “this is called preserving task clustering, and it allows multiple results on the same task to be dependent”

   **Fix:**

   > “This preserves task clustering: the analysis allows for dependence among repeated results from the same task.”

7. **7. Review actions — “accepted” blurs a policy decision with checking an implementation.**

   > “here it was decided by the frozen contract, and was accepted together with the existing compatibility behaviors…”

   Chinese:

   > 「R05 的選擇在別的產品中可能不同；本次已由凍結契約決定，並與其他條文要求保留的既有相容行為一起驗收。」

   **Fix:**

   > “Here, the frozen contract settled the R05 policy, and acceptance checked the corresponding behavior alongside the legacy compatibility behaviors required by the other clauses.”

8. **9. “Fix the policy first” — a slot cannot perform work.**

   > “Each scheduled slot starts from a repo … and works within tools, permissions and budget fixed in advance.”

   **Fix:**

   > “For each scheduled slot, start a fresh session with the repo restored to the designated commit. The agent works within the tools, permissions and budget fixed in advance.”

9. **9.–11. — several administrative calques obscure otherwise concrete actions.**

   **9., “Where the tasks come from”:**

   > “the authors state on their own initiative”

   **Fix:** “the authors explicitly caution”

   **10., “How to record time”:**

   > “when agents work in parallel, whose hours they are is itself hard to determine”

   **Fix:**

   > “when agents work in parallel, attributing human working time is itself difficult.”

   **11., opening:**

   > “the owner who bears the decision”

   **Fix:** “the owner responsible for the decision”

10. **11. “Withdrawal and re-examination” — distinguish reduced effort from reduced oversight.**

    > “The self-check may still reduce failures, rework and human takeover…”

    Chinese:

    > 「自查仍可能減少失敗、重做與人工接手；移除之前，要先確認移除後的這些負擔仍可接受。」

    **Fix:**

    > “The self-check may still reduce failures, rework and the effort required for human takeover; before removing it, confirm that those burdens remain acceptable after removal.”

11. **12. Closing — the last sentence should identify gaps to address, not things evidence “supplies.”**

    > “the next piece of evidence has to supply the task scope, the yardstick’s blind spots, and the human effort.”

    Chinese:

    > 「當決定已經超出這一題，下一筆證據就要補上任務範圍、量尺盲點與人的投入。」

    **Fix:**

    > “Once the decision extends beyond this task, the next evidence must address gaps in task coverage, the yardstick’s ability to detect faults, and measured human effort.”

    Earlier in the same section:

    > “arrange for a real person to be observed”

    **Fix:**

    > “observe someone taking over the work and record their time.”

## Suggested cuts

1. **3. EvalPlus paragraph — remove the English-only definition of yardstick.**

   > “‘No failure observed’ covers only what the yardstick, the acceptance checks and the program that scores them, can see.”

   Chinese:

   > 「所謂『沒有觀察到失敗』，只涵蓋量尺看得見的範圍。」

   **Fix:**

   > “‘No failure observed’ covers only what the yardstick can see.”

2. **8. First regression action — remove another English-only definition.**

   > “the oracle and the grader together are the yardstick.”

   Chinese only says:

   > 「第一種動作檢查評分程式（grader）。」

   This adds a technical definition the Chinese does not make, while §3 supplies a different formulation.

   **Fix:** retain only:

   > “The first action checks the grader, the scoring program.”

No paragraph-level cuts: the repeated qualifications and operational detail are present in the final Chinese. Removing them would reduce fidelity and depth.

## Suggested additions

- **7. R03/R10:** add the failed-turn exception identified above.
- **AI collaboration note:** supply an accurate English-specific public record before claiming that drafting, second-model review and final checks are documented.
- No additional studies, experiences or hypothetical examples are needed.

## Terms still unclear

1. **2., variation table — “blocks of environment.”**

   > “How tasks are sampled; blocks of environment”

   **Fix:**

   > “Task-sampling design; blocks defined by environment conditions”

   “Blocks of environment” is not idiomatic experimental-design English.

2. **9., “Across tasks, fix the rewriting policy first” — distinguish template positions from execution slots.**

   > “keep the six positions”

   **Fix:** “retain the six checklist positions”

   > “number of valid positions”

   **Fix:** “number of applicable checklist positions”

   Keep **slot** for scheduled executions.

3. **9., same subsection — preserve the event identifier.**

   > “EOF, tokens and the root-level error”

   **Fix:**

   > “EOF, token counts and the top-level `error` event”

   Also use **“parser spec change card”** rather than “parser change card” to match Part 1’s named artifact.

4. **10.–11. — “qualified delivery” sounds like a credential or sales classification.**

   > “human effort per qualified delivery”

   **Fix:** first identify a **“final delivery accepted after human handling,”** then consistently use **“accepted final delivery.”** Keep this distinct from acceptance of the agent’s original candidate.

5. **6. table and 11. ROI discussion — “proxy review” never identifies the mechanism.**

   > “AST similarity, proxy review, model list prices”

   Specify what performs this review. If agent review is intended, use **“AI-generated code-review reports.”** Do not leave readers guessing whether this means an agent’s review, a simulated human review or a structural proxy.

No files changed.

<!-- tokens: in 1908910 out 20954 -->
