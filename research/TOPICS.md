# 研究與主題總覽

整理日期：2026-10-04。主題庫的研究訊號主要截至 2026-09-15；系列進度依最新 main 的發布紀錄與本次 Medium 讀回更新。「同一份規格，跑十次」四篇中文已排程，英文主寫遇 Claude 週額度限制，尚未成稿。各份研究紀錄均附查閱日期；外部來源的內容與版本以該日期為準。

目前有 **3 個系列已有中文正文**（一個已發布、兩個已排程；規格變異系列的英文版仍待完成）、**1 個系列已有大綱、尚待成稿**，以及 **14 個編號主題**（9 個候選、4 個觀察中、1 個單篇插曲）。另有 3 個未編號插曲、1 則貼文草稿，以及 3 個較小的研究方向。候選主題的月份是原計畫的最早下限，尚未排程；已排程也不等於已公開。

## 系列與進度

四個系列的順序是：先建立組織與 harness，再驗證 agent 的產出，接著量測同一份規格的實作變異，最後處理 production 營運與追責。各系列篇數依材料決定：《綠燈不是驗收》已擴為總論與四篇，其他系列目前採總論與三篇；中英文的完成狀態分開記錄。

| 系列 | 核心問題與篇章 | 工作區可確認的進度 | 接續入口 |
|---|---|---|---|
| Agentic Engineering | 誰來做、系統怎麼建、如何營運？總論／組織／Harness／Eval 與單位經濟 | 四篇中英版，共八篇，均有正式發布紀錄；首次發布在 2026-09-01～09-05 | [文章清單](../README.md#articles) |
| 綠燈不是驗收 | 怎麼知道 agent 做對了？總論／測試／Review／可靠度／付款實作 | 五篇中英正文與發布包齊全，十份已排程於 2026-10-06～11-05；付款實作篇已納入主系列 | [總論](../2026-10-green-overview/article.md)、[測試篇](../2026-10-green-testing/article.md)、[Review 篇](../2026-10-green-review/article.md)、[可靠度篇](../2026-10-green-reliability/article.md)、[付款實作篇](../2026-10-green-payment/article.md)；[發布佇列](../PUBLISHING.md) |
| 同一份規格，跑十次 | 規範、驗收與方法比較各缺什麼證據？總論／規格／契約／變異 | 40 次正式生成、四篇 Claude Code max 中文主稿與後續潤飾已完成。10/04 合併 main，四篇中文已排程於 11/10～12/01，遠端全文與設定已核對。英文版因 Claude 週額度限制尚未成稿或排程 | [四篇原稿](../README.md#articles)、[發布核對](2026-10/same-spec-ten-runs/publication-2026-10-04.md)、[成稿狀態](2026-10/same-spec-ten-runs/manuscripts/STATUS.md)、[實驗入口](experiments/same-spec-ten-runs/README.md) |
| 把 Agent 當 Production Workload：Agent 的 SRE | 如何觀測、維持可靠度並追責？總論／觀測／可靠／應變與追責 | 原規劃 2026-12；2026-09-15 已重切大綱，本工作區未見系列正文、真實 trace 或 ledger 實作成果 | [新版大綱](2026-10/2026-12-sre-for-agents.md)、[新版圖稿](2026-10/2026-12-sre-for-agents.figures.md)、[發布與推廣計畫](2026-10/2026-12-sre-for-agents.publish.md) |

**目錄月份不能拿來判定發布狀態。** `2026-10-agentic-harness-blueprint/` 與 `2026-11-agentic-eval-economics/` 都屬於已在 9 月發布的第一個系列；`research/2026-10/` 則是 9 月中做的期中研究加圈。正式發布與排程以各篇 `PUBLISHED.md` 和 `PUBLISHING.md` 為準。

## 已排程與尚待成稿系列的後續工作

### 同一份規格，跑十次

2026-09-25 的[研究大綱](2026-10/2026-11-same-spec-ten-runs.md)保留正式研究設計的歷史骨架；目前寫作入口改採[9/28 全面重寫計畫](2026-10/same-spec-ten-runs/rebuild-2026-09-28/rewrite-plan.md)與[研究目錄](2026-10/same-spec-ten-runs/rebuild-2026-09-28/README.md)。全系列統一使用本 repo 的真實 `codex_jsonl.py` 修補任務；原本 Go／Java 範例與獨立付款案例都退出正式設計。

| 項目 | 目前狀態與證據 |
|---|---|
| 二審意見 | 29 項原評審已逐項處置，另納入方法問題；見[修訂對照](2026-10/same-spec-ten-runs/review-resolution.md) |
| 來源查證 | 前輪核讀 5 份原站全文，撤回「首次量測」，區分成本 spread、結構指標與 paired score；見[前輪證據表](2026-10/same-spec-ten-runs/evidence-audit.md)。9/28 全面重寫所補的研究、來源台帳與教學材料另存[本輪研究目錄](2026-10/same-spec-ten-runs/rebuild-2026-09-28/) |
| 可執行實驗 | [研究程式與協議](experiments/same-spec-ten-runs/README.md)固定來源 commit、四份以共同規範為基準的文件、外部評測、隔離 probe、完整名額與分析程式 |
| Pilot | 2 次已完成，均通過 103 個驗收檢查；與正式 40 次完全分開，不當成介入效果 |
| 正式測量 | 40 次完成；四組各 10/10 通過、各 10 種正規化 AST；各組 95% 區間 69.15%–100%，不構成等效或高可靠度證據。見[正式結果](experiments/same-spec-ten-runs/RESULTS.md) |
| 中文全文與發布 | 9/28 Claude Code Opus 5.5 max 主寫、10/03 依試讀意見潤飾。10/04 最新八份正文／貼稿通過 strict zh-TW MCP，0 錯誤、0 警告；四篇中文已建立 Medium 排程並核對全文、連結與 29 張圖。英文版維持 max 主寫，尚待額度重置後續作 |
| 解釋範圍 | 真實 repo 的單檔、tool-free 生成案例；不推論 native skills／完整 agent loop、人類維護成本或 production 擴權 |

原研究排程保留在歷史檔；正式 40 次的完成證據以研究設計、名額與結果紀錄為準。中文已排程為 11/10、11/17、11/24、12/01，每週二臺北時間 09:00；英文規劃為同週四，但尚未建立 Medium 草稿與排程。各項完成證據與待辦見[10/04 發布紀錄](2026-10/same-spec-ten-runs/publication-2026-10-04.md)。

### 把 Agent 當 Production Workload：Agent 的 SRE

新版將重點轉向 **flight recorder 與 accountability**：用 trace 協助除錯，讓受保護的事件帳本支撐結果驗證與追責。總論與三篇深掘只交付以下三個實作成果；runbook、postmortem 與 K8s fleet 容量表已降為示意或後續題目。

| 實作成果 | 用途 | 尚待取得的證據 |
|---|---|---|
| A1：trace schema + OTel Collector config | 串接一次 agent run 的執行紀錄 | 真實 run trace、Jaeger 截圖、vendor 原生 telemetry 可取得欄位的實查 |
| A2：`agent-slo.yaml` | 定義可獨立驗證的結果、SLI、error budget 與處置 | 28 天 revert 基線、成本與介入量測、burn-rate 與最小事件數驗算 |
| A3：ledger-backed attestation status check | 核對執行證據、核准者與被核准的 commit | 可查詢的 append-only ledger、agent 能否修改 hook／紀錄的實測、review event 與 commit 的對應 |

原計畫要求 **9 月底前收齊 Amsterdam 的公開投影片／錄影等材料**，10 月第一週開始儀表化，並與「同一份規格，跑十次」共用實驗 repo。另須在動筆前重查 OTel GenAI semantic conventions，避免把研究時的草案狀態寫成現行標準。詳見 [新版大綱](2026-10/2026-12-sre-for-agents.md)「寫作前要補的證據」。

原計畫的退場條件是：**10/31 若仍沒有真實 run trace 與可查詢的 ledger，就縮成總論、觀測、可靠三篇，應變與追責篇順延。** 發布檔列出的 12 月日期仍是規劃；英文總論是否保留 12/02 的例外日期，也在[發布計畫](2026-10/2026-12-sre-for-agents.publish.md)列為待決。

## 收集中的主題庫

以下狀態、順序與最早時間沿用 [2026-10 backlog](2026-10/backlog.md)，沒有重新評分。`#` 是固定編號，並非順位；兩個表分別保留候選與觀察中條目的原相對順序。「補證據」欄只摘錄適合接續的條件，完整升級條件仍在 backlog 各節。

### 候選：9 題

| # | 主題 | 已收集的切入點 | 接續補證據 | 原最早時間 |
|---|---|---|---|---|
| 1 | Coding Agent 的爆炸半徑 | harness 外的權限控制、工具供應鏈與執行邊界 | 資安協作者審稿、可重現的防禦實驗；與 identity 題切分範圍 | 2027-01 |
| 4 | Skills、Memory 與 Compaction | skill 准入與配對評估、記憶寫入治理、壓縮後規則保留 | 在自己的 repo 做 skill 有／無配對測試，重跑 compaction 實驗 | 2027-03 |
| 3 | Agent runtime 是平台產品 | sandbox fleet、持久化工作區、state／memory、config as IaC | 企業實作或自己的平台實驗，補上書籍主軸；先接續 SRE 的 SLO 定義 | 2027-02，原建議 03 |
| 2 | 知識流失與維護債 | 維護成本、ADR／決策記憶、團隊共同理解；Beck／Meadows 書錨 | 更多縱向研究、團隊案例、軟體腐化貼文與規格系列的讀者回應 | 2027-01，原建議 02 |
| 10 | Agent identity 與委派授權 | principal、逐一撤銷權限、委派鏈；東京授權議題與 workshop | 公開規格或第二個 IdP 實作、企業採用案例 | 2027-02 |
| 8 | 多 agent 的實證帳 | 從拓樸選型轉向獨立證據來源、共用故障與 token 成本 | 自己的單 agent／manager-worker 比較，或軟體工程情境的重現研究 | 2027-04 |
| 5 | Agent 的探索式測試 | tester 使用 computer-use agent 探索產品；《Explore It!》與語音測試案例 | 一輪有紀錄的 exploratory session、補閱讀、取得可重現的公開範例 | 2027-04 |
| 11 | MCP 生態的可用性 | 公開 MCP server 的存續、維護成本與付款機制 | 回原論文核對投影片數字；第二次生態普查或真實依賴事故 | 2027-03 |
| 7 | 棕地的設計維度：DDD 與 Event Storming | legacy 的領域邊界、現代化與設計記憶 | 本圈首次沒有新訊號，仍列候選；若原定 2026-11、12 兩圈仍無新證據，降為觀察中；監看須跟進 DDDesign Taiwan 的 Discord 遷移 | 2027-05 |

最近一圈的四筆變動是：Skills 題的順位上升；多 agent 題從「觀察中」升為「候選」，研究問題改為證據是否獨立；新增 #10～#14 五題；DDD 題記錄第一次沒有新訊號，開始追蹤降級條件。**#1 爆炸半徑與 #10 identity 在原 backlog 被列為同季擇一**，接續選題時要先解決重疊；#1 若缺資安協作者，原規劃由 #2 維護債題先上。

### 觀察中：4 題

| # | 主題 | 已收集的方向 | 何時值得升級 | 原最早時間 |
|---|---|---|---|---|
| 6 | Model 供應是上游依賴 | 額度、斷線、本地混合；可重切為 harness 的模型可攜性 | 3～5 家台灣公司的企業採購觀察，或同一 harness 跨至少 3 個模型的比較，含一個地端模型 | 2027-03 |
| 12 | MCP task lifecycle 與長時間工作 | 長時間 tool／task 的完成、取消、觀測與 SLO | 不同公司的第二個生產案例，或規格定案與多個實作 | 2027-02 |
| 13 | 碳與成本感知的 agent 工程 | 有界重試、right-sizing、每任務成本上限 | 第二家公司的量測，或作者自己的成本 SLI 資料 | 2027-Q2 |
| 14 | 日本作為需求訊號 | 日文社群、書籍、活動與跨語言讀者假說 | 實際日本讀者來源與回應；目前材料只足以提出假說 | 2027-Q2 |

### 單篇插曲與貼文

| 主題 | 素材與狀態 | 原接續條件 |
|---|---|---|
| #9 去技能化：工程師如何保住知識主權 | 文化長文方向，《與不確定性共舞》的續篇；已有習慣化與學習相關材料 | 原規劃 2027-Q1 任一月當插曲；補讀者回應或重現研究，不佔每月系列席位 |
| 東京現場筆記：AGNTCon + MCPCon Japan 給台灣讀者 | 會議摘要已整理，原始逐場筆記另存本機；本工作區尚未見成稿 | 09-15 原建議先分享已發布的 Agentic Engineering 系列，再於 10 月上旬寫五到七個具體機制；須重估時效，並避開既有系列的排程 |
| PSTN、語音與物理世界的動作空間 | 語音 agent 測試 harness、六個工具與阻塞整通電話的 server | 原最早 2027-Q2；先確認公開 repo，才有可重現的範例 |
| 我的 Golden Kubestronaut 之路＋認證地圖 | 學習計畫與認證素材的成文規劃 | 以 CNPE 過關為條件；研究紀錄未提供通過結果，SRE 新版計畫要求排到 2027-01 以後 |
| 軟體腐化貼文（`Fb temp`） | 原紀錄為社群貼文草稿，可支援維護債題 | 原計畫 2026-10 貼粉絲團；截至 09-15 的研究紀錄仍未發布，後續反應可回填 #2 的需求證據 |

東京插曲的時效判斷來自 09-15。原 backlog 列出的 Amsterdam 日期 09-17～18 已早於本次整理日，下一個會議節點是 San Jose 10-22～23；若仍要寫，需重新判斷切入點，並避開已排程的 10/06、10/08 等系列文章。

### 尚未進入編號清單的小題目

[東京會議摘要 §9.2](2026-10/conference_digest.md) 另保留三個較小的方向，尚未形成系列計畫或發布安排：

| 方向 | 收集的問題與可能用途 |
|---|---|
| Generative UI／A2UI | 介面到執行時才產生，要怎麼定義斷言與驗收？原摘要將它視為尚未被測試方法充分涵蓋的輸出類型 |
| 自主瀏覽器／WebMCP | 瀏覽器原生工具介面與 agent 動作空間；09-05 曾因讀者範圍不合而不列，期中會議摘要又收為小候選。原 backlog 列 11/17 試用到期、未續期就刪除，後續需重查狀態 |
| 以驗證為先的 AI for Science | 會議中的跨領域案例，可補充 testing／verification 的討論，尚未升成獨立主題 |

摘要同段的「tool economics as availability risk」已併入 #11 MCP 生態的可用性，不另外計為一題。

## 已收集材料，到哪裡找

| 材料 | 範圍與用途 | 檔案 |
|---|---|---|
| 第一輪 X 摘要 | 2026-07-20～09-04；355 則去重貼文，整理 testing、review、harness、context、成本、資安、runtime 與組織訊號 | [2026-09/x_digest.md](2026-09/x_digest.md) |
| 期中 X 摘要 | 2026-09-01～09-14；398 則去重貼文，另有會議搜尋材料；與第一輪有重疊，兩輪筆數不直接相加 | [2026-10/x_digest.md](2026-10/x_digest.md) |
| 第一輪 arXiv | 2026-05-01～09-05；十個主題群，涵蓋 harness、context、MCP、資安、eval、review、觀測、成本、規格與組織 | [2026-09/arxiv.md](2026-09/arxiv.md) |
| 期中 arXiv | 2026-09-01～09-15；補強 observability、SLO、accountability、skills 與授權。`*` 表示讀完摘要，`**` 表示讀完 PDF（僅 2608.23610）；查詢計數來自搜尋介面，零命中不等於沒有研究 | [2026-10/arxiv.md](2026-10/arxiv.md) |
| 東京會議摘要 | AGNTCon + MCPCon Japan 2026-09-10～11；場次、投影片／時間碼、十五個機制、系列插入點與新題目 | [conference_digest.md](2026-10/conference_digest.md) |
| 《深入理解 AI Agent》書摘 | v2.0；逐章整理 context、memory、tools、eval、持續演化與多 agent 協作，區分書中實測、轉引與作者意見 | [book_ai_agent_book.md](2026-10/book_ai_agent_book.md) |
| FB／LinkedIn／Medium 成效 | 過往研究的需求與讀者回饋；部分歷史成效整理在 style brief 與 backlog | `community_digest.md` 依規則只留本機，本工作區沒有月份摘要檔；可先看 [style_brief.md](2026-10/style_brief.md) 與 [backlog](2026-10/backlog.md) |
| Notion／工作坊／閱讀筆記 | 過往研究曾用作第一手材料索引與引用規劃 | `notion_digest.md` 與 `.context/research/` 原始資料未帶入本工作區；需要時回原收集位置取得，存放規則見 [研究流程](README.md) |

現有摘要能用來定位來源，但論文、規格、會議自報數字與私人材料的引用條件仍要逐項核對。工作區缺少原始檔，表示此處無法重驗相關材料，不代表當時沒有收集。

## 素材已分配的去向

這張表用來避免下一輪把已經展開的內容再提成新系列。詳細分配仍見兩輪 backlog 的「已被吸收的訊號」段落。

| 素材／研究問題 | 主要去向與邊界 |
|---|---|
| mutation、agent 寫的測試、review 分流、constraint tests、pass^k | 「綠燈不是驗收」；探索式測試候選另做使用產品的完整實作 |
| spec、Example Mapping、可執行契約、輸出變異、AGENTS.md conventions | 「同一份規格，跑十次」；skills／memory 候選延伸到准入與治理 |
| trace、SLI／SLO、harness 版本、ledger | 「Agent 的 SRE」；approval artifact 的人類核准原則已在 Review 篇，SRE 延伸為由 ledger 支撐的 attestation；runtime 候選再展開 fleet 與持久化平台 |
| 注入、skill 供應鏈、權限控制 | #1 爆炸半徑；principal 與委派鏈歸 #10 identity，選題時擇一或重新切分 |
| memory | #4 管記憶怎麼寫、怎麼評估與保留；#3 管工作區、儲存與恢復 |
| MCP server | #1 研究安全；#3 研究平台整合；#11 研究服務能否持續可用 |
| 團隊知識與個人能力 | #2 研究組織的共同理解與維護債；#9 以單篇處理去技能化 |

## 接續工作與期限

以下保留既有規劃的日期，並更新已完成工作的狀態。活動與投稿時間在採取行動前仍要重查；本次只更新主題索引，不代表已完成其他系列的研究、實驗、發文或社群分享。

**已完成與尚未實作的待辦分開看。** 最新 [研究 README](README.md#%E5%BE%85%E8%BE%A6)已記錄英文複核等完成證據；總論與 Review 篇均標示核准機制的實測範圍；文章完成，不代表已在 production 實測。各篇上線前確認前篇狀態，上線後回填系列與英文版連結。

| 原期限／窗口 | 接續工作與完成證據 | 依據 |
|---|---|---|
| 9 月底 | 確認 Amsterdam 原始材料的位置；定 A1～A3 欄位，讀 2607.03691、2608.26218、2609.01931 全文，將補證據清單定版 | [SRE 大綱](2026-10/2026-12-sre-for-agents.md) §4、§6 |
| 10/06 起，各篇上線前 | 核對上述發布前待辦；上線後依每篇日期回填系列連結、英文版連結與成效 | [研究待辦](README.md#待辦)、[發布佇列](../PUBLISHING.md) |
| 中文 11/10～12/01；英文待完成 | 40 次正式量測與四篇中文已完成，10/04 合併 main 並完成中文排程。接續完成四篇 Claude max 英文主稿、逐段潤飾、圖表與 Medium 排程；不把原 10/06 的 40／50 次實驗規劃列為待執行 | [正式結果](experiments/same-spec-ten-runs/RESULTS.md)、[發布紀錄](2026-10/same-spec-ten-runs/publication-2026-10-04.md) |
| 10 月（SRE 原規劃） | SRE 儀表化仍待執行；依原計畫保留 run metadata、成本、介入與獨立驗證結果，建立真實 trace、可查詢 ledger 與 revert 基線。規格變異的正式 40 次已完成，不等於這些 SRE 證據也已取得 | [SRE 大綱](2026-10/2026-12-sre-for-agents.md) |
| 10/15（監看項目） | 原 backlog 列 Open Source AI Week 投件截止，關聯 #14 與插曲；是否投稿尚未決定，先確認機會與期限 | [backlog 會議與日期表](2026-10/backlog.md) |
| 10/31 | 檢查是否已取得真實 run trace 與可查詢的 ledger，依原退場條件決定 SRE 系列範圍 | [SRE 大綱](2026-10/2026-12-sre-for-agents.md) §6 |

下一輪選題先沿用 #1、#4、#3、#2 的研究順位；補進實測、讀者回應或採用案例後再重評。候選的最早月份不直接轉成發布承諾。

## 版本與維護入口

| 要做的事 | 採用的檔案 | 歷史資料的用途 |
|---|---|---|
| 查三個後續系列為什麼入選 | [2026-09 selection](2026-09/selection.md) + [期中增修](2026-10/selection.md) | 初次評分、反方意見與原排序保留；期中沒有重新選題 |
| 查目前候選與升級條件 | [2026-10 backlog](2026-10/backlog.md) | [2026-09 backlog](2026-09/backlog.md)供比較變動，不把兩份當成兩套主題庫 |
| 接續規格變異系列 | [成稿狀態](2026-10/same-spec-ten-runs/manuscripts/STATUS.md)、[發布紀錄](2026-10/same-spec-ten-runs/publication-2026-10-04.md)、[正式結果](experiments/same-spec-ten-runs/RESULTS.md) | 中文四篇已排程；英文仍待 Claude max 主寫與發布。既有正式結果不擴大為 native Skill 或真人成本結論 |
| 撰寫 Agent SRE 系列 | [2026-10 大綱](2026-10/2026-12-sre-for-agents.md)、[圖稿](2026-10/2026-12-sre-for-agents.figures.md)、[推廣計畫](2026-10/2026-12-sre-for-agents.publish.md) | `2026-09/` 同名大綱與圖稿是重切前版本，只供追溯 |
| 查「綠燈不是驗收」的內容與進度 | 根目錄五篇 `article.md`／`article.en.md`、各篇發布紀錄 | [原研究大綱](2026-09/2026-10-agentic-green-is-not-done.md)供追溯；標題與排程採成稿及發布紀錄 |
| 執行後續撰稿與潤稿 | [STYLE.md](../STYLE.md)、當期 `style_brief.md`、[現行聲音手冊](2026-09/voice_brief.md) | 歷史字數目標與 voice-pass workflows 不取代作者後來確認的標準 |

後續更新先寫回對應的選題、大綱、backlog 或發布紀錄，再同步本頁的狀態與入口。實驗完成要附結果位置，來源補齊要附查閱日期；私人摘要與原始貼文仍依 `.gitignore` 留在本機。
