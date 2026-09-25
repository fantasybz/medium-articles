# Publication record (English edition)

**Title** Green Is Not Done: Testing, Review and Reliability for Agent Output
**Post ID** `c4fc9f3d8581`（draft https://medium.com/p/c4fc9f3d8581/edit；stable URL after publishing https://medium.com/p/c4fc9f3d8581）
**Schedule** 2026-10-08（四）09:00 GMT+8（2026-09-23 已重新讀取 Medium 排程確認）
**Built with** `./tools/medium_draft.sh 2026-10-green-overview en`, block-by-block verification clean

## Settings

| Item | Value |
|---|---|
| Topics | Software Testing、Code Review、AI、Software Engineering、Engineering Management |
| Preview image | `diagram-04.png`（`1*AGrOkMD2NUf4FXaZ2-bI-A.png`，2026-09-23 已核對） |
| Notify subscribers | yes (default) |

## Status (2026-09-07)

- [x] scheduled 2026-09-07 18:18 for 2026-10-08 09:00 GMT+8 (second of the two schedule actions allowed in 24 h)
- Series links: earlier Parts and the Chinese edition (`582f24223eea`) are linked via medium.com/p/<id>; later Parts stay "(coming soon)" and are patched after each publish

## 口吻潤稿重灌（2026-09-08）

以 `./tools/medium_draft.sh 2026-10-green-overview en --post c4fc9f3d8581` 就地重灌，Post ID 不變。
重載後從伺服器讀回來驗證通過：193 個文字區塊逐塊相符、29 個連結全在、
18 張圖各在自己的槽位、無殘留 placeholder。

**排程未受影響**：重灌後 Stories → Scheduled 仍列 Oct 8, 1:00 AM (UTC)，與原排程相同。

待人工確認：封面圖（所有 figure 都重傳過，Medium 可能改用第一張當預覽圖）。

## 通順度潤稿重灌（2026-09-18）

以 `./tools/medium_draft.sh 2026-10-green-overview en --post c4fc9f3d8581` 就地重灌，Post ID 不變。
內容變更：術語首見補白話、段落接縫、開場路線圖句與結語收束、AGNTCon／書的插入段改寫成
「場景鋪陳 + 證據與收攏」並搬位；作者另裁示四處（書的限制句移位、READY 數字降括號、
感謝 Teddy 那行移到節尾紀律句之後、約束（constraint）與意圖（intent）首見配對）。
`verify_draft.py` 閘門通過（exit 0）。

**排程未受影響**：重灌後 Stories → Scheduled 仍列 Oct 8, 1:00 AM (UTC)。八篇的時段與 Post ID 全部不變（第三次量到）。
**Topics 未受影響**（Review 篇 zh 的面板實際看過，五個都在）。
**封面圖被重設，已還原**：八篇八張全部被 Medium 換成內文第一張 figure；重灌前先把八張封面的
CDN hash 記進 `.context/cover-check/baseline-2026-09-18.json`（與 2026-09-16 那份逐項相同，
表示上一輪的還原守住了），還原後回 Stories → Scheduled 核對，八篇的卡片縮圖都回到 `1*AGrOkMD2NUf4FXaZ2-bI-A.png`。

這一輪學到的：頁內選擇器**仍然列著原始那張的 hash**，所以還原可以用 hash 精準配對，
不必像 2026-09-16 那樣靠算繪高度猜；縮圖本身被裁成 248×248，長寬比不能當判準，
要比就回 CDN 取原圖尺寸。

### 2026-09-18 追加一句（payment 說明）後重灌

第一節補一句「payment 不是術語，是個例子」之後，總論兩篇再各重灌一次
（`--post 582f24223eea` / `--post c4fc9f3d8581`），`verify_draft.py` 都過。
封面同樣被重設，同樣用頁內選擇器點回原本那張；排程 10/06 與 10/08 未動。
其餘六篇這一輪沒有內容變更，沒有重灌。

### 2026-09-21 再重灌（SWE-Gate 來由／圖標題）

The prose is unchanged; the section-3 figure's subgraph title changed (the old one contradicted the piece's own prose), so diagram-02.png was re-rendered and a refill was needed to ship the new image.
`verify_draft.py` 通過。封面同樣被重設，同樣用頁內選擇器點回原本那張；排程未動。
重新算繪的 diagram-02 與原圖尺寸完全相同（zh 664x836、en 664x914），兩種語言都 PASS MERMAID.md。

## 逐句精修與 Medium 同步（2026-09-23）

依作者確認的共用風格，補足動作敘述中的對象與目的，調整敘事承接，並精修指涉、因果、
證據的適用範圍與數字定義。中文與英文正文、發布稿及本輪變更的圖表同步更新。

以 `./tools/medium_draft.sh 2026-10-green-overview en --post c4fc9f3d8581` 就地更新既有排程文章。等待儲存完成後，
另開新分頁從 Medium 讀回，`verify_draft.py` 逐塊比對通過：

| 核對項目 | 結果 |
|---|---|
| 文字區塊 | 198 個，逐塊相符 |
| 連結 | 29 個，目的地與本次發布稿相符 |
| 圖片 | 18 張，槽位及圖檔識別碼與本次發布稿相符 |
| 分隔線 | 16 條，數量相符 |
| 殘留圖片 placeholder | 0 |

封面已選回 `diagram-04.png`，重新載入發布設定後確認識別碼為
`1*AGrOkMD2NUf4FXaZ2-bI-A.png`。正文標題與預覽文字已核對。

Post ID、五個 Topics、訂閱通知設定與排程均保留。發布設定讀回的時間為
**2026-10-08（四）09:00 GMT+8**，文章仍是排程狀態；本次沒有重新排程或提前發布。
發布紀錄原先誤寫的星期已依這個時間校正。

## 跨篇指涉與後半部精修同步（2026-09-24）

跨篇引用改用可辨識的篇名、系列名或主題，移除以未定發布月份指引讀者的文字。
重新潤飾後半部的操作說明、圖表解讀、段落承接與結語，保留研究限制及人力前提；
中英文與發布包同步更新。

以 `./tools/medium_draft.sh 2026-10-green-overview en --post c4fc9f3d8581` 就地更新。等待儲存完成後，另開新分頁
讀回 Medium，逐塊比對及圖片識別碼核對通過：

| 核對項目 | 結果 |
|---|---|
| 文字區塊 | 198 個，逐塊相符 |
| 連結 | 29 個，網址及數量相符 |
| 圖片 | 18 張，槽位及內容識別碼與本次發布包相符 |
| 分隔線 | 16 條，數量相符 |
| 殘留圖片 placeholder | 0 |

封面維持 `diagram-04.png`（`1*AGrOkMD2NUf4FXaZ2-bI-A.png`）。重新讀取發布設定，
確認 Post ID、五個 Topics、訂閱通知、預覽標題與摘要、原排程均與更新前相同。
文章仍排定於 **2026-10-08（四）09:00 GMT+8** 發布；本次沒有重新排程或提前發布。

## 四部曲與付款實例同步（2026-09-25）

以購買無糖純喫綠茶的付款情境補上本文對應的約束、審閱或 mutation 證據說明，系列統一為總論＋四部曲，並加入第四篇〈付款實作篇〉的未排程導覽。中英文保留相同數字、適用條件與實驗限制。

透過 repo 的 `medium_js.py`／`medium_patch.py` 就地更新原有 Post ID。圖片沿用更新前已驗證的 CDN 圖片，內容與原發布包一致。
等待儲存穩定及至少 45 秒寫入緩衝後，另開新分頁，確認原分頁標記不存在，再從 Medium 讀回逐塊核對；若伺服器讀回尚未完整，只等待後重新讀取，不把暫時不完整的結果視為驗證通過。

| 核對項目 | 結果 |
|---|---|
| 文字區塊 | 202 個，逐塊相符 |
| 連結 | 31 個，順序及目標網址相符 |
| 圖片 | 18 張，順序、槽位及內容識別碼相符 |
| 分隔線 | 16 條，數量相符 |
| 殘留圖片 placeholder | 0 |

重新讀取發布設定，確認 Post ID、五個 Topics、訂閱通知設定、預覽標題、封面識別碼與原圖尺寸、排程均與更新前一致。預覽摘要保留原值。
封面維持 `diagram-04.png`（`1*AGrOkMD2NUf4FXaZ2-bI-A.png`）。文章仍排定於 **2026-10-08（四）09:00 GMT+8** 發布；本次沒有重新排程或提前發布。

## 第四篇排程後的導覽同步（2026-09-25）

第四篇已接續排定中文 2026-11-03、英文 2026-11-05，皆為 09:00 GMT+8。本篇將其導覽改為「coming soon」，並移除內文的未排程說明；仍以篇名指引讀者，待第四篇實際上線後再回填連結。

更新後從新分頁讀回，202 個文字區塊、31 個連結、18 張圖片、16 條分隔線皆與貼稿相符；連結順序與目的地、圖片槽位與識別碼也逐項核對。再次讀取發布設定，確認本篇原排程、Post ID、封面、Topics、預覽文字與通知設定均未改動。
