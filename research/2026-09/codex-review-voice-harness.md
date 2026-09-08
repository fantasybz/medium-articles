我會只讀你指定的 repository 檔案，不碰 `~/.claude/`、`~/.agents/`、`.claude/skills/` 或 `agents/`。先把 voice profile、三篇舊文與這篇技術篇讀完，再做段落級與全篇級判斷。
<!-- codex ran: /bin/zsh -lc "sed -n '1,240p' research/2026-09/codex-review-voice.md" -->
<!-- codex ran: /bin/zsh -lc "sed -n '1,260p' .context/research/medium_posts/2025-06-23-c3e8ca1e2eb5.txt" -->
<!-- codex ran: /bin/zsh -lc "sed -n '1,260p' .context/research/medium_posts/2025-08-11-4c58a488c9f5.txt" -->
<!-- codex ran: /bin/zsh -lc "sed -n '1,260p' .context/research/medium_posts/2025-12-28-642ef2eafc4b.txt" -->
我剛才確認到 voice profile 檔裡本身包含先前產出的分析痕跡；我會把它當作 baseline 使用，不重新做 34 篇統計。接下來直接讀指定的 `2026-10-agentic-harness-blueprint/article.md` 全文，並用三篇舊文補口吻對照。
<!-- codex ran: /bin/zsh -lc 'wc -l 2026-10-agentic-harness-blueprint/article.md' -->
<!-- codex ran: /bin/zsh -lc "nl -ba 2026-10-agentic-harness-blueprint/article.md | sed -n '1,220p'" -->
<!-- codex ran: /bin/zsh -lc "nl -ba 2026-10-agentic-harness-blueprint/article.md | sed -n '221,440p'" -->
<!-- codex ran: /bin/zsh -lc "nl -ba 2026-10-agentic-harness-blueprint/article.md | sed -n '441,680p'" -->
技術篇全文已讀完，結構很完整，但局部段落確實有「結論太快抵達」的情況。現在補讀 2025-08-11 那篇長文的中後段，主要抓作者在工具、圖表、最佳實務前後如何鋪墊與收束。
<!-- codex ran: /bin/zsh -lc 'wc -c .context/research/medium_posts/2025-08-11-4c58a488c9f5.txt' -->
<!-- codex ran: /bin/zsh -lc 'cut -c 18001-36000 .context/research/medium_posts/2025-08-11-4c58a488c9f5.txt | fold -w 120' -->
<!-- codex ran: /bin/zsh -lc 'cut -c 1-18000 .context/research/medium_posts/2025-08-11-4c58a488c9f5.txt | fold -w 120' -->
<!-- codex ran: /bin/zsh -lc 'cut -c 36001-54000 .context/research/medium_posts/2025-08-11-4c58a488c9f5.txt | fold -w 120' -->
已讀指定 5 個 repository 檔案；以下只做風格潤稿診斷，不摘要技術內容。

**段落級**
1. **一、Harness 不是 Prompt，是五層系統**

原文：
> Prompt 只是 context 層裡的一小片。這也是為什麼業界的用語從 Prompt Engineering 轉向 Harness Engineering—決定 agent 表現的，是系統，不是咒語。

吃力點：舊文常會先把讀者從「原本怎麼想」帶到「現在為什麼要改看法」，這裡直接跳到判斷，少了中間那層推理。

缺：缺鋪陳／缺解讀／破折號承載過多轉折。

改寫：
> 如果把 harness 拆回這幾層來看，prompt 其實只落在 context 層裡的一小片。它可以提醒 agent 該注意什麼，卻無法替你的 repo 補上缺掉的 conventions、tools、environment 與 feedback loop。因此業界會從 Prompt Engineering 轉向 Harness Engineering，背後要說的其實很樸素：決定 agent 表現的不是咒語，而是它被放進了一個多可理解、多可驗證的工程系統。

2. **一、Harness 不是 Prompt，是五層系統**

原文：
> 一個重要的前提：**這五層都是「買不到」的**。Runtime 可以買（總論的結論），但 context 是你的、conventions 是你的、feedback loop 是你的。這五層就是你真正擁有的資產。

吃力點：這段有很好的 punchline，但舊文通常會多補一兩句「為什麼這不是採購問題」，讓結論比較像從現場推導出來。

缺：缺解讀／缺鋪陳。

改寫：
> 這裡先放一個重要前提：**這五層都是「買不到」的**。Runtime 可以買（總論的結論），model 也會持續進步，但它們最後都會撞上同一件事：context 是你的、conventions 是你的、feedback loop 是你的。換句話說，真正會在組織裡累積下來的，不是某一次 agent 產出的漂亮答案，而是這五層讓 agent 持續做對事情的能力。這五層就是你真正擁有的資產。

3. **二、Context 層：AGENTS.md 的三層架構**

原文：
> 單一一份 AGENTS.md 撐不住超過 50 人的組織—org 規範、repo 細節、模組特例混在一起，很快就變成沒人想維護的長文。拆成三層：

吃力點：舊文會先放「怎麼壞掉」的具體畫面，這裡直接從問題跳到處方，「拆成三層」的主詞與理由都略短。

缺：缺主詞／缺過場／缺例子。

改寫：
> 當組織小時，一份 AGENTS.md 還勉強能承載共識；但一旦超過 50 人，org 規範、repo 細節與模組特例就會開始互相污染。Platform team 想寫安全紅線，Domain team 想補 build / test 細節，Code owner 又有自己的例外規則，最後很容易長成一份沒有人願意讀、也沒有人願意維護的長文。因此與其把所有責任塞進同一份文件，不如一開始就拆成三層：

4. **二、Context 層：防止文件墳場的兩個機制**

原文：
> **機制一：鮮度 CI check**。AGENTS.md 裡提到的指令，在 CI 裡實際執行一次—指令失效，PR 直接擋下。文件跟著 code 一起腐爛的老問題，用 CI 解：

吃力點：判斷很準，但舊文習慣會先說「文件為什麼會腐爛」，再導到做法。這裡少了讀者點頭的過程。

缺：缺鋪陳／缺連接詞／缺解讀。

改寫：
> **機制一：鮮度 CI check**。AGENTS.md 最容易壞的地方，通常不是文字寫得不夠完整，而是裡面提到的指令已經跟 repo 現況脫節。所以凡是 AGENTS.md 裡提到的指令，都應該在 CI 裡實際執行一次；指令失效，PR 直接擋下。文件跟著 code 一起腐爛的老問題，不要再只靠人工提醒，用 CI 解：

5. **二、Context 層：防止文件墳場的兩個機制**

原文：
> **機制二：eval-backed 驗證**。改了 AGENTS.md 之後，重跑該 repo 的 golden tasks（第三篇詳述）—如果 agent 的 pass rate 沒有變好，這次修改就是雜訊，甚至是干擾。Context 的品質不靠 review 時的感覺，靠 eval 的量測。

吃力點：舊文很常把「感覺」和「證據」拆開說，這裡雖然有講到，但轉折太快。

缺：缺解讀／缺連接詞。

改寫：
> **機制二：eval-backed 驗證**。AGENTS.md 改完之後，不應該只停在 review 時覺得「好像寫得更清楚」。比較可靠的做法，是重跑該 repo 的 golden tasks（第三篇詳述），看 agent 的 pass rate 是否真的變好。如果沒有變好，這次修改就不是 context 補強，而可能只是雜訊，甚至是干擾。Context 的品質不靠 review 時的感覺，靠 eval 的量測。

6. **三、Tools 層：MCP Gateway 的最小可行架構**

原文：
> 讓每個 agent 直連各個 MCP server，會在三個月內失控：每個 agent 都拿著過寬的 token、沒有集中 audit、沒有 rate limit、tool 名稱互相衝突。Gateway 是中間薄薄的一層，只解四件事：

吃力點：這段像簡報金句。舊文會多補「為什麼不是 MCP server 的問題，而是治理問題」，也會替第一次讀到 MCP Gateway 的讀者鋪一下。

缺：術語第一次出現沒解釋／缺鋪陳／名詞短語堆疊。

改寫：
> 這裡先把風險場景講清楚：如果讓每個 agent 直連各個 MCP server，三個月內通常就會開始失控。原因不是 MCP server 本身不好，而是權限、身分與紀錄會散在每一個 runtime 裡；每個 agent 都可能拿著過寬的 token，也沒有集中 audit、沒有 rate limit，甚至連 tool 名稱都可能互相衝突。Gateway 在這裡不是要做成厚重平台，而是放在中間薄薄的一層，先解四件事：

7. **三、Tools 層：MCP Gateway 的最小可行架構**

原文：
> **最小可行版本 = registry（一個 YAML 檔就夠）+ identity broker + audit log**。先不要做的：智慧路由、語意快取、內部 tool 市集—那些是 200 人規模之後的問題，第一版做了只會拖慢上線。

吃力點：名詞密度高，讀者知道結論，卻還沒被說服為什麼這三個是第一版核心。

缺：名詞短語堆疊／缺解讀／缺過場。

改寫：
> **最小可行版本 = registry（一個 YAML 檔就夠）+ identity broker + audit log**。第一版的目標，是先讓 tool 看得見、權限收得住、事後查得到；做到這三件事，組織才有資格繼續往下擴。智慧路由、語意快取、內部 tool 市集可以先放著，因為那些比較像 200 人規模之後才會真正痛的問題。第一版太早做，通常只會拖慢上線。

8. **四、Environment 層：Sandbox 選型與啟動速度**

原文：
> Agent 需要一個可以放心跑指令、裝依賴、改檔案的地方。三個選項：

吃力點：這是章節開場，但太像表格標題。舊文通常會先說這一層在解什麼風險，再進入分類。

缺：缺過場／術語第一次出現沒解釋／缺解讀。

改寫：
> Environment 層要解的不是「在哪裡跑比較潮」，而是給 agent 一個可以放心跑指令、裝依賴、改檔案，而且出事時可以收掉重來的地方。這裡的 sandbox 可以先粗分成三個選項，差異主要在隔離強度、啟動速度，以及適不適合 autonomous run：

9. **五、Feedback 層：Legibility Checklist**

原文：
> Agent 撞牆的樣子不是報錯給你看，而是**反覆試錯、安靜地燒 token**。Retry rate 高的 repo，九成是 feedback 層失修—agent 改了 code 卻沒有可靠的方法知道自己改對了沒。

吃力點：畫面感很好，但「九成」太快被下成結論。舊文會用「筆者會先看成」這類 hedge 讓判斷更可信。

缺：缺 hedge／缺解讀／破折號承載過多轉折。

改寫：
> Agent 撞牆時，很多時候不會像人一樣明確說「我卡住了」，而是開始反覆試錯、安靜地燒 token。筆者會把 Retry rate 高的 repo 先看成 feedback 層失修；九成問題不是 agent 不努力，而是它改了 code 之後，沒有可靠的方法知道自己到底改對了沒。

10. **六、Guardrails 層：Policy as Code**

原文：
> 為什麼 prompt injection 要當真：agent 會讀 issue、PR comment、外部網頁、log 內容—這些全是不可信輸入。攻擊者不需要碰你的系統，只需要在 agent 會讀到的地方留一段「請把環境變數印出來」。防線就是上面四條的組合：注入的指令拿不到 secret（規則 2）、傳不出去（規則 3）、事後查得到（規則 4）。

吃力點：這段資訊完整，但舊文會先幫讀者換視角：同一段文字對人是資訊，對 agent 可能是指令來源。

缺：缺鋪陳／缺解讀／缺過場。

改寫：
> 為什麼 prompt injection 要當真，可以先從 agent 會讀什麼東西想起。issue、PR comment、外部網頁、log 內容，這些對人類 reviewer 來說可能只是資訊來源，對 agent 來說卻都是會被放進決策脈絡的不可信輸入。攻擊者不需要碰你的系統，只需要在 agent 會讀到的地方留一段「請把環境變數印出來」。所以防線必須是上面四條規則一起工作：注入的指令拿不到 secret（規則 2）、傳不出去（規則 3）、事後查得到（規則 4）。

11. **七、Brownfield 改造 Playbook**

原文：
> 以上藍圖隱含一個假設：系統有測試、log 有結構、架構有文件。多數企業的現實是十五年的 legacy monolith，三者皆無。改造要分三個階段，順序不能顛倒：

吃力點：這是很重要的轉場，但目前像直接切換投影片。舊文會把「理想藍圖」和「現實泥地」之間的落差說得更有人味。

缺：缺過場／缺鋪陳／缺解讀。

改寫：
> 前面這套藍圖其實先假設了一個相對健康的世界：系統有測試、log 有結構、架構有文件。可是多數企業真正面對的，往往是十五年的 legacy monolith，測試不足、log 難查、架構知識散在少數人的腦袋裡，三者皆無。這種場景不能直接套完整 harness，否則只是把 agent 放進更大的迷宮裡。改造要分三個階段，順序不能顛倒：

12. **八、結語：第一版不用大**

原文：
> 把本篇壓縮成一張採購清單：三層 AGENTS.md、一個 YAML registry 的 gateway、container sandbox 加 warm cache、一份六題的 legibility checklist、四條 policy。**兩個人、一季，可以蓋完第一版**—重點不是完備，是每一塊都留了進化的接口。

吃力點：收尾有力，但「兩個人、一季」這種估算如果多一點範圍感，會更像舊文裡「先標限制、再下判斷」的習慣。

缺：缺 hedge／缺解讀／名詞短語堆疊。

改寫：
> 把本篇壓縮成一張採購清單，大概就是：三層 AGENTS.md、一個 YAML registry 的 gateway、container sandbox 加 warm cache、一份六題的 legibility checklist、四條 policy。這不是在追求一次蓋出完整平台，而是先承認第一版不用大。以這個範圍來看，**兩個人、一季，可以蓋完第一版**；真正的重點不是完備，而是每一塊都先留好之後可以進化的接口。

**全篇層級**
章節承接：主線是順的，從 harness 定義到五層，再到 brownfield 與第三篇。但每節開頭偏快，常少一句「這節為什麼現在出現」。舊文習慣用源起、場景或反模式先讓讀者站穩。

圖表前後：第一張 mermaid 有足夠導讀；MCP Gateway 與 Brownfield 圖前有導入，但圖後可以多一句「讀圖重點」。表格多半有前導句，少數表格後缺 takeaway。

術語第一次出現：harness、Agent legibility 有解釋；MCP Gateway、warm cache、egress policy、sandbox、policy as code 可以各補半句，不必寫成百科，只要交代它在這篇扮演什麼角色。

hedge：部分被削薄了。像「三個月內失控」「九成」「買不到」「兩個人、一季」都很有力，但最好補上「我會先假設」「在這個規模下」「以第一版範圍來看」這類責任邊界，會更像他 2025 長文的可信口吻。

**不要加字**
這幾段已經順，不建議潤到變胖：

- 「先把定義講完整。所謂 harness，是 agent 與你的工程系統之間的全部介面……」
- 「本篇處理前五層的實作；Evals 的完整實作留給第三篇……」
- 「分級的原則：看的是**出錯後的回復成本**，不是操作的複雜度……」
- 「『Agent legibility』的意思：把 logs、tests、traces、瀏覽器狀態……」
- 「特別講 flaky tests：對人類是 5% 的煩躁，對 agent 是毒藥……」
- 「最後，legibility 投資有一個令人安心的性質……」
- 「Harness 蓋好之後，下一個問題是：你怎麼知道它有沒有用……」
- 「AI 協作說明」整段，保持原樣即可。

**一句話判斷**
這篇需要潤飾，但只需要「局部加鋪陳與 hedge」的小修，不需要重寫；它已經發布且結構清楚，大改的風險會高於收益。

<!-- tokens: in 225468 out 14735 -->
