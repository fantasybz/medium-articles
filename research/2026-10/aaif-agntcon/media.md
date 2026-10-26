# 影片覆蓋與圖片來源

核對日期：2026-10-23。對應 [中文版](../../../2026-11-aaif-after-tokyo/article.md)與[英文版](../../../2026-11-aaif-after-tokyo/article.en.md)。兩版共用 17 張圖片，圖說依語言保留，並附講者、官方來源及時間碼。

## 六支影片怎麼核對

完整自動字幕已讀取，再以 gstack headed browser 從頭連續播放到片尾，保留 HTML media `played` 實際範圍。播放過程擷取全時間軸抽樣畫面，逐張 contact sheet 檢查畫面推進、投影片及 demo 尾段；入稿的指定時間另暫停擷取原尺寸 PNG。自動字幕仍可能有轉錄誤差，數字與技術主張另與畫面、官方規格及其他第一手材料對照。

**這不等同模型獨立聽完全部音訊、人工逐字聽打或逐格視聽複核。** 連續播放範圍是覆蓋證據，不能單獨當成理解證據。文章尾端保留相同的方法限制。五支東京影片與後來觀看的歐洲 Logfire 影片分開標示，不以錄影研究推論作者當時逐場出席。

六支合計 122.30 分鐘；留存 486 張時間軸抽樣畫面、23 張 contact sheets，另有指定時間截圖。以下範圍由實際覆蓋紀錄產生，不以影片長度推測已播放。

| 錄影 | 講者／場次 | 長度 | 實際連續播放範圍 | 抽樣畫面／contact sheets |
|---|---|---|---|---|
| [Why Agents Need Connectivity, Not Better Models](https://www.youtube.com/watch?v=3LwylP2as8A) | David Soria Parra／Tokyo | 12:46 | 0–765.541 秒 | 50／3 |
| [Skills over MCP](https://www.youtube.com/watch?v=3oHLjC3wZNE) | Ola Hungerford／Tokyo | 13:41 | 0–821.261 秒 | 54／3 |
| [How Anthropic uses MCP for its own product](https://www.youtube.com/watch?v=e8DMLtP5ibk) | Camila Rondinini／Tokyo | 23:08 | 0–1387.941 秒 | 92／4 |
| [Build Your Own Open-Source Claude Code With Local LLMs](https://www.youtube.com/watch?v=kwKVe27xnw4) | Daniel Oh／Tokyo | 28:19 | 0–1698.681 秒 | 113／5 |
| [Building a Debugging Agent Harness at Uber](https://www.youtube.com/watch?v=iVCDIOf7vXw) | Kriti Dangi／Tokyo | 29:12 | 0–1752.001 秒 | 116／5 |
| [Why Agent Evals Miss What Production Catches](https://www.youtube.com/watch?v=JzBLYv1BTTM) | Marcelo Trylesinski／Europe | 15:12 | 0–912.301 秒 | 61／3 |

### 覆核後影響正文的發現

- Skills：來源識別、digest 與信任是不同問題；07:36 用可讀的投影片畫面，避免採用只有遠景的時間點。
- Anthropic proxy：約 92% 的分母是觀察到的 server，指其對不同使用者回傳相同 tool list。片尾 RBAC 問答已有重新檢查與失效處理，不能寫成講者未考慮撤權。
- 私有模型：18:20 直接呈現 guardrail 實作項目，不拿脫離條件的 0%／100% 數字當成普遍安全結論。片尾仍在確認建置，28:00 出現編譯錯誤；架構討論不因此變成模型效能比較。
- Uber：slide 14 為約 9,000 RCA／月、50% RCA accuracy、PR merge rate 5%→48%。保留說明欄舊數字的差異，並核對測試重現、限制重試及 subagent 輸入範圍的 Q&A。10,000 subagents 是展望，沒有寫成既有規模。
- Logfire：13:29 起是人工檢視與採用提案；14:10–14:40 說明自動建立 eval 當時仍在開發。Runtime traceback、prompt 改善與自動驗證不是同一項已完成能力。

## 入稿圖片

四張個人照片／邀請函、兩張作者 demo 截圖、十一張官方影片截圖。每張圖片用來支持附近的具體敘事或分析，不把舞台展示與作者介面操作當成生產效果實測。

| 圖 | 檔案 | 日期或時間碼 | 內容與用途 |
|---|---|---|---|
| 01 | [01-tokyo-venue.png](../../../2026-11-aaif-after-tokyo/figures/01-tokyo-venue.png) | 2026-09-10 | 東京會場；識別證 QR code 遮蔽；建立參會現場與封面 |
| 02 | [02-invitation.png](../../../2026-11-aaif-after-tokyo/figures/02-invitation.png) | 2026-08-24 | 邀請函；票券代碼在原圖中已遮蔽；區分邀請方署名、作者道謝對象與自己的玩笑 |
| 03 | [03-departure.png](../../../2026-11-aaif-after-tokyo/figures/03-departure.png) | 2026-09-09 | 出發前的機場停機坪；兩週安排行程、家庭支持與旅行工具的故事 |
| 04 | [04-kong-failover.png](../../../2026-11-aaif-after-tokyo/figures/04-kong-failover.png) | [00:50](https://www.facebook.com/reel/1387275603582551/) | Kong demo 的故障切換；區分路由恢復與任務結果 |
| 05 | [05-kong-budget.png](../../../2026-11-aaif-after-tokyo/figures/05-kong-budget.png) | [02:08](https://www.facebook.com/reel/1387275603582551/) | Kong demo 的 Rate limit enforced / Blocked；搭配固定分支原始碼區分限流、部分完成與模擬紀錄 |
| 06 | [06-keynote-connectivity.png](../../../2026-11-aaif-after-tokyo/figures/06-keynote-connectivity.png) | [04:46](https://www.youtube.com/watch?v=3LwylP2as8A&t=286) | 模型能力與連接的關係；讓讀者理解外部狀態為何不能由模型憑空推得 |
| 07 | [15-skills-three-reads.png](../../../2026-11-aaif-after-tokyo/figures/15-skills-three-reads.png) | [06:10](https://www.youtube.com/watch?v=3oHLjC3wZNE&t=370) | Three reads；分開發現、載入與按需讀取，分析入口描述與內容管理的成本 |
| 08 | [07-skills-identity.png](../../../2026-11-aaif-after-tokyo/figures/07-skills-identity.png) | [07:36](https://www.youtube.com/watch?v=3oHLjC3wZNE&t=456) | skill 識別與內容變更；區分來源、內容完整性與信任 |
| 09 | [08-proxy-refresh.png](../../../2026-11-aaif-after-tokyo/figures/08-proxy-refresh.png) | [06:50](https://www.youtube.com/watch?v=e8DMLtP5ibk&t=410) | token refresh 的協調；說明鎖與重新讀取狀態各解決什麼問題 |
| 10 | [16-proxy-request-log.png](../../../2026-11-aaif-after-tokyo/figures/16-proxy-request-log.png) | [17:00](https://www.youtube.com/watch?v=e8DMLtP5ibk&t=1020) | One structured log per request；以完整請求脈絡定位上下游與錯誤層級 |
| 11 | [09-local-architecture.png](../../../2026-11-aaif-after-tokyo/figures/09-local-architecture.png) | [10:50](https://www.youtube.com/watch?v=kwKVe27xnw4&t=650) | 私有 coding assistant 架構；把模型位置與工具可達範圍分開分析 |
| 12 | [10-local-guardrails.png](../../../2026-11-aaif-after-tokyo/figures/10-local-guardrails.png) | [18:20](https://www.youtube.com/watch?v=kwKVe27xnw4&t=1100) | Implementing the Guardrails；公平呈現講者已有控制，進一步說明驗證方法 |
| 13 | [11-uber-investigation.png](../../../2026-11-aaif-after-tokyo/figures/11-uber-investigation.png) | [11:25](https://www.youtube.com/watch?v=iVCDIOf7vXw&t=685) | Under the Hood — Agent Pipeline；把固定蒐集、根因推理、修補與測試接成可交接的流程 |
| 14 | [12-uber-results.png](../../../2026-11-aaif-after-tokyo/figures/12-uber-results.png) | [19:55](https://www.youtube.com/watch?v=iVCDIOf7vXw&t=1195) | Impact，slide 14；保留團隊自述數字與不同指標的分母界線 |
| 15 | [13-logfire-feedback.png](../../../2026-11-aaif-after-tokyo/figures/13-logfire-feedback.png) | [08:55](https://www.youtube.com/watch?v=JzBLYv1BTTM&t=535) | 生產 trace 與錯誤細節；從執行材料找新問題，與驗證提案效果分開 |
| 16 | [17-logfire-prompt-diff.png](../../../2026-11-aaif-after-tokyo/figures/17-logfire-prompt-diff.png) | [13:40](https://www.youtube.com/watch?v=JzBLYv1BTTM&t=820) | 兩項 prompt 差異；區分要求優先順序與 offer_id 語意錯誤 |
| 17 | [14-goodbye-shibuya.png](../../../2026-11-aaif-after-tokyo/figures/14-goodbye-shibuya.png) | 2026-09-12 | T-shirt、Kubestronaut 外套與伴手禮；回到旅程尾聲與未完成的晨跑 |
| 18 | [18-pagerduty-hire.png](../../../2026-11-aaif-after-tokyo/figures/18-pagerduty-hire.png) | 官方簡報第 14 頁 | H.I.R.E. 四個檢查面向；2026-10-25 新增，說明僱用決定的檢查順序 |
| 19 | [19-pagerduty-pipeline.png](../../../2026-11-aaif-after-tokyo/figures/19-pagerduty-pipeline.png) | 官方簡報第 25 頁 | 三步驟評估流程與「evaluate the evaluator」；2026-10-25 新增 |

## 編輯與保留方式

會場照只遮蔽識別證 QR code，邀請函沿用原圖已遮蔽的票券代碼。其他照片只轉為 PNG，影片圖保留原畫面，未以生成圖片補造現場、重繪投影片或修改指標。圖片尺寸、SHA-256、來源、時間碼與轉換紀錄見 [media-manifest.json](media-manifest.json)；發布包由原稿重新產生，圖片以 byte-copy 保留相同內容。

Facebook 貼文的完整擷取、留言與互動者資訊、瀏覽器 session、完整字幕及全片抽樣畫面保留在 gitignored `.context/`，不隨文章匯出。正文只使用作者要求整理的自身經歷及選定圖像。2026 年 10 月 24 日依作者補充，邀請、出發、會場與告別澀谷的原貼文連結補入相應敘事及 References，圖片索引同步記錄來源網址；Kong 操作錄影也保留原貼文入口。未找到可支撐此邀請的七月紀錄，因此沒有補寫七月受邀故事；十月另一場活動邀請也沒有混入。

封面為第一張東京會場照片。原先六篇的素材保留於私有歷史目錄，正式使用清單以本檔與 manifest 為準。

## 第三篇的照片與投影片

2026-10-24 完成的第三篇另使用三張筆者照片：9 月 11 日澀谷夜景與 SHIBUYA SKY 展景，以及 9 月 10 日自主研究驗證的會場照。三張均核對相簿日期與畫面後，保存為乾淨的顯示畫面擷取；它們不是相機原始檔，也沒有保留私人相簿網址或帳號資訊。

另有 CrabRAG p28、Agent Memory s11／s28、自主研究 p35 四張完整投影片轉圖，以及中英各一張驗收比較表。研究方法、逐圖用途與轉圖方式見 [memory.md](memory.md)，尺寸、來源與雜湊見 [memory-media-manifest.json](memory-media-manifest.json)。這三場尚未確認相符的東京錄影，沒有計入本檔前述六支影片的覆蓋數量。

## 2026-10-25 的補充

依作者要求補入 PagerDuty 的場次：[錄影](https://www.youtube.com/watch?v=a7PuFJzgwGg)於 10 月 19 日上線（22:39），自動字幕兩次下載都回 HTTP 429，瀏覽器的字幕面板亦無段落，因此正文依官方簡報全文與影片章節時間碼引用，沒有逐字引用口述；兩張簡報圖以 pdftoppm 110 dpi 轉圖，來源與雜湊見 [media-manifest.json](media-manifest.json)。同日以 `yt-dlp --flat-playlist` 核對 AAIF 頻道 238 支影片的上傳日期與說明欄，東京場次已有錄影者共七場，詳見 [rewrite-2026-10-25.md](rewrite-2026-10-25.md)。
