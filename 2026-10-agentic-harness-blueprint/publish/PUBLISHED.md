# 發布紀錄

**狀態** 草稿（尚未發布，也**沒有設排程**）

**發布佇列順位** 第 1 位（中文三部曲先收完；完整佇列見 ../../PUBLISHING.md 的〈目前的發布佇列〉）

**草稿網址** https://medium.com/p/f2a139f5b561/edit
**Post ID** `f2a139f5b561`
**建立日** 2026-09-02
**建立方式** `./tools/medium_draft.sh 2026-10-agentic-harness-blueprint`（見 [PUBLISHING.md](../../PUBLISHING.md)）

## 為什麼還沒發布

Medium 限制同一作者 **24 小時內最多發布或排程 2 篇**，總論與組織篇已用掉配額。
排程不是繞道——把日期改成隔天再按 Schedule to publish，一樣被同一個計數器擋下來
（實測，見 [PUBLISHING.md](../../PUBLISHING.md) 的〈發文數量上限〉）。
所以這篇目前是純草稿，Scheduled 分頁是空的。

## 已設定好的（發布時不用再弄）

| 項目 | 值 |
|---|---|
| Topics | AI、Software Engineering、Engineering Management、Agentic Ai、DevOps |
| 封面圖 | `diagram-01.png`（五層 harness 藍圖；近正方形，縮成卡片仍讀得清楚） |
| Notify subscribers | 是（預設） |
| 發布位置 | 個人 profile，未投稿 publication |

## 草稿內容核對

| 項目 | 數量 |
|---|---|
| 內文區塊（與轉換後 payload 逐塊比對） | 67，零差異 |
| 插圖 | 7，位置與 📌 標記一致 |
| 章節標題 / 小標 | 8 / 4 |
| 引言 / 列表項 / code block | 2 / 15 / 4 |
| 內文連結 | 8 |

已包含文末的「AI 協作說明」小節。

2026-09-02 把內文 20 處破折號 `——` 改成單個 `—`，**標題也在內**（code block 內的 2 處保留 `——`）
（`Harness 藍圖——把系統變成 agent 讀得懂的地方`
→ `Harness 藍圖—把系統變成 agent 讀得懂的地方`）。Medium 會在每個 em dash 兩側加 hair space，`——` 上線後會裂成 `— —`。
標題是草稿才改得起——已發布文章的網址 slug 在發布當下就固定了。

---

## ⚠️ 發布時要記得

1. **只按 Publish，不要重建草稿**。重建會換掉 Post ID 與網址。
2. 發布後把網址補進本檔與 [README.md](../../README.md) 的索引。
3. 本篇指向營運篇的 2 處連結目前是純文字加「（即將發布）」——營運篇上線後
   要換成真正的 Medium URL（用 `tools/medium_patch.py`）：

| 位置 | 現況 | 之後要改成 |
|---|---|---|
| 開頭「系列導覽」 | `三、營運篇（即將發布）` | 連到營運篇的 Medium URL |
| 文末「系列文章」第 4 項 | 純文字，句尾「（即將發布）」 | 連到營運篇，並拿掉「（即將發布）」 |

指向總論與組織篇的 4 處連結在建草稿前就已填入真正的 Medium URL。
最新內容一律以 `article.md` 為準。
