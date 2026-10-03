# 綠燈不是驗收（一）測試篇：怎麼審閱一份 agent 寫的測試—斷言鬆綁、凍結 bug 與 mutation score

> **TL;DR** — 如果付款被多扣一次，測試還會全綠嗎？審閱 agent 寫的測試，要從這類問題開始：它把什麼當成正確，又真的抓得到什麼錯誤？本篇先辨識測試被放寬、把現有 bug 當答案，以及沒有測到需求的幾種情況，再說明如何比較修改前後的斷言、讓新測試重現舊 bug，並刻意改壞程式來檢查測試的辨識力。這些方法能整理出值得人追問的線索，仍需要有人確認需求是否完整。文末的工作坊實例與十題清單，把這項判斷帶回一份實際的測試套件。

> 系列導覽：[總論](https://medium.com/p/582f24223eea) → **一、測試篇（本篇）** → 二、Review 篇（即將發布） → 三、可靠度篇（即將發布） → 四、付款實作篇（即將發布）

---

## 一、「AI 說沒問題」之後，tester 的新工作

James Bach 是 Context-Driven Testing 與 Rapid Software Testing 方法論的作者。總論借他的語言，把兩件常被混在一起的事切開：checking 是照著已知的規則對答案，testing 是人在判斷這個東西到底行不行。

例如，測試核對一筆付款只扣了一次款，是在做 checking；人追問「顧客在畫面沒回應時又按一次，還會只扣一次嗎」，則可能替測試找出新的情境。CI 是自動執行這些檢查的流程。agent 說「測試全過」，仍要回頭核對執行紀錄；至於已執行的檢查是否足以支持驗收，還需要人的判斷。

總論也給了這條界線的第一個數字。SWE-Gate 這個 benchmark 在一批 Python repo 的修補任務上，把功能測試與 reviewer 提出的約束（constraint）分開執行檢查，結果是通過功能測試的修補裡，有 34% 違反了約束。也就是說，綠燈沒有涵蓋 reviewer 真正在乎的那些要求。

那是綠燈無法涵蓋的其中一層。本篇要談的是更前面的另一層：測試本身有沒有用。這是三道閘裡的第一道，test gate。四部曲的前三篇分別深入這三道閘：test gate 在本篇，review gate 在〈Review 篇〉，reliability gate 在〈可靠度篇〉。第四篇〈付款實作篇〉再用同一筆訂單，把前三篇的判斷落到程式與測試上。

這篇沿用總論的一條責任界線：agent 說已完成、agent 寫出的測試，以及團隊已審查並負責維護的測試，是不同層次的證據。agent 寫的測試通過有效性檢查，再由人核准合併，才升格為團隊擁有的驗收依據。完整的保護機制見總論第二節；本篇專注在升格前，如何確認測試值得信任。

先講為什麼測試比程式碼更需要審。Scrum Community 轉貼過 Lada Kesseler 的一句話，短到可以當標語，大意是：我對 AI 寫的測試的信任，比對它寫的程式碼還少。

理由很直接：測試是 agent 對自己的驗收標準，出題者與考生是同一個。程式碼寫錯了，測試還有機會攔下來。如果連測試的要求都被放寬，這道原本應該攔住錯誤的防線，也就失去了作用。

第二個理由來自 Bach。他說 tester 的核心能力是 rapid learning，也就是把陌生的東西快速學起來的能力。在 agent 時代這句話有一個具體的版本：讀 agent 留下的測試，比讀它的程式碼更快知道它理解了什麼、沒理解什麼。

原因是測試是 agent 對需求的翻譯。假設需求是重送付款不能多扣款，測試卻只要求「回傳不是空的」，兩者的距離就很清楚。測試裡判定對錯的句子叫作斷言（assertion）；事先準備的訂單、付款紀錄與執行環境，則是 fixture。看它準備了什麼、又核對了什麼，能幫 reviewer 找出 agent 理解漏掉的地方。

回到 Lada Kesseler 那句話。它是往「少信一點」走，台灣真正燒起來的討論在 DevOps Taiwan，方向剛好相反。Uncle Bob（Robert C. Martin）是 TDD 最主要的推廣者，有人把他「不讀 agent 的程式碼、只看測試與品質指標」的立場貼上去，底下吵成一串，也有人半開玩笑地要他把該做的測試全部列出來。

他其實列過（[2026-07-26](https://x.com/unclebobmartin/status/2081332683582427641)）：agent 寫得快，把省下的時間花在 unit、acceptance、property、torture、mutation 與 QA 測試上。property testing 用生成的輸入檢查應成立的性質；torture 則把輸入、負載或並行程度推到正常範圍之外，看系統在哪裡失效。這幾種方法各有用途，本篇只深談 mutation，因為它直接追問：程式碼被刻意改動之後，既有測試能不能辨識出差異？

我想把那場討論往前推一步：要放心使用一份測試，光知道它屬於哪一種類型還不夠。得先看它可能怎麼失去保護力，再設法把這些缺口呈現在報告裡。後面的順序就沿著這個問題走：辨識風險、驗證測試、看清工具的邊界，最後決定人仍需要追問什麼。

---

## 二、agent 寫的測試會壞在哪：四種型態

agent 寫的測試可能以不同方式失去保護力。本篇整理四種值得先檢查的型態：斷言被鬆綁、現狀 bug 被錄成 golden file、測試無法辨識錯誤，以及覆蓋率被當成品質。這是檢查的起點，不是一份能涵蓋所有問題的分類。

先用付款的假設情境把差異看清楚：要求「只扣一筆」被改成「至少扣一筆」，是斷言被放寬；把目前錯誤的兩筆扣款存成預期輸出，是把 bug 當答案。這種事先存好、下次直接拿來比對的輸出，叫作 snapshot 或 golden file。若測試先安排一個永遠回傳成功的替身（mock），最後只核對這個成功回覆，也可能完全沒有驗證真正的扣款行為。至於覆蓋率，只記錄程式哪裡被執行過，本身不會確認扣款次數正不正確。

這四種情況都可能呈現綠燈。下表把症狀與檢查方法放在一起；其中 mutant 是被刻意改動、用來考驗測試的一版程式，第四節會實際展開。reward 則是 agent 收到的成功回饋：若只獎勵綠燈，修對程式與放寬答案就可能得到同樣的回饋。

| 型態 | 症狀 | 為什麼 agent 會這樣 | 怎麼偵測 |
|---|---|---|---|
| **斷言鬆綁** | `assertEqual(x, 3)` 變成 `assertTrue(x >= 1)`；`toEqual` 變成 `toMatchObject`；`toHaveBeenCalledTimes(3)` 變成 `toHaveBeenCalled()`；放寬 tolerance、拉長 timeout；刪掉斷言或 `assertRaises`；加 `@skip`、`xfail`、`.only`；刪掉整個測試檔 | 「讓測試過」與「修對 bug」在 reward 上等價；最便宜的鬆綁不是改比較子，是刪掉或跳過 | assertion-change diff：把弱化分成四類（第五節），移除與停用一律阻擋，強度下降與精度放寬阻擋，其餘標記給人看 |
| **凍結 bug 的 golden** | 把現狀輸出錄成 snapshot 或 golden file，bug 從此被測試保護 | 錄現狀零成本；沒有人問「這個期望值從哪裡來」 | 新 golden file 的來源必須寫在 PR 裡；snapshot 更新與 code 變更不得同一個 PR，除非附理由 |
| **無法辨識錯誤的測試** | 測試通過，但沒有執行應驗證的路徑；tautology（`assert result == result`）；只核對 mock 預設的回傳值 | 測試可能只確認了自己的安排，沒有驗證產品行為 | red-then-green：新測試對修補前的 code 執行，必須因為預期的行為差異失敗；只對修改既有行為的 PR。feature PR 用 mutation 輔助檢查；沒有殺死 mutant 是追查線索，不等於證明測試永不失敗 |
| **覆蓋率當品質** | CI 的覆蓋率門檻過了，但 repo 原有的測試只碰到 agent 改動行的 27%（Python） | 覆蓋率是一條可以被改掉的斷言：exclude pattern、trivial test、只呼叫不斷言 | 覆蓋率只看 agent 改動的行，而且與 mutation score 成對讀 |

表裡第三欄要讀成可能的機制，不是對 agent 動機的判定。當回饋只獎勵「測試通過」，修正產品與放寬測試可能得到一樣的成功訊號。流程需要把兩者分開，讓 CI 不只回報有沒有綠，也能指出測試要求是否被改變。

這些風險也出現在其他分類裡。李博杰是 Pine AI 的首席科學家、《深入理解 AI Agent：設計原理與工程實踐》的作者。他在第七章談失敗歸因，也就是從執行紀錄追問錯誤從哪一步開始。其中一類叫 hack 驗證環境：改斷言、加 skip、用 mock 繞過被測邏輯，以及聲稱「測試已通過」卻沒有執行紀錄。

前三項在上面那四種裡都找得到位置，第四項不在：那是連測試都沒有執行，只有一句宣稱。他也提醒，這類分類還會持續擴充；本篇只借用與測試相關的部分。

第四項連 checking 都算不上：只要 CI 實際執行一次測試，就能核對這句宣稱。四種壞法都是測試跑了而且是綠的，這一項是綠燈之前的事，所以本篇不把它列成第五種。

還有一種壞法不列進表，因為它不是測試自己壞掉，是 red-then-green 這道檢查會踩到的坑：**因為錯的理由紅**。

LeSS in Action 這門課教 A-TDD（Acceptance Test-Driven Development，先寫驗收測試再寫實作）時有一條紀律，就是關注錯誤訊息，錯誤訊息要符合預期。red-then-green 的 red 套用同一條紀律：要看到預期的斷言失敗，不是 import error 這種「測試根本沒跑到」的紅。

第三列還有一種更難辨識的情況，留給第七節的工作坊實例。測試會失敗、斷言也是真的，卻走了錯的路徑：它直接從記憶體裡讀取物件，規格要的則是從事件重播還原狀態。只對既有實作執行這三個 check，未必能發現整條需求路徑被省略；還要對照需求建立約束。

把四種壞法與它們各自的 check 排在一起，會看到壞掉的方式雖然有四種，人要防的其實只有兩件事：測試被改弱，與測試沒測到。

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
flowchart LR
    classDef own fill:#d4edda,stroke:#2e7d32,color:#1f2933
    classDef buy fill:#fff3cd,stroke:#b8860b,color:#1f2933
    classDef bad fill:#ffe0e0,stroke:#c0392b,color:#1f2933
    classDef human fill:#e3f2fd,stroke:#1565c0,color:#1f2933
    subgraph a["測試被改弱"]
        direction TB
        A1["斷言鬆綁<br/>assertEqual 改成 assertTrue<br/>刪斷言、加 skip"] --> C1["assertion-change diff<br/>四類弱化 → 阻擋"]
        C1 ~~~ A2["無法辨識錯誤的測試<br/>tautology、只核對 mock"]
        A2 --> C2["red-then-green<br/>只對 fix／behaviour-change PR"]
    end
    subgraph b["測試沒測到"]
        direction TB
        B1["凍結 bug 的 golden<br/>現狀錄成 snapshot"] --> D1["golden 來源欄必填<br/>與 code 同 PR 須附理由"]
        D1 ~~~ B2["覆蓋率當品質<br/>既有測試覆蓋改動行 27%"]
        B2 --> D2["覆蓋率只看 agent 改動行<br/>與 mutation score 成對讀"]
    end
    a ~~~ b
    class A1,A2,B1,B2 bad
    class C1,C2,D1,D2 own
```

四種風險各有可以先做的檢查：三個 check，加上一個交代 golden 來源的 PR template 欄位。它們的成本不同，mutation 尤其需要控制執行範圍。

機器能偵測出測試裡的壞味道，卻無法替人釐清需求的意圖（intent）。這些 check 把可以自動辨識的問題先整理出來，人才有時間回頭想：這份測試，真的在驗證需求想要的行為嗎。

---

## 三、人眼不夠：49%

上一節的處方全部指向工具，沒有一條指向「更仔細的人」。這是有理由的。

一項實驗讓 86 位開發者判斷 LLM 產生的斷言對不對（Poor and Overconfident Judges，2026 年 7 月）。面對正確斷言，判斷準確率是 74%；面對錯誤斷言，則只有 49%。這是判斷結果的比例，不是說只有某一群人具備辨識能力。

兩種情況下的信心卻相近。這代表在該實驗中，錯誤判斷並沒有穩定地伴隨較低信心；不能期待 reviewer 光靠「覺得哪裡不對」，就能知道自己需要再查一次。

實驗還多試了一種條件：在斷言旁邊附上 LLM 自己的解釋，看人會不會判斷得比較準。答案是附上解釋沒有幫助，低品質的解釋反而有害。

用途要先限定。這個實驗評估的是「判斷 LLM 產生的斷言對不對」，不是「判斷被 agent 鬆綁的既有斷言」。後者是第五節 assertion-change diff 的事，兩件事我分開寫，但方向一致。

那如果先告訴人「這段是 AI 寫的」，審查會改善嗎？另一項 eye-tracking 研究觀察到，標示為 LLM 產生的程式碼讓 reviewer 看得更久，卻沒有對應到更深入的審視。至少在這項研究裡，花更多時間並沒有帶來預期的改變。

兩項研究的任務不同，不能合併成一個抓錯率。它們共同提醒的是：延長閱讀時間、提醒程式碼來自 AI，都不能直接當成品質已改善的證據。

因此，「請 senior 仔細看測試」還不算完整的策略。先讓工具指出哪些斷言被弱化、哪些新測試對舊 code 沒有失敗、哪些 mutant 仍然存活，人才能帶著具體疑點回到測試與需求，而不是從第一行開始猜哪裡可能有問題。最後那個 mutant 是什麼，下一節會說明。

把四種壞法攤開，人眼與工具各自能做到什麼，一列一列對照就很清楚：

| 壞法 | 人眼 | 工具 |
|---|---|---|
| 斷言鬆綁 | 需要比較修改前後的檢查強度；刪除的斷言可能淹沒在大量 diff 中 | assertion-change diff，四類分級，移除與停用直接阻擋 |
| 凍結 bug 的 golden | snapshot diff 很長時，難以逐項確認輸出是否符合需求 | PR template 的「golden 來源」欄必填；snapshot 與 code 同 PR 時須附理由 |
| 無法辨識錯誤 | 有些問題可從程式碼看出，有些要執行後才能確認 | red-then-green（fix 與 behaviour-change PR）+ mutation（包含 feature PR） |
| 覆蓋率 game | 只看總覆蓋率，無法知道這份改動受多少保護 | diff-scoped coverage 只看 agent 改動行，與 mutation score 成對 |

表裡「人眼」那一欄有一個共同點：每一格的問題都不是人不夠認真。有些訊號在視覺上根本不顯眼，被刪掉的斷言在 diff 裡就是紅色的一行，跟其他幾百行紅色長得一模一樣。有些問題則要實際執行測試才會浮現，光靠閱讀程式碼，再仔細也看不到。

---

## 四、Mutation testing：當閘門，不當儀式

假設已經有「重送付款不能多扣款」的測試，怎麼知道它真的有效？可以暫時移除防止重複扣款的檢查，再執行一次。如果測試因此失敗，就有具體證據表明它看得見這種錯誤。**Mutation testing（變異測試）**把這種做法系統化：刻意改動運算子、常數或條件，逐一執行測試。每份被改動的程式稱為 mutant；測試抓到它，通常稱為「殺死」，沒抓到則是存活。mutation score 是納入計分的 mutant 中，被辨識出的比例。

可以把它想成先測試警報會不會響。這裡的警報是測試，安排的故障是程式變異，演練發生在測試環境。若警報沒響，要查的是測試漏了什麼，或這次變動是否根本沒有造成可觀察的差異，不能只憑「存活」就判定一定缺測試。

拿 mutation 當閘門不是我先提的。Uncle Bob 的閘門組合是 coverage、CRAP score 與 mutation tests。CRAP score（Change Risk Anti-Patterns）把複雜度與覆蓋率合成一個數字，又複雜又沒被測到的函式分數最高。

這組閘門與它的理由出自他的一則貼文（[2026-07-30](https://x.com/unclebobmartin/status/2082850576832905657)）：TDD 是人的紀律，他不期待 agent 遵守，改用量測結果判斷品質。

第一節那個「不讀 agent 的程式碼」的立場，就是這個。DevOps Taiwan 轉述的是另一份清單：unit、Gherkin（用 Given／When／Then 寫成的驗收測試語法）、mutation 與品質指標，過了他就不再讀 code。兩份清單不完全一樣，但都有 mutation。

本文不走到那麼遠。Review 篇會說人還是要審閱 intent 與 constraint 報告，但同意 mutation 是 test gate 的核心。

mutation testing 不是新東西，執行成本卻一直是導入時要面對的問題。產生 N 個 mutant，就需要對這些變異反覆執行測試；即使用 test selection 縮小每次執行的範圍，這筆成本也不會消失。

agent 讓測試產出變快，也讓逐份人工審閱更難負擔，因此更需要衡量測試的有效性。假設這次只修改付款重試的幾行，就先對那些改動產生變異，不必每次都考驗整個系統。這就是 **diff-scoped mutation**：把變異範圍限定在這份修改。執行時仍可能需要牽涉其他模組的測試；範圍變小不保證便宜，是否划算還要看受影響測試的執行時間。這種做法也不是 agent 時代才出現。

總論第十節講過一句話：驗證工具的價值由觸及範圍決定。diff-scoped mutation 的觸及範圍，正好是 agent 剛改的那幾行。

它的限制也需要先說清楚：mutation 衡量的是「已經寫出來的程式碼有沒有被測試守住」，無法偵測「規格要求的東西根本沒有寫出來」。

具體一點說，它會告訴你這個條件判斷翻過來之後沒有任何測試變紅，不會告訴你這個模組少了一條架構規則、少了一條 business constraint，或是規格要求的那條路徑根本不存在。第七節的例子就是後面這一種。

回到成本。多數人裝這道 check 的時候，面對的是 brownfield，也就是已經跑了很多年、測試套件又大又慢的既有系統。Brownfield 的現實：40 分鐘的測試套件上，diff-scoped mutation 仍然要把受影響的測試重複執行 N 次。

所以它是四道 check 裡**最後裝**的，只在受影響子集能在 10 分鐘內跑完的 repo 上啟用。為什麼是這個順序，總論第十節講過，這裡不重列。

**儀式版與閘門版的差別**：這一題今年夏天被問過兩次。第一次是 Thoughtworks 的 Birgitta Böckeler，她問的是「TDD inside the agent loop—theater or actual value?」（Martin Fowler [2026-08-11](https://x.com/martinfowler/status/2087173563144912985) 轉貼）。agent 在自己的迴圈裡做 TDD，是做給人看的戲，還是真的有價值。

第二次是 Uncle Bob 8 月 17 日做的實驗（negative test experiment），問的是同一題的另一面：他讓四種測試紀律各寫一次同一支程式，驗收測試全綠，程式卻不一樣（[2026-08-17](https://x.com/unclebobmartin/status/2089449442089025936)，設計與結果總論講過）。

這兩個討論讓我回到同一個問題：流程的形狀對了，還需要檢查它是否真的提供保護。叫 agent「執行 mutation，再補測試補到 100%」，如果只追分數，就可能得到過度迎合變異算子的測試。這些測試未必是假的，卻仍然可能漏掉規格裡根本沒有被實作的要求。

閘門版先讓 CI 列出存活的 mutant，再分清原因。例如在輸入已限定為整數的前提下，把「大於零」換成「大於等於一」，判斷結果不會改變。這類 **equivalent mutant（等價變異）**不是測試漏抓；測試原本就無法用行為區分它與原版。確認等價後，排除計分並留下理由；其餘確實改變行為的變異，再查是測試缺口還是規格需要澄清，將可確認的缺口交給 agent 補測試。

門檻是我的建議值，不是業界標準：先以 agent 改動行的 mutation score ≥ 70% 作為合併前的起始參考。導入時先提供一個月的報告，再開始阻擋未達標的 PR。這個數字參考 Uncle Bob 的做法，再加上我的初步估計，尚待自己的試行資料校準；它不是已經驗證過的通用門檻。Review 可以提早確認規格與挑選測試，分數過線則仍要逐項判讀關鍵風險。

**用付款把百分比的限制看清楚。** 前面說的是方法，現在看一份可重現的結果。隨文的 [可執行範例](https://github.com/fantasybz/medium-articles/tree/main/examples/tea_payment)，是一瓶示範售價 35 元的無糖純喫綠茶。測試使用可以控制回覆的假金流，沒有真的刷卡：它先記錄扣款，再模擬回覆逾時。應用程式收不到確定答案，就應保留 `PENDING`（結果待確認），不能自行宣告成功。Reviewer 把「未知結果不得冒充成功，重送不得再次扣款」留下來，寫成 constraint test，也就是持續驗證這份約定的測試；它同時保護功能行為，兩個名稱並不互斥。

這個測試會用同一張訂單與同一個 key 呼叫兩次 `Checkout.pay()`；key 是辨識同一次付款嘗試的識別值。它確認回覆仍是 `PENDING`、沒有代表成功付款的 payment ID，而且金流只被呼叫一次。完整版本另外涵蓋扣款前就逾時的情境，避免把「不知道」誤解成「一定已經扣款」。這些事先約定的預期結果，就是測試的 oracle：用來判斷對錯的依據，不能由待測程式幫自己算答案。

M5 故意把這一個分支改壞：

```python
# 原始付款程式
except TimeoutError:
    receipt = replace(receipt, status="PENDING")

# M5：示範中的錯誤變異
except TimeoutError:
    receipt = replace(receipt, status="PAID")
```

實測固定使用七個人工指定、可執行且不等價的 mutant，沒有排除項目。只有兩個正常購買測試時，抓到 2／7，分數 28.6%；加入其他約束、唯獨漏掉逾時測試時，抓到 6／7，分數已達 85.7%。M5 卻仍然存活。補回逾時測試後，九個測試辨識出全部七個變異，得到 100.0%。每組都先確認原始程式通過，再對每個變異執行所選測試。

這裡用 70% 作教學對照；手選七個 mutant 不能直接套用工具在真實 diff 上的門檻。即使只看數字，85.7% 超過 70%，仍不足以核准這筆付款變更，因為關鍵約束尚未被保護。100% 也只代表這七個指定變異被辨識，並非真實金流、並行或行程重新啟動都已驗證。這個範例使用同一行程內的假金流與依序呼叫，完整程式、Review 的挑選理由與分母說明，已整理在第四篇〈付款實作篇：買一瓶無糖純喫綠茶，從 Review 約束走到 mutation score〉中。

工具方面，JVM 有 PIT、JS 與 TS 有 Stryker、Python 有 mutmut。能不能限定在 diff 範圍，各家支援程度不同，動手前先確認你那套的做法。

把這一節的兩個門檻，跟另外兩道 check 的門檻放在一起，就是本篇的建議值總表：

| 項目 | 我的建議值 | 備註 |
|---|---|---|
| mutation score（agent 改動行） | ≥ 70% 起始參考；關鍵約束另審 | 先報告一個月，再阻擋 |
| 受影響子集的執行時間 | < 10 分鐘才開 mutation | 超過的 repo 先裝前三道 check |
| assertion-change diff | 移除與停用一律阻擋；強度下降、精度放寬阻擋 | 其餘既有斷言變更標 `needs-human-test-review` |
| red-then-green | 只對修改既有行為的 PR | 分類來源不是 PR 作者 |

表裡最容易被跳過的是備註欄的第一列：先提供一個月的報告，再阻擋未達標的 PR。團隊需要先從報告裡看見問題，才知道為什麼值得為這道閘停下來。順序反過來，第一個被擋住的 agent PR 就可能讓整套機制被撤掉。閘門的可信度，要靠這段使用經驗慢慢累積。

---

## 五、Diff 上的三個 check：reference implementation

付款例子說明了分數要如何解讀，接下來要讓每份 PR 都拿得到這類線索。這一節把三個 check 放進同一個 CI 流程：新測試能不能重現舊問題、舊測試有沒有被放寬，以及這次修改的程式是否受到有效保護。diff 指修改前後的差異；下面的設計都以這份差異決定檢查範圍。

三個都是由 CI 自動執行的檢查。導入時先建立前兩個，再加入成本較高的 mutation。

**Check 1：red-then-green。** 假設修補前，重送付款會扣兩次款，新測試卻要求只能扣一次。把同一份測試放到舊版，應該先失敗（red）；放到修正後的版本，才應通過（green）。這樣才能知道它分得出「bug 還在」與「bug 已修好」，不只是剛好在新版上通過。

適用範圍先講。本文的 red-then-green 只對「修改既有行為」的 PR 啟用，也就是 bug fix 與 behaviour change。feature PR 可能依賴 base branch 尚不存在的類別或介面，失敗原因就會是無法載入，而不是預期的行為差異。

這也是本文不把 red-then-green 套用到所有 feature PR 的理由：先排除無法比較的情境，才能讓 red 代表有意義的行為差異。feature PR 的新測試先由 Check 3 輔助評估，再回到需求確認是否測對了對象。

**分類來源必須獨立於 PR 作者。** 如果開 PR 的 agent 可以自行設定分類 label，就可能把應該受檢的修正標成 feature，避開 red-then-green。這裡要防的是流程留下的繞路，不必先假定 agent 一定會這樣做。

分類本身也是驗證的一部分。團隊得先保護分類依據，才能相信「這個 PR 不適用」是有根據的判斷，而不是作者替自己免除檢查。

分類的來源有三個，照順序取。第一個是 issue 或 ticket 的 type 欄，那一欄是人設的。第二個是 harness 的 task type。harness 是 agent 與工程系統之間那層介面，〈Harness 藍圖〉技術篇有完整說明。兩個都沒有時，改用 diff 判斷：只要 PR 修改了任何既有的非測試檔案，就視為 behaviour change，執行這道檢查，只新增檔案的才跳過。

前兩個來源必須由人或受保護的 harness 設定維護，agent 才不能自行改分類。第三個只是沒有任務資訊時的保守推定：它看得出有沒有改既有檔案，看不出需求是否完整。只新增檔案的 fix 也可能漏過，因此分類結果仍要接受抽查。

實作上，一個 CI job，也就是自動流程裡的一份執行工作，會把 PR 新增的測試配上 base branch（尚未合併這次修改的基準版本），在隔離環境執行。結果分成三類：

（a） 測試沒有失敗。標記 `test-never-fails`，這是唯一會加上這個標記的一類。

（b）測試因為預期的行為差異而失敗。對 bug fix，這表示它能重現原有缺陷；對 behaviour change，則表示它能辨識新舊要求的差異。這只完成 red，還要確認同一份測試在修補後通過，才完成 green。

（c）測試因為預期之外的原因失敗，例如 import error、fixture 不存在。這類結果不加 `test-never-fails`，但也不能當成驗證通過。先在報告列明原因，再由人確認是否需要拆開 PR、補齊環境或修正分類，之後重新執行。

把適用範圍與三個出口畫成一張圖，會看到它其實是一個分流器：

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
    N["PR 新增的測試"] --> Q{"PR 是 fix／behaviour change？<br/>看 ticket type 或改了既有檔"}
    Q -->|否| S["跳過<br/>新測試交給 mutation"]
    Q -->|是| R["checkout 到 base branch<br/>對修補前的 code 跑一次"]
    R --> O1["沒紅<br/>標記 test-never-fails"]
    R --> O2["對的理由紅<br/>再確認修補後通過"]
    R --> O3["錯的理由紅<br/>import error、fixture 缺<br/>無法判定、釐清後重跑"]
    class S,O3 buy
    class O1 bad
    class O2 own
```

red-then-green 只對修改既有行為的 PR 啟用。在這三種結果裡，只有「測試沒有失敗」會被標記為 `test-never-fails`。

這三個出口的意義不同：沒有失敗，要查測試是否有辨識力；預期失敗，要接著驗證修補後能通過；非預期失敗，則表示目前還無法判定。把「無法判定」與「通過」分開，才不會讓一份有紅字的報告反而被誤當成綠燈。

**Check 2：assertion-change diff。** 這一道處理的是更安靜的風險：測試檔還在，測試名稱也沒變，但原本抓得到 bug 的斷言被改弱了。CI 依然全綠，diff 上也只是幾行紅綠交錯。

這裡的強弱，可以用付款回覆來理解：核對整份收據完全相同（equality），比只確認它包含某個欄位（containment）要求更多；若最後只問「有沒有回覆」（truthy），金額與狀態就可能都沒被檢查。先比較斷言真正驗證的內容，再依下面四類處理，不只聽 agent 對修改的解釋：

- （a） **強度階梯下降**：equality → containment → truthy。阻擋這個 PR。
- （b） **數量或精度放寬**：call count、tolerance、timeout。阻擋這個 PR。
- （c） **移除**：斷言刪除、`assertRaises` 刪除。一律阻擋這個 PR。
- （d） **停用**：`skip`、`xfail`、`.only`、刪除測試檔。一律阻擋這個 PR。

舉一個假設的情境。一個 PR 說它修好了序列化的 bug，diff 裡有一行把 `toEqual` 換成 `toMatchObject`。功能上這個 PR 可能真的修好了，但這一行讓測試從此不再檢查其他欄位，屬於（a），需要阻擋這個 PR。

其餘既有斷言的變更標 `needs-human-test-review`。對已經升格為團隊擁有（總論第二節的第三類）的測試，任何弱化直接阻擋。

不要只用「同一個 PR 同時改 code 與測試」當成弱化訊號。正常的行為變更也可能需要一起修改兩者；要辨識風險，仍得比較斷言前後究竟改了什麼。

**Check 3：diff-scoped mutation。** 這一道不替整個 repo 做健康檢查，它只問一件事：agent 剛改的那些行，有沒有被測試真正守住。

做法是只對 agent 改動的檔案產生 mutant，再把改動行上的結果列入報告與計分。活下來的 mutant 叫 survivors。多數工具以檔案為單位；若要自行限定到行，必須同時篩選被殺死與存活的 mutant，讓分子、分母使用同一個範圍，不能只過濾 survivors。

feature PR 的新測試不適用 red-then-green，就由這道檢查判斷它們是否守住了新寫的程式碼。

同一個 PR 會啟動三個 job，檢查結果再彙整成同一份報告：

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
    nodeSpacing: 24
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
    P["agent 開的 PR"]
    subgraph jobs["test-gate.yml：三個 job 平行跑"]
        direction LR
        J1["assertion-diff<br/>所有 PR<br/>靜態分析，不執行測試"] ~~~ J2["red-then-green<br/>fix 與 behaviour-change<br/>分類不由 PR 作者決定"] ~~~ J3["mutation-diff<br/>只對 agent 改動行<br/>受影響子集 #lt; 10 分鐘"]
    end
    P --> jobs
    jobs --> R["PR comment：弱化的斷言<br/>沒紅的新測試、活著的 mutant"]
    R --> H["人依報告回查需求與測試<br/>第一個月只報告不阻擋"]
    class J1,J2,J3 own
    class H human
```

三個 job 可以平行執行，結果彙整成同一份報告；red-then-green 依分類決定是否執行。這裡示範的是導入初期的報告模式，第一個月暫不阻擋 PR，不是前面所說的正式閘門已經生效。

第一個月先保留報告，是為了讓接手的人有機會理解新訊號。哪些警告確實指出測試缺口，哪些只是分類或環境設定不完整，都需要逐項核對。等負責人能解釋這些差異，再把可靠的檢查升成阻擋條件，團隊才知道 PR 為什麼被停下來、接著該修什麼。

AGENTS.md 是 agent 開工前會讀的那份專案指示檔。下面把裡面的指示與 CI 實際執行的量測並列，呈現一組「指示 vs 量測」的 Before / After。Uncle Bob 的說法是你沒辦法叫 agent 寫乾淨，只能量測程式碼的品質，再依結果要求它修正（[2026-07-29](https://x.com/unclebobmartin/status/2082497764223492161)）。

Before 示範一份只有指示、尚未接上檢查的 AGENTS.md：

```text
# Before：指示（尚未新增 CI 檢查）
請務必用 TDD。不要修改既有測試。
```

這兩句話每一句都對，但它們是指示。agent 讀完之後，CI 上仍不會多出任何可執行的檢查。

After 用三個檢查 job、一個 `classify` 與一個彙整報告的 job，示範它們之間的關係。這是設計節錄，不能直接貼進 GitHub Actions 執行：runner、套件安裝、job 之間的 artifact 傳遞與權限設定都還要補齊。diff 一律以 base branch 為基準。

`tools/` 底下的五個 script 是你要自己寫的部分，`classify` 一個、三個 check 各一個、貼報告的一個，行為就是上面三個 check 的定義：

```yaml
# test-gate.yml（設計節錄，非可直接執行的 workflow）
# 第一個月只報告；省略 runner、環境安裝與跨 job artifact 傳遞
on: pull_request
jobs:
  classify:              # 分類來源不是 PR 作者：讀連結 issue 的 type 欄；沒有就看是否改了既有的非測試檔
    outputs:
      kind: ${{ steps.kind.outputs.kind }}
    steps:
      - uses: actions/checkout@v4
        with: { fetch-depth: 0 }
      - id: kind
        run: python tools/classify_pr.py --base origin/${{ github.base_ref }} >> "$GITHUB_OUTPUT"
  assertion-diff:        # 所有 PR：分析 diff，不執行產品測試
    steps:
      - uses: actions/checkout@v4
        with: { fetch-depth: 0 }
      - run: python tools/assertion_strength.py --base origin/${{ github.base_ref }} --report weakened.json
  red-then-green:        # 只對 fix / behaviour-change
    needs: classify
    if: ${{ needs.classify.outputs.kind != 'feature' }}
    steps:
      - uses: actions/checkout@v4
        with: { fetch-depth: 0 }
      # script 在隔離環境比較 base 與 PR：記錄 red 原因，再確認同一份測試在 PR 上 green
      - run: python tools/red_then_green.py --base origin/${{ github.base_ref }} --head HEAD --report red_green.json
  mutation-diff:         # 受影響子集 < 10 分鐘的 repo 才開
    steps:
      - uses: actions/checkout@v4
        with: { fetch-depth: 0 }
      # 以相同改動行範圍篩選 killed 與 surviving mutants，再計算分數
      - run: python tools/mutation_diff.py --base origin/${{ github.base_ref }} --report survivors.json
  report:
    needs: [assertion-diff, red-then-green, mutation-diff]
    if: ${{ always() }}  # red-then-green 被跳過時也要出報告
    steps:
      - run: python tools/post_pr_comment.py weakened.json red_green.json survivors.json
```

正式實作時，`red_then_green.py` 必須保存兩次執行的輸出與退出碼，區分預期失敗、非預期失敗與修補後未通過；不能只留下 red 的分類。`report` 則要先取得各 job 上傳的檔案，把未執行、執行失敗與已完成分開呈現，缺檔不能當成通過。

設定裡有兩個決定需要保留下來。`red-then-green` 透過 `if` 讀取 `classify` 的輸出，因此分類依據必須受到保護，不能只把作者填的 label 再讀一次。`report` 使用 `if: always()`，則是要在檢查被跳過或失敗時，仍然留下報告。讀者應該分得出「不適用」「尚未完成」與「已經通過」，而不是看到少了一份結果就自行猜測。

即使這些狀態都寫清楚，還有一件事無法從 YAML 看出來：檢查器是否真的涵蓋了它宣稱要檢查的範圍。2026 年 9 月在東京的 AGNTCon Japan（Linux Foundation 旗下 Agentic AI Foundation 舉辦的 agent 大會）上，Quartic.ai 的兩位 SRE 分享了讓 agent 升級 production Kubernetes 的經驗，其中就有這樣的缺口。

Kubernetes 一次只能升級一個小版本，每次升級算一跳。他們在台上自己講了第一版怎麼漏的：驗證只檢查每一跳之後的第一個節點，管理節點（control plane）上到 1.31、跑工作的節點還留在 1.30，那一跳照樣被標成成功。

修法是按角色找出每一個節點，確認所有節點的版本都符合預期，才准開始下一跳。他們把這段經驗整理成一句話：「A cluster upgrade succeeds only when the whole cluster has crossed the version boundary.」

只檢查部分節點，得到的結果就只能代表那些節點。整個叢集是否完成升級，仍然沒有被驗證。

回頭看本篇的設計，也有兩處需要同樣的警覺。`mutation_diff` 若從檔案範圍自行篩選到行，必須確認篩選器沒有漏掉該計分的 mutant。`classify` 找不到任務資訊時，則只能用「是否修改既有非測試檔」推定行為變更，不能靠這項推定確認需求是否完整。報告應該交代這些邊界，讓名稱裡的「diff」與「classification」不至於變成過度承諾。

Quartic.ai 的示範跑在 kind（本機模擬用的 Kubernetes）叢集上，這一課在 production 付過什麼代價，投影片沒寫。

校準報告時，我會把「執行成功」與「檢查完整」分開確認。前者看 job 是否正常結束，後者要回頭對照預期範圍與實際檢查清單。Quartic.ai 的例子提醒的，正是這兩件事之間的距離。

**Agent 側的配套。** 前面三個 check 都在 CI 上檢查產出。但 agent 若認為既有測試有錯，除了反覆嘗試或修改斷言，流程還能提供什麼處理方式？

一項研究（escalation channels，2026 年 8 月）試著增加另一條路：給 agent 一個結構化的「回報壞測試」工具，讓它認為測試有問題時可以提出證據，不必直接修改斷言。這可以與 CI 的阻擋機制並用。下面的 reward hacking 指為了取得通過訊號而扭曲驗證；勝算比（odds ratio）比較兩組發生該行為的勝算，要連同比較方向與研究設定判讀；frontier model 是研究當時能力最前沿的那幾個 model。

研究在 8 個 frontier model 上量測效果：reward hacking 從 23.6% 降到 5.3%，論文另報告勝算比 9.2；其中 6 個 model 在受測樣本中不再出現該行為。98.7% 的 escalation 不涉及作弊，缺陷偵測覆蓋率（defect-detection coverage）增加 10.1 個百分點。

最後兩個數字讓這個做法值得嘗試：在受測情境裡，多數回報沒有伴隨作弊，缺陷也被辨識得更多。它不是保證 agent 從此誠實，而是讓「提出可核對的問題」成為一條可走的路。導入時有兩個部分。

**第一步，在 harness 裡註冊這個 tool。** harness 管理 agent 能呼叫的工具與工作流程；註冊的意思，是讓「請人確認這份測試」成為它真的能執行的動作。例如規格要求等候 30 秒，測試卻只給 3 秒，agent 應把兩份依據一起提交。下面的格式示範如何把測試位置、理由與證據送給接手的人：

```json
{
  "name": "report_broken_test",
  "description": "你認為某個既有測試本身有錯時呼叫它，不要改斷言。",
  "parameters": {
    "test_id": "tests/test_pool.py::test_timeout",
    "reason": "expected value contradicts the spec in docs/pool.md §3",
    "evidence": "spec says 30s; test asserts 3s"
  }
}
```

`reason` 要說明 agent 認為測試哪裡有問題，`evidence` 則提供可重現的依據。這兩個欄位讓接手的人能核對主張、要求補件，或否決修改建議。欄位填滿本身不代表證據成立，仍要有人完成判斷。

**第二步，在 AGENTS.md 裡告訴 agent 這條路存在。** AGENTS.md 只加一句：「你認為測試錯了，就呼叫 `report_broken_test`，不要改斷言。」工具註冊之外，也要交代何時使用、提出什麼證據，以及回報後由誰接手。

這讓「改環境比寫規則有效」有了具體做法：一邊限制任意改動斷言，一邊提供提出異議的管道。團隊接下來要確認的，是回報有沒有被處理，而不只是工具有沒有被呼叫。

還有一項可以直接放進 PR template 的安排：要求作者交代 snapshot 或 golden file 的期望值從哪裡來。是依照規格推導、取自 production 的實際輸出，還是只記錄「現在執行的結果」？把來源寫出來，reviewer 才知道下一步要核對哪份依據。

記錄現況有它的用途，例如替 legacy code 建立 characterization tests；但現況不能未經確認就升格為正確答案。production 輸出也可能包含缺陷。把「觀察到的行為」與「需求要求的行為」分開，才能避免一份方便的 golden file，變成替 bug 辯護的依據。

---

## 六、覆蓋率是一條可以被改掉的斷言

前一節讓報告說明「測試抓得到什麼」，但團隊可能仍習慣先看覆蓋率。回到付款情境，測試可以完整走過扣款函式，卻從頭到尾沒有核對扣款次數。這就是覆蓋率的界線：它量測哪些程式行被執行過。要用它判斷眼前的 PR，還得確認分母是整個 repo，還是這次真正改動的程式碼。

一項研究（Test Coverage of Agentic PRs）量測了 4,882 個 agent PR，問的問題很窄：repo 原有的測試，會不會經過 agent 改動的那些可執行的行？答案是 Java 只有 61.5%，Python 只有 27.0%。

這裡的分母是該研究樣本中 agent 改動的可執行行，不是所有 Python repo，也不是整個 repo 的覆蓋率。結果提醒我們：就算整體覆蓋率看起來不差，新改動的區域仍可能缺少既有測試保護。

因此，要評估眼前這個 PR，還得另外檢視改動範圍的覆蓋率。整體數字可以保留，但不能替這份改動回答問題。

量測範圍之外，還有另一個需要留意的問題：覆蓋率的計算方式與測試內容都可以被修改。數字提高了，未必表示更多行為受到保護。

例如，在 exclude pattern 裡排除一個檔案，那些行就不再算進分母；測試若只呼叫程式而沒有斷言，會增加執行過的行，卻沒有檢查結果；把難測的邏輯移到被排除的檔案，也會改變數字呈現的樣子。這三種改動都需要連同理由一起審閱。

做這些改動的人可能只是時間不夠，也可能真的被 legacy code 的耦合卡住。先理解困難，才有辦法討論怎麼補測；但無論理由是什麼，都不能把計算範圍改變所帶來的上升，直接記成測試品質的進步。

不必為了這個問題立刻重做整套 coverage 制度。針對 agent PR，可以先把三件事放進既有的審查流程：

第一，另外呈現 agent 改動行的覆蓋率，讓 reviewer 看見這次改動的測試範圍。整體覆蓋率可以繼續追蹤，但不能用來代替這個問題。

第二條，將覆蓋率與 mutation score 搭配判讀。程式碼被執行過，不代表行為有被斷言守住，mutation 補上的正是這項檢查。

第三，exclude pattern 的變更交由人類審核，說明排除的理由、漏掉的範圍，以及還有哪些檢查能補足。要保護的是量測的意義，不只是設定檔本身。

**覆蓋率回答測試執行過哪裡；mutation 進一步檢查，刻意改動那些程式碼時，測試能不能辨識差異。** 兩者搭配，仍然有共同的界線：規格要求的行為如果根本沒被實作，數字可能照樣很好看。下面這個工作坊經驗，讓我具體看見了這個缺口。

---

## 七、第一手實例：測試全綠，replay 從未執行

今年 8 月，我在 Teddy 老師（泰迪軟體講師，部落格「搞笑談軟工」作者）的模式語言工作坊上，拿講師提供的同一份需求檔，分別用兩種方法完成實作：方法 A 只照那份檔案直接寫（工作坊叫它「裸 Prompt」），方法 B 另外加入講師提供的一套作業流程。兩種方法各自在獨立的 git worktree 裡執行，也就是同一個 repo 底下的獨立工作目錄。需求本身很小，就是一個 Product aggregate（領域驅動設計裡一組要一起保持一致的物件）加一個 CreateProduct use case。

下面只談方法 A，因為要講的問題出在它身上。如果只看交付清單，方法 A 的成果很容易讓人放心：25 個檔案、編譯零 warning、5 個測試全綠、分層乾淨、Javadoc 完整。

問題在測試走的路徑。規格要的是 event sourcing：留下發生過的事件，需要狀態時再依序重建。放進這份商品需求來看，「記憶體裡已經有一個商品物件」與「只拿儲存的事件，還能重建出同一個商品」是兩件事；後者才驗證了 replay，也就是重播。測試若只看前者，就還沒回答規格真正要問的問題。

方法 A 的 Product 完全不是 event sourcing。它沒有繼承 `EventSourcedAggregate`，測試也直接從記憶體裡的 aggregate 呼叫 `getDomainEvents()` 讀取事件，永遠不經過重播的路徑。

我當時的紀錄是：A 的 10/16（工作坊的 16 項合規清單過了 10 項）不是「差一點」，而是「在只有一個 InMemory use case 的玩具規模下剛好還沒爆」。

還有一個跟 replay 無關的小洞：測試缺了 `@DirtiesContext`。這是 Spring 用來把受污染的測試 context 移出快取、讓後續測試重新建立 context 的標註。可以想成前一個測試留下的資料，影響了下一個測試；同樣程式因此可能這次通過、下次失敗，形成不穩定的 flaky 測試。是否需要這個標註，要看共用狀態與隔離方式，但只靠 retry 重試到綠，並沒有釐清干擾來源。第八節清單也會追問這件事。

這個例子能說明「綠燈但尚未完成驗收」，也能讓人看見測試與需求走上不同路徑的情況。但這裡檢視的是方法 A 的單次實作，N 等於 1，量測的是合規程度。要討論同一份規格反覆執行時有多大變異，必須另外設計重複執行的實驗，不能從這次結果推論。

回頭看這個例子，我更想釐清的是：每一道 check 到底能幫上什麼忙，又會在哪裡停下來。把能力與限制逐條寫清楚，才知道這份綠燈之外還缺了哪些證據：

- **red-then-green 不適用**：這是 feature PR，新測試對舊 code 一定因為類別不存在而紅。
- **mutation 無法直接驗證缺少的 replay 路徑**：程式碼裡沒有這條路徑，就沒有對應的程式碼可供產生 mutant。
- **補上缺口需要先回到需求**：由人審閱 intent、辨識缺少的行為，再把可重複檢查的要求寫成 constraint test。

這裡沒有實測方法 A 的 mutation score，所以不能把「分數可能很好」當成結果。真正需要保留的判斷是：即使既有 in-memory aggregate 的測試能抓到程式變異，也不能據此證明 replay 已經被實作。mutation 評估的範圍，仍然是拿去產生變異的那份程式碼。

constraint test 那一條的內容會長這樣：aggregate 必須繼承 `EventSourcedAggregate`，或至少一個測試必須經由 rehydrate 建構 aggregate。rehydrate 就是從事件把 aggregate 重建回來的那個動作，也就是規格真正要的那條路徑。這是可靠度篇第二節說的「架構規則」那一類。

人審閱 intent 時，則可以從一句問題開始：「這是 event sourcing 嗎？」

這個例子沒有實測本篇的 test gate，也沒有比較三道閘的效果。它能清楚說明的是：原有測試全過，仍然沒有驗證規格要求的路徑。要補上這個缺口，需要先由人辨識需求與實作的落差，再把能重複檢查的部分寫成 constraint tests。

把規格要的路徑與測試實際走的路徑畫在同一張圖上：

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
    S["規格：Product aggregate<br/>用 event sourcing"] --> C["方法 A 的實作<br/>Product 沒有繼承<br/>EventSourcedAggregate"]
    C --> T["5 個測試全綠<br/>直接讀 in-memory 的<br/>getDomainEvents()"]
    T --> P1["測試走的路徑<br/>記憶體 aggregate → 事件列表"]
    S -.-> P2["規格要的路徑<br/>事件 → rehydrate → aggregate"]
    P2 --> X["從未被執行<br/>沒有任何測試經過 replay<br/>mutation 也量不到"]
    class S human
    class T,P1 buy
    class C,X bad
```

把兩條路徑並排看，5 個測試全綠與 replay 從未執行就不再矛盾：測試確實完成了它們寫下的檢查，只是那些檢查沒有涵蓋需求要的行為。

圖上的虛線標出這個落差。如果審查只順著現有實作與測試閱讀，很容易一直在同一條路徑裡確認細節，卻沒有抬頭問：需求要的另一條路呢？這是我希望留在驗收流程裡的問題。

一旦這個問題被辨識出來，其中一些要求就能寫成新的 check。人的工作不是永遠補在工具後面重查一遍，而是找出目前的檢查還沒有表達出來的需求。

感謝 Teddy 的工作坊，讓這個容易停留在概念裡的落差，成了一份可以回頭檢視的實作經驗。

---

## 八、Tester 的角色：從打勾機器到 test-suite reviewer

工作坊的例子也讓下面這份清單有了用途：幫 tester 從報告裡找到值得追問的地方，再回到需求判斷。它可以提供閱讀順序，卻不能代替讀者確認測試與實作是否對得上；必要時，仍然要打開測試與程式碼仔細看。

使用這份清單時，可以先抓住同一條線：這個答案從哪裡來，測試如何辨識違反它的程式，報告又還沒涵蓋什麼？例如付款測試的答案來自「同一次購買不得重複扣款」，接著查重送的案例與變異結果，最後確認並行、重新啟動等情況是否另有證據。下面十題讓這條閱讀路徑更具體：

| # | 問題 | 對應的 check 或欄位 |
|---|---|---|
| 1 | 期望值從哪裡來？ | PR template 的 golden 來源欄 |
| 2 | 新測試在修正前的程式碼上，是否會因預期的行為差異而失敗？ | red-then-green |
| 3 | 失敗是來自行為差異，還是環境、import 或 fixture 問題？ | red-then-green 的三種結果分類 |
| 4 | 是否有既有斷言被弱化、移除，或測試被停用？ | assertion-change diff |
| 5 | 測試是否只核對 mock 預設的回傳值，沒有驗證產品行為？ | red-then-green、mutation |
| 6 | 哪些 mutant 仍然存活，對應哪些未被測試辨識的變動？ | diff-scoped mutation 報告 |
| 7 | 是否修改覆蓋率的排除範圍（exclude pattern）？ | 覆蓋率設定的變更由人審核 |
| 8 | flaky 測試是否被隔離並追查，還是只重試到通過？ | 〈Harness 藍圖〉：先處理 flaky，再放寬授權 |
| 9 | 測試名稱描述的是行為，還是實作？ | 由人對照需求與測試內容 |
| 10 | 刪掉這個測試後，哪些行為會失去保護？ | 人對照需求，釐清測試是否有效或與其他測試重複 |

前八題可以先由工具提供線索，後兩題更需要回到需求判斷。最後一題尤其值得留著：刪掉一個測試後，哪些行為會失去保護？如果答不出來，可能是測試無效，也可能只是與其他測試重複；下一步是釐清它的用途，不是立刻把它判成「永不紅」。

在 test gate 裡，tester 不只確認測試有沒有執行完畢，也要審閱這份測試如何理解需求。報告能先整理斷言變更、存活的 mutant 與未驗證的範圍；tester 再據此決定哪些地方要補測、哪些要求需要澄清，以及哪些疑點值得用探索式測試繼續追查。

Lisa Crispin 與 Tip House 的《Testing Extreme Programming》說「人人都是測試者」。我在這裡的理解是，合併 agent PR 的人也要對驗收依據負責。可以請工具協助蒐集結果，但不能把「這些測試為什麼足夠」一起交給產出它們的 agent 自己回答。

---

## 九、結語

回到工作坊那個全綠的方法 A。對我來說，這份實作最值得留下的，正是它看起來沒有問題的樣子。A 的測試沒有一個是假的，每一個都真的在跑、真的在斷言，只是全部繞過了規格要的那條路徑。那份綠燈沒有說謊，它只是從來沒有承諾過要涵蓋你以為它涵蓋的東西。

本篇給的三個 check 只做一件事：把「綠燈沒承諾的部分」裡，機器能量測或檢查的部分，逐項呈現在報告裡。assertion-change diff 檢查斷言有沒有被改弱，red-then-green 驗證新測試能否辨識修正前後的差異，diff-scoped mutation 則檢查測試能否發現改動範圍內的變異。這三項 check 未必找得到方法 A 省略的需求路徑，還需要依需求建立 constraint test，以及人對 intent 的審閱。三個都只是更好的 check，不是驗收。

> **agent 寫的測試是它對自己的驗收標準；審它的測試，就是審它以為的「對」。**

測試套件經過這樣的審閱，團隊才比較有依據地討論下一個問題：這個 PR 還需要誰來看、看哪些部分，以及最後由誰核准。〈Review 篇：Review 是控制點，不是瓶頸〉會接著展開這些安排。回到眼前的工作，則可以先從一份已經全綠的測試開始，問它一句：你驗證的，真的是我們原本要做的事嗎？

---

### 系列文章

- [總論：綠燈不是驗收—agent 時代的測試、Review 與可靠度](https://medium.com/p/582f24223eea)
- **一、測試篇（本篇）**
- 二、Review 篇：Review 是控制點，不是瓶頸—分流、reviewer agent 艦隊與閉環禁令（即將發布）
- 三、可靠度篇：SWE-Gate 量測到的 34%—constraint tests、pass^k 與授權擴張的閘門（即將發布）
- 四、付款實作篇：買一瓶無糖純喫綠茶，從 Review 約束走到 mutation score（即將發布）

---

### References

1. Programmers Are Poor and Overconfident Judges of LLM-Generated Assertions — [arXiv 2607.08885](https://arxiv.org/abs/2607.08885)（2026-07-09）〔第三節〕
2. Same Scrutiny, More Time: Eye Tracking on Reviewing LLM-Labelled Code — [arXiv 2606.26505](https://arxiv.org/abs/2606.26505)（2026-06-25）〔第三節〕
3. Test Coverage Analysis of Agentic Pull Requests — [arXiv 2607.18057](https://arxiv.org/abs/2607.18057)（2026-07-20）〔第二、六節〕
4. Can escalation channels redirect reward hacking toward defect disclosure? — [arXiv 2608.29460](https://arxiv.org/abs/2608.29460)（2026-08-29）〔第五節〕
5. SWE-Gate — [Passing Functional Tests Is Not Enough for Software Engineering Agents](https://arxiv.org/abs/2609.04167)（arXiv 2609.04167，2026-09-03）〔總論第三節；本篇第一節一句〕
6. Robert C. Martin（@unclebobmartin）— [2026-07-26 測試種類](https://x.com/unclebobmartin/status/2081332683582427641)〔第一節〕、[2026-07-29 量測程式碼品質，而不是只要求它保持乾淨](https://x.com/unclebobmartin/status/2082497764223492161)〔第五節〕、[2026-07-30 TDD is a human discipline](https://x.com/unclebobmartin/status/2082850576832905657)〔第四節〕、[2026-08-17 negative test experiment](https://x.com/unclebobmartin/status/2089449442089025936)〔第四節〕
7. Martin Fowler（@martinfowler）— [2026-08-11 TDD inside the agent loop](https://x.com/martinfowler/status/2087173563144912985)〔第四節〕
8. 社群討論：Scrum Community in Taiwan（Lada Kesseler 的轉貼、「AI 說沒問題」）；DevOps Taiwan（Uncle Bob 的 mutation gate 討論串）
9. 筆者筆記：LeSS in Action 的 A-TDD 課程筆記；模式語言驅動開發工作坊（2026-08）的 A/B 實作紀錄〔第七節〕；《Testing Extreme Programming》書摘〔第八節〕
10. Agentic Engineering：[技術篇：Harness 藍圖](https://fantasybz.medium.com/agentic-engineering-%E4%B8%89%E9%83%A8%E6%9B%B2-%E4%BA%8C-harness-%E8%97%8D%E5%9C%96-%E6%8A%8A%E7%B3%BB%E7%B5%B1%E8%AE%8A%E6%88%90-agent-%E8%AE%80%E5%BE%97%E6%87%82%E7%9A%84%E5%9C%B0%E6%96%B9-f2a139f5b561)第五節（flaky quarantine）
11. 李博杰《深入理解 AI Agent：設計原理與工程實踐》v2.0 — [第七章〈Agent 的評估〉](https://bojieli.github.io/ai-agent-book/book-en/chapter7/)（2026-09-06，§7.5.2 失敗歸因的 Coding Agent 錯誤分類表）〔第二節〕
12. Quartic.ai — [Letting an Agent Upgrade Production Kubernetes — Without Getting Paged at 3 AM](https://sched.co/2QlD9)（AGNTCon + MCPCon Japan 2026，2026-09-10；[講者投影片](https://hosted-files.sched.co/agntconmcpconjapan26/d9/AGNTCon-MCPCon-Japan-2026_Abhijeet_Sanskar_final.pdf#page=29) slide 29）〔第五節〕
13. Spring Framework 官方文件 — [@DirtiesContext](https://docs.spring.io/spring-framework/reference/testing/annotations/integration-spring/annotation-dirtiescontext.html)，說明測試 context 的失效、移除與重建〔第七節〕。
14. 隨文實作 — [無糖純喫綠茶付款、constraint tests 與七個指定 mutant](https://github.com/fantasybz/medium-articles/tree/main/examples/tea_payment)〔第四節；教學案例與實測，非真實金流〕

---

### AI 協作說明

本文由筆者提出初步構想與章節架構，文字撰寫由 AI（Claude）協作完成，再經筆者逐節校閱與修訂後定稿。文中觀點與判斷為筆者所持，文責亦由筆者自負。

---

*本文發表於 [Medium @fantasybz](https://medium.com/@fantasybz)。若你正在幫團隊裝第一道 test gate，歡迎交流。*
