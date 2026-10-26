# Codex review — 2026-11-aaif-after-tokyo/article.md

> model: gpt-6.1-sol, reasoning: xhigh, 2026-10-26 00:12. 原話照錄，未經摘要。第 3 輪；審的是 2026-10-25 改寫並依前一輪意見修訂後的版本。

我會先讀 STYLE.md 與 style brief，再核對逐字稿、投影片、demo 原始碼及前作。全程只讀取 repository 內的資料，不修改檔案。
<!-- codex ran: /bin/zsh -lc 'cat STYLE.md' -->
<!-- codex ran: /bin/zsh -lc 'cat research/2026-10/style_brief.md' -->
<!-- codex ran: /bin/zsh -lc "sed -n '65,200p' research/2026-10/style_brief.md" -->
<!-- codex ran: /bin/zsh -lc 'wc -l 2026-11-aaif-after-tokyo/article.md .context/research/aaif-2026-10-23/*-transcript.txt' -->
<!-- codex ran: /bin/zsh -lc "rg --files -g 'article.md' -g '"'!agents/**'"' -g '"'!'"\\.claude/**' 2026-10-green-* 2026-09-agentic-engineering-platform 2026-09-agentic-org-des -->
<!-- codex ran: /bin/zsh -lc "rg --files --hidden -g '"'!'"\\.git/**' -g '"'!agents/**'"' -g '"'!'"\\.claude/**' .context/research/aaif-2026-10-23 .context/research/aaif-2026-1 -->
<!-- codex ran: /bin/zsh -lc 'cat .context/research/aaif-2026-10-23/facebook-post-provenance.json' -->
<!-- codex ran: /bin/zsh -lc 'cat .context/research/aaif-2026-10-23/keynote-transcript.txt .context/research/aaif-2026-10-23/skills-transcript.txt' -->
<!-- codex ran: /bin/zsh -lc "rg --files --hidden -g '"'!**/.git/**'"' -g '*.txt' -g '*.md' -g '*.json' .context/research/aaif-2026-10-23/slides/text .context/research/aaif-202 -->
<!-- codex ran: /bin/zsh -lc "rg -n '"'^##|''^###|允許|三類|三種|獨立|團隊擁有|constraint tests|frozen holdout|G2|Red Line'"' 2026-10-green-overview/article.md 2026-10-green-reliability/ar -->
<!-- codex ran: /bin/zsh -lc 'cat .context/research/aaif-2026-10-23/facebook-post-provenance.json' -->
<!-- codex ran: /bin/zsh -lc "sed -n '160,337p' .context/research/aaif-2026-10-23/skills-transcript.txt" -->
<!-- codex ran: /bin/zsh -lc "rg --files .context/research/aaif-2026-10-23/slides/text | rg '2So56|2QlEA|2QlDI|2QlLo|2QlDa|2QlEY'; rg --files --hidden -g '"'!**/.git/**'"' -g ' -->
目前看到的主要問題是主軸分岔：前半問單次行動的「允許、發生、完成」，後半轉向程序更新與長期產品評估。接下來會核對這些延伸是否改變了同一個決定，以及引用前作時是否只是重述既有規則。
<!-- codex ran: /bin/zsh -lc 'cat .context/research/aaif-2026-10-23/proxy-transcript.txt' -->
<!-- codex ran: /bin/zsh -lc 'cat .context/research/aaif-2026-10-23/slides/text/2QlDa-01-running-an-mcp-proxy-at-scale.txt' -->
<!-- codex ran: /bin/zsh -lc 'cat .context/research/aaif-2026-10-23/slides/text/2So56-01-agntcon2026-ntt-docomo-business-kota-tsuyuzaki.txt' -->
<!-- codex ran: /bin/zsh -lc "rg --files --hidden -g '"'!**/.git/**'"' -g '"'!**/agents/**'"' -g '"'!**/.claude/**'"' -g '"'!**/video-review/**'"' -g '"'!**/node_modules/**'"'  -->
<!-- codex ran: /bin/zsh -lc 'cat .context/research/aaif-2026-10-23/uber-transcript.txt' -->
<!-- codex ran: /bin/zsh -lc "rg --files --hidden -g '"'!**/.git/**'"' -g '"'!**/agents/**'"' -g '"'!**/.claude/**'"' -g '"'!**/video-review/**'"' -g '"'!**/node_modules/**'"'  -->
<!-- codex ran: /bin/zsh -lc 'cat .context/research/aaif-2026-10-23/logfire-transcript.txt; cat .context/research/aaif-2026-10-25/hire/ai-agent-metrics.md' -->
<!-- codex ran: /bin/zsh -lc 'cat .context/research/aaif-2026-10-23/slides/text/2QlEA-01-from-clicks-to-context-building-an-open-source-evaluation-pipeline-for-ai-agents-ine-s- -->
<!-- codex ran: /bin/zsh -lc "rg --files --hidden -g '"'!**/.git/**'"' -g '"'!**/agents/**'"' -g '"'!**/.claude/**'"' .context/research/aaif-2026-10-23/sources .context/researc -->
<!-- codex ran: /bin/zsh -lc 'cat .context/research/aaif-2026-10-25/hire/README.md; cat .context/research/aaif-2026-10-23/facebook-invitation-2026-08-24.json' -->
<!-- codex ran: /bin/zsh -lc 'cat .context/research/aaif-2026-10-23/local-transcript.txt' -->
<!-- codex ran: /bin/zsh -lc "rg --files --hidden -g '"'!**/.git/**'"' -g '"'!**/agents/**'"' -g '"'!**/.claude/**'"' -g '"'!**/node_modules/**'"' -g '"'!**/video-review/**'"'  -->
<!-- codex ran: /bin/zsh -lc "rg -n -C 3 '74%|10%|16%|92%' .context/research/aaif-2026-10-23/slides/text/2QlDa-01-running-an-mcp-proxy-at-scale.txt; rg -n '"'^##|''^###'"' 2026 -->
<!-- codex ran: /bin/zsh -lc "python3 -c 'import json,pathlib; base=pathlib.Path(\".context/research/aaif-2026-10-23/sources\"); names=[\"mcp-caching.json\",\"aaif-skills.json\ -->
<!-- codex ran: /bin/zsh -lc "sed -n '57,249p' 2026-10-agentic-harness-blueprint/article.md; sed -n '27,72p' 2026-09-agentic-org-design/article.md" -->
<!-- codex ran: /bin/zsh -lc "sed -n '93,145p' 2026-11-agentic-eval-economics/article.md; sed -n '209,279p' 2026-11-agentic-eval-economics/article.md; sed -n '495,539p' 2026-09 -->
<!-- codex ran: /bin/zsh -lc "python3 -c 'from pathlib import Path; dirs=[Path(\".context/research/aaif-2026-10-24\"),Path(\".context/research/aaif-2026-10-25\")]; [(print(d),[ -->
<!-- codex ran: /bin/zsh -lc "sed -n '281,339p' 2026-11-same-spec-spec/article.md; sed -n '312,389p' 2026-11-same-spec-variance/article.md; sed -n '55,72p' 2026-10-green-overvi -->
<!-- codex ran: /bin/zsh -lc "rg -n -C 2 'red-then-green|先紅再綠|"'^## 五'"' 2026-10-green-testing/article.md; sed -n '58,110p' 2026-10-green-reliability/article.md; sed -n '443,47 -->
<!-- codex ran: /bin/zsh -lc "python3 -c 'from pathlib import Path; import json; d=Path(\".context/research/aaif-2026-10-23\"); names=[p for p in d.glob(\"*.json\") if any(t in -->
已找到兩個具體的歸屬問題：第十一節沿用的 G2 說法，與目前〈Eval、單位經濟與規模化〉第五節的分工不一致；第十節把部分評分驗證建議一起稱為「框架的要求」，但簡報只明講人工 gold set 與信心門檻校準。我會把來源要求與作者延伸分開列。
<!-- codex ran: /bin/zsh -lc "python3 -c 'import json,pathlib,re; b=pathlib.Path(\".context/research/aaif-2026-10-23/sources\"); names=[\"skillsbench.json\",\"mcp-architecture. -->
<!-- codex ran: /bin/zsh -lc "python3 -c 'import json,pathlib; b=pathlib.Path(\".context/research/aaif-2026-10-23/sources\"); names=[\"mcp-skills-spec.json\",\"mcp-skills-overv -->
<!-- codex ran: /bin/zsh -lc "rg -n 'x-llm-type|x-analysis-id|github-writers|github-readers|notification-senders|2000|40|503|429|failover|rate-limited' .context/research/aaif-2 -->
<!-- codex ran: /bin/zsh -lc "rg -n 'CREATED_PRS|SENT_NOTIFICATIONS|create_pull|create_pr|Authorization|API_KEY|x-analysis-id|httpx|requests|KONG' .context/research/aaif-2026-1 -->
<!-- codex ran: /bin/zsh -lc "python3 -c 'import json,pathlib; b=pathlib.Path(\".context/research/aaif-2026-10-23/sources\"); cases={\"skillsbench.json\":[(\"7,308\",900),(\"Se -->
<!-- codex ran: /bin/zsh -lc "sed -n '270,400p' .context/research/aaif-2026-10-23/kong-demo-source/kong/api-gateway/base-config.yaml; sed -n '640,670p' .context/research/aaif-2 -->
<!-- codex ran: /bin/zsh -lc "rg -n 'guide|risk|failure threshold|high-risk|independently|independent|workflow|agent' .context/research/aaif-2026-10-25/openai-guide/guide.txt | -->
<!-- codex ran: /bin/zsh -lc "rg -n 'prompt|proposal|arrival|offer_id|route_id|15|min' .context/research/aaif-2026-10-23/video-review/logfire/visual-inspection.json; python3 -c -->
<!-- codex ran: /bin/zsh -lc "rg -n -C 3 'Authorization|API_KEY|x-analysis-id|x-llm-type|kong|KONG' .context/research/aaif-2026-10-23/kong-demo-source/agent/config.py .context/ -->
<!-- codex ran: /bin/zsh -lc "python3 -c 'import json,pathlib; p=pathlib.Path(\".context/research/aaif-2026-10-23/sources/skillsbench.json\"); t=json.loads(p.read_text())[\"tex -->
<!-- codex ran: /bin/zsh -lc "python3 -c 'from pathlib import Path; import re; p=Path(\"2026-11-aaif-after-tokyo/article.md\"); t=p.read_text(); print(\"chars\",len(t),\"CJK\", -->
<!-- codex ran: /bin/zsh -lc "rg -n '"'^##|''^###|東京鐵塔|commit point|compaction|RRF|oracle|optimistic'"' 2026-11-aaif-after-tokyo/article.md 2026-11-aaif-agent-handoffs/article. -->
<!-- codex ran: /bin/zsh -lc "python3 -c 'import json,pathlib; b=pathlib.Path(\".context/research/aaif-2026-10-23/sources\"); t=json.loads((b/\"mcp-skills-spec.json\").read_tex -->
<!-- codex ran: /bin/zsh -lc "python3 -c 'import json,pathlib; b=pathlib.Path(\".context/research/aaif-2026-10-25\"); d=json.loads((b/\"channel/aaif-videos.json\").read_text()) -->
核心案例還有一個操作定義缺口：「暫緩 rollout」有時指停止擴大曝光，有時又接到把 feature flag 關回去。第十一節寫「只准暫緩，不准關閉」，因此必須明定兩者各會改變什麼狀態，否則核准與驗收可能對不上。
<!-- codex ran: /bin/zsh -lc "rg -n 'models get|harnesses are even|Mazin|238|74%|92%' research/2026-10/aaif-agntcon .context/research/aaif-2026-10-23/sources/schedule-sessions/ -->
<!-- codex ran: /bin/zsh -lc "sed -n '240,259p' 2026-11-aaif-after-tokyo/article.md; sed -n '406,450p' 2026-11-aaif-after-tokyo/article.md; sed -n '43,66p' research/2026-10/sty -->
<!-- codex ran: /bin/zsh -lc "python3 -c 'from pathlib import Path; p=Path(\".context/research/aaif-2026-10-23/slides/text/2QlEA-01-from-clicks-to-context-building-an-open-sour -->
<!-- codex ran: /bin/zsh -lc "python3 -c 'from pathlib import Path; p=Path(\"research/2026-10/conference_digest.md\"); t=p.read_text(); lines=t.splitlines(); matches=[i for i,s -->
<!-- codex ran: /bin/zsh -lc "sed -n '352,382p' .context/research/aaif-2026-10-23/slides/text/2QlDa-01-running-an-mcp-proxy-at-scale.txt; sed -n '55,87p' .context/research/aaif -->
<!-- codex ran: /bin/zsh -lc "python3 -c 'import json,pathlib; b=pathlib.Path(\".context/research/aaif-2026-10-23/sources\"); names=[\"otel-sampling.json\",\"logfire-opt.json\" -->
<!-- codex ran: /bin/zsh -lc "rg -n 'MCP|Model Context|clear|well-documented|feedback|compiler' .context/research/aaif-2026-10-23/sources/agents-md-study.json | head -2; sed -n -->
<!-- codex ran: /bin/zsh -lc "rg -n 'Evaluate the evaluator|gold set|confidence|3h of downtime' .context/research/aaif-2026-10-23/slides/text/2QlEA-01-from-clicks-to-context-bu -->
<!-- codex ran: /bin/zsh -lc "python3 -c 'from pathlib import Path; p=Path(\"2026-11-aaif-after-tokyo/article.md\"); t=p.read_text(); terms=[\"commit point\",\"optimistic locki -->
主要數字已對照本地來源，包括 Kong 的 2,000 token／40 秒、NTT 的 6/6 與 5/6、Uber 的 9,000／50%／48%，以及 SkillsBench 與 PagerDuty 的指標。剩下的問題主要是：把提案寫成已修好、把驗證建議歸給講者，以及前作之間尚未一致的授權閘門定義。
目前不宜定稿。主要問題是驗收單位混用、部分來源歸屬過頭，以及後半段逐漸換了問題。以下只列需改處；全程只讀 repository，未修改檔案。

## 致命問題

1. **十一、〈我會帶回團隊的：三個決定，和一張會議用的表〉：結尾把三種決定寫成同一個操作。**

   > 「三列證據對應同一個操作，卻各自獨立。」

   暫緩 rollout 是外部狀態變更；接受修補是對程式產出的判斷；更新 skill 是程序版本的採用。它們屬於同一個調查，卻不是同一個操作，證據也未必獨立：開關狀態會影響重現條件，調查結果會影響程序更新。

   **修法：**改成「三個決定屬於同一個調查，各有驗收對象與依據」。表格明列各自的「允許依據／實際發生的結果／完成判準」，不要把「最低紀錄」整欄一律叫作發生證據。這是全文三題框架最後必須交出的結果。

2. **三、〈我帶回來的問題：三件事要分開問〉及十一：核心操作沒有固定意思。**

   > 「核准範圍（只准暫緩，不准關閉）」

   「暫緩 rollout」可能是維持目前曝光比例、停止擴大；「關閉 feature flag」則可能撤回既有曝光。第八節 Uber 的「把開關關回去」又是另一種處置。本文一路使用「開關已暫緩」，卻沒有定義究竟改了什麼。

   **修法：**第一次建立案例時就固定狀態。例如，假設目前曝光 10%，暫緩表示維持 10%、停止擴大；關閉表示降到 0%。之後核准、請求、遠端回查與成效觀察全部沿用這組意思。否則「允許什麼」和「完成什麼」無法對上。

3. **六、〈錯誤要能定位，快取要能失效〉：仍把 HTTP 回覆說成服務處理證據。**

   > 「HTTP 回應說的是服務有沒有收到並處理這筆請求」

   HTTP 回覆可能由 proxy 或 gateway 產生；收到 504，後端仍可能已執行。`isError` 也不代表工具一定已進入業務操作，可能在檢查參數時就拒絕。後文雖然補上「不能判定外部效果」，前面的定義仍然誤導。

   第三節的生活例子也有同一個問題：

   > 「訂房系統真的收到了嗎」

   收到請求不等於建立預約。

   **修法：**會議室例子改問「預約紀錄真的建立了嗎」。技術段落分清「沒有收到回覆／HTTP 層回覆／JSON-RPC 錯誤／工具結果」，再明講：這些協助定位失敗；操作回執與目標狀態才支持效果判定。

## 重要問題

1. **十、〈讓評分器自己也被評分〉：把作者補充的驗證要求歸給框架。**

   > 「挑門檻用的資料和最後報告準確率的資料要分開，漏判越權與誤判正常行為也要分開列。這是框架的要求」

   [簡報第 25 頁](/Users/kochi.chuang/conductor/workspaces/medium-articles/dodoma/.context/research/aaif-2026-10-23/slides/text/2QlEA-01-from-clicks-to-context-building-an-open-source-evaluation-pipeline-for-ai-agents-ine-s-bolan-os.txt:449)明講的是：各 LLM 層對人工標記的 gold set 評分，信心門檻由資料校準。留存材料沒有明講獨立報告資料集，以及分列漏判、誤判的要求。

   **修法：**在「不是用猜的」後結束框架要求；接著另起一句：「我會另外要求……」。建議可以保留，歸屬必須改。

2. **九、〈回復舊版工作指引，仍要確認外部狀態〉：提案與套用，被寫成修好。**

   > 「到這裡，修好的是一種失敗，判準也仍由人保管。」

   錄影支持找到問題、提出修改、人工檢視與套用；沒有展示本文那組正反案例的比較結果。本文自己也說驗證設計尚未執行。

   **修法：**改成「到這裡，我們找到一種失敗並提出修改；是否改善，還要經過保留判準的驗證」。不能在轉場時把尚待驗證的提案升格成成果。

3. **十一及十二、〈延伸閱讀：本文接回的幾篇〉：G2 的 recall 繼承了系列內部矛盾。**

   > 「擴權走可靠度篇第五節的 G2 閘門，那是營運篇三道擴張閘門的第二道」

   本篇確實跟著可靠度篇寫；但[目前營運篇第五節](/Users/kochi.chuang/conductor/workspaces/medium-articles/dodoma/2026-11-agentic-eval-economics/article.md:209)把 G2 定為「規模驗證」，個別 write tools 另行審核；G3 才處理深度授權與特定高風險操作。兩篇的 G2 已不是同一個意思。

   **修法：**先統一系列定義。本篇至少明確分開「擴大使用團隊」與「開放某項寫入」，不能用一個 G2 同時指兩者。

4. **五、七、八：幾處 recall 把前作縮小，藉此宣稱新增了其實已有的內容。**

   | 位置與原句 | 問題與具體修法 |
   |---|---|
   | 五、〈來源與內容要一起核對〉：「那篇處理的是一個團隊自己的文件」 | Harness 藍圖第二節已處理 Org／Repo／Dir、跨團隊分發與維護。改成：前作處理組織內文件治理；這次新增的是跨來源識別，以及 host 的核准如何綁定完整內容。 |
   | 七、〈資料邊界必須在讀寫與連線時生效〉：「這裡新增的是驗證的對象，不只連線目標，還有輸出的內容與寫入的位置」 | [Harness 藍圖第六節](/Users/kochi.chuang/conductor/workspaces/medium-articles/dodoma/2026-10-agentic-harness-blueprint/article.md:232)已要求內容與目標範圍檢查。真正新增的是下一個 H3 的做法：經實際入口送出越界請求，確認效果被拒絕。把 recall 接到那裡。 |
   | 八、〈把驗證依據交出去，才有可接手的 PR〉：「固定的蒐集器漏了資料，由平台修」 | 組織篇把 domain MCP tools 的 R／A 放在 domain team。蒐集器程式漏取資料、來源根本沒收資料、領域契約缺欄位，責任不同。補這個分流，不能全部丟給平台。 |

5. **三、〈我帶回來的問題：三件事要分開問〉：NTT 案例的證據限制，到了收束句又消失。**

   > 「操作紀錄回答實際做過什麼」

   此案例的 blocked 判定明確依賴操作者下一句話，[第 13 頁也直接註明這點](/Users/kochi.chuang/conductor/workspaces/medium-articles/dodoma/.context/research/aaif-2026-10-23/slides/text/2So56-01-agntcon2026-ntt-docomo-business-kota-tsuyuzaki.txt:298)。第 14 頁接著展示操作者也可能指錯被刪的檔案。

   **修法：**保留「工具狀態不足，還要交叉核對」這個限制。補一句：本文需要的是能辨識操作對象與結果的紀錄；NTT 展示的正是現有紀錄尚不足的地方。不要把人工重建的判定，寫成工具紀錄已直接提供的事實。

6. **八、〈從線索走到修補，先建立有辨識力的重現〉：最值得分析的授權差異被略過。**

   > 「Uber 的做法是，若開關與 crash 的關聯很強，就先把開關關回去」

   逐字稿支持講者這樣描述系統，但沒有交代這一步的核准位置與政策。本文的假設委託則明定 production 由值班人員決定。兩者的差異不能只靠讀者自行發現。

   **修法：**補明：「演講未交代這步的授權機制；本文不因此把相同權限交給調查 agent。」接著分析：緩解可以在因果尚未完全確定時進行，靠的是當下影響、撤回代價與授權政策，不是模型的信心分數。

7. **四至十一：以下轉場仍是在換題，沒有交接前一段的結果。**

   | 位置與原句 | 缺的交接 |
   |---|---|
   | 四、〈請求可以無狀態，任務與授權仍要接得下去〉：「即使資料與工具都在眼前，新加入的同事仍需要知道調查該怎麼做」 | 前面停在身分與長任務，突然換 SOP。可接回前一個 crash 比較：取得版本與曝光資料後，仍需要程序規定怎麼比較、何時不得下結論。 |
   | 六、〈錯誤要能定位，快取要能失效〉：「失敗紀錄處理的是呼叫結果；快取另有一個問題」 | 這是另開子題。補上與重試的直接關係：舊清單仍列有工具，不代表此刻仍有執行權限；否則快取段落移到註記。 |
   | 八、〈把驗證依據交出去，才有可接手的 PR〉：「PR 通過驗證之後，生產環境仍可能出現測試沒涵蓋的要求。下一場就從那裡開始」 | 下一節換成 agent 本身出錯，不是同一份 App PR 上線。明講受測對象換了：上一節驗修補，下一節驗調查者本身。 |
   | 九、〈回復舊版工作指引，仍要確認外部狀態〉：「下一場談的是把判準交給機器打分時」 | PagerDuty 主要分類互動與摩擦，不是接手判定那張旅客訂位是否完成。補明分類結果能提供什麼診斷，不能代替哪一份操作證據。 |
   | 十一：「這三個時刻累積一季之後，還有續用與擴權兩個決定」 | 又新增兩個沒有展開的決定，沖淡三題收束。移到延伸閱讀，正文留下人工接手成本即可。 |

## 次要問題

1. **六、〈錯誤要能定位，快取要能失效〉：16% 的描述過頭。**

   > 「16% 是其他各種自創格式」

   簡報的 Everything else 還包含 endpoint 消失或搬移的 404，以及 2xx 卻沒有 token，不能全稱自創格式。改成「其他非預期回應」，需要時列一個例子。

2. **八、〈固定資料蒐集流程，把判斷留給需要推理的步驟〉：turn 的定義缺來源。**

   > 「一回合包含一次模型回應與它呼叫的工具」

   簡報與逐字稿支持 20 max turns，沒有在留存材料中找到這個精確計數定義。補 harness 的定義來源，或刪除這句，只保留「不能直接換算成工具次數」。

3. **十、〈讓評分器自己也被評分〉：設計目標被寫成必然結果。**

   > 「每一步都比前一步貴，所以越後面處理的資料越少。」

   成本比較高，不會自動讓資料變少；低信心與未知類別很多時，後段流量照樣會膨脹。改成「流程以分流限制昂貴步驟的處理量；實際比例未公布」。

4. **五、〈來源與內容要一起核對〉：digest 又換回「摘要」，增加歧義。**

   > 「摘要和檔案都由同一個 server 提供」

   前後還有 log 摘要，兩種意思會混。此處一路使用「內容指紋」；文字壓縮才叫摘要。

5. **References [6]、[21]：頁碼與時碼可再精確。**

   > 「官方簡報第 10、12–13 頁」

   NTT「改完檔案後驗證始終沒成功」的直接依據在第 11 頁，應補上。Logfire 則應區分 13:29 開始檢視提案，與約 13:47–13:56 的套用過程，避免把整段動作壓在單一時點。

## 建議刪除

1. **篇首系列導覽：刪重複圖說。**

   > 「系列總覽：從行動、交接到記憶，讓下一位接手者知道哪些有依據，哪些仍待查。」

   上一段與圖內已交代相同內容。保留導覽圖與必要圖例，不再用另一句重述。

2. **一、〈一張邀請，和兩週內排好的東京行〉：刪旅帖支線。**

   > 「行程安排用的是先前自己做的旅行工具『旅帖』，趁這次順手補了多趟旅行的支援。」

   後文沒有用到這項經驗，也沒有改變任何判斷。整段可刪。

3. **一：基金會歸屬移到註腳。**

   > 「貼文裡我向 CNCF 道謝，保存的邀請函則署名 Agentic AI Foundation（AAIF）」

   這是來源釐清，正文不必花一整段處理。保留邀請、臨時安排、想知道業界卡在哪裡；這三者才構成出發動機。

4. **四、〈請求可以無狀態，任務與授權仍要接得下去〉：縮短第二篇內容。**

   > 「工作識別只讓結果找得到，進度與結果怎麼保存、worker 更換後怎麼接續，仍由應用程式安排」

   保留這個判斷與第二篇入口即可。stateless、Tasks、worker 接續不必在本篇先展開一次。

5. **五、〈來源與內容要一起核對〉：刪尚未核對卻先作比較的句子。**

   > 「OpenAI 今年 2 月的〈Harness engineering〉描述了類似做法，本文未能取得原文全文核對」

   未取得全文，就不要先斷言「類似」。只列延伸閱讀，或刪除這筆引用。

6. **十、〈先寫職位說明，再談要不要僱用〉：壓縮四字母逐項介紹。**

   > 「如果這個 agent 是一個人，它的貢獻值不值得一份全職薪水」

   這一段在回答值不值得打造 agent，與本篇單次行動的證據問題距離最遠。保留職責邊界與紅線，H.I.R.E. 全框架縮成簡述；五個指標留作診斷表。

7. **十二、〈離開澀谷之後〉：刪第二次技術清點與衣物盤點。**

   > 「走到今天交得出去的是第十一節那三份紀錄」

   > 「行李裡除了購物任務的成果，還有一件……Kubestronaut 外套。」

   澀谷晨跑與照片是旅程收束；外套沒有推動思考，三份紀錄則剛講完。結尾可直接對照午休貼文的「governance 跟 agent logic 分離」，說明現在為何還要分開確認授權、效果與完成。毋須補造經驗；東京鐵塔也不在本篇，不必硬補。

## 建議補充

1. **TL;DR 與三：把主問題固定在一個可判定的時刻。**

   > 「我們還要先確認什麼，才願意讓它多做一步？」

   可收斂為：「當 agent 回報這一步做完，接手者需要哪些證據，才能核准下一步？」每節都必須增加一項會改變這個決定的資訊。第十節若保留，應解釋摩擦訊號何時要求重新查核，不能另起「值不值得聘用」主線。

2. **各場分析：補的是條件改變後的取捨，不要再加一輪演講摘要。**

   | 場次與目前句子 | 還缺的推論或具體驗證 |
   |---|---|
   | 二、〈被限流之後，先確認哪些步驟已經完成〉：「40 秒內 2,000 個 token 的上限」 | 明講時間窗重設後仍可繼續消耗，因此它不是整個任務的總預算。再加一個反例：角色有建 PR 權限，但目標 repo 不在本次委託內，仍應拒絕。 |
   | 四、〈讓回饋能分辨真正的改善〉：「每千次 session 發生幾次 crash」 | 誰負責確認曝光與 crash 的量測口徑？若資料源漏記 session，標準化後的比例仍可能誤導。MCP 解決取得資料，沒有驗證量尺。 |
   | 五、〈驗證更新時，把授權要求留在比較裡〉：「正常與保留案例不退步」 | 沿用規格修改卡時，補回固定模型、工具、預算、停止條件、重複執行與人工投入。否則只是沿用卡片欄名，沒有沿用前作的比較承諾。 |
   | 六、〈先處理憑證取得與更新的競爭〉：「鎖到期時原本的 worker 若還在換發」 | 問題提出後沒有落地。補一小張供應商契約表：明確拒絕、換發回覆遺失、鎖到期，各自能查什麼、何時必須重新授權。 |
   | 七、〈同時驗證工作能完成、越界會被拒絕〉：「全部拒絕也能得到零次越界」 | 補一個同時滿足兩邊的驗收例：必要套件能取得、未允許端點收不到資料。讓讀者知道要觀察接收端與檔案效果，而不是只看拒絕訊息。 |
   | 八、〈固定資料蒐集流程，把判斷留給需要推理的步驟〉：「省掉每次規劃的錢，是用維護流程的錢換來的」 | 固定流程何時應停止？例如事故類別不在既有資料契約內，就不能繼續把缺資料送進 RCA。補一個轉人工的具體條件。 |
   | 九、〈先分清要求被放寬，還是工具參數用錯〉：「而且不建立訂位」 | 把觀察方式寫出來：非法 offer 被拒絕後，訂位資料裡沒有新增紀錄。這才把「工具回報失敗」接到「外部效果未發生」。 |
   | 十、〈讓評分器自己也被評分〉：「低於門檻的交給較強的模型再看一次」 | 未知類別暴增時，強模型與人工佇列會成為瓶頸。需要分列升級比例、人工處理量與等待時間；低信心分流也抓不到所有高信心錯判。 |

3. **十一：把會議表實填一個反例，別再只走敘述流程。**

   > 「全部是設計範例，欄位與負責角色要換成自己團隊的」

   週一至少應能拿一筆歷史 crash，填完操作對象、核准人、要求版本、遠端查證入口與接手角色。再用三個設計案例驗表：未授權的關閉請求；寫入成功但回覆遺失；操作成功但事故未改善。三者應得到不同的「允許／發生／完成」答案。這比再多一份 checklist 更能暴露契約缺口。

4. **九、〈把生產錯誤變成有明確預期的測試〉：讓 recall 增加新責任。**

   > 「是同一件事放進了產品分析」

   獨立判準、人工校準與禁止自我驗收相關，卻不是同一件事。這次新增的問題是：分類器誤判會直接改變五個指標，進而影響產品決策。把分類器版本、人工標記分歧與漏判／誤判列入指標報告，才是相較前作的新一步。

5. **十二：讓作者經驗推動判斷，而非只包住技術正文。**

   > 「當天貼文的感想是一句話：『governance 跟 agent logic 分離，AI 才進得了 production』」

   午休 demo 是全文真正造成思考轉折的經驗，應讓它一路留在場上：當日介面顯示 Blocked；重查後才分清限流對象、模擬寫入與版本差異。把這條已有證據的認知修正放到結尾，比再列一次原則更有作者自己的位置。

## 術語仍難懂的清單

| 位置與原句 | 仍缺的例子或區分 |
|---|---|
| 三、〈我帶回來的問題〉：「實際成功的 session 卻只有五次」；四：「每千次 session」；六：「失效的 session」 | 同一個字先後指 agent 工作階段、App 使用工作階段與 MCP session。各自加限定詞，不能讓讀者沿用同一個計算單位。 |
| 二：「角色之間交換工作用的是 Agent-to-Agent（A2A）協定」 | 小組比喻仍偏抽象。先寫兩筆不同訊息：「請工程師代理調查 issue 123」與「讀取 issue 123」，再命名 A2A 與 MCP。 |
| 六：「gateway 管進來的請求能不能通過，proxy 替自家產品對外連接各家服務」 | 這不是兩個詞固定的進出分工；Kong 也轉送對外模型請求。改成「這兩個展示各自著重的職責」，避免教出錯誤分類。 |
| 九、導讀：「trace 保留了已納管的步驟」及「沒有 span 的步驟」 | 先用一次調查示範：整次調查是一條 trace，其中一次 crash 查詢是一個 span；另提醒 stack trace 是程式錯誤的呼叫堆疊，並非同一種 trace。 |
| 九、〈把生產錯誤變成有明確預期的測試〉：「optimizer」「LLM-as-judge」 | 先讓讀者看到分工：一個模型提議改指令，另一個模型依保存的旅客要求評分，人決定是否採用。角色名稱放在分工之後。 |
| 九、〈回復舊版工作指引，仍要確認外部狀態〉：「managed variables」「production 標籤」「canary 標籤」 | 一段塞了遠端設定、不可變版本、標籤、分流、任務固定版本與預設值。拆成兩段；先用「production 指向 v3，少量試行指向 v4」解釋，再處理取值失敗。 |
| 九、〈把生產錯誤變成有明確預期的測試〉：「frozen holdout」 | 與 golden tasks、gold set 容易混。直接區分：代表性工作拿來比較、人工標記資料拿來校準、保留案例不交給 optimizer 調整。 |

token、skill、digest、sandbox 已有情境例子，不列為缺漏。commit point、optimistic locking、compaction、RRF、oracle 未出現在本篇，不應把其他兩篇的術語問題算進來。

查核範圍上，主要統計與留存來源相符；未找到可證明捏造的主要數字。Mazin 引句仍只能對照既有聽寫，Kong 當日執行也不能由晚間保存版程式獨立重建；這兩項限制應繼續保留。

<!-- tokens: in 4172226 out 32306 -->
