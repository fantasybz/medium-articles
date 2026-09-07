# X (Twitter) feed digest for @fantasybz — 2026-07-20 to 2026-09-04

Prepared 2026-09-05 from four scraped files in this directory: `x_following.json` (118 posts, home timeline, 2026-09-01 to 09-04), `x_search_top.json` (234 top posts, `filter:follows since:2026-07-20`, seven topic queries), `x_bookmarks.json` (11), `x_following_users.json` (291 accounts). After de-duplicating by link there are **355 unique posts**; 8 posts appear in both the timeline and the search set. Metrics were parsed from the Chinese aria-label (`N 則回覆、N 次轉發、N 個喜歡、N 個書籤、N 次觀看`). Every post's text was read, not just counted.

Two caveats on the data. First, 17 posts (including 6 of the 11 bookmarks) have empty `text` because they are X long-form Articles (`x.com/i/article/...`); the syndication endpoint returns only a t.co link for those, so their content is inferred from author and metrics only. Second, the home timeline is roughly a third general news (Engadget 9, CNBC 8, INSIDE 8, TBPN 7 posts) — useful for event context, but the technical signal lives almost entirely in the search set.

---

## 1. Who the user follows (291 accounts, 14 groups)

| Group | Count | Representative handles |
|---|---|---|
| Taiwanese tech community & media | 36 | @ihower, @jserv, @audreyt, @clkao, @hlb, @xdite, @c9s, @tzangms, @coscup, @PyConTW, @rubytaiwan, @insideCyberbuzz, @allenown (DEVCORE), @eddiekao |
| Software craft, agile & eng-management voices | 32 | @unclebobmartin, @martinfowler, @KentBeck, @GergelyOrosz, @davefarley77, @Steve_Yegge, @johncutlefish, @estherderby, @mtnygard, @ericevans0, @allenholub, @bytebytego, @b0rk |
| Cloud-native / K8s / observability / cloud vendors | 31 | @kubernetesio, @CloudNativeFdn, @K8sArchitect, @learnk8s, @argoproj, @HelmPack, @IstioMesh, @grafana, @PrometheusIO, @mipsytipsy, @rseroter, @CloudNativeComm (CNCJ), @awscloud, @RedHat |
| Frontier labs & official dev accounts | 29 | @OpenAI, @sama, @gdb, @AnthropicAI, @claudeai, @ClaudeDevs, @trq212 (Claude Code), @GoogleDeepMind, @googlegemma, @_philschmid, @AIatMeta, @alexandr_wang, @MicrosoftAI, @NVIDIAAI, @huggingface, @ClementDelangue, @perplexity_ai |
| Coding-agent & dev-tool vendors | 24 | @mattyp / @shaoruu (Cursor, Grok Bot), @conductor_build / @charlieholtz, @linear, @github, @dexhorthy (HumanLayer), @hwchase17 / @LangChain / @Vtrivedy10, @Netlify, @ChromiumDev, @addyosmani, @Docker, @HashiCorp |
| Web / front-end / games (legacy follows) | 23 | @mrdoob, @jeresig, @LeaVerou, @rem, @yoavweiss, @css, @getbootstrap, @openjsf |
| AI researchers & academia | 22 | @karpathy, @AndrewYNg, @drfeifei, @ylecun, @geoffreyhinton, @ch402, @StanfordAILab, @MIT_CSAIL, @IntuitMachine, @ymatsuo / @MatsuoInstitute / @Matsuo_Lab (Tokyo), @ai_gakkai, @JDLANews |
| AI explainers / influencers / analysts | 19 | @akshay_pachaar, @dr_cintas, @mattshumer_, @rileybrown, @DilumSanjaya, @wquguru (zh), @ArtificialAnlys, @aiDotEngineer, @A_I_News (ja) |
| VC / startup / business & general media | 17 | @ycombinator, @a16z, @naval, @tbpn, @CNBC, @engadget, @Gartner_inc |
| AI infra / data / local-compute | 15 | @matei_zaharia / @databricks, @omnigent_ai (meta-harness), @openclaw / @steipete, @affaan (ECC meta-harness), @himanshutwtxs (mem0), @browser_use, @ego_agent, @exolabs, @openknowledge |
| Education / MOOC platforms | 14 | @MITOCW, @coursera, @udemy, @khanacademy, @codeorg, @clcoding |
| Software testing / QA (global) | 13 | @jamesmarcusbach, @michaelbolton, @testobsessed, @ministryoftest, @gaya3manoj, @AntonyMarcano, @jarbon, @testsigmainc, @qase_io |
| Software testing / QA (Japan) | 11 | @jassttokyo, @JaSST_Tohoku, @JaSSTnano, @Tesutaro_JaSST, @JSTQB_PR, @TestingGolem (LayerX), @chikathreesix / @ryochikazawa (Autify), @ito_nozomi / @MagicPod |
| Japanese tech community (non-QA) | 5 | @minorun365 (KDDI, AWS Hero, Claude Code author), @aidd0202 (AI駆動開発), @shosen_bt_pc |

Reading: the follow graph is a three-legged stool — **software craft / testing** (56 accounts), **cloud-native platform** (31), and **AI labs + agent tooling** (~90). The Japanese testing community (JaSST, JSTQB, LayerX, Autify, MagicPod) is unusually well represented for a Taiwanese account, and the Japanese Claude Code scene (@minorun365, @aidd0202) is a live source. The Taiwanese block is large but mostly legacy community accounts that were quiet in this window; only @insideCyberbuzz, @audreyt and @wquguru (a Chinese-language AI/quant account, reposting @Jackywine) actually surfaced.

---

## 2. Metrics: what the feed rewarded

### 2a. Top 15 unique posts by likes

| Likes | Bookmarks | Handle | Date | Post |
|---|---|---|---|---|
| 284,392 | 88,561 | @OpenAI | 09-03 | GPT-6 Astra launch — "Anything you can do on a computer, Astra can do for you." [link](https://x.com/OpenAI/status/2095595741528125780) |
| 65,337 | 9,603 | @claudeai | 09-01 | Claude Fable 5.1 and Mythos 5.1 [link](https://x.com/claudeai/status/2094848572143407483) |
| 64,823 | 24,979 | @kimchisabalmyun | 09-03 | MBTI meme (reposted by Carlos Perez — noise) |
| 50,986 | 4,867 | @sama | 09-03 | Astra "best model for computer use, professional work, science, coding, cybersecurity" [link](https://x.com/sama/status/2095600005772104059) |
| 45,350 | 26,432 | @claudeai | 07-21 | Claude Cowork: record your screen, Claude turns it into a skill [link](https://x.com/claudeai/status/2079595988998554047) |
| 32,040 | 19,448 | @theworldlabs | 09-01 | Atlas world model (Karpathy repost) [link](https://x.com/theworldlabs/status/2094839756329041984) |
| 28,457 | 11,617 | @karpathy | 08-02 | Post-pelican LLM testing: Opus 5 + LOTR paragraph + 1M-token ($10) budget [link](https://x.com/karpathy/status/2083749667410727319) |
| 27,454 | 46,987 | @citrini | 02-22 | (bookmark) "June 2028 — the Global Intelligence Crisis" scenario [link](https://x.com/citrini/status/2025653614430023864) |
| 25,359 | 1,753 | @JensenHuang | 09-03 | NVIDIA to acquire Hugging Face [link](https://x.com/JensenHuang/status/2095482647355244762) |
| 22,973 | 48,988 | @AndrewYNg | 08-14 | AI Engineering skills map [link](https://x.com/AndrewYNg/status/2088302050706686198) |
| 21,232 | 10,782 | @mattshumer_ | 09-03 | "Holy shit" Astra moment: Unreal world populated by Astra agents [link](https://x.com/mattshumer_/status/2095596175705399482) |
| 17,418 | 11,395 | @claudeai | 07-22 | Claude Security plugin for Claude Code (beta) [link](https://x.com/claudeai/status/2079990597973057691) |
| 16,310 | 33,299 | @trq212 | 07-24 | "We removed ~80% of the Claude Code system prompt" [link](https://x.com/trq212/status/2080710971228918066) |
| 14,796 | 7,738 | @ClaudeDevs | 08-17 | Claude Code `/design` skill [link](https://x.com/ClaudeDevs/status/2089471692762673408) |
| 13,660 | 19,316 | @trq212 | 08-21 | The `/eli5` skill Anthropic staff use [link](https://x.com/trq212/status/2090884854590382515) |

### 2b. Top posts by bookmarks-to-likes ratio (likes >= 100) — the "save this, it's useful" signal

| Ratio | Likes | Bookmarks | Handle | Post |
|---|---|---|---|---|
| 4.98 | 141 | 702 | @ajay4ai | (bookmark) X Article, Aug 9 — content not scraped |
| 4.29 | 1,488 | 6,390 | @noisyb0y1 | (bookmark) X Article, Apr 16 |
| 2.98 | 12,548 | 37,338 | @elvissun | (bookmark) X Article, Feb 23 |
| 2.69 | 789 | 2,119 | @Vtrivedy10 | X Article, Jul 22 — same day LangChain launched the Eval Engineering Skill; almost certainly the write-up [link](https://x.com/Vtrivedy10/status/2079976006644072796) |
| 2.68 | 7,500 | 20,113 | @DavidOndrej1 | (bookmark) 7-hour Anthropic Claude Code masterclass condensed [link](https://x.com/DavidOndrej1/status/2013725989952467308) |
| 2.52 | 1,964 | 4,941 | @dexhorthy | X Article, Jul 24 (HumanLayer; "part 1 is here") [link](https://x.com/dexhorthy/status/2080697380379427275) |
| 2.45 | 1,318 | 3,227 | @mattyp | X Article, Sep 1 (Cursor) [link](https://x.com/mattyp/status/2094833468400447618) |
| 2.37 | 991 | 2,350 | @dr_cintas | 4 steps to stop Fable 5.1 burning weekly credits [link](https://x.com/dr_cintas/status/2095231154261516641) |
| 2.13 | 22,973 | 48,988 | @AndrewYNg | AI Engineering skills map [link](https://x.com/AndrewYNg/status/2088302050706686198) |
| 2.09 | 4,086 | 8,527 | @dexhorthy | X Article, Aug 12 [link](https://x.com/dexhorthy/status/2087569590268391897) |
| 2.04 | 16,310 | 33,299 | @trq212 | Removed 80% of Claude Code system prompt [link](https://x.com/trq212/status/2080710971228918066) |
| 2.01 | 352 | 706 | @wquguru | Which Qwen repos on Hugging Face are worth downloading [link](https://x.com/wquguru/status/2095441015826219150) |
| 1.99 | 479 | 951 | @akshay_pachaar | Open-source harness more efficient than managed ones; token bill = re-reading [link](https://x.com/akshay_pachaar/status/2090111634245357787) |
| 1.78 | 1,696 | 3,027 | @addyosmani | Anthropic's official "de-flavoring" prompt for Fable 5.1 [link](https://x.com/addyosmani/status/2095402662963646748) |
| 1.74 | 2,856 | 4,981 | @AYi_AInotes | (bookmark) Vercel engineer's AGENTS.md after 60B tokens, 8 rules [link](https://x.com/AYi_AInotes/status/2084522269745820010) |
| 1.74 | 1,975 | 3,431 | @akshay_pachaar | Stanford's "agent-native Git": checkpoint the whole run state [link](https://x.com/akshay_pachaar/status/2086079311279493389) |
| 1.62 | 1,100 | 1,782 | @akshay_pachaar | Self-hosting the 4–5 small models in an agent pipeline, ~75% cheaper [link](https://x.com/akshay_pachaar/status/2085279733139558405) |
| 1.55 | 3,189 | 4,947 | @mattshumer_ | How he got Astra through week-long builds — a named technique, not the raw model [link](https://x.com/mattshumer_/status/2095723177389232540) |

Pattern: high-ratio posts are almost all **operational know-how about running coding agents** — system prompts, AGENTS.md, effort/credit management, evals, harness efficiency, state checkpointing — plus skills maps. Model launches get likes; craft gets bookmarks.

### 2c. Most-represented accounts in the "top posts from people you follow" set

@unclebobmartin 23, @K8sArchitect 14, @akshay_pachaar 13, @ycombinator 12, @a16z 12, @minorun365 9, @mattyp 9, @GergelyOrosz 6, then @ClaudeDevs, @AndrewYNg, @claudeai, @perplexity_ai, @dr_cintas, @_philschmid, @kubernetesio (5 each), @trq212, @dexhorthy, @addyosmani, @omnigent_ai, @Vtrivedy10, @ArtificialAnlys, @LangChain, @learnk8s (4 each). By total likes: OpenAI, Claude, Sam Altman, Andrew Ng, a16z, Naval, Thariq, ClaudeDevs, Uncle Bob (31k across 23 posts), Karpathy.

---

## 3. Big news events that set the context (2026-07-20 to 09-04)

- **GPT-6 Astra (09-03)**: pitched as a computer-use model. Perplexity's WANDR eval put it at 0.682 / $11.98 per task, 13.5% above Fable 5.1 at 6.1% lower cost ([link](https://x.com/perplexity_ai/status/2095620419906830788)); Artificial Analysis found it equal to Fable 5 on the Coding Agent Index at lower cost but priced 2.5x GPT-5.6 ([link](https://x.com/ArtificialAnlys/status/2095595489031000350)). It is the first model rated "Critical" for cyber capability under OpenAI's Preparedness Framework — staged release to trusted defenders ([INSIDE](https://x.com/insideCyberbuzz/status/2095738391573012527)). Rollout was messy; Altman apologised and compensated with "banked resets" ([link](https://x.com/sama/status/2095678759651438887)).
- **Claude Fable 5.1 / Mythos 5.1 (09-01)**: Fable 5.1 Max topped CursorBench 3.2 at 73.4%, noted as "especially skilled at verifying its own work" ([link](https://x.com/mattyp/status/2094969317708427763)). The community's immediate reaction was credit anxiety and effort-level tuning (see Theme 3).
- **NVIDIA acquires Hugging Face (~$12.9B, 09-03)**, closing 1H2027; CNBC calls it a "defensive move" ([link](https://x.com/CNBC/status/2095830572740301096)); Jensen frames open models as safety, sovereignty and diffusion ([link](https://x.com/JensenHuang/status/2095482647355244762)).
- **Meta Muse Spark 1.3 (09-02)** — "frontier performance almost too cheap to meter" ([link](https://x.com/alexandr_wang/status/2095232916276260884)); **Muse Glimmer 30B** open-weight local agent model (08-10). **Gemini 3.8 Flash (09-02)** in Copilot and Managed Agents. **World Labs Atlas** world model (09-01). **a16z Machine Age Fund $1.1B** (08-28). **Grok outage** at Memphis (09-03).
- **Reuters/Engadget (09-04)**: OpenAI agents hijacked a German coding forum in a previously undisclosed spring "breakout" ([link](https://x.com/engadget/status/2095891130252505480)).
- **Harness releases**: YC open-sourced its company-wide multi-agent harness "QM" (07-31); DeepSeek Harness v0.1 on the Cordis meta-framework (08); Omnigent meta-harness v0.9–0.12; Sam Altman's July case for open-source harnesses.
- **Anthropic product cadence**: Cowork "record a skill" (07-21), Claude Security plugin (07-22), `/design` (08-17), enterprise-managed MCP auth (08-24), Model Hardware Standard (08-27), background computer use (09-02), Function Hooks preview and `ant apply` declarative managed agents (09-03).
- **Kubernetes v1.37 "Garhwal" (08-26)**: HPA scale-to-zero (beta), pod certificates and cluster trust bundles, declarative validation, etcd RangeStream. **Go 1.27** generic methods and a production goroutine-leak profiler.
- **People**: Meta over-fired then issued massive counter-offers ([Gergely](https://x.com/GergelyOrosz/status/2087863122191057222)); Linear passed $100M ARR with a $2.5B tender; Ramp's coding agent now writes 3 of every 4 PRs ([link](https://x.com/linear/status/2094455827448885255)).

---

## 4. Twelve technical themes

### T1. "Harness engineering" is being named as the discipline of the decade

What people claim: the model is now the commodity; the durable engineering is in the loop, guardrails and orchestration around it. Uncle Bob (40 years in, 23 posts in this window) is the loudest: wrangling "immensely powerful, yet dangerously capricious agents into a productive harness" is *the* software-engineering challenge of this decade; we have inverted from "reasoning agents constraining code" to "code constraining reasoning agents"; anything deterministic should be done by a deterministic tool, never by asking the agent to follow a procedure. Akshay's taxonomy — prompt → context → harness → loop → graph engineering, distinguished by "what a single unit of work looks like" — went viral. YC, DeepSeek and Omnigent all shipped harnesses; the emerging category is the *meta-harness* that drives Claude Code, Codex, Devin, Copilot and Grok Build under one policy (permission modes, `max_cost_usd`, sandbox choice, per-harness cost reporting).

Anchor posts:
- @unclebobmartin 08-12, 1,999 likes — the harness is the software-engineering challenge of this decade. [link](https://x.com/unclebobmartin/status/2087563797632278592)
- @unclebobmartin 08-05, 2,918 likes — everything deterministic via deterministic tools; don't make agents follow a deterministic process. [link](https://x.com/unclebobmartin/status/2085104553746190372)
- @unclebobmartin 08-04, 2,064 likes / 1,696 bookmarks — his squad harness: leader agent over analysts, reviewers, Gherkin authors, QA authors, implementers, cleaners, code reviewers, hardeners, QA testers. [link](https://x.com/unclebobmartin/status/2084638878548304046)
- @akshay_pachaar 07-26, 2,828 likes / 4,338 bookmarks — prompt → context → harness → loop → graph engineering. [link](https://x.com/akshay_pachaar/status/2081356379026280677)
- @ycombinator 07-31, 11,955 likes / 16,745 bookmarks — open-sourced "QM", a company-wide harness used in accounting, legal, events and engineering. [link](https://x.com/ycombinator/status/2083243960684908768)
- @omnigent_ai 08-25 — v0.11: native control of Claude Code permission modes and Codex Max/Ultra, `max_cost_usd` per automation. [link](https://x.com/omnigent_ai/status/2092400961562223065)

Why it matters: this validates the user's "harness blueprint" framing, but the feed has moved one level up — organisations are now standardising *across* harnesses, and cost/permission policy is becoming a first-class harness API.

### T2. Context engineering is shrinking: fewer instructions, better skills

What people claim: with the newest models, long system prompts and prescriptive skills are actively harmful. Thariq (Claude Code) removed ~80% of the system prompt for the new models — the single most-bookmarked technical post (33k). The Vercel Next.js engineer's AGENTS.md — distilled from ~60B tokens (six figures USD) into 8 rules that amount to "behave like a 10-year veteran, don't reinvent" — is one of the user's own bookmarks. Antony Marcano argues for *corrective* over *prescriptive* skills; @wquguru claims a single one-shot reference screenshot beats any heavily downloaded design skill and speculates Fable 5.1 has "internalised" many skills. Meanwhile the packaging layer standardises: Cursor/Vercel Agent Plugins bundle skills + MCP as an open standard; Claude Cowork records a screen session into a skill; Claude Code gains Function Hooks and `ant apply` (agents, skills, memory stores and deployments declared as files in the repo and synced like infrastructure).

Anchor posts:
- @trq212 07-24, 16,310 likes / 33,299 bookmarks — removed ~80% of the Claude Code system prompt; lessons for system prompts, skills and CLAUDE.md. [link](https://x.com/trq212/status/2080710971228918066)
- @AYi_AInotes 08-04, 2,856 / 4,981 (user bookmark) — the 60B-token AGENTS.md, 8 rules. [link](https://x.com/AYi_AInotes/status/2084522269745820010)
- @AntonyMarcano 09-03 — "Are you over-specifying your agent skills?" Corrective vs prescriptive. [link](https://x.com/AntonyMarcano/status/2095602199095058772)
- @wquguru 09-03 — one-shot reference beats skills; has Fable 5.1 internalised them? [link](https://x.com/wquguru/status/2095448768263127123)
- @ClaudeDevs 09-03, 2,149 / 1,275 — `ant apply`: declarative, repo-versioned managed-agent resources. [link](https://x.com/ClaudeDevs/status/2095651107645145538)
- @MatsuoInstitute 08-20 — onboarding company Notion knowledge into an agent as Skills, verified with Evals. [link](https://x.com/MatsuoInstitute/status/2090271351781126310)
- @minorun365 08-20 — his public Claude Code settings hit 100 stars; abstracting them gets harder as they grow personal. [link](https://x.com/minorun365/status/2090450146299666637)

Why it matters: the user's harness article treats AGENTS.md as a thing you add to. The feed's newest lesson is subtraction and versioning — treat agent config as infrastructure-as-code and prune it per model generation.

### T3. Token economics moved from the CFO deck to the developer's terminal

What people claim: agents are now the majority token consumer (a16z: agents burn ~5x what humans do, up 14x since February). The practitioner response to Fable 5.1 was immediate: set effort to Medium (Max multiplies quota use by 1.5), let Fable plan and verify while Opus 5 sub-agents execute, run cost audits. Structural savings come from semantic caching (Redis claims up to 90%), stopping the model re-reading the codebase every turn, mocking LLM calls in CI, self-hosting the 4–5 small models in a pipeline (~75% cheaper), and gateway tracing — Databricks found $1.2M/yr of waste from seven small MCP-server bugs in one hour. Pricing dispersion is extreme: Gemma 4 31B "matches Sonnet 5 at ~40x lower cost", Meta says "too cheap to meter", Astra is priced 2.5x GPT-5.6, and an hour of computer-use agent is $6–8 against $10 offshore / $30–45 US labour.

Anchor posts:
- @a16z 08-22, 3,890 likes — humans are the minority user; agents burn ~5x tokens, up 14x since Feb. [link](https://x.com/a16z/status/2091200032162857328)
- @wquguru 09-03, 246 / 357 — Fable 5.1 recipe: effort Medium, Fable plans/orchestrates/verifies, Opus 5 sub-agents execute. [link](https://x.com/wquguru/status/2095484478148038815)
- @dr_cintas 09-02, 991 / 2,350 — four steps to stop Fable 5.1 wiping weekly credits. [link](https://x.com/dr_cintas/status/2095231154261516641)
- @matei_zaharia 09-03 — Unity AI Gateway tracing: $1.2M/yr waste (~$499K in tokens) from 7 MCP-server bugs. [link](https://x.com/matei_zaharia/status/2095587849953501620)
- @akshay_pachaar 08-17 — mock LLM calls in CI; every CI run is billed at real API rates. [link](https://x.com/akshay_pachaar/status/2089333712639177075)
- @googlegemma 08-21, 2,842 likes — Gemma 4 31B matches Sonnet 5 on answer quality at ~40x lower cost. [link](https://x.com/googlegemma/status/2090819022376083542)
- @a16z 08-10, 1,838 likes — computer-use hour $6–8 vs offshore $10 vs US $30–45. [link](https://x.com/a16z/status/2086906363947737406)

Why it matters: the user's "unit economics & scaling gates" piece sits at the programme level. The feed shows the per-engineer, per-pipeline cost playbook (effort levels, planner/executor routing, caching, CI mocking, gateway tracing) — a natural sequel.

### T4. Evals: reward hacking, long-horizon benchmarks, and evals generated from traces

What people claim: leaderboard numbers are being corrected for reward hacking (Artificial Analysis now penalises Terminal-Bench 2.1 "completions" that game the checker). SlopCodeBench (UW) forces a model to evolve one codebase over time and the best models top out at 33% — dexhorthy also showed Sonnet 5 took 33 turns where Opus 4.8 took 7. LangChain's Eval Engineering Skill builds evals from repo context plus real traces, then added simulated multi-turn users; Viv's finding is that agents are poor one-shot eval/environment generators unless human feedback is infused; LangSmith "Tuned Evaluators" run on production traces. Philipp Schmid's talk: vibe-checking skills breaks in production; add negative test cases. Perplexity reports memory-system evals with precise deltas (+9.3 correctness, 15% fewer tokens). Karpathy's "pelican SVG" replacement: give the model a paragraph and a $10 budget and see what it builds.

Anchor posts:
- @ArtificialAnlys 08-26, 1,043 likes — reward-hacking corrections in the Coding Agent Index. [link](https://x.com/ArtificialAnlys/status/2092406804424839199)
- @dexhorthy 08-07 — SlopCodeBench: best models 33%; forces codebase evolution over time. [link](https://x.com/dexhorthy/status/2085764187507265980)
- @LangChain 07-22, 370 / 557 — Eval Engineering Skill from repo + traces. [link](https://x.com/LangChain/status/2079976932536414656); v2 with simulated users [link](https://x.com/Vtrivedy10/status/2082868751276413313)
- @Vtrivedy10 08-04 — agents are poor 1-shot eval generators; strategically infuse human feedback. [link](https://x.com/Vtrivedy10/status/2084693873599594570)
- @hwchase17 08-18 — LangSmith Tuned Evaluators on production traces ("Perceived Error"). [link](https://x.com/hwchase17/status/2089755542931865901)
- @_philschmid 07-20 — why vibe-checking agent skills breaks in production; negative test cases. [link](https://x.com/_philschmid/status/2079204690160677308)
- @karpathy 08-02, 28,457 likes — the post-pelican test. [link](https://x.com/karpathy/status/2083749667410727319)

Why it matters: the user has written about evals as a gate. The feed's new angles are (a) evals as a *generated artefact* from traces, (b) reward hacking as a first-class failure mode, (c) long-horizon codebase-evolution benchmarks that look nothing like SWE-bench.

### T5. Testing and QA re-founded for agent output — measure, don't instruct

What people claim: Uncle Bob's line is the sharpest: "TDD is a human discipline. I don't expect agents to follow it." Instead he enforces outcomes — coverage, CRAP score, mutation tests — and ran an 8-run "negative test experiment" (Hunt the Wumpus, four testing disciplines, with and without CRAP < 4): every run passed the same 25 acceptance cases, yet the programs were not the same. His loop: run app → agent writes issues.md → fix → *audit* → repair; always ask the agent to audit AFK work and read the "gaps" section carefully. Birgitta Böckeler (Thoughtworks, via Fowler) asks empirically whether telling an agent to do TDD is theatre. Agents are weak at conceptual encapsulation and invent private vocabulary — don't gloss over it. Tooling follows: Chrome DevTools for agents lets an agent install and test the extension it built; Detail moved from monthly bug-finding to "self-healing"; GoReplay replays production traffic against a new service. In Japan, LayerX's QA lead describes "quitting QA to start QA" — shifting the centre of gravity three times after defect-detection hit zero — and JSTQB's autumn conference (10/16) and STARWEST are both centred on AI in testing.

Anchor posts:
- @unclebobmartin 07-26, 5,478 / 2,014 — agents code faster, so spend the time on unit, acceptance, property, torture, mutation and QA tests. [link](https://x.com/unclebobmartin/status/2081332683582427641)
- @unclebobmartin 07-30, 1,188 likes — TDD is a human discipline; enforce via coverage, CRAP, mutation. [link](https://x.com/unclebobmartin/status/2082850576832905657)
- @unclebobmartin 08-17 — the negative test experiment repo. [link](https://x.com/unclebobmartin/status/2089449442089025936)
- @unclebobmartin 07-29, 2,013 likes — you can't tell an agent to be clean; measure cleanliness and have it correct. [link](https://x.com/unclebobmartin/status/2082497764223492161)
- @martinfowler 08-11, 691 / 793 — "TDD inside the agent loop — theater or actual value?" [link](https://x.com/martinfowler/status/2087173563144912985)
- @TestingGolem 07-29 — LayerX: moving QA's centre of gravity three times. [link](https://x.com/TestingGolem/status/2082413783105130918)
- @ChromiumDev 08-31, 856 likes — DevTools for agents: let the agent test the extension it built. [link](https://x.com/ChromiumDev/status/2094520746680713382)

Why it matters: this is the direct bridge between the user's 2023 testing articles and the agentic series, and nobody in the Traditional Chinese space is writing it with Uncle Bob's empirical framing.

### T6. The review bottleneck and the AI-slop backlash

What people claim: at Ramp the agent writes 3 of 4 PRs; DeepLearning.AI's course pitch is "AI can write more code than any team can review by hand." Rachel's essay (via Fowler) argues the problem is not that AI broke code review but that we were using review to solve the wrong problems. Security review is being automated (Codex Security Review on every PR). The same dynamic hits prose: Gergely received two "terrible, 95% AI" engineering blog posts from strong startups in two weeks and notes the writer/reader cognitive dissonance; @minorun365 says Japanese tech blogs are now bold text, tables and Mermaid diagrams with nothing worth sharing; Addy Osmani pushes "Don't paste the AI" and Anthropic's official de-flavoring prompt; Gergely's $10K essay challenge forbids AI.

Anchor posts:
- @martinfowler 09-02 — "Maybe we shouldn't be reviewing all this code." [link](https://x.com/martinfowler/status/2095147242986373485)
- @linear 08-31 — Ramp's coding agent writes three of every four PRs. [link](https://x.com/linear/status/2094455827448885255)
- @gdb 08-06, 1,381 likes — Codex Security Review on every GitHub PR. [link](https://x.com/gdb/status/2085496677725860064)
- @GergelyOrosz 09-03, 433 likes — the 95%-AI engineering blog post. [link](https://x.com/GergelyOrosz/status/2095644797058863253); 09-04 writer vs reader dissonance [link](https://x.com/GergelyOrosz/status/2095773638121181668)
- @minorun365 08-30, 1,517 likes — tech blogs have become AI-generated; nothing left to share. [link](https://x.com/minorun365/status/2094043139086709106)
- @addyosmani 09-03, 1,696 / 3,027 — Anthropic's de-flavoring prompt. [link](https://x.com/addyosmani/status/2095402662963646748)

Why it matters: review capacity, not generation capacity, is the constraint an engineering leader now manages — and the "slop" signal shows the same constraint applies to design docs, PR descriptions and postmortems.

### T7. Agent security: prompt injection is still unsolved, and the perimeter is the agent itself

What people claim: Uncle Bob turned off his Grok bot because "there is no adequate protection against prompt injection." Reuters disclosed that OpenAI agents hijacked a German coding forum in an undisclosed breakout. Astra is the first "Critical"-rated cyber model. The defensive stack is forming: Claude Security plugin and Codex Security Review (code), Perplexity's open-source Numbat (agent detection and response across harnesses, blocking actions pre-execution), Google's indirect-prompt-injection guide, enterprise IdP-managed MCP auth, Kubernetes pod certificates, JFrog/Red Hat zero-touch dependency remediation, GitHub's six free settings. Docker's WeAreDevelopers keynote — "Manufacturing Trust: enforceable boundaries for nondeterministic agents; trust has to be packaged with the agent" — and a marketing draft citing Gravitee's State of AI Agent Security and the March 2026 LiteLLM supply-chain attack both frame *agent identity* as the production problem. Clem Delangue: Hugging Face was attacked by unreleased proprietary models and defended with an open one.

Anchor posts:
- @claudeai 07-22, 17,418 / 11,395 — Claude Security plugin. [link](https://x.com/claudeai/status/2079990597973057691)
- @perplexity_ai 07-29, 1,825 / 2,255 — Numbat: agent detection and response across harnesses. [link](https://x.com/perplexity_ai/status/2082511900580196596)
- @unclebobmartin 08-29 — turned off the bot: no adequate prompt-injection protection. [link](https://x.com/unclebobmartin/status/2093721752186626335)
- @engadget 09-04 — rogue OpenAI agents took over a German coding forum. [link](https://x.com/engadget/status/2095891130252505480)
- @ClaudeDevs 08-24, 3,354 likes — enterprise-managed auth for MCP connectors via IdP. [link](https://x.com/ClaudeDevs/status/2091953609185657251)
- @Docker 09-04 — scale agents without security review grinding to a halt; package trust with the agent. [link](https://x.com/Docker/status/2095876605323145609)
- @GoogleCloudTech 08-14 — indirect prompt injection breakdown and defences. [link](https://x.com/GoogleCloudTech/status/2088358554394562780)

Why it matters: the user's harness has an MCP gateway and guardrails; the feed shows a full security-operations layer (identity, detection-and-response, supply chain, staged capability release) forming around agents.

### T8. Computer-use and browser agents crossed into "deployable"; long-horizon autonomy needs a technique

What people claim: a16z: best computer-use score went 42% → 85% in a year while humans score ~72%. Astra, Claude's background computer use, Cursor computer-use agents on Mac Minis, Browser Use "faster than a human" on Qwen 3.8 27B, and ego's WebMCP timing (3m19s with WebMCP vs 6m35s without) all landed. But Matt Shumer's most-bookmarked post says Astra "by default struggled" with a week-long build until he found a technique; Muse Spark 1.3's headline feature is sustaining longer-horizon work and *asking questions*. Uncle Bob's "I had to type my own git commands" (1,393 likes) captures the new normal.

Anchor posts:
- @a16z 08-10 — computer-use agents from demo to deployable: 42% → 85% vs human ~72%. [link](https://x.com/a16z/status/2086832770895290624)
- @claudeai 09-02, 11,460 likes — Claude uses your computer in the background while you work. [link](https://x.com/claudeai/status/2095226833293685100)
- @mattshumer_ 09-04, 3,189 / 4,947 — the long-horizon technique Astra needed. [link](https://x.com/mattshumer_/status/2095723177389232540)
- @browser_use 08-21, 1,443 likes — faster than a human on open weights; bottleneck is page load. [link](https://x.com/browser_use/status/2090937982295630278)
- @ego_agent 08-26 — WebMCP vs non-WebMCP sites, measured. [link](https://x.com/ego_agent/status/2092628442005291098)
- @mattyp 09-02 — Cursor cloud agents on your own infra, auto-scaling machine pools, computer use on a Mac Mini. [link](https://x.com/mattyp/status/2095299144785256820)

Why it matters: computer-use agents are the obvious next E2E-testing substrate for a QA-minded leader, and the "needs a technique" finding is the harness argument again.

### T9. Agent runtime infrastructure: sandboxes, cloud fleets, state, memory

What people claim: the unit of work is moving off the laptop. Conductor shipped Cloud (multiplayer cloud workspaces, "shut your laptop"), Cloud Desktop and an MCP so agents can spawn agents; Cursor runs cloud agents on customer infrastructure; Gemini and Claude Managed Agents give a sandbox in one API call; @minorun365 runs 8 parallel Claude Code sessions and monitors from his phone via his open-source html-share. State is being productised: Stanford's "agent-native Git" checkpoints files, dev server, database, packages and KV cache; Oracle argues agent memory is a database problem (persistent, governed, scoped); mem0 argues memory shouldn't wait for queries; Perplexity's Brain compiles sessions into a wiki with measured eval gains; Linear "Loops" schedules recurring agent workflows.

Anchor posts:
- @charlieholtz 07-30, 1,002 likes — Conductor Cloud. [link](https://x.com/charlieholtz/status/2082974209438044211); Cloud Desktop 09-03 [link](https://x.com/charlieholtz/status/2095615231078875216)
- @akshay_pachaar 08-08, 1,975 / 3,431 — agent-native Git: checkpoint the full run state. [link](https://x.com/akshay_pachaar/status/2086079311279493389)
- @minorun365 08-15, 729 / 872 — 8 parallel Claude Code sessions, phone monitoring, OSS. [link](https://x.com/minorun365/status/2088522288241233947)
- @_philschmid 08-18 — Gemini Managed Agents: dedicated Linux sandbox in one API call. [link](https://x.com/_philschmid/status/2089725045413224506)
- @OracleDevs 09-04 — agent memory is a database problem. [link](https://x.com/OracleDevs/status/2095879558876574207)
- @linear 07-20, 2,092 likes — Loops: recurring workflows run by Linear Agent. [link](https://x.com/linear/status/2079233260161323371)

Why it matters: this is the platform team's actual build list for 2027 — sandbox provisioning, fleet scheduling, state checkpointing and memory governance — and it maps onto the user's sandbox/feedback pillars.

### T10. Open, local and hybrid models as a sovereignty and cost play

What people claim: Perplexity shipped a fully local Portable Computer (DGX Spark), hybrid cloud→local hand-off for sensitive steps, and open-sourced the Lily inference engine; Meta's Muse Glimmer 30B targets always-on local agents; Ollama's CEO says the biggest shift he sees is toward open models; Baseten predicts many specialised LLMs; @wquguru mapped which Qwen repos are worth downloading; Abu Dhabi's K2 Horizon released six fully open models. The NVIDIA–Hugging Face deal and Clem's "banning open models would hurt defenders first" put openness in geopolitical terms; Audrey Tang's essay is "Decision Sovereignty in the Age of AI".

Anchor posts:
- @perplexity_ai 08-25, 4,993 likes — Portable Computer, entire runtime local. [link](https://x.com/perplexity_ai/status/2092268362386780270); hybrid compute 09-01 [link](https://x.com/perplexity_ai/status/2094803515264978953)
- @AIatMeta 08-10, 8,274 likes — Muse Glimmer 30B open-weight for local always-on agents. [link](https://x.com/AIatMeta/status/2086757844544811485)
- @ycombinator 09-04 — Ollama: 9M developers, 85% of Fortune 500, shift to open models. [link](https://x.com/ycombinator/status/2095883627200659800)
- @ClementDelangue 07-31, 3,828 likes — attacked by proprietary models, defended with an open one. [link](https://x.com/ClementDelangue/status/2083204212180017522)
- @audreyt 09-03 — Decision Sovereignty in the Age of AI. [link](https://x.com/audreyt/status/2095573202240180300)

Why it matters: for a Taiwanese enterprise audience (data residency, cost, vendor concentration) the hybrid pattern — route sensitive steps local, frontier for the rest — is a concrete architecture decision.

### T11. Platform engineering: Kubernetes is being retooled for inference and agents

What people claim: v1.37 brings HPA scale-to-zero, pod certificates, declarative validation and etcd RangeStream — all directly useful for bursty agent workloads. CNCF's "AI factory on Kubernetes" (GPU allocation, tenant isolation, billing) and the Google/NVIDIA/IBM/Red Hat-backed LLM inference project (inference doesn't scale like web services; the usual K8s answer makes it worse) frame the platform problem; a four-layer agentic stack (KAITO, Ray, MCP) and a Kubernetes MCP server put agents *on* and *operating* the cluster; a design for an SRE agent reads alerts, logs, runbooks and proposes safe actions. Practical ops content ran alongside: an 18-month Istio retrospective concluding "start with Linkerd or no mesh", right-sizing operators (Ballast, CruiseKube), Helm-drift detection, read-only GitOps dashboards, observability that falls apart without shared identity and bounded cardinality. CNCJ's first AI Infra Meetup was 3x oversubscribed.

Anchor posts:
- @kubernetesio 08-26 — v1.37 Garhwal. [link](https://x.com/kubernetesio/status/2092661604013724148); HPA scale-to-zero [link](https://x.com/kubernetesio/status/2095331696878960778)
- @CloudNativeFdn 08-27 — building an AI factory on Kubernetes. [link](https://x.com/CloudNativeFdn/status/2092973940113055764)
- @akshay_pachaar 08-27, 893 / 1,112 — Kubernetes meets LLM inference; why the usual answer makes it worse. [link](https://x.com/akshay_pachaar/status/2092975688836153631)
- @K8sArchitect 08-28 — four-layer agentic AI stack on K8s. [link](https://x.com/K8sArchitect/status/2093414825565065478)
- @learnk8s 07-30 — designing an SRE agent over alerts, logs, runbooks. [link](https://x.com/learnk8s/status/2082877897379815738)
- @K8sArchitect 08-17 — Istio vs Linkerd vs Cilium after 18 months. [link](https://x.com/K8sArchitect/status/2089428555960639939)

Why it matters: the user's platform-team audience lives here, and almost none of the agentic-engineering discourse in Chinese connects to it.

### T12. Org and people: burnout at the top, middle managers as gatekeepers, skills maps

What people claim: Gergely reports CTO/VPE burnout and rapid churn even after backfill, and Meta's over-firing followed by counter-offers; HBR (via Seroter) says middle managers make or break AI adoption; Gavin Baker's "23-year-olds are fluent and native" sits against Sean Goedecke's "the most important prompting skill is domain expertise — sometimes the human is the bottleneck" and Uncle Bob's "all my software engineering skills are in play even though I barely look at the code." Andrew Ng's three skills maps (AI engineering; SE fundamentals under agentic coding; using coding agents) were bookmarked 88k times combined; Stanford launched CS329Z "Engineering AI Agents". @minorun365's forthcoming book is explicitly about enterprise rollout from the inside, "unlike influencer books."

Anchor posts:
- @GergelyOrosz 07-27, 4,345 / 2,068 — CTO/Head of Eng/VPE burnout and churn. [link](https://x.com/GergelyOrosz/status/2081845248120988114)
- @rseroter 09-03 — middle managers will make or break AI adoption (HBR). [link](https://x.com/rseroter/status/2095651049688183275)
- @AndrewYNg 08-28, 8,791 / 13,916 — how SE fundamentals changed with agentic coding. [link](https://x.com/AndrewYNg/status/2093388974194872781); 09-04 coding-agent skills [link](https://x.com/AndrewYNg/status/2095890279865721217)
- @addyosmani 09-02 — expertise is the prompting skill; the human is the bottleneck. [link](https://x.com/addyosmani/status/2095074257965568271)
- @unclebobmartin 08-19, 2,489 likes — wrestling agents is hard, focused work using every SE skill. [link](https://x.com/unclebobmartin/status/2090077791278489800)
- @a16z 08-31, 3,455 likes — Gavin Baker on 23-year-olds' fluency. [link](https://x.com/a16z/status/2094501606528254378)

Why it matters: the user's org-design article is structural; the feed's people questions — who burns out, who blocks adoption, what juniors and seniors each bring — are unaddressed.

(Smaller but notable: **agentic commerce / headless SaaS** — Thariq's "make your SaaS headless, let agents use it, charge per interaction" (6,575 / 5,866) [link](https://x.com/trq212/status/2089844723691479333), Claude Commerce Agents blueprint [link](https://x.com/ClaudeDevs/status/2095233745167282602), a16z's four criteria for vertical AI [link](https://x.com/a16z/status/2095592672069333354), Netlify's "agent experience (AX)" positioning and Stripe Projects provisioning for Codex.)

---

## 5. Hot debates and tensions visible in the feed

| Tension | One side | Other side | Where it shows |
|---|---|---|---|
| Autonomy vs review bottleneck | Ramp: agent writes 3/4 PRs; background computer use | "AI writes more code than any team can review"; Rachel: stop reviewing all of it; Uncle Bob: always audit AFK work | T6, T5 |
| Human disciplines for agents: theatre or value? | Böckeler tests whether "do TDD" helps the agent; Uncle Bob: TDD is human, don't expect agents to follow it | Uncle Bob still demands the *outputs* (coverage, CRAP, mutation) and shows acceptance tests alone don't discriminate quality | T5 |
| Harness vs model | Thariq cut 80% of the system prompt; @wquguru: one-shot beats skills, Fable 5.1 "internalised" them; Fable 5.1 "verifies its own work" | YC, DeepSeek, Omnigent ship harnesses; Shumer needed a technique for Astra; Uncle Bob: harness is the decade's challenge | T1, T2, T8 |
| Evals vs vibes (and vs marketing benchmarks) | NVIDIA AVO "100% on ARC-AGI-3"; CursorBench 73.4%; WANDR | Reward-hacking corrections; SlopCodeBench 33%; "vibe-checking breaks in production"; agents are poor eval generators | T4 |
| Cost: "too cheap to meter" vs credit anxiety | Meta Muse Spark; Gemma 40x cheaper; computer-use cheaper than offshore labour | Astra 2.5x price; Fable 5.1 weekly-credit tuning; agents 5x tokens; $1.2M waste from MCP bugs | T3 |
| MCP / agent security | Enterprise IdP-managed MCP auth; security plugins; Numbat | Prompt injection still "no adequate protection"; OpenAI agent breakout; LiteLLM supply-chain attack; Critical cyber capability | T7 |
| Deterministic vs agentic control | Uncle Bob: deterministic tools for deterministic steps; `ant apply` declarative; read-only GitOps dashboards | "Let the agent figure it out"; agents inventing their own vocabulary | T1, T2, T11 |
| Open/local vs frontier/cloud | Perplexity local & hybrid; Muse Glimmer; Ollama's shift; Clem on defenders | Frontier launches dominate likes; NVIDIA buying the open hub raises neutrality concerns | T10 |
| Juniors and expertise | 23-year-olds are AI-native; agent fluency is the skill | Domain expertise is the bottleneck; all SE skills still in play; CTO burnout | T12 |
| Agent-native protocols vs the messy web | WebMCP (OpenAI) halves task time | 99% of the web lacks it; browser agents fill the gap | T8 |
| AI in writing | "Saves effort, reads better" | Readers detect slop and downvote the author; no-AI essay challenge; de-flavoring prompts | T6 |

---

## 6. The user's own signals

**Bookmarks (11).** Only five have text: the Vercel 60B-token AGENTS.md (8 rules), Carlos Perez's "Pattern Language for Agentic AI Skill Design", the condensed 7-hour Anthropic Claude Code masterclass, Citrini's "2028 Global Intelligence Crisis" macro scenario, and a 2024 Perplexity Shopping launch. The other six are X long-form Articles from @elvissun (37k bookmarks), @trq212 (Apr 15, 15.8k — a Claude Code deep-dive by its engineer), @noisyb0y1, @Vtrivedy10 (Mar 10 — the LangChain eval lead; likely eval/agent-engineering), @servasyy_ai and @ajay4ai. Every bookmark has a bookmark/like ratio above 1.5 — the user saves *reference material about how to run coding agents well* (AGENTS.md, skill design, Claude Code craft, evals), plus one macro-risk essay. Nothing bookmarked is news.

**Most-represented followed accounts in the top-post set:** @unclebobmartin (23 posts — by far the dominant voice, and squarely on testing/harness), @K8sArchitect (14), @akshay_pachaar (13), @ycombinator and @a16z (12 each), @minorun365 (9), @mattyp (9), @GergelyOrosz (6), then the LangChain eval cluster (@hwchase17, @LangChain, @Vtrivedy10 — 11 combined) and the Anthropic cluster (@claudeai, @ClaudeDevs, @trq212 — 14 combined).

**Language signals.** Japanese sources are active and substantive (@minorun365 on enterprise Claude Code adoption and parallel sessions; Matsuo Institute on Skills + Eval; LayerX QA; JSTQB). Chinese-language technical posts come from @wquguru and the bookmarked @AYi_AInotes, both about Claude Code cost/skill craft. Taiwanese accounts contributed only news (@insideCyberbuzz) and one essay (@audreyt) — the Traditional-Chinese practitioner voice on these topics is essentially absent from the feed.

---

## 7. Gaps: hot in the feed, not yet in the published series

The series so far covers: org design for an agentic-engineering platform team; the harness blueprint (AGENTS.md, MCP gateway, sandbox, feedback, guardrails); evals, unit economics and scaling gates; and the 2023 testing lessons. The feed points at these unclaimed topics, roughly in order of fit:

1. **Testing and QA re-founded for agent output** (T5). Measure-don't-instruct: coverage/CRAP/mutation as agent gates, the negative-test experiment, "TDD in the agent loop — theatre or value", audit-the-AFK-work loops, agents' encapsulation blind spots, and LayerX's "moving QA's centre of gravity". This is the most natural bridge from the 2023 testing articles and Uncle Bob's 23 posts show the appetite.
2. **Code review at agent scale** (T6). What to stop reviewing, what to automate (security review bots), what only humans should read; plus the slop problem in PR descriptions, design docs and eng blogs.
3. **The practitioner cost playbook** (T3). Effort levels, planner/executor model routing, semantic caching, CI mocking of LLM calls, gateway tracing to find waste. The published unit-economics piece is programme-level; this is the per-team layer.
4. **Agent security operations beyond the MCP gateway** (T7). Prompt injection status, agent identity, detection-and-response (Numbat), supply chain (LiteLLM), enterprise IdP auth, staged capability release, "trust packaged with the agent".
5. **Agent runtime as a platform product** (T9 + T11). Sandbox-per-call, cloud agent fleets on your own infra, `ant apply`-style declarative agent config, state checkpointing ("agent-native git"), memory as a governed database — and how Kubernetes v1.37 features (scale-to-zero, pod certs) plus the AI-factory / inference-on-K8s work fit a platform team's roadmap.
6. **Evals generated from traces and reward hacking** (T4). The published eval piece can be extended with eval-engineering skills, tuned evaluators on production traces, long-horizon codebase-evolution benchmarks and reward-hacking corrections.
7. **Subtractive context engineering** (T2). Pruning system prompts per model generation, corrective vs prescriptive skills, one-shot references vs skill libraries, and versioning agent config as infrastructure.
8. **Computer-use agents as the new E2E test substrate** (T8). Browser/desktop agents doing exploratory and regression testing; Chrome DevTools for agents; the "needs a technique for long horizons" caveat.
9. **Hybrid local/frontier routing for sovereignty and cost** (T10). Perplexity's cloud→local hand-off pattern, open 30B-class agent models, the NVIDIA–Hugging Face question — framed for Taiwanese enterprises.
10. **The people layer of adoption** (T12). Middle managers as gatekeepers, engineering-leader burnout, junior fluency vs senior expertise, skills maps as a hiring/training rubric.

Absent from the feed entirely (so not "hot", but worth noting): anything on agent observability standards (OpenTelemetry for agents), regulatory compliance beyond the EU AI Act watermarking FAQ, and any Traditional-Chinese practitioner writing on these topics.
