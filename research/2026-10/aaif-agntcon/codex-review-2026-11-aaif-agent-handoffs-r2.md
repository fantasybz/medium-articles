# Codex review — 2026-11-aaif-agent-handoffs/article.md

> model: gpt-6.1-sol, reasoning: xhigh, 2026-10-25 23:39. 原話照錄，未經摘要。第 2 輪；審的是 2026-10-25 改寫並依前一輪意見修訂後的版本。

我會先讀 STYLE.md 與 style brief，再逐段對照簡報、原始材料和被引用的舊文。全程只讀，不修改檔案。
<!-- codex ran: /bin/zsh -lc 'cat STYLE.md research/2026-10/style_brief.md' -->
<!-- codex ran: /bin/zsh -lc "rg --files --hidden -g '"'!**/.git/**'"' -g '"'!agents/**'"' -g '"'!.claude/**'"' .context/research/aaif-2026-10-23 .context/research/aaif-2026-10 -->
<!-- codex ran: /bin/zsh -lc "rg --files --hidden .context/research/aaif-2026-10-23/slides/text .context/research/aaif-2026-10-25 | rg '(2RCwp|2QlDX|2QlD9|2QlE7|2QlEe|2QlEG|han -->
<!-- codex ran: /bin/zsh -lc 'nl -ba 2026-11-aaif-agent-handoffs/article.md' -->
<!-- codex ran: /bin/zsh -lc "rg -n '"'^#{1,3} |SEC-2291|G2|worktree|義務表|核准疲勞|預先核准|付款|同一行程|版本|gateway|identity broker|secret broker'"' 2026-10-green-*/article.md 2026-09-agenti -->
<!-- codex ran: /bin/zsh -lc 'cat .context/research/aaif-2026-10-23/slides/text/2RCwp-01-agntcon-mcpcon-japan2026-softbank-corp.txt .context/research/aaif-2026-10-23/slides/tex -->
目前最需要核對的是第九節的驗收契約：它把排空、升級與恢復合成一步，卻用「排空次數一次」判斷是否重複造成效果。我會確認這個判準的依據，也查前文的核准範圍與舊文回扣是否一致。
<!-- codex ran: /bin/zsh -lc "python3 -c 'from pathlib import Path
for stem in [\"2QlDX\",\"2QlD9\"]:
 p=next(Path(\".context/research/aaif-2026-10-23/slides/text\").glob(stem+ -->
<!-- codex ran: /bin/zsh -lc "python3 -c 'from pathlib import Path
specs=[(\"2QlDX\",range(38,56)),(\"2QlEe\",range(1,26)),(\"2QlEG\",range(1,29))]
for stem,pages in specs:
 p= -->
<!-- codex ran: /bin/zsh -lc "python3 -c 'from pathlib import Path
p=next(Path(\".context/research/aaif-2026-10-23/slides/text\").glob(\"2QlEe-01-*.txt\")); parts=p.read_text() -->
<!-- codex ran: /bin/zsh -lc 'cat .context/research/aaif-2026-10-23/facebook-post-provenance.json' -->
<!-- codex ran: /bin/zsh -lc "rg -n -A 30 -B 8 'decentralized|handoff|manager pattern|one-way|conversation' .context/research/aaif-2026-10-25/openai-guide/guide.txt" -->
<!-- codex ran: /bin/zsh -lc "rg -n '"'^##|''^###'"' 2026-10-green-*/article.md 2026-09-agentic-engineering-platform/article.md 2026-10-agentic-harness-blueprint/article.md 202 -->
<!-- codex ran: /bin/zsh -lc "rg --files --hidden .context research -g '"'!**/agents/**'"' -g '"'!**/.agents/**'"' -g '"'!**/.claude/**'"' -g '"'!**/.git/**'"' | rg '(handoffs\ -->
<!-- codex ran: /bin/zsh -lc "rg -n -l --hidden -g '*.txt' -g '*.json' -g '*.md' -g '*.html' -g '"'!**/agents/**'"' -g '"'!**/.agents/**'"' -g '"'!**/.claude/**'"' -g '"'!**/co -->
<!-- codex ran: /bin/zsh -lc "sed -n '103,155p' 2026-10-green-review/article.md" -->
<!-- codex ran: /bin/zsh -lc "sed -n '27,72p' 2026-09-agentic-org-design/article.md" -->
<!-- codex ran: /bin/zsh -lc "sed -n '453,535p' 2026-10-green-review/article.md" -->
<!-- codex ran: /bin/zsh -lc "sed -n '121,156p' 2026-10-agentic-harness-blueprint/article.md" -->
<!-- codex ran: /bin/zsh -lc "sed -n '493,517p' 2026-11-same-spec-contract/article.md" -->
<!-- codex ran: /bin/zsh -lc "sed -n '216,249p' 2026-10-agentic-harness-blueprint/article.md" -->
<!-- codex ran: /bin/zsh -lc "sed -n '425,475p' 2026-10-green-testing/article.md" -->
<!-- codex ran: /bin/zsh -lc "sed -n '160,227p' 2026-10-green-review/article.md" -->
<!-- codex ran: /bin/zsh -lc "sed -n '503,585p' 2026-10-green-testing/article.md" -->
<!-- codex ran: /bin/zsh -lc "sed -n '307,335p' 2026-10-green-overview/article.md; sed -n '384,430p' 2026-10-green-reliability/article.md" -->
<!-- codex ran: /bin/zsh -lc "sed -n '377,423p' 2026-10-green-payment/article.md; sed -n '209,227p' 2026-11-agentic-eval-economics/article.md; sed -n '59,69p' 2026-09-agentic-e -->
舊文回扣有一個實質問題：《付款實作篇》第九節已經推導過重啟後的未知結果、provider 查詢契約與識別碼保存期限。本篇把它概括成「同一行程裡依序重送」，縮小了舊文內容；應把新增貢獻放在接手權轉移，以及 Kubernetes 複合操作的復原契約。
<!-- codex ran: /bin/zsh -lc 'cat .context/research/aaif-2026-10-23/title-opening-refinement/facebook-tokyo-office.json .context/research/aaif-2026-10-23/title-opening-refineme -->
<!-- codex ran: /bin/zsh -lc "rg -n -A 12 -B 8 'idempotent|re-run|minor version|Skipping|drain|uncordon' .context/research/aaif-2026-10-23/sources/kubeadm-upgrade.txt .context/ -->
<!-- codex ran: /bin/zsh -lc "rg -n 'create.*pull|pull.*request|429|限流|預算|模擬|建立 PR' 2026-11-aaif-after-tokyo/article.md .context/research/aaif-2026-10-23/kong-demo-source/mock- -->
<!-- codex ran: /bin/zsh -lc "rg --files --hidden .context/research/aaif-2026-10-25 .context/research/aaif-2026-10-23 -g '"'!**/.agents/**'"' -g '"'!**/agents/**'"' -g '"'!**/. -->
<!-- codex ran: /bin/zsh -lc 'cat .context/research/aaif-2026-10-23/title-opening-refinement/facebook-tokyo-office.json .context/research/aaif-2026-10-23/title-opening-refineme -->
<!-- codex ran: /bin/zsh -lc "rg --files --hidden .context/research -g '"'!**/.agents/**'"' -g '"'!**/agents/**'"' -g '"'!**/.claude/**'"' -g '"'!**/site-packages/**'"' -g '*ha -->
<!-- codex ran: /bin/zsh -lc "rg --files --hidden -g '"'!**/.git/**'"' -g '"'!**/.agents/**'"' -g '"'!**/.claude/**'"' -g '"'!**/agents/**'"' -g '"'!**/site-packages/**'"' -g ' -->
<!-- codex ran: /bin/zsh -lc "python3 -c 'from pathlib import Path
p=next(Path(\".context/research/aaif-2026-10-23/slides/text\").glob(\"2RCwp-*.txt\"));parts=p.read_text().spl -->
<!-- codex ran: /bin/zsh -lc "python3 -c 'from pathlib import Path
for name,terms in [(\"kubeadm-upgrade.txt\",[\"idempotent\",\"Skipping MINOR\",\"Skipping minor\",\"Recoverin -->
<!-- codex ran: /bin/zsh -lc "rg -n 'handoffs/|on_handoff|transfer_to_refund_agent|Effective context engineering|independent.*context|isolated.*context' research/2026-10/aaif-a -->
<!-- codex ran: /bin/zsh -lc "sed -n '340,388p' 2026-10-green-overview/article.md; sed -n '110,152p' 2026-11-aaif-agent-handoffs/article.md; sed -n '1,18p' 2026-11-aaif-agent-h -->
<!-- codex ran: /bin/zsh -lc "sed -n '1,60p' .context/research/aaif-2026-10-25/channel/aaif-videos.json; sed -n '244,302p' .context/research/aaif-2026-10-23/kong-demo-source/mo -->
<!-- codex ran: /bin/zsh -lc "python3 -c 'import json
from pathlib import Path
p=Path(\".context/research/aaif-2026-10-25/channel/aaif-videos.json\");d=json.loads(p.read_text() -->
<!-- codex ran: /bin/zsh -lc "rg -n -l --hidden -g '*.json' -g '*.txt' -g '*.md' -g '"'!**/.agents/**'"' -g '"'!**/agents/**'"' -g '"'!**/.claude/**'"' -g '"'!**/refinement-3-r -->
<!-- codex ran: /bin/zsh -lc "python3 -c 'import json
from pathlib import Path
for fn in [\"aaif-videos.json\",\"recent28.json\"]:
 d=json.loads(Path(\".context/research/aaif-2 -->
六場簡報的主要頁碼、版本與失敗案例，目前未見明顯捏造。較大的缺口是：多數段落在談一般授權與儲存設計，直到第七節才碰到交接特有的「前任恢復後，誰還能行動」。第九節也只測送出前與全部完成後，漏掉排空已完成、升級尚未完成的中間狀態。
<!-- codex ran: /bin/zsh -lc "sed -n '1,16p' 2026-11-same-spec-contract/publish/PUBLISHED.md; sed -n '1,13p' 2026-11-aaif-agent-handoffs/publish/en/PUBLISHED.md" -->
<!-- codex ran: /bin/zsh -lc "sed -n '244,300p' .context/research/aaif-2026-10-23/kong-demo-source/mock-api/main.py; rg -n '"'^###|文字 token|''^##|核准|同一行程'"' 2026-11-aaif-agent- -->
<!-- codex ran: /bin/zsh -lc "python3 -c 'from pathlib import Path
p=next(Path(\".context/research/aaif-2026-10-23/slides/text\").glob(\"2QlEG-*.txt\"));ps=p.read_text().split( -->
<!-- codex ran: /bin/zsh -lc "rg -n -i -A 4 -B 3 '2026|8/20|8 / 20|Aug|20' .context/research/aaif-2026-10-23/slides/text/2QlEG-01-20260910-agntcon-japan-hitachi-ito-sato-public -->
<!-- codex ran: /bin/zsh -lc "python3 -c 'from pathlib import Path
p=next(Path(\".context/research/aaif-2026-10-23/slides/text\").glob(\"2QlEG-*.txt\")); ps=p.read_text().split -->
<!-- codex ran: /bin/zsh -lc "rg -n '08|20' .context/research/aaif-2026-10-23/slides/text/2QlEG-01-20260910-agntcon-japan-hitachi-ito-sato-public.txt | head -n 30" -->
另一個明確落差在「沿用義務表的格式」：《契約篇》第九節有要求來源、可觀察義務、允許的自由、可辨識錯法與仍未證明等欄位；本篇只留下情境、行為與查核三欄。這使驗收表省略了自己最需要交代的判準來源與證明邊界。
判定：尚未達到這次修訂的驗收標準。主問題有寫出來，但交接特有的「執行責任如何轉移」出現太晚；第九節的驗收判準則有誤，且漏掉最需要復原的中間狀態。

以下依 repository 內材料核對。六場簡報的主要數字、引文與頁碼未見明顯捏造；問題主要在適用範圍、推論與舊文回扣。本文沒有 timecode；References 3、5 的完整原文快照，本輪未找到，不能宣稱已獨立核實。

## 致命問題

1. **九、〈如果現在由我驗收，會從一次中斷的交接開始〉：把呼叫次數當成外部效果，驗收會判錯。**

   > 「正常效果是節點到 1.31、工作負載只被移動一次。」
   >
   > 「例如每台節點的排空次數是不是一次」

   第二次 `drain` 不必然造成第二次搬移：節點可能仍是空的；一次排空也可能涉及多個 Pod 與後續重新排程。「排空次數」不能直接代表工作負載受到幾次干擾。

   repository 保存的 Kubernetes 文件只說 **`kubeadm upgrade` 可重跑**，沒有替「排空 → 套件更新 → 升級 → 恢復排程」整段流程提供相同保證。

   **修法：**明列每個子步驟的重送契約。驗收觀察「是否新增未獲准的 eviction／維護動作、是否超出允許的服務中斷」，並核對操作識別與節點狀態。若測試刻意要求恰好一次排空，必須標成這個固定測試環境的約定，不能寫成 Kubernetes 的普遍正確性。

2. **五、〈修復之後，重新確認評估與核准〉：新增 worker 的授權分類自相矛盾。**

   > 「例如多了一台同角色的 worker，重跑評估，核准的目標與步驟不變」
   >
   > 「核准時的節點清單與目前的節點清單對不上，就不能宣布完成。」

   新 worker 若也要升級，操作對象已增加；若不升級，又不能依後一句宣布整個叢集完成。「同角色」不足以推出「仍在原核准範圍」。

   **修法：**選定一種契約並貫穿全文：

   - 核准固定的節點識別清單；新增節點須修訂範圍。
   - 核准符合明確條件的動態集合，另外限定角色、數量、容量與維護限制；新增節點須證明符合條件。

   不能一面要求核准綁定目標，一面用「同角色」默認擴張目標。

3. **九、〈如果現在由我驗收，會從一次中斷的交接開始〉：只測操作前、全部完成後，漏掉複合操作執行一半。**

   > 「接著讓這個操作在目標系統完成，卻不把結果交回 agent，就中斷它的工作環境。」

   真正困難的是：排空完成、升級失敗、節點仍不能接受工作；此時維護時段又結束。文章目前的「停止相依步驟」沒有回答該節點由誰恢復、哪些善後仍獲授權。

   **修法：**至少完整走一次「排空完成、版本尚未達標」的復原推導，列出可查證狀態、允許的補救、核准失效後的處置與接案人。再加入**執行服務自身重啟**：只中斷 agent，驗不到服務遺失操作紀錄後是否重複造成效果。

## 重要問題

1. **TL;DR／二、〈交接時，到底交出了什麼？〉／七、〈檔案各自正確，合起來仍可能違反任務要求〉：真正屬於交接的問題到第七節才出場。**

   > 「前任已經不在場」
   >
   > 「A 只是斷線、稍後恢復，B 已經接手……誰還能送出下一步？」

   前六節大部分即使只有一個 agent，也照樣成立：最小權限、操作紀錄、驗收、持久性。第七節才提出「交接是否真的移轉執行責任」，但第二節閱讀地圖沒有它。

   **修法：**核心問題改為：「前任可能中斷，也可能恢復；下一位憑什麼取得接手權，並決定繼續、重做或停止？」把「目前誰能新增操作」放進第二節授權列，第九節再測接手權移轉與舊請求晚到的競態。

2. **二、〈交接時，到底交出了什麼？〉：三種類型混用不同分類軸。**

   > 「第一種是同一個執行流程裡換一個 agent」
   >
   > 「第二種是把一段工作委派給另一個服務」
   >
   > 「第三種是中斷後重新接手」

   「誰保留流程控制權」「是否跨服務」「是否經過中斷」不是互斥類別。跨服務可以採 manager pattern，也可以移交控制權；兩者都可能重啟。

   **修法：**稱為三種「情境」，明說可以重疊。OpenAI 的 manager／decentralized 分類只用來解釋控制權，不要讓讀者以為它對應本機／遠端。

3. **一、〈會議之前，先去看一眼東京鐵塔〉：把作者整理出的問題寫成六場共同的原始企圖。**

   > 「我發現它們都在追問同一件事」

   Studist 主要處理 permission 與 intent 的落差；Juicedata 處理 workspace 的保存契約；Hitachi 處理 OSS 整合缺口。它們並非都以接手者決策為研究問題。

   **修法：**改成「我用這六份材料回答同一個交接問題」。每場先交代講者原本的限制，再說作者借它推導什麼；不能讓統一敘事覆蓋來源本身。

4. **一、〈會議之前，先去看一眼東京鐵塔〉／十、〈結語：留下來的工作，要讓下一個人敢接〉：Kong 的證據層次被悄悄升級。**

   > 「工程師代理已經完成建立 PR 的模擬操作，下一次模型請求卻被限流擋下」

   第一篇寫的是「保存版操作手冊描述了一條……路徑」；本篇改成無條件的既成事件。Facebook 貼文能支持作者午休架設與操作，不能單獨證明這個特定請求序列。

   **修法：**保留「操作手冊描述的情境」。結尾要求「仍有效的核准範圍」時，也要說明這是可復原系統**還需增加的能力**；Kong demo 的角色群組權限不是任務核准紀錄。

5. **四、〈把帳號能力縮成這次任務的操作範圍〉：`safe-gh` 的條件被省略，也還沒證明任務綁定。**

   > 「`safe-gh` 只允許對白名單組織的讀取與對自己建立的 issue 寫入」

   Studist 第 39 頁的寫入範例還有組織、`authors: ["@me"]` 與 `aiAnnotation: "true"`。共用使用者帳號時，「自己建立」尤其不能直接等同「agent 建立」。

   更根本的問題是：**AI 建立的 issue，也可能與目前任務無關。**

   **修法：**準確交代範例條件，再補一句：這先縮小可操作集合；要限制到「這次任務」，仍須另外核對 issue 與任務的關聯。

6. **八、〈讓 task、run 與 tool call 對回同一份授權〉：RACI 回扣省略了 domain tool 的責任。**

   > 「平台負責操作識別、查詢介面與執行協調」

   [組織篇第二節](/Users/kochi.chuang/conductor/workspaces/medium-articles/dodoma/2026-09-agentic-org-design/article.md:57)明列 Domain MCP tools 由 domain team 承擔 R／A。本篇把共用設施與業務操作介面一起交給平台，容易改掉原分工。

   **修法：**平台維護共用識別與協調機制；domain team 負責具體操作的語意、狀態查詢與補救契約。另指定誰對未知結果最終負責，不能只列一串參與角色。

7. **九、〈如果現在由我驗收，會從一次中斷的交接開始〉：縮小舊文，製造本篇的新意。**

   > 「那篇處理的是同一行程裡依序重送」

   這句準確描述付款範例的**實作範圍**，卻不準確描述整篇內容。[付款實作篇第九節](/Users/kochi.chuang/conductor/workspaces/medium-articles/dodoma/2026-10-green-payment/article.md:392)已經推導重啟、外部扣款與本地紀錄的落差、provider 查詢／重試契約、保存期限與人工接手。

   **修法：**寫成「付款範例只實作同一行程；那篇已列出跨重啟的待驗證問題。本篇把它具體化成接手權移轉與多階段基礎設施操作」。刪掉重述既有復原原理的篇幅。

8. **九、〈如果現在由我驗收，會從一次中斷的交接開始〉及〈延伸閱讀〉：並沒有沿用義務表格式。**

   > 「這裡直接把交接的那張填出來」
   >
   > 「本文第九節的交接驗收表沿用它的格式。」

   [契約篇第九節](/Users/kochi.chuang/conductor/workspaces/medium-articles/dodoma/2026-11-same-spec-contract/article.md:493)保留要求來源、可觀察義務、允許的自由、已知錯法與仍未證明。本篇只有情境、行為、查核三欄，正好刪掉辨認錯誤判準所需的欄位。

   **修法：**實際補回來源與版本、仍未證明、不能判定的出口及 owner。否則改稱「沿用逐項交代驗收依據的想法」。

9. **段落轉場：以下位置只有換題提示，沒有承接前一段的結果。**

   | 位置與原句 | 具體修法 |
   |---|---|
   | 一：「晚上，我又貼了一張亮起燈光的鐵塔」 | 只有時間推進，沒有思考推進；併入照片說明。 |
   | 四、〈把帳號能力縮成這次任務的操作範圍〉：「另外三個例子同樣日常」 | 沒有深化 CI 案例，只增加新系統；移至註記。 |
   | 五、〈從全部節點到服務結果，逐層驗收〉：「工具本身也會改變結果」 | 補問：「知道剩下哪些節點後，接手者能否用現有工具接續原計畫？」再帶入工具版本。 |
   | 七、〈版本檢查保住修改，也保留處理衝突的機會〉：「簡報也用租戶與短期的任務 token 限制存取」 | 從上傳完成訊號突然跳授權；移到第六節憑證恢復，回答重新掛載時取得什麼權限。 |
   | 同一 H3：「簡報還介紹了用 copy-on-write 建立的『層』」 | 先提出共享修改容易衝突，是否能先隔離探索；再說分支如何處理這個問題。 |

## 次要問題

1. **七、〈版本檢查保住修改，也保留處理衝突的機會〉：指到不存在的說明。**

   > 「和第二節談的文字 token 是不同的東西」

   第二節沒有解釋文字 token；那在第一篇。刪掉跨篇指涉，直接說這裡是存取憑證。

2. **四、〈把帳號能力縮成這次任務的操作範圍〉：CI 權限被寫成無限。**

   > 「讓 CI 用它的權限做任何事」

   改成「執行 CI 帳號與可取得 secrets 所允許的操作」。Studist 第 24 頁也有這個權限前提。

3. **五、〈評估認為可行，執行仍要核准〉：webhook 解釋過度概括。**

   > 「叢集每次建立新的工作單位時，會先呼叫一個外部的檢查服務」

   改成「若建立請求符合已設定的 admission webhook 規則，API server 會先呼叫該服務」。否則讀者會以為所有建立操作必經同一個外部檢查。

4. **四、〈用允許與越界請求，檢查限制是否生效〉：二手引用仍被寫成研究結論。**

   > 「引用了一項研究，說人對 agent 的核准會隨次數增加而鬆懈」

   第 16 頁列出疲勞／習慣風險並引用論文；Review 篇也明說未讀原文。改成「簡報引用該研究，提醒反覆核准的疲勞風險」，不要超出目前查核層級。

5. **十、〈結語：留下來的工作，要讓下一個人敢接〉：結尾推翻前面的資料需求。**

   > 「它需要的不是前任的對話，而是……」

   前文承認對話有助於恢復脈絡。改成「對話之外，還需要……」，避免把論旨從「對話不足以證明」改成「對話沒有用途」。

6. **〈References〉：來源版本仍不夠可重查。**

   > 「以文件當時版本為準」
   >
   > 「第 3、9–13、18–24 頁」

   References 3 應記 SDK／文件版本及取得日期；References 5 應保留實際引用段落快照。PingCAP「harness 與資料分離」在第 25 頁，現有頁碼範圍漏列；Hitachi 的 8 月 20 日標記在第 10 頁，也應補列。

## 建議刪除

以下段落沒有新增證據或推論，或把主線帶離交接：

| 位置與原句 | 處理 |
|---|---|
| 一：「窗外的紅白塔身很清楚，背後是一大片灰雲。」及「晚上，我又貼了一張……」 | 兩則貼文與日期有來源，但目前是裝飾。保留一張主圖、短圖說，提早進入 Kong 問題。 |
| 二：「handoff 是否啟用的檢查發生在模型填入參數之前」 | SDK 實作細節放註腳；此處先讓讀者理解控制權與資料如何交出。 |
| 三、〈通訊許可要與行動授權分開核對〉：「這和 Review 篇第六節那個 PR 裡假的『SEC-2291』是同一種風險」 | 第二節已引用同一節；第三節只留下相對於舊文新增的授權核對位置。 |
| 四、〈把帳號能力縮成這次任務的操作範圍〉：「另外三個例子同樣日常」 | 刪去連續展開 issue、Terraform、網頁的長串說明；深入 CI 一例即可。 |
| 四、〈用允許與越界請求，檢查限制是否生效〉：「簡報第 16 頁引用了一項研究」 | 與 Review 篇重複，也打斷越界測試到過期評估的交接；移來源註記。 |
| 七、〈版本檢查保住修改，也保留處理衝突的機會〉：「目的相近；drive9 的層把這種隔離搬進了儲存層」 | worktree 回扣目前只有相似性。若無新的判斷，刪掉；不能把相似用途當成語意等價。 |
| 七、〈記憶幫忙找回脈絡，核准仍須回查〉：「記憶只能幫忙找到核准的來源」 | 重複第二、六節。壓成第三篇入口，不再完整重述核准失效的例子。 |
| 八、〈讓 task、run 與 tool call 對回同一份授權〉：「沿著同一次委派，接手者使用的權限應維持在原本範圍內」 | 第三、四節已完成這個論證；改用篇幅處理接手權轉移。 |
| 十：「六份材料共同改變的是我理解交接的方式」「因此，一份好的交接可以明確停在尚未完成」「兩篇最後都回到同一個採用條件」 | 三段重述 TL;DR 與第九節。保留查核成本及同事如何接案，縮短系列自我總結。 |
| 七：「本文沒有用它們完成故障重現或效能量測」等重複方法聲明 | 集中到〈資料與方法註記〉；正文保留會直接改變判讀的限制。 |

## 建議補充

1. **三至八節：每場補上會改變設計選擇的條件與代價。**

   | 場次、H3 與原句 | 缺少的推論與具體補法 |
   |---|---|
   | 三、〈語意檢查還要決定等待、拒絕與接手的時機〉：「不能交由模型自己決定多大風險可以接受」 | 填一條實際處置：語意判斷逾時時，不接受新的排空；已被執行服務接受的操作繼續追蹤。說清楚代價是等待與人工介入，誰承擔這個成本。 |
   | 四、〈把帳號能力縮成這次任務的操作範圍〉：「動到 `.github/` 這類 CI 定義時拒絕」 | 補反例：修改 CI 會載入、但位於其他路徑的 script，仍可能改變 CI 行為。路徑檢查保護的是已列出的範圍；完整效果需要沿依賴路徑檢查，代價是維護成本與誤擋。 |
   | 五、〈修復之後，重新確認評估與核准〉：「核准之後環境還會變」 | 列出哪些觀察欄位一變就使評估失效，以及誰在下一個操作前核對。否則「重新查授權」仍可能搭配過期的環境評估。 |
   | 六、〈先定義保存承諾，再選擇故障注入的位置〉：「已送出的操作識別卻不能遺失」 | 推到底：識別尚未達保存承諾前，就不能送出不可安全重送的操作。持久層不可用時會犧牲可用性；這是設計成本，不只是儲存設定。 |
   | 七、〈檔案各自正確，合起來仍可能違反任務要求〉：「協調或序列化有副作用的步驟」 | 說清楚協調範圍：同一節點、整個叢集，還是共用容量限制？全域序列化最簡單，卻可能不必要地降低吞吐量；範圍過小則保不住任務條件。 |
   | 八、〈共同元件仍需接上業務條件的檢查〉：「選型因此要包含『誰實作這段檢查』」 | 再問一層：既然下單條件已知，為何仍由模型決定能否下單？把必要條件放在訂購服務的確定性狀態轉移，agent 處理資料蒐集與例外。代價是業務規則必須有人維護。 |

2. **七、〈檔案各自正確，合起來仍可能違反任務要求〉：讓「目前接手者」成為可拒絕舊請求的契約。**

   > 「執行服務必須知道目前的接手者是誰」

   補一個例子：B 接手後取得新的接手版本；A 恢復時，即使舊憑證尚未到期，新增步驟也因接手版本過期而被拒絕。接手版本的更新與請求接受必須有一致的先後順序；另測 A 的舊請求延遲抵達。只檢查姓名或帳號不足以處理競態。

3. **九、〈如果現在由我驗收，會從一次中斷的交接開始〉：實際填一份交接紀錄。**

   > 「新的 agent 只拿到已保存的輸入、計畫、工作檔與操作識別」

   至少填出：任務與目標識別、計畫版本、核准來源及失效條件、目前接手版本、操作與子步驟識別、已確認效果、未知結果、查詢入口、允許的下一步、接案人與期限。每個欄位注明誰可寫入、誰提供權威查詢。否則讀者仍須自己把全文翻譯成介面。

4. **九、驗收表：補上停止之後的營運成本。**

   > 「這個停止同樣可以是通過驗收的結果」

   補問：未知結果能留多久？由誰接案？若持續無法查詢，怎麼避免工作永久擱置？VP 需要看到待確認案件數、等待時間與人工查核工時；安全停止本身不等於團隊負擔可接受。

5. **九、結構：拆成三個 H3，讓讀者找得到星期一的工作。**

   現在整節混合契約、故障注入、付款 recall、授權失效與採用決策。可拆成「先定義操作與證據契約」「中斷後如何判斷下一步」「哪些結果支持開放操作」，每段只處理對應決策。

6. **一及十：用已有的午休 demo 紀錄承擔敘事。**

   > 「第一篇那個 Kong 展示留下的問題」

   把 Facebook 當時的判斷「governance 跟 agent logic 分離」接到返台後的修正：分離治理仍沒有回答工作如何接續。這是已有材料支持的思考進展。東京鐵塔照片目前只證明旅程，沒有推動論證；不要替它補造技術頓悟。

## 術語仍難懂的清單

| 位置與原句 | 問題及具體修法 |
|---|---|
| 二：「input filter」「交接的回呼」 | 沒有情境。先說「接手者只看退款相關紀錄」「交棒前由程式核對訂單」，再引入名稱；API 細節移註腳。 |
| 二：「decentralized pattern」「manager pattern」 | 同段塞入跨服務與控制權。先用「轉接後由退款窗口繼續對客」及「主管派人查資料、結果回主管」分清。 |
| 二：「在獨立的 context 裡工作」 | context 尚未建立意思。先說子 agent 只收到自己的任務包，看不到主管全部對話。 |
| 三：「Agent Firewall」「語意檢查」「確定性規則」 | 前者有後置說明；後兩者仍抽象。用同一請求對照：目標是否在清單可直接比對，文字是否夾帶改變任務的指令才涉及意思判讀。 |
| 四、〈強制檢查要放在 agent 無法繞過的位置〉：「reference」「gateway」「sandbox」「secret broker」 | 一段堆四個新元件，sandbox 到第六節才解釋。先走一次「agent 交出節點操作請求，工具端取得金鑰後執行」，只留下理解該路徑所需的名稱。 |
| 五：「被移除的 API」「供應商支援矩陣」 | 尚未有升級失敗的小例子。先說舊部署格式在新版不再接受、某版外掛尚不支援目標版本。 |
| 五：「controller」「webhook」 | 解釋晚於首次使用，且一次介紹兩種機制。第一次列出相容性風險時就用一個會阻擋建立 Pod 的例子帶入。 |
| 六：「commit point」「`fsync`」「RPO／RTO」 | 遊戲存檔類比仍缺可驗收數值的意思。用「已回覆保存成功的修改能否遺失」「多久能重新掛載並讀到它」區分，再說名稱。 |
| 七：「無狀態的 harness」 | 用另一個未解釋詞定義元件。先說「重建後不需要找回本機使用者資料的執行程式」，再帶出 harness。 |
| 七：「copy-on-write」「git worktree」 | 名稱先出場，且兩者關係只說相似。先描述共用起點、各自修改的例子，再界定只隔離哪些檔案效果。 |
| 八：「AGNTCY」「OASF」「SLIM」「Observe」 | 四個品牌／縮寫同時出現，記憶負擔高。正文先保留尋找服務、描述能力、傳訊與觀測四種責任，名稱放比較表。 |
| 八：「token exchange」「JWT」「OAuth 2.0」「OpenTelemetry」 | 門票類比沒有完整分清身分、委派、存取與任務核准。沿同一張採購委託逐步說明，各名稱只承接一件事。 |
| 八：「task、run、tool call」「RACI」 | 定義晚於第 24 頁分析與 H3；RACI 只有舊文入口。首次使用就以一張採購委託、一次處理、一次下單對照；責任直接寫人與交付物。 |

`permission／intent`、`gate`、`optimistic locking`、冪等性已有可理解的例子；需要修的是適用邊界。`digest`、`compaction`、`RRF`、`oracle`、`holdout` 沒有出現在本篇正文，不應為了補術語再加入。

<!-- tokens: in 3589956 out 20187 -->
