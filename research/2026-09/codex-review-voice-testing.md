我會只讀你指定的 repository 檔案，先抓作者聲線基準，再逐段檢查 `2026-10-green-testing/article.md`，不碰你列出的禁讀路徑。
<!-- codex ran: /bin/zsh -lc 'wc -l research/2026-09/codex-review-voice.md' -->
<!-- codex ran: /bin/zsh -lc 'wc -l .context/research/medium_posts/2025-06-23-c3e8ca1e2eb5.txt' -->
<!-- codex ran: /bin/zsh -lc 'wc -l .context/research/medium_posts/2025-08-11-4c58a488c9f5.txt' -->
<!-- codex ran: /bin/zsh -lc 'wc -l .context/research/medium_posts/2025-12-28-642ef2eafc4b.txt' -->
<!-- codex ran: /bin/zsh -lc 'wc -l 2026-09-agentic-engineering-platform/article.md' -->
<!-- codex ran: /bin/zsh -lc 'wc -l 2026-10-green-testing/article.md' -->
三篇 Medium 匯出檔看起來是長行格式，所以我會分別讀完整內容，但避免掃描其他目錄。接著會用行號整理目標文的段落位置。
<!-- codex ran: /bin/zsh -lc "sed -n '1,180p' research/2026-09/codex-review-voice.md" -->
<!-- codex ran: /bin/zsh -lc 'nl -ba 2026-10-green-testing/article.md' -->
目標文已讀到全文。接下來我會讀你指定的三篇長文與 2026-09 已發布格式，主要抽「長段如何銜接、如何先設限制再下判斷、圖表前後怎麼導讀」這些寫作習慣。
<!-- codex ran: /bin/zsh -lc 'wc -c .context/research/medium_posts/2025-06-23-c3e8ca1e2eb5.txt' -->
<!-- codex ran: /bin/zsh -lc 'wc -c .context/research/medium_posts/2025-12-28-642ef2eafc4b.txt' -->
<!-- codex ran: /bin/zsh -lc 'wc -c .context/research/medium_posts/2025-08-11-4c58a488c9f5.txt' -->
<!-- codex ran: /bin/zsh -lc "nl -ba 2026-09-agentic-engineering-platform/article.md | sed -n '1,260p'" -->
<!-- codex ran: /bin/zsh -lc "nl -ba 2026-09-agentic-engineering-platform/article.md | sed -n '261,540p'" -->
2026-09 已發布稿的節奏很清楚：開場用問題鋪路、圖表前多半有一句「先看／把它放進系統」、表格後會補一句判讀。現在我會讀三篇舊 Medium 長文，拿來校準「不是簡短不能用，而是哪些短段少了橋」。
<!-- codex ran: /bin/zsh -lc "perl -CS -0pe 's/FollowWritten by.*//s; s/(ListenShareMore|Press enter or click to view image in full size)/\\n"'$1'"\\n/g; s/([。？！])/"'$1'"\\n/g; -->
第一篇 Medium 檔案本身是 mojibake 文字，需要先用「Latin-1 bytes 還原成 UTF-8」才能讀；我會只在 stdout 做轉碼，不寫任何中間檔。
<!-- codex ran: /bin/zsh -lc "python3 -c \"from pathlib import Path; s=Path('.context/research/medium_posts/2025-06-23-c3e8ca1e2eb5.txt').read_text(encoding='utf-8'); print(s[: -->
轉碼不是整段都一致：有些字元已經是正常 Unicode，有些是 mojibake。我要先確認範圍，再用較保守的修復方式讀正文。
<!-- codex ran: /bin/zsh -lc "python3 -c \"from pathlib import Path; s=Path('.context/research/medium_posts/2025-06-23-c3e8ca1e2eb5.txt').read_text(encoding='utf-8'); print(rep -->
我接下來會把三篇舊文轉成可讀的句段清單，只保留正文段落並去掉 Medium 介面尾巴；這一步是為了校準口吻，不會拿來重述文章技術內容。
這個 sandbox 連 here-doc 暫存檔都不允許，剛剛的命令被擋住了，沒有建立檔案。我改成 `python3 -c` 單行讀取。
<!-- codex ran: /bin/zsh -lc "python3 -c \"from pathlib import Path; p=Path('.context/research/medium_posts/2025-06-23-c3e8ca1e2eb5.txt'); s=p.read_text(encoding='utf-8'); key= -->
第一篇的正文已讀到後段。它的特徵很明顯：段落會先放來源、書摘、比喻，再把焦點拉回軟體實務；這跟目標文很多「只剩結論句」的段落形成對照。
<!-- codex ran: /bin/zsh -lc "python3 -c \"from pathlib import Path; s=Path('.context/research/medium_posts/2025-06-23-c3e8ca1e2eb5.txt').read_text(encoding='utf-8'); key='源起：K -->
<!-- codex ran: /bin/zsh -lc "python3 -c \"from pathlib import Path; s=Path('.context/research/medium_posts/2025-08-11-4c58a488c9f5.txt').read_text(encoding='utf-8'); print(rep -->
第二篇是 GenAI observability 類文章，正文更接近正式技術長文。這篇對目標文最有用的是它怎麼在表格、圖、範例之前補「為什麼要看這個」與「讀完該帶走什麼」。
<!-- codex ran: /bin/zsh -lc "python3 -c \"from pathlib import Path; s=Path('.context/research/medium_posts/2025-08-11-4c58a488c9f5.txt').read_text(encoding='utf-8'); key='CNCF -->
<!-- codex ran: /bin/zsh -lc "python3 -c \"from pathlib import Path; s=Path('.context/research/medium_posts/2025-08-11-4c58a488c9f5.txt').read_text(encoding='utf-8'); key='CNCF -->
第二篇讀完。它雖然有不少清單密度很高的段落，但會在段落前後補判讀句，例如「這張技術全景圖的重點，不是...」，這正是目標文圖表後多處缺掉的句型。
<!-- codex ran: /bin/zsh -lc "python3 -c \"from pathlib import Path; s=Path('.context/research/medium_posts/2025-12-28-642ef2eafc4b.txt').read_text(encoding='utf-8'); print(rep -->
第三篇是可觀測性反思文，語氣比第二篇更像作者成熟期的「現場經驗＋概念校準」。我會讀完整正文後，再回目標文抽出至少 12 段需要補肉的段落。
<!-- codex ran: /bin/zsh -lc "python3 -c \"from pathlib import Path; s=Path('.context/research/medium_posts/2025-12-28-642ef2eafc4b.txt').read_text(encoding='utf-8'); key='引言：從 -->
舊文校準完了。現在我會把目標文依小節與 paragraph 切開，找出那些本身可能正確、但缺主詞、過場或解讀而讓閱讀斷掉的段落。
<!-- codex ran: /bin/zsh -lc "python3 -c \"from pathlib import Path; lines=Path('2026-10-green-testing/article.md').read_text(encoding='utf-8').splitlines(); section=''; in_cod -->
<!-- codex ran: /bin/zsh -lc "python3 -c 'from pathlib import Path
lines=Path(\"2026-10-green-testing/article.md\").read_text(encoding=\"utf-8\").splitlines()
section=\"\"
in_c -->
已讀指定檔案。以下只針對可讀性與作者口吻，不摘要技術內容。

**判讀基準**
Kochi 舊文與 2026-09 已發布稿的長文 register，不是單純寫長，而是常有三層緩衝：先交代來源或限制，再用「換句話說／注意／這裡真正重要的是」把讀者接住，最後才下判斷。這篇的問題多半是判斷正確，但中間橋段被削太薄。

**過簡段落**
1. **一、「AI 說沒問題」之後，tester 的新工作**  
原文：「總論用 James Bach 的語言把 checking 與 testing 切開：CI 綠燈是 checking，agent 說「測試全過」也是 checking；驗收是 testing，是人的判斷。總論也用 SWE-Gate 的 34% 說了綠燈量不到 reviewer 的約束；本篇只談三道閘裡的第一道—test gate—也就是綠燈量不到的另一層：測試本身有沒有用。」  
問題／缺口：總論、James Bach、SWE-Gate、test gate 擠在同一段，舊文通常會先鋪「這篇從哪裡接上來」。缺鋪陳、缺過場、破折號當括號連用。  
改寫：「總論已經先借 James Bach 的語言，把 checking 與 testing 切開。CI 綠燈是 checking，agent 說「測試全過」也是 checking；它們告訴我們某些條件成立，但不等於人已經完成驗收。這篇文章把鏡頭往下拉到第一道閘：test gate。SWE-Gate 的 34% 說的是綠燈量不到 reviewer 的約束；這裡要看的，是更前面那一層，測試本身有沒有用。」

2. **一、「AI 說沒問題」之後，tester 的新工作**  
原文：「Bach 說 tester 的核心能力是 rapid learning。在 agent 時代這句話有一個具體的版本：讀 agent 留下的測試，比讀它的程式碼更快知道它理解了什麼、沒理解什麼。測試是 agent 對需求的翻譯；翻錯的地方，測試會先露餡。」  
問題／缺口：判斷很準，但少了舊文常見的「怎麼看出理解錯」的小橋。缺例子、缺解讀。  
改寫：「Bach 說 tester 的核心能力是 rapid learning。放到 agent 時代，我會把它翻成一件很具體的事：先讀 agent 留下的測試。程式碼告訴我們它做了什麼，測試更早告訴我們它以為需求是什麼；只要翻譯錯了，斷言、fixture、mock 或命名通常會先露餡。」

3. **二、agent 寫的測試會壞在哪：四種型態**  
原文：「第五種不單獨列，但要提：**因為錯的理由紅**。LeSS in Action 教 A-TDD 時有一條紀律—關注錯誤訊息，錯誤訊息要符合預期。red-then-green 的 red 也要檢查：是預期的斷言失敗，不是 import error。」  
問題／缺口：red-then-green 在正文還沒真正展開，讀者容易只記得術語。缺術語第一次出現沒解釋、缺連接詞。  
改寫：「第五種不單獨列，但要先把它放進讀者腦中：**因為錯的理由紅**。LeSS in Action 教 A-TDD 時有一條紀律，紅燈不是只有紅就好，錯誤訊息也要符合預期。red-then-green 的 red 也是同一件事；我們要看到的是預期的斷言失敗，不是 import error 這種環境或分類錯誤。」

4. **二、agent 寫的測試會壞在哪：四種型態**  
原文：「四種壞法各有一個便宜的 check，人不用逐行讀測試。」  
問題／缺口：這是圖後關鍵解讀，但只剩 caption。舊文圖表後常會補「這張圖真正要看的是」。缺解讀、缺過場。  
改寫：「讀這張圖時，不要把它當成 agent 測試問題的分類學，而要把它當成導入順序的草圖。四種壞法各有一個便宜的 check，重點是把人的注意力從「逐行讀測試」移到「看哪裡需要人判斷」；工具先把可機械化的壞味道撈出來，人再把剩下的 intent、constraint 與風險接住。」

5. **三、人眼不夠：49%**  
原文：「另一項 eye-tracking 研究補了一刀：標示為 LLM 產生的程式碼，reviewer 看得更久，但沒有看得更徹底。」  
問題／缺口：「另一項」主詞太薄，研究結果與上一段的關係需要讀者自己補。缺主詞、缺解讀。  
改寫：「另一項 eye-tracking 研究補了一刀：標示為 LLM 產生的程式碼，reviewer 看得更久，但沒有看得更徹底。這個結果跟前一段的 49% 合在一起看，意思不是人類 review 沒價值，而是單純要求 reviewer「更仔細」沒有形成新的資訊結構；時間被花掉了，判斷力卻沒有被工具放大。」

6. **四、Mutation testing：當閘門，不當儀式**  
原文：「它量不到什麼，也要先講：mutation 只量「已經寫出來的程式碼有沒有被測試守住」，量不到「該有的東西沒寫」。第七節會用到這一句—這正是它是「更好的 check」而不是 testing 的證明。」  
問題／缺口：這段 hedge 很重要，但少一層「量不到」的具體樣子。缺例子、缺解讀。  
改寫：「但它量不到什麼，也要先講清楚。mutation 只量「已經寫出來的程式碼有沒有被測試守住」，量不到「該有的東西沒寫」。換句話說，它很適合抓住已存在邏輯的防線漏洞，卻不會替團隊發現少了一條架構規則、少了一條 business constraint，或整條 replay 路徑根本不存在。第七節會用到這一句；這正是它是「更好的 check」而不是 testing 的證明。」

7. **五、Diff 上的三個 check：reference implementation**  
原文：「red-then-green 只對修改既有行為的 PR 開，三個出口只有「沒紅」是壞訊號。」  
問題／缺口：圖後總結太短，沒有把三個出口的判讀拉回人。缺解讀、缺過場。  
改寫：「這張圖要讀成一個分流器：red-then-green 只對修改既有行為的 PR 開，因為 feature PR 在 base branch 上紅，本來就多半是因為類別或入口不存在。三個出口裡，只有「沒紅」是壞訊號；「對的理由紅」代表測試真的抓到舊 code 的缺口，「錯的理由紅」則先留在報告裡，交給人判斷分類是不是混了。」

8. **五、Diff 上的三個 check：reference implementation**  
原文：「**Check 2：assertion-change diff。** 既有斷言被改動時，依四類分級：」  
問題／缺口：從 Check 1 跳到 Check 2 太快，assertion-change diff 的威脅模型沒先講。缺鋪陳、術語第一次出現沒解釋。  
改寫：「**Check 2：assertion-change diff。** 這一道處理的是更安靜的風險：測試看起來還在，名字也沒變，但原本能抓 bug 的斷言被改弱了。既有斷言被改動時，先不要問 agent 為什麼改，先依四類分級：」

9. **五、Diff 上的三個 check：reference implementation**  
原文：「**Check 3：diff-scoped mutation。** 只對 agent 改動的檔案產生 mutant，報告只列改動行上活著的 mutant—多數工具以檔案為單位，能不能直接限定到行各家不同（第四節），限定不到就自己過濾 survivors；feature PR 的新測試靠它。」  
問題／缺口：名詞密度高，且核心問題「只問 agent 改動行有沒有被守住」藏在中間。缺術語第一次出現沒解釋、名詞短語堆疊。  
改寫：「**Check 3：diff-scoped mutation。** 這一道不是要替整個 repo 做健康檢查，而是只問一個問題：agent 剛改的那些行，有沒有被測試真正守住。做法是只對 agent 改動的檔案產生 mutant，報告只列改動行上活著的 mutant；多數工具以檔案為單位，能不能直接限定到行各家不同（第四節），限定不到就自己過濾 survivors。feature PR 的新測試沒有 red-then-green 可以用，所以最後靠它。」

10. **五、Diff 上的三個 check：reference implementation**  
原文：「三個 job 平行跑，輸出報告給人讀，第一個月不阻擋。」  
問題／缺口：這是流程圖後的決策原則，但少了為什麼第一個月只 report。缺解讀、缺鋪陳。  
改寫：「讀完這張 CI 圖，重點只有一句：三個 job 平行跑，輸出報告給人讀，第一個月不阻擋。第一個月的目的不是立刻抓人，而是校準噪音、確認分類來源、累積團隊對報告格式的信任；等大家知道哪些訊號真的代表風險，再把最確定的項目升成阻擋。」

11. **五、Diff 上的三個 check：reference implementation**  
原文：「After 是 CI 裡的三個 job，加一個決定適用範圍的 `classify`（節錄；diff 一律以 base branch 為基準，`tools/` 底下的五個 script—`classify` 一個、三個 check 各一個、貼報告的一個—是你要自己寫的部分，行為就是上面三個 check 的定義）：」  
問題／缺口：一句塞進節錄範圍、base branch、tools、自寫 script 與行為定義。缺鋪陳、名詞短語堆疊、破折號當括號連用。  
改寫：「下面這段 After 是 CI 裡的三個 job，再加上一個決定適用範圍的 `classify`。先說清楚它只是節錄：diff 一律以 base branch 為基準；`tools/` 底下的五個 script（`classify` 一個、三個 check 各一個、貼報告的一個）是你要自己寫的部分，行為就是上面三個 check 的定義。」

12. **六、覆蓋率是一條可以被改掉的斷言**  
原文：「三種 game 法都很便宜：exclude pattern 加一行；只呼叫、不斷言；把難測的邏輯搬到被排除的檔案裡。」  
問題／缺口：例子有了，但缺「為什麼這些不是枝微末節」的判讀。缺解讀。  
改寫：「這也是為什麼覆蓋率很容易被 game。三種 game 法都很便宜：exclude pattern 加一行；只呼叫、不斷言；把難測的邏輯搬到被排除的檔案裡。它們不一定是惡意，有時只是趕時間、有時是 legacy code 太難測，但結果一樣，覆蓋率數字變漂亮，測試對行為的約束沒有變強。」

13. **六、覆蓋率是一條可以被改掉的斷言**  
原文：「處方三條：覆蓋率只看 agent 改動的行；與 mutation score 成對讀；exclude pattern 的變更走人審。」  
問題／缺口：清單太快，沒有把三條處方的責任分開。缺連接詞、缺解讀。  
改寫：「所以處方也要維持很窄，先不要把整個 coverage 制度重做一遍。處方三條：覆蓋率只看 agent 改動的行；與 mutation score 成對讀；exclude pattern 的變更走人審。第一條縮小範圍，第二條補上斷言強度，第三條避免最便宜的逃生門被悄悄打開。」

14. **七、第一手實例：測試全綠，replay 從未執行**  
原文：「這個例子對應到 check 的分析要做對，Staff engineer 一眼就會抓：」  
問題／缺口：語氣有作者的銳利感，但轉進 bullet 前少一層「這個例子要拿來看什麼」。缺過場、缺鋪陳。  
改寫：「接著要把這個例子放回三道 check 裡看，而且分析要做對。它不是拿來證明哪個工具沒用，而是用來拆開每一道 check 的邊界；這種邊界，Staff engineer 一眼就會抓：」

15. **八、Tester 的角色：從打勾機器到 test-suite reviewer**  
原文：「審一份 agent 寫的測試，十題：」  
問題／缺口：表格前導讀太薄，少了舊文常見的「把前文收斂成工具」語氣。缺過場、缺解讀。  
改寫：「到這裡，tester 的工作可以收斂成一張很小的 review checklist。它不是要求每個人手動重讀所有測試，而是把前面幾節的 gate 變成十個可以問出口的問題。審一份 agent 寫的測試，十題：」

16. **九、結語**  
原文：「還有一件 testing 的事，Bach 說它不能自動化：對 agent 產出做探索式測試—不是讀它的測試，是去用它做出來的東西。那是另一篇文章的題目，這裡只點到為止。」  
問題／缺口：結語切得太快，沒有把 test gate 與 testing 的邊界收回來。缺收尾承接、缺解讀。  
改寫：「最後把邊界再往外推一點。還有一件 testing 的事，Bach 說它不能自動化：對 agent 產出做探索式測試，不是讀它的測試，是去用它做出來的東西。這篇先停在 test gate，因為我們要先把「測試本身有沒有用」說清楚；但真正的驗收，最後仍然會回到人如何探索、懷疑與判斷。那是另一篇文章的題目，這裡只點到為止。」

**全篇層級**
章節開場與收尾：大方向有承接，但不少小節結尾是「正確的一句話」，不是「帶讀者走到下一節」。第二節到第三節、第三節到第四節、第六節到第七節尤其明顯。

圖表前後導讀：表格與 mermaid 的內容本身夠清楚，但前後常缺「這張圖要怎麼讀」。建議每張圖前加一句讀法，圖後加一句決策含義，不動表格內容與 mermaid 區塊。

術語第一次出現：checking/testing、test gate、red-then-green、assertion-change diff、diff-scoped mutation、equivalent mutant、defect-detection coverage、constraint test、test-suite reviewer 都需要在第一次進正文時有一句白話錨點。

hedge：不要削。「不是業界標準」、「先報告一個月再阻擋」、「N 等於 1，量的是合規」、「能不能限定在 diff 範圍，各家支援程度不同」這些是作者成熟期可信度的一部分。

**不該再加字**
第 13 段「測試比程式碼更需要審」已經夠清楚，不要稀釋那個判斷。

第 104 段 mutation testing 定義很乾淨，不必再鋪。

第 114 段「儀式版與閘門版的差別」雖長，但銳利，最多修標點，不要補成教科書。

第 116 段門檻與 hedge 保留，這是文章可信度來源。

第 311 段「覆蓋率告訴你測試跑過哪裡，mutation 告訴你測試守住哪裡。」是好句，不要展開。

第 317 到 321 段第一手實例的數字與限制很有力，不要加沒有實測的推論。

第 394 段 tester 角色收束已經完整，可以保留。

第 402 段 pull quote 很準，別加解釋削弱力道。

<!-- tokens: in 1345190 out 22704 -->
