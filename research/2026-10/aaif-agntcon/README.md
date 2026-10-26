# AAIF 東京筆記：行動、交接與記憶的證據

研究日期：2026-10-23～24。依作者方向，先把原先六篇薄短規劃整併為完整長文，再從另六場簡報提出第二篇，接著以記憶與可信結論的三場材料寫成第三篇。三篇各有中英版本，沿用 [STYLE.md](../../../STYLE.md) 的因果分析、概念引介與完整交接標準；六版均已排程，尚未公開。

- 第一篇〈從東京 AGNTCon 回來：Agent 接上工具之後，工作才剛開始〉：[中文](../../../2026-11-aaif-after-tokyo/article.md)、[英文](../../../2026-11-aaif-after-tokyo/article.en.md)。2026-10-25 改寫後為 12 節、21 張圖（19 張來源圖、一張總覽、一張閱讀地圖表），包含邀請與旅程、Kong 原始程式碼、七場錄影、PagerDuty 場次、跨來源研究及與既有系列的回扣。
- 第二篇〈把工作交給另一個 Agent 之前：授權、狀態與復原〉：[中文](../../../2026-11-aaif-agent-handoffs/article.md)、[英文](../../../2026-11-aaif-agent-handoffs/article.en.md)。2026-10-25 改寫後為 10 節、12 張圖，以「交接帶過去的與仍要重查的」串起 SoftBank、Studist、Quartic.ai、Juicedata、PingCAP、Hitachi 的場次。
- 第三篇〈Agent 記住的經驗，下一次還能相信嗎？〉：[中文](../../../2026-11-aaif-agent-memory/article.md)、[英文](../../../2026-11-aaif-agent-memory/article.en.md)。2026-10-25 改寫後為 7 節、12 張圖，包含五張作者照片、四張投影片、兩張表及一張總覽，串起 CrabRAG、Agent Memory 與自主研究驗證；開場保留三張澀谷照片。
- 已排程時段：第一篇中文 11/02、英文 11/04；第二篇中文 11/09、英文 11/11；第三篇中文 11/16、英文 11/18。皆為 2026 年 09:00 Asia/Taipei（UTC 01:00），錯開既有週二／週四發文。
- 三篇開場都附[系列總覽](overview/README.md)，另有中英獨立分享 PNG、SVG、Mermaid 與 HTML 來源，連接行動、交接及記憶三個問題。
- 實際發布狀態以[發布紀錄](publication.md)與各語言的 `PUBLISHED.md` 為準。排程稿不計為已公開作品。
- 依作者對敘述與深度的回饋，兩篇中英文另完成[三輪精修](refinement-3-runs.md)：敘事與決策、逐場機制與反例、全文及雙語精確性。這是三輪編修，不是獨立模型審稿。
- 接續完成[場次小標與開場修訂](title-opening-refinement.md)，小標改由內容帶頭，第二篇加入快閃東京辦公室與東京鐵塔的日夜照片。
- 10/24 再完成[場次分段與術語解說](session-structure-refinement.md)：13 場分析各有 2～3 個小標與一句收束，並補足 A2A／MCP、token、Kubernetes 節點及復原等概念首次需要時的說明；中英文同步核對。

- 2026-10-25 依作者試讀回饋，由 Claude 依同一批來源[重新分析並改寫三篇](rewrite-2026-10-25.md)：每篇先立主軸與閱讀地圖，術語改用情境例子帶入，查核限制集中到文末，補入 PagerDuty 場次與 OpenAI、Anthropic、AI Engineer 的交叉參考，並加深與既有系列的回扣。改寫後再由 Codex（gpt-6.1-sol，xhigh）對中文稿做三輪審稿，每輪核對來源後修訂，原話存於 `codex-review-<dir>-r{1,2,3}.md`，採用與不採用的項目記在同一份重新分析紀錄。六份排程稿已於 2026-10-26 就地重灌（Post ID 與排程不變），重灌重設掉的封面與預覽摘要同日已改回並讀回確認，見 [publication.md](publication.md)〈2026-10-26 重灌〉與各篇 `PUBLISHED.md`。
- 同日接續完成[場次導讀與來源註記](reader-entry-refinement.md)：13 段分析先介紹講者與主題，段內附官方議程及已確認的錄影，未確認錄影的場次附簡報。Kong 的版本、模擬方式與靜態核對範圍集中到文末，正文保留限流範圍等影響判斷的條件。

## 三篇的核心問題與第一性原理

Agent 能取得工具之後，團隊還需要哪些依據，才願意讓它多做一步？文章沿用同一個假設的 App crash 調查，從四個可檢查的前提出發：模型不知道外部系統此刻的狀態；工具呼叫可以改變外部狀態；跨系統操作不會自動一起成功；一份觀察只能支持其涵蓋條件內的判斷。

因此各節依次追問：取得能力與獲准行動如何區分；程序更新為何會改變授權行為；為何逾時不能證明操作失敗；私有推論能控制哪些資料流；重現、合併與事故消除需要什麼不同證據；生產 trace 如何支持下一輪改善。最後收束成暫緩 rollout、接受修補，以及更新共用程序三個決策時刻，各自交代證據與負責的人。這是作者的分析與導入建議，不是 AAIF 制定的標準。

第二篇改問：工作交給另一個 agent 或在重啟後恢復時，接手者如何知道現在仍獲准什麼、外部已經發生什麼，以及什麼才算完成？以明示的 Kubernetes 升級假設案例串起六場簡報，分開通訊權限、當次操作意圖、核准時效、檔案與控制狀態、並行修改及結果驗證。其論證與逐頁依據另見 [handoffs.md](handoffs.md)。

第三篇沿用這個升級例子，再問舊經驗能支持下一次決策到哪裡。模型輸入與人的查核時間有限，摘要必須選擇；環境、資料與授權又會改變，因此來源、適用條件與更正必須跟著記憶保留。三場各有導讀、三個小標及一句判斷，最後提出尚未執行的六種唯讀驗收案例。固定版本程式碼、三輪編修、實際 MCP 結果與圖像來源見 [memory.md](memory.md)及 [memory-media-manifest.json](memory-media-manifest.json)。

## 六支錄影

| 錄影 | 完整字幕 | 正文用途 |
|---|---|---|
| David Soria Parra — [Why Agents Need Connectivity, Not Better Models](https://www.youtube.com/watch?v=3LwylP2as8A) | 12:46，290 段 | 外部狀態與互通需求；展望與實測分開 |
| Ola Hungerford — [Skills over MCP](https://www.youtube.com/watch?v=3oHLjC3wZNE) | 13:41，338 段 | 程序、身分、digest 與採用更新的責任 |
| Camila Rondinini — [How Anthropic uses MCP for its own product](https://www.youtube.com/watch?v=e8DMLtP5ibk) | 23:08，515 段 | refresh 競爭、狀態未知、快取與當下授權；開場投影片題為 Running an MCP Proxy at Scale |
| Daniel Oh — [Build Your Own Open-Source Claude Code With Local LLMs](https://www.youtube.com/watch?v=kwKVe27xnw4) | 28:19，605 段 | 推論位置與執行權限；guardrails 的可觀察驗證 |
| Kriti Dangi — [Building a Debugging Agent Harness at Uber](https://www.youtube.com/watch?v=iVCDIOf7vXw) | 29:12，676 段 | context collection、RCA、mitigation、測試與修補交接 |
| Marcelo Trylesinski — [Why Agent Evals Miss What Production Catches](https://www.youtube.com/watch?v=JzBLYv1BTTM) | 15:12，117 段 | 生產回饋、取樣偏差、人類套用與版本回復限制 |

前五支為東京材料，最後一支為後續觀看的歐洲場錄影。不推論作者現場聽完東京每一場，也不聲稱參加歐洲活動。影片以完整自動字幕、全時間軸抽樣畫面與引用位置畫面核對，包含片尾與有提供的 Q&A；這不等同模型獨立聽完全部音訊或逐格視聽複核。方法與截圖見[媒體紀錄](media.md)。

10/24 另確認 SoftBank〈Designing Trust Boundaries for Agent-to-Agent Systems〉的官方錄影 [Agent-to-Agent Systems](https://www.youtube.com/watch?v=IO6CFh_lRGw)，已補為第二篇的觀看入口。第二篇分析仍以六份簡報為依據，這次新增連結不代表完成第七支影片的全片複核；其餘五場尚未確認相符官方錄影。議程與錄影題名的對照見[本輪來源紀錄](reader-entry-refinement.md)。

## 素材與交付

第一篇的 17 張來源圖片由四張旅程／邀請照片、兩張作者展示錄影截圖，以及十一張官方演講畫面組成。第二篇有兩張筆者東京鐵塔原照與八張公開簡報原頁，分別承接旅途故事與各節需要解釋的機制；兩篇各另有一張系列總覽。照片與技術畫面均有敘事或推論用途；識別證 QR code 已遮蔽，票券代碼原圖已遮蔽。

第三篇有五張筆者照片的乾淨顯示畫面擷取及四張完整投影片轉圖，另有一張驗收比較表及一張系列總覽，中英文分別算繪。兩張 PPTX 引用頁保留完整內容、連線與頁碼。尚未確認這三場相符的東京錄影，文章以簡報與固定版本文件為據；同名的會前影片沒有被當作東京場次。方法與日期見[第三篇來源紀錄](memory.md)。

會議附件及 Chrome 留存的不同版本共保存 41 份（36 PDF、4 PPTX、1 Keynote），逐檔核對大小與 SHA-256。[下載索引](slides.md)記錄來源、覆蓋範圍與未能下載的 ADK Google Slides。原始檔與整包 ZIP 留在本機 `.context/`，公開研究目錄只保留來源清單。

[證據帳本](evidence.md)、[論證大綱](outline.md)、[多來源與跨篇回看](multisource.md)、[審閱紀錄](review.md)、[貢獻與申請對照](contributions.md)分別記錄依據、推導、研究覆蓋、限制與作品用途。私人貼文原文、社團資料、登入狀態、完整字幕及操作日誌只留 `.context/`。

六篇舊稿已移入本機封存，七份已建立的舊 Medium 草稿均先取消排程。第一篇沿用其中兩個既有 ID，其餘五份維持未排程；第二、三篇另建各自的中英版本並排程。舊批次發布程式保持暫停。沒有改變既有系列的發文時段，也沒有代送 Ambassador 申請。
