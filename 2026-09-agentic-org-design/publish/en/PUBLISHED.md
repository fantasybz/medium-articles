# 發布紀錄（英文版）

**網址** https://fantasybz.medium.com/agentic-engineering-part-1-who-does-this-platform-plus-federation-in-practice-92343384d987

**Post ID** `92343384d987`
**發布日** 2026-09-04（08:26 GMT+8）
**建立方式** `./tools/medium_draft.sh 2026-09-agentic-org-design en`

## 設定

| 項目 | 值 |
|---|---|
| Topics | AI、Software Engineering、Engineering Management、Agentic Ai、DevOps |
| 封面圖 | `diagram-02.png`（Platform Team org chart） |
| Notify subscribers | 是 |

## 上線後核對

| 項目 | 數量 |
|---|---|
| 內文區塊（與轉換後 payload 逐塊比對） | 62，零差異 |
| 插圖 | 7，位置與 📌 標記一致 |
| 內文連結 | 9（發布時 5；Part 2 +2、Part 3 +2）|
| 死連結 | 0 |

發布時已帶著指向 EN Overview 與中文版組織篇的連結；中文版組織篇也已回連本篇。

---

## 系列連結：已完成

2026-09-05 EN Part 3 上線後，英文四篇彼此的系列連結全部補成真正的 Medium URL，
中英也雙向互連。八篇線上都驗過：0 個「(coming soon)」、0 死連結、圖數不變。

## 口吻潤稿重灌（2026-09-08）

以 `./tools/medium_draft.sh 2026-09-agentic-org-design en --post 92343384d987 --reuse-figures` 就地重灌，
Post ID 不變。`--reuse-figures` 直接沿用這篇已發布版本上的圖（貼 CDN 網址），
完全不重新上傳——重新上傳會讓存檔寫不完，是這一輪最初把草稿弄壞的原因。
封面圖與 topics 因此都不受影響。

重載後從伺服器讀回來驗證通過：83 個文字區塊逐塊相符、9 個連結全在、
7 張圖各在自己的槽位、無殘留 placeholder。

**還沒上線。** 這篇已發布，改動只存在「已發布版本背後的草稿」裡，讀者看到的
仍是舊版。要讓潤稿生效，必須在編輯器按 **Save and publish**
（`postPublishedType=repub`：網址不變、不會重寄訂閱信）。

### 已發布（2026-09-08）

在編輯器按下 **Save and publish**，潤稿正式上線。網址與 Post ID 不變
（`postPublishedType=repub`，不會重寄訂閱信）。

發布前後各驗一次：草稿 90 個 graf、7 張圖、無殘留 placeholder；
發布後線上頁面 7 張圖、無殘留、內文長度 15896 字元。

## 全文精修與重新發布（2026-09-25）

依目前的文字風格標準逐篇、逐句精修，補全動作與受詞、段落承接及後半部的解釋，並以可辨識的文章名稱或主題指引跨篇閱讀。同步釐清團隊規模與責任、量測指標的分母、成本假設、eval 限制及擴大使用的審查條件；中英文保留相同語意。

**重新發布時間**：2026-09-25 00:23 GMT+8。更新原有 Post ID `92343384d987`，網址與首次發布日期不變。

上傳 4 張有內容變更的圖表後，以已驗證的 CDN 對應填入完整內文；另 3 張沿用原有線上圖片。存檔穩定後另開編輯器讀回，再按 **Save and publish** 更新已發布版本。最後另開公開頁面，比對實際呈現文字與 Medium 儲存內容：

| 核對項目 | 結果 |
|---|---|
| 文字區塊 | 83，逐塊相符 |
| 內文連結 | 9，目的地逐一相符（相對網址還原後比對） |
| 圖片 | 7，身分、順序與段落位置相符；公開頁面皆已載入 |
| 章節分隔 | 11，數量相符 |
| 程式碼區塊 | 0，本篇無程式碼區塊 |
| 殘留 IMGSLOT | 0 |
| 封面圖 | `diagram-02.png`；Medium ID `0*NMkUvcGnsJZ_KD4g.png` |
| 既有設定 | 5 個 topics、PUBLIC、未鎖定付費、個人 profile 均維持原設定 |

更新前實際線上封面為 `diagram-01.png`，與本檔指定封面不符。本次透過編輯器 **Change featured image → Done** 恢復 `diagram-02.png`，並從新的公開頁面確認封面 ID。
