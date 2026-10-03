# 全文證據審查：變異篇第一輪

審查時間：2026-09-25T05:50:49.675016+00:00。審查者：Codex 獨立 evidence lens。

**判定：變異篇需修訂；系列尚未完成審查。** 本輪有 0 項 blocker、2 項 major、4 項 minor。正式數字與主要分母均吻合；問題集中在 AST 解讀、A3 的統計推論，以及幾處範圍或狀態用語。

完整閱讀變異篇 1–230 行；其他三篇尚未審查。僅審查及寫入本報告，未改動正文、凍結資料、論文或舊文。

## 正文版本與審查範圍

| 篇別 | 狀態 | SHA-256 |
|---|---|---|
| overview | NOT_REVIEWED；沒有完整 article.md，尚未審查 | `—` |
| spec | NOT_REVIEWED；沒有完整 article.md，尚未審查 | `—` |
| contract | NOT_REVIEWED；沒有完整 article.md，尚未審查 | `—` |
| variance | REVISE；已讀第 1–230 行 | `10f2baf37137360f244a133ccca05f3f982ae828ac256188df3dcf433428b1e4` |

變異篇為 36,118 bytes。所有位置與引句均對應上表 SHA-256；主代理修稿後須重新核對。本輪沒有根據大綱、部分正文或 raw response 的思考內容宣稱四篇已審。

報告落檔前，偵測主代理已開始修訂正文；新版 SHA-256 為 `ce383be20445328cec4a509e8ce7f519b94e9fe99b2fd927e494ffc4661c3587`。新版尚未複核，本報告的問題與判定仍只對應上表第一版。

## 需要修正的問題

### EV-001 · major · 節點分布不能證明每份候選保留了大量原始骨架

位置：[變異篇 article.md](</Users/kochi.chuang/conductor/workspaces/medium-articles/surabaya-v1/2026-11-same-spec-variance/article.md:118>)，第 118 行。

> 另一方面，候選相對 seed 的 cosine 最低也有 0.9499，表示每一份都保留了大量原本的骨架。單檔修補共用同一份 seed 時，出現這種情形可以預期，這也是組內相似度偏高的來源之一。

數值正確，但推論超出指標。node-type cosine 只比較各種節點的數量，不比對原始程式碼片段、樹的排列或控制流程。高 cosine 不能證明保留多少原始骨架，也沒有識別共同 seed 對組內相似度的因果效果。前句對修改方向保留了「可能」，這兩句卻把同樣未量測的解釋寫成事實。

證據：

- [research/experiments/same-spec-ten-runs/results/formal-2026-09-25/source/analyze.py](</Users/kochi.chuang/conductor/workspaces/medium-articles/surabaya-v1/research/experiments/same-spec-ten-runs/results/formal-2026-09-25/source/analyze.py:314>)（第 314–338 行）：ast.walk 後只以 Counter(type(node).__name__) 建向量，再計算 cosine；沒有共用程式碼比對。
- [research/2026-10/2026-11-same-spec-ten-runs.figures.md](</Users/kochi.chuang/conductor/workspaces/medium-articles/surabaya-v1/research/2026-10/2026-11-same-spec-ten-runs.figures.md:206>)（第 206 行）：現行圖說只寫共同 seed 可能造成高 cosine；未扣除共用程式碼或校正因果關係。
- [research/experiments/same-spec-ten-runs/RESULTS.md](</Users/kochi.chuang/conductor/workspaces/medium-articles/surabaya-v1/research/experiments/same-spec-ten-runs/RESULTS.md:31>)（第 31–33 行）：正式結果將共用 seed 列為可能原因，並明說忽略順序與許多語意差異。

具體修正：候選相對 seed 的 cosine 最低也有 0.9499，表示節點類型的數量比例仍然接近。共同 seed 可能是組內相似度偏高的原因之一，但本輪沒有逐段比對保留了多少原始程式碼；seed 參照也沒有扣除或量出這個影響。

### EV-002 · major · 把未能區分的分數差異寫成真實增益，並跨指標斷言偵測能力

位置：[變異篇 article.md](</Users/kochi.chuang/conductor/workspaces/medium-articles/surabaya-v1/2026-11-same-spec-variance/article.md:173>)，第 173 行。

> 在那份研究中，增益藏在比通過率更細的分數裡，仍被重新執行的變動淹沒。本輪的主要結果是更粗的二元通過結果，每組只有十次，而且全部頂到上限。即使四份 packet 之間有類似大小的差異，這份資料也沒有能力看見。

A3 問的是觀察到的 paired composite score 差異是否來自文件效果或重新執行；p 值未達門檻不能決定真實增益已存在、只是被噪聲淹沒。其約 4.9 個百分點的 composite 差異，也不能直接搬到本輪的二元驗收結果，作為已評估的偵測能力。L171 原本已正確區分，L173 的延伸卻越過這個界線。

證據：

- [research/2026-10/same-spec-ten-runs/evidence-audit.md](</Users/kochi.chuang/conductor/workspaces/medium-articles/surabaya-v1/research/2026-10/same-spec-ten-runs/evidence-audit.md:48>)（第 48–52 行）：4.9pp 是相對 0.5 的 paired composite score，不是 resolve rate；沒有任何 optimizer run 的 sign test 達 .05，不能把差異與 reroll noise 分開。
- [.context/same-spec-ten-runs/sources/2609.12742v1.txt](</Users/kochi.chuang/conductor/workspaces/medium-articles/surabaya-v1/.context/same-spec-ten-runs/sources/2609.12742v1.txt:181>)（第 181–183 行）：A3 §4.2 先報告 score 差異，再討論能否歸因於文件；可偵測範圍依該研究的配對 sign test 定義。
- [research/experiments/same-spec-ten-runs/results/formal-2026-09-25/source/PROTOCOL.md](</Users/kochi.chuang/conductor/workspaces/medium-articles/surabaya-v1/research/experiments/same-spec-ten-runs/results/formal-2026-09-25/source/PROTOCOL.md:124>)（第 124–127 行）：本輪只預定各組的區間，沒有組間 contrast、配對估計或假設檢定；也沒有可直接套用 A3 composite 效果大小的分析。

具體修正：那份研究觀察到分數差異，卻無法判定它來自文件效果還是重新執行的變動。本輪每組只有十次，二元驗收結果又全部頂到上限，同樣不足以據此主張四組等效。兩份研究的指標不同，不能把約 4.9 個百分點直接套成本輪可偵測的差距。

### EV-003 · minor · 「任何一對候選」擴大了實際計算的 pair 範圍

位置：[變異篇 article.md](</Users/kochi.chuang/conductor/workspaces/medium-articles/surabaya-v1/2026-11-same-spec-variance/article.md:116>)，第 116 行。

> 因此，任何一對候選之間的 cosine，都高於任何一份候選相對 seed 的 cosine。

本輪列出的是四組各 45 個組內 pair，合計 180 個。四十份候選的全部兩兩組合是 780 個，包含未列入凍結分析的 600 個跨組 pair。數值範圍不重疊的敘述適用於已計算的 180 個組內 pair，不能把限定省略成所有候選兩兩配對。這是範圍修正，不要求追加事後分析。

證據：

- [research/experiments/same-spec-ten-runs/results/formal-2026-09-25/source/analyze.py](</Users/kochi.chuang/conductor/workspaces/medium-articles/surabaya-v1/research/experiments/same-spec-ten-runs/results/formal-2026-09-25/source/analyze.py:417>)（第 417–425 行）：先以 arm 分組，再對同組 parsed artifacts 使用 itertools.combinations(parsed, 2)。
- [research/2026-10/2026-11-same-spec-ten-runs.figures.md](</Users/kochi.chuang/conductor/workspaces/medium-articles/surabaya-v1/research/2026-10/2026-11-same-spec-ten-runs.figures.md:193>)（第 193–195 行）：F2 上圖只有組內 180 個值；下圖是相對 seed 的 40 個值。

具體修正：在本次計算的 180 個組內 pair 中，每一個 cosine 都高於這 40 份候選各自相對 seed 的 cosine。

### EV-004 · minor · 表格被描述為逐層前提，與兩個完成欄位的定義矛盾

位置：[變異篇 article.md](</Users/kochi.chuang/conductor/workspaces/medium-articles/surabaya-v1/2026-11-same-spec-variance/article.md:47>)，第 47–59 行。

> 下表依序列出四組名額的流向，每一列都是下一列的前提：

cli_success 並不是 artifact_success 的必要條件；研究方案明確保留 CLI 未完成、產物驗收卻合格的情形，L59 也有正確說明。表格最後的失敗計數更不是下一層成功流程。這句把平行記錄的兩個判定重新寫成淘汰漏斗。

證據：

- [research/experiments/same-spec-ten-runs/results/formal-2026-09-25/source/run_study.py](</Users/kochi.chuang/conductor/workspaces/medium-articles/surabaya-v1/research/experiments/same-spec-ten-runs/results/formal-2026-09-25/source/run_study.py:352>)（第 352–386 行）：先記錄 CLI 是否成功，仍可擷取並評測產物；artifact_success 取 evaluator 的 passed，accepted_completion 才是兩者的 AND。
- [research/experiments/same-spec-ten-runs/RESULTS.md](</Users/kochi.chuang/conductor/workspaces/medium-articles/surabaya-v1/research/experiments/same-spec-ten-runs/RESULTS.md:9>)（第 9–18 行）：主要結果是兩者皆成立，另列 CLI × artifact 四格計數。

具體修正：下表把排定名額、兩個分開記錄的完成判定，以及最終交付結果放在一起；主要結果要求 CLI 完成與候選驗收兩項均成立。刪除「每一列都是下一列的前提」。

### EV-005 · minor · 單檔不代表只能用 AST 觀察實作差異

位置：[變異篇 article.md](</Users/kochi.chuang/conductor/workspaces/medium-articles/surabaya-v1/2026-11-same-spec-variance/article.md:122>)，第 122 行。

> 本輪是單檔修補，檔案數不會改變，所以差異只能在 AST 層次看見。

檔案數固定只能說該指標在本輪不會變，不能排除原始程式碼行數、文字差異或其他檔內描述。AST 是本輪預先選定的描述方法，並非單檔任務唯一可用的觀察層次。

證據：

- [research/experiments/same-spec-ten-runs/results/formal-2026-09-25/source/PROTOCOL.md](</Users/kochi.chuang/conductor/workspaces/medium-articles/surabaya-v1/research/experiments/same-spec-ten-runs/results/formal-2026-09-25/source/PROTOCOL.md:133>)（第 133–140 行）：研究方案預先選定 normalized AST hash 與 node-type cosine 來描述候選，並未主張其他檔內描述不可使用。
- [research/2026-10/same-spec-ten-runs/evidence-audit.md](</Users/kochi.chuang/conductor/workspaces/medium-articles/surabaya-v1/research/2026-10/same-spec-ten-runs/evidence-audit.md:36>)（第 36–37 行）：A2 同時列 source files、source lines 與 CSS 行數，這些是體積代理指標；檔案數固定不會使其他量測消失。

具體修正：本輪是單檔修補，檔案數固定，因此事先改用兩種 AST 描述來觀察檔內差異。

### EV-006 · minor · 草稿頁尾把尚未發布的文章寫成已發表

位置：[變異篇 article.md](</Users/kochi.chuang/conductor/workspaces/medium-articles/surabaya-v1/2026-11-same-spec-variance/article.md:230>)，第 230 行。

> *本文發表於 [Medium @fantasybz](https://medium.com/@fantasybz)。若你也在用重複執行檢查 agent 的產出，歡迎交流。*

本篇目前是主寫完成、待修訂的本機草稿，沒有本篇發布紀錄。系列導覽已正確標為即將發布；頁尾卻使用已發表語氣。這個範本句要配合目前的狀態。

證據：

- [2026-11-same-spec-variance/article.md](</Users/kochi.chuang/conductor/workspaces/medium-articles/surabaya-v1/2026-11-same-spec-variance/article.md:5>)（第 5 行）：本稿將其他篇標為即將發布；本次只有變異篇完成全文 evidence lens。
- [2026-11-same-spec-variance/publish/PUBLISHED.md](</Users/kochi.chuang/conductor/workspaces/medium-articles/surabaya-v1/2026-11-same-spec-variance/publish/PUBLISHED.md>)（審查時不存在）：審查時不存在本篇發布紀錄；主代理亦明確表示系列仍在主寫與修稿階段。

具體修正：發布前先移除「本文發表於」一句，或改成「本系列預計於 Medium @fantasybz 發布」。待實際發布並確認網址後再改回已發表語氣。

## 已核對且不需追加警語的項目

| 編號 | 核對位置 | 結果 |
|---|---|---|
| C01 | L3、L11、L30–41、L51–59：名額、執行設定與完成數 | 40 個正式名額，A0／A／B／C 各 10；generation high，CLI 2.1.282；2 次 pilot 與 4 次停止 probe 排除。40 筆 cli_success、artifact_success、accepted_completion 皆為 true；無 timeout、operational error 或 boundary violation。 |
| C02 | L61–63：區間與可推論範圍 | 10/10 的雙側 95% Clopper–Pearson 下界重算為 0.025^(1/10)=0.6915028921812392；69.15%–100% 正確。稿中已交代共同成功機率與獨立性假設、無等效或勝負判定。 |
| C03 | L65、L75–85：103 項有限覆蓋與分母 | 40 份 evaluation.json 各有 103 項、失敗 0，合計 4,120 項；102 batch＋1 EOF 前 streaming probe。重評是同一批產物，未冒充新生成樣本。main()、額外 CLI 參數與內部編碼等未涵蓋處已說明。 |
| C04 | L65–69：重評、獨立資料稽核與隔離 | public-rescore.json 記錄 40 份皆相符；formal-data-audit.json 為 1,903／1,903，317 份公開檔案與 40 份投影的描述吻合。三項 Seatbelt 拒絕 probe 有限於本機設定，沒有宣稱完整 OS 隔離。 |
| C05 | L95–114、L120：AST 定義、表格、相依性 | 重算四組各 45 個 pair 與 10 個 seed 值的中位數、極值及 hash 種類，全部與表格四位小數相符。1 表示計數向量比例相同；hash 不判定語意等價；180 個 pair 非 180 個獨立 run。L116、L118、L122 的延伸另列問題。 |
| C06 | L99–110：F2 圖檔與圖說 | 已開啟正文引用的 F2.png；兩個 panel 均保留 0–1 橫軸。本文圖檔與正式工件 SHA-256 同為 474f4ae875dcababaf7ffcddf501b2b7c49fa5d9ed0e80a4ac9a57a98f9084fb。 |
| C07 | L134–151：耗時、費用與 usage | 從 40 筆 ledger 重算各組耗時與費用的中位數、極值、合計，以及四類 usage，均與正文相符；總費用 5.692342。牌價估計與帳單、輪詢精度、cache 分類、Haiku 計費用途未知等界線正確。 |
| C08 | L17–26、L81：基底缺陷與規範 | 已核對 baseline 重現及 R01–R13。非物件 root 造成 AttributeError、text=123 被舊程式印出且 exit 0、malformed 修補後 exit 6、3→6→4→5→0 優先序均正確。L81 對原 seed 無法符合 exit 6 案例明標推論，未冒充新測試。 |
| C09 | L122、L216：A2 引用版本與限制 | 引用固定 v2 PDF 的 Table 9；Opus 4.7 xHigh base 6 次皆 42 分、source files 15–22 正確。此 42 分表示 14 criteria 首次檢查便全數合格；一般最終分數允許修正後取得部分分數。正文已限單 task、非盲 evaluator 與體積 proxy，沒有把 N=90 寫成單組態樣本。 |
| C10 | L145、L217：A1 成本離散度 | Kimi K3、mini-swe-agent、5 個 SWE-bench Verified tasks、同 specification／effort 15 repeats、geometric SD 中位數 ×1.34 均與 v1 來源吻合。未將成本變異寫成 AST 變異。 |
| C11 | L169–171、L218：A3 數值與計分定義 | 3 個 Kotlin repos；20、26、23 個 held-out tasks；paired composite 的 seed 基準 0.5、GEPA 約 +4.9pp、最佳 sign-test p=.29 均正確。L173 對此結果的延伸另列 EV-002。 |
| C12 | L175、L219：A5 核心研究與限制 | 24 tasks、18 variants、4,644 valid runs 屬核心研究；未與 harness extension 或 hard-task campaign 混算。effort × harness 的介入差異與小任務、架構任務覆蓋不足的限制均吻合。 |
| C13 | L153–155、L220：舊文承接與公開網址 | 成本分母敘述與營運篇第 113 行一致；該篇有已發布及 2026-09-25 00:42 GMT+8 重新發布紀錄。未將 green 系列排程稿寫成已發布。 |
| C14 | L165、L177、L226：模型、真人與研究／寫作分界 | 研究 generation high 與 Claude Code 初稿 max 分開，設計審查 xhigh 未混入正式名額；沒有真人審稿、校準、review 計時或外部重現的說明清楚。 |
| C15 | 全文：主要結論的尺度 | 未宣稱首次量結構、原生 Skill 效果、四組等效、成本 ROI 或 production 授權門檻。未因零失敗省略名額，也未把作者來源核對寫成重現論文 artifact。 |

## 書目與狀態的額外核對

A2 以版本化 PDF 為準。題名為 *Reasoning effort, not tool access, buys first-try reliability in agentic code generation: Evidence from 90 matched agent runs*，作者 Achint Mehta。PDF 為 43 頁，SHA-256 `4c80ac39360e3141df3b6b000823d2b07e92b1e79702a03b24bb35c393fe874d`。版本化及未版本化摘要頁仍使用 *an observational study* 的副標與 22 頁註記；本稿以 arXiv ID 及 [v2 PDF](https://arxiv.org/pdf/2607.02436v2) 引用，未混入摘要頁的題名或頁數。這項版本界線已符合要求，不另列缺漏。

營運篇的成本分母承接可保留：[舊文原段落](</Users/kochi.chuang/conductor/workspaces/medium-articles/surabaya-v1/2026-11-agentic-eval-economics/article.md:113>)，[重新發布紀錄](</Users/kochi.chuang/conductor/workspaces/medium-articles/surabaya-v1/2026-11-agentic-eval-economics/publish/PUBLISHED.md:66>)。本次 Medium 讀取遇 Cloudflare 403，沿用已核對 ledger，不宣稱重新讀取了公開全文。green 系列仍是排程，本稿沒有將它寫成已發布前文。

## 核對方法與可重做性

直接讀取正式 records.jsonl 與 summary.json，重新計算四組名額、完成旗標、CI 下界、費用與耗時的中位數及極值、usage 合計、AST pair 與 seed 摘要；另外讀取 40 份 evaluation.json，確認各 103 項且失敗數為 0。正文 F2.png 已視覺檢查，並確認與正式圖檔 hash 相同。沒有執行候選、重新生成資料或擴增跨組 pair 分析。

| 來源 | SHA-256 |
|---|---|
| [research/experiments/same-spec-ten-runs/RESULTS.md](</Users/kochi.chuang/conductor/workspaces/medium-articles/surabaya-v1/research/experiments/same-spec-ten-runs/RESULTS.md>) | `8b82472ec00144a60803882273804295de236faa67176f91c6ca72e30ea251a3` |
| [research/experiments/same-spec-ten-runs/requirements.json](</Users/kochi.chuang/conductor/workspaces/medium-articles/surabaya-v1/research/experiments/same-spec-ten-runs/requirements.json>) | `32e0a0af2578564624b5a5b5f9d981e0dc296e6eb690b6598482cb809419a515` |
| [research/2026-10/2026-11-same-spec-ten-runs.figures.md](</Users/kochi.chuang/conductor/workspaces/medium-articles/surabaya-v1/research/2026-10/2026-11-same-spec-ten-runs.figures.md>) | `f0d3ff8e49fb5aba841519edc0782d91ed9fd0caf88c9a9492b1f491a238812a` |
| [research/2026-10/same-spec-ten-runs/evidence-audit.md](</Users/kochi.chuang/conductor/workspaces/medium-articles/surabaya-v1/research/2026-10/same-spec-ten-runs/evidence-audit.md>) | `e165f88daf73e3c4ed9fb94b697767f1197a03ceec105049018771aa1648eb86` |
| [research/experiments/same-spec-ten-runs/results/formal-2026-09-25/source/PROTOCOL.md](</Users/kochi.chuang/conductor/workspaces/medium-articles/surabaya-v1/research/experiments/same-spec-ten-runs/results/formal-2026-09-25/source/PROTOCOL.md>) | `94af80dc28a933e18e03c53deb088b9a22161c1d39c296a929efcef3ed977a58` |
| [research/experiments/same-spec-ten-runs/results/formal-2026-09-25/source/analyze.py](</Users/kochi.chuang/conductor/workspaces/medium-articles/surabaya-v1/research/experiments/same-spec-ten-runs/results/formal-2026-09-25/source/analyze.py>) | `c5df73abb76fb4b36bfb63325524419f80ad1b4c7755f2036d8291ca086cb585` |
| [research/experiments/same-spec-ten-runs/results/formal-2026-09-25/source/run_study.py](</Users/kochi.chuang/conductor/workspaces/medium-articles/surabaya-v1/research/experiments/same-spec-ten-runs/results/formal-2026-09-25/source/run_study.py>) | `2d0bd4bb0b0f02a9f12694fcf6867b8e663645cf943dc45f71f1fbfcaf6bfac8` |
| [research/experiments/same-spec-ten-runs/results/formal-2026-09-25/manifest.json](</Users/kochi.chuang/conductor/workspaces/medium-articles/surabaya-v1/research/experiments/same-spec-ten-runs/results/formal-2026-09-25/manifest.json>) | `ba30398118ecde62b2f682884c1e882b2864c22d70faf99549ceab0d7c0a55f2` |
| [research/experiments/same-spec-ten-runs/results/formal-2026-09-25/records.jsonl](</Users/kochi.chuang/conductor/workspaces/medium-articles/surabaya-v1/research/experiments/same-spec-ten-runs/results/formal-2026-09-25/records.jsonl>) | `2be5ed458de2e2defa2ab4f24d88f25bdd3b7340c9207915ab6aa0988c0db7f0` |
| [research/experiments/same-spec-ten-runs/results/formal-2026-09-25/summary.json](</Users/kochi.chuang/conductor/workspaces/medium-articles/surabaya-v1/research/experiments/same-spec-ten-runs/results/formal-2026-09-25/summary.json>) | `8198a4478b8158268298960576655d920db3b8d2dc2bd207348dcef8a346dfb9` |
| [research/experiments/same-spec-ten-runs/results/validation-2026-09-25/public-rescore.json](</Users/kochi.chuang/conductor/workspaces/medium-articles/surabaya-v1/research/experiments/same-spec-ten-runs/results/validation-2026-09-25/public-rescore.json>) | `83c55e0b00bacf039210ad5247a8f9eefde341ba650a75c2b65412afe6ebf258` |
| [research/experiments/same-spec-ten-runs/results/validation-2026-09-25/formal-data-audit.json](</Users/kochi.chuang/conductor/workspaces/medium-articles/surabaya-v1/research/experiments/same-spec-ten-runs/results/validation-2026-09-25/formal-data-audit.json>) | `e66b551ccd89f7f0709a8be9ce060214fbfbf07ad4ab75ef634a00bfff2e82a8` |
| [.context/same-spec-ten-runs/manuscripts/recall-source-check.md](</Users/kochi.chuang/conductor/workspaces/medium-articles/surabaya-v1/.context/same-spec-ten-runs/manuscripts/recall-source-check.md>) | `4f124fd1f9f90ba9f8e161018902fe21c45391fcc5a9cb83906e85a4272473e4` |
| [.context/same-spec-ten-runs/sources/2607.02436v2.pdf](</Users/kochi.chuang/conductor/workspaces/medium-articles/surabaya-v1/.context/same-spec-ten-runs/sources/2607.02436v2.pdf>) | `4c80ac39360e3141df3b6b000823d2b07e92b1e79702a03b24bb35c393fe874d` |
| [.context/same-spec-ten-runs/sources/2608.25399v1.txt](</Users/kochi.chuang/conductor/workspaces/medium-articles/surabaya-v1/.context/same-spec-ten-runs/sources/2608.25399v1.txt>) | `4b91f67f074a10527e52be6fb52e6f9a38c6dfb4566a9974530e2ee1ed47704e` |
| [.context/same-spec-ten-runs/sources/2609.12742v1.txt](</Users/kochi.chuang/conductor/workspaces/medium-articles/surabaya-v1/.context/same-spec-ten-runs/sources/2609.12742v1.txt>) | `b518238c52b31f63458bc9e2724884aba8e169881543b354c9509580f8dda501` |
| [.context/same-spec-ten-runs/sources/2608.01347v6.txt](</Users/kochi.chuang/conductor/workspaces/medium-articles/surabaya-v1/.context/same-spec-ten-runs/sources/2608.01347v6.txt>) | `a9af7ff769f41dff35eefe37d4bcdad7efdb88487ca166670192c0f341c91ad5` |

逐項資料、完整重算數值及問題欄位見 [review-evidence.json](</Users/kochi.chuang/conductor/workspaces/medium-articles/surabaya-v1/research/2026-10/same-spec-ten-runs/manuscripts/review-evidence.json>)。

下一步：先修正上述六項，再以新稿 SHA-256 複核；其餘三篇須等完整正文出現後補審。這份報告不是系列 READY，也不是真人審稿或論文重現。
