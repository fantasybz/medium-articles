# Agentic Engineering 三部曲（三）：Eval、單位經濟與規模化——把 agent 當產品營運

> **TL;DR** — 三部曲最終篇。Runtime 用買的、組織照第一篇組、harness 照第二篇蓋，然後呢？多數導入死在「然後」：沒有 eval 所以換不換 model 靠感覺、沒有成本模型所以 CFO 半年後來砍預算、沒有反作弊的指標所以數字漂亮但沒人變快。本篇給出完整的營運層：eval dataset 的實作 pipeline 與分級、單位經濟與 model routing、指標樹與每個指標的反作弊設計、pilot 之後的 scaling gates，以及 vendor 管理的決策流程。

> 系列導覽：[總論](https://fantasybz.medium.com/%E5%88%A5%E6%80%A5%E8%91%97%E6%89%93%E9%80%A0%E4%BD%A0%E7%9A%84-devin-agentic-engineering-%E7%9A%84%E7%B5%84%E7%B9%94%E7%AD%96%E7%95%A5%E8%88%87-90-%E5%A4%A9%E8%A1%8C%E5%8B%95%E8%97%8D%E5%9C%96-7342ababc417) → [一、組織篇](https://fantasybz.medium.com/agentic-engineering-%E4%B8%89%E9%83%A8%E6%9B%B2-%E4%B8%80-%E8%AA%B0%E4%BE%86%E5%81%9A-platform-federation-%E7%9A%84%E7%B5%84%E7%B9%94%E8%A8%AD%E8%A8%88%E5%AF%A6%E5%8B%99-9d9353ef7f3a) → [二、技術篇](../2026-10-agentic-harness-blueprint/article.md) → **三、營運篇（本篇）**

---

## 一、把 agentic capability 當內部產品營運

先做一個視角轉換：你的「產品」是 paved road，「客戶」是 domain teams，「營收」是被成功委派的任務，「流失」是工程師試了兩次失敗之後，悄悄回去手寫。

這個視角決定了營運的全部內容：產品要有量測（eval 與指標）、要有單位經濟（cost per successful task）、要有成長策略（scaling gates）、要有供應鏈管理（vendor 策略）。本篇依序處理這四件事。

先講為什麼 eval 排第一。總論的判斷是：**eval dataset 是唯一會複利的資產**——model 每半年一代，harness 的假設不斷過時，但「你的工作負載上什麼叫做對」這件事，累積下來就是你的護城河。市場每次 model 升級、每場 vendor 價格戰，都讓它增值一次：因為只有你能在一天內用自己的 eval 驗證新選項，別人只能讀 benchmark 用猜的。

---

## 二、Eval Framework 的完整實作

### Dataset 從哪裡來

多數團隊卡在第一步：「eval 要從哪來？」答案：你的工程歷史裡已經有了，缺的只是回收的 pipeline：

```mermaid
flowchart LR
    SRC1["Incidents /<br/>post-mortems"] --> X["Eval 抽取<br/>（agent 輔助整理）"]
    SRC2["PR history<br/>（被打回的、一次過關的）"] --> X
    SRC3["手工挑選<br/>golden tasks"] --> X
    X --> DS["Eval dataset<br/>（版本控管，與 code 同 repo）"]
    DS --> RUN["定期執行<br/>（harness 改動 / model 升級 / 每週）"]
    RUN --> SCORE["評分<br/>（自動 + 每月人工抽查）"]
    SCORE --> DEC["決策：換 model？修 harness？擴大授權？"]
    DEC -.->|新失敗案例回填| DS
    style DS fill:#d4edda,stroke:#2e7d32
```

三個來源各有特性：

- **Incident 回收**：每份 post-mortem 都是現成的 case——給 agent 當時的 context 與症狀，它能不能找到 root cause？這類 case 最貴也最真實。
- **PR history 回收**：被 reviewer 打回的 agent PR 連同 review comment，是最真實的 negative example；一次過關的則是 golden path。
- **手工 golden tasks**：挑 10–20 個有代表性的已完成任務（bug fix、小 feature、refactor 各幾個），固定 context 與驗收條件。

### Eval case 的形狀

Case 用宣告式格式寫，跟 code 一起版本控管、一起 review：

```yaml
# evals/cases/payment-timeout-fix.yaml（節錄）
id: payment-timeout-fix
source: incident-2026-04-18        # 出處可追溯
context:
  repo: shop-backend
  entry: "使用者結帳偶發 504，附 trace id"
expected:
  root_cause: "connection pool 上限"
  fix_touches: ["internal/db/pool.go"]
  tests_added: true
scoring: rubric                    # rubric / exact / llm_judge
```

### 三級 eval，各司其職

| 級別 | 數量 | 執行時機 | 回答的問題 |
|---|---|---|---|
| **Smoke** | 5–10 | 每次 harness 改動 | 有沒有把基本盤弄壞？ |
| **Golden** | 20–50 | 每週 + 每次 model 升級 | 核心能力有沒有回歸？ |
| **Frontier** | 10–20 | 每月 | 能力邊界推進到哪？該不該擴大授權？ |

Frontier 級最容易被省略，但它回答的是最值錢的問題：**agent 現在做不到的事，下一版 model 做到了沒**——這直接決定授權範圍要不要放寬（見第五節的 gates）。

### LLM-as-judge 的三個陷阱

量大之後一定會用 LLM 當評審，三個坑先講：

1. **Judge 偏好長答案與自信語氣**。Rubric 要綁事實項——測試過了嗎、改的檔案對嗎、root cause 對嗎——而不是「整體品質 1–10 分」。
2. **同家族偏袒**。Judge 與被評的 model 同一家族時會偏心；用不同家族的 model 當 judge，或雙 judge 取交集。
3. **Judge drift**。Judge 用的 model 也會升級，昨天的 85 分和今天的 85 分可能不是同一件事——judge 的 model 版本也要 pin 住、變更要記錄。

校準的錨只有一個：**每月一次、抽 10 個 case 的人工評分**，跟 judge 的分數對照。全自動 eval 是目標，不是起點；沒有人工錨的自動評分，飄掉了你也不會知道。

---

## 三、單位經濟：成本模型與 Model Routing

### 一次 run 的成本解剖

一次 autonomous run 的成本 = model tokens（通常佔 60–80%）+ sandbox 運算（10–25%）+ 週邊（觀測、儲存）。花費從幾十美分到幾十美元不等，而決定因素不是任務難度，是兩個浪費源：

- **Retry tax**：失敗重試的成本。Retry rate 從 30% 降到 10%，總成本直接砍兩成以上——而 retry rate 高的根因，九成在 harness 的 context 與 feedback 層（第二篇），不在 model。**Retry 燒掉的錢，是 harness 品質的稅。**
- **Context 肥大**：把整個 repo 塞進 context 的懶惰做法。第二篇的三層 AGENTS.md 與「repo 層 100 行」紀律，就是 context 的減肥方案。

### Model routing 矩陣

不同工作用不同等級的 model，routing 邏輯放在 platform 層（第二篇的 gateway），各 team 不用自己決定：

| 任務類型 | 建議層級 | 理由 |
|---|---|---|
| Planning、架構判斷 | 最強 model | 錯誤成本最高，一次做對 |
| 大量 code 生成 | 中階 model | 有 tests 兜底，量大 |
| Eval 執行、lint 類 | 便宜 model | 高頻、低風險 |
| Review、安全判斷 | 最強 model | 最後防線不省錢 |

### Budget guardrails

- **Per-team quota + 超額 alert**：先觀察不硬斷——初期的用量分布資訊，比省下的錢更值錢。
- **Run-level kill switch**：單次 run 超過成本上限（例如 20 美元）自動暫停、要求人工確認——這是對付 runaway retry loop 的保險絲。
- **Cost per successful task 看趨勢，不看絕對值**：第一年是學費期（組織篇的預算敘事），第二年才拿它跟人力成本做比較。

---

## 四、指標樹與反作弊

總論給了 North Star 的公式，這裡展開成可以量測的 metric tree：

```mermaid
flowchart TD
    NS["Effective Engineering Leverage"] --> A["Delegation<br/>成功委派的任務比例"]
    NS --> B["Completion<br/>End-to-end 完成率"]
    NS --> C["Attention<br/>人類投入時間 / 任務"]
    NS --> D["Quality<br/>Production 正確性"]
    A --> A1["任務類型覆蓋率"]
    B --> B1["Retry rate"]
    B --> B2["Autonomous completion rate"]
    C --> C1["Review minutes / PR"]
    C --> C2["等待與 context switch"]
    D --> D1["Escape rate"]
    D --> D2["Revert rate"]
    style NS fill:#d4edda,stroke:#2e7d32
```

每個指標都會被 game——不是因為有人惡意，而是 Goodhart's law 的日常運作。所以設計指標時就要配好解藥：

| 指標 | 會被怎麼 game | 對策 |
|---|---|---|
| % tasks delegated | 把大任務拆小灌件數 | 搭配「任務類型覆蓋率」，看廣度不看件數 |
| Review minutes / PR | Rubber stamp 快速放行 | 與 escape / revert rate 成對讀 |
| Completion rate | 只委派簡單任務 | Frontier evals 追蹤能力邊界有沒有前進 |
| Escape rate | 出事不開 incident | Incident 定義綁 SLO，不綁人的判斷 |

原則一句話：**指標成對出現——速度指標必配品質指標**。單獨考核任何一個數字，你就會得到那個數字，以及它背後被犧牲的一切。這是 DevOps 時代 vanity metrics 的 2.0 版教訓。

---

## 五、90 天之後：Scaling Gates

總論給了前 90 天的行動藍圖（選 pilot、量 baseline、建 eval）。Pilot 結束後，最常見的錯誤是宣布成功、全面推廣。規模化要用 gate 制——每道門檻有明確的量化條件，過了才解鎖下一步：

| Gate | 過關條件 | 解鎖 |
|---|---|---|
| **G1：Pilot 結業** | 2 個 teams 穩定使用；eval 就緒；對照 baseline 有感改善 | 擴大到 25% teams |
| **G2：規模驗證** | Retry rate < 15%；escape rate 持平；champions 體系自轉 | 全部 teams + 開放 write 級 tools |
| **G3：深度授權** | Frontier evals 連續穩定；audit 半年無重大事件 | Dangerous tools 白名單、多步 autonomous run |

```mermaid
flowchart LR
    P["Pilot（90 天）"] --> G1{"G1"} --> E1["25% teams"] --> G2{"G2"} --> E2["全員 + write tools"] --> G3{"G3"} --> E3["深度授權"]
    G1 -.->|未過| F1["回頭修 harness / 組織"]
    G2 -.->|未過| F1
    G3 -.->|未過| F1
    style F1 fill:#ffe0e0,stroke:#c0392b
```

兩個紀律：**卡住就回頭修，不硬推**——G2 過不了通常是 harness 問題（第二篇），G3 過不了通常是 guardrails 與 eval 覆蓋問題。以及：**擴張速度由 eval 與 escape rate 決定，不由 roadmap 決定**。Roadmap 上寫著 Q3 全面導入，不構成 G2 自動過關的理由。

---

## 六、Vendor 管理

- **雙 vendor 是常態**：一個主力、一個挑戰者。這不是不信任，是議價結構——你的 eval dataset 讓「讓挑戰者試試」變成一天的事，這正是第二節說的複利在兌現。
- **換 model 的決策流程**：新 model 發布 → 跑 golden + frontier evals → 看三件事：pass rate 變化、cost per task 變化、**新出現的失敗模式**（最容易被忽略）→ 用 20% workload 做兩週 canary → 全量。永遠不要因為 benchmark 分數或 demo 換 model。
- **合約要盯的四件事**：你的 code 與 transcript 是否被用於訓練、log 的保存位置與期限、rate limit 與 SLA、以及價格保護——token 單價波動大，能鎖一年就鎖一年。

---

## 七、系列收尾

三部曲收在總論的同一句話：

> **Buy the intelligence. Build the environment. Own the feedback loop.**

組織（第一篇）決定誰來做；harness（第二篇）決定 agent 能不能做好；營運（本篇）決定你知不知道它做得好不好、值不值得繼續加碼。三者都不是一次到位的工程，是持續經營的內部產品。

如果只能從三件事開始：**量 baseline、挑 pilot、建前 10 個 eval cases**。九十天後，你就有資格用證據而不是 vibes，做下一個決策。

---

### 系列文章

1. [總論：別急著打造你的 Devin](https://fantasybz.medium.com/%E5%88%A5%E6%80%A5%E8%91%97%E6%89%93%E9%80%A0%E4%BD%A0%E7%9A%84-devin-agentic-engineering-%E7%9A%84%E7%B5%84%E7%B9%94%E7%AD%96%E7%95%A5%E8%88%87-90-%E5%A4%A9%E8%A1%8C%E5%8B%95%E8%97%8D%E5%9C%96-7342ababc417)
2. [一、組織篇：誰來做？Platform + Federation 的組織設計實務](https://fantasybz.medium.com/agentic-engineering-%E4%B8%89%E9%83%A8%E6%9B%B2-%E4%B8%80-%E8%AA%B0%E4%BE%86%E5%81%9A-platform-federation-%E7%9A%84%E7%B5%84%E7%B9%94%E8%A8%AD%E8%A8%88%E5%AF%A6%E5%8B%99-9d9353ef7f3a)
3. [二、技術篇：Harness 藍圖——把系統變成 agent 讀得懂的地方](../2026-10-agentic-harness-blueprint/article.md)
4. **三、營運篇（本篇）**

---

### References

1. Anthropic — [Effective harnesses for long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)
2. Google — [2025 DORA report: How are developers using AI?](https://blog.google/innovation-and-ai/technology/developers-tools/dora-report-2025/)
3. Stack Overflow — [Agents on a leash: Agentic AI remains mostly monitored at work](https://stackoverflow.blog/2026/05/27/agents-on-a-leash-agentic-ai-remains-mostly-monitored-at-work/)

---

*本文發表於 [Medium @fantasybz](https://medium.com/@fantasybz)。若你正在把 Agentic Engineering 從 pilot 帶到規模化，歡迎交流。*
