# research/ — 每月主題研究迴圈

這個資料夾放的是流程，用來決定下個月寫什麼；文章本身不在這裡，仍然一篇一個
`YYYY-MM-slug/` 資料夾（見上層 [README.md](../README.md)）。

目標是每月轉一圈、越轉越準的迴圈：

```mermaid
flowchart LR
    classDef own fill:#d4edda,stroke:#2e7d32,color:#1f2933
    classDef buy fill:#fff3cd,stroke:#b8860b,color:#1f2933
    classDef human fill:#e3f2fd,stroke:#1565c0,color:#1f2933
    subgraph in["每月 1–2 日：決定寫什麼"]
        direction TB
        C["1 收集<br/>X / Facebook / LinkedIn<br/>Medium stats / arXiv / Notion"] --> D["2 摘要<br/>四份 digest"]
        D --> P["3 提案 → 評審 → 選題<br/>workflow"]
        P --> O["4 大綱<br/>總論 + 三部曲"]
    end
    subgraph out["當月：寫、發、量"]
        direction TB
        W["5 撰寫與發布<br/>medium_draft.sh"] --> F["6 成效回饋<br/>reads、完讀率、分享"]
    end
    in --> out
    out -.->|重排 backlog、修正權重| in
    class P own
    class F buy
    class O human
```

（示意圖，frontmatter 設定省略。文章與大綱裡的每張圖都要以 [MERMAID.md](../MERMAID.md) 第二節那段 `config` 開頭；這裡不再抄一份，免得兩邊漂移。）

第一圈在 2026-09-05 跑過，產出在 [`2026-09/`](2026-09/)。

## 每月節奏

| 日期 | 做什麼 | 產出 |
|---|---|---|
| 每月 1 日 | `research/scripts/collect.sh all`；arXiv 掃描交給 agent（見 `prompts/arxiv.md`） | `.context/research/YYYY-MM/*.json`（原始 JSON，gitignored）、`research/YYYY-MM/arxiv.md` |
| 1–2 日 | 四個 digest agent（X、社群、arXiv、Notion）把四份 digest 寫進 `research/YYYY-MM/`（Notion 與社群兩份只留本機，見「資料來源」）→ 執行 `workflows/plan-next-three-themes.js` | `research/YYYY-MM/` 下的 `selection.md`、主題大綱 + `backlog.md` |
| 2 日 | `workflows/review-outlines.js` 第二輪批評／修訂 → 每份大綱跑 `research/scripts/codex_review.sh`（Codex，reasoning xhigh，第二個模型的意見）→ 依意見修訂 → 大綱裡每張 Mermaid 圖跑 `research/scripts/mermaid_check.sh`（規範見 [MERMAID.md](../MERMAID.md)）→ 所有中文產出過 zh-tw MCP 檢查（`mcp__zhtw-mcp__zhtw`，markdown、lexical_safe） | `codex-review-*.md`、修訂後的大綱 |
| 2 日 | 人工看一遍：選題是否對、調整大綱、決定要不要換掉某一個 | 定稿的大綱 |
| 3–14 日 | 長度基準（Medium 讀時算 CJK 字、英文字與圖）：已發布總論 3,629 個中文字 ≈ 18 分鐘，深掘 1,800–2,300 字 ≈ 8–12 分鐘，寫的時候以此為準。每篇跑 `workflows/write-article.js`（草稿 → 三視角批評 → 修訂 → 驗證）→ zh-tw agent → 英文版；`scripts/article_to_paste.py` 產 `publish/medium-paste.md`、`scripts/render_images.sh` 算繪圖與表格 PNG；`python3 tools/test_tools.py` 過 lockstep；`tools/medium_draft.sh` 建草稿 | 四篇草稿 × 兩種語言 |
| 15–20 日 | 發布。Medium 24 小時內最多 2 篇，八篇至少要四天，順序見 [PUBLISHING.md](../PUBLISHING.md) | 上線文章 + `PUBLISHED.md` |
| 發布當天 | 粉絲團與 X 貼分享文。2025 年的資料顯示，reads 主要來自粉絲團分享 | 分享文 |
| 月底 | `collect.sh medium` 抓一次 stats，比對上月；回填 `backlog.md` 的權重 | 成效表 |

節奏是建議值。發布配額是硬限制，其餘都可以壓縮。

## 資料來源

| 來源 | 登入方式 | 抓什麼 | 腳本 | 已知問題 |
|---|---|---|---|---|
| X | Chrome Default profile 的 cookie（`auth_token`、`ct0`），`tools/chrome_cookies.py x.com` | 「正在跟隨」時間軸、書籤、追蹤名單、以及 `filter:follows since:… min_faves:…` 的熱門搜尋（8 組關鍵字） | `collect.sh x`、`extract_tweets.js`、`extract_users.js` | 書籤裡的 X 長文只有連結沒有內文；三個 Chrome profile 都是同一個 X 帳號 |
| Facebook | 同上，`facebook.com --subdomains` | 已加入的技術社團、自己的動態、粉絲團「榮民叔叔的藏書筆記」 | `collect.sh facebook`、`extract_fb2.js`（社團，走 `div[role=feed]`）、`extract_fb_timeline.js`（個人頁與粉絲團，用作者名切文字） | 首頁動態是私人內容，不抓；Claude / OpenClaw / Antigravity / GCP 幾個社團多半是轉賣、範本與 cheat sheet 雜訊，真正有訊號的是搞笑談軟工、DevOps Taiwan、Backend 台灣、Scrum、Agile 內湖、DDDesign、Twinkle AI |
| LinkedIn | `linkedin.com --subdomains`（`li_at` 掛在 `.www.linkedin.com`） | 動態牆、已儲存貼文 | `collect.sh linkedin`、`extract_li2.js` | 動態牆 2026-09 只抓到 8 篇（用「Feed post」切文字），selector 待修；已儲存貼文的價值比較高 |
| Medium | `medium.com`（Default profile，同 `medium_draft.sh`） | `me/stats` 全表（presentations / views / reads）、個人頁文章清單 | `collect.sh medium`、`extract_medium.js` | 這是回饋迴圈的輸入；Cloudflare 擋 headless，一律 `--headed` |
| arXiv | 不用登入 | `export.arxiv.org/api/query` 各主題各 50 筆，再讀 abstract；批次查詢會被 429，改用 arxiv.org 搜尋頁補 | agent（`prompts/arxiv.md`） | 提交日與公告日可能差一個多月，表裡要註明 |
| Notion | 桌面版 app 的 cookie（Electron 同款加密），`research/scripts/notion_cookies.py notion.com`；第一次讀 Keychain 要人按「允許」（2026-09-05 10:47 已授權） | 工作區的側欄、最近編輯的 100 頁（內部 `/api/v3/search`）、指定頁面的算繪文字 | `collect.sh notion`、`notion_search.js`、`notion_chunk.js` | `token_v2` 掛在 `app.notion.com`，browse 只收「網域是目前頁面字尾」的 cookie，所以要分兩批：站在 `www.notion.com` 匯入 `.notion.com` 那批，再站在 `app.notion.com` 匯入 `app.notion.com` 那批；`msgstore-*.app.notion.com` 的 AWSALB cookie 丟掉。內部 API 沒有版本保證 |

所有 cookie 都只存在 `mktemp -d`（0700）裡，匯入完就刪；`.gitignore` 也擋了 `*cookies*.json`。

這個 repo 是公開的，所以研究資料分三層，規則寫在根目錄的 `.gitignore`：

- **原始 JSON**（別人的貼文原文）留在 `.context/research/YYYY-MM/`；整個 `.context/` 都是 gitignored，**不要 commit**。
- **`notion_digest.md` 與 `community_digest.md` 只留本機**：前者是作者自己的 Notion 內容，後者逐字引了私人社團裡別人的貼文。`.gitignore` 用 `research/*/notion_digest.md`、`research/*/community_digest.md` 擋掉，檔案仍放在 `research/YYYY-MM/` 給 workflow 讀。fresh clone 不會有這兩份，要先重跑 `collect.sh` 與對應的兩個 digest agent。
- **其餘都 commit**：`x_digest.md`、`arxiv.md`、`style_brief.md`、`selection.md`、`backlog.md`、三份大綱與 `.figures.md`、`codex-review-*.md`。

## 目錄

```
research/
├── README.md                 # 本檔：迴圈怎麼轉
├── scripts/
│   ├── _common.sh            # 給其他腳本 source、不直接執行：ROOT、EX_* 離開碼、browse 的路徑、collect.sh 的鎖、headless 算繪前的 viewport 準備
│   ├── collect.sh            # 收集階段的驅動腳本（由 2026-09-05 跑通的指令整理而成）
│   ├── extract_*.js          # 各平台的 DOM 擷取；selector 會壞，壞了先修這裡
│   ├── merge.py              # 把新抓的一批 JSON 併進累積檔：`--key link|handle` 選去重欄位，`--tag SOURCE` 標來源
│   ├── codex_review.sh       # 用 Codex（xhigh）二審一份大綱或 selection.md（`KIND=outline|selection`），原話存 codex-review-<slug>.md；四份 digest 都要在 research/<month>/ 下才跑，缺一份 exit 64
│   ├── codex_jsonl.py        # codex exec --json 的串流解析（拆出來是因為 bash 單引號裡塞 python 會壞）
│   ├── mermaid_check.sh      # 用 browse 算繪一張 Mermaid 圖並依 MERMAID.md 判 PASS／FAIL（寬、高／寬、節點數）
│   ├── mermaid_check_all.sh  # 抽出一份 .md 裡所有 mermaid 區塊逐張檢查，列成一張表
│   ├── sync_figures.py       # 用 <slug>.figures.md 的已驗證版本覆蓋大綱內嵌的 mermaid（依圖 id）；有對不上或重複的區塊就不寫，除非 --force
│   ├── article_to_paste.py   # article.md → publish/medium-paste.md（mermaid → 📌圖、表格 → 📌表，其餘一字不差）+ figures.json
│   ├── render_images.sh      # 依 figures.json 算繪 diagram-NN.png（走 mermaid_check）與 table-NN.png（HTML 截圖）
│   ├── test_research_scripts.py   # 離線測試（stdlib unittest）：article_to_paste（含每篇已 commit 的 paste == convert(article)）、sync_figures、codex_jsonl、merge、notion_cookies 的守衛，以及 codex_review.sh 的前置檢查（用假的 codex）
│   ├── notion_cookies.py     # Notion 桌面版 cookie 解密（Keychain 授權一次）
│   └── notion_search.js / notion_chunk.js   # Notion 內部 API：最近頁面清單、單頁文字
├── prompts/                  # 四個 digest agent 的 prompt（每月照抄改日期），加上 zh-tw 檢查 agent 的 zhtw_pass.md
├── workflows/                # Workflow 工具的腳本；root／month／today／published 都從 args 進，不寫死
│   ├── plan-next-three-themes.js   # 提案 → 合併 → 評審/反駁 → 選題 → 大綱/批評/修訂 → backlog
│   ├── review-outlines.js          # 第二輪：每份大綱 4 個視角批評（證據稽核／VP 讀者／編輯／圖表設計）→ 修訂 → 驗證（≤ 2 輪）→ 補 Mermaid 圖檔
│   ├── finish-outline.js           # 續跑：批評已跑完但修訂／圖檔被中斷時，用存下來的 issues 驗證 → 必要時修訂 → 補圖檔
│   └── write-article.js            # 寫一篇：從大綱與 figures.md 產 article.md → 三視角批評 → 修訂 → 驗證
└── YYYY-MM/                  # 每一圈的產出；除了標 local 的兩份，其餘都 commit
    ├── x_digest.md / arxiv.md      # digest：X、arXiv
    ├── community_digest.md         # digest：FB 社團／LinkedIn／Medium stats — local only，gitignored
    ├── notion_digest.md            # digest：作者自己的 Notion — local only，gitignored
    ├── style_brief.md        # 寫法摘要；寫完新系列後更新
    ├── selection.md          # 選題結果：評審意見、反駁、每個主題必須遵守的調整
    ├── 2026-10-<slug>.md     # 三個主題的完整大綱（總論 + 三部曲）
    ├── 2026-11-<slug>.md
    ├── 2026-12-<slug>.md
    ├── 2026-1x-<slug>.figures.md   # 每張圖的 Mermaid 原始碼（依 MERMAID.md），mermaid_check.sh 逐張驗過
    ├── codex-review-*.md     # Codex 二審的原話
    └── backlog.md            # 落選主題 + 訊號監看清單

.context/research/YYYY-MM/    # collect.sh 的原始 JSON（整個 .context/ gitignored）
.context/mermaid/             # mermaid_check.sh 的算繪暫存
.context/render/<dir>[-<lang>]/   # render_images.sh 的算繪暫存
.context/collect.lock         # collect.sh 跑的期間持有；mermaid_check.sh 與 render_images.sh 看到它就退出 75，等它跑完再來
```

## 分析階段

四份 digest 分工固定，prompt 在 `prompts/`：

1. `x_digest.md`：追蹤名單分群、貼文依讚數與「書籤／讚」比排序（書籤比高＝有用的技術內容，讚多＝發布新聞）、10–14 個主題、正在爭論的張力、作者自己的訊號（書籤）、與已發布系列的缺口。
2. `community_digest.md`：台灣社團在問什麼、作者自己在 FB 上的聲音、LinkedIn 儲存貼文、Medium 全表成效與完讀率、機會清單。
3. `arxiv.md`：近三個月論文分群、跟業界說法相反的實證、可直接成文的訊號。
4. `notion_digest.md`：作者自己的 Notion：正在讀哪些證照與課程、工作坊筆記、讀書筆記與待讀清單、草稿。用來找第一手材料，也看作者當下的可信地盤（prompt 在 `prompts/notion_digest.md`）。

選題交給 workflow（`workflows/plan-next-three-themes.js`），設計刻意不省：

- 5 個視角各提 4 個候選（續集／作者強項／社群痛點／研究前沿／策略逆風）→ 合併去重成 6–10 個
- 每個候選：2 位不同視角的評審（讀者 VP、資深編輯）打 5 個分項 + 1 位反方（預設要駁倒）
- 選題 agent 看全部分數與反駁，挑 3 個並排到 10／11／12 月，落選的全部進 backlog
- 每個主題：大綱 → 批評（對 style brief、對已發布文章、對 digest 逐一查引用）→ 修訂
- 大綱寫完後再跑一次 `workflows/review-outlines.js`（args：root、month、today、published、files；可選 `lenses: ["evidence","diagram"]` 只跑部分視角、`skipFigures: true` 跳過圖檔階段、`preIssues: {"<basename>.md": [issue, …]}` 把上一次中斷的 run 存下來的批評併進來，該視角就不必重跑。**一次只放一份大綱**：2026-09-06 實測 12 個 critic 同時讀 100K 字元大綱加 digest 會在幾分鐘內撞到 session 上限，只有證據稽核視角需要讀 digest）：每份大綱四個視角獨立批評—證據稽核（逐一對 digest 查引用與數字）、VP 讀者（會不會讀完並轉發）、編輯（格式、重疊、一個月寫得完嗎）、圖表設計（每張圖都要有符合 [MERMAID.md](../MERMAID.md) 的 Mermaid 原始碼，700px 下可讀）—合併 blocker/major 後修訂、再驗證，最多兩輪，最後才補 `.figures.md`。
- workflow 之外再加兩道關卡（2026-09-05 決定）：
  1. **Codex 二審**：`research/scripts/codex_review.sh <outline.md>`，用 OpenAI Codex（`~/.codex/config.toml` 的 model，reasoning `xhigh`）審每份大綱。理由是大綱由 Claude 寫、Claude 批評、Claude 修訂，同一個模型審自己有盲點；Codex 在 repo 根目錄 read-only 跑，會自己讀 digest 與 selection.md 查引用。原話存成 `codex-review-<slug>.md`，再由 Claude 修訂大綱。
  2. **zh-tw 檢查**：所有要給人讀的中文檔（大綱、backlog、selection.md、本 README、之後的 article.md 與 medium-paste.md）最後都過 `mcp__zhtw-mcp__zhtw`（content_type markdown、fix_mode lexical_safe、translationese_domain technical、fix_output search_replace），**逐條看它提議的替換再套，不要整檔覆蓋**：2026-09-06 實測它會把「未通過」改成「未透過」、「縮進容器」改成「縮排容器」、「原始碼」改成「原始程式碼」，三個都是誤判。真正有用的是翻譯腔警告（定語堆疊、被動語態），照著拆句即可。這是最後一步，任何修改之後都要再跑。**大檔（> 30K 字元）交給一個 agent 做**：MCP 工具只吃 `text` 參數，主迴圈自己貼會把整份大綱當輸出 token 重打一遍；agent 依標題切成 ≤ 30K 的段、逐段呼叫、逐條判斷再套回原檔（prompt 見 `prompts/zhtw_pass.md`）。

重跑：把 `research/YYYY-MM/` 的四份 digest 與 `style_brief.md` 準備好（原始 JSON 在 `.context/research/YYYY-MM/`，workflow 不讀它），
在 Claude Code 裡用 Workflow 工具帶 `scriptPath` 執行。四支 workflow 都不寫死路徑、日期與已發布文章：
`root`（repo 根目錄）、`month`（研究月份）、`today`（`YYYY-MM-DD`；workflow 腳本裡沒有 `Date`，缺了會直接丟錯）、
`published`（已發布文章的目錄清單，缺了也丟錯）一律從 args 帶入。目前的 `published` 是下面這四個目錄，新系列上線後在這裡加：

```js
const PUBLISHED = ["2026-09-agentic-engineering-platform", "2026-09-agentic-org-design", "2026-10-agentic-harness-blueprint", "2026-11-agentic-eval-economics"]
Workflow({scriptPath: "research/workflows/plan-next-three-themes.js", args: {root, month: "2026-09", today: "2026-09-05", published: PUBLISHED}})   // 可加 months: ["2026-10", "2026-11", "2026-12"]，預設是 month 之後三個月
Workflow({scriptPath: "research/workflows/review-outlines.js", args: {root, month: "2026-09", today: "2026-09-06", published: PUBLISHED, files: ["research/2026-09/2026-11-same-spec-ten-runs.md"]}})
Workflow({scriptPath: "research/workflows/finish-outline.js", args: {root, month: "2026-09", today: "2026-09-06", published: PUBLISHED, file: "research/2026-09/2026-11-same-spec-ten-runs.md", issuesFile: root + "/.context/research/issues-2026-11.json"}})
```

`write-article.js` 的呼叫在下面待辦裡。中途掛掉可用 `resumeFromRunId` 續跑，已完成的 agent 會回快取結果。

## 讓它越轉越準：回饋與成長機制

這一節是迴圈跟「只做一次的研究」的差別。

**1. 成效回填 backlog。** 每月底抓 Medium stats，算每篇的 reads/views（完讀率）與 claps。
把「表現好的主題族」的權重寫回 `backlog.md`，下個月的選題 agent 會讀到。已知的基準：
2025 年中文長文完讀率 27%、英文 8%；書評型（建築、XP）完讀 46–51%；文章 views 超過
presentations 的那幾週，都是粉絲團有分享的週。這些數字放在 `style_brief.md` 的「reception」段，
每月更新一次。

**2. backlog 是狀態機，不是筆記。** 每個條目有：升級條件（什麼證據出現就升上去）、最早適合的月份、
上次評分。每月 workflow 的 Select 階段會重新排它。連續三個月沒有新證據的條目降到「觀察中」。

**3. 訊號監看清單越長越好。** `backlog.md` 末尾的清單（帳號、arXiv 查詢字串、社團、會議日期）
是下個月 `collect.sh` 與 arXiv prompt 的輸入來源。新發現一個有訊號的帳號或社團，就加進去；
一個社團連續兩個月只有雜訊，就從 `FB_GROUPS` 拿掉。

**4. digest 累積成觀點資料庫。** 每個月的四份 digest 都留在 `research/YYYY-MM/`（兩份只在本機，見「資料來源」），
寫文章時可以回頭引用「三個月前社群在爭什麼」；跨月比對也是 總論 裡「市場走到哪裡了」那一節的素材。

**5. style brief 隨每個系列更新。** 新系列寫完，把用得順的結構、被讀者回應的段落、
出過問題的格式（例如 `——` 會裂）補回 `style_brief.md`。它是給 agent 的 AGENTS.md，
標準跟技術篇說的一樣：新來的 agent 拿著它，能不能不問人就寫出對的大綱。

**6. 系列互連。** 每個新主題的總論要回連上一個系列；本圈的三個主題都建立在 Agentic Engineering
三部曲之上。舊文也要補一句指向新系列，讓讀者能沿著鏈讀。修改已發布文章用 `tools/medium_patch.py`。

## 自動化的邊界

收集階段需要**本機**：Chrome 的 Keychain、headed 瀏覽器、以及第一次讀 Keychain 時人按「允許」。
所以雲端排程（Claude Code 的 schedule routine）跑不了 `collect.sh`；可行的組合是：

- 每月 1 日手動（或本機 cron / launchd）跑 `collect.sh all`，人在旁邊按掉 Keychain 提示；
- 之後的 digest 與 workflow 不需要瀏覽器，但不是一個 session 一次跑完的量（2026-09-06、07 實測）：
  `review-outlines.js` 一次只放一份大綱（12 個 critic 同時讀大綱加 digest，幾分鐘就撞 session 上限）；
  `write-article.js` 一次只寫一篇；大檔的 zh-tw 檢查交給單一 agent、切成 ≤ 30K 字元的段逐段做
  （三份大綱的 zh-tw 三次都撞上限）；run 與 run 之間預期要停下來等額度（10 月四篇的批評／修訂
  就是等 02:00 重置才接上）。`/loop` 適合在收集完成後自動接第一個 run，之後的 run 依上面的粒度一個一個開。

不要為了全自動而把 cookie 存到固定路徑或環境變數；`medium_draft.sh` 對這件事的態度同樣適用。

另外兩件事 workflow 也替不了作者：草稿裡寫了「動筆前會實測」的機制，要真的測過才能發；引用別人工作坊的材料，要先問過。
目前欠著的兩筆在下面待辦最前面。

## 待辦

- [ ] **發布前作者要親手做的兩件事（workflow 補不了）**：
  1. 總論第十節（`2026-10-green-overview/article.md` 約第 638 行）寫「AI 的 approve 永遠不計入 required approvals… 哪一種可行，Review 篇動筆前會實測，這裡只寫結論」—CODEOWNERS 只列人類加 Require review from Code Owners、或 required status check 透過 API 數人類 approve，兩種都**還沒實測**。Review 篇動筆前要在一個 GitHub repo 上真的做一次，再依結果改寫總論那一句。
  2. 測試篇第七節引用了 Teddy 工作坊的 A/B 實作，正文提到 `EventSourcedAggregate`、`getDomainEvents()`、`@DirtiesContext` 這些課程 repo 裡的識別字；notion_digest 對這份材料的原則是「cite the workshop, not the code… ask permission」。發布前要取得 Teddy 同意，或改寫成只引工作坊、不引程式碼。
- [ ] **引用前先取得同意**：已 commit 的大綱與 `selection.md` 現在只用角色稱呼私人社團成員（「一位 Scrum Community 成員」「一位 DevOps Taiwan 成員」），不寫名字；名字、逐字引文與反應數只留在本機的 `community_digest.md`。發布任何引了社團貼文的文章之前，先在本機 digest 裡記下同意（誰、何時、哪一則），記了才把署名還回文章。`notion_digest.md` 與 `community_digest.md` 永遠不 commit（`.gitignore` 已擋，見「資料來源」）：這個 repo 是公開的，前者是作者自己的 Notion 內容，後者逐字引了私人社團裡別人的貼文，還帶著名字與反應數。
- [x] Notion：2026-09-05 已打通（Keychain 授權 + 分網域兩批匯入），流程在 `collect.sh notion`，digest prompt 在 `prompts/notion_digest.md`。資料庫頁（讀書筆記／待讀清單）loadPageChunk 抓不到列，要用算繪文字（`collect.sh` 尚未納入這一步）。
- [x] 大綱與 `<slug>.figures.md` 都會有 Mermaid：修訂 agent 會把圖嵌進大綱、圖檔 agent 另寫一份。以 **figures.md 為準**（它是逐張算繪驗過的），同步已寫成腳本。長期規則：改圖只改 figures.md，`mermaid_check_all.sh` 全 PASS 後跑 `python3 research/scripts/sync_figures.py <outline.md>` 依圖 id 覆蓋大綱內嵌版；它先印出整張對應表，遇到對不上的區塊、或兩個區塊對到同一個 id，就不寫、exit 1（確定要寫加 `--force`，然後手修）。2026-09-06 對 10 月是手動做的，11、12 月的內嵌版已同步。
- [x] 2026-10 第二輪完成（2026-09-06 14:40）：4 視角 41 major 全數修訂、驗證通過；22 張 Mermaid 圖經 `mermaid_check_all.sh` 全部 PASS（5 張由筆者重畫）。11、12 月依序進行。
- [x] 2026-11 第二輪完成（2026-09-06 22:40）：3 視角 + 圖表視角共 70 條意見，`finish-outline.js` 驗證／修訂後補圖檔；16 張 Mermaid 全部 PASS，大綱內嵌版已同步。
- [x] 2026-12 第二輪完成（2026-09-06 23:15）：4 視角 27 major，修訂 51 條、驗證通過（3 個殘留由筆者手修）；14 張 Mermaid 全部 PASS，大綱內嵌版已同步。
- [ ] **10 月四篇初稿都已寫好、機械檢查全過（2026-09-07 00:10）**，等 02:00 額度重置後跑批評／修訂：

      | 篇 | 目錄 | 中文字（正文） | 圖／表 | 目標字數 |
      |---|---|---|---|---|
      | 總論 | `2026-10-green-overview` | 7,168 | 10／9 | 3,500–4,500 |
      | 一、測試篇 | `2026-10-green-testing` | 3,820 | 4／4 | 1,900–2,600 |
      | 二、Review 篇 | `2026-10-green-review` | 3,925 | 4／3 | 1,900–2,600 |
      | 三、可靠度篇 | `2026-10-green-reliability` | 2,850 | 4／3 | 1,900–2,600 |

      四篇的圖全部 `mermaid_check` PASS、`article_to_paste.py` 與 `render_images.sh` 都跑過、`tools/test_tools.py` OK、`——` 為 0；
      三部曲已先跑過一輪 zh-tw（只採納 場景→情境、是一個→是、可執行行→可執行的行；通過→透過、數據→資料、實例→實體、依賴→相依性 都是誤判，未套）。
      批評／修訂（每篇一個 run，總論先；`prev` 帶前面各篇的目錄）：
      `Workflow({scriptPath: "research/workflows/write-article.js", args: {root, month: "2026-09", outline: "research/2026-09/2026-10-agentic-green-is-not-done.md", figures: "research/2026-09/2026-10-agentic-green-is-not-done.figures.md", piece: "總論", dir: "2026-10-green-overview", skipDraft: true, today: "2026-09-07", published: PUBLISHED}})`（`PUBLISHED` 同「分析階段」末段的四個目錄），
      再依序 `piece: "一、測試篇", dir: "2026-10-green-testing", prev: ["2026-10-green-overview"]`、`piece: "二、Review 篇", dir: "2026-10-green-review", prev: [總論, 測試篇]`、`piece: "三、可靠度篇", dir: "2026-10-green-reliability", prev: [前三篇]`。
      每篇修訂後重跑 `article_to_paste.py`、`render_images.sh`、`tools/test_tools.py`，**最後**再跑一次 zh-tw（修訂會改動正文）；然後寫英文版（`article.en.md`，`--lang en`）。三份大綱的 zh-tw agent 也還沒跑完（三次都撞上限）。
- [ ] **Codex 二審尚未跑**：2026-09-05 22:36 撞到 Codex 用量上限（重置時間 2026-09-07 10:25）。重置後三份大綱各跑一次 `research/scripts/codex_review.sh <outline.md>`；`selection.md` 也跑一次 `research/scripts/codex_review.sh research/2026-09/selection.md`（檔名以 `selection` 開頭會自動換成審選題的框架；`KIND=outline|selection` 可強制指定）。依意見修訂，再跑一次 zh-tw 檢查。
- [ ] LinkedIn 動態牆的 selector（目前靠「Feed post」切文字，只抓到 8 篇）。
- [ ] `collect.sh` 還沒以單一腳本從頭跑過一次；第一次請逐段看。
- [ ] **PNG 沒有過期閘門**：已 commit 的 `publish/images/*.png` 跟算繪它們的來源沒有綁在一起。
      `test_research_scripts.py` 只比對 `figures.json` 裡的 mermaid 原始碼與 article.md 一致，表格完全沒比，
      PNG 本身也沒人檢查—改了一張表或一張圖、忘了重跑 `render_images.sh`，測試照樣綠。提案：`render_images.sh`
      每算繪一張，把該圖／表來源的 sha256 寫進 `publish/images/.rendered.json`；`test_research_scripts.py`
      對每篇有 `figures.json` 的文章，斷言 `.rendered.json` 裡的雜湊等於目前來源的雜湊。
- [ ] 這些腳本目前放 `research/scripts/`，不在 `tools/`。能離線測的純 Python 部分（`article_to_paste.py`、
      `sync_figures.py`、`codex_jsonl.py`、`merge.py`，以及 `notion_cookies.py` 的參數與 Keychain 守衛）
      已由 `research/scripts/test_research_scripts.py` 蓋住，規矩同 `tools/`（見根目錄 CLAUDE.md）；
      `codex_review.sh` 的前置檢查（缺 digest 就 exit 64、四份齊全才叫 codex 並寫出 review）也在裡面，用假的 `codex` 測；
      `extract_*.js`、`collect.sh`、`mermaid_check*.sh`、`render_images.sh` 依賴外部 DOM、瀏覽器或 Keychain，
      沒有離線測試，靠執行時自檢。等 selector 穩定再決定要不要把純 Python 那批搬進 `tools/`。
- [ ] 每月更新 `style_brief.md` 的 reception 段與 `backlog.md` 的權重。
