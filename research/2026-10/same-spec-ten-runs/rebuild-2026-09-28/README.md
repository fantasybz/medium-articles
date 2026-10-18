# 全面重寫 research loop

> 本頁保存 2026-09-28 的研究重寫過程。10/03 另依作者試讀意見修訂概念引介與段落連貫，見[最新修訂](../readability-2026-10-03/README.md)與[成稿狀態](../manuscripts/STATUS.md)；本頁品質紀錄只對應 9/28 版本。

本輪回應作者對 why、how、what 深度及實用度的否定，對標十月份「綠燈不是驗收」四篇。

四篇中文正文已由 Claude Code Opus 5.5 `max` 全面重寫，完成主代理逐段潤飾、後半部重讀、獨立代理審查、嚴格繁中檢查及本機發布包驗證。全系列尚未發布，作者尚未確認本輪品質；目前成稿入口見 [STATUS.md](../manuscripts/STATUS.md)，各版本與驗證範圍見[品質紀錄](quality-record.md)。前輪文章及發布包保留私人快照，正式四十次實驗封存不變。

本輪沿 repo research loop 執行來源收集、摘要、提案與反駁、大綱審查、主寫、證據／讀者／編輯審查，以及潤飾與發布包驗證。額度重置前的 Claude xhigh 架構請求失敗，未計為有效複核；後續由 Claude max 主寫、Codex 代理審查與修訂。使用實際本機 CLI 與代理分工，不冒稱已呼叫不存在的 native Workflow 工具。

文章必須回答：讀者為什麼值得處理這個問題、方法透過什麼機制有效、在哪些情況不適用，以及誰可以拿什麼工件做出下一個決定。詞句與格式檢查在論證完成後進行，不能代替這些要求。

研究分工：十月份基準與現稿失敗診斷；規格／契約的基礎與實務；重複評估／實驗設計；當前 spec-driven development 的工作方式與團隊決策。只採用已核對的 primary sources；私人全文快取不進公開稿。

## 研究與論證入口

- [重寫架構](rewrite-plan.md)及[證據如何改變決定](evidence-to-decision.md)：每篇需要補足哪一段推理，來源支持什麼、不支持什麼。
- [規格與契約基礎](spec-foundations-research.md)、[重複評估研究](reliability-research.md)、[現行工具工作方式](tool-landscape-research.md)：保留一手來源、版本及引用限制，各自另有來源台帳。
- [證據／讀者大綱審查](outline-evidence-reader-review.md)、[編輯／圖表審查](outline-editor-diagram-review.md)、[審查處理紀錄](outline-review-resolution.md)：分別記錄架構修正，以及必須等正文才能判斷的品質。

## 四篇共用的實務工件

| 讀者要作的決定 | 已填示例與可用附件 |
|---|---|
| 是否值得評估一項文件改動 | [文件改動提案](document-change-proposal.md) |
| 修改哪一段交代，以及預期它影響什麼 | [規格修改卡](spec-change-card.md)、[自查跨任務改寫政策](self-check-transfer-policy.md) |
| 目前驗收能否辨識合法行為與指定錯法 | [Parser 教學 workbench](workbench/README.md)、[CSV 教學重播](workbench/csv-transfer.md) |
| 下一筆證據該補在哪裡，何時足以採用 | [下一輪比較計畫示例](comparison-plan-example.md)、[兩份實作的靜態查閱](static-review-walkthrough.md) |

Parser 範例的介入為 P 的展開規格，以及 Q 在相同規格上加入凍結 B 的六題自查原文。跨任務時，則須先依共同規格建立並核對自查，不能直接複製 parser 的要求。改寫政策與各題 P／Q 都要事前固定；目前尚未完成全體任務映射，下一輪比較也尚未執行，不能借用原四十次的結果宣稱它有效。

Parser workbench 的 26 項自我檢查與 3 項 oracle 單元測試，以及 CSV 的 11 項自測，均由主代理另行重播。它們是檢查教學裝置的結果，不增加正式研究的生成名額或 103 項驗收。兩張概念圖的用途與驗證見 [圖表說明](figures.md)。

新正文、逐段潤飾與發布包的實際狀態，以[成稿狀態](../manuscripts/STATUS.md)為準。
