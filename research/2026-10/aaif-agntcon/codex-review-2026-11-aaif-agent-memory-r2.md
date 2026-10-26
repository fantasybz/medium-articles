# Codex review — 2026-11-aaif-agent-memory/article.md

> model: gpt-6.1-sol, reasoning: xhigh, 2026-10-25 23:39. 原話照錄，未經摘要。第 2 輪；審的是 2026-10-25 改寫並依前一輪意見修訂後的版本。

我會先讀寫作規範與 style brief，再核對本文、原始材料和前文引用；全程限於此 repository，保持唯讀。審查會直接指出失焦段落、證據越界與可落實的修法。
<!-- codex ran: /bin/zsh -lc 'cat STYLE.md' -->
<!-- codex ran: /bin/zsh -lc 'cat research/2026-10/style_brief.md' -->
<!-- codex ran: /bin/zsh -lc "rg --files --hidden -g '"'!agents/**'"' -g '"'!.claude/**'"' -g '"'!.git/**'"' .context/research/aaif-2026-10-23 .context/research/aaif-2026-10-25 -->
<!-- codex ran: /bin/zsh -lc "sed -n '150,300p' research/2026-10/style_brief.md" -->
<!-- codex ran: /bin/zsh -lc "rg --files -g 'article.md' 2026-10-green-* 2026-11-same-spec-* 2026-10-agentic-harness-blueprint 2026-11-agentic-eval-economics 2026-09-agentic-en -->
<!-- codex ran: /bin/zsh -lc "rg --files --hidden -g '"'!**/.git/**'"' -g '"'!**/.agents/**'"' -g '"'!**/.claude/**'"' -g '"'!**/agents/**'"' .context/research/aaif-2026-10-23  -->
<!-- codex ran: /bin/zsh -lc 'nl -ba 2026-11-aaif-agent-memory/article.md' -->
<!-- codex ran: /bin/zsh -lc "python3 -c 'from pathlib import Path; roots=[\".context/research/aaif-2026-10-23/slides/text\",\".context/research/aaif-2026-10-23\",\".context/re -->
<!-- codex ran: /bin/zsh -lc "sed -n '153,231p' 2026-11-aaif-agent-memory/article.md" -->
目前最需要核對的是第四節的程式批評、第五節對 AIRAS「獨立驗證」的判斷，以及第六節的驗收設計。後兩者可能把設計要求寫得比證據能支持的更強；我會對照固定版本與前文，確認問題出在哪一句。
<!-- codex ran: /bin/zsh -lc 'cat .context/research/aaif-2026-10-23/slides/text/2WZJf-01-crabrag-graph-memory-for-ai-assistants-v0-6-agntcon-japan.txt' -->
<!-- codex ran: /bin/zsh -lc 'cat .context/research/aaif-2026-10-23/slides/text/2QlDp-01-agentmemory-agntcon-mcpcon-opening.txt' -->
<!-- codex ran: /bin/zsh -lc "python3 -c 'from pathlib import Path; roots=[\".context/research/aaif-2026-10-23/sources\",\".context/research/aaif-2026-10-25\",\"2026-11-aaif-ag -->
<!-- codex ran: /bin/zsh -lc "rg --files --hidden .context research -g '"'!**/.git/**'"' -g '"'!**/.agents/**'"' -g '"'!**/.claude/**'"' -g '"'!**/agents/**'"' | rg '/(consolid -->
<!-- codex ran: /bin/zsh -lc 'cat .context/research/aaif-2026-10-23/slides/text/2RqMK-01-agnt-con-2026-v7.txt' -->
<!-- codex ran: /bin/zsh -lc "python3 -c 'from pathlib import Path; p=Path(\".context/research/aaif-2026-10-24/third-article\"); [print(f) for f in sorted(p.iterdir())]'" -->
<!-- codex ran: /bin/zsh -lc 'cat .context/research/aaif-2026-10-24/third-article/agentmemory-code/consolidation-pipeline.ts' -->
<!-- codex ran: /bin/zsh -lc 'cat .context/research/aaif-2026-10-24/third-article/agentmemory-code/auto-forget.ts' -->
<!-- codex ran: /bin/zsh -lc 'cat .context/research/aaif-2026-10-24/third-article/agentmemory-longmemeval.md' -->
<!-- codex ran: /bin/zsh -lc 'cat .context/research/aaif-2026-10-24/third-article/airas-readme.md' -->
<!-- codex ran: /bin/zsh -lc "rg -n '70517|e1c37|branch|sha|ref|confidence|semantic|accessCount|isLatest|score|supersed|reinforc' .context/research/aaif-2026-10-24/third-articl -->
<!-- codex ran: /bin/zsh -lc "rg --files .context/research/aaif-2026-10-24/third-article/web .context/research/aaif-2026-10-24/third-article/agentmemory-code .context/research/ -->
<!-- codex ran: /bin/zsh -lc "rg -n '"'^##|''^###|AGENTS.md|Org|Repo|Dir|oracle|保留|量尺|三種|撤回|常駐|單次|產出|審閱|frozen|holdout|三個陷阱'"' 2026-10-agentic-harness-blueprint/article.md 2026 -->
<!-- codex ran: /bin/zsh -lc "sed -n '1,140p' 2026-10-agentic-harness-blueprint/article.md" -->
<!-- codex ran: /bin/zsh -lc "sed -n '1,130p' 2026-10-green-review/article.md" -->
<!-- codex ran: /bin/zsh -lc "rg -n '"'^## |''^### '"' 2026-11-same-spec-overview/article.md 2026-11-same-spec-contract/article.md 2026-11-same-spec-variance/article.md 2026-10 -->
<!-- codex ran: /bin/zsh -lc "sed -n '384,440p' 2026-10-green-reliability/article.md
sed -n '93,106p' 2026-11-agentic-eval-economics/article.md" -->
<!-- codex ran: /bin/zsh -lc "cat .context/research/aaif-2026-10-25/hire/ai-agent-metrics.md
rg -n 'PagerDuty|人工標|校準|judge' 2026-11-aaif-after-tokyo/article.md" -->
<!-- codex ran: /bin/zsh -lc "sed -n '21,44p' 2026-11-same-spec-overview/article.md
sed -n '34,66p' 2026-11-same-spec-contract/article.md
sed -n '232,258p' 2026-11-same-spec-va -->
已確認一個具體錯誤：第四節用「相容／不相容」示範會觸發 0.9 相似度門檻，但程式按空白切詞並丟掉短詞，這兩句實際算出來只有 0.5。第五節也把 README 描述的 CI 檢查直接判為「獨立驗證」，需要收回到已核對的範圍。
<!-- codex ran: /bin/zsh -lc 'cat .context/research/aaif-2026-10-23/facebook-post-provenance.json
cat research/2026-10/aaif-agntcon/memory-media-manifest.json' -->
<!-- codex ran: /bin/zsh -lc "rg -n -C 5 'gold|calibr|evaluat.*evaluat|human|layer' .context/research/aaif-2026-10-25/hire/README.md .context/research/aaif-2026-10-23/slides/te -->
<!-- codex ran: /bin/zsh -lc "rg --files --hidden .context/research research -g '"'!**/.git/**'"' -g '"'!**/.agents/**'"' -g '"'!**/.claude/**'"' -g '"'!**/agents/**'"' -g '"'! -->
<!-- codex ran: /bin/zsh -lc "python3 -c 'import json; from pathlib import Path; p=Path(\".context/research/aaif-2026-10-23/sources/evals.json\"); x=json.loads(p.read_text());  -->
<!-- codex ran: /bin/zsh -lc "rg -l --hidden -g '*.txt' -g '*.json' -g '*.html' -g '"'!**/.git/**'"' -g '"'!**/.claude/**'"' -g '"'!**/.agents/**'"' -g '"'!**/agents/**'"' -g ' -->
<!-- codex ran: /bin/zsh -lc "rg -n -C 3 'frozen|holdout' 2026-10-green-reliability/article.md
sed -n '1,130p' .context/research/aaif-2026-10-24/third-article/agentmemory-code/ -->
<!-- codex ran: /bin/zsh -lc "sed -n '1,150p' .context/research/aaif-2026-10-23/slides/text/2WZJf-01-crabrag-graph-memory-for-ai-assistants-v0-6-agntcon-japan.txt
cat .context/ -->
<!-- codex ran: /bin/zsh -lc "python3 -c 'import json; from pathlib import Path; x=json.loads(Path(\".context/research/aaif-2026-10-23/sources/evals.json\").read_text())[\"text -->
<!-- codex ran: /bin/zsh -lc "sed -n '27,73p' 2026-09-agentic-org-design/article.md
sed -n '481,538p' 2026-09-agentic-engineering-platform/article.md
sed -n '35,59p' 2026-10-gr -->
<!-- codex ran: /bin/zsh -lc "rg -n 'Kubernetes|1.30|1.31|升級|核准|記憶' 2026-11-aaif-agent-handoffs/article.md | head -35
sed -n '7,100p' 2026-10-green-overview/article.md" -->
<!-- codex ran: /bin/zsh -lc "sed -n '305,410p' .context/research/aaif-2026-10-24/third-article/agentmemory-code/hybrid-search.ts
rg -n 'semantic|consolid|reinforc|accessCount| -->
<!-- codex ran: /bin/zsh -lc "rg -l --hidden -g '*.txt' -g '*.json' -g '*.html' -g '"'!**/.git/**'"' -g '"'!**/.agents/**'"' -g '"'!**/.claude/**'"' -g '"'!**/agents/**'"' -g ' -->
<!-- codex ran: /bin/zsh -lc "nl -ba .context/research/aaif-2026-10-24/third-article/agentmemory-code/auto-forget.ts | sed -n '35,165p'
nl -ba .context/research/aaif-2026-10-24 -->
<!-- codex ran: /bin/zsh -lc "python3 -c 'import json; from pathlib import Path; p=Path(\".context/research/aaif-2026-10-24/third-article/web\"); names=[\"2QlDp-agenda-text.txt -->
<!-- codex ran: /bin/zsh -lc "python3 -c 'from pathlib import Path; p=Path(\".context/research/aaif-2026-10-23/slides/text/2WZJf-01-crabrag-graph-memory-for-ai-assistants-v0-6- -->
前文的章節引用未發現明顯錯置，但 recall 多半停在「前面說過同樣原則」，沒有充分說明記憶層新增了什麼責任。另一個主要缺口是：本文要求資料服務攔住舊摘要，卻沒處理更正途中，舊摘要被較慢的程序重新寫回來的情況。我正在把審查整理成逐節可改的清單。
<!-- codex ran: /bin/zsh -lc "rg -n 'The gate is enforced|Integrity of the experiment|That covers the paper|GH_PERSONAL_ACCESS_TOKEN|verify-record.*checks' .context/research/aa -->
## 致命問題

1. **四、〈更新與遺忘，要讓下一次檢索真的不同〉：用來批評程式的例子不成立。**

   > 「『C 第 3 版與 1.31 相容』和『C 第 3 版與 1.31 不相容』只差一個否定詞，相似度很高」

   這版程式按空白切詞，再丟掉長度不超過兩個字元的詞。兩句留下的集合分別是 `{1.31}`、`{1.31, 不相容}`，Jaccard similarity 是 **0.5**，不會越過 **0.9**。這不是措辭問題，而是核心例證錯誤。改用確實符合演算法的例子，例如同一組詞調換依賴方向，並交代候選還須共用 concept。[程式依據]( /Users/kochi.chuang/conductor/workspaces/medium-articles/dodoma/.context/research/aaif-2026-10-24/third-article/agentmemory-code/auto-forget.ts:82)

2. **五、〈讓更正沿引用關係，傳到下一份摘要〉：把文件宣稱升格成作者已確認的獨立性。**

   > 「拿什麼材料拒絕哪筆變更寫得很清楚，這才是獨立驗證，不是多放一個 agent。」

   README 能支持「專案描述了哪些檢查」，不能單靠它確認部署中的 verifier、判準、workflow 與結果儲存確實不受產出者修改。相同 README 還明寫，benchmark hacking、data leakage、design deviation 仍可能通過 gate。後面的 roadmap 限制，收不回這句已經說滿的結論。

   改成：「README 描述了分開查核紀錄與論文數值的設計；本文未驗證實際部署中的修改權限與繞過路徑。」再分清**數值可追溯、判定符合既定標準、研究方法有效**三件事。[README 依據](/Users/kochi.chuang/conductor/workspaces/medium-articles/dodoma/.context/research/aaif-2026-10-24/third-article/airas-readme.md:176)

## 重要問題

1. **TL;DR／六、〈我會怎麼驗收下一次的記憶〉：核心問題到後面換了定義。**

   > 「本文只問一件事：一項經驗被換了環境、發現漏驗或正式更正之後，下一個 agent 還會不會沿用原結論？」

   > 「還有兩種情況，『可信』在那裡換了意思」

   前者問證據是否仍支持結論；後者加入刪除義務與存取權限。資料正確卻不能提供，和資料已不足以支持判斷，是不同問題。建議保留原題，把刪除與權限移成「導入前提」，主驗收表集中處理適用範圍、更正、衝突與更正傳播。

2. **二、〈先分清這一輪要讀的，和要留給下次的〉：工單／wiki 類比把內容類型誤當成儲存邊界。**

   > 「工單是這一輪要讀的內容；wiki 是留給未來每一輪的經驗。」

   舊工單也能成為 memory；wiki 的部分內容也會進入當次 context。應改成「桌上目前攤開的工單與 wiki 頁面，是這次工作集；櫃子裡可供往後取用的紀錄，是外部儲存」。這樣才能接到真正的問題：**從儲存取進工作集時，如何確認仍適用。**

3. **三、〈把時間與適用範圍放進關係裡〉：GraphRAG 的選型理由仍停在個人頻率。**

   > 「當反向追問每週都出現、而且關係本身常變動，才值得增加圖形儲存」

   每週出現反向查詢，不能單獨推出 graph storage 比資料表划算；SQL 也能維護及反查關係。缺的是同一批問題下，既有方案的查詢維護、關係更新與人工查核成本，是否已超過 graph 的建置和維護成本。補上這個比較，才算回答「設計為什麼值得採用」。

4. **四、〈先分清要保存的經驗，以及這一輪要讀的內容〉：提問和證據沒有交接。**

   > 「有效的更正與常被引用的舊摘要一起存在時，哪一份會先回來？」

   接下來的 BM25、RRF 與 95.2%，回答的是找回相關 session 的能力，沒有回答更正是否優先、舊判定是否被排除。這是假交接。

   應先說：「搜尋排名不能決定哪份判定仍有效。」由有效版本與適用範圍限制候選，再討論如何排序。95.2% 只能作為這條流程中「相關材料能否找回」的旁證。

5. **四、〈反覆出現的說法，還需要新的查核〉及〈更新與遺忘，要讓下一次檢索真的不同〉：不同資料路徑沒有分清。**

   > 「同一句事實再次出現時，這個分支也不補入新的來源關聯。」

   > 「清理程式比較共用同一概念的候選」

   前者寫入 `KV.semantic`；後者處理 `KV.memories`。已核對的 hybrid search 又從 observations／memories 取回內容。文章容易讓讀者以為這是同一筆資料的一條完整生命週期。

   補一張小表，列出資料型別、儲存集合、取回入口、淘汰方式。沒有查到的下游影響，就停在「欄位不能代表新增證據」，不要讓讀者自行補成已證實的檢索後果。[抽取程式](/Users/kochi.chuang/conductor/workspaces/medium-articles/dodoma/.context/research/aaif-2026-10-24/third-article/agentmemory-code/consolidation-pipeline.ts:132)、[取回程式](/Users/kochi.chuang/conductor/workspaces/medium-articles/dodoma/.context/research/aaif-2026-10-24/third-article/agentmemory-code/hybrid-search.ts:329)

6. **五、〈讓更正沿引用關係，傳到下一份摘要〉：J-17 範例的紀錄語義不清楚。**

   > 「判定識別 J-17……目前狀態是已撤回；取代的判定是『必要功能均已通過』」

   J-17 究竟是舊判定、更正事件，還是新判定？「取代的判定」也可能讀成取代後的內容。改成三筆明確紀錄：舊判定 J-17、新判定 J-18，以及 J-18 取代 J-17 的關係。來源需有固定識別與定位，不能只有「節點版本與健康檢查通過」的敘述。

7. **五、〈讓更正沿引用關係，傳到下一份摘要〉／六：尚未定義更正何時生效。**

   > 「資料服務每次查詢都核對目前有效的版本」

   > 「程序中斷後能從中斷處繼續」

   還缺一個會讓舊結論復活的情境：程序甲拿 J-17 重建摘要；程序乙完成撤回；程序甲稍後才把舊摘要寫回。每次查詢核對版本，不等於寫回時也檢查依據。

   補上：更正完成的可觀察時點、摘要發布前核對所依據版本，以及中斷重試不得恢復已撤回狀態。第六節要實際設計這個交錯順序，而不只測更新完後的新 session。

8. **六、〈我會怎麼驗收下一次的記憶〉：把前文三種重查重新對應時，漏掉量尺驗證。**

   > 「對應到記憶上就是保留原始觀察、重評舊判定與重新執行任務三件事。」

   《同一份規格，跑十次》變異篇第八節分的是：檢查 grader、檢查新候選、檢查交付方法。**保留原始觀察是前提，不是檢查新版 grader。**

   改成明確對照：判準或判定器改版，先用已核對的正反材料驗證；重評既有判定，沿用適用的觀察；模型或取回方法改版，取得新的任務結果。不要把新分類寫成原文三分法的直接延續。

9. **六、〈我會怎麼驗收下一次的記憶〉：診斷案例與擴大使用之間缺一層證據。**

   > 「等更新、隔離與不足資料的處理都在相關案例中得到驗證，再擴大使用範圍。」

   七個刻意安排的情境能發現缺陷，不能估計真實工作中的錯誤率與收益。應明確稱為診斷 pilot；通過後，下一步是維持人工核准的小範圍 trial，記錄實際接手與維護成本。這才接得上《同一份規格，跑十次》總論第十節的採用邊界。

10. **七、〈讓經驗留下來，也讓下一個人有理由修正它〉：結尾把驗收缺口推成排程禁令。**

    > 「在補驗完成前，不把正式叢集的升級排進時程。」

    尚未補驗，不等於不能規劃含前置條件的時程。本文能支持的是：不能用舊成功摘要作為放行依據。改成「把報表補驗及正式環境的相容性確認列為放行前置條件，由權責人決定排程與剩餘風險」。

## 次要問題

1. **四、〈先分清要保存的經驗，以及這一輪要讀的內容〉：把 working memory 寫成刪除規則。**

   > 「叫 working memory，任務結束就不必保留。」

   工作集可釋放，不代表其中的決定、未完成事項與證據都不必保存。改成「任務結束後可釋放這份工作集；需要交接或稽核的內容另行保存」。

2. **四、同一 H3：BM25 被說成精確識別保證。**

   > 「要精確找『外掛 C』這個名稱，按字詞比對最可靠，這是 BM25」

   BM25 是按詞彙相關性排行，不能代替 entity ID 或版本欄位的精確比對。「最可靠」也沒有比較證據。改成「名稱與錯誤字串可用字詞搜尋；確認是否同一個外掛，仍用明確識別碼」。

3. **四、〈反覆出現的說法，還需要新的查核〉：抽取流程的啟用條件省略。**

   > 「系統也會從多次工作摘要抽出事實」

   該路徑有 consolidation 開關、provider 與至少五份摘要等條件。首次引用時加上「在啟用這條整理流程的配置中」。也可補更直接的推論：即使沒有新觀察，重處理同一批摘要仍可能刷新這些欄位。

4. **五、〈在結果出現前，先決定怎樣才算有支持〉：講者的對比被寫成研究史事實。**

   > 「傳統研究先產生結果再決定怎麼驗證」

   這是第 35 頁採取的對比框架，不適合概括所有傳統研究。改成「簡報把事後選擇驗證方式，與事前定義驗證方式作對比」。

5. **七、開頭：日期指涉錯誤。**

   > 「9 月 12 日的 Facebook 告別澀谷貼文……同一晚在 SHIBUYA SKY……」

   provenance 記錄貼文是 **9 月 12 日上午**；照片是 **9 月 11 日晚間**。「同一晚」應改成「前一晚」。

6. **References／資料與方法註記：查核範圍要補缺口。**

   > 「文章建議的對策有三種。」

   repository 未找到 References [1] 的原文快照，這個「三種」分類本輪無法完成核驗。不能只憑先前稿件確認。95.2%、86.2%、500 題、約 48 段對話、AAAI 的兩個數字與主要投影片頁碼，則能對回現有材料；本文沒有 timecode 可查。

## 建議刪除

以下是未推進主題，或只有表面承接的段落與片段。

| 位置 | 原句 | 具體處理 |
|---|---|---|
| 一、照片段 | 「相簿裡還有……三張夜景。」 | 三張圖沒有參與推論，卻隔開問題與 agent 定義。移到文末，或只留一張。 |
| 一、末段 | 「第三節看它能不能找對對象……」 | TL;DR 和第二節閱讀地圖已交代路線；刪除這次預告，保留 agent 定義。 |
| 三、導讀 | 「工具一抽屜，卻挑不出此刻該用哪一把」 | 本篇沒有展開 skill selection；刪此分句。 |
| 四、第一個 H3 | 「第 6、7 頁示範了 compaction……」 | 第二節已介紹。縮成一句，直接追問哪些限定條件不能在整理時消失。 |
| 四、第一個 H3 | 「第 18 頁列了該留與該丟的東西……」 | 大部分是一般記憶操作指南。保留「未完成事項不可摘要成已完成」，其餘縮減。 |
| 四、最後一個 H3 | 「至於來源互相衝突的情況……」 | 從低頻教訓、一次性授權突然跳到文字相似度。拆段，以「使用頻率不能裁決來源衝突」交接。 |
| 五、導讀第二段 | 「他在第 17 到 19 頁還放了一組數字……」 | AAAI 成長數字只重述 review 產能問題。刪除這半段，把責任分工移到第六節。 |
| 六、長篇 recall 段 | 「第二條是 Anthropic 的 eval 文章說的飽和……」 | 飽和、污染、人工校準擠在同段，主題變成 eval 教科書。保留與本次採用決定直接相關的規則，其餘連回前文。 |
| 七、照片導語 | 「留作本文的尾圖」 | 是編輯安排，不是讀者需要的內容。保留日期與圖說即可。 |
| References [10] | 「供延伸觀看」 | 正文沒有使用、也未逐字核對。移到單純的延伸觀看，不列成第二節論證依據。 |

會場第 40 頁照片有推動判斷；澀谷照片目前是裝飾。邀請、午休 Kong、東京鐵塔已在系列其他篇承擔敘事，不必為了 recall 再塞回本篇。

## 建議補充

1. **三至五節：每場各補一個尚未完成的第一性原理推論。**

   - **三、〈把時間與適用範圍放進關係裡〉**  
     > 「圖形表示並不免除維護」  
     再推一步：查詢路徑只能解釋**已記錄的關係**，不能證明沒有漏關係。盤點不完整時，答案必須交代涵蓋範圍。這是 graph 的成本與限制，不能只寫誰更新連線。

   - **四、〈反覆出現的說法，還需要新的查核〉**  
     > 「摘要省下讀取成本，也丟掉細節」  
     明說：如果「報表驗過」和「報表沒驗」都被壓成同一句成功摘要，下游無法僅靠摘要恢復差別。必要限定條件必須留下，或保留能取回它們的來源入口。這比再講一次壓縮有風險更深入。

   - **五、〈讓更正沿引用關係，傳到下一份摘要〉**  
     > 「原主張照原標準判定」  
     補上判準改版的成本：哪些舊判定可用原觀察重評，哪些因缺少必要量測必須重新執行。否則「版本都保存」仍沒有轉成維護決策。

2. **五、〈讓更正沿引用關係，傳到下一份摘要〉：把長串假設資料改成能檢查的三筆紀錄。**

   > 「先給一筆可以照著建立的更正紀錄」

   至少分清：

   | 紀錄 | 應清楚呈現 |
   |---|---|
   | J-17 舊判定 | 原主張、判準版本、觀察引用、已撤回、撤回原因 |
   | J-18 新判定 | 限縮後主張、取代 J-17、仍缺哪些驗證、確認人與生效版本 |
   | P-9 衍生摘要 | 依據 J-17，暫不得作為有效依據；重建後改引用 J-18 |

   再問一個目前缺席的問題：誰能提出更正，誰能讓它成為有效判定？有來源，不代表提交者有權改寫團隊結論。

3. **六、〈我會怎麼驗收下一次的記憶〉：補上星期一能交付的結果與採用出口。**

   > 「記錄搜尋與工具查詢次數，以及負責人需要補問的事項」

   應交付一張表：案例、預期判斷、儲存狀態、工具回傳、實際 context、最終回答、人工查核時間、失敗負責人。成本另計摘要重建與關係維護；少查幾次工具不必然省時。

   採用出口也要明訂：更正仍未抵達回答，就停在協助找資料；診斷案例通過，進入有人核准的有限 trial；取得代表性工作中的收益與維護證據後，才討論擴大。

4. **二、五、六／〈延伸閱讀〉：recall 要帶出新增責任。**

   > 「本文第五、六節的三個角色由此而來。」

   Review 篇第一節支持的是重新分配閱讀責任，沒有直接定義這三個角色。改成「沿用該原則，本篇新增以下分工」。角色責任更適合接《組織篇》第二節的 Platform／Domain 分工。

   > 「也不宜把『很久沒有用』直接當成『已經不重要』。」

   這點其實可直接回扣《可靠度篇》第二節：expiry 是重新檢視的提醒，不是刪除理由。本篇新增的應是「人工規則的檢視責任，如何落到自動整理的記憶及其副本」。

   > 「它太鬆會放過錯誤、太嚴會錯怪合法寫法」

   這只是重述契約篇。應帶入該篇第三個盲點：產出者與檢查者共享同一個誤解。用它要求驗收器也接受正反證據案例，而不只要求換一個 agent。

## 術語仍難懂的清單

| 首次需要的位置 | 原文用語 | 具體修法 |
|---|---|---|
| 一、開頭至末段 | 「agent」 | 定義被三張照片隔到後面。把「收到升級評估、自己選擇查詢步驟」提前。 |
| 二 | 「context」 | 用「目前攤開哪些工單、wiki 頁與查詢結果」說明，避免工單／wiki 二分。 |
| 二 | 「token」「context rot」 | token 已有定義，缺容量如何影響本例的判斷；說清楚舊輸出占空間，以及長輸入下找資訊變差是兩種限制。 |
| 二 | 「健康檢查」 | 到第三節才解釋。首次出現就補「服務能回應，尚未證明報表產出」。 |
| 二、末段 | 「Harness」「AGENTS.md」「Org、Repo、Dir」 | 先說「公司共通規則、專案操作說明、局部模組例外」，再命名。 |
| 三、第一個 H3 | 「向量搜尋」 | 先放「升版失敗找回版本更新後無法啟動」的需求，再說數字表示與向量。 |
| 四、第一個 H3 | 「working／episodic／semantic／procedural memory」 | 四個例子有了，但一段塞四種名稱。改成四列表，另列誰維護、什麼變動觸發更新。 |
| 四、第一個 H3 | 「BM25」「RRF」 | BM25 不等於精確 ID 查找；RRF 補一個同一筆記在兩份清單排名不同、如何合併的例子。 |
| 四、第一個 H3 | 「LongMemEval-S」「recall_any@5」 | 將資料配置、命中定義、不能回答什麼拆開。現在同段資訊過密。 |
| 四、第二個 H3 | 「confidence」「accessCount」 | 就地標成「抽取模型自報的信心」「此分支的再次抽取計數」，避免名稱被讀成查核次數。 |
| 四、第三個 H3 | 「索引」「舊快照」 | 先用「正文改了，搜尋目錄與先前匯出包還留舊字」建立問題，再命名。 |
| 五、第一個 H3 | 「verifier」 | 第一次出現時先說誰拿哪些材料、依哪份規則查核，以及產出者不能改什麼。 |
| 五、第一個 H3 | 「oracle」 | 先指明本例的報表驗收清單如何判對錯，再命名；不能只靠前文連結承擔解釋。 |
| 五、第三個 H3 | 「CI」「受保護分支」 | 已說檢查沒過不能進去，還需交代誰控制檢查與例外權限，才能支持獨立性的討論。 |
| 六／延伸閱讀 | 「保留題」「frozen holdout」「校準」 | 分清未參與調整的評估題、人工標記的評分器校準資料，以及正常供 agent 查詢的證據材料。 |

gateway、proxy、digest、sandbox、commit point、optimistic locking 並未在本篇形成正文概念，不必為了術語清單補入。

<!-- tokens: in 2719904 out 21036 -->
