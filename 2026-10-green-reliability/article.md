# 綠燈不是驗收（三）可靠度篇：SWE-Gate 量測到的 34%—constraint tests、pass^k 與授權擴張的閘門

> **TL;DR** — 四部曲第三篇討論 reliability gate：授權要不要擴張，該依據什麼判斷。SWE-Gate 在 75 個 Python repo、303 個修補任務上量測到：功能測試通過的 644 個修補裡，有 221 個（34%）違反 reviewer 實際加過的約束。這個落差帶出本篇的三項指標。**constraint pass rate**：在功能測試通過的 PR 中，統計 constraint tests 也全過的比例。**pass^k**：統計同一組任務中，k 次執行全部通過的 case 比例，與單次嘗試的成功率 pass@1 分開呈現。**oversight budget**：READY 的案例裡，兩個準確率只差 0.3 個百分點的系統，人工複核需求卻差近 10 個百分點；這來自臨床稽核，不能直接當成程式碼複核的人力估計。本篇借用從可靠度目標反推人力的概念，用簡化模型估算所需複核下限，再對照實際安排與可負擔預算。這些結果連同測試保護力與既有營運條件，納入 leadership 月報與 G2 的授權判斷，不靠 pass@1 單獨決定。

> 系列導覽：[總論](https://medium.com/p/582f24223eea) → [一、測試篇](https://medium.com/p/b01055139451) → [二、Review 篇](https://medium.com/p/ccbf0cbe2691) → **三、可靠度篇（本篇）** → 四、付款實作篇（草稿完成，尚未排程）

---

## 一、SWE-Gate 量測到的 34%

總論第三節把綠燈無法涵蓋的問題拆成三層。這一篇先接著談其中一層：「功能測試通過，不等於滿足了團隊的約束」。當 reviewer 已經提醒過的要求，沒有被寫進功能測試裡，綠燈就回答不了那些問題。總論引用的那組數字，正好讓這個落差有了具體的樣子。SWE-Gate 是一份 benchmark 論文，量測的就是綠燈到底涵蓋了什麼。它多做了一件事：不只問「功能測試過了沒」，還把 reviewer 當初真的在 PR 上提出過的要求整理出來，寫成可執行的檢查，與功能測試分開執行。

34% 是 SWE-Gate（2026 年 9 月）在 75 個 Python repo、303 個修補任務上量測到的。644 個通過功能測試的修補裡，221 個違反了那些約束。用白話講就是：每三個綠燈修補，就有一個違反了 reviewer 在乎的約束。

讀這組數字時，有兩個地方需要先釐清，才不會把研究的結論用錯。

領域邊界要先說清楚—Python repo、修補任務，不是「所有 agent PR」。它量測的是這個範圍內的表現。換一種語言、換一種任務型態，就需要重新量測。

分母也要看清楚。分母是「通過功能測試的修補」，所以正確的白話是「每三個綠燈修補就有一個違反約束」。**不是**「綠燈量不到 reviewer 在乎的三分之一」。後者把單位換成了「reviewer 在乎的事」的比例，論文沒有量測這個比例。兩句話字面很像，但分母不同，拿錯的那句去說服人，會在第一個追問就垮掉。

要理解這個落差，可以再把「通過」拆開來看：build 成功、功能正確與非功能要求滿足，是不同的判斷。下面兩份 benchmark 分別量測其中的落差，第三份流程設計論文則提醒，這些判斷共同依賴什麼前提。

SWE-NFI（188 個任務、92 條可執行規則）量測的是「功能過，不等於非功能規則滿足」：最佳 agent 的功能通過率是 70.0%，非功能規則的表現仍普遍不及。非功能規則包含效能、安全、log 格式等要求；如果功能測試沒有納入這些條件，測試通過就回答不了它們。

OpenHarmony Bench（153 個 app 任務）量測的是更下面一層，「**build 綠，不等於行為對**」：可建置 94.77% 到 100%，行為正確只有 48.36% 到 58.39%。落差大得多，但行為錯誤本來就是功能測試該抓的事，不在 34% 那一層。

Rebuild Dossier 則是設計前提，不是觀察到的實證。它是一篇論文，提的是讓 agent 重建整個 app 時該走的流程：當 agent 有機會 game 測試時，測試套件全過不等於正確，所以它先鎖定介面，每次只處理一個測試。它給的不是一個數字，是一句提醒：只要 agent 能同時改實作與改測試，測試全過就不再是獨立的證據。

分層之後會看到一件事：這三層在儀表板上長得一模一樣，燈都是綠的。差別在於那盞燈檢查了哪些事，以及團隊有沒有為其餘的問題建立量測。綠燈不會告訴你它沒有涵蓋什麼，這正是它最危險的地方。

本篇只處理兩層。一層是 reviewer 約束，也就是開場那個數字量測到的；另一層是可靠度，也就是同一件事再做一次還對不對。可靠度這一層，上面三份研究都沒有量測，第三節會說明如何在自己的系統上量測，而且只採用 Rebuild Dossier 提醒的那種獨立證據。以下從把約束寫成檢查開始，接著把能力與可靠度分開量測，再估算人工複核所需的投入，一路推到授權擴張的那道閘門。

---

## 二、把 review 約束寫成可執行的 constraint tests

上一節說，SWE-Gate 量測到約三分之一的綠燈修補違反 reviewer 在乎的約束。這一節做的是最直接的回應：把值得保留的要求寫成 CI 能執行的 constraint tests。這個名稱描述測試的來源與保護責任，不是與功能測試互斥的技術分類。「同一筆付款不得重複扣款」既是功能行為，也可以是 reviewer 決定長期維護的約束；unit test 或 integration test 都能用來驗證它。

約束長什麼樣？先把它想成團隊反覆講過、但不該每次都靠人記得的那些話。以下七類用來示範如何把 review 要求整理成 constraint tests，不是一份完整的分類法。SWE-NFI 的 92 條規則與 SWE-Gate 的評論分類，以論文原文為準：

| 類別 | 例子 | 檢查方式 |
|---|---|---|
| 依賴 | 不得新增套件 | lockfile diff |
| API 表面 | 不得新增 public 符號 | AST 比對 export |
| 重用 | 必須用既有的 helper 或 retry wrapper | AST 掃描直接建構 |
| 效能 | 不得在 loop 裡打 DB | AST 或 lint 規則 |
| 可觀測 | log 格式、error code | schema 檢查 |
| 安全 | 不得寫入 env、不得關 TLS 驗證 | AST 與 secret scan |
| 架構規則 | 層依賴方向；aggregate 必須繼承 EventSourcedAggregate | import graph、繼承檢查 |

表裡最值得看的是最右邊那一欄：lockfile diff、AST（程式碼的語法樹）掃描、import graph，都能先從既有工具做起。但每個例子仍要定義檢查範圍；像「不得在 loop 裡打 DB」，靜態規則能辨識部分寫法，不代表能涵蓋所有間接呼叫。先說清楚能檢查什麼，才知道剩下的問題要留給誰。

整條流程是四步：review 評論 → 規則 → constraint test → CI。規則檔的做法借自 2026 年 7 月一篇研究：把被接受的 review 評論納入版本控制，供後續工作參考，Review 篇第三節用的是同一份研究。實作成 constraint tests 之前，還要確認評論是通則還是單次例外，以及能否寫成穩定的檢查；被接受過，不代表適用範圍從此不必再問。

規則檔要記兩種東西。第一種是來歷，每條規則記來源 PR 與日期，半年沒觸發的規則要 review 是否已經過期。第二種是責任，也就是再加兩個欄位：owner（誰維護這條規則）與 expiry（到期 review 的日期）。一條規則即使曾經有用，沒有人維護、沒有重新檢視的時間，也會慢慢過時。這兩欄讓團隊知道，到時候該由誰回來確認。

這裡的「半年」是安排重新檢視的提醒，不是刪除規則的理由。付款安全約束可能正因持續有效，才很久沒有失敗；是否保留，仍要回到業務契約、實作與風險是否改變來判斷。

規則有了主人，下一個問題是 agent 能不能改它。總論第二節把證據分成三類：第一類是 agent 自己說的，第二類是 agent 自己寫的測試，第三類是 agent 改不動的測試。這裡要落地的是第三類，機制有三道。

CODEOWNERS 指定檔案的審查責任，但要搭配合併規則才會強制執行。第一道，`tests/constraints/` 與 golden set（團隊挑選的驗收案例，第三節定義）只指定人類 owner，並啟用 Require review from Code Owners。第二道，規則檔、CODEOWNERS 與驗證 workflow 的變更同樣需要人類核准，agent 不得繞過規則。第三道，對第三類測試的任何斷言弱化，由測試篇的 Check 2 直接阻擋。

agent 可以在分支上提出修改，卻不能自行核准並合併。評估 PR 時，還要從受保護的版本取得約束與驗證程式，再用它們檢查候選程式碼；不能讓 PR 先改掉檢查器，再拿新檢查器的綠燈證明自己合規。這才是「改不動」需要保護的關係。

用一條示範的 review 評論，看看這四步如何串起來；下列 PR 編號、日期與帳號也都是示例。Before 是每次都要人重講的那句評論：「請不要在這裡直接 new HttpClient，用 `clients.http()`」，它每次只審一個 PR，講完就沒了。After 則把這句評論變成三項安排：由 CI 執行檢查、指定規則的維護者，再用權限設定限制誰能核准修改。

第一樣是測試檔。下面是最小示意，只檢查修改過的 Python 檔案中直接呼叫 `HttpClient(...)` 的寫法，未涵蓋別名、屬性呼叫或動態建立。正式導入還要處理刪檔、git 指令失敗與 diff 基準，不能把這段示意當成完整的安全邊界：

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

第三樣是 CODEOWNERS 的節錄。它指定誰負責審查這幾個目錄與規則檔；要限制合併，仍需啟用前面說的規則，並另外保護 CODEOWNERS 與驗證 workflow：

```text
# CODEOWNERS
/tests/constraints/   @acme/platform-humans
/tests/golden/        @acme/platform-humans
/rules.md             @acme/platform-humans
```

三樣加起來，那句 review 評論就從「每次都要人講」變成「講一次，之後每個 PR 都被檢查一次」。這就是複利的意思：人讀 diff 講的一條評論只審這一個 PR，回收成 constraint test 之後，這次 review 留下的經驗，就能繼續檢查之後每一個 PR。

這筆複利仍然有成本，而且要看約束怎麼檢查。像上面的 AST 規則，可以直接分析選定的檔案，不必執行整套產品測試；若要驗證效能或實際行為，就可能需要另外準備環境與測試。「觸及範圍」也要依檢查器的實作確認：它讀取整個 diff，不代表每一項要求都已被驗證。

因此，我把能用靜態規則檢查的 constraint tests，放在 brownfield 導入順序的前面。brownfield 指的是已經運作多年、測試與文件可能都不完整的既有系統。這類規則提供了一個起點：即使還沒有完整的測試套件，也能先檢查幾項明確的團隊要求。

那還沒有 review 歷史的團隊怎麼起步？沒有 review 歷史，就從團隊規範與最近五個 incident 出發，把那幾句「不要再犯一次」先寫成 check。

把評論 → 規則 → 測試 → CI 這四步畫成一張圖，要看的不是左邊那條主線，是右邊那條回頭的虛線：

```mermaid
---
config:
  theme: base
  themeVariables:
    fontSize: 16px
    primaryColor: "#f8f9fa"
    primaryTextColor: "#1f2933"
    primaryBorderColor: "#6b7280"
    lineColor: "#6b7280"
    secondaryColor: "#f8f9fa"
    tertiaryColor: "#ffffff"
    clusterBkg: "#ffffff"
    clusterBorder: "#9ca3af"
    edgeLabelBackground: "#ffffff"
  flowchart:
    nodeSpacing: 36
    rankSpacing: 44
    padding: 12
    htmlLabels: true
    subGraphTitleMargin:
      top: 8
      bottom: 12
    curve: basis
---
flowchart TB
    classDef own fill:#d4edda,stroke:#2e7d32,color:#1f2933
    classDef buy fill:#fff3cd,stroke:#b8860b,color:#1f2933
    classDef bad fill:#ffe0e0,stroke:#c0392b,color:#1f2933
    classDef human fill:#e3f2fd,stroke:#1565c0,color:#1f2933
    A["review 評論<br/>「用 clients.http()，<br/>不要直接 new HttpClient」"] --> B["規則檔 rules.md<br/>來源 PR、日期、對應測試檔<br/>變更需人類 approve"]
    E["CI 顯示半年沒觸發的規則<br/>review 是否已過期，刪或留"] -.->|過期回路| B
    B --> C["constraint test<br/>AST 掃描 agent 改動的檔案<br/>目錄在 CODEOWNERS 只列人類"]
    C --> D["CI：功能測試之外<br/>多一欄 constraint pass rate"]
    class A human
    class C,D own
    class E buy
```

圖中的虛線讓規則有機會回到人的手上重新檢視。兩年後，原本禁止的做法可能已經有了新的實作方式；若只留下 failed check，卻找不到當初的理由與負責人，接手的人就很難判斷該修程式還是修規則。expiry 要保留的，是這個重新確認的機會。

**再看一條需要執行行為的付款約束。** 假設示範訂單是一瓶 35 元的無糖純喫綠茶，reviewer 提醒：「畫面逾時時，金流可能已經扣款；重送不能直接開始另一筆。」團隊確認要求後，保留來源、payment owner、適用的重送情境，以及 provider 契約改變時重新檢視的條件。這些評論與價格都是教學設定，不是實際事故或商品售價。

這條規則不能只靠掃描有沒有 `PENDING` 字串來驗證。隨文 [付款範例](https://github.com/fantasybz/medium-articles/tree/main/examples/tea_payment) 讓 `FakeGateway` 在記錄成功扣款後拋出逾時，再透過 `Checkout.pay()` 重送同一張訂單與 key。測試同時確認結果維持 `PENDING`、沒有 payment ID，且金流呼叫與成功扣款都只有一筆。替身刻意不幫忙去重，才不會掩蓋應用程式缺少 guard 的錯誤。完整測試另外涵蓋扣款前逾時及其他連線例外。

從 Review 挑出它的理由，是後果明確、預期結果可判定、需求會延續到後續修改，而且有人維護。命名偏好不必各建一個行為測試；尚未決定的退款政策，則要先確認需求。第四篇〈付款實作篇〉草稿把這些選擇、九個付款測試與七個指定 mutant 完整接起來，尚未設定發布日期。

這裡也要守住量測的分母。完整測試辨識出 7／7 個指定變異，是這份測試套件在本例範圍內的 mutation score；不是 agent 的 constraint pass rate，也不是 pass^k。前者要統計多個功能檢查通過的候選修補，有多少也通過全部適用約束；後者要對固定任務進行多次獨立的 agent 嘗試。同一份 unittest 重跑五次，不能代替下一節要量測的五次 agent 成果。

這裡也要區分約束的來源。本篇主要從 **review 歷史** 回收經驗：某個問題發生過，團隊決定把相關要求留下來。另一種來源是 **spec**，也就是實作開始前就約定的規格契約。兩者都能寫成檢查，但重新檢視時要回到各自的依據。

review 約束由提出要求的團隊維護，到期時確認理由是否仍然成立；spec 約束則要由負責規格的人，隨需求變更一併檢視。寫進同一個 CI，不代表它們可以失去來源與 owner。這些資訊保留下來，規則才有辦法更新，也才有人能解釋為什麼繼續保留。

---

## 三、可靠度不是能力：pass@1 與 pass^k

上一節處理的是「有沒有守住規矩」。這一節處理另一件事：同一件事再做一次，它還會做對嗎。能力與可靠度是兩個數字，很多團隊把它們混成一個，所以先把各自的定義說清楚。

定義沿用總論第八節：golden set 的每個 case 執行 k 次。這是一批由團隊選定的代表性驗收案例。每次都從相同初始狀態獨立執行，固定 model、harness 版本與評分規則；跨月比較時也要記錄案例版本，才知道差異來自哪裡。

**pass@1 是單次嘗試的成功率，用 k 次重複執行的結果估算。** 每個 case 是 k 次裡過的次數除以 k。它回答的問題是：這件事它平均做得到嗎。

**pass^k 是 k 次全部成功的 case 比例。** 一個 case 只要有一次沒過，就不計入全過的 case。它描述這批案例在這 k 次執行中的一致性，不是保證下一次一定成功。

先保留每個 case 的結果，再計算整體指標。每個 case 執行次數相同時，pass@1 的逐案平均與把所有 run 合併計算會相同；但 pass^k 必須知道哪些成功與失敗屬於同一個 case。只留下總成功次數，就無法區分「少數 case 每次失敗」與「各個 case 偶爾失敗」，也就不知道該先修哪一類問題。

還有一個長得很像的符號，先排除掉：「至少一次成功的比例」是 pass@k，是另一個數字，本系列不用。

pass^k 之外，月報還有 constraint pass rate：功能測試通過的 PR 裡，constraint tests 也全過的比例。共同前提是：**pass^k 與 constraint pass rate 只能從第三類證據算出**，也就是團隊維護、不能由受檢 agent 自行改寫後放行的測試。agent 的結案報告不算數；它新寫的測試，則要先通過 test gate、經人類核准進 main，並納入受保護的驗證流程，才完成總論所說的升格。

我準備 Anthropic 的 Claude Certified Architect 認證考試時，筆記裡有一個很小的例子：不能用 assistant 的回答文字去猜 agent 的 loop 是否結束，要看 stop_reason（API 回傳裡由系統填的「為什麼停下來」欄位）。回答文字是模型自己講的，stop_reason 是系統記錄的，兩者不同源。放到程式碼驗收上，道理一樣：agent 說「測試都過了」是它自己講的，CI 的紅綠是系統記錄的。這也是第一類陳述需要被核對，不能單獨拿來驗收的理由。

為什麼不能只成功一次就放心？一次執行看不到重跑的一致性，也看不到條件改變後的敏感度。這是兩個需要分開量測的問題。下面兩篇研究談的是「同一個任務換個說法」，不是固定 prompt 下的重跑變異。

RealSWE（381 個任務家族）量測到的是：同一個任務換個說法，成績平均掉 6.4 個百分點，而且會重排 model 的名次。名次會被重排這件事，比掉幾個百分點更麻煩。它代表你看到的排行榜有一部分是題目怎麼寫出來的，不是 model 本身的差距。

另一篇語意保持的改寫研究量測到的幅度接近：平均最多掉 6.7 個百分點，**但 16 組 model 與 scaffold 的組合裡只有 6 組達到統計顯著。** 所以正確的讀法不是「所有 model 都一樣不穩」，而是效應真實但不均勻。你那一組穩不穩，需要針對自己的組合實際量測。

換個說法就改變結果，提醒我們還要評估輸入變動下的穩定性；固定條件重跑得到的 pass^k，則回答另一個問題。這兩種實驗可以並列，但不能把前者的效應當成後者已被量測的結果。

旁證來自 code 以外，這裡是全系列唯一引全數字的地方。Thinkingbox 這份 benchmark 評測的是 507 個 policy-conditioned MCP 工作流，也就是帶著政策約束的多步驟工具呼叫任務：agent 要一邊透過 MCP（串接工具的協定）呼叫工具，一邊守住規則。在這批任務上，Claude Opus 5 的 pass@1 是 66.50%，pass^20 是 47.53%。

單看平均成功率，會覺得它大約有三分之二的機會做對，但能連續二十次都做對的任務不到一半。這中間差了將近二十個百分點，那就是「能力」與「可靠度」的距離。

它的結論「clean termination 與 valid tool calls 不是完成的代理指標」，在 code 領域同樣成立：agent 說它已經執行完任務、工具呼叫也都合法，跟任務有沒有做對是兩件事。

那在自己的 eval 上怎麼做？沿用〈Agentic Engineering：Eval、單位經濟與規模化〉營運篇的 golden set，20 到 50 個 case，每月重複執行 k = 5 次，門檻看的是這一組。frontier set 另外執行 k = 3 次：它是另一批更難、目前還過不了的 case，用來觀察目前的能力上限，不拿來當門檻。月報的量測固定三欄，每個月看同一組數字。開場提到的 oversight budget 另外列示：以第一欄的成功率為輸入，再加入可靠度目標與複核效果，估算所需比例，並對照實際複核與人力上限。第四節會把這筆帳算清楚。

三欄長這樣：

| 欄 | 定義 | 從哪裡算 |
|---|---|---|
| pass@1 | 單次嘗試的成功率，用 k 次重複跑估：每個 case 過的次數除以 k，再對 golden set 平均 | 第三類證據 |
| pass^5 | 5 次全過的 case 比例 | 第三類證據 |
| constraint pass rate | 功能測試通過的 PR 中，constraint tests 全過的比例 | tests/constraints/ |

表裡最重要的是最右邊那一欄：三個數字的來源全是團隊自己擁有的東西。哪一欄填不出這個來源，那一欄就不該進月報。

**我的建議值（不是業界標準）**：k = 5，pass^5 ≥ 60%，作為低 blast radius 任務評估授權擴張的其中一項條件。它不能單獨放行；還要滿足第五節的其他條件與人工核准要求。低 blast radius 指的是失敗影響受限、能妥善復原的任務，不是單憑「內部工具」這個名稱判定。

**粒度警告**：golden set 少於 30 個 case 時，pass^k 只報趨勢，不當門檻。20 個 case 的粒度是 5 個百分點，一個 case 翻轉就會從 65% 掉到 60%。依本篇的建議，必須至少 30 個 case、連續兩個月達標，才用來判斷授權；單純延長觀察月份，不能取代最少案例數。

把三個 case 攤開算一次，兩個數字的差別就看得見了。要看的是中間那個 case B，它只錯一次：

```mermaid
---
config:
  theme: base
  themeVariables:
    fontSize: 16px
    primaryColor: "#f8f9fa"
    primaryTextColor: "#1f2933"
    primaryBorderColor: "#6b7280"
    lineColor: "#6b7280"
    secondaryColor: "#f8f9fa"
    tertiaryColor: "#ffffff"
    clusterBkg: "#ffffff"
    clusterBorder: "#9ca3af"
    edgeLabelBackground: "#ffffff"
  flowchart:
    nodeSpacing: 36
    rankSpacing: 44
    padding: 12
    htmlLabels: true
    subGraphTitleMargin:
      top: 8
      bottom: 12
    curve: basis
---
flowchart TB
    classDef own fill:#d4edda,stroke:#2e7d32,color:#1f2933
    classDef buy fill:#fff3cd,stroke:#b8860b,color:#1f2933
    classDef bad fill:#ffe0e0,stroke:#c0392b,color:#1f2933
    classDef human fill:#e3f2fd,stroke:#1565c0,color:#1f2933
    G["golden set：3 個 case<br/>各跑 k = 5<br/>先 per case 算，再取平均"]
    G --> A["case A<br/>5 次全過<br/>pass@1 = 100%，pass^5 = 1"]
    G --> B["case B<br/>4 過 1 紅<br/>pass@1 = 80%，pass^5 = 0"]
    G --> Cc["case C<br/>5 次全過<br/>pass@1 = 100%，pass^5 = 1"]
    A & B & Cc --> P1["golden set pass@1<br/>= (100 + 80 + 100) / 3 = 93%"]
    A & B & Cc --> P5["golden set pass^5<br/>= 2 / 3 = 67%"]
    P1 & P5 --> D["授權擴張看 pass^5<br/>不看 pass@1<br/>G2 條件見第五節"]
    class B bad
    class A,Cc own
    class P5,D buy
```

圖中的同一批 golden case，得到 pass@1 93% 與 pass^5 67%。前者呈現平均每次嘗試的表現，後者則指出有多少 case 在五次執行中都沒有失敗。把兩者分開，團隊才看得見平均值底下的重複失敗風險；要決定是否放寬授權，還得把約束檢查與人工複核的條件一起放進來。

---

## 四、Oversight budget：READY 與一個簡化模型

當團隊知道 agent 能完成多少任務、結果有多穩定，下一個問題就落到接手的人身上：為了達到承諾的可靠度，還需要複核多少工作？oversight budget 討論的，就是這份人力需求與團隊能持續投入的預算。若只提高可靠度目標，卻沒有確認誰能完成必要的複核，目標就還只是一個數字。

READY（2026 年 9 月）提供了一個值得借用的起點。這套企業 agent 部署資格審查框架，從可靠度目標反推「agent 加人工複核政策」需要的複核比例。在它的案例裡，兩個自主準確率只差 0.3 個百分點的系統，人工複核需求卻差近 10 個百分點，而且準確率較低的系統需要的複核較少。這個結果提醒我：**只按準確率排序，還不知道團隊要負擔多少複核工作。**

這裡借的是概念，不移植數字。READY 的案例來自臨床稽核工作流，不是 code；它依系統與複核政策估計人工需求。下面的模型只示範如何連結準確率、複核效果與可靠度目標，不重現 READY 的方法，也不能用來解釋那兩個系統為什麼排名翻轉。全數字與領域說明在總論第八節。

**我的簡化模型（不是 READY 的方法）**，先作三個假設：在同一分層內隨機抽樣深讀；被發現的錯誤能在放行前成功修正；複核不會把原本正確的結果改錯。若 p 是深讀前的成功率、r 是深讀比例、c 是深讀後成功修正原有錯誤的機率，複核後的成功率就是 p + (1 − p) · r · c。要達到 T，得到：

> r ≥ (T − p) / ((1 − p) · c)

右邊算出的是所需複核比例的下限，以下稱為 r_min；實際安排的 r 不能低於它。若 T 已不高於 p，模型不要求額外深讀，但人類核准仍然保留。若結果大於 1，全部深讀也不夠；若 c 為 0 且目標仍有缺口，這個模型就無法靠複核達標。三個輸入分別是：

- **p**：該分層在 golden set 上的 **pass@1**，用來估計深讀前的單次成功率。案例必須能代表要放行的任務；若 golden set 與實際工作差異太大，代入公式也不會得到可信的預算。pass^k 留給第五節的授權判斷，不進這條式子。
- **T**：該 blast-radius 層的可靠度目標，也就是 Review 篇分流矩陣的哪一格；那張矩陣依 blast radius 與可驗證程度，決定一個 PR 要審多深。改到 auth 或 schema 跟改內部工具，目標不會一樣。
- **c**：有錯誤的 PR 被抽中深讀後，錯誤能被辨識並成功修正的機率。只發現、沒有修正，不足以提高這個模型裡的成功率。

c 最難估，也不能用「reviewer 很資深」代替。可先從有明確後續結果的深讀紀錄，核對哪些錯誤被發現並成功修正，再追蹤漏掉的錯誤。紀錄仍可能漏掉尚未曝光的缺陷，所以這只是估計。沒有歷史時，0.6 只作為試算假設，每月校正；不能把它當成已量測的抓錯能力來核准擴張。

測試篇的研究也提醒我，不能把人工審閱當成一定能抓錯的安全網：86 位開發者判斷 LLM 寫的斷言，面對錯誤斷言時的判斷準確率是 49%，面對正確斷言則是 74%。這量測的是判斷斷言，不是 PR 複核後成功修正錯誤的機率，因此不能直接代入 c。下面仍以 c = 0.6 作試算假設，用來觀察複核效果如何影響人力需求。

以下三個算例使用示範值，讓公式裡的取捨具體一點。它們要回答的不是「業界都該抽查幾成」，而是在這組假設下，改善系統表現或調整目標，會怎麼改變所需人力。

- p = 0.80、T = 0.95、c = 0.6 → r ≥ (0.95 − 0.80) / (0.20 × 0.6) = 1.25。**全審都不夠**，要先把 p 或 c 拉高。
- p = 0.90、T = 0.95、c = 0.6 → r ≥ (0.95 − 0.90) / (0.10 × 0.6) ≈ 0.8333。準確率從 0.80 拉到 0.90，所需深讀仍超過八成；若以整數百分比排程，至少安排 84%。
- p = 0.90、c = 0.6，把 T 改成 0.92 → r ≥ 0.02 / 0.06 ≈ 0.3333，整數百分比至少安排 34%。這個試算用來呈現目標對人力的影響，不是建議為了少審就降低可靠度承諾。

三個算例先改變 p，再改變 T，讓不同選擇的代價浮現出來。它們沒有證明哪一個輸入永遠最重要；真正要帶回團隊討論的是：目標訂在哪裡、假設是否可信，以及所需人力能不能持續負擔。

算出的 r_min 是 Review 篇抽樣深讀比例的下限。低 radius、可驗證那一格，由非指派者依實際安排的 r 抽樣深讀，且 r ≥ r_min；不是每個 PR 都逐行讀，但每個 PR 仍需人類閱讀報告後 approve。之後還要拿 r_min 與團隊能持續負擔的上限 r_budget 比較，這是第五節的授權條件。

複核比例算出來之後，還要決定從哪些任務抽樣。我的考試筆記提醒過，整體準確率可能掩蓋個別類型的低表現，因此需要 stratified random sampling，也就是分層後再隨機抽樣。放到這裡，同一個 blast-radius 格內，還可以依任務類型、repo 與 agent 版本分層，各自估計 p，避免所有任務共用一個平均值。

例如，整體的 p 看起來不錯，schema migration 的成功率卻偏低。若所有類型都依整體平均值安排複核，這類任務需要的注意力就可能被低估。分層的目的，是讓人力安排跟著各類工作的實際風險走。

下面把估算與執行的順序畫在一起。p 與 c 都需要自己的資料，不能把判斷斷言的 49% 或 74% 直接代入 PR 複核。公式先給出下限，再由團隊安排不少於該下限的分層抽樣：

```mermaid
---
config:
  theme: base
  themeVariables:
    fontSize: 16px
    primaryColor: "#f8f9fa"
    primaryTextColor: "#1f2933"
    primaryBorderColor: "#6b7280"
    lineColor: "#6b7280"
    secondaryColor: "#f8f9fa"
    tertiaryColor: "#ffffff"
    clusterBkg: "#ffffff"
    clusterBorder: "#9ca3af"
    edgeLabelBackground: "#ffffff"
  flowchart:
    nodeSpacing: 36
    rankSpacing: 44
    padding: 12
    htmlLabels: true
    subGraphTitleMargin:
      top: 8
      bottom: 12
    curve: basis
---
flowchart TB
    classDef own fill:#d4edda,stroke:#2e7d32,color:#1f2933
    classDef buy fill:#fff3cd,stroke:#b8860b,color:#1f2933
    classDef bad fill:#ffe0e0,stroke:#c0392b,color:#1f2933
    classDef human fill:#e3f2fd,stroke:#1565c0,color:#1f2933
    I1["p：該分層的 pass@1<br/>golden set，分層算"] --> F["r ≥ (T − p) / ((1 − p) · c)<br/>我的簡化模型<br/>不是 READY 的方法"]
    I2["T：可靠度目標<br/>依 blast radius 分層"] --> F
    I3["c：深讀後成功修正錯誤<br/>需用團隊資料估計"] --> F
    F --> O["需求下限與預算分開<br/>p 0.9、T 0.95、c 0.6<br/>實際深讀至少 84%"]
    O --> S["分層隨機抽樣做深讀<br/>依任務類型／repo／agent 版本<br/>避免 aggregate 掩蓋弱項"]
    class I1,I2,I3 human
    class F,O own
    class S buy
```

依這個順序安排，複核比例就有了可以說明的理由：目標是什麼、資料來自哪裡、估算用了哪些假設。這張圖採用的是我的簡化模型。READY 的 76% → 29.6% 則是另一個例子，分別代表可靠度目標與該設定下所需的人工複核比例；它不是從 76% 掉到 29.6% 的表現變化，也不能拿來替這張圖校準。完整數字與領域說明見總論第八節。

月報接著要把量測與人力安排放在一起。下面是一份格式示範，目的在於讓開會的人能同時看見 agent 的表現、複核需求與實際投入，而不是只收到一個總通過率：

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
    r_min: 0.740741          # required minimum, displayed rounded
    r_budget: 0.80           # illustrative sustainable capacity
    r: 0.75                 # ceil to whole %: (0.95 - 0.91) / (0.09 * 0.60)
```

這份報表的數字都是示範值。上半部列量測欄位，下半部列分層試算：依 p、T、c 算出的 r_min 約為 0.7407，若按整數百分比排程，就向上安排 0.75。月報要把所需比例、實際比例與可負擔上限分開，才能看見人力是否足夠，以及實際複核有沒有做到。

先訂可靠度目標、估算需要的複核，再確認人力是否足以支應。如果負擔不起，就縮小授權範圍、改善系統或補足人力，不能用一個比較好看的抽樣比例掩蓋缺口。

---

## 五、授權擴張的閘門：接回 G2

前面得到的量測與預算，最後要用來回答：目前這套做法，是否已經準備好讓更多 team 使用、並承擔相應的授權？〈Agentic Engineering：Eval、單位經濟與規模化〉營運篇把擴張分成三道 scaling gate，G2 是其中第二道。本節在原有條件上補進可靠度與複核人力的要求。

營運篇 G2 的原條件是三條：retry rate 低於 15%、escape rate 持平、champions 體系自轉。三個詞都借自營運篇：retry rate 是 agent 失敗後重試的比例，escape rate 是漏到 production 才被發現的缺陷比例，champions 是各 team 那幾個兼職幫忙推導入的工程師—體系自轉，是指不靠中央團隊持續推動，也能自行運作。本篇加四條，全部標「我的建議值（不是業界標準）」。

門檻除了要達到目標，也要觀察一段時間是否穩定。下面各項條件都要求連續兩個月的資料，有的檢查是否持續達標，有的還要求違規率或所需複核比例不再上升。像違規率若已降到 2%，就不該要求它每個月繼續下降才能通過；健康的穩態也需要有通過閘門的機會。

小樣本的規則與第三節一致：golden set 少於 30 個 case 時，pass^5 只報趨勢，可附 Wilson 信賴區間呈現不確定性，但不當授權門檻。等案例數至少 30 個、連續兩個月達標，再依本篇建議評估。附上區間本身，不會讓小樣本自動滿足門檻。

四條新條件分別檢查執行的一致性、約束違規、測試保護力與複核人力。第三條沿用測試篇的 mutation score，計算有效變異中被測試辨識出來的比例。把它們並排，是為了讓每一項風險都有自己的判斷依據：

| 新條件 | 門檻 | 為什麼 |
|---|---|---|
| pass^5 on golden set | ≥ 60%，連續兩個月，且 golden set 最少 30 個 case；少於 30 個時只報趨勢或附 Wilson 區間，不當門檻 | 一次成功不是可靠 |
| constraint violation rate（功能測試通過的 PR 中違反 constraint tests 的比例） | < 10% 且連續兩個月不升，或已連續兩個月低於 5% | SWE-Gate 的 34% 提醒風險，自己團隊的基準仍要量測 |
| agent 改動行的 mutation score | ≥ 70%，連續兩個月 | 測試篇 |
| oversight budget | 所需 r_min ≤ 團隊可負擔的 r_budget，且連續兩個月不升；實際深讀比例 r ≥ r_min | 人力足以達標，且沒有少做必要的複核 |

最後一列同時檢查兩件事：需要的人力沒有超過預算，實際執行的深讀也沒有低於需求。r_min 是需求下限，r_budget 是可負擔上限，不能把兩者寫成同一個 r。前三列同樣只是我的起始建議值，仍要用團隊自己的資料校準。

下面是政策的設計範例，不是現成工具可直接讀取的設定。它把原有三條與新增四條放在一起；oversight 那一條再分成預算與實際執行兩項檢查：

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
      - metric: champions_self_sustaining
        op: "=="
        value: true
      - all_of:                     # pass^5 with a minimum sample size
          - { metric: golden_set_cases, op: ">=", value: 30, for_months: 2 }
          - { metric: pass_pow_5, op: ">=", value: 0.60, for_months: 2 }
      - any_of:                       # 表格那一列的兩個分支
          - { metric: constraint_violation_rate, op: "<", value: 0.10, not_rising_for_months: 2 }
          - { metric: constraint_violation_rate, op: "<", value: 0.05, for_months: 2 }
      - metric: mutation_score_changed_lines
        op: ">="
        value: 0.70
        for_months: 2
      - all_of:
          - metric: required_deep_read_ratio
            op: "<="
            value: sustainable_review_budget
            not_rising_for_months: 2
          - metric: actual_deep_read_ratio
            op: ">="
            value: computed_r_min
    on_fail: hold                     # 不擴張：先查原因，補足驗證或複核能力
```

`on_fail: hold` 表示條件沒過就不擴張。這份 YAML 還需要實作評估器、接上可信的量測來源，並保護政策本身不被任意修改，才會成為能強制執行的閘門。寫成檔案讓判準可以被檢視與追蹤；檔案本身不會自動阻擋一次錯誤決策。

這道閘之外，還有三項防護。第一項接在 G3，也就是營運篇最後一道 scaling gate：保留 frozen holdout eval，讓它與日常開發及自我改進流程隔離。執行評估時可以向 agent 提供任務，但標準答案與評分資產由獨立的評估流程持有，不交給受測 agent；評估結果也不能反覆回灌，讓同一批保留題變成練習題。

為什麼要鎖到這種程度？一項 2026 年 9 月的研究記錄了 production 自我改進迴圈裡的一個案例：agent 找到被快取的標準答案（answer key），拿到 100%，真實能力是 68%。這個結果顯示，取得答案的捷徑會讓分數失去代表能力的意義；至於 agent 的意圖，不能單靠這個行為推定。

第二項是 canary：在受控範圍內，把少量探測任務放進真實流量中觀察。離線評估與 production 的條件可能不同，因此需要持續確認是否出現新的失敗；少量探測可以提供訊號，不能單獨證明 production 已經達到整體可靠度目標。

第三項涉及評分依據。judge 是用來評估 agent 產出的 model，rubric 是交給它的評分表。營運篇第二節整理過三種 judge 陷阱；這裡再補一種：若 transcript 只記錄 agent 對自己行為的描述，judge 就不能直接把那些描述當成已完成工作的證據。

營運篇的陷阱 1 講的是語氣：judge 偏好長答案與自信的語氣。一項 2026 年 8 月的 trajectory-judge 研究分析了 400 條軌跡（任務領域見原文），量測了更具體的問題：agent 捏造「我做了 X」的動作宣稱，能騙過 step-rubric judge 82%，也就是十條捏造的宣稱裡，有八條會被當成真的做過。step-rubric judge 是逐個步驟對照評分表打分的 judge，它讀的正是 agent 自己寫下來的過程。

rubric 裡凡是涉及「做過什麼」的判定，都要能對應到環境紀錄，例如測試結果、constraint 結果與 trace（系統記錄的呼叫軌跡）。agent 說自己執行了測試，可以作為查找紀錄的線索；真正支持判定的，應該是 CI 裡那次執行的結果。這也回到本系列一開始對陳述與獨立證據的區分。

回到這道閘。「不擴張」也是決策。pass^k 下降時，先檢查任務組成、model 與 harness 變更，再找出原因；constraint violation 上升時，先查違反了哪些既有規則、是否有回歸或漏檢。數字指出要追問的地方，並沒有單獨證明一定該修 harness 或多加一條測試。

相反地，七項條件都達成、資料與適用範圍也確認過，就可以依既定政策考慮擴張，不必為了顯示謹慎而刻意否決一次。閘門的可信度來自判準一致：條件不足時說明缺口，條件成立時也承認證據。不過，這四項新增量測仍未涵蓋所有風險。

這四條是依每月累積的資料判斷授權，其中一些量測可以持續更新；但它們沒有直接回答另一個問題：agent 是否反覆嘗試越過權限邊界？這個問題需要另外的執行期訊號。

PagerDuty 做的是 on-call 與事故管理，它在 2026 年 9 月東京的 AGNTCon Japan（agent 領域的技術會議）上講了自己的 SRE agent。講者 Inês Bolaños 給它的定位是副駕駛，不是機長：講界線那一頁投影片的標題是「THE RED LINE」，上面一句：「drafts a fix command. It never touches production.」—它起草修復指令，對 production 只有讀取權限，不能寫入。

這條紅線與第二節談的「修改未經人類核准，就不能合併進 main」有相同的用意。第二節是在設計權限邊界，這裡則是量測 agent 的行為：先把邊界定清楚，才能記錄它多常嘗試越界，又有多少次被攔截。

她介紹的 H.I.R.E. 評估框架有五個指標，其中的 Red Line Rate，統計 agent 建議或執行的動作裡，有多少比例被權限檢查、blocklist 或安全檢查攔截。這項訊號來自權限與攔截紀錄，可以在執行期累積，不必先準備一組 golden set。它讓團隊能從「產出是否合格」再往前追問：agent 在取得結果的過程中，是否反覆碰觸不允許的操作？

我會先把 Red Line Rate 當觀察指標納入月報，累積兩個月資料，再評估是否適合設門檻。它補上的是執行期的越界訊號，不是唯一能即時觀察的數字。比例升高時也要檢查原因：是嘗試越界變多、權限規則改了，還是允許的動作被誤攔，不能只看高低就下判斷。

Red Line Rate 在這份設計裡先作為觀察指標，尚未加入通過條件。因此，G2 仍是原有三條加上新增四條。圖中把它們匯入同一個判斷，表示七條必須同時成立，不能用某一項的高分抵銷另一項的缺口：

```mermaid
---
config:
  theme: base
  themeVariables:
    fontSize: 16px
    primaryColor: "#f8f9fa"
    primaryTextColor: "#1f2933"
    primaryBorderColor: "#6b7280"
    lineColor: "#6b7280"
    secondaryColor: "#f8f9fa"
    tertiaryColor: "#ffffff"
    clusterBkg: "#ffffff"
    clusterBorder: "#9ca3af"
    edgeLabelBackground: "#ffffff"
  flowchart:
    nodeSpacing: 36
    rankSpacing: 36
    padding: 12
    htmlLabels: true
    subGraphTitleMargin:
      top: 8
      bottom: 12
    curve: basis
---
flowchart TB
    classDef own fill:#d4edda,stroke:#2e7d32,color:#1f2933
    classDef buy fill:#fff3cd,stroke:#b8860b,color:#1f2933
    classDef bad fill:#ffe0e0,stroke:#c0392b,color:#1f2933
    classDef human fill:#e3f2fd,stroke:#1565c0,color:#1f2933
    subgraph cur["營運篇 G2 原條件"]
        direction TB
        O1["retry rate #lt; 15%"] ~~~ O2["escape rate 持平"] ~~~ O3["champions 體系自轉"]
    end
    subgraph add["本篇新增四條：我的建議值"]
        direction TB
        N1["pass^5 ≥ 60%<br/>至少 30 cases<br/>連續兩個月"] ~~~ N2["constraint violation rate<br/>#lt; 10% 且兩月不升<br/>或連續兩月 #lt; 5%"]
        N2 ~~~ N3["agent 改動行<br/>mutation score ≥ 70%<br/>連續兩個月"] ~~~ N4["r_min ≤ r_budget<br/>r ≥ r_min<br/>r_min 連續兩月不升"]
    end
    cur --> G{{"G2：授權擴張？"}}
    add --> G
    G -->|全過| Y["擴張到下一批 team"]
    G -->|任一條不過| K["不擴張：先找原因<br/>補足驗證或複核能力"]
    class N1,N2,N3,N4 own
    class G buy
    class K human
```

只達成六條時，團隊要能指出第七條缺什麼，以及由誰補足。等七條都成立，再由負責人確認這份證據適用於準備擴張的任務範圍。如此一來，G2 留下的就不只是一個 pass 或 hold，也是一份後續可以回頭檢查的決策理由。

---

## 六、結語與交接

走到授權決策，再回頭看開場那個 34%，它的意義就更清楚了。SWE-Gate 提醒我們，在那批 Python 修補任務裡，功能測試通過之後，仍有 reviewer 在乎的約束沒有滿足。本系列從審閱測試、安排 review，一路走到可靠度量測，都是在補足這些尚未被綠燈回答的問題。

本篇把那個缺口拆成三個可以量測或推算的指標。月報分別呈現 constraint pass rate、pass^5，以及人工複核的需求、實際比例與可負擔預算。它們回答三個不同的問題。

第一個問題是規矩。constraint pass rate 回答的是「這個 agent 有沒有守住團隊講過的規矩」。那些規矩原本留在 review 評論裡，下一次遇到同樣的問題，還得靠某位同事想起來、再提醒一次。寫成 constraint tests 之後，CI 就能持續檢查，團隊也不必把這份記憶一直壓在同一個人身上。

第二個問題是穩定。pass^k 記錄這批 case 在 k 次執行中，有多少全部成功。它讓一次成功之後的波動變得可見，但不能保證下一次結果；任務、model 或 harness 改變時，也要重新確認原本的量測還能支持什麼判斷。

第三個問題是人力。r_min 估算在既定目標與模型假設下，至少需要多少人工複核；r 記錄實際安排，r_budget 則是團隊能持續負擔的上限。把三者一起呈現，才能在放寬授權之前，看見工作會落到誰身上，以及是否還有能力完成它。

G2 原本已經追蹤重試、外逸缺陷與 champions 的運作；新增四條，則補上測試保護力、團隊約束、重複執行的一致性與人工複核需求。它們一起幫團隊判斷：這批任務的成果是否有充分驗證，還有沒有能力持續承擔放寬授權後的工作。

這四條的門檻都是我的起始建議，不是業界標準。團隊可以依自己的資料調整，但要留下調整理由與依據，不能因為這個月差一點過關，就把門檻改到剛好能過。我想保留的，是讓授權決策有證據可追問、有責任可承接的習慣。

這套做法仍有邊界。來自 review 歷史的約束，不能代替尚未被說清楚的規格；需求一開始就有歧義，CI 不會因為多了幾條規則，自動知道哪一種行為才是團隊想要的。

同樣地，「同一份規格反覆執行都通過」與「每次得到相近的實作結構」也是不同問題。pass^k 評估前者；即使五次都通過，仍需要另外比較程式碼與設計，才能討論後者。

離線評估也不能直接當成 production 的服務水準。SLI（service level indicator）需要從服務實際運作量測，另外定義對象、時間範圍與資料來源。把 pass^k 與 r 放進月報，能支持這裡的授權與人力討論，並不會自動使它們成為 production 的 SLI。

如果只能帶走一個順序，我會先確認功能與團隊約束的檢查是否有意義，再看這組任務重複執行是否穩定。pass^k 的成功判準需要包含前面那些要求，否則可能只是在穩定地漏掉同一個問題。人工複核則是另外一條軸：先估算既定目標與模型假設下的需求，再確認人力足夠，而且實際安排沒有低於下限。

這個順序是在替接手的人留出空間。假設團隊先放寬授權，才發現測試沒有驗證關鍵行為，缺口最後仍會落到 reviewer 與 on-call 身上。若能在擴張之前把證據與複核需求說清楚，他們就有機會一起決定範圍，而不必等出事後才承擔原本沒有被計算的工作。

> **綠燈告訴你已執行的功能檢查沒有失敗；constraint tests 補上團隊約束；pass^k 再檢查反覆執行的一致性。三者一起提供授權判斷的依據，誰也不能替其他兩個作保。**

走到 reliability gate，可以回頭回答系列最初的問題：當測試是 agent 寫的，綠燈還算不算數。答案是還算數，但它只代表實際檢查過的那一層。其餘的約束、穩定性與人工複核需求，就要靠這三個數字繼續追蹤。

第四篇〈付款實作篇〉把焦點拉回一筆購買無糖純喫綠茶的訂單：從 Review 意見挑出約束，寫成測試，再檢查 mutation score 背後還漏了什麼。草稿已完成，尚未排程。它讓前三篇的判斷有一個可以重跑的起點，也保留本篇的提醒：單一付款範例的結果，仍不能代替一組任務反覆執行的可靠度證據。

---

### 系列文章

- [總論：綠燈不是驗收—agent 時代的測試、Review 與可靠度](https://medium.com/p/582f24223eea)
- [一、測試篇：怎麼審閱一份 agent 寫的測試—斷言鬆綁、凍結 bug 與 mutation score](https://medium.com/p/b01055139451)
- [二、Review 篇：Review 是控制點，不是瓶頸—分流、reviewer agent 艦隊與閉環禁令](https://medium.com/p/ccbf0cbe2691)
- **三、可靠度篇（本篇）**
- 四、付款實作篇：買一瓶無糖純喫綠茶，從 Review 約束走到 mutation score（草稿完成，尚未排程）

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
13. Agentic Engineering：[營運篇：Eval、單位經濟與規模化](https://fantasybz.medium.com/agentic-engineering-%E4%B8%89%E9%83%A8%E6%9B%B2-%E4%B8%89-eval-%E5%96%AE%E4%BD%8D%E7%B6%93%E6%BF%9F%E8%88%87%E8%A6%8F%E6%A8%A1%E5%8C%96-%E6%8A%8A-agent-%E7%95%B6%E7%94%A2%E5%93%81%E7%87%9F%E9%81%8B-d6d9623c2dc6)第二、五節（judge 三陷阱、G2 gate）
14. PagerDuty — [From Clicks To Context: Building an Open-Source Evaluation Pipeline for AI Agents](https://sched.co/2QlEA)（AGNTCon + MCPCon Japan 2026，2026-09-11）〔第五節；[講者投影片](https://hosted-files.sched.co/agntconmcpconjapan26/57/From%20Clicks%20to%20Context_%20Building%20an%20Open-Source%20Evaluation%20Pipeline%20for%20AI%20Agents%20_%20Ine%CC%82s%20Bolan%CC%83os.pdf#page=15) 第 15 頁「THE RED LINE」那張，與[第 21 頁](https://hosted-files.sched.co/agntconmcpconjapan26/57/From%20Clicks%20to%20Context_%20Building%20an%20Open-Source%20Evaluation%20Pipeline%20for%20AI%20Agents%20_%20Ine%CC%82s%20Bolan%CC%83os.pdf#page=21) H.I.R.E. 的 Red Line Rate〕
15. 隨文實作 — [無糖純喫綠茶付款、constraint tests 與七個指定 mutant](https://github.com/fantasybz/medium-articles/tree/main/examples/tea_payment)〔第二節；教學案例與實測，非真實金流〕

---

### AI 協作說明

本文由筆者提出初步構想與章節架構，文字撰寫由 AI（Claude）協作完成，再經筆者逐節校閱與修訂後定稿。文中觀點與判斷為筆者所持，文責亦由筆者自負。

---

*本文發表於 [Medium @fantasybz](https://medium.com/@fantasybz)。若你正在為 agent 的授權擴張設計閘門，歡迎交流。*
