# 規格篇全文：獨立證據審查

日期：2026-09-25。審查者：`series_evidence_review`。已完整閱讀標題、TL;DR、六節、References、AI 協作說明及署名。

**判定：主要證據核對通過；第 125 行有一項方法用語需要 minor 精確化。不是全系列 READY。**

正文：`2026-11-same-spec-spec/article.md`，35,738 bytes、194 行。全文審閱 SHA-256：`829017b621e70355979aa9ad6dc8830842fed52c74f00c95bbae53e52cedb8e6`。

## 唯一待修項

**SPEC-E01（minor），第 125 行：累加設計的限制寫得略廣，容易被讀成任何個別成分差異都不能估。**

原文：「這樣的設計無法把效果拆給個別成分，也估不出成分之間的交互作用」。

凍結 protocol 第 126–128 行明定本輪沒有組間 contrast estimator 或假說檢定。這是本研究分析範圍；累加設計在另訂分析時仍可估相鄰條件的條件性差異，例如在 B 內容之上加入 C pattern，但不能分離各成分跨組合的獨立效果或完整交互作用。

改成「本輪沒有估計組間差值；這種逐組累加的配置，也不能分離各成分在不同組合下的獨立效果或完整交互作用。」或同義限定。

## 全文核對

| 編號 | 本文行號 | 主題與核對結果 |
|---|---|---|
| SE01 | 3、17、19、20、21、24、26、159 | **真實缺陷與例示：**基底固定 commit、root []／null crash 與 numeric text 123 exit 0 均有凍結紀錄。本文 12／3 token 例子明標非原始重現字串，修補後 exit 6 明標由 R05、R08、R11 推導。結語沒有虛構事故或親歷情境。 來源：baseline:8–19,43–48；seed:39,43–45；requirements:69,102,135。 |
| SE02 | 28、30、109、117、190 | **生成設定、名額與寫作分界：**40 名額、每組 10、Opus 5.5 high、CLI 2.1.282、tool-free 與生成後統一評測符合 manifest。主寫 max 另由 invocation／assembly 證明，沒有把寫作 effort 或費用混入正式生成。 來源：manifest；summary；assembly。 |
| SE03 | 38、40、44、45、46、47、48、50、52、54 | **exit 與歷史語義：**舊 exit 5 以 truthiness 記錄發言的事實與修補後非空字串判準已分開。3 → 6 → 4 → 5 → 0、逐行繼續、turn.failed 例外、三條原 stderr 摘要與 exit 6 無摘要均符合凍結要求和測試案例。 來源：seed:43–45,62–71；requirements:124,135,146；evaluator:213–220。 |
| SE04 | 62、66、67、68、69、70、71、72、73、74、75、76、77、78、80 | **R01–R13 摘要表：**逐條核對未見反向規則。R10 已保留 error:null 例外，R03 例外明指失敗狀態與 stderr。表前明說只是摘要、不能只照表實作，完整格式仍以凍結規格為準。 來源：requirements；A0；A。 |
| SE05 | 82、84、86、88、90、92、94 | **相容性、語義等價與驗收覆蓋：**非 JSON 文字略過、未知字串 type 不驗 payload、重複事件相容均正確；作者理由與規格原文分開。A0/A CLI 措辭差異具體揭露，不將 ID／hash 當語義等價證明。literal main／額外 CLI 選項未逐一驗證的限制保留。 來源：A:15–19,29–33,129–133；A0:7,55；evaluator:240–349；wording_caveat。 |
| SE06 | 100、104、105、106、107、111、113、115、123 | **A/B/C 累加內容與 C 範圍：**A/B/C 前綴關係、理由與自查清單、可選純文字 pattern 都符合 packet。B/C 明文不增規範要求且繼承 A 的 CLI 限制，C 未冒充原生 Skill，malformed turn.failed 的失敗訊號也保留。 來源：B:135–150；C:152–173；wording_caveat。 |
| SE07 | 3、30、117、119、121、123、157 | **10／10 與區間：**四組 accepted 均 10／10，雙側 95% Clopper–Pearson 下界 0.6915028921812392，捨入 69.15%。沒有當成下輪保證、已證等效或可靠度勝負；共同通過機率與獨立性假設亦保留。 來源：summary；protocol:118–128。 |
| SE08 | 125 | **每組正規化 AST 不同：**每組 unique_normalized_ast_hashes 均為 10，引用變異篇展開；沒有把 hash 差異改稱品質或維護成本。 來源：summary。 |
| SE09 | 133、135、143、182 | **A1 成本研究：**5 tasks × 12 specs × 3 efforts × 15 repeats＝2,700；正式分析排除 oracle、11 規格。bare user story 相對 full 成本 +29.7%，90% credible interval +5.1–58.7%，95% −0.3–66.8% 含零，方向和數值正確。單一 Kimi K3、mini-swe-agent、按同一價目表估價，未泛化為跨模型 token 比例。資訊移除與本輪介入不同的限制保留。 來源：A1_snapshot:§3.1–3.3,§4.1,Appendix C/E；evidence_audit:15–26。 |
| SE10 | 137、139、183 | **A5 prompt/effort/harness：**核心 24 deterministic tasks、18 variants、4,644 valid runs 正確；語意要求與逐字重述區分，effort 依 harness policy 改變的限定對應 §3／§6.1。小任務與架構覆蓋不足的限制保留，沒有混入另一個 hard-task campaign 的數字。 來源：A5_snapshot:§2–3,§6.1,§11；evidence_audit:68–79。 |
| SE11 | 141、143、145、190 | **本輪成本、cache 與人力空白：**四組總成本相加為 5.692342，文章約 5.69；A0 1.248397→1.25、C 1.547817→1.55；wall 中位數 37.16–40.28 秒，約 37–40；cache read 全 0，creation 順序 A0/A/B/C 遞增。均標 CLI 牌價而非帳單，不含研究／寫作／pilot，未推 ROI、人時或跨任務效果。 來源：summary；protocol:143–149。 |
| SE12 | 147、149、184 | **修訂版本與 SaltBench：**usage:null 變更是明標假設與作者建議，沒有聲稱已執行新規格。SaltBench 的 freeze／dated appended amendments 只用來支持紀錄方式；同時說明原研究有隔離缺口，沒有將其視為完美保護證据。 來源：A4_snapshot:§2.1,§3.2；evidence_audit:54–66。 |
| SE13 | 11、115、135、159、185、186 | **系列 recall：**Harness 第 115 行支持 golden tasks；第 94 行支持文件指引與強制執行分界；第 75–76 行支持資訊用途與 100 行僅為維護建議。green 可靠度第 527 行的引文逐字可對，並標尚待發布，沒有把排程當已發布。 來源：harness_article:75–76,94,115；reliability_article:527；recall_report。 |
| SE14 | 3、13、90、92、125、143、155、157、159、161、163 | **開頭與結語一致：**從 123 假成功回到明確要求；結論交付核對方法與有限觀測，沒有從相同結果推成規格無用。CLI 措辭 caveat 在 TL;DR、§3、§4、成本比較與結語均維持，未重新宣稱已證純措辭效果。作者下一步建議與實驗發現有分開。 來源：wording_caveat；requirements；summary。 |
| SE15 | 178、180、181、182、183、184、185、186、190、192、194 | **References、AI 協作與署名：**來源版本與章節回指正確；研究附件明說僅本機，署名未宣稱已刊登。主寫 max、實驗 high、設計審查 xhigh 分開；AI 審查未冒充真人盲審或外部重現。MCP／多角度品質完成狀態指向動態紀錄，沒有由本報告代簽。 來源：assembly；evidence_audit；recall_report。 |

上表的 requirements／A0／A／B／C／seed／baseline／evaluator／protocol，均指 `research/experiments/same-spec-ten-runs/results/formal-2026-09-25/source/` 的凍結檔；manifest／summary 則位於該正式目錄。精確來源路徑與 SHA-256 見配套 JSON。

## 主寫來源與有限驗證

兩段 Claude 原文 hash 都與 `spec-assembly.json` 一致。原前半部確實來自先前未完整結束的 Claude max 請求所保留的文字；尾段由正常完成的 max 續寫提供。兩段直接合併的 hash 為 `ea582c917e1555c78373a0a5b2593784aaf2119ac8a75cb3299f5f0d608f5a8a`，與組合紀錄一致。這證明原稿來源與編輯前組合，不代表主寫未經主代理後續修改。沒有讀取或輸出 raw thinking。

本文共有 15 個目前存在的本機相對連結、5 處指向仍在建立的兩篇兄弟稿件，非預期缺檔 0 處。依本次任務邊界，兄弟篇導覽不列 blocker；這不是遠端發布驗證。

既有前半部 R10、舊 exit 5、CLI 措辭強度、R03／C pattern 例外與 B/C 表格修正均保留，沒有被全文潤稿改回。第五節的 A1／A5／SaltBench 已對照來源 audit，並重新讀既有原站內容快照的相關段落；沒有新抓網頁或發出模型請求。

## 判定範圍

本報告只判斷本篇證據與推論是否符合資料。修正 SPEC-E01 後須核對實際文字與新 hash，才能關閉唯一待修項。文稿尚需其他角度的 review、MCP 用語檢查與發布包驗證；不簽核其他三篇，不聲稱已發布。
