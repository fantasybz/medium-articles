# 文章研究大綱修訂版：同一份規格，跑十次

> 2026-09-28 敘事修訂：全文已改以研究動機、三個研究問題與 R05 實例串接；現行篇名與敘事分工以[編輯 brief](same-spec-ten-runs/manuscripts/narrative-revision-brief.md)、[四篇全文與品質紀錄](same-spec-ten-runs/manuscripts/STATUS.md)為準。下方保留研究階段大綱，不回改凍結的研究設計。

> 修訂日期：2026-09-25。這是目前採用的研究與寫作骨架，取代[原大綱](../2026-09/2026-11-same-spec-ten-runs.md)的執行方案；原檔保留為歷史紀錄。本輪已完成 40 個正式名額、外部驗收及初步分析，取得第一手資料；本檔保留寫作骨架；四篇本機全文均已完成，入口、逐段潤飾與複核見[成稿紀錄](same-spec-ten-runs/manuscripts/STATUS.md)。實測結果、公開資料與重評狀態見[研究結果](../experiments/same-spec-ten-runs/RESULTS.md)，圖表見[本輪工件](2026-11-same-spec-ten-runs.figures.md)。
>
> 寫作依 [STYLE.md](../../STYLE.md) 與[當期風格摘要](style_brief.md)。本輪已完成的公開來源核對見 [evidence audit](same-spec-ten-runs/evidence-audit.md)，既有評審與方法修訂的逐項處置見 [review resolution](same-spec-ten-runs/review-resolution.md)。本研究依 repo research loop 的階段推進；實際使用 CLI／人工 adapter 的階段須如實記錄，不能稱為未曾呼叫的 native workflow 結果。

> 成稿階段補記：四份文件以共同 R01–R13 為基準，但 A0 的「不需新增 CLI 參數」與 A／B／C 的「新增 CLI 選項不在範圍內」強度不同，不能把原設計意圖當成已證語義等價。原始 packet 與結果保持不變，詳見[措辭限制](same-spec-ten-runs/manuscripts/packet-wording-caveat.md)。

## 一、研究問題與文章範圍

暫定總題為 **「同一份規格，跑十次：把驗收、實作差異與成本分開量測」**。保留「總論＋三部曲」，以同一個真實 repo 的小型維護問題串起規格、契約與重複執行。檔名中的月份是研究歸檔代號，不是發布承諾。

本輪要回答的是：對同一份已凍結的任務要求，獨立產生多份實作時，哪些產出能通過驗收，哪些結構差異仍然存在，取得這些產出花了多少資源。這三個問題需要各自的指標。通過驗收的兩份程式可以長得不同；兩份相同的程式也可能同時有錯。尚未量測人類理解與維護工作，就不能把較高相似度寫成較低維護成本。

這個問題已有相關研究。本系列不再主張首次量測同規格重複實作，也不再預設 spec、conventions 或 pattern 指引哪一種一定有效。本輪的貢獻目標是交付一套範圍清楚、保留失敗、可以重新執行、並對封存產出重新評分的 repo 實驗，以及能連回每份產出的判讀方式。

這裡的「同一份規格」指每個組內使用逐 byte 相同的 packet，獨立生成十次；跨組保留同一組規範要求，文件呈現不同。成本在本研究只指 token 與 provider 回報的牌價估計。

主讀者是已經使用 coding agents 的工程主管、Staff engineer 與測試工程師。他們需要知道新增一份規格或指引後，驗收結果與資源使用是否改變，也需要能辨識「工具執行正常」與「交付內容正確」的差別。總論的 TL;DR 與首段先說明：本輪量測單檔、單次、無工具的 Python 修補，不能代表大型架構設計、長時間 agent 自主工作，或所有 repo 的授權條件。

## 二、第一手案例：研究工具把非文字當成審查結果

正式 task 取自目前的 `medium-articles` repo，固定基底 commit 為 `37f6c0ce9b536f95132d5e01a387f380bbb9639c`，受修改檔案為 [research/scripts/codex_jsonl.py](../scripts/codex_jsonl.py)。它把 `codex exec --json` 的 JSONL 事件轉成審查文字與診斷，並以 exit code 協助呼叫端區分成功、失敗、中斷與沒有訊息。

這是已在基底程式重現的缺陷，不是模型實驗結果：輸入一行合法 JSON `[]` 或 `null`，程式會因假設最外層具有 `.get()` 而以 `AttributeError` 結束；輸入 `agent_message.text = 123`，再接正常 `turn.completed`，程式會印出 `123` 並回傳 exit 0。後者讓「JSON 可解碼」與「具有合法審查文字」混在一起。研究代理於 2026-09-25 重現時，以 `git show` 取得固定 commit 的原始檔，再由 subprocess 傳入固定字串，沒有修改正式 parser。

任務要求是把已知事件的 shape 驗證與終局判定寫清楚，同時保留正常 JSONL stream 的既有輸出與 streaming 行為。新增 schema anomaly 的 exit 6，終局優先序固定為 **3 → 6 → 4 → 5 → 0**。完整欄位規則與 legacy 相容範圍以實驗凍結的 spec／requirements 為準；本段不能取代逐項規格。

付款帳本、Go 的 `payment-timeout-fix` 與 Java/Spring event-sourcing 案例均不列入本輪正式研究。原創 fixture 可以協助檢查研究工具，但不計入模型實驗，也不稱為本 repo 的維護成果。

## 三、執行方案與可說的結論

### 1. 共同條件與四組文字介入

每次生成都取得相同基底 parser，使用固定 model、CLI、high effort、runner 提供的 system input（CLI 內建 context 不可見）、輸出 schema 與預算。候選模型不操作工具，也不讀取 repo；輸入是由 runner 明確組成的 packet，輸出是符合凍結 JSON schema 的單一候選檔案。所有生成程序結束後，runner 封存檔案並由外部 evaluator 統一驗收，hidden 結果不回傳模型，也不在同一名額追加修復對話。

這是**以真實 repo 任務為材料的 tool-free 受控生成研究**。B/C 的文字由 packet 明確提供，不依賴 CLI 自動載入 AGENTS.md 或原生 skill。它不能回答工具使用迴圈、hooks、MCP 或 native skills 的整體效果，也不能把其結果歸因於整個 coding-agent harness。

| Arm | 文字條件 | 可以比較的差異 |
|---|---|---|
| A0 | 精簡 spec，保留所有規範要求 | 與 A 比較同要求的說明套件，不是缺資訊的一句 ticket |
| A | 展開 spec，加入解釋與 examples | 完整說明的基準；examples 不新增 A0 未收到的要求 |
| B | 與 A 相同的完整 spec，加 rationale／checklist | 這份文字指引相對 A 的增量；不新增工具或權限 |
| C | B 的內容，加純文字 pattern 指引 | 這份 pattern 套件相對 B 的增量；不宣稱原生 skill 功能生效 |

A/B/C 的共同 spec 必須逐 byte 一致；A0 與 A 逐 requirement ID 核對覆蓋。A0→A 同時改變說明方式、examples 與長度，不能獨立歸因於字數。B/C 不能包含評估器答案、只有該組知道的秘密要求，或先前 run 的產出。

### 2. 名額、pilot 與凍結

正式計畫是 10 個排程區塊，每個區塊各有 A0/A/B/C 一次，共 **40 個預先排定名額**；區塊內順序事先隨機化，依序啟動，最多四個生成程序並行；工作程序空出後就啟動下一個名額，相鄰區塊可重疊，不是同步開始／結束的時間窗。不得先完成某組十次，再隔幾天執行下一組。另有 2 次 pilot，只檢查 transport、解析、封存、驗收與預算，不計入正式 40 次，也不代表四組都已通過模型驗證。

正式 collection 前要封存 task、四組 packet、model/CLI/runtime 身分、有效設定、輸出 schema、外部 evaluator、相似度 descriptor、預算、40 個名額及分析程式的版本與 hash。僅有本機 freeze 時，稱「執行前封存的研究協議」，不暗示第三方預註冊登錄。本文不另開前代 model 的 N=5 比較，也不根據結果把部分組追加到 N=30。

原始兩次 pilot 已確認 `claude-opus-5-5`、Claude CLI `2.1.282` 與 `high` effort 的輸出及驗收路徑。正式每名額上限 600 秒、CLI 牌價預算停止門檻 USD 5（可能在超過門檻後才停止，不是硬性金額上限）；token／sampling 使用 hosted CLI 可用的設定，沒有宣稱可固定 seed 或 temperature。正式以新的 freeze manifest 及實際 trace 為準。另行觸發的短逾時／低預算 operational probes 與原始 pilot、正式 40 次分開記錄。

### 3. 三個分開的完成欄位

| 欄位 | 定義與用途 |
|---|---|
| `cli_success` | CLI 未觸發預算停止且在時限內正常結束，且 model／tools／MCP／skills 等生成邊界符合凍結設定；沒有 transport、timeout 或 limit error；只回答生成程序是否完成 |
| `artifact_success` | 程序終止後封存的合法、完整單檔候選通過外部驗收；可能包含最多五秒終止寬限期的產出，不代表在時限內完成 |
| `accepted_completion` | `cli_success && artifact_success`；為本輪 primary outcome，每個排定名額都在分母內 |

驗收成功精確指通過凍結的 102 個批次案例與 1 個 EOF 前 streaming probe；這不證明所有可能輸入或每一項內部實作要求，例如是否保留名為 `main()` 的函式。fixture 與 mutation tests 是研究工具的檢查，不是模型或真人基準。

每組先報 `k/10`、termination 類型與 95% two-sided exact binomial interval，並交代共同機率與獨立性是假設，provider 漂移不會被「exact」消除。各組差異僅作描述，不預設哪一組較佳，也不設定優越或等效判定。排程區塊只用於交錯啟動的設計，不計算配對差值或檢定。

模型請求啟動後發生的 timeout、transport failure、schema failure 或操作者介入都保留，不補抽成功結果。評估器故障則標 missing/error；修復後須對全體 sealed snapshots 統一重評並留下 amendment，不把評估器壞掉算成候選失敗。model／設定／hash 不符時停止後續 collection，保留所有已執行記錄並說明 protocol deviation。

### 4. 結構與成本是另外兩張表

結構指標採正式凍結的 Python AST descriptor，只分析候選 parser。本輪採 node-type multiset cosine，名稱寫「AST 節點類型分布的 cosine」；不能稱為 tree-edit similarity。identifier-normalized AST hash 只能判斷正規化表示是否相同，不能提供距離或證明語義等價。解析失敗、空候選與不適用比較記 NA，保留理由。

另報每份候選相對凍結 seed 的 cosine，以及函式／class 數量，讓共享原始程式碼造成的天花板容易辨認。十份候選最多形成 45 個 pair；它們共享同一批 run，不是 45 個獨立樣本。矩陣與 median/min/IQR 是探索性描述，可分開列全部可解析產出與已通過驗收產出，後者須標明是成功者條件分布。單檔任務的檔案集合幾乎不會提供辨識力，不把 Jaccard 硬塞成第二個主指標。

本輪成本只指 provider 回報的 token 與 list-price 估計，並非實際帳單。資源表分 input、output、cache read/write、可取得費用與觀察 wall time；缺失留空並寫原因，不填零。中止名額已消耗的資源也計入。這些數字表示該固定預算下的實際使用量，不是被截斷工作最終完成所需的時間。相似度提高若沒有觀察到驗收改善，不能直接換算成 ROI。

本輪沒有真人校準或 human review 計時。兩份實作即使由真人提供也只形成一個 reference pair，不能稱為「校準帶」。AI 審查意見可協助研究品質檢查，但不替代人類 reviewer 資料。

### 5. 已取得的第一手觀察

2026-09-25 的正式資料已完整保留 40 個名額，A0／A／B／C 各 10／10 通過 `accepted_completion`；每份候選通過 103 項凍結檢查。沒有補抽、逾時、操作失敗或生成邊界違規。每組的雙側 95% Clopper–Pearson 區間都是 69.15%–100%，不足以作高可靠度或等效性結論。

四組各有 10 種不同的 identifier-normalized AST，組內 node-type cosine 中位數依 A0／A／B／C 為 0.995／0.997／0.998／0.996。高 cosine 與不同樹狀表示可以同時成立；共享 seed 及單檔任務可能造成高相似度。每組 45 個 pair 共享十份程式，不增加獨立樣本數。

正式 40 次 CLI 回報牌價估計合計 USD 5.692342，不含研究審查及開發請求，也不是實際帳單。本輪沒有組間 contrast 估計或品質／維護 ROI。完整數值、分母、hash、重評及限制統一引用[正式結果](../experiments/same-spec-ten-runs/RESULTS.md)，避免四篇文章各自手抄一份數字。

## 四、公開證據如何放進文章

正文僅使用已核對的少數來源，每份負責一個問題；精確版本、區間、限制及本機快照 hash 以 [evidence audit](same-spec-ten-runs/evidence-audit.md) 為準。

| 來源 | 在系列中的用途 | 不得延伸成什麼 |
|---|---|---|
| [2608.25399v1](https://arxiv.org/html/2608.25399v1) | 規格篇：規格資訊與成本、成本 spread 的關係；完整交代估計區間 | spec 對程式結構沒有影響、成本效果可跨所有模型外推 |
| [2607.02436v2](https://arxiv.org/pdf/2607.02436v2) | 總論：已有同 spec 重複生成、功能與結構分開量測的案例 | N=90 全是同組態、沒有人工修復、AST 相似度已代表維護品質；發布前仍核對 abstract/PDF metadata 差異 |
| [2609.12742v1](https://arxiv.org/html/2609.12742v1) | 變異篇：paired score 的小增益與 reroll noise 難以區分 | +4.9pp 是 resolve rate，或不顯著就等於 skill 無效 |
| [2609.11076v1](https://arxiv.org/html/2609.11076v1) | 契約篇：referee 獨立性、隔離 probe、amendment 與 halt 記錄 | 歷史 run 已完全隔離、成本比較等於品質改善、不同階段可合併成一個結果 |
| [2608.01347v6](https://arxiv.org/html/2608.01347v6) | 規格篇與變異篇：prompt、effort、harness 的交互作用與估計範圍 | 所有工具／架構任務效果相同，或低 token 就一定較有效率 |

原大綱其他 arXiv 數字、社群互動排名、跨 vendor 可攜性標題及 model 世代預測，均不再承擔本輪論證。未完成來源核對的材料可以保留在 research backlog，不能因為曾寫進 References 就沿用。

本系列與規劃中的「綠燈不是驗收」分工不同：後者處理驗收 gate 與 pass^k；本系列處理固定文件條件下的重複生成分布，`k/10` 不構成 production 擴權 gate。成稿跨篇連結使用確認過的篇名與發布連結。

## 五、總論骨架

暫題：**同一份規格，跑十次：把驗收、實作差異與成本分開量測**。總論的任務是讓讀者知道為什麼要重複執行，以及結果不同時應先問哪一個問題，不提前替四組宣布輸贏。

### 一、審查檔案有內容，為什麼仍然不能當作審查完成

以 parser 對 `text: 123` 回傳成功的重現開場。交代它在研究工具中的用途，再展示 exit 0 與合法文字不一致造成的判讀問題。這是 repo 可重現的 bug；不虛構某次真實事故、同事對話或損失。

### 二、同一個 task 有三種「不同」

用同一份 parser 候選說明驗收結果、實作結構及資源使用的差別。外部研究只負責證明這些結果已有不同量測方式，不能替本研究預告結果。Kahneman《雜訊》可作後續閱讀脈絡，但本輪不靠未核對頁碼的直接引文或法官對映承擔方法。

### 三、先把規格中的判斷寫完整

介紹 schema anomaly、既有 streaming 行為及 exit precedence 如何成為可判定要求。精簡與展開 spec 都必須交付這些要求；examples 的任務是澄清歧義，不是悄悄增加只有某組收到的驗收條件。完整範本與 requirement mapping 留給規格篇。

### 四、四組比較到底動了什麼

呈現四組文字條件與共同設定。解釋這次刻意縮成單次 tool-free 生成，目的是先觀察文件條件與產出的關係。不能把「模型沒有工具」寫成「已驗證 agent tool loop」，也不能把 C 的文字 pattern 簡稱為 native skill 的效果。

### 五、每一個名額都要留下結果

先展示計畫、啟動、正常結束、合法 artifact、驗收通過、缺失與 deviation 的 flow table，再帶讀者看每組的 `k/10`。採用本輪完整 40 個名額；四組各 10／10 的結果，必須連同區間下界及沒有組間優劣判定一起說明。

### 六、兩份程式長得不同，接下來檢查什麼

先看差異是否對應契約失敗；契約都過時，描述 AST 指標能看見與看不見的東西。選展示案例須交代選取規則，不只挑最像或最不像的 pair。沒有人工設計評分時，不把模組數不同、自動比對分數較低直接稱為壞變異。

### 七、如果我是工程主管，我會如何使用這份證據

可以用這種實驗檢查小型維護流程是否值得進一步研究、找出驗收的缺口、估計完整執行的資源。不能用 N=10 的相似度為 production write tools 擴權，也不能拿其他 repo 的數字替自己作判斷。要擴大範圍，應另選多種 task 並設計下一輪，而不是只替紅燈組追加到 N=30。

| 結果情境（不是預測） | 讀者可做的下一步 |
|---|---|
| 四組全數通過 | 本次驗收無法區分組別；考慮另訂更廣任務的研究，不能宣告等效 |
| 某組多次失敗 | 先核對 requirements 與 evaluator，再依該組具體失敗決定是否採用文件 |
| 驗收通過但結構不同 | 描述差異；沒有人工維護資料就不評定好壞 |
| 評估器故障或 generation boundary 失效 | 停止、保留所有名額，依 amendment 處理，不發布完整效果結論 |

每組 10/10 的雙側 95% exact 下界約 69.15%；這個解析度不足以支撐高可靠度或微小差異排序。

### 八、結語回到 parser 的 exit code

回到開場：外層程序完成、合法產出、通過契約，都要分開留下證據。重複執行讓我們看見一次 demo 隱藏的分布；能下多大的結論，仍由 task、介入、驗收與樣本決定。本節待實測完成後按實際結果收束，不預寫「conventions 有效」「skills 收斂」或「越像越好」。

## 六、第一篇骨架：同樣要求，怎麼寫成可比較的 spec

暫題：**同一份規格，跑十次（一）：規格篇—先確認四組收到相同的要求**。

### 一、從真實 bug 寫出可驗收的目標

給讀者基底 parser 的兩個反例與正常輸出的例子，說清楚這次要修的是 shape validation 和 exit 判斷，不是重做整個研究流程。明定可修改檔案、stdlib 與 API／streaming 相容範圍。

### 二、exit code 是行為契約的一部分

解釋 3、6、4、5、0 各代表什麼，以及同一串流可能同時出現多種訊號。優先序不是數值大小，必須有文字規則與可執行 cases；例如 schema anomaly 不能蓋掉明確 error event 的 exit 3。

### 三、給規格作者：A0 可以短，但不能少掉要求

以 requirement coverage 對照 A0/A，逐項核對已知事件 shape、輸出規則、錯誤診斷與終局優先序。展開版本用 examples 解釋容易誤解的地方，不能多出另一套功能。這是本篇主要決策工件。

### 四、rationale 與 pattern 分別添加了什麼

B 說明為什麼要分開辨識、驗證、輸出及結束判定；C 提供固定的文字 pattern。具體內容以 freeze packet 為準，不能在這裡替 C 填參考實作。說明這些是作者選擇的文件套件，不是所有 conventions／skills 的代表。

### 五、規格也有維護成本，但本輪沒有量人時

由規格與成本研究帶出「內容、effort 與 runtime 可能交互作用」，再回到本實驗能取得的 tokens／費用／時間。沒有記錄寫 spec 的工時、理解負擔與重做時間，就不報人的 ROI。需求後續變動則記版本與 amendment，不寫成需求總是晚到的普遍定律。

### 六、結語：先守住可比較，再談哪一組較好

本篇交付的是完整 task spec、四組差異與 coverage 檢查。它們讓〈契約篇—由外部驗收每一份候選 parser〉能驗收相同要求；本次沒有觀察到驗收結果的組間差異，仍不能宣布厚度無用或 pattern 必要。

## 七、第二篇骨架：把 parser 的契約放在生成之外

暫題：**同一份規格，跑十次（二）：契約篇—由外部驗收每一份候選 parser**。

### 一、JSON 解碼成功之後，還有 shape 與語義

用固定案例區分 malformed JSON、合法 JSON 錯型別、已知事件的非法欄位，以及合法 stream。舊 parser 如何處理 malformed JSON 與未知事件，必須逐項寫入相容規範，不能靠「fail closed」口號讓正常輸入全面退化。

### 二、三個 success 欄位各自回答不同問題

用 `cli_success`、`artifact_success`、`accepted_completion` 說明生成程序、輸出 schema 與候選行為三層。避免「CLI 回傳 0，所以 parser 正確」這種外層綠燈覆蓋內層失敗的情況。

### 三、給測試工程師：讓 evaluator 保有自己的規則

候選只收到凍結 packet，輸出只允許一個檔案。外部 driver 保存案例、expected stdout/stderr/exit 與 frozen evaluator；candidate process 只取得該次 JSONL input。驗收不執行候選修改的測試腳本，也不讓候選讀到整份 hidden suite。

### 四、隔離要有 probe，驗收工具也要有反例

說明 tool-free 生成仍須查明 CLI 的全域指引／設定來源，候選 Python 執行也仍須 sandbox。使用正確、錯誤、超時及越界 fixtures 檢查 evaluator 是否依預期分類；這些 fixture checks 是研究工具的驗證，不是 40 次模型結果。

### 五、保留 streaming 的行為，不能只比最後一行

正常 agent message 的文字與順序、command 註記、token summary、stderr 診斷及 exit code 都依 spec 驗證；需要逐行即時輸出的要求由實際 streaming 測試確認，不能只把整串 stdin 一次送完便宣稱驗過 flushing。具體已驗證項與尚未涵蓋項列在實驗 artifact。

### 六、結語：契約通過，仍不代表量完所有品質

parser 契約只能證明已定義的行為及禁止事項，不能證明語義完全等價或未來不會出錯。新發現的 evaluator 缺陷要留下 amendment、對所有候選一致處理，不選擇性把某組改到過關。

## 八、第三篇骨架：四組十次，把完整分布交出來

暫題：**同一份規格，跑十次（三）：變異篇—從四十個名額讀懂結果與限制**。

### 一、先公開研究協議，再看結果

列固定 commit、task、文字條件、model/CLI/runtime、budget、隨機區塊與 freeze 時點。把兩次 pilot 與正式名額分開，交代 pilot 修改了哪些工具或規格。若沒有第三方預註冊就不使用容易誤導的登錄描述。

### 二、給研究結果的簽核者：把四十個名額逐一交代

先報 flow table，再報每組 accepted completion 與區間。所有 failures、limits、usage missing、model drift、evaluation errors 都可追到原始記錄；遇到 boundary breach 或身分／hash 不符而停止則報 incomplete study，不把實際少量資料改稱完整 N=10。

### 三、哪一條 parser 契約最常失敗

按照 requirement ID 彙整 shape、precedence、legacy 和 streaming 的驗收結果，說明分母是 run，不是 assertion 數。只有看過完整資料後才選出主要失敗模式，不能事先預定 C 最懂規則。

### 四、通過的實作還差在哪裡

以已凍結 descriptor 展示成對矩陣與少數可追溯 diff。指出 shared baseline、node-type representation 及單檔 task 的限制。這一節描述差異，不把較相似的組視為最好的組，也不從 hash 相同推語義等價。

### 五、資源使用與是否交付放在一起看

報包括失敗在內的資源分布，必要時另列成功者條件分布。只報各組預先指定的摘要，不估計組間 contrast；費用／效益分母為零或缺失時，不硬算「提高 0.1 相似度的價格」。沒有 reviewer 資料就不列 review minutes。

### 六、這個小實驗沒有解答什麼

本輪只選一個單檔任務，且模型沒有工具；選題者也參與規格制定。固定 effort、provider 不透明、小樣本與 AST 代理指標，進一步限制結果的外推。沒有觀察到差異只能說本次資料未提供足夠區分能力，不能寫四組等效或某種文件無用。

### 七、結語：下一個決策由結果決定

若主要問題是驗收缺口，以 amendment 修正 evaluator，再對全部封存產出一致重評；若都是正常候選，再研究更難或更廣的 task；若某組相似度較高，但 accepted completion 沒有較高，就保留這個有限結果。後續研究須另訂 protocol，不以模型世代、架構品質或授權判斷替本篇擴充結論。

## 九、必要圖表：先定資料需求，不畫結果

全系列先保留五個圖表工件。主代理在 protocol 與結果確定後補 figure plan；本檔沒有 Mermaid 已算繪、PNG 已驗證或正式結果圖的宣稱。

| 工件 | 要讓讀者看懂什麼 | 所需資料與製作條件 |
|---|---|---|
| F1：生成、封存、外部驗收三階段示意 | CLI 正常退出與 artifact 通過是不同判斷 | 依實際 runner/evaluator 畫無數值流程；標出 hidden boundary，不以單向箭頭暗示已證完全隔離 |
| T1：四組文字差異與 requirement coverage | 哪些要求相同，哪一段是介入 | frozen specs、coverage 與 packet hashes；先用文字表，不放效果方向或推薦顏色 |
| T2：parser exit precedence／streaming contract | 同時出現不同事件時如何判斷 | 正式 requirements、cases 與 expected outcomes；只列規範，不填模型結果 |
| T3：名額 flow 與 arm outcome 表 | 成功、失敗、缺失與成本的分母 | 正式 ledger、evaluation 與 usage records；沒有資料時保留欄位，不造 `0/10` 或預期值 |
| F2：探索性結構矩陣或代表 pair 的 diff | 哪些程式差異被 descriptor 看見 | sealed candidates、metric version、有效 pair／NA 理由；用同一候選 ID 連回契約結果，45 pairs 不當獨立 n |

圖表前交代讀法，圖表後說明它能支持的判斷與未回答的問題。正式成稿遵循 repo 圖表規範；若尚未完成結果圖，就保持研究草案，不把原大綱通過 render 的舊圖當成本輪驗證成果。

## 十、研究迴圈與成稿門檻

| 階段 | 本輪要留下的工件 | 何時可說完成 |
|---|---|---|
| 問題與來源 | 真實 bug 重現、五份 source audit、claim／issue ledger | 原站與主張對得上，未核對來源退出 active claim；A2 metadata 差異仍須保留處理紀錄 |
| 方法審查 | 本大綱、review resolution、正式 protocol | 每個評審項有處置；刪除不受測的目標，未完成執行不標已解 |
| 工具與 pilot | frozen seed/packets/evaluator、隔離 probes、2 次 pilot | 工具結果可追溯；pilot 與正式目錄分開，freeze 在首個正式 request 之前 |
| 正式執行 | 40 個排定名額、sealed artifacts、完整 usage/status | 所有名額有狀態；未啟動／中止則明列，不補抽、不篩選成功者 |
| 分析與反方審查 | 結果表、探索矩陣、deviations、獨立 review | 圖表回算到原始資料；估計對象／樣本／區間一致，負結果保留 |
| 成稿與發布 | 四篇正文、References、中英對照及發布包 | 全篇包括後半部與結語均守證據邊界；按 PUBLISHING 流程生成，無結果不冒充完成稿 |

每篇成稿保留「系列文章」「References」「AI 協作說明」尾段；寫明哪些工件由 AI 建立與審閱，生成模型與 Claude 審查同屬一個模型家族，不能稱真人或不同家族的獨立驗證。

本輪不預排發布日期，也不因「最高標準」而補造真人參與。研究結果與四篇中文全文（本機稿）均已完成，正文、圖表與貼稿已複核，不能寫成已遠端發布。英文版與社群 hooks 不在本次範圍；若後續製作，仍須保留相同限制與資料，發布安排另定。
