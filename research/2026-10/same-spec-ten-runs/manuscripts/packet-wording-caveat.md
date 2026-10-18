# 成稿階段補記：A0／A 的 CLI 範圍措辭

發現日期：2026-09-25。這是全文證據複核發現的方法限制，不是變更正式實驗要求或評分方式的 amendment。凍結 packet、requirements、候選與原始結果均保持原樣；本次沒有新增模型樣本。

四組以同一組 R01–R13 為規範基準。A、B、C 的規範段落逐字相同，A0 與 A 則使用不同措辭。相同 requirement ID、hash 核對與 AI 語義審查，都不能證明這兩份文字嚴格等價。

逐字複核找到一處具體差異：

- [A0 的 R01](../../../experiments/same-spec-ten-runs/results/formal-2026-09-25/source/specs/A0.md) 寫「No new CLI arguments or external dependencies are required.」，表示不需新增參數。
- [A 的 R13](../../../experiments/same-spec-ten-runs/results/formal-2026-09-25/source/specs/A.md) 另把「adding CLI options」列為「outside this task」。[B](../../../experiments/same-spec-ten-runs/results/formal-2026-09-25/source/specs/B.md) 與 [C](../../../experiments/same-spec-ten-runs/results/formal-2026-09-25/source/specs/C.md) 都以 A 的全文開頭，也繼承這句話；A0 的 R13 沒有對應句子。

「不需要」與「不在範圍內」的約束強度不同。任務背景可能使實作者採取相同做法，但這項差異是否影響候選，本輪沒有辨識。不能推定它已造成結果差異，也不能因四組都通過驗收，就推定它沒有影響。[凍結評測器](../../../experiments/same-spec-ten-runs/results/formal-2026-09-25/source/evaluator.py) 未逐一檢查額外 CLI 選項，無法替這項範圍語義作出判定。

因此，正文會以「共同 R01–R13 基準」描述設計，並明確保留 A0／A 的措辭限制；不再把它概括為已證明只改寫法、完全沒有規範強度差異的介入。各組 10／10、103 項有限驗收、結構描述與資源紀錄仍是原來那四份 packet 的觀測結果。這些數字不因補記而改變，但它們不能用來估計排除這項差異後的純措辭效果。

規格篇會提供具體例子，總論與變異篇保留簡短提示。若下一輪要修正措辭，須另訂研究版本，不能事後覆寫本輪 packet 再沿用原結果。

這項發現來自獨立 AI 證據審查與主代理逐字複核，不是新增真人盲審。
