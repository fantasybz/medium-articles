# Codex review — 2026-11-aaif-after-tokyo/article.md

> model: gpt-6.1-sol, reasoning: xhigh, 2026-10-25 22:47. 原話照錄，未經摘要。審的是 2026-10-25 改寫後的版本。

我會先讀指定的風格文件，再逐節核對來源與舊文 recall；全程只讀取 repository 內的檔案，不做修改。
<!-- codex ran: /bin/zsh -lc 'cat STYLE.md' -->
<!-- codex ran: /bin/zsh -lc 'cat research/2026-10/style_brief.md' -->
<!-- codex ran: /bin/zsh -lc "rg --files --hidden -g '"'!agents/**'"' -g '"'!.claude/**'"' -g '"'!.git/**'"' .context/research/aaif-2026-10-23 .context/research/aaif-2026-10-25 -->
<!-- codex ran: /bin/zsh -lc "rg --files --hidden .context/research/aaif-2026-10-23 .context/research/aaif-2026-10-25 -g '*.txt' -g '*.json' -g '*.md' -g '*.yaml' -g '*.py' -g  -->
<!-- codex ran: /bin/zsh -lc 'nl -ba 2026-11-aaif-after-tokyo/article.md' -->
<!-- codex ran: /bin/zsh -lc "rg -n '"'^##|''^###|AGENTS|read、write|dangerous|legibility|G2|Red Line|frozen|holdout|三個陷阱|judge|constraint tests|red-then-green|證據|三層'"' 2026-10- -->
<!-- codex ran: /bin/zsh -lc "wc -l -c .context/research/aaif-2026-10-23/{keynote,skills,proxy,local,uber,logfire}-transcript.txt; rg --files --hidden .context/research/aaif-20 -->
<!-- codex ran: /bin/zsh -lc 'cat .context/research/aaif-2026-10-23/keynote-transcript.txt .context/research/aaif-2026-10-23/skills-transcript.txt' -->
目前最明顯的問題是三題框架到了第十節變成「agent 值不值得留下」，結論卻把摩擦指標當成價值證明。我正在核對 H.I.R.E. 的定義，以及 Uber、proxy 的數字，區分來源原話與本文加上的推論。
<!-- codex ran: /bin/zsh -lc 'cat .context/research/aaif-2026-10-23/slides/text/2So56-*.txt .context/research/aaif-2026-10-23/facebook-post-provenance.json' -->
<!-- codex ran: /bin/zsh -lc 'cat .context/research/aaif-2026-10-23/proxy-transcript.txt' -->
<!-- codex ran: /bin/zsh -lc 'cat .context/research/aaif-2026-10-23/slides/text/2QlEA-*.txt .context/research/aaif-2026-10-25/hire/ai-agent-metrics.md' -->
<!-- codex ran: /bin/zsh -lc 'cat .context/research/aaif-2026-10-23/slides/text/2QlEA-*.txt .context/research/aaif-2026-10-25/hire/ai-agent-metrics.md' -->
<!-- codex ran: /bin/zsh -lc 'cat .context/research/aaif-2026-10-23/uber-transcript.txt' -->
<!-- codex ran: /bin/zsh -lc 'cat .context/research/aaif-2026-10-23/logfire-transcript.txt' -->
<!-- codex ran: /bin/zsh -lc "rg -n -C 5 'guard|secret|sudo|curl|OpenCode|open code|LiteLLM|18:|28:|local|shell' .context/research/aaif-2026-10-23/local-transcript.txt" -->
<!-- codex ran: /bin/zsh -lc "rg -n '"'^##|''^###|AGENTS.md|read、write|dangerous|legibility|五層'"' 2026-10-agentic-harness-blueprint/article.md; rg -n '"'^##|''^###|三個陷阱|共享|校準|j -->
<!-- codex ran: /bin/zsh -lc "sed -n '57,156p' 2026-10-agentic-harness-blueprint/article.md; sed -n '178,214p' 2026-10-agentic-harness-blueprint/article.md; sed -n '32,105p' 20 -->
<!-- codex ran: /bin/zsh -lc "rg -n '"'^#|同一|驗收|證據|成本|責任|越界|重試|規格|holdout'"' 2026-11-same-spec-*/article.md 2026-09-agentic-engineering-platform/article.md 2026-09-agentic-org- -->
<!-- codex ran: /bin/zsh -lc "rg -n '"'^##|''^###|三類|第三類|第二類|升格|red-then-green|mutation|oracle'"' 2026-10-green-overview/article.md 2026-10-green-testing/article.md 2026-10-gre -->
<!-- codex ran: /bin/zsh -lc "rg --files --hidden .context/research/aaif-2026-10-25 research/2026-10/aaif-agntcon .context/research/aaif-2026-10-23 -g '"'!**/agents/**'"' -g '" -->
<!-- codex ran: /bin/zsh -lc "rg -n '三類|第三類|第二類|升格|## 五|red-then-green' 2026-10-green-overview/article.md 2026-10-green-testing/article.md; sed -n '384,405p' 2026-10-green-reli -->
<!-- codex ran: /bin/zsh -lc "rg -n -C 4 'x-analysis-id|github-writers|2000|40|503|x-llm-type|CREATED_PRS|SENT_NOTIFICATIONS|429|create_pull_request|rate-limited' .context/rese -->
<!-- codex ran: /bin/zsh -lc "python3 -B -c 'import json; from pathlib import Path
base=Path(\".context/research/aaif-2026-10-23/sources\")
for name in [\"mcp-skills-spec\",\"m -->
<!-- codex ran: /bin/zsh -lc "sed -n '545,650p' .context/research/aaif-2026-10-23/kong-demo-source/kong/api-gateway/base-config.yaml; sed -n '110,175p' .context/research/aaif-2 -->
已找到兩個會改變讀者判斷的落差：NTT 簡報說，判定刪除被擋還依賴操作者下一句話，本文卻寫成工具紀錄本身已證實；H.I.R.E. 文件的 PPR 只算已解決對話、RLR 則按 interaction 計算，正文都省略了分母。接下來核對規格版本、舊文章節與圖說時間點。
<!-- codex ran: /bin/zsh -lc "python3 -B -c 'import json,re; from pathlib import Path
base=Path(\".context/research/aaif-2026-10-23/sources\")
queries={\"mcp-skills-spec\":r\"m -->
<!-- codex ran: /bin/zsh -lc "python3 -B -c 'import json,re; from pathlib import Path
base=Path(\".context/research/aaif-2026-10-23/sources\")
for name,patt in [(\"mcp-architec -->
<!-- codex ran: /bin/zsh -lc "sed -n '647,682p' .context/research/aaif-2026-10-23/kong-demo-source/kong/api-gateway/base-config.yaml; sed -n '188,245p' .context/research/aaif-2 -->
<!-- codex ran: /bin/zsh -lc "rg --files --hidden .context/research/aaif-2026-10-23/video-review -g '*.png' -g '"'!**/agents/**'"' | head -100; python3 -B -c 'import json; from -->
<!-- codex ran: /bin/zsh -lc "sed -n '34,66p' 2026-11-same-spec-contract/article.md; sed -n '518,555p' 2026-11-same-spec-contract/article.md; sed -n '281,337p' 2026-11-same-spe -->
<!-- codex ran: /bin/zsh -lc "sed -n '48,84p' 2026-10-green-overview/article.md; sed -n '55,70p' 2026-09-agentic-org-design/article.md; sed -n '107,117p' 2026-11-agentic-eval-e -->
<!-- codex ran: /bin/zsh -lc "cat .context/research/aaif-2026-10-25/hire/README.md; rg -n 'gold|calibr|human|score|sample|evaluat' .context/research/aaif-2026-10-25/hire/README -->
<!-- codex ran: /bin/zsh -lc "rg -l 'f4dlvY4Qvew|models get a lot|Mazin Gilbert' .context/research/aaif-2026-10-23/sources research/2026-10/aaif-agntcon .context/research/aaif- -->
<!-- codex ran: /bin/zsh -lc "rg -n -C 3 'risk|rating|revers|financial|failure|threshold|human|agent is|Agents are|three' .context/research/aaif-2026-10-25/openai-guide/guide.t -->
<!-- codex ran: /bin/zsh -lc "python3 -B -c 'import json; from pathlib import Path
p=Path(\".context/research/aaif-2026-10-25/pagerduty/meta.json\"); d=json.loads(p.read_text() -->
<!-- codex ran: /bin/zsh -lc "sed -n '1,150p' .context/research/aaif-2026-10-23/slides/text/2QlLo-*.txt; sed -n '1,135p' .context/research/aaif-2026-10-23/slides/text/2QlDI-*.t -->
Uber 的 slide 11 顯示，validation 與 create diff 也使用 LLM，因此「模型只處理 RCA、調查分支與修補」要修正。舊文 recall 的主要落差則是 G2：原文把它用於擴張授權，本篇拿來承接「是否續用」，少了成效與成本的判準；《同一份規格，跑十次》已有的修改卡與人工接手成本，也還沒接進來。
<!-- codex ran: /bin/zsh -lc "python3 -B -c 'from pathlib import Path; import re,html
s=html.unescape(re.sub(\"<["'^>]+>"," ",Path(".context/research/aaif-2026-10-25/openai-har -->
<!-- codex ran: /bin/zsh -lc "python3 -B -c 'from pathlib import Path; import re
p=Path(\"2026-11-aaif-after-tokyo/article.md\"); t=p.read_text()
for i,l in enumerate(t.splitli -->
<!-- codex ran: /bin/zsh -lc "python3 -B -c 'from pathlib import Path
p=Path(\".context/research/aaif-2026-10-25/openai-harness.html\"); print(p.stat().st_size); print(p.read_t -->
<!-- codex ran: /bin/zsh -lc "python3 -B -c 'import json; from pathlib import Path
base=Path(\".context/research/aaif-2026-10-23/sources\")
for name,terms in [(\"mcp-caching\", -->
<!-- codex ran: /bin/zsh -lc "cat 2026-10-green-payment/publish/PUBLISHED.md 2026-11-aaif-after-tokyo/publish/PUBLISHED.md 2026-11-aaif-agent-handoffs/publish/PUBLISHED.md 2026 -->
核對已收斂到幾個必修點：H.I.R.E. 的分母與價值結論、NTT 的證據來源、Uber 的 LLM 節點，以及 managed variables 的標籤與分流。SkillsBench、proxy、Uber 的主要數字與指定簡報頁碼能在本機來源找到；Mazin 原句與 OpenAI「五個月／百萬行」缺少本次可核實的原始內容，會列為待核實，不判成造假。
目前不宜定稿。問題集中在：三題框架中途換了判斷對象、幾處來源被說得比實際證據更強，以及結尾缺少能直接採用的決策紀錄。

已依序讀取兩份風格文件，核對 repository 內的字幕、簡報、程式碼、文件快照、照片及舊文。以下針對你貼出的版本；未修改檔案，未連外，也未逐格重聽影片。

## 致命問題

1. **三、〈我帶回來的問題：三件事要分開問〉；十、〈怎麼證明這個 agent 值得留下來？〉；十一**

   > 「每一場演講各自補上一題的證據」
   >
   > 「一次次任務之外，這個 agent 整體有沒有價值。」

   前者問一次行動能否繼續，後者問一項投資是否值得。正文把「完成任務」「使用者少修改」「值得續用」「可以擴張授權」接成同一條推論，沒有交代它們需要不同證據。

   **修法：**固定主問句為：「Agent 要繼續工作時，誰依哪份授權、操作結果與驗收依據，決定執行、查證或交回人？」第十節只提供長期觀察訊號；續用與擴權另外判斷，不再叫「完成了嗎的最後一層」。

2. **十、〈讓評分器自己也被評分〉**

   > 「而且算這些數字的工具自己也被檢查過。」
   >
   > 「證明一個 agent 值得留下來，靠的是從生產對話算出的摩擦指標，而且算分的評分器自己也經過校準。」

   這裡同時越過兩條證據界線。簡報第 25 頁描述評分與校準的安排，公開 README 有 synthetic gold set 與評估入口；這不等於本文已取得 SRE agent 的校準結果。摩擦指標也不能單獨證明價值：使用者可能沒有發現錯誤，或乾脆沒有使用它。

   **修法：**改成「框架要求評分器接受人工標記資料的校準；本文未取得該 SRE 案例的校準結果」。收束句改為：摩擦指標協助找問題，續用仍須合併任務正確性、事故影響、人工投入與總成本。來源見 [H.I.R.E. README](/Users/kochi.chuang/conductor/workspaces/medium-articles/dodoma/.context/research/aaif-2026-10-25/hire/README.md)。

3. **三、NTT DOCOMO 段落**

   > 「工具紀錄卻寫著那次刪除被擋下，檔案從未被移除」

   你省掉了直接影響本文主張的限制。簡報第 13 頁明寫：判定被阻擋，依賴操作者下一句話，不能只由 tool span 的 status code 建立。本文卻把它寫成工具紀錄本身足以證實。

   **修法：**寫成「研究者交叉核對工具紀錄與操作者後續說明，判定刪除沒有執行；通用錯誤狀態本身不足以區分拒絕與執行失敗」。這才接得上你的三題。見 [NTT 簡報文字，第 12–13 頁](/Users/kochi.chuang/conductor/workspaces/medium-articles/dodoma/.context/research/aaif-2026-10-23/slides/text/2So56-01-agntcon2026-ntt-docomo-business-kota-tsuyuzaki.txt)。

4. **八、〈固定資料蒐集流程，把判斷留給需要推理的步驟〉**

   > 「模型只處理根因分析（RCA）、調查分支與修補。」

   與 slide 11 不符。`bazel_test`、`create_diff` 也列有 Claude Sonnet 與回合上限。這個「只」把混合架構簡化錯了。

   **修法：**改成「資料蒐集器由固定程式執行；後續 RCA、修補、驗證與建立 diff 等節點仍使用模型，但整體順序由流程控制」。區分「固定流程」與「節點內不用 LLM」。見 [slide 11 畫面](/Users/kochi.chuang/conductor/workspaces/medium-articles/dodoma/2026-11-aaif-after-tokyo/figures/11-uber-investigation.png)。

5. **TL;DR；三、證據分類段落**

   > 「讓這三個問題各有一份 agent 自己改不動的證據。」
   >
   > 「只有最後一類能當驗收依據。」

   「改不動」只處理證據保護，沒有處理判準是否正確、觀察範圍是否足夠。團隊維護的錯誤測試，仍然可能穩定放行錯誤。你在《同一份規格，跑十次》契約篇第二節已經把這件事講得更完整。

   **修法：**TL;DR 補成「判準經確認、觀察範圍清楚，而且 agent 不能自行放寬或核准修改的證據」。Recall 保留舊文的限定：「能作為閘門採用的獨立驗收證據」，不要擴寫成所有驗收的充分條件。

## 重要問題

1. **三、閱讀地圖；五、導讀；七、導讀：三題被硬配成場次分類**

   > 「允許嗎？……Skills 的程序核准與更新」
   >
   > 「發生了嗎？……Red Hat 私有部署的資料路徑」

   核准一份程序，不等於核准它提出的生產操作。私有部署的執行限制，主要也在回答允許範圍；只有實際讀寫與連線紀錄，才回答發生什麼。

   **修法：**閱讀地圖改成「這場提供哪種證據／仍缺哪種證據」。允許一場跨兩題，不要為了整齊扭曲材料。

2. **二、〈被限流之後，先確認哪些步驟已經完成〉及〈把「允許、發生、完成」拆開看〉**

   > 「先讀取 GitHub 上的問題單」
   >
   > 「工程師代理已經完成工具操作」

   保存版連問題單也是 mock 資料；正文只在後面揭露 PR 與通知是模擬紀錄。另外，操作手冊的路徑、午休影片的觀察與當晚保存版程式，尚未建立同版本關係。

   **修法：**情境第一次出現就說「模擬 GitHub issue、PR 與通知」。後續明寫「保存版手冊描述的路徑」，不要滑回當日實測口吻。文末註記不能獨自承擔這個區分。

3. **二、收束句**

   > 「Gateway 能把『允許』管好」

   展示證明的是群組 ACL 與用量限制可以集中執行，沒有證明每次操作都核對了委託人、目標、當次核准與有效期間。這比第三節對「允許」的定義窄。

   **修法：**改成「Gateway 能集中執行已配置的政策；政策是否涵蓋這次任務與操作對象，仍須另外確認」。

4. **六、〈錯誤要能定位，快取要能失效〉**

   > 「約 92%……回傳相同的工具清單，所以清單可以按 server 快取」

   觀察到清單相同，不是跨使用者重用的授權依據。應先看 server 宣告的 cache scope 與授權脈絡，不能由 92% 的經驗比例決定。

   **修法：**改成「這個觀察指出可節省的重複請求；實際跨使用者重用，仍須符合 server 的 public/private 宣告與快取契約」。後面的限定移到同一段。

5. **九、〈回復舊版工作指引，仍要確認外部狀態〉**

   > 「同一個『production』標籤下先讓部分流量試用新程序」

   官方文件的模型是：一個 label 指向一個不可變版本，再由 rollout 在不同 labels 間分流。這句把 label 與分流設定混在一起。

   **修法：**寫成「production 指向舊版、canary 指向新版，先將部分流量分給 canary；確認後再移動 production」。見 [Managed Variables 文件快照](/Users/kochi.chuang/conductor/workspaces/medium-articles/dodoma/.context/research/aaif-2026-10-23/sources/logfire-vars.json)。

6. **五、〈來源與內容要一起核對〉**

   > 「規格容許提供完整的檔案清單（manifest）」

   現行快照要求 `resources` 必須是完整清單或 `"dynamic"`；不是任選一份完整清單即可。Dynamic 無法提供相同的內容綁定保證，這個例外只寫在 References，正文判斷卻一路假設有穩定指紋。

   **修法：**明寫兩條路：完整清單逐檔核對；dynamic 不能沿用對固定內容的核准，host 可拒絕載入。見 [Skills specification 快照](/Users/kochi.chuang/conductor/workspaces/medium-articles/dodoma/.context/research/aaif-2026-10-23/sources/mcp-skills-spec.json)。

7. **十、〈五個指標，量的是摩擦而不是點擊〉：缺少分母，讀者無法照算**

   | 原句 | 必須補正 |
   |---|---|
   | 「使用者得刪掉或改寫多少……」 | 文件文字談重做量，實際公式卻是「出現修正的 conversation／全部 conversations」。指出兩者差異，不能當成同一量尺。 |
   | 「平均要來回幾次」 | PPR 只平均已解決的 conversations；有用的澄清問題目前也計入回合。 |
   | 「放棄對話、自己回傳統介面做掉的比例」 | 對話標記只是 proxy；確認是否改走 UI，還須產品 telemetry 與關聯窗口。 |
   | 「一次就答對……的比例」 | IRR 分母是可解決的 conversations，排除沒有 resolving action 定義的資訊型問題。 |
   | 「被……擋下的比例」 | RLR 按 interaction 計算，且文件還涵蓋敏感資訊洩漏、未授權承諾等，不只 gateway 攔截。 |

   **修法：**直接補「計算單位／分子／分母／盲點」四欄，刪掉部分字母框架複述騰出位置。依 [固定版本指標文件](/Users/kochi.chuang/conductor/workspaces/medium-articles/dodoma/.context/research/aaif-2026-10-25/hire/ai-agent-metrics.md)整理。

8. **十、〈先寫職位說明，再談要不要僱用〉**

   > 「從不碰 production」
   >
   > 「停在 MCP 這一層的權限檢查前等人核准」

   同段又說唯讀呼叫可以執行。「不碰」會被理解成不存取；「檢查前等核准」也把控制順序說模糊了。

   **修法：**改成「對 production 僅有讀取權限，不自行執行破壞性變更；MCP 邊界執行權限與封鎖規則，關鍵動作需人工核准」。不要從示意圖自行補出完整核准流程。

9. **五、〈來源與內容要一起核對〉；九、〈把生產錯誤變成有明確預期的測試〉；十一：recall 有失真或只有重述**

   | 本文原句 | 舊文核對與具體修法 |
   |---|---|
   | 「AGENTS.md 分成三層維護，正是因為……卻沒有版本與驗證」 | 〈Harness 藍圖〉第二節主要從維護分工展開，且已有 CI 與 golden tasks。改說本篇新增的是「跨 server 分發後，核准如何綁定到完整內容」。 |
   | 「log 能否依請求查詢……生產版本」 | 舊文第五節已要求 request id、版本與環境。新增 proxy 的上下游結果、credential state、fault domain 如何改變處置，別只重申要結構化 log。 |
   | 「就是同一個陷阱換了名字」 | 舊文是 judge 與受測模型共享盲點；optimizer 同時改目標與評自己，是判準來源與角色混用。改成「兩者都需要獨立的判準來源」，不要說完全相同。 |
   | 「G2 閘門提供了門檻的位置」 | 可靠度篇第五節的 G2 是擴張授權，且要求七項條件；RLR 尚未納入通過條件。不能借來直接決定續用或下線。 |
   | 「一次事故……不能獨自決定所有未來任務」 | 《同一份規格，跑十次》規格篇第八節已做到修改卡，變異篇第十、十一節更有人工成本與未定出口。本篇應直接沿用那張卡，新增遠端分發與執行期版本問題。 |

10. **三、四個條件段落**

    > 「因為 agent 工作的環境有四個繞不開的條件。」

    四條大多也是一般分散式自動化的條件。沒有回答「為什麼 agent 讓這些老問題更難」。

    **修法：**補一段作者推論：模型會依文字回應自行選下一步；若把逾時誤讀為沒執行，錯誤理解便可能變成下一次寫入。既有系統問題因此進入動態決策迴圈。不要暗示這些問題由 agent 才產生。

## 次要問題

1. **五、〈驗證更新時，把授權要求留在比較裡〉**

   > 「在七組 agent 與模型配置……比較……模型自己產生的 skill」

   七組是主要實驗配置；self-generated 條件只涵蓋 Claude Code 與 Codex 的五組配置。

   **修法：**補上這個子集，避免讀者以為三條件完全對稱。16.2 個百分點、7,308 條有效軌跡、84 題中 16 題退步，可在保存來源找到。

2. **八、〈從線索走到修補，先建立有辨識力的重現〉**

   > 「那不是程式能模擬的條件」

   字幕確實有講者類似說法，但不能升格成弱網路無法以程式模擬的通則。

   **修法：**寫成「她以這個案例說明，單元層級的重現不足，因此使用模擬器重建相關環境條件」。

3. **十、案例段落**

   > 「多位工程師花了三小時才處理完」

   簡報寫的是 **3h of downtime**，不是三小時人工投入，也沒有提供同條件前後比較。

   **修法：**寫成「簡報描述一次造成三小時 downtime、涉及多位工程師的事故」。後面的改善保留為團隊敘述。

4. **三、Mazin 段落；五、OpenAI 段落**

   > 「模型得到最多關注，但 harness 更重要。」
   >
   > 「五個月、約一百萬行程式、沒有一行手寫」

   本次沒有找到可獨立核對 Mazin 原句的原始字幕；保存的 `openai-harness.html` 也不是文章正文。

   **修法：**列為待補原始來源，不能標成此次已核實，也不能據此判成捏造。這組 OpenAI 規模數字對本節推論沒有必要，可直接刪。

5. **十二、〈離開澀谷之後〉**

   > 「Kong……Skills……proxy……Uber、Logfire 與 PagerDuty……」

   又重念一次閱讀地圖，沒有增加決定。

   **修法：**換成 crash 案例目前能交出去的三份紀錄及一項待查結果，讓結語真的完成一次交接。

數字與定位的其餘主要核對結果：Kong 的 2,000 token／40 秒配置、proxy 的 74%／92%、Uber 的約 9,000 次／50%／剩餘一半中的約四成／5%→48%／3,000 plugins，以及指定 PagerDuty 頁碼，均能找到對應材料。這只確認引用來源，不代表那些數字已獲獨立驗證。

## 建議刪除

以下段落目前沒有推進主問句，或與相鄰段落重複。

| 位置與原句 | 刪除或改寫方式 |
|---|---|
| 篇首系列總覽：「下圖把三篇各自追問的問題……放在一起」 | 總覽圖與第三節閱讀地圖保留一個完整版本即可；前者縮成系列導覽。 |
| 一：「後面談到的每一場演講，說的其實也是同一件事，只是把『我』換成了 agent。」 | 刪。工具解決旅行痛點，推不出授權、外部狀態與驗收三題。旅帖故事保留短段即可。 |
| 二：「同一天，Kong 的 Juhi Singh……〈The Production Gap〉……」 | 本文沒有分析該場材料，移至 References；不要用相近議題替自己的 demo 增添場次背書。 |
| 四、〈讓回饋能分辨真正的改善〉：「稱為 augmented LLM」 | 刪名稱與旁支。它不改變本節任何判斷。 |
| 四、〈請求可以無狀態，任務與授權仍要接得下去〉：「他後面談到……也可以從同一條調查路徑理解」 | 目前只是宣布相關。壓成「worker 更換後，回饋還能否對回原操作」一段，傳輸細節移第二篇。 |
| 五、〈來源與內容要一起核對〉：「五個月、約一百萬行……」 | 刪規模故事，直接比較本地文件與遠端 skill 的核准差異。 |
| 五、末段：「第三篇會回到另一個角度……螃蟹助理」 | 刪。尚未完成本節採用決定，就轉去預告另一篇。 |
| 八、〈把驗證依據交出去，才有可接手的 PR〉：「這套架構用 PEX 打包……」 | 若不補「接手者如何取得同版環境」，移到前面架構段；目前與 H3 的驗證依據脫節。 |
| 十一：「這也讓開源貢獻有了實際起點」 | 從團隊決策跳到社群參與。移至十二，接回受邀與分享材料的動機。 |
| 十二：「行李裡有會議 T-shirt、購物任務的成果……」 | 與第一節購物任務重複，縮短物品清單；澀谷晨跑保留作旅程收束，不必硬比喻 agent。 |

仍需補實質交接的轉場：

- **四，回饋→stateless：**先問「結果晚回來、worker 已換，這份回饋還找得到原任務嗎？」
- **五，授權更新→SkillsBench：**補明「研究量到效益差異，沒有替授權變更驗證背書」。
- **六→七：**現在只靠「仍是發生了嗎，只是換成資料方向」。應承接：「proxy 紀錄涵蓋哪條路？shell 與其他工具是否也在觀察範圍？」
- **八→九：**先留下「PR 通過驗證後，生產仍可能出現未涵蓋的要求」，再進 Logfire。
- **九→十：**先區分「修好一種失敗」與「整體服務是否值得投入」，不要只說「下一層」。
- **十一，三個時刻→第四個決定：**直接改標題與結構，或把第四個決定移出本篇。

邀請與午休實作能解釋問題怎麼形成；旅帖的強行類比與反覆物品清單只是裝飾。本篇沒有東京鐵塔段落，不需要為了溫度補入其他篇的經驗。

## 建議補充

1. **各場缺少的第一性原理推論**

   下列都應標為作者延伸分析，不冒充講者已驗證的結果。

   | 場次與定位句 | 應補的約束、機制與代價 |
   |---|---|
   | 二、〈故障切換只回答「誰來答」〉：「仍要拿原本的任務要求檢查結果」 | 加一個會改變決策的條件：備援不支援必要工具或輸出要求時，應停止哪個階段？可用性恢復不能自動換取執行資格。 |
   | 四、〈讓回饋能分辨真正的改善〉：「追查……使用量、裝置和觀察期間」 | 指定比較單位，例如同版本、同觸發條件的 crash／session；再說明分群仍可能有偏差，何時只能保留假設。 |
   | 五、〈來源與內容要一起核對〉：「指紋相同只證明內容相同」 | 補「相同腳本呼叫不同版本工具，行為仍可能不同」。內容核對保護哪一層，工具與執行環境版本由誰保存？ |
   | 六、〈先處理憑證取得與更新的競爭〉：「同一時間只有取得鎖的一方更新」 | 補鎖到期、持鎖 worker 停住時的處置。維持單一更新者要付出等待與可用性成本，不能只有正常競爭路徑。 |
   | 七、〈資料邊界必須在讀寫與連線時生效〉：「封鎖 sudo 或對外 curl」 | 說清楚命令封鎖與效果限制不同：同一個連線可由其他程式發出。驗證須涵蓋實際檔案工具、shell、MCP 等入口，並記錄未測通道。 |
   | 八、〈固定資料蒐集流程，把判斷留給需要推理的步驟〉：「能寫死的步驟寫死」 | 固定流程依賴穩定資料契約。新事故需要未配置資料源時，誰擴充流程、何時轉人工？省掉規劃的代價是流程維護。 |
   | 九、導讀：「所以要先上線」 | 補作者採用這個主張的範圍：唯讀、草稿或受限流量如何開始；哪些外部效果仍須先驗證。生產學習有價值，不代表任何失敗成本都可接受。 |
   | 十、〈讓評分器自己也被評分〉：「低於門檻的交給較強的模型」 | 高信心錯誤不會進升級路徑。補高信心樣本的人工抽查、各類別誤判，以及門檻改動如何影響人工佇列與成本。 |

2. **十一：把三個時刻改成一張能帶進週一會議的表**

   > 「就明確核准這個對象與這次動作。」

   「明確」仍不足以交付。至少示範下表，全部標為設計範例：

   | 決定 | 最低紀錄 | 證據不足時 | 負責角色 |
   |---|---|---|---|
   | 暫緩 rollout | 委託人、操作對象、核准範圍與時間、操作識別、遠端結果或版本 | 保留結果未知；無法查證時交人工核對，停止盲目重送寫入 | 值班負責人 |
   | 接受修補 | 需求版本、原版失敗原因、修正版結果、受保護測試版本、未涵蓋條件 | 補重現或需求判斷，不以 agent 自述結案 | Domain reviewer／QA |
   | 更新 skill | 新舊內容、完整清單、適用任務、正反案例、回歸結果、撤回條件 | 維持舊版或限縮試行，結論可為未定 | 程序維護者／平台 |

   再沿一筆「操作逾時但遠端已變更」填完，讓三欄證據真的對應同一個操作。

3. **十一：把「續用」與「擴權」拆成兩個決定**

   > 「僱用與否依據一段時間的摩擦指標。」

   補回〈Agentic Engineering〉總論第十節的人工投入、完成率與交付後缺陷，以及營運篇第三節的成本範圍。續用至少需要相近任務的比較基準；擴權則另看可靠度篇 G2，不可互相代替。

4. **五、九、十一：真正接回《同一份規格，跑十次》**

   > 「一次事故提供修改的理由，不能獨自決定所有未來任務都要照新程序執行。」

   不要再講一次原則。直接用規格篇第八節的修改卡，填上這次 skill 更新的預期作用、保持不變的要求、反例、人工負擔與撤回條件。新增的問題是遠端內容與執行版本如何被保存，這才是 recall 的增量。

## 術語仍難懂的清單

| 位置與原詞 | 具體修法 |
|---|---|
| TL;DR：「MCP keynote、Skills、Anthropic 的 proxy」 | 刪場次名單。摘要先講三個問題，名稱留到情境建立後。 |
| 二：「governance 跟 agent logic 分離」 | 引文後立刻說：代理決定調查步驟；外層決定哪些請求能通過。 |
| 二：「路由」「模型池」 | 用「這類請求送哪裡／有哪些可接手模型」先建立兩者差別。 |
| 三：「迴圈、工具路由、context、記憶、sandbox……」 | 刪術語串。先說同一個 crash 任務需要資料、工具、可執行環境與回饋，再逐一命名。 |
| 三：「context」 | 首次出現就用「這一輪模型實際看得到的資料與指令」說明，不要等到第五節。 |
| 三、七：「sandbox」 | 先舉工作目錄可寫、目錄外假秘密不可讀、指定端點才可連的例子，再命名。 |
| 四：「server」「host」 | 對回案例：提供 crash 查詢的一端；替工程師管理模型與工具連線的應用程式。 |
| 四：「Tasks extension」 | 先說「先拿案件編號，稍後查進度與領結果」，再指出不包含哪些保存與重試責任。 |
| 五：「extension」「SEP-2640」「Final」 | 補一句：這是可選擴充的正式規格狀態，與產品已支援是兩件事。 |
| 五：「URI」 | 不只譯成資源位址；用「同一台 server 上這份程序的位址」對回身分配對。 |
| 五：「digest」 | 「摘要」容易與文字摘要混淆，統一叫內容指紋，說明拿它比較哪兩份內容。 |
| 五：「manifest」 | 直接沿用 SOP：核准的不只首頁，還包括附件清單及每份附件的指紋。 |
| 五：「linter」「結構測試」 | 各給一個文件例子：檢查失效連結／檢查必要章節是否存在。 |
| 六：「scope」「RBAC」 | 先用展示的讀問題單、建 PR、發通知說明權限差異，再命名。 |
| 六：「JSON-RPC」「isError」 | 用同一請求示範：送得到、訊息看得懂、業務操作成功，是三種結果。 |
| 八：「LangGraph」「PEX」「plugin」 | LangGraph 先說流程安排工具；PEX 與 plugin 若不影響決策就刪，不要只報包裝名稱。 |
| 八：「red-then-green」 | 把現有修補前後測試例子移到名稱之前。 |
| 九：「optimizer」「LLM-as-judge」 | 用同一旅客案例分清「提出修改的人」與「依原要求評分的人」。 |
| 九、十：「黃金資料集」「校準」 | 舉一則已由人判定為越權的對話，說明如何核對分類器，以及信心門檻依什麼選。 |
| 十一：「G2 閘門」 | 就地說明是擴張授權的第二道 gate，並保留原文七項聯合條件的範圍。 |

Gateway、proxy、skill、digest 已有類比，但多是先報名稱才解釋；依本輪驗收要求，重排為情境先行即可。`frozen holdout` 已有「不拿來練習的題目」說明，重點是補保管與避免回灌的做法。

`commit point`、`optimistic locking`、`compaction`、`RRF`、`oracle` 沒有出現在這篇正文，不應為了補術語而塞進來。

<!-- tokens: in 4580545 out 23144 -->
