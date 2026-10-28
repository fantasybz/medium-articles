# Publication record (English edition)

**Title** Green Is Not Done, Part 3 — The 34% SWE-Gate Found Behind a Green Build: Constraint Tests, pass^k and the Gate for Expanding Autonomy
**Post ID** `4b6d147bff0d`（draft https://medium.com/p/4b6d147bff0d/edit；stable URL after publishing https://medium.com/p/4b6d147bff0d）
**Schedule** 2026-10-29（四）09:00 GMT+8（2026-10-24 已重新讀取 Medium 排程確認）
**Built with** `./tools/medium_draft.sh 2026-10-green-reliability en`, block-by-block verification clean
**2026-10-26** 原稿與貼稿修訂後已重灌並讀回；同日 /ship 審查發現重繪的圖只有一半解析度，腳本修正後第二次重灌，見文末兩節。

## Settings

| Item | Value |
|---|---|
| Topics | Software Testing、Code Review、AI、Software Engineering、Engineering Management |
| Preview image | `diagram-02.png`（`1*7Mq2-4lNefvJNHjuu8jpLQ.png`，1486×1136，2026-10-26 第二次重灌後已核對） |
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

## 跨篇指涉與後半部精修同步（2026-09-24）

跨篇引用改用可辨識的篇名、系列名或主題，移除以未定發布月份指引讀者的文字。
重新潤飾後半部的操作說明、圖表解讀、段落承接與結語，保留研究限制及人力前提；
中英文與發布包同步更新。

以 `./tools/medium_draft.sh 2026-10-green-reliability en --post 4b6d147bff0d` 就地更新。等待儲存完成後，另開新分頁
讀回 Medium，逐塊比對及圖片識別碼核對通過：

| 核對項目 | 結果 |
|---|---|
| 文字區塊 | 151 個，逐塊相符 |
| 連結 | 23 個，網址及數量相符 |
| 圖片 | 7 張，槽位及內容識別碼與本次發布包相符 |
| 分隔線 | 10 條，數量相符 |
| 殘留圖片 placeholder | 0 |

封面維持 `diagram-02.png`（`1*R6TYJinsdAM_d3U30wrV6Q.png`）。重新讀取發布設定，
確認 Post ID、五個 Topics、訂閱通知、預覽標題與摘要、原排程均與更新前相同。
文章仍排定於 **2026-10-29（四）09:00 GMT+8** 發布；本次沒有重新排程或提前發布。

## 四部曲與付款實例同步（2026-09-25）

以購買無糖純喫綠茶的付款情境補上本文對應的約束、審閱或 mutation 證據說明，系列統一為總論＋四部曲，並加入第四篇〈付款實作篇〉的未排程導覽。中英文保留相同數字、適用條件與實驗限制。

透過 repo 的 `medium_js.py`／`medium_patch.py` 就地更新原有 Post ID。圖片沿用更新前已驗證的 CDN 圖片，內容與原發布包一致。
等待儲存穩定及至少 45 秒寫入緩衝後，另開新分頁，確認原分頁標記不存在，再從 Medium 讀回逐塊核對；若伺服器讀回尚未完整，只等待後重新讀取，不把暫時不完整的結果視為驗證通過。

| 核對項目 | 結果 |
|---|---|
| 文字區塊 | 159 個，逐塊相符 |
| 連結 | 25 個，順序及目標網址相符 |
| 圖片 | 7 張，順序、槽位及內容識別碼相符 |
| 分隔線 | 10 條，數量相符 |
| 殘留圖片 placeholder | 0 |

重新讀取發布設定，確認 Post ID、五個 Topics、訂閱通知設定、預覽標題、封面識別碼與原圖尺寸、排程均與更新前一致。預覽摘要同步將三部曲終篇改為四部曲第三篇，與本篇新版 TL;DR 一致；其餘發布設定保留。
封面維持 `diagram-02.png`（`1*R6TYJinsdAM_d3U30wrV6Q.png`）。文章仍排定於 **2026-10-29（四）09:00 GMT+8** 發布；本次沒有重新排程或提前發布。

## 第四篇排程後的導覽同步（2026-09-25）

第四篇已接續排定中文 2026-11-03、英文 2026-11-05，皆為 09:00 GMT+8。本篇將其導覽改為「coming soon」，並移除內文的未排程說明；仍以篇名指引讀者，待第四篇實際上線後再回填連結。

更新後從新分頁讀回，159 個文字區塊、25 個連結、7 張圖片、10 條分隔線皆與貼稿相符；連結順序與目的地、圖片槽位與識別碼也逐項核對。再次讀取發布設定，確認本篇原排程、Post ID、封面、Topics、預覽文字與通知設定均未改動。

## Concept and narrative polish synchronized (2026-10-03)

The author's requested pass covers the overview and all four parts in Chinese and English. It introduces important concepts through concrete examples and strengthens the progression from each article's question through its sections and paragraphs, including the later measurement, approval and handoff discussions. Research figures, code, diagrams, tables and source links are preserved.

The existing scheduled draft was updated under the same Post ID. After saving, independent fresh navigation verified **160 text blocks, 25 links, 7 original images and 10 dividers** against the final publishing payload, with no image placeholders. Link destinations and order, image identifiers and positions all match.

A further fresh settings read confirmed that the title, cover identifier and dimensions, topics, preview title and subtitle, notification setting and publication schedule exactly match the pre-update baseline. `isPublished: false`; the future schedule remains `2026-10-29T01:00:00Z`. The update did not publish the story early.

## 2026-10-18 發布進度與程式碼連結時點

依作者指定，正文與參考資料暫不連到付款程式碼，並註明待第四篇〈付款實作篇〉發布後提供。情境、實測說明與系列導覽保留；原稿、貼稿與既有草稿同步。

儲存後另開編輯頁逐塊比對：160 個文字區塊、23 個連結、7 張圖、10 條分隔線全部相符；連結目的地與順序一致，付款程式碼連結為 0，圖片識別碼與順序保留。

發布設定另從新分頁讀回，與修改前完全相同：仍為 `isPublished: false`；排程 **2026-10-29 09:00 Asia/Taipei**（`publishAt: 1793235600000`）。標題、Topics、封面、預覽文字與通知設定均保留，沒有重新排程。

## Publication-readiness polish synchronized (2026-10-24)

Clarified independent attempts, cohort denominators, per-PR requirements, numerical reliability targets and the staffing implications of sampling. The report example and ending now explain the remaining evidence and decisions. The source, generated paste and changed figures are synchronized; rationale and review limits are recorded in the [research note](../../../research/2026-10/reliability-payment-polish-evidence.md).

After saving under the same Post ID, fresh editor navigation verified **169 text blocks, 23 links, 7 figures and 10 dividers** against the final payload. Ordered text, link destinations, figure positions, image IDs and dimensions match; no image placeholders remain.

Replaced diagram-01, diagram-02 and table-02 with the revised English images. The cover remains diagram-02, now `1*3BkCssQJxK2HMOF195J5zQ.png` (1486×1136); the other four image identities and dimensions are unchanged. A further fresh settings read confirmed the title, topics, display title/subtitle, notification setting and original schedule. The post remains unpublished and scheduled for **2026-10-29 09:00 Asia/Taipei** (`publishAt: 1793235600000`).

Payment-code links remain absent until this language’s Part 4 actually publishes. No early publication or rescheduling was performed.

## 2026-10-26 重灌與讀回

Claude Code 接手複核後修訂原稿與貼稿（見[研究紀錄](../../../research/2026-10/reliability-payment-polish-evidence.md)的 2026-10-25／26 小節）。作者允許重開 gstack browse daemon 後，先以 `research/scripts/render_images.sh 2026-10-green-reliability en` 重繪整包七張圖（全部通過 MERMAID.md 檢查，`diagram-04` 長寬比 1.44），再以 `./tools/medium_draft.sh 2026-10-green-reliability en --post 4b6d147bff0d` 重灌，未加 `--reuse-figures`。

儲存後重新讀回：**169 個文字區塊、23 個連結、7 張圖、10 條分隔線**均與貼稿相符，placeholder 為 0。七張圖全部重傳；Medium 以內容定址，位元組不變的三張保留原識別碼（`table-01` `1*roevPNsK7WGH3pLAxeacQQ`、`diagram-03` `1*U6DRJpDZC58Fc04m1dTEmQ`、`table-03` `1*duxy4SJVec7HPM3jrn8JQQ`），重繪後位元組改變的四張取得新識別碼：`diagram-01` `1*aoQkc56_RaP6I9LFRlriHA`（664×604）、`table-02` `1*F6zXX1lFnCCsR5Bymoor0g`（1800×586）、`diagram-02` `1*npPKf73a1qhAQ0JmQ2PKxg`（664×522）、`diagram-04` `1*Y3rm-y29DbOSYnxI59p7TQ`（664×934）。

重灌把封面重設成第一張圖 `table-01`；`UpdateSubmitFormStoryPreviewMetadataMutation` 回 `500 throughput exceeded`，改走 `/p/<id>/edit` 右上角選單的 Change featured image 選回新版 `diagram-02.png`，重新載入 `/submission` 讀回 `previewImage.id = 1*npPKf73a1qhAQ0JmQ2PKxg.png`（664×522）。標題、預覽摘要、五個 Topics、通知設定與排程均與重灌前相同：`isPublished: false`，`publishAt: 1793235600000`（2026-10-29 09:00 Asia/Taipei）。重灌前後的設定與圖片識別碼快照存於本機 `.context/ship-2026-10-26b/`，未納入 git。

## 2026-10-26 第二次重灌：圖片解析度修正

同日 /ship 的 Red Team 審查從 PNG 檔頭看出，上一節重繪的四張圖都只有 664 px 寬：`research/scripts/mermaid_check.sh` 拿掉 mermaid 的 `max-width` 之後，`width="100%"` 的 svg 在 inline-block 容器裡退回瀏覽器預設的 300 CSS px，截圖只有 viewBox 一半的解析度，而 viewBox 的尺寸檢查照樣 PASS。10/24 的 `diagram-01`、`diagram-02` 是以別的方法算繪的完整尺寸（1266×1136、1486×1136），所以上一節的重灌把封面從 1486×1136 換成了 664×522。腳本修正（截圖前把 svg 設成 viewBox 的尺寸，並核對 `#wrap` 與 PNG 的寬度，對不上就 FAIL）後重繪整包：四張圖全部成為 2 × viewBox 的尺寸，三張表位元組不變；再以 `./tools/medium_draft.sh 2026-10-green-reliability en --post 4b6d147bff0d` 重灌（未加 `--reuse-figures`），台北時間 11:51–11:53。

儲存後重新讀回：**169 個文字區塊、23 個連結、7 張圖、10 條分隔線**均與貼稿相符，placeholder 為 0。三張表保留原識別碼（`table-01` `1*roevPNsK7WGH3pLAxeacQQ`、`table-02` `1*F6zXX1lFnCCsR5Bymoor0g`、`table-03` `1*duxy4SJVec7HPM3jrn8JQQ`）；四張圖取得新識別碼：`diagram-01` `1*Xcjm6k61CPCI9f3qoozd6A`（1266×1136）、`diagram-02` `1*7Mq2-4lNefvJNHjuu8jpLQ`（1486×1136）、`diagram-03` `1*IW9b7m37dmObDlqkES8z4g`（1596×1424）、`diagram-04` `1*yfQEjw1wOWyB3tNCZo7WQg`（1374×1952）。上一節的四個 664 px 識別碼已不在內文裡。

重灌仍把封面重設成第一張圖 `table-01`，依上一節的方法從 `/p/<id>/edit` 的 Change featured image 選回新版 `diagram-02.png`，重新載入 `/submission` 讀回 `previewImage.id = 1*7Mq2-4lNefvJNHjuu8jpLQ.png`（1486×1136）。標題、預覽摘要、五個 Topics、通知設定與排程均未改變：`isPublished: false`，`publishAt: 1793235600000`（2026-10-29 09:00 Asia/Taipei）。這次重灌的貼稿 `medium-paste.md` SHA-256 為 `d6b9621e5b6c70e846ee0e644794224d311fb2fb25028930cd491dc001456b9e`；重灌前後快照存於本機 `.context/ship-2026-10-26c/`，未納入 git。
