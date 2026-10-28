# 發布紀錄

**標題** After Tokyo AGNTCon: Connecting an Agent Is Only the Beginning
**Post ID** `565d3e375896`
**狀態** 已排程，尚未公開。
**排程** 2026-11-04 09:00 Asia/Taipei（UTC 01:00）；新分頁讀回確認。
**草稿** https://medium.com/p/565d3e375896/edit
**上線後穩定短網址** https://medium.com/p/565d3e375896
**核對時間** 2026-10-29T01:27:19+08:00

## 內容核對

2026-10-27 依作者要求修訂第二節（Kong 展示），與中文版同步：開頭補上全貌與閱讀順序，〈Take permitted, happened, and done apart〉補齊三個詞在內文的對應，收束句前加一段交給第三節的橋接，並把兩處誤寫成午休的貼文時間改為當天下午；改動與理由見[場次導讀與來源註記](../../../research/2026-10/aaif-agntcon/reader-entry-refinement.md)末節。同日以 `medium_draft.sh --post` 就地重灌，Post ID 與排程不變，下表是這次兩次比對的結果。文字區塊比上一輪多 3 段：原第一段拆成兩段，另加導讀段與橋接段。

上一輪：2026-10-25 依作者試讀意見重新分析改寫後，再由 Codex 三輪審稿、逐輪依本地來源核對後修訂；本輪把三輪後的定稿以 `medium_draft.sh --post` 就地重灌，沿用既有 Post ID，排程設定另外讀回核對。重灌走與建新草稿相同的插圖與逐塊比對流程，等待儲存穩定後重新載入再比對一次。本輪起每張來源圖片的圖說不再是正文段落，而是貼進該圖在 Medium 的 caption 欄（含圖說內的連結），`verify_draft.py` 逐張比對 caption 文字、連結數含 caption 內的連結。

| 項目 | 結果 |
|---|---:|
| 文字區塊 | 217，逐塊相符 |
| 連結 | 95，順序與目的地相符 |
| 圖片 | 23，順序與槽位相符 |
| 圖說（Medium caption） | 19，逐張相符 |
| 分隔線 | 1 |
| 圖片 placeholder | 0 |

本語言包包含 19 張來源圖片、1 張系列總覽圖及 3 張表格圖。圖說與連結依語言分開保留；總覽的可分享圖片與可編輯來源見[系列總覽](../../../research/2026-10/aaif-agntcon/overview/README.md)。來源與證據範圍見[研究紀錄](../../../research/2026-10/aaif-agntcon/media.md)。獨立模型審閱已完成：Codex（gpt-6.1-sol）三輪審稿、逐輪依本地來源核對後修訂，採用與不採用的理由見[研究紀錄的 Codex 審稿表](../../../research/2026-10/aaif-agntcon/rewrite-2026-10-25.md)；排程稿不計為已公開的 Ambassador 申請作品。

## 發布設定讀回

核對時間：2026-10-27T23:41:12+08:00。另開新分頁，確認不含原頁面標記，再讀取 Medium 儲存的設定。

| 項目 | 讀回值 |
|---|---|
| `isPublished` | `false` |
| `publishSchedule.publishAt` | `1793754000000`（2026-11-04T01:00:00Z） |
| Topics | Artificial Intelligence、Model Context Protocol、Software Engineering、Open Source、Ai Agents |
| 封面 | `asset-01.png`，`1*jY2nu2UmaSugznxXM7TsMA.png`，1080×1080 |
| 預覽標題 | After Tokyo AGNTCon: Connecting an Agent Is Only the Beginning |
| 預覽摘要 | A Tokyo trip and seven talks reveal why tool access still needs authority, recovery, and evidence of completion.（2026-10-26 依作者指示在發布對話框把「six talks」改為「seven talks」，以符合 10/25 補入的 PagerDuty 場次；從新分頁讀回確認，排程與通知設定未變；2026-10-27 重灌後自訂摘要仍在，從新分頁讀回確認） |
| Notify subscribers | 關閉（`isPublishToEmail: false`） |
| 發布位置 | 個人 profile，未投稿 publication |

Story image 使用筆者自己的東京會場照片（`asset-01.png`，也是內文第一張圖，所以重灌沒有動到封面）。2026-10-26 重灌後，原排程、預覽標題、封面原圖及通知設定與更新前相符；自訂預覽摘要在重灌後仍在，同日依作者指示把「six talks」改為「seven talks」，從新分頁讀回確認，沒有按 Schedule to publish。2026-10-27 再次重灌後，排程、預覽標題、封面、自訂預覽摘要、Topics 與通知設定均與重灌前的讀回相符，沒有按 Schedule to publish。系列文章目前仍為排程稿，待實際公開後再更新「即將發布」標示；英文版連到先行排程的中文版本。

## 2026-10-27 重灌：系列總覽圖改為完整尺寸

系列總覽圖 `diagram-01.png` 原本是 `research/scripts/mermaid_check.sh` 修正前的退回截圖（664×718，瀏覽器預設的 300 CSS px）。作者 2026-10-27 決定重灌，先以修正後的 `research/scripts/render_images.sh` 重繪整包：只有 `diagram-01.png` 變成 1546×1664，其餘表格與照片位元組不變。再以 `./tools/medium_draft.sh 2026-11-aaif-after-tokyo en --post 565d3e375896` 重灌（未加 `--reuse-figures`），台北時間 23:07 完成讀回。

儲存後重新讀回兩次：**214 個文字區塊、95 個連結、23 張圖、19 個 caption** 均與貼稿相符，placeholder 為 0。`diagram-01` 換成 `1*13c3rtiPYUnqcMNjg63q_Q.png`（1546×1664）；舊圖與另兩篇英文版的總覽圖是同一份檔案（`1*mf8T9LOLrhV6-KSPoIQGwQ.png`，664×718）。這篇的 `PostViewerEdge.imageIds` 在重灌前後都是空清單，所以新識別碼改從編輯頁第二個 figure 讀取，再自 Medium CDN 讀 PNG 檔頭核對尺寸；其餘 22 張圖未重新算繪。

封面是內文第一張圖 `asset-01.png`（`1*jY2nu2UmaSugznxXM7TsMA.png`，1080×1080），位元組沒變，重灌後仍是同一個識別碼，不需要重選。自訂的預覽摘要在重灌後仍在。沒有按 Schedule to publish。另開新分頁讀回：封面為原照片，預覽摘要、標題、`publishAt: 1793754000000`（2026-11-04 09:00 Asia/Taipei）、`isPublished: false` 與通知設定（關閉，`isPublishToEmail: false`）皆與重灌前的快照相同。這次重灌的貼稿 SHA-256 為 `e5522d3d27572735ad74e64137b0e4ec76228a01d45d2d23c2f9fd0a5c8b2116`；重灌前後快照存於本機 `.context/refill-2026-10-27/`，未納入 git。

## 2026-10-28 重灌：第二節改版與完整尺寸總覽圖合併

10/27 23:04 那輪換上的完整尺寸總覽圖，被同晚 23:3x 的第二節改版重灌換回 664 px：那次用的發布包（PR #29）裡 `diagram-01.png` 還是舊圖。10/28 唯讀讀回確認，編輯頁第二張圖回到 `1*mf8T9LOLrhV6-KSPoIQGwQ.png`。之後把兩者合在同一個發布包（該次改版的兩個 commit，加上重繪的總覽圖），以 `./tools/medium_draft.sh 2026-11-aaif-after-tokyo en --post 565d3e375896` 再重灌一次。

儲存後重新讀回兩次：**217 個文字區塊、95 個連結、23 張圖、19 個 caption** 均與貼稿相符，placeholder 為 0；編輯頁第二張圖為 `1*13c3rtiPYUnqcMNjg63q_Q.png`（1546×1664）。封面 `1*jY2nu2UmaSugznxXM7TsMA.png` 是第一張圖，未被重設。自訂的預覽摘要在重灌後仍在。沒有按 Schedule to publish。另開新分頁讀回：封面、預覽摘要、標題、`publishAt: 1793754000000`（2026-11-04 09:00 Asia/Taipei）、`isPublished: false` 與通知設定（關閉）皆與這次重灌前的快照相同。這次重灌的貼稿 SHA-256 為 `14ed4e64787ff4080eebac8fe09f511172713b5625f669bc093be8d1c9297953`；快照存於本機 `.context/refill-2026-10-27/`，未納入 git。

## 2026-10-29 重灌：付印前校稿

作者 2026-10-28 要求三篇逐段做書籍付印前等級的校稿，中英文同等級，並與 Codex xhigh 審三輪。本篇先完成：Claude 逐段精修、三輪 Codex 審稿與處置、口吻 pass、zh-TW MCP 檢查；四個超長段落中英同步拆成六段。英文總覽圖的子圖標題改為 ASCII，E、F 兩個節點對齊中文；中文 table-01／02／03、英文 diagram-01 與 table-01／02／03 都已重繪。流程與實質修正見[付印前校稿紀錄](../../../research/2026-10/aaif-agntcon/prepress-polish-2026-10-28.md)。

以 `./tools/medium_draft.sh 2026-11-aaif-after-tokyo en --post 565d3e375896` 從 commit `d65ca46` 的發布包重灌（分支 `fantasybz/aaif-polish-after-tokyo`，開自 main `bd8acd0`）。重灌前確認：除了已關閉的 PR #29 舊分支，沒有其他分支對這一包有未合併的改動；那兩個舊 commit 的內容已隨 PR #30 進入 main。儲存後重新讀回兩次：**223 個文字區塊、95 個連結、23 張圖、19 個 caption** 均與貼稿相符，placeholder 為 0；文字區塊比上一輪的 217 個多 6 個，即拆段多出的六段。

封面仍是會場照 `asset-01.png`（`1*jY2nu2UmaSugznxXM7TsMA.png`），重灌沒有動到。自訂摘要仍在（三次重灌都保住）。沒有按 Schedule to publish。2026-10-29T01:27:19+08:00 另開新分頁讀回：`publishAt: 1793754000000`（2026-11-04 09:00 Asia/Taipei）、`isPublished: false`、通知關閉（`isPublishToEmail: false`），Topics 五個都在。逐篇 log 存於本機 `.context/research/aaif-2026-10-28-polish/`，未納入 git。
