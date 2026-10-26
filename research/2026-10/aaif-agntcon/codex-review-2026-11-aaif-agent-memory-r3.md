# Codex review — 2026-11-aaif-agent-memory/article.md

> model: gpt-6.1-sol, reasoning: xhigh, 2026-10-26 00:13. 原話照錄，未經摘要。第 3 輪；審的是 2026-10-25 改寫並依前一輪意見修訂後的版本。

我會先讀 STYLE.md 與 style brief，再逐節核對原始材料、程式碼與舊文 recall；全程只讀 repository，不修改檔案，也不讀取你列出的禁用路徑。
<!-- codex ran: /bin/zsh -lc 'cat STYLE.md' -->
<!-- codex ran: /bin/zsh -lc 'cat research/2026-10/style_brief.md' -->
<!-- codex ran: /bin/zsh -lc "rg --files -g 'AGENTS.md' -g '"'!agents/**'"' -g '"'!.claude/**'"' -g 'article.md' -g '*LONGMEM*' -g '*consolidation*' -g '*auto-forget*' -g '*hyb -->
<!-- codex ran: /bin/zsh -lc 'nl -ba 2026-11-aaif-agent-memory/article.md' -->
<!-- codex ran: /bin/zsh -lc "find .context/research/aaif-2026-10-23 -maxdepth 3 -type f -not -path './agents/*' -not -path './.claude/*'" -->
<!-- codex ran: /bin/zsh -lc "rg --files --hidden --no-ignore .context/research/aaif-2026-10-23/slides/text | rg '2WZJf|2QlDp|2RqMK'" -->
<!-- codex ran: /bin/zsh -lc "rg '"'^##|''^###'"' 2026-10-green-*/article.md 2026-09-agentic-engineering-platform/article.md 2026-09-agentic-org-design/article.md 2026-10-agent -->
<!-- codex ran: /bin/zsh -lc 'cat .context/research/aaif-2026-10-23/facebook-post-provenance.json' -->
<!-- codex ran: /bin/zsh -lc "rg --files --hidden --no-ignore .context/research/aaif-2026-10-25 | rg 'consolidation|auto-forget|hybrid-search|observe.ts|LONGMEM|README|anthropi -->
<!-- codex ran: /bin/zsh -lc 'cat .context/research/aaif-2026-10-23/slides/text/2WZJf-01-crabrag-graph-memory-for-ai-assistants-v0-6-agntcon-japan.txt' -->
<!-- codex ran: /bin/zsh -lc 'cat .context/research/aaif-2026-10-23/slides/text/2RqMK-01-agnt-con-2026-v7.txt' -->
<!-- codex ran: /bin/zsh -lc 'cat .context/research/aaif-2026-10-23/slides/text/2QlDp-01-agentmemory-agntcon-mcpcon-opening.txt' -->
<!-- codex ran: /bin/zsh -lc "rg --files --hidden --no-ignore .context research | rg '(consolidation-pipeline\\.ts|auto-forget\\.ts|hybrid-search\\.ts|LONGMEMEVAL\\.md|airas.*R -->
目前最嚴重的是第五節的案例前後矛盾：前文說報表原本就在驗收清單、只是沒執行；後面的 J-17／J-18 卻改成判準從 v2 升到 v3 才加入報表。這會混淆「補做漏驗」與「改版判準」，連帶讓第六節不知道該驗哪一種更正。
<!-- codex ran: /bin/zsh -lc 'nl -ba .context/research/aaif-2026-10-24/third-article/agentmemory-code/auto-forget.ts' -->
<!-- codex ran: /bin/zsh -lc 'nl -ba .context/research/aaif-2026-10-24/third-article/agentmemory-code/consolidation-pipeline.ts' -->
<!-- codex ran: /bin/zsh -lc "rg --files --hidden --no-ignore .context/research/aaif-2026-10-24/third-article | rg -v '\\.(png|jpg|pdf|pptx|log)"'$'"'" -->
<!-- codex ran: /bin/zsh -lc 'cat .context/research/aaif-2026-10-24/third-article/airas-readme.md' -->
<!-- codex ran: /bin/zsh -lc "rg --files --hidden --no-ignore .context research -g '"'!**/before/**'"' -g '"'!**/review/**'"' -g '"'!**/publication/**'"' -g '"'!**/codex-fix/** -->
<!-- codex ran: /bin/zsh -lc "python3 -c 'from pathlib import Path; p=Path(\".context/research/aaif-2026-10-23/slides/text/2WZJf-01-crabrag-graph-memory-for-ai-assistants-v0-6- -->
<!-- codex ran: /bin/zsh -lc "sed -n '1,190p' .context/research/aaif-2026-10-24/third-article/agentmemory-code/hybrid-search.ts" -->
<!-- codex ran: /bin/zsh -lc 'cat research/2026-10/aaif-agntcon/memory-media-manifest.json' -->
<!-- codex ran: /bin/zsh -lc 'cat .context/research/aaif-2026-10-24/third-article/agentmemory-longmemeval.md .context/research/aaif-2026-10-24/third-article/agentmemory-code/ma -->
<!-- codex ran: /bin/zsh -lc "rg --files --hidden --no-ignore .context/research/aaif-2026-10-24/third-article/web .context/research/aaif-2026-10-25 | rg '(context|anthropic|eva -->
<!-- codex ran: /bin/zsh -lc "python3 -c 'from pathlib import Path; jobs={\"2026-10-agentic-harness-blueprint/article.md\":[\"## 二、\"],\"2026-09-agentic-org-design/article.md\" -->
<!-- codex ran: /bin/zsh -lc "python3 -c 'from pathlib import Path; jobs={\"2026-11-same-spec-overview/article.md\":[\"## 二、\",\"## 十、\"],\"2026-11-same-spec-contract/article.m -->
<!-- codex ran: /bin/zsh -lc 'cat .context/research/aaif-2026-10-24/third-article/web/2RqMK-agenda-text.txt .context/research/aaif-2026-10-24/third-article/web/2WZJf-agenda-tex -->
<!-- codex ran: /bin/zsh -lc "rg -n 'calib|validat|golden|human|independen|test set|hold.out|judge|rubric' .context/research/aaif-2026-10-25/hire/ai-agent-metrics.md .context/r -->
<!-- codex ran: /bin/zsh -lc "rg -n 'PagerDuty|保留|校準|三種|主張|mem|判定|工作階段|1.30|1.31|"'^(##|###)'"' 2026-11-aaif-after-tokyo/article.md 2026-11-aaif-agent-handoffs/article.md" -->
<!-- codex ran: /bin/zsh -lc "rg -n 'Effective context|context rot|just.in.time|sub.agent|Demystifying|An eval at 100%' .context/research research -g '*.txt' -g '*.md' -g '*.ht -->
三場簡報的主要頁碼、95.2%／86.2% 的檢索數字，以及整理程式的欄位更新，目前都能對上 repo 來源。仍需收緊的是推論邊界：正文已說沒有追到這些欄位對檢索結果的下游影響，開場與結尾卻容易讓讀者以為已觀察到錯誤記憶影響下一次回答。我正在核對舊文回扣與驗收設計。
<!-- codex ran: /bin/zsh -lc "sed -n '190,355p' .context/research/aaif-2026-10-24/third-article/agentmemory-code/hybrid-search.ts" -->
<!-- codex ran: /bin/zsh -lc "rg -n '常駐|單次|"'^##|judge|holdout|## 九'"' 2026-11-same-spec-overview/article.md 2026-10-green-overview/article.md 2026-10-green-testing/article.md  -->
<!-- codex ran: /bin/zsh -lc "rg -n 'Anthropic|context rot|just.in.time|An eval at 100%' .context/research/aaif-2026-10-24/third-article/web research/2026-10/aaif-agntcon/memor -->
<!-- codex ran: /bin/zsh -lc "rg -n 'calib|validat|golden|human|independen|test set|hold.out|judge|rubric' .context/research/aaif-2026-10-25/hire/ai-agent-metrics.md .context/r -->
<!-- codex ran: /bin/zsh -lc "sed -n '350,430p' .context/research/aaif-2026-10-24/third-article/agentmemory-code/hybrid-search.ts" -->
<!-- codex ran: /bin/zsh -lc "sed -n '1,36p' .context/research/aaif-2026-10-25/hire/ai-agent-metrics.md" -->
<!-- codex ran: /bin/zsh -lc "sed -n '65,103p' .context/research/aaif-2026-10-24/third-article/agentmemory-code/consolidation-pipeline.ts" -->
<!-- codex ran: /bin/zsh -lc "nl -ba 2026-11-aaif-agent-memory/article.md | sed -n '70,230p'" -->
<!-- codex ran: /bin/zsh -lc "nl -ba .context/research/aaif-2026-10-23/slides/text/2QlEA-01-from-clicks-to-context-building-an-open-source-evaluation-pipeline-for-ai-agents-ine -->
<!-- codex ran: /bin/zsh -lc "rg -n '資料外洩|test|holdout|oracle|semantic|accessCount|更新時間|暫停|v2|v3|更正|資料與方法' 2026-11-aaif-agent-memory/article.md" -->
<!-- codex ran: /bin/zsh -lc "python3 -c 'from pathlib import Path; p=Path(\".context/research/aaif-2026-10-23/slides/text/2WZJf-01-crabrag-graph-memory-for-ai-assistants-v0-6- -->
<!-- codex ran: /bin/zsh -lc "python3 -c 'import hashlib,json; from pathlib import Path; b=Path(\".context/research/aaif-2026-10-24/third-article\"); rows=json.loads((b/\"agent -->
<!-- codex ran: /bin/zsh -lc "python3 -c 'import hashlib,json; from pathlib import Path; b=Path(\".context/research/aaif-2026-10-24/third-article\"); rows=json.loads((b/\"agent -->
<!-- codex ran: /bin/zsh -lc "rg -n 'write_text|content|base64|sha|readme|consolidation|decode' .context/research/aaif-2026-10-24/third-article/capture_sources.py" -->
<!-- codex ran: /bin/zsh -lc "rg --files --hidden --no-ignore .context/research/aaif-2026-10-24/third-article -g '"'!**/before/**'"' -g '"'!**/review/**'"' -g '"'!**/publicatio -->
<!-- codex ran: /bin/zsh -lc "python3 -c 'import hashlib,json; from pathlib import Path; b=Path(\".context/research/aaif-2026-10-24/third-article\"); rows=json.loads((b/\"agent -->
舊文回扣有一處要改：變異篇第八節分的是「檢查 grader、檢查新候選、檢查交付方法」，本篇把第二項換成「重評既有判定」，卻仍稱為原文的三種重查。另外，「發布前確認判定仍有效」仍有競態：確認後、寫入前若發生撤回，舊摘要仍可能發布；第六節的交錯測試需要涵蓋這個空隙。
目前不宜定稿。核心案例混淆了「漏做既定驗收」與「修改驗收標準」；更正契約也還留著會讓舊摘要復活的競態。

以下依 repo 內的三份簡報、固定版本程式碼、benchmark、AIRAS README、舊文與照片來源核對。本篇沒有時間碼；Anthropic 兩篇原文缺少完整本機快照，無法在你限定的範圍內獨立核對全文。

## 致命問題

1. **五、〈觀察沒有改變，結論仍可能需要撤回〉／〈讓更正沿引用關係，傳到下一份摘要〉：同一案例換了問題。**

   前文說：「**原報表要求也沒有改變；改變的是我們知道當時少驗了什麼。**」後文卻寫：「**判準版本 v2（版本達標與健康檢查）……原因是判準漏了每晚報表**」，接著用「**判準版本 v3（含每晚報表）**」。

   讀者無法判斷：報表一直是要求、驗收器漏檢，還是要求後來才新增。這三者需要不同的更正。

   **修法：**主案例固定使用原本就包含報表的要求版本；撤回的是錯誤判定。若驗收程式漏檢，另記驗收器版本。真正新增報表要求的情況，留到最後一段當另一個案例，不能混進 J-17／J-18。

2. **五、〈讓更正沿引用關係，傳到下一份摘要〉／六、：發布前檢查仍不能阻止舊摘要復活。**

   「**所以摘要發布前要核對所依據的判定是否仍有效**」仍有空隙：甲確認 J-17 有效，乙撤回 J-17，甲才提交 P-9。第六節目前的交錯測試，沒有明確卡在「最後檢查完成、尚未寫入」的位置。

   **修法：**把依據版本核對與摘要發布綁成同一次不可分割的提交；版本不符就拒絕。另定義更正生效時間的承諾：只約束之後的新查詢，還是也約束早已載入舊 context、稍後才輸出的回答？目前「更正完成」沒有完整定義。

## 重要問題

1. **四、〈更新與遺忘，要讓下一次檢索真的不同〉：把未追查的排序因果寫得太實。**

   「**甚至因舊紀錄累積較多使用次數而把 B 排在前面。**」

   已保存的 [hybrid-search.ts](/Users/kochi.chuang/conductor/workspaces/medium-articles/dodoma/.context/research/aaif-2026-10-24/third-article/agentmemory-code/hybrid-search.ts:194) 在這條路徑使用搜尋名次、權重與 agreement bonus，沒有直接使用 `accessCount`。目前不能把計數增加接成這條排序結果。

   **修法：**改成「若檢索另以使用次數加權，舊紀錄可能……」，或追出實際使用該欄位的路徑再下結論。程式觀察與假設風險分開寫。

2. **四、〈反覆出現的說法，還需要新的查核〉：合併事實時，對象識別的問題比計數更直接。**

   「**新抽出的事實若與既有文字相同，只忽略大小寫……**」

   [整理函式](/Users/kochi.chuang/conductor/workspaces/medium-articles/dodoma/.context/research/aaif-2026-10-24/third-article/agentmemory-code/consolidation-pipeline.ts:95) 讀取整個 summaries／semantic 集合，再按事實文字比對；這個分支沒有按服務、專案或環境核對。同一句「This service uses Postgres」可能描述不同服務。

   **修法：**補上推論：同一句文字不等於同一項事實，合併前必須確認主體與適用範圍。是否有其他外層保護，另行註明未追查。這才能接住第三節剛建立的「它屬於誰」。

3. **五、〈觀察沒有改變，結論仍可能需要撤回〉：講者原則與作者實作推論混在同一句。**

   「**規則與權限由誰維護也要指定，否則它只是多放一個 agent。三條原則是……**」

   簡報第 37、39 頁支持 verifier 獨立、研究系統不能影響它；沒有直接提出本文這套維護責任安排。

   **修法：**先完整交代講者三原則，再另起一句：「放到團隊實作，我還會要求……」。不要讓作者建議借到講者的證據地位。

4. **六、：把作者延伸的方法稱為 PagerDuty 的規矩。**

   「**照第一篇 PagerDuty 的規矩，先分清三種材料……**」

   [PagerDuty 簡報](/Users/kochi.chuang/conductor/workspaces/medium-articles/dodoma/.context/research/aaif-2026-10-23/slides/text/2QlEA-01-from-clicks-to-context-building-an-open-source-evaluation-pipeline-for-ai-agents-ine-s-bolan-os.txt:449) 明說的是人工標記 gold set 與 confidence threshold 校準，沒有明說這三類材料的分割。

   **修法：**寫成「沿用 PagerDuty 對評分器校準的要求，本篇再把……分開」。保留方法，修正歸屬。

5. **六、：變異篇的 recall 改寫了原文分類。**

   「**那篇第八節還分了三種重查，對應到記憶上是……重評既有判定……**」

   [變異篇第八節](/Users/kochi.chuang/conductor/workspaces/medium-articles/dodoma/2026-11-same-spec-variance/article.md) 分的是檢查 grader、檢查新候選、檢查交付方法。第二項不是重評既有判定。

   **修法：**明說原文三類，再說本篇新增「用既有觀察重評舊判定」。不要把新增分類包成原文回扣。

6. **一、：思考形成的時間缺乏支撐，也和開場順序打架。**

   「**這個問題是在行程的最後一晚想清楚的。**」

   開場卻由整理相簿、對照簡報與閱讀程式，帶出這個問題。Facebook 告別貼文能支持旅程日期，不能支持當晚形成了這項技術判斷。

   **修法：**刪掉這個時間斷言；除非作者確實記得且願意確認。照片日期可以保留，不必替照片補上一個思想頓悟。

7. **三、〈把時間與適用範圍放進關係裡〉：尚未分清「何時取得」與「何時有效」。**

   「**保留來源紀錄及取得時間**」、「**查詢優先使用符合目標與時間的資料**」。

   今天讀到的文件，可能描述上個月的部署；較晚取得不代表較接近目前狀態。「優先」也沒有說明不適用資料是否仍能支持結論。

   **修法：**沿用同一案例補一句：今天補登的舊部署紀錄，仍屬於舊環境。分開記錄觀察／有效期間與系統收錄時間，並說明歷史資料只能作為歷史依據。

8. **四、到六、：以下轉場仍靠換話題，沒有完成問題交接。**

   | 位置與原句 | 缺少的交接／具體修法 |
   |---|---|
   | 四、〈先分清要保存的經驗，以及這一輪要讀的內容〉：「**保存之後，取回才是問題**」 | 問的是更正，卻轉進 BM25、RRF 與 benchmark。先交代「相關材料找得到，仍不代表有效更正找得到」，再限制搜尋介紹的篇幅。 |
   | 四、〈反覆出現的說法，還需要新的查核〉：「**記憶不只是搜尋舊文字**」 | 前段沒有留下抽取程序的問題。改成「搜尋只能找既有紀錄；但摘要如何被升格成事實，決定了被找到的究竟是什麼」。 |
   | 四、〈更新與遺忘，要讓下一次檢索真的不同〉：「**使用頻率也不能裁決來源衝突**」 | 前段已轉到一次性授權，這裡突然回到衝突。把衝突捷徑移到更新 B／C 的例子後。 |
   | 六、：「**還有兩種情況……它們不是本文的主問題**」 | 刪除與存取控制另開支線。移到附錄，主表保留適用性、更正與傳播。 |
   | 六、：「**還有兩條不同的界線要分開**」 | 單段塞進比較設計、holdout、指標飽和、grader 校準。拆成「怎麼比較」與「題目何時失去評估用途」兩段。 |

## 次要問題

1. **三、開場：頁碼與概括範圍不精確。**

   「**簡報第 8、9 頁描述這類助理的做法……每天早上全部重讀一次**」。

   「every morning」在第 6 頁；第 9 頁寫 every session，且談的是該演講中的 OpenClaw 設定。

   **修法：**引用第 6、8–9 頁，改成「他描述的 OpenClaw 設定會在每次 session 重讀」，避免概括成這類助理的共同實作。

2. **四、〈更新與遺忘，要讓下一次檢索真的不同〉：中文限制說過頭。**

   「**中文句子沒有空白……這條捷徑根本比不出來。**」

   完全相同的中文句子仍會得到相似度 1；不同整句才容易直接變成 0。另外，程式只處理最新候選中的前 1,000 筆。

   **修法：**改成「不能有效辨識不同中文句子的近似與矛盾」，補上候選範圍。英文反例也明確區分「增加一詞」與「替換一詞」，兩者的集合相似度不同。

3. **五、〈讓更正沿引用關係，傳到下一份摘要〉：data leakage 譯成資料外洩容易誤導。**

   「**benchmark hacking、資料外洩與設計偏離**」。

   此處是測試資料提前進入方法開發等評測污染，不是資料被傳給外部。

   **修法：**首次就寫「測試資料洩漏進開發流程」，和後文一致。

4. **七、〈資料與方法註記〉：保存狀態寫錯。**

   「**Anthropic 的工程文章與 Agent Memory 的 benchmark 說明……未保存快照**」。

   repo 已有 [agentmemory-longmemeval.md](/Users/kochi.chuang/conductor/workspaces/medium-articles/dodoma/.context/research/aaif-2026-10-24/third-article/agentmemory-longmemeval.md)，media manifest 也記了固定版本及內容雜湊。

   **修法：**把 Anthropic 與 benchmark 分開交代；後者已有保存文字。

5. **七、〈延伸閱讀：本文接回的幾篇〉：有些 recall 只有掛名。**

   「**本文第六節用模型打分的步驟照它的規矩**」。

   〈Eval、單位經濟與規模化〉第二節確實談 judge 三個陷阱，但本文沒有落到哪個分類容易誤判、怎麼校準。

   **修法：**補一個本篇專屬的校準對照：「尚未驗收」不能判成「不相容」；「有更正連結」不能判成「舊結論已退出有效候選」。否則刪掉這項延伸閱讀。

## 建議刪除

1. **四、〈先分清要保存的經驗，以及這一輪要讀的內容〉：刪重複 compaction 導讀。**

   「**第 6、7 頁示範的 compaction 和第二節說的一樣……**」

   第二節已經完成解釋。此處直接進入四種記憶各自不能丟掉的條件。

2. **四、同一 H3：縮短搜尋方法與 benchmark 長段。**

   「**資料配置：LongMemEval-S 的 500 題……**」

   95.2%、86.2%、500 題、約 48 sessions 與 `recall_any@5` 定義能對上來源；但這一段的主要用途只有「找回相關材料，不等於正確使用更正」。保留這個比較與必要分母，RRF 細節移到註記。

3. **四、〈更新與遺忘，要讓下一次檢索真的不同〉：縮掉第二篇的授權重述。**

   「**目前能做哪些操作，仍由工具端核對這次的授權。這是第二篇反覆說的事……**」

   這裡沒有新增機制。留一句「歷史核准只作歷史紀錄，不能成為本次操作權限」，附回第二篇即可。

4. **一、及七、：澀谷照片目前是裝飾。**

   「**相簿裡還有……夜景**」、「**替這趟旅程留下結尾**」及結尾三張連續照片，都沒有改變技術判斷。真正驅動思考的是第 40 頁會場照片與程式核對。

   **修法：**保留一張澀谷照與可證實的日期，其餘移出正文。不要補造旅行感悟；也不必把邀請、午休 Kong demo、東京鐵塔重新搬進本篇。

5. **七、第二段：刪掉再次完整重播報表案例的部分。**

   「**下一個人應能看到版本與健康檢查的結果仍可查……**」

   第五、六節已經講完。結尾留下作者現在會改變哪個採用決定，以及還缺哪份實測證據。

## 建議補充

1. **五、〈讓更正沿引用關係，傳到下一份摘要〉：把長段紀錄變成讀得懂的對照。**

   「**舊判定 J-17……新判定 J-18……衍生摘要 P-9……**」一次塞入太多識別碼。

   **修法：**改成三列表格，分開主張、要求版本、觀察、狀態、取代關係；先修正前述版本矛盾。讀者應一眼看出：觀察保留、錯判撤回、衍生摘要失效。

2. **六、：補一張週一能交出去的驗收卡。**

   「**每個案例交出去的是一筆紀錄……**」目前列了紀錄欄位，仍缺最小任務的固定內容。

   | 欄位 | 應直接填出的內容 |
   |---|---|
   | 任務與對象 | 固定叢集、服務、目標版本及讀取權限 |
   | 原要求 | 包含報表的同一份驗收清單 |
   | 既有觀察 | 版本達標、健康檢查通過；沒有報表結果 |
   | 更正後允許的結論 | 已確認兩項，報表待驗；尚不足以宣稱必要功能全過 |
   | 禁止的結論 | 全部通過、報表已知不相容 |
   | 傳播驗收 | 正常查詢與摘要重建都不能恢復 J-17 |
   | 人工出口 | 誰能暫停採用舊結論、誰核准替代判定、owner 不在時誰接手 |

3. **三、四、五、：各補一個目前尚未完成的第一性原理推論。**

   | 場次與原句 | 缺少的推論 |
   |---|---|
   | 三、〈把時間與適用範圍放進關係裡〉：「**這些加起來超過圖形儲存的建置與維護成本，才值得換**」 | 先說清楚：換圖形儲存不會自動取得目前部署。成本比較必須包含關係更新延遲與人工補查，不能只比較查詢寫法。 |
   | 四、〈反覆出現的說法，還需要新的查核〉：「**沒有追到它們在檢索結果裡的下游影響**」 | 最值得追的是撤回路徑：`auto-forget` 將舊紀錄標為 `isLatest=false`；已保存的 hybrid enrichment 沒有直接檢查這欄。尚不能判定外層是否補了保護，但這正是本篇應提出的具體驗收缺口。 |
   | 五、〈讓更正沿引用關係，傳到下一份摘要〉：「**讓它成為有效判定的是服務負責人**」 | verifier 分離後，瓶頸可能轉到更正核准佇列。區分「暫停採用可疑舊結論」與「正式核准新結論」，並指定有權執行前者的角色。 |

4. **五、及六、：用既有實例深化 recall，並交代實證差距。**

   「**報表工作……在演練期間設為暫停**」和《綠燈不是驗收》測試篇第七節的「replay 從未執行」是同一種驗收缺口。

   **修法：**明確接回那個已記錄的實例，再指出本篇新增的問題：發現漏驗之後，錯誤成功摘要如何退出下一輪依據。記憶傳播仍須標成假設。前系列已有實作輸出，本篇目前只有靜態核對與測試設計；若要求相同的實證深度，至少還缺一份更正前後的儲存、工具回傳、context 與回答對照。

## 術語仍難懂的清單

| 位置與原詞／句 | 問題與具體修法 |
|---|---|
| 二、：「**輸入量用 token 計算**」 | 有定義，缺用途例子。接著比較整份 log 與摘要各占輸入空間；不要硬換算固定中文字數。 |
| 二、：「**context rot**」 | 只有抽象表現下降。先舉「報表未驗收明明還在輸入裡，回答卻漏用了它」，再命名。 |
| 三、開場：「**Markdown 檔**」 | 補成像 README 的純文字筆記，避免讀者先猜格式。 |
| 三、〈相似性把材料找出來，關係把問題接起來〉：「**GraphRAG**」 | 基本例子已有；仍要交代這是取回資料的方法，並不等於一定要購買圖形資料庫。 |
| 四、〈先分清要保存的經驗，以及這一輪要讀的內容〉：「**working／episodic／semantic／procedural memory**」 | 各有例子，但一段四種太密。改成四列，增加「何時更新、誰確認」欄。 |
| 四、同一 H3：「**BM25**」 | 名稱與錯誤字串仍太泛。用一則實際形式的外掛名稱／錯誤訊息示意字詞比對，再引名稱。 |
| 四、同一 H3：「**RRF**」 | 例子塞在多個新詞之間。獨立成一句「兩份排行榜怎麼合併」；說明它合併相關性排序，不裁決有效性。 |
| 四、〈反覆出現的說法，還需要新的查核〉：「**semantic 集合……memories 集合……observations**」 | 容易和前面的四種記憶分類混淆。就地說明這是該專案三個不同儲存集合。 |
| 四、同一 H3：「**confidence**」 | 已說是模型自報；再明確指出不是正確機率，也不是人工查核結果。 |
| 五、〈在結果出現前，先決定怎樣才算有支持〉：「**oracle 判定通過**」 | 混合標準與執行者。改成「依哪版要求，由哪版驗收器判定通過」。 |
| 五、〈讓更正沿引用關係，傳到下一份摘要〉：「**衍生摘要 P-9**」 | 先說「升級計畫抄用了 J-17 的結論」，再命名為衍生摘要。 |
| 六、：「**記憶快照、索引版本**」 | 用「每輪都還原到同一份測試起始資料，連搜尋目錄也一起還原」帶入。 |
| 六、：「**保留題、校準評分器的資料、證據材料**」 | 用同一案例分別指出：未拿來調整系統的題目、人工已判好的回答、agent 可查的部署與演練紀錄。 |
| 六、：「**pilot／trial**」 | 名稱前已有說明，但還缺具體邊界。各補工作範圍、停止條件與負責人，不只換英文名稱。 |

`agent`、`context`、`compaction`、向量搜尋、RAG、verifier 與索引已有情境引入，不必再加一輪定義。gateway、proxy、digest、A2A、sandbox、commit point、optimistic locking 沒有用於本篇正文推論，無須為了術語完整性補進來。

<!-- tokens: in 2076417 out 20430 -->
