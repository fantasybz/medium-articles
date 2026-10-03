# 審查結果：「同一份規格，跑十次」大綱修訂版（2026-09-25）

**範圍：** 本審查只依 packet 內的檔案與五份原文全文。我沒有執行程式、沒有瀏覽網頁，也沒有人工審查。packet 未提供 pilot 的「103 項檢查」明細與實驗 README，因此下文不推論 pilot 結果能代表正式 40 名額。

**總評：** 大綱與五份來源的對應大致正確。我抽核的 A1–A5 數字都與原文一致，包括 +29.7% 的 90%／95% 區間、×1.34、Table 8/9、+4.9pp 是 paired score、p=.0312／.3125，以及 75 runs。大綱也沒有把 pilot 寫成四組都已驗證。**作為研究骨架，大綱本身沒有 blocker；但開啟正式 40 名額之前，有 1 項 blocker。**

---

## Blocker

**B1｜三份文件的主要估計對象不一致，正式 freeze 前必須統一**

- **位置：**
  - `review-resolution.md` 二、M13 寫「primary C−A，次要 A−A0/B−A/C−B；配對單位是 block」。
  - 大綱 三.3 寫「各組差異僅作描述，不預設哪一組較佳」，但 八.五 又寫「依預先 contrast 比較」，卻沒有定義 contrast。
  - `PROTOCOL.md` 只寫 per-arm 區間與「no superiority…decision rule」，沒有任何 contrast。
  - `accepted_completion` 的定義也不一致：大綱 三.3 的表格是 `cli_success && artifact_success`，PROTOCOL 另外要求「an intact generation boundary」。
- **風險：** 先看結果再選擇報哪個對比，正是 M13 與 N17 要防止的問題。
- **修正：**
  - 在 PROTOCOL 明列要報的 contrast（或明寫「不報任何 contrast」），以及配對方式（block 或獨立）和區間方法。
  - M13 與大綱 三.3、八.五 同步改寫。
  - 三份文件採用同一個 `accepted_completion` 定義。
  - `analyze.py` 的 hash 納入 freeze。完成以上各項之後，才能開啟正式名額。

## Major

**M1｜streaming 相容要求沒有進入 PROTOCOL 的驗收描述**

- **位置：** 大綱 七.五、M22 要求逐行 flush 的實測，但 `PROTOCOL.md`〈External acceptance〉只寫「sends one input stream…compares stdout, stderr and exit status」。
- **修正：** 在 freeze 前寫明 streaming 案例的做法：分段寫入 stdin，並在寫入期間讀取 stdout 的時序斷言。若 evaluator 做不到，大綱 二、七.五 應改寫為「本輪只驗證批次輸出，未驗證即時 flush」。

**M2｜cache 狀態與 cwd 可能讓成本表出現非介入差異**

- **依據：** 2608.01347 附錄 E.4 報告 Claude Code 會把 working directory 嵌進 system prompt，換目錄會破壞 cache 重用。同一段也指出 cache 命中具有機率性，而且跨 session 共用。SaltBench §4.1 另記錄 cache 狀態依帳號與 session 保存。
- **位置：** PROTOCOL 對每個名額都使用「a new empty temporary working directory」，又允許「四個生成程序並行」。
- **風險：**
  - 「fixed system input」未必在 byte 層級固定。
  - 同一 block 內先啟動的名額可能付 cache write，後啟動的則取得 cache read。
- **修正：**
  - 用 probe 確認這個 CLI 版本是否嵌入 cwd；若會，就改用固定路徑名稱。
  - 每個名額記錄啟動位置與 cache read/write。
  - 成本表同時列 billed 與 no-cache 等值，並依啟動位置分層描述。
  - 大綱 三.1 的「固定 system prompt」改成「固定 runner 提供的 system input；CLI 內建 prompt 不可見」（PROTOCOL 已承認這一點）。

**M3｜整檔 AST cosine 可能被共享 seed 壓到天花板**

- **位置：** 大綱 三.4、八.四；PROTOCOL〈Structural measures〉。
- **問題：** 候選都是重寫同一個 seed parser。整檔的 node-type 分布很可能在每一對之間都接近 1，F2 就看不出差異。大綱只把這點列為限制，沒有對策。
- **修正：** 在 freeze 前擇一並凍結：
  - 加入「候選 vs seed」的基準相似度欄；或
  - 只對變更區域（diff 涉及的函式）計算 descriptor。

  若 freeze 後才加，必須標為 amendment 與探索性分析。

**M4｜停止條件可能與組別相關，造成「成功者條件分布」偏差**

- **依據：** SaltBench §4.1 與第 5 節第 16 點：預算上限只截掉 treatment 組的 cell，使後續分析的存活樣本在 treatment 組偏易。
- **位置：** 大綱 三.4、八.四、八.五 雖標示「成功者條件分布」，但沒有要求交代各組失去哪些名額。
- **修正：** T3 與 F2 旁固定列出各組 timeout、budget 停止與無 artifact 的數量及名額 ID，並加註「條件分布只在停止率相近時才可並列比較」。C 組 packet 較長，更需要檢查 600 秒上限是否和組別相關。

## Minor

1. **PROTOCOL 標題寫「preregistration v1」**，與大綱 三.2、八.一「不暗示第三方預註冊」衝突。**修正：** 改成「執行前封存協議 v1（本機 freeze，非第三方登錄）」。
2. **大綱 一「可以重播的 repo 實驗」**與 PROTOCOL「cannot guarantee byte-identical reproduction」衝突。**修正：** 改成「可重新執行與重新評分」。
3. **大綱 八.二「全局預算停止」**：PROTOCOL 只有每個名額 USD 5／600 秒的上限，沒有全局預算。**修正：** 刪除，或在 PROTOCOL 補上全局預算。
4. **PROTOCOL「analyze.py requires all forty scheduled records」**與 halt／incomplete 的報告方式可能衝突。**修正：** 寫明未啟動或中止的名額也要有狀態紀錄，並確認 analyze 在 incomplete 情況下會輸出，而不是直接報錯。
5. **`evidence-audit.md`〈protocol 具體要求〉仍寫「具體 task 尚在選擇」**，已經過期。**修正：** 更新為固定 commit 與 `codex_jsonl.py`，並連回大綱 二。
6. **evidence-audit A4 有兩處不精確：**
   - 「部分 cell 缺 build-provenance receipt」：原文 §8 是「the matrix's cells carry no build-provenance record of their own」，指整個 matrix。
   - 「每 condition n=3」：reading A 有三個 plain 條件是 n=4。**修正：** 照原文改寫。
7. **pilot 的呈現方式：** PROTOCOL 規定 pilot 只跑 A0 與 C。實驗 README 描述「103 checks」時，應註明 A 與 B 沒有實際 model request，以及 pilot 之後是否重新 freeze。
8. **大綱 二的 bug 重現沒有工件連結。** review-resolution R-F5 說「已重現」，但 packet 裡沒有 log 或 hash。**修正：** 附上重現腳本、輸出與 exit code 的 hash。PROTOCOL 也列了 `null`，大綱只寫 `[]`，兩邊應一致。
9. **大綱 三.4 寫「若實作採 cosine」**，PROTOCOL 則已固定為 cosine，且另有 function/class counts。**修正：** 改成確定句，並補上 counts。
10. **A2 的 metadata 差異**（abstract「observational study／22 pages」vs PDF「90 matched agent runs」）只能從 PDF 端核對，packet 沒有 abstract 頁。應維持開放，引用時標注 PDF 版本與 hash。
11. **CLI 版本固定：** SaltBench §4 指出從 PATH 解析 client 會在 vendor 更新時靜默換版。**修正：** 在 freeze manifest 用絕對路徑固定 CLI 版本。

---

**判定：** 大綱可以作為研究骨架接受。B1 必須在正式 freeze 前關閉；M1–M4 應在同一份 freeze 內處理，否則只能以 amendment 標示為探索性分析。正式結果產生前，文章不能引用 pilot 通過作為任何組別的成效證據。