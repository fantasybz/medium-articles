# 契約教學 workbench：同一盞綠燈，漏掉了哪一個問題？

這份教學從文章 repo 的真實 JSONL parser 契約出發，用一份已知的 reference fixture、六個刻意改壞的版本與一份合法改寫，展示兩個需要分開處理的問題：**選了哪些輸入，以及觀察了哪些結果。** 正常案例全部通過，不代表錯型與例外受到保護；終態的三個出口全部相同，也不代表串流時點符合要求。

這是 **2026-09-28 新增的後設教學實驗**，不是正式的 40 份模型候選，也沒有替凍結的 103 項檢查追加結果。沒有呼叫模型、沒有執行正式候選，不計算模型通過率或 mutation score。刻意錯法只能證明這幾個觀察能分辨這幾種行為，不能估算錯誤在實際工作中多常出現。

## 執行與查核

需要 Python 3.10 以上，僅使用標準函式庫。從 repo 根目錄執行：

```sh
python3 research/2026-10/same-spec-ten-runs/rebuild-2026-09-28/workbench/workbench.py --output research/2026-10/same-spec-ten-runs/rebuild-2026-09-28/workbench/my-results.json
python3 -B -m unittest discover -s research/2026-10/same-spec-ten-runs/rebuild-2026-09-28/workbench -p 'test_workbench.py' -v
```

第一個命令會在暫存目錄建立固定 reference、六份刻意錯法與一份合法改寫，先解析並編譯每份 Python，再執行案例；結束時移除暫存目錄。它不接受任意 candidate 路徑。第二個命令檢查教學 oracle 是否接受合法的診斷文字差異，又能拒絕缺行、多行、空原因、錯行號或任何一個出口的錯誤。

本機結果在 [observed-results.json](observed-results.json)，可讀摘要在 [RESULTS.md](RESULTS.md)，要求與觀察的對照在 [obligations.md](obligations.md)。執行碼、fixture 衍生方式、輸入、預期值、實際輸出與 SHA 都保存在結果裡。`stderr` 預期值中的整數代表 malformed 的實體行號，例如 `[1]` 表示恰好一行以 `line 1:` 開頭、具有非空單行原因的診斷，不是完整診斷字串。

腳本先後核對四個凍結來源的 SHA，只讀取它們，不匯入或改寫正式 evaluator。執行採 Python `-I -B` 與一般 subprocess；`-I` 是 Python 的隔離模式，**不是 OS 沙箱**。本教學限於已知 fixture，不提供執行不受信任程式的介面，也不替代、繞過或聲稱等效於正式研究的 macOS Seatbelt。已實際執行的環境為 CPython 3.14.5、Darwin 25.6.0、arm64；其他環境尚未驗證。

## 先預測，再看結果

先看這四組輸入，替 stdout、stderr 和 exit 各寫一個預測。`→` 表示下一個 JSONL 事件，不是同一行裡的字元。完整 JSONL 留在結果檔。

| 教學案例 | 輸入順序 | 判斷時最容易省略的事 |
|---|---|---|
| `happy` | `text: "ok"` → 有效完成 | 正常文字和完成事件都存在，所以應該成功；但這一題沒有碰到錯型 |
| `false-text` | `text: false` → `text: "after"` → 有效完成 | `false` 在 Python 是假值，不代表它在 R05 裡是合法的「沒有訊息」 |
| `continue-after-malformed` | `[]` → `text: "after"` → 有效完成 | 回報壞資料之後，是否仍讀取後面的有效事件 |
| `explicit-failure-priority` | `[]` → 根層 `error: "refused"` → `text: "after"` → 有效完成 | 出現順序與 exit 優先序不是同一件事；早到的 malformed 不能蓋過後來的明確失敗 |

「有效完成」在這四題都表示 `turn.completed`，`usage` 內有合法整數 `input_tokens: 10` 與 `output_tokens: 5`。依 R08，它會印出一個空行，再印出 `<!-- tokens: in 10 out 5 -->` 與換行。

### 一、為什麼 false 這題是 exit 6？

完整輸入如下。這裡故意在錯型之後放一則有效文字，讓我們分清「資料有問題」和「後面仍有可處理內容」。

```jsonl
{"type":"item.completed","item":{"type":"agent_message","text":false}}
{"type":"item.completed","item":{"type":"agent_message","text":"after"}}
{"type":"turn.completed","usage":{"input_tokens":10,"output_tokens":5}}
```

第一行依 R05 判斷：`false` 既不是字串，也不是 null，因此是 malformed。依 R03，stderr 要留下第 1 行的診斷，這一行不輸出訊息，程式仍繼續讀取。第二行是非空字串，必須原樣印出 `after`。第三行的 usage 有效，計為完成並印出 token 註記。

到 EOF 時，四個狀態是：沒有明確失敗、有 malformed、有有效完成、有有效訊息。R11 的優先序是 3 → 6 → 4 → 5 → 0，所以選 6。stdout 有內容並不會消除第一行的錯誤；exit 6 也不要求收回前面已輸出的內容。

用可看見換行的字串表示，預期結果是：

```text
stdout = "after\n\n<!-- tokens: in 10 out 5 -->\n"
stderr = "[codex malformed event] line 1: REASON\n"
exit   = 6
```

`REASON` 只需要是非空的單行原因。reference 實際使用 `text must be a string or null`；這是 fixture 的用字，不是規格要求。檢查器如果只接受這句話，就會替契約新增限制。因此本教學精確比對 stdout 與 exit，並比對 stderr 的完整格式、行數、行號與其他固定診斷，保留 REASON 的合法自由。

為了確認 oracle 沒有偷偷要求 reference 的用字，工作台另建立一份合法改寫，把原因換成 `invalid optional text: text`。它的診斷與 reference 確實不同，仍通過全部四個教學批次案例。這是正對照：評估器除了要拒絕已知錯法，也要接受規格允許的另一種寫法。

### 二、三個出口各自能辨識什麼？

先只執行 `happy`。reference、六份錯法與一份合法改寫全部通過，而且這裡已經比對三個出口。這說明只把檢查寫得精確還不夠，正常輸入根本沒有讓那些錯法露出差異。

再給前表的錯型與例外輸入，三個出口就各自有工作：

| 刻意錯法 | 指定案例 | 與契約不同的出口 | 少看這個出口會發生什麼 |
|---|---|---|---|
| 把非字串轉成字串 | `false-text` | stdout、stderr、exit | `false` 變成成功輸出的 `False`；任何一個錯誤出口都可指出問題 |
| 把假值當成沒有訊息 | `false-text` | stderr、exit | stdout 和正確結果相同，只讀審查內容看不出少了診斷 |
| malformed 後立即結束 | `continue-after-malformed` | 只有 stdout | stderr 的行號與 exit 6 都正確，卻漏掉 `after` 與 token 註記 |
| 明確失敗後仍回傳 6 | `explicit-failure-priority` | 只有 exit | 本教學變異刻意保留所有預期診斷，讓 exit 的錯誤單獨出現 |
| 漏印 malformed 診斷 | `false-text` | 只有 stderr | stdout 正確、exit 也已拒絕成功，但 R03 要求的追查資訊消失 |

這張表的錯法都是預先指定的測試裝置，不是從正式模型候選挑出的失敗。要引用時，應說「這個教學展示了某個觀察的辨識能力」，不能寫成「正式四十次出現了這種錯」。

### 三、三個出口都對了，為什麼仍可能違約？

第六份錯法把逐行迴圈改為先讀完全部輸入：

```python
# reference
for line_number, line in enumerate(sys.stdin, 1):

# 教學錯法：等 stdin EOF 才開始處理
for line_number, line in enumerate(sys.stdin.read().splitlines(True), 1):
```

對四個批次案例，它和 reference 的終態三出口全部符合預期。原因是批次執行已送完輸入並關閉 stdin；這時才讀結果，兩種程式都已取得整段事件，最後可以留下相同內容。

要看見差別，先送出 `text: "stream-before-eof"`，保持 stdin 開啟，要求讀到這行 stdout。之後才送完成事件並關閉 stdin。本機一秒觀察窗裡，reference 先印出了這行；整段緩衝的版本沒有。送完後，兩者的完整 stdout、stderr 與 exit 又完全相同。

這個例子需要新增的是**觀察時點**，不是再增加一個只看終態的案例。它也提醒我們，測試名稱叫 streaming 不會自動證明串流被驗證：要確認 driver 是否真的在 EOF 前讀過輸出。

一秒只是本教學的等待預算，不是契約的 production 延遲門檻。若忙碌主機讓 reference 都未能及時輸出，教學檢查會失敗，不能把它當成已辨識出某個模型問題。可用 `--stream-window-seconds 3` 重新查明本機時序；每次的觀察窗與結果都要一起保存。本例只檢查第一則有效訊息，沒有驗證後續訊息、command、token 或 stderr 的即時性。

### 四、變形測試的關係，也要從契約推導

變形測試會先改造輸入，再檢查新舊輸出應有的關係。它能減少逐案寫死答案的工作，但前提是那個關係本身正確；「看起來不影響意思」還不夠。

在 `false-text` 的輸入前面插入兩個空行。R02 要略過空行，所以有效事件與 stdout 不變，exit 也仍是 6。但 R02／R03 同時要求診斷使用實體行號，第一個 malformed 由第 1 行移到第 3 行。因此：

```text
錯誤關係：插入空行之後，三個出口全部不變。
正確關係：本例 stdout 與 exit 不變；malformed 的實體行號增加 2。
```

如果把錯誤關係當成測試，正確 reference 反而會失敗。不能為了讓這個測試變綠，就去修改 parser 的行號。需要退回檢查的，是測試作者對「不變」的定義。

再看重複事件。以 `text: "same"` 接一個有效完成作為片段，把整個片段送兩次。R13 禁止新增唯一性或 terminal-state 限制：重複訊息要各自印出，完成後的事件也要繼續處理。因此 stdout 片段會出現兩次，exit 仍是 0，stderr 仍空白。這個操作不是冪等；要求「重複輸入不影響輸出」，會錯誤排除契約明文允許、而且要求保留的行為。

兩個例子各指出一件事：變形關係要指定哪個觀察維持不變，也要交代哪些觀察必須跟著改變。它不能靠字面上的「忽略」或「相同事件」自動成立。

## 如何把這份示範用到自己的任務

可以從 [驗收義務表](obligations.md) 的空白模板開始。先寫一條要求要保護的行為，再列出一個符合要求的例子和一個能讓差異浮現的錯法。對每個錯法問：目前觀察的輸出、時間或狀態，真的能把它和合法實作分開嗎？

若兩者結果一樣，先查是案例沒有碰到邊界、觀察漏了一個出口，還是 oracle 本身錯了。前兩種要改案例或觀察方式；第三種要回到要求來源與負責人。不要只增加相似案例，也不要先假定被測程式應該改到通過。

最後保留差異的層次：本 workbench 的 26 項自我檢查與 3 項 oracle 單元測試，驗證的是這份教學裝置按預期工作。它們不是完整 R01–R13 的正確性證明，更不能加入正式研究的樣本數、案例數或模型成本。

初版的 23 項檢查與七份 fixture 紀錄保留在 [runs/initial-results.json](runs/initial-results.json)，相應程式在 [runs/initial-workbench.py.txt](runs/initial-workbench.py.txt)。目前版本追加合法 REASON 改寫，重新執行後為 26 項檢查；兩版不相加成新的研究樣本。
