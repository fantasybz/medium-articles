我會只讀你指定的 repo 內容，先盤點 Medium 文字檔與新草稿的位置，再把 34 篇的正文段落抽出來做風格比對。過程中不會碰 `~/.claude/`、`~/.agents/`、`.claude/skills/` 或 `agents/`。
<!-- codex ran: /bin/zsh -lc pwd -->
<!-- codex ran: /bin/zsh -lc 'find .context/research/medium_posts -type f | wc -l' -->
<!-- codex ran: /bin/zsh -lc 'wc -l 2026-10-green-overview/article.md' -->
<!-- codex ran: /bin/zsh -lc 'rg --files .context/research/medium_posts 2026-10-green-overview' -->
目前確認研究資料夾正好有 34 個 `.txt`，新稿是 `2026-10-green-overview/article.md`。下一步我會先看幾篇樣本的檔案格式，確認標題、Medium chrome、作者尾段分界，再批次抽正文。
<!-- codex ran: /bin/zsh -lc "sed -n '1,80p' .context/research/medium_posts/2021-12-28-eda14393c0df.txt" -->
<!-- codex ran: /bin/zsh -lc 'tail -n 80 .context/research/medium_posts/2021-12-28-eda14393c0df.txt' -->
<!-- codex ran: /bin/zsh -lc "sed -n '1,80p' .context/research/medium_posts/2025-08-13-c0ac58712d92.txt" -->
<!-- codex ran: /bin/zsh -lc "sed -n '1,120p' 2026-10-green-overview/article.md" -->
樣本顯示每篇是 Medium 抓下來的一整串文字：正文大多從 `ListenShareMore` 後開始，尾端在 `FollowWritten by...` 之後是 Medium 介面。標題需要從 `min read·日期` 前的作者欄位反推，我會先建立一份檔名、標題候選、正文長度的索引，避免把 Medium 介面文字混進證據。
這個環境是唯讀的，連 shell here-doc 也會被擋，因為它會嘗試建立暫存檔。我會改用不落地的 `python3 -c` / `rg` 方式讀取與整理，不產生任何檔案。
<!-- codex ran: /bin/zsh -lc "python3 -c \"from pathlib import Path; import re; root=Path('.context/research/medium_posts');
for p in sorted(root.glob('*.txt')):
    s=p.read_t -->
標題候選已能抓到一部分，但早期幾篇的 metadata 形式不完全一致。接著我會用更寬鬆的日期與 `ListenShareMore` 分界重新索引，並抽每篇正文的開頭、段落轉折、結尾句，這些會是後面口吻判斷的主要依據。
<!-- codex ran: /bin/zsh -lc "python3 -c \"from pathlib import Path; import re
for p in sorted(Path('.context/research/medium_posts').glob('*.txt')):
 s=p.read_text(encoding='u -->
有些檔案的 chrome 被壓縮得更嚴重，`ListenShareMore` 沒有出現；這不影響閱讀，但需要另一個正文起點。下一步我會抓每篇內的 `read·日期`、`Press enter`、`Written by` 等實際分界，並直接抽正文片段來人工核對。
<!-- codex ran: /bin/zsh -lc "sed -n '1,1p' .context/research/medium_posts/2022-02-25-d37016c96fa3.txt" -->
<!-- codex ran: /bin/zsh -lc 'tail -c 3000 .context/research/medium_posts/2022-02-25-d37016c96fa3.txt' -->
<!-- codex ran: /bin/zsh -lc 'rg -n "read·|Listen|Share|Written by|Responses|FollowWritten" .context/research/medium_posts/2022-02-25-d37016c96fa3.txt' -->
<!-- codex ran: /bin/zsh -lc 'wc -c .context/research/medium_posts/2022-02-25-d37016c96fa3.txt' -->
<!-- codex ran: /bin/zsh -lc "python3 -c \"from pathlib import Path; import re
for p in sorted(Path('.context/research/medium_posts').glob('*.txt')):
 s=p.read_text(encoding='u -->
<!-- codex ran: /bin/zsh -lc "sed -n '1,1p' .context/research/medium_posts/2023-05-12-997f40f936dd.txt" -->
<!-- codex ran: /bin/zsh -lc 'rg -n "read·|ShareMore|榮民叔叔轉職" .context/research/medium_posts/2023-05-12-997f40f936dd.txt' -->
<!-- codex ran: /bin/zsh -lc 'rg -n "read·|ShareMore|榮民叔叔轉職" .context/research/medium_posts/2023-05-12-b232802632a3.txt' -->
<!-- codex ran: /bin/zsh -lc 'rg -n "read·|ShareMore|榮民叔叔轉職" .context/research/medium_posts/2023-05-12-df260dd66909.txt' -->
<!-- codex ran: /bin/zsh -lc 'rg -n "read·|ShareMore|榮民叔叔轉職" .context/research/medium_posts/2023-05-15-687a6dba39a1.txt' -->
我已經把 34 篇都定位到正文分界，包含幾篇沒有 `min read` 的早期/系列文格式。現在轉去讀新稿全文，目標是找出「資訊正確但過短、少了作者慣常鋪陳」的段落，而不是重寫整篇。
<!-- codex ran: /bin/zsh -lc "nl -ba 2026-10-green-overview/article.md | sed -n '361,540p'" -->
<!-- codex ran: /bin/zsh -lc "nl -ba 2026-10-green-overview/article.md | sed -n '1,180p'" -->
<!-- codex ran: /bin/zsh -lc "nl -ba 2026-10-green-overview/article.md | sed -n '181,360p'" -->
<!-- codex ran: /bin/zsh -lc "nl -ba 2026-10-green-overview/article.md | sed -n '541,760p'" -->
新稿的問題很明確：很多段落是「判斷已經下完、結論很銳利」，但少了舊文常見的「我怎麼走到這個判斷」與「讀者可能在哪裡卡住」兩層緩衝。接著我會回到 34 篇舊文，抽出證據句，特別看第一人稱、問題句、比喻、hedge、段落收束句。
<!-- codex ran: /bin/zsh -lc "python3 -c \"from pathlib import Path; import re
root=Path('.context/research/medium_posts')
for p in sorted(root.glob('*.txt')):
 s=p.read_text(e -->
<!-- codex ran: /bin/zsh -lc "python3 -c \"from pathlib import Path; import re
# manual title map for stable labels
titles={
'2021-12-28-eda14393c0df.txt':'【課程筆記】不確定時代下的敏捷測試-利用 -->
抽樣腳本碰到資料夾裡一個額外的 `*.body.txt` 候選，先停在第一篇，沒有寫入任何檔案。我會重新用一開始盤點出的 34 個原始檔名固定清單跑，避免把衍生或中間檔算進去。
<!-- codex ran: /bin/zsh -lc 'rg --files .context/research/medium_posts | sort' -->
重新盤點後，資料夾裡其實有 34 個帶 Medium id 的原始檔，另外 4 個 `*.body.txt` 看起來是清理後的重複正文。我會以 34 個原始檔為準，必要時只用重複正文核對分界，不把它們當成新文章。
<!-- codex ran: /bin/zsh -lc "python3 -c \"from pathlib import Path; import re
files=sorted([p for p in Path('.context/research/medium_posts').glob('????-??-??-*.txt') if '.bod -->
舊文的穩定訊號已經浮現：早期文章非常常用「源起／後記／參考」框架，並用自嘲、生活場景、讀書路徑把概念帶進來；2025 後變得更像正式長文，但仍保留「先標限制、再下判斷」的習慣。接著我會用全文掃描計數與句子抽樣確認常用詞與 hedge。
<!-- codex ran: /bin/zsh -lc "python3 -c \"from pathlib import Path; import re
files=sorted([p for p in Path('.context/research/medium_posts').glob('????-??-??-*.txt') if '.bod -->
<!-- codex ran: /bin/zsh -lc "python3 -c \"from pathlib import Path; import re
pairs=[
('2021-12-28-eda14393c0df.txt','【課程筆記】不確定時代下的敏捷測試-利用持續測試交付價值',['哄女兒入睡後','為了不要讓心得筆記','現階段自 -->
我以 34 個帶 Medium id 的原始 `.txt` 為準，忽略 Medium chrome 與 `Written by / Responses` 後面的尾巴；資料夾裡另有少數 `.body.txt` 重複清理稿，沒有當成新文章計算。

**1. 口吻**
他的聲音是「讀書筆記型的工程實踐者」：不是單純教學，也不是純評論，而是把書、課程、論文、社群觀察，拉回自己的工作經驗與學習路徑。人稱上早期常用「筆者」「小弟」「自己」，後期轉為「本文」「我認為」「筆者暫定」，語氣從親切自嘲走向更像架構性長文，但仍保留自我校準。

證據：
1. 《不確定時代下的敏捷測試》：「哄女兒入睡後，獨自在書桌前進行每日關機儀式」
2. 《不確定時代下的敏捷測試》：「儘量以最小限度透露課程內容，多一點心得感想」
3. 《不確定時代下的敏捷測試》：「小弟一臉疑惑、不知所措的樣子」
4. 《你所不知道的必學前端 Debug 技巧》：「誰會花10分鐘，去閱讀一篇網路上不明人士」
5. 《你所不知道的必學前端 Debug 技巧》：「一條龍沒有不好，但別成為只會跑龍套的人」
6. 《Extreme Programming Explained》：「歡迎有興趣的朋友一同入坑閱讀」

**2. 節奏**
他的段落通常不是短打，而是「長段鋪陳 → 問題句 → 小結句」。常先放生活場景或閱讀場景，再塞入 technical terms、括號補充、英文原文、圖表說明，最後用一句口語化句子收束。這種長段不是冗餘，而是讓讀者跟上他的思路。

證據：
7. 《CORS 錯誤》：「若了解全貌首先將單字拆解、進行細部分析、各別擊破」
8. 《CORS 錯誤》：「舉例比較容易解釋」
9. 《Business District 之旅》：「換個方向思考，也就是為什麼(Why)使用者要用這個產品？」
10. 《Historical district 之旅》：「把焦點拉回軟體領域」
11. 《Tidy First?》：「雜草都快要長比人高了」
12. 《Role of the Tester》：「事情不是傻人想的那麼簡單」

**3. 概念鋪陳**
他解釋概念的典型順序是：書錨或課程錨點 → 自己為何注意到它 → 先定義名詞 → 用類比或場景降低抽象度 → 回到軟體工程實務 → 加上限制條件。比喻很重要，而且常是城市、旅行、車燈、花園、海面這類可視化場景。

證據：
13. 《Business District 之旅》：「如同一般城市的劃分」
14. 《Business District 之旅》：「按圖索驥，就可以用最短間時間，得到最大的收獲」
15. 《Historical district 之旅》：「Bug 的集散地，春風吹又生」
16. 《You are the headlights》：「開著卡車在夜晚山間彎路上奔馳著」
17. 《Question everything》：「提問就像是服用特效藥一樣」
18. 《XP 的價值、原則與實踐》：「你得親自下田」
19. 《在非決定性的海面上守住品質》：「先看清，再出手」
20. 《在非決定性的海面上守住品質》：「我們的系統越來越像海」

**4. 開場收尾**
開場常用「源起／前言／引言」交代這篇文從哪裡長出來，而不是直接下結論。收尾常用「後記／結語」回到自我提醒、下一篇規劃、與讀者共勉。這讓文章像一段 learning journey，而不是只有資訊摘要。

證據：
21. 《Extreme Programming Explained》：「週末二天下午的空檔時光」
22. 《Planning Extreme Programming》：「曾經以為規劃是裝模作樣的工具」
23. 《Perfect Software》：「未讀之書，卻變成了重讀原文版」
24. 《LLST #10》：「完成只是有限條件下的暫停」
25. 《不確定時代下的敏捷測試》：「與讀者們共勉之 一起加油」

**5. 常用句型**
他常用「可能／也許／應該／當然／筆者試著／先假定／換句話說／回到」來區分事實、推論與個人立場。好的地方是他會把事實與 opinion 分層；像新稿裡「前提，不是事實」「觀察，非統計」「不是業界標準」「待 pilot 校準」其實很符合他的成熟期口吻。不要把這些 hedge 刪掉，它們是可信度的一部分。

證據：
26. 《不確定時代下的敏捷測試》：「當然這只是現階段自己給定的最佳解釋」
27. 《You are the headlights》：「以上幾題並沒有正確答案」
28. 《You are the headlights》：「也許你的世界只有白天」
29. 《Role of the Tester》：「測試人員並不是神」
30. 《與不確定性共舞》：「閱讀心得與延伸思考」
31. 《LLM 雙層測試護欄》：「非決定性的『學習型系統』」
32. 《觀測的修復之道》：「以為每天盯著監控儀表板，就是把『可觀測性』做好了」

**6. 草稿改寫**
| 原文 | 依作者口吻改寫 |
|---|---|
| 「三個情境，多數團隊至少經歷過一個。」 | 先不急著談 gate，回想一下這半年導入 coding agent 的現場，很多團隊其實都卡在差不多的地方。下面三個情境，不一定每個 repo 都發生過，但多數 Engineering VP 或 QA lead 應該至少看過其中一種。 |
| 「一句話的回答，刻意寫成可以不同意的形狀：」 | 先把我的立場講得尖銳一點，因為這句話如果寫得太圓滑，就很容易變成另一句口號。你可以不同意，但至少可以拿它回去對照自己的 branch protection、review policy 與 agent workflow。 |
| 「這本書我還沒讀完，引用集中在定義 testing 與 checking 的那一章與一篇訪談。」 | 先說限制：James Bach 這本《Taking Testing Seriously》我還沒有完整讀完，所以這裡不假裝做全書導讀。本文只取用 testing / checking 定義那一章，以及一篇訪談，作為後面三道閘的語言錨點。 |
| 「每個數字都標領域、樣本數與日期；前兩層各一篇 in-domain 錨點，第三層 code 領域沒有現成數字，用自己的 golden set 量。」 | 這裡刻意把每個數字都標上領域、樣本數與日期，因為 agent 領域的研究更新太快，數字一離開脈絡就很容易被誤用。前兩層我各放一篇 in-domain 錨點；第三層目前 code 領域還沒有我能直接引用的現成數字，所以做法很樸素：回到自己的 golden set 量。 |
| 「人眼也不是安全網：86 位開發者判斷 LLM 寫的斷言，正確的有 74% 看得出來，錯誤的只有 49%，信心卻不降（Poor and Overconfident Judges，2026 年 7 月）。第七節會用到這個數字。」 | 這裡還要補一個容易被忽略的點：把人放回 review 流程，不代表安全網就自動恢復。Poor and Overconfident Judges 在 2026 年 7 月量到，86 位開發者判斷 LLM 寫的斷言時，正確斷言有 74% 看得出來，錯誤斷言卻只有 49%，而信心沒有跟著下降；第七節談 review gate 時會再回來用這個數字。 |
| 「再加一個第一手的：模式語言工作坊的實例—5 個測試全綠，event sourcing 的 replay 路徑從未執行；細節在測試篇。」 | 再補一個比較貼近我自己的例子。在模式語言工作坊裡，表面上 5 個測試全綠，但回頭看才發現 event sourcing 的 replay 路徑從未執行；這不是哪個工具特別差，而是提醒我們：綠燈沒有告訴你它沒走過哪一條路。細節放到測試篇。 |
| 「右欄每一格都是一個 check，不是一個 prompt。」 | 右欄真正重要的地方，不是把 AGENTS.md 寫得更漂亮，而是每一格最後都能落成一個可執行的 check。prompt 可以影響 agent 的行為，但只有 check 才能在它犯錯、偷懶或誤解時，留下可被組織使用的證據。 |
| 「兩者可以差很多；用營運篇的 20–50 個 golden case 跑 k = 5 到 10，自己量。」 | pass@1 與 pass^k 看起來只差一個符號，但決策意義其實差很多。不要拿別人的 benchmark 直接推授權，先用營運篇那組 20–50 個 golden case，跑 k = 5 到 10，讓自己的系統把變異性攤開來給你看。 |

**7. 一句話**
Kochi Chuang 的聲音，是一位持續讀書、做筆記、回到現場驗證的工程實踐者，用謙遜的第一人稱、厚實的脈絡鋪陳與帶 hedge 的判斷，把抽象方法論翻成團隊可以討論的工程語言。

**潤飾守則**
1. 要保留「源起／前言」的來路，不要一開始就只剩結論。
2. 要補「我怎麼想到這裡」的中間層，尤其是書、課程、社群、工作經驗的觸發點。
3. 要保留 `筆者認為`、`前提不是事實`、`觀察，非統計` 這類責任邊界。
4. 要把 technical term 留在原位，必要時加中文說明，不要全部翻掉。
5. 要多用問題句幫讀者停一下，例如「那這代表什麼？」。
6. 要用類比，但類比後一定要「把焦點拉回軟體領域」。
7. 不要把長段全切成短句；他的可讀性來自脈絡，不是極簡。
8. 不要刪掉自嘲與生活感，它讓硬題目有入口。
9. 事實、數字、研究結論要標來源脈絡；意見要明確標成意見。
10. 收尾要留下自我提醒、下一步或讀者可帶走的問題，不要只做 summary。

<!-- tokens: in 1211471 out 22620 -->
