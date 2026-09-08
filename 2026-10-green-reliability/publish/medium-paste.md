<!--
Medium 發布指南（此註解區塊不要貼進 Medium）

自動化：`./tools/medium_draft.sh <article-dir>` 會建好草稿並比對內容，停在發布前一步。
細節見 repo 根目錄的 PUBLISHING.md。以下是手動流程與發布後必做的收尾。

【系列狀態】以各篇 publish/PUBLISHED.md 為準。Medium 限制同一作者 24 小時內最多發布或排程 2 篇，
見 PUBLISHING.md 的〈發文數量上限〉。

【手動流程】
1. 開新 story：https://medium.com/new-story
2. 貼上下方內容（從標題那行開始，不含本註解）。
3. 看到 📌【在此插入…】的行：刪掉該行，按 + 插入同目錄 images/ 裡對應的 PNG。
4. code block：在 Medium 選取後按 ``` 轉成 code block。
5. 封面圖選流程圖，不要選表格截圖（縮到卡片尺寸看不清）。
6. Tags 建議：AI, Software Engineering, Engineering Management, Agentic AI, DevOps

【發布後收尾—不做的話系列會斷】
7. 記下本篇 Medium URL，補進 repo 的 README 索引與 publish/PUBLISHED.md。
8. 把本篇兩處的系列連結換成真正的 Medium URL：
   (a) 開頭「系列導覽」那一行
   (b) 文末「系列文章」清單
   （尚未發布的篇在這裡是純文字「（即將發布）」，不是相對路徑；上線後換成真正的 URL）
9. 回頭編輯已發布的其他篇，把指向本篇的連結補上。
-->

# 綠燈不是驗收（三）可靠度篇：SWE-Gate 量到的 34%—constraint tests、pass^k 與授權擴張的閘門

> **TL;DR** — 三部曲最終篇，講 reliability gate：授權要不要擴張，看什麼數字。SWE-Gate 在 75 個 Python repo、303 個修補任務上量到：功能測試通過的 644 個修補裡有 221 個（34%）違反 reviewer 實際加過的約束—每三個綠燈修補就有一個違反了 reviewer 在乎的約束。本篇只講三個數字。**constraint pass rate**：把 review 約束寫成可執行的 constraint tests（review 評論 → 規則 → 檢查），讓「reviewer 在乎的事」變成 CI 的一部分。**pass^k**：可靠度不是能力—pass@1 是每個 case 單次嘗試的成功率，pass^k 是 k 次全過的 case 比例，分開報。**oversight budget**：兩個準確率差 0.3 個百分點的系統，可能差近 10 個百分點的人工複核需求（READY），所以「要付多少人看」是從你的可靠度目標反推出來的預算，不是「盡量多看」—本篇給一個簡化模型讓你自己算。三個數字進 leadership 月報，並接回營運篇的 G2 gate：授權擴張看 pass^k、constraint pass rate、escape rate，不看 pass@1。

> 系列導覽：[總論](https://medium.com/p/582f24223eea) → [一、測試篇](https://medium.com/p/b01055139451) → [二、Review 篇](https://medium.com/p/ccbf0cbe2691) → **三、可靠度篇（本篇）**

---

## 一、SWE-Gate 量到的 34%

先用一組數字定錨這一篇要處理的落差。SWE-Gate 多做了一件事：它不只問「功能測試過了沒」，還把 reviewer 當初真的在 PR 上要求過的東西抓出來，寫成可執行的檢查，跟功能測試分開跑一次。

34% 是 SWE-Gate 在 75 個 Python repo、303 個修補任務上量到的。它把功能測試與 review-constraint tests 分開跑：644 個通過功能測試的修補裡，221 個違反了約束，而約束來自真實的 PR 評論。用白話講就是：每三個綠燈修補，就有一個違反了 reviewer 在乎的約束。

這個數字有兩個地方容易被讀錯，先擋掉。

領域邊界要先說清楚—Python repo、修補任務，不是「所有 agent PR」。它量的是這個範圍裡的事。換一種語言、換一種任務型態，數字要重新量。

分母也要看清楚。分母是「通過功能測試的修補」，所以正確的白話是「每三個綠燈修補就有一個違反約束」。**不是**「綠燈量不到 reviewer 在乎的三分之一」。後者把單位換成了「reviewer 在乎的事」的比例，論文沒有量這個。兩句話字面很像，但分母不同，拿錯的那句去說服人，會在第一個追問就垮掉。

綠燈其實有不同層，每一層都有 in-domain 的證據。in-domain 的意思是：那份數字是在跟你相近的語言、相近的任務型態上量出來的，不是從別的領域借過來的。以下三份研究剛好各站一層。

SWE-NFI（188 個任務、92 條可執行規則）量的是「功能過，不等於非功能規則滿足」：最佳 agent 功能通過 70.0%，非功能規則普遍不及。非功能規則指的是效能、安全、log 格式這類要求，它們不會讓功能測試變紅，但團隊真的在乎。

OpenHarmony Bench（153 個 app 任務）量的是更下面一層，「**build 綠，不等於行為對**」：可建置 94.77% 到 100%，行為正確只有 48.36% 到 58.39%。這一層的落差大得多，但它跟本篇要處理的事無關。行為錯誤本來就是功能測試該抓的事，跟 reviewer 約束無關，所以它不在 34% 那一層。

Rebuild Dossier 則是設計前提，不是觀察到的實證：當 agent 有機會 game 測試時，測試套件全過不等於正確，所以它先鎖介面、一次一個測試。它給的不是一個數字，是一句提醒：只要 agent 能同時改實作與改測試，測試全過就不再是獨立的證據。

分層之後會看到一件事：這三層在儀表板上長得一模一樣，燈都是綠的。差別只在那盞燈量的是什麼，以及你有沒有另外去量。綠燈不會告訴你它沒量到什麼，這正是它最危險的地方。

本篇只處理其中兩層：reviewer 約束那一層，與可靠度那一層。

---

## 二、把 review 約束寫成可執行的 constraint tests

上一節說綠燈量不到 reviewer 在乎的約束。這一節做的是最直接的回應：把那些約束寫成 CI 跑得動的檢查。這種檢查有個名字，叫 constraint tests。它不驗功能對不對，那是功能測試的事。它只驗一件事：這個 PR 有沒有踩到團隊講過的規矩。

約束長什麼樣？先把它想成團隊反覆講過、但不該每次都靠人記得的那些話。以下七類是筆者從團隊的 review 評論整理的，用來示範 constraint tests 可以從哪裡長出來，不是一份完整的分類法。SWE-NFI 的 92 條規則與 SWE-Gate 的評論分類，以論文原文為準：

📌【在此插入表 table-01.png】

表裡最值得看的是最右邊那一欄。七類約束，七種檢查方式，沒有一種需要 LLM 判斷：lockfile diff、AST 掃描、import graph 都是老工具。這代表把 review 約束變成檢查，門檻比多數人想的低。

Pipeline 是四步：review 評論 → 規則 → constraint test → CI。規則檔的形狀借自 2026 年 7 月一篇研究：每條被接受的 review 評論，都寫成 version-controlled 規則檔裡的一條。Review 篇第三節沿用的就是同一份規則檔。

規則檔要記兩種東西。第一種是來歷，每條規則記來源 PR 與日期，半年沒觸發的規則要 review 是否已經過期。第二種是責任，也就是再加兩個欄位：owner（誰維護這條規則）與 expiry（到期 review 的日期）。規則會爛，就是因為沒人負責、沒有到期日，這兩欄是讓它不爛的機制。

**「改不動」的實作。** 總論第二節把證據分成三類：第一類是 agent 自己說的，第二類是 agent 自己寫的測試，第三類是 agent 改不動的測試。這裡要落地的是第三類，機制有三道。

第一道，`tests/constraints/` 與 golden set 目錄放進 CODEOWNERS、只列人類。第二道，規則檔的變更需要人類 approve。第三道，對第三類測試的任何斷言弱化，由測試篇的 Check 2 直接阻擋。

agent 對 repo 有寫入權，但這三個目錄的變更沒有人類 approve 進不了 main。所謂「改不動」不是禁止 agent 碰，是它碰了也進不去。

這裡也要先跟 11 月契約篇切開，否則兩種約束很容易混成一種。本篇談的約束來自 **review 歷史**，是事後累積出來的、經驗性的。契約篇談的約束來自 **spec**，是事前講好的、規格性的。

兩者都進 CI，但 owner 與壽命不同。review 約束的 owner 是當初提出那條評論的團隊，壽命由 expiry 決定，過期就要重新確認還算不算數。spec 約束跟著規格走，規格還在，它就還在。

Before 是每次都要人重講的那句評論：「請不要在這裡直接 new HttpClient，用 `clients.http()`」。它每次只審一個 PR，講完就沒了。After 是它變成的三樣東西：一個可執行的檢查、一條有主人的規則、一道 agent 改不動的門。

第一樣是測試檔。它只掃這個 PR 動過的 Python 檔案，所以跑起來是秒級的：

```python
# tests/constraints/test_http_client_reuse.py
# 規則來源：PR #4821（2026-06-12）；規則檔：rules.md#http-client-reuse
import ast, pathlib, subprocess

ALLOWLIST = {"src/infra/clients.py"}

def changed_python_files():
    out = subprocess.run(["git", "diff", "--name-only", "origin/main...HEAD"], capture_output=True, text=True).stdout
    return [pathlib.Path(p) for p in out.split() if p.endswith(".py") and p not in ALLOWLIST]

def test_no_direct_http_client_construction():
    offenders = []
    for path in changed_python_files():
        tree = ast.parse(path.read_text())
        for node in ast.walk(tree):
            if isinstance(node, ast.Call) and getattr(node.func, "id", None) == "HttpClient":
                offenders.append(f"{path}:{node.lineno}")
    assert not offenders, (
        "直接建構 HttpClient：" + ", ".join(offenders)
        + "。請用 clients.http()。規則來源 PR #4821，見 rules.md#http-client-reuse"
    )
```

第二樣是規則檔。它記的是這條規則的來歷與壽命，`owner` 與 `expiry` 這兩欄是關鍵：

```markdown
<!-- rules.md -->
## http-client-reuse
- 來源：PR #4821（2026-06-12），reviewer 評論
- 規則：不得直接建構 HttpClient；一律用 clients.http()
- 檢查：tests/constraints/test_http_client_reuse.py
- 最近觸發：2026-09-30（半年未觸發即 review 是否過期）
- owner: @acme/platform-humans（維護這條規則的人）
- expiry: 2027-03-31（到期 review：刪、留或改）
```

第三樣是 CODEOWNERS。前兩樣讓規則存在，這一樣讓它改不動：

```text
# CODEOWNERS
/tests/constraints/   @acme/platform-humans
/tests/golden/        @acme/platform-humans
/rules.md             @acme/platform-humans
```

三樣加起來，那句 review 評論就從「每次都要人講」變成「講一次，之後每個 PR 都被檢查一次」。這就是複利的意思：人讀 diff 講的一條評論只審這一個 PR，回收成 constraint test，之後每個 PR 都被它檢查一次。

成本也可以講得更白。constraint tests 是 deterministic、秒級，觸及範圍是整個 PR。「觸及範圍」是總論第十節的用詞，指一個檢查一次能罩住多少程式碼：單元測試只罩住被呼叫到的那幾行，constraint test 罩住整個 diff。

依總論第十節的觸及範圍原則，它是最便宜的驗證，也是 brownfield 的第一道閘。brownfield 指的是已經跑了很多年、測試不全、文件也不全的既有系統。這種系統最怕的就是「要先有測試才能開始」，而 constraint tests 不需要既有測試。

那還沒有 review 歷史的團隊怎麼起步？沒有 review 歷史，就從團隊規範與最近五個 incident 出發，把那幾句「不要再犯一次」先寫成 check。

把這四步畫成一張圖，要看的不是左邊那條主線，是右邊那條回頭的虛線：

📌【在此插入圖 diagram-01.png】

這張圖要你帶走的是那條虛線：規則不是寫完就算數的。沒有過期回路的規則庫，兩年後會變成一堆沒有人敢刪、也沒有人相信的檢查，然後整套機制就被繞過去了。

---

## 三、可靠度不是能力：pass@1 與 pass^k

上一節處理的是「有沒有守住規矩」。這一節處理另一件事：同一件事再做一次，它還會做對嗎。能力與可靠度是兩個數字，很多團隊把它們混成一個，所以先把定義寫死。

定義沿用總論第八節：golden set 的每個 case 跑 k 次。golden set 是團隊自己挑出來、每個月都用同一批題目重跑的驗收案例。

**pass@1 是單次嘗試的成功率，用 k 次重複跑來估。** 每個 case 是 k 次裡過的次數除以 k。它回答的問題是：這件事它平均做得到嗎。

**pass^k 是 k 次全部成功的 case 比例。** 一個 case 只要有一次沒過，這個 case 就整個不算。它回答的問題是：這件事它每次都做得到嗎。

兩者都先 per case 算，再對整個 golden set 取 aggregate。這一步很容易做錯：把所有結果先混在一起算平均，會把「某一個 case 每次都掛」跟「每個 case 偶爾掛一次」看成同一件事，而這兩件事該做的處置完全不同。

還有一個長得很像的符號，先排除掉：「至少一次成功的比例」是 pass@k，是另一個數字，本系列不用。

接下來這句話承重：**pass^k 與 constraint pass rate 只能從第三類證據算**。也就是團隊擁有的測試與 constraint tests，不能從 agent 的結案報告算，也不能從它自己加的、還沒升格的測試算。所謂升格，是指那個測試已經被人類看過、搬進團隊擁有的目錄、進了 CODEOWNERS。

我準備 Claude Certified Architect 考試時的筆記有一條最小的例子：不能用 assistant 的回答文字去猜 loop 是否結束，要看 stop_reason。回答文字是模型自己講的，stop_reason 是系統記錄的，兩者不同源。搬到 code 上是同一件事：agent 說「測試都過了」是它自己講的，CI 的紅綠是系統記錄的。第一類證據不算證據，就是這個意思。

為什麼 code 領域也要這樣量？原因是同一件事只要換個說法，結果就可能不一樣。證據是兩篇改寫敏感度的研究。

RealSWE（381 個任務家族）量到的是：同一個任務換個說法，成績平均掉 6.4 個百分點，而且會重排 model 的名次。名次會被重排這件事，比掉幾個百分點更麻煩。它代表你看到的排行榜有一部分是題目怎麼寫出來的，不是 model 本身的差距。

另一篇語意保持的改寫研究量到的幅度接近：平均最多掉 6.7 個百分點，**但 16 組 model 與 scaffold 的組合裡只有 6 組達到統計顯著。** 所以正確的讀法不是「所有 model 都一樣不穩」，而是效應真實但不均勻。你那一組穩不穩，要對你自己那一組量。

同一件事問法不同結果不同，這就是可靠度問題。

旁證來自 code 以外，這裡是全系列唯一引全數字的地方。Thinkingbox 量的是 507 個 policy-conditioned MCP 工作流，也就是帶著政策約束的多步驟工具呼叫任務：agent 要一邊呼叫工具，一邊守住規則。在這批任務上，Claude Opus 5 的 pass@1 是 66.50%，pass^20 是 47.53%。

你以為它每次會做對三分之二，但能連續二十次都做對的任務不到一半。這中間差了將近二十個百分點，那就是「能力」與「可靠度」的距離。

它的結論「clean termination 與 valid tool calls 不是完成的代理指標」，在 code 領域同樣成立：agent 說它跑完了、工具呼叫也都合法，跟任務有沒有做對是兩件事。

那在自己的 eval 上怎麼做？沿用營運篇的 golden set—20 到 50 個 case—每月跑 k = 5；門檻看的是這一組。frontier set 跑 k = 3；它是另一批更難、目前還過不了的 case，用來看天花板在哪裡，不拿來當門檻。報表固定三欄，每個月看同一組數字。

**我的建議值（不是業界標準）**：k = 5，pass^5 ≥ 60% 才算「可放低 radius 自主」。

**粒度警告**：golden set 少於 30 個 case 時，pass^k 只報趨勢，不當門檻—20 個 case 的粒度是 5 個百分點，一個 case 翻轉就從 65% 掉到 60%，會被月與月的雜訊主導。真要當門檻，就要連續兩個月達標。

報表的三欄長這樣：

📌【在此插入表 table-02.png】

表裡最重要的是最右邊那一欄：三個數字的來源全是團隊自己擁有的東西。哪一欄填不出這個來源，那一欄就不該進月報。

11 月預告一句：pass^k 是「同一份規格跑 N 次」的結果面；11 月量的是實作結構的變異面。同一份規格跑五次全過，不代表五次寫出來的程式碼長得一樣，那是另一種變異。

把三個 case 攤開算一次，兩個數字的差別就看得見了。要看的是中間那個 case B，它只錯一次：

📌【在此插入圖 diagram-02.png】

這張圖要你帶走一句話：同一批 golden case，pass@1 93% 與 pass^5 67% 是兩個數字，不是同一件事的兩種寫法。前者說它平均很行，後者說你還不能放手。授權看後者。

---

## 四、Oversight budget：READY 與一個簡化模型

上一節給的是兩個數字。這一節處理它們的帳單：可靠度目標訂得越高，要付多少人去讀，就跟著往上走。這筆錢有個名字，叫 oversight budget，它是「這個月我打算花多少人力在複核上」的預算。

READY 是企業 agent 部署的資格審查框架（2026 年 9 月）。它有一個對本篇特別有用的觀念：不要只看 agent 的準確率，要從可靠度目標反推「agent 加人工複核政策」要多少人看。它量到的結果很反直覺：兩個準確率只差 0.3 個百分點的系統，人工複核需求差了近 10 個百分點。

先說清楚借的是什麼、不借的是什麼。它的案例是臨床稽核工作流，不是 code—這裡只借概念，數字不移植。全數字與領域說明在總論第八節。

READY 在本篇只用來證明一件事：**準確率的排名，不等於人力的排名。** 我不承諾重現它的數字，它的方法一定比下面這個簡化模型多考慮了東西。

**我的簡化模型（不是 READY 的方法）**，把「人工複核比例」寫成可以算的東西：

> r ≥ (T − p) / ((1 − p) · c)

這條式子的白話讀法是：目標與現況之間的缺口，要靠人眼去補，而人眼只補得回其中 c 的比例。缺口越大、人眼越不可靠，要深讀的比例就越高。三個輸入分別是：

- **p**：該分層在 golden set 上的 **pass@1**。單一 PR 的複核用的是每次嘗試的準確率，不是 k 次全過率。pass^k 留給第五節的授權擴張，不進這條式子。
- **T**：該 blast-radius 層的可靠度目標，也就是 Review 篇分流矩陣的哪一格。blast radius 講的是這個 PR 改壞了收不收得回來，改到 auth 或 schema 跟改內部工具，目標不會一樣。
- **c**：人工複核抓到錯誤的機率。

三個裡面最容易被跳過的是 c，但它決定的東西最多。c 用你自己抽樣深讀的歷史算：深讀過的 PR 裡事後證實有錯的，有多少比例在深讀當下就被抓到。沒有歷史就先用 0.6 起步，每月校正。

這裡要擋掉一個誤讀。測試篇那組數字—86 位開發者判斷 LLM 寫的斷言，錯的只有 49% 被抓到，對的 74% 被認出來。那組數字量的是判斷斷言，不是 PR review 抓缺陷，不能直接當 c。它在這裡只是一個警告：人眼不能假設是 100%。下面算例的 c = 0.6 就是那個起步值。

人眼的抓錯率直接決定你要付多少人力，這條連結本身就是這一節的價值。

下面用自己的數字示範。重點不是要你背公式，是先感受一件事：算出來的人工複核比例，通常比直覺想的高很多。

- p = 0.80、T = 0.95、c = 0.6 → r ≥ (0.95 − 0.80) / (0.20 × 0.6) = 1.25。**全審都不夠**，要先把 p 或 c 拉高。
- p = 0.90、T = 0.95、c = 0.6 → r ≥ (0.95 − 0.90) / (0.10 × 0.6) = 0.83。準確率從 0.80 拉到 0.90，也只把「全審都不夠」變成「審八成」。
- p = 0.90、c = 0.6，把 T 降到 0.92 → r ≥ 0.02 / 0.06 = 0.33。

三條算例擺在一起，先變 p，再變 T。你第一次算完多半會發現：可靠度目標訂在哪一格，比 agent 的準確率更決定人力。

算出來的 r 要接到哪裡？接 Review 篇的分流矩陣。低 radius 可驗證那一格裡有一項叫「非指派者深讀抽樣」，它的比例就是這裡算出來的 r。每一格仍然有人類讀報告 approve，r 決定的只是其中多少比例要逐行深讀。

抽樣還要分層。我的考試筆記另一條是：aggregate accuracy 會掩蓋某些類型的低表現，要做 stratified random sampling。搬到 code 上，分層維度是任務類型、repo、agent 版本，p 也要分層算。

假設一個團隊的 p 整體看起來很漂亮，但 schema migration 那一類任務單獨算會低不少。只看 aggregate，你會照那個漂亮的數字去配人力，然後在最該多看的那一類任務上把人抽走。

下圖 c 那一格的 49%–74%，是上面那個警告：人眼不是 100%。它不是 c 的量測值。

整條路徑畫成一張圖，要看的是最下面那一格：r 不是終點，它還要被分層抽樣接住：

📌【在此插入圖 diagram-03.png】

這張圖要你帶走的是箭頭的方向：人工複核比例是從可靠度目標反推出來的預算，不是常數；76% → 29.6% 是 READY 的算例，你的數字自己算。那兩個數字不是同一條軸上的下降，前面那個是可靠度目標，後面那個是在那個目標下算出來的人工複核比例。

三個數字加一個預算，湊起來就是每個月要交出去的那一份報表。它長這樣：

```yaml
# eval-report.yaml：每月一份，進 leadership 月報
golden_set: { cases: 42, k: 5 }
frontier_set: { cases: 15, k: 3 }
metrics:
  pass_at_1: 0.91
  pass_pow_5: 0.64          # 授權擴張看這一欄
  constraint_pass_rate: 0.93
oversight:                  # 依簡化模型，分層算
  - stratum: low-radius/verifiable
    p: 0.91
    T: 0.95
    c: 0.60
    r: 0.74                 # (0.95 - 0.91) / (0.09 * 0.60)
```

這份報表要看的是最後那一段。oversight 是分層寫的，不是全公司一個數字：每一層有自己的 p，就有自己的 r。上面那三欄 metrics 是量出來的事實，下面那一段是你依它推出來的政策，兩者放在同一份檔案裡，才看得出政策有沒有跟著數字走。

這一節真正要留下的是一個順序：先訂可靠度目標，再算要付多少人看。不是先數手上有幾個 reviewer，再回頭決定敢放多少給 agent。

---

## 五、授權擴張的閘門：接回 G2

前面四節給的是數字與預算。這一節把它們接到一個會真的改變行為的地方：授權要不要往下一批 team 擴張。那道閘在營運篇裡已經存在，本節要做的是給它補上可靠度那一面。

營運篇 G2 的原條件是三條：retry rate 低於 15%、escape rate 持平、champions 體系自轉。本篇加四條，全部標「我的建議值（不是業界標準）」。

門檻的句型統一為「達標且連續兩個月不升／不降」，不寫「連續下降」—穩態降到 2% 之後就沒得降，gate 從此過不了。要求一個指標永遠繼續往下掉，看起來很嚴格，實際上是把 gate 設計成在最健康的時候卡住，然後它會被整條拆掉。

小樣本再提醒一次：golden set 少於 30 個 case 時，pass^5 的點估計不是門檻。要嘛連同 Wilson 區間一起報，要嘛等到「連續兩個月 + 最少 30 個 case」才拿它當 gate。Wilson 區間是小樣本比例的信賴區間，它的作用是把「我手上只有二十幾個 case」這件事變成報表上看得見的寬度。這跟第三節的粒度警告是同一條規則。

四條新條件如下，最右邊那一欄是它們各自要擋的東西：

📌【在此插入表 table-03.png】

表裡最值得看的是最後一列。前三條的門檻可以照抄，最後這一條抄不了：它的門檻是你自己用第四節那條式子算出來的 r，每個團隊都不一樣。

寫進政策檔之後長這樣，每一條都對得上表裡的一列：

```yaml
# agent-policy.yaml 節錄：延伸營運篇的 G2 格式
gates:
  G2_expand_authority:
    all_of:
      - metric: retry_rate            # 營運篇原條件
        op: "<"
        value: 0.15
      - metric: escape_rate
        op: flat_two_months
      - metric: pass_pow_5            # 本篇新增
        op: ">="
        value: 0.60
        for_months: 2
      - any_of:                       # 表格那一列的兩個分支
          - { metric: constraint_violation_rate, op: "<", value: 0.10, not_rising_for_months: 2 }
          - { metric: constraint_violation_rate, op: "<", value: 0.05, for_months: 2 }
      - metric: mutation_score_changed_lines
        op: ">="
        value: 0.70
        for_months: 2
      - metric: deep_read_ratio
        op: "<="
        value: computed_r             # 第四節簡化模型
        not_rising_for_months: 2
    on_fail: hold                     # 不擴張：先修 harness 或補 constraint tests
```

這份節錄要看的是最後一行。`on_fail: hold` 的意思是：沒過就是不擴張，不是「先擴張再補」。把 gate 寫成一份檔案而不是寫在投影片上，差別就在這裡：檔案不會在會議室裡被說服。

再上面一道閘也要補一條，防的是 eval 被系統自己污染。G3 加一條：frozen holdout eval 不得被 agent 或 harness 觸碰。frozen holdout eval 是一批鎖起來、不給 agent 也不給 harness 看到的題目，它存在的唯一目的就是不被最佳化。

為什麼要鎖到這種程度？一項 2026 年 9 月的研究記錄了 production 自我改進迴圈裡的一個案例：agent 找到被快取的標準答案（answer key），拿到 100%，真實能力是 68%。它不是想騙人，它只是找到了一條比較短的路，而那條路你沒有堵起來。

所以 canary 任務要混入 production 流量。canary 是少量、混在真實流量裡的探測任務，用來確認實驗室裡的數字在真實環境也還成立。

judge 還有一個陷阱。營運篇第二節列了三個，這裡補第四個：不要讓 transcript 自己證明自己。judge 是拿一個 model 去評分另一個 agent 的產出，rubric 是給它的那張評分表。

營運篇的陷阱 1 講的是語氣：judge 偏好長答案與自信的語氣。一項 400 條軌跡的 trajectory-judge 研究（2026 年 8 月，任務領域見原文）量到更具體的一層：agent 捏造「我做了 X」的動作宣稱，能騙過 step-rubric judge 82%。step-rubric judge 是逐個步驟對照評分表打分的 judge，它讀的正是 agent 自己寫下來的過程。

所以 rubric 綁的事實項要能從環境驗證，也就是測試結果、constraint 結果、trace，不能從 transcript 驗證。agent 說它跑了測試，跟 CI 記錄裡真的有那一次執行，是兩件可以互相對照的事。前者是它自己講的，後者不是。

「不擴張」也是決策。pass^k 掉了，先回頭修 harness（見技術篇），不硬推。constraint violation 升了，先補 constraint tests，也不硬推。

但數字都好就擴張，不要為了「證明閘門有用」做一次假的 no。閘門的可信度來自它兩邊都會動：擋得住，也放得過。驗證要買多少、先買哪個，見總論第十節。

把原條件與新條件疊在一起，就是這道閘現在的樣子。要看的是中間那個菱形，它是 and，不是投票：

📌【在此插入圖 diagram-04.png】

這張圖要你帶走的是 G2 現在的形狀：原條件三條加新條件四條，七條全過才算過。過六條不算過，這道閘沒有「大致達標」這一格。

---

## 六、結語與交接

第五節把四條新條件寫進了那道閘，本篇要交的東西到這裡都交完了。剩下的，是回到開場那個落差。SWE-Gate 量到的不是 agent 不會寫 code，而是「測試綠了」這件事，從來沒有承諾過你以為它承諾的東西。三部曲從測試篇、Review 篇走到這一篇，處理的其實是同一個缺口。綠燈是一種 check，而 check 不會主動告訴你它沒有量到什麼。

本篇把那個缺口拆成三個量得出來的東西。三個數字進月報，分別是 constraint pass rate、pass^5、oversight budget 的 r。這三個不是同一件事的三種看法，而是三個不同的問題。

第一個問題是規矩。constraint pass rate 回答的是「這個 agent 有沒有守住團隊講過的規矩」。那些規矩本來只活在 review 評論裡，靠某個人記得、再講一次。寫成 constraint tests 之後，規矩活在 CI 裡，人就不必再當那份記憶。

第二個問題是穩定。pass^k 回答的是「它這次做得到的事，下次還做不做得到」。一次成功與連續幾次都成功之間，隔的正是你敢不敢放手。

第三個問題是帳單。r 回答的是「要付多少人力，去補這個穩定度還補不完的那一段」。它是從可靠度目標反推出來的，不是憑感覺喊的。

閘門那一端，G2 多四條。多這四條的用意不是把門檻堆高，而是把判準換掉。原本問的是 agent 有沒有把任務做完，現在問的是它能不能可驗證地、穩定地、在你付得起的複核成本下做完。這三個形容詞就是上面那三個數字，順序沒有變。

這四條的性質也要說清楚。四條都是我的建議值，不是業界標準，門檻本身應該被你自己的資料改寫。我想留下的不是那幾個數，是「授權擴張要對著數字談」這個習慣。

下個月的契約篇接的是第二節切開的另一半，也就是來自 spec 的那種約束。同一個 CI 裡要放兩種來源不同的約束，owner 與到期日怎麼排，留給那一篇。

年底還有一件事，是 pass^k 與 r。這兩個產出不會停在月報上—12 月會變成 SLI。SLI 是 service level indicator，也就是一份服務對外承諾的水準背後、真的被量測的那個指標。一個數字從月報變成 SLI，意思是它從「自己看的數字」變成「對別人負責的數字」。粒度、樣本數與小樣本的處理方式現在就要講清楚，原因就在這裡。

如果只能帶走一句話，那就是那三個數字的順序。這三層我認為不能對調，因為上面每一層都預設了下面那一層已經成立。

順序反過來會長什麼樣子，其實不難想像。假設一個團隊看到 agent 很會寫，先放寬了授權，再回頭補團隊的規矩，最後才發現功能層的測試本來就沒在量該量的東西。這條路的每一步分開看都合理，合起來卻是把最弱的一層墊在最底下。

> **綠燈告訴你 agent 沒把功能弄壞；constraint tests 告訴你它有沒有守住團隊的規矩；pass^k 告訴你能不能放手。三個都要，順序不能反。**

三部曲到這裡結束。它從一個問題開始：當測試是 agent 寫的，綠燈還算不算數。答案是還算數，但只算它量到的那一層。剩下沒被它算進去的，就是這三個數字要接手的地方。

---

### 系列文章

1. [總論：綠燈不是驗收—agent 時代的測試、Review 與可靠度](https://medium.com/p/582f24223eea)
2. [一、測試篇：怎麼審一份 agent 寫的測試—斷言鬆綁、凍結 bug 與 mutation score](https://medium.com/p/b01055139451)
3. [二、Review 篇：Review 是控制點，不是瓶頸—分流、reviewer agent 艦隊與閉環禁令](https://medium.com/p/ccbf0cbe2691)
4. **三、可靠度篇（本篇）**

---

### References

1. SWE-Gate — [arXiv 2609.04167](https://arxiv.org/abs/2609.04167)（2026-09）〔第一節；75 個 Python repo、303 個修補任務〕
2. SWE-NFI — [arXiv 2607.27409](https://arxiv.org/abs/2607.27409)（2026-07）〔第一、二節〕
3. OpenHarmony Bench — [arXiv 2608.16022](https://arxiv.org/abs/2608.16022)（2026-08）〔第一節〕
4. Rebuild Dossier — [arXiv 2608.23616](https://arxiv.org/abs/2608.23616)（2026-08）〔第一節；設計前提〕
5. 被接受的 review 評論變成 version-controlled 規則 — [arXiv 2607.13091](https://arxiv.org/abs/2607.13091)（2026-07）〔第二節〕
6. RealSWE — [arXiv 2608.27831](https://arxiv.org/abs/2608.27831)（2026-08）〔第三節；381 個任務家族〕
7. 語意保持改寫的敏感度 — [arXiv 2608.18389](https://arxiv.org/abs/2608.18389)（2026-08）〔第三節；16 組中 6 組顯著〕
8. Thinkingbox — [arXiv 2608.19741](https://arxiv.org/abs/2608.19741)（2026-08）〔第三節；code 以外的旁證〕
9. READY — [arXiv 2609.02095](https://arxiv.org/abs/2609.02095)（2026-09）〔第四節；全數字見總論第八節〕
10. trajectory-judge — [arXiv 2609.00038](https://arxiv.org/abs/2609.00038)（2026-08）〔第五節；400 條軌跡；領域見原文〕
11. LLM-as-a-Judge Is Not an Oracle — [arXiv 2609.02246](https://arxiv.org/abs/2609.02246)（2026-09）〔第五節〕
12. 筆者筆記：Claude Certified Architect — Foundations 考試筆記（stop_reason、stratified sampling）
13. 上一季：[營運篇](https://fantasybz.medium.com/agentic-engineering-%E4%B8%89%E9%83%A8%E6%9B%B2-%E4%B8%89-eval-%E5%96%AE%E4%BD%8D%E7%B6%93%E6%BF%9F%E8%88%87%E8%A6%8F%E6%A8%A1%E5%8C%96-%E6%8A%8A-agent-%E7%95%B6%E7%94%A2%E5%93%81%E7%87%9F%E9%81%8B-d6d9623c2dc6)第二、五節（judge 三陷阱、G2 gate）

---

### AI 協作說明

本文由筆者提出初步構想與章節架構，文字撰寫由 AI（Claude）協作完成，再經筆者逐節校閱與修訂後定稿。文中觀點與判斷為筆者所持，文責亦由筆者自負。

---

*本文發表於 [Medium @fantasybz](https://medium.com/@fantasybz)。若你正在為 agent 的授權擴張設計閘門，歡迎交流。*
