# 發布紀錄

**狀態** 草稿（尚未發布，也**沒有設排程**）

**草稿網址** https://medium.com/p/d6d9623c2dc6/edit
**Post ID** `d6d9623c2dc6`
**建立日** 2026-09-02
**建立方式** `./tools/medium_draft.sh 2026-11-agentic-eval-economics`（見 [PUBLISHING.md](../../PUBLISHING.md)）

## 為什麼還沒發布

同技術篇：Medium 限制同一作者 **24 小時內最多發布或排程 2 篇**，總論與組織篇
已用掉配額，排程也被同一個計數器擋下（見 [PUBLISHING.md](../../PUBLISHING.md)
的〈發文數量上限〉）。Scheduled 分頁是空的。

依系列順序，這篇排在技術篇之後發。

## 已設定好的（發布時不用再弄）

| 項目 | 值 |
|---|---|
| Topics | AI、Software Engineering、Engineering Management、Agentic Ai、DevOps |
| 封面圖 | `diagram-02.png`（Effective Engineering Leverage 指標樹；字級最大） |
| Notify subscribers | 是（預設） |
| 發布位置 | 個人 profile，未投稿 publication |

## 草稿內容核對

| 項目 | 數量 |
|---|---|
| 內文區塊（與轉換後 payload 逐塊比對） | 64，零差異 |
| 插圖 | 7，位置與 📌 標記一致 |
| 章節標題 / 小標 | 7 / 10 |
| 引言 / 列表項 / code block | 3 / 21 / 1 |
| 內文連結 | 8 |

已包含文末的「AI 協作說明」小節。

2026-09-02 把全篇 17 處破折號 `——` 改成單個 `—`，**標題也在內**
（`Eval、單位經濟與規模化——把 agent 當產品營運`
→ `Eval、單位經濟與規模化—把 agent 當產品營運`）。Medium 會在每個 em dash 兩側加 hair space，`——` 上線後會裂成 `— —`。
標題是草稿才改得起——已發布文章的網址 slug 在發布當下就固定了。

---

## ⚠️ 發布時要記得

1. **只按 Publish，不要重建草稿**。重建會換掉 Post ID 與網址。
2. 發布後把網址補進本檔與 [README.md](../../README.md) 的索引。
3. 本篇指向技術篇的 2 處連結目前是純文字加「（即將發布）」。如果技術篇先發布，
   **建議在發布本篇之前**就把這兩處換成真正的 URL，這樣本篇一上線就是完整的：

| 位置 | 現況 | 之後要改成 |
|---|---|---|
| 開頭「系列導覽」 | `二、技術篇（即將發布）` | 連到技術篇的 Medium URL |
| 文末「系列文章」第 3 項 | 純文字，句尾「（即將發布）」 | 連到技術篇，並拿掉「（即將發布）」 |

指向總論與組織篇的 4 處連結在建草稿前就已填入真正的 Medium URL。
最新內容一律以 `article.md` 為準。
