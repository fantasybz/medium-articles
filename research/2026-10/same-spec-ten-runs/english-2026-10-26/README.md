# 2026-10-26／27 英文版主寫、審稿與發布紀錄

「同一份規格，跑十次」四篇中文已於 2026-10-04 排程（11/10、11/17、11/24、12/01，臺北 09:00）。本輪補齊四篇英文版：主稿、逐段潤飾、第二模型三輪審稿、發布包與 Medium 排程。中文正文、貼稿與正式實驗封存沒有改動。

## 進度

| 篇目 | 英文稿 | 讀者審查 | Codex 審稿 | Medium 英文 Post ID | 英文排程（臺北） |
|---|---|---|---|---|---|
| 總論 | 完成 | 完成（Claude） | r1、r2、r3 | `3700b5d771fd` | 2026-11-12（四）09:00，已讀回 |
| 規格篇 | 完成 | 完成（Claude） | r1、r2、r3 | `3c356327ea3c` | 2026-11-19（四）09:00，已讀回 |
| 契約篇 | 完成 | 完成（Claude） | r1、r2、r3 | `97d5d4dc4fa8` | 2026-11-26（四）09:00，已讀回 |
| 變異篇 | 完成 | 完成（Claude） | r1、r2、r3 | `3745c88d2c66` | 2026-12-03（四）09:00，已讀回 |

中文四篇維持 10/04 的排程（11/10、11/17、11/24、12/01）。每篇英文草稿寫入後一次、重新載入後一次逐塊比對：總論 175 段／49 連結／7 圖，規格篇 194／64／8，契約篇 226／56／7，變異篇 200／59／7；分隔線 0、無 placeholder。四篇的排程、Topics、封面、預覽標題與摘要、通知設定都從新分頁讀回，紀錄在各篇 `publish/en/PUBLISHED.md`，操作細節與實測到的三個 Medium 行為在 [PUBLISHING.md](../../../../PUBLISHING.md)〈2026-10-27〉。

## 主稿怎麼產生

- 主寫由 Claude Code 2.1.310 這個 session 派出的四個子代理完成，每篇一個，effort `max`，沒有指定其他模型，因此沿用本 session 的模型 `claude-fable-5-1`；主稿以 Write／Bash 分段寫入 `article.en.md`，不受單次回覆長度限制。四個代理於 2026-10-26 12:29Z 同時啟動；規格篇與變異篇的代理曾撞到 session 額度（臺北 10/27 01:00 重置），重置後以同一個代理接續，沒有改由其他模型代寫。
- 四篇共用一份書面簡報 `.context/same-spec-en-2026-10-26/brief.md`（SHA-256 `3a014b7b2fd1e76931f082909892135cc40f410fd924be32a3f34341bb1826f7`）：中文稿為唯一依據；先讀 STYLE.md、當月 style brief、已核可的英文版（綠燈付款篇、AAIF 第三篇）；引用凍結 spec 時必須用原始英文，不得把中文節譯回譯；研究事實清單（40/40 不排序、69.15%–100% 的 i.i.d. 條件、180 配對非獨立、P／Q 與 288 名額未執行、教學重播不計入樣本、high 與 max effort 分屬不同流程等）；連結對應表（前系列連結改指英文版，本系列中文 Post ID 先保留，由 root editor 在草稿建立後置換）；術語表。
- 主稿原稿快照保留在 `.context/same-spec-en-2026-10-26/<piece>-writer-draft.md`（gitignore），每一輪修訂後另存 `-after-rN.md`，方便對照哪一句是審稿改的。

## 機械檢查

`.context/same-spec-en-2026-10-26/mirror_check.py <dir>` 比對中英兩版的 H2／H3 數、表格數、程式區塊數、Mermaid 數、連結數與連結目的地多重集合（套用前系列的中→英對應表後必須完全相同；英文版另多兩條指向自己中文版的連結）、「即將發布」與 `(coming soon)` 數、References 條數，並列出英文散文中殘留的中文字（行內程式碼與署名除外）。四篇在每一輪修訂後都是 CLEAN。

## 審稿

- **Claude 獨立讀者審查**：每篇一個全新的子代理（effort xhigh），以三個視角審：英文讀者的理解路徑（概念是否先有例子再有名詞、段落交接、判斷步驟是否齊全）、逐段忠實度（引中文與英文原句並給修正）、英文品質與術語一致。審查代理只讀不改；意見由 root editor 逐條裁決後套用。
- **Codex 第二模型審稿**：`.context/same-spec-en-2026-10-26/codex_review_en.sh <dir>`（gpt-6.1-sol、reasoning xhigh、read-only sandbox），每篇三輪：審→改→再審。原話照錄在本目錄 `codex-review-<dir>-rN.md`。Codex 對照的是中文定稿與凍結研究材料（RESULTS.md、SPECS.md、PROTOCOL.md、四份 spec、requirements.json、workbench 紀錄）。
- **裁決原則**：中文是唯一依據；英文不新增主張。兩位審稿都指出英文版加入了中文沒有的直接引文（Lamport 原句），最後改回與中文同樣的轉述，只保留中文本來就引用的 spec 原文；凍結 spec 的句子在英文版一律用原文，並標明是引用。審稿指出但屬於中文原稿本身的問題（例如 R03 的 `turn.failed` 例外、`if text:` 反例在 `formal-02-A0` 實際程式中的精確形式），英文版以不改變中文主張的方式補上精確措辭，並在此記錄；中文稿未改。
- **不採納的建議**：改英文篇名（已進入排程計畫與四篇系列區塊，且「Instruction」對未讀正文的讀者較易懂）；刪除英文版替 yardstick、slot、arm、EM 補的一句定義（STYLE.md 要求每篇可獨立閱讀，名詞首次出現要就地說明）；把章節標題改寫成與中文不同的句式。

## 術語決定（四篇一致）

交代 → brief；候選 → candidate；產物 → artifact（不用 product，與 stdout 的 output 區分）；量尺 → yardstick，每篇首次出現時說明「oracle 與 grader 合起來」；正反對照 → positive and negative controls；stdout／stderr／exit code → the three channels，沙盒的通道 → route；名額 → slot（generation slot），自查範本的位置 → checklist position；一次生成 → single-shot generation；合格交付 → qualifying delivery；修改卡 → spec change card；義務表 → obligation table；比較卡 → comparison card；代理 review → review by an AI agent；保護力 → ability to detect faults；模式語言驅動開發工作坊 → the pattern-language-driven development workshop（沿用十月英文版）。

## 連結

- 前系列《綠燈不是驗收》改指英文版：`582f24223eea→c4fc9f3d8581`、`b01055139451→51d001a6dcd5`、`ccbf0cbe2691→4d36d0f2f9c1`、`3c64a9622777→4b6d147bff0d`、`46377fd460fe→20452944263b`；Harness 藍圖改指英文版 `3facc281f633`。
- 本系列各篇：英文草稿建立後，依「只預填本篇發布時應已上線的篇」的既定規則，把後建立的英文篇連到先前篇的英文 Post ID，尚未上線的後篇保留 `(coming soon)`；每篇系列行與署名都連回自己的中文版。
- 研究附件維持固定 commit `774759192ab0e0b2da3d8b163eb3f07f3d12f4c3`。

## 圖表

英文發布包以 `research/scripts/article_to_paste.py <dir> --lang en` 與 `research/scripts/render_images.sh <dir> en` 產生。本輪發現 `mermaid_check.sh` 把 svg 截在瀏覽器預設 300 CSS px（每張流程圖只有 664 px 寬），這是 `fantasybz/ship` 分支 10/26 已修的問題（commit `ba772b7`：截圖前把 svg 設成 viewBox 寬高並核對 PNG 寬度），已 cherry-pick 進本分支；研究腳本測試 126 項通過。重繪後總論流程圖 1586×2246、契約篇 1400×990（2x），表格一律 1800 px 寬。四篇中文排程稿的流程圖仍是舊版 664 px 截圖，是否重灌另行決定。

## 驗證

- `python3 tools/test_tools.py` 331 項、`python3 -m unittest research/scripts/test_research_scripts.py` 126 項（含 Mermaid 修正的新測試，以及四份英文貼稿與 `figures.json` 是 `convert()` 結果的語料檢查）、`python3 -B -m unittest discover -s examples/tea_payment` 21 項，全部通過；lockstep 掃描確認四篇 `article.en.md` 與 `publish/en/medium-paste.md` 的連結清單與 `(coming soon)` 數一致。
- 鏡像檢查四篇 CLEAN（最終版本）；術語掃描四篇一致。
- 英文圖表：總論流程圖 1586×2246、契約篇 1400×1038（viewBox 760×1086、668×483，2x），表格 1800 px 寬，全部 PASS；目視檢查流程圖與較大的表格，英文標籤沒有裁切。
- Medium：四篇皆 `isPublished: false`，`publishAt` 分別對應 `2026-11-12T01:00:00Z`、`2026-11-19T01:00:00Z`、`2026-11-26T01:00:00Z`、`2026-12-03T01:00:00Z`；封面識別碼與尺寸、五個 Topics、通知、摘要與預覽標題均與計畫相符。Stories 的 Scheduled 日曆本輪只看了十月頁，十一、十二月的條目以各篇提交頁的讀回為準。
- 尚未做：中文四篇上線後回填英文版連結與後篇連結；中文排程稿的 664 px 流程圖是否重灌，另行決定；下一輪 P／Q 比較與人工資料仍是後續研究。
