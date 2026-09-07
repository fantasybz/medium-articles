# Codex review — selection

> model: gpt-5.5, reasoning: xhigh, 2026-09-07 14:04. 原話照錄，未經摘要。

我會只讀你指定的 repo 內檔案，不碰 skill 目錄也不改檔。先把 selection、digest、backlog、style brief 和四篇已發布文章交叉讀完，再回頭逐條核對引用與重疊。
<!-- codex ran: /bin/zsh -lc 'wc -l research/2026-09/selection.md research/2026-09/arxiv.md research/2026-09/x_digest.md research/2026-09/community_digest.md research/2026-09/n -->
<!-- codex ran: /bin/zsh -lc 'pwd && rg --files research/2026-09 2026-09-agentic-engineering-platform 2026-09-agentic-org-design 2026-10-agentic-harness-blueprint 2026-11-agent -->
第一輪檔案確認完成：目標檔都在 repo 內，沒有需要外部瀏覽。接下來我會先核對 digest 裡的 citation 編號與數字，再看四篇既有文章的主張邊界。
<!-- codex ran: /bin/zsh -lc "sed -n '221,520p' research/2026-09/arxiv.md" -->
<!-- codex ran: /bin/zsh -lc "sed -n '521,700p' research/2026-09/arxiv.md" -->
<!-- codex ran: /bin/zsh -lc "sed -n '1,220p' research/2026-09/arxiv.md" -->
arXiv digest 先讀完了。selection 的大數字多數有來源，但有幾個會被資深讀者抓：`2607.08885` 不是測 tester，而是 programmer 判斷 assertion；`2608.23610`、`2608.21311` 在目前輸出的片段裡只出現在 digest 綜述，不在主表；這種 citation 要降格或補原文摘要。
下一步會用 `rg` 直接抽 selection 裡引用的 arXiv id，避免只靠長表記憶；同時讀 X / community / Notion digest 來核對需求訊號是不是被誠實使用。
<!-- codex ran: /bin/zsh -lc "sed -n '1,220p' research/2026-09/x_digest.md" -->
<!-- codex ran: /bin/zsh -lc "sed -n '221,380p' research/2026-09/x_digest.md" -->
<!-- codex ran: /bin/zsh -lc "rg -n \"2607\\.08885|2607\\.13196|2607\\.03316|2607\\.21997|2608\\.21311|2607\\.09902|2607\\.21656|2607\\.19267|2609\\.04167|2607\\.27409|2608\\.1 -->
X digest 的需求訊號方向跟 selection 大致一致：10 月 testing/review 最強；12 月 SRE/observability 在 feed 裡反而被標成「幾乎缺席」，所以它不能用熱度當理由，只能用作者地盤與空白市場當理由。11 月的 Teddy/Kim 訊號不在 X digest，得靠 community digest。
<!-- codex ran: /bin/zsh -lc "sed -n '181,340p' research/2026-09/community_digest.md" -->
<!-- codex ran: /bin/zsh -lc "sed -n '1,180p' research/2026-09/community_digest.md" -->
<!-- codex ran: /bin/zsh -lc "sed -n '1,140p' research/2026-09/notion_digest.md" -->
<!-- codex ran: /bin/zsh -lc "sed -n '1,80p' research/2026-09/style_brief.md" -->
<!-- codex ran: /bin/zsh -lc "sed -n '1,260p' research/2026-09/backlog.md" -->
community / Notion / backlog / style brief 讀完後，三個主題的最大風險已經很明顯：不是題目不夠強，而是 10 月和 12 月都會重踩已發布三部曲的 harness/eval/gate 語言。現在我會讀四篇已發布文章，確認哪些段落不能再重講。
<!-- codex ran: /bin/zsh -lc "sed -n '261,560p' 2026-09-agentic-engineering-platform/article.md" -->
<!-- codex ran: /bin/zsh -lc "sed -n '1,260p' 2026-09-agentic-engineering-platform/article.md" -->
<!-- codex ran: /bin/zsh -lc "sed -n '1,260p' 2026-09-agentic-org-design/article.md" -->
<!-- codex ran: /bin/zsh -lc "sed -n '1,320p' 2026-10-agentic-harness-blueprint/article.md" -->
已發布的總論、組織篇、技術篇已讀到：AGENTS.md、MCP gateway、sandbox、legibility、policy、brownfield、eval dataset 都已經被講過。後續如果只是把同一張 harness mindmap 換成 testing/SRE 字眼，會變成自我重複。
<!-- codex ran: /bin/zsh -lc "sed -n '1,260p' 2026-11-agentic-eval-economics/article.md" -->
<!-- codex ran: /bin/zsh -lc "rg -n \"pass\\"'^k|pass@1|G1|G2|gate|SLO|trace|observ|eval|constraint|review|cost|budget|human|escape|AGENTS|harness|SRE|production|Green|綠|驗收|可靠| -->
<!-- codex ran: /bin/zsh -lc "rg -n \"pass\\"'^k|pass@1|G1|G2|gate|SLO|trace|observ|eval|constraint|review|cost|budget|human|escape|AGENTS|harness|SRE|production|綠燈|驗收|可靠|變異|va -->
四篇已發布文章也讀完了。最硬的判斷是：10 月可保留但要收窄，11 月是三個裡最有新增性，12 月若不大幅改題會撞到已發布營運篇和技術篇。
<!-- codex ran: /bin/zsh -lc "nl -ba research/2026-09/selection.md | sed -n '1,190p'" -->
<!-- codex ran: /bin/zsh -lc 'rg -n "''^#|''^##|''^###|''^'"\\| \\*\\*2026|"'^'"\\| Agentic|"'^'"\\| 候選|"'^'"\\| agentic|"'^'"\\| review|"'^'"\\| spec|"'^'"\\| sre|"'^'"\\| cod -->
**致命問題**

- `2026-12：把 Agent 當 Production Workload / thesis_zh`：這題目前跟已發布的技術篇、營運篇重疊太高。技術篇已講 `logs / traces / audit / policy`，營運篇已講 `eval dataset / cost per successful task / scaling gates / vendor management`。  
  修法：不要寫泛用「Agent 的 SRE」。重切成「Agent Run Flight Recorder：trace、approval、incident evidence」；只交付一份 `agent-run evidence schema + incident runbook`。

- `2026-10 / 三、可靠度篇`：`pass^k` 的 coding-agent 證據不足。`SWE-NFI 2607.27409` 是 functional vs non-functional，不是 pass^k；`OpenHarmony 2608.16022` 是 buildability vs behavioral correctness，也不是 pass^k。真正支撐 pass^k 的 `Thinkingbox 2608.19741` 是非 code workflow。  
  修法：把 gate 改成 `functional pass rate + constraint violation rate + NFI/behavioral pass + escape rate`。`pass^k` 只當旁證，等 11 月自己的 N-run 實驗再升格。

- `2026-11 / thesis_zh`：`變異數在 loop 裡，不在 spec 裡` 仍然講太滿。`2608.25399` 只能支持「spec 厚度影響 token，但該研究未觀察到 run-to-run variance 改變」，不能推出 spec 不影響變異。  
  修法：改成「變異數是整個 harness loop 的輸出；spec 是其中一個 input，不是唯一槓桿」。

- `2026-12 / thesis_zh`：`SRE 十年來累積的方法剛好全部適用` 是 overclaim。Agent run 不是穩定 service request；review、approval、tool side effect、model drift 都不是傳統 SRE 可直接套。  
  修法：改成「SRE 的語言有用，但要替 agent 補三個新 SLI：tool-call effect、approval provenance、constraint escape」。

- `排序理由`：12 月排 SRE 的理由不夠硬。X digest 明說 agent observability 在追蹤帳號裡幾乎沒人寫，這可以是空白市場，也可能是需求不足。  
  修法：12 月要嘛降成 2027 backlog，要嘛把 `Coding Agent 的爆炸半徑` 提前，因為它的 arXiv 證據密度和 VP 風險感更強。

**重要問題**

- `2026-10 / 二、Review 篇`：`2607.03316 / 2607.21997 36.4% 接受 / 56.3% 拒絕` 寫法不誠實。這組比例來自 `2607.03316`；`2607.21997` 在 digest 裡是五個 agent 的 54,791 comments 與 resolution pattern，不是同一組接受率。  
  修法：拆成兩句：`2607.03316` 給接受/拒絕率，`2607.21997` 給哪些 comment 會被處理。

- `2026-10 / 二、Review 篇`：`2607.19267` 被寫成「一句話讓 ~80% 外洩 PR 過關」太寬。digest 說的是 laundered PR past scanner / 五-agent pipeline scanner，不等於真實組織 merge。  
  修法：改成「讓約 80% laundered PR 通過該實驗 pipeline 的 scanner」。

- `2026-10 / 一、測試篇`：`人對錯誤斷言的判別只有 49%` 需要標明是 `86 programmers`，不是 tester，也不是所有 reviewer。  
  修法：寫成「86 位 programmer 對錯誤 assertion 的判別只有 49%」。

- `2026-11 / 二、契約篇`：`spec 跨 agent 不可攜（F1 0.035）` 太泛化。`2608.21208` 是 Oracle → PostgreSQL migration，Kiro/Gemini/Copilot 的特定場景。  
  修法：改成「在 DB migration benchmark 中，Kiro-authored specs 給 Gemini 消化時 Token F1 掉到 0.035」。

- `2026-11 / 二、契約篇`：`只做 what` 跟 Notion 裡 Teddy 的定義衝突；Teddy 是 `需求 = What`、`規格 = How`。  
  修法：總論第一節先定義本系列用語，並說明站在 Teddy SDD ladder 的 `Spec-anchored`，不是 `Spec-as-source`。

- `2026-11 / 三、變異篇`：實驗規模對一個月四篇太重。三組、每組 N≥10、AST similarity、測試率、constraint 違規數，很容易拖死 11 月。  
  修法：只做一個 repo、一種任務、一個語言；指標固定為 `test pass / 16-item constraint score / touched-files Jaccard / cost`。AST similarity 可降成 appendix。

- `2026-12 / 一、觀測篇`：`2609.01466` 不是 OTel semantic conventions 證據，是 structured live trace ledger 對 observer token/accuracy 的證據。  
  修法：OTel 用標準文件或 Alolita keynote 當來源；`2609.01466` 只支持「structured trace 比 raw transcript 更可觀察」。

- `2026-12 / 二、可靠篇`：`SLI 只用 telemetry 拿得到的東西` 卻列 `oversight budget`、`pass^k`。這兩個多半是 policy/eval output，不是 raw telemetry。  
  修法：分成 Runtime SLI、Eval SLI、Governance SLI 三欄，不要硬塞進 telemetry。

- `2026-12 / 三、應變與追責篇`：`vendor 條款互相矛盾` 要縮小。`2608.15678` 是 four tools / 18 policy docs / seven providers 的 mapping，不是所有 vendor terms。  
  修法：寫成「現有 provider policy 與 platform controls 對 approval responsibility 沒有共同標準」。

**次要問題**

- `2026-10 / thesis_zh`：`CI 綠燈是 agent 的自我申報` 不準。CI 是 external check，agent closing statement 才是 self-report。  
  修法：改成「CI 綠燈只是 checking，不是驗收；agent 結案報告更不是證據」。

- `2026-10 / 三、可靠度篇`：`綠燈是 34% 的謊言` 可當社群標題，但正文必須每次加 domain。  
  修法：第一次出現就寫「在 SWE-Gate 的 functionally-passing repairs 中，34% 違反 reviewer constraints」。

- `2026-10 / 二、Review 篇`：`人讀 intent 與 constraint，不讀 diff` 會被 Staff engineer 直接打槍。  
  修法：改成「人優先讀 intent / constraint / risky diff；低風險 diff 由 deterministic checks 與 reviewer agent 預篩」。

- `2026-11 / 一、規格篇`：`四十條 Gherkin，然後呢` 是好問題，但要給出口。  
  修法：補一張 decision table：哪些 Gherkin 進 acceptance tests、哪些進 examples、哪些丟棄、哪些變成 reviewer constraints。

- `2026-12 / 為什麼是這個`：`這題現在沒人在講` 跟 Notion 的 Google `Agent Ops` 白皮書衝突。  
  修法：改成「中文工程管理圈幾乎沒人在把 agent run 當 SRE workload 講」。

- `Notion 補充 / 跨主題`：Golden Kubestronaut capstone 會撞 12 月。  
  修法：CNPE 若過，排成 11 月插曲；12 月只在開場用一段，不要再開一條雲原生自傳線。

**建議刪除**

- `2026-12 / 二、可靠篇`：刪掉 K8s sandbox fleet 的細節。這是 backlog `Agent runtime 是平台產品`，放這裡只會稀釋 SLO。保留一句「1,000 人以上才需要 fleet-level SLI」。

- `2026-12 / 三、應變與追責篇`：刪掉「上鏈 $2.30」當主賣點。VP 會被 blockchain 字眼分心。  
  改成「tamper-evident append-only ledger；L2 anchoring 只放 footnote」。

- `2026-10 / 二、Review 篇`：刪掉 `reviewer agent 艦隊` 的炫技包裝。  
  改成一張 `review routing matrix`：auto reject、agent pre-review、human required、security required。

- `2026-11 / 二、契約篇`：刪掉 `SpecMine 47 萬份 spec 長什麼樣` 的 survey 展開。  
  只拿它證明 SDD artifact 已有 corpus；正文聚焦 contract-first / drift gate。

- `落選候選 / 席位經濟`：不要在 10–12 月偷渡個人 Pro/Max 抱怨。selection 已經判定讀者錯位，這個判斷是對的。

**建議補充**

- `2026-10 / 總論`：補 Bach 的 `testing vs checking` 作為全篇詞彙規則。mutation score、constraint tests、pass^k 都叫 check；驗收是 human testing / risk judgment。

- `2026-10 / 一、測試篇`：補作者 workshop A/B 作為主案例：裸 prompt 10/16、`execute-uc` 16/16、測試全綠但 event-sourcing replay 沒測到。這比堆 arXiv 更有殺傷力。

- `2026-10 / 三、可靠度篇`：補一份 `constraint-test template`，來源欄位要有 `review_comment_id / owner / enforcement / expiry`。這是 Staff engineer 可直接帶走的東西。

- `2026-11 / 總論`：補 Kahneman《雜訊》的 `noise audit`。同一 case、多次判斷、量 dispersion，剛好替「同一份規格跑十次」給書錨。

- `2026-11 / 三、變異篇`：補實驗預註冊：model version、temperature/effort、harness version、prompt、repo commit、N、失敗分類。否則結果會像心得文，不像 evidence。

- `2026-12 / 總論`：補「什麼時候 agent 才算 production workload」的判準：會排程執行、會呼叫 write tool、會碰 customer/internal data、會產生 PR 或 deploy artifact、失敗會消耗 on-call attention。

- `2026-12 / 三、應變與追責篇`：補 `approval artifact` 的具體 schema：`run_id / actor / model / harness_version / prompt_digest / tools_used / constraints_checked / human_approver / decision_time`。

總判斷：10 月可做但要砍掉 eval 重複；11 月是三個裡最有新增性，值得排第二；12 月目前不合格，必須重切成 flight recorder / accountability，否則建議把 `Coding Agent 的爆炸半徑` 提前，把 SRE 留到 2027。檔案未修改。

<!-- tokens: in 720217 out 11414 -->
