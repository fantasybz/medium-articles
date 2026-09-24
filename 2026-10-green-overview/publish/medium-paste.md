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

# 綠燈不是驗收：agent 時代的測試、Review 與可靠度

> **TL;DR** — 導入 coding agent 之後，如果團隊反覆遇到 CI 綠了、review 排隊、上線仍出事，值得回頭檢查的，是驗收依據是否跟著改變。當實作與測試都由 agent 撰寫、測試又未經獨立審查，綠燈只證明它通過了自己出的題；借用 James Bach 的區分，那是 *checking*，還不足以完成 *testing*。驗證層的三道閘各有分工：test gate 衡量測試的保護力（mutation score），review gate 決定誰審閱哪些內容，reliability gate 用 constraint tests 與 pass^k 判斷授權能否擴張。人如何審閱 payment PR、AI approve 算不算、TDD 能不能當閘門，會在第一節結尾提出。數字都標領域：「34% 的綠燈修補違反 reviewer 約束」是 SWE-Gate 在 75 個 Python repo 上量測到的。文末附 90 天藍圖。

> 系列導覽：**總論（本篇）** → 一、測試篇（即將發布） → 二、Review 篇（即將發布） → 三、可靠度篇（即將發布）。延伸閱讀「Agentic Engineering 三部曲」：[別急著打造你的 Devin](https://fantasybz.medium.com/%E5%88%A5%E6%80%A5%E8%91%97%E6%89%93%E9%80%A0%E4%BD%A0%E7%9A%84-devin-agentic-engineering-%E7%9A%84%E7%B5%84%E7%B9%94%E7%AD%96%E7%95%A5%E8%88%87-90-%E5%A4%A9%E8%A1%8C%E5%8B%95%E8%97%8D%E5%9C%96-7342ababc417) → [組織篇](https://fantasybz.medium.com/agentic-engineering-%E4%B8%89%E9%83%A8%E6%9B%B2-%E4%B8%80-%E8%AA%B0%E4%BE%86%E5%81%9A-platform-federation-%E7%9A%84%E7%B5%84%E7%B9%94%E8%A8%AD%E8%A8%88%E5%AF%A6%E5%8B%99-9d9353ef7f3a) → [技術篇](https://fantasybz.medium.com/agentic-engineering-%E4%B8%89%E9%83%A8%E6%9B%B2-%E4%BA%8C-harness-%E8%97%8D%E5%9C%96-%E6%8A%8A%E7%B3%BB%E7%B5%B1%E8%AE%8A%E6%88%90-agent-%E8%AE%80%E5%BE%97%E6%87%82%E7%9A%84%E5%9C%B0%E6%96%B9-f2a139f5b561) → [營運篇](https://fantasybz.medium.com/agentic-engineering-%E4%B8%89%E9%83%A8%E6%9B%B2-%E4%B8%89-eval-%E5%96%AE%E4%BD%8D%E7%B6%93%E6%BF%9F%E8%88%87%E8%A6%8F%E6%A8%A1%E5%8C%96-%E6%8A%8A-agent-%E7%95%B6%E7%94%A2%E5%93%81%E7%87%9F%E9%81%8B-d6d9623c2dc6)

---

## 一、每個 Engineering VP 都在問的問題：「AI 說沒問題」之後，我該相信什麼？

先不急著談驗收的閘門。我想從導入 coding agent 後，團隊可能遇到的幾個時刻開始。工具已經交出成果，接手的人卻還得回答：我憑什麼相信它？

下面三個情境，有的來自社群討論，有的是為了說明風險而整理的例子。它們未必都發生在你的 repo，卻指向同一個值得追問的問題。

第一個發生在日常的進度確認裡。你問 RD 這個 PR 測過了嗎，他回「AI 說沒問題」。Scrum Community（台灣的 Scrum 社群，Facebook 社團）有一則貼文講的就是這件事。先別急著把這個回答當成偷懶。更值得追問的是：除了 agent 的說法，團隊有沒有準備好能讓他拿來核對的證據？

第二個發生在修 bug 的時候。你叫 agent 修一個 failing test，它回報已經修好，CI 也綠了。回頭看 diff，`assertEqual` 變成 `assertIn`，`== 3` 變成 `>= 1`。測試綠了，bug 還在。它修好的不是程式，是那個會抗議的斷言。

第三個發生在事後。上線後出事，回頭看那個 PR，approve 的是 reviewer agent。人沒有讀過它。假設這件事要寫成 postmortem，最難填的一格會是「這個改動誰看過」，而那一格填不出人名。

三個情境的共同點是：**團隊沒有另外確認驗收依據是否可靠**。agent 的陳述、它自己改過的測試，以及 reviewer agent 的 approve，本來是不同的訊號，卻都被直接當成「可以放行」的理由。

先講清楚本系列聚焦的情境：實作與測試多半都由 agent 撰寫，團隊需要重新確認兩者之間的驗證關係。

CI 綠燈本身是環境執行檢查的結果，不是 agent 的陳述。問題在於：如果 agent 同時改了實作與驗收它的測試，而團隊沒有獨立審查測試，出題者與考生就成了同一個。綠燈仍然是真的，只是還不足以證明原本的需求已經被滿足。

這裡有一個我還回答不了的問題。我讀到的研究沒有一篇統計過：agent 開的 PR 裡，有多少比例含了 agent 寫的測試。所以「**測試多半是 agent 寫的**」在本系列是討論前提，不是已知的普遍事實。第 1 個月可以先統計：新增或修改的測試檔，有多少比例是 agent 寫的。這個比例會影響導入的優先順序，但測試的獨立性與有效性，對其他 repo 也同樣重要。

面對上面三個情境，我想提出三個可以拿來討論的主張。你不同意也沒關係，至少可以帶著它們，回頭檢視自己的 branch protection（GitHub 上的設定，規定 PR 要滿足什麼才准 merge）、review policy 與 agent workflow。

在提出主張之前，先交代這裡會用到的幾個詞。payment 指的是付款相關的程式碼，這裡拿它當例子，是因為出錯後可能影響付款正確性，auth 與 schema 也常需要高度注意。constraint tests 是把 reviewer 提出的可檢查要求，變成由 CI 執行的檢查。mutation 報告則是「把程式故意改壞，再看測試會不會紅」的結果。intent 是 PR 說明裡「想改什麼、為什麼改」那一段。AGENTS.md 是放在 repo 裡、寫給 agent 讀的專案說明檔。constraint tests 與 mutation 報告後面各有一節：

> **Green is checking. Acceptance is testing.** 所以改到 payment 的 PR，先確認 constraint tests 與 mutation 報告能涵蓋關鍵要求，再讓人以 intent 與報告為起點，深入查閱被標示或仍有疑問的 hunk；尚未具備這些依據時，仍以逐行審閱為常態。評論中能持續檢查的要求，則回收成 constraint test。AI 的 approve 不計入 branch protection，不管哪一家。AGENTS.md 寫 TDD 可以，拿 TDD 的形狀當閘門不行。

這三個主張是我的流程設計建議；testing 與 checking 的區分，則借自 James Bach。下一節先把這組語言講清楚，再從數據與測試史理解綠燈為什麼不足以代表驗收，逐一說明三道閘的用途，最後整理成決策清單與行動藍圖。

---

## 二、書錨：Bach 的 testing 與 checking

要說清楚這三道閘為什麼存在，我想先回到一本談測試的書。James Bach 是 context-driven testing（看情境決定怎麼測，不照固定流程）與 Rapid Software Testing 方法論的作者，這一節的書錨是他的《Taking Testing Seriously》。他一輩子在做的事，就是把「測試」跟「照著清單打勾」分開。

這本書裡有一句話，我在自己的 Facebook 粉絲團引過：「Testing is the opposite of faith in the product. Testing begins with faith in the existence of trouble.」我在意的是這句話的後半段。測試的起點不是相信產品沒問題，而是相信麻煩一定在某個地方等著。

這裡也交代一下閱讀進度：這本書我還沒讀完，引用集中在定義 testing 與 checking 的那一章與一篇訪談。

那 checking 又是什麼？Bach 的定義是這樣寫的：「Checking is the mechanistic process of verifying propositions… testing cannot be automated, but checking can.」

用白話說，checking 是拿一組已經寫好的命題去對答案，對得起來就綠、對不起來就紅，機器做這件事比人快也比人穩。testing 則是人帶著判斷去問「這東西到底行不行」，Bach 說它沒辦法自動化。

所以 CI 自動執行 checking，這件事本身沒有問題。需要分開看的是：CI 確實執行了什麼、測試中的命題由誰確認，以及 agent 最後怎麼描述結果。「測試全過」這句話本身，只是一份陳述。

把陳述與執行結果分開之後，下一個問題才是：哪些結果足以作為驗收依據？本系列把來源分成三類，後三篇沿用同一組代號：

- （a） **agent 的陳述**：「已完成」「測試全過」「LGTM」。
- （b） **agent 寫的或改過的測試**：綠了，只證明它通過了自己出的題。
- （c） **團隊擁有的測試與 constraint tests**：環境的量測，agent 改不動。

三類裡，只有（c）能作為本系列閘門採用的獨立驗收證據。（a）可以提示要查什麼，（b）能提供實際執行的結果；但在團隊確認測試本身之前，兩者都不足以單獨支持放行。

這裡會有一個很自然的反問：agent 對 repo 有寫入權，（c） 憑什麼改不動？要回答它需要兩條機制，一條決定測試怎麼升格，一條決定升格之後誰動得了。

**升格規則**：agent 寫的測試通過 test gate（斷言沒有弱化、mutation 有殺傷力），**而且被人類 approve 進 main**，才從 （b） 升格為 （c）。也就是說，分類看的是「誰為它負責過」，不是「誰打的字」。

**改不動**：`tests/constraints/` 與 golden set 目錄的 CODEOWNERS 只列人類，並啟用要求 code owner 核准的合併規則；（c）類測試的任何弱化直接阻擋。golden set 是一組固定的代表性任務，用來反覆評估同一套 agent。這裡的「改不動」是指 agent 不能自行核准並合併修改，不是不能在分支上提出變更。檢查時還要使用受保護的測試版本，才能避免 PR 先改掉考卷、再拿那份考卷證明自己通過。實作與限制在可靠度篇。

升格規則裡的 mutation，是把程式碼做出一個刻意的變動，再看測試是否失敗。若這個變動確實改變了行為，測試卻沒紅，就值得追查哪一項要求沒有被斷言守住。mutation score 統計的是有效變異中被測試抓到的比例，衡量的是測試對這些變動的敏感度，不只是程式碼曾被執行到哪些地方。

有了這個區分，後面的用語也就清楚了。mutation score、constraint tests 與 pass^k（k 次全過的比例）都是**更好的 check**，不是 testing 的替代品。testing 是帶著「一定有問題」的信念去看這個系統，那還是人的工作。

這種分工現場已經有人在做。我引那句話的粉絲團貼文下面，有讀者回覆說，tester 現在用 vibe coding（只看結果、不看程式碼，全交給 agent 寫）做丟棄式的測試工具。所謂丟棄式，是寫完就丟，只為了回答當下的一個疑問。這正是本系列的立場：agent 是 tester 的工具，不是替代。

把 checking 與 testing 攤成左右兩欄，界線會比文字清楚。左欄是機器做得到的事，右欄是只有人做得到的事：

📌【在此插入圖 diagram-01.png】

左欄最下面那一格提醒了一件容易忘記的事：mutation、constraint tests 與 pass^k 也站在 checking 這一側。把 check 做得更好，不會自動完成 testing。它能先處理可重複的檢查，讓人帶著結果與疑點，繼續判斷還需要查什麼。

那麼，現在的 check 到底漏掉了什麼？下一節先用兩組研究結果說明，再指出需要由團隊自己量測的可靠度問題。

---

## 三、2026 年，數據怎麼說：綠燈無法涵蓋的三層

綠燈無法涵蓋的問題可以分成三層：功能測試過不等於約束滿足、有測試不等於測到、一次成功不等於可靠。三層各自對應一個問題，需要的證據也不同。

這裡刻意把每個數字都標上領域、樣本數與日期，因為 agent 領域的研究更新太快，數字一離開脈絡就很容易被誤用。前兩層我各放一篇 in-domain 錨點，也就是在 code 這個領域本身量測得到的研究結果，不是從別的領域借過來的。第三層 code 領域目前沒有我能直接引用的現成數字，所以做法很樸素：用自己的 golden set 反覆執行任務，量測可靠度。

表裡的 SWE-Gate 是一組評測。它做的事，是把 agent 修補過的程式碼同時丟給功能測試與 reviewer 約束，看兩邊的結果差多少。三層與各自的錨點如下：

📌【在此插入表 table-01.png】

同樣三層，換成一張圖看它們跟 CI 綠燈的關係。要看的是每一層跟綠燈之間的那段距離：

📌【在此插入圖 diagram-02.png】

最後那個箭頭提醒的是：這三層問題都需要在 CI 綠燈之外另外驗證，不能只靠目前的綠燈判斷。

人眼也不能單獨當成安全網，這是我原本以為還可以當退路的地方。一項實驗讓 86 位開發者判斷 LLM 寫的斷言對不對：面對正確斷言時，判斷準確率是 74%；面對錯誤斷言時，只有 49%，而信心並沒有相應下降（Poor and Overconfident Judges，2026 年 7 月）。這裡統計的是判斷的準確率，不是把參與者分成看得懂與看不懂的兩群。

這批實驗裡，錯誤斷言有將近一半未被正確辨識，主觀信心也沒有可靠地提醒人停下來確認。它不能推論每個 reviewer 都一樣，卻足以提醒我們：把檢查全部交給人眼，仍然有盲點。第七節談「什麼值得人讀」時，會回頭用這個結果。

讓這個落差變得具體的，是我自己在工作坊遇到的一個例子。它的規模比上面那些研究小得多，卻讓「測試全綠」與「需求被滿足」的差別直接擺在眼前。今年夏天在泰迪軟體 Teddy 老師的模式語言驅動開發工作坊，我叫 agent 做一個很小的需求。它交出來的結果是這樣的：5 個測試全綠，event sourcing 的 replay 路徑從未執行。

event sourcing 是把狀態變化存成事件、需要時再從事件重建狀態的做法，replay 就是那條重播路徑。它在這份需求裡是關鍵，卻沒有被測試執行到。測試全綠，只代表已執行的檢查沒有失敗；那條沒走過的路是否正確，綠燈沒有回答。細節在測試篇。

這個例子讓我在意的，是一個比「agent 可不可信」更具體的問題：**測試確實執行了，卻沒有涵蓋需求要求的路徑**。它讓第二層的落差變得清楚；另外兩層，仍需要各自的證據。

這聽起來像是 agent 帶來的新問題，其實不是。下一節把時間軸拉開，你會看到同一齣戲已經演過一次。

---

## 四、測試史已經演過一次

面對新的驗證問題，我常會回頭找工程史裡相似的處境。〈別急著打造你的 Devin〉借 DevOps 2014–2016 的發展討論組織選擇；這一篇則回到測試史，看看哪些爭論已經有過前例。

換的理由是：今天用來驗證 agent 產出的許多方法，測試領域早已討論過。新的壓力，是產出變快之後，團隊必須重新安排驗證的成本與分工。下面這張圖把測試史放在左邊，把今天的驗證層放在右邊，看它們如何對應：

📌【在此插入圖 diagram-03.png】

這張圖有兩條重點值得展開。

第一條在左邊那條時間線。它從 Fagan inspection（一群人坐下來逐行讀程式的正式審查）開始，一路走到 Humble & Farley（《Continuous Delivery》的兩位作者）的 deployment pipeline，而 pipeline 早就說過，commit stage 綠了不是 release。agent 時代並沒有推翻這件事，只是把後面幾個 stage 重新發明成三道閘。

第二條在右邊。mutation testing 的成本一直在於反覆執行測試，agent 並沒有讓這筆運算成本消失。它改變的是另一端：測試產出得更快，逐份人工審閱更難負擔，衡量測試有效性的需求也更迫切。把 mutation 限定在改動範圍內，才有機會讓成本與保護力取得平衡。

**測試史留下的方法還在，現在需要重新計算的，是團隊願意為哪些驗證投入時間與成本。**

下一節先從測試開始：既然測試也可以由 agent 撰寫，指示能幫上什麼忙，又有哪些結果仍需要另外量測？

---

## 五、別教 agent 怎麼測，衡量它交出的成果

Uncle Bob（Robert C. Martin）大概是這個產業裡最不可能放棄 TDD 的人，TDD 最主要的推廣者就是他。他今年夏天在 X 上把立場講完了，所以下面這兩則貼文特別值得看。7 月 29 日他說：你沒辦法叫 agent「保持乾淨」，只能量測程式碼的品質，再依結果要求它修正。隔天 7 月 30 日他把話說得更白：TDD 是人類的紀律，他不期待 agent 遵守。

連 TDD 的推廣者都把 agent 的紀律問題交給量測，這就是本節標題那句話的起點。

另一個角度來自 Birgitta Böckeler，她是 Thoughtworks 負責 AI 輔助開發的人，她的同事 Martin Fowler（《Refactoring》的作者）8 月 11 日轉貼了她這篇「TDD inside the agent loop—theater or actual value?」。她把它當成實證問題來問：agent 迴圈裡的 TDD，究竟是演給人看的儀式，還是真的有用？

本文的答案就是第一節那三個主張裡的最後一個。TDD 的步驟可能影響 agent 的探索路徑，所以 AGENTS.md 寫「請用 TDD」可以；但是否帶來品質改善，仍要看產出。**拿 TDD 的形狀當閘門不行**，不能只看它是否照順序寫出測試與實作，就認定需求已經被滿足。

Uncle Bob 在 8 月 17 日還做了一個小實驗，本文照著那則貼文叫它 negative test experiment：同一個題目，換四種寫測試的紀律，再各配上有沒有 CRAP 門檻，一共 8 次 run，看寫出來的程式長得一不一樣。CRAP 是 Change Risk Anti-Patterns，一個把圈複雜度（程式分支的多寡）與覆蓋率合起來算的風險分數，分數越高，代表這段程式又複雜又沒被測到。

結果是這樣的：**全部通過同樣的 25 個驗收案例，寫出來的程式卻不一樣**。這說明同一組驗收案例，仍然容許不同的實作結構；至於哪一份比較好，還需要額外的品質判準。它與 SWE-Gate 都提醒我們綠燈有邊界，但一個觀察實作差異，一個量測約束違反，不能視為同一份證據。

台灣的討論其實也走到同一個位置。Scrum Community 有一則貼文說，把人類的「價值」要求 AI 是對的，把「做事習慣」硬套在 AI 身上是錯的。我同意這個切法，只是還要補一句：差的不是共識，是閘門還沒人寫出來。

下面這張表把「指示型」與「量測型」兩種做法排在一起。左欄是你想要的結果，中欄是只提出指示的做法，右欄是可以真的當閘門的做法：

📌【在此插入表 table-02.png】

右欄把要求接到可核對的結果：有些由 CI 直接檢查，有些先讓 agent 提出證據，再由團隊確認。prompt 可以引導行為；要支持放行，還需要知道實際發生了什麼，以及誰核對過這份結果。

三道閘的零件到這裡都零散地出現過了。下一節把它們放進同一張圖，順序也一次講清楚。

---

## 六、驗證層的三道閘

前五節可以整理成一張圖。左邊是 agent 交出的程式碼、測試與陳述，右邊是團隊用來評估它們的三道閘。閘門裡仍然有 checking，差別在於驗收標準與放行責任由團隊掌握：

📌【在此插入圖 diagram-04.png】

圖的重點在中間那條分界線：左邊做得再好，也不會自己跨到右邊來。右邊三道閘則是有順序的，前一道沒過，後一道不必談。

每道閘都需要說清楚：要回答什麼問題、用什麼指標量測，以及由誰負責：

📌【在此插入表 table-03.png】

表裡有一個零件是三道閘共用的：constraint tests；其他名詞留到各自那一節定義。舉一個假設的情境，reviewer 在某個 PR 上留過「這裡不要每次都開一個新的 HTTP client」，這句話被寫成一條 CI 每次都會跑的規則，它就從一則評論變成了一道 check。

constraint tests 由 test gate 的 owner 安裝與維護，reliability gate 則使用這些檢查得到的 constraint pass rate：功能測試過了的 PR 裡，constraint tests 也全過的比例。

三道閘共用一句設計哲學：**設計環境比寫規則有效**。

有一項研究用實驗檢驗了這個方向。它給 agent 一個正式的「回報壞測試」出路，也就是可以說出「這個測試本身有問題」的管道，結果 agent reward hacking 的比例就掉到約四分之一。reward hacking 指的是它跑去讓測試通過，而不是去把 bug 修對（escalation channels，2026 年 8 月）。基準值、全部數字與那個工具的 schema 都在測試篇。

與其猜測 agent 為什麼改掉測試，我更想先確認：流程有沒有讓它提出異議、交出證據，並等待團隊判斷的路。

test gate 與 reliability gate 裡的量測可以自動執行，review gate 的分流也能交給工具協助。但要由誰審閱、哪些疑點必須追問，以及最後是否核准，仍然需要團隊作出判斷。

---

## 七、Review 是控制點，不是瓶頸

人的時間該花在哪裡，Martin Fowler 9 月 2 日轉的那一篇「Maybe we shouldn't be reviewing all this code」問得比我直接：問題不是 AI 弄壞了 code review，是我們一直拿 review 解決錯的問題。

本文的版本：**review 的重設計不是讓人讀得更快，是決定什麼值得人讀。**

[〈別急著打造你的 Devin〉](https://fantasybz.medium.com/%E5%88%A5%E6%80%A5%E8%91%97%E6%89%93%E9%80%A0%E4%BD%A0%E7%9A%84-devin-agentic-engineering-%E7%9A%84%E7%B5%84%E7%B9%94%E7%AD%96%E7%95%A5%E8%88%87-90-%E5%A4%A9%E8%A1%8C%E5%8B%95%E8%97%8D%E5%9C%96-7342ababc417)第四節的「Review 成為新瓶頸」，我自己要修正：瓶頸是症狀，病因是把人放在錯的閘門上讀錯的東西。

這一節有兩個數字要用，一個講規模，一個講關聯。

先講規模。一項長期追蹤研究（From Human-Centric to Agentic Code Review，2026 年 7 月）橫跨從人審到 agent 審的三個世代、一百萬個 PR。它發現 agent 發起與多 agent review **在某些採用模式下**讓決策更快，但沒有更好。「在某些採用模式下」這個限定是論文自己加的，不是我加的。

再講關聯。另一項縱向研究（一樣是長期追蹤）追蹤了 182 個 repo（Post-merge fate of agentic code，2026 年 7 月），發現 agentic code 需要顯著更多矯正性維護，也就是事後修 bug。它給出的關聯是這樣的：免審合併率—沒有任何人類 approve 就 merge 的比例—每高 10 個百分點，維護負擔約高 6%。

這個數字要小心讀。原句是 "is associated with"，相關不是因果，所以它撐不起「不 review 就一定會爛」這種說法。但它足夠讓免審合併率變成一個該進月報的指標。這裡的免審合併包含只有 AI approve 的合併，第一節主張 2 說的「不計入」，就是這件事。

除了維護負擔，還有另一項風險要另外處理。2026 年 7 月的研究 Trust but Verify 發現，受測資料裡大多數真實外洩的 secret，在 merge 前沒有被抓到。這不能全歸因於免審合併，卻提醒團隊需要檢查整條流程的資安防線。完整數字在 Review 篇。

把加分與負債畫成一張圖，中間那個菱形就是這一節標題所說的控制點：

📌【在此插入圖 diagram-05.png】

圖右邊放的是兩種流程選擇與它們需要追蹤的結果。回收評論能讓相同要求持續被檢查；放掉審查則可能留下維護與資安風險。這是流程設計的理由，不是把前面的關聯數字當成因果證明：採用之後，仍要量測風險是否真的下降。

面對付款相關的改動，逐行審閱仍然有價值。但如果團隊把它當成唯一的安全網，人的注意力就得承擔太多事情。我認為至少有兩個理由，值得把可重複的檢查先交給工具。

第一個理由是第三節那個 49%：在那項實驗裡，開發者辨識錯誤斷言的準確率大約只有一半。它評估的是斷言判斷，不是完整的 PR review，不能直接推成 review 的抓錯率；它提醒的是，花時間閱讀不等於一定判斷正確。

第二個理由是，審查中累積的知識需要留下來。一則評論即使解決了眼前的 PR，也未必會在下一次改動時被想起。把其中可重複檢查的要求寫成 constraint test，後續 PR 就能持續接受相同的檢查，reviewer 也不必一再提醒同一件事。

所以在 blast radius 高的 PR 上，人讀 diff 找出的可重複檢查條件，要回收成 constraint tests。blast radius 指的是改動出錯後會波及多大範圍。auth、payment、schema、infra 通常需要高度注意；內部工具也要看它握有什麼權限、影響哪些資料，不能只憑名稱判成低風險。

等 constraint tests 與 mutation 報告足以涵蓋該類改動時，人就改為審閱 intent 與報告，並深入檢視被標紅或仍有疑問的 hunk。hunk 是 diff 裡的一段改動。沒有被標紅，不代表沒有風險；如果報告無法回答 intent 裡的關鍵要求，這個 PR 就還不算可驗證。受監管系統的審閱要求與抽讀安排，在 Review 篇另外說明。

下面這張分流圖有四個出口，其中兩格需要人深入審閱：

📌【在此插入圖 diagram-06.png】

右下角那一格是容易被略過的起點：影響範圍受限、卻缺少驗證依據的 PR，先補 check，再安排閱讀報告與核准。若關鍵要求仍無法驗證，就不能只因為被歸為低風險，便把一個匆忙的 approve 當成足夠的交代。

這四個出口對應到 Review 篇的分流矩陣。那一篇會接著說明 reviewer 艦隊如何分工、為什麼需要禁止同一個 session 自審，以及核准紀錄應該留下哪些資訊。這裡先保留一個判斷：安排人讀什麼之前，團隊要先知道這個 PR 已有哪些證據、還有哪些疑問。

review gate 處理的是眼前這個 PR 該如何審閱。即使這次審查通過，團隊仍要面對另一個問題：這類任務重複交給 agent，表現是否足夠穩定，值得放寬授權？

---

## 八、可靠度不是能力：pass@1、pass^k 與 oversight budget

一次把任務做對，會讓人看見 agent 的能力；同一類任務反覆交付時，能不能維持表現，才是安排授權時需要知道的事。這兩個問題要分開量測，不能只用一個「通過率」帶過：

- **pass@1**：每個 case 每次嘗試的成功率，用 k 次重跑估計。
- **pass^k**：k 次全部成功的 case 比例。
- 兩者都先逐個 case 算，再對整個 golden set 取平均。「至少一次成功」是 pass@k，本系列不用它。

用一個 case 來看會更清楚。假設固定任務與執行條件，每次都從相同的初始狀態獨立執行，其中一次失敗：

📌【在此插入圖 diagram-07.png】

同一批執行結果，會同時得到這兩個數字。pass@1 保留了其中成功的嘗試；pass^k 則追問這個 case 是否每一次都成功。只要有一次失敗，這個 case 就不能算進 k 次全過的那一群。差距來自判定條件不同，不是兩份報告互相矛盾。

要知道這個差距對自己的系統有多大，可以沿用〈Agentic Engineering：Eval、單位經濟與規模化〉營運篇建議的 golden set：選 20–50 個 case，每個獨立執行 k = 5 到 10 次。這份量測結果才是討論授權範圍的起點；別人的 benchmark 可以提供參考，無法代替團隊作出決定。

知道成功率與穩定性之後，還要把人的時間算進來。這裡借用一個 **code 以外的案例**，說明為什麼準確率相近的系統，可能需要不同的複核安排。借的是思考方式，案例中的人力比例不能直接套到 coding agent。

READY 是企業 agent 部署的資格審查框架（2026 年 9 月），它做的事是在放行一個 agent 系統之前，先問「要達到你要的可靠度，得配多少人看」。它的案例是臨床稽核工作流、16 個 agent 系統、750 個 case，領域不是 code。

其中兩個系統的自主準確率只差 0.3 個百分點（72.8% 對 72.5%）。把可靠度目標都訂在同一個 76%，需要的人工複核比例卻差了近 10 個百分點（39.2% 對 29.6%）—準確率高的那個要更多人看。

**準確率的排名，不是人力的排名。**

我的讀法是：除了「它對幾成」，還要看錯誤能不能被複核政策辨識。若錯誤集中在可識別的情境，人力可能比較容易安排；若錯誤難以預判，就需要擴大複核範圍。這是我從結果反推的可能解釋，論文沒有把這組差距歸因於這個機制。

人工複核需求可以由可靠度目標反推，再與團隊能負擔的人力比較。本系列用 oversight budget 討論這筆預算；可靠度篇會把所需下限、實際安排與可負擔上限分開計算。先把兩個系統並排看：

📌【在此插入圖 diagram-08.png】

兩個系統的自主準確率相近，達到相同可靠度目標所需的複核比例卻不同。對要安排人力的主管來說，這個差距不能藏在平均準確率裡：選擇系統時，也得確認團隊是否負擔得起它需要的複核工作。

所以 leadership 月報要把單一的「通過率」換成三個數字，前兩個是上面那對 golden set 數字，第三個是第六節的 constraint pass rate：

📌【在此插入表 table-04.png】

這三個數字各自補上一部分證據，也各有界線。pass@1 可以追蹤能力變化，卻不足以單獨決定授權；pass^k 必須連同任務集合與 k 一起讀，才有比較的意義；constraint pass rate 則只涵蓋已經寫成檢查的要求。月報把它們分開，才能避免一個漂亮的總分掩蓋了不同的風險。

這些量測要接回〈Agentic Engineering：Eval、單位經濟與規模化〉營運篇的 G2，也就是決定是否放寬授權的閘門。判斷不能只靠 pass@1，還要一起看 pass^k 與 escape rate；後者是未被這些閘門攔截、直到 production 才被發現的缺陷比例。

G2 原本追蹤重試、外逸缺陷與 champions 的運作。本系列再補上四個條件：pass^k、由 1 減去 constraint pass rate 得到的 constraint violation rate、mutation score 下限，以及 oversight budget。可靠度篇會把它們整理成同一張決策表，交代什麼情況可以擴張、什麼情況應該先停下來。

量測能力，讓團隊知道工具是否進步；決定授權，還要對失敗後果與接手的人力負責。

到這裡，三道閘各自要回答的問題、需要的證據與負責的人已經交代清楚。接下來回到日常工作，看看哪些熟悉的做法，可能正好繞過了這些判斷。

---

## 九、八個反模式

流程設計放在文件裡往往很清楚，到了忙碌的 PR 佇列裡，團隊仍可能回到最順手的做法。下面整理八個反模式，右欄用具體情境說明。讀的時候，可以對照自己的驗收流程，看看哪些訊號被當成了足夠的證據。

📌【在此插入表 table-05.png】

八個反模式各自歸哪一道閘，用一張圖分派：

📌【在此插入圖 diagram-09.png】

這張圖把症狀連回可以著手改善的流程。遇到斷言鬆綁，可以先檢查 test gate 是否辨識得到；遇到同一個 session 自審，就要回頭看 review gate 的隔離與核准機制。這不表示 agent 本身沒有問題，而是讓團隊知道，除了更換模型，自己還能在哪裡補上控制。

在台灣社群的討論裡，我較常看到「覆蓋率當品質」與「閉環 review」，也就是表裡的 5 與 6。這是我的觀察，沒有統計支持。兩者容易成為順手選項，或許也與導入成本有關：既有 CI 通常已經有覆蓋率數字，同一份席位訂閱也讓人容易沿用原本的 agent 做 review。理解這些限制，才有辦法提出團隊負擔得起的替代流程。

閉環 review 佔多少比例，我讀到的研究沒有一篇統計過。現有研究記錄的是另一種配對。一項 2026 年 8 月的研究（AI-to-AI Code Reviews）看了 248,641 個 PR，跨產品的 AI 審 AI，也就是用不同家的 reviewer 去審 agent 開的 PR，目前只佔約 1.6%，但在 2025 年 Q1 到 Q3 之間成長超過 100 倍。

不同產品之間的配對，可以是本系列允許的做法，但仍要隔離生成與審查的 context，最後由人核准。「不同家」本身不保證獨立。真正需要另外追蹤的，是同 model、同 session 自審的比例；論文沒有統計這個數字，團隊要從自己的 review 紀錄計算。

症狀認得出來之後，剩下的是決策。下一節我把自己放到 Engineering VP 或 QA lead 的位子上，寫我會核准什麼、不會核准什麼。

---

## 十、如果我是 Engineering VP / QA lead，我會怎麼決策

如果要把前面九節帶進一次預算或流程會議，我會先問：這項提案準備用什麼證據支持放行，又把哪些責任交給了誰？下面三句是為了說明判斷而寫的提案例子。以目前提供的依據，我**不會**核准：

> 「把 QA 團隊轉型成 prompt 團隊。」
> 「用 AI review 清掉 review backlog，AI approve 即可 merge。」
> 「以 eval 通過率 85% 為據，Q4 開放所有 team 的 write tools。」

第一句沒有交代測試判斷由誰承接，第二句省略了人的核准，第三句則把單次通過率直接當成放寬授權的依據。第三句的 write tools，是讓 agent 能改動系統的工具權限。三個提案缺的證據不完全相同，但都還沒有說清楚：原本由人承擔的判斷，改流程之後要靠什麼守住。

我**會**核准四件事：

1. **先把 review 評論變成 constraint tests。** 從最近 90 天被打回的 agent PR 抽 50 條 review 評論，分類、挑出可執行的，寫成前 10 條 constraint tests。沒有評論歷史的 repo，改從最近 5 個 incident 的 postmortem 導出前 5 條。這是主路線，不是退路，因為每一條「以後不准再發生」本來就是一條約束。
2. **先在一個 pilot repo 試行 mutation gate**，只計算 agent 改動的行。團隊達 200 人以上，或已有 QA lead 能持續解讀報告時，可以評估導入；無論人數多少，都要有人負責校準，而且受影響的測試子集要能在 10 分鐘內執行完畢。先用**我的建議值（不是業界標準）** mutation score ≥ 70% 作為觀察起點。先累積一個月的報告，再決定是否啟用阻擋；低於門檻時，將漏掉的行為與測試缺口交回 agent 修補，由負責人處理例外與誤判。
3. **reviewer agent 必須是不同 vendor、或至少不同 session 的 instance**（換一家模型，或至少另開一個對話來審），而且 AI 的 approve 永遠不計入 required approvals。required approvals 是 GitHub 上「這個 PR 要幾個 approve 才能 merge」的那個設定。只有 AI approve 的合併，在第七節的免審合併率裡算免審。GitHub 上有兩條候選機制。一條是 CODEOWNERS 只列人類，再加上 Require review from Code Owners；另一條是用 required status check 去數人類的 approve。筆者尚未在生產 repo 實測，會先用一個 GitHub App 的 approve 在自己的 repo 驗證這兩條路走不走得通，設計草稿在 Review 篇。
4. **讓核准紀錄對應到人，以及他實際審閱的內容。** approval artifact 應記錄核准者與被審內容的 hash；內容變更後，就需要重新取得核准。高 blast radius 的 PR，任務指派者不可兼任核准者。Where Accountability Lives（2026 年 8 月）指出，各家 vendor 對「誰可以核准 agent 的 PR」有互相矛盾的條款。這也提醒我，團隊必須明訂自己的責任分工，不能只憑工具介面上的 approve 判定責任已經有人承接。

**驗證預算怎麼想。** 一項 2026 年 8 月的研究（The reach of a verification tool decides its value）給了我一個原則：驗證工具的價值由觸及範圍決定。樣本是 1,116 個 web app、6 個 model、8 種工具配置。它的例子是 boot probe，只檢查程式能不能啟動的探針：只花完整 shell 約 35% 的 token 成本，就移除了幾乎所有啟動失敗，完整 shell 則是 2.35 倍成本。

我的導入順序是：先補能以較低成本攔住常見錯誤的 check，再增加執行成本較高的驗證。constraint tests 若能用靜態分析實作，可和 assertion-change diff 一起先做；前者若涉及行為或效能，仍然需要執行程式。接著是 red-then-green 與 diff-scoped mutation，最後才加入 k 次重跑與 step-rubric judge，也就是按步驟評分的 LLM 評審。這是依成本與風險安排的建議順序，不是那篇研究直接比較出的排名。

預算的比例是這樣：agent 的產出每花 1 元，就配 0.3 到 0.5 元去驗證它。分母是 agent token 加生成側 CI（agent 產出的機器成本），分子是驗證側 compute（驗證它的機器成本）。**比例是筆者暫定的啟發式，待 pilot 校準**—那篇論文只撐得起原則，撐不起比例。**人工複核的時間不在這個比例裡**，它走可靠度篇的 oversight budget，兩筆分開向 CFO 報。

**50 / 200 / 1,000 人怎麼安排。** 以下是三種導入情境，討論檢查如何從少數 repo 推廣到整個組織，與 G2 的授權擴張是不同的決策。表中的 50 人團隊假設還沒有餘裕維護 mutation 報告；人數只用來描述情境，真正的前提仍是能否安排負責人：

📌【在此插入表 table-06.png】

規模擴大後，需要改變的不只是啟用哪些 check，還包括誰維護規則、誰解讀報告，以及誰處理例外。paved road 指平台預先提供、預設就能使用的流程。把檢查放進這條流程，可以減少各 repo 重複設定的工作；但報告若沒有人接手，集中安裝也不會自動帶來品質。

**Brownfield：先裝哪道閘。** 考慮一個具體情境：15 年的 legacy monolith、測試套件跑 40 分鐘、覆蓋率 30%，又沒有整理好的 review 評論歷史。下面安排的是這類 repo 的驗證層導入順序，每一步列出各自的前提。它不取代〈別急著打造你的 Devin〉第七節讓 agent 讀得懂系統的 legibility 順序：characterization tests → logs / traces → architecture rules。連測試都沒有時，先用 characterization tests 記錄既有行為，算第 0 步；記錄下來的結果仍要區分哪些是需求、哪些只是待釐清的現況：

📌【在此插入表 table-07.png】

這四個 check 對人寫的 PR 一樣有用—斷言鬆綁、凍結 bug、違反團隊約束，都不是 agent 發明的。**即使 agent 路線失敗，這幾道閘也不會白裝。**

---

## 十一、90 天的驗證層行動藍圖

前面的決策若要開始執行，團隊還需要一個能承受的順序。這份 90 天藍圖先從建立基準與小範圍試行開始，再逐步加入阻擋與授權決策。每個階段都要留下可檢查的結果，才知道下一步是否準備好了。

先講起點。閘門裝上去以後，你一定會被問「所以到底有沒有比較好」，要回答這個問題，就得先知道導入之前的狀況。所以第 1 個月的主要工作是建立 baseline，也就是先量測還沒有任何介入時的表現，作為日後比較的基準。

需要追蹤的指標有六個。〈Agentic Engineering：Eval、單位經濟與規模化〉營運篇已經提出其中兩個：escape rate（定義見第八節），以及 review minutes / PR，也就是每個 PR 平均需要的人工審查分鐘數。本系列再增加四項，用來看清測試與驗收依據如何改變：

- 既有斷言被弱化的 PR 比例
- snapshot 或 golden file（錄下現況輸出當答案的檔案，非 golden set）更新未附理由的比例
- 既有測試覆蓋 agent 改動行的比例
- 新增或修改的測試檔由 agent 寫的比例

最後一個要單獨說一句。這項統計要確認的是第一節的前提是否成立，而不是評斷品質。如果新增測試多半仍由人撰寫，這個 repo 就與第一節設定的情境不同，可以據此調整導入節奏；但還要確認測試是否經過獨立審查，不能只靠作者身分判斷。上一節的理由仍然成立：這幾道 check 對人寫的 PR 一樣有用。先掌握現況，才能安排適合這個團隊的導入節奏。

基準建立之後，就能安排試行與比較。下表用月份表示建議節奏，右欄則說明每個階段必須留下什麼成果。月份到了，不代表條件自然成立；是否往下走，仍要看退出條件。

📌【在此插入表 table-08.png】

表裡最容易被跳過的是退出條件。它們用來判斷是否準備好往下走，不能被月份排程取代。若 constraint tests 一整個月都沒有阻擋 PR，先確認它們是否真的涵蓋預期風險，也可以拿過去違規的修補重播驗證。沒有攔到問題，可能是改動恰好都符合規則，也可能是檢查漏了；不能為了證明閘門有用，就刻意挑一條會擋人的規則。

表格回答的是每個月做什麼。下面這張圖只取前三個月，把每一個月的退出條件排出來，看它們最後怎麼收斂到同一個決策：

📌【在此插入圖 diagram-10.png】

這條路線最後要走到一次有依據的授權決策。負責的人需要能說明：哪些結果支持擴張，或哪些風險讓團隊選擇維持現狀。即使三個月後仍未擴張，只要理由清楚、下一步要補的證據也明確，試行就已經替團隊回答了重要的問題。

最後補兩個提醒，都是我認為最容易把這件事做壞的地方：

1. **mutation 最後裝，先報告、後阻擋。** 第 1 個月先觀察報告，第 3 個月再依校準結果啟用阻擋。團隊需要先看懂哪些訊號值得停下來，才有理由信任新閘門。red-then-green 也要交代適用範圍：本文只對修改既有行為的 PR 啟用；feature PR 可能因類別或介面尚不存在而無法執行測試，那不是要驗證的行為差異，不能當成有效的 red。
2. **constraint tests 先從團隊已有共識、又能清楚檢查的規則開始。** 例如在特定任務中不新增依賴、不新增 public API，或遵守既定的 log 格式。這些要求仍需要說清楚適用範圍，不能假設所有人本來就同意。若「不可以跨層呼叫」在團隊裡還沒有共同定義，先把邊界討論清楚，再寫進 CI；否則一個 failed check 會同時承擔技術檢查與架構爭議，讓接手的人無從判斷。

工具與人力會影響進度，退出條件則幫助團隊守住判斷。若證據還不夠，讓計畫慢一點，比為了趕上時間表而提早放寬授權更值得。

---

## 十二、結語

回到第一節那三個情境。三道閘都裝上以後，它們會怎麼收場？

RD 再被問「這個 PR 測過了嗎」的時候，就能拿著幾份具體的結果一起討論：constraint 報告是否通過、mutation 報告指出哪些風險、這個 PR 在分流矩陣裡需要哪一種審查。那句「AI 說沒問題」，終於有了可以繼續追問的依據。

那個把 `assertEqual` 改成 `assertIn` 的 PR，在 merge 之前就會被 assertion-change diff 認出來：equality 換成 containment 是強度下降，直接阻擋。測試照樣是綠的，這個 PR 就是過不去。

至於原本只有 reviewer agent approve 的流程，人類核准機制與核准紀錄落實後，就能回答「誰審閱了哪一版內容」。這不能保證上線後不出事，但能讓事後檢討有明確的起點，查清楚當時看過什麼、哪些風險沒有被辨識。

這三個變化，都從團隊重新掌握驗收依據開始：測試本身有人確認，檢查結果可以重現，核准也能追溯到內容與負責的人。agent 能力提高仍然有幫助，但組織不必等到它不再犯錯，才開始建立這些流程。

回到 Bach。checking 可以自動化，testing 仍需要人的判斷。agent 讓建立與執行部分 check 更容易，也讓團隊必須更認真地問：省下的時間，要留給哪些還沒有被檢查到的問題？我想保留的人力，正是用來先假設這裡可能有問題，再設法把它找出來。

最後留一個有日期的預測，這樣它才可以被驗證，也才可以被打臉。到 2027 年，reliability gate 會成為 G2 的標配，「只報 pass@1」會像今天「只看覆蓋率」一樣讓人皺眉。這是我的判斷，不是任何一份趨勢報告的結論。

> **當實作與測試都出自 agent、又缺少獨立審查，綠燈只是它通過自己出的題。量測它交出的成果，再把人的時間留給需要判斷的地方。**

對我來說，這套設計最後仍然回到第一節那位被問「測過了嗎」的工程師。希望他下次不用只轉述 agent 的回答，而是能和 reviewer 一起看證據、提出疑問，也知道哪些問題還值得花時間查下去。工具先完成可重複的檢查，人才有餘裕繼續做這部分的工作。

系列後三篇分別展開 test gate、review gate 與 reliability gate。若要從手上的 PR 開始，可以先讀〈測試篇：怎麼審閱一份 agent 寫的測試〉，確認那些已經變綠的測試，究竟保護了什麼。

---

### 系列文章

三篇深掘各講一道閘：

1. **總論（本篇）**
2. 一、測試篇：怎麼審閱一份 agent 寫的測試—斷言鬆綁、凍結 bug 與 mutation score（即將發布）
3. 二、Review 篇：Review 是控制點，不是瓶頸—分流、reviewer agent 艦隊與閉環禁令（即將發布）
4. 三、可靠度篇：SWE-Gate 量測到的 34%—constraint tests、pass^k 與授權擴張的閘門（即將發布）

延伸閱讀「Agentic Engineering 三部曲」：[總論](https://fantasybz.medium.com/%E5%88%A5%E6%80%A5%E8%91%97%E6%89%93%E9%80%A0%E4%BD%A0%E7%9A%84-devin-agentic-engineering-%E7%9A%84%E7%B5%84%E7%B9%94%E7%AD%96%E7%95%A5%E8%88%87-90-%E5%A4%A9%E8%A1%8C%E5%8B%95%E8%97%8D%E5%9C%96-7342ababc417)、[組織篇](https://fantasybz.medium.com/agentic-engineering-%E4%B8%89%E9%83%A8%E6%9B%B2-%E4%B8%80-%E8%AA%B0%E4%BE%86%E5%81%9A-platform-federation-%E7%9A%84%E7%B5%84%E7%B9%94%E8%A8%AD%E8%A8%88%E5%AF%A6%E5%8B%99-9d9353ef7f3a)、[技術篇](https://fantasybz.medium.com/agentic-engineering-%E4%B8%89%E9%83%A8%E6%9B%B2-%E4%BA%8C-harness-%E8%97%8D%E5%9C%96-%E6%8A%8A%E7%B3%BB%E7%B5%B1%E8%AE%8A%E6%88%90-agent-%E8%AE%80%E5%BE%97%E6%87%82%E7%9A%84%E5%9C%B0%E6%96%B9-f2a139f5b561)、[營運篇](https://fantasybz.medium.com/agentic-engineering-%E4%B8%89%E9%83%A8%E6%9B%B2-%E4%B8%89-eval-%E5%96%AE%E4%BD%8D%E7%B6%93%E6%BF%9F%E8%88%87%E8%A6%8F%E6%A8%A1%E5%8C%96-%E6%8A%8A-agent-%E7%95%B6%E7%94%A2%E5%93%81%E7%87%9F%E9%81%8B-d6d9623c2dc6)。

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
