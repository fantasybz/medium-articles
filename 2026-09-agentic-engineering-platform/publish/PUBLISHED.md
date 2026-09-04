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
發布當下唯一被 Medium 改掉的是 em dash 被加上 hair space，屬於它的排版慣例；
後來連同破折號本身一起改了，見下面的同步紀錄第 8 項。

---

## 同步紀錄

發布後 `article.md` 又改了六處，2026-09-02 已全部同步到線上版（用
`tools/medium_patch.py`，見 [PUBLISHING.md](../../PUBLISHING.md) 的〈改已發布的文章〉）。
線上版逐塊比對過：130 個文字區塊全數相符、20 個連結全在、14 張圖各在原位。

| # | 位置 | 做了什麼 | 狀態 |
|---|---|---|---|
| 1 | 文末（結語之後、References 之前） | 新增「系列文章」清單（線上版原本完全沒有，這篇因此是孤兒文章） | ✅ |
| 2 | TL;DR 之後 | 新增「系列導覽」一行 | ✅ |
| 3 | 第五節 規模建議表 | 重新上傳 `table-04.png`（30–100 人那列改為「仍不編專職…champions 過載才開 2–4 人的 Enablement Pod」；>500 人那列補上「（8–12 人起跳）」） | ✅ |
| 4 | 第五節「即使超過 500 人…」段末 | 接上指向組織篇的一句話 | ✅ |
| 5 | 第六節 | 「一段具體的 AGENTS.md」整節換成「AGENTS.md：寫對與寫錯的差別」好壞對照版 | ✅ |
| 6 | 文末小標 | 「本系列文章」→「系列文章」 | ✅ |
| 7 | 文末（系列文章之後、署名那行之前） | 新增「AI 協作說明」小節 | ✅ |
| 8 | 全篇 | 內文的破折號 `——` 一律改成單個 `—`（24 處；code block 內的 2 處保留 `——`，Medium 不會在 `<pre>` 加 hair space，那裡不會裂）。Medium 會在每個 em dash 兩側加 hair space，`——` 上線後會裂成 `— —` | ✅ |

## ⚠️ 還差的：兩張圖要重新上傳

線上版的這兩張圖在文章裡難以閱讀，已在 repo 重畫（`article.md` 的 mermaid 與
`publish/images/` 的 PNG 都換了），線上版還是舊圖，要在 Medium 編輯器裡換掉。
英文版尚未發布，其 `publish/en/images/` 已是新圖，不需另外處理。

| 圖 | 原本的問題 | 新圖 |
|---|---|---|
| 第七節 `diagram-07.png` | 612×3960，1:6.5 的直條，在文章裡要滑好幾個螢幕 | 1198×1588，把 12 節點直鏈收成一個迴圈節點 |
| 第八節 `diagram-08.png` | 1568×78，20:1 細條（`direction TB` 在 LR 父圖裡被忽略），字在 Medium 上會縮到約 6px | 810×1044，改成上下兩張卡片 |

## 系列連結：已完成

2026-09-03 營運篇上線後，中文三部曲四篇彼此的系列連結全部補成真正的 Medium URL，
線上版與 repo 原始檔一致。四篇線上都驗過：0 死連結、0 殘留「（即將發布）」、
0 裂開的破折號，圖數不變。

中英互連也完成了：2026-09-03 英文版上線後，本篇文末已加上「英文版：English edition」的連結，
英文版也回連本篇。
