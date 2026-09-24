<!--
Medium 發布指南（此註解區塊不要貼進 Medium）

自動化：`./tools/medium_draft.sh <article-dir>` 會建好草稿並比對內容，停在發布前一步。
細節見 repo 根目錄的 PUBLISHING.md。以下是手動流程與發布後必做的收尾。

【系列狀態】以各篇 publish/PUBLISHED.md 為準。Medium 限制同一作者 24 小時內最多發布或排程 2 篇，
見 PUBLISHING.md 的〈發文數量上限〉。

【手動流程】
1. 開新 story：https://medium.com/new-story
2. 貼上下方內容（從標題那行開始，不含本註解）。
3. 看到 📌【在此插入…】的行：刪掉該行，按 + 插入同目錄 images/ 裡對應的 PNG。
4. code block：在 Medium 選取後按 ``` 轉成 code block。
5. 封面圖選流程圖，不要選表格截圖（縮到卡片尺寸看不清）。
6. Tags 建議：AI, Software Engineering, Engineering Management, Agentic AI, DevOps

【發布後收尾—不做的話系列會斷】
7. 記下本篇 Medium URL，補進 repo 的 README 索引與 publish/PUBLISHED.md。
8. 把本篇兩處的系列連結換成真正的 Medium URL：
   (a) 開頭「系列導覽」那一行
   (b) 文末「系列文章」清單
   （尚未發布的篇在這裡是純文字「（即將發布）」，不是相對路徑；上線後換成真正的 URL）
9. 回頭編輯已發布的其他篇，把指向本篇的連結補上。
-->

# Agentic Engineering 三部曲（三）：Eval、單位經濟與規模化—把 agent 當產品營運

> **TL;DR** — 三部曲最終篇，接著處理環境建好之後的日常決策：如何知道 agent 做得好不好、一次完成任務花多少錢，以及什麼時候適合擴大使用。本篇整理 eval dataset 的建立與維護、成本模型與 model routing、需要搭配解讀的指標，以及 pilot 之後的 scaling gates 和 vendor 管理。文中的數量與門檻是起始建議，團隊仍要依任務風險、樣本與實際成效調整，才能把一次導入變成持續有人負責的內部產品。

> 系列導覽：[總論](https://fantasybz.medium.com/%E5%88%A5%E6%80%A5%E8%91%97%E6%89%93%E9%80%A0%E4%BD%A0%E7%9A%84-devin-agentic-engineering-%E7%9A%84%E7%B5%84%E7%B9%94%E7%AD%96%E7%95%A5%E8%88%87-90-%E5%A4%A9%E8%A1%8C%E5%8B%95%E8%97%8D%E5%9C%96-7342ababc417) → [一、組織篇](https://fantasybz.medium.com/agentic-engineering-%E4%B8%89%E9%83%A8%E6%9B%B2-%E4%B8%80-%E8%AA%B0%E4%BE%86%E5%81%9A-platform-federation-%E7%9A%84%E7%B5%84%E7%B9%94%E8%A8%AD%E8%A8%88%E5%AF%A6%E5%8B%99-9d9353ef7f3a) → [二、技術篇](https://fantasybz.medium.com/agentic-engineering-%E4%B8%89%E9%83%A8%E6%9B%B2-%E4%BA%8C-harness-%E8%97%8D%E5%9C%96-%E6%8A%8A%E7%B3%BB%E7%B5%B1%E8%AE%8A%E6%88%90-agent-%E8%AE%80%E5%BE%97%E6%87%82%E7%9A%84%E5%9C%B0%E6%96%B9-f2a139f5b561) → **三、營運篇（本篇）**

---

## 一、把 agentic capability 當內部產品營運

先換一個視角：把平台提供的 paved road 當成內部產品，domain teams 就是使用它的團隊。這個產品有沒有價值，要看工程師能否把合適的任務交給 agent、取得可接受的結果，並且願意繼續使用。如果嘗試之後仍得花大量時間善後，回到手動工作也可能是合理選擇；平台需要理解這個選擇背後的原因。

Paved road 是平台維護的預設路徑，把環境、權限與驗證方式整合在一起。團隊有特殊需求時，可以提出例外，但要說清楚由誰維護、承擔哪些風險，以及如何保留必要的檢查。

用這個角度看，採購只是起點。後續營運至少要持續回答四個問題：

- **成效**：哪些任務被委派，哪些通過驗收，又需要多少人工協助？Eval 與使用紀錄要一起回答。
- **單位經濟**：包含失敗與重試之後，每件通過驗收的任務花費多少？
- **擴大使用**：現有證據足以支援哪些新任務或團隊，哪些缺口要先處理？
- **供應商選擇**：價格、功能或政策改變時，有沒有經過驗證且負擔得起的替代方案？

本篇依序處理這四個問題，也把它們連回同一個決策：下一筆投入，應該用來擴大使用，還是改善目前的流程。

Eval 排在前面，是因為後續比較需要共同基準。Eval dataset 是團隊維護的任務集合，每個 case 都有必要的 context、驗收條件與評分方式，讓不同 model 或 harness 版本在可比較的條件下接受評估。

總論把 eval dataset 視為可以持續累積價值的資產。這個價值來自團隊逐步釐清「什麼結果可以接受」，並把失敗經驗轉成可重複檢查的案例。不過，需求、系統與風險都會改變，dataset 也需要維護，不能把舊答案永遠當成正確答案。

有了這份基準，新 model 或價格方案出現時，團隊就能用自己的工作負載比較選項。評估仍然需要時間與成本，但不必每次都從 vendor 的展示重新猜起。

---

## 二、Eval Framework 的完整實作

### Dataset 從哪裡來

「Eval 要從哪裡來？」是很實際的起始問題。我會先回頭整理工程歷史：哪些事故值得重現、哪些 PR 暴露了判斷缺口，以及哪些日常任務最能代表團隊的工作。這些都是材料，還需要整理與驗證，才能成為可用的 case。

下圖把材料整理、版本控管、執行、評分與決策連起來，也保留一條把新失敗案例補回 dataset 的路徑：

📌【在此插入圖 diagram-01.png】

最後那條回填路徑，讓日常使用能持續修正 eval 的盲點。既有案例仍可保護已知行為，新案例則讓團隊看見工作內容與風險的變化。兩者都需要維護，不能只靠增加執行頻率維持代表性。

整理三種來源時，我會分別注意：

- **Incident**：從 post-mortem 重建當時可取得的症狀、版本與必要資料，確認環境可以重現。根因與修復答案留給評分端，不能直接放進受測 agent 的 context。
- **PR history**：被退回的 PR 與 review comment 可以揭露錯誤模式，但 review 意見也要查證。已核准的 PR 同樣需要獨立確認結果，不能把「曾經合併」直接當成正確答案。
- **手工挑選的任務**：可以先整理 10–20 個代表性的 bug fix、小 feature 與 refactor，固定輸入與驗收條件。這是建立流程的起始建議，後續要依實際任務分布補足樣本。

### Eval case 的形狀

我會用結構化欄位記錄 case 的來源、context、期望結果與評分方式，讓它可以一起版本控管與 review。下面是虛構的付款逾時案例，用來說明格式；日期、repo 與根因都不是本文引用的真實事故，也不是可直接執行的 eval framework：

```yaml
# evals/cases/payment-timeout-fix.yaml（虛構案例示意）
id: payment-timeout-fix
source: example-incident-2026-04-18 # 示意識別碼，非真實事故
context:
  repo: shop-backend
  entry: "使用者結帳偶發 504，附 trace id"
expected:
  root_cause: "connection pool 上限"
  candidate_files: ["internal/db/pool.go"] # 調查線索，不是唯一合法修改位置
  tests_added: true
scoring: rubric                    # rubric / exact / llm_judge
```

`source` 要能說明案例來自哪裡；人工設計的案例也可以納入，只要清楚標示。`expected` 應由評分端保存，避免洩漏答案。範例裡的檔案只是可能相關的位置，不能用「有沒有改到這個檔案」判定修復正確；`tests_added: true` 也只能確認有新增測試，還要檢查測試能否辨認原本的缺陷。

### 三級 eval，各司其職

我會依用途把 eval 分成三級。表中的數量與頻率是起始建議，並非業界標準；樣本應隨任務類型、風險與執行成本調整：

📌【在此插入表 table-01.png】

Frontier 用來探索目前還不穩定、但有價值的任務，讓團隊觀察新版本是否改善了能力邊界。它的結果可以支援授權討論，卻不能單獨決定是否開放高風險操作；實際環境的限制、事故處理與回復能力仍要一起檢查。

### LLM-as-judge 的三個陷阱

評分先採用可直接查證的方法，例如測試結果、輸出比對與政策檢查。對需要判讀說明或多種合理解法的部分，可以讓另一個 model 依 rubric 協助評分，也就是 LLM-as-judge。採用之前，我會先處理三種風險：

1. **表達方式影響評分**。長答案與自信語氣可能掩蓋內容錯誤。Rubric 要要求可查證的依據，例如測試結果、根因證據與修正行為，避免只給模糊的總分。
2. **Judge 與受測 model 共享盲點**。不同 model 的評分可能有不同偏差；換一家族或使用雙 judge，可以增加比較訊號，但不能保證獨立或正確。意見分歧需要回到證據檢查。
3. **Judge drift**。評分 model、prompt 或 rubric 改變後，同一個分數可能代表不同標準。記錄完整版本與設定，變更時重新評估一組人工標註案例。

人工抽查是必要的校準來源，也需要明確 rubric 與分歧處理。我會先安排每月抽查 10 個 case，涵蓋成功、失敗與 judge 意見分歧的情況，再依風險擴大樣本。這個數量只是起點，不能用來保證罕見錯誤已被涵蓋；人工評分本身也應定期對照與討論。

自動化可以減少重複評分的工作，人工抽查則幫團隊發現標準與實際需求之間的落差。目標是讓評估結果足以支援決策，而不是把人工介入降到零。

---

## 三、單位經濟：成本模型與 Model Routing

### 一次 run 的成本解剖

談成本前，先定義計算範圍。一次 run 的直接成本可以包含 model 使用量、sandbox 運算、觀測與儲存。各項占比會隨任務、快取、計價方式與執行時間改變，應從自己的帳單與 run 紀錄計算。

接著把同一任務的所有嘗試連起來。這裡的 **cost per successful task**，定義為同一觀察期內納入統計的直接成本，除以通過驗收的任務數；分子包含失敗、重試與最後放棄的任務。若沒有任務通過，應報告總成本與零完成件數，不能把單位成本記成零。比較整體效益時，另外列出人工 review、返工與平台維護成本。

- **重試成本要看實際嘗試次數**。假設每次嘗試都花費 `c`，每件任務最多額外重試一次，且最終通過率與任務組成不變。需要重試的任務比例從 30% 降到 10%，平均成本就從 `1.3c` 降到 `1.1c`，約減少 15.4%。這只是算例；實際重試可能長短不同、發生多次，不能只從 retry rate 推算省下多少錢。
- **Context 要符合任務需求**。如果只修改一個 handler，卻每次讀取大量無關內容，就可能增加成本與判斷負擔。技術篇的分層文件與明確連結，有助於提供必要資訊；但不能只為了降低 token 數，刪掉驗證所需的背景。

### Model routing 矩陣

Model routing 是依任務特性選擇合適的 model 或執行工具。Platform team 可以維護共通路由與紀錄，domain team 則提供風險與驗收條件，雙方用 eval 決定哪些組合可用。這個判斷需要隨工作負載與版本更新，無法做一次就永遠沿用。

下表整理我會先檢查的條件。Model 的價格或等級可以提供選項，真正的依據仍是它在這類任務上的表現：

📌【在此插入表 table-02.png】

Planning 與 review 值得投入較多驗證，因為前者影響後續方向，後者可能影響是否接受結果。但使用最強的 model 也不能保證判斷正確，更不代表它自動取得最終核准權限。

### Budget guardrails

Budget guardrails 要讓團隊在學習期間保有空間，也能及早發現失控的消耗。我會同時設定團隊層與單次執行的限制：

- **團隊配額與分段 alert**：先給足以完成 pilot 的預算，接近門檻時通知 owner；需要增加時，再依任務需求與已取得的結果調整。初期可以保留彈性，但仍要有總額上限。
- **Run-level kill switch**：單次 run 超過設定成本或嘗試次數時暫停，例如先以 20 美元作為某類 pilot 的檢查點。實際上限要依任務設定，並考慮尚未回報的費用與進行中的請求。恢復前由負責人確認是否值得繼續。
- **從 pilot 就追蹤單位成本**：和相近任務的人工投入、品質與完成率一起比較。第一年的學習成本可以單獨說明，但必須指出它換來什麼改善，不能等到第二年才開始算帳。

如果只要求成本下降，團隊可能會減少必要的驗證，或把人工善後移出統計範圍。成本因此要和品質、完成率及人工投入一起閱讀，才知道流程是否真的改善。

---

## 四、指標樹與反作弊

總論用四個面向描述工程效益，這裡把它們展開成可量測的指標。Delegation 是符合條件的任務中，實際交由 agent 嘗試的比例；Completion 則以這些已委派任務為分母，統計通過驗收的比例。兩者分開，才能看見使用範圍與完成能力的差異。

📌【在此插入圖 diagram-02.png】

這四個面向要一起解讀，不能直接相乘成一個總分。人工投入包含 review、修正、調查與等待造成的負擔；品質則需要交付後的觀察。本文的 escape rate 指「交付後才發現缺陷的變更」占同批交付變更的比例，比較時必須使用相同的觀察窗口與缺陷定義。短期沒有發現缺陷，仍不等於已經證明沒有問題。

指標也會改變人的行為。當單一數字成為考核目標，大家可能在沒有惡意的情況下，優先選擇能讓數字改善的工作。設計報表時就要保留任務組成與品質訊號，避免把這種變化誤認為能力提升：

📌【在此插入表 table-03.png】

我的原則是：**速度與成本指標，都要搭配品質與人工投入解讀**。如果 review 時間下降，卻有更多同事在交付後處理返工，改善的可能只是報表。把這些負擔放回同一個視野，討論才會接近團隊真正經歷的工作。

---

## 五、90 天之後：Scaling Gates

總論建議先用一段有範圍的 pilot，選定團隊、量測 baseline 並建立 eval。到了原定檢視時間，下一步不必然是全面推廣；有時更合理的決定，是把已找到的問題修好，再繼續觀察。

我會用 gates 整理擴大前需要的證據，但把「增加使用團隊」與「放寬操作權限」分開核准。下面的 25%、15% 與半年觀察期都是討論起點，應依風險、樣本量與任務組成調整；達到門檻，也只是進入審查的條件：

📌【在此插入表 table-04.png】

審查前要先定義「持續使用」與「有人支援」如何確認，也要記錄各指標的分母與觀察期。半年沒有重大事故，可能只是工作量小或尚未遇到某種情境，不能直接推成安全證明。Dangerous tools 涉及 production 或外部世界，更需要針對操作本身確認範圍、核准人與回復方法。

下圖表示逐步審查的方向。每一個階段都可以縮小範圍或回頭改善，沒有因為日期到了就自動開放的步驟：

📌【在此插入圖 diagram-03.png】

回頭的路徑都指向改善工作。它們提醒團隊，暫停擴大本身也是一個有效決策，接下來要把未通過的原因轉成具體修正與驗證。

第一個原則是**先查原因，再安排改善**。門檻未通過，可能涉及 harness、model、任務選擇或組織支援。依執行紀錄與案例找到缺口、指定 owner，再決定重做哪一組驗證，不能只把時程往後延一季。

第二個原則是**擴大範圍要跟得上證據與支援能力**。Roadmap 可以安排檢視時間，不能代替核准理由。進入下一階段後，仍要保留停止、回復與重新審查的條件，持續觀察新團隊與新任務帶來的變化。

這些決策需要可追溯的 eval、實際使用紀錄與事故資料。相同的比較基礎，也能幫團隊評估供應商選項，而不必把更換 vendor 當成另一次從零開始的導入。

---

## 六、Vendor 管理

Vendor 管理要讓團隊保有選擇，同時看見維持選項的成本。我會把工作分成三部分：

- **準備可驗證的替代方案**：資源允許時，保留一個主力與一個候選 vendor。用相同 eval 檢查候選方案，也記錄認證、工具相容性、資料政策與遷移成本。不能因為有第二個帳號，就認為隨時切得過去。
- **分階段評估 model 變更**：先執行 golden 與 frontier evals，比較通過率、完整成本與新失敗模式。結果可接受，再選擇低風險、可比較的 workload 做 canary；20% 流量、兩週可以是某次試驗的起點，但仍要依事件數與風險調整。只有預定條件通過且回復方式確認可用，才逐步擴大。
- **確認合約與實際設定**：檢查 code、transcript 是否用於訓練，資料與 logs 的保存位置、期限及刪除方式，以及 rate limits、SLA 與計價條件。長期價格承諾還要一起評估最低用量、解約與遷移限制。

替代方案不一定便宜，也不一定需要一直承接正式流量。重點是知道切換需要哪些工作、誰能完成，以及組織是否願意負擔；這樣遇到價格或政策變動時，才能作出實際可行的決定。

---

## 七、系列收尾

回到總論提出的主張，三部曲想保留的是組織理解與改善自己工程流程的能力：

> **Buy the intelligence. Build the environment. Own the feedback loop.**

組織篇「誰來做？」釐清責任與支援；技術篇「Harness 藍圖」建立可操作、可驗證的環境；營運篇則讓團隊持續檢查成果與成本。這三件事需要一起維護，才能讓使用者遇到問題時找得到人，也讓平台知道下一步該改善什麼。

如果現在只能先做三件事，我會選定有 owner 的 pilot、量測可比較的 baseline，並建立前 10 個經過查證的 eval cases。到了檢視時間，再把使用紀錄、人工負擔與品質結果放在一起，決定繼續改善、擴大使用，或停止不合適的流程。時間經過多久不是成果；團隊能說清楚這次嘗試學到了什麼，才是下一個決策的起點。

---

### 系列文章

1. [總論：別急著打造你的 Devin](https://fantasybz.medium.com/%E5%88%A5%E6%80%A5%E8%91%97%E6%89%93%E9%80%A0%E4%BD%A0%E7%9A%84-devin-agentic-engineering-%E7%9A%84%E7%B5%84%E7%B9%94%E7%AD%96%E7%95%A5%E8%88%87-90-%E5%A4%A9%E8%A1%8C%E5%8B%95%E8%97%8D%E5%9C%96-7342ababc417)
2. [一、組織篇：誰來做？Platform + Federation 的組織設計實務](https://fantasybz.medium.com/agentic-engineering-%E4%B8%89%E9%83%A8%E6%9B%B2-%E4%B8%80-%E8%AA%B0%E4%BE%86%E5%81%9A-platform-federation-%E7%9A%84%E7%B5%84%E7%B9%94%E8%A8%AD%E8%A8%88%E5%AF%A6%E5%8B%99-9d9353ef7f3a)
3. [二、技術篇：Harness 藍圖—把系統變成 agent 讀得懂的地方](https://fantasybz.medium.com/agentic-engineering-%E4%B8%89%E9%83%A8%E6%9B%B2-%E4%BA%8C-harness-%E8%97%8D%E5%9C%96-%E6%8A%8A%E7%B3%BB%E7%B5%B1%E8%AE%8A%E6%88%90-agent-%E8%AE%80%E5%BE%97%E6%87%82%E7%9A%84%E5%9C%B0%E6%96%B9-f2a139f5b561)
4. **三、營運篇（本篇）**

---

### References

1. Anthropic — [Effective harnesses for long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)
2. Google — [2025 DORA report: How are developers using AI?](https://blog.google/innovation-and-ai/technology/developers-tools/dora-report-2025/)
3. Stack Overflow — [Agents on a leash: Agentic AI remains mostly monitored at work](https://stackoverflow.blog/2026/05/27/agents-on-a-leash-agentic-ai-remains-mostly-monitored-at-work/)
4. Anthropic — [Demystifying evals for AI agents](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents)

---

### AI 協作說明

本文由筆者提出初步構想與章節架構，文字撰寫由 AI（Claude）協作完成，再經筆者逐節校閱與修訂後定稿。文中觀點與判斷為筆者所持，文責亦由筆者自負。

---

*本文發表於 [Medium @fantasybz](https://medium.com/@fantasybz)。英文版：[English edition](https://fantasybz.medium.com/agentic-engineering-part-3-evals-unit-economics-and-scaling-running-agents-like-a-product-1cb1855a2046)。若你正在把 Agentic Engineering 從 pilot 帶到規模化，歡迎交流。*
