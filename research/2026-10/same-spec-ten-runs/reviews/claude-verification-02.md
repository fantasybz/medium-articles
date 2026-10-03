# 第 2 輪驗證：兩項阻擋

**判定：READY**（只限阻擋 1、2；未重開其他範圍）

## 阻擋 1：營運失敗被誤判為邊界漂移，已修正

**程式證據：**
- 只有以下四種情況會令 `boundary_violation=True`：
  - init 暴露非空的 tools、mcp_servers、skills 或 slash_commands；
  - init 的模型是非 `<synthetic>` 的其他模型字串；
  - 任何層級出現 `tool_use`；
  - assistant 出現真實且不同的模型名稱。
- 以下情況只會得到 `unknown`、`operational_error` 或 `incomplete_trace`，不會 halt：
  - `<synthetic>` 訊息、缺少 model、缺少 init、`message` 不是 dict；
  - JSON 行截斷、UTF-8 位元組截斷。
- `run_locked` 只在 `boundary_violation` 時 halt。它改用 `read_bytes()`，原先的解碼例外路徑已消除。

**回歸測試：**
- 涵蓋原 529 fixture、缺少 model、空 trace、截斷的 UTF-8，以及畸形 envelope 內的 `tool_use`（仍判為違規）。
- 整合測試確認：兩個 slot 都留在原位，沒有 `HALTED.json`，`accepted_completion` 全為 false。

**實測（CLI 2.1.282）：**
- timeout 0.5s：2/2 為 `timeout`，violation=false，沒有 halt。
- budget 0.0001：2/2 為 `operational_error`（`error_max_budget_usd`），沒有 halt。
- 凍結後 `run_study.py` 與測試檔都沒有變動。

## 阻擋 2：評分依賴 CLI，已修正

- run 啟動時與評分迴圈前後都用 `verify(check_cli=False)`。這條路徑不解析 PATH、不執行 `--version`、不讀 binary hash，也不比對 `ANTHROPIC_*` 名稱。
- `cli_args` 在給定 executable 時不查 PATH。
- 測試刪除 CLI 後，`check_cli=False` 仍然通過，`check_cli=True` 則失敗，符合預期。
- 子程序與版本檢查都帶 `DISABLE_AUTOUPDATER=1`。此設定已寫入 manifest，並由 verify 強制檢查。
- CLI 只在每次生成啟動前檢查，與 PROTOCOL 一致。

## 殘餘事項（非阻擋）

1. **timeout 探針的覆蓋範圍**：0.5s 探針沒有 usage 或 cost，推測在模型輸出前就被終止。因此生成途中收到 SIGTERM 的真實 trace 仍未觀測到。分類邏輯不依賴這一點，因為任何 synthetic 或部分輸出都不構成違規。
2. **budget 探針的覆蓋範圍**：`modelUsage` 只有 Haiku，且 output tokens 為 0。停止時點推測在背景 Haiku 呼叫之後、Opus 生成之前。它驗證的是預算停止的記錄路徑，不是生成途中的超額。
   - 建議 PROTOCOL 補一句：`modelUsage` 可能包含 CLI 的輔助模型，它們不是生成模型，也不算漂移。程式已正確忽略這部分。
3. **生成階段的自動更新**：`DISABLE_AUTOUPDATER` 只作用於子程序。若同一台機器上的其他 Claude Code 工作階段自動更新，並清除凍結的版本檔，下一次生成啟動會 HALT。這是刻意的完整性停止，不影響評分。建議 campaign 期間全域停用自動更新。
4. **resume 的漏停窗口（原阻擋範圍外）**：若 runner 在寫入 `generation.json` 之後、halt 之前被硬殺，resume 後其餘 slot 會照常生成。評分迴圈只記錄 `boundary_failure`，不會 halt。可在評分迴圈遇到此狀態時補一個 raise。

以上兩項阻擋已解除，可以啟動正式 40 slots。
