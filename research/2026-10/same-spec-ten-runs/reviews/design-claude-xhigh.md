# 預正式啟動閘門審查（40 slots）

**審查範圍**：只依本封包內容。`analyze.py`、`campaign_status.py`、seed、`requirements.json`、`task.json` 不在封包中，PROTOCOL 對它們的描述未經本次驗證。

## 規格等價與 oracle 忠實度：無阻擋

- **規格等價**：A、B、C 的 R01–R13 正文逐段相同。A0 逐條比對後語意等價，沒有多出或缺少的規範。
- **C 的組成**：C 同時包含 B 的非規範段落，屬累積式設計。PROTOCOL 應明寫「C = B + pattern」，這只是文件修正。
- **案例數**：102 個批次案例加 1 個串流探針，共 103 項。分組為 legacy 16、compat 18、hardening 68，計數正確。
- **可追溯性**：每個案例都對得到明文條款。沒有案例要求規格未定義的行為，也沒有案例會拒絕合規實作。測試輸入不含 `\r` 或 U+2028，所以讀取方式不會影響行號。
- **Clopper–Pearson**：10/10 的下界 69.15% 正確。

**可接受的已記錄限制：**
- R01 中「保留 main 入口」「不加新參數」兩項沒有被檢查。主要端點應寫成「通過 103 項外部檢查」，不能寫成「完全符合規格」。
- C-locale CJK 案例在 `-X utf8=0` 下，stdio 使用 surrogateescape。一個沒有設定 UTF-8 的樸素實作，可能靠位元組往返直接通過。
  - 請確認突變測試已殺死「移除 UTF-8 設定」的變體。
  - 若沒有，報告需註明此條件未被區辨。

## 阻擋 1：營運失敗被判為邊界漂移，並永久 HALT

- **位置**：`parse_trace` 中 `generated != {expected_model}` 使 `boundary_ok=False`，接著 `run_locked` 在生成迴圈中執行 `score()` 並拋出 `RuntimeError("Observed model/tool boundary drift")`，最後寫入 `HALTED.json`。
- **違反的規範**：PROTOCOL 規定「disconnect、malformed response、budget stop、timeout 留在原 slot」，並把邊界破壞只定義為「工具呼叫或不同的生成模型」。
- **離線可重現觸發**：stdout.jsonl 內容如下：
  - 合法 init；
  - `{"type":"assistant","message":{"model":"<synthetic>","content":[{"type":"text","text":"API Error: 529"}]}}`；
  - `{"type":"result","is_error":true,...}`。

  此時 `generated={"<synthetic>"}`，status 被標為 `boundary_failure`，campaign 永久停止。assistant 事件缺少 `model` 時同樣觸發（`generated={None}`）。
- **實際觸發**：Claude Code 在重試耗盡的 API 錯誤（529、429、連線中斷、用量上限）時，以及可能在超過輸出 token 上限時，會輸出 model 為 `<synthetic>` 的 assistant 訊息。請用凍結的 CLI 版本實測確認。在 4 路並行、high effort、40 slots 的條件下，這並不罕見。
- **後果**：
  - 40 slots 無法完成，`analyze.py` 依設計拒絕計算。
  - 營運失敗被誤標為邊界破壞，這是分類錯誤，不只是限制。
- **為何 pilot 沒有發現**：兩個 pilot 都只走過成功路徑。timeout、預算停止、API 錯誤的真實 trace 都沒有實測，包括 SIGTERM 後 CLI 是否會輸出 synthetic 中斷訊息。
- **修正**：
  1. `<synthetic>` 或帶有錯誤欄位的 assistant 事件，歸為營運錯誤：`cli_success=False`，保留在原 slot，不 halt。
  2. 只有真實且不同的模型名稱，或出現 tool_use，才 halt。
  3. 加入上述離線回歸 fixture。
  4. 用拋棄式 freeze 實測失敗路徑（例如 `--timeout 20`、`--budget 0.01`），確認 timeout 與預算停止都留在原 slot 而不是 HALT。
  5. 修正後重新凍結。

## 阻擋 2（條件式：未停用 CLI 自動更新時）：版本檢查可在評分階段 HALT

- **位置**：評分迴圈在每個 slot 前後呼叫 `verify()`，其中執行 `claude --version`。
- **可重現觸發**：所有生成結束後，替換 PATH 上的 `claude` 或讓 CLI 自動更新。第一個 SCORED 之前就會拋出 `ValueError`，寫入 HALTED。
- **後果**：
  - 40 個 slot 全部變成 generated_not_scored，且不可 resume。
  - 評分根本不使用 CLI，這個檢查不提供任何效度保障，卻可能毀掉一個已完成生成的 campaign。
  - 生成期間發生同樣情況也會中斷 campaign。
- **修正**：
  - 執行環境設定 `DISABLE_AUTOUPDATER=1`，並寫入 manifest。
  - CLI 版本只在每次啟動生成前檢查。
  - 評分階段只驗 source、manifest、Python。

## 非阻擋（低機率或已記錄，建議順手修）

- **HALT 路徑缺少保護**：`run_locked` 直接呼叫 `read_text()` 與 `parse_trace`，沒有 `score()` 那層例外保護。trace 尾端 UTF-8 多位元組被截斷，或 `message` 不是 dict，都會直接 HALT。先前修的是 JSON 行截斷，不是位元組截斷。
- **評分中途被硬殺後 resume**：`candidate.mkdir()` 會拋出 FileExistsError，進而 HALT。
- **孤兒子程序**：runner 遭 SIGHUP 或 SIGKILL 時，以 `start_new_session` 啟動的 Claude 子程序會繼續執行，寫入已標為 interrupted 的資料夾並持續產生成本。建議以 nohup／caffeinate 執行。
- **輪詢延遲**：`proc.wait(timeout=5)` 與 `verify()` 會阻塞輪詢，實際觀測延遲可能超過 0.5 秒。保守的 timeout 標記仍然有效，但 PROTOCOL 應註明 wall_seconds 是觀測時間。
- **環境變數未記錄**：繼承的 `CLAUDE_CODE_MAX_OUTPUT_TOKENS`、`MAX_THINKING_TOKENS`、`ANTHROPIC_*` 以及認證方式都沒有記錄。建議在 manifest 記錄一份允許清單（不含秘密值）。

## 判定：NOT READY

需要完成：
1. 修正阻擋 1，並附離線 fixture 與真實失敗路徑實測。
2. 停用 CLI 自動更新，或移除評分階段的 CLI 版本檢查。
3. 重新凍結。

完成後即可啟動 40 slots，其餘項目不需要擴大範圍。