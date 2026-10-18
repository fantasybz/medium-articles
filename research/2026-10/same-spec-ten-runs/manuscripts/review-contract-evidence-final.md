# 契約篇全文證據結案

審查時間：2026-09-25T09:29:18.329096+00:00。

**判定：契約篇全文在本次證據範圍通過，未解 blocker／major／minor 均為 0。** 先前完整閱讀第 1–291 行發現的 1 major、1 minor 均已解決；此結案繼承全文審查並核對兩項精確修訂，不是只簽新增段落，也不是全系列 READY。

目前 [article.md](../../../../2026-11-same-spec-contract/article.md) 有 293 行、45,725 bytes，SHA-256：`6f99865b86beabc93adfa6ca61a2e8cd826cf926eb9b4afbfca7a149f81019cc`。

## 全文基礎與精確差異

[完整初審](review-contract-evidence.md)與 [JSON](review-contract-evidence.json)保留 `416476b5ade3ded365cd3faff9477d666175ceb5154eddffc75ed18a8da18def` 的全文覆蓋及原始 finding。已核對六節、四張表、全部範例、F1、References、AI 協作與署名。

本次依 [contract-evidence-delta.json](contract-evidence-delta.json) 的兩項改寫，從現稿逆向還原精確得到初審 SHA，再由初審稿正向重播精確重建現稿。新增一個段落讓篇幅由 291 行增為 293 行；沒有額外數值、表格、例示或來源改動。新第 191–215 行已逐段重讀，並對照第一節的錯誤診斷及後段限制。

| 初審 finding | 原程度 | 新稿位置 | 結案依據 |
|---|---|---|---|
| CONTRACT-E01：候選／生成／隔離分類混為一層 | major | 203、205 | reference、語義 mutants 與候選 timeout 測試先說明；三項 preflight denial probes另列。批次 `_grade` 的 `timeout`／`output_limit`／`mismatch` 與生成 trace 的 `boundary_violation` 明確分開，並明說不能把每種候選越界都辨識成獨立類別。 |
| CONTRACT-E02：全部可控輸入與開關固定 | minor | 195 | 改為明確送出的 packet 及封存紀錄列出的模型、effort、CLI 開關；不再涵蓋沿用而未完整記錄的環境與 provider/CLI context。 |

第 205 行還保留了正確的診斷邊界：mismatch 應對照規格、expected 與實際輸出，不能直接假定候選語義必錯。這與 evaluator 可能有缺陷、須保留版本與一致重評的結語相符。

## 未變項與範圍

四張表、六個 fenced blocks（含 F1 Mermaid 與五個文字範例）逐 byte 不變。F1 的核准來源 hash 仍為 `0ba7420d3a7af4899388038dc97cd94bef12c8a50311377b1052315799bd6c97`。七行輸入的 4/5/6 malformed 行號、null／false 的 stderr 差異、exit 3 優先於 6、streaming 僅檢查可觀察的即時輸出、103 項有限涵蓋與 CLI wording caveat 均保持原樣。

正式結果與來源未改。第 207 行的 83 項工具測試仍與每候選 103 項及 40 個名額分開。第 249–251 行的版本化 amendment 建議，與本輪使用相同 oracle 的整批重評亦維持區別：未新增模型樣本，補記也不回寫原 packet／規範／評分。

本輪沒有重新執行候選或發出模型請求，沒有讀 raw Claude response／思考文字，沒有重新上網查證，也沒有改正文或凍結資料。語文 MCP、視覺渲染與遠端發布依各自流程處理；此結案不代替全系列、英文稿或發布驗證。
