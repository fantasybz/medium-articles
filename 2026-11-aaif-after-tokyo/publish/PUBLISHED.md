# 發布紀錄

**標題** 從東京 AGNTCon 回來：Agent 接上工具之後，工作才剛開始
**Post ID** `e3d060cb8b03`
**狀態** 已排程，尚未公開。
**排程** 2026-11-02 09:00 Asia/Taipei（UTC 01:00）；新分頁讀回確認。
**草稿** https://medium.com/p/e3d060cb8b03/edit
**上線後穩定短網址** https://medium.com/p/e3d060cb8b03
**核對時間** 2026-10-26T10:34:32+08:00

## 內容核對

2026-10-25 依作者試讀意見重新分析改寫後，再由 Codex 三輪審稿、逐輪依本地來源核對後修訂；本輪把三輪後的定稿以 `medium_draft.sh --post` 就地重灌，沿用既有 Post ID，排程設定另外讀回核對。重灌走與建新草稿相同的插圖與逐塊比對流程，等待儲存穩定後重新載入再比對一次。本輪起每張來源圖片的圖說不再是正文段落，而是貼進該圖在 Medium 的 caption 欄（含圖說內的連結），`verify_draft.py` 逐張比對 caption 文字、連結數含 caption 內的連結。

| 項目 | 結果 |
|---|---:|
| 文字區塊 | 214，逐塊相符 |
| 連結 | 94，順序與目的地相符 |
| 圖片 | 23，順序與槽位相符 |
| 圖說（Medium caption） | 19，逐張相符 |
| 分隔線 | 1 |
| 圖片 placeholder | 0 |

本語言包包含 19 張來源圖片、1 張系列總覽圖及 3 張表格圖。圖說與連結依語言分開保留；總覽的可分享圖片與可編輯來源見[系列總覽](../../research/2026-10/aaif-agntcon/overview/README.md)。來源與證據範圍見[研究紀錄](../../research/2026-10/aaif-agntcon/media.md)。獨立模型審閱已完成：Codex（gpt-6.1-sol）三輪審稿、逐輪依本地來源核對後修訂，採用與不採用的理由見[研究紀錄的 Codex 審稿表](../../research/2026-10/aaif-agntcon/rewrite-2026-10-25.md)；排程稿不計為已公開的 Ambassador 申請作品。

## 發布設定讀回

核對時間：2026-10-26T10:34:32+08:00。另開新分頁，確認不含原頁面標記，再讀取 Medium 儲存的設定。

| 項目 | 讀回值 |
|---|---|
| `isPublished` | `false` |
| `publishSchedule.publishAt` | `1793581200000`（2026-11-02T01:00:00Z） |
| Topics | Model Context Protocol、Artificial Intelligence、Software Engineering、Open Source、Ai Agents |
| 封面 | `asset-01.png`，`1*jY2nu2UmaSugznxXM7TsMA.png`，1080×1080 |
| 預覽標題 | 從東京 AGNTCon 回來：Agent 接上工具之後，工作才剛開始 |
| 預覽摘要 | 從受邀赴東京、午休實作到七場錄影，追問 Agent 行動的授權、失敗後的狀態與交付證據。（2026-10-26 重灌後一度讀回為自動摘自 TL;DR 的首句；同日在發布對話框的 Write a preview subtitle 欄重設為此句，從新分頁讀回確認）；原記的「六場錄影」改為「七場」，以符合 10/25 補入的 PagerDuty 場次 |
| Notify subscribers | 關閉（`isPublishToEmail: false`） |
| 發布位置 | 個人 profile，未投稿 publication |

Story image 使用筆者自己的東京會場照片（`asset-01.png`，也是內文第一張圖，所以重灌沒有動到封面）。2026-10-26 重灌後，原排程、預覽標題、封面原圖及通知設定與更新前相符；預覽摘要一度讀回為自動摘自 TL;DR 的首句，同日依作者指示在發布對話框重設為自訂句並把「六場錄影」改為「七場」，從新分頁讀回確認，沒有按 Schedule to publish。系列文章目前仍為排程稿，待實際公開後再更新「即將發布」標示；英文版連到先行排程的中文版本。

## 2026-10-27 重灌：系列總覽圖改為完整尺寸

系列總覽圖 `diagram-01.png` 原本是 `research/scripts/mermaid_check.sh` 修正前的退回截圖（664×948，瀏覽器預設的 300 CSS px）。作者 2026-10-27 決定重灌，先以修正後的 `research/scripts/render_images.sh` 重繪整包：只有 `diagram-01.png` 變成 1156×1664，其餘表格與照片位元組不變。再以 `./tools/medium_draft.sh 2026-11-aaif-after-tokyo --post e3d060cb8b03` 重灌（未加 `--reuse-figures`），台北時間 23:04 完成讀回。

儲存後重新讀回兩次：**214 個文字區塊、94 個連結、23 張圖、19 個 caption** 均與貼稿相符，placeholder 為 0。`diagram-01` 由 `1*hcfJVSrI3ZyNIne3eMmvSQ.png`（664×948）換成 `1*F4Urac80aH8T4p1KGCd5fw.png`（1156×1664，自 Medium CDN 讀 PNG 檔頭核對），其餘 22 張圖保留原識別碼。

封面是內文第一張圖 `asset-01.png`（`1*jY2nu2UmaSugznxXM7TsMA.png`，1080×1080），位元組沒變，重灌後仍是同一個識別碼，不需要重選。預覽摘要被換成自動摘錄，已把自訂句填回 Write a preview subtitle 欄並以 Tab 離開欄位。沒有按 Schedule to publish。另開新分頁讀回：封面為原照片，預覽摘要、標題、`publishAt: 1793581200000`（2026-11-02 09:00 Asia/Taipei）、`isPublished: false` 與通知設定（關閉，`isPublishToEmail: false`）皆與重灌前的快照相同。這次重灌的貼稿 SHA-256 為 `dc59296554a1951d7e270960e97b74f0086998219e6598da8862af081ff6da2e`；重灌前後快照存於本機 `.context/refill-2026-10-27/`，未納入 git。
