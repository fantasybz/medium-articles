# Publication record (English edition)

**Title** Green Is Not Done, Part 2 — Review Is the Control Point, Not the Bottleneck: Triage, Reviewer Fleets and the Closed-Loop Ban
**Post ID** `4d36d0f2f9c1`（draft https://medium.com/p/4d36d0f2f9c1/edit；stable URL after publishing https://medium.com/p/4d36d0f2f9c1）
**Schedule** 2026-10-22（四）09:00 GMT+8（2026-09-23 已重新讀取 Medium 排程確認）
**Built with** `./tools/medium_draft.sh 2026-10-green-review en`, block-by-block verification clean

## Settings

| Item | Value |
|---|---|
| Topics | Software Testing、Code Review、AI、Software Engineering、Engineering Management |
| Preview image | `diagram-02.png`（`1*7E7igGi0v150j59JclJy9g.png`，2026-09-23 已核對） |
| Notify subscribers | yes (default) |

## Status (2026-09-07)

- [x] scheduled 2026-09-07 18:35 for 2026-10-22 09:00 GMT+8
- Series links: earlier Parts and the Chinese edition (`ccbf0cbe2691`) are linked via medium.com/p/<id>; later Parts stay "(coming soon)" and are patched after each publish

## 口吻潤稿重灌（2026-09-08）

以 `./tools/medium_draft.sh 2026-10-green-review en --post 4d36d0f2f9c1` 就地重灌，Post ID 不變。
重載後從伺服器讀回來驗證通過：178 個文字區塊逐塊相符、29 個連結全在、
7 張圖各在自己的槽位、無殘留 placeholder。

**排程未受影響**：重灌後 Stories → Scheduled 仍列 Oct 22, 1:00 AM (UTC)，與原排程相同。

待人工確認：封面圖（所有 figure 都重傳過，Medium 可能改用第一張當預覽圖）。


## 東京會議證據插入後重灌（2026-09-16）

以 `./tools/medium_draft.sh 2026-10-green-review en --post 4d36d0f2f9c1` 就地重灌，Post ID 不變。內容變更：same insertion as the zh edition, plus one Reference。
`verify_draft.py` 閘門通過（exit 0）：文字區塊逐塊相符、連結全在、4 圖 3 表各在自己的槽位、無殘留 placeholder。

**排程未受影響**：重灌後 Stories → Scheduled 仍列 Oct 22, 1:00 AM (UTC)；八篇的時段與 Post ID 全部不變。
**Topics 未受影響**（同批另一篇實際打開設定面板看過，五個都在）。

**封面圖被重設，已還原。** 重灌後 Medium 把預覽圖重設成內文第一張 figure（`table-01.png`，表格截圖）；
重灌前先記下的封面是 `diagram-02.png`（CDN `1*7E7igGi0v150j59JclJy9g.png`），用編輯器 → Review scheduled story →
Change preview image 的頁內選擇器點回同一張 → Done。回 Stories → Scheduled 核對卡片縮圖，
檔名與重灌前相同。做法見 PUBLISHING.md〈整篇重灌〉。

## 通順度潤稿重灌（2026-09-18）

以 `./tools/medium_draft.sh 2026-10-green-review en --post 4d36d0f2f9c1` 就地重灌，Post ID 不變。
內容變更：術語首見補白話、段落接縫、開場路線圖句與結語收束、AGNTCon／書的插入段改寫成
「場景鋪陳 + 證據與收攏」並搬位；作者另裁示四處（書的限制句移位、READY 數字降括號、
感謝 Teddy 那行移到節尾紀律句之後、約束（constraint）與意圖（intent）首見配對）。
`verify_draft.py` 閘門通過（exit 0）。

**排程未受影響**：重灌後 Stories → Scheduled 仍列 Oct 22, 1:00 AM (UTC)。八篇的時段與 Post ID 全部不變（第三次量到）。
**Topics 未受影響**（Review 篇 zh 的面板實際看過，五個都在）。
**封面圖被重設，已還原**：八篇八張全部被 Medium 換成內文第一張 figure；重灌前先把八張封面的
CDN hash 記進 `.context/cover-check/baseline-2026-09-18.json`（與 2026-09-16 那份逐項相同，
表示上一輪的還原守住了），還原後回 Stories → Scheduled 核對，八篇的卡片縮圖都回到 `1*7E7igGi0v150j59JclJy9g.png`。

這一輪學到的：頁內選擇器**仍然列著原始那張的 hash**，所以還原可以用 hash 精準配對，
不必像 2026-09-16 那樣靠算繪高度猜；縮圖本身被裁成 248×248，長寬比不能當判準，
要比就回 CDN 取原圖尺寸。

### 2026-09-21 再重灌（投影片連結指到引用的那一頁）

以 `./tools/medium_draft.sh 2026-10-green-review en --post 4d36d0f2f9c1` 就地重灌，Post ID 不變。
內容變更只有一處：References 裡 Studist《Intent as Code》 那一條，連結加上 `#page=16`，讀者點過去直接落在文中引用的那一頁，
不必自己在幾十頁的 deck 裡找。頁碼是對著 PDF 內文逐頁核過的，不是照投影片上印的頁碼推的。
`verify_draft.py` 閘門通過（exit 0）。

**Medium 會保留 fragment**（這一輪實測）：連結被包成 `medium.com/r/?url=…` 之後，
把 `url=` 參數解碼回來，`#page=16` 原封不動還在。所以錨點在 Medium 上是有效的。

**排程未受影響**：仍是 Oct 22, 1:00 AM (UTC)。八篇的時段與 Post ID 全部不變（第四次量到）。
**封面圖**：被重設，已用頁內選擇器以 CDN hash 配對點回 `1*7E7igGi0v150j59JclJy9g.png`，/submission 頁讀回確認。

## 逐句精修與 Medium 同步（2026-09-23）

依作者確認的共用風格，補足動作敘述中的對象與目的，調整敘事承接，並精修指涉、因果、
證據的適用範圍與數字定義。中文與英文正文、發布稿及本輪變更的圖表同步更新。

以 `./tools/medium_draft.sh 2026-10-green-review en --post 4d36d0f2f9c1` 就地更新既有排程文章。等待儲存完成後，
另開新分頁從 Medium 讀回，`verify_draft.py` 逐塊比對通過：

| 核對項目 | 結果 |
|---|---|
| 文字區塊 | 193 個，逐塊相符 |
| 連結 | 34 個，目的地與本次發布稿相符 |
| 圖片 | 7 張，槽位及圖檔識別碼與本次發布稿相符 |
| 分隔線 | 12 條，數量相符 |
| 殘留圖片 placeholder | 0 |

封面已選回 `diagram-02.png`，重新載入發布設定後確認識別碼為
`1*7E7igGi0v150j59JclJy9g.png`。正文標題與預覽文字已核對。

Post ID、五個 Topics、訂閱通知設定與排程均保留。發布設定讀回的時間為
**2026-10-22（四）09:00 GMT+8**，文章仍是排程狀態；本次沒有重新排程或提前發布。
發布紀錄原先誤寫的星期已依這個時間校正。
