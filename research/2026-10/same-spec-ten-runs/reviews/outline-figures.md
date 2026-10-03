# 審查意見：「同一份規格，跑十次」五個圖表工件（F1、T1、T2、T3、F2）

**審查範圍與依據：** 本次只審閱使用者提供的五份檔案：大綱修訂版、`evidence-audit.md`、`review-resolution.md`、`PROTOCOL.md` 與兩份風格文件。我沒有執行任何程式，沒有瀏覽外部來源，也沒有取得人工審查結果。實驗 README 與 freeze bundle 不在 packet 內，因此我無法確認「兩次 pilot 通過 103 項檢查」這件事；以下判斷也不以此為前提。

## 結論

**本輪大綱修訂沒有 blocker。** 五個工件目前只定義資料需求，沒有填入虛構數值、預期排序或效果方向，符合「先定資料需求，不畫結果」的原則。

不過，下面 M1 到 M3 必須在正式 freeze 之前關閉。否則 T3 的欄位定義與分母會與凍結後的 `analyze.py` 對不上。

## 各工件的性質與發布準備度

| 工件 | 性質 | 製作前提 | 目前可否定稿 |
|---|---|---|---|
| F1 | 可執行研究的流程圖，須依實際程式繪製 | freeze bundle | 否，要等 freeze |
| T1 | 規格與介入對照表 | frozen packets 與 coverage 檢查 | 否，要等 freeze |
| T2 | 契約規範表 | frozen requirements 與 cases | 否，要等 freeze |
| T3 | 結果表 | 40 個正式名額的完整 ledger | 否，正式 40 次未執行 |
| F2 | 探索性結果圖 | sealed candidates 與 metric | 否，正式 40 次未執行 |

五個工件都不是概念圖。F1 容易被畫成概念示意，但它必須反映 runner 與 evaluator 的實際行為。

## Major

**M1：三份文件對主要結果的定義不一致**

- **位置：** 大綱§三.3 表格將 `accepted_completion` 定義為 `cli_success && artifact_success`。`PROTOCOL.md`〈Schedule, stopping, and outcomes〉則另外要求 "an intact generation boundary"。
- **問題：** 若 T3 依大綱建欄，邊界被破壞的名額仍可能被算成通過。
- **修法：**
  - 大綱§三.3 與 T3 改為三條件。
  - T3 新增 `boundary_intact` 欄。
  - T3 新增一列「boundary breach → campaign halt」，並列出其後未啟動的名額數。

**M2：是否報告組間差值，文件之間互相矛盾**

- **位置：** `review-resolution.md` M13 寫「primary C−A，次要 A−A0/B−A/C−B，配對單位是 block」。這與以下三處衝突：
  - 大綱§三.3：「各組差異僅作描述，不預設哪一組較佳」。
  - `PROTOCOL.md`〈Analysis〉：只列各組的 Clopper–Pearson 區間，並寫明 "no superiority… decision rule"。
  - 大綱§八.五：「依預先 contrast 比較觀察差值」。
- **修法：** freeze 前擇一處理。
  - 若保留 contrast，要在 PROTOCOL 寫明差值定義、以 block 配對的區間方法，以及 missing 值的處理方式。
  - 若不保留，就刪除 M13 的 "primary" 字樣與§八.五的 contrast，T3 也不設差值欄。
  - 在做出決定之前，T3 一律不設差值欄。

**M3：T3 的分母與狀態分類尚未定義完整**

- **位置：** 大綱§三.3 一方面說「每個排定名額都在分母內」，另一方面又說「評估器故障則標 missing/error」。此外，`PROTOCOL.md` 允許在五秒寬限期內 `artifact_success` 為真、但 `cli_success` 為假。
- **問題：** 現有欄位無法同時表達「在分母內」與「缺失」，也無法呈現 CLI 與 artifact 的交叉組合。
- **修法：** T3 拆成三塊。
  - **(a) 狀態格：** 以 10 個 block × 4 組排成 40 格，每格填一個互斥的終局代碼，例如：未啟動（halt）、interrupted、timeout、transport、budget stop、schema invalid、驗收失敗、evaluator error、accepted。這樣也能直接看出時間漂移。
  - **(b) 各組結果：** 每組報 `k/10`、未解決的 missing 數與雙側 95% 區間。明定未解決的 missing 不計入 k，也不從 10 中移除；只要還有 missing，該組就標為「未完成」。
  - **(c) 交叉表：** `cli_success × artifact_success` 的 2×2 表。
- **呈現方式：** 區間以文字，或以固定 0–100% 軸的點加區間呈現，不使用長條圖。

**M4：T3 把成本併入結果表，與大綱自己的原則衝突**

- **位置：** §九 的 T3 列寫「成功、失敗、缺失與成本的分母」，但§三.4 說結構與成本是「另外兩張表」。
- **修法：** 另立資源表（T3b），或把資源移出 T3。資源表的欄位包括：
  - input、output、cache read/write tokens。
  - 「CLI 回報的 list-price 估計（非實際帳單）」。
  - wall time，並註明輪詢間隔 0.5 秒的解析度，以及 timeout 截斷不代表完工時間。
  - 缺失值留空並附原因，不填零。

**M5：F2 的編碼方式未決定，且容易誇大差異**

- **位置：** §九 的 F2 列寫「結構矩陣**或**代表 pair 的 diff」，兩種做法尚未擇一。
- **問題：** 候選檔都從同一個 seed 修改而來，node-type cosine 很可能集中在接近 1 的區間。熱圖若自動縮放色階，會把極小的差異畫得很醒目。
- **修法：**
  - 主圖改為每組一條 pair 值點圖。軸範圍固定並在圖上標明，同時標出有效 pair 數與 NA 數。
  - 另列「候選檔與 seed 的 cosine」作為參照，讓讀者判斷這個指標有沒有辨識力。這是新增的 descriptor，必須在 freeze 前寫進 PROTOCOL。
  - 完整矩陣放附錄。
  - 補上 PROTOCOL 已列、但大綱漏掉的 function/class counts。
  - 代表 diff 的選取規則事先凍結，例如取中位數 pair，並以 candidate ID 決定平手。
  - 全部可解析產出與已通過驗收產出，分成兩個標明的 slice。

**M6：F1 必須反映實際執行順序與邊界**

- **位置：** §九 的 F1 列。依 `PROTOCOL.md`〈Release gates〉，所有候選「generate all candidates before evaluation」，也就是先全部生成、再統一評估，並不是每個名額生成後立即驗收。
- **F1 須包含：**
  - 先全部生成、後統一評估的兩段式順序。
  - candidate process 在執行時看得到 event stream，但看不到 expected outputs。
  - Seatbelt sandbox 旁邊只標示「probe 紀錄 <路徑>」，不標「已隔離」。
  - boundary breach 通往 halt 的路徑。
  - 五秒 grace period。
- **標註：** 圖說寫明「依 freeze bundle <hash> 繪製」。

## Minor

- **m1｜T2：** 「3 → 6 → 4 → 5 → 0」的箭頭寫法容易被讀成時間順序或數值大小。建議改成排名表，欄位為：代碼、意義、「同時出現時是否勝出」、驗證方式。驗證方式要分開真實 streaming 測試與一次性送完 stdin 的 batch 測試；M22 仍未關閉。表格內容應從 frozen cases 檔自動產生，並附上 hash。
- **m2｜T1：** packet hash 放附錄，正文不放。新增兩個欄位：「新增規範要求：無」，以及說明由誰、用什麼方式核對。本輪沒有真人審查，因此要寫明是 script 或 AI 核對。另外補一列共同條件，填入 freeze 後的 model ID 與 effort。
- **m3｜§九開頭：** 「在 protocol 與結果確定後補 figure plan」與本表的功能矛盾。F1、T1、T2 只需要 freeze 即可製作。建議把這句改成分兩階段，並在表中新增「所在篇章與節次」欄。
- **m4｜PROTOCOL 標題：** 目前寫 "preregistration v1"，與大綱§三.2「不暗示第三方預註冊」衝突。圖說與 T3 表頭一律改用「執行前封存的研究協議」。
- **m5｜Pilot：** pilot 的結果不進入 T3 或 F2。若正文提到「103 項檢查」，要寫清楚分母，說明是每次 pilot 各 103 項還是合計，並附上檢查清單連結。同時註明 pilot 只涵蓋 A0 與 C 兩組，不代表四組已通過驗證，也不能用來預測正式 40 次的結果。