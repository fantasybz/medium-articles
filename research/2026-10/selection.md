# 2026-10 期中加圈：12 月重切與 10 月的插入點

> 決定日期 2026-09-15。三個主題不變，這不是新的選題—本檔只記錄期中這一圈改了什麼。觸發有三：作者現場參加 **AGNTCon + MCPCon Japan 2026**（東京，2026-09-10–11，整合摘要 `research/2026-10/conference_digest.md`，逐場筆記 `.context/research/2026-09-conf/notes_sep10.md`、`notes_sep11.md`）；李博杰《深入理解 AI Agent：設計原理與工程實踐》**v2.0**（2026-09-06，Apache-2.0，`research/2026-10/book_ai_agent_book.md`）；第二模型對 2026-12 大綱的完整審查（2026-09-07 產出，`research/2026-09/codex-review-2026-12-sre-for-agents.md`，判定不合格）。**基準仍是 `research/2026-09/selection.md`**：三個月的主題、排序、落選候選與四條 12 月修正全部沿用，本檔只做增修。

---

## 1. 12 月改了什麼

主軸重切：從「把 harness 裝上儀表」改成 **flight recorder / accountability**。承重句是**「trace 是除錯用的，ledger 才是證據用的」**。改版後的大綱與圖檔在 `research/2026-10/2026-12-sre-for-agents.md` 與 `.figures.md`。

| 篇 | 改版前 | 改版後 |
|---|---|---|
| 總論 | 十二節；主軸「把 harness 裝上儀表」；F2 歷史 timeline 當骨架 | 十一節；刪 F2 與 timeline（與 9 月總論 §三重複）、新增 §七 tamper boundary、原 §七 + §八 合併、原 §十 規模併入 VP 決策；新封面 F14 |
| 觀測篇 | 六節；span 模型直接開場 | 七節；新增 §2 訊號可得性矩陣（G7，排在 span 模型之前）、§5 最小 reference implementation、§6 資料治理（G8）；刪 G3、G5；全篇 Tempo 一律改 Jaeger |
| 可靠篇 | 八節；三訊號 OR 定義成功；K8s 容量表一整節 | 七節；新增 §2 workflow evidence matrix（R6）、§5 SLI → action（R7）；刪 R5；六個 SLI 每列加 `min_events`；change acceptance 降為 lagging gate；`harness.lock` 收進 `agent-slo.yaml` |
| 應變與追責篇 | 七節；標題掛 incident response；attestation 讀 trace | 六節且順序重排（證據能不能信排在出事怎麼辦之前）；新增 §2 tamper boundary（I6）；標題改掛 tamper boundary；attestation 真值換成 event ledger + GitHub review event |

**三個工件（本月不交付第四個）**：A1 觀測篇的 trace schema + OTel Collector config；A2 可靠篇的 `agent-slo.yaml`；A3 應變與追責篇的 ledger-backed attestation status check（≤ 50 行的 `attest verify`）。runbook 範本、postmortem 範本、K8s fleet 容量表一律降為文中示意 + backlog。

**時程**：9/19–9/30 定規格、補證據由 15 項砍到 8 項；10 月整月做儀表化與 28 天 revert 基線；10/15–11/05 寫應變與追責篇與觀測篇、11/06–11/20 可靠篇、11/21–11/30 總論；12/01 總論 → 12/04 → 12/08 → 12/11。**硬性退場條件**：10/31 沒跑出真實 run trace 與可查詢的 ledger，12 月降為三篇。

**第二模型的 36 項（致命 6／重要 12／次要 5／建議刪除 6／建議補充 7）全部採納，零項駁回**，其中五項改了做法：

| 項目 | 處置 | 一句話理由 |
|---|---|---|
| tamper boundary 放可靠篇 §6 | 改落點 | 它是 flight recorder 能成立的前提，拆成總論 §七（概念）＋應變篇 §2（四條可驗規則），不另開第三處 |
| EU AI Act 放觀測篇資料治理表 | 改落點 | 時間差只落應變篇 §5，治理表加一行指過去，避免同一事實兩處 |
| `min_events` 三個來源不一致 | 採 Codex 換算 | SE ≤ budget/3 → 170 / 300 / 170；會議地圖的 200 與 arXiv 地圖的 30 作廢，分歧記進 open questions |
| 圖號 R2c / R6 / G7 | 改編號 | 統一成 R6、R7、G7、G8，四份地圖對得起來 |
| AgentLogs 的用法 | 依建議刪除 #5 | 全系列不得再寫「最大」與「拿來練 dashboard」，只留「可以對照規模的公開遙測資料集」 |

**新的錨點**（東京場次與書章，只列進正文的）：

| id / 章節 | 內容 | 落點 |
|---|---|---|
| `2QlDa` slide 35 | MCP proxy 的單一結構化事件 schema，含 `fault_domain` 與 `exclude_from_error_rate` | 觀測篇主 schema |
| `2QlEG` p.24 | 日立參考實作的 who-vs-why 缺口，與 orders were sometimes placed despite unmet terms or approvals | 總論 §三、應變篇 |
| `2So56` slides 2 / 10 / 13 / 18 | 103 session 的 23.5 turns、6/6 成品對 vs 5/6 session 成功、`rm -f events.jsonl -> blocked` 卻在道歉、semconv 連 denied vs failed 都表達不了（verified 2026-08-31） | 總論 §五、觀測篇 §3 |
| `2QsV2`、`2RaW6`、`2QsUJ` | Gilbert 的 harness 定義與「we don't talk about agentic AI evaluations」；AAIF 會員 269 家 / 14 sectors（organiser-reported）；新設 agents accountability WG | 總論 §二 |
| `2QlDI` slide 14、`2QlDv` slide 17 | Uber 每月約 9,000 份 RCA；heavy approval flows get skipped under stress | 總論 §三、§十 |
| `2VRYC` | A writable log can be altered or deleted；五條對抗性驗收測試 | 總論 §六、應變篇 §3 |
| 書 ch.1 §1.2 | Agent = Model + Harness，harness 的邊界與 Verify 規則 | 總論 §五書錨段 |
| 書 ch.7 Exp 7-6 | 52 筆真實失敗裡 24 筆自稱完成卻被 verifier 否決 | 總論 §五（全系列唯一帶書數字處） |
| 書 ch.10 §10.5 | 多 agent 的拜占庭故障 | 總論 §五 |

---

## 2. 10 月四篇要插什麼

10 月四篇的稿子已經寫好，這一圈**不重寫**。可以插入的十五處列在 `conference_digest.md` §4 的表裡：每一列都標了文章、章節原文標題、要加的那一句、來源 id 與投影片號，十一列是既有段落裡加一句、四列是延長既有表格，沒有一列需要重畫圖。規則只有一條—**插入只補證據，不改作者的行文**：新增的句子接在原句之後，不動論點順序、不換標題、不替換既有數字；沒有一手來源或只能二手轉引的，整列不用（該節另記了兩列被否決的理由）。

---

## 3. 11 月的備忘（本圈不動大綱）

`conference_digest.md` §5 與書的 ch.7 / ch.2 有一批材料該進 11 月，這一圈只登記、不改檔：

- 「same prompt, same model, same harness，兩次結果完全不同」是現場講出來的（`2VPr7` slide 2），而且**同一份規格的 run-to-run 分布，全場沒有一位講者報過**—這是 11 月的第一手空位，但也要誠實說出沒人發表的原因。
- 唯一一個量出來的變異預算：三次重試 1st 86% / 2nd 99%（`2TjiE` slide 18）。
- 「縮小 decision surface」是五個講者各自的答案（`2VPr7`、`2WF5N`、`2RCwp`、`2QlDC`、`2QlDg`），正好支持 9 月已採納的修正「變異在 loop，不在 spec」。
- 方法學警告要照抄：一個 model 一場、stopping rule 未標準化、五個條件同時變動（`2So56` slides 8 / 9 / 17）。
- 書 ch.7 §7.2 的 Pass@k 與 Pass^k 公式（p=0.6、k=5 → 99.0% vs 7.8%）與 §7.7 的 SE ≈ √(p(1−p)/n)（n=100、p=0.70 → ±9pp）；ch.2 的 KV cache 與狀態欄則是「變異來自 loop 的哪一段」的機制解釋。

---

## 4. 這一圈的限制

9 月兩位評審對 12 月的四條修正**原封不動繼續綁**：可靠篇只留一個工件；K8s sandbox fleet 不超過一段並標明是 1,000 人規模的問題；不引 Claude Taiwan 的席位抱怨當需求證據；排在 12 月，等 10、11 月的交接量出來。另外三條仍然成立：不得停在 2025 兩篇觀測文的 model-call 層、不得重講已發布四篇與 10 月四篇、Google 的「Agent Ops」要正面點名。

東京推翻或修正了三件事。其一，9 月寫的「這題現在沒人在講」要改口—AAIF 已經有 observability WG 與新設的 agents accountability WG，講的卻多半是 vendor 自家 gateway 內的觀測；真正還空著的是中文，以及你自己 harness 這一層。其二，「規格已有 `invoke_agent` / `execute_tool`」不能再寫，落地名一律 `org.*`，動筆前依 2026-11 版規格再查一次。其三，東京的數字幾乎都是 organiser-reported、vendor-reported 或 team-reported，每一處都要標出自報身分，不得當成第三方量測；Reuters / Engadget 與 Grok outage 一律不進正文，也不進 References。
