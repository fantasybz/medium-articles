# Style brief — how @fantasybz writes (2026-10 cycle)

> 共用標準：撰稿、潤稿與翻譯前先讀 [STYLE.md](../../STYLE.md)。作者最新要求與共用標準優先；本檔保留當期格式、素材與歷史觀察。

> Updates `research/2026-09/style_brief.md` with the October drafts, the 09-08 voice polish and Medium data as of 2026-09-15.

## Author identity
- Kochi Chuang (莊軻齊). Senior SWE @ Appier, CNCF Kubestronaut, long testing background (2023 *Lessons Learned in Software Testing*; reads James Bach / *Taking Testing Seriously*), observability practitioner. Brand 「榮民叔叔的藏書筆記」 (FB fan page KochiLearningJourney, 727 followers); reads Fowler and the Japanese QA community.
- Takes first-hand notes at events — 模式語言驅動開發工作坊 (2026-08), AGNTCon + MCPCon Japan (Tokyo, 2026-09-10–11) — and uses them as named evidence.
- Traditional Chinese (Taiwan usage), English technical terms untranslated (agent, harness, eval, gate, constraint tests, mutation score). A full English edition ships as a separate, cross-linked story. Audience: Engineering VPs, EMs, Staff engineers, platform/SRE/QA leads in Taiwan, plus English-speaking peers.

## Series architecture (the shape, with the October numbers)
- One theme = **總論 + 三部曲**. October 「綠燈不是驗收」: 總論 (three gates, anti-patterns, VP decision, 90-day blueprint) → 測試篇 (assertion-change diff, red-then-green, mutation score) → Review 篇 (triage matrix, reviewer fleet, closed-loop ban) → 可靠度篇 (constraint pass rate, pass^k, oversight budget).
- **Length snapshot after the 09-08 polish (historical)**: 總論 ≈ 10,000 CJK chars / 12 sections / 18 figures (10 mermaid + 8 tables); each part ≈ 7,600–8,000 chars / 6–9 sections / 7–8 figures (4 mermaid + 3–4 tables；可靠度篇只有 6 節）. Targets were 3,600 and 1,800–2,300; the drafts run 2.8–4× that and **the author accepted the overrun**. Earlier long articles also attracted completed reads; this does not establish length as their cause. Those targets are historical planning estimates, not a sentence-compression budget or a minimum to pad toward; retain necessary explanation and narrative.
- Opening: `# Title` → `> **TL;DR** — ...` (360–730 chars: symptoms → one-line thesis → what each gate measures → the disagreeable claims → one sourced number with its domain → what the tail delivers) → `> 系列導覽：…` with **本篇** bolded, unpublished siblings 「（即將發布）」/"(coming soon)", plus a 「上一季」 row.
- Chinese-numeral sections (`## 一、…`), 6–12 per piece (總論 12; 測試篇 9; Review 篇 8; 可靠度篇 6); the last is 結語 / 結語與交接, returning to the opening question or documented experience before a hand-off; a blockquote is optional.
- Tail: `### 系列文章` → `### References` (numbered, org — [title](url), each with a 〔第 N 節〕 back-pointer) → `### AI 協作說明` → italic signature.

## Rhetorical moves that recur
- Opens with the question the reader is actually asking (§一〈「AI 說沒問題」之後，我該相信什麼？〉), answered by a bolded one-liner. Anti-patterns named before prescriptions (「八個反模式」); decision artefacts everywhere (triage matrices, gate tables with exit criteria, a 90-day plan with 退出條件); cross-references so the four read as one product.
- Numbers ship with sample size and domain: 「34% 的綠燈修補違反 reviewer 約束」 carries 「SWE-Gate 在 75 個 Python repo、303 個任務上量測到」. Vendor- or organiser-reported figures say so; his own are 「我的建議值（不是業界標準）」.
- **書錨 opening (new, 總論 §二).** A named book carries the thesis before any data: 「書錨：Bach 的 testing 與 checking」 says who Bach is, quotes two verbatim lines, **states the limit honestly** (「先說限制：這本書我還沒讀完」), then derives the series' vocabulary from it (evidence classes a / b / c, reused by all four).
- **Before/After config blocks (new).** Short, paired, concrete: `# Before：指示（agent 讀完，什麼都沒有變）` vs the executable rule; `# Before：同一個 runner、同一個 session 審自己` vs the fleet config. Always 「指示 → 可執行的檢查」.
- **The 「設計規格，非現成工具」 label (new).** Any YAML/CODEOWNERS/policy block not run in production says so in its first comment line — `reviewer-fleet.yaml（設計規格，非現成工具）`, `CODEOWNERS（設計草稿，未在生產 repo 實測…）` — and the prose repeats it plus how he will verify.
- **Reader roles (new).** Each piece names the person it changes, in a section title: 總論 「如果我是 Engineering VP / QA lead，我會怎麼決策」; 測試篇 「Tester 的角色：從打勾機器到 test-suite reviewer」; Review 篇 assigns fleet roles (verifier / falsifier / architect); 可靠度篇 speaks to whoever signs off autonomy.
- First-hand evidence gets its own section (「第一手實例：測試全綠，replay 從未執行」): his own workshop A/B run, mechanism named.
- **Voice rules re-established by the 2026-09-08 polish** (the eight September stories were republished in place — `repub`, no re-notify, +2–4 min; PUBLISHING.md 〈目前的發布佇列〉, `voice_brief.md`): it **added sentences rather than cutting them**. Introduce what each figure or table is meant to clarify, explain new terms, and distinguish the author's judgment from findings. Do not require an identical lead-in, first-person marker or 「不是 A，而是 B」 closing in every section. The old punctuation measurements describe that revision, not quotas for future prose: the polish cut the October four from 5.4–7.5 dashes per 1,000 prose chars to 1.2–2.2 (2.04 / 1.16 / 2.12 / 2.20), and September 總論 now sits at 2.08 (dashes 29 → 22).

## 作者確認的共用標準（2026-09-23）

本月與後續所有系列遵循 [STYLE.md](../../STYLE.md) 及 [現行聲音手冊](../2026-09/voice_brief.md)。這次修正的重點是：

- 動作交代完整。測得結果用「量測」，計算比例用「統計」或「計算」，評估效果用「衡量」，確認要求用「檢查」或「驗證」。同樣檢查「跑、收、擋、放、綁、接」的對象與目的，不做機械替換。
- 敘事從既有的工作坊、閱讀與會議紀錄出發，交代問題如何帶出作者的思考。可以補承接與解釋，不能補造親歷、對話、情緒或研究發現。
- 逐篇、逐句核對指涉、因果、適用條件與數字分母。小樣本、作者建議值、理論框架與實測結果分開寫，不能為了讓句子有力就放大結論。
- 短句、反轉句、第一人稱與連接詞依情境使用。舊手冊的禁詞、固定句型與標點配額不再沿用；完整清楚優先於壓縮字數。
- 中英版保留相同文意與限制，正文、圖表、政策範例與發布稿同步更新。舊稿字元數與詞頻是歷史紀錄，不是這輪稿件的驗收門檻。

## Conference and book material (new for this cycle)
- **A session is cited as speaker, company, session, slide/timestamp**: 「在 AGNTCon Japan 的 X 場，<講者>（<公司>）在 slide N 說…」. Stage numbers are organiser-, vendor- or team-reported and say so; press coverage is not a source. Ground truth is `notes_sep10/11.md`.
- **References entry for a session**: `org — [session title](https://sched.co/<id>)`, or the slide PDF URL from `sessions.md` when one exists.
- **A book is cited as 《書名》第 N 章〈節〉**, author named on first use; References `Bojie Li — [AI Agents in Depth](https://github.com/bojieli/ai-agent-book)` or the chapter page `…/book-en/<chapterN>/`.
- Same shape as the personal material already cited: one numbered entry, kind first — 「筆者筆記：…模式語言驅動開發工作坊（2026-08）的 A/B 實作紀錄〔第七節〕」.
- An insertion earns its place only by adding evidence the piece lacks: never restate an arXiv finding with a conference anecdote.

## Formatting rules (enforced by repo tooling)
- Unchanged from the 2026-09 brief: MERMAID.md limits, mermaid and tables rendered to PNG, bold + blockquote, single `—`, link edits in both article and paste file, `publish/` never hand-edited.

## What the Medium data says about reception (stats page, as of 2026-09-15)
- Medium's columns are **Presentations / Views / Reads**; an earlier draft of the 2026-09 brief misread views as reads and reads as claps. Ratio = reads / views.
- **September series, 11–14 days in**: zh four = 105 / 43 / 15 (35%); en four = 121 / 26 / 6 (23%). Since 2026-09-05: zh +11 / +14 / +4; en +30 / +16 / +4 on the three comparable. **Chinese still finishes; English now gets clicked** — the feed distributes English, the Chinese rides on the author's network.
- **Org design beats harness**: 組織篇 is the most-viewed Chinese part (11 views) and best-finished English one (Part 1: 9 / 4, 44%); 技術篇 is least clicked in both (zh 3; en 6 / 1) despite the build list. October's four are all method pieces — give each an organisational hook in title and opening.
- **The overview is the door**: 別急著打造你的 Devin holds 58% of Chinese views (25 of 43) and its reads still move (7 → 8). October schedules 總論 first (10/06–10/29, zh Tuesday, en Thursday；2026-09-23 已依 Medium 排程時間校正發布紀錄的星期）.
- **No fan-page share yet, and it shows.** Except for the zh overview, views sit below presentations (69 vs 226 for the series) — the opposite of the 2025 shared weeks (與不確定性共舞: 142 presentations, 619 views). The 727-follower page has not been told the series exists; one public profile post (28 reactions, 3 shares) matches the overview's +6 views. Telling it is October's cheapest lever.
- **Length after the polish did not hurt**: every story gained 2–4 min on 09-08 and completion held (zh 38% → 35% on small numbers; Part 1 en rose to 44%). Lifetime leaders are still long pieces — 與不確定性共舞 (619 / 98), Dual-Layer Test Guardrails EN (507 / 33), 《建築的永恆之道》 (245 / 125, 51%), 觀測的修復之道 (90 / 21) — plus evergreen notes (敏捷測試 3,000 views). The back catalogue gained ~a dozen views and **no** new reads; all 21 September reads were the series. Monthly block for 2026-09: 267 / 82 / 21, +2 followers, +2 subscribers (39 / 13 on 09-05).

## Implications for the next themes
- Keep the 總論+三部曲 shape, the 書錨 opening, the decision-artefact density and the labelled-artefact honesty. Length is not the problem; missing 導讀句 and role statements are.
- **December re-cut** (`selection.md` §1): the spine moves from 「把 harness 裝上儀表」 to **flight recorder / accountability**, carried by 「trace 是除錯用的，ledger 才是證據用的」. Only **three artefacts** ship — A1 trace schema + OTel Collector config, A2 `agent-slo.yaml`, A3 a ≤ 50-line ledger-backed `attest verify` check; runbook/postmortem templates and the K8s capacity table drop to sketches. Hard exit: no real run trace and queryable ledger by 10/31 → three pieces. Tokyo forces three corrections: AAIF now has an observability WG and a new **agents accountability** WG, so 「沒人在講」 goes; `org.*` names only; every Tokyo number labelled self-reported.
- **November backlog** (`selection.md` §3, `backlog.md`): the variance outline is unchanged this cycle. The first-hand gap: 「same prompt, same model, same harness，兩次結果完全不同」 was said on stage (`2VPr7` slide 2) yet **no speaker reported a run-to-run distribution for one spec** — say so, and say why. Supporting material: the GEPA/SkillOpt null whose gain cannot be separated from run-to-run variance (2609.12742), the vendor `plugin eval` (paired arms, three runs, 2-of-3 majority) as a miniature pass^k, and the Haiku-gate angle (variance across models, not runs).
