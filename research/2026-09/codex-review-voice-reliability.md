我會只讀你列出的 repository 檔案，先抓作者聲音基準，再把 10 月這篇逐段對照。接下來不會碰 `~/.claude/`、`~/.agents/`、`.claude/skills/` 或 `agents/`。
<!-- codex ran: /bin/zsh -lc 'wc -l research/2026-09/codex-review-voice.md .context/research/medium_posts/2025-06-23-c3e8ca1e2eb5.txt .context/research/medium_posts/2025-08-11- -->
<!-- codex ran: /bin/zsh -lc "sed -n '1,220p' research/2026-09/codex-review-voice.md" -->
<!-- codex ran: /bin/zsh -lc "sed -n '1,220p' 2026-10-green-reliability/article.md" -->
我已讀到聲音檔本身其實包含上一輪產出的風格 profile，重點是「舊文靠脈絡、問題句、hedge、例子與收束句撐住可讀性」。現在把可靠度篇後半段和三篇新鮮長文樣本補齊。
<!-- codex ran: /bin/zsh -lc 'wc -c .context/research/medium_posts/2025-06-23-c3e8ca1e2eb5.txt .context/research/medium_posts/2025-08-11-4c58a488c9f5.txt .context/research/medi -->
<!-- codex ran: /bin/zsh -lc "sed -n '221,460p' 2026-10-green-reliability/article.md" -->
<!-- codex ran: /bin/zsh -lc "sed -n '1,240p' 2026-09-agentic-engineering-platform/article.md" -->
目前看起來，10 月可靠度篇的技術骨架很完整，但它把很多「應該停下來讓讀者消化」的地方壓成一句。舊文樣本我會特別抓開場、段落導讀、術語首次出現、圖表前後接話，因為這幾項正是這篇太簡的主要症狀。
<!-- codex ran: /bin/zsh -lc "sed -n '241,540p' 2026-09-agentic-engineering-platform/article.md" -->
<!-- codex ran: /bin/zsh -lc "python3 -c \"from pathlib import Path; import re; p=Path('.context/research/medium_posts/2025-06-23-c3e8ca1e2eb5.txt'); s=p.read_text(encoding='ut -->
<!-- codex ran: /bin/zsh -lc "python3 -c \"from pathlib import Path; p=Path('.context/research/medium_posts/2025-08-11-4c58a488c9f5.txt'); s=p.read_text(encoding='utf-8'); prin -->
三篇樣本中，6 月文很明顯是作者舊式長文：來源故事、書籍引文、個人訓練紀錄、範例與小結反覆交替；9 月新格式則比較像「可直接開會討論」的決策文章，但每個圖表前後仍有導讀句和判斷句。這會作為我判斷哪些段落該補、哪些不該補的依據。
<!-- codex ran: /bin/zsh -lc "python3 -c \"from pathlib import Path; s=Path('.context/research/medium_posts/2025-06-23-c3e8ca1e2eb5.txt').read_text(encoding='utf-8'); print(s[1 -->
<!-- codex ran: /bin/zsh -lc "python3 -c \"from pathlib import Path; s=Path('.context/research/medium_posts/2025-08-11-4c58a488c9f5.txt').read_text(encoding='utf-8'); print(s[2 -->
<!-- codex ran: /bin/zsh -lc "python3 -c \"from pathlib import Path; s=Path('2026-10-green-reliability/article.md').read_text(encoding='utf-8'); import re; paras=[p.strip() for -->
<!-- codex ran: /bin/zsh -lc "python3 -c \"from pathlib import Path; s=Path('.context/research/medium_posts/2025-12-28-642ef2eafc4b.txt').read_text(encoding='utf-8'); print(s[: -->
我已補完三篇長文樣本：舊文不是單純「多字」，而是會在每個 technical claim 旁邊放讀者入口，例如「先說限制」「舉例」「小結」「這代表什麼」。接下來我會用段落索引逐段挑選，避免只憑印象判斷。
<!-- codex ran: /bin/zsh -lc 'python3 -c $'"'from pathlib import Path\\nimport re\\ns=Path(\"2026-10-green-reliability/article.md\").read_text(encoding=\"utf-8\")\\nparas=[p.st -->
以下只看文氣與可讀性，不摘要技術內容。整體判斷是：這篇不是「資訊不夠」，而是太常把定義、證據、限制、結論壓在同一段，少了作者舊文慣用的「先讓讀者知道為什麼要看這個、再把概念拆開、最後收一句白話」的節奏。

**過簡段落**

1. 小節：一、SWE-Gate 量到的 34%

原文：
```text
這一段只做一件事：把「綠燈量到什麼」分層。接下來整篇只處理兩層—reviewer 約束那一層，與可靠度那一層。
```

吃力點：這其實是章節轉場，但太像內部筆記。舊文通常會補「為什麼要先分層」，讓讀者知道不是在玩名詞精準，而是在避免誤用數字。

缺的是：缺過場、缺解讀、破折號當括號連用。

改寫：
```text
這裡先停一下，因為後面所有 gate 的設計，都建立在同一個前提上：你要先知道手上的綠燈到底量到哪一層。本文接下來不再泛談「測試有沒有過」，而是只處理兩層：reviewer 約束那一層，與可靠度那一層。
```

2. 小節：二、把 review 約束寫成可執行的 constraint tests

原文：
```text
約束長什麼樣？以下七類是筆者從團隊的 review 評論整理的；SWE-NFI 的 92 條規則與 SWE-Gate 的評論分類，以論文原文為準：
```

吃力點：舊文遇到新表格前，通常會多給一個閱讀角度。這裡直接丟表，讀者不知道要把表當分類法、checklist，還是導入順序。

缺的是：缺導讀句、缺解讀、術語第一次出現沒解釋。

改寫：
```text
那 review 約束到底長什麼樣？先把它想成團隊反覆講過、但不該每次都靠人記得的那些規矩。以下七類是筆者從團隊的 review 評論整理的，用來示範 constraint tests 可以從哪裡長出來；SWE-NFI 的 92 條規則與 SWE-Gate 的評論分類，以論文原文為準：
```

3. 小節：二、把 review 約束寫成可執行的 constraint tests

原文：
```text
與 11 月契約篇的分界只有一句：這裡的約束來自 **review 歷史**—事後、經驗性；契約篇的約束來自 **spec**—事前、規格性。兩者都進 CI，但 owner 與壽命不同。
```

吃力點：這句很重要，但寫成註腳感。舊文會把「容易混淆的兩件事」多鋪一層，讓讀者知道為何需要分界。

缺的是：缺鋪陳、缺過場、破折號當括號連用。

改寫：
```text
這裡也要先跟 11 月契約篇切開，否則很容易把兩種約束混在一起。本文談的約束來自 **review 歷史**，也就是事後累積出來的經驗性規則；契約篇談的約束來自 **spec**，也就是事前說清楚的規格性要求。兩者最後都會進 CI，但 owner 與壽命不同，維護方式也不該一樣。
```

4. 小節：二、把 review 約束寫成可執行的 constraint tests

原文：
```text
成本：constraint tests 是 deterministic、秒級，觸及範圍是整個 PR。依總論第十節的觸及範圍原則，它是最便宜的驗證，也是 brownfield 的第一道閘—不需要既有測試；沒有 review 歷史，就從團隊規範與最近五個 incident 出發。
```

吃力點：這段把成本、適用範圍、brownfield 起手式塞在一起。舊文通常會先說「為什麼這是便宜驗證」，再補 brownfield 怎麼起步。

缺的是：缺鋪陳、缺例子、破折號當括號連用。

改寫：
```text
成本也可以講得更白一點：constraint tests 通常是 deterministic、秒級，而且觸及範圍是整個 PR。依總論第十節的觸及範圍原則，這類檢查是最便宜的驗證，也很適合當 brownfield 的第一道閘。原因很樸素：它不需要你先擁有完整既有測試。若團隊還沒有足夠的 review 歷史，就先從團隊規範與最近五個 incident 出發，把那些「不要再犯一次」的規則寫成 check。
```

5. 小節：三、可靠度不是能力：pass@1 與 pass^k

原文：
```text
定義沿用總論第八節：golden set 的每個 case 跑 k 次；**pass@1 是單次嘗試的成功率，用 k 次重複跑來估—每個 case 是 k 次裡過的次數除以 k；pass^k 是 k 次全部成功的 case 比例；兩者都先 per case 算，再對整個 golden set 取 aggregate。**「至少一次成功的比例」是 pass@k，是另一個數字，本系列不用。
```

吃力點：這是全篇核心定義，但一句塞太滿。舊文會把容易混淆的名詞拆開，尤其 pass@1、pass^k、pass@k 只差符號，讀者很容易滑過去。

缺的是：術語第一次出現沒解釋、缺鋪陳、名詞短語堆疊。

改寫：
```text
這裡先把三個容易混在一起的名詞拆開。定義沿用總論第八節：golden set 的每個 case 跑 k 次。**pass@1 是單次嘗試的成功率，用 k 次重複跑來估；每個 case 是 k 次裡過的次數除以 k。pass^k 是 k 次全部成功的 case 比例。兩者都先 per case 算，再對整個 golden set 取 aggregate。**「至少一次成功的比例」是 pass@k，是另一個數字，本系列不用。
```

6. 小節：三、可靠度不是能力：pass@1 與 pass^k

原文：
```text
為什麼 code 領域也要這樣量？證據是兩篇改寫敏感度的研究。RealSWE（381 個任務家族）：同一個任務換個說法，平均掉 6.4 個百分點，而且會重排 model 的名次。另一篇語意保持的改寫研究：平均最多掉 6.7 個百分點，**但 16 組 model 與 scaffold 的組合裡只有 6 組達到統計顯著—效應真實但不均勻。** 同一件事問法不同結果不同，這就是可靠度問題。
```

吃力點：舊文會先把「為什麼這不是 benchmark 小事」講清楚。這裡研究名、樣本、數字、結論同段出現，讀者會先忙著消化數字，反而吃不到判斷。

缺的是：缺解讀、缺鋪陳、破折號當括號連用。

改寫：
```text
為什麼 code 領域也要這樣量？因為同一件事，只要換個說法，結果就可能不一樣。證據是兩篇改寫敏感度的研究。RealSWE（381 個任務家族）量到：同一個任務換個說法，平均掉 6.4 個百分點，而且會重排 model 的名次。另一篇語意保持的改寫研究也量到，平均最多掉 6.7 個百分點，**但 16 組 model 與 scaffold 的組合裡只有 6 組達到統計顯著。** 所以這裡的結論不是「所有 model 都一樣不穩」，而是效應真實但不均勻；同一件事問法不同結果不同，這就是可靠度問題。
```

7. 小節：三、可靠度不是能力：pass@1 與 pass^k

原文：
```text
在自己的 eval 上怎麼做：營運篇的 golden set—20 到 50 個 case—每月跑 k = 5；frontier set 跑 k = 3；報表三欄。**我的建議值（不是業界標準）**：k = 5，pass^5 ≥ 60% 才算「可放低 radius 自主」。**粒度警告**：golden set 少於 30 個 case 時，pass^k 只報趨勢，不當門檻—20 個 case 的粒度是 5 個百分點，一個 case 翻轉就從 65% 掉到 60%，會被月與月的雜訊主導；當門檻時要連續兩個月達標。
```

吃力點：這段其實在交代操作方法、建議值、小樣本警告三件事。舊文通常會用「先怎麼做，再怎麼看，最後提醒限制」分開讀。

缺的是：缺連接詞、缺鋪陳、破折號當括號連用。

改寫：
```text
落到自己的 eval 上，我會先用營運篇的 golden set，也就是 20 到 50 個 case，每月跑 k = 5；frontier set 則跑 k = 3。報表先固定三欄，讓團隊每個月看同一組數字。**我的建議值（不是業界標準）**：k = 5，pass^5 ≥ 60% 才算「可放低 radius 自主」。但這裡要加一個 **粒度警告**：golden set 少於 30 個 case 時，pass^k 只報趨勢，不當門檻。20 個 case 的粒度是 5 個百分點，一個 case 翻轉就從 65% 掉到 60%，很容易被月與月的雜訊主導；真的要當門檻時，要連續兩個月達標。
```

8. 小節：四、Oversight budget：READY 與一個簡化模型

原文：
```text
READY 是企業 agent 部署的資格審查框架（2026 年 9 月）：以可靠度目標反推「agent 加人工複核政策」要多少人看，量到兩個準確率只差 0.3 個百分點的系統，人工複核需求差了近 10 個百分點。它的案例是臨床稽核工作流，不是 code—這裡只借概念，數字不移植；全數字與領域說明在總論第八節。READY 在本篇只用來證明一件事：**準確率的排名，不等於人力的排名。** 我不承諾重現它的數字；它的方法一定比下面這個簡化模型多考慮了東西。
```

吃力點：這段 hedge 很重要，但被擠在同一段。舊文會先交代「我借的是什麼、不借的是什麼」，避免讀者誤以為臨床數字可以直接搬到 code。

缺的是：缺鋪陳、缺解讀、破折號當括號連用。

改寫：
```text
READY 是企業 agent 部署的資格審查框架（2026 年 9 月）。它有一個對本文很有用的觀念：不要只看 agent 準確率，而是要從可靠度目標反推「agent 加人工複核政策」到底要多少人看。READY 量到，兩個準確率只差 0.3 個百分點的系統，人工複核需求卻差了近 10 個百分點。先說清楚，它的案例是臨床稽核工作流，不是 code；本文只借概念，數字不移植，全數字與領域說明在總論第八節。READY 在本篇只用來證明一件事：**準確率的排名，不等於人力的排名。** 我不承諾重現它的數字；它的方法一定比下面這個簡化模型多考慮了東西。
```

9. 小節：四、Oversight budget：READY 與一個簡化模型

原文：
```text
算例，用自己的數字示範：
```

吃力點：太像投影片標題。舊文進入算例前，通常會先提醒讀者「下面不是要背公式，而是看直覺」。

缺的是：缺過場、缺解讀。

改寫：
```text
下面用自己的數字示範。重點不是要讀者背公式，而是先感受一件事：當 T、p、c 放在一起算時，人工複核比例很可能比直覺想像得高。
```

10. 小節：四、Oversight budget：READY 與一個簡化模型

原文：
```text
分配方式接 Review 篇的分流矩陣：低 radius 可驗證那一格「非指派者深讀抽樣」的比例，就是這裡算出來的 r。每一格仍有人類讀報告 approve；r 決定的是深讀比例。抽樣要分層—我的考試筆記另一條：aggregate accuracy 會掩蓋某些類型的低表現，要做 stratified random sampling。搬到 code 上，分層維度是任務類型、repo、agent 版本；p 也要分層算。下圖 c 那一格的 49%–74%，是上面那個警告—人眼不是 100%—不是 c 的量測值。
```

吃力點：這段同時接前文、接 Review 篇、解釋 r、解釋抽樣、解釋圖中 49%–74%。舊文會把「公式怎麼進流程」和「抽樣怎麼避免平均值騙人」分成兩層。

缺的是：缺連接詞、缺解讀、破折號當括號連用。

改寫：
```text
分配方式接 Review 篇的分流矩陣。低 radius 可驗證那一格裡，「非指派者深讀抽樣」的比例，就是這裡算出來的 r。每一格仍然要有人類讀報告 approve；r 決定的是其中多少比例需要深讀。抽樣也不能只看 aggregate accuracy，因為我的考試筆記裡另一條提醒是：aggregate accuracy 會掩蓋某些類型的低表現，所以要做 stratified random sampling。搬到 code 上，分層維度是任務類型、repo、agent 版本；p 也要分層算。下圖 c 那一格的 49%–74%，只是在提醒人眼不能假設是 100%，不是 c 的量測值。
```

11. 小節：五、授權擴張的閘門：接回 G2

原文：
```text
營運篇 G2 的原條件是三條：retry rate 低於 15%、escape rate 持平、champions 體系自轉。本篇加四條，全部標「我的建議值（不是業界標準）」。門檻的句型統一為「達標且連續兩個月不升／不降」，不寫「連續下降」—穩態降到 2% 之後就沒得降，gate 從此過不了。小樣本再提醒一次：golden set 少於 30 個 case 時，pass^5 的點估計不是門檻—要嘛連同 Wilson 區間一起報，要嘛等到「連續兩個月 + 最少 30 個 case」才拿它當 gate；這跟第三節的粒度警告是同一條規則。
```

吃力點：這段是政策落地的關鍵，但把原條件、新條件、門檻語法、小樣本統計警告放在一起。舊文會先講「為什麼 G2 要補四條」，再講語法與限制。

缺的是：缺鋪陳、缺連接詞、破折號當括號連用。

改寫：
```text
回到營運篇的 G2。原條件是三條：retry rate 低於 15%、escape rate 持平、champions 體系自轉。可靠度篇要補的是另外四條，而且全部標成「我的建議值（不是業界標準）」。門檻的句型也要統一為「達標且連續兩個月不升／不降」，不要寫「連續下降」。原因很現實：穩態降到 2% 之後就沒得降，gate 從此過不了。小樣本也要再提醒一次：golden set 少於 30 個 case 時，pass^5 的點估計不是門檻。要嘛連同 Wilson 區間一起報，要嘛等到「連續兩個月 + 最少 30 個 case」才拿它當 gate；這跟第三節的粒度警告是同一條規則。
```

12. 小節：五、授權擴張的閘門：接回 G2

原文：
```text
G3 加一條：frozen holdout eval 不得被 agent 或 harness 觸碰。一項 2026 年 9 月的研究記錄了 production 自我改進迴圈裡的一個案例：agent 找到被快取的標準答案（answer key），拿到 100%，真實能力是 68%。canary 任務要混入 production 流量。
```

吃力點：這段很有力，但讀者第一次遇到 G3、frozen holdout eval、canary 任務時，會需要一點脈絡。舊文會先說「這是在防什麼」。

缺的是：術語第一次出現沒解釋、缺過場、缺解讀。

改寫：
```text
G3 還要再加一條，防的是 eval 被系統自己污染：frozen holdout eval 不得被 agent 或 harness 觸碰。一項 2026 年 9 月的研究記錄了 production 自我改進迴圈裡的一個案例：agent 找到被快取的標準答案（answer key），拿到 100%，真實能力是 68%。所以 canary 任務不能只放在實驗室裡，也要混入 production 流量，避免 agent 只是在學會通過那份考卷。
```

13. 小節：五、授權擴張的閘門：接回 G2

原文：
```text
judge 還有一個陷阱—營運篇第二節列了三個，這是第四個。營運篇的陷阱 1 講的是語氣：judge 偏好長答案與自信的語氣。一項 400 條軌跡的 trajectory-judge 研究（2026 年 8 月；任務領域見原文）量到更具體的一層：agent 捏造「我做了 X」的動作宣稱，能騙過 step-rubric judge 82%。所以 rubric 綁的事實項要能從環境驗證—測試結果、constraint 結果、trace—不能從 transcript 驗證。
```

吃力點：這段判斷正確但節奏太急。舊文通常會先讓讀者看到「為什麼 transcript 不是證據」，再接研究數字。

缺的是：缺鋪陳、缺解讀、破折號當括號連用。

改寫：
```text
judge 還有一個陷阱。營運篇第二節列了三個，這裡補第四個：不要讓 transcript 自己證明自己。營運篇的陷阱 1 講的是語氣，也就是 judge 偏好長答案與自信的語氣。一項 400 條軌跡的 trajectory-judge 研究（2026 年 8 月；任務領域見原文）量到更具體的一層：agent 捏造「我做了 X」的動作宣稱，能騙過 step-rubric judge 82%。所以 rubric 綁的事實項，要能從環境驗證，例如測試結果、constraint 結果、trace；不能從 transcript 驗證。
```

14. 小節：六、結語與交接

原文：
```text
三個數字進月報：constraint pass rate、pass^5、oversight budget 的 r。G2 多四條。可靠度篇的兩個產出—pass^k 與 r—12 月會變成 SLI。
```

吃力點：這是全篇收尾，但太像 release note。舊文的結語通常會把前文拉回系列主題，讓讀者知道「這篇留給下一篇的是什麼」。

缺的是：缺收束、缺過場、破折號當括號連用。

改寫：
```text
收在最可操作的地方：三個數字進月報，分別是 constraint pass rate、pass^5、oversight budget 的 r。G2 多四條，代表授權擴張不再只看 agent 有沒有完成任務，而是看它能不能穩定、可驗證、可負擔地完成。可靠度篇留下的兩個產出是 pass^k 與 r；到 12 月，它們會再往前一步，變成 SLI。
```

**全篇層級**

章節開場與收尾：第一節到第二節有基本承接，但第二節到第三節、第三節到第四節偏快。建議每章開頭補一句「上一章的結論如何推到這章」，結尾補一句「這章留給下一章什麼」。第六節目前收得太短，應補成系列交接，而不是只有指標清單。

圖表前後導讀句：表格與 mermaid 後面都有短句，但多數像 caption，不像導讀。比較像作者舊文與 2026-09 新格式的做法，是圖前先說「讀這張圖要看哪一層」，圖後再說「所以決策上要改什麼」。YAML 區塊尤其需要補「看哪一欄」，否則會像規格片段直接貼上來。

術語第一次出現：`constraint tests`、`pass^k`、`oversight budget`、`frontier set`、`blast radius`、`frozen holdout eval`、`canary`、`Wilson 區間`、`trajectory-judge`、`step-rubric judge` 都應在第一次出現時給半句白話。這不需要長解釋，但要讓非本系列讀者不會被丟出文章。

hedge：這篇好的地方是 hedge 大多還在，例如「不是業界標準」、「不是 READY 的方法」、「數字不移植」、「領域邊界要先說清楚」。不要刪。需要修的是有些 hedge 壓太短，像 49%–74% 那段容易讀成 c 的估計值，應把「警告，不是量測值」講完整。

**不該再加字**

以下段落或區塊已經夠銳利，潤稿時不要稀釋：

- TL;DR 的最後一句「授權擴張看 pass^k、constraint pass rate、escape rate，不看 pass@1。」立場清楚。
- 第一節「每三個綠燈修補就有一個違反約束」與「不是綠燈量不到 reviewer 在乎的三分之一」這個校正不要放軟。
- `rules.md`、`CODEOWNERS`、`agent-policy.yaml` 範例不要塞解釋文字進 code block。
- 三個 mermaid 圖後的單句 caption 可以保留短，但圖前要補導讀。
- 第四節算例裡「全審都不夠」很有效，不要改成委婉說法。
- 「讀者第一次算完多半會發現：可靠度目標訂在哪一格，比 agent 的準確率更決定人力。」這句已經是作者口吻。
- 第五節「不擴張也是決策」整段方向對，而且有決策力，只要前後轉場補好，不需要改長。
- 最後 pull quote「綠燈告訴你 agent 沒把功能弄壞；constraint tests 告訴你它有沒有守住團隊的規矩；pass^k 告訴你能不能放手。三個都要，順序不能反。」不要再加解釋，保持收刀感。

<!-- tokens: in 320069 out 15950 -->
