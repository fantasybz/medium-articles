# 2026-09 選題結果：接下來三個月的主題

> 決定日期 2026-09-05。依據：五個視角共 20 個提案 → 合併成 8 個候選 → 每個候選 2 位評審（讀者 VP、資深編輯）各打 5 個分項、1 位反方預設要駁倒 → 由筆者（Claude 主迴圈）做最後選擇。評分與反駁原文在 `.context/research/judged.json`。

## 一句話版

| 月份 | 主題 | 一句話論點 |
|---|---|---|
| **2026-10** | 綠燈不是驗收：agent 時代的測試、Review 與可靠度 | CI 綠燈是 agent 的自我申報，不是驗收—別教 agent 怎麼測，去量它留下了什麼；而 review 是決定 agent 對組織是加分還是負債的唯一控制點。 |
| **2026-11** | 同一份規格，跑十次：把實作變異數當成 harness 的驗收指標 | 生成越便宜，「同樣的輸入會不會長出同樣的東西」越值錢—變異數在 loop 裡，不在 spec 裡；spec、AGENTS.md conventions、Pattern Language 是三支調變異的槓桿。 |
| **2026-12** | 把 Agent 當 Production Workload：Agent 的 SRE—可觀測、可靠、可追責 | Agent 的結案報告不是證據，trace 才是—沒裝儀表的 harness，你營運的不是產品，是傳聞。 |

三個主題都建立在已發布的 Agentic Engineering 三部曲之上：組織篇決定誰來做、技術篇蓋 harness、營運篇管 eval 與成本；接下來三個月分別回答「怎麼知道 agent 做對了」（10 月）、「怎麼知道 harness 做對了」（11 月）、「怎麼把整套東西當 production 營運」（12 月）。

---

## 2026-10：綠燈不是驗收

- **slug** `agentic-green-is-not-done`
- **title_zh** 綠燈不是驗收：agent 時代的測試、Review 與可靠度
- **title_en** Green Is Not Done: Testing, Review and Reliability for Agent Output
- **thesis_zh** CI 綠燈是 agent 的自我申報，不是驗收—別教 agent 怎麼測（TDD 儀式），去量它留下了什麼（mutation score、constraint tests、pass^k）；而 review 是決定 agent 對組織是加分還是負債的唯一控制點，重設計的重點不是讓人讀得更快，而是決定什麼值得人讀、誰審誰、AI 審 AI 何時該禁止。

**為什麼是這個**：這是兩個最高分候選（`agentic-output-verification` 38.5、`review-is-the-control-point` 37.0）的合體—兩位評審都指出它們共用同一批提案來源，而 review 候選的第三部是「大雜燴」。合起來剛好是「測試 → review → 可靠度閘門」一條驗證層。這也是作者最有立場的地盤：2023 年的 *Lessons Learned in Software Testing* 系列、2025 年的雙層測試護欄，社群也把粉絲團跟「測試哲學」連在一起。

**三部曲**

| 篇 | 標題 | 重點 |
|---|---|---|
| 一、測試篇 | 怎麼審一份 agent 寫的測試—斷言鬆綁、凍結 bug 與 mutation score | 「AI 說沒問題」之後 tester 要看什麼：assertion loosening、把現狀 bug 錄成 golden、覆蓋率是一條可以被改掉的斷言；mutation testing 當閘門而不是 TDD 儀式；人對錯誤斷言的判別只有 49%（2607.08885）所以要靠工具。 |
| 二、Review 篇 | Review 是控制點，不是瓶頸—分流、reviewer agent 艦隊與閉環禁令 | 兩層證據：真實 PR 資料集（2607.13196 一百萬 PR 更快沒更好、2607.03316 / 2607.21997 36.4% 接受 / 56.3% 拒絕、2608.21311 AI 審 AI 兩季成長 100 倍、2607.09902 每 +10pp 免審合併多 6% 維護負擔）驅動處方；實驗室結果（2607.21656 異質配對）只用來說明「異質」原則並標明會隨 model 版本翻轉。分流矩陣（人讀 intent 與 constraint，不讀 diff）、reviewer agent 的 YAML、社交工程 PR（「已預先核准」一句話讓 ~80% 外洩 PR 過關，2607.19267）、AI 審 AI 的禁用條件、approval artifact 綁人。 |
| 三、可靠度篇 | 綠燈是 34% 的謊言—constraint tests、pass^k 與授權擴張的閘門 | SWE-Gate（2609.04167）：功能測試通過的修補有 221/644 違反 reviewer 實際加的約束 → 把 review 約束寫成可執行的 constraint tests；可靠度不是能力：pass@1 與 pass^k 分開報（code 領域用 SWE-NFI 2607.27409、OpenHarmony 2608.16022；Thinkingbox 2608.19741 的 66.5% vs 47.5% 是非 code 工作流，只當旁證）；oversight budget（READY 2609.02095：0.3pp 準確率差換 10pp 人工複核）；接回營運篇的 G2 gate：授權擴張看 pass^k 與 escape rate，不看 pass@1。 |

**評審意見與已採納的修正**

1. 標題級數字要標領域：「34%」寫成「在 SWE-Gate 的量測裡」，不寫「所有 agent PR」；pass^k 的數字來源多半不是 coding agent，降為「同一模式在 code 以外也出現」。
2. 總論要有一本書當錨—書評型長文完讀率最高（建築 51%、XP 46%），方法清單型（雙層護欄）完讀最低。錨定 James Bach *Taking Testing Seriously*（作者已買、已在粉絲團引用）。
3. 修正對自己數據的誤讀：與不確定性共舞是 619 views / 98 reads（16%），不是 619 reads。
4. 台灣訊號要誠實：DavidKo「AI 說沒問題」「它把斷言改掉了」是 9 與 3 個反應，是真實痛點但不是燒起來的話題；燒起來的是 Uncle Bob 的 mutation test 閘門（40 反應）與 Clean Code 2nd ed.（190 反應 / 38 分享）。
5. 動筆前把引用的 19 篇 arXiv 全部讀完 abstract（反方指出其中 11 篇在 digest 裡只有 API 一行摘要）。
6. 發布計畫寫進粉絲團分享：2025 年 views 超過 presentations 的週，都是粉絲團有分享的週。

---

## 2026-11：同一份規格，跑十次

- **slug** `same-spec-ten-runs`
- **title_zh** 同一份規格，跑十次：把實作變異數當成 harness 的驗收指標
- **title_en** Same Spec, Ten Runs: Output Variance as the Acceptance Metric for Your Harness
- **thesis_zh** 生成越便宜，「同樣的輸入會不會長出同樣的東西」越值錢。固定一份規格、不介入、跑 N 次，實作的變異數就是 harness 的驗收指標—變異數在 loop 裡，不在 spec 裡；spec 厚度、AGENTS.md conventions、Pattern Language skills 是三支調變異的槓桿，而不是上限。

**為什麼是這個**：台灣資料集裡分享數最高的技術訊號（搞笑談軟工 Teddy Chen 的可重現性測試，298 反應 / 74 分享；Kim Kao 的 bounded context 每次抽出的數量不同），四篇已發布文章完全沒碰，作者本人出席過該工作坊、有第一手材料。候選原本叫「規格是新的原始碼」（37.0，被反方駁倒），駁倒的理由被全部採納：命題從「spec 決定上限」改成「變異在 loop、spec 是槓桿之一」。排在 11 月而不是 10 月，是因為它需要作者自己先跑一組實驗（見下）。

**三部曲**

| 篇 | 標題 | 重點 |
|---|---|---|
| 一、規格篇 | agent 與人都能驗收的規格長什麼樣—從 Example Mapping 到 agent 讀得懂的 spec | BDD 是溝通不是工具（Dan North）；Example Mapping → Claude Code → Gherkin 的流程與「四十條 Gherkin，然後呢」的反問；user story 換成完整 spec 讓 token +29.7%（2608.25399），但同篇也說 run-to-run variance unchanged—誠實寫出來；需求總是晚到、預先警告無效（2609.03028）。 |
| 二、契約篇 | spec 變成可執行的契約—contract-first、drift gate 與跨 vendor 的不可攜 | 只做「what」：contract-first tests（2608.17177）、drift gate（2606.27045）、把 SWE-Gate 的 constraint tests 當非功能附件、spec 跨 agent 不可攜（F1 0.035，2608.21208）、SpecMine 的 47 萬份 spec 長什麼樣（2608.25202）。ADR / 設計理由那一半不放這裡（見總論的 what / how / why 三張地圖）。 |
| 三、變異篇 | 回答 Teddy 的問題—用「同一份規格的變異數」當 harness 的驗收指標 | 作者自己的實驗：一個 repo、一份固定 spec、三種約束條件（無 / AGENTS.md conventions / Pattern Language skills）、每組 N≥10、量 AST 或結構相似度、測試通過率、review 約束違規數；對照 2608.26197（deterministic planning constraints 做到 reproducibility 1.000）證明變異在 loop；變異門檻接進營運篇 G2 scaling gate 當第四軸。 |

**評審意見與已採納的修正**

1. 變異篇抬成總論的脊椎：總論用 Teddy 的問題開場，決策工件是「固定 spec 跑 N 次」的變異門檻；三部曲才是展開。
2. 換題：「Spec is the new source」與 Sean Grove 的「specs are the new code」撞名、「clean loop not clean code」是別人的留言；標題以變異為錨。
3. 契約篇拆開：只留 spec → 可執行契約；ADR 與決策記憶縮成第三篇一節或總論的 what / how / why（spec / AGENTS.md / ADR：owner、壽命、enforcement）地圖。
4. **10 月就要開始跑實驗**，否則 11 月只能引別人的一行摘要—在 Teddy 剛開完工作坊的主場上，沒有第一手數據就是學生作文。
5. 社群訊號只用 Teddy 與 Kim Kao；DavidKo 的轉貼（7–13 反應）與 2025 年的水球潘講題不當主證據。

---

## 2026-12：把 Agent 當 Production Workload

- **slug** `sre-for-agents`
- **title_zh** 把 Agent 當 Production Workload：Agent 的 SRE—可觀測、可靠、可追責
- **title_en** Treat Agents as Production Workloads: SRE for Agents—Observable, Reliable, Accountable
- **thesis_zh** Agent 不是開發工具，是一個會花錢、會出事、會被打的 production workload—它需要 trace、SLO、error budget 與 on-call，而 SRE 十年來累積的方法剛好全部適用。Agent 的結案報告不是證據，trace 才是；沒裝儀表的 harness，你營運的不是產品，是傳聞。

**為什麼是這個**：與爆炸半徑（34.8）幾乎同分（35.0），兩者取一。取 SRE 的理由：作者可信的地盤（OTCA、Kubestronaut、2025 年的 CNCF GenAI Observability 與觀測性反模式兩篇）在這裡而不在資安；反方對爆炸半徑指出「非資安專職作者在資安題目被 CISO 抓到兩處 overclaim 就會傷整個系列」；X digest 標記 agent observability 是 291 個追蹤帳號裡完全沒人寫的缺口—這是機會不是沒需求，但總論要正面承認「這題現在沒人在講」。排 12 月：接在驗證層（10 月）與可重現性（11 月）之後，兩篇的交接點（pass^k、oversight budget、變異門檻）才有東西可以進 SLO；KubeCon NA 在 11 月，12 月正好接 Kubernetes v1.37 與 CNCF 的 AI 議程。

**三部曲**

| 篇 | 標題 | 重點 |
|---|---|---|
| 一、觀測篇 | 一次 agent run 的 trace 長什麼樣—OTel GenAI semantic conventions 落地 | 把 harness 本身裝上儀表：run / tool-call / model-call 的 span、cost per trace、eval-in-prod；結構化 trace 讓觀察者 token 少 14–15 倍（2609.01466）；GitHub Copilot cloud agent 6,400 萬筆日誌（2608.29204）當範例資料；復用既有 o11y stack（組織篇說過的原則），差別只在新的 signal。 |
| 二、可靠篇 | Agent SLO：把 pass^k、oversight budget 與 harness 版本當 production dependency 管 | 只做一個工件—agent SLO spec：SLI 只用 telemetry 拿得到的東西（run availability、tool-call error rate、latency、cost per successful task、oversight budget）；error budget 決定授權擴張（接營運篇 gates）；harness pin 與 diff 當 change management（只改 tool-output 裁切就 28%→49%，2608.26218；vendor 每天出兩版，2607.03691）。K8s sandbox fleet（v1.37 scale-to-zero、pod certificates）壓成一節並標明是 1,000 人規模的問題。 |
| 三、應變與追責篇 | Agent 出事的時候—incident response、flight recorder 與「誰批准了這個 PR」 | Agent 當第一線 on-call 的邊界；agent 自己出事的 runbook；防竄改事件帳本已經很便宜（每事件 48µs、每 10 萬事件 $2.30 上鏈，2609.01931）；47 個平台 0 個預設輸出 content-addressed 身分（2608.23610）；vendor 條款對「誰核准 agent 的 PR」互相矛盾（2608.15678）。資安面的 context 提權只留一段指向 backlog 的爆炸半徑主題。 |

**評審意見與已採納的修正**

1. 可靠篇砍到一個工件（agent SLO spec），把多 vendor failover、額度、被 ban、hybrid local 全部讓給 backlog 的席位經濟主題，只留一句。
2. K8s sandbox 容量問題壓成一節並標規模，或留給未來的「agent runtime as platform product」。
3. 需求訊號誠實化：不借用 Claude Taiwan 的席位抱怨；本主題自己的訊號是 OTel GenAI semantic conventions（LinkedIn 儲存）、Alolita 的 KubeCon Japan keynote、莊硯光的 Grafana + Claude Code AIOps bot（17 分享，注意那是 agent 做 SRE，不是 SRE for agents）。
4. 排 12 月，讓 10、11 月的交接（pass^k、oversight budget、變異門檻）具體化之後再寫 SLO。

---

## 排序理由

10 月先做驗證層，因為它接在營運篇「eval 是唯一會複利的資產」後面最自然，也是作者立場最強、社群最需要的中文材料。11 月的變異實驗要在 10 月開跑，所以不能排第一；它跟 10 月共用「constraint tests」與「量測不指示」的語言，讀者能接。12 月的 SRE 要等前兩個月產出量（pass^k、oversight budget、變異門檻），才有 SLO 可以定，也剛好接 KubeCon NA 與年底 retro；預算季（10–11 月）不適合它，因為它不是預算敘事。

## 落選候選（進 backlog）

| 候選 | 分數 | 反方 | 去處 |
|---|---|---|---|
| Coding Agent 的爆炸半徑（漏洞在 harness 不在 model） | 34.8 | 未駁倒（sev 3） | **backlog 第一順位**，最早 2027-01。動筆前要修：三個「台灣案例」沒有一個是 coding-agent 事故（700 GB 是國外故事、Zeabur 是平台入侵、台新原文說「不是 AI 失控」），要改寫成「台灣還沒有公開的 agent 事故，但 Zeabur 的環境變數同倉就是爆炸半徑的形狀」；2608.27443 受測者是 113 位非技術使用者且 HITL 排名第一，2608.28502 平均 ASR 只有 1.21%，兩處不能 overclaim；先在總論切分「論文的 harness = vendor runtime」與「系列的 harness layer = 你蓋的」。最好找一位資安協作者。 |
| AGENTS.md 不會讓 agent 變聰明（context / skills / memory 實證） | 33.5 | 未駁倒（sev 3） | 命題調弱成「pass rate 對 context 檔不敏感，要配 quality 側指標成對讀」（2607.27250 只有 17 任務 / 288 run；2606.20512 的 +7.5pp 要誠實呈現）；compaction 那一部與爆炸半徑衝突，二選一。skills 供應鏈材料可併入爆炸半徑。最早 2027-02。 |
| 速度免費之後：規格、團隊與人 | 33.0 | 駁倒（sev 3） | 規格篇已被 11 月吃掉；人篇證據撐不住（21x 是專案成長不是個人吞吐、N=21 質性研究）。若重建，以「知識流失與維護債」為軸（2607.09902、2606.13298、2607.05677、2608.25241、DDDTW 66 反應、Kent Beck 91 反應），做成團隊層的組織篇續集。 |
| 別用座位數編 2027 預算（席位經濟、韌性、主權） | 28.5 | 未駁倒但讀者錯位 | 最強證據全是 Claude Taiwan 個人 Pro / Max 使用者的抱怨，目標讀者買的是 Team / Enterprise seat 或 API；需要 3–5 家台灣公司的企業層採購觀察才寫得動。作者地盤不含採購與 CFO 敘事。降為觀察中。 |

## 評分總表（兩位評審平均，滿分 50）

| 候選 | demand | fit | diff | decomp | durab | 平均 | 反方 |
|---|---|---|---|---|---|---|---|
| agentic-output-verification | 8 / 8 | 9 / 9 | 7 / 7 | 6 / 7 | 8 / 8 | 38.5 | 未駁倒 |
| review-is-the-control-point | 7 / 9 | 8 / 8 | 8 / 7 | 6 / 6 | 8 / 7 | 37.0 | 未駁倒 |
| spec-is-the-new-source | 7 / 8 | 8 / 9 | 6 / 7 | 7 / 7 | 7 / 8 | 37.0 | **駁倒** → 依反方重建為 11 月主題 |
| sre-for-agents | 6 / 6 | 8 / 8 | 8 / 7 | 6 / 6 | 7 / 8 | 35.0 | 未駁倒 |
| coding-agent-blast-radius | 7 / 7 | 6 / 7 | 8 / 8 | 6.5 / 7 | 7 / 6 | 34.8 | 未駁倒 |
| context-engineering-evidence | 7 / 7 | 8 / 7 | 7 / 6 | 7 / 6 | 6 / 6 | 33.5 | 未駁倒 |
| after-free-throughput-teams-people | 7 / 7 | 7 / 7 | 6 / 6 | 6 / 6 | 7 / 7 | 33.0 | **駁倒** |
| seat-economics-resilience-sovereignty | 7 / 7 | 6 / 6 | 5 / 6 | 5 / 6 | 4 / 5 | 28.5 | 未駁倒 |

（每格為 editor / reader 的分數。）

---

## Notion 補充（2026-09-05 11:30 加入，來自 `notion_digest.md`）

作者自己的 Notion 打通後，四份摘要變成五份。以下幾點會直接改變大綱的寫法，大綱 agent 必須採納：

**跨主題**
- 作者正在 Golden Kubestronaut 的最後一站：十張證照已過（LFCS → CNPA，2025-10 → 2026-06），只剩 CNPE（第一次 46/64，第二次已預約；Notion 最近三頁都是 CNPE 模擬題）。Claude Certified Architect – Foundations 約在 2026-04 考過。作者答應過要寫「我的 Golden Kubestronaut 之路」，排期不要跟 12 月撞。
- 讀書筆記裡有 Kahneman《雜訊》（2022），引句「人類只要做出判斷，就會有雜訊」—noise audit 的方法就是「同一份規格、跑 N 次」，可當 11 月總論的書錨。
- `Fb temp`（2026-09-02）是一篇談軟體腐化的草稿，源自 LeSS in Action 的討論；可當 11 月 drift gate 的引子，也可帶出 backlog 的「知識流失與維護債」。

**10 月（綠燈不是驗收）**
- 《Taking Testing Seriously》的筆記只到「節錄」階段（定義章 + Bach podcast，反思欄空白）—動筆前先把書讀完。Bach 的 testing / checking 之分正好磨利論點：CI 綠燈與 agent 的自我申報都是 *checking*；驗收是 *testing*；mutation score、constraint tests、pass^k 是更好的 check，要用這個詞稱呼它們。
- 作者在模式語言工作坊做過的 A/B（裸 prompt 10/16 vs `execute-uc` skill 16/16，Opus 4.7，兩個 worktree）是 N=1 的**合規**數據，不是變異數據：拿來當 10 月「綠燈不是驗收」的實例（測試全綠但 event-sourcing replay 從未被執行、缺 `@DirtiesContext` 導致 CI 間歇紅燈），不要拿去 11 月當變異證據。
- 其他第一手材料有三份。XP 系列書摘（11 本，其中 3 章已發表；*XP Installed* 題詞：「XP 是第一個將焦點放在驗證上的流行開發流程」）。LeSS in Action 的 A-TDD 筆記：失敗的測試要因為對的理由失敗、避免負向斷言、真資料勝過 mock。CCA-F 筆記：獨立 review instance 勝過 self-review、CI review 與生成 session 分開、不信自我申報的信心、分層抽樣做人工審查。

**11 月（同一份規格，跑十次）**
- Teddy 工作坊的框架要正面引用：去技能化開場、SDD 階梯（Spec-first / Spec-anchored / Spec-as-source）、Context vs Form（支持修正後的論點「變異在 loop 不在 spec」）、需求＝What vs 規格＝How、Four-Form Patterns（Pattern / Rules / Gates）、雙迴圈 Human → Context → LLM → Validation → Machine 與 repo hooks / check scripts 的對應。
- **名詞衝突**：本主題契約篇原本寫「只做 what」，但 Teddy 的用法是「需求＝What、規格＝How」。大綱要先定義自己的 需求／規格 用法並對照 Teddy 的，並說明本系列站在他 SDD 階梯的哪一階。
- 變異實驗要在作者自己的 repo 重做 skills 那一組，不要用 Teddy 的課程 repo。
- 2025 學習預算頁顯示作者買過「規格驅動開發實戰」課—規格篇有第一手材料。

**12 月（Agent 的 SRE）**
- CNPE 的考試範圍剛好對到三部曲：Jaeger / OTel Collector / Prometheus（觀測篇）、Kyverno / OPA / PSS（guardrails）、Argo Workflows / Crossplane / CRDs（runtime）、Gateway API timeouts 與 namespace isolation；OpenCost 模擬題 → cost-per-task SLI；CCA-F 的結構化錯誤分類 → tool-call error-rate SLI，結構化 manifest → flight recorder。
- Google 白皮書把這門學問叫「Agent Ops」，是命名上的對手，總論要點名並說明為什麼用 SRE 的語言。
- 12 月必須明確超越 2025 年的兩篇觀測性文章（CNCF GenAI Observability、觀測的修復之道），不能只是重講。
- ihower 工作坊有 Braintrust 的實作，可當 eval-in-prod 的示範。

**backlog 追加**
- 平台工程 / IDP as a product（作者整年在讀，12 月只給一節）；系統思考與 CLD（Meadows、Senge、呂毅道場）可當重建「速度免費之後」的脊椎；去技能化獨立成文；DDD / Event Sourcing 作為 agent 產出的設計維度；agent 的探索式測試；被否決的席位經濟主題裡的 inference infra 那一半。

**安全提醒（不進文章）**：Notion 的《Appier O'Reilly Learning》頁面含明文帳密與一組 API key，建議移出 Notion。摘要裡沒有轉錄。
