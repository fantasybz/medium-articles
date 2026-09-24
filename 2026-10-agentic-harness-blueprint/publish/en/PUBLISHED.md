# 發布紀錄（英文版）

**網址** https://fantasybz.medium.com/agentic-engineering-part-2-the-harness-blueprint-making-your-system-legible-to-agents-3facc281f633

**Post ID** `3facc281f633`
**發布日** 2026-09-04（23:52 GMT+8）
**建立方式** `./tools/medium_draft.sh 2026-10-agentic-harness-blueprint en`

草稿是 2026-09-02 建的，等了兩天才發：Medium 限制同一作者在滾動 24 小時內最多
2 篇「已發布或已排程」，排程也吃同一個計數器。EN Overview 於 09-04 23:32 滾出
窗外，才空出位子。發布時只按 Publish，沒有重建草稿，所以 Post ID 與網址沿用草稿。

## 設定

| 項目 | 值 |
|---|---|
| Topics | AI、Software Engineering、Engineering Management、Agentic Ai、DevOps |
| 封面圖 | `diagram-01.png`（five-layer harness blueprint；近正方形，縮成卡片仍讀得清楚）|
| Notify subscribers | 是 |

Topics 在建草稿時就設好了，發布當下五個 chip 都還在，不必重設。封面與中文版技術篇
選同一張，兩個語版的卡片看起來是一組。

## 上線後核對

| 項目 | 數量 |
|---|---|
| 內文區塊（與轉換後 payload 逐塊比對） | 67，零差異 |
| 插圖 | 7（3 張 diagram + 4 張 table），位置與 📌 標記一致 |
| 內文連結 | 11（發布時 9；Part 3 +2）|
| 死連結 | 0 |
| 空段 | 0 |

發布前後段落數都是 74，沒有掉塊。

## 連結狀態

發布時已帶著指向 EN Overview、EN Part 1 與中文版技術篇的連結。發布後回頭補上
指向本篇的連結：

| 篇 | 補在哪 |
|---|---|
| EN Overview `8187e7ec80f9` | 開頭 `Series:` 那行、文末 `The series` 清單 |
| EN Part 1 `92343384d987` | 同上 |
| EN Part 3 草稿 `1cb1855a2046` | 同上（草稿裡先補好，發布時就是完整的）|
| 中文版技術篇 `f2a139f5b561` | 文末「英文版：English edition」|

EN Part 3 於 2026-09-05 09:40 上線後，本篇裡指向它的 2 處也換成真正的連結，
「(coming soon)」歸零。英文四篇的系列連結至此全部收乾淨。

最新內容以 `article.en.md` 為準；`publish/en/medium-paste.md` 由它產生。

## 口吻潤稿重灌（2026-09-08）

以 `./tools/medium_draft.sh 2026-10-agentic-harness-blueprint en --post 3facc281f633 --reuse-figures` 就地重灌，
Post ID 不變。`--reuse-figures` 直接沿用這篇已發布版本上的圖（貼 CDN 網址），
完全不重新上傳——重新上傳會讓存檔寫不完，是這一輪最初把草稿弄壞的原因。
封面圖與 topics 因此都不受影響。

重載後從伺服器讀回來驗證通過：94 個文字區塊逐塊相符、11 個連結全在、
7 張圖各在自己的槽位、無殘留 placeholder。

**還沒上線。** 這篇已發布，改動只存在「已發布版本背後的草稿」裡，讀者看到的
仍是舊版。要讓潤稿生效，必須在編輯器按 **Save and publish**
（`postPublishedType=repub`：網址不變、不會重寄訂閱信）。

### 已發布（2026-09-08）

在編輯器按下 **Save and publish**，潤稿正式上線。網址與 Post ID 不變
（`postPublishedType=repub`，不會重寄訂閱信）。

發布前後各驗一次：草稿 101 個 graf、7 張圖、無殘留 placeholder；
發布後線上頁面 7 張圖、無殘留、內文長度 19216 字元。

## 全文精修與重新發布（2026-09-25）

依目前的文字風格標準逐篇、逐句精修，補全動作與受詞、段落承接及後半部的解釋，並以可辨識的文章名稱或主題指引跨篇閱讀。同步釐清團隊規模與責任、量測指標的分母、成本假設、eval 限制及擴大使用的審查條件；中英文保留相同語意。

**重新發布時間**：2026-09-25 00:33 GMT+8。更新原有 Post ID `3facc281f633`，網址與首次發布日期不變。

上傳 4 張有內容變更的圖表後，以已驗證的 CDN 對應填入完整內文；另 3 張沿用原有線上圖片。存檔穩定後另開編輯器讀回，再按 **Save and publish** 更新已發布版本。最後另開公開頁面，比對實際呈現文字與 Medium 儲存內容：

| 核對項目 | 結果 |
|---|---|
| 文字區塊 | 94，逐塊相符 |
| 內文連結 | 11，目的地逐一相符（相對網址還原後比對） |
| 圖片 | 7，身分、順序與段落位置相符；公開頁面皆已載入 |
| 章節分隔 | 12，數量相符 |
| 程式碼區塊 | 4，內容與換行、縮排相符 |
| 殘留 IMGSLOT | 0 |
| 封面圖 | `diagram-01.png`；Medium ID `0*3y2jtYSQijlS6bao.png` |
| 既有設定 | 5 個 topics、PUBLIC、未鎖定付費、個人 profile 均維持原設定 |

封面維持本檔指定的圖片，並從新的公開頁面確認封面 ID。
