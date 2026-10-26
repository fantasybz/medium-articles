# Codex review — 2026-11-aaif-agent-memory/article.md

> model: gpt-6.1-sol, reasoning: xhigh, 2026-10-25 22:47. 原話照錄，未經摘要。審的是 2026-10-25 改寫後的版本。

我會先讀 STYLE.md 與 style_brief.md，再核對本文引用的簡報、程式快照和前作。全程只讀取此 repository 內的資料，不修改檔案；無法核實的內容會明確標出。
<!-- codex ran: /bin/zsh -lc 'pwd && cat STYLE.md && cat research/2026-10/style_brief.md' -->
<!-- codex ran: /bin/zsh -lc "rg --files -uuu .context/research/aaif-2026-10-23 .context/research/aaif-2026-10-25 | rg '(transcript|slides/text|memory|airas|crab|LONGMEM|consol -->
<!-- codex ran: /bin/zsh -lc "rg --files -g article.md -g AGENTS.md -g '*memory*' -g '*airas*' -g '*crab*' 2026-11-aaif-agent-memory 2026-10-green-* 2026-11-same-spec-* 2026-09 -->
<!-- codex ran: /bin/zsh -lc 'rg --files -uuu .context/research/aaif-2026-10-23/slides/text && nl -ba 2026-11-aaif-agent-memory/article.md' -->
<!-- codex ran: /bin/zsh -lc 'cat .context/research/aaif-2026-10-23/slides/text/2WZJf-01-crabrag-graph-memory-for-ai-assistants-v0-6-agntcon-japan.txt' -->
<!-- codex ran: /bin/zsh -lc 'cat .context/research/aaif-2026-10-23/slides/text/2QlDp-01-agentmemory-agntcon-mcpcon-opening.txt' -->
<!-- codex ran: /bin/zsh -lc "rg --files -uuu .context research 2026-11-aaif-agent-memory | rg '(memory|airas|anthropic|context-engineering|evals|shibuya|provenance|70517|e1c37 -->
主線的缺口已經出現：第六節要驗的是「更正後，下一個 agent 會不會改判斷」，但前文多次岔到搜尋、分類與一般 eval。核對時我會分清哪些問題必須補論證，哪些只是重複或錯引。
<!-- codex ran: /bin/zsh -lc 'cat .context/research/aaif-2026-10-23/slides/text/2QlDp-01-agentmemory-agntcon-mcpcon-opening.txt' -->
<!-- codex ran: /bin/zsh -lc 'cat .context/research/aaif-2026-10-23/slides/text/2RqMK-01-agnt-con-2026-v7.txt' -->
<!-- codex ran: /bin/zsh -lc "rg --files -uuu .context/research/aaif-2026-10-24/third-article -g '"'!pptx-preview/**'"' | rg '(benchmark|readme|manifest|web/.*text|source)' | r -->
<!-- codex ran: /bin/zsh -lc "cat .context/research/aaif-2026-10-24/third-article/airas-readme.md && rg -n 'LongMem|recall|500|48|95.2|86.2|Lifecycle|reinforc|decay|supersed|co -->
<!-- codex ran: /bin/zsh -lc 'cat .context/research/aaif-2026-10-24/third-article/agentmemory-code/consolidation-pipeline.ts && cat .context/research/aaif-2026-10-24/third-arti -->
<!-- codex ran: /bin/zsh -lc "rg --files -uuu .context/research/aaif-2026-10-25 | rg -v '(before|after|snapshots|screenshots|images|\\.png|\\.jpg)' | head -n 140 && cat researc -->
<!-- codex ran: /bin/zsh -lc "rg --files -uuu .context research -g '*.txt' -g '*.md' -g '*.json' | rg -v '(before|after|revision|snapshots|review|superseded|pptx-preview|public -->
<!-- codex ran: /bin/zsh -lc "sed -n '1,175p' 2026-10-agentic-harness-blueprint/article.md && sed -n '1,155p' 2026-11-agentic-eval-economics/article.md" -->
<!-- codex ran: /bin/zsh -lc "rg -n -A 18 -B 8 'Kubernetes|1.30|1.31|PagerDuty|黃金|人工標記|每一層|CrabRAG|Chin|skill' 2026-11-aaif-agent-handoffs/article.md 2026-11-aaif-after-tokyo/a -->
<!-- codex ran: /bin/zsh -lc "rg -n '"'^## |''^### |oracle|holdout|保留|校準|預設|撤回|判準'"' 2026-11-same-spec-overview/article.md 2026-11-same-spec-contract/article.md 2026-11-same-sp -->
<!-- codex ran: /bin/zsh -lc "rg -l -uuu -g '*.md' -g '*.txt' -g '"'!**/before/**'"' -g '"'!**/after/**'"' -g '"'!**/diffs/**'"' -g '"'!**/publication/**'"' -g '"'!**/review/** -->
<!-- codex ran: /bin/zsh -lc "rg -l -uuu -g '*.json' -g '*.html' -g '*.txt' -g '*.md' -g '"'!**/before/**'"' -g '"'!**/after/**'"' -g '"'!**/snapshots/**'"' -g '"'!**/review/** -->
已核對三份簡報的主要頁碼、Agent Memory 的欄位更新與刪除程式，以及 AIRAS README。95.2%／86.2% 與其檢索指標的界線有來源支持。目前較實質的缺口是：正文沒有處理程式實際如何判斷記憶被「取代」，驗收設計也尚未區分是哪一段流程讓更正生效。
<!-- codex ran: /bin/zsh -lc "sed -n '1,82p' 2026-10-green-review/article.md && sed -n '220,330p' 2026-10-green-reliability/article.md && sed -n '232,258p' 2026-11-same-spec-va -->
<!-- codex ran: /bin/zsh -lc "sed -n '85,180p' 2026-11-aaif-agent-memory/article.md && sed -n '1,180p' .context/research/aaif-2026-10-24/third-article/agentmemory-code/hybrid-s -->
<!-- codex ran: /bin/zsh -lc "sed -n '330,390p' 2026-10-green-reliability/article.md && sed -n '232,258p' 2026-11-same-spec-variance/article.md && sed -n '21,44p' 2026-11-same- -->
<!-- codex ran: /bin/zsh -lc "rg -n -m 20 'LongMem|95.2|86.2|500|48|recall_any' .context/research/aaif-2026-10-24/third-article/agentmemory-readme.md research/2026-10/aaif-agnt -->
<!-- codex ran: /bin/zsh -lc "rg --files -uuu -g '*LONG*' -g '*longmem*' -g '*context-engineer*' -g '*alake*' -g '*W2HV*' -g '*Q0Vkg*' -g '"'!**/site-packages/**'"' . && python -->
<!-- codex ran: /bin/zsh -lc "cat .context/research/aaif-2026-10-24/third-article/agentmemory-longmemeval.md && python3 -B -c 'import json,pathlib; s=json.loads(pathlib.Path(\" -->
<!-- codex ran: /bin/zsh -lc "rg --files -uuu .context/research/aaif-2026-10-23/sources .context/research/aaif-2026-10-24/third-article/web | sort && sed -n '330,390p' 2026-10- -->
<!-- codex ran: /bin/zsh -lc "nl -ba .context/research/aaif-2026-10-24/third-article/agentmemory-code/consolidation-pipeline.ts | sed -n '92,165p' && nl -ba .context/research/a -->
<!-- codex ran: /bin/zsh -lc "rg -n 'frozen|holdout' 2026-10-green-reliability/article.md && rg -n 'context|Context|Attention|attention|rot' .context/research/aaif-2026-10-24/t -->
找到一處明確的 recall 錯置：《Harness 藍圖》第二節的三層是 Org／Repo／Dir，依適用範圍與維護責任區分，並非本文所說的「常駐指引／單次交代」。另外，Agent Memory 的清理程式會依文字相似度與建立時間停用舊記憶；這與正文「較新不代表較正確」的建議直接相關，應拿出來分析。
<!-- codex ran: /bin/zsh -lc "rg -n -m 8 'Effective context engineering|attention budget|context rot|W2HVdB4Jbjs|Architecting Agent Memory' research/2026-10/aaif-agntcon/multis -->
前作回扣已核對完。契約篇的 oracle、變異篇的 holdout、可靠度篇第五節的引用方向相符；但本文把「題目已用來調整系統」和「題目全過、指標飽和」接成同一件事，推論不成立。AAAI 的數字也對得上，但原圖標的是 reviewed papers，本文改寫成了「投稿量」。
已依序讀完兩份風格文件，僅核對 repository 內材料，未修改檔案。

## 致命問題

1. **二、〈先分清這一輪要讀的，和要留給下次的〉：把前作寫成它沒有說過的分類。**

   > 「我在〈Harness 藍圖〉第二節把 AGENTS.md 分成三層維護，區分的也是同一件事：哪些是每次都要載入的常駐指引，哪些是單次任務的交代。」

   [原文第二節](/Users/kochi.chuang/conductor/workspaces/medium-articles/dodoma/2026-10-agentic-harness-blueprint/article.md)分的是 **Org／Repo／Dir 的適用範圍與維護責任**，不是常駐／單次。這是錯引。改成：「那篇依適用範圍分配文件維護責任；現在要追問，自動抽出的經驗由誰確認適用範圍、負責撤回。」常駐文件與單次交代的區分，應接《同一份規格，跑十次》總論第二節。

   同段的「**因為沒有人替它分層**」也應刪除。第四節自己就介紹了分類與整理程序；真正缺的是責任與驗證，不是完全沒有人或程序分類。

2. **五、〈讓更正沿引用關係，傳到下一份摘要〉→六、：沒有定義「更正完成」。**

   > 「若暫時無法重建，就先標為待更新，讓檢索不要把它當成目前有效的相容性依據。」

   「標記」不會自行讓所有搜尋入口停止提供舊結論。本文承諾的是下一個 agent 的判斷改變，卻沒有交代：主紀錄已撤回、索引尚未更新時，誰負責攔住舊摘要？

   補一個最小契約：更正指向固定判定 ID；資料服務查核目前有效版本；衍生摘要完成重建前不得作為有效依據；程序中斷後可繼續處理。第六節再加入「只完成一半更新就開始查詢」的案例。否則這套設計只能驗順序正常時的更正。

## 重要問題

1. **四、〈更新與遺忘，要讓下一次檢索真的不同〉：避開了程式最值得分析的反例。**

   > 「較晚出現的筆記可能只是重貼舊內容，較高的文字相似度也不會告訴我們哪個說法符合現況。」

   但你核對的 [auto-forget.ts](/Users/kochi.chuang/conductor/workspaces/medium-articles/dodoma/.context/research/aaif-2026-10-24/third-article/agentmemory-code/auto-forget.ts:95)，會比較共用 concept 的候選；詞集合相似度超過 0.9 時，將建立時間較早者設為 `isLatest=false`。這不是語義上的矛盾驗證。

   應直接分析這個落差：兩句只差否定詞的長敘述可能高度相似；較新的文字也未必有較新的證據。明確分開「簡報描述的生命週期」「此版本的判定捷徑」「作者建議的更正規則」。目前只是把原則再說一次，沒有追到設計代價。

2. **四、〈反覆出現的說法，還需要新的查核〉：來源欄位的限制沒有追到底。**

   > 「真正支持結論的可能仍只有最早那次測試演練。」

   [consolidation-pipeline.ts](/Users/kochi.chuang/conductor/workspaces/medium-articles/dodoma/.context/research/aaif-2026-10-24/third-article/agentmemory-code/consolidation-pipeline.ts:132)還有更直接的問題：新 fact 的 `sourceSessionIds` 填入整批近期摘要的 session IDs；相同 fact 再次出現時，該分支沒有補入新的來源關聯。

   補一句關鍵推論：**列出來源場次，不等於知道哪一段觀察支持哪一個 fact。** 接著說明需要保存逐項支持關係，否則後面「沿引用關係更正」缺少可用的起點。

3. **六、：比較設計沒有隔離會自行改變的記憶狀態。**

   > 「更新前後都分別開兩個新工作階段。」
   >
   > 「先只改記憶材料或取回方式。」

   新工作階段不等於新的記憶儲存狀態。前一次查詢若會增加計數、留下摘要或觸發整理，後一次就不再只差指定的更正。

   每次試行應從同一份記憶快照開始；固定目前環境、索引版本與資料權限，明訂是否允許自動寫入。要測取回，就固定寫入結果；要測更新流程，才開放相應寫入。否則失敗與改善都難歸因。

4. **六、：把 holdout 污染與指標飽和接成同一件事。**

   > 「這批驗收題目一旦用來調整記憶系統，就不能再當成沒看過答案的保留題；Anthropic 的 eval 文章說得更直接，一組全過的題目只能擋回歸，提供不了改善的訊號。」

   「說得更直接」不成立。前者是題目已參與調整，後者是成功率沒有上升空間。未見題也可能全過；已污染題也可能尚未全過。

   拆成兩個判斷，分別接變異篇第八節與 Anthropic 的 saturation 說明。「提供不了改善訊號」也應限於已飽和的成功指標，不能涵蓋查核時間、成本等所有結果。

5. **五、導讀第二段：數字相符，量測對象被改寫。**

   > 「AAAI 的投稿量從 2020 年的 7,737 件長到 2026 年的 23,680 件。」

   第 17 頁標的是 **papers reviewed**。不能自行改成投稿量。改為「簡報列出的已審稿件數」，並把「審稿人力跟不上」保留為講者提出的瓶頸判斷，不當作這兩個數字直接證明的事實。

6. **三、〈把時間與適用範圍放進關係裡〉：skill 段同時錯置因果與主線。**

   > 「skill 一多就難挑：沒有對應 skill 時直接停住、選錯 skill 卻自信執行、skill 之間接不起來。」

   第 12–14 頁是適應、選擇、組合三種問題，不能都歸因於數量增加。

   > 「而情境就是關係。」

   情境還包含目標、時間、權限與未確認事項。改成「關係是描述情境的一部分」，或直接刪除整段，讓第三節結尾交出真正的下一題：「對象找對了，整理後的敘述仍可能把觀察寫成更大的結論。」

7. **四、〈先分清要保存的經驗，以及這一輪要讀的內容〉；六、：兩處轉場只有換題，沒有交棒。**

   > 「檢索時再選擇這次需要的部分。」

   前面在談保存哪些經驗，這裡突然進入 BM25、RRF 與 benchmark。先提出尚未解決的問題：「有效更正與常被引用的舊摘要一起存在時，哪一份會先回來？」搜尋機制才有用途。

   > 「這個案例走完後，再把其他情境分開……」

   刪除與權限案例突然加入。先交代：內容有證據，仍可能已被要求刪除，或不應提供給目前角色。否則「可信」在這裡悄悄換了意思。

## 次要問題

1. **二、：把 context 寫成整輪工作的固定輸入。**

   > 「模型每次處理工作時能讀的輸入有容量限制，這份輸入叫 context。」

   Agent Memory 第 4 頁說的是每次 model call 組裝 context。補明「同一任務內也會多次組裝」，避免讀者把工作階段、context 與長期記憶當成三個固定容器。

2. **二、：context rot 被寫成逐 token 必然發生的機制。**

   > 「每多放一個 token，模型對其他內容的注意力就少一點。」

   改成「輸入變長時，模型找出並使用相關資訊的表現可能下降」。不要把工程上的注意力預算比喻寫成逐 token 的定量規律。本輪未取得 [1] 完整原文，不能把這句標為已逐字核實。

3. **三、〈相似性把材料找出來，關係把問題接起來〉：把講者的示意故事寫成搜尋方法的普遍邊界。**

   > 「相似度只給最近的東西，從不給通往它的路徑。」

   加上「單靠一次向量近鄰搜尋」。向量搜尋可以搭配欄位篩選與其他查詢程序；問題是單一相似度不足以代表關係，不是所有使用向量的系統都做不到。

4. **四、〈先分清要保存的經驗，以及這一輪要讀的內容〉：秘密與可壓縮資料混在一起。**

   > 「丟掉或壓縮秘密、沒有教訓的原始 log……」

   改成「秘密不應進入記憶；其他低價值內容則略去或壓縮」。壓縮秘密不等於移除秘密。

5. **〈資料與方法註記〉：搜尋結果被升格成不存在的斷言。**

   > 「截至 2026-10-25，AAIF 官方頻道尚未上架這三場的東京錄影。」

   repo 的研究紀錄自己限定為「未建立對應」，不是證明不存在。改成「本次查找未找到能確認對應這三場的東京錄影」。

   其餘主要核對結果：95.2%、86.2%、500 題、約 48 場次及指標定義有本地來源；主要引用頁碼相符；9 月 12 日 Facebook 貼文日期相符。本文沒有 timecode。MongoDB 延伸影片的內容範圍仍未由本輪逐字稿核實。

## 建議刪除

以下段落沒有增加判準、證據或新的問題。

| 位置 | 應刪或縮併的原句 | 具體處理 |
|---|---|---|
| 一之前〈系列導覽〉 | 「本文沿用《綠燈不是驗收》的證據觀點……」後接五篇連結 | 開頭保留本系列導覽。前作在真正使用其判斷時連結，避免先交一份閱讀清單。 |
| 一、首段及三張連續照片 | 「第一張裡……另兩張把視線帶回城市……」 | 保留一張澀谷照；刪除另外兩張的逐景介紹。它們沒有改變記憶問題。 |
| 二、context 段末 | 「MongoDB 的 Richmond Alake……可作延伸觀看。」 | 移到 References。正文沒有使用它補任何推論。 |
| 三、〈把時間與適用範圍放進關係裡〉末段 | 「第一篇提過，Chin 在同一場也用三張投影片說明 skill……」 | 刪除；它把已建立的版本與來源問題拉回工具挑選。 |
| 四、第一個 H3 首段 | 「這與第二節引用的 Anthropic 文章說的是同一套做法。」 | 合併兩處 compaction 說明，不必再宣布兩份材料相同。 |
| 五、導讀第二段後半 | 「我在《綠燈不是驗收》Review 篇寫 PR 審閱時遇到的，是同一個瓶頸換了產業。」 | 若不展開責任與查核分工，連同 AAAI 數字段刪除。這只是相似性 recall。 |
| 七、首段 | 「燈籠、牆上的字與日期，替澀谷夜景補上了所在的位置。」 | 展景沒有推動最後的判斷。照片可留作尾圖，刪除解說段。 |
| 七、第二至四段 | 「這次最值得接著追的……」「三篇東京筆記走到這裡……」「我會先挑一項……」 | 分別重播第一節、系列總覽與第六節。三段縮成一次收束，留下讀者接手後要改變的決定。 |

## 建議補充

1. **TL;DR→一、→六、：把核心問題提前，停止輪流回答三個不同版本。**

   > 「記憶的價值在於幫接手者作出有根據的決定。」

   這句太廣，前兩篇也成立。直接使用第六節的問題：

   **「一項經驗被換了環境、發現漏驗或正式更正後，下一個 agent 還會不會沿用原結論？」**

   第三節處理是否適用於同一對象；第四節處理記錄如何改變；第五節處理改判的依據；第六節觀察改變是否抵達回答。每段只需負責其中一步。

2. **三至五、：補足各場在條件改變後的成本。**

   | 場次與原句 | 缺少的推論 |
   |---|---|
   | 三、〈把時間與適用範圍放進關係裡〉：「持續維護關係的價值才會增加。」 | 反向追查可以用資料表連接處理。選 graph 的理由還需對照查詢形狀、關係變動與維護成本。給出先用既有資料表、何時才值得增加圖形儲存的選擇條件。 |
   | 四、〈反覆出現的說法，還需要新的查核〉：「未來不用重讀每個過程。」 | 摘要省下讀取成本，也丟掉細節。哪些事實可以壓縮、哪些例外必須保留來源入口？用報表未驗收這個例子，說明一次過度抽象如何增加後續查核成本。 |
   | 五、〈在結果出現前，先決定怎樣才算有支持〉：「先決定怎麼驗證，再產生可驗證的主張。」 | 預先定義能限制事後改口，也可能漏掉有價值的新發現。補明：原主張照原標準判定；新發現另立主張與驗證，不回改原紀錄。再交代 verifier 的規則與權限由誰維護。 |

3. **五、〈讓更正沿引用關係，傳到下一份摘要〉：給一份可以照著建立的記錄。**

   > 「新增一份指向原判定的更正紀錄。」

   至少列出：判定 ID、對象與版本、驗收要求版本、支持的觀察、目前狀態、取代哪份判定、確認人、受影響摘要。用本文的報表案例填一筆，標為假設資料。

   第六節就能核對這筆記錄是否正確儲存、取回、載入與引用，而不是再讀一遍原則。

4. **二、五、六、與〈延伸閱讀〉：讓 recall 改變本篇的設計。**

   > 「這延續〈綠燈不是驗收〉的問題……」

   目前多數回扣停在共同立場。應改成以下具體承接：

   | 前作核對結果 | 本篇應增加什麼 |
   |---|---|
   | 《同一份規格，跑十次》契約篇第二節的 oracle 說明相符 | 記憶不只保存「通過」，也保存哪個 oracle 版本判定通過。正文補章節連結。 |
   | 變異篇第八節的 holdout 引用相符 | 更值得帶入的是「改量尺、改產物、改方法，要重查不同東西」。對應到保留原始觀察、重評舊判定與重新執行任務。 |
   | Review 篇第一節確實談產出超過審閱能力 | 該篇往下走的是「重新分配誰讀什麼」。本篇應指定誰核對觀察、誰核准撤回、誰維護取回流程。 |
   | 營運篇第二節與可靠度篇第五節的延伸閱讀描述相符 | 指定記憶評分者的版本、人工分歧處理與未見題用途；不要只在文末列連結。 |

5. **三、案例→五、報表案例：讓外掛真的做一件事。**

   > 「服務 A 使用 B 第 2 版。」

   B／C 只是代號，讀者不知道換版為何影響判斷。可明訂為假設的儲存外掛，服務 A 透過它寫出每晚報表。健康檢查能回應，仍未驗到報表寫入；如此第五節是在深化第三節，而非另加一項驗收要求。

6. **一、與七、：用已記錄的研究動作承擔溫度。**

   > 「整理時，我把照片對回官方簡報第 40 頁，也順手讀了 Agent Memory 專案的記憶整理程式。」

   這條「現場照片→回查簡報→讀程式→改變判斷」應提到開場前面。結尾只需交代這次核對如何改變作者願意相信的範圍。邀請、午餐 Kong demo、東京鐵塔屬前兩篇，不必重播，也不必新增親歷敘事。

## 術語仍難懂的清單

| 首次需要的位置與原句 | 仍卡住的詞 | 具體修法 |
|---|---|---|
| 一、：「讓模型自己決定下一步、再透過工具……」 | agent | 先寫它收到升級評估後，如何自行選擇查部署、讀相容性文件，再命名。現在只有抽象定義。 |
| 二、：「每多放一個 token……」 | token、context rot | token 尚未解釋。先說模型把文字切成小單位計算輸入量，與字數不完全相同；再用舊 log 擠占本次必要資訊的情境帶入。 |
| 二、；四、第一個 H3 | compaction | 把「長串健康檢查輸出整理成結果，但保留報表尚未驗收」放在第一次命名前；刪除後面的重教。 |
| 三、末段：「skill 一多就難挑……」 | skill | 若保留，先以「升級前檢查 SOP，內含適用時機與步驟」介紹，再命名；否則刪段。 |
| 四、第一個 H3：「working memory……episodic memory……」 | 四種 memory | 四個英文名稱先堆完才給例子。改為每個升級情境後接一個名稱，並直接說明保存與更新方式有何不同。 |
| 四、第一個 H3：「依字詞排序的 BM25……名次合併排序……RRF」 | BM25、RRF | 先示範精確找外掛名稱，以及兩張搜尋清單分數不能直接相比，再介紹名稱。 |
| 四、第二個 H3：「新抽出的事實……抽取者……」 | 抽取、confidence | 指明這裡是模型從多份摘要產生 fact 與信心值；不能讓讀者以為有另一個外部查核者。 |
| 四、第三個 H3：「索引……匯出的舊快照……」 | 索引、快照 | 用「主紀錄已刪，搜尋目錄仍指向舊內容；匯出副本也還在」先建立問題。 |
| 五、第二、三個 H3 | verifier、CI、受保護分支 | 先展示哪個檢查拿什麼材料拒絕哪筆變更，再命名。現在容易被讀成多放一個 agent 就取得獨立驗證。 |
| 六、及延伸閱讀 | eval、judge、黃金資料集、holdout | 先交代誰作答、誰評分、哪些答案由人工確認、哪些題目不參與調整，再使用名稱。 |

向量／RAG、Kubernetes／叢集／工作負載、oracle 已有情境或定義，不必再增設術語教學。`recall_any@5` 的界線也已交代，應拆短段落。gateway、proxy、digest、A2A/MCP、sandbox、commit point、optimistic locking 並非本篇實際展開的概念，不要為了補術語而塞進來。

<!-- tokens: in 2489202 out 21973 -->
