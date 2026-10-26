# 場次導讀與來源註記修訂

日期：2026-10-24。接續[場次分段與術語解說](session-structure-refinement.md)，依作者試讀回饋處理兩個問題：Kong 分析常被查核限制打斷；各場分析對第一次接觸材料的讀者，缺少簡短介紹與直接觀看來源的入口。

## Kong 的閱讀順序

正文沿著模型故障切換、用量限制、部分完成與接續工作展開。固定版本日期、兩份設定的差異、模擬紀錄的保存方式與本次靜態核對範圍，集中到 References 後的「Kong 展示的資料註記」，中英文對應。

會改變機制判讀的資訊仍在首次使用時交代：工具寫入模擬 PR 與通知、固定 HTTP 503 如何觸發切換，以及 2,000 total tokens／40 秒只約束 `github-writers` 群組。費用分析接著說明，控制整個任務的花費還需要合併其他角色用量與模型單價。正文不再反覆插入可用性保證或沒有完成生產部署的提醒。

筆者午休操作錄影與固定版本程式碼放在開場段內，另依作者補充加入 [AI-data-Path-demo 專案首頁](https://github.com/fantasybz/AI-data-Path-demo)，讓讀者自行延伸。Kong／Mirantis 的〈The Production Gap〉標為同日相關場次；下午演講的議程不能證明午休展示用了同一個執行版本。

## 各場導讀與來源入口

兩篇共 13 段場次及實作分析，先介紹講者、主要問題與內容，再進入原有小標與推論。13 段中英對應的 2～3 個小標與收束句全部保留；除 Kong 的連貫性調整及專案首頁入口外，各場第一個小標以後的分析未改動。標題、個人故事的敘述與圖片順序保留，並在敘事及 References 補齊七個 Facebook 原始來源入口，涵蓋邀請、旅途、會場、Kong 錄影與東京鐵塔照片。

| 分析材料 | 官方議程 | 段內媒體入口 |
|---|---|---|
| Kong 午休實作；相關場次 The Production Gap | [相關場次](https://agntconmcpconjapan26.sched.com/event/2QlDL/the-production-gap-why-governing-agent-traffic-is-the-key-to-shipping-multi-agent-systems-juhi-singh-kong-prithvi-raj-mirantis) | [筆者操作錄影](https://www.facebook.com/reel/1387275603582551/)；官方演講錄影尚未確認 |
| Keynote: MCP and the Era of Connectivity | [議程](https://agntconmcpconjapan26.sched.com/event/2QrbB/keynote-mcp-and-the-era-of-connectivity-david-soria-parra-co-creator-of-mcp-anthropic) | [官方錄影](https://www.youtube.com/watch?v=3LwylP2as8A) |
| Keynote: Skills Over MCP: From Experiment to Extension | [議程](https://agntconmcpconjapan26.sched.com/event/2QlLo/keynote-skills-over-mcp-from-experiment-to-extension-ola-hungerford-principal-engineer-nordstrom) | [官方錄影](https://www.youtube.com/watch?v=3oHLjC3wZNE) |
| Running an MCP Proxy at Scale | [議程](https://agntconmcpconjapan26.sched.com/event/2QlDa/running-an-mcp-proxy-at-scale-camila-rondinini-anthropic) | [官方錄影](https://www.youtube.com/watch?v=e8DMLtP5ibk) |
| Build Your Own Open-Source Claude Code With Local LLMs | [議程](https://agntconmcpconjapan26.sched.com/event/2QlEY/build-your-own-open-source-claude-code-with-local-llms-daniel-oh-red-hat) | [官方錄影](https://www.youtube.com/watch?v=kwKVe27xnw4) |
| MCP-Powered Crash Investigation: How 11 MCP Servers Help an AI Agent Debug Production Issues at Uber | [議程](https://agntconmcpconjapan26.sched.com/event/2QlDI/mcp-powered-crash-investigation-how-11-mcp-servers-help-an-ai-agent-debug-production-issues-at-uber-kriti-dangi-uber) | [官方錄影](https://www.youtube.com/watch?v=iVCDIOf7vXw) |
| Self-Healing Agents Need Observability | [議程](https://agntconmcpconeu26.sched.com/event/2WNSu/self-healing-agents-need-observability-marcelo-trylesinski-pydantic) | [官方錄影](https://www.youtube.com/watch?v=JzBLYv1BTTM) |
| Designing Trust Boundaries for Agent-to-Agent Systems: Lessons Learned from a Technical PoC | [議程](https://agntconmcpconjapan26.sched.com/event/2RCwp/designing-trust-boundaries-for-agent-to-agent-systems-lessons-learned-from-a-technical-poc-ryuji-iijima-softbank-corp) | [官方錄影](https://www.youtube.com/watch?v=IO6CFh_lRGw)；[公開簡報](https://hosted-files.sched.co/agntconmcpconjapan26/3a/AGNTCon_MCPCon_Japan2026%E7%99%BB%E5%A3%87%E8%B3%87%E6%96%99_SoftBank_Corp_%E9%A3%AF%E5%B3%B6%E7%AB%9C%E5%85%90.pdf) |
| Intent as Code: Why Existing Permissions Aren’t Enough for AI | [議程](https://agntconmcpconjapan26.sched.com/event/2QlDX/intent-as-code-why-existing-permissions-arent-enough-for-ai-masaya-nakamura-studist) | 相符官方錄影尚未確認；[公開簡報](https://hosted-files.sched.co/agntconmcpconjapan26/ab/Intent-as-Code%20%2813%29.pdf) |
| Letting an Agent Upgrade Production Kubernetes — Without Getting Paged at 3 AM | [議程](https://agntconmcpconjapan26.sched.com/event/2QlD9/letting-an-agent-upgrade-production-kubernetes-without-getting-paged-at-3-am-sanskar-agrawalla-abhijeet-chaudhuri-quarticai) | 相符官方錄影尚未確認；[公開簡報](https://hosted-files.sched.co/agntconmcpconjapan26/d9/AGNTCon-MCPCon-Japan-2026_Abhijeet_Sanskar_final.pdf) |
| Stateful Sandboxes for Stateless Agents: Designing Durable Volumes for MCP Tool Workspaces | [議程](https://agntconmcpconjapan26.sched.com/event/2QlE7/stateful-sandboxes-for-stateless-agents-designing-durable-volumes-for-mcp-tool-workspaces-rui-su-juicedata) | 相符官方錄影尚未確認；[公開簡報](https://hosted-files.sched.co/agntconmcpconjapan26/4e/Stateful%20Sandboxes%20for%20Stateless%20Agents%20%C2%B7%20designed-r3.pdf) |
| Externalizing Agent State: Memory and Filesystem Management for Sandboxed Coding Agents | [議程](https://agntconmcpconjapan26.sched.com/event/2QlEe/externalizing-agent-state-memory-and-filesystem-management-for-sandboxed-coding-agents-tadatoshi-sekiguchi-pingcap) | 相符官方錄影尚未確認；[公開簡報](https://hosted-files.sched.co/agntconmcpconjapan26/17/EN%20_GNTCon-Japan-2026_PingCAP%20Seki.pdf) |
| What's Missing in the Open Agentic Stack: Lessons From OSS Integration | [議程](https://agntconmcpconjapan26.sched.com/event/2QlEG/whats-missing-in-the-open-agentic-stack-lessons-from-oss-integration-tatsuya-sato-satoshi-ito-hitachi-ltd) | 相符官方錄影尚未確認；[公開簡報](https://hosted-files.sched.co/agntconmcpconjapan26/bf/20260910_AGNTCon_Japan_Hitachi_Ito_Sato_public.pdf) |

議程題名與錄影標題有些不同，依講者、內容與活動核對配對。歐洲場的〈Self-Healing Agents Need Observability〉對應錄影〈Why Agent Evals Miss What Production Catches〉；SoftBank 的完整議程題名出現在官方頻道〈Agent-to-Agent Systems〉的影片說明中。第二篇新增的 SoftBank 連結是觀看入口，本文仍以原先六份簡報的完整文字與引用頁面為分析依據，沒有把這次連結核對寫成全片複核。

未確認錄影的場次，已用講者姓名、題名及關鍵字查詢官方 AAIF 頻道與搜尋結果。這是截至本次查找的狀態，不能推論錄影不存在或日後不會發布。查閱頁面、查詢文字與網址保存在本機研究目錄，正文只在資料說明集中交代。

## 本輪驗證

兩篇中英原稿各自重新產生 Medium 發布包。54 份發布用圖片副本與來源檔及前輪雜湊相符；第一篇每版 17 張、第二篇每版 10 張，東京鐵塔日景照仍為第二篇 story image。共凍結 66 份文章、貼稿、圖片索引與圖片輸入，再進行同步。

繁中檢查使用實際 MCP：先以 `lexical_safe` 提出建議，逐項按語意判讀，再對最終中文原稿與生成貼稿執行 `strict`、`fix_mode=none`。保留表示工作步驟的「程序」、表示驗收結果的「通過」、表示採用技術的「導入」，以及原始題名、程式識別字與必要的 Markdown 換行，不機械套用詞彙替換。

| 最終送檢稿 | errors | warnings | info | SHA-256 |
|---|---:|---:|---:|---|
| `2026-11-aaif-after-tokyo/article.md` | 0 | 52 | 24 | `d68b6495b64d8744b3ed7f616297ee9e2cf8bc91c0b9728f929e52fe4d8f5e38` |
| `2026-11-aaif-after-tokyo/publish/medium-paste.md` | 0 | 52 | 24 | `a774504f778fc14e43cbc7005f2e3bc89c382937b48ff3cb66d592196a2933e9` |
| `2026-11-aaif-agent-handoffs/article.md` | 0 | 36 | 15 | `a09a7700b75696689b2814efdcf13cb04db5823627f475a50de8fd402951948b` |
| `2026-11-aaif-agent-handoffs/publish/medium-paste.md` | 0 | 36 | 15 | `2c2f2c239e57340e6d00351ee0db0b72b84f5d06e5d6d4e67b3a51799eaaf032` |

以上四份均被 MCP 接受。警告保留上下文判讀紀錄：長講者／場次名稱觸發的長句提示，以及程序、工程、權限撤銷等詞彙，不作為自動改寫依據。檢查結果與原文雜湊保存在 `.context/research/aaif-2026-10-24/kong-flow/`。索引、發布紀錄、共用風格與四份發布 ledger 另以同一 strict 模式核對，最終雜湊見該目錄的 `docs-mcp-manifest.json`。

20 項既有測試通過，涵蓋文章與貼稿同步、連結、語言包完整性、Post ID，以及生成稿與圖片索引可重現性。工具程式沒有變更；前輪較大範圍的測試保留為歷史紀錄，不冒充本輪重跑。這次仍由撰稿代理核對，未新增獨立模型審查。

## 現有 Medium 稿件同步

四個原 Post ID 的最終正文均已核對。第一篇英文的首次同步回報中斷，接續直接讀回並核對已儲存的正文，沒有再次重灌；其餘三份沿正常同步流程更新。四份皆在儲存穩定後留 45 秒緩衝，再從新分頁逐塊比對；連結目的地與順序、圖片槽位、分隔線及零 placeholder 均通過。排程、預覽標題與摘要、Topics、作者照片封面及關閉訂閱通知的設定另由新分頁讀回，與本輪修改前一致。第一篇英文的中斷與復核日誌分開保留。

| 版本 | Post ID | 區塊／連結／圖片 | 排程（Asia/Taipei） |
|---|---|---|---|
| after-tokyo-zh | [`e3d060cb8b03`](https://medium.com/p/e3d060cb8b03/edit) | 205／64／17 | 2026-11-02 09:00 |
| after-tokyo-en | [`565d3e375896`](https://medium.com/p/565d3e375896/edit) | 205／65／17 | 2026-11-04 09:00 |
| agent-handoffs-zh | [`e68dc5ab1275`](https://medium.com/p/e68dc5ab1275/edit) | 151／33／10 | 2026-11-09 09:00 |
| agent-handoffs-en | [`8b39e1abe616`](https://medium.com/p/8b39e1abe616/edit) | 150／34／10 | 2026-11-11 09:00 |

四篇仍為尚未公開的排程稿，沒有重新送出排程、建立替代文章或代送 Ambassador 申請。完整發布設定以[目前發布紀錄](publication.md)與各語言的 `PUBLISHED.md` 為準。前輪的檢查與雜湊仍保留在原紀錄，不覆寫成這次的結果。

同日接續完成的[第三篇](memory.md)另有自己的材料、三輪編修與語文檢查，目前只產生本機中英文稿及發布包，沒有混入上述四份遠端同步計數。
