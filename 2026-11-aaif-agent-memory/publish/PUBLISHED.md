# 發布紀錄

**標題** Agent 記住的經驗，下一次還能相信嗎？
**Post ID** `5380c278562e`
**狀態** 已排程，尚未公開。
**排程** 2026-11-16 09:00 Asia/Taipei（UTC 01:00）；新分頁讀回確認。
**草稿** https://medium.com/p/5380c278562e/edit
**上線後穩定短網址** https://medium.com/p/5380c278562e
**核對時間** 2026-10-29T06:34:33+08:00

## 內容核對

2026-10-25 依作者試讀意見重新分析改寫後，再由 Codex 三輪審稿、逐輪依本地來源核對後修訂；本輪把三輪後的定稿以 `medium_draft.sh --post` 就地重灌，沿用既有 Post ID，排程設定另外讀回核對。重灌走與建新草稿相同的插圖與逐塊比對流程，等待儲存穩定後重新載入再比對一次。本輪起每張來源圖片的圖說不再是正文段落，而是貼進該圖在 Medium 的 caption 欄（含圖說內的連結），`verify_draft.py` 逐張比對 caption 文字、連結數含 caption 內的連結。

| 項目 | 結果 |
|---|---:|
| 文字區塊 | 126，逐塊相符 |
| 連結 | 49，順序與目的地相符 |
| 圖片 | 13，順序與槽位相符 |
| 圖說（Medium caption） | 7，逐張相符 |
| 分隔線 | 1 |
| 圖片 placeholder | 0 |

本語言包包含 7 張來源圖片、1 張系列總覽圖及 5 張表格圖。圖說與連結依語言分開保留；總覽的可分享圖片與可編輯來源見[系列總覽](../../research/2026-10/aaif-agntcon/overview/README.md)。來源與證據範圍見[研究紀錄](../../research/2026-10/aaif-agntcon/memory.md)。獨立模型審閱已完成：Codex（gpt-6.1-sol）三輪審稿、逐輪依本地來源核對後修訂，採用與不採用的理由見[研究紀錄的 Codex 審稿表](../../research/2026-10/aaif-agntcon/rewrite-2026-10-25.md)；排程稿不計為已公開的 Ambassador 申請作品。

## 發布設定讀回

核對時間：2026-10-26T10:34:32+08:00。另開新分頁，確認不含原頁面標記，再讀取 Medium 儲存的設定。

| 項目 | 讀回值 |
|---|---|
| `isPublished` | `false` |
| `publishSchedule.publishAt` | `1794790800000`（2026-11-16T01:00:00Z） |
| Topics | Artificial Intelligence、Model Context Protocol、Software Engineering、Open Source、Ai Agents |
| 封面 | `asset-01.png`，`1*yXCiu5bX04CCZi96j9C3LA.png`，2400×1350（2026-10-26 重灌後一度被重設為總覽圖 `diagram-01.png`；同日在發布對話框用 Change preview image 依圖片識別碼選回、按 Done，從新分頁讀回確認） |
| 預覽標題 | Agent 記住的經驗，下一次還能相信嗎？ |
| 預覽摘要 | 從澀谷照片到三場會議材料，追問 Agent 記憶的來源、適用條件，以及更正如何進入下一次任務。（2026-10-26 重灌後一度讀回為自動摘自 TL;DR 的首句；同日在發布對話框的 Write a preview subtitle 欄重設為此句，從新分頁讀回確認） |
| Notify subscribers | 關閉（`isPublishToEmail: false`） |
| 發布位置 | 個人 profile，未投稿 publication |

Story image 使用筆者自己的澀谷觀景台夜景照（`asset-01.png`）。2026-10-26 重灌後封面一度被 Medium 重設為內文第一張圖（系列總覽圖），同日依作者指示在發布對話框用 Change preview image 選回原照、按 Done 存檔，預覽摘要也重設回自訂句，兩者皆從新分頁讀回確認；沒有按 Schedule to publish。原排程、預覽標題及通知設定與更新前相符。10/25 改寫後正文保留一張澀谷開場照與一張 SKY 慶典照，另兩張澀谷照留在 `figures/` 未使用。系列文章目前仍為排程稿，待實際公開後再更新「即將發布」標示；英文版連到先行排程的中文版本。

## 2026-10-27 重灌：系列總覽圖改為完整尺寸

系列總覽圖 `diagram-01.png` 原本是 `research/scripts/mermaid_check.sh` 修正前的退回截圖（664×948，瀏覽器預設的 300 CSS px）。作者 2026-10-27 決定重灌，先以修正後的 `research/scripts/render_images.sh` 重繪整包：只有 `diagram-01.png` 變成 1156×1664，其餘表格與照片位元組不變。第一次執行 `./tools/medium_draft.sh 2026-11-aaif-agent-memory --post 5380c278562e` 在載入 Drafts 頁時遇到 `net::ERR_ABORTED`，還沒開編輯器就停止，讀回確認文章未被更動；重跑後完成，台北時間 23:19 讀回。

儲存後重新讀回兩次：**126 個文字區塊、49 個連結、13 張圖、7 個 caption** 均與貼稿相符，placeholder 為 0。`diagram-01` 由 `1*hcfJVSrI3ZyNIne3eMmvSQ.png`（664×948）換成 `1*F4Urac80aH8T4p1KGCd5fw.png`（1156×1664，自 Medium CDN 讀 PNG 檔頭核對），其餘 12 張圖保留原識別碼。

重灌把封面重設成新的總覽圖，在 `/p/5380c278562e/submission` 用 Change preview image 依識別碼選回 `asset-01.png`（`1*yXCiu5bX04CCZi96j9C3LA.png`，2400×1350）、按 Done。預覽摘要被換成自動摘錄，已把自訂句填回 Write a preview subtitle 欄並以 Tab 離開欄位。沒有按 Schedule to publish。另開新分頁讀回：封面為原照片，預覽摘要、標題、`publishAt: 1794790800000`（2026-11-16 09:00 Asia/Taipei）、`isPublished: false` 與通知設定（關閉，`isPublishToEmail: false`）皆與重灌前的快照相同。這次重灌的貼稿 SHA-256 為 `05d31ef6d798fe281d1e91c97b39012bc03861b1c9523359ce0e95d5d24a3d01`；重灌前後快照存於本機 `.context/refill-2026-10-27/`，未納入 git。

## 2026-10-28 重灌：長段落補上全貌與閱讀順序

作者 2026-10-28 要求第三篇比照第一篇 Kong 段處理最長的三節：§四（Agent Memory）與§五（AIRAS）開頭補閱讀順序，結尾補橋接；§六（驗收設計）開頭補閱讀順序，補上三個小標，結尾補一段交給結語的橋接；改動與理由見[場次導讀與來源註記](../../research/2026-10/aaif-agntcon/reader-entry-refinement.md)末節。以 `./tools/medium_draft.sh 2026-11-aaif-agent-memory --post 5380c278562e` 從 commit `cf13c71` 的發布包重灌（未加 `--reuse-figures`）；這個分支開自 main，總覽圖已是完整尺寸版。重灌前先確認沒有其他分支對這一包有未合併的改動，也請 phnom-penh session 在這段期間不要動這份稿。

儲存後重新讀回兩次：**135 個文字區塊、49 個連結、13 張圖、7 個 caption** 均與貼稿相符，placeholder 為 0；文字區塊比上一輪的 126 個多 9 個：六段新文字與三個新小標。`diagram-01` 仍是 `1*F4Urac80aH8T4p1KGCd5fw.png`（1156×1664），664 px 舊圖不在稿裡。

重灌又把封面重設成總覽圖，在 `/p/5380c278562e/submission` 用 Change preview image 依識別碼選回 `asset-01.png`（`1*yXCiu5bX04CCZi96j9C3LA.png`，2400×1350）、按 Done；預覽摘要也被換成自動摘錄，已把自訂句填回 Write a preview subtitle 欄並以 Tab 離開欄位，這次 `/submission` 沒有出現 500 錯誤。沒有按 Schedule to publish。2026-10-28T21:59:31+08:00 另開新分頁讀回：封面為原照片，預覽摘要為自訂句，`publishAt: 1794790800000`（2026-11-16 09:00 Asia/Taipei）、`isPublished: false`、通知關閉（`isPublishToEmail: false`），Topics 五個都在。逐篇 log 存於本機 `.context/research/aaif-2026-10-28-long-sections/`，未納入 git。

## 2026-10-29 重灌：付印前校稿

作者 2026-10-28 要求三篇逐段做書籍付印前等級的校稿，中英文同等級，與 Codex xhigh 審三輪，依發布順序逐篇定稿、逐篇重灌。本篇是第三篇：Claude 逐段精修、統籌處理 32 項標記、三輪 Codex 審稿與處置、口吻 pass、zh-TW MCP 檢查。六個超長段落中英同步拆開，共切七處。幾處依投影片原文修正：第 28 頁圖說、第 26 頁的三種搜尋、第 18 頁的留與丟。中文 table-02／03／04／05 重繪，其餘圖片不變。流程與實質修正見[付印前校稿紀錄](../../research/2026-10/aaif-agntcon/prepress-polish-2026-10-29-memory.md)。

以 `./tools/medium_draft.sh 2026-11-aaif-agent-memory --post 5380c278562e` 從 commit `cace9af` 的發布包重灌。分支 `fantasybz/aaif-polish-memory` 疊在第二篇的 `fantasybz/aaif-polish-handoffs` 之上，最底下開自 main `bd8acd0`。重灌前確認沒有其他分支對這一包有未合併的改動：`fantasybz/green-reliability-backfill` 列出的 commit 是把 main 併進去的 merge，這一包的內容與 main 相同。儲存後重新讀回兩次：**142 個文字區塊、49 個連結、13 張圖、7 個 caption** 均與貼稿相符，分隔線 1、placeholder 為 0。文字區塊比上一輪的 135 個多 7 個，即拆段多出的七段。

重灌又把封面重設成總覽圖，在 `/p/5380c278562e/submission` 用 Change preview image 依識別碼選回 `asset-01.png`（`1*yXCiu5bX04CCZi96j9C3LA.png`，2400×1350）、按 Done。預覽摘要也被換成自動摘錄，已把自訂句填回 Write a preview subtitle 欄並以 Tab 離開欄位。沒有按 Schedule to publish。2026-10-29T06:34:33+08:00 另開新分頁讀回：封面為原照片，預覽摘要為自訂句，`publishAt: 1794790800000`（2026-11-16 09:00 Asia/Taipei）、`isPublished: false`、通知關閉（`isPublishToEmail: false`），Topics 五個都在。貼稿 SHA-256 為 `da3f53ae258aa4bb4d27807381e69940238210acf3cf49030d67cbd210d48018`。逐篇 log 存於本機 `.context/research/aaif-2026-10-28-polish/`，未納入 git。
