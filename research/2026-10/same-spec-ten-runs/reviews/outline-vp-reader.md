# 審查結果：「同一份規格，跑十次」大綱修訂版

**總評：** 本輪選題可以保留。大綱已清楚交代幾項限制：無工具（tool-free）、單檔、N=10，以及 AST 只是結構代理指標。四篇骨架目前沒有把 pilot 寫成實驗結果，也沒有預先宣布哪一組勝出。

問題集中在兩處：
- 大綱、評審處置紀錄與 PROTOCOL 三份文件的定義互相不一致。
- 對 VP 讀者而言，缺少「結果出來後要做什麼決策」的對應表。

兩次 pilot 通過 103 項檢查，只證明管線可以運作。它不支持任何一組的效果判讀，也不能拿來預測 formal40 會出現天花板效應。本審查只依據所提供的文件，沒有執行任何程式、瀏覽網頁或進行真人審查。

---

## Blocker（1 項）：阻擋開啟 formal40，不阻擋大綱續寫

**B1　主要比較尚未凍結，而且三份文件互相矛盾**

- **位置：**
  - review-resolution §二 M13 寫「primary C−A，次要 A−A0/B−A/C−B；配對單位是 block」。
  - 大綱 §三.3 寫「各組差異僅作描述，不預設哪一組較佳」。
  - 大綱 §八.五 又寫「依預先 contrast 比較觀察差值」。
  - PROTOCOL〈Analysis fixed before formal execution〉只列各組區間，沒有任何 contrast，也沒有 block 配對。
- **風險：** 看到結果之後才挑選比較方式。這正是 PROTOCOL 宣稱要防範的事。
- **修法（freeze 前擇一，三份文件同步）：**
  - (a) 刪除 M13 的 primary 與次要 contrast。大綱 §八.五 改為「只報各組 k/10 與區間，組間差異不作推論」。
  - (b) 把 C−A 等比較的估計量、區間方法與 block 配對寫進 PROTOCOL 與 `analyze.py`。

---

## Major（7 項）

**MJ1　Primary endpoint 的定義不一致**
- **位置：** PROTOCOL 的 accepted completion 包含「intact generation boundary」。大綱 §三.3 表格只寫 `cli_success && artifact_success`。
- **修法：** 在表格補上 boundary 條件，或註明「發生 breach 即停止 campaign，該名額不以功能失敗計」。欄位名稱要與 `analyze.py` 一致。

**MJ2　「preregistration v1」用詞越界**
- **位置：** PROTOCOL 標題。它與大綱 §三.2、§八.一「不暗示第三方預註冊登錄」互相衝突。
- **修法：** 改名為「執行前封存協議 v1（本機 freeze，無第三方登錄）」。

**MJ3　A1 來源與本輪 A0/A 對比不同類，讀者容易誤移植 +29.7%**
- **位置：** 大綱 §四 來源表的 2608.25399 列，以及規格篇 §五。
- **問題：** A1 比較的是 bare user story（刪除資訊）與 full spec。本輪 A0 與 A 的規範要求相同，差別在寫法。
- **修法：** 在規格篇明寫：「A1 比的是資訊有無，本輪比的是同一組要求的寫法，不能用 A1 預期 A0 比較貴。」引用時同時列出 95% 區間（−0.3%～+66.8%，包含零），並註明這是單一模型、五個 task 的結果。

**MJ4　Streaming 驗收沒有落到協議裡**
- **位置：** 大綱 §七.五與 M22 要求逐行 flush 的實際測試。PROTOCOL〈External acceptance〉只寫「sends one input stream」。
- **修法：** freeze 前在 PROTOCOL 列出 streaming 案例與判定方式，例如逐行寫入 stdin，再檢查對應輸出出現的時點。若沒有實作，契約篇 §五只能寫「streaming 行為本輪未驗證」。

**MJ5　不足 40 個名額時沒有分析路徑**
- **位置：** PROTOCOL 規定 `analyze.py`「requires all forty」，但同一份文件又規定 breach 必須停止並報告 incomplete。大綱 §八.二也要求報告 incomplete study。
- **修法：** freeze 前定義不完整資料集的輸出：
  - 已執行名額的 flow table；
  - 未啟動的名額標為 not started；
  - 是否計算各組區間，要事先寫明。

**MJ6　VP 讀者缺少決策對應，tool-free 邊界也出現太晚**
- **位置：** 總論 §一 把主讀者寫成「已經使用 coding agents」，tool-free 卻到 §四才說明。§七 的決策大多是「是否值得進一步研究」。
- **修法：**
  1. 在 TL;DR 與總論 §一 首段就寫明「單檔、單次、無工具生成，不是 agent loop」。
  2. 在總論 §七 加一張事先寫好的「結果情境 → 可做的決策」表。表內只寫情境，不填預期值，至少涵蓋：
     - 四組全數通過：天花板效應，本設定下四組無法區分；
     - 某一組大量失敗：先檢查 requirement coverage 與 evaluator；
     - 都通過但結構差異大：只能描述差異，不能判斷好壞；
     - evaluator 故障。
  3. 事先說明解析度：10/10 的 95% 下界約為 69%，組間的小差距不能拿來排序。

**MJ7　A2 的 metadata 差異尚未解決，卻擔任總論的主要證據**
- **位置：** 大綱 §四 的 2607.02436v2 列；audit A2 記錄標題不同、頁數 22 對 43。
- **修法：** 列為發布閘門。引用時標明所讀版本是 v2 PDF 並附上 hash，只引用 Table 8/9 的數量代理指標。差異解決前，不寫進 TL;DR。

---

## Minor（7 項）

- **MN1　反例不一致：** 大綱 §二只列 `[]`，PROTOCOL 列 `null` 或 `[]`。兩處要統一。
- **MN2　audit 內容過時：** evidence-audit〈對本系列 protocol 的具體要求〉仍寫「具體 task 尚在選擇」。應補上已選定的 commit 與檔案。
- **MN3　總題容易誤導：** A0 與 A/B/C 並非同一份文字，只共享同一組要求。副題或總論 §四首次出現時，要說清楚是「同一組要求」。「跑十次」依 STYLE.md 補上對象，例如「每組獨立生成十次，共 40 個名額」。
- **MN4　成本數字會被誤讀成預算：** PROTOCOL 的 USD 5 是牌價上限。大綱 §三.4 與 T3 要標明「依牌價估算，非實際帳單」。
- **MN5　預設了方向：** 大綱 §八.七「若 pattern 提高相似度卻沒有交付收益」隱含了預期。改成中性寫法：「若某組相似度較高，但 accepted completion 沒有較高」。
- **MN6　三部曲缺少讀者角色：** style brief 要求每篇在節標題點名受影響的角色。規格篇、契約篇、變異篇應各自補上，例如 spec 作者、QA lead、自主權簽核者。
- **MN7　exit code 意義太晚出現：** 3/4/5 的含義在總論 §三首次出現時就要一句話交代，不要等到規格篇 §二。

---

## 成稿前的證據閘門

1. B1 解決，三份文件同步後才 freeze。
2. sandbox 與 CLI probe、streaming 測試都有實際紀錄。
3. 40 個名額全部有狀態，或依 MJ5 的規則輸出 incomplete 報告。
4. A2 版本差異已處理。
5. 所有圖表都回算到原始資料。

pilot 結果只能放在變異篇 §八.一，作為管線驗證，不列入任何一組的 k/10。