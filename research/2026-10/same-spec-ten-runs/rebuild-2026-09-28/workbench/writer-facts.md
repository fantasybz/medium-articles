# 給主寫者的可引用事實與最小重播例子

來源：[observed-results.json](observed-results.json)；方法與邊界：[README.md](README.md)。所有下列結果都是可信 fixture 的後設教學，不是 40 份正式模型候選的發現。

## R05 false、後續有效訊息與完成事件

原始輸入：

```jsonl
{"type": "item.completed", "item": {"type": "agent_message", "text": false}}
{"type": "item.completed", "item": {"type": "agent_message", "text": "after"}}
{"type": "turn.completed", "usage": {"input_tokens": 10, "output_tokens": 5}}
```

reference 實際三出口：

```json
{
  "stdout": "after\n\n<!-- tokens: in 10 out 5 -->\n",
  "stderr": "[codex malformed event] line 1: text must be a string or null\n",
  "returncode": 6
}
```

推導：第一行 false 依 R05／R03 診斷且不算發言；第二行 after 算發言；第三行 usage 有效所以印 token 註記；EOF 時無明確失敗但有 malformed，R11 決定 exit 6。REASON 的確切用字不是規範。

合法 REASON 改寫的實際結果：

```json
{
  "stdout": "after\n\n<!-- tokens: in 10 out 5 -->\n",
  "stderr": "[codex malformed event] line 1: invalid optional text: text\n",
  "returncode": 6
}
```

這份合法改寫通過全部四個教學批次案例，雖然 stderr 字串與 reference 不同。

## 正常案例看不到六種錯法

輸入為 text:"ok" 加有效完成事件時，reference、六份刻意錯法及合法改寫全部通過。加入邊界案例後，下列三份錯法各只在一個出口不同：

| Fixture／案例 | 不同的出口 | reference | 刻意錯法 |
|---|---|---|---|
| `stop-after-malformed`／`continue-after-malformed` | stdout | `"after\n\n<!-- tokens: in 10 out 5 -->\n"` | `""` |
| `omit-malformed-diagnostic`／`false-text` | stderr | `"[codex malformed event] line 1: text must be a string or null\n"` | `""` |
| `wrong-priority`／`explicit-failure-priority` | returncode | `3` | `6` |

這是預先指定的已知錯法；不能寫成正式候選的錯誤分類或頻率。

## EOF 前觀察程序

1. 啟動 fixture；stdin、stdout、stderr 都使用 pipe。
2. 只送以下一行並 flush stdin，保持 stdin 開啟：

```jsonl
{"type": "item.completed", "item": {"type": "agent_message", "text": "stream-before-eof"}}
```

3. 在 1 秒觀察窗內，嘗試從 stdout 讀到 `stream-before-eof\n`。reference 讀到，`stdin.read()` 整段緩衝版本沒有讀到。
4. 完成上述觀察後才送以下一行，再關閉 stdin：

```jsonl
{"type": "turn.completed", "usage": {"input_tokens": 10, "output_tokens": 5}}
```

5. 兩份 fixture 結束後的三出口完全相同：

```json
{
  "stdout": "stream-before-eof\n\n<!-- tokens: in 10 out 5 -->\n",
  "stderr": "",
  "returncode": 0
}
```

buffering 版本也通過全部四個批次終態案例。因此例子支持的是「需要 EOF 前的觀察」，不是模型效能或特定等待門檻。

## 變形關係的反例

- 在 false 案例前插兩空行：stdout／exit 不變；診斷的實體行號 1 → 3。若要求 stderr 也不變，正確 fixture 反而被拒絕。
- 將 text:"same"＋有效完成整段送兩次：stdout 片段重複兩次；stderr 空、exit 0。R13 要求處理重複與完成後事件，這個操作不是冪等。

## 邊界

- 目前 26 項自我檢查＋3 項 oracle 單元測試通過；不能將數量當成完整契約涵蓋或 mutation score。
- reference 和六種錯法、一份合法改寫都通過語法解析與編譯，沒有藉 SyntaxError 或 traceback 製造辨識結果。
- 沒有新模型呼叫，不更動正式 N=40／103，也沒有使用或弱化正式 Seatbelt。
- 標準庫 subprocess 僅執行固定可信 fixture。Python -I 不是 OS 沙箱。
- 一秒觀察窗受排程影響；reference 若也沒有在 EOF 前輸出，應先處理環境／觀察有效性。
- 只觀察第一則有效訊息；stdout／stderr 各自比對，沒有量測兩者之間的全域交錯順序。
