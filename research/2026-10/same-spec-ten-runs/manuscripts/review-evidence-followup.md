# 變異篇證據複核

審查時間：2026-09-25T06:00:38.719376+00:00。

**判定：變異篇證據核對完成，無待修問題；系列仍未完成審查。** 六項初審問題均已解決，未發現新增的實質證據問題；目前 open blocker／major／minor 皆為 0。

完整閱讀 ce383be2 版本第 1–262 行，再核對兩段時態差異及還原 hash，最終判定涵蓋 1cf47ca4 版本。只審查變異篇，其他三篇仍待完整正文。未修改正文、封存資料或初審報告。

正文：[article.md](</Users/kochi.chuang/conductor/workspaces/medium-articles/surabaya-v1/2026-11-same-spec-variance/article.md:1>)；40,265 bytes、262 行。最終 SHA-256：`1cf47ca478afca22ff028c285c4d0550a844e4794886b7e345fa122a27cac800`。

已全文審閱版本 SHA-256：`ce383be20445328cec4a509e8ce7f519b94e9fe99b2fd927e494ffc4661c3587`。最後兩處改寫見 [時態修正紀錄](</Users/kochi.chuang/conductor/workspaces/medium-articles/surabaya-v1/research/2026-10/same-spec-ten-runs/manuscripts/final-sibling-status-fix.json>)；反向套用紀錄可精確還原前版 hash，沒有額外數值或證據變動。

初審保留於 [review-evidence.md](</Users/kochi.chuang/conductor/workspaces/medium-articles/surabaya-v1/research/2026-10/same-spec-ten-runs/manuscripts/review-evidence.md>) 與 [review-evidence.json](</Users/kochi.chuang/conductor/workspaces/medium-articles/surabaya-v1/research/2026-10/same-spec-ten-runs/manuscripts/review-evidence.json>)。兩檔的內容與 hash 均未改動。

## 初審問題的處理

| 問題 | 原程度 | 新稿行號 | 判定與證據 |
|---|---|---|---|
| EV-001 | major | 122 | 已解決。只說節點種類的數量比例仍接近；明說未量出原始程式碼或樹狀結構保留多少，也未估計或扣除共用起點的影響。 |
| EV-002 | major | 199、201 | 已解決。區分觀察到的 score 增加與文件效果；明說 A3 與本輪量尺不同，不能搬用 4.9 個百分點，且本輪沒有相應檢定力分析。 |
| EV-003 | minor | 120 | 已解決。限定為 180 個已計算的組內 pair，明確排除跨組配對；極值 0.9831 與 0.9783 正確。 |
| EV-004 | minor | 49、51、61 | 已解決。表格改為名額與結果欄位，CLI 與產物各有判定條件；保留 CLI 未完成但產物驗收合格的情形，不再描述為逐層必要前提。 |
| EV-005 | minor | 126 | 已解決。改成檔案數不能區分本輪候選，因此選用 AST 描述檔內差異，未宣稱 AST 是唯一能觀察差異的方法。 |
| EV-006 | minor | 262 | 已解決。頁尾改為作者與 Medium profile，已移除本篇發表於 Medium 的既成狀態。 |

## 新增與改寫內容的核對

| 編號 | 新稿行號 | 核對結果 |
|---|---|---|
| F01 | 63、65 | **CI 解讀：**雙側 95% Clopper–Pearson 區間仍為 69.15%–100%，以反覆抽樣的涵蓋率說明；沒有把下界當成下一輪保證，也未主張等效。 |
| F02 | 81、83、85、87、89 | **驗收盲點與零失敗：**兩個例子只指出至少能辨別哪些錯法，沒有排除其他盲點。103 項的有限覆蓋、每候選分母與多種可能原因均保留。 |
| F03 | 126、246 | **A2 版本與 42 分 rubric：**使用 Achint Mehta 的版本化 v2 PDF 題名。Table 9 的六次 42 分明確解釋成 14 criteria 首次檢查便全數合格；整體研究允許修正提示的規則，未套成這六次需要修復。 |
| F04 | 128 | **教學示例的選取：**選取紀錄與 frozen schedule 一致：A0 block 01、02。正文標為成稿階段的事後說明示例，不列入原分析計畫，也不宣稱代表其他候選。 |
| F05 | 130、132、139、141、150 | **教學程式節錄與結構描述：**兩個 Python code block 逐字存在於對應 candidate。第一份 main() 的區域變數與 malformed 字典、第二份 _State 及各個事件處理函式，均與原檔相符；沒有推論維護優劣。 |
| F06 | 150 | **教學 pair 的數值與驗收：**兩份 candidate hash 與 ledger、summary、evaluation 一致；各有 103 項驗收合格，normalized AST hash 不同。獨立重算 cosine 為 0.9939804370606344，正文 0.99398 的捨入正確。 |
| F07 | 152、238、240、241、242、243、244、245、252 | **附件連結與公開狀態：**正文 14 個本機相對連結均存在。兩處明說尚未遠端發布，且公開發文仍須補上版本固定、可存取的入口。這是本機證據核對，未冒充附件已公開。 |
| F08 | 11、95、251、252 | **新增舊文承接：**組織篇回扣對應舊文第 233 行，URL 與已發布紀錄吻合。green 可靠度篇回扣對應第 529 行，使用 repo 稿件並標示尚待發布，未把排程當成發布。 |
| F09 | 34、35、36、37、38、39、53、54、55、56、57、111、112、113、114、166、167、168、169、171、175、179 | **正式數字與表格：**固定版本、40 名額、各組 10/10、103 項、AST 與資源表，均與第一輪已重算的 ledger／summary 相符。新增示例未改分母或擴增生成樣本。 |
| F10 | 177、183、219 | **成本解讀：**描述本輪 A0 合計最低，同時區分可觀察的費用差額與跨任務效果；未把牌價估計寫成帳單、ROI、品質提升或維護成本。 |
| F11 | 173、197、199、201、203、247、248、249 | **其他論文：**A1 的 ×1.34 成本 geometric SD、A3 的 20／26／23 與 composite 約 4.9pp、A5 的 24 tasks／18 variants／4,644 runs 均正確；版本 URL 沒有混用。 |
| F12 | 205、258 | **研究／寫作與真人狀態：**generation high、主寫 max、研究審查 xhigh 分開；補充 Codex 也參與，但仍無真人理解、維護成本、盲審或外部重現資料。 |
| F13 | 17、221 | **最後兩段時態修正：**規格篇與契約篇改為仍在成稿中，與已完成研究分開；結語改回本篇開頭，不再斷言未完成總論的內容。反向套用兩個 replacements 後，SHA 精確回到已全文審閱的 ce383be2 版本，證明這次僅有這兩處變動。 |

## 教學示例的精確證據

選取紀錄：[.context/same-spec-ten-runs/manuscripts/teaching-example-selection.json](</Users/kochi.chuang/conductor/workspaces/medium-articles/surabaya-v1/.context/same-spec-ten-runs/manuscripts/teaching-example-selection.json>)，時間為 `2026-09-25T05:41:52.542094+00:00`。依規則回到凍結 schedule，最前面的 A0 區塊確實是 01、02。這是成稿時增補的教學對照，沒有追認為執行前的分析計畫。

| 名額 | 原始節錄 | candidate SHA-256 | normalized AST SHA-256 | 驗收 |
|---|---|---|---|---|
| `formal-01-A0` | [原檔](</Users/kochi.chuang/conductor/workspaces/medium-articles/surabaya-v1/research/experiments/same-spec-ten-runs/results/formal-2026-09-25/formal-01-A0/candidate/codex_jsonl.py:73>) 第 73–76 行 | `7cc9bf5a24969310f18a50aad43ac26d4a59066321b2256ec03806da076dd2b2` | `dd9079c5cbee025c08b062f5523227d75eb87b5fcc2f8b49ad34ec053628d91d` | 103／103 |
| `formal-02-A0` | [原檔](</Users/kochi.chuang/conductor/workspaces/medium-articles/surabaya-v1/research/experiments/same-spec-ten-runs/results/formal-2026-09-25/formal-02-A0/candidate/codex_jsonl.py:26>) 第 26–31 行 | `f2a65e9e26aaa195ab1c0b8caf2c1920cb4e3d2ee3ad2abf30d1620a78008a57` | `1301aa94cf4b67a4c8e8aa6b9e1aa72295922c23cd203992934c9108ed504c42` | 103／103 |

第一份的事件分支位於 `main()`；第二份的 `_handle_line()` 位於原檔第 152 行，第 176–184 行分別呼叫 `_handle_item()`、`_handle_turn_completed()` 與 `_handle_turn_failed()`。這些是原檔可直接確認的組織差異，沒有靠高 cosine 推算而得。

直接以 `ast.parse` 建立兩份原檔的節點種類計數，再計算 cosine，得到 **0.9939804370606344**；與既有封存 pair 相同。正文顯示 **0.99398**，捨入正確。兩段 code block 也逐字存在於原檔。這次只解析原始程式碼，沒有執行候選。

## 狀態與判定範圍

本文的 14 個本機相對連結均存在。第 152、238 行明說資料尚未遠端公開。本輪只確認 repo 內的證據，沒有確認附件或文章已經發布。公開發文時，仍需完成稿中承諾的固定版本附件入口。

總論、規格篇、契約篇維持 **PENDING／NOT_REVIEWED**。本判定沒有替這三篇背書，也沒有把 AI 審查寫成真人審稿或外部重現。

本輪沿用已核對的論文版本與 Medium 發布紀錄；未重試 Cloudflare，未讀取主寫 raw response 的思考內容，未重新生成任何樣本。

## 來源版本

| 來源 | SHA-256 |
|---|---|
| [.context/same-spec-ten-runs/manuscripts/teaching-example-selection.json](</Users/kochi.chuang/conductor/workspaces/medium-articles/surabaya-v1/.context/same-spec-ten-runs/manuscripts/teaching-example-selection.json>) | `eeb3862f3715800aa159de5c8765d3e5751a1a8103dc8476497cc1e5ceb6d920` |
| [research/2026-10/same-spec-ten-runs/manuscripts/final-sibling-status-fix.json](</Users/kochi.chuang/conductor/workspaces/medium-articles/surabaya-v1/research/2026-10/same-spec-ten-runs/manuscripts/final-sibling-status-fix.json>) | `7ffee95b08341abc6467b0a3ed737376fdc9b2c7da625290791f22cbd512b095` |
| [research/experiments/same-spec-ten-runs/results/formal-2026-09-25/manifest.json](</Users/kochi.chuang/conductor/workspaces/medium-articles/surabaya-v1/research/experiments/same-spec-ten-runs/results/formal-2026-09-25/manifest.json>) | `ba30398118ecde62b2f682884c1e882b2864c22d70faf99549ceab0d7c0a55f2` |
| [research/experiments/same-spec-ten-runs/results/formal-2026-09-25/records.jsonl](</Users/kochi.chuang/conductor/workspaces/medium-articles/surabaya-v1/research/experiments/same-spec-ten-runs/results/formal-2026-09-25/records.jsonl>) | `2be5ed458de2e2defa2ab4f24d88f25bdd3b7340c9207915ab6aa0988c0db7f0` |
| [research/experiments/same-spec-ten-runs/results/formal-2026-09-25/summary.json](</Users/kochi.chuang/conductor/workspaces/medium-articles/surabaya-v1/research/experiments/same-spec-ten-runs/results/formal-2026-09-25/summary.json>) | `8198a4478b8158268298960576655d920db3b8d2dc2bd207348dcef8a346dfb9` |
| [.context/same-spec-ten-runs/sources/2607.02436v2.pdf](</Users/kochi.chuang/conductor/workspaces/medium-articles/surabaya-v1/.context/same-spec-ten-runs/sources/2607.02436v2.pdf>) | `4c80ac39360e3141df3b6b000823d2b07e92b1e79702a03b24bb35c393fe874d` |
| [2026-11-same-spec-variance/figures/F2.png](</Users/kochi.chuang/conductor/workspaces/medium-articles/surabaya-v1/2026-11-same-spec-variance/figures/F2.png>) | `474f4ae875dcababaf7ffcddf501b2b7c49fa5d9ed0e80a4ac9a57a98f9084fb` |
| [research/experiments/same-spec-ten-runs/results/formal-2026-09-25/formal-01-A0/candidate/codex_jsonl.py](</Users/kochi.chuang/conductor/workspaces/medium-articles/surabaya-v1/research/experiments/same-spec-ten-runs/results/formal-2026-09-25/formal-01-A0/candidate/codex_jsonl.py>) | `7cc9bf5a24969310f18a50aad43ac26d4a59066321b2256ec03806da076dd2b2` |
| [research/experiments/same-spec-ten-runs/results/formal-2026-09-25/formal-02-A0/candidate/codex_jsonl.py](</Users/kochi.chuang/conductor/workspaces/medium-articles/surabaya-v1/research/experiments/same-spec-ten-runs/results/formal-2026-09-25/formal-02-A0/candidate/codex_jsonl.py>) | `f2a65e9e26aaa195ab1c0b8caf2c1920cb4e3d2ee3ad2abf30d1620a78008a57` |

完整檢查結果與 14 個附件目的地見 [JSON 複核紀錄](</Users/kochi.chuang/conductor/workspaces/medium-articles/surabaya-v1/research/2026-10/same-spec-ten-runs/manuscripts/review-evidence-followup.json>)。
