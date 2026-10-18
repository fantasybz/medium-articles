# 契約教學實際執行結果

執行時間（UTC）：`2026-09-27T17:02:45.623214+00:00`。

這是新增的可信 fixture 教學，不是正式模型研究。無新模型請求，未執行任何正式候選，未增加 N=40 或原本的 103 項檢查。

## 結果

- 1 份 reference、6 份刻意錯法與 1 份合法 REASON 改寫都通過 Python AST 解析與編譯，執行沒有 SyntaxError 或 traceback。
- 8 份 fixture 都通過正常輸入的三出口檢查；因此只有正常案例的檢查，無法辨識這 6 種錯法。
- 加入錯型、後續事件與明確失敗案例後，5 種錯法按預期被辨識。
- 合法 REASON 改寫雖然產生不同於 reference 的診斷字串，仍通過全部 4 個批次案例。oracle 因而沒有把 reference 用字當成唯一答案。
- 整段輸入緩衝的錯法仍通過全部 4 個批次終態案例，但 EOF 前的觀察能把它與 reference 分開。
- 兩組變形示例均符合從契約推導的關係，同時否定過度寬泛的「輸出不變」或「重複冪等」假設。
- 26 項教學自我檢查全部通過；另有 3 項 oracle 單元測試通過。這些數字只描述教學裝置的驗證。

完整輸入、預期值、實際值與逐出口比較見 [observed-results.json](observed-results.json)。

## 三個可以獨立出錯的出口

| Fixture | 對照案例 | stdout | stderr | exit |
|---|---|---|---|---|
| stop-after-malformed | continue-after-malformed | **不符合** | 符合 | 符合 |
| omit-malformed-diagnostic | false-text | 符合 | **不符合** | 符合 |
| wrong-priority | explicit-failure-priority | 符合 | 符合 | **不符合** |

三列都使用有效語法的錯法，而且各自只在一個出口偏離該輸入的預期結果。因此，任何單一出口都不足以代替其餘兩個。這是刻意安排的辨識示例，不是正式候選的錯誤頻率。

## 終態相同，EOF 前的輸出不同

| Fixture | 觀察窗 | EOF 前看到訊息 | 送完輸入後的三出口 |
|---|---|---|---|
| reference | 1.0 秒 | 是 | 全部符合 |
| buffer-until-eof | 1.0 秒 | 否 | 全部符合 |

兩者最終 stdout 都是 `"stream-before-eof\n\n<!-- tokens: in 10 out 5 -->\n"`，stderr 都是空字串，exit 都是 0。只有在 stdin 還開著時讀取 stdout，才會看見這個差異。

觀察窗只服務於本機教學，不是效能基準，也不是 production 時限；reference 若同樣沒有及時輸出，就應先處理環境或觀察方式，不能把它解讀為完成了有效的正反對照。

## 合法的另一種答案

`false-text` 案例的 reference 診斷為 `[codex malformed event] line 1: text must be a string or null\n`；合法改寫的診斷為 `[codex malformed event] line 1: invalid optional text: text\n`。兩者都符合 R03 的非空單行原因，stdout 與 exit 也相同，因此都應通過。若測試只接受第一個字串，錯的是測試新增了規格沒有的要求。

## 兩個變形關係

1. 在 `false-text` 前插兩空行：stdout 與 exit 不變，malformed 診斷由 `line 1` 變 `line 3`。要求 stderr 也完全不變，會拒絕正確 reference。
2. 將合法的「same 訊息＋完成」片段重複：stdout 片段出現兩次，stderr 仍空、exit 仍 0。R13 明文保留重複事件，要求冪等會新增契約沒有的去重限制。

## 來源與環境

- Python：`3.14.5 (main, May 10 2026, 10:21:34) [Clang 21.0.0 (clang-2100.0.123.102)]`。
- 系統：`Darwin 25.6.0 / arm64`。
- 執行：標準函式庫 subprocess、Python `-I -B`、暫存目錄中的可信 fixture；沒有 OS 沙箱。
- reference 為 AI 撰寫的研究工具 fixture，不是人工 baseline。它通過本教學案例，並不構成完整正確性證明。
- 沒有匯入或呼叫正式 evaluator，沒有更改 Seatbelt。原始 source SHA 在教學前後相同。
- 工作台程式 SHA-256：`2ef3e7c87fb9f62e06f82911055af8e7d277dec2225a0a8ebdca589826a645b9`。

| 凍結來源（source/ 下） | SHA-256 |
|---|---|
| `tests/fixtures/parser_reference.py` | `aad3638eecf746ee473893d805e0734f68dd2a861f4de25be7831da390db1c9f` |
| `tests/test_task_evaluator.py` | `e6ff5eaa2fa043aa4a95a1fadf32bab7df7cc388905b9d81912278a05e82c952` |
| `requirements.json` | `32e0a0af2578564624b5a5b5f9d981e0dc296e6eb690b6598482cb809419a515` |
| `evaluator.py` | `443b47cc93ca1559293a6025472696eee8351a25cb8486e09ee682bcfd29508a` |

每一份衍生 fixture 的唯一替換位置、替換文字與 SHA，另存於 JSON 的 `fixtures`。正反案例的 expected output 在工作台中獨立列出，沒有把當次 reference 輸出直接當成 oracle。

## 限制與引用方式

可以引用：「後設教學使用六種有效語法的刻意錯法，展示正常案例與終態觀察各自可能留下的盲點；每一份錯法都能通過正常案例，五份被其他三出口案例辨識，整段緩衝則需要 EOF 前觀察。」

不能引用成：「正式四十份候選發生六種失敗」「驗收涵蓋全部 R01–R13」「模型錯誤率為六分之五」，或「一般 subprocess 等效於正式沙箱」。示例沒有對應人力工時、維護品質或正式研究中某類錯法的盛行率。

初版紀錄留在 [runs/initial-results.json](runs/initial-results.json)，包含追加合法正對照之前的 23 項檢查。當前版本重新產生結果，不合併兩版計數。
