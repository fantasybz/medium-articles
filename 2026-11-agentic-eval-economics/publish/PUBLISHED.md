# 發布紀錄

**網址** https://fantasybz.medium.com/agentic-engineering-三部曲-三-eval-單位經濟與規模化-把-agent-當產品營運-d6d9623c2dc6

**Post ID** `d6d9623c2dc6`
**發布日** 2026-09-03（01:16 GMT+8）
**發布方式** `./tools/medium_draft.sh 2026-11-agentic-eval-economics`（見 [PUBLISHING.md](../../PUBLISHING.md)）

## 設定

| 項目 | 值 |
|---|---|
| Topics | AI、Software Engineering、Engineering Management、Agentic Ai、DevOps |
| 封面圖 | `diagram-02.png`（Effective Engineering Leverage 指標樹；字級最大） |
| Notify subscribers | 是 |
| 發布位置 | 個人 profile，未投稿 publication |

## 上線後核對

| 項目 | 數量 |
|---|---|
| 內文區塊（與轉換後 payload 逐塊比對） | 64，零差異 |
| 插圖 | 7，位置與 📌 標記一致 |
| 內文連結 | 11（發布時 10；英文版 +1）|
| 死連結 / 殘留「（即將發布）」/ 裂開的破折號 | 0 / 0 / 0 |

**這篇是唯一一上線就完整的中文篇。** 指向總論、組織篇、技術篇的 6 處連結在按下
Publish 之前就全部補好了（技術篇 2026-09-02 發布後立刻補的），所以讀者從第一秒
看到的就是完整的系列導覽，沒有任何「（即將發布）」或死連結的空窗期。
這是 [PUBLISHING.md](../../PUBLISHING.md)〈把一個系列剩下的篇數發完〉第 4 點的作法。

中文三部曲到此收完：總論、組織篇、技術篇、營運篇四篇彼此的系列連結全部是真正的
Medium URL。

---

## 中英互連：已完成

2026-09-05 09:40 英文版上線（`1cb1855a2046`）後，本篇文末補上一行
「英文版：English edition」指向那一篇；英文版那側也帶著回連本篇的連結。
編輯既有 story、「Save and publish」送出，網址不變、不重寄訂閱信。
補完核對：段落 71、插圖 7、空段 0、死連結 0。

## 口吻潤稿重灌（2026-09-08）

以 `./tools/medium_draft.sh 2026-11-agentic-eval-economics --post d6d9623c2dc6 --reuse-figures` 就地重灌，
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
發布後線上頁面 7 張圖、無殘留、內文長度 7141 字元。

## 全文精修與重新發布（2026-09-25）

依目前的文字風格標準逐篇、逐句精修，補全動作與受詞、段落承接及後半部的解釋，並以可辨識的文章名稱或主題指引跨篇閱讀。同步釐清團隊規模與責任、量測指標的分母、成本假設、eval 限制及擴大使用的審查條件；中英文保留相同語意。

**重新發布時間**：2026-09-25 00:42 GMT+8。更新原有 Post ID `d6d9623c2dc6`，網址與首次發布日期不變。

上傳 5 張有內容變更的圖表後，以已驗證的 CDN 對應填入完整內文；另 2 張沿用原有線上圖片。存檔穩定後另開編輯器讀回，再按 **Save and publish** 更新已發布版本。最後另開公開頁面，比對實際呈現文字與 Medium 儲存內容：

| 核對項目 | 結果 |
|---|---|
| 文字區塊 | 92，逐塊相符 |
| 內文連結 | 12，目的地逐一相符（相對網址還原後比對） |
| 圖片 | 7，身分、順序與段落位置相符；公開頁面皆已載入 |
| 章節分隔 | 11，數量相符 |
| 程式碼區塊 | 1，內容與換行、縮排相符 |
| 殘留 IMGSLOT | 0 |
| 封面圖 | `diagram-02.png`；Medium ID `1*EP8dOSBtD3SHDsPO9nYgeg.png` |
| 既有設定 | 5 個 topics、PUBLIC、未鎖定付費、個人 profile 均維持原設定 |

更新前實際線上封面為 `diagram-01.png`，與本檔指定封面不符。本次透過編輯器 **Change featured image → Done** 恢復 `diagram-02.png`，並從新的公開頁面確認封面 ID。
