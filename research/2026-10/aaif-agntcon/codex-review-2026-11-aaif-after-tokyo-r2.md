# Codex review — 2026-11-aaif-after-tokyo/article.md

> model: gpt-6.1-sol, reasoning: xhigh, 2026-10-25 23:39. 原話照錄，未經摘要。第 2 輪；審的是 2026-10-25 改寫並依前一輪意見修訂後的版本。

我會先讀 STYLE.md 與 style brief，再核對本文、原始材料和舊文引用；全程只讀，不修改檔案，也不讀取你禁止的目錄。審查會優先抓主線斷裂、證據越界與引用失真。
<!-- codex ran: /bin/zsh -lc "pwd && rg --files -g 'STYLE.md' -g 'style_brief.md' -g 'article.md' -g '*transcript.txt' -g '*provenance*' -g '*metrics*' -g '*guide*' -g '*manife -->
<!-- codex ran: /bin/zsh -lc 'cat STYLE.md research/2026-10/style_brief.md' -->
<!-- codex ran: /bin/zsh -lc 'nl -ba 2026-11-aaif-after-tokyo/article.md' -->
<!-- codex ran: /bin/zsh -lc 'cat .context/research/aaif-2026-10-23/keynote-transcript.txt .context/research/aaif-2026-10-23/skills-transcript.txt .context/research/aaif-2026-1 -->
<!-- codex ran: /bin/zsh -lc 'wc -l 2026-11-aaif-after-tokyo/article.md .context/research/aaif-2026-10-23/*-transcript.txt && rg --files .context/research/aaif-2026-10-23/slide -->
<!-- codex ran: /bin/zsh -lc 'cat .context/research/aaif-2026-10-23/keynote-transcript.txt .context/research/aaif-2026-10-23/skills-transcript.txt' -->
目前有一個主線問題：文章把「單次行動的三個問題」和「續用、擴權的長期決策」放在同一條論證裡，第十節甚至明說自己不回答前三題。我會核對這段延伸是否必要，也會追查結尾的操作狀態是否與第十一節一致。
<!-- codex ran: /bin/zsh -lc 'cat .context/research/aaif-2026-10-23/uber-transcript.txt' -->
<!-- codex ran: /bin/zsh -lc 'cat .context/research/aaif-2026-10-23/logfire-transcript.txt' -->
<!-- codex ran: /bin/zsh -lc 'cat .context/research/aaif-2026-10-23/local-transcript.txt' -->
<!-- codex ran: /bin/zsh -lc 'cat .context/research/aaif-2026-10-25/hire/ai-agent-metrics.md .context/research/aaif-2026-10-25/hire/README.md' -->
<!-- codex ran: /bin/zsh -lc 'cat .context/research/aaif-2026-10-23/slides/text/2QlEA-01-from-clicks-to-context-building-an-open-source-evaluation-pipeline-for-ai-agents-ine-s- -->
<!-- codex ran: /bin/zsh -lc "rg --files .context/research/aaif-2026-10-23 .context/research/aaif-2026-10-25 | rg -v '/(kong-demo-source|refinement-3-runs|superseded-series|tit -->
<!-- codex ran: /bin/zsh -lc "rg -n '"'^#{1,4} |三類|三種|自己|G2|golden|holdout|constraint|四個|委派|成功任務|修改卡|人工|未定'"' 2026-10-green-overview/article.md 2026-10-green-testing/article.md -->
<!-- codex ran: /bin/zsh -lc "python3 -B -c 'import json; from pathlib import Path
for name in [\"mcp-skills-spec\",\"mcp-architecture\",\"skillsbench\",\"logfire-vars\",\"mcp- -->
<!-- codex ran: /bin/zsh -lc "sed -n '1,245p' 2026-10-agentic-harness-blueprint/article.md" -->
<!-- codex ran: /bin/zsh -lc "sed -n '1,140p' 2026-10-green-overview/article.md && sed -n '225,370p' 2026-10-green-reliability/article.md" -->
<!-- codex ran: /bin/zsh -lc "rg -n '"'^## |''^### '"' 2026-10-green-reliability/article.md 2026-10-green-testing/article.md 2026-09-agentic-engineering-platform/article.md 202 -->
已核對的舊文引用中，有一處明確錯位：第七節把 constraint tests 指到《綠燈不是驗收》可靠度篇第五節，實際內容在第二節。另有一個更大的技術問題：第六節把 HTTP、JSON-RPC 與工具錯誤當成外部操作是否完成的判據；這會破壞全文原本要建立的「回應狀態與外部效果分開看」。
<!-- codex ran: /bin/zsh -lc "rg -n 'github-writers|github-readers|notification-senders|2000|40|x-analysis-id|x-llm-type|503|rate-limiting|acl|key-auth|consumers|credentials' . -->
<!-- codex ran: /bin/zsh -lc "rg --files .context/research/aaif-2026-10-23/kong-demo-source/agent && sed -n '1,36p' .context/research/aaif-2026-10-23/kong-demo-source/kong/api- -->
<!-- codex ran: /bin/zsh -lc "python3 -B -c 'import json; from pathlib import Path
for name in [\"mcp-skills-spec\",\"mcp-skills-overview\",\"logfire-vars\"]:
 x=json.loads((Pa -->
<!-- codex ran: /bin/zsh -lc "python3 -B -c 'import json,re; from pathlib import Path
patterns={\"skillsbench\":r\"7,308|16.2|84|16 tasks|self.generated|seven|Table 2|five\", \ -->
<!-- codex ran: /bin/zsh -lc "rg --files .context/research/aaif-2026-10-23/video-review | rg '(logfire|uber|local|proxy|keynote|skills)' | rg '(820|1100|1680|1195|685|370|456|4 -->
<!-- codex ran: /bin/zsh -lc "rg -n -A 16 -B 6 'What is an agent|independent|independently|risk rating|risk ratings|failure threshold|threshold|reversibility|financial' .contex -->
<!-- codex ran: /bin/zsh -lc "python3 -B -c 'import json; from pathlib import Path
base=Path(\".context/research/aaif-2026-10-25\")
for name in [\"channel/aaif-videos.json\",\" -->
<!-- codex ran: /bin/zsh -lc "python3 -B -c 'from pathlib import Path
for name, pages in [(\"2QlEA-01-from-clicks-to-context-building-an-open-source-evaluation-pipeline-for-ai- -->
<!-- codex ran: /bin/zsh -lc "rg --files .context/research/aaif-2026-10-23/video-review/proxy | sort && python3 -B -c 'from pathlib import Path
p=Path(\".context/research/aaif- -->
<!-- codex ran: /bin/zsh -lc "sed -n '1,100p' .context/research/aaif-2026-10-23/slides/manifest.json && rg -n '74%|refresh failures|74|server' .context/research/aaif-2026-10-23 -->
來源核對又找到一個數字口徑問題：第六節稱「約 74% 的授權服務」符合錯誤規格，但官方簡報寫的是 refresh failures 的錯誤分布；字幕口述與投影片不一致。這裡不能寫「分母清楚」，應揭露衝突或刪掉比例。Kong 的「鑰匙由櫃台發」也超出了程式碼能支持的說法。
<!-- codex ran: /bin/zsh -lc "python3 -B -c 'import json,re; from pathlib import Path
for n,pats in {\"skillsbench\":[r\"4\\.1\",r\"Table 3\",r\"16\\.2\",r\"16 of 84\"],\"mcp-c -->
<!-- codex ran: /bin/zsh -lc "python3 -B -c 'from pathlib import Path
p=Path(\".context/research/aaif-2026-10-23/slides/text/2QlDa-01-running-an-mcp-proxy-at-scale.txt\")
for i -->
<!-- codex ran: /bin/zsh -lc "sed -n '281,312p' 2026-11-same-spec-spec/article.md && sed -n '27,72p' 2026-09-agentic-org-design/article.md && python3 -B -c 'import json,re; fro -->
<!-- codex ran: /bin/zsh -lc "rg -n 'Mazin|models get a lot|harnesses are even|01:10|22:27|2c945fe' research/2026-09 research/2026-10/aaif-agntcon .context/research/aaif-2026-1 -->
<!-- codex ran: /bin/zsh -lc "python3 -B -c 'from pathlib import Path; import re
s=Path(\".context/research/aaif-2026-10-25/openai-harness.html\").read_text(); print(\"bytes\", -->
查核已完成，正在整理審稿結果。最需要修的是第六節的錯誤語義與 74% 分母、Kong 憑證機制的描述，以及第十、十一節偏離單次行動的主線。Uber 的主要數字與頁碼、Logfire 13:40 的修改內容、PagerDuty 指標公式都能在保存來源中找到；後兩者仍有推論或使用方式需要補強。
<!-- codex ran: /bin/zsh -lc "rg -n '~25%|74%|short-lived|full lease|Zero model|three-step|guardrail' .context/research/aaif-2026-10-23/slides/text/2QlDa-01-running-an-mcp-prox -->
這版仍有會誤導實作的錯誤，也還沒把「三個問題」貫穿到底。以下依 STYLE.md、style brief、保存的字幕、投影片、程式碼與舊文核對；未修改檔案，未讀取禁用目錄。

## 致命問題

1. **六、〈錯誤要能定位，快取要能失效〉：把回應狀態誤寫成外部效果。**

   > 「工具結果裡的 `isError` 說的是業務操作沒有做成。三層都成功才算做到」

   `isError` 不足以證明沒有產生任何效果：工具可能先改開關，再在後續步驟失敗。HTTP 成功也不證明目標狀態成立；JSON-RPC error 更不只代表「訊息看不懂」。

   **修法：**改成「三層狀態用來定位回應在哪裡失敗；操作是否生效，仍須查操作紀錄與目標狀態；任務是否完成，再依原要求驗收」。這是全文最不能寫錯的地方。

2. **六、〈錯誤要能定位，快取要能失效〉：74% 的分母存在來源衝突。**

   > 「她也給了一個分母清楚的數字：在 Anthropic 觀察到的授權服務裡，只有約 74%……」

   字幕約 09:06 確實說 servers，但官方簡報 PDF 第 19 頁、錄影約 09:22 的標題寫的是 **refresh failures**，接著列出 74%／10%／16% 的錯誤分布。不能把這寫成「分母清楚」。[簡報文字](/Users/kochi.chuang/conductor/workspaces/medium-articles/dodoma/.context/research/aaif-2026-10-23/slides/text/2QlDa-01-running-an-mcp-proxy-at-scale.txt:360)

   **修法：**揭露口述與投影片口徑不同；未取得樣本說明前，刪除服務比例的判斷，或只描述投影片呈現的錯誤分布。

3. **二、〈被限流之後，先確認哪些步驟已經完成〉：把驗證憑證寫成核發憑證。**

   > 「不同角色拿不同鑰匙，而且鑰匙由櫃台發，不寫在代理的程式裡。」

   保存版是在 Kong 設定 consumer 的 key-auth credentials；agent 從環境變數取得對應 API key，再附在請求上。這能支持集中驗證與政策管理，不能支持 Kong 在此實作中負責發證，也不能暗示 agent 不持有憑證。[Kong 設定](/Users/kochi.chuang/conductor/workspaces/medium-articles/dodoma/.context/research/aaif-2026-10-23/kong-demo-source/kong/api-gateway/base-config.yaml:15)、[agent 設定](/Users/kochi.chuang/conductor/workspaces/medium-articles/dodoma/.context/research/aaif-2026-10-23/kong-demo-source/agent/config.py:119)

   **修法：**寫成「各角色使用不同憑證，Kong 依身分套用群組政策；agent 仍需持有或取得自己的憑證」。

4. **TL;DR／十、全節／十一、全節：三個問題被換成三個決定，最後又增加兩個決定。**

   > 「本文把每一次行動拆成三個問題」
   >
   > 「它不回答單次行動的三個問題」
   >
   > 「三列證據對應同一個操作，卻各自獨立。」

   「允許／發生／完成」是查核面向；「止血／接受修補／更新 skill」是決策對象。三列表格也不是同一個操作，而是同一次調查衍生的不同決定。再加入續用與擴權，主線就從單次行動往外擴成整套產品營運。

   **修法：**第十一節讓每個決定都回答允許、發生、完成三題。第十節完整 H.I.R.E. 與季度投資決策移到延伸閱讀；本篇只留下能補足行動查核的紅線紀錄與評分器校準。

## 重要問題

1. **三、閱讀地圖：把機制與前提列成已提供的證據。**

   > 「完成：行動結果能回饋給模型」
   >
   > 「允許：程序的來源識別與內容指紋核對」

   能取得回饋，是驗收的前提；來源與 digest，是內容識別與一致性的依據。兩者分別不等於任務完成、程序獲准。

   **修法：**將第二欄改為「提供的機制／能支持的判斷」，再明列回饋內容、核准紀錄與驗收結果各由誰提供。否則正文的區分被導覽表自己混掉。

2. **三、NTT DOCOMO 段：recall 正確，但推論接錯層。**

   > 「這正是《綠燈不是驗收》總論把證據分成三類的理由」

   舊文的三類在處理證據由誰確認、誰能自行修改；NTT 案例新增的是「紀錄能否分辨被拒絕、執行失敗與參與者誤認」。不是再證明一次只有團隊測試能當閘門。

   **修法：**補出新結論：**受保護的測試回答產出是否符合要求，操作紀錄回答實際做過什麼，兩者不能互相替代。**刪掉一部分舊分類重述。

3. **七、〈同時驗證工作能完成、越界會被拒絕〉：recall 章節錯誤。**

   > 「這和《綠燈不是驗收》可靠度篇把 review 約束寫成 constraint tests 是同一個習慣」

   相關內容在可靠度篇**第二節**，不是其他引用集中使用的第五節；本句也未提供定位連結。[原節](/Users/kochi.chuang/conductor/workspaces/medium-articles/dodoma/2026-10-green-reliability/article.md:35)

   **修法：**直接標第二節，並交代新增之處：舊文主要驗證程式與合併約束，本篇驗證執行環境是否真的拒絕指定效果。

4. **九、〈把生產錯誤變成有明確預期的測試〉：把潛在失敗模式寫成 optimizer 的既定職責。**

   > 「optimizer 的問題則是同時決定『應該做到什麼』與『自己有沒有做到』」

   展示中的 optimizer 提出修改，人檢視並套用；演講還明說自動產生 eval 當時未上線。來源沒有顯示它已同時掌握要求與驗收。

   **修法：**改成條件句：「若讓 optimizer 連判準一起修改，再用修改後的判準驗收，就會……」。保留這是作者延伸分析的標示。

5. **十、〈五個指標，量的是摩擦而不是點擊〉：從兩個比例跳到能力診斷。**

   > 「一次解決率很高、放棄率也很高，表示 agent 在它擅長的小範圍很準，其他地方沒用。」

   HIRE 文件也有這句，但仍不是必然推論。IRR 分母是可解決對話，DIY 分母是全部對話；任務組成不同就可能同時偏高。

   **修法：**改成「可能存在能力範圍落差，須按 intent、版本與使用族群分群確認」。不能把來源作者的概括直接升格成診斷規則。

6. **六、〈先處理憑證取得與更新的競爭〉：把來源已有的設計當成自己的補充。**

   > 「我會再補一條：鎖本身要有到期時間」

   官方簡報第 15 頁已寫 short-lived lock，第 16 頁也談等待完整 lease。[來源](/Users/kochi.chuang/conductor/workspaces/medium-articles/dodoma/.context/research/aaif-2026-10-23/slides/text/2QlDa-01-running-an-mcp-proxy-at-scale.txt:262)

   **修法：**歸還講者。作者真正可以往下追的是：鎖過期時原 worker 仍在換發，接手者如何避免再次使用同一枚舊 token？單純加到期時間沒有解決這個競爭。

7. **二、〈把「允許、發生、完成」拆開看〉：晚間保存版與午休觀察仍容易被讀成同一次實證。**

   > 「Gateway 正確執行了限流……工程師代理已經完成建立 PR 的工具操作」

   午休截圖支持介面顯示 Blocked；PR 工具先成功、後遇 429 的路徑來自保存版手冊。版本相同尚未確認，不能讓讀者自行拼成午休執行的完整事實。

   **修法：**本段開頭直接寫「依晚間保存版手冊描述的路徑」。版本限制會改變判讀，不宜只留文末。

8. **五至十一節：下列轉場沒有真正交接前一節的結果。**

   | 位置與原句 | 問題與修法 |
   |---|---|
   | 六、導言：「前一節的程序描述了理想順序，實際執行卻會遇到……」 | 只是從理想到現實的通用轉折。改問：程序內容已核准，為何仍無法知道一次呼叫是否生效？ |
   | 六、〈錯誤要能定位，快取要能失效〉：「快取則把同一個資訊落差延伸到時間。」 | 從操作結果未知跳到工具清單過期，未知的對象換了。先說「失敗紀錄處理呼叫結果；快取另有授權資訊過期的問題」。 |
   | 六、結尾：「下一場把模型搬回私有環境，問的正是這件事。」 | 私有部署本身不回答 proxy 以外的路徑是否受控。改成「下一場提供另一種部署方式，讓我們檢查限制是否涵蓋整條路徑」。 |
   | 九、結尾：「這個 agent 整體值不值得繼續投入，是另一個問題」 | 明確另開主題，沒有推進原三題。移走完整長期營運討論。 |
   | 十一、開頭：「現在把假設的 crash 調查走完一次。」 | 第十節得到的分類與校準結果沒有進入這次調查，只是回到中斷的故事。若保留第十節，須讓評分可靠性實際改變第十一節的決定。 |

9. **十二、第二段：已知狀態與操作歸因沒有在結尾分清。**

   > 「附遠端回查到的開關版本」
   >
   > 「待查的是那筆逾時的請求究竟有沒有改到開關。」

   兩句可以同時成立，但結尾沒有說明：現在是「目標狀態已確認、操作歸因未知」，還是連暫緩都尚未確認。

   **修法：**明寫是哪一種。不要再用含混的「操作結果待查」收束全文。

## 次要問題

1. **三、NTT DOCOMO 段：5/6 容易被讀成任務正確率。**

   > 「實際成功的 session 卻只有五次。」

   投影片第 9–11 頁顯示，另一場是在 session 中未完成成功驗證，最後由操作者放棄；停止規則也未標準化。

   **修法：**補這個失敗定義，避免讀者把它讀成六份中有一份修錯。

2. **五、〈驗證更新時，把授權要求留在比較裡〉：研究數字離本文情境太遠。**

   > 「人工整理的 skill 平均提高通過率 16.2 個百分點」

   數字可對到 SkillsBench，但跨領域平均不是 crash 調查程序的預期收益。來源的 Software Engineering 分組增益是 4.5 個百分點。

   **修法：**縮短總量介紹，保留任務間退步與領域差異；不要讓跨領域平均成為讀者最容易記住的承諾。

3. **八、〈把驗證依據交出去，才有可接手的 PR〉：plugin 被過度等同。**

   > 「plugin 就是第五節談的那種程序與工具的組合，在 Uber 市集裡的形式。」

   第五節介紹的是 MCP 分發 skill；沒有證據顯示 Uber plugin 與該 extension 是同一種封裝或使用相同核准機制。

   **修法：**寫成 Uber 使用的擴充套件，可能包含 skill 與工具配置；兩者共通的是程序維護問題。

4. **九、導言：trace 的涵蓋範圍說得過滿。**

   > 「Trace 記錄這次工作裡的每一步、每次工具互動與結果」

   只能看到實際納入 instrumentation 的部分。

   **修法：**改成「展示中的 trace 保留了已納管的步驟與工具互動」，並把缺失紀錄列為待查，不能把沒有 span 當成沒有執行。

5. **十、〈先寫職位說明，再談要不要僱用〉：框架面向被寫成固定程序。**

   > 「四個字母真的就是僱用一個人的檢查順序。」

   來源將它們列為四個面向，沒有建立必須依序執行的程序。

   **修法：**改成「四個檢查面向」。

6. **十、〈讓評分器自己也被評分〉：規則的確定性被寫成正確性。**

   > 「這一層沒有模型，不會漂移也不會幻覺。」

   這是講者的主張，但固定規則仍可能分類錯誤，事件與 taxonomy 改版也會改變口徑。

   **修法：**限定為沒有模型抽樣與模型版本造成的變動；規則仍需版本與正反案例。

7. **十、〈讓評分器自己也被評分〉：成本推論過於確定。**

   > 「門檻調高，人工佇列與成本就跟著增加。」

   先增加的通常是升級處理量；是否進人工，還取決於強模型能否解決。

   **修法：**拆開強模型處理量、人工量與總成本。

8. **五、OpenAI 段／References 11：本機保存內容不足以完成核對。**

   > 「文件被當成 agent 工作的依據，由 linter 與結構測試檢查」

   `openai-harness.html` 保存的是驗證頁，沒有文章正文。此處應列為本次無法獨立核實，不能算完成來源核對；這不等於判定引述錯誤。

   **修法：**補可核對的正文摘錄或刪掉這段額外背書。Mazin 引句同樣只能核對到作者研究筆記，仍須保留聽寫身分。

## 建議刪除

以下段落刪掉後，主要論證不會少一個必要步驟。

| 位置與原句 | 處理 |
|---|---|
| 一、旅帖段：「就順手把工具改成支援多趟旅行」 | 刪整段。它在回答工具是否有用，沒有推進行動證據。邀請、家人與購物任務留簡短背景即可。 |
| 一、末段：「本文使用五場東京演講……」 | 縮成一句，完整清點留〈核對方法〉。 |
| 三、harness 段：「我在〈Harness 藍圖〉把這個環境拆成五層」 | 刪五個名詞逐一介紹。後文沒有逐層使用這份分類，反而形成第二套導覽。 |
| 四、〈請求可以無狀態，任務與授權仍要接得下去〉中的 stateless、Tasks 詳解 | 移第二篇；本篇留下「任務識別不證明操作只做一次」與當次授權即可。 |
| 五、〈來源與內容要一起核對〉：「OpenAI 今年 2 月的……也是同一個方向」 | 刪。重複前面的文件維護論點，又增加來源負擔。 |
| 十、完整 H.I.R.E. 縮寫展開及五指標教學 | 移營運延伸文；本篇保留紅線與 evaluator 校準的必要部分。 |
| 十一、末段：「這三個時刻累積一季之後……」 | 移走季度續用與 G2 詳解。這裡主要重述營運篇與可靠度篇。 |
| 十二、第二段：「三份紀錄和一項待查結果」 | 刪大部分清點。第十一節才剛逐項講完。 |
| 十二、開源貢獻段：「這也讓開源貢獻有了實際起點。」 | 移文末短註。這是另一個值得談的問題，尚不是本文結論所需。 |

邀請與午休實作可以留下：前者交代為何到場，後者確實改變作者的問題。澀谷照片目前只負責旅程收尾，保留短段即可；不必硬把晨跑寫成技術寓言，也不必加入本篇沒有的東京鐵塔經驗。

## 建議補充

1. **各場第一性原理還缺的下一步。以下都應標成作者推論或未執行的設計。**

   | 位置與原句 | 應補的推論與代價 |
   |---|---|
   | 二、gateway 段：「全部走這個櫃台」 | 集中政策也集中故障影響。補 gateway 不可用時哪些工作停止；任務識別與群組政策由可信的哪一端決定，避免把請求自帶標籤當成授權依據。 |
   | 四、〈讓回饋能分辨真正的改善〉：「每千次 session 發生幾次 crash」 | 暫緩後可能根本沒有相同觸發條件的曝光。補分母為零或不可比較時不能判定修補有效，以及何時安排受控觀察。 |
   | 五、〈來源與內容要一起核對〉：「工具與執行環境的版本要由誰保存」 | 不要停在問題。指定平台保存工具契約與環境版本，程序維護者確認相容範圍；任一項變更觸發哪組回歸。代價是維護完整依賴關係。 |
   | 六、〈先處理憑證取得與更新的競爭〉：「維持單一更新者的代價是等待」 | 再補 lease 過期、原更新者未結束的路徑。說清楚何時停止自動恢復、轉重新授權，不能讓鎖成為「已解決競爭」的口號。 |
   | 七、〈資料邊界必須在讀寫與連線時生效〉：「每個入口……都算」 | 接回〈Harness 藍圖〉第四、六節已指出的白名單外傳問題：允許連 GitHub，不代表允許把資料寫進公開 comment。新增的是驗證操作對象與輸出，而非再重述要有 sandbox。 |
   | 八、〈固定資料蒐集流程，把判斷留給需要推理的步驟〉：「每個節點各有……回合上限」 | 回合上限控制消耗，不能判定資料足夠。補缺原始 log、證據互相衝突、無法重現時的人工出口，避免固定流程把缺資料包成高信心結論。 |
   | 九、〈回復舊版工作指引，仍要確認外部狀態〉：「這一次實際使用哪一版」 | 一次任務可能跨多次取值。補任務是否固定版本，或逐步保存實際版本；否則同一個 trace 可能混用新舊程序，無法重現。 |
   | 十、〈讓評分器自己也被評分〉：「信心門檻就是在這批資料上挑的」 | 將選門檻的校準資料與最後報告準確性的資料分開；另列漏判越權與誤判正常行為。只說 gold set 不足以回答評分器是否可信。 |

2. **十一、決策表：現在是紀錄清單，還不是完整的接受條件。**

   > 「最低紀錄」

   有核准時間、操作識別，不代表核准仍有效，也不代表操作符合要求。

   **修法：**每列增加「可繼續的條件」。暫緩 rollout 至少填出：核准的開關與環境、允許的狀態變更、有效期間、執行前對象版本，以及執行後預期狀態。資料只是欄位，條件才會改變決定。

3. **十一、逾時案例：補上等待與不採取行動的代價。**

   > 「查不到就交人工核對，不重送寫入。」

   Staff engineer 下一個問題會是：交給誰、多久必須接手、事故仍擴大時怎麼辦？

   **修法：**加一個依團隊事故政策設定的接手期限與升級入口；允許 agent 繼續唯讀調查，同時凍結有疑義的寫入。不要讓「未知」變成沒有負責人的終點。

4. **八、平台與領域分工段：補真正有增量的組織 recall。**

   > 「平台團隊維護 harness，領域團隊提供調查知識」

   這正好能接〈Agentic Engineering 組織篇〉第二節的 RACI，而本文沒有接。

   **修法：**指出當固定 collector 漏資料、領域 skill 誤判、工具越權時，分別誰負責修正；production ownership 仍由領域團隊承擔。這比再次介紹 harness 五層更有用。

5. **九、offer_id 段：把低成本預防寫成可以驗收的工具契約。**

   > 「工具仍應在產生訂位效果前，核對它收到的 offer……」

   **修法：**補一組正反例：有效且屬於這次搜尋的 offer 可以送出；route_id、過期 offer 或其他使用者的 offer 被拒絕，且沒有建立訂位。這才把 prompt 修正往工具保證推進一步。

## 術語仍難懂的清單

| 首次需要的位置與原句 | 仍缺什麼／具體修法 |
|---|---|
| 一：「AAIF」「CNCF」「Linux Foundation」 | 三個組織關係未交代。首次用一句說明活動主辦與基金會歸屬，保留作者無法確認邀請原因的限制。 |
| 一：「Agentic Engineering 的起點」 | 只說重新分工仍偏抽象。用同一個 crash 工作說明：人定要求與核准、agent 調查、平台提供受控工具。 |
| 二：「read、write、dangerous 三級授權」 | 分類名稱不是例子。直接配查 crash、建草稿 PR、變更 production 開關，再說級別依效果與對象判斷。 |
| 二／六：「gateway」「proxy」 | 個別比喻有了，兩者的關係沒有。說明它們在各自案例中都是中介，但負責的政策與憑證工作不同，並非必須串接的兩層。 |
| 三：「context……feedback……guardrails」 | 五個英文名詞一次出現，讀者還不知道後文為何需要整套分類。刪名詞清點，保留調查所需資料、結果與限制。 |
| 五：「用 CI……用 golden tasks」 | CI 到第七節才解釋；golden tasks 未就地說明。先說「文件改版後，重做固定的幾個調查任務，比較結果」，再命名。 |
| 五：「dynamic」 | 知道不能固定指紋，還不知道情境。補「同一位址每次依即時資料產生不同程序」，再說為何舊核准不能涵蓋新內容。 |
| 六：「scope，例如 offline_access」 | 中文「授權範圍」仍不夠。補「允許使用者離線時繼續換發憑證」這個用途，並保留供應商差異。 |
| 六：「JSON-RPC」「isError」 | 目前解釋會教錯。用同一次開關操作，分別示範找不到方法、參數不合規、執行途中失敗；外部效果另查。 |
| 七：「限制執行指令的 shell」 | shell 只是新名詞。先說「agent 能透過終端機啟動其他程式」，再引入 shell，接到為何封鎖單一命令不足。 |
| 五／七：「linter」「結構測試」「靜態分析」 | 三者靠中文名稱仍難區分。各給一個輸入與失敗例：失效連結、缺必要章節、未執行程式便查出危險寫法。 |
| 八：「plugin」 | 與 skill、MCP server 的封裝關係不清。限定為 Uber 市集套件，避免把不同系統的名稱視為同一規格。 |
| 八：「20 回合」 | 一回合包含哪些互動沒有交代。說明這是該 harness 的 turn 計數，不能直接換算成工具次數或通用成本門檻。 |
| 十一：「G2……原有三條加新增四條」 | 只有代號與條件數量，讀者必須離開本文才知道在判什麼。移至延伸閱讀；若保留，至少交代評估範圍與它不取代當次核准。 |

`digest`、兩種 token、sandbox、feature flag／rollout 已有情境解釋；主要缺口是彼此的責任與判斷邊界。`commit point`、`optimistic locking`、`compaction`、`RRF`、`oracle` 未出現在本篇，不應為了補術語再塞進來。

<!-- tokens: in 5019114 out 25327 -->
