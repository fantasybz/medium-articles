# 會議 digest agent 的 prompt（期中加圈用）

作者去了一場會議，回來要把它併進當月的研究迴圈時用。2026-09-15 第一次跑（AGNTCon + MCPCon Japan 2026）。
輸入分兩層：先把 sched 的議程、附件投影片（pdftotext／pptx／keynote／OCR）、keynote 直播字幕、主辦方部落格抓到
`.context/research/<slug>-conf/`，由一個 agent 寫成**逐場筆記**（每場一個區塊：Materials／Thesis／Key claims & numbers／
Mechanisms／Case study／Quotable lines／Relevance + Signal 1–5；一天一份，`notes_<day>.md`，全部場次都寫、作者打勾的標 ✅），
再由下面這個 agent 把兩天筆記、主辦方貼文、X／LinkedIn 的會議搜尋、作者自己的貼文整合成一份 digest。
產出 `research/YYYY-MM/conference_digest.md`（會 commit：只引公開的會議材料與公開貼文，作者的 FB 限友貼文只改寫、只記反應數）。
`codex_review.sh` 要讀到它才審得了引用它的大綱：`EXTRA_DIGESTS="conference_digest.md" research/scripts/codex_review.sh <outline.md>`；
`review-outlines.js` / `finish-outline.js` 同樣用 `extraSources` 帶進去。

```
You are working inside the git repo at {ROOT}. Today is {TODAY}. The author is Kochi Chuang (Medium @fantasybz;
Senior Software Engineer @ Appier; CNCF Kubestronaut; software-testing background; writes long-form
Traditional-Chinese Medium articles for Engineering VPs / Staff engineers, one theme per month = 總論 + 三部曲).
The planned themes are in {ROOT}/research/{PLAN_MONTH}/ (selection.md and the three outlines); the unpublished
articles are {UNPUBLISHED_DIRS}. Backlog items are numbered in {ROOT}/research/{PLAN_MONTH}/backlog.md.
Rules: quote numbers exactly as the source states them and say where (slide N / [hh:mm:ss] / file); never invent
a number, id, name or quote; when a deck is image-only say so; label vendor-reported figures as such.

TASK: write {OUT}/conference_digest.md — the integrated digest of {EVENT} for the monthly research loop. This file
WILL be committed to a public repo: quote public conference material and public X/LinkedIn posts freely, but do
not copy the author's Facebook friends-only posts verbatim (paraphrase, cite reaction counts only).
Inputs (read all): {CONF}/notes_*.md (per-session notes, each ending in a cross-cutting section), {CONF}/sessions.md
(✅ = attended), the organiser's posts under {CONF}/*_txt/, {RAW}/x_conf_search.json, {RAW}/linkedin_conf_search.txt,
the author's own posts in {RAW}/facebook_own.json, and the digests already written in {OUT}/ (cross-reference only).
Structure (Markdown, ~4,000–6,000 words; every claim cites session id + slide/timestamp or the post):
1. Header: what the event was, the organisers' numbers, the announcements, the author's attendance (count, tracks, skips).
2. Ecosystem map after the event (projects, working groups, what the next editions add).
3. Twelve to eighteen mechanisms with numbers, ranked by usefulness to the next theme to be written: claim → number →
   source → which section it feeds → whether it closes an objection in the latest codex-review-*.md.
4. Insertion candidates for the unpublished articles: table — article, real section heading, the sentence to add
   (in Chinese as it could appear), source session + slide, why it strengthens rather than pads. 8–15 rows, each new.
5. Material for the theme after that.
6. Tensions: where speakers contradicted each other.
7. Social echo: X / LinkedIn / the author's own posts with counts; what the Taiwanese communities did NOT say.
8. Quotable lines (15–25, attributed, id + slide/timestamp).
9. Backlog and watch-list updates: accounts / projects / dates / arXiv query strings; which backlog item each strengthens.
10. Cross-check against any book digest in {OUT}/ (same claim / opposite claim), the strongest anchors for the theme.
Final reply: a 10-line summary; the file is the deliverable.
```
