# 發布紀錄

**網址** https://fantasybz.medium.com/agentic-engineering-三部曲-一-誰來做-platform-federation-的組織設計實務-9d9353ef7f3a

**Post ID** `9d9353ef7f3a`
**發布日** 2026-09-02
**發布方式** `./tools/medium_draft.sh 2026-09-agentic-org-design`（見 [PUBLISHING.md](../../PUBLISHING.md)）

## 設定

| 項目 | 值 |
|---|---|
| Topics | AI、Software Engineering、Engineering Management、Agentic Ai、DevOps |
| 封面圖 | `diagram-02.png`（Platform Team 編制圖） |
| Notify subscribers | 是 |
| 發布位置 | 個人 profile，未投稿 publication |

Topics 原本填 `Agentic AI`，Medium 正規化成 `Agentic Ai`。
封面圖 Medium 原本自動選了第一張 `diagram-01.png`，改掉是因為它是 1568×312 的寬圖，
縮到卡片尺寸後字會糊掉；`diagram-02.png` 的長寬比與字級都撐得住。

## 上線後核對

| 項目 | 數量 |
|---|---|
| 內文區塊（與轉換後 payload 逐塊比對） | 發布時 60；現為 62（後續加了 AI 協作說明），零差異 |
| 插圖 | 7，位置與 📌 標記一致 |
| 章節標題 / 小標 | 8 / 4 |
| 引言 / 列表項 / code block | 4 / 19 / 0 |
| 內文連結 | 發布時 4；現為 9（技術篇、營運篇、英文版陸續補上）|
| 閱讀時間 | 8 min read |

---

## 系列連結：已完成

2026-09-03 營運篇上線後，中文三部曲四篇彼此的系列連結全部補成真正的 Medium URL，
線上版與 repo 原始檔一致。四篇線上都驗過：0 死連結、0 殘留「（即將發布）」、
0 裂開的破折號，圖數不變。

中英互連也完成了：2026-09-04 英文版上線後，本篇文末已加上「英文版：English edition」的連結，英文版也回連本篇。

## 口吻潤稿重灌（2026-09-08）

以 `./tools/medium_draft.sh 2026-09-agentic-org-design --post 9d9353ef7f3a --reuse-figures` 就地重灌，
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
發布後線上頁面 7 張圖、無殘留、內文長度 6794 字元。
