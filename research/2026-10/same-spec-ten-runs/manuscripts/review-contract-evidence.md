# 契約篇全文證據審查

審查時間：2026-09-25T09:29:18.329096+00:00。

**此報告保存 `416476b5` 全文初審：1 項 major、1 項 minor，無 blocker。** 主代理已另依意見修稿；新版的正式結案與綁定 hash，請看 [final closure](review-contract-evidence-final.md)。本報告保留原問題，不以新版覆蓋初審紀錄。

完整讀取 [article.md](../../../../2026-11-same-spec-contract/article.md) 當時的第 1–291 行，包含六節、四張表、F1、所有範例、References、AI 協作及署名。全文初審 SHA-256：`416476b5ade3ded365cd3faff9477d666175ceb5154eddffc75ed18a8da18def`，45,267 bytes。不是只審新增尾段；前半部也已重讀，並對照第五節與結語。現在的 article.md 已是修訂版，初審全文可以由現稿反向套用 [contract-evidence-delta.json](contract-evidence-delta.json) 逐 byte 還原。

## Findings

### CONTRACT-E01 — major：候選評分沒有統一的越界失敗分類

初審第 203 行寫「越界的實作必須記為越界」，接著說「逾時、越界與語義失敗分開記錄」。這把三種不同層級的檢查混在一起，會讓讀者誤以為候選 evaluator 會辨識所有越界並給出獨立分類。

直接來源是 [evaluator.py](../../../experiments/same-spec-ten-runs/results/formal-2026-09-25/source/evaluator.py) 第 267–291 行：`_grade` 只在批次結果記錄 `timeout`、`output_limit` 或 `mismatch`，沒有候選越界分類。未識別的 sandbox 會拋出 `EvaluationUnavailable`，也不是把該候選標為「越界」。

[sandbox.py](../../../experiments/same-spec-ten-runs/results/formal-2026-09-25/source/sandbox.py) 第 96–129 行的 `read_denied`、`write_denied`、`network_denied` 是三項 preflight 操作是否得到 `PermissionError` 的紀錄。`test_sandbox.py` 第 26–29 行核對這三項；第 42–53 行另測真實 timeout 與輸出限制。`tests/test_task_evaluator.py` 第 138–195 行測 reference、語義 mutants 與延遲輸出 mutation。生成紀錄的 `boundary_violation` 則是 `run_study.py` 對 model/tool trace 的另一層檢查。

建議把 reference／語義 mutants／候選 timeout 的工具測試說清楚，再另列三項隔離 denial probes，保留觀測範圍。不能只因某候選沒通過，就把原因推成語義錯誤或已辨識的越界。

### CONTRACT-E02 — minor：沒有固定所有研究者能控制的輸入與開關

初審第 195 行寫「研究者控制得到的輸入與開關都已固定，也留下了紀錄。」這比實際凍結範圍強。

[manifest.json](../../../experiments/same-spec-ten-runs/results/formal-2026-09-25/manifest.json) 的 `environment_controls.unobserved_context` 明載其他 environment values 與 provider/CLI context 沿用，並未記錄或完整固定。[run_study.py](../../../experiments/same-spec-ten-runs/results/formal-2026-09-25/source/run_study.py) 第 58–79 行先複製環境，再固定列出的值；不能由此推成所有可控制的本機條件都已固定。

建議限定為明確送出的 packet，以及封存紀錄列出的 model、effort 與 CLI 開關，並保留其餘 context、環境與服務狀態未完全掌握的限制。OS 版本事後補記與 Haiku 用途未辨識的其他句子正確。

## 全文檢查

以下行號均指初審 `416476b5`，新版第 205 行後因新增段落順延兩行。

| 編號 | 初審行號 | 結果 |
|---|---|---|
| CE01 | 3、9、11、13、45、243 | **起點與 legacy 缺陷：**[]／null crash 及 numeric text + completion 的 exit 0 有 baseline-reproduction；原始 seed 以固定 commit/hash 識別。未虛構生產事故。 |
| CE02 | 15、17、27、35、43、47、49 | **七行 JSONL 範例：**七個實體行依序為文字、非 JSON、空白、array、string、numeric text、completed；malformed 行號 4/5/6 正確。stdout 保留訊息與 token 前導空行，stderr 三行且無 EOF6 summary；先前輸出不回收。這是規格推導例示，不冒充封存案例。 |
| CE03 | 53、62、64、66、72、74、178、179、180、181、183 | **null、fallback 與示意對照表：**root/type/item shape、bool tokens、unknown 字串類型例外正確。error:null 合法失敗，錯誤 error envelope 先 malformed 再 FAILED no message 再 EOF3 summary。command 殼與 160 字元、LGTM 重複與 requirement IDs 均保留先前修正。 |
| CE04 | 84、86、87、88、92、94、96、98 | **平行成功欄位、四格與 CI：**cli_success/artifact_success 平行、accepted 取交集；五秒寬限只屬 timeout。正式各組 true/true10，其餘0；CP95 69.15–100 的共同 Bernoulli、獨立與涵蓋率限制正確，不保證可靠度或等效。 |
| CE05 | 100、104、106、108、110、166、168、170、172、187 | **generator、candidate、driver 與 F1：**模型只收到 packet；候選必須取得當次 stdin，driver 保留整份套件／預期結果／比對邏輯。第172行已限定輸入介面。F1 byte-identical 核准來源；先全生成再評測、異常停機不補跑一致。無全管道隔離或真人獨立性保證。 |
| CE06 | 104、168、174、185 | **前篇 recall 與 owner：**Harness 文件/CI 分工、green Review 的作者陳述、green 可靠度的約束來源與 owner，均能對回本地原文；green 系列明說尚未發布。 |
| CE07 | 193、195 | **CLI 設定與控制範圍：**--tools 空值、disable-slash-commands、safe-mode、strict-mcp-config、setting-sources 空值均在正式 invocation；init 工具/MCP/skills/slash 空清單由 trace 核對。Haiku 只在 cost accounting，OS版本後補正確；但控制範圍的全稱句見 CONTRACT-E02。 |
| CE08 | 197、201 | **Seatbelt probe 的時間與範圍：**freeze 04:24:12.039363 UTC、launch preflight 04:24:22.093608、首名額04:24:22.246230。read/write/network bind 三項拒絕真實紀錄，不追認全 OS/IPC 隔離；重新驗收不倒補舊執行的安全證據。 |
| CE09 | 199、201、247、282 | **SaltBench 方法與歷史限制：**§3.2 明載 file-reading tool 在 harness process、不受 subprocess path deny；未觀察利用不等於有保護。§8 matrix cells 無各自build-provenance record，mapping為事後重建。append-only修訂與分開halt/失敗的引用屬方法，未把後來修補追認為舊run已完全隔離。 |
| CE10 | 203、205 | **工具 fixtures 與 83 項分母：**工具驗證紀錄83/83，靜態數六個test檔也有83個test method；這不是83候選或新增模型樣本。reference與語義mutants、真實timeout、denial probes存在，但沒有原稿所稱統一越界候選分類，見CONTRACT-E01。 |
| CE11 | 209、211、213、224、226、235 | **streaming 可觀察行為：**批次比較最終輸出不足驗時序；probe 在stdin未EOF且未terminal時觀察第一則訊息，之後送suffix。未要求特定flush API；不擴張為每種stdout/stderr均即時、全串流路徑都受測。 |
| CE12 | 215、217、222 | **R10 null 與 false 的 stderr：**明寫兩行各自當完整輸入：null不malformed，false多一行malformed；兩者stdout皆空、EOF皆3，只有這項stderr差異。or {}會吞false診斷的機制說明正確；未聲稱本輪實測了例示。 |
| CE13 | 3、106、187、237、239、249、253 | **有限103與CLI caveat：**字面main/額外CLI/內部編碼未逐一檢查；同R IDs不等於等價。CLI措辭影響未辨識，通過103不能消除差異。補記未改規範／評分，未偽裝成原協議amendment。 |
| CE14 | 170、245、247、249、251、253 | **重評、amendment與結語：**既有同oracle重評40×103一致不增模型樣本；將來修oracle須保留舊版、另版本記理由、全部候選一致重評。單模型候選、AI稽核及無真人盲審限制保留；不把工具通過推成所有品質。 |
| CE15 | 255、264、266、276、277、287、289、291 | **References、主寫與公開狀態：**46本機相對連結皆存在；資料與四稿是本機/未發布。head/tail actual invocation max，meta成功、退出0、單terminal；artifact hashes與assembly精確相符。正式high40名額與max主寫分開，無英文／遠端發布簽核。 |

## 幾項具體核對

開場七行 JSONL 的空白第 3 行仍計入實體行號，因此 malformed 恰好是第 4、5、6 行。第一則有效文字加上 R08 前導空行及 token 註記，與 stdout block 完全相同。沒有 explicit failure，所以 EOF 選 6，且無摘要。第 64–72 行的 malformed `turn.failed` 則先診斷、再 FAILED fallback、最後 EOF3 摘要，3 優先於 6。

第五節的兩行 `error:null` 與 `error:false` 明說各自當成完整輸入；合法 null 的 stderr 有兩行，false 的 stderr 多一則 malformed。兩者 stdout 都空、exit 都為 3，這才是只比 exit code 無法發現差異的具體原因。

streaming probe 的主要證據在 `sandbox.py:132–176` 與 `evaluator.py:307–316`：送 prefix、在候選仍執行且 stdin 未 EOF 時觀察 exact early stdout，然後送 suffix。第 213 行已限定為可觀察行為，候選可以用其他方式即時輸出，不必呼叫特定 flush 函式；第 235 行也明說只有第一則 agent message 有這項 probe，沒有替所有類型的輸出及診斷簽即時性。

隔離時間次序為 freeze `2026-09-25T04:24:12.039363+00:00`，launch preflight `04:24:22.093608`，首名額 `04:24:22.246230`。三項 probe 是讀取 oracle-canary、寫檔與 localhost bind 的拒絕紀錄；其餘 OS/IPC 通道未受測。OS 版本補記是 `04:28:29.524679`，確實晚於正式開始。

SaltBench 快照第 134 行（§3.2）明列 harness file-reading 工具沒有進入 subprocess sandbox，缺少 path-tool permission 規則；沒有讀取事件不是有保護的證據。第 375 行（§8）明列 matrix cells 沒有各自的 build-provenance record，instrument mapping 為事後重建；正文沒有把後來控制追認為舊 run 的完整隔離。第 136 行的 append-only amendment，以及第 139–141 行的 halt 類別，均符合本篇引用範圍。本輪沿用本地版本化快照，未重新上網。

正式前工具驗證 JSON 記錄 83 項、exit 0；六個 test 檔以 AST 靜態數得 test method 32＋8＋3＋23＋5＋12＝83。這是既有工具測試資料的核對，沒有重新執行工具或候選，也沒有把 subtest、103 項案例或 40 個模型名額加進這個分母。

## 來源與主寫完整性

本輪核對 18 份凍結核心來源與紀錄，加上 40 份 evaluation，58 個 hash 均符合 archive；既有 evaluation 每份有 103 項且全部通過。manifest、候選、要求與原始結果沒有修改。四組 CLI/artifact 四格直接由 records 重計，均為 true/true 10，其餘 0。沒有重跑候選或重新聲稱做完 317 檔稽核。

F1 與核准 figures.md 的 Mermaid 區塊逐 byte 相同，hash 是 `0ba7420d3a7af4899388038dc97cd94bef12c8a50311377b1052315799bd6c97`；這是來源／語義檢查，不代替渲染檢查。46 個本機相對連結皆存在，未作遠端發布驗證。

head 與 tail 的 invocation 都指定 `claude-opus-5-5`／max；meta 均 success、exit 0、單 terminal。原文 artifact hashes 分別為 `23d3292fc8b01bc1d5b97ea674d10d1231b7ab0d5da49461ff45d5209c432279`、`25f0a08fd8dc6828fbc6ddd21cfe986872ad7d1bf430dca2efe6c43ad6f8b4e9`，以一個換行串接得到 assembly 所記的 `ddceb2a648ea56a3a6fbebfc3bcb9b9c861308ade0c986324c7e779ff8a5f80a`。正式 high 生成與 max 主寫明確分開；未讀 raw response 或思考文字。

## 歷史版本與後續

初審已精確逆向核對 `contract-final-clarification-delta.json`、`contract-final-polish-delta.json` 與 `contract-language-delta.json`，依序還原 `416476b5 → 8103c437 → d7d1244e → 6f6c03c1`。第 172 行的輸入介面限定正確：整份套件不交給候選，但個別 JSONL 事件流仍從 stdin 提供。這幾項改善沒有抹去本輪新發現的兩項問題。

本文不是全系列 READY，也不是真人盲審、外部重現或 MCP 語文報告。兩項初審 finding 及完整來源 hash 保留於 [JSON](review-contract-evidence.json)；修訂版是否解決，另見 [final closure](review-contract-evidence-final.md)。
