# Style brief — how @fantasybz writes (distilled from the four published 2026 articles + Medium history)

## Author identity
- Kochi Chuang (莊軻齊). Senior Software Engineer @ Appier (digital advertising, E2E reliability), CNCF Kubestronaut (working toward Golden Kubestronaut; OTCA certified), long software-testing background (2023 series on *Lessons Learned in Software Testing*; reads James Bach / *Taking Testing Seriously*), observability practitioner (2025 pieces on GenAI observability in CNCF and observability anti-patterns).
- Personal brand: 「榮民叔叔的藏書筆記」(book-notes persona; Medium tagline 榮民叔叔轉職攻城獅的藏書筆記; Facebook fan page KochiLearningJourney; own FB book-club group). Reads Martin Fowler, architecture classics, Japanese QA community (JaSST/JSTQB).
- Writes in Traditional Chinese (Taiwan usage) with English technical terms left untranslated (agent, harness, eval, runtime, sandbox, paved road, champion). Publishes a full English edition of each piece as a separate Medium story, cross-linked.
- Audience: Engineering VPs, EMs, Staff engineers, platform/SRE/QA leads in Taiwan (and English-speaking peers).

## Series architecture (the format the user wants to repeat monthly)
- One theme = **總論 (overview) + 三部曲 (three deep dives)**. In the Sept 2026 series: 總論 (strategy + decision framework + 90-day plan, ~28k chars, 18 min read) → 一、組織篇 (org/people/budget) → 二、技術篇 (reference implementation, "Staff engineer can start building after reading") → 三、營運篇 (measurement, unit economics, scaling gates, vendor mgmt). Each deep dive ~13–16k chars (8–12 min read).
- Every article opens with: `# Title`, then `> **TL;DR** — ...` (one dense paragraph with the thesis and what the piece delivers), then `> 系列導覽：總論 → 一 → 二 → 三` with **本篇** bolded, then `---`.
- Sections numbered with Chinese numerals: `## 一、...`, `## 二、...`; sub-sections `### ...`. 8–12 sections. Closing section is a 結語 with a one-line quotable thesis in a blockquote.
- Tail: `### 系列文章` numbered list (本篇 bolded) → `### References` (numbered, org — [title](url)) → `### AI 協作說明` (fixed paragraph: 本文由筆者提出初步構想與章節架構，文字撰寫由 AI（Claude）協作完成，再經筆者逐節校閱與修訂後定稿。文中觀點與判斷為筆者所持，文責亦由筆者自負。) → italic signature line (*本文發表於 Medium @fantasybz ... 歡迎交流。*).

## Rhetorical moves that recur
- Opens with the question the target reader is actually asking ("每個 Engineering VP 都在問的問題") and answers it up front with a bolded one-liner (`**Own your Agentic Engineering Platform, but don't own the whole agent.**`, `**Buy the intelligence. Build the environment. Own the feedback loop.**`).
- Anchors claims with named industry sources and numbers (OpenAI Harness Engineering, Anthropic long-running harnesses, DORA, Stack Overflow survey, AAIF member count), each linked; never vague "experts say".
- Historical analogy as the spine: DevOps/Cloud-Native 2014–2016 ↔ Agentic 2026; mapping tables (Jenkins job ↔ agent workflow, CI runner ↔ sandbox ...); timeline diagram.
- Names anti-patterns explicitly (「不要成立這種 Team」, 文件墳場, review 成為新瓶頸, 自己造 runtime) before prescribing the pattern.
- Decision artefacts: RACI tables, size-tiered recommendations (50 / 200 / 1,000 人), decision trees, buy-vs-build split, gate tables with exit criteria, 90-day plan table with 退出條件, metric trees with 反作弊 (Goodhart) counter-measures, budget buckets for the CFO.
- "如果我是 Engineering VP，我會怎麼決策" — first-person, opinionated, explicit about what they would NOT approve. Labels own numbers as 「我的建議值（不是業界標準）」.
- Before/After code or config snippets (AGENTS.md 寫錯 vs 寫對; log line before/after; policy YAML), short and concrete.
- Brownfield reality check: acknowledges 15-year legacy monoliths; ordering of investments; "即使失敗這筆投資也不會白費".
- Contrarian on people: junior engineers as review-trained pipeline, champions chosen for DX skills not prompt skills.
- Predictions with dates ("到 2028–2030 年這個名字會消失").
- Cross-references between parts ("詳見第三篇"), so the four pieces read as one product.

## Formatting rules (enforced by repo tooling)
- Mermaid diagrams (flowchart / timeline / mindmap) rendered to PNG for Medium; tables rendered as PNG too. 10–14 figures per 總論, 4–6 per deep dive. Every figure must follow the repo standard in MERMAID.md (2026-09-05): layout width 500–900px, aspect 0.5–1.5, ≤ 12 nodes, ≤ 3 lines × 14 CJK chars per node, TB for > 5 nodes, four semantic classes (own green / buy amber / bad red / human blue) via classDef, the shared YAML frontmatter `config` block (no fontFamily inside it; the renderer injects the font), fontSize 16px, no emoji. Width 500–900 px, aspect 0.5–1.5. Wide things are drawn vertically, narrow-tall flows go two-column (subgraph-to-subgraph edges); a figure that does not fit is split, never shrunk.
- Dash: single `—` only (never `——` in prose; Medium adds hair spaces). Bold for key phrases; blockquotes for the quotable line.
- Links in prose to primary sources; a References section at the end.
- English edition mirrors structure 1:1 with its own figures.

## What the Medium data says about reception (stats page, lifetime)
- Highest-viewed pieces (Medium stats columns are Presentations / Views / Reads; an earlier draft of this brief misread views as reads and reads as claps): 與不確定性共舞：LLM 時代的工程實踐與文化調適 (619 views / 98 reads), LLM Dual-Layer Test Guardrails EN (506 views / 33 reads), 淺談 CNCF 生態下的生成式 AI Observability (130 views / 44 reads), LLM 雙層測試護欄 zh (106 views / 10 reads), 觀測的修復之道 (86 views / 21 reads). Long (17k–27k chars, 27–49 min) Chinese pieces on testing/quality and observability in the LLM era are the proven strength; the author noted on FB that a 17,000-character piece passed 100 reads.
- The Sept 2026 Agentic Engineering series is days old (20–26 views each), so no verdict yet.

## Implications for the next three monthly themes
- Keep the 總論+三部曲 product shape, the DevOps-history spine where it fits, and the decision-artefact density.
- Lean into the author's credible ground: testing/QA, observability/SRE, Kubernetes/cloud-native, engineering culture — now applied to agents.
- Each theme should have a one-line thesis, a named anti-pattern set, a reference implementation part, and an operations/measurement part.
