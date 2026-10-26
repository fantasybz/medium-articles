# TODOS

## Publishing tooling

### 五份 AAIF ledger 的「核對時間」改記成批次時間

**What:** `2026-11-aaif-*/publish[/en]/PUBLISHED.md` 裡五份在 2026-10-26 封面／摘要改回那一輪的核對時間都寫 `10:34:32+08:00`，那是更新 ledger 的批次時間，不是各篇另開新分頁讀回的時間。

**Why:** 句型「核對時間：T。另開新分頁……再讀取 Medium 儲存的設定」讓讀者以為五篇在同一秒各讀回一次；出處失真，雖然不會讓操作者做錯事。

**Context:** 2026-10-26 /ship 的對抗式審查（Claude 子代理）指出。逐篇實際讀回的時間沒有另外記下（本機 `.context/research/aaif-2026-10-25/codex-fix/readback-log.txt` 只有批次標頭），所以只能改句子，例如「五篇同批處理，批次起始 10:34:32，各篇讀回值見下表」；前一輪（01:46–02:04）是逐篇記的，之後的批次更新也應逐篇記或明寫批次。

**Effort:** S
**Priority:** P3
**Depends on:** None

### `--post` 收尾訊息的驅動測試併入 sibling 測試，省一次 drive

**What:** `tools/test_tools.py` 的 `test_a_refill_warns_about_both_resets_medium_was_measured_to_make` 第二段（新草稿模式不印第 5 項）可併進 `test_a_new_draft_runs_to_the_end_too`，該測試已用同一組 rules 跑過並錨定 `returncode == 0` 與「Publish dialog」。

**Why:** 少一次 ~1.2 秒的完整 driver drive（tools 套件已約 90 秒，多半是這類子程序 drive）；同時把負向斷言放在有錨定的 drive 後面，不再依賴 sibling 測試才不致空泛。

**Context:** 2026-10-26 /ship 第三輪 review 的 Testing／Maintainability specialist 指出負向斷言未錨定、Performance specialist 指出重複 drive。當時因 review 修正循環已達上限未改。改法：在 sibling 測試的 `assertIn("Publish dialog", ...)` 之後加 `assertNotIn("Preview subtitle: it MAY reset too", ...)`，並刪掉新測試的第二段 drive；另可對第 5 項加一個只有它才有的字串斷言（例如 `Medium saves on blur`）。

**Effort:** S
**Priority:** P3
**Depends on:** None

## Research notes

### `research/TOPICS.md` 的 AAIF 列更新圖數

**What:** `research/TOPICS.md:16` 的 AAIF 東京筆記列仍寫 10/24 的計數（17／10／9 張來源圖、第三篇一張比較表）；10/25 改寫後為 19／10／7 張來源圖加 3／3／5 張表格圖（見各語言包 `figures.json` 與 ledger）。

**Why:** 主題庫是研究迴圈的索引，圖數對不上會讓下一輪研究誤判素材量。

**Context:** 2026-10-26 /ship 的文件稽核（/document-release 子代理）回報為 documentation debt；該列是標註日期的索引快照、不在當次 diff 內，所以沒有自動改。更新時一併核對「整理日期」句。

**Effort:** S
**Priority:** P3
**Depends on:** None

## Completed
