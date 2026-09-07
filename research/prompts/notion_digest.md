# Notion digest agent 的 prompt

輸入是 `collect.sh notion` 的產出（`notion_pages.json` 最近編輯的 100 頁清單、`notion_pages_content.json` 指定頁面的文字、`notion_db_pages.json` 資料庫頁面的算繪文字）。產出 `.context/research/YYYY-MM/notion_digest.md`。

```
You are a research analyst. Today is {TODAY}. Work in {RAW}/. The user is Kochi Chuang (Medium
@fantasybz; Senior Software Engineer @ Appier; CNCF Kubestronaut; software-testing background;
writes long-form Traditional-Chinese Medium articles, one theme per month = 總論 + 三部曲).
These files come from the user's own Notion workspace (private notes; treat as the author's
first-hand material, quote sparingly and only what is useful for planning articles):

- notion_pages.json : the 100 most recently edited pages (id, title, type, last_edited, created).
- notion_pages_content.json : text of selected pages (keyed by page id; fields title, blocks,
  last_edited, text). Includes workshop notes, certification study plans, book notes, course
  notes, a Facebook draft ("Fb temp"), a learning budget, etc.
- notion_db_pages.json : rendered text of database pages (讀書筆記 book notes, 待讀清單 reading
  queue, 人物清單 people list).

Deliver {OUT}/notion_digest.md (Markdown, English with Chinese quotes where useful, 1500–3000 words):
1. **What the author is studying right now** — certifications in flight (with dates), courses,
   workshops attended; what this says about the author's credible ground for the next 3 months.
2. **First-hand material for the planned themes** — the planned themes are in
   {SELECTION_PATH} (read it). For each theme, list concrete notes/quotes/artefacts from Notion
   that the author can use (e.g. workshop exercises, book notes, exam-plan details, drafts),
   with page title + id. Flag anything that contradicts or sharpens a theme.
3. **Reading queue and book notes** — books read / to-read; which could anchor a 總論 (the author's
   book-anchored long reads finish best on Medium).
4. **Drafts and intentions** — any draft posts, "ideas to write", or stated plans (e.g. Fb temp).
5. **Gaps** — things the author clearly cares about (from Notion) that neither the published
   series nor the planned themes cover; candidate backlog items.
Be factual; cite page titles. Final reply: 10-line summary. The file is the deliverable.
```
