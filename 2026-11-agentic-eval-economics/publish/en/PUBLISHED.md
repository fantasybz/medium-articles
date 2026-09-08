# 發布紀錄（英文版）

**網址** https://fantasybz.medium.com/agentic-engineering-part-3-evals-unit-economics-and-scaling-running-agents-like-a-product-1cb1855a2046

**Post ID** `1cb1855a2046`
**發布日** 2026-09-05（09:40 GMT+8）
**建立方式** `./tools/medium_draft.sh 2026-11-agentic-eval-economics en`

系列最後一篇。EN Part 1 於 09-05 08:26 滾出 24 小時視窗，空出名額後就發了。
只按 Publish，沒有重建草稿，Post ID 與網址沿用草稿。

## 設定

| 項目 | 值 |
|---|---|
| Topics | AI、Software Engineering、Engineering Management、Agentic Ai、DevOps |
| 封面圖 | `diagram-02.png`（Effective Engineering Leverage 指標樹）|
| Notify subscribers | 是 |

三張 diagram 都是很寬的橫幅（1568×234／266／242），`diagram-02` 最高、縮成卡片後
字級最大，跟中文版營運篇選同一張。

## 上線後核對

| 項目 | 數量 |
|---|---|
| 內文區塊（與轉換後 payload 逐塊比對） | 64，零差異 |
| 插圖 | 7（3 張 diagram + 4 張 table），位置與 📌 標記一致 |
| 內文連結 | 11 |
| 死連結 | 0 |
| 空段 | 0 |
| 「(coming soon)」 | 0 |

**一上線就是完整的**：三篇姊妹作都已先發布，草稿裡的連結在發布前就全部補好了，
所以沒有短暫的佔位期。

## 連結狀態：系列完成

發布後回頭把指向本篇的連結補進另外三篇英文版與中文版營運篇：

| 篇 | 補在哪 |
|---|---|
| EN Overview `8187e7ec80f9` | 開頭 `Series:` 那行、文末 `The series` 清單 |
| EN Part 1 `92343384d987` | 同上 |
| EN Part 2 `3facc281f633` | 同上 |
| 中文版營運篇 `d6d9623c2dc6` | 文末「英文版：English edition」|

補完之後八篇全部驗過：0 個「(coming soon)／（即將發布）」、0 死連結、
0 裂開的破折號，圖數不變，中英雙向互連。

最新內容以 `article.en.md` 為準；`publish/en/medium-paste.md` 由它產生。

## 口吻潤稿重灌（2026-09-08）

以 `./tools/medium_draft.sh 2026-11-agentic-eval-economics en --post 1cb1855a2046 --reuse-figures` 就地重灌，
Post ID 不變。`--reuse-figures` 直接沿用這篇已發布版本上的圖（貼 CDN 網址），
完全不重新上傳——重新上傳會讓存檔寫不完，是這一輪最初把草稿弄壞的原因。
封面圖與 topics 因此都不受影響。

重載後從伺服器讀回來驗證通過：91 個文字區塊逐塊相符、11 個連結全在、
7 張圖各在自己的槽位、無殘留 placeholder。

**還沒上線。** 這篇已發布，改動只存在「已發布版本背後的草稿」裡，讀者看到的
仍是舊版。要讓潤稿生效，必須在編輯器按 **Save and publish**
（`postPublishedType=repub`：網址不變、不會重寄訂閱信）。

### 已發布（2026-09-08）

在編輯器按下 **Save and publish**，潤稿正式上線。網址與 Post ID 不變
（`postPublishedType=repub`，不會重寄訂閱信）。

發布前後各驗一次：草稿 98 個 graf、7 張圖、無殘留 placeholder；
發布後線上頁面 7 張圖、無殘留、內文長度 16068 字元。
