# 發布紀錄

**標題** 總論：綠燈不是驗收—agent 時代的測試、Review 與可靠度
**Post ID** `582f24223eea`（草稿／排程網址 https://medium.com/p/582f24223eea/edit；上線後的穩定短網址 https://medium.com/p/582f24223eea）
**排程** 2026-10-06（一）09:00 GMT+8（尚待作者確認；2026-09-07 以 Publish 對話框的 Schedule for later 設定，見下方狀態）
**建立方式** `./tools/medium_draft.sh 2026-10-green-overview`，逐塊比對零差異（見 [PUBLISHING.md](../../PUBLISHING.md)）

## 設定

| 項目 | 值 |
|---|---|
| Topics | Software Testing、Code Review、AI、Software Engineering、Engineering Management |
| 封面圖 | Medium 預設第一張 figure（`diagram-01.png`，是圖不是表格，未改） |
| Notify subscribers | 是（預設） |
| 發布位置 | 個人 profile，未投稿 publication |

## 狀態（2026-09-07）

- [x] 排程完成：2026-09-07 18:12 設定，Stories 頁 Scheduled 清單顯示 Oct 6, 1:00 AM（UTC，即 09:00 GMT+8）；同一篇多出來的重複草稿 `3e2b234fd2e7` 已刪除
- 系列連結：本篇連到「發布時已上線」的篇；其餘保留「（即將發布）」，上線後用 `medium_patch.py subst` 回填（見 PUBLISHING.md〈目前的發布佇列〉）
- 英文版：`publish/en/PUBLISHED.md`（Post ID `c4fc9f3d8581`，排程 2026-10-08（三）09:00）

## 上線後核對（發布後填）

| 項目 | 數量 |
|---|---|
| 內文區塊（與轉換後 payload 逐塊比對） | 建草稿時零差異 |
| 插圖 | 見 `publish/figures.json` |
| 死連結 / 殘留「（即將發布）」/ 裂開的破折號 | 上線後檢查 |

## 口吻潤稿重灌（2026-09-08）

以 `./tools/medium_draft.sh 2026-10-green-overview --post 582f24223eea` 就地重灌，Post ID 不變。
重載後從伺服器讀回來驗證通過：193 個文字區塊逐塊相符、28 個連結全在、
18 張圖各在自己的槽位、無殘留 placeholder。

**排程未受影響**：重灌後 Stories → Scheduled 仍列 Oct 6, 1:00 AM (UTC)，與原排程相同。

待人工確認：封面圖（所有 figure 都重傳過，Medium 可能改用第一張當預覽圖）。

## 通順度潤稿重灌（2026-09-18）

以 `./tools/medium_draft.sh 2026-10-green-overview --post 582f24223eea` 就地重灌，Post ID 不變。
內容變更：術語首見補白話、段落接縫、開場路線圖句與結語收束、AGNTCon／書的插入段改寫成
「場景鋪陳 + 證據與收攏」並搬位；作者另裁示四處（書的限制句移位、READY 數字降括號、
感謝 Teddy 那行移到節尾紀律句之後、約束（constraint）與意圖（intent）首見配對）。
`verify_draft.py` 閘門通過（exit 0）。

**排程未受影響**：重灌後 Stories → Scheduled 仍列 Oct 6, 1:00 AM (UTC)。八篇的時段與 Post ID 全部不變（第三次量到）。
**Topics 未受影響**（Review 篇 zh 的面板實際看過，五個都在）。
**封面圖被重設，已還原**：八篇八張全部被 Medium 換成內文第一張 figure；重灌前先把八張封面的
CDN hash 記進 `.context/cover-check/baseline-2026-09-18.json`（與 2026-09-16 那份逐項相同，
表示上一輪的還原守住了），還原後回 Stories → Scheduled 核對，八篇的卡片縮圖都回到 `1*q2k7_AHpOTz2bU-HpP9ioA.png`。

這一輪學到的：頁內選擇器**仍然列著原始那張的 hash**，所以還原可以用 hash 精準配對，
不必像 2026-09-16 那樣靠算繪高度猜；縮圖本身被裁成 248×248，長寬比不能當判準，
要比就回 CDN 取原圖尺寸。

### 2026-09-18 追加一句（payment 說明）後重灌

第一節補一句「payment 不是術語，是個例子」之後，總論兩篇再各重灌一次
（`--post 582f24223eea` / `--post c4fc9f3d8581`），`verify_draft.py` 都過。
封面同樣被重設，同樣用頁內選擇器點回原本那張；排程 10/06 與 10/08 未動。
其餘六篇這一輪沒有內容變更，沒有重灌。
