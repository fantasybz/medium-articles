# 第二篇：授權、狀態與復原的證據與推導

研究日期：2026-10-23。中文原稿：[把工作交給另一個 Agent 之前](../../../2026-11-aaif-agent-handoffs/article.md)；[英文版](../../../2026-11-aaif-agent-handoffs/article.en.md)。

這篇回答獨立問題：工作跨 agent 或跨重啟環境後，接手者如何知道現在可以做什麼、已經發生什麼，以及何時算完成？第一篇沿著 crash 調查處理連接、程序與交付；第二篇沿著假設的 Kubernetes 升級，處理委派、狀態時效、持久化與並行。沒有把第一篇的六支影片再拆成六篇。

## 來源與證據邊界

以下頁碼都是 PDF 從 1 起算的頁序。原始檔案、SHA-256、檔案格式與下載結果見 [簡報清單](slides.md)及 [JSON](slides-manifest.json)。完整文字擷取保存在 `.context/research/aaif-2026-10-23/slides/text/`，引用圖片保留原頁內容。

| 場次 | 本文使用的材料 | 可以支持的判斷 | 不可擴大的結論 |
|---|---|---|---|
| [Ryuji Iijima／SoftBank](https://sched.co/2RCwp) | p6、12–16：A2A v0.3 PoC、通訊與信任邊界、串流判斷、確定性／語意檢查 | 可連線與可執行下游操作，需要不同控制；串流檢查要定義時機與失敗行為 | PoC 排除 MCP 工具、資料存取與完整平台；沒有防護效果 benchmark |
| [Masaya Nakamura／Studist](https://sched.co/2QlDX) | p30–34、38–42、48–49、58–63：帳號能力、任務意圖、wrapper 旁路與外部強制控制 | 任務範圍通常小於帳號能力；控制須在 agent 無法任意修改的邊界生效 | `safe-terraform` 在 p42 標為當時未公開；沒有宣稱全部工具已可安裝或已重跑 |
| [Sanskar Agrawalla、Abhijeet Chaudhuri／Quartic.ai](https://sched.co/2QlD9) | p14、17、19–24、27、29–30：分階段流程、四種 gate、唯讀 collector、逐節點驗證、工具版本失敗 | 建議、核准與完成各需不同證據；UNKNOWN 要保留；修復後重評；驗收涵蓋目標全部節點 | p17 是 kind／local Ollama PoC；不是作者生產升級實測；核准雜湊／時效為作者建議 |
| [Rui Su／Juicedata](https://sched.co/2QlE7) | p3–8、9–13：六種狀態、資料與控制分離、commit point／RPO／RTO、故障注入 | 檔案保存不能替代外部狀態與有效核准；不同狀態需不同保留／復原政策 | 設計指引，不是已量測的持久性或復原時間保證；作者故障測試尚未執行 |
| [Tadatoshi Sekiguchi／PingCAP](https://sched.co/2QlEe) | 英文 p12–13、20–23：mem9、drive9、非同步上傳、任務 token、版本衝突檢查 | 檔案可見、遠端持久化、同版寫入與任務衝突是不同問題 | 本文沒有審查當前 repo 或重現服務；記憶內容不能代替即時核准 |
| [Tatsuya Sato、Satoshi Ito／Hitachi](https://sched.co/2QlEG) | p17–20、23–26：採購流程、直接整合／AGNTCY／agentgateway、E2E 缺口 | 元件功能不會自動組成完整委派與驗收；識別關聯需跨 task／run／tool call | 技術圖截至 2026-08-20；偶發未核准訂購沒有完整分母，不當普遍失敗率或永久產品排名 |

[Kubernetes 升級文件](https://kubernetes.io/docs/tasks/administer-cluster/kubeadm/kubeadm-upgrade/)與[版本偏差政策](https://kubernetes.io/releases/version-skew-policy/)已另行讀取。它們支持 kubeadm 不支援跳過次要版本、各元件容許偏差不同，以及完成後需檢查所有節點的說明。正文沒有把特定 kubeadm 路徑外推到全部託管服務。

## 從第一性原理推到驗收

1. 收到訊息只能證明訊息抵達。接手服務可能持有較大能力，所以任務的授權範圍必須被明確傳遞與重新檢查。
2. 判斷依賴某一刻的材料。叢集、計畫或核准條件改變後，原判斷未必仍適用，因此核准需對應具體對象與版本。
3. 本機紀錄與外部行動有不同提交時刻。中斷後必須查明完成、失敗與未知，不能只因檔案寫著完成就跳過，也不能因回應遺失就全部重做。
4. 防止同一檔案被過期內容覆寫，只處理一種衝突。多檔案、同一外部資源與已送出的操作，仍需要工作層的協調與查詢。
5. 驗收證據只涵蓋實際觀察範圍。control plane 達標無法代表全部 worker；基礎設施 Ready 也不代表每個業務要求成立。

第八節的中斷交接與故障條件是設計情境，不是執行紀錄。平台工程師負責操作與復原邊界，服務負責人定義業務條件，reviewer 檢查驗收是否涵蓋要求。結論支持從有限工作開始，再依證據擴大自動化。

[第三輪精修](refinement-3-runs.md)另補明測試條件：接手 agent 不能讀取驗收裝置私下記錄的故障時刻；操作識別要在送出前持久保存；「查不到」須依服務的可見性、保留期限與重送契約解讀。取得新憑證和重新取得任務核准也分開驗證。這些都是設計前提，沒有聲稱所有 Kubernetes 工具已提供相同能力。Quartic.ai 的失敗則依原頁保留「只檢查第一台節點」，不將三台未升級 worker 寫成驗收恰好涵蓋另一半。

## 圖片與閱讀方式

開場加入 9 月 9 日快閃東京辦公室與東京鐵塔夜景的兩張筆者照片，從旅途日常接回會議分頁。兩則原貼文的日期、文字及照片已核對，詳見[標題與開場修訂](title-opening-refinement.md)。JPEG 轉為原尺寸 PNG，沒有裁切、調色或添加畫面；本篇共十張圖片。

八張完整投影片轉成 1920 px 寬 PNG，沒有裁切或修改內容：SoftBank p12／15、Studist p58、Quartic.ai p21／29、Juicedata p5、PingCAP p23、Hitachi p24。已逐張視覺檢查可讀性與來源標示；中英文共用原圖，各自保留圖說。逐圖雜湊見 [handoffs-media-manifest.json](handoffs-media-manifest.json)。

本篇閱讀六份簡報的完整文字，對引用頁面做視覺核對；沒有宣稱重新看完六個場次的錄影。這與第一篇六支錄影的完整字幕／時間軸抽樣檢視方法不同。保存的 Chrome 分頁只能證明資料線索，不作逐場出席證明。
