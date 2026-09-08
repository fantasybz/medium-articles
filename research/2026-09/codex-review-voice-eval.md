我會只讀你指定的 repository files，不碰 `~/.claude/`、`~/.agents/`、`.claude/skills/` 或 `agents/`。先確認檔案長度，再分段讀完 baseline、三篇舊文與目標文章。
<!-- codex ran: /bin/zsh -lc 'wc -l research/2026-09/codex-review-voice.md .context/research/medium_posts/2025-06-23-c3e8ca1e2eb5.txt .context/research/medium_posts/2025-08-11- -->
<!-- codex ran: /bin/zsh -lc "pwd && rg --files | rg '"'^(research/2026-09/codex-review-voice'"\\.md|\\.context/research/medium_posts/2025-(06-23-c3e8ca1e2eb5|08-11-4c58a488c9f -->
檔案都在 workspace 裡，目標文章約 211 行；三篇 Medium 匯出檔看起來是長行格式，所以我會用 `sed` / `fold` 只做讀取，避免漏掉段落邊界。
<!-- codex ran: /bin/zsh -lc "sed -n '1,260p' 2026-11-agentic-eval-economics/article.md" -->
<!-- codex ran: /bin/zsh -lc "sed -n '1,220p' research/2026-09/codex-review-voice.md" -->
<!-- codex ran: /bin/zsh -lc 'wc -c .context/research/medium_posts/2025-06-23-c3e8ca1e2eb5.txt .context/research/medium_posts/2025-08-11-4c58a488c9f5.txt .context/research/medi -->
baseline 已讀完；它本身就是前次產出的 voice profile。接下來我會只讀三篇指定舊文的正文格式與語氣，不重新做 34 篇統計，只用它們校準「長文 register」的段落厚度。
<!-- codex ran: /bin/zsh -lc "perl -CS -0pe 's/([。！？])/"'$1'"\\n/g; s/(ListenShareMore|Written by|Responses)/\\n\\n"'$1'"\\n/g' .context/research/medium_posts/2025-08-11-4c58a4 -->
<!-- codex ran: /bin/zsh -lc "perl -CS -0pe 's/([。！？])/"'$1'"\\n/g; s/(ListenShareMore|Written by|Responses)/\\n\\n"'$1'"\\n/g' .context/research/medium_posts/2025-06-23-c3e8ca -->
<!-- codex ran: /bin/zsh -lc "perl -CS -0pe 's/([。！？])/"'$1'"\\n/g; s/(ListenShareMore|Written by|Responses)/\\n\\n"'$1'"\\n/g' .context/research/medium_posts/2025-12-28-642ef2 -->
三篇匯出檔第一次直接讀取出現 mojibake，表示檔案編碼不是目前 shell 預設能直接呈現的形式。我要先確認編碼，再用正確轉碼讀正文；仍然只讀指定檔案、不落地產生新檔。
<!-- codex ran: /bin/zsh -lc 'xxd -l 80 .context/research/medium_posts/2025-06-23-c3e8ca1e2eb5.txt' -->
<!-- codex ran: /bin/zsh -lc 'file -I .context/research/medium_posts/2025-06-23-c3e8ca1e2eb5.txt .context/research/medium_posts/2025-08-11-4c58a488c9f5.txt .context/research/me -->
<!-- codex ran: /bin/zsh -lc locale -->
確認結果是檔案本身標成 UTF-8，但正文像是被 double-encoded 過；直接輸出會把「引言」顯成 `å¼...`。我會在讀取時做一次反 mojibake 轉碼，只用於螢幕輸出與判讀。
<!-- codex ran: /bin/zsh -lc "python3 -c \"from pathlib import Path
p=Path('.context/research/medium_posts/2025-12-28-642ef2eafc4b.txt')
s=p.read_text(encoding='utf-8')
fixed=s -->
<!-- codex ran: /bin/zsh -lc "python3 -c \"from pathlib import Path
p=Path('.context/research/medium_posts/2025-08-11-4c58a488c9f5.txt')
s=p.read_text(encoding='utf-8')
fixed=s -->
<!-- codex ran: /bin/zsh -lc "python3 -c \"from pathlib import Path
p=Path('.context/research/medium_posts/2025-06-23-c3e8ca1e2eb5.txt')
s=p.read_text(encoding='utf-8')
fixed=s -->
第一個反轉碼策略被某些已經是正常 Unicode 的字元擋住，表示檔案是「局部正常、局部 mojibake」混合。下一步我會用保守的段落抽取：只修可安全修的片段，不能安全修的部分保留原字元，不改檔案。
<!-- codex ran: /bin/zsh -lc "python3 -c \"from pathlib import Path
s=Path('.context/research/medium_posts/2025-12-28-642ef2eafc4b.txt').read_text(encoding='utf-8')
print(repr( -->
<!-- codex ran: /bin/zsh -lc "python3 -c \"from pathlib import Path
for f in ['2025-06-23-c3e8ca1e2eb5.txt','2025-08-11-4c58a488c9f5.txt','2025-12-28-642ef2eafc4b.txt']:
 s=Pat -->
重新檢查後，檔案內容其實是正常 UTF-8；剛才是 `perl -CS` 輸出造成顯示錯亂。改用 Python 直接切正文片段即可。
<!-- codex ran: /bin/zsh -lc "python3 -c \"from pathlib import Path
p=Path('.context/research/medium_posts/2025-06-23-c3e8ca1e2eb5.txt')
s=p.read_text(encoding='utf-8')
start=s -->
<!-- codex ran: /bin/zsh -lc "python3 -c \"from pathlib import Path
p=Path('.context/research/medium_posts/2025-08-11-4c58a488c9f5.txt')
s=p.read_text(encoding='utf-8')
start=s -->
<!-- codex ran: /bin/zsh -lc "python3 -c \"from pathlib import Path
p=Path('.context/research/medium_posts/2025-12-28-642ef2eafc4b.txt')
s=p.read_text(encoding='utf-8')
start=s -->
目標文章本身我已讀到完整結構：一開始產品營運視角，接著 eval、cost/model routing、metric tree、scaling gates、vendor、系列收尾。現在我會把三篇舊文剩餘正文分段看完，重點看它如何在 technical term 前後補脈絡、例子與責任邊界。
唯讀環境連 here-doc 的暫存檔都不允許，這不影響任務；我會改成 `python3 -c` 單行讀取，不建立任何暫存檔。
<!-- codex ran: /bin/zsh -lc "python3 -c \"from pathlib import Path; s=Path('.context/research/medium_posts/2025-06-23-c3e8ca1e2eb5.txt').read_text(encoding='utf-8'); start=s.f -->
<!-- codex ran: /bin/zsh -lc "python3 -c \"from pathlib import Path; s=Path('.context/research/medium_posts/2025-08-11-4c58a488c9f5.txt').read_text(encoding='utf-8'); start=s.f -->
<!-- codex ran: /bin/zsh -lc "python3 -c \"from pathlib import Path; s=Path('.context/research/medium_posts/2025-12-28-642ef2eafc4b.txt').read_text(encoding='utf-8'); start=s.f -->
舊文的長文 register 方向已經很清楚：它不是單純加長，而是常用「源起／定義／例子／回到實務／小結」來讓抽象概念落地。還差兩篇後半段與一篇尾段，我會讀完後再開始列目標文章的可改段落。
<!-- codex ran: /bin/zsh -lc "python3 -c \"from pathlib import Path; s=Path('.context/research/medium_posts/2025-06-23-c3e8ca1e2eb5.txt').read_text(encoding='utf-8'); start=s.f -->
<!-- codex ran: /bin/zsh -lc "python3 -c \"from pathlib import Path; s=Path('.context/research/medium_posts/2025-08-11-4c58a488c9f5.txt').read_text(encoding='utf-8'); start=s.f -->
<!-- codex ran: /bin/zsh -lc "python3 -c \"from pathlib import Path; s=Path('.context/research/medium_posts/2025-12-28-642ef2eafc4b.txt').read_text(encoding='utf-8'); start=s.f -->
我現在會把目標文依 heading 與段落切出來，避開 code fence、mermaid、table 本體。這樣可以精準挑「該補厚度」的正文段，不會誤動到你要求一字不改的表格與圖。
<!-- codex ran: /bin/zsh -lc "python3 -c \"from pathlib import Path
s=Path('2026-11-agentic-eval-economics/article.md').read_text(encoding='utf-8')
section=[]; in_code=False; b -->
上一個段落切分命令只是 shell quoting 出錯，沒有讀到新內容。改成單引號包住 Python 程式碼重新跑一次。
<!-- codex ran: /bin/zsh -lc "python3 -c '
from pathlib import Path
s=Path(\"2026-11-agentic-eval-economics/article.md\").read_text(encoding=\"utf-8\")
section=[]; in_code=Fals -->
候選段落大多集中在圖表前後、術語第一次出現、以及幾個把判斷壓成 slogan 的位置。Vendor 管理那節是 list 形式，但也有同樣問題，我會把它納入判讀，因為它影響全篇收束。
<!-- codex ran: /bin/zsh -lc "nl -ba 2026-11-agentic-eval-economics/article.md | sed -n '1,215p'" -->
有，這篇需要潤飾，但不需要重寫；結構、判斷與資訊順序已經成立，問題主要是少數段落太像高密度營運 checklist，補回 Kochi 舊文常見的「來路、解讀、例子、限制條件」即可。

**過於簡潔段落**

1. 所在小節：一、把 agentic capability 當內部產品營運  
原文：  
> 這個視角決定了營運的全部內容：產品要有量測（eval 與指標）、要有單位經濟（cost per successful task）、要有成長策略（scaling gates）、要有供應鏈管理（vendor 策略）。本篇依序處理這四件事。

為什麼吃力：舊文通常會先把比喻拉回工程現場，再展開分類；這段直接把四個名詞排完。缺連接詞、缺鋪陳、名詞短語堆疊。  
改寫：  
一旦把 agentic capability 當成內部產品看，後面的營運問題就不只是工具採購，而是產品管理：你要知道哪些任務真的被委派成功，這需要 eval 與指標；你要知道每次成功委派花多少錢，這就是 cost per successful task；你也要知道何時該擴大授權、何時該停下來修平台，這會落到 scaling gates 與 vendor 策略。本篇依序處理這四件事。

2. 所在小節：一、把 agentic capability 當內部產品營運  
原文：  
> 先講為什麼 eval 排第一。總論的判斷是：**eval dataset 是唯一會複利的資產**—model 每半年一代，harness 的假設不斷過時，但「你的工作負載上什麼叫做對」這件事，累積下來就是你的護城河。市場每次 model 升級、每場 vendor 價格戰，都讓它增值一次：因為只有你能在一天內用自己的 eval 驗證新選項，別人只能讀 benchmark 用猜的。

為什麼吃力：判斷很有力，但「唯一」太滿，舊文會補「在本文脈絡裡」這類責任邊界。缺 hedge、缺解讀、破折號當括號連用。  
改寫：  
所以我會先把 eval 放在第一個位置。在這篇的脈絡裡，總論那句 **eval dataset 是唯一會複利的資產**，不是在說其他投資不重要，而是在提醒：model 每半年一代，harness 的假設會跟著真實使用情境慢慢過時；但「你的工作負載上什麼叫做對」這件事，一旦被 case 化、版本控管、持續回填，就會變成團隊自己的護城河。市場每次 model 升級、每場 vendor 價格戰，都會讓這份資料集重新派上用場，因為你能在一天內用自己的 eval 驗證新選項，別人只能讀 benchmark 用猜的。

3. 所在小節：二、Eval Framework 的完整實作 / Dataset 從哪裡來  
原文：  
> 多數團隊卡在第一步：「eval 要從哪來？」答案：你的工程歷史裡已經有了，缺的只是回收的 pipeline：

為什麼吃力：這是圖前導讀句，但舊文會先說「為什麼這不是空白開始」再帶圖。缺鋪陳、缺圖表導讀。  
改寫：  
多數團隊第一次談 eval，常常會先卡在第一步：「eval 要從哪來？」我的答案是：先不要把它想成全新的研究專案，工程歷史裡其實已經留下很多材料。Incident、PR history、手工 golden tasks 都可以變成 case，差別只在於要用一條穩定的回收 pipeline，把它們整理成可以重跑、可以評分、也可以回填失敗案例的 dataset。下面這張圖先把資料流畫出來：

4. 所在小節：二、Eval Framework 的完整實作 / Eval case 的形狀  
原文：  
> Case 用宣告式格式寫，跟 code 一起版本控管、一起 review：

為什麼吃力：「宣告式格式」第一次出現沒有交代，舊文會先定義再示範。缺術語解釋、缺解讀。  
改寫：  
Case 我會建議用宣告式格式寫，而不是只留一段自然語言 prompt。意思是把來源、context、expected result 與 scoring rule 分開寫清楚，讓 reviewer 可以像 review code 一樣檢查它，也讓之後 model 升級或 harness 改動時，同一個 case 能被穩定重跑。它應該跟 code 一起版本控管、一起 review：

5. 所在小節：二、Eval Framework 的完整實作 / 三級 eval，各司其職  
原文：  
> Frontier 級最容易被省略，但它回答的是最值錢的問題：**agent 現在做不到的事，下一版 model 做到了沒**—這直接決定授權範圍要不要放寬（見第五節的 gates）。

為什麼吃力：結論正確，但缺少為什麼 Frontier 容易被省、以及如何連到授權。缺鋪陳、缺解讀、破折號當括號連用。  
改寫：  
Frontier 級最容易被省略，因為它短期看起來不像 Smoke 或 Golden 那麼直接保護日常流程。但它其實在回答最值錢的問題：**agent 現在做不到的事，下一版 model 做到了沒**。如果 Frontier 長期沒有推進，授權範圍就不該因為 demo 變漂亮而放寬；如果它開始穩定過關，才有理由把討論帶到第五節的 gates，看能不能讓 agent 接更深一層的任務。

6. 所在小節：二、Eval Framework 的完整實作 / LLM-as-judge 的三個陷阱  
原文：  
> 校準的錨只有一個：**每月一次、抽 10 個 case 的人工評分**，跟 judge 的分數對照。全自動 eval 是目標，不是起點；沒有人工錨的自動評分，飄掉了你也不會知道。

為什麼吃力：舊文會補「為什麼人工不是萬靈丹，但仍需要」。缺解讀、缺 hedge。  
改寫：  
最後還是要留一個人工校準的錨：**每月一次、抽 10 個 case 的人工評分**，再拿它跟 judge 的分數對照。這不是因為人工一定比較神，而是因為 judge 本身也是會變動的系統；當 rubric、model 版本或 case 分布慢慢改變時，人工抽查可以幫你確認分數是不是還在量同一件事。全自動 eval 是目標，不是起點；沒有人工錨的自動評分，飄掉了你也不會知道。

7. 所在小節：三、單位經濟：成本模型與 Model Routing / 一次 run 的成本解剖  
原文：  
> 一次 autonomous run 的成本 = model tokens（通常佔 60–80%）+ sandbox 運算（10–25%）+ 週邊（觀測、儲存）。花費從幾十美分到幾十美元不等，而決定因素不是任務難度，是兩個浪費源：

為什麼吃力：數字密度高，而且「不是任務難度」太絕對；舊文會先把前提說清楚。缺 hedge、缺過場。  
改寫：  
先把一筆帳拆開來看：一次 autonomous run 的成本 = model tokens（通常佔 60–80%）+ sandbox 運算（10–25%）+ 週邊（觀測、儲存）。實務上，花費從幾十美分到幾十美元不等；真正需要盯的，常常不只是任務本身有多難，而是成本被哪些地方白白燒掉。下面兩個浪費源，會比單純換便宜 model 更早影響單位經濟：

8. 所在小節：三、單位經濟：成本模型與 Model Routing / Model routing 矩陣  
原文：  
> 不同工作用不同等級的 model，routing 邏輯放在 platform 層（第二篇的 gateway），各 team 不用自己決定：

為什麼吃力：第一次進入 Model routing，但只給結論，沒有解釋決策原理。缺術語第一次交代、缺主詞、缺解讀。  
改寫：  
Model routing 的重點，是不要把「選哪個 model」丟回每個 team 自己猜。不同任務的錯誤成本、可驗證性與執行頻率不同，所以 routing 邏輯應該放在 platform 層（第二篇的 gateway）：team 描述任務，platform 依任務類型選擇 model 等級，並把成本與品質資料回收給後續調整。

9. 所在小節：四、指標樹與反作弊  
原文：  
> 每個指標都會被 game—不是因為有人惡意，而是 Goodhart's law 的日常運作。所以設計指標時就要配好解藥：

為什麼吃力：Goodhart's law 第一次出現但沒有解釋，舊文會先用一句白話定義。缺術語解釋、缺例子、破折號當括號連用。  
改寫：  
接著要補上反作弊設計。每個指標都會被 game，不一定是因為有人惡意，而是 Goodhart's law 的日常運作：當一個數字被拿來管理，它就會開始吸引行為往那個數字靠攏。對 agentic engineering 來說，這代表速度、委派率、completion rate 都不能單獨看；設計指標時就要先替每個數字配好解藥。

10. 所在小節：五、90 天之後：Scaling Gates  
原文：  
> 總論給了前 90 天的行動藍圖（選 pilot、量 baseline、建 eval）。Pilot 結束後，最常見的錯誤是宣布成功、全面推廣。規模化要用 gate 制—每道門檻有明確的量化條件，過了才解鎖下一步：

為什麼吃力：段落方向很好，但「gate 制」第一次正式落地時缺少一點操作定義。缺術語解釋、缺圖表導讀、破折號當括號連用。  
改寫：  
總論給了前 90 天的行動藍圖（選 pilot、量 baseline、建 eval）。但 pilot 結束後，真正危險的不是沒成果，而是有一點成果就宣布成功、全面推廣。規模化要用 gate 制，意思是每道門檻先寫清楚量化條件，過了才解鎖下一步；沒過就回頭修，不把 roadmap 當成通行證。下面這張表先列 gate 與解鎖範圍，後面的圖再把流程畫出來：

11. 所在小節：五、90 天之後：Scaling Gates  
原文：  
> 兩個紀律：**卡住就回頭修，不硬推**—G2 過不了通常是 harness 問題（第二篇），G3 過不了通常是 guardrails 與 eval 覆蓋問題。以及：**擴張速度由 eval 與 escape rate 決定，不由 roadmap 決定**。Roadmap 上寫著 Q3 全面導入，不構成 G2 自動過關的理由。

為什麼吃力：兩個判斷擠在同一段，舊文會拆出「第一、第二」讓讀者跟上。缺連接詞、缺過場、破折號當括號連用。  
改寫：  
這裡我會保留兩個紀律。第一，**卡住就回頭修，不硬推**；G2 過不了通常是 harness 問題（第二篇），G3 過不了通常是 guardrails 與 eval 覆蓋問題。第二，**擴張速度由 eval 與 escape rate 決定，不由 roadmap 決定**；Roadmap 上寫著 Q3 全面導入，只能代表目標，不構成 G2 自動過關的理由。

12. 所在小節：六、Vendor 管理  
原文：  
> - **換 model 的決策流程**：新 model 發布 → 跑 golden + frontier evals → 看三件事：pass rate 變化、cost per task 變化、**新出現的失敗模式**（最容易被忽略）→ 用 20% workload 做兩週 canary → 全量。永遠不要因為 benchmark 分數或 demo 換 model。

為什麼吃力：流程正確，但像 runbook 條列，少了為什麼這樣做；「永遠不要」也比舊文慣常語氣硬。缺解讀、缺 hedge。  
改寫：  
- **換 model 的決策流程**：新 model 發布時，先不要被 benchmark 分數或 demo 帶著跑。比較穩的流程是：新 model 發布 → 跑 golden + frontier evals → 看三件事：pass rate 變化、cost per task 變化、**新出現的失敗模式**（最容易被忽略）→ 用 20% workload 做兩週 canary → 全量。這樣做的目的，是把「換不換」從感覺題拉回證據題，也讓 vendor 管理回到第二節那份 eval dataset 上。

**全篇層級**

章節開場與收尾：開場能承接三部曲，但二、三、六節收得偏快，常用 `---` 直接切章。可在二節尾補一句「eval 會進入成本決策」，三節尾補一句「成本不能單獨看，下一節看指標反作弊」，六節尾補一句接到「Own the feedback loop」。

圖表前後導讀句：圖表前大多有一句，但圖後的讀圖句偏短。Dataset pipeline、metric tree、scaling gates 都建議只補圖前後文字，不改 mermaid 區塊與表格內容。

術語第一次出現：`paved road`、`eval dataset`、`LLM-as-judge`、`Goodhart's law`、`model routing`、`Budget guardrails`、`scaling gates`、`Dangerous tools` 都可以加一句白話定義。舊文習慣是先定義再展開，不會只丟術語。

hedge：有被削薄。像「唯一」、「一定」、「九成」、「不是任務難度」、「永遠不要」這些地方，建議補回「在本篇脈絡裡」、「通常」、「多半」、「我會建議」等邊界，保留判斷力但降低過度斷言感。

**不該再加字**

`先做一個視角轉換...` 這段很順，產品／客戶／營收／流失的比喻夠準，不必稀釋。

`LLM-as-judge 的三個陷阱` 的三個條列已經清楚，若前面補好導入，條列本身不用展開。

`原則一句話：指標成對出現...` 是漂亮的小結，已經有判斷、有後果、有 DevOps 對照，不必加例子。

系列收尾的 `Buy the intelligence. Build the environment. Own the feedback loop.` 與後面兩段讀起來穩，不建議再加長。

`AI 協作說明`、`References`、`系列文章`、Medium footer 屬於發布資訊，除非事實變更，否則不要潤。

<!-- tokens: in 776486 out 18745 -->
