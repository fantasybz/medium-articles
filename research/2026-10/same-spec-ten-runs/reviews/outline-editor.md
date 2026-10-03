# 「同一份規格，跑十次」大綱修訂版審查

**審查範圍**：本審查只讀了這次提供的六份檔案，包括大綱、STYLE、2026-10 style brief、evidence audit、review resolution 與 PROTOCOL。我沒有執行程式、沒有瀏覽網頁，也沒有人工審查。實驗 README 與「103 項檢查」的內容不在 packet 內，我無法核對。以下不把 pilot 通過當成任何 arm 的模型證據。

**結論：就大綱修訂而言，沒有 blocker。** M1–M5 牽涉正式 endpoint 與分析規則，必須在第一個正式 request 之前收斂。如果 freeze 已經完成，就要以 amendment 處理，否則分析規則會變成看過資料後才決定。各檔日期一律是 2026-09-25，彼此一致。

---

## Major

**M1　主要比較對象有三種說法**
- **位置**：
  - review-resolution M13 寫「primary C−A，次要 A−A0/B−A/C−B」，N32 寫「三相鄰對比」。
  - 大綱三.3 寫「各組差異僅作描述」，八.五 寫「依預先 contrast」，但全文沒有定義這些 contrast。
  - PROTOCOL〈Analysis〉只報各組區間，也沒有任何判定規則。
- **修法**：以 PROTOCOL 為準，把 M13 改為「沒有 primary contrast；若報差值，只描述 A−A0、B−A、C−B，配對單位是 block」。同時把這條規則寫進 analyze.py 與 freeze manifest。大綱八.五要列出這三個差值，或刪掉「預先 contrast」。

**M2　primary endpoint 少了一個條件**
- **位置**：大綱三.3 的表把 `accepted_completion` 定義為 `cli_success && artifact_success`，七.二 也照此說明。PROTOCOL 則另外要求 "an intact generation boundary"。
- **修法**：在三.3 的表中新增 `boundary_intact`。它的判準是初始化 trace 顯示指定 model，而且 tools、MCP、skills、slash commands 都是 0。同時交代邊界被突破時整個 campaign 停止，以及已啟動名額如何留在分母中。

**M3　「preregistration」違反大綱自訂的命名規則**
- **位置**：PROTOCOL 標題是 "preregistration v1"。大綱三.2 與八.一 規定，沒有第三方登錄時不使用登錄描述。
- **修法**：把標題改為 "Frozen pre-execution protocol v1 (local; not registered with a third-party registry)"，中英文版與 References 同步修改。

**M4　streaming 驗證範圍對不上**
- **位置**：大綱七.五與 review M22 要求用真實 streaming 測試檢查逐行 flush。PROTOCOL〈External acceptance〉只寫 "sends one input stream… compares stdout, stderr and exit"，沒有時序檢查。從 packet 看不出 103 項檢查是否包含這一項。
- **修法**：freeze 前在 protocol 與 case 表中加入 incremental-output 測試，也就是分段寫入 stdin，並在 EOF 之前讀到對應輸出。若不做這項測試，二與七.五的「保留 streaming 行為」要改成「保留最終輸出的內容與順序；即時 flush 尚未驗證」。

**M5　未完成的 campaign 與 analyze.py 的前提互相衝突**
- **位置**：
  - PROTOCOL 規定 analyze.py 要有全部 40 筆紀錄才計算，但 boundary breach 會讓剩餘名額停止執行。
  - 大綱八.二 寫「全局預算停止」，但 PROTOCOL 只有每個名額 600 秒與 USD 5 的上限，沒有全局預算。
- **修法**：規定 campaign 停止時，由 runner 為未啟動的名額寫入 `not_started` 紀錄，讓凍結的 analyze.py 仍能輸出 incomplete 報告。「全局預算停止」則改成 protocol 實際存在的停止條件：boundary breach 與 identity/hash 不符。

**M6　與「綠燈不是驗收」系列重疊，卻沒有交代兩者的關係**
- **位置**：
  - 10 月系列已經談過外層綠燈、mutation score 與 pass^k，其中 pass^k 屬於可靠度篇。
  - 本大綱七.二「避免 CLI 回傳 0 就視為 parser 正確」、八.二 的 `k/10`，以及 PROTOCOL 的 mutation tests，都會讓讀者覺得在重講同一套觀點。
  - 大綱全篇沒有提到這個系列。
- **修法**：在總論二加一段說明分工。可靠度篇處理單一流程的 gate 與 pass^k。本系列量測同一份規格在不同文件條件下的重複生成分布，而 `k/10` 不是 pass^k gate。依 STYLE〈跨篇指涉〉，引用時要用確認過的篇名與連結。

**M7　「可以重播」與「第一手」的邊界不清**
- **位置**：
  - 大綱一寫「可以重播的 repo 實驗」，但 PROTOCOL 明言 hosted model 無法保證逐位元重現。
  - 二的標題是「第一手案例」，而「重現時以 `git show`…」一句沒有主詞。
  - 二只列出 `[]`，PROTOCOL 還提到 `null` 也會讓程式 crash。
- **修法**：
  - 把一的說法改成「封存產出可以重新評估，流程可以重新執行，但生成結果不保證相同」。
  - 在二補上由誰、在哪一天、用什麼命令重現。它是研究流程中的重現，不能寫成作者親歷的事故。
  - 把 `null` 反例加進二。

---

## Minor

**m1　大綱與 PROTOCOL 的已定值不同步**
- **位置**：大綱三.2–三.4 仍寫「本檔未填寫 model ID…」「若實作採 node-type cosine」。PROTOCOL 已固定 `claude-opus-5-5`、high、600 秒、USD 5、seed 20260925，以及三項結構指標。
- **修法**：大綱改成連到 freeze manifest 取值，並把「若採」改成已選定的描述。狀態列補上「2 次 pilot（A0、C）已執行，結果見實驗入口；正式 40 個名額尚未執行」。不能寫成 A、B 已經驗證。

**m2　「成本」一詞超出量測範圍**
- **位置**：總題寫「把……成本分開量測」，但 PROTOCOL 說明 list price 不等於實際帳單。
- **修法**：把標題改成「資源使用」，或在第一次出現時定義為「provider 回報的 token 與 list-price 估算」。

**m3　TL;DR 引用數字的區間限制**
- **位置**：大綱尚未規劃 TL;DR 中「有來源、交代範圍的數字」。
- **修法**：若採用 A1 的 +29.7%，要同時寫出 90% 區間，並說明 95% 區間包含 0。

**m4　缺少讀者角色與組織切入點**
- **位置**：style brief 要求每一篇在標題或開場點出讀者角色。目前只有總論七有工程主管。
- **修法**：規格篇對 Tech lead 與規格作者，契約篇對測試工程師，變異篇對簽核自主權的人。

**m5　後半部退回短語堆疊**
- **位置**：八.六與十的表都以名詞片語堆疊，違反 STYLE〈整篇要有一致的完成度〉。六.六寫「下一篇」。
- **修法**：成稿時補上使用情境與負責的人。把「下一篇」改成契約篇的篇名。

**m6　結語的條件不完整**
- **位置**：八.七「先改 evaluator」。
- **修法**：補上「以 amendment 對全部 sealed snapshots 統一重評」。同一段的「正常候選」沒有定義，要寫清楚。

**m7　尾段與 AI 審查身分未規劃**
- **位置**：大綱沒有規劃系列文章、References 與 AI 協作說明三段尾段。
- **修法**：在 AI 協作說明中寫明，生成模型與本審查同屬 Claude（claude-opus-5-5），AI 審查不能當成真人或獨立人工審查。PROTOCOL release gate 中的 "independent design review" 也要註明審查者的身分。

**m8　review-resolution 的排字錯誤**
- **位置**：以下詞彙缺空格：「allowlistedpacket」「successslice」「reviewminutes」「3warm-up」「reproducibility1.000」「vsaccepted」。R-m3 的「没有」是簡體字。
- **修法**：補上空格，並把「没有」改成「沒有」。

**m9　評估順序與 PROTOCOL 不一致**
- **位置**：PROTOCOL 規定全部候選生成完成後才開始評估。大綱三.1 的寫法像是每封存一份就立刻驗收。
- **修法**：依 PROTOCOL 同步修改三.1 的敘述。

---

## 其他確認

- **證據使用**：大綱四的五份來源用途與 evidence audit 的限定一致。A2 的 metadata 差異仍未解決，大綱已保留這項標註。
- **未見的問題**：我沒有發現虛構的親歷事件、對話或結果。大綱也沒有把 pilot 結果外推到正式 40 次。