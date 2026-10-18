# 同一份規格，跑十次：正式研究結果

2026-09-25。使用目前 `medium-articles` repo 的真實 `codex_jsonl.py` 修補任務。**A0、A、B、C 四組各 10／10 通過主要終點；每組都有 10 種不同的 identifier-normalized AST。** 這是單檔、無工具、固定模型設定的受控案例，並未測量原生 Skill、完整 agent loop 或人類維護成本。

完整資料見[封存索引](results/formal-2026-09-25/archive.json)、[原始名額台帳](results/formal-2026-09-25/records.jsonl)、[可回算摘要](results/formal-2026-09-25/summary.json)及[凍結分析器產生的報告](results/formal-2026-09-25/report.md)。重現命令見 [README](README.md)；來源查證與審查時序見 [research loop](../../2026-10/same-spec-ten-runs/research-loop.md)。

成稿階段另找到一項比較限制：A0 寫不需新增 CLI 參數，A／B／C 則另把新增 CLI 選項列為任務範圍之外。四組以共同 R01–R13 為基準，仍不能宣稱 A0／A 的措辭強度已證等價。原始 packet 與數值不變，影響是否存在也未由本輪辨識；詳見[措辭差異補記](../../2026-10/same-spec-ten-runs/manuscripts/packet-wording-caveat.md)。

## 驗收結果

主要終點固定為 `accepted_completion = cli_success && artifact_success`。CLI 必須正常完成且生成邊界完整，候選必須通過全部 102 個批次案例及 1 個 EOF 前 streaming probe。這個通過條件只涵蓋凍結的 103 項檢查，不是所有可能輸入與內部實作要求的證明。

| 組別 | CLI 完成 | 候選通過 | 主要終點 | 雙側 95% Clopper–Pearson 區間 |
|---|---:|---:|---:|---|
| A | 10/10 | 10/10 | 10/10 | 69.15%–100.00% |
| A0 | 10/10 | 10/10 | 10/10 | 69.15%–100.00% |
| B | 10/10 | 10/10 | 10/10 | 69.15%–100.00% |
| C | 10/10 | 10/10 | 10/10 | 69.15%–100.00% |

40 個正式名額全部保留，沒有補抽、重試或事後追加樣本；沒有 timeout、operational error、boundary violation、缺少候選或不可解析 AST。每組 CLI × artifact 的四格計數都是「true／true：10，其餘三格：0」。原始 2 次 pilot 與另外 4 次停止路徑 probe 全部排除。

每組只有 10 次，區間下界仍約 69.15%；四組結果相同不構成等效性證據，也無法選出較可靠的組別。區間依賴共同 Bernoulli 機率及獨立性假設，provider 漂移或相依性不會因採用 exact interval 而消失。本輪沒有組間 contrast 估計、顯著性檢定或勝負判定。

## 結構差異

| 組別 | 可解析候選 | 有效 pairs | AST cosine 中位數［最小值、最大值］ | 不同正規化 AST hash 數 | 對 seed 的 cosine 中位數［最小值、最大值］ |
|---|---:|---:|---|---:|---|
| A | 10/10 | 45/45 | 0.996975［0.991281、0.999600］ | 10 | 0.962484［0.951163、0.970361］ |
| A0 | 10/10 | 45/45 | 0.994710［0.983119、0.998213］ | 10 | 0.965595［0.949927、0.978295］ |
| B | 10/10 | 45/45 | 0.997509［0.993698、0.999708］ | 10 | 0.959382［0.955575、0.966537］ |
| C | 10/10 | 45/45 | 0.996477［0.990320、0.999664］ | 10 | 0.965676［0.952907、0.970697］ |

cosine 比較各種 AST 節點類型的數量，會忽略順序及許多語義差異；正規化 hash 則比較另一種保留樹狀順序的表示。因此，高 cosine 與不同 hash 可以同時成立。兩者都不是正確性、可維護性或人類審閱工時的指標。

每組 45 個 pair 共享同一批 10 份程式，合計 180 個 pair 仍只有 40 個生成名額，不能把它們當成 180 個獨立觀測。共同 seed 與單檔修補也可能造成高相似度；seed 參照讓這個限制可見，沒有把它消除。完整逐候選／逐 pair 數值保留在 summary，沒有只挑某份代表實作或成功者子集合。

正式結構圖採固定 0–1 座標，見[圖表工件](../../2026-10/2026-11-same-spec-ten-runs.figures.md)。

## 回報的資源使用

| 組別 | 生成耗時中位數（秒） | CLI 回報 USD 合計 | 費用觀察數 | Input tokens | Output tokens | Cache read／creation tokens |
|---|---:|---:|---:|---:|---:|---:|
| A | 37.300 | 1.382626 | 10/10 | 20 | 46037 | 0／52202 |
| A0 | 37.273 | 1.248397 | 10/10 | 20 | 44935 | 0／39339 |
| B | 40.277 | 1.513502 | 10/10 | 20 | 50161 | 0／57749 |
| C | 37.161 | 1.547817 | 10/10 | 20 | 49072 | 0／64234 |

正式 40 次的 CLI 回報牌價估計合計 **USD 5.692342**；不含研究審查、pilot 與其他開發請求，也不是訂閱或信用卡帳單。各資源欄位均取得 40/40 筆，沒有將缺失填零。耗時是 runner 觀察到完成／逾時時的生成耗時，驗收另行執行。

Input／output／cache 表使用 CLI terminal `usage` 的原始分類；`modelUsage` 另外保存各模型明細。Haiku 只出現在 `modelUsage` 計費明細，未出現在候選生成的 assistant 訊息；它在 CLI 內部的用途無法由這份 trace 證明。這些計費 tokens 不一定出現在 terminal usage。不能只拿 input 欄乘上一個模型單價重建帳單。四組 cache read 都回報 0，仍有 cache creation；本輪沒有實驗性重置 cache，也不估算無 cache 的反事實價格或維護 ROI。

## 版本與完整性

| 欄位 | 本次紀錄 |
|---|---|
| 任務來源 | `fantasybz/medium-articles`，commit `37f6c0ce9b536f95132d5e01a387f380bbb9639c` 的 `research/scripts/codex_jsonl.py` |
| 生成設定 | `claude-opus-5-5`，effort `high`；`2.1.282 (Claude Code)` |
| 本機封存 | `2026-09-25T04:24:12.039363+00:00`；26 份 source、四份 packet、完整 40 個排定名額 |
| Manifest SHA-256 | `ba30398118ecde62b2f682884c1e882b2864c22d70faf99549ceab0d7c0a55f2` |
| Ledger SHA-256 | `2be5ed458de2e2defa2ab4f24d88f25bdd3b7340c9207915ab6aa0988c0db7f0` |
| 執行 | 最多四個生成程序並行；10 個交錯排程區塊，相鄰區塊可重疊；所有生成結束後才驗收 |
| 每名額停止條件 | 600 秒；CLI 牌價 USD 5 停止門檻。實測低預算 probe 會先超過設定才停止，所以不是硬性金額上限 |
| 評測 | macOS Seatbelt，外部 oracle；正式前 read／write／network-denial probes 通過；候選前後 hash 相同 |

這是本機執行前封存，不是第三方預註冊。Python build、CLI binary 與明確輸入有版本或 hash；隱藏 provider context、sampling seed／temperature、服務實作及完整 OS 狀態沒有被固定。OS 版本是在開始生成後才補記為 macOS 26.6.2／arm64，不能倒寫成 pre-freeze pin。

公開資料保留原封不動的 manifest、source、packet、候選、case outcomes 與 ledger。`trace-public.jsonl` 是明確標示的 projection，移除思考內容及本機／transport 識別資訊，保留 parser 判定所需證據；每份 projection 有原始 raw hash 與投影 hash，原始 trace 留在本機。它不是原始 trace 的逐 byte 複本。封存 source 內的 README／PROTOCOL 描述執行前狀態；目前完成狀態以本頁為準。

## 獨立核對與重評

正式前已完成四個 outline lenses、Claude xhigh 設計審查及第二輪 blocker 複核、Codex gpt-5.5 xhigh 審查與第二輪複核。83 項研究工具測試及既有 301＋108 項回歸檢查通過；這些工具檢查與每候選 103 項驗收不是同一個分母。

已從可公開封存包的 `source/archive.py`，在全新空白工作目錄、`PATH=/usr/bin:/bin` 的環境重新驗收 40 份候選；不需要 Claude CLI，也沒有新模型請求。**40／40 份、每份 103 項 case outcome 與原紀錄完全一致**，原候選及紀錄未被覆寫。見[完整重評結果](results/validation-2026-09-25/public-rescore.json)與[執行紀錄](results/validation-2026-09-25/public-rescore-execution.json)。第一次正式評測與本次重評各執行 4,120 項檢查，這不是新增 40 個生成樣本。

[獨立資料稽核](results/validation-2026-09-25/formal-data-audit.md)判定 **READY**，1,903／1,903 項核對通過：包含 317 份公開檔案 hash、40 份可由原始 trace 重建的投影、名額／啟動順序、模型邊界、逐候選驗收、重評結果、區間及所有 AST pairs。這是 AI 代理的獨立核對，不是人類盲審；[機器可讀紀錄](results/validation-2026-09-25/formal-data-audit.json)保留逐項證據。

## 本輪結論與下一步

目前可支持的結論是：在這個真實 repo 的小型 parser 修補上，四份指令包以共同 R01–R13 為規範基準，各產生十份實作並通過既定驗收，而每組內仍可觀察到結構表示不同。這批資料沒有提供提高某組可靠度、原生 Skill 效果或降低真人維護成本的證據。成稿繼續維持單一 task、small n、驗收覆蓋與 descriptor 的限制；四篇中文全文（本機稿）已完成 Claude Code `max` 主寫、逐段潤飾、複核與嚴格中文檢查，目前尚未發布。詳見[主寫與品質紀錄](../../2026-10/same-spec-ten-runs/manuscripts/STATUS.md)。

2026-09-28 文稿更新：四篇依作者意見重新主寫與潤飾，補足研究動機、系列承接與四份 spec 的具體差異；[本輪紀錄](../../2026-10/same-spec-ten-runs/manuscripts/STATUS.md)另列。此更新只涉及研究呈現，不更動正式設定、候選、評分或樣本數。
