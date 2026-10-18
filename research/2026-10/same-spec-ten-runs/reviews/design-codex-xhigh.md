**結論：仍有 launch blocker。** 目前不建議開跑正式 40 slots；不是因為範圍太小，而是有幾個會讓「已觀測 40 次」事後無法被信任或無法正確呈現的具體缺口。

1. [run_study.py] `verify(destination)` / `main()`
觸發：freeze 後、正式 run 前，若工作目錄中的 source 有任何改動。
問題：`verify()` 以目前 `ROOT` 的 `inputs()` 對 manifest 比對；但 `main()` 會先呼叫 `verify(destination)`，之後才 `execv` 到 `destination/source/run_study.py`。因此 freeze 後若 repo source 有合法後續編輯，runner 會拒跑；這與 protocol 說「Run and analyze from that bundle」不一致。這是 source freeze / measurement mismatch，會讓正式 campaign 可用性取決於外部工作區狀態，而不是 frozen bundle。

2. [evaluator.py] `cases()` vs [requirements.json] R03/R10
觸發：`turn.failed` 的 `error` 或 nested `message` 型別錯誤。
問題：R03 說 malformed event「contributes no stdout and does not count as completed turn or agent message」，例外只有 `turn.failed` 保留 explicit failure 與 legacy diagnostic。Evaluator 的 `wrong-failed-error-envelope-*` case 允許 malformed `turn.failed` 後面的 `message("after")` 和 `DONE` 仍輸出 stdout，這是對整體 stream continuation 的合理解讀；但 R03 字面也可被讀成只丟棄 malformed 該行。建議把 R03 明確改成「該 malformed event contributes no stdout」，避免 oracle 被視為 hidden requirement。

3. [evaluator.py] `cases()` / hidden expected stderr
觸發：candidate 對 malformed reason 輸出空字串、多行字串、或不同診斷順序。
R03 只要求 REASON 非空單行；`stderr_matches()` 接受任意非換行內容，這點 OK。但 R10 case 要求 malformed diagnostic 一定先於 `[codex turn FAILED]`，規格有寫「emit the R03 line first」，OK。無 blocker。只是文章中不能寫 evaluator 沒有任何隱含格式約束；它仍固定 prefix、line number、順序與 legacy text，這些是公開 requirements。

4. [analyze.py] `validate_inputs()`
觸發：campaign 因 boundary breach / halt 而未滿 40，但有人誤用 `analyze.py`。
此處已正確拒絕 incomplete data；不是 blocker。配套 [campaign_status.py] 也不算 CI。可接受限制：incomplete campaign 不報 confidence intervals。

5. [analyze.py] `render_report()` / resource denominators
觸發：usage/cost 欄位缺失或某些 failed slots 沒有 provider usage。
目前 report 有 `observed/planned`，token 也有 observed counts；成本 table 有 `Cost observed / planned`。missing 不填零。這已處理 missing denominators，非 blocker。

6. [article outline] `research/2026-10/2026-11-same-spec-ten-runs.md`
觸發：正式結果尚未產出時，若文章直接發布或沿用「已凍結／已 pilot／工具已通過」語氣。
目前大綱多處仍是計畫語氣，且明說正式實驗尚未執行；可接受。但發布 gate 必須要求結果段不得把 pilots、tool checks、source audit 或 independent reviews 寫成 formal results。這是 release blocker，不是 run blocker。

7. [PROTOCOL.md] Generation boundary
觸發：Claude CLI metadata 中 safe mode 仍揭露 built-in components。
Protocol 已說 identities are recorded，且 `parse_trace()` 要求 tools/MCP/skills/slash commands 空、assistant 無 tool_use、assistant model 符合 expected。可接受限制，不是 blocker。

**正式開跑前必修：** 修正 `run_study.py` 的 frozen-bundle verify/run 流程；並把 R03 對 malformed event 的「丟棄範圍」改成明確指「該行事件」而非後續 stream。其他項目目前可作為 documented limitations，不必擴成新人類研究或額外瀏覽任務。