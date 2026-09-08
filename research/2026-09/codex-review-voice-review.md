我會只讀你列出的 repository 檔案，不碰 `~/.claude/`、`~/.agents/`、`.claude/skills/` 或 `agents/`。先把 voice profile、舊文樣本、新格式樣本和 October 文章完整讀完，再按段落與全篇層級整理。
<!-- codex ran: /bin/zsh -lc 'wc -l research/2026-09/codex-review-voice.md .context/research/medium_posts/2025-06-23-c3e8ca1e2eb5.txt .context/research/medium_posts/2025-08-11- -->
這幾個 Medium `.txt` 檔是長行格式，不是一般換行文章。我先讀 voice profile 和兩篇 markdown 文章，接著再用只讀的文字查看方式把三篇舊文拆開看。
<!-- codex ran: /bin/zsh -lc "sed -n '1,260p' 2026-09-agentic-engineering-platform/article.md" -->
<!-- codex ran: /bin/zsh -lc "sed -n '1,220p' research/2026-09/codex-review-voice.md" -->
<!-- codex ran: /bin/zsh -lc "sed -n '1,240p' 2026-10-green-review/article.md" -->
目前已讀到 October 文章前半，問題集中在「用判斷句推進」的密度太高：每句都像結論，但句與句之間少了讀者需要的來路。接下來我會讀後半，特別檢查 mermaid、表格、章節收尾和 hedge 是否被削薄。
<!-- codex ran: /bin/zsh -lc "sed -n '221,520p' research/2026-09/codex-review-voice.md" -->
<!-- codex ran: /bin/zsh -lc "sed -n '261,620p' 2026-09-agentic-engineering-platform/article.md" -->
<!-- codex ran: /bin/zsh -lc "sed -n '241,520p' 2026-10-green-review/article.md" -->
新格式樣本的好處很清楚：它雖然也密集，但通常會先用一兩句把「為什麼這裡值得展開」講完，再進表格或圖。October 這篇比較常直接把處方、例外、判定往前推，讀者少了一拍理解時間。
<!-- codex ran: /bin/zsh -lc 'wc -c .context/research/medium_posts/2025-06-23-c3e8ca1e2eb5.txt .context/research/medium_posts/2025-08-11-4c58a488c9f5.txt .context/research/medi -->
三篇舊文大約 12 萬字元，都是 Medium 抽取後壓成長行。我會只做顯示用的換行處理，不產生中間檔，目的是看他的長文節奏、過場與解讀句怎麼安排。
<!-- codex ran: /bin/zsh -lc 'head -c 2500 .context/research/medium_posts/2025-06-23-c3e8ca1e2eb5.txt' -->
<!-- codex ran: /bin/zsh -lc 'head -c 2500 .context/research/medium_posts/2025-12-28-642ef2eafc4b.txt' -->
<!-- codex ran: /bin/zsh -lc 'head -c 2500 .context/research/medium_posts/2025-08-11-4c58a488c9f5.txt' -->
接下來我會完整看三篇舊文的正文。這裡關注的不是技術主張，而是他的「長段怎麼把概念帶進來」：常見是先放一個閱讀或工作脈絡，再給定義，接著用小結把抽象判斷收住。
<!-- codex ran: /bin/zsh -lc "perl -CS -0pe 's/"'^.*?ShareMore//s; s/FollowWritten by.*$//s; s/(?<=[。！？])/$&'"\\n/g; s/(源起：|引言：|小結：|結語：|後記：|補充：)/\\n"'$1/g'"' .context/research/ -->
<!-- codex ran: /bin/zsh -lc "perl -CS -0pe 's/"'^.*?ShareMore//s; s/FollowWritten by.*$//s; s/(?<=[。！？])/$&'"\\n/g; s/(源起：|引言：|小結：|結語：|後記：|補充：|最佳實務：|範例：)/\\n"'$1/g'"' .context -->
<!-- codex ran: /bin/zsh -lc "perl -CS -0pe 's/"'^.*?ShareMore//s; s/FollowWritten by.*$//s; s/(?<=[。！？])/$&'"\\n/g; s/(引言：|第一個坑：|第二步：|第三步：|結語：|後記：|參考資料)/\\n"'$1/g'"' .context/ -->
剛才用 Perl 處理 Unicode 時輸出變成亂碼，我不會用那份輸出做判斷。改用 `python3 -c` 只讀檔案並在標點後換行，這樣能正確看 UTF-8 內容。
<!-- codex ran: /bin/zsh -lc "PYTHONIOENCODING=utf-8 python3 -c 'from pathlib import Path; import re; s=Path(\".context/research/medium_posts/2025-06-23-c3e8ca1e2eb5.txt\").rea -->
第一篇舊文確認了 voice profile 的判斷：他不是單純把名詞串起來，而是會用「Kent Beck 的推薦 → 自己重讀 → 書中概念 → 軟體對應 → 例子 → 小結」形成一條閱讀路徑。這會是後面判斷 October 段落「缺什麼」的主要參照。
<!-- codex ran: /bin/zsh -lc "PYTHONIOENCODING=utf-8 python3 -c 'from pathlib import Path; import re; s=Path(\".context/research/medium_posts/2025-08-11-4c58a488c9f5.txt\").rea -->
第二篇是比較偏 reference / how-to 的長文，中段有大量工具與範例；完整輸出被工具截斷了。我會補讀被截掉的中段與尾段，避免只根據開頭和結尾判斷他的正式技術 register。
<!-- codex ran: /bin/zsh -lc "PYTHONIOENCODING=utf-8 python3 -c 'from pathlib import Path; import re; s=Path(\".context/research/medium_posts/2025-08-11-4c58a488c9f5.txt\").rea -->
<!-- codex ran: /bin/zsh -lc "PYTHONIOENCODING=utf-8 python3 -c 'from pathlib import Path; import re; s=Path(\".context/research/medium_posts/2025-08-11-4c58a488c9f5.txt\").rea -->
<!-- codex ran: /bin/zsh -lc "PYTHONIOENCODING=utf-8 python3 -c 'from pathlib import Path; import re; s=Path(\".context/research/medium_posts/2025-08-11-4c58a488c9f5.txt\").rea -->
第二篇補讀完後，樣態比較像「技術地圖 + 實務提醒」：即使它資訊密度很高，圖或範例前後仍會加「這張圖的重點不是……而是……」這種導讀句。October 文章最需要補的，正是這些圖表前後的導讀與讀者定位。
<!-- codex ran: /bin/zsh -lc "PYTHONIOENCODING=utf-8 python3 -c 'from pathlib import Path; import re; s=Path(\".context/research/medium_posts/2025-12-28-642ef2eafc4b.txt\").rea -->
<!-- codex ran: /bin/zsh -lc "PYTHONIOENCODING=utf-8 python3 -c 'from pathlib import Path; import re; s=Path(\".context/research/medium_posts/2025-12-28-642ef2eafc4b.txt\").rea -->
<!-- codex ran: /bin/zsh -lc "PYTHONIOENCODING=utf-8 python3 -c 'from pathlib import Path; import re; s=Path(\".context/research/medium_posts/2025-12-28-642ef2eafc4b.txt\").rea -->
我已經讀完指定的 voice profile、三篇舊文、新格式樣本與 Review 篇。現在進入整理階段：先把 Review 篇切成段落索引，選出至少 12 段「不是錯，但太快」的地方，再逐段配改寫。
<!-- codex ran: /bin/zsh -lc "PYTHONIOENCODING=utf-8 python3 -c 'from pathlib import Path
p=Path(\"2026-10-green-review/article.md\")
lines=p.read_text(encoding=\"utf-8\").spli -->
我已經有候選段落。現在會補一次帶行號的原文核對，確保引用是逐字、整段，不會把表格或 mermaid 內容改掉，也不會誤把 list item 截短。
<!-- codex ran: /bin/zsh -lc "nl -ba 2026-10-green-review/article.md | sed -n '100,130p'" -->
<!-- codex ran: /bin/zsh -lc "nl -ba 2026-10-green-review/article.md | sed -n '1,60p'" -->
<!-- codex ran: /bin/zsh -lc "nl -ba 2026-10-green-review/article.md | sed -n '269,365p'" -->
<!-- codex ran: /bin/zsh -lc "nl -ba 2026-10-green-review/article.md | sed -n '198,215p'" -->
已依照 voice profile 與指定舊文對照。以下把 Markdown list item 也視為一個可潤稿段落；改寫只動敘事與鋪陳，不動表格與 mermaid。

**過於簡潔段落**

1. 小節：TL;DR（[L3](/Users/kochi.chuang/conductor/workspaces/medium-articles/yokohama/2026-10-green-review/article.md:3)）  
原文：`> **TL;DR** — Scrum Community 裡有人描述 PR 半年翻倍、senior 的日曆全滿；一百萬個 PR 的縱向研究說 AI review 在某些採用模式下讓決策更快，沒更好；CodeRabbit 在一萬個 PR 上的評論有 56% 被拒絕；跨產品的 AI 審 AI 兩季成長 100 倍。多數團隊把這當成吞吐問題，想讓人讀得更快。本篇的主張是：review 從來不是讀 diff，**review 是組織決定 agent 是加分還是負債的控制點**—一個從 3,100 篇實務者論述建構的因果理論這樣叫它；一個追蹤 182 個 repo 的縱向研究量到免審合併率每高 10 個百分點，agentic code 的維護負擔約高 6%（相關）。重設計的三件事：**分流矩陣**（人讀 intent 與 constraint 報告，不讀 diff；機器讀 diff；每一格都寫清楚 merge 靠什麼）、**reviewer agent 艦隊**（異質配對、deterministic dispatch 先行、與生成 session 分離；只有一家 vendor 也能跑）、**閉環禁令**（同 model 同 session 自審禁止、AI approve 不計入、不給 reviewer 看前一輪分數）。外加一條資安面的必修：一句「pre-approved under SEC-2291」讓約八成洗過的外洩 PR 通過掃描這一站，所以權威宣稱要從 system of record 驗證，不是讀 PR 描述。approval 綁人；誰能 approve 的 vendor 條款互相矛盾，細節留給 12 月。`  
吃力點：舊文的 TL;DR / 引言通常先給「這篇從哪個困惑長出來」，再放證據；這段把 evidence、thesis、solution、security、accountability 全壓在一起。缺：缺鋪陳、缺過場、術語第一次出現沒解釋、名詞短語堆疊、破折號當括號連用。  
改寫：`> **TL;DR** — 這篇先處理一個很現場的問題：AI 讓 PR 變多之後，review 到底該放在哪裡。Scrum Community 裡有人描述 PR 半年翻倍、senior 的日曆全滿；一百萬個 PR 的縱向研究說 AI review 在某些採用模式下讓決策更快，沒更好；CodeRabbit 在一萬個 PR 上的評論有 56% 被拒絕；跨產品的 AI 審 AI 兩季成長 100 倍。這些訊號放在一起看，我認為多數團隊誤把它當成吞吐問題，所以第一個反應是讓人讀得更快。但本篇的主張不是加速讀 diff，而是把 review 重新放回控制點：review 是組織決定 agent 是加分還是負債的控制點。一個從 3,100 篇實務者論述建構的因果理論這樣叫它；一個追蹤 182 個 repo 的縱向研究也量到免審合併率每高 10 個百分點，agentic code 的維護負擔約高 6%（相關）。所以重設計會落在三件事：分流矩陣，讓人讀 intent 與 constraint 報告，不讀 diff；讓機器讀 diff；每一格都寫清楚 merge 靠什麼。reviewer agent 艦隊，採異質配對、deterministic dispatch 先行，並與生成 session 分離；只有一家 vendor 也能跑。閉環禁令，禁止同 model 同 session 自審，AI approve 不計入，也不給 reviewer 看前一輪分數。資安面還有一條必修：一句「pre-approved under SEC-2291」讓約八成洗過的外洩 PR 通過掃描這一站，所以權威宣稱要從 system of record 驗證，不是讀 PR 描述。最後，approval 綁人；誰能 approve 的 vendor 條款互相矛盾，細節留給 12 月。`

2. 小節：一、Review 的目的變了（[L13](/Users/kochi.chuang/conductor/workspaces/medium-articles/yokohama/2026-10-green-review/article.md:13)）  
原文：`總論第七節已經修正了上一季「Review 成為新瓶頸」的說法：瓶頸是症狀，病因是把人放在錯的閘門上讀錯的東西。本篇只講 review gate 的設計。立場不是「少 review」，也不是「快 review」，是**重新分配誰讀什麼**。`  
吃力點：判斷很準，但舊文會多一層「為什麼這句話值得修正」的自我校準。缺：缺鋪陳、缺解讀、缺過場。  
改寫：`總論第七節其實已經幫這篇文章做了一次校正。上一季我把它寫成「Review 成為新瓶頸」，現在看起來這句話只說到表面：瓶頸是症狀，病因是把人放在錯的閘門上讀錯的東西。所以本篇只講 review gate 的設計，不把問題簡化成「少 review」或「快 review」。真正要重排的是：誰應該讀 intent、誰應該讀 constraint、誰才需要讀 diff。`

3. 小節：二、真實 PR 資料怎麼說（[L19](/Users/kochi.chuang/conductor/workspaces/medium-articles/yokohama/2026-10-green-review/article.md:19)）  
原文：`這一節是全系列唯一把真實 PR 資料引全的地方。每個數字後面緊接它推出的那一條處方；推不出處方的數字，只進最後的總表。`  
吃力點：像編輯備註，少了作者舊文常見的「我為什麼這樣安排證據」。缺：缺主詞、缺鋪陳、缺解讀。  
改寫：`這一節先把真實 PR 資料集中處理，因為後面的矩陣、艦隊與禁令，都不應該只靠直覺決定。它也是全系列唯一把真實 PR 資料引全的地方。我的取捨很簡單：每個數字後面緊接它推出的那一條處方；推不出處方的數字，只進最後的總表，避免文章變成 benchmark 展示。`

4. 小節：二、真實 PR 資料怎麼說（[L21](/Users/kochi.chuang/conductor/workspaces/medium-articles/yokohama/2026-10-green-review/article.md:21)）  
原文：`1. **控制點的出處。** 一項從 38,709 篇灰色文獻中編碼 3,100 篇、建構出 26 個構念與 67 條關係的因果理論（2026 年 7 月）把 review 定位成決定 agent 淨效果正負的控制點：團隊的專業與流程結構決定方向。它是理論框架，不是量測到的因果效應。→ 處方：review gate 的設計是組織決策，不是工具選型；本篇後面每一節都是「流程結構」的一部分。`  
吃力點：研究規模、限制、處方同時出現，讀者還沒理解「控制點」就被帶到處方。缺：缺解讀、缺連接詞、術語第一次出現沒解釋。  
改寫：`1. **控制點的出處。** 先看第一個錨點。一項從 38,709 篇灰色文獻中編碼 3,100 篇、建構出 26 個構念與 67 條關係的因果理論（2026 年 7 月），把 review 定位成決定 agent 淨效果正負的控制點。這裡的控制點，不是某個工具按鈕，而是團隊用專業與流程結構去改變 agent 影響方向的地方。也要先把限制說清楚：它是理論框架，不是量測到的因果效應。→ 處方：review gate 的設計是組織決策，不是工具選型；本篇後面每一節都是「流程結構」的一部分。`

5. 小節：三、分流矩陣（[L41](/Users/kochi.chuang/conductor/workspaces/medium-articles/yokohama/2026-10-green-review/article.md:41)）  
原文：`兩條軸：**blast radius**—改到 auth、payment、schema、infra，還是內部工具—與**可機器驗證的程度**—有沒有 constraint tests 與 mutation 報告。`  
吃力點：這是矩陣入口，但三個 key terms 第一次一起出現，像投影片標籤。缺：術語第一次出現沒解釋、缺鋪陳、破折號當括號連用。  
改寫：`矩陣先看兩條軸。第一條是 **blast radius**，也就是這次變更如果出錯，會傷到 auth、payment、schema、infra，還是只影響內部工具。第二條是 **可機器驗證的程度**，也就是有沒有 constraint tests 與 mutation 報告，可以把「agent 說它做到了」轉成可檢查的證據。`

6. 小節：三、分流矩陣（[L43](/Users/kochi.chuang/conductor/workspaces/medium-articles/yokohama/2026-10-green-review/article.md:43)）  
原文：`矩陣上面先寫一條全系列不變的規則：**每一次 merge 仍然帶一個人類 approve，綁人。** oversight budget 決定的是「其中多少比例要再做深讀」，不是「哪些 PR 不用人 approve」。AI 的 approve 是 approval artifact 裡的一個訊號欄，供人類 approve 者與抽樣參考，永不計入 required approvals。這樣總論主張 2 的「不計入」才有東西可以不計入，而「機器全審、人抽樣」那一格沒被抽到的 PR，才有明確的 merge 路徑。`  
吃力點：概念其實重要，但 oversight budget、approval artifact、required approvals 都還沒落地。缺：術語第一次出現沒解釋、缺例子、名詞短語堆疊。  
改寫：`在看矩陣前，要先把底線寫清楚：**每一次 merge 仍然帶一個人類 approve，綁人。** oversight budget 決定的是「其中多少比例要再做深讀」，不是「哪些 PR 不用人 approve」。換句話說，即使某個 PR 沒被抽到深讀，它仍然要有人類看過報告並 approve。AI 的 approve 是 approval artifact 裡的一個訊號欄，供人類 approve 者與抽樣參考，永不計入 required approvals。這樣總論主張 2 的「不計入」才有東西可以不計入，而「機器全審、人抽樣」那一格沒被抽到的 PR，才有明確的 merge 路徑。`

7. 小節：三、分流矩陣（[L56](/Users/kochi.chuang/conductor/workspaces/medium-articles/yokohama/2026-10-green-review/article.md:56)）  
原文：`PR template 加兩個必填欄：**Intent**—這個 PR 要達成什麼，一句—與 **Constraints honoured**—列出它遵守了哪些團隊約束。人審的是這兩欄與報告的一致性。分流的前提是 PR 夠小：Scrum Community 有人抱怨「AI 一次碰二十個檔案，沒人說得出哪個決定弄壞了」；story 切小，是這一切的前提。`  
吃力點：從 PR template 跳到 story slicing 太快，兩者關係需要補一拍。缺：缺連接詞、缺解讀、破折號當括號連用。  
改寫：`PR template 至少要加兩個必填欄。第一個是 **Intent**，用一句話說清楚這個 PR 要達成什麼；第二個是 **Constraints honoured**，列出它遵守了哪些團隊約束。這兩欄不是文件裝飾，而是讓人類 reviewer 可以不從 diff 猜意圖。人審的是這兩欄與報告的一致性。當然，分流的前提是 PR 夠小：Scrum Community 有人抱怨「AI 一次碰二十個檔案，沒人說得出哪個決定弄壞了」；story 切小，是這一切的前提。`

8. 小節：四、reviewer agent 艦隊（[L110](/Users/kochi.chuang/conductor/workspaces/medium-articles/yokohama/2026-10-green-review/article.md:110)）  
原文：`台灣已經有人在做。Claude Taiwan 有一則留言描述自家的「艦隊模式」：兩個審查 agent 分別負責證實與證偽，一個架構 agent 防過度設計，一個總監工。社群已經在自己組 reviewer 艦隊，缺的是禁令與責任設計。本節給它一份可以 review 的設定與三條原則。`  
吃力點：舊文會把社群觀察轉成「為什麼我注意到它」；這裡直接從例子跳到設計規格。缺：缺鋪陳、缺過場。  
改寫：`這件事台灣其實已經有人在做。Claude Taiwan 有一則留言描述自家的「艦隊模式」：兩個審查 agent 分別負責證實與證偽，一個架構 agent 防過度設計，一個總監工。這個例子有意思的地方，不是名稱很帥，而是它已經把 review 從單一 reviewer，拆成多個不同視角的檢查角色。社群已經在自己組 reviewer 艦隊，現在缺的不是想像力，而是禁令與責任設計。本節給它一份可以 review 的設定與三條原則。`

9. 小節：四、reviewer agent 艦隊（[L116](/Users/kochi.chuang/conductor/workspaces/medium-articles/yokohama/2026-10-green-review/article.md:116)）  
原文：`**原則三：與生成分離。** 這是我準備 Claude Certified Architect 考試時的筆記：independent review instance 勝過 self-review；CI review 與 code generation 的 session 要分離；review 分兩道—先逐檔的 local pass，再跨檔的 integration pass。`  
吃力點：這段很像筆記原文，讀者不知道為什麼 session 分離可以降低閉環風險。缺：缺解讀、缺例子、術語第一次出現沒解釋。  
改寫：`**原則三：與生成分離。** 這是我準備 Claude Certified Architect 考試時的筆記：independent review instance 勝過 self-review；CI review 與 code generation 的 session 要分離。原因很直覺，如果 reviewer 跟 generator 共用同一段脈絡，它很容易接著原本的假設往下合理化，而不是重新檢查。review 也應該分兩道：先逐檔的 local pass，看單一檔案內的問題；再跨檔的 integration pass，看 intent、constraint 與整體行為是否對得起來。`

10. 小節：五、閉環禁令（[L210](/Users/kochi.chuang/conductor/workspaces/medium-articles/yokohama/2026-10-green-review/article.md:210)）  
原文：`兩種有條件允許：不同 vendor、隔離 session、人讀報告 approve 加抽樣深讀—允許；同 vendor 但不同 session—允許 comment，**它的 approve 不進 approval artifact 的訊號欄**。不是「不能按 approve」，是按了也不算訊號—這才是它跟異質 reviewer 的實質差別。`  
吃力點：規則很重要，但條件、權限、訊號欄三件事擠在一起，容易被誤讀成 vendor policy。缺：缺鋪陳、缺解讀、破折號當括號連用。  
改寫：`這裡要分清楚兩種有條件允許。第一種是不同 vendor、隔離 session、人讀報告 approve 加抽樣深讀，允許。第二種是同 vendor 但不同 session，允許 comment，但**它的 approve 不進 approval artifact 的訊號欄**。重點不是「不能按 approve」，而是按了也不算訊號。這才是它跟異質 reviewer 的實質差別：前者可以成為一個獨立訊號，後者只能當成額外 comment 來讀。`

11. 小節：六、社交工程 PR（[L275](/Users/kochi.chuang/conductor/workspaces/medium-articles/yokohama/2026-10-green-review/article.md:275)）  
原文：`一項研究（2026 年 7 月）搭了一條五個 agent 的 pipeline—triage、dev、scan、review、deploy—跑五個 production LLM。攻擊很簡單：一個要求「加 telemetry」但其實把 `os.environ` 外洩出去的 issue，標上一句「pre-approved under SEC-2291」。結果約 80% 洗過的 PR **通過掃描這一站**，最差的格子 55% 完全淪陷。內容掃描器抓不到它；只有 intent reasoning 有幫助。另一個約 1,000 個對抗 PR 的基準—把真實 CVE 的修補倒轉回去、重新引入漏洞，再用 15 種敘事包裝—顯示 8 個 review agent 都被敘事影響。`  
吃力點：這段是全篇最有故事性的材料，但寫法仍像壓縮研究卡片，少了舊文常見的「場景慢放」。缺：缺例子、缺鋪陳、缺解讀、破折號當括號連用。  
改寫：`這一節的攻擊範例值得慢一點看。一項研究（2026 年 7 月）搭了一條五個 agent 的 pipeline，包含 triage、dev、scan、review、deploy，並跑五個 production LLM。攻擊很簡單：issue 表面上要求「加 telemetry」，但實際上把 `os.environ` 外洩出去，然後在描述裡標上一句「pre-approved under SEC-2291」。結果約 80% 洗過的 PR **通過掃描這一站**，最差的格子 55% 完全淪陷。也就是說，問題不在 secret scan 沒有努力，而是在這個實驗設定裡，內容掃描器抓不到它；只有 intent reasoning 有幫助。另一個約 1,000 個對抗 PR 的基準，把真實 CVE 的修補倒轉回去、重新引入漏洞，再用 15 種敘事包裝，也顯示 8 個 review agent 都被敘事影響。`

12. 小節：七、Approval 綁人（[L344](/Users/kochi.chuang/conductor/workspaces/medium-articles/yokohama/2026-10-green-review/article.md:344)）  
原文：`approval artifact 的最小定義：人類身分，加上被審 tuple 的 hash—diff、constraint 報告、mutation 報告、reviewer agent 的版本—加上 AI reviewer 的訊號欄，comment 或 approve，只供參考。`  
吃力點：approval artifact 和 tuple hash 第一次真正定義，但被寫成一句名詞串。缺：術語第一次出現沒解釋、名詞短語堆疊、缺例子、破折號當括號連用。  
改寫：`這裡把 approval artifact 先定義到最小可用就好。它至少要留下三件事：第一，人類身分，因為 approval 最後要綁人；第二，被審 tuple 的 hash，包含 diff、constraint 報告、mutation 報告、reviewer agent 的版本，讓之後可以知道當時到底審了哪一份東西；第三，AI reviewer 的訊號欄，記錄 comment 或 approve，但只供參考。`

13. 小節：八、結語與落地順序（[L361](/Users/kochi.chuang/conductor/workspaces/medium-articles/yokohama/2026-10-green-review/article.md:361)）  
原文：`順序：PR template 的兩欄 → deterministic dispatch → AI approve 不計入 → 異質 reviewer，或單一 vendor 的隔離 session → 分流矩陣正式上線 → 高 radius 兩格的指派者禁令 → 免審合併率進月報。**不要第一天就在全部 repo 套指派者禁令**：先有可驗證的格，再有禁令。`  
吃力點：結語落地順序很有用，但像 checklist，少了舊文結尾常見的「為什麼這個順序能降低風險」。缺：缺解讀、缺收尾、缺鋪陳。  
改寫：`如果要落地，我會把順序拆得保守一點：PR template 的兩欄 → deterministic dispatch → AI approve 不計入 → 異質 reviewer，或單一 vendor 的隔離 session → 分流矩陣正式上線 → 高 radius 兩格的指派者禁令 → 免審合併率進月報。這個順序的重點，是先讓 PR 變得可驗證，再開始提高治理強度。**不要第一天就在全部 repo 套指派者禁令**：先有可驗證的格，再有禁令。否則組織感受到的只會是流程變重，而不是 review gate 變準。`

**全篇層級**

章節開場與收尾：主軸有承接，但多數章節開場太像簡報頁標題。第一節到第三節需要補「從 bottleneck 到 control point」的橋；第四節到第五節需要補「艦隊為什麼會引出閉環禁令」；第八節有落地順序，但收尾少了舊文常見的反思句。

圖表前後：表格和 mermaid 內容本身清楚，不該動；要補的是導讀句與讀圖句。尤其第三節矩陣、第四節 YAML / mermaid、第五節閉環圖、第六節社交工程圖，前後目前多是一句功能性 caption，缺少「這張圖要讀哪個因果關係」。

術語第一次出現：`review gate`、`blast radius`、`constraint tests`、`mutation 報告`、`oversight budget`、`approval artifact`、`deterministic dispatch`、`grounded file review`、`closed-loop review`、`system of record`、`branch protection`、`required status check`、`tuple hash` 都需要第一次出現時多半句定義。

hedge：整體沒有被嚴重削掉，像「相關，非因果」「筆者的判斷」「不當量化保證」「尚未在生產 repo 實測」都要保留。需要補 hedge 的地方是第六節的「只有 intent reasoning 有幫助」，最好加上「在這個實驗設定裡」。

**不該再加字**

不要稀釋 [L54](/Users/kochi.chuang/conductor/workspaces/medium-articles/yokohama/2026-10-green-review/article.md:54) 指派者禁令的判斷，它已經有 300 人公司、ticket owner、VP 反問，夠像作者會寫的實務段。

不要稀釋 [L114](/Users/kochi.chuang/conductor/workspaces/medium-articles/yokohama/2026-10-green-review/article.md:114) 「deterministic 的事交給 deterministic 工具」這個鋒利判斷；最多補一個前導，不要把它講軟。

不要刪 [L206-L208](/Users/kochi.chuang/conductor/workspaces/medium-articles/yokohama/2026-10-green-review/article.md:206) 裡的限制說明，特別是「這是我的推論，論文沒有量缺陷」和「回饋成 prompt 的版本論文沒量」。

不要動 [L340](/Users/kochi.chuang/conductor/workspaces/medium-articles/yokohama/2026-10-green-review/article.md:340) 的未實測 hedge。這段可信度來自「設計草稿」「先驗證一次」「GitHub 的規則也會變」。

不要加字到 [L363](/Users/kochi.chuang/conductor/workspaces/medium-articles/yokohama/2026-10-green-review/article.md:363) 的收束句。它是全篇最好的 punchline，留短才有力。

<!-- tokens: in 1274436 out 19842 -->
