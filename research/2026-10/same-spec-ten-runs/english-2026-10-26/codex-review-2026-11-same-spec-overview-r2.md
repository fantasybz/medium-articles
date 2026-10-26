# Codex review — 2026-11-same-spec-overview/article.en.md (round 2)

> model: gpt-6.1-sol, reasoning: xhigh, 2026-10-27 01:05. Codex's own words, not summarised. Round 2; reviewing the English edition against the final Chinese article and the frozen study.

I’ll read the writing standards first, then compare the English against the Chinese source and frozen study. I’ll keep all work read-only and inside this repository.
<!-- codex ran: /bin/zsh -lc 'cat STYLE.md' -->
<!-- codex ran: /bin/zsh -lc 'cat research/2026-10/style_brief.md' -->
<!-- codex ran: /bin/zsh -lc "sed -n '1,225p' 2026-11-same-spec-overview/article.md" -->
<!-- codex ran: /bin/zsh -lc "sed -n '1,145p' 2026-10-green-payment/article.en.md
sed -n '1,130p' 2026-11-aaif-agent-memory/article.en.md" -->
<!-- codex ran: /bin/zsh -lc 'rg --files research/experiments/same-spec-ten-runs research/2026-10/same-spec-ten-runs/manuscripts 2026-11-same-spec-overview 2026-11-same-spec-sp -->
<!-- codex ran: /bin/zsh -lc "sed -n '180,390p' 2026-11-same-spec-overview/article.md" -->
The English appears to retain the main evidence limits, including the lack of a ranking from 40/40 passes and the unexecuted P/Q proposal. I’m now checking the spec quotations and recording smaller meaning shifts separately from awkward English.
<!-- codex ran: /bin/zsh -lc 'cat research/experiments/same-spec-ten-runs/RESULTS.md' -->
<!-- codex ran: /bin/zsh -lc "sed -n '125,180p' 2026-11-same-spec-overview/article.md
sed -n '390,500p' 2026-11-same-spec-overview/article.md" -->
<!-- codex ran: /bin/zsh -lc 'cat research/experiments/same-spec-ten-runs/results/formal-2026-09-25/source/specs/A0.md
cat research/experiments/same-spec-ten-runs/results/forma -->
<!-- codex ran: /bin/zsh -lc 'cat research/experiments/same-spec-ten-runs/PROTOCOL.md
cat research/experiments/same-spec-ten-runs/SPECS.md' -->
<!-- codex ran: /bin/zsh -lc 'cat research/2026-10/same-spec-ten-runs/manuscripts/STATUS.md' -->
<!-- codex ran: /bin/zsh -lc "rg -n '"'^#{1,3} |288|budget|預算|obligation table|change card|self-check|qualifying|accepted'"' 2026-11-same-spec-{overview,spec,contract,variance} -->
<!-- codex ran: /bin/zsh -lc "sed -n '1,80p' 2026-10-green-payment/article.en.md
sed -n '165,210p' 2026-11-aaif-agent-memory/article.en.md
sed -n '290,330p' 2026-10-green-payme -->
<!-- codex ran: /bin/zsh -lc "rg --files --hidden -g '"'!**/.git/**'"' -g '"'!**/.claude/**'"' -g '"'!**/.agents/**'"' -g '"'!**/agents/**'"' research/2026-10/same-spec-ten-run -->
<!-- codex ran: /bin/zsh -lc "python3 -B -c 'from pathlib import Path; base=Path(\"research/experiments/same-spec-ten-runs/results/formal-2026-09-25/source/specs\"); a,b,c=[(ba -->
<!-- codex ran: /bin/zsh -lc "rg --files --hidden -g '"'!**/.git/**'"' -g '"'!**/.claude/**'"' -g '"'!**/.agents/**'"' -g '"'!**/agents/**'"' .context/same-spec-en-2026-10-26 r -->
<!-- codex ran: /bin/zsh -lc "cat .context/same-spec-en-2026-10-26/brief.md
cat .context/same-spec-en-2026-10-26/writers-started-at.txt
rg -n 'English|英文|overview|Opus|max|mode -->
I found two remaining fidelity issues: “less information” becomes “less text,” and §3 adds Lamport quotations absent from the Chinese. The AI note also claims English checks are recorded in STATUS.md, but that page still lists the English drafts and checks as unfinished.
<!-- codex ran: /bin/zsh -lc "sed -n '1,115p' MERMAID.md
cat 2026-11-same-spec-overview/publish/en/figures.json" -->
<!-- codex ran: /bin/zsh -lc "cat research/2026-10/same-spec-ten-runs/rebuild-2026-09-28/document-change-proposal.md
sed -n '1,180p' research/2026-10/same-spec-ten-runs/rebuild -->
<!-- codex ran: /bin/zsh -lc "python3 -B -c '
from pathlib import Path
import re, json
base=Path(\"2026-11-same-spec-overview\")
z=(base/\"article.md\").read_text(); e=(base/\" -->
<!-- codex ran: /bin/zsh -lc "python3 -B -c '
from pathlib import Path
import re,json
b=Path(\"2026-11-same-spec-overview\")
s=(b/\"article.en.md\").read_text()
m=json.loads((b -->
<!-- codex ran: /bin/zsh -lc "nl -ba 2026-11-same-spec-overview/article.en.md | sed -n '1,95p'
nl -ba 2026-11-same-spec-overview/article.en.md | sed -n '205,235p'
nl -ba resear -->
The source audit is complete: table dimensions, code examples, reference numbering, back-pointers and link targets match. The existing English publication assets are stale, however: the diagram and tables 1, 4 and 6 still contain older wording, including “Fix the … fixtures” where the manuscript now says “Hold … constant.”
## Fatal

None found in the study claims. The English preserves the limits on 40/40, the i.i.d./common-p assumptions behind the Clopper–Pearson interval, the unexecuted P/Q design, the teaching material’s separate status, and HIGH generation versus MAX writing effort.

The R05, R13 and C quotations match the frozen English specs. Reference numbering, URLs, section back-pointers, table dimensions, JSON/text examples and final closure are carried across. Mermaid config and node IDs are unchanged.

## Important

1. **AI collaboration note — the linked record does not support the English-check claim.**

   > “the paragraph-by-paragraph polish, second-model review and final checks are recorded in the same STATUS.md.”

   [STATUS.md:45](research/2026-10/same-spec-ten-runs/manuscripts/STATUS.md:45) still says the English manuscripts, polishing and figures are unfinished, including “沒有正文產出.”

   **Fix:** remove the quoted clause until STATUS.md identifies the English draft, reviewed revision and completed checks. Retain the Claude Code/MAX attribution only where the generation record supports it. This is a documentation contradiction, not proof that the English work never happened.

2. **6. A narrow case: four briefs, forty candidates, all 103 checks passed — information becomes length.**

   Chinese:

   > 另一項研究提供了對照，提醒我們別把「資料少」直接當成「比較便宜」。

   English:

   > “Another study offers a counterpoint, a reminder not to equate ‘less text’ with ‘cheaper.’”

   “Less text” changes the variable from information supplied to document length—the distinction the following paragraphs explicitly defend.

   **Fix:** “Another study offers a counterpoint: less information does not necessarily mean lower cost.”

3. **3. Book anchor: Lamport’s blueprints preserve the choices already made — two quotation expansions are English-only additions.**

   Chinese:

   > 第一，寫下規格，會迫使作者在修改程式之前先說清楚程式應該做什麼；很多沒想清楚的地方，要試著寫下來時才會浮現。

   English adds:

   > “Before we start to write any piece of code, we should understand what that code is supposed to do.”

   Chinese:

   > 他也交代了自己的界線：寫規格不能保證程式不會崩潰，要消除 coding bug，仍需要其他方法。

   English replaces the paraphrase with:

   > “By itself, writing specs won’t ensure that our programs never crash. We still need to use methods and tools that have been developed for eliminating coding bugs.”

   These are additional quotations, even if accurately sourced. The Chinese does not present them.

   **Fix:**

   > “First, writing a spec forces the author to state what the program should do before modifying the code. Gaps in our thinking often surface only when we try to write it down.”

   > “He also states the limit: writing specs cannot guarantee that programs will never crash; eliminating coding bugs still requires other methods.”

4. **4. Three layers of question… / 7. After everything passes… / 9. A one-page proposal… — the publication assets contain older wording.**

   The current §7 table says:

   > “Hold the verified positive and negative control fixtures constant”

   The [existing table image](2026-11-same-spec-overview/publish/en/images/table-04.png) still says:

   > “Fix the positive and negative fixtures with verified behavior”

   “Fix” can mean repair them, which changes the intended action. Tables 1 and 6 and the diagram also differ from the manuscript; the diagram still uses “cases” where the source now uses “controls.”

   **Fix:** regenerate the English publication package from the reviewed manuscript. Recheck the resulting diagram width. The existing render is about 760 CSS px wide, but it does not render the current wording.

## Minor

1. **1. After the workshop gap, the question changed its target — the heading is a calque.**

   > “After the workshop gap, the question changed its target”

   **Fix:** “The workshop gap led me back to the brief.”

   Also:

   > “I left a note that I have gone back to many times since.”

   **Fix:** “I recorded an observation that I have returned to many times since.”

2. **1. After the workshop gap… — the previous-series hand-off is buried in nominalizations.**

   > “Green Is Not Done started from the acceptance of what was produced, and followed the question onward to the responsibility of review…”

   **Fix:** “Green Is Not Done began by asking how to accept an artifact, then followed that question into review responsibility and the reliability evidence a class of tasks needs before authorization can be widened.”

3. **2. After one success, who bears the cost of a default? — complete the self-check action.**

   > “listing several inputs that must each be confirmed.”

   Confirmed to exist? Confirmed correct?

   **Fix:** “listing input cases the agent must check individually before submission.”

   Also:

   > “it does not need an effect comparison before it stands.”

   **Fix:** “These obligations apply without waiting for a comparative study.”

4. **3. Book anchor… — remove the fragment.**

   > “A parser’s job is to recognize the text it receives as data the program can work with; reading one line of a message and extracting its contents, say.”

   **Fix:** “A parser turns incoming text into data the program can process—for example, by reading a message line and extracting its contents.”

   “Book anchor” also reads like an internal editorial label. Use **“3. Lamport’s blueprint: what a spec preserves.”**

5. **4. Three layers of question… — unnatural wording obscures the central distinction.**

   > “did this artifact do the behavior that was decided”

   **Fix:** “did this artifact implement the agreed behavior”

   > “that constraint needs a provenance and a matching acceptance check”

   **Fix:** “the team must record the constraint’s basis and provide a matching acceptance check.”

   Heading fix: **“4. Three questions: identify the evidence you need.”**

6. **7. After everything passes… — “read along” does not express the review action.**

   > “Rather than rushing to judge which is better, read along three questions…”

   **Fix:** “Before judging which implementation is better, trace three things: where `text` is validated, when a valid event changes state, and where EOF precedence is decided.”

7. **8. Triaging the CSV case… — the idempotency explanation is harder than the Chinese needs it to be.**

   > “replaying the same batch of events may only produce the first run’s effect; that latter guarantee is what idempotent handling would mean here.”

   **Fix:** “Idempotent handling would mean that replaying the same batch adds no effects beyond those of its first processing.”

   Keep the preceding statement that R13 does **not** require that guarantee.

8. **9. A one-page proposal… — name the actor.**

   > “The proposal makes the claim reviewable, and rejectable.”

   **Fix:** “The proposal lets the team review the claim and reject it.”

   > “the EM/Staff and the people who actually carry the work decide together”

   **Fix:** “the EM/Staff and the people who will bear the workload decide together.”

9. **10. Three exits… — “walk the process” is translated phrasing.**

   > “walk the process first”

   **Fix:** “test the process first.”

   Use **“10. Three paths: test the process, run a limited trial, or adopt a default.”** Retain “diagnostic pilot” in the explanation.

10. **11. Closing: who maintains that paragraph, and when it is withdrawn — simplify the maintenance trigger.**

    > “A requirement having been filled in, or acceptance now covering a certain fault, can each trigger a review…”

    **Fix:** “Resolving a missing requirement or extending acceptance checks to cover a known fault can trigger a review. Neither automatically justifies withdrawal…”

    Also:

    > “The next three parts each add one capacity for judgment.”

    **Fix:** “Each of the next three parts develops a different skill for making these decisions.”

## Suggested cuts

- **3. Book anchor…:** remove the two English-only quotation expansions identified above. Preserve both underlying arguments.
- **4. Three layers of question…:**

  > “The oracle and the grader together are the yardstick this piece keeps referring to.”

  This adds a formal definition absent from the Chinese. For a strict twin, delete it. The existing distinction and answer-key analogy already explain the relationship.
- No paragraph-level cuts elsewhere. The repeated evidence limits and adoption conditions also exist in the Chinese; deleting them selectively would reduce fidelity.

## Suggested additions

- **AI collaboration note:**

  > “final checks are recorded in the same STATUS.md.”

  Before retaining this claim, add an actual English-edition record identifying the writer/run configuration, reviewed revision, completed reviews and checks still pending. Record completed work only.

- No additional studies, anecdotes, numerical examples or substantive argument are needed.

## Terms still unclear

1. **4. Three layers of question… — controls appear before their explanation.**

   > “An oracle checked with positive and negative controls”

   Move the existing explanation before the first table:

   > “Prepare verified legitimate and faulty implementations, then check that the yardstick accepts the former and rejects the latter. These are the positive and negative controls used below.”

   This relocates existing content rather than adding another example.

2. **7. After everything passes… — “close” lacks a reference point.**

   > “the score can be close even when they execute in a different order.”

   **Fix:** “Similar node counts can produce a high similarity score even when execution order differs.”

3. **9. A one-page proposal… — “pieces of work” blurs the counting unit.**

   > “there is one task, but six pieces of scheduled work.”

   **Fix:** “There is one task and six scheduled slots: three under P and three under Q. Each slot contains one session.”

4. **9. A one-page proposal… — distinguish original acceptance from eventual delivery.**

   > “whether that extra self-check increases qualifying deliveries”

   Later:

   > “per final qualifying delivery”

   The first concerns the agent’s original candidate; the second can include separately recorded human repair.

   **Fix the first:** “whether the extra self-check increases the proportion of original candidates that pass acceptance.”

   **Fix the second:** “per final qualifying delivery, including deliveries completed after separately recorded human repair.”

No files changed.

<!-- tokens: in 1331906 out 18885 -->
