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

# 綠燈不是驗收（一）測試篇：怎麼審閱一份 agent 寫的測試—斷言鬆綁、凍結 bug 與 mutation score

> **TL;DR** — 總論說：當實作與測試都由 agent 撰寫、測試尚未經獨立審查，綠燈還不足以支持驗收。這一篇講 test gate 的工具。測試寫下了 agent 對需求的理解，因此也需要被審閱。常見風險有四種：斷言被鬆綁、現狀 bug 被錄成 golden、測試無法辨識錯誤或走的不是規格要求的路徑、覆蓋率被當成品質。單靠人眼並不可靠：一項 86 位開發者的實驗裡，判斷 LLM 所寫錯誤斷言的準確率只有 49%，信心卻沒降。本篇用 **assertion-change diff、red-then-green、diff-scoped mutation score** 協助辨識這些風險，並交代各自的成本與限制。文末附 tester 審閱測試的十題 checklist，以及我在模式語言工作坊遇到的「測試全綠、replay 從未執行」實例。那個例子讓我看見：測試有效性之外，還得有人確認實作是否回應了原本的需求。

> 系列導覽：[總論](https://medium.com/p/582f24223eea) → **一、測試篇（本篇）** → 二、Review 篇（即將發布） → 三、可靠度篇（即將發布）

---

## 一、「AI 說沒問題」之後，tester 的新工作

James Bach 是 Context-Driven Testing 與 Rapid Software Testing 方法論的作者。總論借他的語言，把兩件常被混在一起的事切開：checking 是照著已知的規則對答案，testing 是人在判斷這個東西到底行不行。

照這個分法，CI 執行的是 checking；agent 說「測試全過」，則是在陳述檢查結果，還需要回頭核對執行紀錄。至於這些檢查是否足以支持驗收，仍然是 testing 所需要的人的判斷。

總論也給了這條界線的第一個數字。SWE-Gate 這個 benchmark 在一批 Python repo 的修補任務上，把功能測試與 reviewer 提出的約束（constraint）分開執行檢查，結果是通過功能測試的修補裡，有 34% 違反了約束。也就是說，綠燈沒有涵蓋 reviewer 真正在乎的那些要求。

那是綠燈無法涵蓋的其中一層。本篇要談的是更前面的另一層：測試本身有沒有用。這是三道閘裡的第一道，test gate。三道閘就是這個系列的三篇深掘，test gate 在本篇，review gate 是下一篇，reliability gate 在可靠度篇。

至於三分法（agent 的陳述、agent 寫的測試、團隊擁有的測試），以及「什麼時候 agent 寫的測試才算團隊的測試」這條升格規則，總論第二節已經寫過，這裡不重列。

先講為什麼測試比程式碼更需要審。Scrum Community 轉貼過 Lada Kesseler 的一句話，短到可以當標語，大意是：我對 AI 寫的測試的信任，比對它寫的程式碼還少。

理由很直接：測試是 agent 對自己的驗收標準，出題者與考生是同一個。程式碼寫錯了，測試還有機會攔下來。如果連測試的要求都被放寬，這道原本應該攔住錯誤的防線，也就失去了作用。

第二個理由來自 Bach。他說 tester 的核心能力是 rapid learning，也就是把陌生的東西快速學起來的能力。在 agent 時代這句話有一個具體的版本：讀 agent 留下的測試，比讀它的程式碼更快知道它理解了什麼、沒理解什麼。

原因是測試是 agent 對需求的翻譯。程式碼只告訴你它做了什麼，測試會告訴你它以為需求是什麼。翻錯的地方，斷言、fixture（測試前先準備好的資料與環境）與測試名稱會先露餡。

回到 Lada Kesseler 那句話。它是往「少信一點」走，台灣真正燒起來的討論在 DevOps Taiwan，方向剛好相反。Uncle Bob（Robert C. Martin）是 TDD 最主要的推廣者，有人把他「不讀 agent 的程式碼、只看測試與品質指標」的立場貼上去，底下吵成一串，也有人半開玩笑地要他把該做的測試全部列出來。

他其實列過（[2026-07-26](https://x.com/unclebobmartin/status/2081332683582427641)）：agent 寫得快，把省下的時間花在 unit、acceptance、property、torture、mutation 與 QA 測試上。property testing 用生成的輸入檢查應成立的性質；torture 則把輸入、負載或並行程度推到正常範圍之外，看系統在哪裡失效。這幾種方法各有用途，本篇只深談 mutation，因為它直接追問：程式碼被刻意改動之後，既有測試能不能辨識出差異？

我想用這一篇回應那場討論：除了列出測試種類，還需要把三個 check 與各自的門檻講清楚。順序是：先看 agent 寫的測試會壞在哪，再看為什麼人眼擋不住，然後是 mutation 這道門檻與 diff 上的三個 check，接著是覆蓋率為什麼當不了這道門檻，再用一個我親手實作時遇到的例子畫出它們的邊界，最後收在 tester 審一份測試的十題 checklist。要講 check 之前，得先知道它們各自在防什麼。

---

## 二、agent 寫的測試會壞在哪：四種型態

agent 寫的測試可能以不同方式失去保護力。本篇整理四種值得先檢查的型態：斷言被鬆綁、現狀 bug 被錄成 golden file、測試無法辨識錯誤，以及覆蓋率被當成品質。這是檢查的起點，不是一份能涵蓋所有問題的分類。

這四種壞法在 CI 上長得一模一樣，都是綠的。這裡只給 check 的名字，實作留到第五節。golden file 是事先存好的「正確輸出」，測試拿實際輸出與它比對；表裡提到的 mutant，是被故意改壞的一版程式碼，第四節會展開。四種型態與它們的偵測方式對照如下：

📌【在此插入表 table-01.png】

表裡第三欄要讀成可能的機制，不是對 agent 動機的判定。當回饋只獎勵「測試通過」，修正產品與放寬測試可能得到一樣的成功訊號。流程需要把兩者分開，讓 CI 不只回報有沒有綠，也能指出測試要求是否被改變。

這些風險也出現在其他分類裡。李博杰是 Pine AI 的首席科學家、《深入理解 AI Agent：設計原理與工程實踐》的作者。他在第七章談失敗歸因，也就是從執行紀錄追問錯誤從哪一步開始。其中一類叫 hack 驗證環境：改斷言、加 skip、用 mock 繞過被測邏輯，以及聲稱「測試已通過」卻沒有執行紀錄。

前三項在上面那四種裡都找得到位置，第四項不在：那是連測試都沒有執行，只有一句宣稱。他也提醒，這類分類還會持續擴充；本篇只借用與測試相關的部分。

第四項連 checking 都算不上：只要 CI 實際執行一次測試，就能核對這句宣稱。四種壞法都是測試跑了而且是綠的，這一項是綠燈之前的事，所以本篇不把它列成第五種。

還有一種壞法不列進表，因為它不是測試自己壞掉，是 red-then-green 這道檢查會踩到的坑：**因為錯的理由紅**。

LeSS in Action 這門課教 A-TDD（Acceptance Test-Driven Development，先寫驗收測試再寫實作）時有一條紀律，就是關注錯誤訊息，錯誤訊息要符合預期。red-then-green 的 red 套用同一條紀律：要看到預期的斷言失敗，不是 import error 這種「測試根本沒跑到」的紅。

第三列還有一種更難辨識的情況，留給第七節的工作坊實例。測試會失敗、斷言也是真的，卻走了錯的路徑：它直接從記憶體裡讀取物件，規格要的則是從事件重播還原狀態。只對既有實作執行這三個 check，未必能發現整條需求路徑被省略；還要對照需求建立約束。

把四種壞法與它們各自的 check 排在一起，會看到壞掉的方式雖然有四種，人要防的其實只有兩件事：測試被改弱，與測試沒測到。

📌【在此插入圖 diagram-01.png】

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

📌【在此插入表 table-02.png】

表裡「人眼」那一欄有一個共同點：每一格的問題都不是人不夠認真。有些訊號在視覺上根本不顯眼，被刪掉的斷言在 diff 裡就是紅色的一行，跟其他幾百行紅色長得一模一樣。有些問題則要實際執行測試才會浮現，光靠閱讀程式碼，再仔細也看不到。

---

## 四、Mutation testing：當閘門，不當儀式

Mutation testing 會刻意改動程式碼，例如換一個運算子、改一個常數或反轉條件，再執行測試。測試失敗，表示它抓到了這個 mutant，通常稱為「殺死」；測試沒失敗，mutant 就存活。存活可能代表測試缺口，也可能是變動沒有改變可觀察的行為，需要進一步判讀。mutation score 統計的是納入計分的 mutant 中，被測試殺死的比例。

它對測試做的事，跟 chaos engineering 對 production 做的事是同一個念頭：先自己弄壞一次，看警報會不會響。差別只在弄壞的對象是程式碼，會響的是測試。

拿 mutation 當閘門不是我先提的。Uncle Bob 的閘門組合是 coverage、CRAP score 與 mutation tests。CRAP score（Change Risk Anti-Patterns）把複雜度與覆蓋率合成一個數字，又複雜又沒被測到的函式分數最高。

這組閘門與它的理由出自他的一則貼文（[2026-07-30](https://x.com/unclebobmartin/status/2082850576832905657)）：TDD 是人的紀律，他不期待 agent 遵守，改用量測結果判斷品質。

第一節那個「不讀 agent 的程式碼」的立場，就是這個。DevOps Taiwan 轉述的是另一份清單：unit、Gherkin（用 Given／When／Then 寫成的驗收測試語法）、mutation 與品質指標，過了他就不再讀 code。兩份清單不完全一樣，但都有 mutation。

本文不走到那麼遠。Review 篇會說人還是要審閱 intent 與 constraint 報告，但同意 mutation 是 test gate 的核心。

mutation testing 不是新東西，執行成本卻一直是導入時要面對的問題。產生 N 個 mutant，就需要對這些變異反覆執行測試；即使用 test selection 縮小每次執行的範圍，這筆成本也不會消失。

agent 讓測試產出變快，也讓逐份人工審閱更難負擔，因此更需要衡量測試的有效性。能控制成本的方法之一，是只對 agent 改動範圍做 **diff-scoped mutation**，減少需要產生與執行的 mutant。這種縮小範圍的做法並非 agent 時代才出現，也不保證一定便宜；是否划算，仍要看受影響測試的執行時間。

總論第十節講過一句話：驗證工具的價值由觸及範圍決定。diff-scoped mutation 的觸及範圍，正好是 agent 剛改的那幾行。

它的限制也需要先說清楚：mutation 衡量的是「已經寫出來的程式碼有沒有被測試守住」，無法偵測「規格要求的東西根本沒有寫出來」。

具體一點說，它會告訴你這個條件判斷翻過來之後沒有任何測試變紅，不會告訴你這個模組少了一條架構規則、少了一條 business constraint，或是規格要求的那條路徑根本不存在。第七節的例子就是後面這一種。

回到成本。多數人裝這道 check 的時候，面對的是 brownfield，也就是已經跑了很多年、測試套件又大又慢的既有系統。Brownfield 的現實：40 分鐘的測試套件上，diff-scoped mutation 仍然要把受影響的測試重複執行 N 次。

所以它是四道 check 裡**最後裝**的，只在受影響子集能在 10 分鐘內跑完的 repo 上啟用。為什麼是這個順序，總論第十節講過，這裡不重列。

**儀式版與閘門版的差別**：這一題今年夏天被問過兩次。第一次是 Thoughtworks 的 Birgitta Böckeler，她問的是「TDD inside the agent loop—theater or actual value?」（Martin Fowler [2026-08-11](https://x.com/martinfowler/status/2087173563144912985) 轉貼）。agent 在自己的迴圈裡做 TDD，是做給人看的戲，還是真的有價值。

第二次是 Uncle Bob 8 月 17 日做的實驗（negative test experiment），問的是同一題的另一面：他讓四種測試紀律各寫一次同一支程式，驗收測試全綠，程式卻不一樣（[2026-08-17](https://x.com/unclebobmartin/status/2089449442089025936)，設計與結果總論講過）。

這兩個討論讓我回到同一個問題：流程的形狀對了，還需要檢查它是否真的提供保護。叫 agent「執行 mutation，再補測試補到 100%」，如果只追分數，就可能得到過度迎合變異算子的測試。這些測試未必是假的，卻仍然可能漏掉規格裡根本沒有被實作的要求。

閘門版先讓 CI 列出存活的 mutant，再區分需要補測試的缺口與 equivalent mutant。後者指變動前後的可觀察行為相同，測試原本就無法區分。可確認的等價變異應排除並留下理由，其餘缺口再交給 agent 補測試，由人判讀需要裁量的部分。這樣才不會把每份報告全部丟回 reviewer。

門檻是我的建議值，不是業界標準：agent 改動行的 mutation score ≥ 70% 才進入 review。導入時先提供一個月的報告，再開始阻擋未達標的 PR。這個數字是 Uncle Bob 的做法加上我的初步估計，11 月會補上自己的數據。

工具方面，JVM 有 PIT、JS 與 TS 有 Stryker、Python 有 mutmut。能不能限定在 diff 範圍，各家支援程度不同，動手前先確認你那套的做法。

把這一節的兩個門檻，跟另外兩道 check 的門檻放在一起，就是本篇的建議值總表：

📌【在此插入表 table-03.png】

表裡最容易被跳過的是備註欄的第一列：先提供一個月的報告，再阻擋未達標的 PR。團隊需要先從報告裡看見問題，才知道為什麼值得為這道閘停下來。順序反過來，第一個被擋住的 agent PR 就可能讓整套機制被撤掉。閘門的可信度，要靠這段使用經驗慢慢累積。

---

## 五、Diff 上的三個 check：reference implementation

前面幾節說明了判斷的依據，這一節把它們變成 CI 裡可以執行的檢查。三個 check 各自防範不同的問題，導入前也各有需要確認的條件。

三個都是由 CI 自動執行的檢查。導入時先建立前兩個，再加入成本較高的 mutation。

**Check 1：red-then-green。** 這一道問的是最基本的一件事：這個新測試，在 bug 還在的時候會不會失敗。會失敗，它才有資格說自己抓得到那個 bug。

適用範圍先講。本文的 red-then-green 只對「修改既有行為」的 PR 啟用，也就是 bug fix 與 behaviour change。feature PR 可能依賴 base branch 尚不存在的類別或介面，失敗原因就會是無法載入，而不是預期的行為差異。

這也是本文不把 red-then-green 套用到所有 feature PR 的理由：先排除無法比較的情境，才能讓 red 代表有意義的行為差異。feature PR 的新測試先由 Check 3 輔助評估，再回到需求確認是否測對了對象。

**分類的來源必須不是 PR 的作者。** 如果由開 PR 的 agent 自己設定分類 label，事情很快會變質。agent 被「讓測試過」的 reward 驅動，它會學到一件事：所有 PR 都標成 feature，就不會被檢查。

閘門的適用範圍不能由受檢者決定。這跟系列的「衡量產出，而不是檢查過程的形式」是同一件事。

分類的來源有三個，照順序取。第一個是 issue 或 ticket 的 type 欄，那一欄是人設的。第二個是 harness 的 task type。harness 是 agent 與工程系統之間那層介面，上一季技術篇講過。兩個都沒有時，改用 diff 判斷：只要 PR 修改了任何既有的非測試檔案，就視為 behaviour change，執行這道檢查，只新增檔案的才跳過。

前兩個來源必須由人或受保護的 harness 設定維護，agent 才不能自行改分類。第三個只是沒有任務資訊時的保守推定：它看得出有沒有改既有檔案，看不出需求是否完整。只新增檔案的 fix 也可能漏過，因此分類結果仍要接受抽查。

CI job 的做法是把 PR 新增的測試 checkout 到 base branch 上，執行一次，輸出分三類。

（a） 測試沒有失敗。標記 `test-never-fails`，這是唯一會加上這個標記的一類。

（b）測試因為預期的行為差異而失敗。對 bug fix，這表示它能重現原有缺陷；對 behaviour change，則表示它能辨識新舊要求的差異。這只完成 red，還要確認同一份測試在修補後通過，才完成 green。

（c）測試因為預期之外的原因失敗，例如 import error、fixture 不存在。這類結果不加 `test-never-fails`，但也不能當成驗證通過。先在報告列明原因，再由人確認是否需要拆開 PR、補齊環境或修正分類，之後重新執行。

把適用範圍與三個出口畫成一張圖，會看到它其實是一個分流器：

📌【在此插入圖 diagram-02.png】

red-then-green 只對修改既有行為的 PR 啟用。在這三種結果裡，只有「測試沒有失敗」會被標記為 `test-never-fails`。

這三個出口的意義不同：沒有失敗，要查測試是否有辨識力；預期失敗，要接著驗證修補後能通過；非預期失敗，則表示目前還無法判定。把「無法判定」與「通過」分開，才不會讓一份有紅字的報告反而被誤當成綠燈。

**Check 2：assertion-change diff。** 這一道處理的是更安靜的風險：測試檔還在，測試名稱也沒變，但原本抓得到 bug 的斷言被改弱了。CI 依然全綠，diff 上也只是幾行紅綠交錯。

既有斷言被改動時，先不要問 agent 為什麼改，先依四類分級：

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

📌【在此插入圖 diagram-03.png】

三個 job 可以平行執行，結果彙整成同一份報告；red-then-green 依分類決定是否執行。這裡示範的是導入初期的報告模式，第一個月暫不阻擋 PR，不是前面所說的正式閘門已經生效。

第一個月不阻擋是刻意的。那一個月要做的是校準噪音、確認分類來源沒有錯、讓人對報告的格式建立信任。等大家知道哪些訊號真的代表風險，再把最確定的那幾項升成阻擋。

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

這份設計有兩個地方值得看。一個是 `red-then-green` 透過 `if` 讀取 `classify` 的輸出，決定是否執行檢查，適用範圍是機器決定的，不是 PR 作者決定的。另一個是 `report` 的 `if: always()`，red-then-green 被跳過時仍然要產生報告，不然 feature PR 在報告上會看起來像沒被檢查過。

還有第三個地方，yaml 裡看不到：檢查器自己也會漏。今年九月在東京的 AGNTCon Japan（Linux Foundation 旗下 Agentic AI Foundation 辦的 agent 大會）上，Quartic.ai 的兩位 SRE 講了他們讓 agent 升級 production Kubernetes 的經驗。

Kubernetes 一次只能升級一個小版本，每次升級算一跳。他們在台上自己講了第一版怎麼漏的：驗證只檢查每一跳之後的第一個節點，管理節點（control plane）上到 1.31、跑工作的節點還留在 1.30，那一跳照樣被標成成功。

修法是按角色找出每一個節點，確認所有節點的版本都符合預期，才准開始下一跳。他們把這段經驗整理成一句話：「A cluster upgrade succeeds only when the whole cluster has crossed the version boundary.」

只檢查部分節點，得到的結果就只能代表那些節點。整個叢集是否完成升級，仍然沒有被驗證。

這份 yaml 自己就有兩個地方踩到同一個盲點。`mutation_diff` 底下多數工具以檔案為單位，限定不到行就得自行篩選，篩選器漏掉的行不會出現在報告上。`classify` 找不到連結的 issue，就退回看有沒有改既有的非測試檔，那一步辨識的是「修改了既有檔案」，不等於確認「修改了行為」。這兩個檢查都有各自能涵蓋的範圍，報告的名稱卻很容易讓人以為它們已經檢查了全部。

Quartic.ai 的示範跑在 kind（本機模擬用的 Kubernetes）叢集上，這一課在 production 付過什麼代價，投影片沒寫。

所以校準時還要多確認一件事：這三個 check 實際檢查了哪些範圍，又漏掉了什麼。

**Agent 側的配套。** 前面三個 check 都在 CI 上檢查產出。但 agent 若認為既有測試有錯，除了反覆嘗試或修改斷言，流程還能提供什麼處理方式？

一項研究（escalation channels，2026 年 8 月）試著增加另一條路：給 agent 一個結構化的「回報壞測試」工具，讓它認為測試有問題時可以提出證據，不必直接修改斷言。這可以與 CI 的阻擋機制並用。下面的 reward hacking 指為了取得通過訊號而扭曲驗證；勝算比（odds ratio）比較兩組發生該行為的勝算，要連同比較方向與研究設定判讀；frontier model 是研究當時能力最前沿的那幾個 model。

研究在 8 個 frontier model 上量測效果：reward hacking 從 23.6% 降到 5.3%，論文另報告勝算比 9.2；其中 6 個 model 在受測樣本中不再出現該行為。98.7% 的 escalation 不涉及作弊，缺陷偵測覆蓋率（defect-detection coverage）增加 10.1 個百分點。

最後兩個數字讓這個做法值得嘗試：在受測情境裡，多數回報沒有伴隨作弊，缺陷也被辨識得更多。它不是保證 agent 從此誠實，而是讓「提出可核對的問題」成為一條可走的路。導入時有兩個部分。

**第一步，在 harness 裡註冊這個 tool。** 它的呼叫格式如下：

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

`reason` 與 `evidence` 兩個欄位是關鍵。它們逼 agent 把「這個測試錯了」寫成一個可以被人否決的主張，而不是一句抱怨。

**第二步，在 AGENTS.md 裡告訴 agent 這條路存在。** AGENTS.md 只加一句：「你認為測試錯了，就呼叫 `report_broken_test`，不要改斷言。」工具註冊之外，也要交代何時使用、提出什麼證據，以及回報後由誰接手。

這讓「改環境比寫規則有效」有了具體做法：一邊限制任意改動斷言，一邊提供提出異議的管道。團隊接下來要確認的，是回報有沒有被處理，而不只是工具有沒有被呼叫。

最後一個小東西，成本幾乎是零：PR template 加一個「golden 來源」欄，必填。新的 snapshot 或 golden file 從哪裡來，只有三個答案可以選：規格、production 的實際輸出、還是「現在跑出來就是這樣」。

第三個答案不是不行，但要寫出來，讓 reviewer 看得到。凍結 bug 的 golden，幾乎都是在沒有人問這個問題的時候長出來的。

---

## 六、覆蓋率是一條可以被改掉的斷言

覆蓋率是多數團隊已經裝好的那道閘，也是最容易被誤讀的一個數字。一組資料就能說明它誤讀在哪裡。

一項研究（Test Coverage of Agentic PRs）量測了 4,882 個 agent PR，問的問題很窄：repo 原有的測試，會不會經過 agent 改動的那些可執行的行？答案是 Java 只有 61.5%，Python 只有 27.0%。

這裡的分母是該研究樣本中 agent 改動的可執行行，不是所有 Python repo，也不是整個 repo 的覆蓋率。結果提醒我們：就算整體覆蓋率看起來不差，新改動的區域仍可能缺少既有測試保護。

因此，要評估眼前這個 PR，還得另外檢視改動範圍的覆蓋率。整體數字可以保留，但不能替這份改動回答問題。

這也是為什麼覆蓋率很容易被 game。game 在這裡當動詞用，指的是不改善品質、只把數字做漂亮。

三種 game 法都很便宜。第一種是 exclude pattern 加一行，那個檔案從此不算進分母。第二種是只呼叫、不斷言，行被跑到了，行為沒有被檢查。第三種是把難測的邏輯搬到被排除的檔案裡。

這三種都不一定是惡意的，有時候只是趕時間，有時候是 legacy code 真的難測。但結果一樣：覆蓋率變漂亮，測試對行為的約束沒有變強。

所以處方也要窄，先不要把整個 coverage 制度重做一遍。可以先從三件事做起：

第一條，覆蓋率只看 agent 改動的行。這條縮小範圍，讓整體數字沒有辦法替新的程式碼擋子彈。

第二條，將覆蓋率與 mutation score 搭配判讀。程式碼被執行過，不代表行為有被斷言守住，mutation 補上的正是這項檢查。

第三條，exclude pattern 的變更由人類審核。這條把最便宜的那道逃生門關上。

一句話：**覆蓋率告訴你測試跑過哪裡，mutation 告訴你測試守住哪裡。**

---

## 七、第一手實例：測試全綠，replay 從未執行

今年 8 月，我在 Teddy 老師（泰迪軟體講師，部落格「搞笑談軟工」作者）的模式語言工作坊上，拿講師提供的同一份需求檔，分別用兩種方法完成實作：方法 A 只照那份檔案直接寫（工作坊叫它「裸 Prompt」），方法 B 另外加入講師提供的一套作業流程。兩種方法各自在獨立的 git worktree 裡執行，也就是同一個 repo 底下的獨立工作目錄。需求本身很小，就是一個 Product aggregate（領域驅動設計裡一組要一起保持一致的物件）加一個 CreateProduct use case。

下面只談方法 A，因為要講的問題出在它身上。如果只看交付清單，方法 A 的成果很容易讓人放心：25 個檔案、編譯零 warning、5 個測試全綠、分層乾淨、Javadoc 完整。

問題在測試走的路徑。規格要的是 event sourcing：aggregate 不直接存狀態，只存每一次發生的事件，要用的時候再從事件一件一件重播回來。

方法 A 的 Product 完全不是 event sourcing。它沒有繼承 `EventSourcedAggregate`，測試也直接從記憶體裡的 aggregate 呼叫 `getDomainEvents()` 讀取事件，永遠不經過重播的路徑。

我當時的紀錄是：A 的 10/16（工作坊的 16 項合規清單過了 10 項）不是「差一點」，而是「在只有一個 InMemory use case 的玩具規模下剛好還沒爆」。

還有一個跟 replay 無關的小洞：測試缺了 `@DirtiesContext`。這是 Spring 用來把受污染的測試 context 移出快取、讓後續測試重新建立 context 的標註。若測試已改變共用狀態，卻沒有適當重設或隔離，就可能發生相互干擾。只靠 retry 把結果重試到綠，並沒有解決這個問題；這也是第八節清單裡會追問 flaky 處理方式的原因。

先說這個例子能證明什麼、不能證明什麼。這是「綠燈但沒驗收」與「測錯對象」的實例，不是變異數據（variance，同一題重跑幾次結果會差多少）。N 等於 1，衡量的是合規程度。變異的題留給 11 月。

回頭看這個例子，我更想釐清的是：每一道 check 到底能幫上什麼忙，又會在哪裡停下來。把能力與限制逐條寫清楚，才知道這份綠燈之外還缺了哪些證據：

- **red-then-green 不適用**：這是 feature PR，新測試對舊 code 一定因為類別不存在而紅。
- **mutation 也抓不到**：程式碼裡根本沒有 replay 路徑，所以不存在「replay 路徑的 mutant」可以活。
- **抓得到的是兩樣東西**：一條 constraint test（把 reviewer 提出的約束寫成可執行檢查的測試），以及由人審閱 intent。

mutation 那一條值得多說一句。Product 既然不是 event sourcing，那個 in-memory aggregate 的 mutation score 很可能還很漂亮。這正是第四節那一句：它無法偵測「規格要求的東西根本沒有寫出來」，是更好的 check，不是 testing。

constraint test 那一條的內容會長這樣：aggregate 必須繼承 `EventSourcedAggregate`，或至少一個測試必須經由 rehydrate 建構 aggregate。rehydrate 就是從事件把 aggregate 重建回來的那個動作，也就是規格真正要的那條路徑。這是可靠度篇第二節說的「架構規則」那一類。

人審閱 intent 時，則可以從一句問題開始：「這是 event sourcing 嗎？」

這個例子沒有實測本篇的 test gate，也沒有比較三道閘的效果。它能清楚說明的是：原有測試全過，仍然沒有驗證規格要求的路徑。要補上這個缺口，需要先由人辨識需求與實作的落差，再把能重複檢查的部分寫成 constraint tests。

把規格要的路徑與測試實際走的路徑畫在同一張圖上：

📌【在此插入圖 diagram-04.png】

5 個測試全綠，規格要的 replay 路徑從未被執行。

圖上那條虛線才是重點。它是規格要求存在、但實作與測試都沒有走過的路徑。任何只看「已經寫出來的東西」的 check，都看不到一條不存在的線。

檢查器能做到的事停在這裡，人還需要回到原本的需求，確認實作是不是走在正確的路上。

感謝 Teddy 的工作坊，讓這個容易停留在概念裡的落差，成了一份可以回頭檢視的實作經驗。

---

## 八、Tester 的角色：從打勾機器到 test-suite reviewer

到這裡，前面幾節可以收斂成一張很小的清單。它不要求任何人重讀所有測試，它要求的是問對問題，而且多數問題已經有工具會回答。

審閱一份 agent 寫的測試時，可以逐一確認這十個問題：

📌【在此插入表 table-04.png】

前八題可以先由工具提供線索，後兩題更需要回到需求判斷。最後一題尤其值得留著：刪掉一個測試後，哪些行為會失去保護？如果答不出來，可能是測試無效，也可能只是與其他測試重複；下一步是釐清它的用途，不是立刻把它判成「永不紅」。

這就是 tester 在 test gate 的位置：不是打勾機器，是 test-suite reviewer。工作內容從「跑完測試、確認全綠」，換成「閱讀報告、判斷哪些訊號需要人介入」。

Lisa Crispin 與 Tip House 的《Testing Extreme Programming》說「人人都是測試者」。agent 時代這句話的具體版本是：每個 merge agent PR 的人，都在審一份測試。

---

## 九、結語

回到工作坊那個全綠的方法 A。對我來說，這份實作最值得留下的，正是它看起來沒有問題的樣子。A 的測試沒有一個是假的，每一個都真的在跑、真的在斷言，只是全部繞過了規格要的那條路徑。那份綠燈沒有說謊，它只是從來沒有承諾過要涵蓋你以為它涵蓋的東西。

本篇給的三個 check 只做一件事：把「綠燈沒承諾的部分」裡，機器能量測或檢查的部分，逐項呈現在報告裡。assertion-change diff 檢查斷言有沒有被改弱，red-then-green 驗證新測試能否辨識修正前後的差異，diff-scoped mutation 則檢查測試能否發現改動範圍內的變異。這三項 check 未必找得到方法 A 省略的需求路徑，還需要依需求建立 constraint test，以及人對 intent 的審閱。三個都只是更好的 check，不是驗收。

> **agent 寫的測試是它對自己的驗收標準；審它的測試，就是審它以為的「對」。**

下一篇是 Review 篇：test gate 過了之後，這個 PR 誰要讀、讀什麼、誰審誰，以及 AI 審 AI 什麼時候該禁止。至於 Bach 說不能自動化的那一件—對 agent 產出做探索式測試，不是讀它的測試，是去用它做出來的東西—那是另一篇文章的題目，這裡只點到為止。

---

### 系列文章

1. [總論：綠燈不是驗收—agent 時代的測試、Review 與可靠度](https://medium.com/p/582f24223eea)
2. **一、測試篇（本篇）**
3. 二、Review 篇：Review 是控制點，不是瓶頸—分流、reviewer agent 艦隊與閉環禁令（即將發布）
4. 三、可靠度篇：SWE-Gate 量測到的 34%—constraint tests、pass^k 與授權擴張的閘門（即將發布）

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
10. 上一季：[技術篇](https://fantasybz.medium.com/agentic-engineering-%E4%B8%89%E9%83%A8%E6%9B%B2-%E4%BA%8C-harness-%E8%97%8D%E5%9C%96-%E6%8A%8A%E7%B3%BB%E7%B5%B1%E8%AE%8A%E6%88%90-agent-%E8%AE%80%E5%BE%97%E6%87%82%E7%9A%84%E5%9C%B0%E6%96%B9-f2a139f5b561)第五節（flaky quarantine）
11. 李博杰《深入理解 AI Agent：設計原理與工程實踐》v2.0 — [第七章〈Agent 的評估〉](https://bojieli.github.io/ai-agent-book/book-en/chapter7/)（2026-09-06，§7.5.2 失敗歸因的 Coding Agent 錯誤分類表）〔第二節〕
12. Quartic.ai — [Letting an Agent Upgrade Production Kubernetes — Without Getting Paged at 3 AM](https://sched.co/2QlD9)（AGNTCon + MCPCon Japan 2026，2026-09-10；[講者投影片](https://hosted-files.sched.co/agntconmcpconjapan26/d9/AGNTCon-MCPCon-Japan-2026_Abhijeet_Sanskar_final.pdf#page=29) slide 29）〔第五節〕
13. Spring Framework 官方文件 — [@DirtiesContext](https://docs.spring.io/spring-framework/reference/testing/annotations/integration-spring/annotation-dirtiescontext.html)，說明測試 context 的失效、移除與重建〔第七節〕。

---

### AI 協作說明

本文由筆者提出初步構想與章節架構，文字撰寫由 AI（Claude）協作完成，再經筆者逐節校閱與修訂後定稿。文中觀點與判斷為筆者所持，文責亦由筆者自負。

---

*本文發表於 [Medium @fantasybz](https://medium.com/@fantasybz)。若你正在幫團隊裝第一道 test gate，歡迎交流。*
