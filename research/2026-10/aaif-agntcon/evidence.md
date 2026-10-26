# 證據帳本與修正紀錄

核對日期：2026-10-23。此檔整理公開來源；逐字稿、原始頁面、作者私人筆記與截圖保存在忽略版本控制的 `.context/research/aaif-2026-10-23/`。

## 必須保留的修正

1. **Uber 數字以影片與 slide 14 為準。** [19:27–20:37](https://www.youtube.com/watch?v=iVCDIOf7vXw&t=1167)：團隊自述約 9,000 RCA／月、RCA accuracy 50%、PR merge rate 5%→48%。舊議程／影片說明仍為 5,000 與 5%→30%。不同材料不能拼接成同一實驗。Slide 的約 2 倍是 fixed resolution 指標，不能改寫為解決時間減半。未提供完整取樣期間、判定方式或基準控制，不推論為 MCP 的因果效果。
2. **不能把 Uber 的 50% 與 40% 相加。** [19:46](https://www.youtube.com/watch?v=iVCDIOf7vXw&t=1186) 的 40% 接在 remaining 50% 之後。分母與「方向有幫助」的判準不足，本文不換算總成功率。
3. **Skills over MCP 已有正式 extension。** [官方 overview](https://modelcontextprotocol.io/extensions/skills/overview) 現列 SEP-2640 Final；SDK／host 支援仍在實作。演講描述提案過程，不能直接當現在的支援矩陣。
4. **Proxy 演講有回應 RBAC。** [21:49–22:32](https://www.youtube.com/watch?v=e8DMLtP5ibk&t=1309) 明講權限變更應有重新檢查／失效機制。約 92% 的分母是其觀察到的 server；它們對不同使用者回傳相同 tool list，並非可以忽略使用者授權的通則。
5. **本機場次沒有忽略安全。** [15:51–19:20](https://www.youtube.com/watch?v=kwKVe27xnw4&t=951) 明列秘密資料、指令、程式碼與政策控制；本文延伸成如何驗證，不能以稻草人方式批評講者。
6. **Logfire 的 human review 與未來功能有界線。** [13:29–14:40](https://www.youtube.com/watch?v=JzBLYv1BTTM&t=809) 人工套用提案；自動產生 eval 在演講時尚未正式上線。不能從舊錄影推論 10 月的產品支援狀態。
7. **AAIF 的專案清單會變。** [首頁](https://aaif.io/) 於本次讀取列十個專案，不能沿用九月的五個。[OpenSandbox 官方文章](https://aaif.io/blog/the-sandbox-as-an-agent-primitive) 日期為 2026-10-22；本文只談目前可核對的專案關係，不聲稱所有個案公司或工具都是 AAIF 專案。

## 來源與可使用的主張

| 來源 | 支持 | 限制與本文用法 |
|---|---|---|
| [MCP architecture](https://modelcontextprotocol.io/docs/2026-07-28/learn/architecture) | host、client、server 的責任分工 | 不推論為商業結果保證；本文的決策框架為作者分析 |
| [MCP Skills overview](https://modelcontextprotocol.io/extensions/skills/overview) 與其 specification | 發現、讀取、來源識別、manifest、檔案 digest、啟用與核准 | server＋URI 才是身分；digest 不證明可信；實際 host 支援須驗證 |
| [Agent Skills](https://agentskills.io/specification) | 可攜的指示、腳本與參考材料格式 | 與 MCP 的傳輸／發現 extension 分開 |
| [SkillsBench v1](https://arxiv.org/html/2602.12670v1) | curated skills 在受測設定的平均增益 16.2 個百分點；有負向任務 | 摘要寫 86 tasks，methods／圖表為 84 evaluated；有 16/84 負向結果。不是 MCP transport 實驗，不搬用為個別系統提升承諾 |
| [Evaluating AGENTS.md v1](https://arxiv.org/html/2602.11988v1) | 開發者撰寫與自動生成 context files 結果不同；有成本負擔 | 不說所有 AGENTS.md 都有害；repo-wide context 與按需 skills 是不同處置 |
| [MCP caching 2026-07-28](https://modelcontextprotocol.io/specification/2026-07-28/server/utilities/caching) | private cache 的 auth context 邊界、public 的適用條件、ttlMs、失效限制 | TTL 是新鮮度提示；每次 tool 執行仍有存取控制；私有快取不可跨不同 token 共用 |
| [MCP authorization 2026-07-28](https://modelcontextprotocol.io/specification/2026-07-28/basic/authorization) | HTTP 授權角色與 CIMD | 自動字幕 SIMD 誤辨；stdio 與 HTTP 授權不能混寫 |
| [RFC 9700 §4.14](https://www.rfc-editor.org/rfc/rfc9700.html#section-4.14) | rotation、refresh token replay detection、綁定 scope/resource | public client 的 MUST 與 confidential client 要求有別；不把特定供應商 grace policy 當標準 |
| [Redis distributed locks](https://redis.io/docs/latest/develop/clients/patterns/distributed-locks/) | 租約有效期與失效條件、唯一持有者、fencing 建議 | lock 不能原子提交遠端服務與本地儲存；遺失 rotation 回應是作者 failure analysis，非講者披露事故 |
| [OpenCode permissions](https://opencode.ai/docs/permissions/) | allow／ask／deny、規則與模式 | 不把一份指示檔當 OS 隔離；工具版本影響行為 |
| [goose permissions](https://goose-docs.ai/docs/guides/managing-tools/goose-permissions/) | 模式、預設及 read/write 分類限制 | 分類有模型判斷成分；不宣稱提供完整隔離 |
| [AGENTS.md](https://agents.md/) | 專案說明與開發指引格式 | 不能單靠文字阻擋系統呼叫 |
| [Claude Code sandboxing](https://www.anthropic.com/research/claude-code-sandboxing) | 檔案系統與網路隔離應共同考慮 | 某工具實作示例，非所有本機模型的共同保障 |
| [Infrastructure noise](https://www.anthropic.com/research/infrastructure-noise) | 同模型／harness 的資源設定也能改變 eval | 受控 Terminal-Bench 2.0 結果不能直接推論 OpenCode 與其他模型優劣 |
| [Demystifying evals](https://www.anthropic.com/research/demystifying-evals-for-ai-agents) | outcome、trace、grader、任務與重跑的區分 | eval 能回答的問題受環境和判準限制 |
| [OpenTelemetry sampling](https://opentelemetry.io/docs/concepts/sampling/) | head/tail sampling，選擇保留錯誤或慢請求 | 保留下來的 trace 比例不能直接當全量失敗率 |
| [Logfire prompt optimization](https://pydantic.dev/articles/logfire-prompt-optimization) | 生產 trace 帶出改進、人審、可能退步 | 小展示無法支持「eval 無用」；產品已承認 regression/canary |
| [Managed Variables](https://pydantic.dev/docs/logfire/manage/managed-variables/) | 不可變版本、可移動 label、分流與 fallback | 變數回復不會撤銷外部操作；fallback 仍須驗證 |
| [Logfire MCP](https://pydantic.dev/articles/debugging-production-with-logfire-mcp-and-cursor) | 透過 MCP 讀取觀測材料 | 讀取觀測資料與寫入行為政策是不同權限 |

## 個別影片的閱讀路徑

- Keynote：0:25–4:48 連接的角色；6:19–10:46 stateless、快取、tasks、skills、identity；10:47–12:37 對 server 品質和社群參與的邀請。前段「一兩個月」為預測，不當已驗證事實。
- Skills：1:48–4:16 工具能力與程序知識；5:20–7:55 discovery、漸進式讀取、URI、digest；8:15–10:54 提案過程與最小核心。
- Proxy：5:38–8:24 refresh race；13:54–15:00 tools/list 快取；15:03–17:29 錯誤層級；21:49–22:32 RBAC。
- Local：10:18–12:58 私有模型架構；15:51–19:20 guardrails；20:49 起 Java／Quarkus 示範，片尾仍在確認建置，28:00 畫面出現編譯錯誤。沒有可靠的安全性或品質比較結果。
- Uber：9:07–10:40 確定性 context collection；10:44–12:59 RCA／子代理；13:28–14:09 mitigation；14:20–15:11 validate→PR；15:14–17:47 harness／skill 分工；23:04–24:48 測試與重試的 Q&A。
- Logfire：2:07–5:07 行程重排展示；7:06–9:21 建議與執行環境修正；9:29–10:25 managed variables；12:30–13:21 MCP；13:29–14:40 人工套用與尚未正式提供的 eval generation。

## 不採用的延伸

不使用未能核實的「42% 開發時間」「全球 3,000 億美元」當文章主張；不把 tool-list 相同當權限相同；不把合併率當事故消除率；不把更新 prompt 當程式缺陷修復；不把所有 trace 都視為可公開訓練資料；不把文章數量當 Ambassador 錄取條件。

## 個人故事與圖片的證據界線

8/24 邀請函、9/9 出發貼文、9/10 會場與 Kong 展示、9/12 告別澀谷，支持旅程的時間與當時明述的動機。七月沒有找到足以支持本次邀請的材料，不補造更早的邀約；十月另一個活動的邀請不混入東京故事。私人內容只轉述作者自身經驗，照片去除票券／識別證敏感資訊，不刊出留言、反應名單或孩子姓名。

Kong 操作錄影截圖支持介面顯示 failover 與 Rate limit enforced／Blocked，不證明外部 PR、通知、完整計費或生產治理效果。原貼文附的 GitHub 專案於 10/23 公開查閱回傳 404；後續依作者指定的 Chrome 工作坊群組找回 `fantasybz/AI-data-Path-demo`，完成 `read-readme` 分支固定 commit `2c945fe4ad3ffc4ec65558579439dc9d06c90ebe` 的靜態核對。這取代早期「原始碼未取得」的結論，但沒有證明錄影當時跑的是同一個 commit。逐圖來源與影片覆蓋見 [media.md](media.md)。

## 後續深入核對

Kong 分支日期為 2026-09-10T22:27:33+09:00。`base-config.yaml` 的 orchestrator／subagent 模型池為 GPT-4o → GPT-4o mini，摘要模型池方向相反；不要把預設分支 README 的多供應商範例套到此分支。Failover 透過固定 503 模擬器觸發。`rate-limited` 情境對 `github-writers` 設定 2,000 total tokens／40 秒，以 `x-analysis-id` 分區；這不等於全任務金額預算。Playbook 保留 PR 工具成功後再遇到模型 429 的路徑。`CREATED_PRS` 與 `SENT_NOTIFICATIONS` 是記憶體模擬紀錄，沒有建立外部 PR 或送出客戶通知。

第一篇已將 keynote 與 Skills 分開深入討論，新增三次讀取、manifest／dynamic、結構化請求紀錄與 Logfire 兩項 prompt 差異。Logfire 的明確旅客期限和 `offer_id`／`route_id` 錯用屬於不同缺陷；fallback 重新引入舊行為是作者分析，不是講者披露事故。

第二篇採用其他六場公開簡報，完整頁碼、推導與限制見 [handoffs.md](handoffs.md)。官方議程附件與額外材料的下載覆蓋見 [slides.md](slides.md)，下載完整不等於對每一份簡報都完成視覺審閱。
