# 綠燈不是驗收：agent 時代的測試、Review 與可靠度

> **TL;DR** — 導入 coding agent 半年後，多數團隊撞到同一組症狀：CI 綠了、review 排隊、上線出事。三件事是同一個問題—當測試也是 agent 寫的，綠燈只證明它通過了自己出的題。用 James Bach 的話說，那是 *checking*，不是 *testing*。本文提出驗證層的三道閘：test gate 量測試留下了什麼（mutation score），review gate 決定什麼值得人讀、誰審誰，reliability gate 用 constraint tests 與 pass^k 決定授權能不能擴張。三個你可以不同意的主張：改到 payment 的 PR，一旦 constraint tests 與 mutation 報告到位，人讀 intent 與 constraint 報告，不讀 diff；AI 的 approve 不計入 branch protection，不管哪一家；AGENTS.md 寫 TDD 可以，拿 TDD 的形狀當閘門不行。數字都標領域—「34% 的綠燈修補違反 reviewer 約束」是 SWE-Gate 在 75 個 Python repo 上量到的。文末附 90 天藍圖。

> 系列導覽：**總論（本篇）** → 一、測試篇（即將發布） → 二、Review 篇（即將發布） → 三、可靠度篇（即將發布）。上一季：[別急著打造你的 Devin](https://fantasybz.medium.com/%E5%88%A5%E6%80%A5%E8%91%97%E6%89%93%E9%80%A0%E4%BD%A0%E7%9A%84-devin-agentic-engineering-%E7%9A%84%E7%B5%84%E7%B9%94%E7%AD%96%E7%95%A5%E8%88%87-90-%E5%A4%A9%E8%A1%8C%E5%8B%95%E8%97%8D%E5%9C%96-7342ababc417) → [組織篇](https://fantasybz.medium.com/agentic-engineering-%E4%B8%89%E9%83%A8%E6%9B%B2-%E4%B8%80-%E8%AA%B0%E4%BE%86%E5%81%9A-platform-federation-%E7%9A%84%E7%B5%84%E7%B9%94%E8%A8%AD%E8%A8%88%E5%AF%A6%E5%8B%99-9d9353ef7f3a) → [技術篇](https://fantasybz.medium.com/agentic-engineering-%E4%B8%89%E9%83%A8%E6%9B%B2-%E4%BA%8C-harness-%E8%97%8D%E5%9C%96-%E6%8A%8A%E7%B3%BB%E7%B5%B1%E8%AE%8A%E6%88%90-agent-%E8%AE%80%E5%BE%97%E6%87%82%E7%9A%84%E5%9C%B0%E6%96%B9-f2a139f5b561) → [營運篇](https://fantasybz.medium.com/agentic-engineering-%E4%B8%89%E9%83%A8%E6%9B%B2-%E4%B8%89-eval-%E5%96%AE%E4%BD%8D%E7%B6%93%E6%BF%9F%E8%88%87%E8%A6%8F%E6%A8%A1%E5%8C%96-%E6%8A%8A-agent-%E7%95%B6%E7%94%A2%E5%93%81%E7%87%9F%E9%81%8B-d6d9623c2dc6)

---

## 一、每個 Engineering VP 都在問的問題：「AI 說沒問題」之後，我該相信什麼？

三個情境，導入 coding agent 半年以上的團隊多半經歷過至少一個。

第一個：你問 RD 這個 PR 測過了嗎，他回「AI 說沒問題」。Scrum Community 裡把這個問題講得最短的一則貼文講的就是這件事—回答的人不是偷懶，他是真的不知道除了相信 agent 之外還能看什麼。

第二個：你叫 agent 修一個 failing test，它修好了。回頭看 diff，`assertEqual` 變成 `assertIn`，`== 3` 變成 `>= 1`。測試綠了，bug 還在。

第三個：上線後出事，回頭看那個 PR，approve 的是 reviewer agent。人沒有讀過它。

三個情境的共同點只有一個：**唯一的證據來自 agent 自己**—它寫的測試、它說的話、它給的 approve。「測試全過」「已完成」「LGTM」都是 agent 對自己出的題做的 checking，組織卻把它們當成了驗收。

一個前提要先講清楚。CI 綠燈是環境跑出來的量測，不是 agent 的陳述；它變成「自我申報」只在一個條件下成立—那些測試是 agent 自己寫的或改過的，出題者與考生是同一個。沒有研究量過 agent PR 裡有多少比例含 agent 寫的測試，所以「**測試多半是 agent 寫的**」在本系列是筆者的前提，不是事實：條件不成立的 repo 不適用；第 1 個月先量你的比例。

一句話的回答，形狀刻意讓你第一節就有東西可以不同意：

> **Green is checking. Acceptance is testing.** 所以改到 payment 的 PR，一旦 constraint tests 與 mutation 報告到位，人就不該再讀 diff，該讀 intent 與 constraint 報告；在那之前，人讀 diff 的每一條評論都要回收成 constraint test。AI 的 approve 不計入 branch protection，不管哪一家。AGENTS.md 寫 TDD 可以，拿 TDD 的形狀當閘門不行。

---

## 二、書錨：Bach 的 testing 與 checking

去年在天瓏買了 James Bach 的《Taking Testing Seriously》，在粉絲團引過一句：「Testing is the opposite of faith in the product. Testing begins with faith in the existence of trouble.」有讀者回覆說，tester 現在用 vibe coding 做丟棄式的測試工具—正是本系列的立場：agent 是 tester 的工具，不是替代。

Bach 對 *checking* 的定義：「Checking is the mechanistic process of verifying propositions… testing cannot be automated, but checking can.」CI 是 checking 的自動化；agent 說「測試全過」，是它對自己命題的 checking—測試也是它寫的，連命題都是它出的。

**證據的三分法**，定義在此，後三篇沿用：

- (a) **agent 的陳述**：「已完成」「測試全過」「LGTM」。
- (b) **agent 寫的或改過的測試**：綠了，只證明它通過了自己出的題。
- (c) **團隊擁有的測試與 constraint tests**：環境的量測，agent 改不動。

只有 (c) 算證據；(a) 與 (b) 的差別，只在 (b) 有 CI 幫它按 enter。三分法要撐得住一個反問：agent 對 repo 有寫入權，(c) 憑什麼改不動？兩條機制。**升格規則**：agent 寫的測試通過 test gate（斷言沒有弱化、mutation 有殺傷力）**而且被人類 approve 進 main**，才從 (b) 升格為 (c)—分類看「誰為它負責過」，不是「誰打的字」。**改不動**：`tests/constraints/` 與 golden set 目錄的 CODEOWNERS 只列人類，(c) 類測試的任何弱化直接阻擋；實作在可靠度篇。

用語也在這裡定調：mutation score、constraint tests、pass^k 都是**更好的 check**；testing—帶著「一定有問題」的信念去看—還是人的工作。

誠實聲明：這本書我還沒有從頭讀到尾，引用集中在定義 testing 與 checking 的那一章，以及 Bach 的一篇訪談；有誤讀是我的問題。

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
    subgraph chk["Checking：機械地驗證命題"]
        direction TB
        C1["CI 綠燈<br/>覆蓋率門檻"] ~~~ C2["agent 對自己寫的測試<br/>說「全過」「已完成」"]
        C2 ~~~ C3["mutation、constraint tests<br/>pass^k：更好的 check"]
    end
    subgraph tst["Testing：帶著「一定有問題」<br/>的信念去學習與評估"]
        direction TB
        T1["讀 intent 與 constraint 報告<br/>問「這個期望值從哪來」"] ~~~ T2["對產出做探索式測試"]
        T2 ~~~ T3["做出 timely 的業務決策<br/>merge、擴張授權、不擴張"]
    end
    chk -.->|不等於| tst
    class C1,C2 buy
    class C3 own
    class T1,T2,T3 human
```

---

## 三、2026 年，數據怎麼說：綠燈量不到的三層

每個數字都標領域、樣本數與日期；一層只放一篇 in-domain 的錨點。

| 層 | 主張 | 錨點（in-domain） | 更多證據 |
|---|---|---|---|
| 功能測試過 ≠ 約束滿足 | 綠燈只檢查了 reviewer 在乎的一部分 | SWE-Gate：644 個通過功能測試的修補，221 個（34%）違反從真實 PR 評論導出的約束（75 個 Python repo、303 個任務，2026 年 9 月） | 可靠度篇 |
| 有測試 ≠ 測到 | agent 改的程式碼有多少被測試碰到 | Test Coverage of Agentic PRs：4,882 個 agent PR，repo 原有測試只碰到 agent 改動行的 61.5%（Java）與 27.0%（Python）（2026 年 7 月） | 測試篇 |
| 一次成功 ≠ 可靠 | pass@1 與 pass^k 是兩個數字 | 用你自己的 golden set 跑 k 次（定義在第八節） | 可靠度篇 |

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
    G{"CI 綠燈"}
    subgraph layers["三層，各一個 in-domain 錨點"]
        direction LR
        L1["功能測試過 ≠ 約束滿足<br/>綠燈只檢查了 reviewer<br/>在乎的事的一部分"] --> S1["SWE-Gate：644 個綠燈修補<br/>34% 違反 reviewer 約束<br/>75 個 Python repo"]
        L2["有測試 ≠ 測到<br/>agent 改的程式碼<br/>有多少被測試碰到"] --> S2["Test Coverage of Agentic PRs<br/>既有測試覆蓋 agent 改動行<br/>Java 61.5%、Python 27.0%"]
        L3["一次成功 ≠ 可靠<br/>pass@1 與 pass^k<br/>是兩個數字"] --> S3["你自己的 golden set<br/>pass@1 與 pass^k 分開報<br/>算法見可靠度篇"]
    end
    G --> layers
    layers --> C["你現在量的東西<br/>量不到這三層"]
    class G buy
    class L1,L2,L3 bad
    class S3 own
```

人眼也不是安全網：一項讓 86 位開發者判斷 LLM 寫的斷言的研究發現，正確的斷言他們有 74% 看得出來，錯誤的只有 49%，信心卻沒有跟著降（Poor and Overconfident Judges，2026 年 7 月）。第七節會用這個數字決定人該讀什麼。

再加一個我自己的：模式語言工作坊裡親手跑出來的實例—5 個測試全綠，event sourcing 的 replay 路徑從未執行過；細節在測試篇。

結論不是「agent 不可信」，是**你現在量的東西，量不到這三層**。

---

## 四、測試史已經演過一次

上一季用 DevOps 2014–2016 當歷史脊椎；這一季換一條線，因為題目本來就是測試的地盤。

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
    subgraph past["測試史／CD 史"]
        direction TB
        P1["1976 Fagan inspection<br/>人逐行讀"] --> P2["1978 mutation testing<br/>等四十年才夠便宜"]
        P2 --> P3["2009 Bach／Bolton<br/>checking ≠ testing"]
        P3 --> P4["2010 deployment pipeline<br/>commit 綠 ≠ release"]
    end
    subgraph now["2026 agent 驗證層"]
        direction TB
        N1["人讀 intent 與 constraint<br/>機器讀 diff"] ~~~ N2["diff-scoped mutation<br/>第一次有經濟理由當閘門"]
        N2 ~~~ N3["綠燈是 checking<br/>agent 說「全過」也是"]
        N3 ~~~ N4["test → review → reliability<br/>你的 90 天裝三道閘"]
    end
    past --> now
    class N1 human
    class N2,N4 own
    class N3 buy
```

重點只有兩條。第一，Humble & Farley 的 deployment pipeline 早就說 commit stage 綠了不是 release，後面還有 acceptance、capacity、manual 各 stage；agent 時代只是把「後面幾個 stage」重新發明成 test、review、reliability 三道閘。第二，mutation testing 等了四十年的經濟理由，agent 給了—當「寫測試」變成免費，「測試有沒有用」就成了唯一值錢的問題。

一句話：**歷史沒有教我們新東西，只是把我們以前偷懶沒做的那幾個 stage 帳單寄來了。**

---

## 五、別教 agent 怎麼測，量它留下了什麼

Uncle Bob 今年夏天在 X 上把立場講完了：TDD 是人類的紀律，他不期待 agent 遵守（7 月 30 日）；你沒辦法叫 agent「保持乾淨」，只能量它的乾淨程度再叫它修（7 月 29 日）。

Böckeler 的文章（Fowler 8 月 11 日轉貼）把「TDD inside the agent loop—theater or actual value?」當成經驗問題來問。本文的立場是第三個可反駁的主張：儀式的價值不是零—它會改變 agent 的探索路徑—所以 AGENTS.md 寫「請用 TDD」可以；但**拿 TDD 的形狀當閘門不行**，閘門只量產出。

Uncle Bob 8 月 17 日的 negative test experiment 講得最清楚：8 次 run、四種測試紀律、有無 CRAP 門檻，**全部通過同樣的 25 個驗收案例，寫出來的程式卻不一樣**。驗收測試全綠，不能區分品質—SWE-Gate 的個人版。

台灣的討論已經走到同一個地方。Scrum Community 有一則貼文說得準：把人類的「價值」要求 AI 是對的，把人類的「做事習慣」硬套在 AI 身上是錯的。差的只是還沒有人把閘門寫出來。

| 你想要的 | 指示型做法（不當閘門） | 量測型做法（當閘門） |
|---|---|---|
| 測試有效 | AGENTS.md：「請用 TDD」 | mutation score ≥ 門檻（只算 agent 改動的行） |
| 不改壞既有測試 | 「不要修改既有斷言」 | CI 檢查：既有斷言被弱化 → 阻擋；bug fix PR 另跑 red-then-green |
| 遵守 reviewer 的約束 | 「請遵守團隊規範」 | constraint tests（review 評論 → 規則 → 可執行檢查） |
| 誠實回報 | 「如果測試有問題請告訴我」 | 結構化的 escalation tool（`report_broken_test`） |
| 可靠 | 「請仔細檢查」 | pass^k 在 golden set 上 ≥ 門檻 |

右欄每一格都是一個 check，不是一個 prompt—這是本文對「指示」與「量測」的全部立場。

---

## 六、驗證層的三道閘

把前面五節收成一張圖。左邊是 agent 那一側：產出 PR、寫測試、CI 綠燈、失敗重試、說「已完成、測試全過」，每一件都是 checking。右邊是驗收這一側的三道閘，merge 與擴張授權只從右邊出去。

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
    subgraph gen["Agent 這一側：checking"]
        direction TB
        A["Agent 產出 PR"] --> B["agent 寫的測試"]
        B --> G{"CI 綠燈"}
        G -.->|失敗，重試| A
        G --> S["「已完成、測試全過」"]
    end
    subgraph ver["驗收這一側：三道閘"]
        direction TB
        T["Test gate<br/>mutation、assertion diff"] --> R["Review gate<br/>人讀 intent 與 constraint"]
        R --> L["Reliability gate<br/>pass^k、constraint 通過率"]
        L --> M["merge／擴張授權"]
    end
    gen --> ver
    class B,G,S buy
    class T,L own
    class R human
```

每道閘回答一個問題、量一個東西、由一個角色擁有：

| 閘 | 問題 | 量什麼 | Owner | 深掘 |
|---|---|---|---|---|
| Test gate | 這份測試能抓到 bug 嗎？ | mutation score、assertion-change diff、red-then-green | QA / test lead + platform | 測試篇 |
| Review gate | 這個 PR 值得誰讀、讀什麼？ | 分流矩陣、reviewer 異質性、approval artifact | EM + senior | Review 篇 |
| Reliability gate | 這種任務可以放多少授權？ | constraint pass rate、pass^k、oversight budget | platform + VP | 可靠度篇 |

三道閘的設計哲學是同一句：**設計環境比寫規則有效**。一項研究給 agent 一個正式的「回報壞測試」出路，它 reward hacking（讓測試過而不是修對 bug，改斷言是其中一種）的比例就掉到原本的四分之一左右—23.6% 到 5.3%，8 個 frontier model 裡 6 個完全消失（escalation channels，2026 年 8 月；工具 schema 在測試篇）。agent 不是想騙你，是你只給了它一條路。

---

## 七、Review 是控制點，不是瓶頸

Martin Fowler 9 月 2 日轉了一篇「Maybe we shouldn't be reviewing all this code」，它的說法是：問題不是 AI 弄壞了 code review，是我們一直拿 review 解決錯的問題。本文的版本：**review 的重設計不是讓人讀得更快，是決定什麼值得人讀。** [上一季總論](https://fantasybz.medium.com/%E5%88%A5%E6%80%A5%E8%91%97%E6%89%93%E9%80%A0%E4%BD%A0%E7%9A%84-devin-agentic-engineering-%E7%9A%84%E7%B5%84%E7%B9%94%E7%AD%96%E7%95%A5%E8%88%87-90-%E5%A4%A9%E8%A1%8C%E5%8B%95%E8%97%8D%E5%9C%96-7342ababc417)第四節點名的「Review 成為新瓶頸」，這一季修正為：瓶頸是症狀，病因是把人放在錯的閘門上讀錯的東西。

兩個數字，一個講規模、一個講關聯。規模：一項橫跨三個世代、一百萬個 PR 的縱向研究（From Human-Centric to Agentic Code Review，2026 年 7 月）發現，agent 發起與多 agent review **在某些採用模式下**讓決策更快，但效率沒有轉成 review 品質—更快，沒更好。關聯：另一項追蹤 182 個 repo 的縱向研究（Post-merge fate of agentic code，2026 年 7 月）發現 agentic code 需要顯著更多的矯正性維護；免審合併率每高 10 個百分點，agentic 維護負擔約高 6%—原句是 "is associated with"，相關不是因果，但足夠讓免審合併率成為要量的指標。另一項 2026 年 7 月的研究還發現，真實外洩的 secret 大多在 merge 前沒被抓到—數字在 Review 篇。

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
    nodeSpacing: 96
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
    A["agent 產出的 PR"] --> R{"review gate<br/>組織的控制點"}
    R -->|管住| G1["加分<br/>矯正性維護下降"]
    G1 --> G2["review 評論回收成<br/>constraint tests"]
    R -->|放掉| B1["負債<br/>免審合併率每 +10pp<br/>維護負擔約 +6%（關聯）"]
    B1 --> B2["外洩 secret 多半<br/>在 merge 前沒被抓到"]
    G2 & B2 --> M["免審合併率進月報<br/>當成要管的指標"]
    class R human
    class G1,G2 own
    class B1,B2 bad
    class M buy
```

那麼，人讀 payment 的 diff 為什麼不是安全網？第三節的數字：人對錯誤斷言的判斷準確率 49%，信心與判斷正確時差不多。所以在高 blast radius 的格子裡，人讀 diff 抓到的東西要回收成 constraint test；報告到位的那天，就換成讀 intent 與報告。這個 PR 誰要讀，取決於 blast radius 與有沒有報告可以替人讀。人只在兩格讀：

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
    P["agent 開的 PR"] --> Q1{"blast radius 高？<br/>auth／payment／schema／infra"}
    Q1 -->|是| Q2{"有 constraint tests<br/>與 mutation 報告？"}
    Q1 -->|否| Q3{"有 constraint tests<br/>與 mutation 報告？"}
    Q2 -->|有| O1["人讀 intent 與報告<br/>不讀 diff、approve 綁人"]
    Q2 -->|沒有| O2["人讀 diff<br/>約束回收成 test"]
    Q3 -->|有| O3["機器全審（異質）<br/>人依預算抽樣"]
    Q3 -->|沒有| O4["先補 check<br/>再談 review"]
    class O1,O2 human
    class O3 own
    class O4 buy
```

四個出口就是 Review 篇分流矩陣的四格；矩陣全表、reviewer 艦隊、AI 審 AI 的禁止條件、approval artifact 怎麼綁人，全部留給 Review 篇。

---

## 八、可靠度不是能力：pass@1、pass^k 與 oversight budget

先把定義釘死：

- **pass@1**：每個 case 單次嘗試的成功率（跑 k 次取平均）。
- **pass^k**：k 次全部成功的 case 比例。
- 兩者都先 per case 算，再對 golden set 取 aggregate。「至少一次成功」是 pass@k，本系列不用它。

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
    C["同一個 golden case<br/>跑 k = 5 次"]
    subgraph runs[" "]
        direction LR
        r1["run 1 過"] ~~~ r2["run 2 過"] ~~~ r3["run 3 過"]
        r4["run 4 紅"] ~~~ r5["run 5 過"]
    end
    C --> runs
    runs --> P1["該 case 的 pass@1<br/>= 4 次過／5 次 = 80%"]
    runs --> P5["該 case 的 pass^5 = 0<br/>5 次裡有一次紅就不算全過"]
    class r1,r2,r3,r5 own
    class r4 bad
    class P5 buy
```

兩者可以差很多；code 領域沒有現成的數字，用你自己的 golden set 量—營運篇的 20–50 個 golden case，跑 k = 5 到 10。

第三個數字是人力，這裡借一個 **code 以外的旁證**—概念用、數字不移植。READY 是一個企業 agent 部署的資格審查框架（2026 年 9 月），案例是臨床稽核工作流、16 個 agent 系統、750 個 case：兩個系統的自主準確率 72.8% 與 72.5%，只差 0.3 個百分點；要達到同一個 76% 的可靠度目標，所需人工複核比例卻分別是 39.2% 與 29.6%—準確率高的那一個要更多人看。**「準確率排名」與「你要付多少人力」不是同一個排名。** 「人工複核比例由可靠度目標反推」，本系列叫它 oversight budget，演算法在可靠度篇（下圖為 READY 的兩個系統，非 code 旁證）：

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
    subgraph sa["系統 A：準確率高 0.3pp"]
        direction TB
        A1["自主準確率 72.8%<br/>（比 B 高 0.3pp）"] --> A2["可靠度目標 76%<br/>（兩系統相同）"] --> A3["需人工複核 39.2%<br/>（比 B 多近 10pp）"]
    end
    subgraph sb["系統 B：人力少近 10pp"]
        direction TB
        B1["自主準確率 72.5%<br/>（比 A 低 0.3pp）"] --> B2["可靠度目標 76%<br/>（兩系統相同）"] --> B3["需人工複核 29.6%<br/>（比 A 少近 10pp）"]
    end
    sa ~~~ sb
    class A2,B2 human
    class A3 bad
    class B3 own
```

給 leadership 的月報，用三個數字取代單一的「通過率」：

| 數字 | 回答 | 不能拿來做什麼 |
|---|---|---|
| pass@1（golden set） | 能力有沒有進步 | 決定授權 |
| pass^k（golden set，k = 5–10） | 這類任務可以放多自主 | 跟別家的 benchmark 比 |
| constraint pass rate（SWE-Gate 式） | 綠燈之外還違反了什麼 | 取代 review |

接回營運篇的 G2：授權擴張看 pass^k 與 escape rate，不看 pass@1。上一季說「roadmap 寫 Q3 全面導入，不構成 G2 自動過關的理由」；這一季給它四個可量的條件—pass^k、constraint violation rate、mutation score floor、oversight budget—全表在可靠度篇。

---

## 九、八個反模式

前面各節一個個碰過，這裡收成症狀清單：

| # | 反模式 | 你會在哪裡看到它 |
|---|---|---|
| 1 | **綠燈即驗收** | 「CI 過了、覆蓋率 90%，可以上」 |
| 2 | **TDD 儀式** | AGENTS.md 寫「請先寫測試」，看到 TDD 形狀的 commit 就放心 |
| 3 | **斷言鬆綁修復** | 修 failing test 時把 `assertEqual` 改成 `assertIn`、加 `@skip`、刪 `assertRaises` |
| 4 | **凍結 bug 的 golden** | 把現狀輸出錄成 snapshot / golden file，bug 從此被測試保護 |
| 5 | **覆蓋率當品質** | 以覆蓋率門檻放行 agent PR；exclude pattern、空斷言都能把數字做出來 |
| 6 | **閉環 review** | 同一個 model、同一個 session 審自己的 PR；或 AI approve 就算過 |
| 7 | **讀 diff 的人** | senior 逐行讀 agent diff，PR 排隊，最後 rubber stamp |
| 8 | **只報 pass@1** | 對 leadership 報「eval 通過率 85%」並據此擴大授權 |

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
    R["綠燈不是驗收<br/>八個反模式"]
    subgraph gt["Test gate（測試篇）"]
        direction TB
        t1["TDD 儀式"] ~~~ t2["斷言鬆綁修復"] ~~~ t3["凍結 bug 的 golden"] ~~~ t4["覆蓋率當品質"]
    end
    subgraph gr["Review gate（Review 篇）"]
        direction TB
        r1["閉環 review"] ~~~ r2["讀 diff 的人"]
    end
    subgraph gl["Reliability gate（可靠度篇）"]
        direction TB
        l1["綠燈即驗收"] ~~~ l2["只報 pass@1"]
    end
    R --> gt
    R --> gr
    R --> gl
    class t1,t2,t3,t4,r1,r2,l1,l2 bad
```

閉環 review 帶一個規模數字：跨產品的 AI 審 AI—不同家的 reviewer 審 agent 的 PR—只佔 agent PR 約 1.6%，但 2025 年 Q1 到 Q3 成長超過 100 倍（AI-to-AI Code Reviews，248,641 個 PR，2026 年 8 月）。它量的是跨產品配對；同 model 同 session 的閉環有多大，沒人量過，你要自己量。

筆者在台灣社群最常看到的是 5 與 6—觀察，非統計：覆蓋率是既有 CI 最容易接上的門檻；訂閱制的席位經濟讓「用同一個訂閱審自己」最便宜。

---

## 十、如果我是 Engineering VP / QA lead，我會怎麼決策

我**不會**核准：

> 「把 QA 團隊轉型成 prompt 團隊。」
> 「用 AI review 清掉 review backlog，AI approve 即可 merge。」
> 「以 eval 通過率 85% 為據，Q4 開放所有 team 的 write tools。」

我**會**核准四件事：

1. 一個 pilot repo 裝 mutation gate，只算 agent 改動的行。門檻用**我的建議值（不是業界標準）**：mutation score ≥ 70%，低於就回 agent 補測試，不是給人讀。
2. 從最近 90 天被打回的 agent PR 抽 50 條 review 評論，分類、挑出可執行的，寫成前 10 條 constraint tests。沒有評論歷史的 repo，從最近 5 個 incident 的 postmortem 導出前 5 條—這是主路線，不是退路：每一條「以後不准再發生」本來就是約束。
3. reviewer agent 必須是**不同 vendor、或至少不同 session** 的 instance；AI 的 approve 永遠不計入 required approvals，用 GitHub 現有機制做到—CODEOWNERS 只列人類加 Require review from Code Owners，或 required status check 數人類的 approve—設定節錄在 Review 篇。
4. approval artifact 綁人類身分與被審內容的 hash；高 blast radius 的 PR，任務指派者不可 approve。vendor 條款對「誰能 approve agent 的 PR」互相矛盾（Where Accountability Lives，2026 年 8 月），細節留給 12 月的追責篇。

**驗證預算怎麼想。** 一項在 1,116 個 web app、6 個 model、8 種工具配置上做的研究（The reach of a verification tool decides its value，2026 年 8 月）給了我一個框架：驗證工具的價值由觸及範圍決定—只檢查能不能啟動的 boot probe，用 shell 約 35% 的 token 成本就移除了幾乎所有啟動失敗，完整 shell 是 2.35 倍成本。所以先買觸及範圍最大的 check（constraint tests、assertion-change diff），再買要執行測試的（red-then-green、mutation），最後才買貴的（k 次重跑、step-rubric judge）。

**我的建議值，機器對機器**：每 1 元的 agent token 加生成側 CI，配 0.3 到 0.5 元的驗證側 compute—分母是 agent 產出的機器成本，分子是驗證它的機器成本。**人工複核的時間不在這個比例裡**，它走可靠度篇的 oversight budget，兩筆分開向 CFO 報。

**50 / 200 / 1,000 人怎麼裝。** G2 講的是授權擴張，不是閘門從一個 repo 推到四十個，所以另給一張表：

| 規模 | 驗證層怎麼裝 | 誰擁有 |
|---|---|---|
| 50 人（5–10 個 repo） | 只裝 constraint tests + assertion-change diff；mutation 不開—沒人看報告 | platform 兼任；沒有 QA lead 就是最資深的 reviewer |
| 200 人（30–50 個 repo） | 四道 check 進 paved road 的 CI template；新 repo 預設開，舊 repo 依 brownfield 順序開；reviewer fleet 一份設定檔集中定義 | QA lead 擁有 test gate；EM 擁有 review gate 的分流矩陣 |
| 1,000 人 | test gate 由 platform 當產品營運（版本、SLA、dashboard）；reviewer fleet 集中管理、各 BU 選配；oversight 抽樣比例各 BU 自算 | platform 產品 owner + 各 BU 的 QA lead |

**Brownfield：先裝哪道閘。** 台灣讀者的實況多半是 15 年的 legacy monolith：測試套件跑 40 分鐘、覆蓋率 30%、沒有 review 評論歷史可挖。我的安裝順序，每一步只依賴自己那一格的前提：

| 順序 | 閘 | 為什麼先 | 前提 |
|---|---|---|---|
| 1 | **constraint tests** | 不需要既有測試；原料從團隊規範與 incident postmortem 出發（見上第 2 項） | 零 |
| 2 | **assertion-change diff** | 純 diff 分析，零執行成本，40 分鐘的套件不用跑 | 零 |
| 3 | **red-then-green（bug fix PR）** | 只對受影響的測試子集跑—改到哪個 module 就跑哪個 module 的測試 | 能算受影響子集：test selection 或目錄對應 |
| 4 | **diff-scoped mutation** | 最貴，最後裝 | 受影響子集 10 分鐘內跑完 |

這四個 check 對人寫的 PR 一樣有用—斷言鬆綁、凍結 bug、違反團隊約束，都不是 agent 發明的。**即使 agent 路線失敗，這幾道閘也不會白裝。**

---

## 十一、90 天的驗證層行動藍圖

第 1 個月要量的 baseline 有六個：上一季已在量的 escape rate 與 review minutes / PR，加四個新數字—既有斷言被弱化的 PR 比例、snapshot 或 golden file 更新未附理由的比例、既有測試覆蓋 agent 改動行的比例、新增或修改的測試檔由 agent 寫的比例（最後一個量的是本系列的前提）。

| 階段 | 目標 | 退出條件 |
|---|---|---|
| **第 1 個月** | 量六個 baseline（見上）；pilot repo 裝 assertion-change diff 與 diff-scoped mutation，red-then-green 只開 bug fix PR；抽 50 條 review 評論分類（第十節第 2 項） | 四個新數字有 baseline；mutation 報告出現在 PR 上（先不阻擋） |
| **第 2 個月** | 前 10 條 constraint tests 進 CI；reviewer agent 換成異質 instance；PR template 加 intent 與 constraint 欄；**AI approve 不計入 required approvals**；agent 拿到 escalation tool | 至少一次 constraint test 擋下綠燈 PR；斷言弱化比例下降 |
| **第 3 個月** | golden set 跑 k = 5 算 pass^k；用新的 G2 條件做一次授權去留決策；三個數字進 leadership 月報 | 月報有 pass@1 / pass^k / constraint pass rate 三欄，**且有人據此做過一次授權去留決策並公開理由**—擴張或不擴張都算 |
| **第 4–6 個月** | 以 repo 為單位重複：先推 agent PR 佔比最高的 repo，依 brownfield 順序開；200 人以上把四道 check 進 paved road 的 CI template | 每月至少一個新 repo 走完第 1–2 個月；免審合併率進月報 |

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
    M1["第 1 個月<br/>量 baseline、pilot repo 裝<br/>assertion diff、mutation 報告"] --> E1["退出：四個數字有 baseline<br/>mutation 報告出現在 PR 上"]
    M1 --> M2["第 2 個月<br/>10 條 constraint tests 進 CI<br/>異質 reviewer、AI 不計入"]
    M2 --> E2["退出：constraint test 擋下過<br/>一個綠燈 PR；斷言弱化下降"]
    M2 --> M3["第 3 個月<br/>golden set 跑 k = 5 算 pass^k<br/>三個數字進月報"]
    M3 --> E3["退出：月報三欄到位<br/>做過一次公開理由的授權決策"]
    M3 --> G["G2 授權去留決策<br/>擴張或不擴張都算"]
    class E1,E2,E3 own
    class G buy
```

兩個提醒：

1. **mutation gate 先報告、後阻擋**，直接阻擋會被拆掉。同理，red-then-green 只對修改既有行為的 PR 開—新測試要對修補前的 code 因為對的理由紅；對 feature PR 也開，每個 feature PR 都會因「類別不存在」而紅，一樣被拆掉。feature PR 的新測試交給 mutation。
2. **constraint tests 先從「可執行而且爭議最少」的規則開始**：不新增依賴、不新增 public API、log 格式；不要從架構規則開始。

---

## 十二、結語

回到 Bach：checking 可以自動化，testing 不能。agent 把 checking 的成本壓到接近零，反而讓 testing 變成組織裡最稀缺的東西。一個有日期的預測，明標是筆者的：到 2027 年，reliability gate 會成為 G2 的標配，「只報 pass@1」會像今天「只看覆蓋率」一樣讓人皺眉。

> **測試是 agent 寫的，綠燈就只是它通過了自己出的題。別教它怎麼測，去量它留下了什麼—然後把人放到該讀的地方。**

11 月的主題「同一份規格跑十次」，會把 pass^k 往 harness 的變異數再推一步。

---

### 系列文章

本文是「綠燈不是驗收」系列的總論，三篇深掘各把一道閘講到可以開工的深度：

1. **總論（本篇）**：checking 與 testing、綠燈量不到的三層、三道閘、VP 決策清單、brownfield 安裝順序與 90 天藍圖
2. 一、測試篇：怎麼審一份 agent 寫的測試—斷言鬆綁、凍結 bug 與 mutation score（即將發布）
3. 二、Review 篇：Review 是控制點，不是瓶頸—分流、reviewer agent 艦隊與閉環禁令（即將發布）
4. 三、可靠度篇：SWE-Gate 量到的 34%—constraint tests、pass^k 與授權擴張的閘門（即將發布）

上一季「Agentic Engineering 三部曲」：[總論](https://fantasybz.medium.com/%E5%88%A5%E6%80%A5%E8%91%97%E6%89%93%E9%80%A0%E4%BD%A0%E7%9A%84-devin-agentic-engineering-%E7%9A%84%E7%B5%84%E7%B9%94%E7%AD%96%E7%95%A5%E8%88%87-90-%E5%A4%A9%E8%A1%8C%E5%8B%95%E8%97%8D%E5%9C%96-7342ababc417)、[組織篇](https://fantasybz.medium.com/agentic-engineering-%E4%B8%89%E9%83%A8%E6%9B%B2-%E4%B8%80-%E8%AA%B0%E4%BE%86%E5%81%9A-platform-federation-%E7%9A%84%E7%B5%84%E7%B9%94%E8%A8%AD%E8%A8%88%E5%AF%A6%E5%8B%99-9d9353ef7f3a)、[技術篇](https://fantasybz.medium.com/agentic-engineering-%E4%B8%89%E9%83%A8%E6%9B%B2-%E4%BA%8C-harness-%E8%97%8D%E5%9C%96-%E6%8A%8A%E7%B3%BB%E7%B5%B1%E8%AE%8A%E6%88%90-agent-%E8%AE%80%E5%BE%97%E6%87%82%E7%9A%84%E5%9C%B0%E6%96%B9-f2a139f5b561)、[營運篇](https://fantasybz.medium.com/agentic-engineering-%E4%B8%89%E9%83%A8%E6%9B%B2-%E4%B8%89-eval-%E5%96%AE%E4%BD%8D%E7%B6%93%E6%BF%9F%E8%88%87%E8%A6%8F%E6%A8%A1%E5%8C%96-%E6%8A%8A-agent-%E7%95%B6%E7%94%A2%E5%93%81%E7%87%9F%E9%81%8B-d6d9623c2dc6)。

---

### References

1. James Bach — *Taking Testing Seriously*（書）；Bach / Bolton — Testing and Checking（satisfice.com）
2. SWE-Gate — [Passing Functional Tests Is Not Enough for Software Engineering Agents](https://arxiv.org/abs/2609.04167)（2026-09-03）
3. arXiv — [Test Coverage Analysis of Agentic Pull Requests](https://arxiv.org/abs/2607.18057)（2026-07-20）
4. arXiv — [Programmers Are Poor and Overconfident Judges of LLM-Generated Assertions](https://arxiv.org/abs/2607.08885)（2026-07-09）
5. arXiv — [Can escalation channels redirect reward hacking toward defect disclosure?](https://arxiv.org/abs/2608.29460)（2026-08-29）
6. arXiv — [READY or Not: Reliable Enterprise Agent Deployment](https://arxiv.org/abs/2609.02095)（2026-09-02）
7. arXiv — [From Human-Centric to Agentic Code Review: three generations of GenAI and review quality](https://arxiv.org/abs/2607.13196)（2026-07-14）
8. arXiv — [Do These Violent Delights Have Violent Ends? Post-merge fate of agentic code](https://arxiv.org/abs/2607.09902)（2026-07-10）
9. arXiv — [Trust but Verify? Security debt of autonomous coding agents](https://arxiv.org/abs/2607.12428)（2026-07-14）
10. arXiv — [AI-to-AI Code Reviews of GitHub Pull Requests](https://arxiv.org/abs/2608.21311)（2026-08-21）
11. arXiv — [Where Accountability Lives: mapping human responsibility to workflow artifacts](https://arxiv.org/abs/2608.15678)（2026-08-16）
12. arXiv — [The reach of a verification tool decides its value](https://arxiv.org/abs/2608.28795)（2026-08-28）
13. Robert C. Martin（@unclebobmartin）— [2026-07-26 測試種類](https://x.com/unclebobmartin/status/2081332683582427641)、[2026-07-29 measure cleanliness](https://x.com/unclebobmartin/status/2082497764223492161)、[2026-07-30 TDD is a human discipline](https://x.com/unclebobmartin/status/2082850576832905657)、[2026-08-05 deterministic tools](https://x.com/unclebobmartin/status/2085104553746190372)、[2026-08-17 negative test experiment](https://x.com/unclebobmartin/status/2089449442089025936)
14. Martin Fowler（@martinfowler）— [2026-08-11 TDD inside the agent loop（Birgitta Böckeler）](https://x.com/martinfowler/status/2087173563144912985)、[2026-09-02 Maybe we shouldn't be reviewing all this code](https://x.com/martinfowler/status/2095147242986373485)
15. 社群討論：Scrum Community in Taiwan 的公開貼文（「AI 說沒問題」、「把人類的價值要求 AI 是對的」）

---

### AI 協作說明

本文由筆者提出初步構想與章節架構，文字撰寫由 AI（Claude）協作完成，再經筆者逐節校閱與修訂後定稿。文中觀點與判斷為筆者所持，文責亦由筆者自負。

---

*本文發表於 [Medium @fantasybz](https://medium.com/@fantasybz)。若你正在為組織設計 agent 產出的驗證層，歡迎交流。*
