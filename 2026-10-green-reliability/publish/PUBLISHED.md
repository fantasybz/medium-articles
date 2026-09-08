# 發布紀錄

**標題** 三、可靠度篇：SWE-Gate 量到的 34%—constraint tests、pass^k 與授權擴張的閘門
**Post ID** `3c64a9622777`（草稿／排程網址 https://medium.com/p/3c64a9622777/edit；上線後的穩定短網址 https://medium.com/p/3c64a9622777）
**排程** 2026-10-27（一）09:00 GMT+8（尚待作者確認；2026-09-07 以 Publish 對話框的 Schedule for later 設定，見下方狀態）
**建立方式** `./tools/medium_draft.sh 2026-10-green-reliability`，逐塊比對零差異（見 [PUBLISHING.md](../../PUBLISHING.md)）

## 設定

| 項目 | 值 |
|---|---|
| Topics | Software Testing、Code Review、AI、Software Engineering、Engineering Management |
| 封面圖 | Medium 預設第一張 figure（`diagram-01.png`，是圖不是表格，未改） |
| Notify subscribers | 是（預設） |
| 發布位置 | 個人 profile，未投稿 publication |

## 狀態（2026-09-07）

- [x] 排程完成：2026-09-07 18:45 設定為 2026-10-27 09:00 GMT+8（第一次點到月曆裡九月尾巴的 27，顯示 9/27，改點十月格子後才對；排程前一律核對顯示的日期字串）
- 系列連結：本篇連到「發布時已上線」的篇；其餘保留「（即將發布）」，上線後用 `medium_patch.py subst` 回填（見 PUBLISHING.md〈目前的發布佇列〉）
- 英文版：`publish/en/PUBLISHED.md`（Post ID `4b6d147bff0d`，排程 2026-10-29（三）09:00）

## 上線後核對（發布後填）

| 項目 | 數量 |
|---|---|
| 內文區塊（與轉換後 payload 逐塊比對） | 建草稿時零差異 |
| 插圖 | 見 `publish/figures.json` |
| 死連結 / 殘留「（即將發布）」/ 裂開的破折號 | 上線後檢查 |

## 口吻潤稿重灌（2026-09-08）

以 `./tools/medium_draft.sh 2026-10-green-reliability --post 3c64a9622777` 就地重灌。
Post ID 不變。驗證：148 個文字區塊逐塊相符、19 個連結全在、7 張圖各在自己的槽位、
10 條分隔線、`figuresLeft: 0`、無殘留 placeholder。

**實測：排程沒有掉。** 重灌後 Stories → Scheduled 仍列 Oct 27, 1:00 AM（UTC，
即 09:00 GMT+8），與原排程相同。這是本 repo 第一次驗證「編輯排程草稿會保留排程」。

待人工確認：封面圖。所有 figure 都是刪掉重傳的，Medium 可能改用第一張圖
（table-01）當預覽圖，需要進設定確認仍是當初挑的那張 diagram。
