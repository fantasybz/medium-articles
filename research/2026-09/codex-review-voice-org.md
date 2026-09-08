我會只讀你列出的五個 repository 檔案：先看既有 voice profile，再對照三篇舊文，最後逐段讀 2026-09 的 article。由於你要求不要重做 baseline，我會把它當校準依據，而不是重新歸納作者風格。
<!-- codex ran: /bin/zsh -lc "sed -n '1,260p' research/2026-09/codex-review-voice.md" -->
<!-- codex ran: /bin/zsh -lc "sed -n '1,260p' .context/research/medium_posts/2025-06-23-c3e8ca1e2eb5.txt" -->
<!-- codex ran: /bin/zsh -lc "sed -n '1,260p' .context/research/medium_posts/2025-08-11-4c58a488c9f5.txt" -->
<!-- codex ran: /bin/zsh -lc "sed -n '1,260p' .context/research/medium_posts/2025-12-28-642ef2eafc4b.txt" -->
三篇舊文有些是 Medium 抓下來的一整行，直接 `sed` 會很難讀。我會用只讀管線把句點、標題與 Markdown 分隔整理成可閱讀片段；仍然只碰你指定的三篇與新文，不掃 repository。
<!-- codex ran: /bin/zsh -lc "perl -CSD -0pe 's/(。|！|？)/"'$1'"\\n/g; s/(Press enter or click to view image in full size|ShareMore|FollowWritten by)/\\n"'$1'"\\n/g; s/(源起：|引言|結語 -->
<!-- codex ran: /bin/zsh -lc "perl -CSD -0pe 's/(。|！|？)/"'$1'"\\n/g; s/(Press enter or click to view image in full size|ShareMore|FollowWritten by)/\\n"'$1'"\\n/g; s/(CNCF 社群|G -->
<!-- codex ran: /bin/zsh -lc "perl -CSD -0pe 's/(。|！|？)/"'$1'"\\n/g; s/(Press enter or click to view image in full size|ShareMore|FollowWritten by)/\\n"'$1'"\\n/g; s/(引言：|第一個坑： -->
<!-- codex ran: /bin/zsh -lc "nl -ba 2026-09-agentic-org-design/article.md | sed -n '1,220p'" -->
新文已讀完。它的架構很清楚，問題不是內容薄，而是有幾個段落像 memo note：判斷、名詞、動作都在，但舊文常見的「先把讀者帶到同一個場景」少了一拍。我現在把段落按小節編號，挑最值得動的 10 段。
<!-- codex ran: /bin/zsh -lc "awk 'BEGIN{RS=\"\"; ORS=\"\\n---BLOCK---\\n\"} {gsub(/\\n/,\"\\\\n\"); print NR \":\" "'$0}'"' 2026-09-agentic-org-design/article.md | sed -n '1,2 -->
舊文校準已夠抓出差異：Jun 23 文章偏「書錨＋概念鋪陳＋例子」，Aug 11 偏「工具地圖＋圖前導讀＋最佳實務」，Dec 28 偏「場景故事＋問題句＋文化收束」。Aug 11 檔案較長，我再分段補讀被終端截掉的中後段，避免只用前半篇校準。
<!-- codex ran: /bin/zsh -lc "perl -Mutf8 -CSD -0ne '"'$s=$_; $start=9000; $len=4500; print substr($s,$start,$len);'"' .context/research/medium_posts/2025-08-11-4c58a488c9f5.tx -->
<!-- codex ran: /bin/zsh -lc "perl -Mutf8 -CSD -0ne '"'$s=$_; $start=4500; $len=4500; print substr($s,$start,$len);'"' .context/research/medium_posts/2025-08-11-4c58a488c9f5.tx -->
<!-- codex ran: /bin/zsh -lc "perl -Mutf8 -CSD -0ne '"'$s=$_; $start=0; $len=4500; print substr($s,$start,$len);'"' .context/research/medium_posts/2025-08-11-4c58a488c9f5.txt | -->
<!-- codex ran: /bin/zsh -lc "perl -Mutf8 -CSD -0ne '"'$s=$_; $start=13500; $len=4500; print substr($s,$start,$len);'"' .context/research/medium_posts/2025-08-11-4c58a488c9f5.t -->
我已補讀 Aug 11 的中段，包括 Argo Rollouts、Prometheus/Grafana、Kubeflow Pipelines 的圖表與最佳實務區。最後再讀尾段，然後我會直接整理交付清單。
<!-- codex ran: /bin/zsh -lc "perl -Mutf8 -CSD -0ne '"'$s=$_; $start=18000; $len=4500; print substr($s,$start,$len);'"' .context/research/medium_posts/2025-08-11-4c58a488c9f5.t -->
<!-- codex ran: /bin/zsh -lc "perl -Mutf8 -CSD -0ne '"'$s=$_; $start=22500; $len=4500; print substr($s,$start,$len);'"' .context/research/medium_posts/2025-08-11-4c58a488c9f5.t -->
<!-- codex ran: /bin/zsh -lc "perl -Mutf8 -CSD -0ne '"'$s=$_; $start=27000; $len=4500; print substr($s,$start,$len);'"' .context/research/medium_posts/2025-08-11-4c58a488c9f5.t -->
我判斷：這篇需要「輕量潤飾」，不是重寫；它已經發布且主張清楚，最值得補的是承接、導讀與第一輪術語交代，避免把原本銳利的 memo-style 判斷稀釋成長篇解說。

**過短段落**
1. 小節：一、為什麼組織會自然滑向錯誤設計  
原文：「總論點名了四種失敗模式，其中「中央 Agent Team」最值得展開—因為它不是愚蠢的決定，而是組織重力的自然結果。三股力量會把你推向那裡：」  
吃力：舊文通常會先交代「我為什麼要從這裡切入」，再下判斷；這裡直接把組織重力丟出來，讀者還沒站穩。  
缺：缺鋪陳、缺過場、破折號當括號連用。  
改寫：  
「總論裡我點名了四種常見失敗模式，這一篇先把「中央 Agent Team」拉出來談。原因不是它最荒謬，剛好相反，它往往是會議室裡最容易被接受的選項。當 AI 預算、稀缺人才與治理焦慮同時出現時，組織很自然會想先把人集中起來、把責任掛到一個新的 team 底下。問題是，這個選項解決的是管理上的不安，不一定解決交付現場的摩擦。大致上，有三股力量會把你推向那裡：」

2. 小節：一、為什麼組織會自然滑向錯誤設計  
原文：「三股力量都真實存在，但它們追求的是「好管理」，不是「好產出」。Conway's law 在這裡要反著用：你最後得到的交付系統，會長得跟你的組織圖一樣—中央 team 的組織圖，產出的就是 ticket queue 型的交付系統.」  
吃力：舊文會把抽象法則拉回具體工作流；這裡判斷很準，但「ticket queue」的壞處還沒展開。  
缺：缺解讀、缺例子、破折號當括號連用。  
改寫：  
「這三股力量都真實存在，也都不是壞意。但它們共同追求的是「好管理」，不一定是「好產出」。如果用 Conway's law 回頭看，組織圖其實會預先寫進你的交付系統裡：當所有 agentic work 都必須排進中央 team 的 queue，domain team 就會從 owner 退成需求提出者，platform team 也會從槓桿提供者變成接單單位。久了以後，你得到的不是 self-service，而是一條披著 AI 外衣的 ticket queue。」

3. 小節：二、Platform + Federation 的完整設計  
原文：「總論給了概念圖，這裡把三個角色的分工落到 RACI 的精度：」  
吃力：舊文在圖前通常會說「這張圖要看什麼」；這裡直接進圖，RACI 也第一次出現但沒交代。  
缺：缺導讀、術語第一次出現沒解釋。  
改寫：  
「總論先給了一張概念圖，這裡再往下收斂成可以拿去討論責任邊界的版本。RACI 在這裡不是流程管理的裝飾，而是用來回答四個很現實的問題：誰真的負責做、誰最後 accountable、誰需要被 consult、誰只要 informed。先看圖，再看表，重點會落在三個角色如何互相牽制，而不是誰擁有 agent 這個名詞。」

4. 小節：三、三種規模的實際編制  
原文：「Skill mix 的重點：這是 **product team，不是 research team**—它的產品是 paved road，客戶是內部工程師。所以要找的是做過 developer tooling、CI、test infra 的人，而不是模型研究背景的人。Security 那 0.5 個人用借的：讓資安 team 有參與感，比之後被稽核打回來便宜得多.」  
吃力：舊文會先定義 metaphor；這裡的 paved road 很關鍵，但沒解釋就接招聘條件。  
缺：缺解讀、術語第一次出現沒解釋、破折號當括號連用。  
改寫：  
「Skill mix 的重點可以先抓一個方向：這是 **product team，不是 research team**。這裡說的 product 不是對外收費的產品，而是給內部工程師每天走的 paved road，也就是 runtime、sandbox、AGENTS.md template、eval framework 與成本觀測這些共用能力。所以這個 pod 最需要的，不是模型研究背景，而是做過 developer tooling、CI、test infra 的人。Security 那 0.5 個人我會建議用借的，讓資安 team 從一開始就在設計裡，比事後被稽核打回來便宜得多。」

5. 小節：四、Champion 制度：最常被做壞的一環  
原文：「Champion 不是頭銜，是一份有 job description 的工作。做壞的方式千篇一律：找最資深的人掛名、不給時間、不列考核，半年後制度名存實亡.」  
吃力：舊文常會補「為什麼這會發生」；這裡像結論句，少了組織現場的畫面。  
缺：缺鋪陳、缺例子。  
改寫：  
「Champion 制度最容易被誤會的地方，是把它當成榮譽頭銜，而不是一份有 job description 的工作。很多組織一開始都做得很漂亮：每個 team 指派一位最資深的人、開一個 channel、宣布 guild 成立。但如果沒有保留時間、沒有明確產出、也沒有把 adoption 指標放進考核，半年後通常只會剩下一串名單。這時候 champion 還在，只是制度已經名存實亡。」

6. 小節：四、Champion 制度：最常被做壞的一環  
原文：「**Guild 運作**：雙週一次 guild meeting，內容只有三種—內部 demo、痛點清單（帶回 platform 的 backlog）、以及最有價值的：**失敗案例分享**。agent 在哪裡把事情做砸、為什麼，是整個組織最稀缺的學習材料.」  
吃力：舊文會把「失敗案例」為何珍貴多說一步；這裡太快進入清單。  
缺：缺解讀、缺連接詞、破折號當括號連用。  
改寫：  
「**Guild 運作**：雙週一次 guild meeting 就夠了，內容也不要貪多。第一是內部 demo，讓大家看見 paved road 真的怎麼用；第二是痛點清單，把 domain team 卡住的地方帶回 platform 的 backlog；第三，也是我認為最有價值的，是 **失敗案例分享**。agent 在哪裡把事情做砸、為什麼做砸、當時 guardrails 為什麼沒有接住，這些才是整個組織最稀缺的學習材料。」

7. 小節：五、與現有組織的整併決策  
原文：「多數公司已經有 DevEx team、Platform team 或 SRE。agentic 歸誰？用這棵決策樹：」  
吃力：舊文會先把決策壓力說清楚；這裡直接丟問題，圖的判讀目的偏薄。  
缺：缺過場、缺導讀。  
改寫：  
「接著會碰到一個很實際的問題：多數公司不是白紙一張，通常已經有 DevEx team、Platform team 或 SRE。這時候 agentic 不該因為名字新，就自動長出一條平行組織線。比較好的問法是：現有的 internal developer platform 能不能吸收這個 mission？如果不能，是暫時不能，還是能力上根本不適合？下面這棵決策樹，就是用來把這個討論從政治問題拉回組織能力問題。」

8. 小節：五、與現有組織的整併決策  
原文：「SRE 的角色也一樣：agent observability 直接復用 SRE 的 o11y stack（trace、metrics、alerting），不要讓 platform team 重建一套。差別只在多了幾個新的 signal：run id、tool call、retry 與 token 用量.」  
吃力：舊文第一次出現術語時會補用途；o11y stack 與 signal 對非 SRE 讀者偏快。  
缺：術語第一次出現沒解釋、缺解讀。  
改寫：  
「SRE 的角色也可以用同樣邏輯看待。agent observability 不需要讓 platform team 重新蓋一套觀測平台，而是直接復用 SRE 已經在營運的 o11y stack，也就是 trace、metrics、alerting 這些既有能力。真正新增的是觀測維度：run id 用來串起一次 agent 執行，tool call 用來看它碰了哪些外部能力，retry 用來衡量不穩定性，token 用量則把成本拉進同一張圖裡。」

9. 小節：六、預算與提案：向 CFO 說什麼  
原文：「**ROI 敘事**：不要用「取代幾位工程師」—這個敘事第一會嚇到團隊，第二根本不準。用 **attention 槓桿**：human review minutes / PR 的下降 × PR 總量 = 釋放出來的工程注意力；搭配 production escape rate 持平的證據，證明速度沒有用品質換來.」  
吃力：舊文會把公式前後的解讀補足；這裡公式有力，但 CFO 與工程團隊各自要聽什麼沒有鋪開。  
缺：缺解讀、術語第一次出現沒解釋、破折號當括號連用。  
改寫：  
「**ROI 敘事**：我不建議用「取代幾位工程師」作為主軸。這個說法第一會嚇到團隊，第二也不準，因為 agentic engineering 比較像把工程注意力重新分配，而不是簡單刪掉人力。比較能對 CFO 與工程團隊同時說得通的，是 **attention 槓桿**：human review minutes / PR 的下降 × PR 總量 = 釋放出來的工程注意力。再搭配 production escape rate 持平的證據，才能說明速度提升不是拿品質去換。」

10. 小節：七、人才：招募、轉型與 junior 路徑  
原文：「**招募**：JD 的關鍵字不是 prompt engineering。要找的是做過 developer tooling、CI、test infra、文件系統的人，外加一個難量化但關鍵的特質：**能忍受非確定性系統的 debug 心性**—agent 的失敗不可完全重現，跟傳統軟體的除錯體驗完全不同.」  
吃力：舊文會用一兩句把「為什麼不是 prompt engineering」講透；這裡判斷正確但跳太快。  
缺：缺鋪陳、缺解讀、破折號當括號連用。  
改寫：  
「**招募**：JD 的關鍵字不是 prompt engineering。真正要找的，是做過 developer tooling、CI、test infra、文件系統的人，因為這個角色每天要處理的是工程師怎麼把 agent 放進既有 workflow，而不是單純寫出漂亮 prompt。除此之外，還有一個難量化但很關鍵的特質：**能忍受非確定性系統的 debug 心性**。agent 的失敗常常不可完全重現，錯誤也不一定穩定落在同一條路徑上，這跟傳統軟體的除錯體驗完全不同。」

11. 小節：七、人才：招募、轉型與 junior 路徑  
原文：「這條路徑產出的是「會定義問題與驗收條件的工程師」—正好是 agent 時代最稀缺的能力。跳過這條路徑、把 review 全部留給 senior 的組織，三年後會發現自己沒有接班梯隊.」  
吃力：舊文常在結論前補一層「這代表什麼」；這裡直接收斂，力道有，但略像 slide。  
缺：缺解讀、缺過場、破折號當括號連用。  
改寫：  
「這條 junior 路徑真正產出的，不只是比較會用工具的人，而是「會定義問題與驗收條件的工程師」。這點在 agent 時代會變得更稀缺，因為很多工作可以被委派，但什麼叫做做對、風險在哪裡、哪些地方需要 human review，仍然要有人能判斷。若組織跳過這條路徑，把 review 全部留給 senior，短期看起來比較快，三年後大概會發現自己沒有接班梯隊。」

**全篇層級**
章節開場與收尾：主線清楚，但多數章節開場偏像會議備忘錄。舊文常見的「源起、前一節留下的問題、這節要解哪個坑」可以補一兩句，尤其是一到二、三到四、五到六之間。結尾有承接下一篇，但可以再多一句回到本篇的核心提醒，避免只像系列導覽。

圖表前後導讀：RACI 圖、200 人 org chart、整併決策樹都有用，但圖前導讀偏短。RACI 前要先解釋 RACI；200 人圖後可補「為什麼 Security 是 0.5」已經有，但圖前可以先說這不是標準答案；三種規模表格前後要提醒讀者看「升級訊號」而不是只看 headcount。

術語第一次出現：建議補一行 local definition 的術語包括 `Platform + Federation`、`RACI`、`paved road`、`champion`、`IDP`、`o11y stack`、`policy as code`、`FinOps`、`attention 槓桿`、`production escape rate`、`retry tax`、`golden workflow`。不用寫成 glossary，只要第一次出現時順手交代。

hedge：這篇的 hedge 比 October drafts 好很多，但仍有幾句太絕對，例如「production ownership 永遠在 domain team」、「長期一定合併」、「如果提案裡出現...把它刪掉」。這些可以保留銳利度，但補上「在多數產品工程組織裡」、「我會建議」、「除非你真的在做 infra vendor」之類的責任邊界，會更像舊文的成熟口吻。

**不要再加字**
這些段落已經順，不建議稀釋：

「> **TL;DR** — 這是[《別急著打造你的 Devin》](https://fantasybz.medium.com/%E5%88%A5%E6%80%A5%E8%91%97%E6%89%93%E9%80%A0%E4%BD%A0%E7%9A%84-devin-agentic-engineering-%E7%9A%84%E7%B5%84%E7%B9%94%E7%AD%96%E7%95%A5%E8%88%87-90-%E5%A4%A9%E8%A1%8C%E5%8B%95%E8%97%8D%E5%9C%96-7342ababc417)的第一篇深掘。總論的結論是：不要成立中央 Agent Team，要成立小型的 Agentic Platform Team。這一篇把「怎麼組」講到可以直接拿去開編制會議的程度：三種規模的實際編制、champion 制度的選拔與考核、與現有 DevEx / SRE 的整併決策，以及向 CFO 提案時的預算敘事。」

「> 想要 self-service 的系統，就要先畫出 self-service 的組織圖。」

「三種規模對照：」後面的表格不要展開成散文，表格本身已經夠乾淨。

「組織設計的目標可以壓縮成一句話：」

「> **讓 domain team 保有 context 與 ownership，讓 platform team 保有 leverage 與 guardrails，champion 讓兩邊持續對話。**」

「本文由筆者提出初步構想與章節架構，文字撰寫由 AI（Claude）協作完成，再經筆者逐節校閱與修訂後定稿。文中觀點與判斷為筆者所持，文責亦由筆者自負。」

<!-- tokens: in 514745 out 12457 -->
