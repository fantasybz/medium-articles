# 2026-12 英文版與發布推廣：把 Agent 當 Production Workload—Agent 的 SRE

主計畫在 **`research/2026-10/2026-12-sre-for-agents.md`**（§5 英文版與推廣、§6 發布 各留一行指標指到這裡）；本檔收主計畫交出來的全部推廣工作—英文版、Medium topics、封面圖、上線與分發時程、四個平台的貼文，以及社群回收。

> 建檔於 2026-09-16，內容取自 `research/2026-09/2026-12-sre-for-agents.md`（重切前的 §5 英文版注意事項、§6 發布與推廣），依 `.context/research/2026-10/dec-recut-plan.json` 的 tail 兩條（order 15、16）拆分。**主計畫只回答一個問題：四篇寫不寫得完、三個工件交不交得出來**；推廣的決定一律落在這裡。
>
> 本月承重句已換成 **trace 是除錯用的，ledger 才是證據用的**—所有對外文案以這句為準，不再賣「把 harness 裝上儀表」。重切刪掉的章節（證照敘事、歷史 timeline、F2 / G5 / R5）若還有文案在賣，見 §8 的作廢清單。

---

## 1. 英文版計畫

**英文版是固定交付**，四篇都要有；1:1 結構、不新增段落與來源（此條與主計畫 §5 同步）。

**title_en**：*Treat Agents as Production Workloads: SRE for Agents—Observable, Reliable, Accountable*。三篇：

- *Part 1 — What a Trace of One Agent Run Looks Like: Landing the OTel GenAI Semantic Conventions*
- *Part 2 — Agent SLOs: Six SLIs the Agent Can't Fill In, Buying Autonomy with Error Budget, and Managing the Harness as a Production Dependency*
- *Part 3 — When the Agent Breaks: Tamper Boundaries, Flight Recorders and "Who Approved This PR?"*—**Part 3 的英文標題本次改過**：中文篇名已由「incident response」改成「tamper boundary」，英文照改，不要沿用舊的 *Incident Response*。

**英文版 TL;DR 首句考慮用備用一**：*Nearly every SRE practice transfers to agents; the SLI does not, because the agent fills in its own SLI.*—重切後，這句要補上第二件重做的事（證據的存放），中文備用一已經是「SRE 的方法幾乎全部可以借，但兩件事要重做：SLI 的來源，與證據的存放」，英文首句照這個版本寫：*Nearly every SRE practice transfers to agents. Two things don't: where the SLI comes from, and where you keep the evidence.*

**關鍵詞四個不可動**（主計畫 §5 列的同一組，此處是唯一維護處）：

- *completion claim*（結案報告；**不用** closing report）
- *event ledger*（事件帳本）
- *behavioural tuple*（行為組態；沿用 2608.23610 的用語，第一次出現加一句 *the paper's tuple has seven components; the four columns here are a subset*）
- *tamper boundary*（防竄改邊界）

**其餘翻法固定**：傳聞 → *hearsay*；追責 → *accountability*（標題已定）；授權擴張 → *expanding autonomy*；儀表 → *instrumentation*；快訊號 / 落後 gate → *fast signal / lagging quality gate*（**舊稿寫 lagging budget，改**—change acceptance 在重切後是 lagging quality gate，不是 budget，英文寫成 budget 會直接牴觸可靠篇的立論）。`org.approval`、claimed / verified outcome、`accepted_risk`、intervention ratio、approval minutes、burn rate、`min_events`、rollback 一律不翻，兩版共用；PromQL、YAML 片段也兩版共用，不重打一份。

**英文讀者特別敏感的三處**（主計畫 §5 的同一份清單，這裡展開）：

1. **OTel 名詞照規格原文**，不翻；`invoke_agent` / `execute_tool` / `gen_ai.*` 與 `org.*` 擴充、以及「提給規格的名字」三類，英文版要分得比中文版更清楚—LinkedIn 的讀者裡有規格作者。落地名一律 `org.approval` 與 `org.approval.*`；提案名是不帶 org 前綴的 `human.approval`，第二個提案是 `org.tool.decision`。**這個順序在英文版只交代一次，不要在正文其他地方讓 `human.approval` 亂跑。**
2. **「Agent Ops」也是一家公司的名字**，英文版要多一句 *AgentOps the product is not what I mean*。命名對手重切後是三個—Google 的 Agent Ops、AAIF 的 agents accountability、筆者的 SRE—英文版的對比句要寫滿三個，不能只寫 Google。
3. **「probe 的位置要重做」要明講 black-box probe 那一章**，否則英文 SRE 讀者會覺得你不知道。英文讀者對 SRE book 很熟：error budget、SLO、burn-rate alerting 的章節名可以直接引、少解釋；反過來要多解釋的是 harness layer（連回 9 月 EN 版的定義）與 10、11 月的接口。

**書的引用形式**：見主計畫 §5 的同名條目（中／英兩種寫法與 Bojie Li 的一句出處說明，在那裡維護，本檔不複製）。

**台灣社群引用要加脈絡**：一位 Backend 台灣作者的貼文要說明「a Taiwanese backend community post on a Grafana + Claude Code AIOps bot」；Backend 台灣、DevOps Taiwan 各加一句是什麼；Claude Taiwan 不出現。Ramp 3/4 PR（@linear 2026-08-31）中文四篇正文一處都不用，**只有英文版要一句「有規模」的脈絡時才回頭取，且不進任何 References**。

**Kubestronaut / CNPE 一句話交代**：英文讀者不一定知道 Golden Kubestronaut 是什麼，加一句「the CNCF track of 15+ certifications」。**（原總論 §一 的證照敘事已刪，此則作廢**—12 月四篇英文版一個字都不提證照，這句留到 2027-01 的 interlude 再用。**）**

**Medium 數據提醒**：英文版帶 impression 不帶 read（2025 英文 8% 完讀 vs 中文 27%）。英文版的價值是 LinkedIn / KubeCon 圈的可發現性，所以**英文版一定要在 LinkedIn 發**，並 tag OTel GenAI SIG 相關人（keynote 講者全名確認後）。

**圖表**：英文版自己一套 PNG，1:1 結構；表格類（F3、F6、F7、R2a / R2b）英文可以更精簡，因為不用雙語對照。R2a / R2b 重切後各多一欄 `min_events`（5 欄），英文版跟著改；封面見 §3。

---

## 2. Medium topics

**五個**：Site Reliability Engineering、Observability、AI Agents、OpenTelemetry、Platform Engineering。

備選：Kubernetes、DevOps—若 Medium 只吃五個，優先保留前五。

---

## 3. 封面圖

**本月封面是 F14**（重切後改的，主計畫 §6 只留一行，決策記在這裡）：**兩個 store**—harness hooks 分兩條，Trace store（Jaeger、30 天、除錯用）與 Event ledger（append-only、hash chain、證據用）；ledger 再出兩條到 SLI / burn-rate 與 attestation status check；旁邊一個 bad class 節點「可寫的 log 當證據」標明反模式。8 節點，flowchart TB。它一張圖說完本月的承重句—trace 是線索、ledger 才是證據—比舊封面更貼這一版的主軸。**F14 的原始碼待補、尚未跑過 `research/scripts/mermaid_check.sh`**，交稿前補跑再出 PNG。

**F5 由封面降為內文圖**：一次 agent run 的 trace 樹—`invoke_agent` → 一個展開的 `org.step #k`（`gen_ai.*` → `execute_tool` → `org.approval` 直排）+ 收合的 #1 與 #N，每個節點寫 span 名 + 一行來源。6 節點、實測 629×623、高／寬 0.99，在 FB 縮圖上看得出是一棵樹—**縮圖表現仍然是全系列最好的，若 F14 跑出來的尺寸在 FB 上糊掉，退回 F5 當封面**。注意 F5 的 approval 節點已改標 `org.approval`，舊 PNG 不能直接拿去用。

**備選**：F3 的 SRE ↔ Agent 對照表（對 SRE 讀者更有感，但縮圖上文字太小）。

---

## 4. 上線與分發時程

中文四篇的時程、寫作順序與硬性退場條件在**主計畫 §6**，這裡不重抄。本檔只管上線之後的事：

- **上線窗口 12/1–12/12**，四篇順序不變：12/01 總論 → 12/04 觀測篇 → 12/08 可靠篇 → 12/11 應變篇。
- **英文版**：總論 EN **12/02**；三篇 EN **12/15–12/18** 集中發（本月刻意把英文版壓到中文四篇全部上線之後；9 月是隔兩天就發 EN，這次不照那個做法）。
- **原則（主計畫 §5）**：中文版全部上線之後再處理英文版與社群分發。**總論 EN 的 12/02 是這條原則唯一的例外**，沿用舊稿「英文版隔天」的做法；要嚴守原則就把它移到 12/12 之後，見 §9。
- 11 月的「我的 Golden Kubestronaut 之路」interlude 若與 CNPE 結果撞期，順延到 2027-01；**12 月不排**，正文不因此改一個字。

---

## 5. 發布順序

社群 digest 的結論：**粉絲團分享的那一週，才是 views 超過 impressions 的一週**。順序照這個排：

1. **總論發布當天**：粉絲團貼文 + LinkedIn（英文版隔天）。
2. **隔天**：DevOps Taiwan（觀測 / SLO 角度）與 Backend 台灣（回應一位 Backend 台灣作者那篇的角度—**先私訊**，引用同意還沒拿到，見 §9）。
3. **觀測篇發布時**：Grafana & Friends Taipei 相關貼文 / CNCJ 或 CNCF Taiwan 的社群；LinkedIn 在英文版上線時再發一次，tag OTel GenAI SIG。
4. **應變篇發布時**：Backend 台灣（該群對事故分析文的分享數最高，兩則指標貼文見 `community_digest.md`）。

---

## 6. 貼文草稿

### FB 粉絲團 hooks（三則，用作者的自嘲口吻）

**三則 FB hook 留在主計畫 §6**（`dec-recut-plan.json` tail order 16 指定 FB hook 不搬出主計畫），本檔不留副本—要改就改 `research/2026-10/2026-12-sre-for-agents.md` §6 那三則。

**舊版三則（2026-09-05 稿）留作紀錄**：總論舊版結尾是「Kubestronaut 大叔終於寫回自己的地盤了」—**（原總論 §一 證照敘事已刪，此則作廢）**；觀測篇舊版寫「幾十次 model call、幾百次 tool call、幾次人按 approve」，已被有真實數字的版本取代；應變篇舊版用「47 個 CI/CD 與 agent 平台，0 個預設會…」，那個數字沒有作廢（仍在應變篇追責那節），只是 FB 這一則改用東京現場更有畫面的材料。

### X hooks（英文，每篇一則）

- **總論（本次重寫）**：「An agent's completion claim is not evidence. Neither is the trace—that's a debugging clue, and it expires in 30 days. The evidence is an append-only ledger the agent cannot reach. Nearly every SRE practice transfers to agents; two things don't—where the SLI comes from, and where you keep the evidence. Google calls this Agent Ops, the foundation calls it agents accountability; I call it SRE, because the name decides which ten years of practice you get to borrow. New series: SRE for agents.」
  - 舊版只點名 Google 一個命名對手，也還停在「trace 才是證據」的舊脊椎—**重寫，不是作廢**：§二 那一節還在，只是對手從一個變三個，而且 trace 在本版已經降級成線索。
- **可靠篇（沿用，未改）**：「Six SLIs the agent can't fill in. Autonomy isn't granted; it's bought with error budget. And your harness is a production dependency—same model, same task, fail-to-pass 28% → 49% by changing only how the harness trims tool output. Pin it, diff it, canary it. Part 2: the agent-slo.yaml.」
  - 28% → 49% 重切後是**總論 §八的 headline**，可靠篇 §6 接完整證據鏈。「每個數字只落一處」是正文的紀律，不約束貼文，這則照用。
- **應變篇（沿用，未改）**：「0 of 47 CI/CD and agent platforms emit a content-addressed identity of what actually ran, by default. 'Who approved this PR?' should be a span and a status check that reads the trace, not the PR body—and not a forensic exercise.」
  - 兩點微調再發：篇名已改成 tamper boundary，結尾的 *reads the trace* 要改成 *reads the ledger*（CI 對的是帳本，不是三十天就過期的 trace）。想換一句更有現場感的就用可引用的一句話備用三：*The model could not observe the outcome of its own blocked call.*

### LinkedIn（英文版主戰場）

一則長貼文：

- **開頭**用 KubeCon + CloudNativeCon Japan 2026 的 keynote（Alolita S.，OTel GC，GenAI semantic conventions for observing agentic systems）與 OTel GenAI conventions 現況—**講者全名、講題原文與錄影／投影片連結確認後 tag 本人**。
- **主體**明說本系列的姿態：**照用規格的 `invoke_agent` / `execute_tool`，規格沒有的先落 `org.*`**—實作、YAML、status check 與所有圖表一律寫 `org.approval`，一個例外都沒有；**提給規格時才用不帶 org 前綴的 `human.approval`**，第二個提案是 `org.tool.decision` ∈ `denied_before_execution | executed_failed | executed_ok`。這是跟 SIG 對話的姿態，不是另起一套。
  - **舊稿寫的是「只擴充 `human.approval`（不加 org 前綴，因為是提給規格的名字）」—重寫**：重切後落地名與提案名分家，照舊稿發會跟系列正文對不起來。
- 可以加一句這個提案姿態現在有對象：AAIF 的 observability WG 與 agents accountability WG，*every working group is open to non-members*（引句依重切後總論 §六 line 219；兩個 WG 的成立時間點見 §二）。
- **結尾**放總論 EN 連結。
- 舊稿結尾的「cert-pass 貼文在 LinkedIn 有 100+ 反應，若 Golden 剛完成可以同一則帶過」—**（原總論 §一 證照敘事已刪，此則作廢）**；證照要發就自己一則，不跟 12 月系列綁。

---

## 7. 社群回收

收集 DevOps Taiwan / Backend 台灣留言裡的「我們的 agent 出過什麼事」，匿名化後是 **2027 爆炸半徑主題**的台灣案例來源—selection 指出，目前沒有一個公開的台灣 coding-agent 事故。應變篇的資安面只留一段、指向那個主題，回收來的案例正好接在那裡。

---

## 8. 本次重切造成的作廢與改寫

| 項目 | 處置 | 原因 |
|---|---|---|
| 封面 F5 | **改**為 F14（F5 降為內文圖、列備選） | 封面要賣兩個 store，不是賣 trace 樹；F5 的 approval 節點也改標了 `org.approval` |
| 英文版「Kubestronaut / CNPE 一句話交代」 | **（原 §一 證照敘事已刪，此則作廢）** | 證照敘事整段刪除，12 月正文不提 |
| FB 總論 hook 舊版（Kubestronaut 大叔） | **（原 §一 證照敘事已刪，此則作廢）**，新版見 §6 | 同上；新版改用「trace 三十天就過期」 |
| LinkedIn 結尾 cert-pass 帶過 | **（原 §一 證照敘事已刪，此則作廢）** | 同上 |
| LinkedIn 主體的 `human.approval`（不加 org 前綴） | **重寫**為落地 `org.approval` + 提案 `human.approval` / `org.tool.decision` | 重切第三條主線：規格詞彙以實查為準，規格沒有的先落 `org.*` |
| X 總論 hook | **重寫**（trace 降級為線索、命名對手補到三個） | 承重句換成 trace vs ledger；§二 命名對手由一個變三個 |
| X 應變篇 hook 結尾 *reads the trace* | **改**成 *reads the ledger* | CI 的真值來源是帳本 |
| 英文關鍵詞 *lagging budget* | **改**成 *lagging quality gate* | change acceptance 不再進 budget |
| EN Part 3 標題 *Incident Response* | **改**成 *Tamper Boundaries* | 中文篇名同步改過 |
| FB 應變篇 hook 舊版（47 個平台） | **保留為紀錄**，不作廢 | 該數字仍在應變篇追責那節；只是 FB 改用東京現場材料 |

---

## 9. 待決

- **總論 EN 的 12/02**與「中文版全部上線之後再處理英文版與社群分發」互相牴觸（12/02 時三篇中文還沒發完）。兩種做法都成立—照舊稿隔天發，或整批推到 12/12 之後—**動筆前擇一**，選完主計畫 §5 與本檔 §4 一起改。
- **一位 Backend 台灣作者的 AIOps bot 貼文仍需取得引用同意與連結**。拿不到的話，總論 §一 那句改寫成不指名的一般敘述，§5 發布順序第 2 步的「回應那篇的角度」也要跟著換成一般的 DevOps / Backend 角度。
- **F14 尚未跑過 `mermaid_check.sh`**，封面 PNG 出圖前必須先跑；跑出來的尺寸若在 FB 縮圖上不成立，照 §3 退回 F5。
- **KubeCon Japan keynote 講者的全名、講題原文與錄影連結**還沒確認，LinkedIn 要 tag 本人就得先補上（同總論「來源對照」第 39 條的待補項）。
