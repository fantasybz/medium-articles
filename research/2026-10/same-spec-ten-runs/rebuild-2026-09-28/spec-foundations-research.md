# 規格與契約基礎研究：從「文件比較」改成「讀者怎麼作決定」

研究日期：2026-09-28（Asia/Taipei）。本報告是全面重寫的研究紀錄，不是系列正文。所有外部頁面均透過獨立的 gstack `/browse` 讀取；PDF 由同一工具下載後，使用本機 `pdftotext -layout` 讀取。來源全文快取保留在本機研究工作區，不隨本報告公開；存取時間、版本、查證章節與快取 SHA-256 見 [來源台帳](spec-foundations-source-ledger.json)。本報告沒有修改正式實驗封存，也沒有執行新一輪模型生成或新增驗收實驗。

## 一、目前稿件最缺的，不只是更多資料

現稿把 A0、A、B、C 的內容、103 項檢查與四十次結果說得更完整了，但讀者仍先被要求理解研究方法，最後才收到文件維護建議。「綠燈不是驗收」系列則先讓讀者辨認：眼前要作什麼決策：哪一種證據不足、下一步由誰補、補到什麼程度才能改變決定。

這一輪基礎資料指向一個可貫穿四篇的問題：**當程式可以反覆生成，團隊究竟有哪些決定不能交給下一次生成重新猜？那些決定要怎麼保存、檢查與修改？**

規格的價值因此有三層，不能只量測 prompt 長短：

1. **找出還沒決定的事。** 使用者想要的行為、相容責任、例外政策尚未確定時，模型幫忙補成流暢的文件，可能只是把問題藏起來。Example Mapping 的關鍵正是把規則、例子與未決問題分開。
2. **保存已作出的選擇，同時留下合法的實作自由。** 哪些是使用者／呼叫端依賴的外部行為，哪些只是方便實作的建議？RFC 2119 甚至明說，不應用規範詞強加與互通無關的方法；Lamport 談非形式規格時，則從使用介面需要哪些知識出發。
3. **讓選擇可以受到反駁。** 把規則變成檢查後，還要知道檢查漏掉什麼、是否誤禁合法實作。Property、metamorphic relation、mutation 分別提供不同角度，不能合併成一個「多加測試就好」。

本案正式研究預先完成 R01–R13，模型不能提問或執行測試。因此它觀察的是「既有決策如何被不同文件交代，以及一次生成留下什麼」，**沒有測得規格探索如何改善產品決策，也沒有測得互動式 agent 的整體工作流程**。把這條界線寫清楚，能讓研究成為較大工程問題的一個具體觀測，而不是整個系列的全部世界。

## 二、八組值得真正進正文的來源

### S1｜Lamport：spec 首先是讓人把問題想清楚的工具

- **一手來源：** Leslie Lamport，*Why We Should Build Software Like We Build Houses*，作者存檔標示 24 January 2013，PDF pp. 1–3。[作者 PDF](https://lamport.azurewebsites.net/pubs/wired.pdf)；[作者書目與版本說明](https://lamport.azurewebsites.net/pubs/pubs.html#wired)。書目說這是作者保留的最後版本，可能就是 Wired 當時刊出的版本；不要宣稱已核對出版社版。2015 的擴寫版 *Who Builds a House without Drawing Blueprints?* 未成功取得全文，不混用兩版。
- **問題／機制：** 寫下 spec 迫使作者在改碼前說清楚程式應做什麼；它也把使用介面所需的知識從「必須讀懂實作」移到可維護的說明。作者把形式化視為一個連續光譜，多數簡單方法用非形式文字就能說清楚；若某個部分微妙或關鍵，才值得使用更精密的方法與工具。
- **何時適用：** 相容性修補、交接、重新產生實作、需要跨人員保留理由的介面。對 parser 而言，`null` 在每個欄位的含義與 exit 優先序，就是下一位維護者不能從「型別修補」四字猜出的知識。
- **反例／限制：** 這是作者的工程立場與個人經驗，不是比較試驗；不要把文中修改 180 行所花的工時變成規格投資報酬率。作者自己也說，寫規格不保證程式不會 crash，仍需要消除 coding bug 的方法。
- **改變讀者動作：** 開始改碼前，請介面使用者回答「僅閱讀這份說明，不讀實作，能否知道怎麼使用與何時不能信任輸出？」答不出來的部分，先記成未決問題，不要先擴充文件字數。
- **具體產物：** 一頁「呼叫端需要知道的行為」：輸入類別、可觀察輸出、失敗／部分輸出的意義、相容承諾、允許自由、未決問題。這是本報告建議範本，非 Lamport 原文範本，也尚未在團隊實測。

### S2｜Example Mapping：不知道 Then 時，先承認這是一個問題

- **一手來源：** Matt Wynne（Cucumber project lead），*Introducing Example Mapping*，8 December 2015。[原文](https://cucumber.io/blog/bdd/example-mapping-introduction/)。核對章節：How it works、Instant feedback、Benefits、Friends episodes、Known unknowns、`Who should come?`、`So when do we write Gherkin?`
- **問題／機制：** 將 story、規則、具體例子、沒人能回答的問題分開。例子用來發現規則含義，問題用來顯示仍欠缺誰的知識或決定。作者指出，討論是為了讓團隊共同理解完成條件，不必在探索會議中立刻寫成完整 Gherkin。
- **何時適用：** PM、developer、tester／維運人員對「合理」各有解釋；legacy repair 有不漂亮但既有人依賴的行為；agent 要求更多上下文，團隊卻不確定缺的是資訊還是決策。
- **反例／限制：** 把未知 outcome 寫成某個測試的 expected value，並沒有解決未知。也不必每條大家已理解的規則都強造例子。原文的 25 分鐘是作者實務建議，不是實驗證明的最佳時長；本文不需重複成績效數字。
- **改變讀者動作：** 以 `text: null`、`text: false`、`text: " "` 為例，先問三者各意味什麼、誰能批准差異；再討論如何表達給 agent。若呼叫端要「沒有訊息就等下一段」，而測試作者把 false 也當成缺值，應先釐清契約，不能把這當模型表達能力問題。
- **具體產物：** 規則／例子／問題／決定者四欄的小表。每個未決問題要有負責回答的人與暫行假設；不能讓一份完整排版的 SPEC.md 看起來已替人作出決定。正式 A0–C 已預先回答這些問題，故此產物是研究前後的工程實務延伸，非本輪的觀測結果。

### S3｜BCP 14：規範強度與實作自由要分開

- **一手來源：** Scott Bradner，RFC 2119 *Key words for use in RFCs to Indicate Requirement Levels*，March 1997，§§1–7；Barry Leiba，RFC 8174 *Ambiguity of Uppercase vs Lowercase in RFC 2119 Key Words*，May 2017，§2。[RFC 2119](https://www.rfc-editor.org/rfc/rfc2119.html)；[RFC 8174](https://www.rfc-editor.org/rfc/rfc8174.html)。
- **問題／機制：** 必須、建議、可選各自允許不同的選擇；SHOULD 容許有理由的例外，但要理解其後果。2119 §6 說明規範詞應審慎使用，不應用來強加與互通無關的方法。8174 補充只有採用該慣例的大寫關鍵詞具有其定義；沒有這些詞的文字仍可能是規範。
- **何時適用：** API、通訊協定、相容責任，以及範例寫法容易被誤當硬要求的 agent 指引。C 提供 helper pattern，並不把 helper 名稱或類別配置變成契約。
- **反例／限制：** 不能反推「沒有 MUST 就不是要求」，RFC 有其 IETF 語境，不能自動成為每份 repo 文件都必須遵守的標準，也不能將 C 的 lowercase optional 字眼當成它已正式採用 BCP 14。
- **改變讀者動作：** 審查規格差異時，不應停在 requirement ID，還要逐項問「這個改寫縮小／放寬了哪一種合法選擇？」A0 的「不需要新 CLI 參數」與 A 額外的「新 CLI 選項不在範圍」正好是待處理例子。
- **具體產物：** 可接受行為／禁止行為／可選建議對照表；每項要求同時附「一個應拒絕的實作」與「一個應接受、但採不同寫法的實作」。後者防止 oracle 偷偷把示範程式當唯一答案。

### S4｜Hypothesis：測很多輸入前，先檢查是否測對了 domain

- **一手來源：** Hypothesis team，文件版本 **6.168.2**，*Quickstart* 與 *Domain and distribution*，頁面沒有獨立出版日，本次 2026-09-28 擷取。[Quickstart](https://hypothesis.readthedocs.io/en/latest/quickstart.html)；[Domain and distribution](https://hypothesis.readthedocs.io/en/latest/explanation/domain.html)。核對：Write your first test、Running in a test suite、Filtering inside a test、Dependent generation；`How should I choose a domain for my test?`、`Okay, but what is the distribution?`
- **問題／機制：** property 規定某類輸入應滿足的關係，strategy 說明可以生成哪些輸入。文件區分 domain 與生成機率分布：使用者負責選 domain，Hypothesis 的分布以找到 bug 為目標，並不模擬真實生產流量，也不均勻抽樣。
- **何時適用：** 單一例子之後仍有許多組合、空值／邊界值、輸入順序或資料形狀。parser 可以把「非 null 的非字串 text 都應 malformed」轉成多種類 JSON 值，檢查數值、bool、陣列與物件，而不只重播 `123`。
- **反例／限制：** 若 strategy 只生成字串，就永遠找不到 false 被錯當空值；若先 `assume(text)`，就可能把最需要的假值排除。測過一萬個輸入也不能當作一萬次生產成功率樣本，因為產生的分布不是 production distribution。限制過度也可能排除 bug-triggering 值。
- **改變讀者動作：** reviewer 同時審 property 與 generator：規則有沒有漏？domain 是否把最危險的值排除？生成的 case 若失敗，能否保留最小重現？不要只看 test count。
- **具體產物：** 要求→輸入 domain→必須成立的關係→可接受例外→最小反例表。依測試需要選擇生成器，並記錄未納入的輸入範圍；不能把此延伸描述成本輪 103 項凍結檢查已使用 Hypothesis。

### S5｜1998 原始 metamorphic testing：一個成功例子還能追問什麼

- **一手來源：** T. Y. Chen、S. C. Cheung、S. M. Yiu，*Metamorphic Testing: A New Approach for Generating Next Test Cases*，Technical Report **HKUST-CS98-01**，1998。作者 HKUST 頁面提供原始 PDF。[PDF](https://www.cse.ust.hk/~scc/publ/CS98-01-metamorphictesting.pdf)；[作者書目](https://www.cse.ust.hk/~scc/publ/publ.html)。核對 §1（pp.2–3）、§2（p.3）、§3.1（pp.4–5）、§3.4（pp.8–10）、§4（pp.10–11）。原件為舊 PDF，文字擷取數學符號有亂碼；本報告不用擷取後的公式逐字引用。
- **問題／機制：** 一次沒有揭露錯誤的成功輸入，仍可用其輸入／輸出與領域知識設計 follow-up case，尋找原案例未暴露的錯誤。原文用 binary search 與線性方程等例子，說明目前答案看似正確，經有意義的轉換後仍可能暴露錯誤。
- **何時適用：** 精確答案難取得，但多次相關執行間有已知關係；或已有有限 fixtures，想追問「換掉不該影響結果的部分，還成立嗎？」它是其他測試策略的補充，不要求先廢棄已有 oracle。
- **反例／限制：** 關係來自領域知識，不是「改輸入而預期不變」的萬能公式。1998 報告主要呈現動機與例子，作者明說完整方法論仍待發展；不要把它說成大型實證研究。production 執行的 follow-up case 也不能任意改動真實資料。
- **改變讀者動作：** 先寫 source input、transformation、允許改變的輸出、必須維持的輸出與適用前提，再讓 agent 實作 relation check。
- **具體產物：** 本案可用「插入空行」的關係審查，見下一節。最重要的教學不是產生更多 case，而是讓讀者發現一個看似合理的 relation 為何違反既有契約。

### S6｜PIT：殺死 mutant 是測試的訊號，不是替分數湊滿

- **一手來源：** PIT maintainers，*Basic Concepts*，未標頁面日期／版本，2026-09-28 存取。[官方文件](https://pitest.org/quickstart/basic_concepts/)。核對 Mutation Operators、Mutants、Equivalent Mutations、Running the tests。
- **問題／機制：** 在實作中施加小變化，觀察原測試是否會失敗。官方示例把 `>=` 改為 `>`，使邊界上的不同能驗證測試是否真正區分行為；執行到一行不代表 assertion 能察覺錯誤。
- **何時適用：** 已有全部通過的測試套件，仍想知道它對特定錯誤是否有保護力；尤其適合本案真實邊界：bool 是否誤算 int、空白字串是否遭 trim、exit 優先序是否反轉、flush 是否失去。
- **反例／限制：** 存活的變化可能是語義等價，或差異不在本次測試的契約範圍。PIT 也區分 Survived、No coverage、Non viable、Timed Out、Memory error、Run error。這些不能全都叫模型答錯，也不能為殺光 mutant 而把 REASON 固定成規格未要求的字句。
- **改變讀者動作：** 每個存活 mutant 都先作分類：真的破壞要求但測試沒看到？合法差異？無效變體？執行工具問題？必要時補規格或檢查，留下處理理由，不以總分取代審查。
- **具體產物：** 人工選擇、逐項對應 requirement 的 fault matrix，包含「應殺死」與「應放行」兩種對照。本案是 Python，PIT 是 Java bytecode 工具，正文不能暗示已直接以 PIT 驗收 parser；這裡借用官方定義與失敗分類，實作工具需另選。

### S7｜Claude Code 現行實務：spec、執行回饋與 reviewer 是不同工作

- **一手來源：** Anthropic，*Best practices for Claude Code*，動態官方文件，無獨立出版日期，本次 2026-09-28 擷取。[文件](https://code.claude.com/docs/en/best-practices)。核對 Give Claude a way to verify its work；Explore first, then plan, then code；Write an effective CLAUDE.md；Let Claude interview you；Add an adversarial review step；Avoid common failure patterns。
- **問題／機制：** 官方工作流先理解現有程式、再規劃與實作；較大的 feature 可透過訪談找出邊界與取捨，將 spec 留成獨立、可引用的產物。可執行的 check 讓 agent 看到結果並修正；fresh-context review 再依要求找真正缺口。
- **何時適用：** 實際 coding-agent 工作流；與本研究 tool-free one-shot 形成明確對照。讀者可以用本研究學到如何辨認文件差異，卻不能直接把成本與成功率搬到可查 repo、可跑測試、可澄清需求的 session。
- **反例／限制：** 官方同頁警告，過長 CLAUDE.md 會讓重要指令被噪音淹沒；應觀察改動是否真的改變行為。文件亦警告「被要求找缺口」的 reviewer 傾向提出缺口，追逐所有意見會過度工程化。以上為廠商實務建議，沒有本文可引用的隨機比較效果量；新 context 也不代表完全獨立的知識／訓練來源。
- **改變讀者動作：** 持久專案指引、單次 feature spec、執行 check、核准／review criteria 分開維護；每份說明有清楚用途。只針對違反 correctness 或 stated requirement 的 review finding 必修，風格偏好留作選擇。
- **具體產物：** 任務交付紀錄最少保留 requirement revision、檔案／介面範圍、out-of-scope、驗證指令與輸出、未解問題、review finding disposition。工具命令會變，正文宜講判斷鏈與官方入口，避免把版本特定指令鋪成大篇幅操作指南。

### S8｜2026 MT／LLM 研究者觀點：連測試關係本身也會幻覺

- **來源性質：** Zheng Zheng、Zenghui Zhou、Yinwang Xu、Daixu Ren、Tsong Yueh Chen，*Bidirectional Empowerment of Metamorphic Testing and Large Language Models: A Systematic Survey*，**arXiv:2605.13898v1，12 May 2026**。[全文](https://arxiv.org/html/2605.13898v1)。採用作者在 §6.1 討論的方法論，以及 §6.3 提出的研究議題，**不把它引用的他人實驗數字當本輪一手證據**；它是 preprint survey，HTML 還有 placeholder DOI，不宣稱已正式刊登 CSUR。
- **問題／機制：** 用 LLM 產生 metamorphic relation 可以降低手工成本，也會產生看似合理、實際不必要或不成立的關係；太弱漏錯、太強誤報。自然語言改寫也可能改變語用或任務條件，不能假設所有 paraphrase 都保持語義。
- **何時適用：** 自動產生 tests、agent 自動提出 invariants、規格改寫等價性檢查，尤其適合本系列對 A0/A 的語義差異討論。
- **反例／限制：** 檢查兩份產出是否一致，不等於確認兩份都正確； stochastic system 的一次 relation violation 也可能混有正常變異。文中建議的人工、constraint、多模型檢查是研究方向，並非已證明其中任一種可以消除此問題。
- **改變讀者動作：** agent 提出一條 property 後，先要求它列出「什麼時候不成立」與一個反例，再由領域負責人確認前提。測試 relation 的有效性要獨立記錄，不能因它已跑成綠燈就視為既定規格。
- **具體產物：** relation assurance card：來源條文、source/follow-up、前提、允許差異、反例、誰批准、目前覆蓋缺口。這個範本是編輯建議，沒有宣稱為論文原有工具。

## 三、一組能把 how 寫深的連續 worked example

以下全是依已凍結 R01–R13 推導的**教學／驗證設計建議，尚未執行的新實驗**。不可寫成正式四十份候選的發現。

### 1. 從 caller 的判斷起，而不是從 Python 型別起

caller 想取得一份可使用的審查。parser 會提前送出 stdout，所以「螢幕上有字」不足以表示最後成功；要連同 exit code 判讀。本次修補不應允許數字 `123` 被當成有效審查，也不能為了拒絕這一行，漏讀後來真正的遠端失敗。

這裡先有兩個產品／相容選擇：怎樣算有效訊息、什麼失敗要主導最終狀態。決定後才有 R05 與 R11；型別檢查是實作這些選擇的手段。這一段能讓讀者知道為什麼要有十三條看似瑣碎的規則。

### 2. 用例子暴露規則，再把未知交給有責任的人

| 例子 | 現行凍結契約的決定 | 決策含義 |
|---|---|---|
| `text: null` | 沒有訊息，不算 malformed | 呼叫端仍需等其他事件 |
| `text: false` | malformed，不能當空訊息 | 合法 JSON 型別不等於合法 domain 值 |
| `text: " "` | 有效訊息，原樣印出並計為發言 | 保留 legacy 相容；不能順手替 caller 改政策 |
| malformed 之後又收到 `turn.failed` | 最終 exit 3 | 較早發生的錯型，不能遮住後來的明確失敗 |

若讀者自己的 repo 對空白訊息沒有政策，表格第三列應先是問題卡；不能照抄本案的答案。要求、理由、例子三者要能分別指出出處。

### 3. 審查關係本身，而不只是執行它

有人可能提出：插入空行不應影響 parser，因此原始與變換後的 stdout、stderr、exit 全部相等。這條 relation 太強。R02 忽略空行的事件效果，R03 卻用實體行號報告錯型位置。

正確設計有兩條路：若只想用相等比較，先把 domain 限制為不含 malformed 的串流；若要涵蓋 malformed，就保留 stdout／exit 的相等關係，並按插入位置調整後續 diagnostic line number 的預期。這也示範 property 與 generator 必須一起審查：前提藏在 generator 裡，讀者才知道全綠代表什麼。

另一個誘人的錯誤關係是「重複同一事件不應改變結果」。R13 接受重複，並不是去除重複；重複有效訊息應印出兩次。若 agent 生成了冪等測試，再把實作修到符合，反而破壞規格。

### 4. 用故意犯錯和合法改寫一起挑戰 oracle

| 受控改變 | 預期判斷 | 檢查目的 |
|---|---|---|
| 將 text 型別檢查改成 truthiness，讓 false 靜默消失 | 應拒絕 | R05 錯型是否有診斷與狀態效果 |
| 對非空 text 呼叫 strip | 應拒絕 | 空白、內嵌內容是否原樣保留 |
| usage 用 `isinstance(n, int)`，未排除 bool | 應拒絕 | Python 型別繼承是否誤穿 domain 規則 |
| 移除 stdout flush | 若結果因此未在 EOF 前出現，streaming probe 應拒絕 | 終態內容正確仍可能漏掉時序要求；不能以沒呼叫特定函式本身判錯 |
| EOF 將 malformed 放在明確失敗之前 | 應拒絕 | 需有兩者同時出現的 trace 才能辨識優先序 |
| 將合法單行 REASON 改成另一句合法說明 | 應接受 | oracle 是否偷加精確措辭要求 |
| 從 dict 狀態改成 `_State` 類別，外部行為一致 | 應接受 | 合法內部設計自由是否真的存在 |

若前五種錯誤未被辨識，先檢查是測試輸入未觸及、assertion 沒看到、還是測試工具本身出錯；若最後兩種被拒絕，則應檢查 oracle 是否比規格更窄。這比「103 項都過」更能教讀者如何衡量契約的保護力，但必須實際執行才可報結果。

## 四、建議寫進系列的讀者決策方法

這是本報告的綜合建議，非任何一篇來源提出並驗證的統一框架。

| 症狀 | 待查證據 | 可調整的決定 | 尚不能推論 |
|---|---|---|---|
| 人對 null／空白有不同期望 | 問題卡、caller 與相容責任人說明 | 決定政策、切分 scope、暫停未決部分 | 模型只要讀更長的 spec 就會懂 |
| 規格有要求，候選做錯 | 最小輸入、實際輸出、對應條文、候選路徑 | 補例子／理由、改執行回饋、修實作 | 只由一行錯碼推知模型漏讀或誤解 |
| 測試全綠，人工仍能提出錯誤行為 | 一個破壞要求但被放過的 mutant | 擴充觀測面、修 oracle 或補缺漏要求 | 加測試數量就代表更可靠 |
| 兩份候選內部結構不同 | 相同契約結果、change task、review 維護資料 | 決定是否有必要加架構限制 | AST 差異就是不穩定／品質差 |
| 文件變長且成本上升 | 分清內容差異、tool 使用、task 難度、人工作業成本 | 測試特定文件改動是否值得保留 | 字數造成成本；最短版本全情境最佳 |

給不同角色的交付物可以很小：負責需求的人留下未決問題與相容決定；實作者拿到行為要求及可選設計；tester 維護反例與可觀察結果；reviewer 確認限制有理由，並分類存活 mutant；EM／Staff 再依實际返工與審查時間，決定要投資哪一個環節。不要在本文直接發明「90 天即可省多少」的承諾。

## 五、寫作位置與研究界線

- **總論：** Lamport／Example Mapping 提供 why，再把研究界線放進「產品決策→可交代規格→外部證據→可重複觀測」的脈絡。不要先列模型、effort、hash 才解釋這些對人的意義。
- **規格篇：** 先示範規則、例子與未知的分辨，再展示四份真實 spec 如何處理已決定的要求；BCP 14 用來解釋規範強度與實作自由，並連到 A0/A 已知措辭缺口。A0 不是無規格 baseline，必須保留。
- **契約篇：** 保留已有 `123 → exit 6` 的清楚推導，但向外多走一步：何謂足夠的觀察、合法自由、property 前提、oracle 自測與 mutant disposition。正式 103 項、既有工具自測、後續建議實驗必須分欄。
- **變異篇：** 先問哪種差異會改變 reader 的 release／維護決策，再介紹 AST/cosine。多樣實作可能是契約容許的自由；是否增加維護負擔，要另有 change task 或人類 review 資料，不能靠圖表自動推出。
- **數字節制：** 這八組來源不需要再堆任何效果百分比。重點是新增判斷方法、可執行反例、責任界線。2026 MT survey 的 93 studies、Example Mapping 的 25 分鐘、Hypothesis 預設樣本數都不是本文需要借來增加權威的數字。

## 六、取得失敗與未採用項目

- Michael Jackson *The World and the Machine* 原作者 Open University 網站失效／TLS 失敗，ACM DOI 頁被 403 擋住。本輪沒有驗證全文，**不可由記憶補引其段落或公式**。
- Lamport 2015 CACM 擴寫版被 403 擋住，採用成功取得的 2013 作者存檔，明確標示版本。
- QuickCheck 作者首頁取得成功，原 manual 連結正文為空。本輪以 Hypothesis 官方具體文件支撐可操作細節，不宣稱讀了 QuickCheck 2000 原始論文。
- 最初猜測 HKU 的 1998 PDF 路徑失敗；後來從共同作者 Cheung 的 HKUST 書目找到正確原始技術報告，已保存可核對版本。
- Spec Kit 當日 README 取得成功，但由 root 另行研究現行 SDD 工具，不在本報告重複擴張工具清單。

## 七、可供改寫的交付物

[規格修改卡](spec-change-card.md) 提供已填寫的 parser 假設案例、可填空範本與 CSV 轉用示例。卡片把未決需求、規範、理由、自查及可選寫法分開，並連到獨立比較計畫；它是設計範例，尚未有介入效果的觀察結果。
