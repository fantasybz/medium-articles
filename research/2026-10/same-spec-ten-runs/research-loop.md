# 「同一份規格，跑十次」research loop 執行紀錄

2026-09-25。本輪依 [repo research loop](../../README.md) 的階段執行，使用本機 CLI adapter 與實際檔案，**沒有呼叫 native Workflow 工具**。研究材料是目前 repo 的真實 JSONL parser，固定 commit、規格與實驗程序見[實驗入口](../../experiments/same-spec-ten-runs/README.md)。本頁記錄已完成的工作及仍未完成的發布條件，不把研究大綱當成文章成稿。

## 來源與研究範圍

先恢復既有研究輸入與原評審，建立 37 個 arXiv ID 的本機 inventory，再選出五份真正負責論證的 primary sources。這五份逐一閱讀公開全文、核對版本、指標、區間與限制，結果見 [evidence audit](evidence-audit.md)。沒有重跑或宣稱重新收集缺少的十月社群 digest，也沒有把私有 Notion／社群輸入轉成公開實驗材料。

使用者後來指定自己的 repo，因此採 `fantasybz/medium-articles` 的 `research/scripts/codex_jsonl.py`，放棄先前的原創付款 fixture。原始程式碼的 `null`／`[]` crash 與數字訊息假成功已重現，來源及例子見 [task.json](../../experiments/same-spec-ten-runs/task.json) 與 [baseline-reproduction.json](../../experiments/same-spec-ten-runs/baseline-reproduction.json)。正式 parser 沒有被實驗候選覆蓋。

## 審查與修訂

四個 outline lenses 各使用全新、無工具的 Claude CLI 呼叫，主模型 `claude-opus-5-5`、effort `high`。設計審查另用 Claude `xhigh` 與 Codex `gpt-5.5 xhigh`；effort 因任務而異，正式生成一律固定 `high`。這是 AI 審查，沒有聲稱人類盲審或審查模型與生成模型完全獨立。呼叫與輸出 hash、實際 metadata 見 [review index](reviews/index.json)；原始意見保留，不因修正或撤回而改寫。

| 階段 | 實際輸出 | 主要意見與處置 |
|---|---|---|
| Evidence lens | [原始評審](reviews/outline-evidence.md) | 指出 protocol、analyzer 與大綱對組間 contrast 不一致。正式前統一只報各組摘要，移除 analyzer 的 contrast 輸出；補 streaming、共同 seed、不可見 context 與來源限制 |
| VP reader lens | [原始評審](reviews/outline-vp-reader.md) | 提早交代單檔／無工具邊界、四篇分工與研究後能做的決定；加 `10/10` 的區間下界，撤掉尚無數據的 ROI 推論 |
| Senior editor lens | [原始評審](reviews/outline-editor.md) | 區分每組相同 packet 與跨組相同規範；統一 parser 案例，不虛構作者事故；以本機執行前封存取代第三方預註冊措辭 |
| Diagram designer lens | [原始評審](reviews/outline-figures.md) | 圖只表達實際流程；F1 顯示全部生成後才評測，T2 用退出碼排名，T3 保留所有名額，F2 固定座標與分母 |
| Claude 設計審查 | [xhigh 原始評審](reviews/design-claude-xhigh.md) | 確认四組 R01–R13 等價，103 項案例未偷偷加入新要求；指出 synthetic API error 與真正邊界違規混淆，以及評分階段不應依賴 CLI 版本，須修正後複核 |
| Codex 獨立設計審查 | [xhigh 原始評審](reviews/design-codex-xhigh.md) | 對 live runner 執行順序的 finding 經核對為誤讀；另將 R03 的 discard 範圍明寫為「該行」，四組同步修改 |
| Claude verification 02 | [xhigh 原始複核](reviews/claude-verification-02.md) | 兩項 blocker 判定 READY。真實 probes 覆蓋的是生成前停止，沒有冒稱已觀察到 Opus 生成中的 API 529／逾時；這些部分輸出情形另由回歸案例涵蓋 |
| Codex verification 02 | [原始複核](reviews/codex-verification-02.md) | 檢查原始入口順序、回歸測試與四組 R03 修訂，撤回第一項 finding，確認第二項已關閉；沒有剩餘 blocker |

先前另嘗試 `claude-opus-5-5 max` 廣範圍審查，900 秒逾時且沒有可用評審；它記為失敗嘗試，不列為通過的審查。之後以明確範圍的 `xhigh` 取得完整意見。Claude 的第二輪只核對實際 blocker 的修正及失敗路徑 probe，兩項均關閉。複核另指出硬中斷恰好發生於寫入 generation 紀錄之後、記錄 halt 之前時的 resume 空窗；正式前補上啟動任何新名額前重查舊 trace／ledger 的行為，23 項 runner tests 通過，包括該中斷窗口的回歸案例。這項修改不回寫先前 probe bundle，也不宣稱原 probe 已執行新版 source。另補分析／archive／status 的一致拒絕條件：即使已有 40 筆，存在 halt 或已記錄的 boundary violation 仍不能報完整研究的區間。這是在正式資料產生前的完整性修正，沒有改變主要終點、分母或統計方法。

歷史二審 29 項、方法審查 22 項及新增 inventory 32 項的逐項去向見 [review resolution](review-resolution.md)。撤回不當主張與取得實測證據是不同的關閉層級。

## 執行與驗證狀態

[開發驗證紀錄](reviews/development-evidence.json)保留各 campaign 的來源 hash、完整名額及實測隔離 probe。原始兩個 pilot（A0、C）已各完成一次，兩份候選各通過 103 項外部檢查；它們只用於開發驗證，**不計入正式 40 個名額**。pilot 使用的舊版 bundle 原封保留，之後的分析定義與 runner 修正必須在正式封存前完成。

正式前另做短逾時及極低 CLI 預算的 operational probes，確認停止名額不會被重抽，也不會因缺少正常模型訊息而冒充觀察到模型漂移。這些 probe 另有 campaign，不回填原 pilot 或正式分母。正式版本已於 2026-09-25 04:24:12 UTC 封存，manifest SHA-256 為 `ba30398118ecde62b2f682884c1e882b2864c22d70faf99549ceab0d7c0a55f2`。來源共 26 份檔案；[正式前 83 項測試](reviews/validation-before-formal.json)全部通過。OS 版本另在開始生成後才取得[補充紀錄](reviews/runtime-supplement.json)，不冒充 pre-freeze OS pin。[正式結果](../../experiments/same-spec-ten-runs/RESULTS.md)已記錄完整 40 次、四組各 10/10 通過與結構描述，並連到完整封存與整批重評。40 份候選每份 103 項 case outcomes 都與第一次正式評測一致，沒有新模型請求或增加生成樣本。

## 圖表、語言與發布條件

[圖表工件](../2026-11-same-spec-ten-runs.figures.md)已完成 F1／T1／T2 的正式來源核對、T3 結果表及 F2 正式圖。F1 使用 Mermaid 11.17.2 真實算繪並通過尺寸檢查；F2 使用封存 renderer 與固定 matplotlib 依賴，完整呈現 180 個 pair 值與 40 個 seed 值，固定 0–1 座標。兩張圖都已實際檢視，不以語法或產圖命令成功取代視覺檢查。

本輪執行 zh-TW MCP 的技術文章檢查。自動替換仍需語意判讀，例如測試「通過」不能改為「透過」，研究「登錄」也不能改成「登入」。全文核對包含結語中的限制，不能只修 TL;DR。

未完成的文章發布條件：四篇成稿、篇內引用與圖表排版的最終檢查，以及來源 `2607.02436v2` abstract／PDF metadata 差異的明確註記。實驗完成不會自動使四篇文章或這項外部版本問題變成已完成。

正式後的文字澄清：獨立資料核對指出，trace 只能證明 Haiku 出現在 `modelUsage` 計費明細、沒有出現在候選生成 assistant 訊息，無法證明其 CLI 內部用途。因此結果改採這個較窄說法；原協議的 bookkeeping 用語保留在凍結包，現行 [PROTOCOL](../../experiments/same-spec-ten-runs/PROTOCOL.md)另加有日期的澄清，沒有改寫原始 source、資料或分析定義。

正式資料另經[獨立稽核](../../experiments/same-spec-ten-runs/results/validation-2026-09-25/formal-data-audit.md)，判定 READY，1,903／1,903 項核對通過。稽核涵蓋排程、來源、trace、分母、317 份公開檔案、40 份投影及完整重評證據。它是另一次 AI 代理的資料核對，不是人類盲審，也沒有新增生成名額。


## 2026-09-25 首輪全文撰寫紀錄（額度重置前）

依使用者要求，四篇分別呼叫 Claude Code `claude-opus-5-5 --effort max` 主寫；[實際呼叫紀錄](manuscripts/writer-provenance.json)與四十個研究名額分開保存。變異篇正常完成，規格篇留下部分正文，總論與契約篇沒有完整正文。另三篇續接遇到 Claude session 額度限制，小型探測確認預計臺北時間 16:10 重置；沒有改由其他模型代寫，也沒有背景重試。

變異篇經主代理全文潤飾，以及證據、編輯與讀者三種角度的獨立複核，問題均有處置。新增真實候選對照明標事後教學示例，沒有回填事前分析。正文與貼稿的 strict zh-TW MCP 均為 errors=0、warnings=0；語境誤報逐項記錄，不做整批替換。圖表已檢視，F2 原檔與貼稿 PNG 雜湊一致，正式 317 份封存檔案未變。詳見[成稿狀態與驗證](manuscripts/STATUS.md)。

A2 的版本化 PDF 已再次下載核對，雜湊與原查證一致；摘要頁與 PDF 首頁題名差異仍存在。變異篇使用 PDF 首頁完整題名及 v2 連結，沒有把這次核讀說成重現作者實驗。舊文承接也區分已發布系列與尚待發布稿。這輪完成的是變異篇本機全文，系列仍未完成，更沒有發布到遠端。

## 成稿階段發現的方法限制

全文逐字複核找到 A0／A 的 CLI 範圍措辭強度差異，詳見[補記](manuscripts/packet-wording-caveat.md)與[獨立複核](manuscripts/review-wording-caveat.md)。上表保留的是執行前評審當時的判斷，不能用較早的等價判定蓋過後來發現的差異。現行正文、RESULTS 與 T1 已改成共同規範基準，並保留比較限制；沒有改寫凍結 packet、evaluator、候選或數值，也沒有補抽名額。


## 2026-09-25 額度重置後的四篇成稿

依使用者選擇維持 Claude Code `max`。實際 CLI 請求確認恢復後，以章節資料包續寫，規格篇後半、總論前後半及契約篇前後半均完整產出。四篇現在都有中文全文，主代理依現行風格逐段潤飾，另讀後半部至結語，並完成證據、編輯與讀者三種角度的獨立複核。

所有正文與貼稿的實際 zh-TW MCP 嚴格回報皆為零錯誤、零警告，資訊提示另附逐項判讀。20 張圖表已檢視，四份貼稿與 converter 同步，317 份正式封存檔案沒有變動。契約篇分類與環境控制的證據修訂也留下原意見與差異紀錄。實際版本、呼叫、複核及交付驗證見[品質紀錄](manuscripts/STATUS.md)。首輪未完成的紀錄保留為歷史，不能再當作目前狀態；本輪仍未發布到遠端。

## 2026-09-27–28：依作者閱讀意見重寫敘事

作者指出前版動機、系列連貫、故事性與 spec 比較不足。先建立全系列共同 brief，再由實際 Claude Code max 重寫四篇。額度恢復後四篇全部完成；主代理逐段核對凍結 spec、研究資料與既有系列，修正條文編號、helper 適用範圍與 AST hash 的使用界線，再處理 Claude xhigh 全系列讀者審查。

本輪使用實際 zh-TW MCP 檢查四份正文與四份貼稿，全部零錯誤、零警告；資訊提示保留語境處置。12 張 PNG 已檢視，桌面與手機預覽通過，317 份研究封存未變。本輪沒有新增實驗名額，沒有把編輯建議回填成事前研究計畫，亦尚未發布。見[本輪品質紀錄](manuscripts/STATUS.md)。
