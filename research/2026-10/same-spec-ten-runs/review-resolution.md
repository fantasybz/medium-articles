# 「同一份規格，跑十次」評審處置紀錄

修訂日期：2026-09-25。對應[目前採用的大綱](../2026-11-same-spec-ten-runs.md)與[公開證據核對](evidence-audit.md)。原[大綱](../../2026-09/2026-11-same-spec-ten-runs.md)及 [2026-09-07 Codex xhigh 評審](../../2026-09/codex-review-2026-11-same-spec-ten-runs.md)保留為歷史，不以舊檔前言的「已修」替代本次逐項檢查。

**研究設計、正式 40 次、外部驗收、分析、可公開封存及整批重評已完成。** 四組各 10/10 通過，40 份候選的 103 項 case outcomes 重評一致；下表補上資料層證據。四篇文章仍待成稿，來源版本限制保留。執行入口為[實驗 README][experiment]，不能把工具測試通過改寫成正式模型結果。

正式前的證據與時序如下：

- [開發驗證紀錄][development]保留原始 A0、C 各一次 pilot，以及另外四個 timeout／budget-stop probe 名額。兩個原始 pilot 的候選各通過 103 項外部檢查；這六個開發名額的來源版本、用途與狀態分開保存，全部排除於正式 40 次之外。真實失敗 probe 覆蓋的是生成前停止；529 與部分輸出的分類另外由離線回歸案例驗證。
- [正式前驗證清單][validation]與[完整測試紀錄][tests]記錄 83 項研究工具測試全數通過，包含規格覆蓋、外部 oracle、突變案例、macOS 隔離、streaming、台帳／分析、公開 projection 與重評的拒絕條件。另記錄本輪稍早已通過的既有 repo 測試 301 項及研究 scripts 測試 108 項；這些是回歸檢查，與每候選的 103 項驗收、正式名額數各有不同分母。
- [Claude verification 02][claude-v2]關閉兩項指定 blocker；[Codex verification 02][codex-v2]撤回入口順序的誤讀，並確認四組 R03 修訂。兩份複核都保留原有範圍。之後新增的 resume 空窗及 halt／boundary violation 分析拒絕條件由回歸測試確認，時序見 [research loop][loop]，不把後來的修正倒寫成舊 probe 已驗過。
- 正式 bundle 於 **2026-09-25 04:24:12 UTC** 在本機封存，包含 40 個預排名額、四組 packet、source 與 runtime 記錄。manifest SHA-256 為 `ba30398118ecde62b2f682884c1e882b2864c22d70faf99549ceab0d7c0a55f2`，已寫入[正式前驗證清單][validation]；清單所列工具 source hashes 與正式 bundle 相符。原 manifest 及執行包已保留於本機，另有逐 byte 相同的[可公開 manifest][manifest]與[完整封存索引][archive]；原始 trace 留在本機，公開 projection 明列刪除欄位及 raw／projection hashes。這是本機執行前封存，不是第三方預註冊。

本輪方法審查來自 `.context/same-spec-ten-runs/method-review.md`，其中前段提出原創付款案例，第 12 節改成 tool-free；使用者後續明確要求使用自己的 repo，因此本輪採 **目前 medium-articles 的真實 parser bug**，不採前段付款案例。方法報告的先前提案保留為修訂歷史，不能混進 active spec 或正式樣本。

固定基底 commit：`37f6c0ce9b536f95132d5e01a387f380bbb9639c`。task：`research/scripts/codex_jsonl.py` 對合法 JSON 錯型別造成 crash 或假成功；目標為 shape anomaly exit 6、終局優先序 3 → 6 → 4 → 5 → 0，以及正常 legacy streaming 相容。四組是同要求的精簡／展開 spec、rationale 與純文字 pattern；固定 Claude high effort、tool-free、單一 JSON/file output。正式 40 名額、10 個事前隨機排程區塊已完整執行；2 次原始 pilot 與 4 次停止路徑 probe 另列，不併入正式資料。

## 一、既有評審的 29 項逐項處置

ID 與本次 `.context/same-spec-ten-runs/issue-inventory.md` 對齊。評審中的六項刪除建議即使與前項重複，也保留獨立列，確保沒有漏件。

| ID | 原評審要求 | 本輪處置與大綱位置 | 關閉證據／仍開放之處 |
|---|---|---|---|
| R-F1 | sampling 不能是唯一變異來源 | 撤掉唯一 entropy／機制全在 loop 的說法；大綱三、八區分本機控制與 provider 不透明 | 主張已撤；[protocol][protocol]與[開發 probes][development]區分可觀察邊界及未知 context，[正式前驗證][validation]記錄凍結 hash；provider 不透明仍是限制。 |
| R-F2 | 刪「沒人量過／第一次」 | 大綱一、四改為已有研究，本輪交付可追溯 repo 量測；evidence audit A2 核到結構數量資料 | 主張已撤，見 [audit A2][audit]；abstract／PDF metadata 差異仍開放，沒有因工具就緒而關閉。 |
| R-F3 | 50 runs／真人／多篇中英／大量圖的工作量不實際 | 大綱三、九、十改 40 正式＋2 pilot；刪舊 model 組、真人工作承諾與同步發布日；圖縮到 5 個必要工件 | 範圍已修，見[大綱][outline]與[正式前驗證][validation]；[40 個名額已完成][results]，沒有真人研究或四篇成稿。 |
| R-F4 | F8 不能把 Dockerfile 文獻放低變異實點 | 新圖表清單不沿用 F8，沒有任意座標或授權象限 | 已撤除，見[目前圖表工件][figures]；無舊 F8 文獻座標或授權象限。 |
| R-F5 | Go／Java worked example 不一致 | 四篇統一 current repo 的 Python JSONL parser；真實 seed 與兩個反例已由固定 commit 重現 | [task provenance][task]、[基底 bug 重現][baseline]與[oracle／規格測試][tests]已完成；[設計審查][claude-design]確認 103 案例可追溯，也明列未涵蓋的規格細節。 |
| R-M1 | 獨佔來源數字反覆重述 | 新 active 稿不使用那三組 harness-pin 數字；各核對來源分派明確用途 | [目前大綱][outline]與[audit][audit]已採少數核對來源；舊三組獨佔數字退出論證。 |
| R-M2 | repo-level complexity 觀察不能當 run-to-run 機制 | 移除 2608.25241 的因果借用；結構差異與維護成本分開 | 不當論據已撤，見[大綱][outline]與[protocol 限制][protocol]；沒有維護成本資料。 |
| R-M3 | 不可說需求總是晚到 | 規格篇只談本 task 版本與 amendment，不沿用普遍化句子 | 普遍化句子已撤，見[大綱][outline]；本輪修訂時序見[research loop][loop]。 |
| R-M4 | 不可將完整 spec 說成必要條件 | 規格篇以語意要求可比與 coverage 為目標，不宣稱必要／充分定理 | [四組 requirements][requirements]、[規格覆蓋測試][tests]及[Claude 語意審查][claude-design]已確認本 task 的要求可比；仍不宣稱必要／充分條件。 |
| R-M5 | reproducibility 1.000 不能等同 bit-for-bit 或僵硬度 | 不沿用 2608.26197，刪 build 類比及未量成本 | 已撤除，見[大綱][outline]與[audit][audit]；來源雜湊只用於完整性，不推出僵硬度或維護成本。 |
| R-M6 | Uncle Bob 的 same spec 8 times 不受支持 | 不以該案例開場，不沿用 same spec 或固定組態 N=8 | 已撤除，見[大綱][outline]；未來若重引該案例，須另核原 repo。 |
| R-M7 | G2 混入 A/B/C 研究 arm | 本輪完全移除 production 擴權 gate；40 次是研究名額，不是每季營運預算 | 已撤除，見[protocol 範圍][protocol]；正式 40 次不構成 production 擴權門檻。 |
| R-M8 | 30 PR 排 3 warm-up 後仍用 n=30 | 沒有真人 review，本輪不列 review minutes、Spearman 或 warm-up 數據 | 已撤除，見[protocol][protocol]與[analysis 測試][tests]；沒有 review minutes、人類基線或 warm-up 數據欄。 |
| R-M9 | Spec 不可攜標題過大 | 契約篇改外部 parser 驗收，不作跨 vendor 可攜性結論 | 已撤除，見[大綱][outline]與[protocol][protocol]；僅驗本 parser，不推論跨 vendor 可攜性。 |
| R-m1 | CLAUDE.md 安全規則不可泛化所有 conventions | 不沿用 4.4–16%及普遍 enforcement 推論；B/C 明定為文字介入 | 文字推論已修；[真實隔離 probe][development]與[隔離回歸測試][tests]支持本機邊界，不能泛化成所有 conventions 已受 enforcement。 |
| R-m2 | digest 未報不等於論文未報 pass rate | audit A1 讀全文後更正；新稿不再寫未報，也不把未顯著當等價 | 全文解讀已修，見 [audit A1][audit]；正式模型結果尚待評分。 |
| R-m3 | 壞變異分類三層不一致 | 改「契約結果／待解讀結構差異／資源使用」，不把低相似度自動判壞 | 分類已修，見[大綱][outline]、[protocol][protocol]與[analysis 測試][tests]；沒有真人語義判讀，不能把相似度低直接判成壞變異。 |
| R-m4 | pseudo-config 不能稱 reference implementation | 新稿只連實驗包；規格／設計與已驗證工具分開，未 render 圖與未執行程式不報完成 | 工具已有[83 項測試紀錄][tests]、[開發實測][development]及[來源 hash][validation]；[正式封存][archive]與[40 份重評][rescore]已完成；文章仍未成稿。 |
| R-D1 | 刪首次量測主張 | 同 R-F2；大綱總論、三部曲與未製作 hooks 均不預設首次 | 已撤除，見[大綱][outline]、[audit A2][audit]；對應 R-F2。 |
| R-D2 | 刪跨系列三組獨佔數字 | 同 R-M1；本輪少數已核對 anchors 取代舊引用堆疊 | 已撤除，見[大綱][outline]及[audit][audit]；對應 R-M1。 |
| R-D3 | 刪前代 model 迷你組 | 不在 40 正式或 2 pilot 名額內，也不預測 model 已吃掉 skills | 已撤除，見[正式範圍][protocol]與[凍結紀錄][validation]；無前代模型對照名額。 |
| R-D4 | 刪 F8 文獻實點 | 同 R-F4；新 figure 需求沒有該圖 | 已撤除，見[圖表工件][figures]；對應 R-F4。 |
| R-D5 | 刪 bit-for-bit 類比 | 同 R-M5；只保留實際定義的 artifact hash，hash 不是距離 | 已撤除，見[指標定義][protocol]與[analysis 測試][tests]；雜湊相等不當作距離。 |
| R-D6 | BDD 回顧壓半節 | 不回顧 Dan North／四色卡；直接用 parser 要求與反例建立 spec | 已按 parser 要求重切，見[大綱][outline]與[requirements][requirements]；四篇仍待成稿。 |
| R-A1 | 加 Threats to validity | 大綱三、八明列單 task、單檔、tool-free、選題、provider、small n、descriptor 與真人缺口 | 限制已納入[大綱][outline]及[protocol][protocol]；[複核][claude-v2]保留 probe 覆蓋限制，正式執行若有 deviation 須另記。 |
| R-A2 | 加結果 CSV schema | 要求 run 台帳、status、AC 明細、pairwise 另表；實際 field/type/NA 規則以 freeze 版本為準 | [固定 JSONL／summary 定義][protocol]及[完整性、NA、分母測試][tests]已通過；實作採 JSONL／JSON；正式台帳尚待完成。 |
| R-A3 | 補 N=30 終局判定 | 採方法審查更嚴格修法：撤結果觸發加樣，固定 10/arm；另輪 N=30 須新 protocol | 原結果觸發加樣 gate 已撤；[正式前驗證][validation]對應固定 40 名額封存，不用事後門檻追加樣本。 |
| R-A4 | 加 contract_surface 避免 refactor 誤擋 | 本輪撤通用 path/label drift gate；單一候選檔由外部 stdout/stderr/exit/streaming 契約驗收 | 通用 path／label gate 已撤；[單檔與 symlink 拒絕、schema、streaming 測試][tests]已通過，外部契約與[規格覆蓋限制][claude-design]一併保留。 |
| R-A5 | 加 source audit table | 已有五份 versioned primary-source audit 及完整 37-ID local inventory；其他來源退出 active 論證 | [五份 versioned source audit][audit]已完成，37-ID 本機 inventory 保留；未宣稱查證 37 份全文或獨立重現，A2 metadata 仍開放。 |

## 二、方法審查：採納、改寫與未完成條件

下表分開「設計與工具已驗證」和「正式資料仍待完成」。右欄連結到實際工件；測試通過只關閉其覆蓋的行為，不能保證所有實作或一般化結論。第 12 節 tool-free 方案與使用者指定的 repo task 優先於方法報告前段的 tool-enabled／付款案例。

| ID | 方法問題與來源位置 | Active 方案 | 已取得的關閉證據／資料層待辦 |
|---|---|---|---|
| M01 | 真實性與 task 選擇；方法§2、最新使用者指示 | 固定 medium-articles commit 與 parser；付款 fixture 不作正式資料 | 已由[task.json][task]、[baseline reproduction][baseline]及[seed 固定 commit 測試][tests]核對；實驗候選不覆蓋 production parser。 |
| M02 | arm 與時間混淆；§1/4 | 10 區塊×4 組、區塊內事前隨機、按 schedule 順序執行 | [凍結紀錄][validation]已對應 40 名額、10 區塊、seed 20260925；[schedule／resume 測試][tests]通過。[正式封存][archive]保存實際 launch 台帳，區塊不表示同步時間窗。 |
| M03 | A0 漏要求、字數被當單獨原因；§2 | 精簡 A0 與展開 A 含相同規範；A/B/C 共享完整 spec | [requirements][requirements]及[同規範 ID 測試][tests]通過；[Claude 設計審查][claude-design]逐條確認語意等價，[Codex 複核][codex-v2]確認四組 R03 同步修訂。 |
| M04 | C 同時加 skill/hooks/settings；§2/12 | C 只增加 text pattern，共同 tool-free 設定固定 | [requirements][requirements]明定 C = B + optional text pattern；[規格測試][tests]與[設計審查][claude-design]核對，沒有新增 native Skill、hook 或工具權限。 |
| M05 | 真正受測對象；§12 | 模型一次產生 JSON 單檔，無工具、無 hidden feedback、無同名額修復輪 | [兩個 pilot 的 trace 判定][development]與[邊界 parser 測試][tests]支持已觀察的 model／能力邊界；[Claude 複核][claude-v2]確認 unknown 與 violation 分開。每個正式 run 仍須逐筆核對。 |
| M06 | 全域 context 與其他 run 污染；§4/5/12 | 空白 cwd 與獨立設定/session；輸入只含 allowlisted packet | [protocol][protocol]與[凍結驗證][validation]記錄明示 packet、CLI／Python、允許的環境控制；[environment 測試][tests]不存憑證。不可見 inherited/provider context 未被完整固定，這是保留限制。 |
| M07 | 評估器被改寫／candidate 讀答案；§5/12 | 外部 driver 保存 expected；封存候選；candidate 只收案例 input 並受 sandbox | [開發隔離 probe][development]已觀察讀／寫／網路拒絕；[真實 sandbox、oracle、突變測試][tests]通過。驗收為 103 項外部檢查，範圍不足處見[設計審查][claude-design]。 |
| M08 | output extraction 事後修補；§12 | 凍結 JSON/file schema 與 extraction 規則，拒絕錯型別／越界檔名 | [精確單檔 allowlist／JSON extraction 測試][tests]通過，含 code fence、錯型別及邊界違規；[開發 traces][development]有實際候選，未做事後修補。 |
| M09 | pilot 與 formal 混用；§3/12 | 2 pilot 獨立保存，40 formal 另排；正式前 freeze | [開發紀錄][development]分列原 2 pilot、另 4 failure probes 及各自 source hash；[正式前驗證][validation]連到全新正式 manifest。正式來源沒有沿用舊 pilot bundle 的已修宣稱。 |
| M10 | 成功定義混用；§6/12 | 三欄 cli_success/artifact_success/accepted_completion | [success flag 與 evaluator fault 測試][tests]通過，[開發紀錄][development]保留成功／停止案例；primary 仍為兩欄皆真。正式三欄結果尚待完成。 |
| M11 | censoring 與補抽；§8 | request 開始就占名額；timeout/error/schema failure 保留 primary 分母，不補抽 | [真實 timeout／budget probes][development]保留原名額，[Claude 複核][claude-v2]確認沒有 halt 或補抽；[interrupted／missing 台帳測試][tests]通過。[正式 40 槽][ledger]均為 completed，沒有補抽或缺槽。 |
| M12 | evaluator fault、model drift 與 missing；§8 | evaluator 故障按量測失敗停收，不記成候選失敗；修正須 amendment 與整批重評；identity/hash 不符停止正式 collection | [CLI 無關的評分、evaluator fault、resume 漏停與 halt 拒絕測試][tests]通過，[Claude 複核][claude-v2]與[修訂時序][loop]可追溯。[正式全 cohort 重評][rescore]已完成且逐 case 一致；本次沒有修改 evaluator，未發生量測 amendment。未來修正仍須另記。 |
| M13 | 主比較與統計單位；§6/7 | 只報各組預先指定的結果與區間，不做組間 contrast 估計或配對檢定 | [protocol][protocol]已固定僅各組摘要；[report 無組間 contrast、pair 分母測試][tests]通過。正式結果未產生，不能把 45 pairs 當獨立樣本數。 |
| M14 | 區間、等效與十連勝誤讀；§7 | 報 k/10、two-sided 95% exact 區間與假設；不推等效/pass^10/production gate | [0/10、5/10、10/10 exact interval 測試][tests]通過，[設計審查][claude-design]核對 10/10 下界約 69.15%；這是方法數值，並非宣稱正式觀察到 10/10。 |
| M15 | 相似度定義不實／共享 base 掩蓋差異；§6.3/12 | 僅候選 parser、固定 AST descriptor；依實作正確命名 | [固定 metric 定義][protocol]、[seed／AST／雜湊測試][tests]與[source hashes][validation]已完成。AST node-type multiset cosine、normalized hash 與 seed cosine 分別命名，不稱 tree-edit 或維護性。 |
| M16 | parsefailure、no-op 與 success slice 偏差；§6.3 | NA 保留原因；empty 留 NA；unchanged seed 的 cosine 可為 1，驗收結果獨立報告；主描述納入全部可解析候選，不另做成功子集合 | [empty、缺 artifact、有效 pair 分母與 seed cosine 測試][tests]通過。unchanged seed 的 cosine 可為 1；正確性另看外部驗收，empty 留 NA。主描述涵蓋全部可解析候選，不另挑 accepted 子集合；正式 pair 清單待產生。 |
| M17 | 沒有真人仍推成本／校準帶；§9 | 不收集真人審閱時間或真人校準資料（沒有填入虛構欄值） | [protocol][protocol]與[research loop][loop]明列 AI review／fixture 身分；沒有真人 review minutes 或 calibration 數值。此項以移除主張關閉，不以 AI fixture 補人類基線。 |
| M18 | 資源使用混分母／把 token 當全成本；§6.2/8 | 分 token/cache/費用/wall；失敗也報；缺失不是零 | [開發紀錄][development]保留 usage、cache、auxiliary model 與 CLI list-price cost；[缺失／alias／失敗耗用測試][tests]通過。[protocol][protocol]明列 budget 不是嚴格金額上限，[正式資源分母][results]為各欄 40/40，沒有截尾名額；仍不推算未被觀察的完成成本。 |
| M19 | 正式樣本結果導向加量；§8 | 固定 40；取消紅燈才 N=30 與前代 model 對照 | [正式前驗證][validation]記錄固定 manifest；[完整 40 槽、重複／未知／缺少 record 拒絕測試][tests]通過。實際名額一致性於正式完成後核對，不預先關閉資料層。 |
| M20 | 框架圖、hypotheses 預設贏家；§11 | 五項必要 figure/table；流程圖及規格表已製作，結果圖不預填數值，也沒有 A<B<C 主結論 | [圖表工件][figures]已有 F1 流程圖及 T1／T2，算繪與檢視見[research loop][loop]；T3／F2 必須等正式資料，沒有預填贏家或效果。 |
| M21 | nativeworkflow 未用卻報已執行；§12 | 按 repo stages 使用 CLI/manual adapter 時明說 adapter | [research loop][loop]與[review index][review-index]已保存 CLI/manual adapter 的輸入／輸出／hash 及採納紀錄；未聲稱呼叫 native Workflow。 |
| M22 | streaming 相容被 batch 測試取代；task 要求 | externalcontract 包含逐行 flush／順序與 legacy 正常案例 | [真實 before-EOF probe 與整段緩衝突變測試][tests]通過；[兩個 pilot][development]各通過含 streaming 的 103 項外部檢查。正式每個候選仍須由同一 frozen oracle 驗收。 |

正式協議的細節以已封存 bundle 為準。[驗證清單][validation]保留工具與 manifest 的對應 hash；正式生成的固定模型為 `claude-opus-5-5`、effort `high`，CLI 2.1.282、Python 3.14.5／macOS。每名額 600 秒、CLI USD 5 list-price 停止門檻均已列入[protocol][protocol]；USD 5 不是嚴格金額上限或實際帳單。正式期間不改 source、規格、主要終點或分析定義；若出現量測故障，保留原始證據、記錄 amendment，不能回寫 frozen bundle。

## 三、新增 inventory 問題的去向

這張表讓 `.context` 內的 32 個新增問題也能追蹤；同一個根因可能由多個 M 項共同處理。

| Inventory ID | 問題 | 處置／仍開放之處 |
|---|---|---|
| N01 | 原 37 來源未核實 | [audit][audit]只恢復五份已讀全文來源；其餘未核對來源不作 active 論據，沒有標全部 verified。 |
| N02 | 兩人一 pair 當校準帶 | R-m3、M17：已在[大綱][outline]與[protocol][protocol]撤除人類校準帶及門檻；沒有補造人類資料。 |
| N03 | A0 不是純厚度 | M03：[requirements][requirements]、[語意審查][claude-design]及[規格測試][tests]已確認同要求；字數純因果主張已撤。 |
| N04 | Cbundle 混因果 | M04/M05：[規格][requirements]明寫 C = B + text pattern，[設計審查][claude-design]已核對；runtime 功能固定。 |
| N05 | agent 修改評測 | M07/M08：[單檔封存、外部 oracle、隔離與竄改測試][tests]通過；正式候選完整性仍逐筆驗證。 |
| N06 | 小差異等於無效果 | M14：[protocol][protocol]與[interval 測試][tests]只支持描述及區間；沒有把小差異解讀成等效。 |
| N07 | 相似度等於統計 variance／維護性 | R-m3、M15/M17：[指標定義][protocol]及[分析測試][tests]分開 descriptor、正確性與資源；不推維護性。 |
| N08 | 成對 median 與向心 median 混用 | M15/M16：[固定來源 hash][validation]及[summary／pair 測試][tests]確認目前定義；正式摘要尚待產生。 |
| N09 | pairwise pseudo-replication | M13/M16：[protocol][protocol]與[pair 分母測試][tests]保留 run 共用造成的非獨立性，不以 pairs 擴大 n。 |
| N10 | 計畫被寫成實測 | M20：[research loop][loop]與本表區分工具已驗證、formal 已量測並重評、文章未成稿；不再沿用「全部未執行」或「全部完成」。 |
| N11 | skills 成本先借文獻下界 | 已在[大綱][outline]及[protocol][protocol]撤預期成本範圍；不預設 C 的 token 或品質方向。 |
| N12 | 排除 turn limit／人工介入 | M11/M12：[開發失敗 probes][development]及[中斷／停止測試][tests]保留分母，不補抽；正式缺失與中止仍待逐筆審查。 |
| N13 | runner 丟 exitstatus | M10/M11：[runner／三種成功狀態測試][tests]及[真實停止紀錄][development]已驗證 status、returncode、timeout 保留；正式台帳待完成。 |
| N14 | worktree 未隔離 | M05–M07：[真實 sandbox probe][development]、[隔離測試][tests]與[CLI 複核][claude-v2]已完成；不可見 context 限制仍列於[protocol][protocol]。 |
| N15 | 按 arm 分星期執行 | M02：[正式前驗證][validation]對應固定 10 區塊排程，[schedule 測試][tests]通過；實際 launch 時點保留於[正式封存][archive]。 |
| N16 | reviewblindness 與學習效應 | M17：本輪已在[protocol][protocol]撤真人 review 量測；[AI review 紀錄][loop]沒有冒稱人類盲審。 |
| N17 | 紅燈後追加樣本 | M19：[protocol][protocol]及[正式凍結紀錄][validation]已取消 N=30 救援；資料完成後仍須核對沒有追加名額。 |
| N18 | 26%與 rule of three 混淆 | M14：[exact interval 測試][tests]核對雙側 95% 定義，見[protocol][protocol]；不混用 rule of three。 |
| N19 | G2 圖准黃燈但正文門檻不同 | R-M7：[大綱][outline]與[目前圖表][figures]已撤 production 授權 gate／象限。 |
| N20 | 30/40/50/90 樣本混亂 | M09/M11/M19：[開發紀錄][development]分列 2 原始 pilot + 4 failure probes，皆排除正式 40；[凍結紀錄][validation]固定 10/arm，沒有真人／舊模型／季度樣本。 |
| N21 | 改 spec 一字即 driftgate 放行 | R-A4：[requirements][requirements]與[stdout／stderr／exit／streaming 測試][tests]驗本 task 行為，已撤通用 path／label gate。 |
| N22 | 特選只讓 skill 有答案的 task | M01/M03/M04：[真 bug 重現][baseline]與[四組語意審查][claude-design]已完成；[protocol][protocol]仍揭露選題者參與及單 task 限制。 |
| N23 | D10 把 exploit 變動寫 benchmark 分數 | 該來源退出 active 論證，見[audit][audit]與[大綱][outline]；未沿用 70 points 或 N=10 口號。 |
| N24 | 文件互動占比寫成閱讀時間 | 已在[大綱][outline]撤該 hook；[protocol][protocol]不量測閱讀時間或真人 review 時間。 |
| N25 | 圖箭頭暗示未證因果 | M20：[F1 與圖表規劃][figures]只表實際流程，算繪與檢視見[research loop][loop]；T3／F2 採正式資料，不用 pilot 或預設收益。 |
| N26 | pass 與 variance 稱統計獨立 | [大綱][outline]與[protocol][protocol]分別描述驗收、結構、資源；已撤統計獨立性與運氣判斷。 |
| N27 | model/CLI 可用性未核對 | M05/M06：[真實 pilot／probes][development]與[Claude 複核][claude-v2]已核對 CLI 2.1.282 及生成 identity；[正式前驗證][validation]記錄最終 bundle hash，正式每次生成仍檢查。 |
| N28 | 社群授權／日期／人氣排名 | [大綱][outline]沒有沿用未核對原句、授權、人氣或日期；公開來源範圍見[audit][audit]。 |
| N29 | 成本欄位／每 0.1similarity 價格無定義 | M18：[費用與 usage 定義][protocol]、[真實開發紀錄][development]及[資源缺失測試][tests]已完成；未造每 0.1 similarity 的價格。 |
| N30 | 來源版本／精度不一致 | [audit][audit]以 version URL／hash 區分來源；A2 外部 metadata 仍開放，數值解讀保留各自分母。 |
| N31 | 結語保證零壞變異或替換未支持假設 | [大綱][outline]與[protocol][protocol]保留未支持就報未支持的條件；[正式結論][results]保留 10/10 的區間限制、沒有等效／維護成本推論；文章成稿後仍須檢查結語。 |
| N32 | 四槓桿／迷你第四組／月份預告混用 | [大綱][outline]與[requirements][requirements]統一四組；月份僅歸檔，不承諾發布；四篇仍待成稿。 |

## 四、資料驗證結果與仍開放的發布條件

1. **外部來源版本：** [audit A2][audit]記錄的 `2607.02436` abstract 與 v2 PDF 標題／頁數差異仍需再次核對。這不影響撤掉「沒人量過」的過度主張，但正式引用須保留所讀版本、hash 與差異註記。
2. **正式資料已取得：** [40 個名額][ledger]全部保留，四組各 10/10 通過，無補抽、缺少候選、逾時或邊界違規。每候選 103 項驗收、資源分母及 structural descriptors 見[正式結果][results]。存在 halt、已觀察到 boundary violation 或缺槽時仍拒絕完整研究區間，本次沒有這些情況。
3. **正式封存與重評已完成：** [可公開封存包][archive]保存來源、輸入、候選、驗收及投影 trace。由此包的 frozen oracle 在新空白 cwd、PATH 不含 Claude CLI 的環境[重新驗收全部 40 份][rescore]，每份 103 項 case outcomes 與原結果一致，沒有新模型請求或覆寫原結果。分析與 T3／F2 均讀完整正式資料。
4. **結果審查：** 兩份 verification 02 只關閉指定設計／工具問題；實際資料由另外的獨立核對覆蓋，不將設計 review 當成結果 review。[獨立資料稽核][data-audit]已判定 READY，1,903/1,903 項核對通過；具體範圍見[正式結果][results]，不稱為人類盲審。每個新增 deviation 都要回到本表相應項目，不能抹掉失敗名額。
5. **文章與發布：** 四篇目前仍是論證骨架，需要成稿、引用核對、圖表解讀、全文語言與發布檢查。真人成本、通用架構效果與 production 授權不在本輪範圍，不能在後半部、結語、英文版或社群文案重新加回。

本表保留原 29 項二審、22 項方法問題及 32 項 inventory ID。後續只在取得工件後補上資料層的證據連結與狀態，保留先前修改、review 撤回、開發失敗路徑及 protocol amendment 的時序。

[outline]: ../2026-11-same-spec-ten-runs.md
[audit]: evidence-audit.md
[experiment]: ../../experiments/same-spec-ten-runs/README.md
[protocol]: ../../experiments/same-spec-ten-runs/PROTOCOL.md
[task]: ../../experiments/same-spec-ten-runs/task.json
[baseline]: ../../experiments/same-spec-ten-runs/baseline-reproduction.json
[requirements]: ../../experiments/same-spec-ten-runs/requirements.json
[figures]: ../2026-11-same-spec-ten-runs.figures.md
[development]: reviews/development-evidence.json
[validation]: reviews/validation-before-formal.json
[tests]: reviews/study-tests-before-formal.log
[loop]: research-loop.md
[review-index]: reviews/index.json
[claude-design]: reviews/design-claude-xhigh.md
[claude-v2]: reviews/claude-verification-02.md
[codex-v2]: reviews/codex-verification-02.md

[results]: ../../experiments/same-spec-ten-runs/RESULTS.md
[manifest]: ../../experiments/same-spec-ten-runs/results/formal-2026-09-25/manifest.json
[archive]: ../../experiments/same-spec-ten-runs/results/formal-2026-09-25/archive.json
[ledger]: ../../experiments/same-spec-ten-runs/results/formal-2026-09-25/records.jsonl
[rescore]: ../../experiments/same-spec-ten-runs/results/validation-2026-09-25/public-rescore.json

[data-audit]: ../../experiments/same-spec-ten-runs/results/validation-2026-09-25/formal-data-audit.md
