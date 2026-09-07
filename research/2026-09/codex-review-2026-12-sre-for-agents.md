# Codex review — 2026-12-sre-for-agents

> model: gpt-5.5, reasoning: xhigh, 2026-09-07 14:18. 原話照錄，未經摘要。

我會先只讀你指定的 repo 內檔案與已發布文章，核對引用、段落重疊、以及 selection/style 的硬性約束。不會碰任何技能目錄，也不會修改檔案。
<!-- codex ran: /bin/zsh -lc pwd -->
<!-- codex ran: /bin/zsh -lc 'rg --files research/2026-09' -->
<!-- codex ran: /bin/zsh -lc 'rg --files 2026-09-agentic-engineering-platform 2026-09-agentic-org-design 2026-10-agentic-harness-blueprint 2026-11-agentic-eval-economics' -->
檔案都在指定 repo 內。我接下來會分兩批讀：先讀 selection/style 與四份 digest 建立約束和事實表，再讀已發布文章找重疊與已講過的工件。
<!-- codex ran: /bin/zsh -lc 'wc -l research/2026-09/style_brief.md' -->
<!-- codex ran: /bin/zsh -lc 'wc -l research/2026-09/selection.md' -->
<!-- codex ran: /bin/zsh -lc 'wc -l research/2026-09/arxiv.md' -->
<!-- codex ran: /bin/zsh -lc 'wc -l research/2026-09/x_digest.md' -->
<!-- codex ran: /bin/zsh -lc 'wc -l research/2026-09/community_digest.md' -->
<!-- codex ran: /bin/zsh -lc 'wc -l research/2026-09/notion_digest.md' -->
我會先抓完整內容，不只看摘要行，因為這份計畫大量用到「digest 裡的一句話」當證據。接著會抽出每個 arXiv/X/社群/Notion 來源的實際數字與限定語。
<!-- codex ran: /bin/zsh -lc "sed -n '1,120p' research/2026-09/style_brief.md" -->
<!-- codex ran: /bin/zsh -lc "sed -n '1,220p' research/2026-09/notion_digest.md" -->
<!-- codex ran: /bin/zsh -lc "sed -n '1,220p' research/2026-09/selection.md" -->
selection/style 的硬約束很清楚：12 月要限定「中文、harness layer」，不能拿 Claude Taiwan 席位抱怨當證據，K8s 只能是規模化段落，且一定要超越 2025 model-call observability。現在開始核對每個 cited source 的實際 digest 內容。
<!-- codex ran: /bin/zsh -lc "sed -n '1,180p' research/2026-09/x_digest.md" -->
<!-- codex ran: /bin/zsh -lc "sed -n '1,220p' research/2026-09/arxiv.md" -->
<!-- codex ran: /bin/zsh -lc "sed -n '1,180p' research/2026-09/community_digest.md" -->
<!-- codex ran: /bin/zsh -lc "sed -n '181,360p' research/2026-09/x_digest.md" -->
<!-- codex ran: /bin/zsh -lc "sed -n '221,460p' research/2026-09/arxiv.md" -->
<!-- codex ran: /bin/zsh -lc "sed -n '181,360p' research/2026-09/community_digest.md" -->
初步看到幾個高風險點：計畫有些地方已經自覺標「動筆前確認」，但正文段落仍把它當既定證據用；另外 OTel span 名稱、KubeCon keynote、Reuters/Engadget 事件這類時效/規格來源不能只靠 digest。繼續讀完 arXiv 後半與已發布文章。
<!-- codex ran: /bin/zsh -lc 'wc -l 2026-09-agentic-engineering-platform/article.md' -->
<!-- codex ran: /bin/zsh -lc "sed -n '461,700p' research/2026-09/arxiv.md" -->
<!-- codex ran: /bin/zsh -lc 'wc -l 2026-09-agentic-org-design/article.md' -->
<!-- codex ran: /bin/zsh -lc 'wc -l 2026-10-agentic-harness-blueprint/article.md' -->
<!-- codex ran: /bin/zsh -lc 'wc -l 2026-11-agentic-eval-economics/article.md' -->
arXiv digest 的後半支持多數數字，但也暴露出一個問題：計畫把「content-addressed behavioural configuration」改寫成自己的 tuple 時有標註，但應變篇又把它說成「對齊」，這要收斂。接著看四篇已發布稿，重點抓已用過的表格、gate、RACI、metric tree、sandbox/MCP/guardrails，避免 12 月重寫同一篇。
<!-- codex ran: /bin/zsh -lc 'rg -n "''^(#|##|###)|TL;DR|SRE|observability|trace|OTel|SLO|error budget|on-call|postmortem|harness|MCP|sandbox|AGENTS|guardrail|kill switch|rever -->
<!-- codex ran: /bin/zsh -lc 'rg -n "''^(#|##|###)|TL;DR|SRE|observability|trace|OTel|SLO|error budget|on-call|postmortem|harness|MCP|sandbox|AGENTS|guardrail|kill switch|rever -->
<!-- codex ran: /bin/zsh -lc 'rg -n "''^(#|##|###)|TL;DR|SRE|observability|trace|OTel|SLO|error budget|on-call|postmortem|harness|MCP|sandbox|AGENTS|guardrail|kill switch|rever -->
<!-- codex ran: /bin/zsh -lc 'rg -n "''^(#|##|###)|TL;DR|SRE|observability|trace|OTel|SLO|error budget|on-call|postmortem|harness|MCP|sandbox|AGENTS|guardrail|kill switch|rever -->
<!-- codex ran: /bin/zsh -lc 'wc -l research/2026-09/2026-12-sre-for-agents.md' -->
<!-- codex ran: /bin/zsh -lc 'rg -n "''^(#|##|###|####)|為什麼是現在|一句話論點|總論的分工原則|Outcome 來源規則|觀測篇|可靠篇|應變|寫作前要補|總論與三篇之間的不重疊檢查|上稿 References|來源對照" research/2026-09/2026-12-sre-for-ag -->
<!-- codex ran: /bin/zsh -lc "rg -n \"2609\\.01466|2609\\.01931|2608\\.23610|2608\\.15678|2608\\.26218|2607\\.03691|2608\\.11274|2608\\.29204|2608\\.11965|2608\\.24271|2608\\.1 -->
<!-- codex ran: /bin/zsh -lc "sed -n '79,120p' 2026-09-agentic-engineering-platform/article.md" -->
<!-- codex ran: /bin/zsh -lc "sed -n '142,166p' 2026-09-agentic-org-design/article.md" -->
<!-- codex ran: /bin/zsh -lc "sed -n '101,129p' 2026-10-agentic-harness-blueprint/article.md" -->
<!-- codex ran: /bin/zsh -lc "sed -n '178,207p' 2026-10-agentic-harness-blueprint/article.md" -->
<!-- codex ran: /bin/zsh -lc "sed -n '84,112p' 2026-11-agentic-eval-economics/article.md" -->
<!-- codex ran: /bin/zsh -lc "sed -n '112,166p' 2026-11-agentic-eval-economics/article.md" -->
已發布四篇的重疊主要集中在三塊：DevOps ↔ Agentic 對照、組織篇的「復用 SRE o11y stack」、技術篇的 MCP gateway / guardrails、營運篇的 cost model / metric tree / G1–G3。12 月要成立，必須把「trace-backed SLO 與 attestation」做成主工件，否則會像 9 月營運篇的延長版。
<!-- codex ran: /bin/zsh -lc 'rg -n "a16z|matei|Databricks|Unity AI Gateway|OpenAI agents|Engadget|Reuters|Uncle Bob|unclebob|Kubernetes v1.37|Garhwal|HPA scale-to-zero|pod cer -->
<!-- codex ran: /bin/zsh -lc 'rg -n "Backend 台灣|Grafana|openab|Claude Code|AIOps|Agent Ops|KubeCon|Alolita|OTel|Weinberg|Grok|Claude Taiwan|席位|觀測|observability|Backend|DevOps T -->
<!-- codex ran: /bin/zsh -lc "rg -n \"2608\\.22752|2608\\.25399|2608\\.23067|2608\\.21929|2608\\.23550|2609\\.00006|2608\\.21311|2608\\.24979|Frontier|READY|Thinkingbox|traject -->
我只用 repo 內指定檔案核對；沒有外部 browsing。未列為問題的數字大多能在 digest 對上。問題集中在 OTel 規格假設、SLI 定義、低流量 burn-rate、追責 tuple、以及篇幅失控。

**致命問題**
- **總論 §六 / 觀測篇 §2 / F5**：`invoke_agent`、`execute_tool` 被寫成 OTel GenAI semconv「規格已有」，但這不是 digest 可驗證內容，且計畫自己也列為動筆前確認。這是封面與主工件的承重點。  
  修法：正文改成「以 2026-11 semconv 實查為準；規格沒有的先落 `org.*`」，F5 不要在確認前標「規格已有」。

- **總論 §五 / 觀測篇 §2 / 可靠篇 §3**：`outcome_verified=success` 只要 tests、CI、human approval 三者之一即可，邏輯太鬆。人的 approve 不是「事實」，只是責任承擔；CI green 也只是 check。這會把「agent 不能自填 SLI」換成「人可以用意見填 SLI」。  
  修法：改成 workflow-specific evidence matrix。bug-fix PR 至少要 `tests_exit_0 AND ci_green AND final_review AND merge`；human approval 單獨只能叫 `accepted_risk`，不能叫 verified success。

- **可靠篇 §3 / §5 / 觀測篇 §6**：低流量問題只處理 revert rate，沒有處理 run availability。若一條 golden workflow 每月 30–100 個 run，1h / 5m burn-rate alert 對 run availability 幾乎沒有統計意義。  
  修法：所有 burn-rate rule 加 `min_events`；低於門檻只進 daily/weekly gate。1h/5m 只用在 tool-call 這種高事件量訊號，或跨 workflow 聚合。

- **可靠篇 §3 / YAML `error_budget_policy`**：前文說三個事件比率都進 error budget，但 YAML 的 `remaining` 只取 run availability 與 tool error，revert rate 只是 gate。這是內部矛盾。  
  修法：二選一。要嘛改成「兩個 fast error budget + 一個 lagging quality gate」；要嘛真的建立第三個 lagging budget，只是不 alert。

- **應變篇 §4 / 2608.23610**：論文的 behavioural tuple 尚未確認，計畫卻把自己的四欄 hash 說成 behavioural tuple 對應。這可能是誤用來源。  
  修法：明寫「2608.23610 證明平台缺 content-addressed behavioural configuration；本文四欄 attestation 是作者設計，不等於論文定義，全文確認後再對齊」。

- **全系列 / §6 時程**：12/1、12/4、12/8、12/11 四篇，加上 15 項補證據、實作 instrumentation、status check、真 trace 截圖、全文讀六篇論文，不是一個作者一個月可控的範圍。  
  修法：只保三個工件：trace schema + Collector config、`agent-slo.yaml`、attestation status check。K8s fleet、資安 survey、英文版集中發都延後。

**重要問題**
- **總論 §三「有規模」/ AgentLogs**：「目前最大公開 agent 遙測資料集」在 digest 沒有支撐。digest 只支撐 307,416 tasks、64.3M log entries。  
  修法：刪「最大」，改「一份可用來練 dashboard 的公開資料集」。

- **總論 §五 / 2608.26742**：把 Claude Code 208 頁 handbook 稱為「vendor 自己的操作手冊」不誠實。digest 只說 operational reference，沒有說 Anthropic 官方。  
  修法：除非確認作者與官方性，改成「一份 Claude Code 操作手冊」。

- **總論 §三 / Reuters-Engadget / Grok outage**：新聞與 outage 都只從 X digest 來，不能當研究級證據。  
  修法：找到 Reuters/Engadget 原文才引用；Grok outage 找不到原始貼文就只寫「據 X 報告」，不進 References。

- **總論 §十 / 可靠篇 §7**：「Kubernetes 也在為這種 workload 改版」過強。v1.37 features 是 general platform primitive，不是為 agent workload 設計。  
  修法：改「v1.37 有幾個剛好可借的 primitive」。

- **可靠篇 §7 / 2608.15127**：「容量規劃是記憶體與啟動時間，不是 CPU」過強。digest 只支撐 non-LLM components dominate latency、sandbox memory peaks 28GB、四個修正省 29–40%。  
  修法：改「CPU 不是唯一主軸；memory peak、cold start、non-LLM latency 必須一起量」。

- **可靠篇 §3 / tool-call error rate**：permission error、business error、測試失敗、故意的 deny 可能是正常控制，不應全部燒 budget。  
  修法：拆成 `unexpected_tool_failure_rate`、`policy_violation_rate`、`expected_check_failure_rate`。只有 unexpected failure 進 budget。

- **觀測篇 §6**：「vendor 原生 telemetry export 做不出 F5 trace tree」目前是待實測，不是證據。  
  修法：在自己的 instrumentation 實驗完成前，只寫成 hypothesis；完成後補 compatibility table。

- **應變篇 §4 / status check**：CI 從 Tempo 讀 trace 會受 30 天 retention 影響，且 Tempo 是 debug store，不是 evidence store。  
  修法：status check 的真值來源改 event ledger；Tempo link 只給人查 trace。

- **總論 §四 / F2**：DevOps/SRE 歷史類比重複 9 月總論 §三。  
  修法：刪 F2 或縮成一段，只保留「SRE 借得動 / 要重做」F7，這才是 12 月新增價值。

- **總論 §十 / F11**：50 / 200 / 1,000 人規模表重複組織篇 §三。  
  修法：只列 SRE delta：trace、SLO、on-call、attestation；sandbox 買/建不要再重講。

- **觀測篇 §5**：trace → eval 回填會重複營運篇 §二 eval pipeline。  
  修法：只補一個 `source: trace:r_...` 的 eval case 範例，不重畫 pipeline。

- **應變篇 §1 / 2608.12654**：SteerBench-Work 已標非 coding / 非 SRE，仍用 28.1% / 1.0% 支撐 on-call 邊界太勉強。  
  修法：數字移腳註；主論證靠 tool tier、independent review、dangerous tools policy。

**次要問題**
- **總論與三篇不重疊檢查 / burn-rate**：說「每個數字只落一處」，但 13.4 / 5.6 / 0.93 在觀測、可靠、應變、YAML 多處出現。  
  修法：可靠篇為 canonical；其他篇只寫「同可靠篇的 28 天 burn-rate rule」。

- **觀測篇 §2 / `human.approval`**：把未提案成功的名字故意不加 org prefix，像在替標準命名，不像落地文。  
  修法：實作一律用 `org.approval`；最後一段再說「可提案成 `human.approval`」。

- **可靠篇 §3 / cost per successful task**：只看 successful denominator 會藏掉失敗成本與任務組成變化。  
  修法：同時列 `cost_per_attempted_run`、`waste_cost_rate`，並依 `task_class` / `risk_tier` 分層。

- **可靠篇 §3 / latency**：扣掉 approval latency 會讓 VP 看不到真實 lead time。  
  修法：分兩個指標：automation active time、end-to-end lead time。

- **應變篇 §2 / page rule**：「只有 injection 與 touches production 才 page」太粗。  
  修法：page 條件改成 blast radius：dangerous tool、credential exposure、prod data mutation、external side effect、injection。

**建議刪除**
- **總論 §一 CNPE / Kubestronaut 開場**：壓成一句。不要讓證照敘事搶走 thesis。
- **總論 §四 F2 timeline**：刪。9 月已講過 DevOps 對照。
- **可靠篇 §7 K8s / CNPE 詳表**：移到 backlog「agent runtime as platform product」。12 月只留 F11 的一列。
- **應變篇 §6 資安段**：保留一段結論即可。2608.27299、2609.01222、2608.28502 不要展開成小型爆炸半徑文。
- **AgentLogs dashboard 練習殘留**：既然練習節已刪，總論不要再暗示可以拿來「練 dashboard」太多。
- **英文版與推廣細節**：從主計畫拆出去。現在干擾判斷篇章是否寫得完。

**建議補充**
- **觀測篇 §2 前**：加「signal availability matrix」：Claude Code CLI、Codex、Copilot cloud agent、Cursor cloud、Managed Agents 分別能不能拿 run / tool / approval / cost / outcome。
- **觀測篇 §2 / §6**：補最小 reference implementation：一個 PostToolUse hook 發 OTLP、Collector config、PromQL、真 trace 截圖。
- **可靠篇 §3**：補 workflow evidence matrix。不同 workflow 的 success evidence 不同，不能全靠三種訊號 OR。
- **可靠篇 §5**：補 SLI → action table：哪個 SLI 燒掉、freeze / add approval / rollback / page / vendor escalation 各怎麼走。
- **全系列**：補 tamper boundary。agent 能不能改 hook、改 `harness.lock`、關 telemetry、改 PR body？答案必須是「不能」，而且要說靠什麼隔離。
- **應變篇 §4**：補 ledger-backed attestation flow：PR body 是索引，CI 真值讀 ledger，review event 讀 GitHub API。
- **觀測篇 §6 / 應變篇 §3**：補資料治理表：哪些 attribute 可進 trace，哪些只能 hash，transcript 誰能看，retention 多久。

<!-- tokens: in 1330563 out 17806 -->
