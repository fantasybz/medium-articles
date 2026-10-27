# 排程與內容驗證紀錄

**標題** 同一份規格，跑十次（二）：契約篇—把要求變成驗收，中間還缺哪些判斷？
**Post ID** `f7684c057c0e`
**草稿網址** https://medium.com/p/f7684c057c0e/edit
**狀態** 已排程於 **2026-11-24（二）09:00 Asia/Taipei（GMT+8）** 發布；2026-10-18 讀回時 `isPublished: false`，尚未公開。

## 發布設定

| 項目 | 新分頁讀回的值 |
|---|---|
| Topics | Software Testing、Code Review、AI、Software Engineering、Engineering Management |
| 封面圖 | `diagram-01.png`（`1*GFWOFlXX_RmgbTUH1v55-g.png`，1092×942；2026-10-27 重灌後選回新版並讀回確認） |
| 預覽標題 | 同一份規格，跑十次（二）：契約篇—把要求變成驗收，中間還缺哪些判斷？ |
| 預覽摘要 | 要求寫好了，檢查就一定可信嗎？從三行輸入推導應有結果，再用刻意錯法與合法差異，檢查驗收工具看得見什麼。 |
| Notify subscribers | 已勾選，`isPublishToEmail: true` |
| 發布排程 | 2026-11-24（二）09:00 GMT+8；`2026-11-24T01:00:00Z` |

Medium 會在標題的破折號旁加入空白或細空白；比對沿用發布工具的正規化，文字內容相同。

## 2026-10-04 內容與排程核對

沿用 `tools/medium_draft.sh` 建立完整草稿。等待儲存後另開分頁，排程完成後再另開分頁核對一次，正文與本機貼稿逐塊相符。

| 核對項目 | 結果 |
|---|---|
| 文字區塊 | 226 個，逐塊相符 |
| 連結 | 54 個，目的地與順序相符 |
| 圖片 | 7 張，順序與槽位相符 |
| 分隔線 | 0 條 |
| 圖片占位文字 | 0 |

正文與貼稿均通過實際 strict zh-TW MCP，錯誤與警告各為 0。發布設定的封面、Topics、預覽文字、通知與 UTC 排程也從新分頁讀回確認。版本指紋與驗證範圍見[本輪發布紀錄](../../research/2026-10/same-spec-ten-runs/publication-2026-10-04.md)。

## 後續維護

系列連結只預填本篇發布時應已上線的前篇；尚未上線的後篇保留「即將發布」。發布前須確認前篇實際狀態；後篇上線後再回填連結。研究附件固定在公開 commit `774759192ab0e0b2da3d8b163eb3f07f3d12f4c3`。

英文版規劃接在 2026-11-26（四）09:00，但 Claude Code max 的主寫請求被週額度限制拒絕，尚未產出英文正文或 Medium 草稿，也尚未排程。維持作者指定的 max 主寫，完成後再逐段潤飾與核對，接著發布。

## 2026-10-18 發布進度核對

從新分頁讀回，仍為 `isPublished: false`；排程為 **2026-11-24 09:00 Asia/Taipei**（`publishAt: 1795482000000`），與原排程相符。本次僅核對，沒有重貼正文或更動發布設定。

正文與目前貼稿逐塊相符：226 個文字區塊、54 個連結、7 張圖、0 條分隔線。連結數量及圖片槽位通過既有驗證器；本次不重查所有外部引文的可用性。

## 2026-10-27 重灌：流程圖改為完整尺寸

`diagram-01.png` 原本是 `research/scripts/mermaid_check.sh` 修正前的退回截圖（664×582，瀏覽器預設的 300 CSS px）。作者 2026-10-27 決定重灌，先以修正後的 `research/scripts/render_images.sh` 重繪整包：只有 `diagram-01.png` 變成 1092×942，其餘表格位元組不變。再以 `./tools/medium_draft.sh 2026-11-same-spec-contract --post f7684c057c0e` 重灌（未加 `--reuse-figures`），台北時間 23:25 完成讀回。

儲存後重新讀回兩次：**226 個文字區塊、54 個連結、7 張圖** 均與貼稿相符，placeholder 為 0。`diagram-01` 由 `1*tAFGUekCIWEd6qayUszNuw.png`（664×582）換成 `1*GFWOFlXX_RmgbTUH1v55-g.png`（1092×942，自 Medium CDN 讀 PNG 檔頭核對），其餘 6 張圖保留原識別碼。

重灌把封面重設成內文第一張圖（表格 `1*XFszBI6N9nX3O12Hda4wqw.png`，1698×476），在 `/p/f7684c057c0e/submission` 用 Change preview image 依識別碼選回新版 `diagram-01.png`（`1*GFWOFlXX_RmgbTUH1v55-g.png`，1092×942）、按 Done。預覽摘要被換成自動摘錄，已把自訂句填回 Write a preview subtitle 欄並以 Tab 離開欄位。沒有按 Schedule to publish。另開新分頁讀回：封面為新版 `diagram-01.png`，預覽摘要、標題、`publishAt: 1795482000000`（2026-11-24 09:00 Asia/Taipei）、`isPublished: false` 與通知設定（開啟，`isPublishToEmail: true`）皆與重灌前的快照相同。這次重灌的貼稿 SHA-256 為 `0dcf2f5d05a071851e5d03700a5d7415a96e508b9d311a085eaafaf060c9503a`；重灌前後快照存於本機 `.context/refill-2026-10-27/`，未納入 git。
