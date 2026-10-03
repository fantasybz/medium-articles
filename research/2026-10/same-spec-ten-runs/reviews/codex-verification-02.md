確認：這兩項都可關閉。

1. Finding1 是誤讀，應撤回。你貼的 `main()` 沒有在 `execv` 前呼叫 `verify(destination)`。實際順序是：live runner 解析 `run` -> 找 `destination/source/run_study.py` -> `ROOT != frozen_script.parent` 時直接 `os.execv(...)`。`verify(destination)` 首次出現在 frozen script 進入後的 `run_locked()` head。你補的 regression test 也正好鎖住這點：若 live `verify` 被呼叫會 fail，但實際先進 `execv`。

2. Finding2 也已關閉。R03 現在明確寫「malformed event on that line contributes no stdout」且「continue reading; never ... stop processing later events」，所以 discard scope 已限定為該行/該 event，不會吞掉後續 stream。`turn.failed` 例外也明確保留，與 R10 一致。

結論：這兩個 prior blockers 沒有剩餘 blocker。