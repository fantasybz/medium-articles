# Codex review — 2026-10-agentic-green-is-not-done

> model: gpt-5.5, reasoning: xhigh, 2026-09-07 14:08. 原話照錄，未經摘要。

我會只讀 repo 內指定的研究摘要、style / selection、既有文章與這份計畫本身，然後按你指定的五類輸出審稿意見。不會碰任何 Claude/agents 目錄，也不會修改檔案。
<!-- codex ran: /bin/zsh -lc 'pwd && rg --files research/2026-09 2026-09-agentic-engineering-platform 2026-09-agentic-org-design 2026-10-agentic-harness-blueprint 2026-11-agent -->
<!-- codex ran: /bin/zsh -lc 'wc -l research/2026-09/arxiv.md research/2026-09/x_digest.md research/2026-09/community_digest.md research/2026-09/notion_digest.md research/2026- -->
我先把判斷基準讀完：selection 決定這份計畫必須修正哪些舊問題，style brief 決定文章格式，四份 digest 決定哪些數字不能亂用。接著再看四篇已發文章，避免把同一套 G2 / eval / guardrail 再寫一次。
<!-- codex ran: /bin/zsh -lc 'nl -ba research/2026-09/style_brief.md' -->
<!-- codex ran: /bin/zsh -lc 'nl -ba research/2026-09/selection.md' -->
<!-- codex ran: /bin/zsh -lc "nl -ba research/2026-09/arxiv.md | sed -n '1,220p'" -->
<!-- codex ran: /bin/zsh -lc 'nl -ba research/2026-09/x_digest.md' -->
<!-- codex ran: /bin/zsh -lc 'nl -ba research/2026-09/community_digest.md' -->
<!-- codex ran: /bin/zsh -lc 'nl -ba research/2026-09/notion_digest.md' -->
selection 裡最重要的硬約束是：標題級數字要標領域、社群訊號不能膨脹、19 篇 arXiv 不能只憑 digest 一行、10 月不能偷吃 11/12 月題材。style brief 也要求每篇要有 decision artifact、reference implementation / snippet、brownfield 現實檢查，而不是只做觀念文。
<!-- codex ran: /bin/zsh -lc "nl -ba research/2026-09/arxiv.md | sed -n '110,260p'" -->
<!-- codex ran: /bin/zsh -lc "nl -ba research/2026-09/arxiv.md | sed -n '260,430p'" -->
<!-- codex ran: /bin/zsh -lc "nl -ba research/2026-09/arxiv.md | sed -n '430,620p'" -->
<!-- codex ran: /bin/zsh -lc "nl -ba research/2026-09/x_digest.md | sed -n '130,240p'" -->
<!-- codex ran: /bin/zsh -lc "nl -ba research/2026-09/x_digest.md | sed -n '240,340p'" -->
<!-- codex ran: /bin/zsh -lc "nl -ba research/2026-09/community_digest.md | sed -n '145,240p'" -->
目前看起來，計畫已經修掉不少 selection 指出的過度宣稱：例如 SWE-Gate 的 34% 分母、READY 非 code 旁證、AI-to-AI 的 cross-product 限定都有寫進去。但我也看到幾個還會被 Staff/VP 抓的地方：主張一的「payment PR 不讀 diff」仍然比 evidence 強，且 review / reliability gate 的職責邊界還有互相踩線。
接下來我讀四篇已發布稿。重點不是找字面重複，而是看這份 10 月計畫有沒有把上一季已經交代過的 org / harness / eval / G2 再包一遍。
<!-- codex ran: /bin/zsh -lc 'nl -ba 2026-09-agentic-org-design/article.md' -->
<!-- codex ran: /bin/zsh -lc 'nl -ba 2026-09-agentic-engineering-platform/article.md' -->
<!-- codex ran: /bin/zsh -lc 'nl -ba 2026-10-agentic-harness-blueprint/article.md' -->
<!-- codex ran: /bin/zsh -lc 'nl -ba 2026-11-agentic-eval-economics/article.md' -->
四篇已發布稿確認了重疊風險：上一季已經講過 harness 五層、AGENTS.md、feedback legibility、guardrails、eval dataset、G2 gates、90 天藍圖。10 月計畫要能成立，必須把新內容收束在「test/review/reliability gates 的可執行檢查」，不能再重講「怎麼導入 agentic platform」。
<!-- codex ran: /bin/zsh -lc 'rg -n "''^(#|##|###) " research/2026-09/2026-10-agentic-green-is-not-done.md' -->
<!-- codex ran: /bin/zsh -lc "rg -n \"2609\\.04167|2609\\.02095|2607\\.18057|2608\\.21311|2608\\.29460|2607\\.08885|2607\\.19267|2607\\.13196|2607\\.09902|2607\\.03316|2607\\.1 -->
<!-- codex ran: /bin/zsh -lc 'rg -n "review|diff|approve|branch protection|CODEOWNERS|GitHub|AI approve|required approvals|human approve|指派者|抽樣|人工複核" research/2026-09/2026-10-a -->
<!-- codex ran: /bin/zsh -lc "rg -n \"G2|90 天|Brownfield|AGENTS\\.md|MCP gateway|guardrails|eval|golden|review 成為新瓶頸|legibility|policy YAML|agent-policy|flaky|pass\\"'^k|oversi -->
**致命問題**
1. 【§1 一句話論點、§2 TL;DR、§2 一】核心前提仍未被量到：`agent PR 的測試多半由 agent 寫/改`。計畫有承認，但 TL;DR 又寫成普遍現象。修法：所有 headline/TL;DR 改成「**在 agent 新增或修改測試的 PR 裡**」，沒有第一手比例就不要寫「多數團隊」。

2. 【§1 三個可反駁主張 #1、Review 篇 §三】「payment PR 不讀 diff」證據撐不起來。SWE-Gate 只證明 functional tests 通過仍違反 reviewer constraints，不證明高風險金流變更可以不看 diff。修法：改成「不逐行全讀；讀 intent、constraint report、mutation report，並只讀被標紅 hunk / compliance-sensitive files」。

3. 【§1 為什麼是現在、§2 八、可靠度篇 §四】READY 的「臨床稽核、16 個 agent 系統、750 case」不在 [arxiv.md](/Users/kochi.chuang/conductor/workspaces/medium-articles/yokohama/research/2026-09/arxiv.md:56)。在 repo 來源裡只能驗到 72.8/72.5、39.2/29.6、76%。修法：把全文摘錄補進研究檔；否則正文只能寫「READY 摘要顯示……領域待全文確認」。

4. 【§4 寫作前要補的證據、§6 發布節奏】這個月寫不完。四篇 zh、四篇 en、22 張 Mermaid、GitHub ruleset 實測、mutation tool 查證、Bach 補讀、社群授權、第一手 PR 實驗，還要 10 月啟動 11 月實驗。修法：10 月只承諾 zh 四篇 + en 總論；英文三部曲延後。圖減半，Review 篇 references 壓到 10 篇內。

5. 【可靠度篇 §四 C3】oversight formula 把 2607.08885 的 49%–74% 拿來當 `c` 的量級，仍是 domain mismatch。那篇量的是「判斷 LLM 斷言」，不是 review PR 抓錯率。修法：`c` 必須來自本組織抽樣深讀的歷史資料；49%–74% 只能當「人眼不可假設為 100%」的警告。

**重要問題**
1. 【§2 三、F3、測試篇 §二/§六】2607.18057 已可定案：digest 寫的是 `existing tests cover`，不是 PR 內測試覆蓋率，見 [arxiv.md](/Users/kochi.chuang/conductor/workspaces/medium-articles/yokohama/research/2026-09/arxiv.md:217)。修法：刪掉「PR 內測試版」備案；這篇不能拿來支撐「agent 自己的測試沒測到自己改動」。

2. 【可靠度篇 §二、Review 篇 §三】2607.13091 支撐「review comment 變 version-controlled rule + pre-submit checklist」，不直接支撐「constraint test 進 CI」，見 [arxiv.md](/Users/kochi.chuang/conductor/workspaces/medium-articles/yokohama/research/2026-09/arxiv.md:223)。修法：2607.13091 只當規則回收證據；可執行 constraint tests 用 SWE-Gate/SWE-NFI 支撐，你自己的 AST check 當 implementation。

3. 【§2 十 驗證預算】2608.28795 是 web app boot probe / shell reach 的成本研究，不足以推出「每 1 元生成配 0.3–0.5 元驗證 compute」。修法：刪比例，或明標「作者暫定 budgeting heuristic，待 pilot 校準」；來源只用來講 reach principle。

4. 【§2 十 Brownfield】和已發布 Harness 篇衝突。Harness 篇 brownfield 順序是 characterization tests → logs/traces → architecture rules；本計畫改成 constraint tests 第一。修法：加「這是驗證層安裝順序，不取代 legibility brownfield 順序」；或補第 0 步：先 characterization tests 鎖現狀。

5. 【Review 篇 §三】「每次 merge 都有人類 approve」但低 radius 可由指派者一分鐘 approve，實務上會變 rubber stamp。修法：一分鐘 approve 要有最小 checklist 與簽核句；抽樣深讀必須由非指派者做，且抽樣比例公開。

6. 【Review 篇 §四/§五/§七】「AI approve 是訊號欄」語意混亂。既然不計入 required approvals，同 vendor 不同 session 又不進訊號欄，就不要用 GitHub `APPROVED` 事件。修法：artifact 欄位改成 `ai_review_verdict: pass|fail|uncertain`，GitHub approve 只保留給人。

**次要問題**
1. 【§2 一】「CI 綠、review 排隊、上線出事是同一個問題」太硬。修法：改成「同一個驗證層缺口的三個症狀」。

2. 【§2 五】「Uncle Bob negative test experiment 是 SWE-Gate 的個人版」過度類比。修法：改成「同方向旁證：acceptance tests 全過仍無法區分品質」。

3. 【可靠度篇 §三】`pass@1 = k 次平均` 會被懂 benchmark 的人挑戰。修法：寫成「用 k 次 repeated runs 估計 pass@1」，並明確區分 `pass@k`、`pass^k`。

4. 【§6 粉絲團 hook、可靠度篇 hook】READY hook 寫「兩個 agent 準確率差 0.3pp……」但 domain 放「見文內」不夠。修法：社群貼文也直接標「非 code、臨床稽核工作流旁證」。

5. 【§2 圖清單】總論 10 張 Mermaid + 表格圖太像簡報，不像 Medium 長文。修法：總論留 F1、F2、F7、F9、F12；其他表格化。

**建議刪除**
1. 刪【§2 八 F10 READY 圖】：非 code 旁證不值得在總論畫圖，會放大 domain mismatch。
2. 刪【§2 九 F11 反模式圖】：反模式表已足夠，圖只是重複。
3. 刪【§2 十 0.3–0.5 元驗證 compute】：目前是沒有來源的 CFO 數字，風險最高。
4. 刪或移【Review 篇 §二 secret 那列】：放在社交工程 PR 或 deterministic scan，不要塞進「真實 PR review 資料」主線。
5. 刪【§1/§2 過多 model launch name-dropping】：Fable/Astra 只留「vendor 開始販售 self-verification」一句，不要讓文章像追新聞。
6. 刪【歷史類比中的 Fagan/Google readability 支線】：Bach + deployment pipeline + mutation testing 已夠，review 史會分散主軸。

**建議補充**
1. 加【全系列共用 evidence ledger】：每個來源列 `domain / n / 可支持的句子 / 禁止推論`。這會直接防止 READY、2607.18057、2607.13091 再被誤用。
2. 加【Review 篇 §三】`risk-map.yaml`：用 path/CODEOWNERS 定義 auth/payment/schema/infra，否則 blast radius 只是口號。
3. 加【測試篇 §五、Review 篇 §七、可靠度篇 §二】實際 artifact 範例：PR comment、approval artifact、constraint report、mutation report。Staff engineer 需要看到輸出長什麼樣。
4. 加【測試篇 §四/§五】false positive 與 bypass 策略：equivalent mutants、mutation timeout、assertion-diff allowlist、snapshot 合理更新、flaky quarantine。
5. 加【可靠度篇 §五】小樣本信賴區間：golden set 20–50 case 時，門檻不要只給點估計；至少用 Wilson interval 或「連續兩月 + 最小樣本數」。
6. 加【§4 補證據】「agent 寫測試比例」的 provenance 定義：bot account、co-authored-by、commit signer、PR label、session log，哪一種算 agent-written 要先定義。

<!-- tokens: in 862151 out 13393 -->
