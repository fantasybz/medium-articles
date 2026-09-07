# Community digest — what Kochi's networks are talking about (as of 2026-09-05)

Sources: `facebook_groups.json` (346 posts, 17 groups), `fb_groups_all.json` (35 groups), `facebook_own.json` (72 entries, fan page + profile), `linkedin_saved.txt` (9 saved posts), `linkedin_feed.json` (8 feed items), `medium_stats.txt` (41 stories, lifetime), `medium_articles.json`.

Reading note on numbers: Facebook's scraped text doubles bare reaction counts when no reactor names are attached (`所有心情：1010` is 10, `340 340` is 340). All counts below are de-duplicated. Engagement is given as reactions / comments / shares where visible.

---

## 1. Taiwanese tech-community pulse

The live groups, by last-post recency (`fb_groups_all.json`): Kobo (44 min), Scrum Community in Taiwan (7 h), Backend 台灣 (1 day), DevOps Taiwan (2 days), Agile community in 內湖 (1 week), 搞笑談軟工 (1 week), DDDesign Taiwan (5 weeks), the user's own 藏書交流社團 (14 weeks), 趨勢科技 Trender (3 years, dead). The AI-vendor groups (Claude Taiwan, MCP/Vibe Coding, OpenClaw x2, Claude Cowork Users, Antigravity, GCP & K8s) are high-volume but mostly noise: Claude Max "20x 1 year" resale scams via WhatsApp appear at least seven times, the two OpenClaw groups are n8n template vaults and Thai/Vietnamese tool round-ups, and GCP & K8s is entirely "Be Cloud Architect" AI-generated cheat-sheet spam plus Khmer political posts. The signal lives in six Taiwanese practitioner groups: 搞笑談軟工, DevOps Taiwan, Scrum Community, Agile 內湖, DDDesign Taiwan, Backend 台灣, plus Twinkle AI and the practical threads in Claude Taiwan.

Eleven clusters follow, ordered by the engagement they draw.

### 1.1 "Clean loop, not clean code" — reproducibility as the test of a harness

The single most-shared idea in the whole dataset is Teddy Chen's (搞笑談軟工) reproducibility criterion.

| Post | Group | Engagement |
|---|---|---|
| 「你的 AI Coding 方法，可以做到『輸入相同的規格，不需要人為介入，既可重複產生幾乎相同的程式實作嗎？』如果可以，我認為你的 Context Engineering/Loop Engineering 就算成功了」 | 搞笑談軟工 | 298 / 17 / 74 shares |
| Clean Code 2nd ed. TC translation, Uncle Bob vs. John Ousterhout appendix; a commenter asks 「不知道 AI 寫的程式碼，有可能『無瑕』嗎？」 | 搞笑談軟工 | 190 / 13 / 38 |
| Teddy's reply: 「Clean Code 是生成流程的產物，而不是生成流程本身」; the commenter's response 「『clean』的不是『code』，是『loop』，是『harness』」 | 搞笑談軟工 | 76 / — / 11 |
| 150 hours writing an AI Coding paper, 9k words grew to 18k | 搞笑談軟工 | 193 / 4 / 16 |
| Sharing the AI coding project with the ezKanban student team: 「Feedback loop 變長了，lead time 也拉長了」; top comment: 「AI coding 目前最被低估的瓶頸，不是 code，而是架構規劃與抽象對接」 | 搞笑談軟工 | 111 / 3 / 23 |
| Mapping Pattern Language onto Harness Engineering (= diagnosis / misfit detection) and Loop Engineering (= piecemeal growth) | 搞笑談軟工 | 45 / — / 13 |
| Students measured LOC variance across regenerations; commenter asks whether stronger models (Fable 5) need fewer constraints | 搞笑談軟工 | 57 / 3 / 11 |
| Kim Kao: 「大家也開始做到很複雜的系統了嗎？Harness engineering 會是幫助你走得穩健的一環」 (walkinglabs "Learn Harness Engineering", Marcus 的學習筆記 「AI agent 又翻車？先別怪模型，你可能少了一副『馬具』」) | DDDesign Taiwan | 18 / 1 / 7 |
| DevOps Taiwan on the RePPIT framework; William Yeh: 「很多細節都在 superpowers 或 Matt Pocock skills 裡面實現出來了」 | DevOps Taiwan | 23 / 4 / 3 |
| Maple Kuo on `gh skill install` (GitHub CLI v2.90, agentskills.io, 45 harnesses); reply: 「我近幾個月來都是交給 claude/codex 自己決定要安裝或使用什麼樣的 skill」 | Backend 台灣 | 24 / 2 / 10 |

Terminology practitioners use: 馴服 AI, 模式語言 (Pattern Language), 生成流程, 馬具 / harness, Context Engineering, Loop Engineering, 可維護, 規格 (spec), 棕地專案 (brownfield), Skills.

Implication for an article aimed at engineering leaders: "harness" has already crossed from English blogs into Taiwanese vocabulary, and the crowd's yardstick is not eval score but determinism of output under a fixed spec. The user's Harness Blueprint piece defines the components; it does not yet answer Teddy's question, which is the one people are sharing. Note that the user attended Teddy's workshop as 學號1號 and reacted to three of these posts.

### 1.2 AI-era testing: 「AI 說沒問題」

DavidKo Learning Journey cross-posts to Scrum Community, Agile 內湖 and DevOps Taiwan and is, by volume, the loudest voice on testing.

- 「AI Coding 之後，RD 最常說的不是『我測過了』，而是『AI 說沒問題』。覆蓋率 90%？放心。CI 綠了？可以上。」 (Scrum, 9 / — / 2; also Agile 內湖).
- Lada Kesseler's two-layer strategy: 「我信任 AI 寫的測試，比信任它寫的程式碼還少」 (Scrum, 7).
- 「你叫 AI 修 failing test，它把斷言改掉了」 — six failure patterns: loosened assertions, bugs frozen into tests, specs drifting out of sync (Scrum, 3).
- 「讓 AI Agent 自己做 TDD，是儀式還是真有價值？」 (DevOps Taiwan, 23 / — / 8).
- 「以前不寫測試，理由是『沒空』；現在 AI 都能幫你生測試了，理由升級成『Token 太貴』」 (Scrum, 5).
- Uncle Bob's stance relayed by John Yu: he no longer reads agent-written code as long as it clears unit tests, Gherkin tests, mutation tests and quality metrics; 陳正瑋 adds 「馬丁大叔快點把所有該做的 test 都詳細列出來啊」 (DevOps Taiwan, 40 / 5 / 3).
- 「把人類的『價值』(品質、測試、整潔) 要求 AI，是對的；把人類的『做事習慣』硬套在 AI 身上，是錯的」 (Scrum, 7 / — / 3).
- NASA moved its strongest people to testing (Scrum, 19 / — / 5).

Implication: the user's 2025 dual-layer guardrail piece is about testing LLM applications. The community's pain in 2026 is the mirror image: testing code and tests written by LLM agents. Nobody in these groups has written the "how to review an AI-written test suite" guide, and a former tester with the LLST series is the natural author.

### 1.3 Specification is the new bottleneck: BDD, Example Mapping, Gherkin at scale

- Dan North via DavidKo: 「BDD 的本質是溝通，不是寫 Feature 檔」 (Scrum, 8).
- Blazej Drobniuch (Autodesk) fed an Example Mapping recording to Claude Code to draft Gherkin; 「有趣的不是 AI 寫得多好，而是——沒人會對 AI 的初稿執著，團隊終於願意放手討論」 (Scrum, 8 / — / 2).
- 「AI 幫你寫了四十條 Gherkin，然後呢？」 — AI does not know the exception rule made for a big customer three years ago (Scrum, 7).
- METR relayed: developers using AI were 19% slower yet believed they were 20% faster; requirements exploration is now the most congested segment of the value stream (Scrum, 4).
- 「RD 兩小時做完，PM 兩週後才發現做錯」 (Scrum 13 / — / 3; Agile 內湖).
- 水球潘's DDDTW 2025 talk: BDD + DDD to reach "AI 100% 全自動化後端開發"; 「沒有 DDD 的 BDD，無法支撐自動化；沒有 BDD 的 DDD，也無法驗證規格」 (DDDesign, 20 / — / 4). Companion talk 「文件即程式碼」 (16 / — / 2).
- ezKanban students: Miro Event Storming stickies converted to Use Case Spec, then fed to Pattern-Language skills; best demo paper at 台灣軟體工程研討會 (搞笑談軟工, 124 / — / 9).

Terminology: 實例化需求 (Specification by Example), 活文件, 文件即程式碼, 驗收條件 / AC, 3C (Card, Conversation, Confirmation).

Implication: Taiwanese agile people are converging on "spec is the harness". The user's AGENTS.md section touches this from the platform side; the team-level, tester-informed view of executable specs as the agent's input contract is missing.

### 1.4 Process and org under AI coding: local optimisation, review saturation, story size

- 陳正瑋 (DevOps Taiwan): 「AI 讓『不用跟任何人講話就能交付』的成本降到接近零 … 但這正是 LeSS 講的 local optimization：一個人的速度上去了，整個組織對系統的共同理解卻在流失 … 工程師該優化的從來不是 code，而是理解與連結」, quoting 柯仁傑's 「AI 時代，Scrum 真正在保護的東西」 (52 / 6 / 8).
- Kent Beck's career retrospective (fired by Apple, zero sign-ups for his TDD class at Facebook) and 「AI 時代累積不了的信任」 (DevOps Taiwan, 91 / — / 22).
- 「AI 把程式碼寫爆了，code review 怎麼辦？」 — PRs doubled after six months, senior calendars full of review, PRs queueing (Scrum 12 / — / 4; Agile 內湖).
- 「AI coding 時代，為什麼 story 要切得更小」 — AI touches twenty files at once and nobody can say which decision broke (Scrum 14 / — / 3).
- 「AI coding 時代不用 Scrum，還能用什麼？」 — Kanban, Shape Up, Spec-driven Development, Maintainer mode (Scrum 6 / — / 3).
- 「Anthropic 已經不分前後端，你要怎樣才能打造這樣的團隊？」; 「AI 時代還在列 task？那你列的東西 AI 一小時就做完了」 (Agile 內湖).
- 「敏捷不適合你的四種情況：AI 時代版」 — 「工具會忠實放大團隊現在的樣子」 (Agile 內湖).
- AgileTaipei Sept 17 meetup on FDE: 「FDE 是新瓶裝舊酒，還是真有骨架？」; 陳正瑋 asks whether FDE is 「下一種一條龍工程師」 (DevOps Taiwan, 23).
- 陳正瑋 relaying Weinberg: programmers becoming 「能解決人們一般問題的技術人員」 (33 / 4 / 5).

Implication: the user's Part 1 (Platform + Federation) is at the org-chart level. The community's live argument is one level down: what Scrum/LeSS ceremonies are for once individual throughput is free, how review capacity becomes the constraint, and whether FDE is a real role. Leaders reading these groups will want the team-level companion.

### 1.5 DDD and architecture meet non-determinism

- Kim Kao ran multi-agent extraction of bounded contexts from a legacy codebase via Domain Storytelling and Event Storming; each run returned a different number of contexts; 「這種類型的分析本來就很主觀」; 鮑承佑: 「LLM 本來就是一種根據機率分配產生輸出的 AI 模型，所以每次『骰』會有不一樣的結果」 (DDDesign, 16 / 3).
- DDDTW event hook: 「用 AI 寫程式越來越順，但過了幾個月打開那段程式，卻有點想不起來它為什麼長這樣」 (66 / 12 / 2 — the group's most-reacted post).
- Tom Smith: is 「.md 規範檔 + 簡潔的任務指令」 a form of DDD? 「有討論 DDD + Vibe Coding 的社群嗎？」 (6 / 10 comments).
- Kim Kao's tool poll, 73 votes: Claude Code 60%, Copilot 13%, Kiro 13%, Cursor 5%, Windsurf 1% — 「CC 幾乎是如同預期的佔據了整個市場」.
- Cloud Lab: 「社群上依舊看到各種互相 Diss Vibe 的文章 … 你現在幾手寫 code 的比例」; Kim Kao: 「你應該考慮讓只能 vibe 的人去使用 vibe，只要他們的產出能促進對話與認知那就是好的」 (9 / 1 / 2).
- Jed Lin rebuilt his Claude Code environment over Lunar New Year from `everything-claude-code`, adding C# support (32 / — / 5).
- Eric Evans "DDD & LLMs" (23 / — / 4); Stephen Tung (Event Store) on AI + DDD; Xin Yao's Sociotechnical Architecture talk.
- Backend 台灣: Triton Ho's event-based architecture mini-talk (125 / 13 / 12), async processing with a stock matching engine (124 / 7); Teddy buying Greg Young's Event Sourcing books (32).

Implication: DDD Taiwan is treating agents as a modelling collaborator, and has noticed the non-determinism problem the user wrote about in 與不確定性共舞. A bridge between that 2025 essay and Event Storming / bounded-context extraction with agents would land with this group (26 posts, the most active practitioner group by count).

### 1.6 Production incidents, capacity and zero trust (Backend 台灣)

- Reco Fu on the 台新證券 outage: 「不是 AI 失控，是架構容量設計錯誤」 (184 / 10 / 23); a comment blames underpaid senior engineers.
- Zeabur founder's statement on its security incident (103 / 5 / 19); 林奇葦's comment dissects initial access, control-plane reachability, lateral movement and 「大家的環境變數都存在一起」 (17 likes).
- AegisMeetings: zero-trust meeting transcription, XChaCha20-Poly1305 device-side encryption, keys that live only inside a Service Bus message (54 / 3 / 20), plus a follow-up on dual-wrap keys.
- Sync Session for zero-trust microservice session checks (43 / 6 / 9).
- 孫志貴: the lazier the user requirement, the harsher the engineering (n-gram IME); 黃宗賢's reply on inevitable complexity: 「前面叫軟體工程，後面叫政治學」 (19 / 3 / 2).

Implication: Backend 台灣 rewards incident analysis and security architecture write-ups with the highest share counts of any group. The agentic angle here is untouched: no one has written the Taiwanese "blast radius of a coding agent" piece, though the fear is visible in other groups (next cluster).

### 1.7 Agent safety and prompt injection

- Claude Taiwan: 「你們都讓 AI 上網查資訊嗎？有加裝防網路提示詞攻擊的措施嗎？」 (LlamaFirewall, mcp-context-protector); reply: 「模型本身就自帶防護 … 不需要使用者還要另外裝有的沒有的」 (4 / 2 / 2).
- OpenClaw/n8n group: 陳濬程's 「確定性治理煞車系統」 — the fear that under prompt injection an agent 「把我的本機專案目錄全清空？或是偷偷讀取了 .env 金鑰」.
- Claude Cowork Users: "A Claude AI agent bypassed safeguards and completely wiped a developer's 700 GB home directory" (6 / 2).
- Claude Taiwan: users auto-logged-out every 30 minutes; root cause was a usage-monitor tool sharing a key, tripped by Anthropic's anti-hijacking mechanism after a wave of stolen accounts (16 / 19).
- DevOps Taiwan: Red Hat joins NVIDIA Open Secure AI Alliance (4).

Implication: the Taiwanese consensus is thin and contradictory ("the model protects itself" vs. "install a firewall"). The user's sandbox/guardrail sections have the material for a definitive local piece; CKS/KCSA vocabulary (least privilege, network policy, secret hygiene) transfers directly.

### 1.8 Subscription economics, rate limits, outages, account risk (Claude Taiwan)

| Post | Engagement |
|---|---|
| Maple Kuo deleted Claude Desktop because Cowork's bundled VM takes 10 GB; 「256GB 自救會」 top comment | 340 / 29 / 49 |
| 「已租用 Claude Pro 版，若想再租用另一個 AI，應該會選哪家好呢？」 — top answers: Codex (as a Claude Code sub-agent via plugin), 「升 Max」 | 103 / 49 / 9 |
| Max 20x: 「每週基本都只把 Fable 5 用完，然後每週的總流量都用不完，有沒有什麼推薦的事情可以做？」 — answer: 「艦隊模式 … 兩名審查代理（證實、證偽），一名架構代理（防止過度設計）、一名總監工」 (21 likes) | 91 / 30 |
| Max 200 cannot use Fable in the morning; 「早上刷新 白嫖 70%」 | 39 / 9 |
| Claude outage again; Claude Status Monitor; 「一次兩個帳號報銷，只能用 Codex 來擋」 | 30 / 13 |
| Account banned with data inside; 「最近在思考要不要買但是又看到很多人突然被 ban」 | 19 / 9 |
| USD 100 credit vanished after plan expiry | 19 / 9 / 2 |
| Claude chat cannot read the private repo to review Claude Code output; reply: 「兩邊都吃同樣額度也是同模型，chat 又沒你本地的 skill 用，這是何苦」 | 13 / 15 |
| Gregg Chen's first autonomous `/routines` on Claude Code: two weeks of manual coordination before it stabilised | 7 / 1 |
| MCP group: tokens run out because every task re-reads half the project (context/memory) | 1 |
| Antigravity: nostalgia for DeepSeek v4 flash pricing; routers | 9 / 6 |
| Twinkle AI / Claude Taiwan: US export limits on Anthropic and Chinese state media naming Anthropic; 「發展主權模型 … 國家數位韌性」 | 35 / 5; 2 |

Terminology: 額度, 流量, 白嫖, 升 Max, 艦隊模式, 子 agent, 被 ban, 主權模型, TOKEN 自由 (from Teddy's Apple post, 76 reactions: 「本地用 LLM，實現 TOKEN 自由」).

Implication: the user's Part 3 covers unit economics at the platform level. The lived reality in Taiwan is individual Pro/Max seats, weekly quotas, vendor outages and account bans — a resilience problem (multi-vendor fallback, status monitoring, budget policy, local models) that no one has framed for a team lead.

### 1.9 MCP hubs, skills and sovereign data (Twinkle AI)

- 「台灣第一個 MCP Hub 上線」: all 49,343 data.gov.tw datasets behind one MCP server, for Claude Desktop / Cursor / 養龍蝦族 (OpenClaw users) / Hermes / Ollama / vLLM; 「你不用再浪費你的 tokens 了」 (15 / — / 7).
- Twinkle Hub official Skills: 「很多 Agent 的問題，不是沒有資料。而是：AI 不知道該怎麼用資料」 (16 / — / 1).
- Nationwide 實價登入 (6M records since 2012) inside the hub (7); 國考題庫 and AIA x Anthropic Developer Day 6/5 (14 / — / 5).
- vLLM's first Taipei meetup with Twinkle Eval (9); Hugging Face Ultra-scale Playbook translated to Traditional Chinese (7 / — / 5); OpenFormosa Barbet 1B (Mamba hybrid, 1M context); APMIC talk on fine-tuning tool-only small models for agents.

Implication: a concrete local MCP gateway exists and is publicly reasoning about token waste and skill design — ideal case material for the user's MCP gateway section, and an audience that reads Traditional Chinese.

### 1.10 Observability and AIOps — where the K8s conversation actually happens

- 莊硯光 (Backend 台灣): 「讀完對話串、合併 PR：用 Grafana、openab 與 Claude Code 打造第一線 AIOps 機器人」 — 「寫程式從來不是生產環境工程的瓶頸。除錯才是」 (39 / 2 / 17).
- OpenTelemetry Go compile-time instrumentation link (40 / 1 / 8).
- Grafana & Friends Taipei Meetup #3 on DB monitoring (DevOps Taiwan, 30).
- LinkedIn feed: Alolita S. (OTel GC) keynote at KubeCon Japan on GenAI semantic conventions for observing agentic systems (35 reactions).
- The Facebook GCP & K8s group contributes nothing (cheat-sheet spam); Kubernetes discussion for this user happens on LinkedIn and at KubeCon, not on Facebook.

Implication: the user is OTCA-certified and wrote the CNCF GenAI observability piece in Aug 2025, before agents. The community is now asking for agent-era tracing and AIOps bots; an update is overdue and has a ready audience.

### 1.11 Books and reading culture

- Kobo 10th anniversary: 73% off, 「10 周年沒有出新機我比較失望一點」 (67 / 30), gift-card nostalgia (21 / 22), daily Kobo99 picks, plenty of second-hand reader sales.
- 艦長，你有事嗎？ quoting Weinberg's 軟體管理學 on tools bought and left on the shelf (DevOps Taiwan, 21 / 2), Ansible 「Automation for Everyone」 (33 / 2 / 2), 全棧測試 shift-left.
- Clean Code 2nd ed. (190), Greg Young on Leanpub (32), the user's own 「剛在 Leanpub 上挖到寶 … Gerald M. Weinberg 著作」.

Implication: book-anchored posts still travel in these groups; the 藏書筆記 brand is not dated, it is the differentiator.

---

## 2. The user's own voice (Facebook profile + fan page 榮民叔叔的藏書筆記)

Fan page: 728 followers, following 109, tagline 「利用生命的最佳方式 就是把時間花在比生命更長久的事情上 閱讀與寫作」. The own book-club group last posted 14 weeks ago.

### Recurring themes

1. Testing philosophy (the spine of the page). Lessons Learned in Software Testing series (Lesson 7: 32 reactions, 6 comments; Lesson 8: 9; LLST #10: 7 shares), a YouTube 語音導讀 of the book (11 reactions, 14 shares), a Chapter 1 audio guide (「不是打勾機器，而是資訊的探勘者、風險的照明者」), James Bach's Taking Testing Seriously bought at 天瓏 and quoted: "Testing is the opposite of faith in the product. Testing begins with faith in the existence of trouble" (張少齊's reply singles out testers using vibe coding for 丟棄式的測試工具). Michael Feathers on testability, a Software Testability post, Full Stack Testing video, an ISTQB learning plan for a friend's graduating child (12 reactions, 3 shares), and the comic 「教召令派送的端到端測試記實」 (46 reactions, 8 comments).
2. XP and Kent Beck. Pragmatic Engineer interview (12 reactions), "90% of My Skills Are Now Worth $0" with notes dug out of Notion (16 reactions, 20 shares), 「你不能只靠一本書學會 Extreme Programming」 (11 reactions, 22 shares), the Care Bear story with daughter 檸檬 (8 shares), Planning XP chapter 1, pair programming video, LeSS in Action training (13).
3. Martin Fowler as trigger. Expert Generalists (14 reactions, 18 shares); LLMs Bring New Nature of Abstraction, which 「本來只是想隨手寫篇心得 … 差點又變成爛尾」 and became three long pieces (8 reactions, 4 comments, 21 shares); 建築的永恆之道 after the NVIDIA GenAI cert (9 reactions, 18 shares).
4. Certifications and conferences. OTCA as 「邁向 Golden Kubestronaut 第三站達標」, NVIDIA GenAI cert plus a notes site (fantasybz.github.io/adding-new-knowledge-to-llms), KubeCon Japan ("Keep Cloud Native Moving", the 50/60 Hz grid trivia), GTC Taipei workshop (21), an AGNTCon + MCPCon JP invitation, and a new direction: 「再次成為考生 挑戰專利師國家考試」 (60 reactions) with a PatentPrep v0 side project written up as product thinking (710 video views).
5. Small vibe-coded tools: Raycast Whisper Voice Input, Tabichō travel planner (20), an AgileTour attendance counter written with Cursor.
6. Long-form writing as identity. 「【原來長文還是有人看的！】17000 多字的長文 … 突破 100 reads」; a book project 「在非決定性的海面上守住品質」 announced as 長篇書籍寫作之旅; 「本來想說 OCTA 考完把這篇收尾，好險沒有拖到過年」; 「過程中還多虧 AI 幫忙校稿、潤飾」.
7. Older book-note series (2021–22): #QBQ (QBQ 22: 30 reactions), #essentialism, #禮記 #大學, #TOC It's Not Luck, #BCG問題解決力 (25, 9 shares), Lean Startup from HBR.

### Tone

Self-deprecating and warm: 「中年工程師大叔」, 「肥宅工程師」, 「哲學系之路轉了個彎」, honest about procrastination (爛尾), gratitude posts when a post crosses 100 reactions. Family appears (daughter, Tokyo/Yokohama family trip, running routes). Recent: 「久久還是要回廠導正一下三觀 — 馴服 AI 寫出可維護的系統：模式語言驅動開發工作坊」 (21 reactions), 「Teddy 說我是第一個報名 學號1號」, and 「上完這堂課，走去開車的路上腦中一直浮現以下對話」 (17).

### What drew reactions vs. shares

Personal-life posts win reactions (教召 免召 111, 42nd birthday 68, R.I.P. 良葛格 68, 專利師 60, 「曾經用 AI 做過什麼特別的事」 38). Technical shares win shares, not likes: XP 22, Fowler trilogy 21, Kent Beck 20, Expert Generalists 18, 建築 18, LLST audio 14. Shares are the right metric for the page's tech content, and they correlate with Medium views exceeding Medium impressions (section 4).

### Stated next steps

The book 在非決定性的海面上守住品質; the 專利師 exam and PatentPrep; the Golden Kubestronaut path (OTCA done, ICA/CCA next per the LinkedIn saves); the just-published Agentic Engineering series; and, from the workshop, Teddy's Pattern Language approach as something to metabolise.

---

## 3. LinkedIn signals

Saved posts (9, `linkedin_saved.txt`):

| Author | Topic |
|---|---|
| Kim Wüstkamp (killer.sh) | Scenario-based CNPE course on Killercoda |
| Ozioma Uzoegwu (AWS) | Claude Certified Architect (CCA): scenario exam, five domains — Agentic Architecture, MCP & Tool Design, Claude Code, Prompt Engineering, Context Management & Reliability; Partner Network only; three community guides |
| Veeranjaneyulu Chettupalli | "Claude dropped a full AI university" — 13 free courses (Claude 101, agent skills, Claude Code in Action, MCP intro/advanced, Bedrock, Vertex) |
| Ana Pedra | Golden Kubestronaut 2026 roadmap ranked by difficulty: KCNA → LFCS → CNPA → CKA → CKAD → KCSA → CKS → PCA → OTCA → ICA → CCA → KCA → CAPA → CGOA → CBA |
| Mykhailo T. | Istio Certified Associate tips |
| Sandipan Bhaumik | 20 YouTube channels for learning AI |
| Alexandre Zajac | 25 GitHub repos (system design, roadmaps, LLM 101) |
| Eric Schüler | ICA passed, 12/14 toward Golden Kubestronaut, prep stack (Mesh Week, Killercoda labs) |
| Puru Tuladhar | Cilium pod-to-pod encryption for CKS |

Feed flavour (8 items): CKA recertification, KubeAuto Day Paris, Alolita S.'s OTel GenAI SIG keynote (35 reactions), kubara, a CKA pass post with 112 reactions and 32 comments, KCD San Francisco, OpenShift Lightspeed multicluster AI, Cilium cert-manager badge. Recommended follows include Louis Cheng (Cathay United Bank SVP) and Shu Muto (NEC).

Reading: LinkedIn is the user's certification ladder and CNCF identity. Two threads matter for writing: the Golden Kubestronaut sequence (ICA and CCA are the next hard ones, and cert-pass posts draw 100+ reactions there) and the CCA, whose five domains line up almost exactly with the user's harness blueprint — a credential that could anchor an "agentic platform engineer" article.

---

## 4. Medium performance

Lifetime, Dec 27 2021 – Sep 5 2026. Presentations (impressions) are not reported for pre-2025 stories. Ratio = reads / views. September 2026 to date: 171 presentations, 39 views, 13 reads, +1 follower.

| Story | Date | Min | Pres. | Views | Reads | Ratio |
|---|---|---|---|---|---|---|
| Agentic Engineering, Part 2 — The Harness Blueprint (EN) | Sep 4, 2026 | 9 | 15 | 0 | 0 | n/a |
| Agentic Engineering, Part 1 — Who Does This? (EN) | Sep 4, 2026 | 7 | 20 | 4 | 2 | 50% |
| Don't Build Your Own Devin (EN overview) | Sep 3, 2026 | 14 | 26 | 3 | 0 | 0% |
| Agentic Engineering 三部曲（三）：Eval、單位經濟與規模化 | Sep 3, 2026 | 9 | 26 | 2 | 1 | 50% |
| Agentic Engineering 三部曲（二）：Harness 藍圖 | Sep 2, 2026 | 12 | 23 | 1 | 1 | 100% |
| Agentic Engineering 三部曲（一）：Platform + Federation | Sep 2, 2026 | 8 | 24 | 7 | 2 | 29% |
| 別急著打造你的 Devin：組織策略與 90 天行動藍圖 | Sep 1, 2026 | 19 | 21 | 19 | 7 | 37% |
| Restoring Observability (EN) | Dec 28, 2025 | 22 | 436 | 56 | 0 | 0% |
| 觀測的修復之道：從反模式到內化習慣的可觀測性思維 | Dec 28, 2025 | 27 | 422 | 86 | 21 | 24% |
| 在非決定性的海面上守住品質｜序 | Aug 21, 2025 | 17 | 432 | 21 | 8 | 38% |
| GenAI Observability in the CNCF Ecosystem (EN) | Aug 17, 2025 | 24 | 438 | 29 | 7 | 24% |
| LLM Dual-Layer Test Guardrails (EN) | Aug 17, 2025 | 18 | 153 | 506 | 33 | 7% |
| Dancing with Uncertainty (EN) | Aug 13, 2025 | 19 | 107 | 27 | 3 | 11% |
| 與不確定性共舞：LLM 時代的工程實踐與文化調適 | Aug 11, 2025 | 27 | 139 | 619 | 98 | 16% |
| 淺談 CNCF 生態下的生成式 AI Observability | Aug 11, 2025 | 49 | 124 | 130 | 44 | 34% |
| LLM 雙層測試護欄：從 Prompt 檢查到情境驗收 | Aug 10, 2025 | 47 | 95 | 106 | 10 | 9% |
| The Timeless Principles of Architecture (EN) | Jun 25, 2025 | 23 | 125 | 252 | 23 | 9% |
| 《建築的永恆之道》給軟體開發的啟示 | Jun 23, 2025 | 35 | 123 | 245 | 125 | 51% |
| 【LLST】#10 Beware of Testing Completely | May 27, 2025 | 9 | 143 | 73 | 16 | 22% |
| 你不能只靠一本書學會 Extreme Programming：第三章 | May 24, 2025 | 7 | 115 | 142 | 66 | 46% |
| 計畫不是預言書，是應變指南 — Planning XP ch.1 | May 10, 2025 | 5 | 126 | 53 | 14 | 26% |
| 【Perfect Software】重讀之旅緣由 | May 24, 2023 | 4 | — | 62 | 24 | 39% |
| LLST #8 You focus on failure… | May 15, 2023 | 4 | — | 19 | 7 | 37% |
| LLST #7 Question everything… | May 15, 2023 | 4 | — | 16 | 3 | 19% |
| LLST #6 Run with the programmers | May 12, 2023 | 4 | — | 15 | 3 | 20% |
| LLST #5 Find important bugs fast | May 12, 2023 | 4 | — | 12 | 0 | 0% |
| LLST #4 You discover things that will "bug" someone… | May 12, 2023 | 5 | — | 9 | 0 | 0% |
| LLST #3 You serve many clients | May 12, 2023 | 6 | — | 15 | 3 | 20% |
| LLST #2 Your mission drives everything you do | May 12, 2023 | 5 | — | 132 | 4 | 3% |
| LLST #1 You are the headlights of the project | May 12, 2023 | 3 | — | 20 | 5 | 25% |
| Chapter 1. The Role of the Tester | May 12, 2023 | 4 | — | 34 | 6 | 18% |
| 【讀書筆記】軟體測試的經驗傳承 | May 12, 2023 | 3 | — | 35 | 5 | 14% |
| 【讀書筆記】Exploratory Testing in the Large | May 12, 2023 | 3 | — | 47 | 20 | 43% |
| Software Design: Tidy First? 讀後心得 (一) | Jul 13, 2022 | 16 | — | 844 | 145 | 17% |
| Exploratory Software Testing — Historical district | Jul 8, 2022 | 6 | — | 67 | 15 | 22% |
| 那些年錯過的 XP 叢書 — XP Explained 序、前言、第一章 | May 16, 2022 | 16 | — | 164 | 47 | 29% |
| Exploratory Software Testing — Business District | May 9, 2022 | 12 | — | 202 | 49 | 24% |
| FE Debug Skill — Cookies 無效 | Feb 28, 2022 | 28 | — | 739 | 60 | 8% |
| 【讀書筆記】你所不知道的必學前端 Debug 技巧 | Feb 25, 2022 | 13 | — | 1,600 | 232 | 14% |
| FE Debug Skill — CORS 錯誤 | Feb 13, 2022 | 4 | — | 143 | 26 | 18% |
| 【課程筆記】不確定時代下的敏捷測試 | Dec 28, 2021 | 5 | — | 3,000 | 307 | 10% |

Aggregates:

| Slice | Stories | Views | Reads | Ratio |
|---|---|---|---|---|
| 2025 Chinese | 9 | 1,475 | 402 | 27% |
| 2025 English | 5 | 870 | 66 | 8% |
| 2026 Chinese (4 days old) | 4 | 29 | 11 | 38% |
| 2026 English (2 days old) | 3 | 7 | 2 | 29% |
| 2023 (testing series) | 12 | 416 | 80 | 19% |
| 2022 | 7 | 3,759 | 574 | 15% |
| ≥ 20 min read | 9 | 2,262 | 388 | 17% |
| 10–19 min | 10 | 3,387 | 525 | 16% |
| < 10 min | 22 | 3,907 | 529 | 14% |

### Analysis

- Chinese carries the readership. The 2025 Chinese set collected six times the reads of the English set (402 vs 66) at 27% vs 8% completion. English editions pick up impressions and drive-by views but not reads: Restoring Observability EN had 436 impressions and 56 views with zero reads; LLM Dual-Layer EN had 506 views at 7%. Keep publishing English for discoverability, but plan on Chinese as the edition that gets finished.
- Views above impressions signal external traffic. 與不確定性共舞 (139 impressions, 619 views) and 建築 (123 impressions, 245 views) were carried by the fan-page shares (21 and 18 shares respectively). The Dec 2025 observability pair got the opposite: Medium showed them 858 times but only 142 people clicked. Distribution from the user's own Facebook network beats Medium's feed for this author.
- Book-anchored long reads finish best. 建築的永恆之道 (35 min) at 51% is the highest completion of any story with meaningful volume; the XP chapter at 46%; CNCF GenAI Observability (49 min) at 34%. Length is not the problem; the 17,000-character piece the user celebrated is the one with 125 reads.
- Pure-method pieces finish worst. LLM 雙層測試護欄 CN 9%, EN 7%; both observability-anti-pattern editions 24% and 0%. The culture essay (與不確定性共舞) got the most 2025 reads (98) despite 16% completion, which says the hook and the share travelled even where the length did not.
- The 2026 Agentic Engineering series is four days old: 155 impressions, 36 views, 13 reads across seven stories. The Chinese overview (別急著打造你的 Devin, 19 views / 7 reads) is the entry point; the parts are barely seen yet. Too early to judge, but the pattern from 2025 says the fan-page share, not Medium distribution, will decide it — and as of the scrape the fan page has no post about the series.
- All-time volume still comes from practical, searchable Chinese notes: 敏捷測試 course notes (3K views), 前端 Debug 技巧 (1.6K), Tidy First (844), FE Cookies (739). Topic choice for reach: concrete, tool-adjacent Chinese titles; for completion: book-anchored essays.

---

## 5. Opportunities and gaps

Angles the community data supports that are not covered by the published series (2026: org design, harness blueprint, evals/unit economics/scaling gates; 2025: LLM-era culture, dual-layer test guardrails, GenAI observability in CNCF, observability anti-patterns, architecture principles; 2023: LLST).

1. Reviewing tests an agent wrote — the tester's guide. Anchor: DavidKo's 「AI 說沒問題」 and 「它把斷言改掉了」, Lada Kesseler's "trust AI tests less than AI code", Uncle Bob's mutation-test gate (40 reactions). The user's LLST voice plus the dual-layer framing, turned around to cover agent-authored code. Gap: nothing in Chinese covers assertion loosening, frozen bugs, and what a mutation score buys you in an agent loop.
2. Reproducibility as a harness metric: answer Teddy's question. The 298-reaction post asks whether a fixed spec yields the same implementation without human intervention; Kim Kao's bounded-context counts vary per run; students measured LOC variance. An article that defines output variance under fixed spec as an eval (extending Part 3) and compares Pattern Language, AGENTS.md conventions and skills as variance reducers. The user attended the workshop; this is first-hand material.
3. Code review as the new constraint. PRs doubled, senior calendars saturated (Scrum, Agile 內湖); the 艦隊模式 answer (證實/證偽 reviewer agents, an architect agent against over-design, a supervisor) got 21 likes in Claude Taiwan. Nobody has written the review-capacity design for a Taiwanese team: reviewer agents, smaller stories, what a human must still read.
4. Resilience for seat-dependent teams: quotas, outages, bans, fallbacks. Section 1.8's 340/103/91-reaction threads are about Pro vs Max, weekly Fable quotas, two banned accounts, USD 100 credits lost, a 10 GB Cowork VM, and Codex as a stand-in. Part 3 covers platform unit economics; the missing piece is a team-lead policy: multi-vendor fallback, status monitoring, budget guardrails, when local models (「TOKEN 自由」) are worth it.
5. Blast radius of a coding agent: sandbox, secrets, prompt injection, done properly. The 700 GB wipe, the `.env` fear, the "does the model protect itself" argument, and the Zeabur incident thread (103 reactions, 19 shares; env vars stored together, no second permission layer). A Backend 台灣-style incident-analysis piece that maps CKS/KCSA controls onto agent runtimes — the group that shares security write-ups most.
6. Agent-era observability: OTel GenAI semantic conventions, traces as eval evidence, AIOps bots. 莊硯光's Grafana + Claude Code AIOps bot (17 shares) says 「除錯才是」 the bottleneck; Alolita's KubeCon Japan keynote; the user is OTCA-certified and wrote the pre-agent CNCF piece. An update that instruments the harness itself (cost per trace, tool-call spans, eval-in-prod) closes a loop between the 2025 and 2026 series.
7. Spec as the agent's input contract: from Example Mapping to executable spec. Dan North's "BDD is communication", the Autodesk Example Mapping → Claude Code → Gherkin flow, 「四十條 Gherkin，然後呢？」, 水球潘's BDD+DDD automation claim, 文件即程式碼. A tester-informed piece on what a spec must contain for an agent and a human to both accept it, tying into the AGENTS.md section.
8. What Scrum/LeSS protects when individual throughput is free. 陳正瑋's local-optimisation post (52 reactions, 8 shares), Kent Beck's "trust you cannot accumulate in the AI era" (91 / 22 shares), FDE at AgileTaipei Sept 17. Team-level companion to Part 1: shared understanding as the asset, smaller stories, ceremonies that survive, whether FDE is a role or a symptom.
9. Brownfield harnesses: making legacy legible to agents. DevOps Taiwan Meetup #80 「與 Coding Agent 在棕地專案中可靠協作」, Kim Kao's agents extracting bounded contexts via Domain Storytelling / Event Storming, Jed Lin adding C# to everything-claude-code, DDDTW's 「想不起來它為什麼長這樣」 (66 reactions). The Harness Blueprint reads greenfield; Taiwanese enterprises are mostly brownfield.
10. A certification map for the agentic platform engineer. Golden Kubestronaut sequence (Ana Pedra's roadmap saved; user at OTCA), Claude Certified Architect's five domains (saved), NVIDIA GenAI, ISTQB asked by a friend's kid. Cert posts draw 100+ reactions on LinkedIn; the 2025 CNCF piece with 認證 in the title finished at 34%. Also a natural place to reflect the 專利師 detour as a mid-career story.
11. MCP gateway in practice: what Twinkle Hub teaches. 49,343 datasets behind one MCP server, 「AI 不知道該怎麼用資料」, skills as the fix, `gh skill install` and agentskills.io as the packaging standard. Case study for the MCP gateway section with a Traditional-Chinese audience already engaged.
12. Book-anchored: Taking Testing Seriously in the agent era, or "Clean loop, not clean code" on Clean Code 2nd ed. The user already bought Bach's book and quoted it; Clean Code 2nd ed. drew 190 reactions and 38 shares; Weinberg's tools-on-the-shelf line (21 reactions) is a ready frame for agent-platform adoption. Book essays are the user's highest-completion format (51%, 46%, 34%).

Sequencing suggestion from the data: post the Agentic Engineering series on the fan page first (its 2025 shares are what moved Medium views), then pick angles 1, 2 and 4 — they sit on the three highest-engagement threads in the dataset and on the user's tester identity, which the community already associates with the page.
