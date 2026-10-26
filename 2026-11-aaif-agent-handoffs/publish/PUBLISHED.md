# 發布紀錄

**標題** 把工作交給另一個 Agent 之前：授權、狀態與復原
**Post ID** `e68dc5ab1275`
**狀態** 已排程，尚未公開。
**排程** 2026-11-09 09:00 Asia/Taipei（UTC 01:00）；新分頁讀回確認。
**草稿** https://medium.com/p/e68dc5ab1275/edit
**上線後穩定短網址** https://medium.com/p/e68dc5ab1275
**核對時間** 2026-10-26T10:34:32+08:00

## 內容核對

2026-10-25 依作者試讀意見重新分析改寫後，再由 Codex 三輪審稿、逐輪依本地來源核對後修訂；本輪把三輪後的定稿以 `medium_draft.sh --post` 就地重灌，沿用既有 Post ID，排程設定另外讀回核對。重灌走與建新草稿相同的插圖與逐塊比對流程，等待儲存穩定後重新載入再比對一次。本輪起每張來源圖片的圖說不再是正文段落，而是貼進該圖在 Medium 的 caption 欄（含圖說內的連結），`verify_draft.py` 逐張比對 caption 文字、連結數含 caption 內的連結。

| 項目 | 結果 |
|---|---:|
| 文字區塊 | 160，逐塊相符 |
| 連結 | 54，順序與目的地相符 |
| 圖片 | 14，順序與槽位相符 |
| 圖說（Medium caption） | 10，逐張相符 |
| 分隔線 | 1 |
| 圖片 placeholder | 0 |

本語言包包含 10 張來源圖片、1 張系列總覽圖及 3 張表格圖。圖說與連結依語言分開保留；總覽的可分享圖片與可編輯來源見[系列總覽](../../research/2026-10/aaif-agntcon/overview/README.md)。來源與證據範圍見[研究紀錄](../../research/2026-10/aaif-agntcon/handoffs.md)。獨立模型審閱已完成：Codex（gpt-6.1-sol）三輪審稿、逐輪依本地來源核對後修訂，採用與不採用的理由見[研究紀錄的 Codex 審稿表](../../research/2026-10/aaif-agntcon/rewrite-2026-10-25.md)；排程稿不計為已公開的 Ambassador 申請作品。

## 發布設定讀回

核對時間：2026-10-26T10:34:32+08:00。另開新分頁，確認不含原頁面標記，再讀取 Medium 儲存的設定。

| 項目 | 讀回值 |
|---|---|
| `isPublished` | `false` |
| `publishSchedule.publishAt` | `1794186000000`（2026-11-09T01:00:00Z） |
| Topics | Artificial Intelligence、Model Context Protocol、Software Engineering、Open Source、Ai Agents |
| 封面 | `asset-01.png`，`1*l8bZZAVGBqlT0sVQdyRXdg.png`，2048×1152（2026-10-26 重灌後一度被重設為總覽圖 `diagram-01.png`；同日在發布對話框用 Change preview image 依圖片識別碼選回、按 Done，從新分頁讀回確認） |
| 預覽標題 | 把工作交給另一個 Agent 之前：授權、狀態與復原 |
| 預覽摘要 | 從東京六場簡報與一個升級案例，追問交接後的權限、未知結果，以及什麼證據才算完成。（2026-10-26 重灌後一度讀回為自動摘自 TL;DR 的首句；同日在發布對話框的 Write a preview subtitle 欄重設為此句，從新分頁讀回確認） |
| Notify subscribers | 關閉（`isPublishToEmail: false`） |
| 發布位置 | 個人 profile，未投稿 publication |

Story image 使用筆者在東京辦公室拍攝的東京鐵塔日景照（`asset-01.png`）。2026-10-26 重灌後封面一度被 Medium 重設為內文第一張圖（系列總覽圖），同日依作者指示在發布對話框用 Change preview image 選回原照、按 Done 存檔，預覽摘要也重設回自訂句，兩者皆從新分頁讀回確認；沒有按 Schedule to publish。原排程、預覽標題及通知設定與更新前相符。系列文章目前仍為排程稿，待實際公開後再更新「即將發布」標示；英文版連到先行排程的中文版本。
