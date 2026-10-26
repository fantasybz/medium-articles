# 發布紀錄

**標題** 從東京 AGNTCon 回來：Agent 接上工具之後，工作才剛開始
**Post ID** `e3d060cb8b03`
**狀態** 已排程，尚未公開。
**排程** 2026-11-02 09:00 Asia/Taipei（UTC 01:00）；新分頁讀回確認。
**草稿** https://medium.com/p/e3d060cb8b03/edit
**上線後穩定短網址** https://medium.com/p/e3d060cb8b03
**核對時間** 2026-10-26T01:46:00+08:00

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

核對時間：2026-10-26T01:46:00+08:00。另開新分頁，確認不含原頁面標記，再讀取 Medium 儲存的設定。

| 項目 | 讀回值 |
|---|---|
| `isPublished` | `false` |
| `publishSchedule.publishAt` | `1793581200000`（2026-11-02T01:00:00Z） |
| Topics | Model Context Protocol、Artificial Intelligence、Software Engineering、Open Source、Ai Agents |
| 封面 | `asset-01.png`，`1*jY2nu2UmaSugznxXM7TsMA.png`，1080×1080 |
| 預覽標題 | 從東京 AGNTCon 回來：Agent 接上工具之後，工作才剛開始 |
| 預覽摘要 | （2026-10-26 重灌後讀回）Medium 目前顯示的是自動摘自內文 TL;DR 的首句：「TL;DR — 8 月底一張臨時的邀請，讓我在兩週內安排了東京 AGNTCon + MCPCon 的行程。午休時把 Kong 的多代理展示架起來跑了三個情境……」。先前記的自訂摘要「從受邀赴東京、午休實作到六場錄影，追問 Agent 行動的授權、失敗後的狀態與交付證據。」不在 Medium 設定裡（也已不符新稿的「錄影」數），要自訂請作者在發布對話框重設 |
| Notify subscribers | 關閉（`isPublishToEmail: false`） |
| 發布位置 | 個人 profile，未投稿 publication |

Story image 使用筆者自己的東京會場照片。本次更新後，原排程、預覽標題與摘要、封面原圖及通知設定均與更新前相符。系列文章目前仍為排程稿，待實際公開後再更新「即將發布」標示；英文版連到先行排程的中文版本。
