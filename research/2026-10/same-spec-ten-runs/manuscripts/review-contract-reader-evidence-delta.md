# 契約篇讀者複核：證據修訂的有界檢查

結論：**PASS_CONTRACT_EVIDENCE_DELTA_READER_SCOPE，0 項新增讀者問題**。本輪只檢查兩處修訂與第四節相鄰段落，沒有重做全文或技術查核，也不覆寫先前 final 報告。

- 現稿 SHA-256：`6f99865b86beabc93adfa6ca61a2e8cd826cf926eb9b4afbfca7a149f81019cc`
- 前次讀者結案 SHA-256：`416476b5ade3ded365cd3faff9477d666175ceb5154eddffc75ed18a8da18def`
- 差異紀錄：`contract-evidence-delta.json`
- 本次閱讀：第 187–211 行。

第 195 行把固定項目限於 packet，以及封存紀錄列出的模型、effort 與 CLI 開關。它和同段未固定的 provider context、sampling 與 OS 狀態對照清楚，不再讓讀者以為所有環境條件都已完整固定。

第 203–205 行現在能辨別三層：工具測試如何對照已知實作與候選 timeout；preflight probe 實際驗證哪些操作被拒絕；生成紀錄又如何以 boundary_violation 核對模型、工具與 trace。批次案例的 timeout、output_limit、mismatch 沒有再被寫成辨識所有候選越界的分類器。

修訂也補足判斷的下一步。timeout 要回頭看候選行為與執行環境；mismatch 則核對規格、expected 與實際輸出，不能立即把責任歸為候選語義有錯。相鄰段落仍將三項 probe 的限制、83 項工具測試、103 項候選驗收和 40 次生成分開，段落承接自然。

兩處替換均只出現一次。反向還原得到前次讀者結案 SHA，再正向套用與現稿逐 byte 相同；只有紀錄中的兩處文字變動。全文因其中一段拆為兩段，由 291 行增為 293 行。未改動文字沿用原全文及後半部讀者複核。

技術事實由 evidence 代理核對；本報告只確認讀者能否看懂分類層次與證據邊界。未修改正文、先前報告或凍結研究資料。
