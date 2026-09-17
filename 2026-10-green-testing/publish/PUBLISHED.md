# 發布紀錄

**標題** 一、測試篇：怎麼審一份 agent 寫的測試—斷言鬆綁、凍結 bug 與 mutation score
**Post ID** `b01055139451`（草稿／排程網址 https://medium.com/p/b01055139451/edit；上線後的穩定短網址 https://medium.com/p/b01055139451）
**排程** 2026-10-13（一）09:00 GMT+8（尚待作者確認；2026-09-07 以 Publish 對話框的 Schedule for later 設定，見下方狀態）
**建立方式** `./tools/medium_draft.sh 2026-10-green-testing`，逐塊比對零差異（見 [PUBLISHING.md](../../PUBLISHING.md)）

## 設定

| 項目 | 值 |
|---|---|
| Topics | Software Testing、Code Review、AI、Software Engineering、Engineering Management |
| 封面圖 | `diagram-03.png`（2026-09-16 用 CDN 原圖的高寬比對出來的；本欄原本寫 `diagram-01.png`，是記錯。內文第一張其實是 `table-01.png`，所以這個封面是人挑過的，不是 Medium 預設） |
| Notify subscribers | 是（預設） |
| 發布位置 | 個人 profile，未投稿 publication |

## 狀態（2026-09-07）

- [x] 排程完成：2026-09-07 18:25 設定為 2026-10-13 09:00 GMT+8（這是當天第三個排程動作，Medium 沒有擋—排程似乎不吃「兩篇」配額，或配額只算發布）
- 系列連結：本篇連到「發布時已上線」的篇；其餘保留「（即將發布）」，上線後用 `medium_patch.py subst` 回填（見 PUBLISHING.md〈目前的發布佇列〉）
- 英文版：`publish/en/PUBLISHED.md`（Post ID `51d001a6dcd5`，排程 2026-10-15（三）09:00）

## 上線後核對（發布後填）

| 項目 | 數量 |
|---|---|
| 內文區塊（與轉換後 payload 逐塊比對） | 建草稿時零差異 |
| 插圖 | 見 `publish/figures.json` |
| 死連結 / 殘留「（即將發布）」/ 裂開的破折號 | 上線後檢查 |

## 口吻潤稿重灌（2026-09-08）

以 `./tools/medium_draft.sh 2026-10-green-testing --post b01055139451` 就地重灌，Post ID 不變。
重載後從伺服器讀回來驗證通過：175 個文字區塊逐塊相符、19 個連結全在、
8 張圖各在自己的槽位、無殘留 placeholder。

**排程未受影響**：重灌後 Stories → Scheduled 仍列 Oct 13, 1:00 AM (UTC)，與原排程相同。

待人工確認：封面圖（所有 figure 都重傳過，Medium 可能改用第一張當預覽圖）。


## 東京會議證據插入後重灌（2026-09-16）

以 `./tools/medium_draft.sh 2026-10-green-testing --post b01055139451` 就地重灌，Post ID 不變。內容變更：§二 加李博杰第七章九類失敗的 hack 驗證環境；§五 加 Quartic.ai 升級 production K8s 只檢查第一個節點的自承案例（`2QlD9` slide 29）；References 加兩條。
`verify_draft.py` 閘門通過（exit 0）：文字區塊逐塊相符、連結全在、4 圖 4 表各在自己的槽位、無殘留 placeholder。

**排程未受影響**：重灌後 Stories → Scheduled 仍列 Oct 13, 1:00 AM (UTC)；八篇的時段與 Post ID 全部不變。
**Topics 未受影響**（同批另一篇實際打開設定面板看過，五個都在）。

**封面圖被重設，已還原。** 重灌後 Medium 把預覽圖重設成內文第一張 figure（`table-01.png`，表格截圖）；
重灌前先記下的封面是 `diagram-03.png`（CDN `1*a_Hihzjn8tRZFtfv52gPqQ.png`），用編輯器 → Review scheduled story →
Change preview image 的頁內選擇器點回同一張 → Done。回 Stories → Scheduled 核對卡片縮圖，
檔名與重灌前相同。做法見 PUBLISHING.md〈整篇重灌〉。
