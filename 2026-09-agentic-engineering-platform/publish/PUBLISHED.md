# 發布紀錄

**網址** https://fantasybz.medium.com/別急著打造你的-devin-agentic-engineering-的組織策略與-90-天行動藍圖-7342ababc417

**Post ID** `7342ababc417`
**發布日** 2026-09-01
**發布方式** `./tools/medium_draft.sh 2026-09-agentic-engineering-platform`（見 [PUBLISHING.md](../../PUBLISHING.md)）

## 設定

| 項目 | 值 |
|---|---|
| Topics | AI、Software Engineering、Engineering Management、Agentic Ai、DevOps |
| 封面圖 | `diagram-04.png`（Platform + Federation 組織圖） |
| Notify subscribers | 是 |
| 發布位置 | 個人 profile，未投稿 publication |

Topics 原本填 `Agentic AI`，Medium 正規化成 `Agentic Ai`。
封面圖 Medium 原本自動選了 `table-01.png`，改掉是因為表格截圖縮到卡片尺寸後看不清楚。

## 上線後核對

| 項目 | 數量 |
|---|---|
| 內文區塊（與轉換後 payload 逐塊比對） | 120，零差異 |
| 插圖 | 14，位置與 📌 標記一致 |
| 章節標題 / 小標 | 12 / 9 |
| 引言 / 列表項 / code block | 9 / 29 / 2 |
| 內文連結 | 17 |
| 閱讀時間 | 18 min read |

`<path>`、`<snake_case>` 這類角括號在 code block 裡都完整保留。
唯一被 Medium 改掉的是 21 處 `——` 被加上 hair space，屬於它的排版慣例。

---

## ⚠️ 待同步到線上版（發布後才做的修正）

本篇發布之後，為了與後來產出的三部曲對齊，`article.md` 又改了六處。線上版目前仍是舊內容，
**其中第 1 項會讓這篇成為沒有出口的孤兒文章**。工具只能建新草稿，這些要在 Medium 編輯器裡手動改。

| # | 位置 | 要做的事 |
|---|---|---|
| 1 | 文末（結語之後、References 之前） | 整段新增「系列文章」清單——線上版完全沒有，讀者無從得知有三部曲。三篇的 Medium URL 要等它們發布後填入 |
| 2 | TL;DR 之後 | 新增一行「系列導覽」（與三部曲三篇同格式），連結同上 |
| 3 | 第五節 規模建議表（`table-04.png`） | 重新上傳圖片。30–100 人那列已改為「仍不編專職…champions 過載才開 2–4 人的 Enablement Pod」（原本與組織篇矛盾）；>500 人那列補上「（8–12 人起跳）」 |
| 4 | 第五節 「即使超過 500 人…」段末 | 句尾接上指向組織篇的一句話 |
| 5 | 第六節 「一段具體的 AGENTS.md」 | 整個小節換成新版「AGENTS.md：寫對與寫錯的差別」（標題、引言、code block、新增的一段說明都變了）。原本的 code block 與技術篇逐字相同，改成好壞對照 |
| 6 | 文末小標 | 「本系列文章」→「系列文章」 |
| 7 | 文末（系列文章之後、署名那行之前） | 新增「AI 協作說明」小節——線上版沒有 |
| 8 | 第七節的流程圖（`diagram-07.png`） | 重新上傳。原圖 612×3960（1:6.5 直條）在文章裡難以閱讀，已重畫為 1198×1588 |
| 9 | 第八節的 Buy / Build 圖（`diagram-08.png`） | 重新上傳。原圖 1568×78（20:1 細條，字會縮到看不見）已重畫為 810×1044 |

最新內容一律以 `article.md` 為準；`medium-paste.md` 已同步重新產生。
