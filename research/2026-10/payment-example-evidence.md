# 第四篇〈付款實作篇〉：研究、實測與取捨

更新：2026-09-25。這是作者要求的系列擴寫，依 [research loop](../README.md) 做定向蒐集、證據整理、獨立質疑、修訂與雙語交付；不重新執行整月選題，也不假造社群支持或發布日期。

## 問題與文章安排

作者要求以「購買無糖純喫綠茶」完整解釋三種選擇：從 Review 留下哪些 constraint tests、依風險選誰審閱哪些內容、選哪些程式與 mutant 來檢查測試保護力。依作者要求，系列採用「總論＋四部曲」，共五篇文章。既有總論與前三篇各補對應段落，第四篇〈付款實作篇〉保留連續的契約、程式、實驗與判讀。中英文共十份原稿同步更新；第四篇尚未排程，不指定發布月份。

付款場景、35 元新台幣售價、Review 評論與 owner 角色均為教學設定。程式以伺服器已授權、不可變訂單為前提，使用標準函式庫與假金流，沒有真實帳號、網路或扣款。沒有將示範寫成作者親歷的事故。

## 一手來源與證據界線

下列網頁均於 2026-09-25 使用 gstack browse 閱讀。只保留公開來源的摘要與連結；原始擷取內容不納入 Git。

| 來源 | 類型與直接支持的內容 | 本次如何使用／不能推出什麼 |
|---|---|---|
| [Stryker: Mutant states and metrics](https://stryker-mutator.io/docs/mutation-testing-elements/mutant-states-and-metrics/) | 工具官方定義。detected 包含 killed、timeout；有效但未覆蓋的 mutant 仍在一般分母；compile/runtime error 與 ignored 另有分類 | 實作篇 §6–7 說明不能任意刪除分母。本例採遇執行錯誤即中止的保守 runner，不宣稱複製 Stryker 的完整分類 |
| [Stryker: Equivalent mutants](https://stryker-mutator.io/docs/mutation-testing-elements/equivalent-mutants/) | 官方文件以具體例子說明等價與辨識限制 | §6 要求以可觀察行為與輸入範圍提出理由；沒有測到不能當等價證明。不保證能自動判定所有等價變異 |
| [Stripe: Idempotent requests](https://docs.stripe.com/api/idempotent_requests) | 官方 API 契約。相同 key 可重用已開始執行請求的結果，參數須符合；key 至少保存 24 小時後可能清除 | §1、9 區分本地去重與 provider 契約、保存期限。本例不串接 Stripe，不套用其狀態名稱或宣稱永久 exactly-once |
| [Stripe: Handle errors](https://docs.stripe.com/error-handling) | 官方整合建議。連線錯誤結果不確定，可查詢／接收 webhook；在其冪等契約下可用相同 key 重試 | §1 修正「逾時就一律不能重試」的過度推論。教學程式保留 PENDING 是有限範圍內的保守策略，不是一般金流規則 |
| [AWS Builders’ Library: Making retries safe with idempotent APIs](https://aws.amazon.com/builders-library/making-retries-safe-with-idempotent-APIs/) | 業者第一手設計經驗；request ID 的意圖、相同 ID 不同參數、晚到請求與保留期限 | §9 補足識別與生命週期問題；不是付款系統的共同標準，也不代表記憶體實作已具備分散式保證 |
| [Google: What to look for in a code review](https://google.github.io/eng-practices/review/reviewer/looking-for.html) | 官方工程指引：設計、功能、測試、逐行理解受託範圍、閱讀更大脈絡及專門能力 | §2 支持審閱範圍與能力的原則；三種付款責任分工是作者建議，不是 Google 的三人政策 |
| [Petrović et al.: Practical Mutation Testing at Scale: A view from Google](https://research.google/pubs/practical-mutation-testing-at-scale-a-view-from-google/)（2021） | 第一手工業研究；本輪讀取 Google Research 的論文摘要，非付費全文。摘要說明變更範圍 mutation、過濾、依歷史算子表現選擇 | §6 支持成本與可採取行動的結果一起考量。未引用未讀全文的統計、因果結論，也不把研究當 70% 或七個手選 mutant 的驗證 |

## 自行執行的證據

完整程式：[examples/tea_payment](../../examples/tea_payment/README.md)。
逐項結果：[observed-mutations.json](../../examples/tea_payment/observed-mutations.json)。

```bash
python3 -B -m unittest discover -s examples/tea_payment -p 'test_*.py' -v
python3 -B examples/tea_payment/mutation_demo.py
```

| 選擇 | 原始程式通過的方法數 | killed／納入計分 | 分數 | 存活者 |
|---|---|---|---|---|
| functional | 2 | 2／7 | 28.6% | M2、M3、M4、M5、M7 |
| without-timeout | 8 | 6／7 | 85.7% | M5 |
| full | 9 | 7／7 | 100.0% | 這七個都被辨識 |

分母固定七個人工指定、可執行且有行為反例的變異，排除數為零。上面的 discover 命令共執行 21 個測試：九個付款測試另有十二個 runner 回歸測試；後者不計入付款測試數，也不計入 mutant 分母。未測量 agent 重複生成、constraint pass rate 或 pass^k，沒有 production 成效資料。

runner 先檢查 baseline，逐一在暫存目錄載入 mutated module，核對三種選擇模式的測試數與逾時測試名稱；並非逐一鎖定所有測試身分。import／執行錯誤、skip、數量不符、逾時測試缺失或改名及 subprocess timeout 會中止，不當作 killed。報告保留斷言失敗的測試 ID，不包含斷言訊息。M5 的 timeout 是應用程式情境，和 mutation runner 執行超時不同。

## 獨立 Review 與修正

依作者要求，Claude Code 以唯讀、無工具的獨立審閱方式，檢查完整程式、文件與實際輸出。Codex 負責執行、判讀與修正；未把模型的推論冒充執行紀錄。

1. 第一輪指出：呼叫 provider 前的 PENDING 紀錄沒有對應的非逾時例外測試；timeout 測試改名可能悄悄改變 suite；載入環境可能使 runner 選到原始模組；timeout 只涵蓋扣款後；假金流 capture 斷言的證據界線需說清楚。
2. 修正：新增 M7 與非逾時例外測試、扣款前後兩種 timeout subtest、固定命名與方法數、隔離 Python 環境、驗證模組路徑，並增加四個防止假證據的 runner 回歸測試。第一版六個 mutant 的數字不再作為目前文章的結果。
3. 第二輪確認以上修正，另指出 decline 後重送尚未直接驗證、規則文件仍殘留只測扣款後 timeout 的描述。已在原 decline 測試中加入重送，確認結果相同且 provider 只呼叫一次；修正文案，保持九個付款測試與七個變異的分母。輸入空 key 的 guard 不在本實驗範圍，README 明確揭露；runner 的路徑與選擇保護改用明確錯誤，不依賴可停用的 assert。

4. 第三輪複核確認 N1–N6 均已處理，判定在教學範圍內 PASS；測試與實際 JSON 的逐項結果一致。另補齊 C3 與 M2 的對照及 runner 中止條件說明。

5. Ship 的獨立覆蓋檢查再補八個 runner 回歸測試：測試 error、expected failure／unexpected success、數量漂移、原始 baseline 失敗、變異目標缺失／不明確、子行程逾時與完整 JSON 報告。共有十二個 runner 測試，付款測試仍為九個，七個 mutant 的結果不變。

6. 最後一輪獨立複核確認十二個 runner 測試與雙語編修，另指出中文把 M5 的變異動作與測試替身製造逾時混為一談。已改為「M5 改的是付款程式收到 `TimeoutError` 時的處理」，與英文和程式一致。

7. 獨立的來源稽核逐一對照七份原始擷取內容，確認引用支持本文主張；Google mutation 研究的驗證範圍仍限於公開摘要，沒有延伸成全文已讀。最後也把「我執行」改成實驗已實際執行的中性敘述，不把 AI 執行的命令寫成作者親手操作。

8. Claude Code 使用 `--effort max` 的複核判定教學範圍 PASS，另指出三項證據精確度：M2 的多個失敗測試會掩蓋個別斷言被刪除；簡化 runner 的 survived 包含沒有執行到的分支；runner 的檢查範圍與 JSON 內容不可寫得比實作更廣。已在雙語正文、README 與規則對照補足說明，刪除中文「九個測試才辨識出」的必要性暗示。Codex 在隔離副本把 C1 重送與 C2 換 key／改訂單內容三個測試改為 `pass`，實際重跑確認 21 個測試仍通過，三組 kill 集合與 28.6%／85.7%／100% 不變；逐項失敗測試名單有改變。正式範例保留全部斷言。

9. 針對上述三項精確度修正，Claude Code 再以 `--effort xhigh` 對照程式、雙語段落、README、規則文件與主機提供的實驗結果，確認內容一致並判定 PASS；沒有將這次無工具審閱寫成重新執行。

這些修正的意義，是讓獨立 Review 擴大可觀察的風險，再用可重跑測試確認，不是累積模型的 approve 數量。

## 編輯與交付檢查重點

- 總論把三道閘交接到同一筆付款，並澄清 Review 可以在最終核准前提早確認約束。
- 測試篇補 M5 的實際程式變異、固定分母與 85.7% 仍缺關鍵保護的案例；70% 保留為作者起始參考。
- Review 篇補角色／hunk 選擇、評論取捨與責任紀錄；沒有把檔名或 35 元單價當風險分級。
- 可靠度篇修正功能測試與 constraint tests 互斥的說法；補行為案例，區分方法數、mutant 數、候選修補與 agent 嘗試。
- 實作篇完整保留假金流、單行程、依序呼叫的界線。並行、持久化、provider idempotency、對帳、webhook、授權、退款與實際交付都需要另外的證據。
- 兩種語言保留相同條件、數字與未完成範圍。既有八篇排程不改，第四篇〈付款實作篇〉只建立中英文草稿，不補造日期。
