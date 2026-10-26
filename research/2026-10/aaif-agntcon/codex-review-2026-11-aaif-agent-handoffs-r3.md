# Codex review — 2026-11-aaif-agent-handoffs/article.md

> model: gpt-6.1-sol, reasoning: xhigh, 2026-10-26 00:13. 原話照錄，未經摘要。第 3 輪；審的是 2026-10-25 改寫並依前一輪意見修訂後的版本。

我會先讀 STYLE.md 與 style brief，再逐節核對原始材料和舊文引用；全程只讀取 repository 內的檔案，不做修改。
<!-- codex ran: /bin/zsh -lc 'cat STYLE.md research/2026-10/style_brief.md' -->
<!-- codex ran: /bin/zsh -lc "rg --files -g 'article.md' -g 'AGENTS.md' -g '"'!agents/**'"' -g '"'!.claude/**'"' 2026-10-green-* 2026-09-agentic-engineering-platform 2026-09-ag -->
<!-- codex ran: /bin/zsh -lc 'cat research/2026-10/style_brief.md' -->
<!-- codex ran: /bin/zsh -lc "rg --files --hidden -g '"'!agents/**'"' -g '"'!.git/**'"' -g '"'!.claude/**'"' .context/research/aaif-2026-10-23 .context/research/aaif-2026-10-25 -->
<!-- codex ran: /bin/zsh -lc "rg --files --hidden .context/research/aaif-2026-10-23/slides/text .context/research/aaif-2026-10-23/kong-demo-source | rg '2RCwp|2QlDX|2QlD9|2QlE7 -->
<!-- codex ran: /bin/zsh -lc "rg -n '"'^##|''^###|第六節|第九節|權威|預先核准|疲勞|Quartic|worker|G2|RACI|idempoten|provider|harness|egress'"' 2026-10-green-*/article.md 2026-09-agentic-*/ar -->
<!-- codex ran: /bin/zsh -lc "rg --files --hidden .context/research/aaif-2026-10-23 | rg 'transcript.txt"'$|facebook-post-provenance|handoff|anthropic|openai|kubernetes|sdk'"'  -->
<!-- codex ran: /bin/zsh -lc 'cat .context/research/aaif-2026-10-23/facebook-post-provenance.json' -->
<!-- codex ran: /bin/zsh -lc "cat '.context/research/aaif-2026-10-23/slides/text/2RCwp-01-agntcon-mcpcon-japan2026-softbank-corp.txt'" -->
<!-- codex ran: /bin/zsh -lc "cat '.context/research/aaif-2026-10-23/slides/text/2QlDX-01-intent-as-code-13.txt'" -->
目前看到兩個要往下追的問題：主軸承諾回答「誰取得接手權」，但接手權的設計到第七節才出現；第九節則把升級失敗後「恢復節點」列為補救選項，還需要交代什麼狀態下能安全這樣做。接著會核對投影片，分清哪些是講者的設計、哪些是作者新增的要求。
<!-- codex ran: /bin/zsh -lc "python -c 'from pathlib import Path; root=Path(\".context/research/aaif-2026-10-23/slides/text\"); targets=[(\"2RCwp*\",[17,18,19]),(\"2QlDX*\",[1 -->
<!-- codex ran: /bin/zsh -lc "python3 -c 'from pathlib import Path; root=Path(\".context/research/aaif-2026-10-23/slides/text\"); targets=[(\"2RCwp*\",[17,18,19]),(\"2QlDX*\",[ -->
<!-- codex ran: /bin/zsh -lc 'cat .context/research/aaif-2026-10-23/slides/text/2QlD9-01-agntcon-mcpcon-japan-2026-abhijeet-sanskar-final.txt' -->
<!-- codex ran: /bin/zsh -lc 'cat .context/research/aaif-2026-10-23/slides/text/2QlE7-01-stateful-sandboxes-for-stateless-agents-designed-r3.txt' -->
<!-- codex ran: /bin/zsh -lc 'cat .context/research/aaif-2026-10-23/slides/text/2QlEe-01-en-gntcon-japan-2026-pingcap-seki.txt' -->
<!-- codex ran: /bin/zsh -lc 'cat .context/research/aaif-2026-10-23/slides/text/2QlEG-01-20260910-agntcon-japan-hitachi-ito-sato-public.txt' -->
<!-- codex ran: /bin/zsh -lc "rg -n -i -C 5 'pull request|rate.limit|限流|429|simulation|simulate|scene 3|governance' .context/research/aaif-2026-10-23/kong-demo-source/Kong-Demo -->
<!-- codex ran: /bin/zsh -lc "rg --files --hidden .context/research/aaif-2026-10-23/sources .context/research/aaif-2026-10-25 | rg -v '/codex-fix/|/decks/|/pagerduty/|/channel/ -->
<!-- codex ran: /bin/zsh -lc "rg -n '東京鐵塔|天氣不太好|下了一整晚|pfbid02zFB|pfbid02Dgd' .context/research/aaif-2026-10-23 research/2026-10/aaif-agntcon -g '*.json' -g '*.md' -g '"'!zhtw*' -->
<!-- codex ran: /bin/zsh -lc "rg -n -i 'handoff|input.filter|refund.agent|on_handoff|authorization|context.engineer|sub.agent|kubeadm|idempotent|minor.version' .context/researc -->
<!-- codex ran: /bin/zsh -lc 'cat .context/research/aaif-2026-10-23/title-opening-refinement/facebook-tokyo-office.json .context/research/aaif-2026-10-23/title-opening-refineme -->
<!-- codex ran: /bin/zsh -lc "rg -n '"'^##|''^###'"' 2026-10-agentic-harness-blueprint/article.md 2026-09-agentic-org-design/article.md 2026-11-agentic-eval-economics/article.m -->
<!-- codex ran: /bin/zsh -lc "sed -n '307,388p' 2026-10-green-overview/article.md
sed -n '196,228p' 2026-10-green-review/article.md
sed -n '420,515p' 2026-10-green-review/artic -->
<!-- codex ran: /bin/zsh -lc "rg --files --hidden .context -g '"'!**/agents/**'"' -g '"'!**/.agents/**'"' -g '"'!**/.claude/**'"' -g '"'!**/.git/**'"' | rg -i '(handoffs?["'^/] -->
<!-- codex ran: /bin/zsh -lc "sed -n '384,438p' 2026-10-green-reliability/article.md
sed -n '209,280p' 2026-11-agentic-eval-economics/article.md
sed -n '377,418p' 2026-10-green -->
<!-- codex ran: /bin/zsh -lc "sed -n '121,157p' 2026-10-agentic-harness-blueprint/article.md
sed -n '216,250p' 2026-10-agentic-harness-blueprint/article.md
sed -n '27,74p' 2026 -->
<!-- codex ran: /bin/zsh -lc "rg -n -C 4 'Quartic|control plane|worker|第一台|1.31' 2026-10-green-testing/article.md
sed -n '590,630p' .context/research/aaif-2026-10-25/openai-gui -->
<!-- codex ran: /bin/zsh -lc "rg -l --hidden 'transfer_to_refund_agent|on_handoff|Effective context engineering for AI agents' .context research/2026-10/aaif-agntcon -g '"'!**/ -->
六份簡報的主要頁碼、六節點案例與版本數字都已對上。證據上的問題較集中：PingCAP 投影片只展示短期 token 的能力，本文卻進一步寫成重新掛載時必定換證；Kubernetes 文件只替 `kubeadm upgrade` 說明可重跑，不能用來支持整段節點升級的復原。舊文回扣也有重複，接下來會檢查本篇究竟新增了什麼判斷。
<!-- codex ran: /bin/zsh -lc 'cat .context/research/aaif-2026-10-23/sources/kubernetes-version-skew.txt' -->
<!-- codex ran: /bin/zsh -lc 'cat .context/research/aaif-2026-10-23/sources/kubeadm-upgrade.txt' -->
<!-- codex ran: /bin/zsh -lc "nl -ba 2026-11-aaif-agent-handoffs/article.md | sed -n '85,230p'" -->
<!-- codex ran: /bin/zsh -lc "cat .context/research/aaif-2026-10-23/multisource-digest.md
sed -n '1,180p' research/2026-10/aaif-agntcon/rewrite-2026-10-25.md" -->
<!-- codex ran: /bin/zsh -lc "cat .context/research/aaif-2026-10-23/multisource-digest.md
sed -n '1,100p' research/2026-10/aaif-agntcon/rewrite-2026-10-25.md" -->
<!-- codex ran: /bin/zsh -lc "rg -n -C 3 'minor|skip|kubeadm|kubelet' .context/research/aaif-2026-10-23/sources/kubernetes-version-skew.txt | tail -110" -->
<!-- codex ran: /bin/zsh -lc "rg -n -C 3 'idempotent|Recovering|failed|rollback|Skipping|uncordon|Upgrade worker|kubelet' .context/research/aaif-2026-10-23/sources/kubeadm-upgr -->
<!-- codex ran: /bin/zsh -lc "nl -ba 2026-11-aaif-agent-handoffs/article.md | sed -n '230,370p'" -->
<!-- codex ran: /bin/zsh -lc "sed -n '1,100p' 2026-11-aaif-after-tokyo/article.md
sed -n '1,38p' 2026-11-aaif-agent-memory/article.md
cat 2026-11-same-spec-contract/publish/PUB -->
<!-- codex ran: /bin/zsh -lc "rg -n '"'^(##|###)|task|run|tool call|handoff|復原|交接|PR|request|write'"' 2026-09-agentic-engineering-platform/article.md | head -70
rg -n -C 2 'cre -->
<!-- codex ran: /bin/zsh -lc "sed -n '317,370p' 2026-11-aaif-agent-handoffs/article.md
sed -n '250,300p' .context/research/aaif-2026-10-23/kong-demo-source/mock-api/main.py
sed -->
<!-- codex ran: /bin/zsh -lc "python3 -c 'from pathlib import Path; import re; t=Path(\"2026-11-aaif-agent-handoffs/article.md\").read_text(); terms=re.findall(r\"[A-Za-z][A-Za -->
還有兩個會影響結論的缺口：接手版本能拒絕舊請求，卻沒有交代誰有權指定新接手者，也沒說版本如何綁定那個身分；「升級失敗」則不能直接推出節點能安全恢復排程。另已確認一處敘事時間錯位：Facebook 紀錄支持午休操作 demo，但「governance 跟 agent logic 分離」的貼文時間是當天下午 4:42。
<!-- codex ran: /bin/zsh -lc "rg -n 'Scope Control|ttl 1h|Conﬂict Detection|Token Exchange|static internal list|user-centric|procurement use case|Items are ordered|Only an expl -->
**判定：尚未達到這輪驗收標準。** 核心缺口是接手權如何取得、部分失敗後如何安全復原，以及哪些證據足以支持下一步。全程只讀 repository，未修改檔案。

## 致命問題

1. **七、〈檔案各自正確，合起來仍可能違反任務要求〉：接手版本沒有回答誰有權接手。**

   > 「B 接手時取得新的接手版本，A 恢復後即使舊憑證還沒到期，新增的步驟也因為接手版本過期而被拒絕。」

   這只描述如何拒絕舊版本，沒有交代誰能指定 B、根據什麼條件移轉，也沒有把版本綁定到 B 的身分。第九節還說 agent 能讀接手版本；A 若讀到 h2，再用 h2 送出請求，系統憑什麼拒絕？

   **修法：** 明訂由受信任的協調者或有權人員更新「任務、目前持有者的 run identity、接手版本、操作範圍」，更新必須與請求接受有一致順序。新增測試：A 使用最新版本冒充接手者、B 與 C 同時要求接手。這才回答 TL;DR 的「憑什麼取得接手權」。

2. **九、〈中斷後如何判斷下一步〉：把恢復排程寫成升級失敗後的通用補救。**

   > 「允許的補救只有兩種……或者把節點恢復接受工作、留在舊版本。」

   `upgrade 失敗` 不代表節點仍完整停在舊版本，更不代表它適合承載工作。`uncordon` 只是重新允許排程，不會修復部分更新、kubelet 異常或不相容元件。這段省略的正是接手者最需要知道的狀態。

   **修法：** 拆成「確認未修改且健康，可以恢復排程」「部分修改，可依已核准程序修復」「狀態不明或不健康，維持隔離並交人處理」。每條都指定版本、健康與容量證據。刪掉「只有兩種」。

## 重要問題

1. **二、〈交接時，到底交出了什麼？〉：主問題有四件事，閱讀地圖卻硬塞成三列。**

   > 「用誰的權限、做到哪個範圍、此刻誰能新增操作」

   身分、任務授權、執行責任不是同一件事。正文一路處理授權與狀態，直到第七節才真正碰到「前任恢復後誰能繼續」。TL;DR 最尖銳的問題因此長時間沒有展開。

   **修法：** 閱讀地圖拆出「目前誰持有接手權」，第二節就放入 A 失聯、B 接手、A 恢復的情境。後面各節逐次補齊同一份交接紀錄，而不是反覆說「這一場回答第一／第二件事」。

2. **二、〈交接時，到底交出了什麼？〉：三種情境不是同一個分類維度。**

   > 「第一種是同一個執行流程裡換一個 agent……第二種是把一段工作委派給另一個服務……第三種是中斷後重新接手。」

   前兩項混合控制方式與部署位置，第三項是故障生命週期。加一句「可以重疊」沒有降低理解成本。整段又一次塞入 SDK、工具、filter、回呼、兩種 pattern、子 agent、摘要與恢復。

   **修法：** 先問「交出控制權，還是只派工作等結果？」再問「交接過程是否跨服務或遇到重啟？」SDK 細節移註腳。正文只保留會改變接手證據的差異。

3. **六、〈先分清哪些資料要留、哪些權限要重查〉：把可用功能寫成已存在的恢復流程。**

   > 「重新掛載時拿到的就是這種短期、受限的存取，不是前任的憑證。」

   [PingCAP 第 21 頁](/Users/kochi.chuang/conductor/workspaces/medium-articles/dodoma/.context/research/aaif-2026-10-23/slides/text/2QlEe-01-en-gntcon-japan-2026-pingcap-seki.txt:315)支持 tenant、路徑權限與 `--ttl 1h`，沒有證明每次重新掛載都重新核發，也沒有展示前任憑證如何失效。

   **修法：** 改成「這項能力可用來設計重新掛載時的換證流程；簡報沒有展示換證與接手權移轉的整合」。把後半句歸回作者建議。

4. **五、〈修復之後，重新確認評估與核准〉：沒有區分預期進展與意外漂移。**

   > 「哪些觀察欄位一變就讓評估失效……各節點的版本與角色……」

   升級本來就會改變節點版本。照目前文字，每完成一步都可能讓整份評估失效。另一方面，「外掛設定變了」可能改變風險，不能只因目標與步驟沒變，就預設可沿用核准。

   **修法：** 分成「計畫已預期的狀態轉移」「仍在預先核准界線內的變動」「超出界線的變動」。核准應包含可接受的變動條件，不只是固定快照。

5. **五、〈從全部節點到服務結果，逐層驗收〉：把新操作授權與完成事實混在一起。**

   > 「升級能否結束，要由目前環境下仍有效的核准……共同決定。」

   核准到期後，不能新增操作；但不應因此抹去到期前合法接受、後來才確認完成的效果。是否必須在窗口內完成，是另一條需要明訂的契約。

   **修法：** 分清「何時停止接受新操作」「已接受操作是否繼續」「何時可以確認結果」「維護窗口超時由誰處理」。各自測試。

6. **七、〈版本檢查保住修改，也保留處理衝突的機會〉：保留在本機不等於保住成果。**

   > 「也保留 B 可以重新整合的成果。」

   第 23 頁只說失敗檔案留在失敗的一端。前文已說 sandbox 可以消失、上傳非同步；拒絕寫入後若丟棄 sandbox，B 的修改仍可能遺失。

   **修法：** 加上拒絕後的保存責任：把衝突副本另存為可持久查詢的成果，確認保存成功後才清理環境。否則只能說「暫時保留本機修改」。

7. **九、〈先定義操作與證據契約〉：又把整段升級縮成一個可重跑指令。**

   > 「升級指令本身，官方文件說明可以重跑。」

   [Kubernetes 存檔](/Users/kochi.chuang/conductor/workspaces/medium-articles/dodoma/.context/research/aaif-2026-10-23/sources/kubeadm-upgrade.txt:972)說的是 `kubeadm upgrade`，不包含套件安裝、kubelet 更新與重啟、排空及恢復排程。第五節「升級本身只是一行指令」也有同樣問題。

   **修法：** 明確寫出命令名稱，將本文測試限制為一個 worker 的哪些操作。不要用「升級」同時指單一命令、子步驟與整個任務。

8. **九、〈中斷後如何判斷下一步〉：「接受」沒有定義，故障切點無法判讀。**

   > 「讓執行服務在接受操作之後、寫下紀錄之前重啟」

   「接受」是收到封包，還是已承諾能追蹤這次操作？若已對外承諾接受，卻尚未持久登記，前面的操作查詢契約就可能不成立。

   **修法：** 分開「收到請求」「持久登記」「回覆接受」「產生效果」「保存結果」，逐一指定切點與預期。否則驗收者不知道測到的是正常復原，還是服務違反自身承諾。

9. **五、〈評估認為可行，執行仍要核准〉：回扣三道閘時，新增性說過頭。**

   > 「這場把同樣的證據要求落實成機器可讀的評估狀態」

   舊文三道閘檢查的是測試辨識力、review 與任務可靠度，不是升級 readiness 的四種狀態。「讀不懂不能算通過」在測試篇的非預期失敗處置也已經出現。

   **修法：** 寫成共同原則的不同應用。本篇新增的重點應是：**評估、核准與現況如何在交接後重新對齊**，不是再次發現 UNKNOWN 應阻擋。

## 次要問題

1. **一、〈會議之前，先去看一眼東京鐵塔〉：敘事時間沒有來源支持。**

   > 「午休時我寫下『governance 跟 agent logic 分離』」

   [Facebook 存檔](/Users/kochi.chuang/conductor/workspaces/medium-articles/dodoma/.context/research/aaif-2026-10-23/facebook-post-provenance.json)顯示貼文時間為 9 月 10 日下午 4:42；內容支持午休操作 demo，不能證明午休寫下這句話。

   **修法：** 「午休時把 demo 架起來，當天貼文寫下……」。

2. **四、〈把帳號能力縮成這次任務的操作範圍〉：把示範規則的適用操作擴大了。**

   > 「寫入則限於……作者是自己……帶有 AI 標記的 issue」

   Studist 第 39 頁的示範是 `operations: ["edit"]`，不是所有寫入。

   **修法：** 改成「示範中的 issue 編輯規則要求……」，不要替建立、留言等操作補上未展示的保證。

3. **五、〈評估認為可行，執行仍要核准〉：webhook 故障結果寫得太絕對。**

   > 「若那個服務不支援新版本，升級後符合規則的新工作都建不起來。」

   是否阻擋還取決於匹配範圍、失敗方式與設定。原簡報特別列的是 fail-closed webhook。

   **修法：** 加上「若請求必須通過它，且失敗時設定為拒絕」。否則讀者會把所有 webhook 異常都理解成相同後果。

4. **八、〈三種整合方式，分別把維護責任放在哪裡？〉：兩處把解讀寫成來源細節。**

   > 「agent 的位址寫死在程式裡」  
   > 「換一張目標系統接受的受限通行證」

   第 18 頁寫的是靜態端點清單，不必然是寫死在程式碼；token exchange 也不能單靠名稱推出權限已縮小。

   **修法：** 改成「由應用程式維護靜態端點清單」，並將權限縮小寫成必須配置與驗證的條件。

5. **八、開場與〈共同元件仍需接上業務條件的檢查〉：預期規則和觀察結果應更早分開。**

   > 「而且『只有在所有條件與人類核准完成後才下單』」

   第 28 頁是流程要求；第 24 頁才是實際曾違反要求的觀察。

   **修法：** 開頭直接寫「預期規則是……但他們後來觀察到未滿足條件仍下單」。不要等讀完架構清單才揭露矛盾。

6. **九、〈先定義操作與證據契約〉：交接紀錄不是一份可以直接判讀的狀態。**

   > 「操作識別 op-17，子步驟……各有自己的識別」  
   > 「允許的下一步是查詢與回報，不含新的變更」

   沒列出子識別，也沒說 `/operations/op-17` 查的是整體還是單一步驟；後文卻允許「接續尚未完成的工作」。

   **修法：** 排成表格，列出 parent operation、各子操作識別與狀態；說明什麼證據與哪個權威決定能把「只准查詢」更新成「准許下一步」。

7. **十、〈延伸閱讀：本文接回的幾篇〉及 References：查核範圍需要精確。**

   六份簡報的主要頁碼、Quartic.ai 的 3＋3 節點、1.30／1.31／1.32、五項檢查，以及 PingCAP 的一小時範例均能對上；本篇沒有 timecode 引文。OpenAI guide 的兩種 pattern 也對得上。SDK 與 Anthropic 的精確引文，本輪未在 repo 找到可獨立核對的原文快照；研究紀錄的「已查閱」不能代替原文。**這兩項應標為未完成本輪獨立核對，不能直接判為造假。**

## 建議刪除

以下段落沒有增加新的判斷，或離開本節尚未回答的問題。

| 位置與原句 | 具體處理 |
|---|---|
| 一、首段：「可惜今天的天氣不太好」，以及日夜照片連續圖說 | 天候目前只是旅程裝飾。保留短段與封面照即可；夜景可移文末。不要替照片補造技術領悟。 |
| 一、末段：「這篇使用公開議程所附的六份簡報……」 | 移入〈資料與方法註記〉，正文只留「返台重讀，不代表逐場出席」。 |
| 二、長段：「文件叫 input filter……交接的回呼裡」 | API 細節移註腳；保留「可過濾資料、交棒前可檢查」即可。 |
| 四、〈把帳號能力縮成這次任務的操作範圍〉：「`safe-webfetch` 依使用者實際行為……」 | 這裡沒有新增升級交接的判斷。移資料註記，正文集中分析一條無法繞過的執行路徑。 |
| 四、〈用允許與越界請求，檢查限制是否生效〉：「簡報第 16 頁引用一項研究……」 | 核准疲勞已在舊文展開，本節也沒提出如何選擇人工核准的具體準則。刪段或補準則。 |
| 六、〈本機進度與遠端結果，可能在中斷時分開〉：「先寫『完成』再操作……先操作再寫檔……」 | 與前段兩種落差合併，保留「兩個系統有不同完成時刻」的原因。 |
| 七、〈記憶幫忙找回脈絡，核准仍須回查〉：「mem9 在對話結束時保存紀錄……」 | 縮成章末一句交棒；不要在接手權尚未處理完整時切到第三篇。 |
| 八、〈三種整合方式，分別把維護責任放在哪裡？〉：「Directory……OASF……SLIM……Observe……」 | 元件清單移比較表或註記。正文先處理「條件未滿足仍下單」，再說架構如何承擔這項檢查。 |
| 九、〈中斷後如何判斷下一步〉：「但第九節已經列出跨重啟……」 | 付款篇的待驗證清單不用再背一次。只保留本篇新增的接手者更換與多階段操作。 |
| 九、〈哪些結果支持開放操作〉：「用一張義務表把每一項要求的來源……」 | 契約篇方法介紹縮成一句，直接帶讀本篇表格的一列。 |
| 十、首段：「我原本是在替每場演講找位置」 | 刪除整理文章的後設敘述，直接進入接班同事重建證據的成本。 |

需要重接的轉場：

| 位置與原句 | 缺的交接 |
|---|---|
| 一：「回台北重讀材料時……」 | 東京鐵塔段沒有產生任何待解問題。直接讓 Kong 的中斷情境成為開場問題。 |
| 五、〈從全部節點到服務結果，逐層驗收〉：「完成的判斷也有相同問題」 | 前面是核准時效，這裡是驗收漏項。改問：「核准清單固定後，誰確認執行器沒有漏掉其中一台？」 |
| 同小節：「工具本身也會改變結果」 | 只是增加題目。先問：「知道還剩哪些節點後，新環境取得的工具能否接續原計畫？」 |
| 七、末段：「由誰把它們接成一條不可繞過的流程？」 | 八、前半回答的是連線整合，不是業務流程強制。把 Hitachi 的下單失敗提前。 |
| 九、〈中斷後如何判斷下一步〉：「兩個案例的本地摘要可以很相似」 | 中間已插入多個案例，指涉失焦。直接點名「遠端已完成但回覆遺失」與「請求尚未送出」。 |

## 建議補充

1. **三至八、各場分析：深度缺口應補在設計條件，不再補一般警語。**

   | 場次／位置與原句 | 還缺的第一性原理推論 |
   |---|---|
   | 三、〈語意檢查還要決定等待、拒絕與接手的時機〉：「語意判斷逾時時，不接受新的排空」 | 已討論延遲與誤判；還要交代「新」以哪個接受時刻為界，以及檢查後排隊、授權到期的請求如何處理。 |
   | 四、〈強制檢查要放在 agent 無法繞過的位置〉：「核對計畫與目前條件後……操作」 | 還缺任務規則由誰產生、如何對回核准版本。把政策移遠端，只改變修改權限，沒有自動解決政策正確性。 |
   | 五、〈評估認為可行，執行仍要核准〉：「再做規則檢查，交給模型評估」 | **模型必要性仍停在摘要。** 哪些判斷無法由規則完成？模型能解讀哪些非結構資料？找不到相容性證據時為何不能自行補答案？也要比較固定自動化流程。 |
   | 六、〈先定義保存承諾，再選擇故障注入的位置〉：「分析草稿可以重建，已送出的操作識別卻不能遺失」 | 把重建成本落到實際安排：哪些留本機、哪些必須先持久登記、哪些成果要發布。再說持久層不可用時停掉哪些能力。 |
   | 七、〈版本檢查保住修改，也保留處理衝突的機會〉：「失敗的檔案留在寫入失敗的那一端」 | 補上衝突後的保存與清理成本；並說明並行探索何時值得付出合併與重新驗證的代價。 |
   | 八、〈三種整合方式，分別把維護責任放在哪裡？〉：「讓團隊少寫一些各自獨有的整合程式」 | 前半仍偏元件摘要。選型表應直接列出：哪個元件讀核准、哪個元件拒絕下單、哪個團隊維護條件；連線便利程度不能回答這三題。 |

2. **九、〈哪些結果支持開放操作〉：把星期一的工作分給具體角色。**

   > 「我會先在可丟棄的測試環境裡，只驗收一種有限操作。」

   補三項交付物即可：

   - **Staff／平台：** 寫一份單一步驟契約，明訂接受時刻、操作識別、接手者身分、查詢與重送語意。
   - **QA／SRE：** 對同一步驟安排送出前、效果後回覆前、服務重啟、舊接手者恢復四種切點，保存外部效果紀錄。
   - **VP／服務負責人：** 決定可承受的待確認時間與人工處理量；超出時縮小自動化範圍。不要只列指標名稱。

3. **四、八、九的舊文回扣：把新增部分寫清楚。**

   > 「我在〈Harness 藍圖〉第六節提過的幾件事在這裡有了對應」

   Harness 舊文已要求 per-run scoped token、工具端持有 secret、後端驗證與不可繞過路徑。本篇若再完整講一次，只有換例子。

   **修法：** 把新增部分集中在「同一任務跨 run 後，操作識別保持什麼、接手身分改變什麼、舊 run 如何失去新增操作資格」。Review、測試、付款、組織與契約篇的章節回扣大致對得上；應縮短重述，保留這些差異。

4. **十、〈結語：留下來的工作，要讓下一個人敢接〉：讓真實經驗承擔收束。**

   > 「午休時我寫下『governance 跟 agent logic 分離』」

   可用的思考轉折已經存在：當天關注治理與 agent logic 分離；返台重讀後，發現分離仍未交代中斷工作如何接續。把這個轉折放在首尾即可。邀請與澀谷照片不在本篇，不需要為了溫度補進來。

## 術語仍難懂的清單

| 首次出現位置與原文 | 具體修法 |
|---|---|
| 一：「建立 PR 的模擬操作」 | PR 到第二節才解釋。第一次寫「建立程式變更提案（PR）」。 |
| 一：「governance 跟 agent logic 分離」 | 緊接白話：「agent 選下一步，外層系統決定請求能不能通過。」 |
| 四、〈把帳號能力縮成這次任務的操作範圍〉：「CI 用它的帳號與拿得到的 secrets」 | 先說「CI 自動登入其他系統所需的密碼或 API key」，再稱 secrets。 |
| 四、〈強制檢查要放在 agent 無法繞過的位置〉：「reference」 | 用「金鑰代號」示範，並說工具仍須驗證誰有權使用；不要暗示拿到代號就能換到金鑰。 |
| 同小節：「每次 run」 | run 到第八節才定義。首次補「這次啟動 agent 到結束的一輪執行」。 |
| 五、〈評估認為可行，執行仍要核准〉：「API server」「webhook」「controller」 | 同段塞太多依賴名詞。先走一筆建立工作請求：誰收件、誰檢查、誰持續調整；其他元件清單移註記。 |
| 七、開場：「無狀態的 harness」 | 「執行程式」太籠統。用「負責讓 agent 讀任務、呼叫工具並繼續下一步的控制程式」建立角色。 |
| 七、〈版本檢查保住修改，也保留處理衝突的機會〉：「copy-on-write」 | 先說兩個工作區共用起點、各自保存修改，再引入名稱；保留外部效果不受隔離的界線。 |
| 七、〈檔案各自正確，合起來仍可能違反任務要求〉：「序列化」「鎖的就是進行中的 worker 數」 | 改用一個維護名額：先取得名額才開始，確認操作結束才釋放。說清楚這不是兩邊各自讀取一個數字。 |
| 同小節：「接手版本」 | 需要完整的持有者與發放規則，不能只當成遞增號碼。見致命問題一。 |
| 八、〈三種整合方式，分別把維護責任放在哪裡？〉：「AGNTCY、Directory、OASF、SLIM、Observe」 | 一次五個名稱。正文只留「尋找接手者、描述能力、傳訊與觀測」；產品名移表格。 |
| 同小節：「JWT 與 OAuth 2.0」 | 分清憑證格式與授權機制；沒有分析其差異，就刪除縮寫，只說驗證存取憑證。 |
| 八、〈共同元件仍需接上業務條件的檢查〉：「OpenTelemetry」「trace」「埋點」 | 用一筆採購從 task、agent 到下單服務的時間線解釋；再說時間線為何仍不能證明核准。 |
| 八、〈讓 task、run 與 tool call 對回同一份授權〉：「domain team」「production ownership」 | 首次寫成「負責該產品或服務的團隊」「上線後品質與事故責任」。 |

`commit point／RPO／RTO`、`optimistic locking`、冪等性已有情境承接，問題主要在契約條件，不必再加一輪類比。`proxy、skill、digest、compaction、RRF、oracle、holdout` 未在這篇正文展開，不應把其他篇的術語問題算到本篇。

<!-- tokens: in 2483655 out 22794 -->
