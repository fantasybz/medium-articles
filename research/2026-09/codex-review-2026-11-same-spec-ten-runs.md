# Codex review — 2026-11-same-spec-ten-runs

> model: gpt-5.5, reasoning: xhigh, 2026-09-07 14:13. 原話照錄，未經摘要。

我會只讀 repo 內的研究摘要、計畫檔與已發布文章，不碰你列出的技能目錄，也不修改任何檔案。這次是內容審查，不需要啟用任何 skill。
<!-- codex ran: /bin/zsh -lc pwd -->
<!-- codex ran: /bin/zsh -lc 'wc -l research/2026-09/2026-11-same-spec-ten-runs.md research/2026-09/arxiv.md research/2026-09/x_digest.md research/2026-09/community_digest.md r -->
<!-- codex ran: /bin/zsh -lc 'rg --files' -->
我先抓研究摘要與 selection/style brief，會用它們當「證據邊界」。接著才對照 plan 與已發布文章，避免被 plan 自己的修訂說法帶著走。
<!-- codex ran: /bin/zsh -lc "nl -ba research/2026-09/selection.md | sed -n '1,220p'" -->
<!-- codex ran: /bin/zsh -lc "nl -ba research/2026-09/arxiv.md | sed -n '1,220p'" -->
<!-- codex ran: /bin/zsh -lc "nl -ba research/2026-09/style_brief.md | sed -n '1,120p'" -->
<!-- codex ran: /bin/zsh -lc "nl -ba research/2026-09/x_digest.md | sed -n '1,360p'" -->
目前 selection 明確要求 11 月要守住兩條底線：第一，不能再把「spec 決定上限」講成主論點；第二，沒有第一手 N-run 數據就撐不起這個題。接下來我會逐條核對引用數字，尤其是 plan 內反覆使用的 arXiv id。
<!-- codex ran: /bin/zsh -lc "nl -ba research/2026-09/arxiv.md | sed -n '260,430p'" -->
<!-- codex ran: /bin/zsh -lc "nl -ba research/2026-09/arxiv.md | sed -n '100,260p'" -->
<!-- codex ran: /bin/zsh -lc "nl -ba research/2026-09/arxiv.md | sed -n '430,620p'" -->
<!-- codex ran: /bin/zsh -lc "nl -ba research/2026-09/community_digest.md | sed -n '1,360p'" -->
<!-- codex ran: /bin/zsh -lc "nl -ba research/2026-09/notion_digest.md | sed -n '1,140p'" -->
研究摘要裡已經看到幾個高風險點：2608.25399 的 `run-to-run variance unchanged` 在 digest 只和 token spend 放在一起，plan 卻想把「輸出結構變異沒人量過」當主張；2608.26197 只有 abstract 一行，不能承擔太多重量。現在我讀已發布四篇，找重疊與讀者工件缺口。
<!-- codex ran: /bin/zsh -lc "nl -ba 2026-09-agentic-org-design/article.md | sed -n '1,260p'" -->
<!-- codex ran: /bin/zsh -lc "nl -ba 2026-09-agentic-engineering-platform/article.md | sed -n '1,560p'" -->
<!-- codex ran: /bin/zsh -lc "nl -ba 2026-11-agentic-eval-economics/article.md | sed -n '1,260p'" -->
<!-- codex ran: /bin/zsh -lc "nl -ba 2026-10-agentic-harness-blueprint/article.md | sed -n '1,320p'" -->
<!-- codex ran: /bin/zsh -lc "rg -n \"2608\\.25399|2608\\.26197|2608\\.23740|2607\\.27877|2608\\.26218|2609\\.03966|2608\\.22752|2608\\.30300|2608\\.20851|2608\\.16618|2609\\.0 -->
<!-- codex ran: /bin/zsh -lc 'rg -n "Teddy|Kim Kao|Uncle Bob|AGENTS.md|G2|review minutes|payment-timeout-fix|spec-lint|drift|A0|Fable|Kahneman|雜訊|人類校準|N=10|N ≥ 10|same spec|同一份 -->
<!-- codex ran: /bin/zsh -lc 'rg -n "unclebobmartin|negative|25|acceptance|Fable 5.1|Thariq|trq212|AYi_AInotes|AntonyMarcano|wquguru|over-spec|skills|reproduc|TDD|mutation|same -->
<!-- codex ran: /bin/zsh -lc 'rg -n "AGENTS.md|MCP|sandbox|eval|G2|review minutes|Cost|Retry|Golden|payment-timeout-fix|policy|conventions|Guardrails|legibility|90 天|變異|spec|契約 -->
**致命問題**
- **總論 §四 / 一句話論點**：`變異源自 model sampling；源頭只有一個` 講太滿。摘要只支持 loop / topology / harness 會影響 variance，不支持 sampling 是唯一來源；tool output、外部 API、時間、flaky tests、context assembly 也會製造差異。  
  **修法**：改成「在 pin 住外部狀態後，model sampling 是主要 entropy；harness / context / tools / environment 會放大或衰減它」。

- **總論 TL;DR、§五、P3 §五、FB/X hooks**：`輸出結構的變異沒人直接量過 / 第一次量` 不誠實。`arxiv.md` 對 2608.25399 明寫 `run-to-run variance unchanged`，只是摘要沒說量的是 token 還是 output。  
  **修法**：全文改成「摘要未交代 variance 指標；本系列補一個 repo-specific structural similarity 量法」。刪掉「沒人量過」「第一次」。

- **變異篇 §二 / 第 3 節寫作前證據**：一個月內要完成 50 runs、人類校準帶、AST similarity、30 PR 盲審、七篇全文、Teddy/Kim 授權、25 張圖、四篇中英版，實際不可行。  
  **修法**：保留 A0/A/B/C 各 N=10 與人類校準帶；砍迷你前代 model、英文同步、非必要圖。AST 從第一天就允許 difflib fallback，不要把工具校準放在發文前一週。

- **總論 §六、F8 / 變異篇 P3-T3**：2607.25141 被拿來放進「穩定地錯」象限，但 digest 只說 Dockerfile/Compose 一致漏掉三類 non-functional 要求，沒有 run-to-run variance 數據。圖上把它放在低變異位置，是視覺 overclaim。  
  **修法**：F8 拿掉該點，或標成「概念示意，非該論文量測值」。

- **規格篇 / 契約篇 vs 變異篇**：前兩篇用 `payment-timeout-fix` 的 Go 範例，變異篇實驗卻改成 Java/Spring event-sourcing。讀者會問：你給的模板與 gate，到底有沒有跑出第三篇的數字？  
  **修法**：全系列只用一個實驗案例。若 skills 必須靠 Java/Spring 才有價值，就把規格篇與契約篇的 worked example 也改成那個 repo；`payment-timeout-fix` 只作為已發布營運篇的格式回顧。

**重要問題**
- **來源歸屬表 / 總論 §四**：你說 2608.26218、2609.03966、2608.22752 是 12 月獨佔，但總論 §四重述了 `28%→49%`、`0.00 vs 0.96`、`53%→10%`。  
  **修法**：11 月只寫「多篇 harness-pin 研究顯示組態敏感，數字留 12 月」，不要列數字。

- **總論 §六**：2608.25241 的 `+53% vs +27%` 是 observational repo-level quality cost，不是「每次長得不一樣累積出來」的證據。  
  **修法**：改成「品質側指標值得量的動機」，不要當 run-to-run variance 的機制證據。

- **規格篇 §四 / 總論 §五**：`需求總是晚到` 超過 2609.03028 的摘要。來源只說 late requirements 一旦在首次實作後出現，造成約 2x invalidation，且預警無效。  
  **修法**：改成「晚到需求很貴，而且事先警告無效」，不要寫「總是」。

- **總論 §五 / 規格篇 §三**：2608.16618 被寫成「完整是必要條件」。摘要只說能力越強越依賴 correct, complete human specs。  
  **修法**：改成「完整 spec 的槓桿變大」，不要寫必要條件。

- **總論歷史類比 / §九**：2608.26197 的 `reproducibility 1.000` 被比成 bit-for-bit build，還加上 `plan 僵硬度`。digest 只有 reproducibility metric 與 latency cost。  
  **修法**：全文只保留「特定 3/4 cells 的 reproducibility metric 1.000；代價是 latency」。其他等全文讀完再寫。

- **英文版 hooks / Uncle Bob 引用**：`same spec 8 times` 不受 `x_digest.md` 支持。digest 支持的是同一個 Wumpus 問題、四種測試紀律、同樣 25 acceptance cases 都過、programs not the same。  
  **修法**：改成 `same acceptance suite / same problem`，不要寫 same spec。

- **總論 §七 / G2 gate**：`3 tasks × 3 組 × N=10 = 90 runs / 季` 把研究實驗和 production gate 混在一起。G2 應該驗收「目前要擴權的 harness」，不是每季重跑 A/B/C。  
  **修法**：G2 基準改成 `3 tasks × current harness × N=10 = 30 runs`；只有比較候選 harness 時才乘以組數。

- **變異篇 §二 / review minutes**：你說前 3 份 warm-up 不計入，卻又說 Spearman 在 30 個 PR 上算。  
  **修法**：二選一：要嘛 30 全部進模型並控制 sequence index；要嘛明寫 Spearman n=27。

- **契約篇 §四**：`Spec 不可攜` 標題太大。2608.21208 支持的是 SQL 遷移情境下 Kiro spec 給 Gemini 讀崩掉，不支持所有 spec 都不可攜，也不支持 contract 一定可攜。  
  **修法**：標題改成「散文 spec 不可攜；契約可攜要自己量」。

**次要問題**
- **總論 §八 / 反模式 7**：2608.23550 是 `CLAUDE.md security rules`，不是一般 AGENTS.md conventions。  
  **修法**：只用來支持「安全規則寫進 Markdown 不等於 enforcement」，不要泛化成所有 conventions。

- **T1 註腳 [a]**：`pass rate 未報` 是 digest 未報，不一定是論文未報。  
  **修法**：改成「摘要未報 pass rate；待全文確認」。

- **P3-2 / 總論 §六**：壞變異有時寫三層，有時分類樹又拆成契約層、設計層、成本層。  
  **修法**：固定成三類：契約違規、設計分歧、成本後果；好變異另列，不算層。

- **規格篇 §六 / 契約篇 §六**：`spec-lint`、`drift-gate.yml` 都說 pseudo-config，但又叫 Reference implementation。  
  **修法**：要嘛提供可跑的最小 script；要嘛改名成「implementation sketch」。

**建議刪除**
- **總論 / hooks**：刪「沒人直接量過」「第一次直接量」。這會被 eval 圈抓爆。
- **總論 §四**：刪 12 月獨佔來源的三組數字。
- **變異篇 §七**：刪前代 model 迷你第四組，除非 10 月初已確認 model 可用且成本可控。
- **F8**：刪 2607.25141 的實點。
- **歷史類比**：刪 `2608.26197 = bit-for-bit` 這句。
- **規格篇 §一**：Dan North / Example Mapping / 四十條 Gherkin 壓到半節，否則又變 BDD 回顧文。

**建議補充**
- **變異篇 §二**：加 `Threats to validity`：單一 repo、單一 task、Java/Go 不一致、無 seed、tool/env nondeterminism、reviewer learning effect、作者選題偏差。
- **變異篇 §二**：加結果 CSV schema：`arm, run_id, model_id, harness_sha, test_exit, contract_violations, style_violations, similarity, jaccard, tokens, wall_clock, max_turns_hit, files_read, review_minutes, review_sequence`。
- **總論 §六 / 變異篇 §六**：補 N=30 最終判定表。現在只說「加跑到 N=30 再判」，沒說 30 次後紅黃綠怎麼算。
- **契約篇 §三**：補 `contract_surface:`，不要只靠 `implemented_by:`。否則任何 refactor 都會讓 drift gate 誤判。
- **整份 plan**：加一張「source audit table」：claim / source / domain / evidence level / article section。這會直接防止 domain-mismatched 引用。

<!-- tokens: in 833202 out 13679 -->
