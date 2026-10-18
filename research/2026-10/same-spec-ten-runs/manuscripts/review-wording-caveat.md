# 措辭差異補記與前半部修正：獨立複核

日期：2026-09-25。審查者：`series_evidence_review`。判定：**三項前次問題與兩項小建議皆已修正；補記與跨篇限定成立。**

本輪只簽核新增措辭限制與前半部修正，**不是規格篇全文或全系列 READY**。沒有修改其他文章或封存檔。

## 對應版本

| 檔案 | SHA-256 |
|---|---|
| `.context/same-spec-ten-runs/manuscripts/spec-edited-prefix.md` | `9c9a41d4a9b3df43e9cb8410628a624ad895c43ed726511a64e8a4a29b0eae54` |
| `research/2026-10/same-spec-ten-runs/manuscripts/packet-wording-caveat.md` | `96e7ab484df0564d3ddfb5396216c0c63da83e22bf47fa0c251ecf362bf60490` |
| `research/experiments/same-spec-ten-runs/RESULTS.md` | `aa7d79489df2b0f457dc9d97bfd00547a58820a450b0fdae354bde98e38f9764` |
| `2026-11-same-spec-variance/article.md` | `5117ed22f1f93b6c5f8c094259addb87cb3b255f4f1d589ce213ccfecc24139a` |

## 前次五項處置

| 編號 | 修訂前半部行號 | 判定 |
|---|---|---|
| E-P01 | 75、80 | 已解決。R10 明寫 error 非 null 且非物件、message 非 null 且非字串；與 R10 原規格和既有 null 例外段落一致。 |
| E-P02 | 28、86、88、96、100、101 | 已解決。區分共同規範基準與已證語義等價；具體指出 A0 不需新增 CLI 參數、A/B/C 列為範圍之外，影響未辨識，保留 frozen packet。 |
| E-P03 | 38 | 已解決。舊行為改成未記錄 agent 發言，truthiness 與修補後 R05 非空字串判準分開。 |
| E-P-optional-R03 | 68 | 已解決。turn.failed 的例外明確指失敗狀態與 stderr 診斷，沒有暗示可計入 stdout、完成或發言。 |
| E-P-optional-pattern | 109 | 已解決。C pattern 摘要已保留 malformed turn.failed 的失敗訊號。 |

## 本次補記與跨篇檢查

- **W01：**定位為成稿後限制，不追認為預先登錄，也不修改 frozen 要求／評分。A0 原句與 A/R13 的分拆引文準確，B/C 繼承範圍清楚。（packet-wording-caveat.md 第 3、5、9、10 行）
- **W02：**影響是否存在未辨識；既不推定造成結果差異，也不以全數通過推定沒有影響。保留原始觀測，不估計排除差異後的純措辭效果，下一輪另訂版本，沒有冒充真人盲審。（packet-wording-caveat.md 第 12、14、16、18 行）
- **W03：**開頭補上 CLI 措辭限制；結語改為共同 R01–R13 基準，沒有宣稱語義等價。（RESULTS.md 第 7、79 行）
- **W04：**同步改為共同規範基準；具體指出 A0 與 A/B/C 差異，分布僅屬這四份實際 packet，不是純措辭效果。（article.md 第 17、28、30 行）
- **W05：**全文讀取未找到與補記矛盾的 purity 或已證規範等價主張。TL;DR 同一規格指各固定組內重複；結果等效性未證明與文字語義未證等價是兩項不同限制。成本段仍只描述 observed order，結語未因補記改判組別優劣。（article.md 第 3、67、89、91、177、179、195、203、215、219、221、225 行）
- **W06：**變異篇四張表及第二節至文末逐 byte 不變；新補記未改原數值。RESULTS 的 12 個組別表格列與 USD 總額仍符合 frozen summary。
- **W07：**重新核對 archive 索引 317 份檔案 hash 全部相符，summary hash 仍是原值；沒有新模型請求或候選執行。
- **W08：**補記、RESULTS、變異篇的本機相對連結皆存在；這不是遠端發布驗證。

- **W09：**本輪指出的 B/C 表格局部歧義已修正為「追加段不增要求；繼承 A 的措辭限制」，前綴欄改為 B 以 A 全文開頭、C 以 B 全文開頭。與第 88、96 行一致。（修訂前半部第 98、102–103 行）

## 數值與原始資料未變

以既有 MCP 紀錄的 `response.text` 取回上次證據審閱全文，SHA-256 精確為 `1cf47ca478afca22ff028c285c4d0550a844e4794886b7e345fa122a27cac800`。與目前變異篇比對，只有第一節第 17、28 行改寫和新增第 30 行；TL;DR、所有表格，以及第二節至文末均逐 byte 相同。因此原 AST、驗收、費用與引用數值沒有因補記改動。

另將 RESULTS 的四組驗收、AST、資源表，共 12 個資料列及 USD 5.692342 總額，與凍結 summary 重新對照，全部相符。summary SHA-256 仍為 `8198a4478b8158268298960576655d920db3b8d2dc2bd207348dcef8a346dfb9`。本輪重新檢查 archive 索引全部 317 份檔案的 hash，0 處不符。這是完整性核對，沒有重新執行候選或增加樣本。

## 尚待處理

本輪範圍內無未解問題。

## 判定邊界

變異全文已從標題讀到文末，這一輪只查新增 caveat 是否與既有段落矛盾，並沿用已綁定前版 hash 的完整證據審查。沒有重新驗證第三方論文，也沒有新增模型生成、候選重評、真人盲審或遠端發布。本報告不取代全文潤稿與 zh-TW MCP 檢查。規格尾段加入後仍須真正的全文 review。
