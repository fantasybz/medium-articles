# Backlog：2027 年起的主題候選（2026-09 迴圈）

> 建立於 2026-09-05 的第一圈選題。輸入：`selection.md` 的四個落選候選與排序理由、`.context/research/judged.json` 的評審分數與反方意見、三份 digest（X、社群、arXiv）的缺口／訊號／機會段、以及作者 Notion 摘要的缺口段。這份檔案是狀態機，不是筆記：每個條目都有升級條件與最早月份，每月的 Select 階段重排一次；條目的排序是「有多大機會在下一圈被選上」，不是「多重要」。

## 使用規則

- **狀態**：`候選`（可進下月提案池）、`觀察中`（證據不足，不主動提案，但持續監看）、`插曲`（單篇，不佔主題席位）。
- **升級**：條目列出的「升級證據」任一項出現，就標記日期並進下月提案池，由 judge 重新打分。
- **降級**：連續三個月沒有新證據的 `候選` 降為 `觀察中`；`觀察中` 六個月沒動就刪除（留在 git 歷史即可）。
- **月份**：「最早月份」是依賴關係推出來的下限（哪一篇要先發、哪本書要先讀完、哪個實驗要先跑），不是排程；實際排期由當月 Select 決定。
- **回填**：每月底 `collect.sh medium` 之後，把 10–12 月四篇的 reads／完讀率寫進文末「成效權重」表，供 judge 調整 demand 與 format 的權重。

## 一句話總表

| # | 條目 | 狀態 | 上次評分 | 最早月份 | 一句話 |
|---|---|---|---|---|---|
| 1 | Coding Agent 的爆炸半徑 | 候選 | 34.8（未駁倒） | 2027-01 | 漏洞在 harness 不在 model；寫在 prose 裡的規則不是控制，harness 外的 reference monitor 才是 |
| 2 | 知識流失與維護債 | 候選 | 33.0（原題駁倒，重建） | 2027-01（建議 02） | 吞吐量免費之後，組織付的帳是共同理解與可維護性，agent 一樣都不會幫你補 |
| 3 | Agent runtime 是平台產品 | 候選 | 未評（新） | 2027-02（建議 03） | sandbox fleet、state、memory、agent config as IaC—platform team 的 2027 build list |
| 4 | Skills、Memory 與 Compaction | 候選 | 33.5（未駁倒；context 檔半部已被 11 月吸收） | 2027-03 | context 的第二層治理：skill 准入靠配對實測、memory 當資料庫管、規則在壓縮中蒸發 |
| 5 | Agent 的探索式測試 | 候選 | 未評（新） | 2027-04 | testing 不能自動化—tester 拿 computer-use agent 去「用」agent 做出來的東西 |
| 6 | Model 供應是上游依賴 | 觀察中 | 28.5（讀者錯位） | 2027-03 | 席位、額度、斷線、本地混合—把 vendor 當 dependency 做 SRE |
| 7 | 棕地的設計維度：DDD 與 Event Storming | 候選 | 未評（新） | 2027-05 | 總論與技術篇的 brownfield 三階段之後，agent 在 legacy 上做出來的邊界對不對 |
| 8 | 艦隊不是免費的：multi-agent 拓樸 | 觀察中 | 未評（新） | 2027-05 | 拓樸的影響跟 model 一樣大、coordinator 沒有可量測的好處—社群直覺 vs 實證 |
| 9 | 去技能化 | 插曲 | 未評 | 2027-Q1 | 單篇文化長文，與不確定性共舞的續集 |
| — | 我的 Golden Kubestronaut 之路 ＋ 認證地圖 | 插曲 | — | CNPE 過關後的下一個月 | 不要跟 2026-12 撞 |

---

## 1. Coding Agent 的爆炸半徑：漏洞在 harness，不在 model

**title_zh**：Coding Agent 的爆炸半徑：漏洞在 harness，不在 model

**pitch**：寫在 CLAUDE.md 裡的安全規則是 write-only channel。481 份公開 CLAUDE.md 只有 4.4–16% 的安全規則對應到任何可執行控制（2608.23550）；Claude Code `/compact` 一輪後保留 53% 安全規則、五輪後剩 10%（2608.22752）；harness 組裝 context 時把低權限內容抬成 root—6/6 coding harness、13/13 攻擊目標全中，含三個有自動權限審查的（2608.27299）；12 個真實 harness（含 Claude Code、Codex）被 MessageRole 與 Cross-Scope 兩類 context 提權打到 RCE（2609.01222）；plugin lifecycle hooks 讓 7/7 harness 淪陷、Microsoft Defender recall 0%（2609.03884）。能真正限制爆炸半徑的只有 harness 外面的確定性 enforcement：per-run identity、authorization broker（被攻陷的 sub-agent 可達動作 1.5 vs 8,100，2609.00267）、flow／origin policy（外洩 33%→0% 且 utility 反而上升，2608.22868）、egress 與 audit。三部曲雛形：威脅模型篇（五種入口—context 提權、hook 與 skill 供應鏈、MCP server、repo 內容與測試執行、memory 洗白授權—× blast-radius matrix）→ 控制篇（hook／permission／broker 與 CKS 對照表；敘事主軸是「我技術篇寫的四條 policy 能買到什麼、買不到什麼」）→ 供應鏈與應變篇（skills 自我中毒 20–42%、刪除後仍持續 2608.25776；skill 竊取 32 次呼叫 2608.26733；covert steering 2609.02564；SkillBloat 5–10 倍 token 2608.21929；靜態掃描器繞過 >90% 2607.02357；接 2026-12 應變篇的 runbook）。

**為什麼沒進前三**：與 SRE 幾乎同分（34.8 vs 35.0），取 SRE 是因為作者可信的地盤（OTCA、Kubestronaut、2025 年兩篇觀測性文章）在那邊；反方指出非資安專職作者在資安題目被 CISO 讀者抓到兩處 overclaim 就會傷整個系列。具體的 overclaim：三個「台灣案例」沒有一個是 coding-agent 事故（700 GB 清空是國外故事在 6 反應的 vendor 社團轉貼、Zeabur 是平台入侵、台新原文說「不是 AI 失控，是架構容量設計錯誤」）；2608.27443 的受測者是 113 位非技術使用者、human-in-the-loop 排名第一，不能寫成「人工 approve 不是控制」；2608.28502 平均 ASR 只有 1.21%，47pp 是不同部署窗口的波動不是均值。此外「harness」一詞與系列定義相衝（論文的 harness＝vendor runtime，系列的 harness layer＝你蓋的）。台灣需求訊號偏弱：Claude Taiwan 的 LlamaFirewall 串 4/2/2、700 GB 貼文 6/2；Backend 台灣高分享的是非 agent 事故（台新 184/10/23、Zeabur 103/5/19）。

**動筆前必修**（2026-12 應變篇已預告它是 2027 第一順位，不能再拖）：(1) 總論第一節切分兩層 harness；(2) 第二支柱改成「ask-by-default 讓人工核准退化成 rubber stamp；核准只有在被核准的東西 legible 且有 deterministic 後盾時才是控制」，如實揭露 2608.27443 的非技術受測者與 2608.28502 的 1.21%；(3) 台灣案例改寫成「台灣還沒有公開的 agent 事故，但 Zeabur 的環境變數同倉與台新的容量設計錯誤，正是 agent 拿到 credential 後爆炸半徑會放大的架構前提」；(4) 每篇壓到 8–10 個 anchor，其餘進 References，避免 survey 化；(5) 找一位資安協作者掛名審稿（DEVCORE、或 Backend 台灣寫 zero-trust 系列的作者）。

**升級證據**：台灣出現第一起公開的 coding-agent 事故，且 Backend 台灣的事故解剖貼文 ≥ 100 反應或 ≥ 15 分享；資安協作者確認；Numbat、ClawSentry、Claude Security plugin 之一在台灣企業落地並有人寫心得；2608.28502 或 2608.27299 的後續研究在 Fable 5.x／Astra 世代重測仍成立；OpenAI「德國論壇劫持」事件有正式 post-mortem；Kubernetes pod certificates 或 IdP-managed MCP auth 在企業有採用案例。

**最早月份**：2027-01。若協作者找不到，與第 2 條互換，本條延到 2027-02。

---

## 2. 知識流失與維護債：吞吐量免費之後，組織付的帳

**title_zh**：知識流失與維護債：吞吐量免費之後，組織付的帳

**pitch**：原候選「速度免費之後：規格、團隊與人」被駁倒—規格篇被 2026-11 吃掉，人篇的證據撐不住（21x 是 vLLM／SGLang 在 LLM 熱潮中的專案成長，論文只證明 bot 沒寫那些 PR；2609.03456 是單一公司 N=21 的質性研究）。重建成團隊層的組織篇續集，軸是「知識流失與維護債」，只用硬數據：每 +10pp 免審合併多約 6% 修正性維護（2607.09902）；agent 導入後的架構「改善」是分母效應—smell 絕對數不變、LOC +12.8%（2606.13298）；開發者評他人的 AI code 較難維護（2607.05677）；沒有 committed config 的 agent-first repo 認知複雜度成長兩倍（+53% vs +27%）、73.8% 設定檔 commit 後不再碰（2608.25241）。台灣訊號：DDDTW「用 AI 寫程式越來越順，但過了幾個月打開那段程式，卻有點想不起來它為什麼長這樣」（66 反應，該社團最高）、Kent Beck「AI 時代累積不了的信任」（DevOps Taiwan 91 反應／22 分享）、陳正瑋的 LeSS local optimization「一個人的速度上去了，整個組織對系統的共同理解卻在流失」（52/6/8）。作者第一手材料：`Fb temp`（2026-09-02）那篇軟體腐化草稿，以及 LeSS in Action 講師的回覆；系統思考道場 (13) 兩句：「R1 加班上癮迴路／R2 走捷徑上癮迴路都會產生更多 Legacy Code」、「沒有保存產生這些程式的背景知識、Context」；Meadows／Senge／呂毅 CLP 讀到 60–100%；Kent Beck《The Beauty of Maintenance》80%；Goldratt《絕不是靠運氣》筆記。書錨候選：Beck 或 Meadows；骨架用 CLD（causal loop diagram）或 TOC 的瓶頸遷移。三部曲雛形：維護債篇（no-review merge 的維護債＋分母效應；決策工件是 team-level 的 review 容量政策）→ 決策記憶篇（ADR 進 repo、agent 可讀的 ADR、2026-11 總論 what／how／why 地圖的完整版；ontology-grounded project memory 0.98–1.00 vs vector 6–27%，2608.13662）→ 團隊篇（吞吐量免費之後 Scrum／LeSS 在保護什麼：story 切更小、哪些 ceremony 是共同理解的儀式、FDE 是職位還是症狀）。

**為什麼沒進前三**：原題駁倒；人篇（burnout、中階主管、2027 headcount）是作者最沒有操作經驗的領域，headcount 敘事在 2027-01 也已過季；規格篇讓給 2026-11。

**升級證據**：2026-11 變異篇發布後，讀者對「ADR／決策記憶一節」的回應（留言、分享）超過其他節；`Fb temp` 貼到粉絲團的反應 ≥ 20 或分享 ≥ 5；2607.09902／2606.13298 類型的縱向研究再出 1–2 篇；DDDesign Taiwan 或 DevOps Taiwan 再出現「想不起來為什麼長這樣」類貼文；LeSS／Scrum 社群對 AgileTaipei 09-17 FDE 場的後續討論。

**最早月份**：2027-01（若第 1 條缺協作者則本條先上）；建議 2027-02。不論排哪個月，不寫 headcount 決策敘事。

---

## 3. Agent runtime 是平台產品：sandbox fleet、state、memory 與 agent config as IaC

**title_zh**：Agent runtime 是平台產品：sandbox fleet、state 與 agent config as IaC

**pitch**：技術篇的 sandbox 一節與 2026-12 的「K8s sandbox fleet 一節（標明 1,000 人規模）」都刻意壓縮了同一件事：agent 的工作單位正在離開筆電。Conductor Cloud、Cursor cloud agents on your own infra（auto-scaling machine pools、Mac Mini 上跑 computer use）、Gemini／Claude Managed Agents 一個 API call 給一個 sandbox、`ant apply` 把 agents／skills／memory stores 宣告成 repo 裡的檔案（@ClaudeDevs 09-03，2,149 讚）、Stanford「agent-native Git」checkpoint 整個 run 的檔案／dev server／資料庫／KV cache、Oracle「agent memory 是資料庫問題」、Linear Loops 排程 agent workflow；Kubernetes v1.37 的 HPA scale-to-zero、pod certificates、declarative validation 剛好對上 bursty agent workload；CNCF「AI factory on Kubernetes」與 @K8sArchitect 的四層 agentic stack；serving 側 non-LLM 元件在半數 agentic app 主宰延遲、sandbox 記憶體峰值 28 GB（2608.15127）。作者是這題最過度合格的人：CNPA／CNPE／CBA（Backstage）／Crossplane／Argo／Kyverno 一整年的證照，Notion 承諾的講題「如何構建 Internal Developer Platform」。X digest gap #5、Notion 缺口 #1。三部曲雛形：Sandbox fleet 篇（per-call sandbox、warm pool、scale-to-zero、pod identity、容量與成本模型—技術篇 sandbox 選型表的規模版）→ State 與 Memory 篇（run checkpoint、memory 當 governed database；supersession-aware memory 0.91 vs RAG 0.57–0.59，2608.20685）→ Agent config as IaC 篇（`ant apply` 式宣告、harness pin／diff 承接 2026-12 可靠篇的 change management、Backstage／IDP 把 agent 當 self-service 產品；MCP gateway 第二版—tool 曝露變成檢索，tool token 從 70.1% 的 context 降到 0.8%，2608.23992；Twinkle Hub 把 49,343 個 data.gov.tw 資料集放在一個 MCP server 後面當台灣案例）。

**為什麼沒進前三**：2026-12 已把它壓成一節並明講「留給未來的 agent runtime as platform product」；SLO 要先定義（2026-12）才有東西給 fleet 的 autoscaling 與 error budget 用；它是 build list 不是決策敘事，單獨成月會太「方法清單」（作者完讀率最差的格式），需要一條新的歷史脊椎（CI runner → warm pool 已在技術篇用過）或一本書錨。

**升級證據**：CNPE 過關、Golden Kubestronaut 到手（總論開場的資格）；KubeCon NA 2026-11 出現 ≥ 3 場以 agent sandbox／AI factory／inference on K8s 為題的講題；`ant apply` 或等價的宣告式 agent 資源進 GA；台灣有公司在 DevOps Taiwan、CNTUG 或 Grafana & Friends Taipei 分享「自家 K8s 跑 agent fleet」；Kubernetes v1.38（預計 2026-12）有 agent 相關的 KEP；arXiv `sandbox AND agent AND Kubernetes` 在 2608.15127 之後再出 2 篇以上。

**最早月份**：2027-02；建議 2027-03，讓 2026-12 SRE 的 SLO 詞彙先沉澱。

---

## 4. Skills、Memory 與 Compaction：context 的第二層治理

**title_zh**：AGENTS.md 之後：Skills、Memory 與 Compaction 的實證報告

**pitch**：原候選「AGENTS.md 不會讓 agent 變聰明」（33.5）的 context 檔部分已被 2026-11 總論 §五吸收（2607.27250、2606.20512、2608.25241、2608.11095、2608.21964，命題調弱成「pass rate 對 context 檔不敏感，要配 quality 側指標成對讀」）；skills 供應鏈的資安材料劃給第 1 條。剩下三塊沒人碰：(a) skills 的經濟學—注入「對的」公開 skill 讓 Pass@2 掉 1.3–4.2%、token +72–394%、只在 17–36% 的 skill-project 配對有幫助（2608.23067），對上 ACES 的配對 live trial 72.8% 正向（2608.20614），矛盾的解法是「准入靠配對實測，不靠下載數」；常駐描述吃掉 7.1% 的 200k 視窗（2609.00065）；repo skills 隨 release 悄悄過期，agent 只能維持 29.9–69.7% F1（2608.21964）；SKILL.md 採用率超過 MCP（9/11 vs 8/11，2609.00006）；Claude Code plugin 六個月成長 8.8 倍、Claude 共同撰寫 34.9% 的 commit（2608.28497）。(b) memory 治理—supersession-aware memory 0.91 vs RAG 0.57（2608.20685）、persistent memory 會製造假授權且執行端 98.6% 照做（2609.01836）、Oracle／mem0／Perplexity Brain 的產品化。(c) compaction—`/compact` 一輪 53%、五輪 10%（2608.22752）、壓縮增益不跨任務（2608.31057）、recall trap（2608.14838）。X 訊號：Thariq 砍掉約 80% Claude Code system prompt（33,299 書籤，本窗最高的技術貼文）、Vercel 60B token 蒸餾出的 8 條 AGENTS.md（作者書籤）、Antony Marcano 的 corrective vs prescriptive skills、@wquguru「Fable 5.1 內化了 skills 嗎」。台灣：Backend 台灣 `gh skill install` 串「我近幾個月都交給 claude/codex 自己決定要裝什麼 skill」（24/2/10）、搞笑談軟工「更強的 model 是否需要更少約束」（57/3/11）。交付物：platform team 的 skill 准入 gate（paired eval、token 上限、release 對齊檢查、provenance 欄位）與 compaction-proof 的 typed retention policy。

**為什麼沒進前三**：反方指出原 thesis 講過頭（2607.27250 只有 17 任務／288 run，是「量不到 ≥10–15pp 的效應」不是「不會動」；2606.20512 的 +7.5pp 直接反駁「pass rate 不會動」）；第三部是 compaction／retrieval／memory 三個弱關聯題的拼盤；Compaction Cliff 量在 Sonnet 4.6 上，到 2027 年很可能過時；台灣直接訊號只有兩則；三個候選同時切 skills 材料。被拆走一半後，剩下的份量撐不撐得起一個月要重新驗證。

**升級證據**：作者在自己的 repo 用當時的 Claude Code 版本重跑 Compaction Cliff 的幾個 config，確認機制仍在；skill marketplace 出現第一起公開的供應鏈事故，或 `gh skill install`／agentskills.io 加上簽章與 provenance；2608.23067 vs 2608.20614 的矛盾有第三篇研究裁決；搞笑談軟工「更強 model 更少約束」的討論在 Fable 5.x／Astra 世代再起（作者可先去回那條留言補訊號）；memory-as-database 的產品有台灣使用者心得。

**最早月份**：2027-03（2026-11 吸收的部分要先發布，避免自我重複）。

---

## 5. Agent 的探索式測試：testing 不能自動化，所以 tester 要去「用」它

**title_zh**：Agent 的探索式測試：checking 之外，tester 拿 computer-use agent 去用它做出來的東西

**pitch**：2026-10 總論用 Bach 的 testing／checking 之分把 mutation score、constraint tests、pass^k 都定位成更好的 *check*，探索式測試只給一段。缺的那一篇是：checking 之外，tester 對 agent 產出與 harness 本身的 exploratory testing 長什麼樣—不是讀 agent 寫的測試，是拿 computer-use／browser agent 去操作它做出來的東西、對 harness 做 session-based test management、把 charter 寫成 agent 讀得懂的探索任務、以及人保留哪些探索不外包。X 訊號：a16z 說 computer-use 一年從 42% 到 85%（人類約 72%）、Claude 背景 computer use（11,460 讚）、Chrome DevTools for agents 讓 agent 測自己蓋的 extension（856 讚）、Cursor 在 Mac Mini 上跑 computer-use agents、LayerX QA lead「移動 QA 重心三次」（@TestingGolem）、JSTQB 秋季大會（2026-10-16）與 STARWEST 都以 AI in testing 為軸；Matt Shumer「Astra 預設撐不過一週的 build，要有一個 technique」（3,189 讚／4,947 書籤）是 harness 論點的再現。arXiv：驗證工具的 reach 決定價值—boot probe 用 35% 的成本拿到多數價值、截圖對效能失敗無用（2608.28795）；75.5% 未完成的 run 自稱完成（2608.24979）；同一 agent 加一段 security section，發現 24 vs 51，最嚴重的那個只有人工測到（2608.20963）。作者第一手：Appier E2E reliability 本職、2022 年兩篇《Exploratory Software Testing》讀書筆記（202／67 views）、`Exploratory Testing Guidelines`（2025-07）、待讀 Whittaker《Exploratory Software Testing》與 Hendrickson《Explore It!》、2023 LLST 系列、粉絲團「不是打勾機器，而是資訊的探勘者、風險的照明者」。書錨：Hendrickson《Explore It!》。

**為什麼沒進前三**：2026-10 已佔掉測試主題的席位，半年內不宜再有測試題；computer-use agent 當 E2E substrate 的成熟度與成本（$6–8／小時）還在變；作者的探索式測試待讀清單還沒讀完。

**升級證據**：2026-10 發布後讀者對「探索式測試一段」的回應；作者在工作上用 computer-use agent 跑過至少一輪 exploratory session 並有數據（找到的 bug 數 vs 人工 charter、成本）；JSTQB 10/16 或 STARWEST 出現「exploratory testing with agents」講題；Whittaker／Hendrickson 讀完；computer-use 定價下降到可日常使用。

**最早月份**：2027-04（與 2026-10 隔半年）。

---

## 6. Model 供應是上游依賴：席位、額度、斷線與本地混合

**title_zh**：Model 供應是上游依賴：把 vendor 當 dependency 做 SRE

**pitch**：原候選「別用座位數編 2027 預算」（28.5）。結構論點站得住—seat 不是成本單位而是單點故障；把 model 供應當成會斷、會被 ban、會漲價的上游依賴來管，有 SLO、有 fallback、有本地選項—但證據全在個人層：Claude Taiwan 的 340／103／91 反應三串（Cowork VM 佔 10 GB、Pro 之外再租哪家、Max 20x 每週用完 Fable）、兩個帳號同時報銷「只能用 Codex 來擋」、被 ban 資料在裡面、USD 100 credit 到期歸零、共用 key 觸發反劫持每 30 分鐘登出。反方建議的重切：一、韌性篇（vendor-as-dependency 的 SLO／error budget、多 vendor failover runbook、憑證衛生、資料出口、營運篇四件事之外的合約條款）；二、本地與混合篇（vLLM、K8s v1.37 scale-to-zero、CNCF AI factory 的 GPU 配額與租戶隔離、Perplexity 式雲→本地交接、27B model 跨 scaffolding 139 倍成本差 2608.08654、Twinkle Hub／OpenFormosa／APMIC 生態、資料駐留對照表—作者 NCA-AIIO、NIM labs、「Sizing LLM Inference Systems」筆記在這裡）；三、Token 流向篇（scaffolding 139 倍、tool schema 70.1%→0.8%、skills +72–394%、boot probe 35%、explorer model 省 84–95% token 2608.29675、manager-worker $11.71 vs $61.11 2608.26480、Databricks 用 gateway tracing 一小時找到 $1.2M／年的浪費、每月 cost audit checklist—營運篇 §三的續集，也就是 X digest gap #3 的 practitioner cost playbook）。2026-12 可靠篇只留一句「vendor outage 是 run availability 的 infra_failed，從 budget 排除、另開 vendor SLI」，其餘全在這裡。

**為什麼沒進前三**：讀者錯位—目標讀者買 Team／Enterprise seat 或走 Bedrock／Vertex API，個人 Pro／Max 痛點多半不成立；「台灣團隊的 agent 算力是一堆座位」在四份研究檔中沒有企業層佐證；作者地盤不含採購與 CFO 敘事；額度數學押在 Anthropic 當下的方案機制上，兩個月就過時；四個名詞並列、韌性篇塞了兩篇的量。

**升級證據**（第一項缺一不可）：3–5 家台灣公司的企業層採購型態觀察（可匿名：Team／Enterprise seat vs API vs 混合、額度政策、fallback 有無）；Grok Memphis（09-03）等級的 vendor outage 再發生且有台灣團隊公開影響；美國出口限制或主權模型政策有具體法規動作（Twinkle AI 35 反應那條的後續）；vLLM 台北 meetup 第二場以上、Twinkle Eval 有企業使用案例；Claude Taiwan 以外的實務社團（DevOps Taiwan、Backend 台灣）出現席位／額度討論。

**最早月份**：2027-03（對準 2027 Q1 採購複審；2026-10／11 的預算季已錯過）。狀態：觀察中。

---

## 7. 棕地的設計維度：用 DDD 與 Event Storming 讓 legacy 對 agent 可讀

**title_zh**：棕地的設計維度：用 DDD 與 Event Storming 讓 legacy 對 agent 可讀

**pitch**：總論 §七與技術篇 §七都給了 brownfield 三階段（可驗證 → 可觀測 → 可約束），2026-11 量的是結構變異，但沒有一篇教「設計」這個維度：agent 在 legacy 上做出來的東西，邊界對不對、模型對不對。DDDesign Taiwan 是資料集裡貼文數最多的實務社團（26 篇）：Kim Kao 用多 agent 從 legacy 抽 bounded context，每次數量不同（16/3）；水球潘 DDDTW 2025「沒有 DDD 的 BDD 無法支撐自動化；沒有 BDD 的 DDD 也無法驗證規格」（20/4）；Tom Smith「有討論 DDD + Vibe Coding 的社群嗎？」（6 反應／10 留言）；Eric Evans「DDD & LLMs」（23/4）；ezKanban 學生從 Event Storming 便利貼到 Use Case Spec 再進 Pattern Language skills（124/9，台灣軟體工程研討會最佳 demo）；DevOps Taiwan Meetup #80「與 Coding Agent 在棕地專案中可靠協作」；Backend 台灣 Triton Ho 的 event-based 架構（125/13/12）。arXiv：VB6 → C# 現代化平均 70% 等價，高複雜度功能花 6 倍 token 只有一半等價（2608.28972）；一人小隊在 brownfield 的綁束是規格品質與機構知識（2605.18461）；ontology-grounded project memory 0.98 vs vector 6–27%（2608.13662）；coupled facts 的可得性而非距離決定成敗、harness 為同樣的事實付十倍 token（2608.16630）。作者第一手：事件溯源與 CQRS 實作班（陳建村）70%、DP2 設計模式課（2022）、待讀 Evans／Vernon／Brandolini、Teddy 工作坊的 Product Aggregate 練習與「event-sourcing replay 從未被測到」的診斷（2026-10 已用）。三部曲雛形：邊界篇（agent 抽 bounded context 的變異怎麼量；Domain Storytelling／Event Storming 當 agent 的輸入）→ 現代化篇（legacy 遷移的 token／等價曲線；characterization tests 之後的下一步）→ 設計記憶篇（ADR、ontology memory，與 2026-11 契約篇、第 2 條決策記憶的接口）。

**為什麼沒進前三**：需要作者先讀完 DDD 書單；與 2026-11 變異篇（Kim Kao 訊號）和第 2 條（決策記憶）的接縫要先切清楚；DDD 社群雖活躍但單篇反應偏低（多在 6–25），分享才是這群人的指標。

**升級證據**：Kim Kao 或 DDD Taiwan 年會出現 agent + DDD 的正式講題並被分享 ≥ 10；作者讀完 Evans 或 Brandolini 並有讀書筆記可當書錨；2026-11 變異篇的 Kim Kao 段落引來 DDDesign Taiwan 的討論；2608.28972 類型的 legacy 現代化案例再出 1–2 篇。

**最早月份**：2027-05。

---

## 8. 艦隊不是免費的：multi-agent 拓樸的實證

**title_zh**：艦隊不是免費的：multi-agent 拓樸的實證

**pitch**：三個月的主題都沒碰的一塊。Claude Taiwan 的「艦隊模式」（兩名審查代理證實／證偽、一名架構代理防過度設計、一名總監工，21 讚）與 Uncle Bob 的 squad harness（leader 之下 analysts、reviewers、Gherkin authors、implementers、hardeners，2,064 讚／1,696 書籤）是社群的直覺；arXiv 的實證卻不客氣—拓樸的影響跟 model 一樣大（10 種拓樸、100 run，分數差 >30、wall-clock 2 倍，管得太緊反而變差，2607.27877）；指定 coordinator 沒有可量測的好處，共用檔案在八個 agent 時省 42% output token（2608.16801）；manager-worker 幫某些 model +20–30pp、傷另一些 −1 到 −9pp，token 三倍（2608.26480）；共用上游 telemetry 的 agent quorum 故障域是 1（2609.02925）；失敗的多 agent 軌跡重跑只有 6.9% 修好（2608.25920）；異質配對找到更多缺陷 69.8% vs 53.1%（2606.14445，2026-10 已用一半）。決策工件：拓樸選型表（pipeline／manager-worker／peer／quorum × 什麼時候值得）與「艦隊的 token 帳」。

**為什麼沒進前三**：2026-10 Review 篇已用掉 reviewer agent 艦隊與異質配對；除此之外台灣訊號只有一則 21 讚的留言；證據多為實驗室 benchmark（LiveCodeBench、from-scratch 專案），與 model 版本強耦合，半年後可能翻轉；作者沒有營運過多 agent 拓樸的第一手數據。

**升級證據**：作者 2026-11 變異實驗的三組延伸出「單 agent vs manager-worker」的第四組並有數據；`ant apply` managed agents 或 Omnigent 類 meta-harness 讓多 agent 拓樸變成可 diff、可 eval 的設定檔；台灣團隊在社團公開艦隊模式的成效（不只是「怎麼設」）；2607.27877／2608.16801 類研究在生產 repo（非 from-scratch）重現。

**最早月份**：2027-05。狀態：觀察中。

---

## 9. 去技能化：當 agent 代替思考，工程師如何保住知識主權（單篇）

**title_zh**：去技能化：當 agent 代替思考，工程師如何保住知識主權

**pitch**：Teddy 工作坊 Day 1 的開場（定義、三個原因、三個後果、podcast「去技能化 2.0：當 AI 代替思考，專業人士如何失去知識主權？」）、Bach 的 rapid learning、LeSS 對團隊學習的堅持、Kent Beck「90% of My Skills Are Now Worth $0」（作者粉絲團 16 反應／20 分享）、Addy Osmani「expertise 才是 prompting skill，有時人才是瓶頸」、Andrew Ng 三張 skills map（合計 88k 書籤）、SDD 課堂「交得更多、懂得更少」（2608.30572）、「de-democratisation：改變的是控制不是取用」（2608.24720）、一年後的五類心理成本（2609.03456，只當佐證）。這是文化長文而不是三部曲—與不確定性共舞（619 views／98 reads，2025 年中文最高 views）的續集，hook 會傳播但完讀率低（16%），所以要在前三分之一就給決策工件（junior 的 review-trained pipeline 續篇、哪些技能刻意不外包、團隊學習的 ceremony）。

**為什麼沒進前三**：不是主題格式（單篇）；人篇證據被反方判為撐不住；作者是 Senior IC，寫 headcount 與中階主管會像聽來的—所以只寫工程師個人與團隊學習，不寫組織人事。

**升級證據**：2026-11 發布後 Teddy 或搞笑談軟工對去技能化一段的回應；「去技能化 2.0」podcast 或 Teddy 的 18k 字論文正式發表；2608.30572 類的教育研究再出；粉絲團貼 Kent Beck 類貼文分享數再破 20。

**最早月份**：2027-Q1 任一月當插曲（不佔主題席位；可作為粉絲團導流的長文）。

---

## 插曲（不佔主題席位）

- **我的 Golden Kubestronaut 之路 ＋ agentic platform engineer 的認證地圖**。Notion 學習計畫承諾的 capstone；LinkedIn 認證貼文動輒 100+ 反應（CKA pass 112 反應／32 留言），2025 年標題含「認證」的 CNCF 文完讀 34%；Claude Certified Architect 五大 domain 對到 harness 藍圖、Ana Pedra 的 Golden 路線圖、CNPE 情境題對到 2026-12 三部曲。條件：CNPE 第二次過關。排期：過關後的下一個月，作為該月主題之外的單篇；**不要跟 2026-12 撞**。
- **`Fb temp` 軟體腐化貼文**（2026-09-02 草稿）：2026-10 貼粉絲團，當 2026-11 drift gate 與第 2 條的預告；它的反應數就是第 2 條的升級證據之一。

## 已被 10–12 月吸收、下圈不要再提的訊號

| 訊號 | 去了哪裡 |
|---|---|
| Review 容量、reviewer agent 艦隊、AI 審 AI、社交工程 PR（X gap #2、社群機會 #3） | 2026-10 Review 篇 |
| 審 agent 寫的測試、mutation gate、TDD 儀式、Bach 書錨（X gap #1、社群機會 #1、#12） | 2026-10 測試篇＋總論 |
| Evals from traces、reward hacking、escalation tool、judge 盲點（X gap #6） | 2026-10 可靠度篇（judge、pass^k）與 2026-12 觀測篇（eval-in-prod） |
| Teddy 的可重現性、Kim Kao 變異、spec 當輸入契約、Example Mapping（社群機會 #2、#7） | 2026-11 全部 |
| AGENTS.md 對 pass rate 不敏感、rationale 註解、skills 過期（arXiv signal #4 的 context 檔半部） | 2026-11 總論 §五 |
| OTel GenAI semantic conventions、AIOps bot、flight recorder、誰核准了 PR（社群機會 #6、arXiv cluster G） | 2026-12 全部 |
| Harness pin／diff、28%→49%、每天兩版（arXiv signal #2） | 2026-12 可靠篇 |
| K8s v1.37 sandbox fleet | 2026-12 一節；完整版在第 3 條 |
| Vendor outage／額度 | 2026-12 一句；完整版在第 6 條 |
| Skills 供應鏈資安（EVOMAL、skill 竊取、covert steering、SkillBloat） | 第 1 條；2026-11 明講不碰 |
| Agentic commerce／headless SaaS、WebMCP（X 小節） | 不在讀者範圍，不列 |

## 訊號監看清單

每月 1 日 `collect.sh` 與 `prompts/arxiv.md` 的輸入。格式：看什麼 → 出現什麼算訊號 → 影響哪一條。

**X 帳號**

1. @unclebobmartin、@martinfowler（含 Böckeler、Rachel 的轉發）— 測試／review／harness 的立場文；一則破 2,000 讚，或 Fowler 轉發「TDD in the agent loop」的後續實驗 → 第 5 條、2026-10 的回響。
2. @trq212、@ClaudeDevs、@claudeai — Claude Code 的 Function Hooks、`ant apply`、Security plugin、`/compact` 與 permission 機制的變更；任何改變 compaction 或 permission 行為的 release → 第 1、4 條要重測數字。
3. @perplexity_ai（Numbat）、@Docker（Manufacturing Trust）、@allenown（DEVCORE）— agent detection & response、agent identity；台灣資安圈第一篇 agent 事故分析 → 第 1 條升級。
4. @charlieholtz／@conductor_build、@mattyp（Cursor cloud agents）、@K8sArchitect、@kubernetesio、@CloudNativeFdn — sandbox fleet、AI factory、v1.38 → 第 3 條。
5. @dexhorthy、@hwchase17／@Vtrivedy10、@ArtificialAnlys — SlopCodeBench、tuned evaluators、reward-hacking 修正的新一輪 → 2026-10 回響與第 8 條的拓樸 eval。
6. @minorun365、@TestingGolem、@jassttokyo／@JSTQB_PR — 日本企業導入與 QA 重心移動；JSTQB 秋季大會（2026-10-16）議程 → 第 5 條。
7. @OracleDevs、@himanshutwtxs（mem0）、@akshay_pachaar — memory as database、agent-native git、harness 效率 → 第 3、4 條。

**LinkedIn**

8. Alolita S.（OTel GC）與 OTel GenAI SIG — semantic conventions 從 development 進 stable 的時點 → 2026-12 引用要更新；Kim Wüstkamp（killer.sh）CNPE 課程、Ana Pedra 的 Golden 路線圖 — 作者 CNPE 過關後認證貼文的反應 → 插曲排期。

**arXiv 查詢字串（在 `prompts/arxiv.md` 現有 20 組之外追加）**

9. `"privilege escalation" AND (harness OR "coding agent")`、`skill AND ("supply chain" OR poisoning) AND agent`、`"reference monitor" AND agent` → 第 1 條；追蹤 2608.27299、2609.01222、2608.28502 在新一代 model 的重測。
10. `("technical debt" OR maintenance OR "code quality") AND "coding agent" AND (longitudinal OR "post-merge")`、`"architectural decision" AND agent AND memory` → 第 2 條（2607.09902、2606.13298、2608.13662 的後續）。
11. `(sandbox OR "agent runtime" OR "internal developer platform") AND Kubernetes AND agent`、`"agentic workloads" AND serving` → 第 3 條（2608.15127 的後續）。
12. `(compaction OR "context window" OR "working memory") AND "coding agent"`、`"agent skills" AND (evaluation OR staleness OR provenance)` → 第 4 條（2608.22752、2608.23067 vs 2608.20614 的裁決）。
13. `("exploratory testing" OR "computer-use agent" OR "GUI agent") AND (testing OR QA)` → 第 5 條；`"multi-agent" AND (topology OR coordination) AND "software engineering"` → 第 8 條；`("domain-driven design" OR "bounded context" OR "event storming") AND LLM` → 第 7 條；`(deskilling OR "skill atrophy") AND developers AND AI` → 第 9 條。

**Facebook 社團（保留在 `FB_GROUPS`；括號內是該社團的有效指標）**

14. Backend 台灣：分享數 ≥ 15 的事故／資安解剖 → 第 1 條。搞笑談軟工：Teddy 的 pattern language、LOC 變異、去技能化、18k 字論文 → 2026-11 回響、第 7、9 條。DDDesign Taiwan：Kim Kao、DDD Taiwan 年會、DDD + agent 討論 → 第 7 條。DevOps Taiwan：陳正瑋、棕地／FDE meetup 後續、莊硯光 → 第 2、3 條。Scrum Community in Taiwan 與 Agile 內湖：DavidKo 測試貼文的反應是否從個位數升高 → 2026-10 回響；FDE → 第 2 條。Twinkle AI：MCP Hub、vLLM 台北 meetup、主權模型 → 第 3、6 條。Claude Taiwan 只當第 6 條的症狀計數器，不當主證據；GCP & K8s、OpenClaw ×2、Antigravity 連續兩個月只有雜訊，從 `FB_GROUPS` 拿掉。

**會議與日期**

15. JSTQB 秋季大會 2026-10-16（AI in testing → 第 5 條）；STARWEST（每年 9–10 月，確認 2026 日期 → 第 5 條）；KubeCon + CloudNativeCon NA 2026-11（確認日期，數 agent／AI factory 議程 → 第 3 條、2026-12 引用）；Kubernetes v1.38 預計 2026-12（agent 相關 KEP → 第 3 條）；DDD Taiwan 年會（往年 Q4，確認 2026 日期 → 第 7 條）；DevOpsDays Taipei 與 KCD Taipei（確認 2026–27 日期 → 第 3 條）；AgileTaipei 2026-09-17 FDE 場的事後貼文（→ 第 2 條）；Twinkle AI／vLLM 台北 meetup 第二場（→ 第 6 條）；作者自己的 CNPE 第二次考試（→ 插曲排期與第 3 條）。

## 成效權重（每月底回填）

已知基準（`style_brief.md` reception 段）：2025 年中文長文完讀 27%、英文 8%；書評型 46–51%（建築、XP）、方法清單型 9–24%（雙層護欄、觀測反模式）、文化型 hook 會傳播但完讀 16%（與不確定性共舞 619 views／98 reads）；views 超過 presentations 的週都是粉絲團分享的週。對 backlog 的含意：有書錨的條目（第 2 條 Beck／Meadows、第 5 條 Hendrickson、第 9 條）在 format 分項加分；純 build list 的條目（第 3、4 條）要找到歷史脊椎或書錨才提案。

| 月份 | 主題 | 中文 views／reads／完讀 | 英文 views／reads | 粉絲團分享 | 對 backlog 的調整 |
|---|---|---|---|---|---|
| 2026-09 | Agentic Engineering 三部曲 | 29／11／38%（發布 4 天） | 7／2 | 尚未貼 | — |
| 2026-10 | 綠燈不是驗收 | | | | |
| 2026-11 | 同一份規格，跑十次 | | | | |
| 2026-12 | Agent 的 SRE | | | | |
