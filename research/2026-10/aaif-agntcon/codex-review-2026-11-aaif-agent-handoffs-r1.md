# Codex review — 2026-11-aaif-agent-handoffs/article.md

> model: gpt-6.1-sol, reasoning: xhigh, 2026-10-25 22:47. 原話照錄，未經摘要。審的是 2026-10-25 改寫後的版本。

我會先讀 STYLE.md 與 style_brief，再逐項核對簡報、來源與舊文 recall。全程只讀，不修改檔案，也不讀取你禁止的目錄。
<!-- codex ran: /bin/zsh -lc 'cat STYLE.md' -->
<!-- codex ran: /bin/zsh -lc 'cat research/2026-10/style_brief.md' -->
<!-- codex ran: /bin/zsh -lc 'nl -ba 2026-11-aaif-agent-handoffs/article.md' -->
<!-- codex ran: /bin/zsh -lc "rg --files -g 'AGENTS.md' -g 'article.md' -g '"'!agents/**'"' -g '"'!.claude/**'"' -g '"'!**/agents/**'"' -g '"'!**/.claude/**'"'" -->
<!-- codex ran: /bin/zsh -lc "rg --files --hidden .context/research/aaif-2026-10-23 .context/research/aaif-2026-10-25 research/2026-10/aaif-agntcon -g '"'!agents/**'"' -g '"'!* -->
<!-- codex ran: /bin/zsh -lc 'cat .context/research/aaif-2026-10-23/facebook-post-provenance.json' -->
<!-- codex ran: /bin/zsh -lc "rg -n 'handoffs/|input_filter|is_enabled|1000|1,000|2,000|2000|context engineering|on_handoff|all previous|token' research/2026-10/aaif-agntcon/mu -->
<!-- codex ran: /bin/zsh -lc "rg --files --hidden .context/research/aaif-2026-10-23/slides/text .context/research/aaif-2026-10-25 | rg '(2RCwp|2QlDX|2QlD9|2QlE7|2QlEe|2QlEG|han -->
<!-- codex ran: /bin/zsh -lc "rg -n '"'^#{1,3} |SEC-2291|已預先核准|第六節|核准疲|G2|三道|Quartic|綠茶|冪等|短效|secret|registry|identity broker|義務表|worktree|十份|四種'"' 2026-10-green-*/article.md 2 -->
已看到兩個需要優先核對的主張：第二節把 SDK handoff 稱為「協定層」，第七節則把 drive9 的隔離方式說成與作者舊研究「做的是同一件事」。這兩處都可能把不同層次的機制混在一起。
<!-- codex ran: /bin/zsh -lc 'cat .context/research/aaif-2026-10-23/slides/text/2RCwp-01-agntcon-mcpcon-japan2026-softbank-corp.txt .context/research/aaif-2026-10-23/slides/tex -->
<!-- codex ran: /bin/zsh -lc 'cat .context/research/aaif-2026-10-23/slides/text/2QlD9-01-agntcon-mcpcon-japan-2026-abhijeet-sanskar-final.txt' -->
<!-- codex ran: /bin/zsh -lc 'cat .context/research/aaif-2026-10-23/slides/text/2QlEe-01-en-gntcon-japan-2026-pingcap-seki.txt' -->
<!-- codex ran: /bin/zsh -lc 'cat .context/research/aaif-2026-10-23/slides/text/2QlEG-01-20260910-agntcon-japan-hitachi-ito-sato-public.txt' -->
<!-- codex ran: /bin/zsh -lc "sed -n '16,80p' research/2026-10/aaif-agntcon/handoffs-media-manifest.json" -->
<!-- codex ran: /bin/zsh -lc "rg --files --hidden .context/research research/2026-10 -g '"'!**/agents/**'"' -g '"'!**/.claude/**'"' | rg '(handoff|anthropic|context-engineering -->
<!-- codex ran: /bin/zsh -lc "sed -n '290,370p' .context/research/aaif-2026-10-25/openai-guide/guide.txt" -->
<!-- codex ran: /bin/zsh -lc "python3 -c 'from pathlib import Path; p=Path(\".context/research/aaif-2026-10-23/slides/text/2QlDX-01-intent-as-code-13.txt\"); pages=p.read_text( -->
<!-- codex ran: /bin/zsh -lc "sed -n '307,384p' 2026-10-green-overview/article.md" -->
<!-- codex ran: /bin/zsh -lc "sed -n '165,250p' 2026-10-green-review/article.md" -->
<!-- codex ran: /bin/zsh -lc "rg -n 'SEC-2291|已預先核准|"'^## |Habituation|Intent as Code'"' 2026-10-green-review/article.md; sed -n '420,442p' 2026-10-green-testing/article.md" -->
<!-- codex ran: /bin/zsh -lc "rg -n 'G2|"'^## 五|''^## 六|''^## 三|registry|identity broker|secret|短效|egress'"' 2026-10-green-reliability/article.md 2026-10-agentic-harness-bluepr -->
六場簡報的主要頁碼與 Kubernetes 數字已對上。較大的問題在論證邊界：本文把「可能沒有交齊」寫成「沒有跟著過去」，把幾種交接當成同一種 handoff；驗收章又預設執行服務已有操作識別與安全重送能力。接下來會核對舊文，分清哪些回扣增加了推論，哪些只是重述。
<!-- codex ran: /bin/zsh -lc "sed -n '384,406p' 2026-10-green-reliability/article.md" -->
<!-- codex ran: /bin/zsh -lc "sed -n '121,144p' 2026-10-agentic-harness-blueprint/article.md" -->
<!-- codex ran: /bin/zsh -lc "rg -n 'handoff|decentralized|manager pattern|control|conversation' .context/research/aaif-2026-10-25/openai-guide/guide.txt" -->
<!-- codex ran: /bin/zsh -lc "rg -n 'worktree|無工具|一次生成|四十|十份|隔離|義務表|"'^## |''^### '"' 2026-11-same-spec-contract/article.md 2026-11-same-spec-overview/article.md" -->
<!-- codex ran: /bin/zsh -lc "rg -n '冪等|PENDING|同一行程|並行|重啟|綠茶|request_id|idempotency|"'^## |''^### '"' 2026-10-green-payment/article.md" -->
<!-- codex ran: /bin/zsh -lc "rg -l --hidden 'is_enabled|on_handoff|transfer_to_refund_agent|1,000.2,000|1,000.?2,000|Day1晚安|可惜今天的天氣不太好' .context/research/aaif-2026-10-25 .cont -->
<!-- codex ran: /bin/zsh -lc "sed -n '493,517p' 2026-11-same-spec-contract/article.md" -->
<!-- codex ran: /bin/zsh -lc "sed -n '835,868p' .context/research/aaif-2026-10-25/openai-guide/guide.txt" -->
<!-- codex ran: /bin/zsh -lc 'cat .context/research/aaif-2026-10-23/title-opening-refinement/facebook-office-date.txt .context/research/aaif-2026-10-23/title-opening-refinement -->
<!-- codex ran: /bin/zsh -lc "rg -n 'worktree|無工具|一次生成|sandbox|隔離|生成' research/experiments/same-spec-ten-runs/RESULTS.md" -->
<!-- codex ran: /bin/zsh -lc "python3 -c 'from pathlib import Path; p=Path(\".context/research/aaif-2026-10-23/slides/text/2RCwp-01-agntcon-mcpcon-japan2026-softbank-corp.txt\" -->
<!-- codex ran: /bin/zsh -lc "sed -n '1,110p' 2026-11-aaif-agent-memory/article.md" -->
<!-- codex ran: /bin/zsh -lc "sed -n '1,125p' 2026-11-aaif-after-tokyo/article.md" -->
<!-- codex ran: /bin/zsh -lc "rg -n 'handoff|context|token|SDK|OpenAI|Anthropic' research/2026-10/aaif-agntcon/handoffs.md" -->
<!-- codex ran: /bin/zsh -lc "rg --files --hidden .context/research/aaif-2026-10-25 -g '*.json' -g '*.md' -g '*.txt' -g '*.html' | rg -v '(review|channel|pagerduty)'" -->
<!-- codex ran: /bin/zsh -lc "rg -n 'worktree|mkdtemp|TemporaryDirectory|workspace|candidate_dir|cwd=' research/experiments/same-spec-ten-runs -g '*.py' -g '"'!**/candidates/** -->
<!-- codex ran: /bin/zsh -lc "sed -n '90,260p' 2026-11-aaif-agent-handoffs/article.md" -->
<!-- codex ran: /bin/zsh -lc "sed -n '405,456p' research/experiments/same-spec-ten-runs/results/formal-2026-09-25/source/run_study.py" -->
<!-- codex ran: /bin/zsh -lc "rg -n 'version|skew|Skipping|minor|kubeadm|worker' .context/research/aaif-2026-10-23/sources/kubeadm-upgrade.txt" -->
<!-- codex ran: /bin/zsh -lc "rg -n '"'^[0-9]{1,2}:[0-9]{2}|'"\\[[0-9]{1,2}:[0-9]{2}|timestamp|timecode' 2026-11-aaif-agent-handoffs/article.md" -->
<!-- codex ran: /bin/zsh -lc "rg -n 'handoff|權限|狀態|recover|復原|共享|RACI|owner|停止|rollback|回滾|on-call' 2026-09-agentic-org-design/article.md 2026-09-agentic-engineering-platform/a -->
<!-- codex ran: /bin/zsh -lc "sed -n '1,65p' research/experiments/same-spec-ten-runs/RESULTS.md" -->
已確認一個事實錯誤：正式的《同一份規格，跑十次》研究使用無工具的一次生成，runner 建立的是暫存目錄，不是四十個 git worktree；本文混入了八月工作坊的隔離做法。

另外，repo 保存的 Kubernetes 官方文件明說 `kubeadm upgrade` 可冪等重跑。第九節必須指定測的是哪個操作，並區分「再次呼叫」與「新增一次效果」，否則驗收無法判定。
<!-- codex ran: /bin/zsh -lc "nl -ba 2026-11-aaif-agent-handoffs/article.md | sed -n '236,266p'" -->
<!-- codex ran: /bin/zsh -lc "nl -ba 2026-11-aaif-agent-handoffs/article.md | sed -n '84,106p'" -->
<!-- codex ran: /bin/zsh -lc "rg -n 'Sandbox 與權限|產出品質|production ownership|"'^## |G2：|G3：'"' 2026-09-agentic-org-design/article.md 2026-11-agentic-eval-economics/article.md" -->
<!-- codex ran: /bin/zsh -lc "rg -n '1,000|2,000|1000|2000|on_handoff|is_enabled|input_filter|transfer_to_refund_agent' .context/research/aaif-2026-10-23/multisource-digest.md  -->
回扣的主要問題已分清：Review 篇的 SEC-2291、測試篇的漏查 worker、契約篇的義務表都有對應內容；「三道閘原本只有過與不過」則沒有原文支持。稿件也尚未接上組織篇既有的責任分工：結果未知時，誰接手、多久內處理、由誰決定恢復或停止。
<!-- codex ran: /bin/zsh -lc "sed -n '27,70p' 2026-09-agentic-org-design/article.md" -->
<!-- codex ran: /bin/zsh -lc "rg -n '429|PR created|create_pull_request|rate.limit|in.memory|memory|mock' .context/research/aaif-2026-10-23/kong-demo-source -g '*.md' -g '*.py' -->
目前不宜定稿。主線應收斂成：**前任無法再解釋時，接手者憑什麼決定繼續、重做或停止？** 現稿仍混用不同種類的交接，且有一處作者自身研究的事實錯誤。

已核對六份簡報、相關舊文章與研究紀錄。六場主要數字與頁碼未發現不符；SDK 與 Anthropic 工程文章未找到完整原文封存，相關逐字引用及摘要長度仍待核。

## 致命問題

1. **二、〈交接時，到底交出了什麼？〉：把 SDK 控制流程、跨服務委派與故障恢復混成一種 handoff。**

   > 「協定層的 handoff 做了什麼，可以直接看 OpenAI 的 Agents SDK。」

   SDK 的 agent 切換不是 A2A 協定，也沒有因此提供跨服務的持久化、權限委派或故障恢復。後文卻一路用它替三種問題建立共同前提。

   **修法：**先區分「同一執行流程換 agent」「把工作委派給另一個服務」「中斷後重新接手」。明說本文比較它們共同需要的證據，不宣稱共享同一套交接機制。

2. **TL;DR、二、十：把「沒有保證有效」寫成「沒有傳過去」。**

   > 「三樣東西沒有跟著過去：原本核准的範圍到此刻是否仍有效、外部系統實際做到哪裡，以及這件工作怎樣才算完成。」

   核准紀錄、操作結果與驗收條件都可能隨交接傳遞。真正的問題是來源可信度、完整性與時效。現句把整篇建立在過度斷言上。

   **修法：**改成「交接可以帶上這三類資料，但傳遞本身不保證它們完整、可信，或現在仍有效」。TL;DR 的「看得到前面發生的一切」也應改為「預設取得先前對話紀錄」；對話不等於全部事實。

3. **七、〈版本檢查保住修改，也保留處理衝突的機會〉：作者研究經歷寫錯。**

   > 「讓四種交代各生成十份程式，就是把每一份放進獨立的 git worktree 隔離執行。」

   正式研究是無工具的一次生成；[封存 runner](/Users/kochi.chuang/conductor/workspaces/medium-articles/dodoma/research/experiments/same-spec-ten-runs/results/formal-2026-09-25/source/run_study.py:438)使用 `TemporaryDirectory`，不是四十個 git worktree。[正式研究結果](/Users/kochi.chuang/conductor/workspaces/medium-articles/dodoma/research/experiments/same-spec-ten-runs/RESULTS.md:3)也明確限制研究範圍。git worktree 是測試篇記錄的八月工作坊做法。

   **修法：**刪除這筆 recall，或準確改引工作坊。即使改引，也只能說隔離修改的目的相近，不能說 drive9 layers「做的是同一件事」；外部操作、憑證與網路效果不會因此隔離。

4. **七、〈檔案各自正確，合起來仍可能違反任務要求〉＋九：缺少「誰現在有權接著執行」。**

   > 「讓平台在執行服務裡協調或序列化有副作用的步驟。」

   > 「新的 agent 只拿到已保存的輸入、計畫、工作檔與操作識別。」

   序列化沒有回答：A 只是斷線、稍後恢復，B 已經接手，兩者誰還能送出下一步？兩者可能持有同一份仍有效的任務核准。查核授權與防止兩個接手者同時行動，是不同要求。

   **修法：**補「A 失聯、B 接手、A 恢復」的案例。執行服務必須辨識目前接手者，拒絕前任新增步驟；已接受的操作則繼續追蹤結果。這才把交接從傳資料推進到轉移執行責任。

## 重要問題

1. **九：沒有指定操作，驗收預期無法判定。**

   > 「最直覺的『從最後一行重跑』，恰好會把同一件事再做一次。」

   再次呼叫不一定新增一次效果。repo 保存的 [Kubernetes 官方文件](/Users/kochi.chuang/conductor/workspaces/medium-articles/dodoma/.context/research/aaif-2026-10-23/sources/kubeadm-upgrade.txt:972)明說 `kubeadm upgrade` 可以冪等重跑。排空、套件安裝、通知與升級，也各有不同的重送語意。

   **修法：**挑定一個操作，列出「正常效果」「容許的再次呼叫」「禁止新增的效果」。驗收應檢查契約是否被破壞，不能把第二次呼叫直接算錯。

2. **九：操作識別與結果查詢的服務契約仍太薄。**

   > 「這個設計要求執行服務接受預先產生的操作識別。」

   一個識別碼沒有自行解決副作用與紀錄之間的中斷。讀者還會問：同一識別帶不同節點或計畫怎麼辦？操作尚在執行時回什麼？服務自己重啟後還認得嗎？紀錄過期後能否重送？

   **修法：**補最小契約：識別對應固定參數；區分未接受、執行中、完成、失敗與無法判定；交代保存期限及服務重啟後的承諾。把這些列為採用前提，不讓它們躲在「服務承諾」四字裡。

3. **三、〈語意檢查還要決定等待、拒絕與接手的時機〉：未說清楚檢查發生在效果之前還是之後。**

   > 「內容尚未判定時能不能觸發行動。」

   這是本節應回答的問題，現稿只把它交回服務負責人。若檢查的是執行後串流回來的狀態，阻擋回覆也無法撤銷已發生的操作。

   **修法：**沿升級案例區分「尚未交給執行服務的請求」與「操作已開始後的回報」。前者能阻止執行；後者主要支援偵測與復原。這項推導應標為作者分析，不能讓讀者以為 SoftBank PoC 已驗證完整操作控制。

4. **四、〈把帳號能力縮成這次任務的操作範圍〉：把示範設定寫成工具的固定保證。**

   > 「`safe-push` 禁止 commit 裡動到 `.github/` 這類 CI 定義。」

   Studist 第 48–49 頁描述的是 push 前檢查已提交檔案，條件不符時拒絕或要求人工核准，並保留人工 `--force` 路徑；不是禁止建立這類 commit。`safe-gh` 的組織與 issue 限制也是設定例。

   **修法：**全部加上「投影片的示範設定」。準確區分 commit、push 與人工例外。`safe-webfetch` 則補一句：網址範圍被允許，不代表內容已可信，更不代表其中指令取得執行權。

5. **四、〈強制檢查要放在 agent 無法繞過的位置〉：把權限隔離簡化成機器位置。**

   > 「正是因為放在 agent 自己的機器上會被同一個執行者改掉。」

   同一台機器可以有 agent 無權修改的控制；遠端服務也可能接受過度寬鬆的請求。關鍵是 agent 能否修改政策、取得底層憑證或繞過執行入口。

   **修法：**改寫成控制權與可繞過路徑的問題。遠端化的收益與成本，應包含介面限制、可用性、政策維護與例外處理。

6. **五、〈評估認為可行，執行仍要核准〉：為製造新意，扭曲舊文。**

   > 「《綠燈不是驗收》總論第六節的三道閘原本只有過與不過。」

   [原文第六節](/Users/kochi.chuang/conductor/workspaces/medium-articles/dodoma/2026-10-green-overview/article.md:307)是在區分三種驗收責任，沒有宣告所有結果只能二分。測試篇第五節更已要求區分未執行、失敗與完成。

   **修法：**改成「這場把前文的證據要求進一步落實成機器可讀的評估狀態」。新增的是狀態與後續處置的對應，不是首次發現未知。

7. **五、〈修復之後，重新確認評估與核准〉：重查規則還沒有形成可執行判斷。**

   > 「若核准後有人增加節點、換了 controller……就需要依明訂條件重查或重新取得核准。」

   「明訂條件」正是讀者需要本文協助決定的內容。任何變動都重簽會讓流程停滯；一律沿用又會執行過期計畫。

   **修法：**至少示範三類變動：不影響核准的觀察更新、需要重評但可沿用範圍的變動、必須重新核准的目標或步驟變更。完成驗收也要處理核准清單與目前節點清單不一致的情況。

8. **六、〈先分清哪些資料要留、哪些權限要重查〉：把儲存配置推成授權行為。**

   > 「如此一來……權限是否仍有效，會由當下的授權服務重新決定。」

   控制狀態放外部、秘密不進快照，不會自動產生重新授權流程。外部紀錄也可能過期，甚至被 agent 改寫。

   **修法：**明標這是作者建議，補上誰能寫核准紀錄、接手時向誰查、查詢失敗怎麼處理。別讓「外部」成為可信的同義詞。

9. **八、〈三種整合方式，分別把維護責任放在哪裡？〉：架構 recall 說得過滿。**

   > 「Hitachi 的第三種方式就是那個架構接上 A2A 之後的樣子。」

   Harness 藍圖包含 identity broker 與受限憑證；Hitachi 第 20 頁仍明列使用者委派需要自行建置。入口位置相似，不代表授權能力相同。

   **修法：**改成「集中入口的位置相近，但端到端委派仍是缺口」。接著比較缺少哪份核准資料、哪個元件應取得並強制檢查它，recall 才有增量。

10. **二＋十、〈References〉：外部文件的描述需要縮小範圍。**

    > 「Anthropic 的做法則偏向後者……最後只交回一份一到兩千個 token 的濃縮摘要。」

    這把一篇工程文章介紹的子 agent 設計，概括成 Anthropic 的整體做法；「只」也把例示長度寫成固定限制。repo 的重新分析紀錄不足以替代完整原文核對。

    **修法：**改成「該文介紹的一種子 agent 設計」。補原文封存與定位後，再決定是否保留長度。SDK 的完整歷史與回呼授權說法，也應保留預設條件、適用版本及精確段落。

11. **九：G2 recall 只剩口號。**

    > 「這也是可靠度篇第五節 G2 閘門問的事：擴張授權要有證據，而不是有感覺。」

    舊文談任務集合、重複表現、觀察期間與複核人力；本文提供的是少數故障案例設計。營運篇又區分擴大團隊使用與高風險操作授權。

    **修法：**明說本篇案例是必要的驗證項目，不能單獨支持擴權。把「某種恢復行為符合契約」與「團隊已準備承擔更多操作」拆開。

12. **以下轉場仍只有題材切換，沒有交出上一段的結果。**

    | 位置與原句 | 斷點與具體修法 |
    |---|---|
    | 一：「這次回頭整理東京行，照片之外……」 | 天候、夜景沒有產生交接問題。縮短旅途文字，用已有 Kong 中斷案例提出「下一個接手者怎麼知道做到哪裡」。 |
    | 二：「把這些設計放在一起看……」 | 將 SDK 切換與子任務回報直接合併。先說它們差在哪裡，再提出共同的證據問題。 |
    | 四：「對工具採用也要保留時間點。」 | 從核准疲勞突然跳到未公開工具。移入資料註記。 |
    | 五：「工具本身也會改變結果。」 | kubeadm 版本失配另起一題。補「接手者還必須取得哪版工具，才能照原計畫繼續」。 |
    | 五結尾 → 六開頭 | 已談完驗收，突然換成持久儲存。補問：這些評估、核准與結果在環境消失後，哪些還找得到？ |
    | 七：「記憶則有不同的時效問題。」 | 從並行衝突轉去 mem9，沒有承接結果。縮成第三篇入口。 |
    | 七結尾 → 八開頭 | 從資料機制換到整合選型。補問：上述查核散在不同元件，由誰把它們接成不可繞過的流程？ |
    | 九：「讀完六份材料……」 | 以閱讀經過重新開場。直接承接第八節：現在用哪個中斷案例檢查整條責任鏈？ |

## 次要問題

1. **三、〈通訊許可要與行動授權分開核對〉：講者課次編排不準。**

   > 「第二課接著來：A2A 告訴我們 agent 怎麼溝通……」

   SoftBank 第 9–12 頁仍屬 Lesson #1；Lesson #2 從第 13 頁開始。改成「由這個定義，他進一步指出」，避免替講者重編課次。

2. **四、〈把帳號能力縮成這次任務的操作範圍〉：危險排名沒有依據。**

   > 「因此最危險的是第三個。」

   外洩、任意程式執行與 CI 劫持誰最危險，取決於憑證及影響範圍。改成「第三個尤其值得注意，因為它能改變後續自動執行的流程」。

3. **五、〈評估認為可行，執行仍要核准〉：y／n 的中文有歧義。**

   > 「只有明確的 y 或 n 才繼續。」

   雖然投影片如此寫，中文容易被讀成 n 也繼續升級。改成「必須明確回答；y 才執行，n 停止升級」。

4. **五、〈從全部節點到服務結果，逐層驗收〉：失敗案例引用錯接。**

   > 「他們的教訓是……升級工具也要一次只走一個小版本。[9]」

   第 30 頁失敗與修正來自 Quartic.ai，應引用 [8]；[9] 用於補充 Kubernetes 規則。分開講者案例與官方政策。

5. **五開頭：Ollama 與模型名稱混用。**

   > 「模型用本機的 Ollama。」

   改成「透過本機 Ollama 執行模型」。投影片沒有因此交代實際模型版本，不能讓讀者以為已具備重現所需資訊。

6. **六開頭：把短命環境當成 sandbox 定義。**

   > 「Sandbox 可以想成臨時租的工作間……退房時整間清空。」

   Sandbox 的重點是隔離與限制；是否短命是生命週期選擇。改成「這場使用的 sandbox，是可隨任務丟棄的隔離工作環境」。

7. **六、〈先分清哪些資料要留、哪些權限要重查〉：錯誤的篇內 recall。**

   > 「這就是第二節說的『憑證不該跟著對話過去』……」

   第二節沒有這句主張，表格還列出交接可能帶過去憑證。刪除引號，改為本節明確提出的設計建議。

8. **八、〈共同元件仍需接上業務條件的檢查〉：保留講者歸屬，也補觀測能力的條件。**

   > 「OpenTelemetry 記錄『為什麼』。」

   這是投影片的概括，不是 OTel 自動提供決策理由。補明：必須有相應埋點與資料關聯，才能重建流程；trace 本身也不是核准證據。

## 建議刪除

1. **一、〈會議之前，先去看一眼東京鐵塔〉：刪天候的重複鋪陳。**

   > 「白天的紅白塔身換成了夜裡的燈色，灰濛濛的天氣倒是一路留到了晚上。」

   這段只有旅行裝飾。兩張照片可以保留，日期、雨夜移到圖說；正文縮短。貼文能支持天氣敘述，不能替照片補出工程上的領悟。

2. **二：刪尚未被後文使用的 SDK 細節。**

   > 「交接時附帶的結構化資料只給回呼函式用，不會改變目的地。」

   後文沒有討論目的地選擇。移入註記；正文留下控制流程切換、可見紀錄與授權檢查三件事。

3. **四、〈把帳號能力縮成這次任務的操作範圍〉：縮減四套情境並排。**

   > 「簡報的四個風險例子都很日常……」

   issue、Terraform、CI、網頁指令一次帶入，讀者尚未回到升級交接就要換四次場景。正文完整分析一例，其餘放簡表或來源註記。

4. **四、〈用允許與越界請求，檢查限制是否生效〉：縮短核准疲勞重述。**

   > 「我在 Review 篇第三節引用過同一張投影片。」

   舊文已展開相同研究與風險。本篇只需交代新增判斷：哪些重複確認改由確定性檢查處理，哪些風險接受仍需要人。

5. **七、〈記憶幫忙找回脈絡，核准仍須回查〉：移走 mem9 的完整流程摘要。**

   > 「用模型抽出值得記住的事實，再決定整合、覆寫或刪除既有事實……」

   這段推進的是第三篇的問題。留「記憶只能幫忙找核准來源」及連結即可。

6. **八、〈三種整合方式，分別把維護責任放在哪裡？〉：縮掉產品名詞巡禮。**

   > 「Directory……OASF……SLIM……Observe……」

   正文用「找人、描述能力、傳話、觀測」帶出維護責任；產品名稱放比較表。現在讀者得先消化產品家族，才讀得到選型判斷。

7. **十、〈結語：留下來的工作，要讓下一個人敢接〉：刪社群宣言。**

   > 「整理成社群材料時，也把原本的預期、失敗切點與修正理由留下來。」

   這是作者出版工作，沒有回答主管如何接手任務。結尾停在一個小任務的中斷演練，以及誰承接尚未釐清的結果。

## 建議補充

1. **TL;DR＋二：固定一個問題，讓三份證據成為它的答案。**

   > 「交出去的到底是什麼？」

   建議改問：「前任不在場時，下一個接手者憑什麼決定繼續、重做或停止？」授權、外部狀態與完成條件分別回答這個決定需要什麼，而非再列三個平行主題。

2. **三至八：各補一個條件改變後的成本或反例。**

   | 節次／H3 與現句 | 還缺的第一性原理推導 |
   |---|---|
   | 三／〈語意檢查還要決定等待、拒絕與接手的時機〉：「等更多內容又會增加延遲。」 | 等待會佔用什麼資源？逾時時哪些動作仍安全？判斷完成前，哪個元件能阻止效果發生？ |
   | 四／〈強制檢查要放在 agent 無法繞過的位置〉：「新增操作也要有人維護。」 | 操作介面愈通用，愈可能重新暴露任意執行；愈專用，維護與例外處理愈多。示範界線怎麼選。 |
   | 五／〈修復之後，重新確認評估與核准〉：「原來的報告描述的是修復前的叢集。」 | 核准對應的是環境的哪些條件？哪些漂移使證據失效？過度重評又會造成多少停滯？ |
   | 六／〈先定義保存承諾，再選擇故障注入的位置〉：「可容許遺失多少已確認的工作。」 | 分析草稿可重建，已送出的操作識別卻可能不能遺失。兩者不宜共用同一個保存承諾。 |
   | 七／〈檔案各自正確，合起來仍可能違反任務要求〉：「協調或序列化……步驟。」 | 協調者故障怎麼辦？前任恢復怎麼辦？鎖住哪一段才足以保護任務要求，又不拖慢唯讀工作？ |
   | 八／〈三種整合方式，分別把維護責任放在哪裡？〉：「集中入口才有維護上的理由。」 | 共用入口也集中故障與政策錯誤的影響。入口不可用時，查詢與變更是否採取不同處置？ |

3. **九：把承諾的義務表實際交出來。**

   > 「交接的驗收也值得一張同樣的表。」

   契約篇已經提供表格；本篇不能停在說值得做。至少填出：

   | 情境 | 接手者可接受的行為 | 驗收者查什麼 |
   |---|---|---|
   | 正常、核准有效 | 完成指定有限操作 | 正確目標、效果與完成條件 |
   | 遠端完成、回覆遺失 | 查明結果後接續 | 沒有新增違約效果 |
   | 請求尚未送出 | 依服務契約決定送出或停止 | 沒有把「查不到」直接當成未執行 |
   | 結果暫時無法查詢 | 停止相依步驟並交接 | 指定接手人、查詢入口與期限 |
   | 計畫改版或核准失效 | 阻止不再獲准的新步驟 | 舊檔沒有恢復舊權限 |
   | 前任恢復、兩者同時行動 | 拒絕前任新增步驟 | 目前接手權由服務判定 |
   | 同一識別帶不同參數 | 拒絕不一致請求 | 沒有沿用其他目標的結果 |
   | worker 尚未完成 | 留下待辦，不宣布整體完成 | 預期清單獨立於執行器回報 |

4. **八、〈讓 task、run 與 tool call 對回同一份授權〉＋九：接回組織篇的責任分工。**

   > 「並留下可追查到負責人的紀錄。」

   「查得到人」還不等於有人接案。組織篇第二節已有 [RACI](/Users/kochi.chuang/conductor/workspaces/medium-articles/dodoma/2026-09-agentic-org-design/article.md:56)：平台負責共用環境與權限，domain team 承擔產品品質與 production ownership。

   **補法：**平台處理操作識別、查詢介面及執行協調；服務 owner 定義業務驗收與風險接受；值班者承接逾時未明結果。列明誰決定恢復、停止或另提補救操作。

5. **五、〈從全部節點到服務結果，逐層驗收〉＋九：把既有 recall 推到它原本未驗證的邊界。**

   > 「我在……測試篇第五節借用過這個失敗。」

   測試篇的引用對得上；付款篇與契約篇的引用也有對應內容。但本篇的新增價值應明列：

   - 測試篇：從「漏查對象」推到「驗收清單不得沿用執行器的漏項」。
   - 付款篇：從同一行程依序重送，推到跨重啟、紀錄保存與服務查詢契約。
   - 契約篇：從說明義務表用途，推到本篇實際填好的恢復驗收表。

6. **一＋十：用已有操作紀錄推動敘事。**

   > 「這兩張照片，替短短的東京行留下了會議之外的記憶。」

   鐵塔照片目前只有氣氛。可用第一篇已記錄的 Kong 情境接問：模擬操作已有結果，後續模型請求卻被限流；若換一個 agent，如何判斷接續位置？保留「返台重讀後提出的問題」這個時間點，別寫成當天已經領悟。邀請與澀谷照片分屬另兩篇，不必搬來補溫度。

## 術語仍難懂的清單

以下列的是仍需就地解釋或調整首次出現位置的詞。

| 位置與原句 | 術語／具體修法 |
|---|---|
| TL;DR：「OpenAI 的 Agents SDK 把 handoff 做成……」 | **agent、Agents SDK、handoff**：先用「評估者把後續執行交給另一個角色」建立情境；補 SDK 是開發套件，切換的是哪段控制流程。 |
| 一：「SoftBank 的 A2A 信任邊界」 | **A2A、MCP**：第三節才解釋，首次使用太早。前移一句，或開場先寫工作委派與工具介面。 |
| 二：「input filter……回呼函式……decentralized pattern……manager pattern」 | 一段堆四個概念。先區分「轉交後自己退出」與「主管收回子任務結果」；其餘移註記。 |
| 二：「乾淨的 context……一到兩千個 token」 | **context、文字 token**：先說子 agent 只收到自己的任務材料；摘要長度沒有必要就刪數字。 |
| 二：「PR 描述裡……」；四：「issue……repo」 | **PR、issue、repo**：本篇獨立閱讀時沒有入口。首次以「程式變更提案」「問題單」「程式庫」帶出。 |
| 三：「Agent Firewall」 | 先用「A 可以聯絡 B，但 B 能否動用帳號仍要另查」說明檢查對象；避免讓名稱暗示已控制所有動作。 |
| 四：「`terraform plan`……provider」 | **Terraform、plan、provider**：解釋來得晚，provider 未解。用「看似只看變更預覽，過程仍會載入外部程式」帶入。 |
| 四：「push……CI……commit……remote」 | 說清「先在本機存版本，再送遠端，遠端觸發自動工作」；別在同段事後集中補詞。 |
| 四：「CLI 包裝工具」；下一個 H3 才解釋 | **CLI、wrapper、hook**：首次就用「同一條操作指令，送出前先經檢查」帶入，並立即指出能否直接呼叫原工具。 |
| 四：「gateway、sandbox 與 secret broker」 | **gateway、sandbox、secret broker、secret reference**：這串最需要拆。分別說誰收請求、誰限制執行環境、誰代取金鑰，以及 agent 手上的 reference 能做什麼。 |
| 五：「controller……webhook……admission webhook」 | 用一個實際升級阻擋情境介紹：某個部署檢查服務不相容，可能讓新工作無法建立。再區分各角色。 |
| 五：「kind……Ollama」 | 說明是本機測試叢集工具與模型執行服務；別把 Ollama 當模型名稱。 |
| 六：「commit point、RPO 與 RTO……`fsync`」 | 遊戲存檔已有入口，但三種承諾仍擠在一起。分清「何時算保存」「容許丟多少」「多久恢復」，再指出不等於遠端操作完成。 |
| 七：「無狀態的 harness」 | **harness、stateless**：先說哪些程式可以重建、哪些任務資料必須另外保存；限定為這個架構的設計。 |
| 七：「租戶與短期的任務 token」 | **tenant、授權 token**：用「不同客戶各有資料範圍；這張一小時通行證只開 `/repo/docs`」帶入，與第二節文字 token 分開。 |
| 七：「copy-on-write 建立的『層』」 | 先說兩個分支各改同一起始檔案，再命名；補清楚隔離哪些資料，以及外部操作仍共用哪些系統。 |
| 八：「Keycloak 的 token exchange」 | 用採購角色換取目標系統接受的受限通行證說明；持有憑證仍不等於這張訂單已核准。 |
| 八：「AGNTCY……OASF……SLIM……Observe」 | 名稱密度過高。正文先講四種問題，產品名稱集中比較表。 |
| 八：「JWT 與 OAuth 2.0」 | 不要只列標準名稱。先說入口驗證憑證來源與適用對象，再說它仍缺少哪份任務核准。 |
| 八：「registry、identity broker 與 audit log」 | recall 仍須自足：工具清冊、受限憑證取得處、操作紀錄各如何支持這次交接。 |
| 九：「這裡需要的冪等性……」 | 綠茶例子放到名稱之前；接著限定同一操作、相同參數與保存期間內的承諾。 |

`skill、digest、compaction、RRF、oracle、holdout` 未在本篇正文作為分析概念使用，不應為湊術語解釋而加入。`permission／intent`、`gate`、`optimistic locking`、`task／run／tool call` 已有可辨識的情境入口；優先修正上表的首次使用與概念堆疊。

<!-- tokens: in 1976304 out 20189 -->
