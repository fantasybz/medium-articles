# 可靠度與付款實作篇：發布前精修紀錄

日期：2026-10-24；2026-10-25 與 2026-10-26 的接手複核與 /ship 審查記在文末小節。範圍為《綠燈不是驗收》第三篇〈可靠度篇〉、第四篇〈付款實作篇〉的中英文原稿、貼稿與受影響圖表。

依作者要求，這輪從讀者做判斷的過程檢查兩篇後續文章：先交代具體情境，再引入概念，說明證據能回答什麼問題，最後接到授權、人力或核准決策。既有的[共用風格](../../STYLE.md)與[當月風格摘要](style_brief.md)持續適用。

## 可靠度篇：從量測結果走到決策

| 原本容易產生的疑問 | 本輪補充 | 證據與適用範圍 |
|---|---|---|
| 一份 PR 已通過，為什麼還要量測可靠度？ | 開頭接續 Review 篇，區分單次驗收與擴大委派範圍的判斷 | 通過個別 PR 的證據，與同類任務反覆執行的證據分開記錄 |
| 重跑是否可以接著上一次修好的狀態？ | 各次嘗試回到相同起點，不沿用前次修改、答案或對話 | 獨立嘗試的比較與實務上修正後重跑各有用途，統計時要分開 |
| pass^k 能否直接以整體 pass@1 的 k 次方代替？ | 分清實際量測的連續成功率、簡化機率示意與至少成功一次的 pass@k | 公式示意不能取代同一組任務反覆執行的量測 |
| 同一份 PR 重跑多次，分母怎麼算？ | 示範固定記錄每份 PR 首個通過功能檢查並送驗的候選版本；保留版本與結果，重跑另列 | 真實 PR 的固定樣本與 golden set 實驗分開；證據缺失也另列 |
| 整體約束通過率高，能否接受個別失敗？ | 以假設的 100 個候選版本中 93 個通過、7 個失敗說明分母 | 整體指標供風險判斷，個別 PR 仍須通過自己的必要約束 |
| Review 分流矩陣是否自帶可靠度目標 T？ | T 改為團隊為該類任務明確設定的數值；矩陣決定責任與審查深度 | 0.95 等數字是示範假設，不能從矩陣的格子直接讀出 |
| 抽查公式算出比例，就能安排人力嗎？ | 補上模型前提與樣本選擇的影響，再換算 100 份、抽查 75%、每份 20 分鐘為 25 小時 | 工作量加倍為 50 小時；這仍未包含其他審閱工作。若只抽查自動檢查通過者，須在該選取政策下重新估計 p、c |
| 30 個案例與信賴區間能否支持擴權？ | 說明 30 例僅作為起步清單，信賴區間不會消除樣本選擇偏差 | G2 仍限低影響、可驗證的工作，每份 PR 保留人工核准 |
| 月報數字齊全，還缺什麼？ | 逐項解讀示範月報、指出缺少的證據及負責補件的人；YAML 加入範圍、約束樣本與 `on_missing: hold` | 月報中的示範數字沒有改寫為作者實測的 production 成效 |

兩種語言各重繪 `diagram-01.png`、`diagram-02.png` 與 `table-02.png`。圖中標示約 93%／67%，保留其他授權條件；英文圖表調整換行，公式與比較條件能完整閱讀。兩篇各仍有七張圖，封面仍選 `diagram-02.png`。

## 付款實作篇：讓測試、審閱與合併證據接得起來

第五節程式摘錄補上呼叫 provider 前的 pending 紀錄，與[隨文實作](../../examples/tea_payment/payment.py)對齊。文字先解釋 `Receipt`、`Attempt`，再帶讀者看連線錯誤為何跳過第二次寫入與回傳，最後連到 M7 的檢查目的。

重送保護的條件統一為：依序呼叫**同一個 `Checkout` 實例，且該實例仍保有先前紀錄**。即使沒有重啟行程，重新建立實例也會失去這份記憶。這個界線已寫進程式摘錄前、審閱示例與第九節。明確拒絕付款後，也不能直接為同一訂單換一個 key；重新授權或換卡屬於示範之外的新流程。

第八節沿用 Review 篇的付款重送情境，補足以下判斷鏈：

1. PR 沒有新 commit，目標分支或佇列仍可能改變合併候選版本。
2. 分開記錄 PR head、base、候選 commit 與 tree；check run 的所屬 commit 還要對應實際取出執行測試的版本。
3. 核准紀錄保留驗證資產版本、必要檢查的來源／執行 ID／結果，以及核准者的範圍、理由與時間。
4. 候選版本改變後重新確認證據，再依差異與風險安排人工審閱；核對後到合併前也要防止版本被換掉。
5. merge、squash、rebase 可能產生不同 commit；保留候選內容與最終內容的對應及合併後核對結果。

這是核准政策的設計示例。程式沒有新增 approval service、merge queue 或真實付款 provider。本輪沒有修改可執行範例、測試或七個 mutant。

## 一手來源與查核界線

Git／GitHub 文件於本輪透過 gstack browse 重新查閱，原始文字快照留在 gitignored 的 `.context/reliability-payment-polish-2026-10-24/`。採用原則延續[合併候選版本與核准紀錄](review-approval-drift-evidence.md)：

- [Git Objects](https://git-scm.com/book/en/v2/Git-Internals-Git-Objects)與 [git-merge-tree](https://git-scm.com/docs/git-merge-tree)：區分檔案樹內容與 commit 的歷史／中繼資料。
- [Checks API](https://docs.github.com/en/rest/checks/runs#create-a-check-run)：check run 對應 commit，需保留識別碼、狀態與結果。
- [Merge queue](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/configuring-pull-request-merges/managing-a-merge-queue)與 [merge_group](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows#merge_group)：候選組合會包含最新 base 與前方 PR；必要的 Actions 檢查須涵蓋對應事件。
- [Protected branches](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches)：平台可接受 skipped／neutral；付款測試必須實際執行且成功，是本文建議的更嚴格政策。沒有把所有 base 或 queue 變動說成必然自動撤銷所有核准。
- [Merge methods](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/configuring-pull-request-merges/about-merge-methods-on-github)：最終 commit SHA 與候選 SHA 不一定相同。

可靠度篇的既有研究數字與研究限制保留。本輪著重原稿的定義、推論與讀者判斷過程，沒有重新執行論文實驗，也沒有重新查核所有外部引文。付款測試的設計與歷次修正仍見[付款實作研究紀錄](payment-example-evidence.md)。

## 審閱與本機驗證

Claude Code 審閱曾實際啟動，但回報 `Credit balance is too low`，沒有產生模型審閱結果。本輪另以新的唯讀 Codex CLI 工作階段完成技術與編輯審閱；編輯審閱指出同一 `Checkout` 實例及 T 的數值定義兩項問題，均已修正。最後一輪完整雙語審閱回覆 `NO_FINDINGS`。這些是同一提供者的獨立工作階段，不記成 Claude Code 或跨提供者審閱。

本機三套 `unittest` 通過：工具 301 項、研究腳本 121 項、付款與 mutation runner 21 項，合計 443 項。付款教學實驗另行重跑，同一組七個指定、非等價 mutant 的結果仍為：功能測試 2/7（28.6%）、移除逾時測試 6/7（85.7%）、完整約束測試 7/7（100%）。這些分數只描述這組測試對七種指定錯誤的辨識能力。

六張更新圖表逐張檢查文字、換行、尺寸與邊界；四份貼稿與圖表定義由原稿重新產生。測試紀錄與圖表檢查資料留在上述本機證據目錄。

## Medium 排程稿讀回

四份既有排程稿已更新。等待儲存後以新分頁讀回全文、連結、圖片與發布設定；全部仍為 `isPublished: false`。

| 排程稿 | Post ID | 發布時間（Asia/Taipei） | 文字區塊 | 連結 | 圖片 | 分隔線 |
|---|---|---|---:|---:|---:|---:|
| 可靠度篇（中） | `3c64a9622777` | 2026-10-27 09:00 | 169 | 22 | 7 | 10 |
| 可靠度篇（英） | `4b6d147bff0d` | 2026-10-29 09:00 | 169 | 23 | 7 | 10 |
| 付款實作篇（中） | `46377fd460fe` | 2026-11-03 09:00 | 157 | 32 | 7 | 11 |
| 付款實作篇（英） | `20452944263b` | 2026-11-05 09:00 | 157 | 33 | 7 | 11 |

付款篇七張原圖保留；可靠度篇每種語言替換三張更新圖表，封面仍選新版 `diagram-02.png`。正文標題、Topics、預覽標題與摘要、通知設定及原排程均保留。可靠度兩份稿件仍各有零個付款程式碼連結，付款篇各保留兩個；回填總論與前三篇仍以同語言第四篇實際公開為準。

初次新分頁讀回付款稿時，曾暫時缺少文末區塊；等待後再次唯讀核對即取得完整版本，沒有重新貼稿或把部分儲存當成完成。最終數字來自通過全文核對的讀回紀錄。逐篇證據另記於各語言發布包的 `PUBLISHED.md`，全系列時程見 [PUBLISHING.md](../../PUBLISHING.md)。

## 2026-10-25 接手複核（Claude Code）

接手 10/24 的精修結果後，由 Claude Code 通讀兩篇中文原稿，並把跨篇引用逐條對回已發布的總論、測試篇、Review 篇、Agentic Engineering 營運篇與組織篇；付款篇的程式摘錄、測試名稱、JSON 鍵名與 M1–M7 失敗矩陣，則對照 `examples/tea_payment/` 與 `mutation_demo.py` 的實際輸出。另派兩個獨立 agent 分別通讀兩篇的中英文稿，結果見下方小節。

### 可靠度篇：三處修正，中英同步

| 位置 | 原稿問題 | 修正與依據 |
|---|---|---|
| 第三節 Thinkingbox 段 | 「這裡是全系列唯一引全數字的地方」 | 總論第八節已引用 READY（臨床稽核工作流，非 code）的 72.8%／72.5%／76%／39.2%／29.6%，這句話不成立；刪去該子句，只保留「旁證來自 code 以外」 |
| 第三節月報三欄段 | 「開場提到的 oversight budget」 | TL;DR 與第一節只描述「人還需要複核多少」，沒有出現這個名稱；改為在此處首次命名（引用 TL;DR 原句），第四節仍是完整定義 |
| 第五節 G2 原條件 | 「escape rate 持平、champions 體系自轉」，並解釋為「不靠中央團隊持續推動，也能自行運作」 | 已發布的營運篇 G2 寫的是「escape rate 未惡化；champions 有工時與支援」；組織篇把 champions 設計為每 team 一位、20% 工時、有 sponsor 協調資源的角色，總論第八節也寫成「champions 是否能承接工作」。改回營運篇用語，連同 `agent-policy.yaml` 的指標名、第五節示範月報的第二個判斷，以及 diagram-04 的兩個節點文字 |

三處都只改句內文字，行數不變；英文版依相同文意修正。中英 `medium-paste.md` 與 `figures.json` 由原稿重新產生。

### 核對無誤的項目

- 跨篇引用：總論第二節三類證據（a／b／c）、總論第八節 READY 全數字、測試篇 Check 2 與 86 位開發者的 49%／74%、測試篇 70% 起始建議、Review 篇第三節（arXiv 2607.13091）與第七節（合併候選版本）、Review 篇「高 radius 由指派者以外的人核准」、營運篇第二節三個 judge 陷阱、營運篇 golden set 20–50、G3 為最後一道 gate。
- 算術：221／644 ≈ 34%；(100%+80%+100%)／3 ≈ 93%、2／3 ≈ 67%；20 個 case 粒度 5 個百分點；三個 r 算例 1.25／0.8333／0.3333；示範月報 r_min 0.740741、r 0.75；75 份 × 20 分鐘 = 25 小時；Thinkingbox 66.50% − 47.53% ≈ 19 個百分點。
- 付款篇：三段測試摘錄與第五節 `Checkout.pay()` 摘錄逐字等於 `test_payment.py`／`payment.py`；逾時摘錄已註明完整程式改用 `subTest`；`FakeGateway` 的 `error_after_capture` 確實拋出 `ConnectionError`；`mutation_demo.py` 的 JSON 鍵名（`baseline_passed`、`baseline_tests`、`scored_mutants`、`excluded_mutants`、`failing_tests`、`mutation_score`）與三組名稱（`functional`、`without-timeout`、`full`）與第九節一致；第七節失敗對照表九列七欄逐格等於 `full` 組的 `failing_tests`（M1 由八個方法辨識、收據測試不辨識；M2 由六個方法辨識，key 不移到另一訂單不辨識）；空 `pass` 反例的推論與矩陣相符；`-p test_payment.py` 執行得到 9 個測試，整個目錄 21 個。
- 中文版尚未附英文版連結，是 PUBLISHING.md 既有流程（英文版上線後才在中文版文末補一行），不是缺漏。

### 驗證

三套 `unittest` 通過：工具 301、研究腳本 121、付款與 runner 21。`mutation_demo.py` 重跑仍為 28.6%／85.7%／100.0%。修改的中文句子以 zh-tw 檢查（markdown、lexical_safe、technical），僅建議「導入→匯入」，屬已知誤判，未採用。


### 獨立審閱結果與第二輪修正（2026-10-25）

兩個 agent 各自通讀一篇的中英文全文（可靠度篇 615／617 行、付款篇 501／504 行均全讀），分別回報 10 項發現，沒有 high 等級；數字、算式、跨篇章節號與付款範例邊界的一致性均核對無誤。採用與未採用如下。

**可靠度篇（中英同步）**

- 第五節 G2 三個詞的註解：營運篇把 retry rate 定義為「需要重試的任務比例」，escape rate 定義為「交付後才發現缺陷的變更占同批交付變更的比例」；原稿寫成「agent 失敗後重試的比例」「漏到 production 才被發現的缺陷比例」，分母對不上，已改用營運篇的分母。總論第八節的「缺陷比例」寫法已發布，本輪不動。
- 同段「sponsor 或平台團隊可以求助」是第一輪新寫的句子，容易被讀成營運篇的定義；改成泛稱「找得到人支援」。
- 英文：「221 violated one of those constraints」改為「at least one」；「independent evidence Rebuild Dossier warned about」改為「called for」，它警告的是不獨立的證據；「category （c）」統一為本篇其他處的「third class」；第五節「check that it applies」的 it 沒有先行詞，改為 they；結語「consistency across repeated tasks」改為「repeated attempts on the task set」，對齊中文「這組任務重複執行」。
- 未採用：「違規率降到 2% 不該要求繼續下降」被指為反駁不存在的要求；這句說明的是門檻為何寫成「不再上升」而非「持續下降」，與表格、YAML 一致，保留。「這就是複利的意思」在冒號後即給出定義，保留。

**付款實作篇（中英同步）**

- 第三節五則示範評論沒有任何一則提到拒絕，表格卻把「拒絕或逾時是否被當成成功」拆成 C3、C4，C3 因此沒有評論來源。第三則評論改為「明確拒絕與逾時，都不能被寫成付款成功；而且逾時之前，金流端可能已經扣款」；`examples/tea_payment/rules.md` 的評論清單同步補上 C3 一條。
- 第六節開頭「第三種『挑選』」沒有交代前兩種；補一句指回第二節（誰審閱、先讀哪裡）與第三節（哪些意見變成測試）。
- 第八節 merge queue 只有連結沒有說明，merge group 卻先在審閱紀錄範本出現；在連結處補一句佇列如何組成候選組合。「符合分流要求的人」補為「Review 篇風險分流」，英文 routing policy 改為 triage，與 Review 篇英文版一致。
- TL;DR「確認測試抓錯能力的方法」改為「一種方法」；測試篇另有 assertion-change diff 與 red-then-green，英文原本就是 a way。
- 英文：補回中文第二節「這個 PR 還缺少足夠的可機器驗證證據」一句；「rule record(s)」統一為 rule card；結語「testing／review／reliability part」統一為 Testing／Review／Reliability article；第五節 runner 段的 it 改為 that label，指 survived 標籤而不是 runner；「follow capture followed by」改寫為時間順序的走法；「in Section 7」句中大寫改小寫。
- 未採用：中文版文末尚無英文版連結，是 PUBLISHING.md 既定流程（英文上線後補），不是缺漏。

**（c）的全形括號是刻意的。** `article_to_paste.py` 會拒絕英文散文中的半形 (c)，因為 Medium 會自動改成 ©；第一次改成半形後貼稿產生失敗、研究測試亮紅，已改回全形。這條規則只出現在腳本訊息裡，審閱 agent 與人都容易誤判為排版錯誤。

### 最終驗證與待辦

三套測試再次通過：301／121／21。四份貼稿與可靠度篇兩份 `figures.json` 由原稿重新產生；新寫的中文句子以 zh-tw 檢查，仍只有「導入→匯入」這個已知誤判。本輪沒有改動付款範例的程式、測試與七個 mutant，只補了 `rules.md` 的一條評論對照。

2026-10-26 完成：作者允許重開 gstack browse daemon 後，先以 `render_images.sh` 重繪可靠度篇中英兩包（七張全過 MERMAID.md 檢查，`diagram-04` 長寬比 1.40／1.44），再依 PUBLISHING.md 的順序以 `--post` 重灌四份排程稿並逐塊讀回（169／22、169／23、157／32、157／33 個文字區塊與連結，各 7 張圖），封面以編輯器選單選回原圖並讀回確認，排程、標題、預覽摘要、Topics 與通知設定均未改變。各篇 ledger 記有新舊圖片識別碼；重灌前後快照在本機 `.context/ship-2026-10-26b/`。

2026-10-26 第二次重灌：第三次 /ship 審查的 Red Team 從 PNG 檔頭看出，上午重繪的可靠度篇四張圖都只有 664 px 寬。原因在 `mermaid_check.sh`：拿掉 mermaid 的 `max-width` 之後，`width="100%"` 的 svg 在 inline-block 容器裡退回瀏覽器預設的 300 CSS px，截圖只有 viewBox 一半的解析度，而 viewBox 的尺寸檢查照樣 PASS；10/24 以別的方法算繪的 `diagram-01`、`diagram-02` 原是完整尺寸，上午的重灌把封面從 1468×1136 換成了 664×528。以 merge-base 的 PNG 檔頭、`.context/render/` 裡 svg 的屬性，以及一次對照實驗（拿掉修正，守門立刻 FAIL）確認後修正腳本：截圖前把 svg 設成 viewBox 的寬高，並核對 `#wrap` 與 PNG 的寬度和 2x 倍率；`_common.sh` 另在 daemon 屬於別的 session 時以 75 退出，`render_images.sh` 在清舊圖之前先做這個檢查（上午第一次重繪就是這樣把七張圖刪光再全部 FAIL 的）；五個 fake-browse 測試固定這些行為。兩篇四包全部重繪（可靠度篇四張圖中文 1076／1468／1456／1300、英文 1266／1486／1596／1374 px 寬；付款篇 `diagram-01` 中文 1224×792、英文 1402×792；十五張表位元組不變），四份排程稿於 11:46–11:58 再重灌一次並逐塊讀回，數目與上午相同，封面選回各篇原圖，排程與設定未變；各篇 ledger 新增「第二次重灌」小節並記下貼稿的 SHA-256。Red Team 另兩項建議（runbook 不該把縮小的尺寸寫成預期結果；ledger 應記貼稿摘要）已分別改寫與補記，摘要與 committed 貼稿的對照測試列為後續。

### /ship 審查（2026-10-25、2026-10-26）

gstack pre-landing review 派出 testing、maintainability、security、performance、simplification 五個 specialist 與 Red Team，另以五項功能性探測確認貼稿重產冪等、全形括號守門、`figures.json` 與文章一致、mutation demo 分數與 corpus 測試，全部通過。採納的修正：PUBLISHING.md 的 2026-10-25 小節移到最新優先的位置，補上重灌範圍、識別碼變動與時程底線；英文可靠度篇第五節的 routing policy 改為 triage policy；兩種語言結語的 champions 用語對齊「有工時與支援」；四份 ledger 補註排程稿尚未重灌。未採納、留作後續建議：讓 `render_images.sh` 寫出每張圖來源的 SHA-256 側檔並加測試，使過期的 PNG 能在離線測試中被發現；讓 `medium_draft.sh` 取鎖並在 `--post` 前讀取 publishAt。2026-10-26 第二次 /ship 審查再補兩處：可靠度篇第五節引用營運篇 G2 的第一條時，寫明 15% 是營運篇的討論起點並要求重試原因可追查（中英同步）；runbook 補上重灌後四份稿件的封面都會重設成第一張表、要選回原封面。`research/2026-10/2026-12-sre-for-agents.md` 裡沿用舊 G2 條件的一行也已更正。同日 Step 11 的 Claude 對抗式審查指出 runbook 對識別碼的說法不準；10/26 重灌實測後改寫為：`--post` 會重傳全部七張圖，但 Medium 以內容定址，位元組不變的圖保留識別碼、變了的才換新，並補上重繪 FAIL 時先還原舊圖的步驟；Codex 的 adversarial 與結構化審查都完成且無發現，但輸出缺少標記而被判 unverified，第二次嘗試撞到用量上限（2026-11-01 之後恢復）。另外，`research/2026-09/` 的九月大綱與 figures 檔仍寫著舊的「escape rate 持平、champions 體系自轉」，那些是凍結的規劃文件，本輪不改；之後的十一月稿件引用 G2 時，以營運篇第五節的現行用語為準。

2026-10-26 第三次 /ship 審查（合併 origin/main 之後）：specialist 指出 runbook 的 `diagram-04` 長寬比仍寫 1.45（重繪後是 1.40／1.44）、兩篇可靠度篇 ledger 設定表的封面列仍是 10/24 的識別碼，皆已更正；Red Team 的解析度發現與處理見上一節。

第二輪審查（10/26 晚間重派，中間撞到兩次 session 額度，10/27 01:00 後完成）：testing、maintainability、simplification 三個 specialist 各自重現同一個問題：`_common.sh` 的 pre-flight 以 `status=$(browse status 2>/dev/null) || status=""` 讀狀態，但 browse 把「started by another session」寫在 stderr 並以 1 退出、stdout 是空的，所以第一輪加的守門對真實的 browse 永遠不會觸發；測試之所以是綠的，是 fake 把訊息印在 stdout。已改為收兩個串流（`2>&1 || true`）；fake 改成模仿真實通道（stderr、exit 1）之後，拿掉修正三個測試就亮紅；並以真實的 browse 驗證（從另一個行程開 headed daemon，再以無旗標的 `browse status` 讀：stdout 空、stderr 帶拒絕、exit 1；修正後的 pre-flight 以 75 退出）。同輪另補 `mermaid_check.sh` 的 foreign-daemon 測試與空檔／非 PNG 截圖測試、命名兩個容差常數、缺 `#wrap` 量測時給獨立訊息、刪掉 `render_images.sh` 表格段多餘的 pre-flight、擴充 `EX_TEMPFAIL` 的註解，並在 CLAUDE.md 記下這個 capture 形式的陷阱。security specialist 兩次都被額度切斷，第三輪重派。
