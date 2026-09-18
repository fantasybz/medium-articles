# 發布紀錄

**標題** 三、可靠度篇：SWE-Gate 量到的 34%—constraint tests、pass^k 與授權擴張的閘門
**Post ID** `3c64a9622777`（草稿／排程網址 https://medium.com/p/3c64a9622777/edit；上線後的穩定短網址 https://medium.com/p/3c64a9622777）
**排程** 2026-10-27（一）09:00 GMT+8（尚待作者確認；2026-09-07 以 Publish 對話框的 Schedule for later 設定，見下方狀態）
**建立方式** `./tools/medium_draft.sh 2026-10-green-reliability`，逐塊比對零差異（見 [PUBLISHING.md](../../PUBLISHING.md)）

## 設定

| 項目 | 值 |
|---|---|
| Topics | Software Testing、Code Review、AI、Software Engineering、Engineering Management |
| 封面圖 | `diagram-02.png`（2026-09-16 用 CDN 原圖的高寬比對出來的；本欄原本寫 `diagram-01.png`，是記錯。內文第一張其實是 `table-01.png`，所以這個封面是人挑過的，不是 Medium 預設） |
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


## 東京會議證據插入後重灌（2026-09-16）

以 `./tools/medium_draft.sh 2026-10-green-reliability --post 3c64a9622777` 就地重灌，Post ID 不變。內容變更：§五 加 PagerDuty 的 Red Line Rate（`2QlEA` deck p. 21）；References 加一條。
`verify_draft.py` 閘門通過（exit 0）：文字區塊逐塊相符、連結全在、4 圖 3 表各在自己的槽位、無殘留 placeholder。

**排程未受影響**：重灌後 Stories → Scheduled 仍列 Oct 27, 1:00 AM (UTC)；八篇的時段與 Post ID 全部不變。
**Topics 未受影響**（同批另一篇實際打開設定面板看過，五個都在）。

**封面圖被重設，已還原。** 重灌後 Medium 把預覽圖重設成內文第一張 figure（`table-01.png`，表格截圖）；
重灌前先記下的封面是 `diagram-02.png`（CDN `1*dt6CGm73bHy5WRyvsd7ppQ.png`），用編輯器 → Review scheduled story →
Change preview image 的頁內選擇器點回同一張 → Done。回 Stories → Scheduled 核對卡片縮圖，
檔名與重灌前相同。做法見 PUBLISHING.md〈整篇重灌〉。

## 通順度潤稿重灌（2026-09-18）

以 `./tools/medium_draft.sh 2026-10-green-reliability --post 3c64a9622777` 就地重灌，Post ID 不變。
內容變更：術語首見補白話、段落接縫、開場路線圖句與結語收束、AGNTCon／書的插入段改寫成
「場景鋪陳 + 證據與收攏」並搬位；作者另裁示四處（書的限制句移位、READY 數字降括號、
感謝 Teddy 那行移到節尾紀律句之後、約束（constraint）與意圖（intent）首見配對）。
`verify_draft.py` 閘門通過（exit 0）。

**排程未受影響**：重灌後 Stories → Scheduled 仍列 Oct 27, 1:00 AM (UTC)。八篇的時段與 Post ID 全部不變（第三次量到）。
**Topics 未受影響**（Review 篇 zh 的面板實際看過，五個都在）。
**封面圖被重設，已還原**：八篇八張全部被 Medium 換成內文第一張 figure；重灌前先把八張封面的
CDN hash 記進 `.context/cover-check/baseline-2026-09-18.json`（與 2026-09-16 那份逐項相同，
表示上一輪的還原守住了），還原後回 Stories → Scheduled 核對，八篇的卡片縮圖都回到 `1*dt6CGm73bHy5WRyvsd7ppQ.png`。

這一輪學到的：頁內選擇器**仍然列著原始那張的 hash**，所以還原可以用 hash 精準配對，
不必像 2026-09-16 那樣靠算繪高度猜；縮圖本身被裁成 248×248，長寬比不能當判準，
要比就回 CDN 取原圖尺寸。
