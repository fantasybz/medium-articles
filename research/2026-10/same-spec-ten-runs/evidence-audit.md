# 「同一份規格，跑十次」公開證據核對

核對日期：2026-09-25（UTC；Asia/Taipei 同日）。狀態：**五份第一手來源已核對與精讀；尚未重跑作者 artifact，也尚未執行本系列的實驗。**

本次由主代理以 repo 指定的 gstack browse 取得 arXiv 原站內容，再逐項讀方法、結果、限制與相關附錄。四份使用帶版本的 HTML 全文，一份使用 v2 PDF 及文字抽取。下面所謂「已核對」指原站檔案內確有該項報告，不是獨立重現、peer review 背書或可外推到所有 repo 的結論。

原大綱的 37 個 arXiv ID 已另做完整 inventory；本輪只恢復下列五份為可用來源，其中只有 2608.25399 屬於原 37 個。其餘舊來源的數字不因出現在 digest 就自動恢復。D09/D10 是搜尋線索，正文引用以這份 audit 的限定為準。

## 這次改變了哪些判斷

**「輸出結構沒人量過／本系列第一次量」必須刪除。** 2607.02436v2 記錄同一份 spec 的重複生成，並列出固定組態下的檔案數、原始程式碼行數和 CSS 行數分布。這不是本系列預定的 AST metric，但足以使原來的全面性新穎宣稱站不住。不能把「沒有使用我選的指標」改寫成「沒有人量過結構」。[2607.02436v2](https://arxiv.org/pdf/2607.02436v2)

可保留的研究問題是：在這個 repo、這個 task、明確分開的資訊條件下，重複執行會產生哪些功能、約束、結構及成本差異；哪些差異值得審查。成本離散度、功能通過率、程式結構差異與維護成本是不同結果，不可互相代替。把其中一個當作所有 harness 的單一驗收指標，超過本輪證據。

## A1：task specification 與成本

來源：[Can your AI agent be cheaper? — v1 HTML](https://arxiv.org/html/2608.25399v1)。讀取位置：§3.1–3.3、§4.1–4.3、§5、Appendix A/C。層級：單一模型、五個 coding tasks 的受控重複量測；非本系列實驗。

| 核對項 | 原文結果與解讀 |
|---|---|
| 樣本 | SWE-bench Verified 5 tasks × 12 specifications × 3 effort levels × 15 repeats＝2,700 runs；Kimi K3、mini-swe-agent、temperature 1。正式分析排除提供解答的 oracle prompt，保留 11 種規格。 |
| +29.7% 的方向 | §4.1／Appendix C：bare user story 相對 full specification 的**成本較高 29.7%**，不是 full spec 較高；這是分層模型估計，按單一費率計價。90% credible interval 為 +5.1%～+58.7%；95% 為 −0.3%～+66.8%，包含零。正文宜說成本，不能無條件等同跨模型 token 比例。 |
| variance 指什麼 | §4.3：同 specification/effort 重複執行的成本 geometric SD，中位數 ×1.34；各 specification 的中位數 ×1.29～×1.40。這不是 AST、架構或檔案相似度。 |
| 限制 | 五 task、單模型；不能從「未偵測成本 spread 改變」推出「spec 不影響結構」。Appendix A 記錄原先 60-turn cap 對簡略規格截斷較多，改 120 後重跑 112 筆，其中 108 成功；因此 budget/stop rule 也是方法的一部分。 |

**寫作處理：** 可說這篇量過規格內容對成本及成本離散度的影響；刪「variance 指標未交代」與「論文沒量 pass rate」這兩個過期缺口。全文有 solve-rate 分析，但不支持「兩種規格等價」。不再只用文件厚度解釋效果；它移除了具體資訊。

## A2：同一份 spec 的功能與結構差異

來源：[2607.02436v2 PDF](https://arxiv.org/pdf/2607.02436v2)，對照 [abstract page](https://arxiv.org/abs/2607.02436)。精讀位置：Methods（PDF 印刷頁 5–10）、Results 的 Tables 2/3/8/9、Limitations（頁 28–29）、Data availability。

| 核對項 | 原文結果與解讀 |
|---|---|
| 設計 | 90 runs 來自同一份 frozen web-app spec；包含多個 model、harness、effort、tool、prompt 條件，**不是同一組態 N=90**。條件未隨機分派，作者將統計解讀為描述性比較。 |
| 功能分母 | 14 criteria、滿分 42。Docker 首次失敗為 40/90；各條件可收到修正提示，因此最終分數不是完全不介入的 pass rate。 |
| 直接結構證據 | Table 8：Opus 4.6 High base 的 7 次重複，source files 10–17、source lines 792–1,319、CSS 41–626。Table 9：Opus 4.7 xHigh base 的 6 次全部 42 分，但 source files 15–22、CSS 174–468。 |
| 邊界 | 這些是數量與體積 proxy，不是 AST similarity、bounded-context correctness 或維護成本。單 task、作者知道組態且親自驗證、native host 與 agent 環境可能不同；完整 session transcript 未保存。 |

**metadata 差異保留：** abstract page 的標題末段為 *an observational study*，comments 寫 22 pages；本次版本化 PDF 題名末段為 *Evidence from 90 matched agent runs*，實檔共 43 pages。不能把兩者悄悄合併成同一個版本摘要；本 audit 的新增結構敘述只依下方 hash 對應的 PDF。這個差異宜在發布前再次核對。

## A3：SKILL 收益是否大於重複噪聲

來源：[Skill Issue — v1 HTML](https://arxiv.org/html/2609.12742v1)。精讀位置：§3–4.3、§6、Appendix C。層級：三個 Kotlin repos 的文件最佳化與 held-out 比較。

| 核對項 | 原文結果與解讀 |
|---|---|
| 比較設計 | Claude Code／Sonnet 4.6；固定 base，隱藏 git history，以 empty-seed rollout 配對 candidate rollout；SKILL 文件為改變項。held-out tasks 分別為 20、26、23。 |
| +4.9pp 指什麼 | §3.2／§4.2：seed 自比基準為 0.5 的 **paired composite score**；GEPA 分別 .554、.567、.525，平均相對 .5 約 +4.9pp。它不是 resolve rate 提高 4.9pp。 |
| 分開的功能結果 | resolved tasks 分別 13→16/20、16→20/26、14→15/23。配對 score 還考慮測試篡改、成功宣稱、hidden tests 與 bounded tie-breakers。 |
| 不確定性 | §4.2 沒有任何 optimizer run 的 sign test 達 .05；最佳 p=.29。這是未能在該資料量下區分收益與 reroll noise，不是證明 SKILL 無效。維護者意見與兩個 open issues 的示例另列，不能替代 held-out 判斷。 |

**寫作處理：** 用它說明先定義估計對象、再處理 agent 的自然變動。不可把這篇變成「AGENTS.md 不影響 pass rate」「quality 軸一定更敏感」或 pattern skill 必然收斂結構的證據。

## A4：SaltBench 的 protocol 與未解答問題

來源：[SaltBench — v1 HTML](https://arxiv.org/html/2609.11076v1)。精讀位置：§2.1、§3.1–3.6、§4–4.1、§7–8。層級：protocol 加上分階段量測；各階段不可混成一個結果。

| 核對項 | 原文結果與解讀 |
|---|---|
| 可借用的方法 | freeze／append-only amendments、獨立 referee、以 breach probes 檢查隔離、不同 termination class。這些是設計方法，不等於每次歷史 run 都有完整隔離。 |
| 關鍵反證 | §3.2：後來發現 file-reading tool 不受 subprocess sandbox 的 path deny 保護；無讀取事件不等於具備保護。§8：該價格 matrix 的所有 cell 都缺自身 build-provenance receipt。不能引用為「已完美隔離」案例。 |
| 成本讀值 | §4：diet-bare treatment 在 5 個 authored Rust components 全部較貴；原登錄以每 condition n=3 為基礎；reading A 在補測後有三個 plain 條件為 n=4，不能把所有 cell 都寫成 n=3。五個 component 的方向比較，單側 sign test p=.0312。這只支撐該組比較的方向；作者不將 per-problem ratios 當 population multiplier。 |
| 另一組未定 | statement amendment 是另一對比，k=4、3/4 高於 parity、p=.3125；以 k=4 該單側測試最好也只有 .0625。不能和前項合寫「5 components 的測試沒結論」。 |
| 品質與成本分開 | 原 matrix 計價時沒有逐 cell correctness verdict；後補 correctness pass 為 post hoc，未分出 arms。不能推出較貴換到較正確。 |

**寫作處理：** 用它強化本系列的失敗台帳、隔離實測與版本邊界。budget halt 可以在交付分析算「未完成」，但不能冒充已完成的語義測試失敗；兩種分母都須保留。

## A5：prompt、effort、harness 的交互作用

來源：[Prompt-Induced Waste in Coding Agents — v6 HTML](https://arxiv.org/html/2608.01347v6)。精讀位置：§2–3、§6–6.1、§11–12；核對 supplementary campaigns 的分界。

| 核對項 | 原文結果與解讀 |
|---|---|
| 核心研究 | 24 個 deterministic coding tasks、18 prompt variants；其中 9 個 primary variants 保留 objective、AC、test command。核心 4,644 valid runs／2,801 trace annotations 與 hard-task effort campaign 分開。 |
| 能支持什麼 | §3：語意要求會改變推理／驗證工作；逐字重述沒有重現所有效應。這支撐「資訊與動作要求不能只當字數」。§6.1 顯示 effort intervention 的效果依 harness policy 改變。 |
| 明確分界 | dsh extension 是 5 tasks × 5 arms × 3 repeats＝75 runs，各 arm 15/15 成功；它測該設定的額外 effort，不是困難任務的最佳策略。跨 harness 絕對成本並非此 extension 的 primary estimand。 |
| 限制 | 主 tasks 小、功能上限高；architecture-dependent tasks 幾乎未覆蓋。全文沒有建立 AST similarity、human calibration band 或低結構變異的 production 授權門檻。controller 設計也不是已證實成果。 |

**寫作處理：** 固定共同 runtime/gates，才比較文件條件；若 C 同時新增 skill、hooks、settings，就只能稱 bundle 比較，不能把三者效果全記到 skill。四個累加條件也不能估出完整 factorial interaction。

## 對本系列 protocol 的具體要求

以下是本系列依證據作的設計判斷，並非上述論文已驗證的門檻。依使用者最新指示，正式 task 已選定目前 `medium-articles` repo 的 `codex_jsonl.py` 型別驗證修補，基底固定為 `37f6c0ce9b536f95132d5e01a387f380bbb9639c`。付款情境或人工 fixture 不列為正式實驗，不能把它的示範結果當成真實 repo 證據。

1. 在 `medium-articles` 選定一個真實 task、固定基底 commit，並使用獨立 evaluator。A0/A 保留相同規範要求，比較精簡與展開說明套件；B/C 只在預定 treatment 有差異。不能讓工具、權限、tests 同時改變而仍聲稱識別出文件效果。
2. 分開報功能、契約違規、結構 proxy、成本與 termination。所有分派 run 都進台帳，crash、timeout、budget stop、invalid pin 不能從成本／失敗報表消失。
3. 40 次基礎分派與真人工作分開。沒有真人就保留 human calibration／review 未執行；兩份真人實作最多給一個 reference pair，不能產生統計「帶」。
4. 相似度只能先作探索性指標。N=10 的小差距不能作等價證據，45 個 pair 不是 45 個獨立樣本，也不構成 production G2 擴權許可。
5. 預先凍結 outcome definitions、分析、排除／替補／停機規則，再執行 scored runs。若結果不支持方向性假設，就報告未支持；不能更換成功指標，讓原敘事維持勝利。

## 取得方式與 artifact manifest

存放目錄：`.context/same-spec-ten-runs/sources/`（本機、gitignored）。HTML `.txt` 是 browse 可見文字快照，含擷取標記，**其 SHA-256 是快照 hash，不是官方 HTML 原始位元組 hash**。PDF hash 對應下載檔案；PDF `.txt` 是文字抽取，因此另列 hash。manifest 能固定本次讀過什麼，不能證明作者 data／code 已重現。

| 檔案 | 原站 URL／性質 | SHA-256 |
|---|---|---|
| `2608.25399v1.txt` | [versioned source](https://arxiv.org/html/2608.25399v1) | `4b91f67f074a10527e52be6fb52e6f9a38c6dfb4566a9974530e2ee1ed47704e` |
| `2607.02436-abs.txt` | [versioned source](https://arxiv.org/abs/2607.02436) | `0acd3c48f5bec24ef612e0a301d4c2d49cbc9f190411b46ec9bde769de7f6bb6` |
| `2607.02436v2.pdf` | [versioned source](https://arxiv.org/pdf/2607.02436v2) | `4c80ac39360e3141df3b6b000823d2b07e92b1e79702a03b24bb35c393fe874d` |
| `2607.02436v2.txt` | PDF text extraction; source above | `f3110591bb651b85bea92dec019e201ebc9a5acca60061a544e73b96559cd2fa` |
| `2609.12742v1.txt` | [versioned source](https://arxiv.org/html/2609.12742v1) | `b518238c52b31f63458bc9e2724884aba8e169881543b354c9509580f8dda501` |
| `2609.11076v1.txt` | [versioned source](https://arxiv.org/html/2609.11076v1) | `fe75b652a5685f3dda94fbd36bd4585d3bf0534fd06b5599c0e16dc64a2ba046` |
| `2608.01347v6.txt` | [versioned source](https://arxiv.org/html/2608.01347v6) | `a9af7ff769f41dff35eefe37d4bcdad7efdb88487ca166670192c0f341c91ad5` |


所有 URL 本次由主代理於 2026-09-25 存取；audit 撰寫時 clock 為 2026-09-25 03:25:13 UTC。本次沒有對第三方資料集或程式庫發出新請求，也沒有把論文內的引用視為已讀原來源。A2 的 metadata 差異仍待釐清；其餘各來源也只支撐上列限定範圍。
