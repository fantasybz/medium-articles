# Publication record (English edition)

**Title** Green Is Not Done, Part 3 — The 34% SWE-Gate Found Behind a Green Build: Constraint Tests, pass^k and the Gate for Expanding Autonomy
**Post ID** `4b6d147bff0d`（draft https://medium.com/p/4b6d147bff0d/edit；stable URL after publishing https://medium.com/p/4b6d147bff0d）
**Schedule** 2026-10-29（四）09:00 GMT+8（2026-09-23 已重新讀取 Medium 排程確認）
**Built with** `./tools/medium_draft.sh 2026-10-green-reliability en`, block-by-block verification clean

## Settings

| Item | Value |
|---|---|
| Topics | Software Testing、Code Review、AI、Software Engineering、Engineering Management |
| Preview image | `diagram-02.png`（`1*R6TYJinsdAM_d3U30wrV6Q.png`，2026-09-23 已核對） |
| Notify subscribers | yes (default) |

## Status (2026-09-07)

- [x] scheduled 2026-09-07 18:47 for 2026-10-29 09:00 GMT+8
- Series links: earlier Parts and the Chinese edition (`3c64a9622777`) are linked via medium.com/p/<id>; later Parts stay "(coming soon)" and are patched after each publish

## 口吻潤稿重灌（2026-09-08）

以 `./tools/medium_draft.sh 2026-10-green-reliability en --post 4b6d147bff0d` 就地重灌，Post ID 不變。
重載後從伺服器讀回來驗證通過：148 個文字區塊逐塊相符、20 個連結全在、
7 張圖各在自己的槽位、無殘留 placeholder。

**排程未受影響**：重灌後 Stories → Scheduled 仍列 Oct 29, 1:00 AM (UTC)，與原排程相同。

待人工確認：封面圖（所有 figure 都重傳過，Medium 可能改用第一張當預覽圖）。

## 東京會議證據插入後重灌（2026-09-16）

以 `./tools/medium_draft.sh 2026-10-green-reliability en --post 4b6d147bff0d` 就地重灌，Post ID 不變。
內容變更只有一句：§5 授權擴張的閘門加入 PagerDuty 的 Red Line Rate（`2QlEA`，deck p. 21），
加一條 References。

驗證（寫入後一次、從 Medium 重讀後再一次，兩次相同）：
150 個文字區塊逐塊相符、22 個連結全在、7 張圖各在自己的槽位、10 條分隔線、無殘留 placeholder。

**排程未受影響（第二次實測）**：重灌後 Stories → Scheduled 仍列 Oct 29, 1:00 AM (UTC)，
八篇的排程日期與 Post ID 全部不變。2026-09-08 那次已經量過一次，這次是複驗。

**封面圖：仍是表格截圖。** 這次實際看了圖：卡片上的預覽是 constraint-test 分類表
（`table-01.png`），不是圖。對照組是同一篇的中文版 `3c64a9622777`（本次未重灌），
它的封面是 pass^k golden set 流程圖。兩個語言的 paste 都是 `table-01.png` 排在
`diagram-01.png` 之前，所以 Medium 取第一張 figure 就會取到表格。

無法從現況分辨這是「英文版一直都是表格」還是「重灌把封面重設成第一張 figure」——
本欄從 2026-09-08 起就掛著「待人工確認」，中間沒有人看過。要分辨只能在下一次重灌前
先記下當時的封面。

已處理：封面改成 golden set pass^k 流程圖，即 `diagram-02.png`（不是先前寫的 diagram-01——那是照中文 ledger 抄的，中文那欄記錯了檔名）。
做法：編輯器 → Review scheduled story → Change preview image（頁內縮圖選擇器）→ 點 `1*R6TYJinsdAM_d3U30wrV6Q.png` → Done。
按 Done 即存，沒有按 Schedule to publish；之後 Stories → Scheduled 的卡片縮圖已換成該檔名。

## 通順度潤稿重灌（2026-09-18）

以 `./tools/medium_draft.sh 2026-10-green-reliability en --post 4b6d147bff0d` 就地重灌，Post ID 不變。
內容變更：術語首見補白話、段落接縫、開場路線圖句與結語收束、AGNTCon／書的插入段改寫成
「場景鋪陳 + 證據與收攏」並搬位；作者另裁示四處（書的限制句移位、READY 數字降括號、
感謝 Teddy 那行移到節尾紀律句之後、約束（constraint）與意圖（intent）首見配對）。
`verify_draft.py` 閘門通過（exit 0）。

**排程未受影響**：重灌後 Stories → Scheduled 仍列 Oct 29, 1:00 AM (UTC)。八篇的時段與 Post ID 全部不變（第三次量到）。
**Topics 未受影響**（Review 篇 zh 的面板實際看過，五個都在）。
**封面圖被重設，已還原**：八篇八張全部被 Medium 換成內文第一張 figure；重灌前先把八張封面的
CDN hash 記進 `.context/cover-check/baseline-2026-09-18.json`（與 2026-09-16 那份逐項相同，
表示上一輪的還原守住了），還原後回 Stories → Scheduled 核對，八篇的卡片縮圖都回到 `1*R6TYJinsdAM_d3U30wrV6Q.png`。

這一輪學到的：頁內選擇器**仍然列著原始那張的 hash**，所以還原可以用 hash 精準配對，
不必像 2026-09-16 那樣靠算繪高度猜；縮圖本身被裁成 248×248，長寬比不能當判準，
要比就回 CDN 取原圖尺寸。

這一篇第一次重灌在重載後的 settle poll 失敗（`no Medium editor on this page`），
沒有走到 `verify_draft.py`。照腳本自己寫的恢復方式重跑同一道就過了；
重跑前先開編輯器看過：圖 7 張到齊、無殘留 placeholder、仍是 Scheduled。

### 2026-09-21 再重灌（SWE-Gate 來由／圖標題）

Section 1 now says where the 34% came from (the overview's three-layer table leaves that layer to this piece) and carries the publication date.
`verify_draft.py` 通過。封面同樣被重設，同樣用頁內選擇器點回原本那張；排程未動。
重新算繪的 diagram-02 與原圖尺寸完全相同（zh 664x836、en 664x914），兩種語言都 PASS MERMAID.md。

### 2026-09-21 再重灌（投影片連結指到引用的那一頁）

以 `./tools/medium_draft.sh 2026-10-green-reliability en --post 4b6d147bff0d` 就地重灌，Post ID 不變。
內容變更只有一處：References 裡 PagerDuty 那一條加了頁碼錨點。這一篇引的其實是兩張不同的投影片——
第五節先描述並引述「THE RED LINE」那張（p.15），下一段才是 H.I.R.E. 的 Red Line Rate 指標定義頁（p.21），
原本的條目只指 p.21，讀者要自己往回翻六頁。現在兩頁各給一個錨點，點過去就落在對的那一頁。
頁碼是對著 PDF 內文逐頁核過的，不是照投影片上印的頁碼推的（p.15 上逐字對過
「Reads the signals and drafts a fix command.」與「It never touches production.」）。
`verify_draft.py` 閘門通過（exit 0）。

**Medium 會保留 fragment**（這一輪實測）：連結被包成 `medium.com/r/?url=…` 之後，
把 `url=` 參數解碼回來，`#page=N` 原封不動還在。所以錨點在 Medium 上是有效的。

**排程未受影響**：仍是 Oct 29, 1:00 AM (UTC)。八篇的時段與 Post ID 全部不變（第四次量到）。
**封面圖**：被重設，已還原成 `1*R6TYJinsdAM_d3U30wrV6Q.png`，/submission 頁讀回確認。注意 Stories → Scheduled 上，卡片縮圖仍顯示舊的 `1*GIFtopFIBTu6FEE9q44RiA.jpeg`，那是 Medium 自己的社群卡快取，不是實際預覽圖——核對要以 /submission 為準。

## 逐句精修與 Medium 同步（2026-09-23）

依作者確認的共用風格，補足動作敘述中的對象與目的，調整敘事承接，並精修指涉、因果、
證據的適用範圍與數字定義。中文與英文正文、發布稿及本輪變更的圖表同步更新。

以 `./tools/medium_draft.sh 2026-10-green-reliability en --post 4b6d147bff0d` 就地更新既有排程文章。等待儲存完成後，
另開新分頁從 Medium 讀回，`verify_draft.py` 逐塊比對通過：

| 核對項目 | 結果 |
|---|---|
| 文字區塊 | 151 個，逐塊相符 |
| 連結 | 23 個，目的地與本次發布稿相符 |
| 圖片 | 7 張，槽位及圖檔識別碼與本次發布稿相符 |
| 分隔線 | 10 條，數量相符 |
| 殘留圖片 placeholder | 0 |

封面已選回 `diagram-02.png`，重新載入發布設定後確認識別碼為
`1*R6TYJinsdAM_d3U30wrV6Q.png`。正文標題與預覽文字已核對。

Post ID、五個 Topics、訂閱通知設定與排程均保留。發布設定讀回的時間為
**2026-10-29（四）09:00 GMT+8**，文章仍是排程狀態；本次沒有重新排程或提前發布。
發布紀錄原先誤寫的星期已依這個時間校正。
