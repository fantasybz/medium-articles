# 發布紀錄

**標題** 綠燈不是驗收（一）測試篇：怎麼審閱一份 agent 寫的測試—斷言鬆綁、凍結 bug 與 mutation score
**Post ID** `b01055139451`（草稿／排程網址 https://medium.com/p/b01055139451/edit；上線後的穩定短網址 https://medium.com/p/b01055139451）
**排程** 2026-10-13（二）09:00 GMT+8（2026-09-23 已重新讀取 Medium 排程確認）
**建立方式** `./tools/medium_draft.sh 2026-10-green-testing`，逐塊比對零差異（見 [PUBLISHING.md](../../PUBLISHING.md)）

## 設定

| 項目 | 值 |
|---|---|
| Topics | Software Testing、Code Review、AI、Software Engineering、Engineering Management |
| 封面圖 | `diagram-03.png`（`1*WRLX5mB0ii2V1t7EAf7dSA.png`，2026-09-23 已核對） |
| Notify subscribers | 是（預設） |
| 發布位置 | 個人 profile，未投稿 publication |

## 狀態（2026-09-07）

- [x] 排程完成：2026-09-07 18:25 設定為 2026-10-13 09:00 GMT+8（這是當天第三個排程動作，Medium 沒有擋—排程似乎不吃「兩篇」配額，或配額只算發布）
- 系列連結：本篇連到「發布時已上線」的篇；其餘保留「（即將發布）」，上線後用 `medium_patch.py subst` 回填（見 PUBLISHING.md〈目前的發布佇列〉）
- 英文版：`publish/en/PUBLISHED.md`（Post ID `51d001a6dcd5`，排程 2026-10-15（四）09:00）

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

## 通順度潤稿重灌（2026-09-18）

以 `./tools/medium_draft.sh 2026-10-green-testing --post b01055139451` 就地重灌，Post ID 不變。
內容變更：術語首見補白話、段落接縫、開場路線圖句與結語收束、AGNTCon／書的插入段改寫成
「場景鋪陳 + 證據與收攏」並搬位；作者另裁示四處（書的限制句移位、READY 數字降括號、
感謝 Teddy 那行移到節尾紀律句之後、約束（constraint）與意圖（intent）首見配對）。
`verify_draft.py` 閘門通過（exit 0）。

**排程未受影響**：重灌後 Stories → Scheduled 仍列 Oct 13, 1:00 AM (UTC)。八篇的時段與 Post ID 全部不變（第三次量到）。
**Topics 未受影響**（Review 篇 zh 的面板實際看過，五個都在）。
**封面圖被重設，已還原**：八篇八張全部被 Medium 換成內文第一張 figure；重灌前先把八張封面的
CDN hash 記進 `.context/cover-check/baseline-2026-09-18.json`（與 2026-09-16 那份逐項相同，
表示上一輪的還原守住了），還原後回 Stories → Scheduled 核對，八篇的卡片縮圖都回到 `1*a_Hihzjn8tRZFtfv52gPqQ.png`。

這一輪學到的：頁內選擇器**仍然列著原始那張的 hash**，所以還原可以用 hash 精準配對，
不必像 2026-09-16 那樣靠算繪高度猜；縮圖本身被裁成 248×248，長寬比不能當判準，
要比就回 CDN 取原圖尺寸。

### 2026-09-21 再重灌（投影片連結指到引用的那一頁）

以 `./tools/medium_draft.sh 2026-10-green-testing --post b01055139451` 就地重灌，Post ID 不變。
內容變更只有一處：References 裡 Quartic.ai 的 K8s 升級 那一條，連結加上 `#page=29`，讀者點過去直接落在文中引用的那一頁，
不必自己在幾十頁的 deck 裡找。頁碼是對著 PDF 內文逐頁核過的，不是照投影片上印的頁碼推的。
`verify_draft.py` 閘門通過（exit 0）。

**Medium 會保留 fragment**（這一輪實測）：連結被包成 `medium.com/r/?url=…` 之後，
把 `url=` 參數解碼回來，`#page=29` 原封不動還在。所以錨點在 Medium 上是有效的。

**排程未受影響**：仍是 Oct 13, 1:00 AM (UTC)。八篇的時段與 Post ID 全部不變（第四次量到）。
**封面圖**：被重設，已還原成 `1*a_Hihzjn8tRZFtfv52gPqQ.png`，/submission 頁讀回確認。

## 逐句精修與 Medium 同步（2026-09-23）

依作者確認的共用風格，補足動作敘述中的對象與目的，調整敘事承接，並精修指涉、因果、
證據的適用範圍與數字定義。中文與英文正文、發布稿及本輪變更的圖表同步更新。

以 `./tools/medium_draft.sh 2026-10-green-testing --post b01055139451 --retitle` 就地更新既有排程文章。等待儲存完成後，
另開新分頁從 Medium 讀回，`verify_draft.py` 逐塊比對通過：

| 核對項目 | 結果 |
|---|---|
| 文字區塊 | 188 個，逐塊相符 |
| 連結 | 23 個，目的地與本次發布稿相符 |
| 圖片 | 8 張，槽位及圖檔識別碼與本次發布稿相符 |
| 分隔線 | 13 條，數量相符 |
| 殘留圖片 placeholder | 0 |

封面已選回 `diagram-03.png`，重新載入發布設定後確認識別碼為
`1*WRLX5mB0ii2V1t7EAf7dSA.png`。正文標題與預覽文字已核對。

Post ID、五個 Topics、訂閱通知設定與排程均保留。發布設定讀回的時間為
**2026-10-13（二）09:00 GMT+8**，文章仍是排程狀態；本次沒有重新排程或提前發布。
發布紀錄原先誤寫的星期已依這個時間校正。

## 跨篇指涉與後半部精修同步（2026-09-24）

跨篇引用改用可辨識的篇名、系列名或主題，移除以未定發布月份指引讀者的文字。
重新潤飾後半部的操作說明、圖表解讀、段落承接與結語，保留研究限制及人力前提；
中英文與發布包同步更新。

以 `./tools/medium_draft.sh 2026-10-green-testing --post b01055139451` 就地更新。等待儲存完成後，另開新分頁
讀回 Medium，逐塊比對及圖片識別碼核對通過：

| 核對項目 | 結果 |
|---|---|
| 文字區塊 | 188 個，逐塊相符 |
| 連結 | 23 個，網址及數量相符 |
| 圖片 | 8 張，槽位及內容識別碼與本次發布包相符 |
| 分隔線 | 13 條，數量相符 |
| 殘留圖片 placeholder | 0 |

封面維持 `diagram-03.png`（`1*WRLX5mB0ii2V1t7EAf7dSA.png`）。重新讀取發布設定，
確認 Post ID、五個 Topics、訂閱通知、預覽標題與摘要、原排程均與更新前相同。
文章仍排定於 **2026-10-13（二）09:00 GMT+8** 發布；本次沒有重新排程或提前發布。

## 四部曲與付款實例同步（2026-09-25）

以購買無糖純喫綠茶的付款情境補上本文對應的約束、審閱或 mutation 證據說明，系列統一為總論＋四部曲，並加入第四篇〈付款實作篇〉的未排程導覽。中英文保留相同數字、適用條件與實驗限制。

透過 repo 的 `medium_js.py`／`medium_patch.py` 就地更新原有 Post ID。測試篇的中英文 `table-03.png` 重新算繪並上傳，其他圖片沿用更新前已驗證的 CDN 圖片。
等待儲存穩定及至少 45 秒寫入緩衝後，另開新分頁，確認原分頁標記不存在，再從 Medium 讀回逐塊核對；若伺服器讀回尚未完整，只等待後重新讀取，不把暫時不完整的結果視為驗證通過。

| 核對項目 | 結果 |
|---|---|
| 文字區塊 | 196 個，逐塊相符 |
| 連結 | 25 個，順序及目標網址相符 |
| 圖片 | 8 張，順序、槽位及內容識別碼相符 |
| 分隔線 | 13 條，數量相符 |
| 殘留圖片 placeholder | 0 |

重新讀取發布設定，確認 Post ID、五個 Topics、訂閱通知設定、預覽標題、封面識別碼與原圖尺寸、排程均與更新前一致。預覽摘要保留原值。
封面維持 `diagram-03.png`（`1*WRLX5mB0ii2V1t7EAf7dSA.png`）。文章仍排定於 **2026-10-13（二）09:00 GMT+8** 發布；本次沒有重新排程或提前發布。
