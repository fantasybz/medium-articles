# Publication record (English edition)

**Title** Part 1 — Reviewing the Tests an Agent Wrote
**Post ID** `51d001a6dcd5`（draft https://medium.com/p/51d001a6dcd5/edit；stable URL after publishing https://medium.com/p/51d001a6dcd5）
**Schedule** 2026-10-15（三）09:00 GMT+8（two days after the Chinese edition, same week）
**Built with** `./tools/medium_draft.sh 2026-10-green-testing en`, block-by-block verification clean

## Settings

| Item | Value |
|---|---|
| Topics | Software Testing、Code Review、AI、Software Engineering、Engineering Management |
| Preview image | Medium default, first figure (`diagram-01.png`) |
| Notify subscribers | yes (default) |

## Status (2026-09-07)

- [x] scheduled 2026-09-07 18:31 for 2026-10-15 09:00 GMT+8
- Series links: earlier Parts and the Chinese edition (`b01055139451`) are linked via medium.com/p/<id>; later Parts stay "(coming soon)" and are patched after each publish

## 口吻潤稿重灌（2026-09-08）

以 `./tools/medium_draft.sh 2026-10-green-testing en --post 51d001a6dcd5` 就地重灌，Post ID 不變。
重載後從伺服器讀回來驗證通過：175 個文字區塊逐塊相符、20 個連結全在、
8 張圖各在自己的槽位、無殘留 placeholder。

**排程未受影響**：重灌後 Stories → Scheduled 仍列 Oct 15, 1:00 AM (UTC)，與原排程相同。

待人工確認：封面圖（所有 figure 都重傳過，Medium 可能改用第一張當預覽圖）。


## 東京會議證據插入後重灌（2026-09-16）

以 `./tools/medium_draft.sh 2026-10-green-testing en --post 51d001a6dcd5` 就地重灌，Post ID 不變。內容變更：same two insertions as the zh edition, plus two References。
`verify_draft.py` 閘門通過（exit 0）：文字區塊逐塊相符、連結全在、4 圖 4 表各在自己的槽位、無殘留 placeholder。

**排程未受影響**：重灌後 Stories → Scheduled 仍列 Oct 15, 1:00 AM (UTC)；八篇的時段與 Post ID 全部不變。
**Topics 未受影響**（同批另一篇實際打開設定面板看過，五個都在）。

**封面圖被重設，已還原。** 重灌後 Medium 把預覽圖重設成內文第一張 figure（`table-01.png`，表格截圖）；
重灌前先記下的封面是 `diagram-03.png`（CDN `1*PalxTLDGSOxYu-qXcJDhlA.png`），用編輯器 → Review scheduled story →
Change preview image 的頁內選擇器點回同一張 → Done。回 Stories → Scheduled 核對卡片縮圖，
檔名與重灌前相同。做法見 PUBLISHING.md〈整篇重灌〉。
