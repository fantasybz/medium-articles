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
| 內文區塊（與轉換後 payload 逐塊比對） | 60，零差異 |
| 插圖 | 7，位置與 📌 標記一致 |
| 章節標題 / 小標 | 8 / 4 |
| 引言 / 列表項 / code block | 4 / 19 / 0 |
| 內文連結 | 8 |
| 閱讀時間 | 8 min read |

---

## ⚠️ 還差的：三部曲後兩篇的連結

發布時三部曲的另外兩篇尚未發表——Medium 限制同一作者 24 小時內最多發布或排程 2 篇，
總論與本篇已用掉配額（排程一樣被擋，細節見 [PUBLISHING.md](../../PUBLISHING.md) 的
〈發文數量上限〉）。

本篇發布當下，指向技術篇與營運篇的 4 處連結還是 GitHub 相對路徑，在 Medium 上會 404。
2026-09-02 已改成純文字並標「（即將發布）」，線上版目前沒有死連結。等那兩篇上線後
要換成真正的 Medium URL（用 `tools/medium_patch.py`）：

| 位置 | 現況 | 之後要改成 |
|---|---|---|
| 開頭「系列導覽」 | `二、技術篇（即將發布）` | 連到技術篇的 Medium URL |
| 開頭「系列導覽」 | `三、營運篇（即將發布）` | 連到營運篇的 Medium URL |
| 文末「系列文章」第 3 項 | 純文字，句尾「（即將發布）」 | 連到技術篇，並拿掉「（即將發布）」 |
| 文末「系列文章」第 4 項 | 純文字，句尾「（即將發布）」 | 連到營運篇，並拿掉「（即將發布）」 |

指向總論的 3 處連結在發布前就已填入真正的 Medium URL，不需要再改。
2026-09-02 另外補上了文末的「AI 協作說明」小節（發布時的版本沒有），
並把 15 處破折號 `——` 改成單個 `—`（本篇沒有 code block 用到破折號）——Medium 會在每個 em dash 兩側加
hair space，`——` 上線後會裂成 `— —`。
改完逐塊比對過：62 個文字區塊全數相符、4 個連結全在、7 張圖各在原位。

最新內容一律以 `article.md` 為準。它目前有 3 處指向總論的 Medium URL、
4 處指向技術篇與營運篇的 GitHub 相對路徑，與線上版一致；那 4 處要等兩篇發布後才填得進去。
