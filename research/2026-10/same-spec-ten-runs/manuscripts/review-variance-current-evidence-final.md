# 變異篇本輪差異證據結案

審查時間：2026-09-25T09:10:27.833776+00:00。

**判定：本篇證據範圍通過，未解 blocker／major／minor 均為 0。** 本判定以先前全文證據審查為基礎，加上本輪全部文字差異核對；不是全系列 READY，也不是公開發布完成。

正文：[article.md](../../../../2026-11-same-spec-variance/article.md)，266 行、41,225 bytes。本次綁定 SHA-256：`3ee25eaa1ca3ae1f177403f1719eb833a5c07ecfa972d4189e2129ab2fff6b0d`。

## 範圍與版本鏈

先前的[全文證據複核](review-evidence-followup.md)完整讀取 `ce383be20445328cec4a509e8ce7f519b94e9fe99b2fd927e494ffc4661c3587` 版本，核對最後兩段時態差異後簽到 `1cf47ca478afca22ff028c285c4d0550a844e4794886b7e345fa122a27cac800`。該輪已核對正式數字、論文版本、教學候選與 recall。六項初審問題的結案保留於原報告，本輪沒有覆寫。

接續的[措辭限制複核](review-wording-caveat.md)涵蓋 `5117ed22f1f93b6c5f8c094259addb87cb3b255f4f1d589ce213ccfecc24139a`：僅第一節三段新增共同基準／CLI 限制，其他表格與第二節以後不變。本輪再次由已保存的 zh-TW 回報 `response.text` 取回 `1cf47ca4` 原文，確認這段承接沒有其他變更。

本輪逐段重讀目前第 1–266 行，比對開頭、限制、結語與 AI 協作說明，並核對兩份 delta：

| 變更紀錄 | 前版 SHA-256 | 後版 SHA-256 | 實際驗證 |
|---|---|---|---|
| `variance-current-polish-delta.json` | `5117ed22f1f93b6c5f8c094259addb87cb3b255f4f1d589ce213ccfecc24139a` | `26adde9c3e9578ec949dbdc10e3c23fcb5faa6b20673bd8edce1120607703386` | 9 項紀錄、10 處字串替換；正向重播與逆向還原均符合 hash。 |
| `variance-final-reader-delta.json` | `26adde9c3e9578ec949dbdc10e3c23fcb5faa6b20673bd8edce1120607703386` | `3ee25eaa1ca3ae1f177403f1719eb833a5c07ecfa972d4189e2129ab2fff6b0d` | 第 79 行 1 處替換；正向與逆向均符合 hash。 |

兩份紀錄位於 `.context/same-spec-ten-runs/manuscripts/`，完整 SHA-256 見本報告的 [JSON](review-variance-current-evidence-final.json)。逆向處理「候選模型 → 生成模型」時，依原文限定於兩處「不使用工具」的句子；後段原已存在的兩處「候選的生成模型」未倒改。再正向套用原 delta 的全部規則，可逐 byte 重建現稿，沒有未記錄的正文變更。

本次是既有全文審查加差異結案；沒有重做第三方論文全文查證、模型實驗、候選執行或圖表渲染。

## 各項變更的證據判定

| 項目 | 現稿行號 | 核對結果 |
|---|---|---|
| CLI 範圍限制加入 TL;DR | 3；對照 17、28、30、89、91 | 通過。共同 R01–R13 基準與語義已證等價分開，明說措辭差異的實作影響未辨識。 |
| 系列導覽、第一節交接與尾段連結 | 5、17、231–235 | 通過。指向本機稿並明示尚未發布；沒有把本輪結案擴張成兄弟篇已通過審查。 |
| 兩處「候選模型」改為「生成模型」 | 3、32 | 通過。模型收到 packet 並交出候選程式，候選是被外部 evaluator 執行的檔案，角色更精確。 |
| 「選題的人」改為「選題的研究代理」 | 195；對照 207、262 | 通過。研究實作由 AI 代理協作，作者提出研究方向；沒有虛構作者親手執行、真人盲審或新增模型家族獨立性。 |
| 正式生成成本段落潤飾 | 185；對照 173、183、187 | 通過。40 名額都 accepted，因此本資料沒有失敗或放棄名額的正式生成成本可分攤。仍限定為 CLI 牌價估計，不是帳單或人力 ROI。 |
| 失敗案例數與失敗候選數 | 79–81；對照 89–91 | 通過。修正了計數單位的理由，沒有再說改變分母本身必然讓案例多的要求較容易失敗；原零失敗數值未改。 |

### A0／A 措辭差異仍是未辨識的限制

[凍結 A0](../../../experiments/same-spec-ten-runs/results/formal-2026-09-25/source/specs/A0.md)第 7 行原句是「No new CLI arguments or external dependencies are required.」。[凍結 A](../../../experiments/same-spec-ten-runs/results/formal-2026-09-25/source/specs/A.md)第 133 行將「adding CLI options」列為「outside this task」。本輪再次以 bytes 確認 B 以 A 全文開頭、C 以 B 全文開頭，所以限制落在 A0 對 A／B／C 的比較。

正文第 30 行保留「影響是否存在未辨識」，第 89 行保留額外 CLI 參數等未逐一驗證的範圍。第 177–179、203、221、225 行仍只描述觀測到的結果，沒有回頭宣稱純措辭效果、等效或附加指引無用。**103 項全數通過不能證明這項措辭差異沒有影響。** 原 packet 與評分不回寫；這一點與[公開補記](packet-wording-caveat.md)一致。

### 第三節的計數理由與零失敗

研究[大綱](../../2026-11-same-spec-ten-runs.md)第 219 行要求以 run 為分母按 requirement ID 彙整。[凍結 evaluator](../../../experiments/same-spec-ten-runs/results/formal-2026-09-25/source/evaluator.py)第 270–291 行保留每個案例的 requirement IDs 與 passed，第 336–349 行以集合輸出 failed requirements。一份候選同一條要求連錯數個案例，按 run 計數仍只算一次；按失敗案例數比較則會重複計入。各要求配置的案例數確實不同，且同一案例可涵蓋多個 requirement ID，因此不能把按案例的分布當作按候選的分布。

本輪直接讀取既有 40 份 `evaluation.json`，沒有執行候選：

- 40 份候選，每份 103 項，共 4,120 項 case outcome。
- 失敗案例數 0、失敗候選數 0；R01–R13 各自的失敗 run 數都是 0。
- 各候選的 coverage 配置相同；各 R ID 覆蓋案例數依序為 5、12、67、12、13、11、7、26、11、15、41、21、5。這些數字包含重疊標記，不能相加當成不同案例總數。

因此第 79 行的新寫法正確，第 81 行「按案例、requirement ID 或組別統計皆為零」仍成立；這僅是已凍結 103 項的結果，不是所有可能行為都正確，也沒有識別 CLI 措辭差異的因果影響。讀者意見 `VARIANCE-CURRENT-READER-01` 在證據層面已解決。

## 不變項與檔案完整性

四張數值表、三個 code block、F2 圖說與連結都逐 byte 等同 `1cf47ca4` 已全文審閱版。F2 PNG hash 仍為 `474f4ae875dcababaf7ffcddf501b2b7c49fa5d9ed0e80a4ac9a57a98f9084fb`；本輪只核對 hash，沒有重做視覺檢查。

本輪核對 manifest、records、summary、R01–R13 requirements、四份 specs、evaluator 與 runner 共 10 份來源，以及 40 份既有 evaluation，合計 50 個 hash 均符合 archive 索引。這是針對本輪主張的完整性核對，不是重新宣稱做完 317 檔完整稽核。先前 317 檔核對仍以既有報告為準。正式數字與 frozen data 均未修改。

## 狀態與限制

目前核對了 23 處本機相對連結，結案時全部存在，包括主代理剛組合的總論與契約稿。本輪只確認連結目的檔存在，沒有替兄弟篇全文簽核，也沒有冒充已完成發布驗證。第 154、242 行仍明說研究附件尚未遠端公開，公開發文前仍需補版本固定、可存取的入口。

未解問題 0；本次判定只結清變異篇的證據範圍。沒有新增模型樣本、候選執行、真人盲審、論文重現或遠端發布。zh-TW MCP 與編輯／讀者檢查沿用各自報告，本報告不宣稱重新執行。未閱讀或輸出 raw Claude thinking，未改正文、其他報告或凍結資料。
