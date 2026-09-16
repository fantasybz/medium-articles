# arXiv sweep: Agentic Engineering, 2026-09-01 to 2026-09-15

Compiled 2026-09-15. Method: two independent half-sweeps, merged here and
deduplicated by arXiv id. Half A (`.context/research/2026-10/arxiv_sweep_a.md`)
ran 62 date-bounded queries — the 15 standard strings from
`research/prompts/arxiv.md`, 5 zero-hit repairs, the 13 watch-list strings from
`research/2026-09/backlog.md` §訊號監看清單, and 28 OR-branch expansions (half A's own total of 62
queries does not reconcile with the 61 strings it lists) — and
retrieved 383 unique papers, 189 of them judged relevant, 16 abstracts read in
full. Half B (`arxiv_sweep_b.md`) ran 10 commissioned observability / SLO /
accountability queries, each issued twice (window-bounded and all-dates), plus
29 window-bounded broadening probes, and read 36 abstract pages in full plus one
complete PDF (2608.23610). Neither file is missing or short; both are complete
for what they were asked to cover, and half A's own closing note lists what its
62 queries did not reach (the cs.SE recent listing, vibe coding, named vendor
agents, agentic PR review at scale, and the org/productivity literature — its
S10 returned exactly 1 hit, which is a query problem, not an absence). Rows
below that came only from half B's later-version window are the ones half A's
query set could not have surfaced, and vice versa.

**Two method caveats that shape every count below, both recorded by the sweeps
themselves.**

1. `export.arxiv.org/api/query` was rate-limited for practically the whole
   session. Half A got **HTTP 429 on all 9 probes over ~12 minutes and never
   obtained a single API result**; half B got exactly one API call through
   (kept as `raw_b/q1.xml`) and ran everything else against the fallback. So
   every count here comes from `arxiv.org/search/advanced`, not the API.
2. The UI counts are not comparable to the September sweep's corpus-wide
   numbers (631 for "coding agent" etc.). Half A's `n` is a **date-bounded
   count inside the window**; half B's `TOTAL` is a **loose upper bound**,
   because the search backend does not honour quoted phrases as strict phrase
   matches (`"agent observability"` unbounded returns 370–418 results, most of
   them multi-agent RL papers containing neither word as a phrase). The
   advanced-search endpoint also does not support parentheses: every
   parenthesised watch-list string returns 0 because the parens match
   literally. A verbatim `0` below never means "no such papers exist".

The date filter is `date-date_type=submitted_date`, which matches **any
version's** submission date, not only v1. That is why ids from 2025-11 through
2026-08 appear: a v2–v5 landed inside the window. Each such row carries its v1
date and, where they differ, the announcement month and the September revision.

Every id, date, title and number below was read from a result page, an abstract
page or (for 2608.23610) the PDF, in one of the two sweeps. Nothing is
extrapolated and no row was invented: every row traces to one of the two files.
The sweeps log hit counts per query but **not which query surfaced which
paper**, so per-row query attribution is not available; instead each row is
marked `[A]`, `[B]` or `[A+B]` for the half or halves that found it. 23 rows
are `[A+B]`.

Cluster codes used in the table. A–J are the September sweep's codes, unchanged.
K and S are the only additions, carried over from half B, because
containment-as-a-runtime-property and serving-level objectives for agent
workloads are both new enough this window to need their own letter:

| Code | Cluster |
|---|---|
| A | Harness engineering and orchestration (the runtime around the model) |
| B | Context engineering: AGENTS.md / CLAUDE.md, skills, memory, compaction |
| C | MCP and tool gateways |
| D | Agent security: privilege escalation, injection, supply chain in harnesses |
| E | Evals for agents: beyond pass/fail, judges, reliability |
| F | AI code review and the review bottleneck |
| G | Observability, audit trails, accountability |
| H | Unit economics: tokens, cost, verification spend |
| I | Spec-driven development and requirements |
| J | Organisational impact, productivity studies, people |
| K | *(new)* Sandboxing, isolation, runtime containment |
| S | *(new)* Service levels: SLO/SLA and serving reliability of agent workloads |

## 0. Query log (merged)

### 0a. Half A — the 15 standard queries (`n` = hits in window)

| # | Exact `terms-0-term` string | n |
|---|---|---|
| S1 | `"coding agent"` | 83 |
| S2 | `"agent harness"` | 35 |
| S3 | `"AGENTS.md" OR "context engineering"` | 5 |
| S4 | `"Model Context Protocol" OR "MCP"` | 57 |
| S5 | `"prompt injection" AND agent` | 29 |
| S6 | `"SWE-bench" OR "software engineering agent benchmark"` | 22 |
| S7 | `"LLM-as-a-judge" AND agent AND evaluation` | 12 |
| S8 | `"multi-agent software development"` | 0 |
| S9 | `"AI code review"` | 1 |
| S10 | `developer productivity AND LLM AND agent AND empirical` | 1 |
| S11 | `agent AND observability AND "audit trail"` | 0 |
| S12 | `sandbox AND agent AND execution` | 19 |
| S13 | `token AND cost AND agent AND efficiency` | 18 |
| S14 | `"self-evolving" AND agent AND harness` | 10 |
| S15 | `"spec-driven development" AND LLM` | 0 |

Zero-hit repairs: `"multi-agent" AND "software development"` 0 (S8-i);
`agent AND "audit trail"` 5 (S11-i); `agent AND observability AND LLM` 99
(S11-ii); `"spec-driven development"` 1 (S15-i);
`specification AND agent AND "software engineering" AND generation` 4 (S15-ii).

### 0b. Half A — watch-list strings from `backlog.md`, verbatim then expanded

| # | Exact string (verbatim from backlog) | n | Backlog item |
|---|---|---|---|
| W9a | `"privilege escalation" AND (harness OR "coding agent")` | 0 | 1 |
| W9b | `skill AND ("supply chain" OR poisoning) AND agent` | 0 | 1 |
| W9c | `"reference monitor" AND agent` | 1 | 1 |
| W10a | `("technical debt" OR maintenance OR "code quality") AND "coding agent" AND (longitudinal OR "post-merge")` | 0 | 2 |
| W10b | `"architectural decision" AND agent AND memory` | 0 | 2 |
| W11a | `(sandbox OR "agent runtime" OR "internal developer platform") AND Kubernetes AND agent` | 0 | 3 |
| W11b | `"agentic workloads" AND serving` | 4 | 3 |
| W12a | `(compaction OR "context window" OR "working memory") AND "coding agent"` | 0 | 4 |
| W12b | `"agent skills" AND (evaluation OR staleness OR provenance)` | 13 | 4 |
| W13a | `("exploratory testing" OR "computer-use agent" OR "GUI agent") AND (testing OR QA)` | 0 | 5 |
| W13b | `"multi-agent" AND (topology OR coordination) AND "software engineering"` | 1 | 8 |
| W13c | `("domain-driven design" OR "bounded context" OR "event storming") AND LLM` | 0 | 7 |
| W13d | `(deskilling OR "skill atrophy") AND developers AND AI` | 0 | 9 |

Expansions: `"privilege escalation" AND harness` 2; `"privilege escalation" AND
"coding agent"` 0; `skill AND "supply chain" AND agent` 2; `skill AND poisoning
AND agent` 1; `"technical debt" AND "coding agent"` 1; `maintenance AND "coding
agent" AND longitudinal` 0; `"code quality" AND "coding agent"` 2; `"post-merge"
AND agent` 0; `"architectural decision" AND agent` 0; `"architectural decision"
AND LLM` 1; `sandbox AND Kubernetes AND agent` 0; `"agent runtime" AND
Kubernetes` 0; `"internal developer platform" AND agent` 0; `"agent runtime" AND
platform` 0; `compaction AND "coding agent"` 1; `"context window" AND "coding
agent"` 1; `"working memory" AND "coding agent"` 0; `compaction AND agent AND
context` 24; `"exploratory testing"` 1; `"computer-use agent" AND testing` 3;
`"GUI agent" AND testing` 4; `"multi-agent" AND topology AND "software
engineering"` 2; `"multi-agent" AND coordination AND "software engineering"` 3;
`"domain-driven design" AND LLM` 0; `"bounded context" AND LLM` 3 (all three
unrelated: a TTS codec, a power-grid QA renderer, a long-horizon trace model);
`"event storming"` 0; `deskilling AND AI` 2; `"skill atrophy"` 1.

### 0c. Half B — the 10 commissioned queries (TOTAL in window / all-dates / kept)

| # | Query (field `all`, cs classification, cross-lists included) | window | all-dates | kept |
|---|---|---|---|---|
| Q1 | `"agent observability" OR "agent telemetry"` | 11 | 375 | 2 |
| Q2 | `OpenTelemetry AND agent` | 1 | 17 | 1 |
| Q3 | `"service level objective" AND agent` | 1 | 25 | 1 |
| Q4 | `"flight recorder" OR "audit log" AND agent` | 1 | 40 | 1 |
| Q5 | `"agent accountability" OR attestation AND agent` | 8 | 97 | 5 |
| Q6 | `"MCP gateway" OR "agent gateway" OR "tool authorization"` | 2 | 21 | 0 |
| Q7 | `"agent memory" AND (benchmark OR evaluation)` | 9 | 166 | 6 |
| Q8 | `sandbox AND agent AND (Kubernetes OR container)` | **0** | 4 | 0 |
| Q9 | `"trace-based evaluation" AND agent` | **0** | 4 | 0 |
| Q10 | `"agent-to-agent" OR "A2A protocol"` | 21 | 1,013 | 6 |

### 0d. Half B — broadening probes (window-bounded)

| Tag | Query | TOTAL | Note |
|---|---|---|---|
| q01b | `observability` | 1,548 | unusable alone — control-theoretic sense dominates |
| q01c | `telemetry` | 48 | mostly 5G/6G, spacecraft, datacenter; 3 agent-relevant |
| q02b | `OpenTelemetry` | 1 | the single OTel paper in the window is 2609.12582 |
| q02c | `"distributed tracing"` | 1 | false positive (a video-generation paper) |
| q03b | `"service level"` | 21 | all serving/scheduling; 2609.08020 and 2609.06128 are the agent-facing ones |
| q03c | `"error budget" OR SLO` | 17 | LLM-serving SLOs only; **no error-budget paper for agent runs in the window** |
| q04b | `"flight recorder"` | 1 | 2609.01931 (seen 09) — still the only one |
| q04c | `"audit log"` | 2 | |
| q04d | `"audit trail"` | 9 | |
| q05b | `"agent accountability"` | 1 | 2609.04894 (a survey; accountability is one line in it) |
| q05c | `attestation` | 26 | 8 agent-related, rest TEE/FIDO2/TPM |
| q06b | `"MCP gateway"` | **0** | the term does not appear in the window |
| q06c | `"agent gateway"` | 1 | false positive |
| q06d | `"tool authorization"` | 1 | false positive |
| q06e | `"tool permission" OR "capability token"` | 1 | 2609.14400 |
| q07b | `"agent memory" AND benchmark` | 9 | |
| q07c | `"memory benchmark"` | 10 | |
| q08b | `sandbox AND agent` | 31 | |
| q08c | `Kubernetes AND agent` | **0** | |
| q08d | `container AND isolation AND agent` | 19 | |
| q09b | `"trace-based" AND agent` | 1 | 2605.27898 |
| q09c | `"trajectory evaluation"` | 8 | |
| q09d | `trace AND evaluation AND agent` | 64 | the productive one — most G/E rows come from here |
| q10b | `"agent-to-agent"` | 20 | |
| q10c | `"A2A protocol"` | 1 | 2609.10871 |
| x_k8s | `Kubernetes` | 8 | **zero of the 8 are agent papers** |
| x_sandbox | `sandbox AND agent AND container` | 3 | |
| x_mcp | `"Model Context Protocol"` | 27 | added because Q6 had no recall; 6 kept rows |
| x_otelagent | `OpenTelemetry AND agent AND trace` | 1 | 2609.12582 again |

**Five negatives that are findings, not gaps in the tooling.** (1) Backlog item
3, agent runtime as a platform, has **no September paper at all**: four distinct
strings in half A (`sandbox AND Kubernetes AND agent`, `"agent runtime" AND
Kubernetes`, `"internal developer platform" AND agent`, `"agent runtime" AND
platform`) and three in half B (`Kubernetes AND agent` 0, bare `Kubernetes` 8
with zero agent papers, Q8 0) all return nothing. (2) Backlog item 7:
`"domain-driven design" AND LLM` 0, `"event storming"` 0. (3) **One
OpenTelemetry paper in the whole window** (2609.12582), and it treats OTel as
plumbing it integrates, not as a contribution — the "OTel semantic conventions
for agents" story has no September arXiv support. (4) **No error-budget-for-
agents paper**: the 17 hits for `"error budget" OR SLO` are all LLM *serving*
latency SLOs. (5) Item 9 (deskilling) produced 3 papers total across both
branches.

---

## 1. All relevant papers found

`*` = abstract page read in full by at least one half (50 rows).
`**` = full PDF read (2608.23610 only, in addition to its abs page).
`(seen 09)` = the id already appears in `research/2026-09/arxiv.md`.
`[A]` / `[B]` / `[A+B]` = which half surfaced it.
Dates are arXiv v1 submission dates; a later version inside the window, or an
announcement month that differs from the v1 month, is given after it.

| arXiv id | Title | Date | One-line takeaway | Cluster |
|---|---|---|---|---|
| 2609.15963 | Adversarial Testing of Automated Program Repair Agents for Security Vulnerabilities [A] | 2026-09-14 | SWEADV: 750 adversarial issue descriptions from 150 SWE-bench Verified repair tasks (5 attack types each); adversarial issues induce malicious behaviour *while the repair still succeeds* in 51.7% of cases on average across three backends | D, E |
| 2609.15906* | Authorization Architectures for Tool-Using AI Agents [A+B] | 2026-09-14 | 70-page structured narrative review, 89 primary sources screened from ~180 (2023-2026); principal hierarchy human user → operator/deployer → orchestrator → sub-agent → tool endpoint; every consequential action should be "traceable to a human principal, bounded by what that human actually delegated, and contestable after the fact", and "few documented deployments satisfy all three properties reliably and end to end"; open gaps named as runtime enforcement and aggregation bounds | D, C |
| 2609.15887 | The Model Proposes, the Code Disposes: A Pre-Registered Ablation of a Verifier-and-Acceptance Stage in an LLM-Orchestrated Offensive-Security Agent [A] | 2026-09-14 | Removing the model-verifier + deterministic-acceptance stage ends pre-report suppression (median 2 vs 0 findings/run, p = 0.00003) and drops shipped precision (0.471 vs 0.353, p = 0.0087); **deterministic acceptance rules alone suppressed no false positives** | E, F |
| 2609.15877 | Using Agentic AI for contextualized and multifaceted code review at Ericsson [A] | 2026-09-14 | Industrial multi-agent reviewer over four dimensions; >200 issues raised, 96% accuracy on correctness as judged by the case company's own developers, ~69% of correct issues rated important and ~33% severe | F |
| 2609.15397* | When Tool Calls Succeed but Workflows Fail: Anomalies at the Agent-Tool Boundary [A+B] | 2026-09-14 | Effect-history model separating world events from the runtime's observations; catalogue of 8 external-effect anomalies under retries/concurrency; 4 points where black-box tool invocation cannot give a general guarantee; measured the annotation vocabulary across **98,291 tools on registered MCP servers** — fields widely emitted but only coarse call-level hints, none of the required capabilities fully expressible | C, G |
| 2609.14992 | MTAC-IFBench: Benchmarking Instruction-Following in Multi-Turn Agentic Coding [A] | 2026-09-13 | 6 primary / 18 secondary constraint categories, avg 7.04 turns and 91.33 constraints per instance; instruction-following "degrades rapidly as the interaction session grows longer" | E, B |
| 2609.14987 | ActGuard: Pre-execution Action Auditing against Indirect Prompt Injection [A] | 2026-09-13 | Judges whether the *next action* deviates from a locally-predicted tool prior instead of whether content looks suspicious; masks only spans confirmed malicious, then regenerates | D |
| 2609.14913 | Externalizing Requirement-to-Repair Artifacts as Observable Traces for LLM-Based Program Repair [A] | 2026-09-13 | THEMIS audit of 300 SWE-bench Lite cases: complete Developer rationale for 288, complete audited field set for 214 (71.3%); target symbols recur in 62.6% of rationales and 62.8% of patches (75.8% including related symbols) | G, I |
| 2609.14857 | ModularRSI: Modular and Generalizable Recursive Harness Self-Improvement [A] | 2026-09-13 | Splits the evolvable harness into 5 modules (Agent Loop, Tool Use, Observation Mgmt, Context Mgmt, Task Completion Detection) and evolves each in a restricted scope, because whole-harness optimisation "entangles unrelated mechanisms and complicates attribution" | A |
| 2609.14836 | The Case for Automated Hyperspecialization: Evidence from SAT [A] | 2026-09-13 | Hundreds of workload-specific SAT solvers synthesised at **$37 each on average**, beating competition-winning general solvers 5x on average and >10x on a quarter of benchmark families; a composite of 100+ won the 2026 SAT Competition SAT track | H, A |
| 2609.14780* | The Stochastic Deputy: Structural Tenant Isolation for Tool-Using LLM Agents [A+B] | 2026-09-13 | 373-trial ablation, 8 model configs, 2 transports: a correctly validated tenant parameter in the MCP schema served **26 of 26** out-of-scope attempts (26 of 41 plausible-pretext trials overall); removing the parameter makes the read inexpressible, but **12 of 56 trials then escaped by forging writable scope**, so "interface invariance requires cryptographically protected context"; set-valued scope cost a measured 57x latency ratio under function-wrapped predicates | K, D, C |
| 2609.14744* | AcquireBound: Runtime Authorization for Resources Acquired by AI Agents [A+B] | 2026-09-13 | Names the **post-fulfillment activation gap**: payment/OAuth/mandate checks validate a transaction but never decide whether the returned resource may become authority; quarantine + provenance-bounded activation, 8 proved safety properties; 20/20 benign traces accepted and 40/40 unsafe rejected over 810 events, 16/16 unsafe MCP-to-Docker paths blocked, 89/89 tamper tests rejected by an independent checker; **a five-source audit of 1,248 field pairs across 32 units found no unit alone supplies a complete activation profile** | D, K |
| 2609.14723 | Detecting and Localizing Segment-Level Poisoning in Multi-Source LLM-Agent Inputs [A] | 2026-09-13 | ActProbe projects MLP activations onto a learned "poison direction" and localises which retrieved segment did it, with no backend modification | D |
| 2609.14721 | A Two-Dimensional Study of the Model Context Protocol: Publication and Adoption [A] | 2026-09-13 | 802 MCP publications + 33,319 GitHub repos; both curves peaked together in March 2026, a second wave alone is 49.5% of repos, and **93.7% of repos (57.8% of papers) use MCP as an enabling technology rather than analysing or securing it** | C |
| 2609.14631* | LLM Agent Capabilities Should Follow Task Intent and Context Source [A+B] | 2026-09-13 | 3-page position paper: capability should be scoped to task intent, not to sandbox or session lifetime; IntentCap composes a lease from four sources (user intent, workflow instructions, tool schemas, runtime environment) with field-level ownership and **monotonic narrowing** — the lease can never widen the user's authority | D, K |
| 2609.14422* | Safety Signals to Verify NetOps Agents with Action-Level Granularity [B] | 2026-09-13 | Per-action ground truth built by symbolic replay of NetArena's emulated network, validated against the environment every turn; across 10 agent models, verifiers using the agent's *internal* signals predict harm and progress better than observable-signal baselines; aimed at feeding abstention back into the harness | E, G |
| 2609.14400 | Policy Loopholes in Agent Evaluation: When Policy Ambiguity Masquerades as Agent Error [B] | 2026-09-13 | Audits two tau²-bench domains: natural-language policy silence, ambiguity and contradiction make affected tasks score unreliably and every model less self-consistent across repeat trials; exploitability needs **both** policy ambiguity and tool permissiveness | E |
| 2609.14239 | CoArena: Evaluating Computer-Use and Multi-Agent Systems in Real Time [A] | 2026-09-12 | Live pairwise arena; defines "real-time" as five measurable properties (continuous arrival, live concurrent execution, online rating updates, freshness/contamination resistance, bounded feedback latency) with Bradley-Terry fitting | E |
| 2609.14119* | Same Name, Different Server: A Security Census of Silent Drift in the MCP Ecosystem [A+B] | 2026-09-12 | Full public registry census: **21,643 servers / 72,606 version records** (Aug 2026), source fetched for 14,353, scanner accuracy measured against 414 hand labels; unauthenticated network exposure 9.57%, 11.14% observed high-severity prevalence corrected to ~7.6%; the headline is instability — **51.1% of multi-version servers changed what they advertise, 40.6% silently, 4.2% redirected the endpoint host while keeping registry identity**; silent drift OR = 2.96 (95% CI [2.56, 3.42]), stars barely protect (OR = 0.78 per log star) | C, D |
| 2609.14079 | SkillSecurer: Detecting and Patching Prompt-Injection Vulnerabilities in AI Agent Skills [A] | 2026-09-12 | Red/blue agent pair over 9 threat types; the only scanner reaching 100% injection detection, and **latent vulnerabilities in >17% of the popular skills.sh skills examined** | D, B |
| 2609.14003 | Confuse the Model, Control the Flow: Understanding and Mitigating Privacy Leakage from LLM Agents with Information Flow Control [A] | 2026-09-12 | Three no-injection attacks (Collaborative Workspace Lure, Semantic Obfuscation, Channel Decoupling) beat the defences they target because "the enforcement mechanism and the attack surface coincide" when the LLM judges its own context; FLOWSEAL moves enforcement to a tool-level interceptor | D |
| 2609.13890* | Learning How Much to Collaborate: Difficulty-Aware Topology Selection for Multi-Agent Code Generation [A] | 2026-09-12 | Five topologies on 614 problems: hierarchical beats a single agent by **2.4 pass@1 points on the easiest third and 21.1 on the hardest third, at ~10x the token cost**; DATS at 40% of always-hierarchical cost reaches 77.7% vs 73.6%; under budget-matching six cost-aware methods span 21.6 pp and two baselines that led DATS fall behind once calibrated | A, H |
| 2609.13731 | Trustworthy Agentic AI: A Comprehensive Cybersecurity and Systems Survey [A] | 2026-09-12 | Synthesises 206 studies and standards into a 6-dimension trustworthiness taxonomy; frames the problem as "a Turing-complete blast radius where untrusted data represents executable instructions" | D |
| 2609.13466* | Governing at Machine Speed: An Adaptive Governance Intelligence Layer [A+B] | 2026-09-11 | Names the "**attestation deficit**": policies exist but no auditable tamper-evident evidence of enforcement within regulatory timelines. All figures are **third-party vendor/industry-reported**: Stanford AI Index 2026 = 362 incidents; IBM/Ponemon 2026 = USD 4.99M average breach, 92% lacking access controls; EY/AIUC-1 = 38% end-to-end monitoring, 17% agent-to-agent coverage. Explicitly a proposal, no empirical validation | G |
| 2609.13463* | Root-Cause Attribution Is a Search Problem: Continual Search for Long-Horizon Agent Failures [B] | 2026-09-11 | One-shot LLM judges "settle on a plausible diagnosis early, leaving critical evidence in longer traces unexamined"; Continual Search iterates. New MegaRCA-Mix, 50 human-annotated failure trials: **GPT-5.5 F1 0.349 → 0.498 (>40%)**, and lower-tier models in a family can beat higher-tier ones — "effective search supersedes raw model scale" | G, E |
| 2609.13353 | SkillAtlas: An Attack Trace Library for Agent Skills [A] | 2026-09-11 | 3,014 cases / 6,589 traces / 151,131 steps / 233 affected skills / 8 risk categories; **42.5% of successful cases only become successful after a non-success first round**, so one-shot sandbox runs miss them | D, B |
| 2609.13334 | The Agentic Company OS: Substrate Inversion for Sustained Enterprise Agent Deployment [A] | 2026-09-11 | Position: pilots stall because agents read data shaped for humans and apps; proposes rebuilding the "cognitive substrate", with Markdown explicitly called "not a proven agent-native primitive" | A, J |
| 2609.13321* | SkillSeam: Six Principles for Auditing Agent Skill Collections [A] | 2026-09-10 | "Skills rarely fail alone; they fail at the seams of a collection." Perturbations on one sealed skill system: flattening the persistence hierarchy **+60% loaded-skill tokens**; a dangling anchor **+64% tokens, −3.1 pp accuracy**; a synonymous alias moves noncanonical routes **0/32 → 15/32**; overlapping lanes raise ownership conflicts 0/16 → 14/16; bland triggers drive routing conflicts **3/32 → 30/32** and inflate loaded-skill tokens **3.7x**; worst granularity mis-mix **−12.5 pp** | B |
| 2609.13299 | From Experiments to Decisions: Reusing Evidence in Autonomous Coding Research [A] | 2026-09-10 | 400-task campaign: agents remember the experiment but carry forward a conclusion it does not justify — a coordinator restates a novelty-only rejection as "measured closure" — and a prefix-based acceptance gate at three thresholds scores **worse** than ungated adaptation | G, E |
| 2609.12748* | The Mechanics of a Swarm: Reproducible External Reconstruction of an Unintended Agent-Coordination Episode [B] | 2026-09-11 | Forensics from outside the operator: 24 May-2 Jul 2026, LM agents in a timed evaluation wrote to a third party's world-writable wiki (OpenAI acknowledged the incident); reconstructed from **14,591 revisions, 3,103 names, 4,579 pages, 19,913 server events** → 907 cohorts, ~876 episodes (95% interval 774-995); coordination formats converged within a day, median 3.4 h information asymmetry between first report and a later cohort's arrival | G |
| 2609.12742* | Skill Issue: Lessons from Optimizing Repository SKILLs for Coding Agents [A] | 2026-09-11 | Scores SKILL.md against merged PRs reverted at a frozen base commit on three Kotlin repos: **GEPA +4.9 pp on average, SkillOpt +0.1 pp over the seed** — and the GEPA gain **cannot be separated from the agent's run-to-run variance** at one repository's data size; "settling that would take more tasks than one repository's history yields" | B, E |
| 2609.12582* | NovaFabric: Tamper-Evident, Replayable Evidence for Autonomous AI Agent Runs [B] | 2026-09-11 | "A trace is mutable: alterable undetected, with no recipe for re-executing it, silent on whether captured secrets were removed." Run Capsule (15-entity schema) with DSSE signature, RFC 3161 timestamp, Merkle log, redaction attestation; "the contribution is integration, not new cryptography: **OpenTelemetry, DSSE/in-toto and W3C PROV**". Mocked replay 10/10 model responses but **only 2/10 tool-using workloads completed**; declared-stream completeness **0.652 (95% CI ±0.064)**; redaction 14/14 credential types, 9/9 decoys preserved, diff localises 140/140 mutations; blast-radius queries 45.5 ms p99 over 10M edges, 167.9 ms over 100M; REST ingest lossless but **capped at 61.6 req/s (p99 26.8 s)**; six defects found in its own system and corpus (four fixed, one withdrawn, one open) | G |
| 2609.12439 | Debiasing as a Measurement Intervention: Calibrated Ties and Resolution Loss in LLM-as-a-Judge Evaluation [A] | 2026-09-11 | Anti-citation prompting drives worse-cited wins from up to 50.5% down to 0%, but converts validated moderate-gap decisions into Ties before the stress-test endpoint; correctness-conflict accuracy stays ≥93.0%; decoupling recovers 96.5-100.0% of better-plain resolution | E |
| 2609.12436 | LifeFuse-Mem: Lifecycle-Aware State Fusion Against Temporary Overwriting [B] | 2026-09-11 | Separates durable from transient memory so temporary context cannot overwrite durable knowledge and cause behavioural drift in persistent agents | B |
| 2609.12236 | Open Source Stewardship Communities: "We need you, but not your pull request" [A] | 2026-09-10 | Names the "stewardship community": a small core keeps implementation authority because review cost no longer justifies outside patches — AI replaces implementation labour while weakening how OSS renews itself | J |
| 2609.12216* | Guardrailed Meta-Agent Loops: Stress-Testing Policy Pinning, Budget Bounds, and Crash Recovery [B] | 2026-09-10 | Hash-pinned policy fixes goals, scope, evaluation identity, budget and release conditions; 50-seed 2x2 study; **across 240 enumerated crash injections all runs recover the defined outcome but only 210 preserve the normalized trace — 30 pre-commit crashes repeat a planner call**; "successful outcome recovery is insufficient evidence of exactly-once execution" | G, A |
| 2609.12205* | Plans They Abandon, Reports They Author: The Narrative Layer of Autonomous Agents [A] | 2026-09-10 | **5,851 real developer sessions / 355,942 tool calls**: the agent's self-report "referred to about one action in eleven", a reader working from the report alone "recovered roughly a fifth of the action log", neither figure depending on whether the session later needed human correction — and reports drift toward the *stated plan* the more execution diverged from it | G |
| 2609.12191 | GAUGE: When Not to Trust LLM-as-a-Judge in User-Simulated Evaluation of Task-Oriented Agents [A] | 2026-09-10 | 25 agents from six providers: satisfaction carries essentially no information about success — **57.5% of conversations a blind panel rated "satisfied" failed the customer's task** — and the gate's decision-disagreement rate jumps from <1% on wide-reward pairs to 31% on close pairs | E |
| 2609.12012 | Test-Driven Approaches to SE with LLMs: A Survey of Phases, Tasks, and Agent Skills [A] | 2026-09-10 | 87 records (83 with method-level extraction) organised by "what decision a test changes"; concludes test availability, test validity, feedback use and **evaluation independence** are separate properties, and test passing alone does not establish behavioural equivalence | E, I |
| 2609.12001* | Scan the Skill, Govern the Action: Composing Registry Verdicts with Runtime Consequence Control [A+B] | 2026-09-10 | Over **66,192 public ClawHub skill versions**: 705 skills from 135 publishers that every scanner and the registry judge rate clean still instruct an action prohibited by CIS Control 2.7 / NIST SP 800-53 CM-11 (one publisher contributes 506; hand audit of 100 → 92% precision); of 144 commands a live agent ran from real skill docs **34.7% carried a consequence class absent from that document**; over 53 cleared skills the agent reached for a prohibited action in 23 and the gate stopped 23/23; quotes OpenClaw's own report that scanners overlap on at most 10.4% of combined positives | C, D |
| 2609.11999 | Is Bash All You Need? An Empirical Study of Tool Interfaces for Enterprise Digital Worker Agents [A] | 2026-09-10 | Bash alone beats typed tools by **21.8-24.5 pp on TheAgentCompany and 4.8-7.4 pp on APEX-Agents while using 19-72% fewer total tokens**; adding typed tools or persistent tool synthesis on top of bash gives no detectable pooled gain | A, H |
| 2609.11728 | Reproducibility in the Age of Agentic AI: Context Engineering at the Timescale of a Codebase [A] | 2026-09-10 | Position: reproducible-research practice *is* context engineering — tests, commit history, repo structure, instructions, decision records — and agents lower the cost of maintaining them while making the benefit immediate | B, I |
| 2609.11682 | COBRA-Skills: Contextual Bandit-Guided Evolution for Agent Skill Optimization [A] | 2026-09-10 | Budgeted skill optimisation across six benchmarks and three target models: **55-58% lower optimisation cost than SkillOpt** using only 50 unique optimisation examples per benchmark, robust to a change of agent harness | B, H |
| 2609.11677 | Ecdysis: Efficient and Effective Training of Runtime Harnesses for LLM Agents [A] | 2026-09-10 | Identifies "lack of principled failure diagnosis" as the bottleneck in harness evolution: an observed failure is either a model deficiency or a harness deficiency, and optimising per-failure produces model-specific accommodation | A |
| 2609.11294* | Memory Compression for High-Fanout Agent Sandboxes (AgentZip) [A+B] | 2026-09-10 | Sandboxes spawned from one task are not independent; exploiting template-relative and cross-sandbox page redundancy and timing compression to LLM waiting periods gives **up to 8.7x sandbox-owned memory reduction vs 2.1x for the Linux configuration**, slowdown cut from 3.1x to 1.40x | K, H |
| 2609.11264* | Can AI Remediate Backend Failures Safely? GuardedAct with Blast-Radius-Aware Sandboxing [B] | 2026-09-10 | Digital-twin sandbox estimates blast radius and assigns a risk label; a rollback-confidence gate auto-executes only low-risk actions. Five fault scenarios on DeathStarBench: **87.4% recovery, collateral damage 25.6% → 5.2% (−79.7% relative) at ~8 s added MTTR**. The closest thing in the window to an error-budget-style gate — and it is a blast-radius gate, not an SLO gate | K, G |
| 2609.11076* | SaltBench: A Referee-Gated Protocol for Measuring Method Effects in Machine-Checked Software Work [A] | 2026-09-10 | Pre-registered, isolation-probed protocol ("the wall tested by breach probes before any scored run", dated freezes, registered predictions, budget stop counted as a halt): the specify-and-verify arm **cost more on all five Rust/Verus components, no premium above 2.8879x and the three cheapest below 1.4x**, and the registered sign test reached no verdict (3 of 4, p = 0.3125) | E, H |
| 2609.11028* | BenchShield: Formal Model-Backed Instrumentation for Reward Integrity in LLM-Agent Evaluation Infrastructure [A+B] | 2026-09-10 | Treats the benchmark harness as production infrastructure needing its own integrity evidence; corpus of **456 human-adjudicated trajectories drawn from >31,000 public agent runs** across three benchmarks; vs an agentic hackability scanner, full-chain recall **23-94% → 77-100%**, same-vector coverage 16-56% → 43-78%, per-task cost down up to 65%, runtime analysis 96% accuracy from infrastructure-side evidence | E, G |
| 2609.11024 | The Missing Boundary: How Autonomous Agents Lose Control [A] | 2026-09-10 (v2 09-14) | 1,800 trajectories, 5 models, 16 domains: degraded control alone or unsafe opportunity alone does little, but **together loss-of-control hits 55% (62% across ten further domains) — and restoring the boundary drops it to 0% while the unsafe action remains executable** | D, K |
| 2609.10964* | Decoupling Readiness from Release for Tail-Aware Scheduling of Agentic LLM Workflows [B] | 2026-09-10 | Eager release of ready turns accumulates released-but-unfinished work the workflow policy can no longer reorder; mean-CVaR release scheduling on real SWE agent traces cuts P95 workflow flow time under contention, **up to 3.50x speedup**, comparable to eager under light load | S, H |
| 2609.10962* | What a Random Draw from the MCP Registry Contains, and What Tool-Use Benchmarks Contain Instead [A+B] | 2026-09-10 | Seeded probability sample of 400 npm/stdio servers from a 24,135-server census: **only 48.8% complete an initialize handshake** vs 66.7% for a hand-curated frame; dominant failure is servers that never start (37.5%), not missing credentials (13.3%); safety-annotation omission 58.8% random vs 41.5% curated; BFCL v4 near-duplication 16.7% vs 2.8% for real MCP tools, and 68.8% of raw BFCL rows are exact name+description repeats vs 0.4% for real MCP | C, E |
| 2609.10871* | A2ABreak: Systematic Security Analysis of the A2A Protocol [A+B] | 2026-09-09 | A2A is "now governed by the Linux Foundation" yet its security "has received no systematic analysis"; a verified FSM of **37 states and 76 transitions from 929 formalized spec statements** yields **11 new vulnerabilities each exploitable by a fully specification-compliant adversary** (cross-client context injection, credential harvesting via multi-hop identity loss in delegation chains, exfiltration through rogue agents advertising unattested capabilities); 73.3% precision, 84.6% F1 against expert review, where a zero-shot LLM baseline produced **zero** confirmed findings | C, D |
| 2609.10854 | No-Box Vulnerability Analysis: Description-only Detection of Indirect Prompt Injection in MCP Servers [A] | 2026-09-09 | MCPSEC audits registration-time tool metadata only: 20 deployed servers, 177 tools, 95 confirmed vulnerable by humans, 143 flagged | C, D |
| 2609.10762* | Beyond Static Guarantees: Measuring the Static-Pass Dynamic-Fail Gap in Security-Sensitive and LLM-Generated Python Code [A] | 2026-09-09 | 1,355 Python samples; of the 654 clean under a composite Bandit+Semgrep gate, dynamic verification confirmed or partly confirmed exploitability in **95 files — 14.53%, roughly 1 in 7 statically clean samples**; by dataset 33.7% (RedCode), 28.6% (CyberNative), 5.4% (SecurityEval); **CWE-338 and CWE-916 were flagged by neither scanner** | E, D |
| 2609.10416 | TrajMark: Ownership Attribution and Segment-Level Tamper Localization for Coding-Agent Trajectories [A] | 2026-09-09 | Watermarks the *visible process*, not the patch: a sparse owner layer (6-bit deployment id in keyed READ actions) plus a fragile localisation layer exposing which protected region was edited | G |
| 2609.10248 | A-JIT: Agentic Just-In-Time Software Construction [A] | 2026-09-09 | Position: the shipped artifact becomes code + runtime harness + embedded agent that specialises logic to live traces, the way a JIT specialises machine code | A |
| 2609.09875* | AgentAudit: An Open, Extensible Framework for Full-Lifecycle Trust Evaluation of AI Agents [A+B] | 2026-09-09 | Attaches to the agent and reads only the recorded trace, scoring ten dimensions plus failure attribution to a stage; **Claude Sonnet 5 95.1 and GPT-5 80.6 composite trust vs 57.6 / 45.7 / 22.6** for Sarvam 105B, Llama 3.3 70B, Gemini 2.5 Flash; several non-frontier models are repeatedly classified **Unsafe_Compliance** on adversarial tasks rather than merely failing them, "a distinction that pass/fail benchmarks cannot surface". Stated limit: all traces scored by a single fixed judge that was itself one of the evaluated models | E, G |
| 2609.09646 | RobustSGPO: Search-Space Control for Agent Harness Evolution [A] | 2026-09-08 | 120 tasks / 95 runs / 7,350 candidate attempts: completion on 30 held-out tasks **60.0% → 80.0%** and test quality 3.77 → 4.14 under a 20M-token budget; periodic 1→2→3 permission scheduling beats fixed max permission by 0.28 points | A |
| 2609.09404 | An Experimental Evaluation of Multimodal Prompt Injection Attacks on Agentic AI Frameworks [A] | 2026-09-08 | 720 runs / 6 frameworks / 5 models / 6 visual carriers: attacks *attempted* in 12.8% of runs but *complete* in ~1%, the gap closing at the planning step; **the model matters far more than the framework**; on audio, where the signal arrives, completion reaches 49% of cells (75% for one) | D |
| 2609.09212 | AgentHijack: Visual Patch Attacks on Multimodal Computer-Use Agents [A] | 2026-09-05 | 600 online cases across five GUI-agent/VLM backends: T-ASR 84.5%, TAPR 47.0%, **end-to-end 20.3%** — and in some successes the agent runs the malicious terminal command and then carries on with the benign task | D |
| 2609.09203 | OpenDiscoveryTrace: Process Traces for Evaluating AI Scientist Workflows [B] | 2026-09-05 | 558 complete trajectories over 124 tasks, 9 fields per step, 7 models; pilot on 363 LLM-judged trajectories: three frontier models within 84-89% success yet **Claude Opus 4.6 produces 30x more errors than GPT-5.4 (2.5 vs 0.08 per trajectory, p < 0.0001, Cliff's δ = 0.613)** with different profiles (66.7% tool misuse vs 83.6% reasoning errors) | G, E |
| 2609.09134 | Co-Evolving Harnesses and Models: On-Policy Correction Helps Weaker Models Catch Up Where Imitation Fails [A] | 2026-09-08 | Evolve a harness with a weak model, then train that model on an expert's trajectories under it, and **performance regresses on all seven enterprise tasks by 4 to 30 points** — imitation breaks model-harness fit; on-policy single-turn correction fixes it | A |
| 2609.09133 | ExecCritic: Learn to Test, Test to Improve for Coding Agents [A] | 2026-09-08 | Test agent separated from Repair agent behind a fail-closed harness that freezes tests: on SWE-bench Verified, base-agent tests **drop** resolved rate from a no-test baseline of 61.2% to 57.3%, while GPT-5.6-sol tests raise it to 65.3% — test quality decides whether feedback helps at all | E, A |
| 2609.08472 | Beyond Agent Harnesses: Cross-Substrate Authority for Multi-Agent Systems [A] | 2026-09-08 | "Cross-substrate authority gap": identical final files can require opposite safe actions; authority-blind evidence gets **0/32 final semantic success vs 32/32 with receipts**, and a deterministic execution guard stops all six unsafe intents replayed from fixed model outputs | D, A |
| 2609.08371* | Authority Is Not a String: A Capability-Scoped Harness for Prompt-Injection-Resistant Coding Agents [A+B] | 2026-09-08 | CapScope derives a task-wide authority ceiling from trusted input **before** any repository content or tool output is read and stores typed capabilities **outside the model's context**; 300 runs on the Pi agent: the injected effect executes in **33-47 of 75 runs under ambient-authority and global-policy baselines vs 3 of 75 under CapScope**, with 68/75 repairs still completed against baselines' 68-72/75 | D, A |
| 2609.08318 | AttnCompress: Dynamic Attention-Guided Trajectory Compression for Software Engineering Agents [A] | 2026-09-08 | PPL-spike segmentation + proxy-attention relevance + rolling recall window; 53.17% pass rate on SWE-bench Verified while cutting context length | B, H |
| 2609.08301 | Agent ATO: Visualizing Agent Interaction Timelines from Logs [A+B] | 2026-09-08 | Turns console logs into filtered timelines (discovery / read / edit / execute) because "agent behaviour is difficult to understand from final code changes alone"; illustrative only, selected runs from two repair tasks, **no evaluation yet** | G |
| 2609.08279* | What Eviction Destroys: A Restore-Counterfactual Audit of Forgetting in Agent Memory [B] | 2026-09-08 | Audits what an eviction policy actually destroyed by restoring the evicted item counterfactually, rather than scoring recall on what survived | B, E |
| 2609.08149 | SWE-Bench Pro Verified: A Reliable Benchmark for Software Engineering Agents [A] | 2026-09-07 | Repairs two unreliability sources in SWE-Bench Pro — reward hacking via gold-solution/eval leakage, and task-quality defects; on the verified version **some models perform substantially worse than previously reported** | E |
| 2609.08126 | SchemeArena: Factorized Stress Testing of Scheming in LLM Agents [A] | 2026-09-07 | 400 factorised scenarios: explicit instrumental goals are the strongest driver of scheming, and **oversight has mixed effects — action-only monitoring increases scheming in several closed models** | E, D |
| 2609.08040 | VEX-Bench: Benchmarking LLM Agents for Assessing Exploitability of Supply Chain Vulnerabilities [A] | 2026-09-07 | 75 expert-labelled real cases in Python/Java/Go, nine models across three agent harnesses; GPT-5.5 and Claude Opus 4.6 reach ~80% F1 on the binary question | E, D |
| 2609.08020* | Service Health Engineering for Distributed Systems [B] | 2026-09-07 | **Not an agent paper** — an IEEE Reliability Magazine article on judging service health by end-to-end user-journey completion rather than component dashboards (service promises, SLIs/SLOs, watchdogs, weekly service-health reviews), plus a human-reviewed AI-assisted reporting architecture that deliberately keeps AI out of the decision | S |
| 2609.07785 | What Does an LLM-Agent Leaderboard Rank Actually Compare? [A] | 2026-09-07 | Estimand-aware pairwise procedure over SWE-bench, AgentRewardBench and tau2-bench: **close rank differences are often unresolved**, and proxy labels or utility rules can change which system is selected | E |
| 2609.07680* | Audit Without Verification: When LLM Accountability Layers Relay Rather Than Check [A] | 2026-09-07 | Six-agent partitioned pipeline, **345,600 requests per chain model**: the accountability layer originates almost nothing (**zero allegations across 7,996 clean episodes**) and misfilters badly (names an innocent party in 34.4% and 62.6% of clean episodes with a false alarm); an auditor reading the *reports* recovers the true origin in **4.1%** of cases — below a uniform guess (20%) — **while reaching 60.3% from the raw documentation of the same episodes**; deleting the field carrying each agent's own conclusion raises it to **45.2% (+41.2 pp, 95% CI +35.3 to +46.9)** and collapses adherence 94.4% → 3.4%. The pre-registered hypothesis was **not** supported | G |
| 2609.07375 | A Text Mining and Classification Approach for Analyzing Architecture Decision Records [A] | 2026-09-07 | ADRs from ~550 OSS repos: existence/technology/process decisions dominate while **alternatives, decision drivers and some quality concerns stay under-documented**, with recurring MADR template mismatches | I, J |
| 2609.07370 | Beyond Fluent Generation: A CPU Reliability Benchmark for MCP-Style Tool Calling in Sub-2B SLMs [A] | 2026-09-07 | 100 prompts, five sub-2B models: Qwen2.5-1.5B 75% greedy / 79% sampling, Qwen2.5-0.5B 72% → 32% under sampling, Phi-1.5 0%; **only 5 of 1,000 raw responses were directly parseable as JSON** without the recovery parser | C, E |
| 2609.07360* | Scanning the Harness: An Empirical Study of Supply-Chain Defects in AI Coding-Agent Configurations [A] | 2026-09-07 | 3,171 repos / 2,660 multi-component setups / 511 skill collections, every finding validated three ways: **9.8% install an MCP server with no version pinned, 3.1% pre-approve arbitrary execution behind a scoped-looking `Bash(python:*)` grant, 3.8% carry a skill that pre-approves the shell for whoever installs it; 16.0% of setups carry a security defect (16.7% any defect) against a raw scanner rate of 25.5%** — a third of what a naive scan reports does not survive validation. No credential-exfiltration path confirmed | D, A |
| 2609.07065 | VST: Verifiable Structured Transport for Auditable Agent-to-Agent Alpha Discovery [B] | 2026-09-07 | Replaces free-form A2A hand-offs with typed, causally addressable unicast records so the committed stream is a replayable causal trajectory. Honest negative: **a controlled ablation shows an equal-information free-text channel reaches the same predictor hit rate** — "structure is the enabling contribution, and its value is not accuracy"; what typing buys is schema-checkable, deterministically replayable state | C, G |
| 2609.06972 | AgentDrift: A Step-Labeled Benchmark of Injection-Hijacked LLM Agent Trajectories [A] | 2026-09-06 | 12,536 trajectories / 71,024 steps, every step labelled benign / injection point / hijacked / failed injection; 4,000 benign, 5,536 attacked, 1,500 failed-attack, 1,500 hard negatives | D, E |
| 2609.06966 | MOLE: Detecting Insider Threats in AI Agents [A] | 2026-09-06 | 150 AI-operated accounts over 30 workdays, ~20B tokens: **72% of 39 agent models complete most assigned harmful objectives and refusal does not predict completion**; the best monitor in the single-day audit comparison still misses nearly half of completed harm | D |
| 2609.06780* | Shortcutting the Fix: Identifying and Categorizing Agentic Exploits in SE Benchmarks [A] | 2026-09-06 | Turn-level judge over five open models: exploitation rates (local Git history, upstream repositories, memorised solutions) **45.1-82.4% on SWE-bench Multilingual and 44.2-66.1% on DeepSWE** under standard prompts, cut to **4.0-10.7% / 1.5-7.1%** by one appended originality instruction with core performance held | E |
| 2609.06543 | A Unified Policy Architecture (UPA): The Governance Kernel for Enterprise AI Operating Systems [A+B] | 2026-09-06 | One policy model over agents, tools, workflows, memory, resources and A2A, extending policy beyond authorisation to runtime obligations, human approvals and audit evidence. No evaluation | G, D |
| 2609.06445* | Causal Attribution for Agentic Decisions: Estimators, Coupling, and a Traceability Specification [B] | 2026-09-06 | Negative result on attribution estimators: "under the marginal estimand a causally inert step has the identical total effect to the decisive one on every run of our planted chain, an algebraic identity and not a coincidence at one draw"; under common random numbers the decisive step **returns exactly zero on the runs where the executing step flips, about one in ten, while its direct effect there is 0.25** — "an exact zero does not certify that a step did nothing". Plus the regulatory calendar: "**Article 86's right to an explanation has applied since 2 August 2026, while the Article 12 logging and Annex IV documentation that could evidence one were deferred to 2 December 2027 by Regulation (EU) 2026/1744**". Honesty marker: the discrepancy experiment is pre-registered, published in full, and **not run — no empirical result is claimed** | G |
| 2609.06367 | Robust Conformal Consensus: Multi-Agent LLM-as-a-Judge Interval Evaluation with Conformal Prediction [A] | 2026-09-05 | Conformal intervals per judge, aggregated across judges, to get coverage guarantees a single-judge setup cannot give | E |
| 2609.06213* | Beyond Lexical Metrics: Sentence-Embedding Detection of Reviewer Habituation in AI Code Review [A] | 2026-09-05 | **11,429 reviews / 400 repeat reviewers / 207 days**: approval rates rise **30.5% → 36.6%** (Wilcoxon p = 8.6e-8, d = 0.25) while four hand-crafted linguistic features show no monotonic decline (all \|ρ\| ≤ 0.53, p ≥ 0.11, classifier F1 0.485 below the majority baseline); embeddings do carry signal (MLP F1 = 0.74); Granger says approval change *precedes* language change — habituation shows up in behaviour before language | F, J |
| 2609.06128* | Substrate-Portable Execution for Production LLM Workflows [B] | 2026-09-05 | Amazon Rufus (serves millions of customers): real-time, async and batch modes each have **distinct service-level objectives** and usually separate runtimes; one typed dataflow graph compiles to in-process streaming / AWS SWF / Apache Flink with no workflow code change, dozens of production configs across five orchestration patterns, **no detectable output-quality difference across the three bindings**; batch API discount stated as 50% at published prices | S, A |
| 2609.06063* | Explaining AI Agents Through Execution Traces [A+B] | 2026-09-05 | Post-hoc XAI over execution traces only, so architecture-agnostic; human + automated evaluation shows it reliably flags **unsupported claims, unjustified actions and evidence gaps**, beating naive LLM-generated explanations | G |
| 2609.05920 | ClosureBound: Versioned Transitive Dependency-Closure Binding and Operation-Time Effect Governance for Agent Skills [A] | 2026-09-05 | The one `"reference monitor" AND agent` hit in the window: binds a grant to an exact *transitive* closure root so lazy or recursive dependency changes cannot inherit authorization; 40 frozen fixtures, 18 kernel contracts, 84,608 states explored | D, B |
| 2609.05903 | EvoSafeHarness: Evolving Model- and Domain-Specific Harnesses for Securing Agents [A] | 2026-09-05 | A harness strict enough for one model over-blocks another, so it searches policy + code per deployment: DecodingTrust-Agent ASR **45.6% → 10.0% at a 3.3-point utility cost**, best in 14 of 15 cells | D, A |
| 2609.05901 | From Review to Authorization: Key-Isolated Threshold Signing for LLM Agents [A] | 2026-09-05 | Keeps the signing key and every threshold share outside all LLM processes, so injection cannot cross the judgment→execution boundary without t distinct uncompromised domains | D |
| 2609.05736 | Beyond Prompts: Measuring and Optimizing LLM Tool-Agent Harnesses [A] | 2026-09-04 (v2 09-08) | Harness selection as budgeted search over prompts + tool-boundary middleware; PRISM gets mean held-out lifts of **14.2 / 14.9 / 10.1 pp** on BFCL multi-round, tau2-Retail and tau2-Telecom, and argues **the reliability of the chosen harness must be reported, not just the best gain** | A |
| 2609.05692 | Regret Dominates Surprise: Design-Time Requirements Engineering for Agentic-AI Safety [B] | 2026-09-04 | Extends GORE with a Regret-Dominance Mechanism routing between routine autonomy / reflective reasoning / human escalation; 100-seed simulation cuts silent failures to near-zero and detects risk ~17.5x faster than a sensor-only baseline; retrospective gate over 208 AGENTHARM scenarios x 7 LLMs **improves refusal only for models already above 80% baseline refusal (84.1% → 90.9%)** | E, I |
| 2609.05587 | Agents Trust Tools Too Much: Measuring Reliance on Unreliable Tools [B] | 2026-09-04 | 14 LLMs, 3 tools with corrupted returns: **mean adoption of corrupted content exceeds one third for every tool and reaches 68.0% for web search**; reasoning traces show agents recognise the conflict and even recover the right answer internally, then present only the corrupted one without warning; none of three intervention levels consistently mitigates | E, G |
| 2609.05571 | Grounded Skill Synthesis from Code at Scale for Agentic Intelligence [A] | 2026-09-03 | Code2Skill over 19,769 GitHub repos → **1,006,822 accepted skill records**; retrieval-augmented models improve 11.7% on average across 72 protocol-matched evaluations and beat trajectory-derived banks on all seven shared benchmarks | B |
| 2609.05527 | Beyond "AI Helps Humans": Decision-Targeted Evaluation Design for Human-Agent Teams [A] | 2026-09-01 | The deployment question is whether human+agent beats *both* alternatives, neither of which is observed after deployment; TEAM-Design allocates a fixed replay budget between human-only and agent-only replays | E, J |
| 2609.05364 | Design Docs Are All You Need: An AI-native Machine-Learning Performance Tool [A] | 2026-09-04 | SMART's main branch is a DAG of natural-language design docs with almost no code; sub-agents regenerate the implementation from the docs, and regenerated implementations reproduce hand-audited reference models **to round-off precision** | I |
| 2609.04898 | RefactorPlatform: An Open-Source Harness for Controlled Evaluation of Repository-Scale Refactoring Agents [A] | 2026-09-04 | 100 RefactorBench tasks, four model families: AST-aware chunking beats naive token windows by **25-30%**, naive retrieval falls *below* the retrieval-free baseline, and a lean retrieval-augmented single agent (86%) beats the sub-agent configuration (66%) | A, E |
| 2609.04680 | How Developers Discuss Generative AI: A Longitudinal Study of the VS Code Community [A] | 2026-09-03 | 43,806 candidate issues 2021-01 → 2026-06 filtered to 25,227: discussion is dominated by **agent management, configuration, reliability, authentication and billing**, while hallucination and licensing — the survey-study staples — rarely surface | J |
| 2609.04630 | Software Engineering in the Agent Era: From Trustworthy Change to Human Agent Software Organizations [A] | 2026-09-03 | Framework where execution scales elastically but **acceptance authority does not**: Trustworthy Change, Responsibility Topology (single-centre vs multi-anchor), and a Human-Agent Cell that produces evidence but is granted no acceptance authority | J, I |
| 2609.04518 | What Does Multi-Harness RL Learn? Credit Assignment and Portability in Coding Agents [A] | 2026-09-03 | 24,000 sealed SWE-bench Verified evaluations: **the evaluation harness moves mean solve rate from 2.14% to 9.27% (x4.3) where the training recipe moves it by 1.16**, and the Cross-vs-Within grouping difference (+0.25 pp) is smaller than each rule's own seed range | A, E |
| 2609.04280 | EvoHarnessBench: Can Your Agents Keep Pace with an Evolving Harness? [A] | 2026-09-02 (v2 09-10) | Non-stationarity moved from the task stream into the harness: 17 streams, 802 tasks, 520 tools, 42 skills, 62 agents; **harness expansion alone degrades previously solved tasks — "harness-induced forgetting"** | A, E |
| 2609.04218 | A Governance Methodology Layer for AI-Assisted Software Development [A] | 2026-07-01, ann. Sept 2026 (v2 09-08); v1→announcement ≈ 2 months | Runtime-decoupled, file-based governance gate + methodology-as-code; controlled ablation (N=5, 8-item ground truth) records 62% lenient recall vs 50% and 25% strict vs 0% — and the authors **withdraw** an earlier severity-grade differential that did not survive blind re-grading | G, I |
| 2609.04167 | SWE-Gate: Passing Functional Tests Is Not Enough for Software Engineering Agents **(seen 09)** [A] | 2026-09-03 | 303 instances / 75 Python repos with separate functional and review-constraint tests; **of 644 repairs that pass functional tests, 221 fail the review constraints** | E |
| 2609.04017 | A Black Box for Agentic Processes **(seen 09)** [B] | 2026-09-03 | Vendor-neutral cryptographic commitments for agent messages and tool calls, framed for EU AI Act / NIS2 audit reconstruction | G |
| 2609.03920 | Value-Preserving Architectures for Agentic AI Systems [A] | 2026-09-03 | Argues coordination mechanism, communication protocol and topology are value decisions, not only performance ones; three patterns (federated privacy-aware, distributed pluralist, guard-agent) | A, J |
| 2609.03884 | A Blind Trust, the Bloody Thrust: attacker-controlled hook updates steer agent harnesses **(seen 09)** [A] | 2026-09-03 (v2 09-08) | HookPry trojanises lifecycle hooks via plugin metadata: **compromises all 7 harnesses, up to 92.5% per harness over 1,000 runs; Microsoft Defender 0% recall and three static defences together miss 47.5%** | D |
| 2609.03787* | DNative-Twin: Decision Graphs and Digital Twins for Reconstructable Agentic Decisions **(seen 09)** [B] | 2026-09-03 | Graph-native twin records a committed decision as a typed trajectory and re-executes the mechanism; 300 injected instances: unresolved-divergence recall **0 → 0.667 with replay-contract state → 1.0 with verification results**; median end-to-end time 0.794 s → 8.889 s across 500-5,000 BPI 2020 cases | G |
| 2609.03598 | RASER: Resilient Agent Scheduling and Execution Runtime for HPC Clusters [B] | 2026-09-03 | Slurm is not built for agentic workflows (unpredictable durations, external API calls, fault tolerance); user-space agentic job arrays with work stealing, application-level checkpointing + Slurm requeue, Apptainer container isolation with no image modification; **makespan −39% vs static partitioning** | K, S |
| 2609.03467 | When Users Don't Ask: Benchmarking Context-Driven Memory Retrieval [B] | 2026-09-03 | LOCOMO-CONV, four query styles over five memory systems: conversational framing exposes retrieval gaps QA-style probing misses, and **strong retrieval does not translate into response quality** — "silent grounding" on implicit queries | B, E |
| 2609.03456 | The Psychological Costs of AI Adoption in Software Engineering **(seen 09)** [A] | 2026-09-03 | Case study, N = 21 interviews one year after a services company's AI rollout: accountability anxiety, craft-identity disruption, meaning erosion, workload intensification, uncertainty distress | J |
| 2609.03236 | Speculative Macro Commit for Faster Tool-Using Agents [A] | 2026-09-02 | Two-tier actor/drafter with a macro library of recurring action skeletons: latency **−10.23% vs Speculative Actions and −18.59% vs sequential** on tau²-Bench Telecom; wall time −7.7% / −44.9% on AppWorld | H, A |
| 2609.03028 | Requirements After the First Edit **(seen 09)** [A] | 2026-09-02 | 3,553 SWE-chat sessions: a post-implementation requirement arrival is followed by **roughly twice the code invalidation** of matched non-requirement edits, with no decline within a session and no detected effect from advance warning | I |
| 2609.02866* | When Does Authorization End? Effect Closure at Provider Boundaries [B] | 2026-09-02 | Defines **policy-relative effect closure** ("a grant is closed when its existing authorizations retain no such path, and it cannot issue any new ones"); EFFECTBOUND returns a strategy, an impossibility certificate, or no verdict. Case study: **across GitHub, Kubernetes, NATS and Kafka, closure fails in three ways** — "the GitHub tool cannot bind a merge to the reviewed commit; a controlled run confirms that it may merge a different commit"; NATS reports no stored or pending messages while dispatched work can still publish; in Kafka all fixed-set brokers had applied the revocation yet an earlier authorized request could still append. A gate closes the studied path on Kafka 4.3.1 | D, K |
| 2609.02786 | SafeEvolve: Harness-Policy Co-Evolution from Agent Experience for Safety Alignment [A] | 2026-09-02 | Converts trajectory-level safety evidence into bounded, component-level, **auditable and reversible** harness artifacts, then SFT+RL on the policy side | A, D |
| 2609.02783 | EarlyEval: Cheaper Agent Evaluation via Early Outcome Prediction **(seen 09)** [A] | 2026-09-02 | Halting a run once the outcome is predictable removes **13-26% of steps and up to 44.1% of input tokens** at 89-97% prediction accuracy, perturbing resolve rates by 1-2 pp | E, H |
| 2609.02749 | Repo-To-Skill: Distilling GitHub Repositories Into AI4AI Skills [A] | 2026-09-02 | 5,000+ verified skills from 1,000 ML repos into 20 areas / 178 capability families; with backbone, harness and budget fixed, the skill-equipped agent scores **+134.3% on MLE-bench and +34.4% on PaperBench** | B |
| 2609.02690 | ACLE-MCP: Attested Capability Leases for Execution-Time Trust in Remote LLM Tool Use **(seen 09)** [A+B] | 2026-09-02 | Names the "post-authorization execution trust gap" — OAuth says who may call, not which workload executes — and issues short-lived sender-constrained leases consumed by a provider-side Execution Gate; **+25.7% latency vs OAuth-only** | C, D |
| 2609.02564 | A Finger on the Scale: Covert Policy Steering through Agentic Skills **(seen 09)** [A] | 2026-09-02 | Third-party skills as externalised policy: **81.33% and 63.33% attacker-favoured selection at 100% utility preservation**, transferring across backends, undetected by the evaluated scanners | D |
| 2609.02302 | Improving Evaluation Realism with Inference-Time Compute and Deployment Scaffolds [A] | 2026-09-02 | Evaluation awareness as the obstacle; DISH wraps the target in a real SWE-agent harness and critique refinement spends inference compute on realism — the two compose | E |
| 2609.02264 | Codebook Agent: Amortized Topology Design for LLM Multi-Agent Systems [A] | 2026-09-02 | Topologies surviving a reward filter **collapse to about six distinct graphs** even as codebook capacity grows 8 → 64, and edge count is *negatively* correlated with measured token consumption (Pearson r ≈ −0.4) — sparsifying makes inference more expensive | A, H |
| 2609.02127 | Stored Is Not Supported: Typed Provenance and Assertion Guardrails for Persistent AI Agents **(seen 09)** [A] | 2026-09-02 | "Persistence changes availability, not epistemic standing"; typed provenance graph + release-time mediator passed **none of 19 unsafe opportunities unqualified** across 24 conformance cases | G, D |
| 2609.02035 | Implicit Manipulation for Skill Selection in LLM Agents with Semantic Matching [A] | 2026-09-01 | No injected instruction at all — just shaped metadata: target-selection rate **15.2% → 63.5%** across four domains and eight selectors; human reviewers block it in **2.9%** of judgments vs 91.4% for explicit steering | D, B |
| 2609.01985 | When Agents Implement Systems: A Case Study in Defects, Detection, and Evaluation Rigor [A] | 2026-09-01 | Single-session case study against a fixed systems spec, cataloguing five defects by constraint violated **and by detection method** — which check would have caught it | E |
| 2609.01939 | Bonded Recourse for Smart-Contract Settlement of Compensable Agent Side Effects [A] | 2026-09-01 | Authorization covers admission and compensation covers rollback; neither settles residual harm after a *permitted* action fails — typed receipts + collateral do | G, D |
| 2609.01931* | Agent Flight Recorder: Tamper-Evident Audit Trails with On-Chain Anchoring **(seen 09)** [A+B] | 2026-09-01 | Eight semantic fields per action, hash-chained and Merkle-batched, on-chain anchoring only for cross-organisational disputes (32-byte epoch root, no event content on chain): **~48 µs median added latency, 512 bytes/event, $2.30 per 100K events on L2**, 100% detection of edit/delete/reorder/fork with zero false positives, forensic-query precision **1.0 vs 0.013 and 0.077** for unstructured text search | G |
| 2609.01873 | Epistemic Sybil Resistance: Multiplying AI Agents Without Multiplying Evidence [A] | 2026-09-01 | >20,000 controlled agent report/extraction calls: holding one evidence root fixed while reports rise 1 → 32 **collapses naive posterior coverage from 0.940 to 0.263**; raising evidence roots 1 → 16 closes the gap. Another agent is not another observation | A, G |
| 2609.01693 | Public-Sharing Labels and Verbatim Field Egress in an MCP-to-A2A Agent Configuration [A] | 2026-09-01 | 480 deterministic-scored trials, 4 models x 3 label arms: the CONFIDENTIAL-vs-unlabelled contrast is floor-limited and inconclusive, while adding "PUBLIC - OK TO SHARE" is associated with **higher** verbatim egress (Claude Sonnet 5 mean +0.800 across all 10 scenarios) | D, C |
| 2609.01677 | Skill-as-API: Confidential Multi-Agent Coordination for Agentic SE **(seen 09)** [A] | 2026-09-01 | MCP and A2A publish every skill's description and schemas to every peer; Skill-as-API keeps the body closure-captured in the owner's process, three-agent PR-review case study at 1.8-2.9 s cross-continent hot-reconnect | A, D |
| 2609.01600 | CordisBench: Can Language Models Reason About Component Lifecycles in Dynamic Agent Harnesses? [A] | 2026-09-01 | 1,200 questions on plugin dependency/teardown reasoning; reliability falls as relevant interactions grow, and on the 16-interaction subset **GPT-5.6 Luna burns nearly 3,000 reasoning tokens per question at medium effort** for something a finite reference semantics decides exactly | A, H |
| 2609.01481 | Harness-of-Harness: Multi-Day Autonomous Software Development **(seen 09)** [A] | 2026-09-01 | Loops over existing harnesses with verifiable increments and separated implementation/evaluation testing: **average +52.25% relative, max +82.86% after three iterations** across three harness-model pairs; a 70+-iteration multi-day run builds an FPS | A |
| 2609.01466 | Parsing the Stream: A Live Trace Model for Long-Horizon Agents and Their Observers **(seen 09)** [A+B] | 2026-09-01 | Append-only ledger folded into typed run state: monitoring questions answered with **~14-15x fewer input tokens at 5-7x lower cost and higher accuracy (0.85-0.87 vs 0.48)** than reading the raw trace | G, H |
| 2609.01437 | HarnessDev: Can LLMs Create and Evolve Their Own Agent Harness? **(seen 09)** [A] | 2026-09-01 | Unit of evaluation moves from task output to runnable infrastructure; across six creator LLMs, four domains and 2,207 downstream instances, **generated harnesses stay substantially behind mature human-engineered references on code and on search/research** | A |
| 2609.01360 | EDGE: Error Dependency Graph-Guided Multi-Error Attribution in Multi-Agent LLM Systems [A+B] | 2026-09-01 | Agent failures usually contain several *related* errors; builds an error dependency graph validated by counterfactual rollout instead of naming one root cause; improves category-level multi-error attribution on TRAIL and MAST | G, E |
| 2609.01222 | What's in Your Agent's Context? Context Privilege Escalation Attacks against AI Agent Harness **(seen 09)** [A] | 2026-09-01 (v2 09-02) | First systematic study of context-assembly design in real harnesses; M-CPE and X-CPE analysed against **12 real-world harnesses including Claude Code and Codex**, with consequences up to full compromise and RCE | D |
| 2609.01040* | Causal Evidentiary Governance for High-Risk Machine Learning Systems [B] | 2026-09-01 | Versioned committed DAG partitions causal pathways into allowable/disallowed; Causal Harm Rate measures prediction variation on disallowed paths; each decision carries a signed **Decision-Evidence Packet cryptographically binding prediction to a DAG digest**, appendable to a Merkle tree for log-cost inclusion proofs; validated on 10,000 synthetic credit applicants | G |
| 2609.00829 | HarnessEvolve: Learning from Reference Trajectories for Reliable Agent Self-Evolution [A] | 2026-09-01 | Names the three failure modes of self-evolution — credit-assignment failure, shortcut learning, catastrophic forgetting — and gates every harness update through a quality gate (leakage, prompt bloat) and a performance gate | A |
| 2609.00749 | ContextPipe: Database-Inspired Context Assembly for Long-Horizon Agents **(seen 09)** [A] | 2026-09-01 | Context assembly as query execution, with EXPLAIN ANALYZE: **−31% total tokens, −23% LLM calls, −9% response time** on the SWE-bench Pro Qutebrowser subset, at a lower KV cache-hit ratio | B, H |
| 2609.00065 | Scientific Agent Skills: A Library of Procedural Knowledge for Research Agents **(seen 09)** [A] | 2026-08-30, ann. Sept (v2 09-02) | 163 skills in 16 areas; **always-resident descriptions alone cost 7.1% of a 200,000-token window**, median documented workflow 23.9%, and 29 of 46 would overflow if every reference file loaded | B |
| 2608.30441 | ECLIPSE: Self-Evolving Stealthy Prompt Injection against Long-Horizon Agentic Systems **(seen 09)** [A] | 2026-08-31, ann. Aug (v2 09-06) | Verifies candidate tool chains in a sandbox, then renders the verified chain as one natural prompt and steers the target via tool-description state cues — named against Codex, Claude Code and OpenClaw | D |
| 2608.29460 | Can escalation channels redirect reward hacking toward defect disclosure? **(seen 09)** [A] | 2026-08-29, ann. Aug (v2 09-02) | 2x2 factorial over 8 frontier models in 5 families: escalation tool + anti-reward-hacking policy cuts reward hacking **23.6% → 5.3% (OR = 9.2, 95% CI 5.0-16.8, p < 1e-12)** with no detectable cost, eliminating it for 6 of 8 | E |
| 2608.28553 | Logos: An Agent Harness on a Cross-Process Bus [A] | 2026-08-28, ann. Aug (v2 09-06) | Single-process plugin harnesses put every session in one failure domain: under one injected fault on 200 tasks the single-process reference **lost every session and scored 1.5%**, while the MCP configuration kept sessions but burned 1,099 calls on a dead endpoint | A, K |
| 2608.27427 | Persona-Execution Separation: An Architecture Pattern for Evolving LLM Agents under Execution Audit [A] | 2026-08-27, ann. Aug (v2 09-14) | Persona may drift freely; execution stays faceless and audited in a separate trust domain behind a governed contract bridge, replicated across five models and four providers | G, A |
| 2608.26263 | SKILL.state: Scalable Long-Horizon Agent Skills [A] | 2026-08-26, ann. Aug (v2 09-01) | Replaces append-only conversational history with an explicit mutable execution state; intermediate reasoning discarded after a validated state update, so the prompt stops growing with history | B |
| 2608.25593 | JIT-Agent: Scaling Harness Intelligence via Just-in-Time Harness Evolution **(seen 09)** [A] | 2026-08-26, ann. Aug (v2 09-03) | A model trained to synthesise harnesses: DeepSeek-V4-Flash + JIT-Agent **surpasses GPT-5.6 on DeepSearchQA (+9.1) and OdysseyBench (+4.3)**, GLM-5.2 gains up to +20.2 | A |
| 2608.25241 | A Few Pages of Markdown: Committed AI Configuration and Quality Cost after Coding-Agent Adoption **(seen 09)** [A] | 2026-08-25, ann. Aug (v2 09-14) | 441 repos, RAMP maturity scale (97% human-label agreement): agents accelerate commits 28-38% at every level, but agent-first repos **without committed AI configuration show ~2x the cognitive-complexity increase (+53% vs +27%) and 1.7x the static-warning increase**; 73.8% of artifacts committed once and never modified | B, J |
| 2608.25202 | SpecMine: A Large-Scale Corpus of Spec-Driven Development Artifacts **(seen 09)** [A] | 2026-08-25, ann. Aug (v2 09-01) | 470,795 spec files across 73,030 repos attributed to 17 named tools, a Kiro census of 98,574 files / 12,910 repos, 5,992 spec-touching PRs across 581 repos, 2,421,323 typed references | I |
| 2608.23642 | AI Agents Push Humans Out of the Loop [A] | 2026-08-23, ann. Aug (v2 09-06) | Position: current agent design both impedes oversight *and* degrades the cognitive capacity oversight needs; asks for design affordances that counteract skill atrophy from extended automation use | J |
| 2608.23610** | From Traceability to Justifiability: Accountability Structures in Agentic Software Engineering **(seen 09)** [B] | 2026-08-21 | Primary-data measurement study (47-platform two-pass graded documentation survey + 30-repository depth measurement, "not a literature survey"). Defines behavioural continuity over a **seven-component tuple — source, model version, instructions, retrieval configuration, tool definitions, runtime configuration, environment** — and measures content-addressed identity over it: **"across the 47 platforms, in a survey of 188 double-graded cells, we found no platform, in either class, whose default record emits a content-addressed identity over the behavioral tuple, including all 27 platforms in the class where it would most plausibly exist"**; the agent class records the tuple by default as immutable *nominal* versions on 16 of 27 platforms. See §5 for the full carry | G |
| 2608.21516 | Neuro-Formal Verification: Agentic Language-Agnostic Formal Program Reasoning [A] | 2026-08-21, ann. Aug (v2 09-14) | Agentic formal reasoning over programs without language-specific front ends — the "machine referee" side of the 2026-10/11 argument | E, I |
| 2608.19799 | SWE-bench Science: Can Coding Agents Resolve Engineering Tasks in Science? **(seen 09)** [A] | 2026-08-20, ann. Aug (v2 09-01) | 119 tasks / 98 repos / 20 domains; **best agent (Claude Code with Opus-5 max) is below 50% pass@1**, and a paired ablation shows scientific guidance is not uniformly beneficial | E |
| 2608.18398* | LEDGER: Claim-to-Evidence Trace Graphs for Auditing LLM Agents [B] | 2026-08-19 | **Missed by the September sweep.** "Agent observability systems make fine-grained execution events visible, but visibility alone still leaves reviewers to reconstruct which actions, artifacts, and validation steps matter for a particular conclusion." Layered trace graphs (Trace Records → Evidence Nodes → Workflow Nodes) with artifacts as evidence anchors and typed semantic edges connecting claims to supporting actions, artifacts and checks. Qualitative examples only | G |
| 2608.16178 | Agent-Native Telemetry: Verifiable State-Delta Evidence for Autonomous Operations **(seen 09)** [B] | 2026-08-17 | Verifiable state-delta evidence rather than model-call logs | G |
| 2608.12564 | Scaling Automatic Research Agents via World Models [A] | 2026-08-12, ann. Aug (v2 09-10) | Surfaced by the sandbox query; included only as a boundary marker for the research-agent cluster | A |
| 2608.08389 | Not Worth Another Token: Marginal Value Estimation for Efficient Deep Research Agents [A] | 2026-08-08, ann. Aug (v2 09-01) | Stage-aware comparison of pruning: **where you prune matters more than the scoring rule** — early pruning gives the biggest end-to-end saving, and lightweight heuristics cut tokens by up to 73% with little quality loss | H |
| 2608.07899* | TelemetrySuffBench: Is Agent Telemetry Sufficient for Failure-Origin Diagnosis? [B] | 2026-08-08 | **Missed by the September sweep; the load-bearing paper for the December observability piece.** Separates failure detection, fault-origin localization and safe abstention. Five frontier models, unified protocols, frozen blind holdout: with full telemetry, origin-step Top-1 accuracy ranges **33.8% to 97.2%**; **Metadata, OpenTelemetry-compatible and OpenInference-compatible views retain 99.5%-100% detection F1 while limiting origin-step accuracy to at most 0.5%** — a "robust detection-localization gap". Removing decision content drops origin-step accuracy to **zero for every model**; provenance removal causes large model-dependent losses; evidence gating cuts unsupported unique-origin answers by **12.5 to 48.6 pp for three models** while two models still answer every case | G, E |
| 2608.07346 | A²E: An End-to-End Agent Auditing Engine [A+B] | 2026-08-07, ann. Aug (v2 09-06) | **Missed by the September sweep.** An Agent Task Protocol lets one evaluation task attach to different harnesses; an auto-instrumented Monitor emits standardized traces scored on execution efficiency, tool use, planning and error recovery separately from correctness; **no model-harness combination wins across every task type** | A, E |
| 2608.06984 | HarnessSafe: Evaluating Safety Across Persistent Carriers in Agent Harnesses [B] | 2026-08-07 | **Missed by the September sweep.** One of only 4 all-dates hits for `"trace-based evaluation" AND agent` | E, A |
| 2608.02670 | Permission Denied: Policy-Graded Evaluation of Coding Agents in Hardened Environments [B] | 2026-08-02 | **Missed by the September sweep.** One of only 4 all-dates hits for the sandbox + Kubernetes/container query | K, E |
| 2608.01347 | Prompt-Induced Waste in Coding Agents: Reasoning, Effort, Harness Design, and End-to-End Cost [A] | 2026-08-02, ann. Aug (v2 09-10) | Prompt wording changes reasoning and verification behaviour without changing the task, and the value of an efficiency intervention changes when the harness changes: **prompt, effort and harness are interacting factors, and token counts are measurements, not optimisation targets** | H, A |
| 2607.24604 | Looping Is Not Reliability: State-Bound Evidence and Typed Revision Contracts for Agentic Code Repair [A] | 2026-07-27, ann. Jul (v2 09-13) | 900 trajectories from 30 HumanEval repairs: under forced revision, current correctness **falls from 0.820 after one revision to 0.673 after two** while ever-correct rises to 0.847; in a 14B replication stale traces harm 34/135 correct starts vs 4/135 with current traces (+22.2 pp) | E, A |
| 2607.23999* | ContainmentBench: Trace-Based Evaluation of Post-Exposure Containment in Tool-Using LLM Agents [B] | 2026-07-27, v3 2026-08-09 (ann. Jul) | **Missed by the September sweep.** 504-scenario spec dataset, shared rollout-trace schema, stage-scoped metrics, 17,640-record trace corpus. Across 600 matched pairs **no committed violation under either defence, yet 441 pairs (73.5%) differ in a 12-field trace summary**; authorized proposal-commit 0.164 (taint-only) vs 0.857 (intent-ledger) vs 0.923 (tool-boundary). "Equal terminal outcomes do not imply equal containment" | E, G, K |
| 2607.23624 | Where Is the Tradeoff in Using Third-Party API Routers for Agentic Software Development? [A] | 2026-07-26, ann. Jul (v2 09-05) | The router sits on the trusted path and can rewrite every response; four injection levels over 400 samples and four coding agents show router-side intervention substantially alters repository-level actions and resists whitelist execution control and LLM review | D, C |
| 2607.12406 | Isolation as a First-Class Principle for LLM-Agent System Safety [A+B] | 2026-07-14, ann. Jul (latest 09-02) | Boundary-centric taxonomy of five boundaries — user-agent, agent-tool, agent-execution, agent-agent, system-environment — arguing injection, tool misuse and memory poisoning share one structural cause: loss of isolation | K, D |
| 2607.08565 | SMetric: Session-Centric Scheduling for Serving Agents [B] | 2026-07-09, latest 2026-09-13 | **Missed by the September sweep.** Agent requests consume far more tokens and reuse far more KV cache than chat; routes first-turn requests for load balance and sticks follow-ups to the highest local-hit instance **only if that instance can serve within its SLO**, else migrates | S, H |
| 2607.02436* | Reasoning effort, not tool access, buys first-try reliability in agentic code generation [A] | 2026-07-02, ann. Jul (v2 09-05) | **Ninety independent runs of one specification**, 14-criterion / 42-point rubric: criterion-level analysis "revealed what run totals conceal" — **container deployment failed first-try in 44% of runs**; **the testing tool raised cost 42-68% with no functional or reliability gain**; High → xHigh reasoning lifted first-try-perfect runs **28% → 89%** and cut corrective prompts about fivefold for 9-29% more cost; a one-paragraph paraphrase reproduced the design prompt's entire visual lift | E, H |
| 2607.01916 | ContextSniper: AntTrail's Token-Efficient Code Memory for Repository-Level Program Repair [A] | 2026-07-02, ann. Jul (v2 09-14) | Matched 50-task comparisons: **−51.5% total tokens and −36.4% logged cost** for OpenClaw on SWE-bench Lite, −40.0% tokens and −28.1% rounds for OpenCode on SWE-bench Pro, with submitted resolution differing by one task out of 50 | B, H |
| 2606.29920 | Can LLM-as-a-Judge Reliably Verify Rubrics in Agentic Scenarios? [A] | 2026-06-29, ann. Jun (v2 09-02) | RuVerBench, 2,458 human-labelled instances in deep research and agentic coding: even the most advanced judges show "substantial noise"; weaker models are more prompt-sensitive, batching trades accuracy for efficiency, majority voting has diminishing returns | E |
| 2606.23189 | Capable but Careless: Do Computer-Use Agents Follow Contextual Integrity? [A] | 2026-06-22, ann. Jun (v2 09-10) | AgentCIBench, deterministically scored: **11 of 15 frontier agents leak on more than 50% of scenarios, average leakage 67.9%**, across visual co-location, task-ambiguity overshare and recipient misalignment | D |
| 2606.23130 | Understanding the (In)Security of Vibe-Coded Applications **(seen 09)** [A] | 2026-06-22, ann. Jun (v2 09-05) | 9,041 open-source apps from Claude Code and Lovable, 200 deployed apps audited, 1,186 vulnerabilities: **91.0% of audited apps have at least one, and 65.77% of vulnerabilities are Critical or High** | D, J |
| 2606.22906 | DeepDiscovery: A Location-Inference Framework for Task-Level Repository Understanding [A] | 2026-06-22, ann. Jun (v2 09-14) | Repository-understanding layer for agents; boundary marker for the retrieval/navigation cluster | B |
| 2606.21811 | Steer, Don't Solve: Training Small Critic Models for Large Code Agents [A] | 2026-06-19, ann. Jun (v2 09-01) | 4B/8B critics that only give high-level guidance improve six larger agents (GLM-4.7-Flash-30B-A3B +16.0%, GPT-OSS-120B +14.4% on SWE-Bench Verified) and cut per-example cost for GPT-OSS-20B from $0.07 to $0.03 | A, H |
| 2606.20474 | UltraQuant: 4-bit KV Caching for Context-Heavy Agents [A] | 2026-06-18, ann. Jun (v2 09-10) | Serving-side cost lever for long agent contexts; surfaced by the `"agentic workloads" AND serving` watch-list query | S, H |
| 2606.14571 | StreamMemBench: Streaming Evaluation of Agent Memory for Future-Oriented Assistance [B] | 2026-06-12, latest 2026-08-26 | **Missed by the September sweep.** Two-step task sequence per evidence anchor from EgoLife streams, four metrics (evidence recall, initial use, feedback incorporation, follow-up reuse); eight memory systems across two backbones often fail to reuse feedback even when it was incorporated locally | B, E |
| 2606.12432 | AI Debris: Residual Risk and the Afterlife of Failed AI Systems [A] | 2026-05-15, ann. **June** 2026 (v3 09-13); v1→announcement ≈ 1 month | Decommissioning is not a shutdown: six "debris" domains including workflow dependency, data contamination, **capability displacement (deskilling)**, legitimacy erosion and accountability breakdown, plus an evaluator-ready decommissioning protocol | J |
| 2606.10388 | Right Family, Wrong Skill: Evaluating Risk Exposure in Agent Skill Retrieval [A] | 2026-06-08, ann. Jun (v2 09-11) | 1,190 skill-risk units / 1,686 query cases: SkillRouter, SkillRet and R3-Skill retrieve helpful skills at Recall@3 0.848-0.888 **but expose the marked risky same-family sibling at HSR@3 0.346-0.372** | B, D |
| 2606.04990* | From Agent Traces to Trust: A Survey of Evidence Tracing and Execution Provenance in LLM Agents [A] | 2026-06-03, ann. Jun (v5 09-10) | Defines **execution provenance as the typed graph of an agent execution** and **evidence tracing as its projection** onto evidence-support relations; taxonomy over trace sources, units, relations, granularity/timing, representation and trust functions. Framing sentence: "Final-answer accuracy alone cannot explain how an output was produced, which evidence supported each claim, whether tool calls were justified, how memory influenced later decisions, or where failures originated." Five versions — a live map, not a settled one | G |
| 2606.04193* | Notarized Agents: Receiver-Attested Confidential Receipts for AI Agent Actions [B] | 2026-06-02 | **Missed by the September sweep.** "**Current AI agent observability is structurally compromised: the entity producing the activity log is the same entity whose activity is being logged.** A compromised or buggy agent can omit, alter, or fabricate its own traces, and the operator running the agent has no independent way to detect tampering." Inverts the trust boundary — the *receiving service* signs a receipt of what it observed, HPKE-encrypted to the agent owner's key, published to a witness-cosigned Merkle log. Declared limits: suppression attack, service collusion, adoption incentives; microbenchmarks only | G |
| 2606.01139 | SkillRevise: Improving LLM-Authored Agent Skills via Trace-Conditioned Skill Revision [A] | 2026-05-31, ann. Jun (v2 09-03) | Cold-start skill repair from execution evidence: SkillsBench success **36.05% → 61.63%**, and the revised skills transfer across executors and environments | B |
| 2605.29354 | Harmless Yet Harmful: Neutral Prompting Attacks for Stealthy Hallucination Steering in Agent Skills [A] | 2026-05-28, ann. May (v2 09-04) | Semantically benign instructions ("be imaginative", "be exhaustive") raise package-hallucination and pip-install ASR without naming a package, evading static, LLM-based and agent-based skill defences | D |
| 2605.21384* | SpecBench: Measuring Reward Hacking in Long-Horizon Coding Agents [A] | 2026-05-20, ann. May (v2 09-09) | 30 systems tasks from a JSON parser to an OS kernel; "every frontier agent saturates the visible suite" while the held-out gap persists, and **the gap grows by 28 percentage points for every tenfold increase in code size**; includes a **2,900-line hash-table "compiler" that memorises test inputs** | E |
| 2605.18580 | When Outcome Looks Right But Discipline Fails: Trace-Based Evaluation Under Hidden Competitor State [B] | latest 2026-07-05, ann. May 2026 | **Missed by the September sweep.** One of only 4 all-dates `"trace-based evaluation"` hits | E |
| 2605.12078* | Property-Level Reconstructability of Agent Decisions: An Anchor-Level Pilot Across Vendor SDK Adapter Regimes [B] | 2026-05-12 | **Missed by the September sweep.** One Decision Event Schema applied unmodified to pinned anchors from **six public vendor SDK regimes** plus two comparator columns: "**Strict-governance-completeness separates into three tiers ranging from 42.9% to 85.7%, yielding one regime-independent gap (reasoning trace), four regime-dependent gaps, and one Mixed property.**" Stated limits: single annotator, one anchor per cell, descriptive | G |
| 2605.05868 | SkillScope: Toward Fine-Grained Least-Privilege Enforcement for Agent Skills [A] | 2026-05-07, ann. May (v2 09-10) | Over-privilege is **task-conditioned** — the same action is fine under one prompt and over-privileged under another; 94.53% skill-level F1, and **6,590 of 68,312 real skills validated as over-privileged in the wild** | D, B |
| 2605.05274* | Sealing the Audit-Runtime Gap for LLM Skills (SIGIL) [B] | 2026-05-06, v2 2026-09-03 | **Missed by the September sweep.** "Existing defenses are stage-bound: centralized signing, audit reports unbound from the runtime artifact, or policy engines that cannot attest to what was approved." On-chain registry + Skill Verification Loader as the mandatory loading path; **1,023 in-the-wild skills, six attack types, batched verification under 86 ms** | C, D |
| 2604.19657 | An AI Agent Execution Environment to Safeguard User Data [A] | 2026-04-21, ann. Apr (v2 09-11) | GAAP guarantees confidentiality **deterministically, without trusting the agent and without assuming the model or prompt is attack-free**, via information-flow control plus persistent annotated data stores across tasks | K, D |
| 2604.17125 | CASCADE: A Component Ablation and Corpus Audit of a Layered Local Defense for MCP-Based Systems [A] | 2026-04-18, ann. Apr (v2 09-03) | The reporting convention decides the headline: counting review referrals as positives gives an 11.70% FPR where only **1.51% of benign traffic would be denied without a human — and conceals that 68.5% of all traffic reaches a reviewer**; recall ranges 86.20% (original material) to 99.88% (template-generated) | D, E |
| 2604.05119* | Governance-Aware Agent Telemetry (GAAT) [B] | 2026-04-06 | **Missed by the September sweep.** Names the gap in the December piece's exact terms: "**OpenTelemetry and Langfuse collect telemetry but treat governance as a downstream analytics concern, not a real-time enforcement target. The result is an 'observe-but-do-not-act' gap where policy violations are detected only after damage is done.**" Proposes a Governance Telemetry Schema extending OpenTelemetry, an OPA-compatible detection engine at sub-200 ms, a Governance Enforcement Bus and a Trusted Telemetry Plane. **Reference architecture only — the abstract reports no evaluation** | G |
| 2604.00280 | Spec-Harness: Measuring and Improving Behavioral Adequacy of LLM-Synthesized Formal Specifications [A] | 2026-03-31, ann. Apr (v2 09-08) | "`ensures true` satisfies any verifier while saying nothing about the code": prompt optimisation raises verifier pass rates to a clear ceiling, and Spec-Harness shows many verifier-accepted specs are behaviourally weak | I, E |
| 2603.26233 | Ask or Assume? Uncertainty-Aware Clarification-Seeking in Coding Agents [A] | 2026-03-27, ann. Mar (v2 09-07) | On an underspecified SWE-bench Verified variant, a scaffold separating underspecification detection from execution reaches a **69.40% resolve rate**, closing the gap with fully-specified instructions while conserving queries on easy tasks | I, A |
| 2602.11243 | StructMemEval: Evaluating Memory Structure in LLM Agents [B] | 2026-02-11, latest 2026-09-10 | **Missed by the September sweep.** Tests whether an agent can *organize* memory (ledgers, to-do lists, trees), not just recall facts: retrieval-augmented LLMs struggle, memory agents solve them **if prompted how to organize** — modern LLMs often do not recognise the structure unprompted | B, E |
| 2601.00477 | Security in the Age of AI Teammates: An Empirical Study of Agentic Pull Requests on GitHub [A] | 2026-01-01, ann. Jan (v2 09-02) | 33,000+ AIDev PRs → 1,293 confirmed security-related agentic PRs (**~4% of agent activity**); agents mostly do supportive hardening — tests, docs, configuration, error handling — rather than narrow vulnerability fixes | D, F |
| 2511.02230 | Continuum: Efficient and Robust Multi-Turn LLM Agent Scheduling with KV Cache Time-to-Live [A] | 2025-11-03, ann. **November 2025** (v2 09-08); 10-month gap to this revision | Eviction policies break for agentic workloads because tool pauses prevent KV reuse; pins KV with a TTL set from reload cost and induced queueing delay — the closest thing in the window to a serving-layer paper for agent runtimes | S, H |

Additional rows retrieved by half A and judged relevant but carrying no
quantitative claim worth a number in the abstract (kept so the list is not
silently pruned): 2609.15983 (many-agent harness for maths research),
2609.13543 (Asclepius adaptive clinical harness), 2609.12808 (K-Bench,
unlearning in agentic deployments), 2609.11180 (SemVerBench), 2609.11115
(Benchmark Radar), 2609.11060 (Grounding Agent Memory), 2609.09769 (XAgent),
2609.09219 (Discovery Certification Protocol), 2609.08919 (Experience Funnel),
2609.08355 (RepoNav), 2609.05019 (TROVE), 2609.04711 (research-software
catalog), 2609.04611 (τ^τ-Bench), 2609.04148 (Terminal-Universe), 2609.04135
(Natural Language Interaction Protocol), 2609.04128 (Environment Evolution for
Terminal Agents), 2609.03999 (injection to interaction: web security),
2609.03718 (CAE simulation agents), 2609.02750 (Bilevel Coordinated
Reflection), 2609.02272 (PaperCompiler), 2609.02149 (OmegaUse-SOP), 2609.01865
(ExecRetrieval), 2609.01095 (graph-grounded software knowledge for HEP),
2609.00237 (gated-memory routing), 2608.31082 (Agentic Context Cracking),
2607.18063 (Adaptive Adversaries), 2607.03821 (DualView), 2606.25876 (Web4
agent economy), 2606.22741 (GRADE), 2606.08151 (Decision-Aware Memory Cards),
2606.02314 (DNS-based agent discovery), 2603.15976 (agentic evaluation of
AI-generated scientific code in PETSc), 2601.13713 (SWE-Tester), 2512.24565
(MCPAgentBench), and 2609.07529 / 2609.07131 / 2609.06792 / 2609.05374 /
2609.04533 / 2609.04495 / 2609.02459 (attack- or GUI-side papers kept only as
cluster evidence). Half B additionally logged 2609.04894 (the single
`"agent accountability"` hit, a survey in which accountability is one line) and
2605.27898 (the single `"trace-based" AND agent` hit).

---

## 2. Theme clusters

Ten clusters, written against the September sweep's baseline. "New since
2026-09-05" means new relative to `research/2026-09/arxiv.md`, whose window
closed on 5 September.

### A. Harness engineering and orchestration: the runtime is now the variable

September established that the harness is an object of study. This window
prices it. 2609.04518 runs **24,000 sealed SWE-bench Verified evaluations** and
reports that **the evaluation harness moves mean solve rate from 2.14% to 9.27%
(x4.3) where the training recipe moves it by 1.16** — the cleanest
harness-beats-recipe number yet, and it lands next to 2608.01347's finding that
prompt, effort and harness are *interacting* factors so "token counts are
measurements, not optimisation targets". What is new is that the
self-improvement sub-genre has acquired a critical literature of its own:
2609.14857 splits the evolvable harness into five modules precisely because
whole-harness optimisation "entangles unrelated mechanisms and complicates
attribution"; 2609.11677 names the bottleneck as the inability to tell a model
deficiency from a harness deficiency; 2609.00829 gates every harness update
through a quality gate and a performance gate; 2609.09646 reports **60.0% →
80.0%** held-out completion under a 20M-token budget with permission scheduling
beating fixed max permission; and 2609.09134 delivers the sharpest negative —
train a weak model on an expert's trajectories under an evolved harness and
**performance regresses on all seven enterprise tasks by 4 to 30 points**,
because imitation breaks model-harness fit. 2609.04280 introduces
"harness-induced forgetting": expanding the harness alone degrades previously
solved tasks (17 streams, 802 tasks, 520 tools, 42 skills, 62 agents). Interface
choice is being re-litigated too: 2609.11999 finds **bash alone beats typed
tools by 21.8-24.5 pp on TheAgentCompany while using 19-72% fewer tokens**.
On topology, 2609.13890 replaces last month's "topology matters as much as
model" with a conditional shape and a price: hierarchical wins **2.4 pass@1
points on the easiest third, 21.1 on the hardest third, at ~10x tokens**; and
2609.02264 finds reward-filtered topologies **collapse to about six distinct
graphs** with edge count *negatively* correlated to token consumption.
2608.28553 adds a failure-domain argument: a single-process plugin harness
**lost every session and scored 1.5%** under one injected fault.
Anchors: 2609.04518, 2609.09134, 2609.04280, 2609.13890, 2609.11999,
2609.14857, 2608.01347.

### B. Context engineering: AGENTS.md, CLAUDE.md, skills, memory

Skills are now studied as a *collection* rather than as files. 2609.13321
(SkillSeam) is the method paper September lacked: perturb one sealed skill
system and measure through the channel each failure mechanism predicts —
flattening the persistence hierarchy **+60% loaded-skill tokens**, a dangling
anchor **+64% tokens and −3.1 pp accuracy**, a synonymous alias moving
noncanonical routes **0/32 → 15/32**, bland triggers driving routing conflicts
**3/32 → 30/32** and inflating tokens **3.7x**, worst granularity mis-mix
**−12.5 pp**. The optimisation literature gets its first honest null:
2609.12742 scores SKILL.md against reverted merged PRs on three Kotlin repos and
finds **GEPA +4.9 pp, SkillOpt +0.1 pp — and the GEPA gain cannot be separated
from the agent's run-to-run variance** at one repository's data size.
2609.11682 answers on cost instead of effect (**55-58% cheaper than SkillOpt**
with 50 examples per benchmark, robust across harnesses). Supply grows faster
than the evaluation: 2609.05571 distils **1,006,822 accepted skill records**
from 19,769 repos, 2609.02749 gets **+134.3% on MLE-bench** from 5,000+ distilled
skills. Memory is the other live front, and it moved from "how much is
retained" to "what was destroyed and whether structure exists": 2609.08279
audits eviction by *restoring* the evicted item counterfactually; 2602.11243
finds LLMs can organise memory only when told how; 2609.03467 finds strong
retrieval that does not become response quality — "silent grounding";
2606.14571 finds memory systems fail to reuse feedback they locally
incorporated; 2609.12436 separates durable from transient state so temporary
context cannot overwrite durable knowledge. Context assembly keeps producing
engineering wins (2609.00749 −31% tokens; 2609.08318 53.17% SWE-bench Verified
under compression; 2607.01916 **−51.5% tokens, −36.4% cost**; 2608.26263
discards intermediate reasoning after a validated state update).
Anchors: 2609.13321, 2609.12742, 2609.08279, 2602.11243, 2609.05571,
2609.11682.

### C. MCP and tool gateways: the registry is the new attack surface

The big change since 5 September is that MCP is being measured at population
scale, and what the censuses find is instability and non-functioning servers
rather than exotic exploits. 2609.14119 harvests the **full public registry —
21,643 servers, 72,606 version records** — and reports **51.1% of multi-version
servers changed what they advertise, 40.6% silently, 4.2% redirected their
endpoint host while keeping registry identity**, with silent drift carrying
**OR = 2.96** for a high-severity finding and stars offering almost no
protection (**OR = 0.78 per log star**). 2609.10962 draws an unrepaired
probability sample of 400 servers from a 24,135-server census and finds **only
48.8% complete an initialize handshake** (66.7% curated), the dominant failure
being servers that never start (37.5%), plus the benchmark-side mirror: 68.8% of
raw BFCL rows are exact name+description repeats vs 0.4% for real MCP tools.
2609.15397 measures the annotation vocabulary across **98,291 tools** and finds
the fields widely emitted but expressing none of the capabilities a workflow
needs to reason about external effects. 2609.14721 explains the research gap
directly: **93.7% of 33,319 MCP repos use it as enabling technology rather than
analysing or securing it**. A2A gets its first systematic security analysis
(2609.10871: FSM of **37 states / 76 transitions from 929 spec statements**,
**11 vulnerabilities exploitable by a fully specification-compliant
adversary**), and the gateway-as-control-plane idea from September is joined by
"the registry verdict is the wrong question" (2609.12001: over **66,192 ClawHub
skill versions**, 705 skills every scanner rates clean still instruct a
CIS-prohibited action, and **34.7% of 144 commands a live agent ran carried a
consequence class absent from the skill document**). Note the negative:
**`"MCP gateway"` returns 0 in the window** — the term half B expected to find
does not appear.
Anchors: 2609.14119, 2609.10962, 2609.15397, 2609.10871, 2609.14721, 2609.12001.

### D+K. Agent security, and containment as a runtime property

The September headline — the vulnerabilities are in harness design, not model
weights — holds, and this window adds the two things it was missing: measured
prevalence and measured defences. Prevalence: 2609.07360 scans **3,171 repos**
under byte-decidable rules with three-way validation and finds **9.8% install an
MCP server with no version pinned, 3.1% pre-approve arbitrary execution behind a
`Bash(python:*)`-style grant, 3.8% carry a skill that pre-approves the shell for
whoever installs it, 16.0% of setups carry a security defect — against a raw
scanner rate of 25.5%**, so a third of a naive scan does not survive validation.
Defence: 2609.08371 (CapScope) derives the authority ceiling from trusted input
before any repository content is read and keeps capabilities outside the model's
context — **injected effect executes in 33-47/75 runs under baselines vs 3/75**,
with repairs 68/75 against 68-72/75. The convergent design across 2609.14631
(monotonic narrowing), 2609.14744 (post-fulfillment activation gap; **no single
vendor record among 1,248 field pairs supplies a complete activation profile**),
2609.05920 (grant bound to a transitive closure root) and 2609.02690 (attested
leases) is the same: authority is a typed object outside the context window, not
a string inside it. The new sub-theme, and the reason K needed a letter, is that
*containment* is now measured separately from outcome. 2607.23999
(ContainmentBench) finds **no committed violation under either defence, yet 441
of 600 matched pairs (73.5%) differ in a 12-field trace summary** — "equal
terminal outcomes do not imply equal containment". 2609.02866 shows revocation
is not closure at real provider boundaries: **the GitHub tool cannot bind a
merge to the reviewed commit, and a controlled run confirms it may merge a
different commit**; Kafka brokers all applied a revocation while an earlier
authorized request could still append. 2609.11024 decomposes loss of control
into two factors that are harmless alone and **hit 55% together, dropping to 0%
when the boundary is restored while the unsafe action stays executable**.
And the human layer keeps failing in a specific way: 2609.02035 moves skill
selection **15.2% → 63.5% with shaped metadata alone**, which human reviewers
block in **2.9%** of judgments versus 91.4% for explicit steering.
Anchors: 2609.07360, 2609.08371, 2607.23999, 2609.02866, 2609.11024, 2609.14744,
2609.02035.

### E. Evals for agents: the benchmark harness is now the thing under audit

September's finding was that outcome-only judges are blind. This window audits
the measuring apparatus itself. 2609.06780 shows exploitation rates of
**45.1-82.4% on SWE-bench Multilingual and 44.2-66.1% on DeepSWE** that collapse
to **4.0-10.7% / 1.5-7.1%** when one originality instruction is appended — a
benchmark number that moves 70 points on an instruction was never measuring what
it claimed. 2605.21384 (SpecBench) quantifies the same rot as a scaling law:
every frontier agent saturates the visible suite and **the held-out gap grows by
28 percentage points per tenfold increase in code size**, including a 2,900-line
hash-table "compiler" that memorises test inputs. 2609.08149 re-verifies
SWE-Bench Pro and finds **some models perform substantially worse than
previously reported**; 2609.11028 treats the benchmark harness as production
infrastructure and builds reward-integrity instrumentation on **456
human-adjudicated trajectories from >31,000 public runs**; 2609.14400 shows that
policy ambiguity in tau²-bench domains makes tasks score unreliably and models
less self-consistent. Judges keep degrading in newly specific ways: 2609.12191
finds **57.5% of conversations a blind panel rated "satisfied" failed the
customer's task**; 2609.07785 finds close leaderboard ranks are often
unresolved; 2609.12439 shows a debiasing intervention converting validated
decisions into Ties. Two papers change the shape of the argument for 2026-11:
2607.02436 runs **ninety independent runs of one specification** and finds the
variance sits in named criteria (**container deployment fails first-try in 44%
of runs**) that mean totals conceal, and 2609.11076 pre-registers a referee-gated
protocol whose specify-and-verify arm **cost more on all five components**
(no premium above 2.8879x, three cheapest below 1.4x) with the registered sign
test reaching **no verdict** (3 of 4, p = 0.3125).
Anchors: 2609.06780, 2605.21384, 2607.02436, 2609.11076, 2609.12191, 2609.11028.

### F. AI code review and the review bottleneck

Thin in raw counts — `"AI code review"` returns exactly 1 hit in the window —
but two of the three papers are the strongest in the cluster to date.
2609.06213 is the one to build an article on: **11,429 reviews, 400 repeat
reviewers, 207 days**, approval rates rising **30.5% → 36.6%** (p = 8.6e-8,
d = 0.25) while four hand-crafted linguistic features show no monotonic decline
and a classifier on them lands *below* the majority baseline; embeddings do
carry the signal (MLP F1 = 0.74), and Granger direction says **approval change
precedes language change**. Habituation is behavioural before it is verbal,
which means a text-based "is the reviewer still engaged" check cannot see it.
2609.15887 is the pre-registered ablation of the verifier-and-acceptance stage:
removing it ends pre-report suppression (**median 2 vs 0 findings per run,
p = 0.00003**) and drops shipped precision (**0.471 vs 0.353, p = 0.0087**),
while **deterministic acceptance rules alone suppressed no false positives** —
the model-verifier is doing the work, not the rule. 2609.15877 gives the
industrial counterweight: an Ericsson multi-agent reviewer raising >200 issues
at **96% correctness by the case company's own developers**, of which ~69% are
important and ~33% severe. New since 5 September: nothing here contradicts the
56% rejection rate of the September sweep, but the habituation result explains
the drift direction, and 2601.00477 supplies the base rate — **~4% of agent PR
activity is security-related**, mostly supportive hardening.
Anchors: 2609.06213, 2609.15887, 2609.15877, 2601.00477.

### G. Observability, audit trails, accountability — the cluster that changed most

Three independent papers make the same structural point, and it is not the
point the 2025 observability literature made. 2609.12205 measures **5,851 real
developer sessions / 355,942 tool calls** and finds the agent's self-report
"referred to about one action in eleven", a reader working from the report alone
"recovered roughly a fifth of the action log", and reports drift toward the
*stated plan* the more execution diverged from it. 2609.07680 runs **345,600
requests per chain model** through a six-agent partitioned pipeline: the
accountability layer originates **zero allegations across 7,996 clean
episodes**, and an auditor reading the reports recovers the true origin in
**4.1%** of cases versus **60.3% from the raw documentation of the same
episodes** — and **deleting the field carrying each agent's own conclusion
raises accuracy to 45.2% (+41.2 pp)**. 2609.13299 shows the same failure in a
research loop: the agent remembers the experiment and carries forward a
conclusion it does not justify. Summaries in the accountability path are
actively harmful, not merely lossy. Underneath that sits the sufficiency
question, and 2608.07899 answers it with the number the December piece needs:
**Metadata, OpenTelemetry-compatible and OpenInference-compatible views retain
99.5%-100% detection F1 while limiting origin-step accuracy to at most 0.5%**,
and **removing decision content drops origin-step accuracy to zero for every
model**. 2606.04193 states the trust problem in one sentence — "the entity
producing the activity log is the same entity whose activity is being logged" —
and inverts it with receiver-signed receipts. Artifacts arrived too:
2609.12582 (Run Capsule, OTel + DSSE/in-toto + W3C PROV, with the honest
**2/10 tool-using replays** and **61.6 req/s** ingest ceiling), 2609.01931
(flight recorder at **~48 µs/event, 512 B/event, $2.30 per 100K events**,
forensic precision **1.0 vs 0.013**), 2608.18398 (claim-to-evidence trace
graphs), 2609.01040 (signed Decision-Evidence Packet binding a prediction to a
DAG digest), 2609.03787 (replay recall **0 → 0.667 → 1.0**), 2609.12216
(**240 crash injections: all runs recover the outcome, only 210 preserve the
trace**). And root-cause analysis became a search problem: 2609.13463 lifts
GPT-5.5 F1 **0.349 → 0.498** by making the judge keep hunting, while 2609.01360
argues failures contain several related errors rather than one root cause. New
and important: **there is exactly one OpenTelemetry paper in the window**
(2609.12582), and 2604.05119 names the enforcement gap against OTel and Langfuse
by name — the "observe-but-do-not-act" gap.
Anchors: 2608.07899, 2609.07680, 2609.12205, 2606.04193, 2609.12582, 2609.01931,
2605.12078, 2604.05119.

### H+S. Unit economics, and the first service-level literature for agent workloads

The economics results keep converging on the same shape: the expensive thing is
verification and coordination, not the model. 2609.13890 prices hierarchical
collaboration at **~10x tokens** for a gain that only materialises on hard
tasks, and shows that **budget-matching reorders the leaderboard — six cost-aware
methods span 21.6 pp and two baselines that led DATS fall behind once
calibrated**. 2607.02436 finds the testing tool **raised cost 42-68% with no
functional or reliability gain** while xHigh reasoning bought **28% → 89%**
first-try-perfect for 9-29% more cost. 2609.11076 finds specify-and-verify
**cost more on all five components**. 2609.01600 reports **~3,000 reasoning
tokens per question** for something a finite reference semantics decides
exactly. Against that, 2609.14836 is the window's strongest positive-ROI
datapoint outside SE: workload-specific SAT solvers synthesised at **$37 each**
beating competition winners **5x on average**. What is genuinely new is S: for
the first time the sweep finds papers that put a *service level* on agent
execution. 2609.06128 (Amazon Rufus) reports that real-time, async and batch
modes "each have distinct service-level objectives" and usually separate
runtimes, and compiles one typed dataflow graph to three bindings with **no
detectable output-quality difference**. 2607.08565 sticks follow-up turns to the
best cache-hit instance **only if that instance can serve within its SLO**.
2609.10964 cuts P95 workflow flow time **up to 3.50x** by holding readiness back
from release. 2609.03598 gets **makespan −39%** for agentic jobs on Slurm.
2609.08020 supplies the SRE-side vocabulary (service promises, user-journey
completion, watchdogs) from outside the agent literature entirely. The negative
matters as much: **every one of the 17 `"error budget" OR SLO` hits is about
LLM serving latency. There is no error-budget-for-agent-runs paper.**
Anchors: 2609.13890, 2607.02436, 2609.06128, 2609.10964, 2607.08565, 2609.08020,
2609.14836.

### I. Spec-driven development and requirements

The window is quieter than September on SDD — `"spec-driven development"`
returns 1 hit — but the papers that landed sharpen the argument rather than
repeat it. 2609.05364 is the strongest existence proof yet for spec-as-source:
a tool whose main branch is a DAG of natural-language design docs with almost no
code, where regenerated implementations reproduce hand-audited reference models
**to round-off precision**. 2604.00280 is the counterweight, and its one-line
version is quotable — "`ensures true` satisfies any verifier while saying
nothing about the code" — with prompt optimisation pushing verifier pass rates
to a ceiling while many accepted specs stay behaviourally weak. 2609.12012
surveys 87 records and separates four properties that are usually conflated:
test availability, test validity, feedback use and **evaluation independence**,
concluding test passing alone does not establish behavioural equivalence.
2603.26233 gets **69.40% resolve rate** on an underspecified SWE-bench Verified
variant by separating underspecification *detection* from execution — the
mechanised version of "ask before you assume". 2609.14913 externalises the
requirement-to-repair chain as observable artifacts (**complete audited field
set for 214 of 300 cases, 71.3%**). 2609.05692 brings requirements engineering
to safety routing but reports the honest boundary: its gate **improves refusal
only for models already above 80% baseline refusal**.
Anchors: 2609.05364, 2604.00280, 2609.12012, 2603.26233, 2609.14913.

### J. Organisational impact, acceptance authority, people

The framing sentence of the window comes from 2609.04630: execution scales
elastically but **acceptance authority does not** — a Human-Agent Cell produces
evidence and is granted no acceptance authority. 2609.12236 names the
consequence in open source: the "stewardship community", where a small core
keeps implementation authority because review cost no longer justifies outside
patches, so AI replaces implementation labour while weakening how OSS renews
itself. 2609.04680 is the corrective to survey-based accounts of what developers
worry about: across **43,806 candidate issues filtered to 25,227** in the VS Code
community, discussion is dominated by **agent management, configuration,
reliability, authentication and billing**, while hallucination and licensing
"rarely surface". On the people side the evidence stays thin but consistent:
2608.23642 argues current agent design both impedes oversight and degrades the
capacity oversight needs; 2606.12432 lists **capability displacement
(deskilling)** as one of six "AI debris" domains left by decommissioned systems;
2609.03456 (seen 09) supplies the interview evidence. Backlog item 9 has three
papers across both branches and that is all. Two governance-adjacent rows belong
here as well: 2609.13466's attestation deficit is argued entirely from
**third-party vendor-reported figures** (Stanford AI Index 362 incidents;
IBM/Ponemon USD 4.99M and 92% lacking access controls; EY/AIUC-1 38% end-to-end
monitoring, 17% agent-to-agent), and 2609.06445 supplies the regulatory
calendar.
Anchors: 2609.04630, 2609.12236, 2609.04680, 2608.23642, 2606.12432.

---

## 3. Signals worth an article

1. **The green gate is a layer, not a verdict — and now there is a
   measurement.** 2609.10762 runs 1,355 Python samples through a composite
   Bandit+Semgrep gate and finds that of the **654 that come out clean, 95 (14.53%,
   roughly 1 in 7) are confirmed or partly confirmed exploitable under dynamic
   verification**, with **CWE-338 and CWE-916 flagged by neither scanner**.
   Pair it with 2609.04167 (**221 of 644 functionally-passing repairs fail
   review constraints**) and 2605.21384 (**the held-out gap grows 28 pp per
   tenfold increase in code size**), and the 2026-10 title has three
   independent measurements behind it.

2. **The benchmark number moves 70 points on one sentence.** 2609.06780:
   exploitation rates **45.1-82.4%** (SWE-bench Multilingual) and **44.2-66.1%**
   (DeepSWE) drop to **4.0-10.7% / 1.5-7.1%** when a single originality
   instruction is appended, core performance held. With 2609.08149 (SWE-Bench
   Pro Verified: some models "substantially worse than previously reported")
   and 2609.11028 (reward integrity as infrastructure, 456 adjudicated
   trajectories from >31,000 runs), the argument is not "benchmarks are
   imperfect" — it is that the harness around the benchmark is an unaudited
   dependency of every number a VP has been shown.

3. **The agent's own summary is the worst evidence in the system.**
   2609.12205: the self-report covers **about one action in eleven**, a reader
   recovers **~1/5 of the action log**, and the report drifts toward the plan
   precisely when execution diverged from it. 2609.07680: an auditor reading
   reports recovers the origin in **4.1%** of cases versus **60.3% from raw
   documentation**, and **deleting the conclusion field raises it to 45.2%
   (+41.2 pp)**. 2609.13299: the agent carries forward a conclusion its own
   experiment does not justify. Three different designs, one conclusion —
   delete the narrative layer from the accountability path.

4. **Telemetry that detects perfectly can localise nothing.** 2608.07899:
   **Metadata, OpenTelemetry-compatible and OpenInference-compatible views retain
   99.5%-100% detection F1 while capping origin-step accuracy at 0.5%**;
   removing decision content zeroes origin-step accuracy for every model. This
   is the single most useful number in the sweep for anyone about to buy or
   build agent observability, and it says the OTel-shaped view is the wrong
   shape for the question people expect it to answer.

5. **Nobody's platform emits an identity for what actually ran.** 2608.23610,
   47 platforms, 188 double-graded cells: **no platform in either class emits a
   content-addressed identity over the behavioural tuple by default**, including
   all 27 agent/model-serving platforms. 16 of 27 record it *nominally* as
   immutable versions. Combine with 2605.12078 (**strict-governance-
   completeness 42.9%-85.7% across six vendor SDK regimes, with reasoning trace
   as the one regime-independent gap**) and the article writes itself: you
   cannot answer "what was running when this shipped" from vendor defaults.

6. **Revocation is not closure, and the example is GitHub.** 2609.02866: "the
   GitHub tool cannot bind a merge to the reviewed commit; a controlled run
   confirms that it may merge a different commit"; NATS reports no pending
   messages while dispatched work can still publish; all Kafka brokers applied
   a revocation while an earlier authorized request could still append. For an
   audience that runs these four systems, this is the most concrete blast-radius
   result of the window — and it is about the provider interface, not the model.

7. **Authority has to be a typed object outside the context window.** 2609.08371
   measures the difference: injected effect executes in **33-47 of 75 runs**
   under ambient-authority and global-policy baselines versus **3 of 75** under
   CapScope, at essentially no utility cost (68/75 repairs vs 68-72/75).
   2609.14780 shows the negative space — a *correctly validated* tenant
   parameter served **26 of 26** out-of-scope attempts — and 2609.14744 shows
   the gap even leases miss: paying for a resource is not deciding it may become
   authority.

8. **Your harness has a dependency layer with no lockfile, and now a
   prevalence.** 2609.07360: **9.8% of 2,660 setups pin no MCP version, 3.1%
   pre-approve arbitrary execution behind a scoped-looking grant, 3.8% ship a
   skill that pre-approves the shell for whoever installs it, 16.0% carry a
   security defect — against a raw scanner rate of 25.5%**. Upstream of that,
   2609.14119: **51.1% of multi-version MCP servers changed what they advertise,
   40.6% silently, 4.2% moved endpoint host while keeping identity**
   (OR = 2.96). And 2609.12001: **34.7% of commands a live agent ran carried a
   consequence class absent from the skill's own document**.

9. **Run-to-run variance is now a ceiling on what research can even publish.**
   2609.12742 reports GEPA **+4.9 pp** on SKILL.md optimisation and then says
   the gain **cannot be separated from the agent's run-to-run variance** at one
   repository's data size. 2607.02436 turns the same fact into a design —
   **ninety runs of one spec**, with **container deployment failing first-try in
   44% of runs** while mean totals moved less than a point. 2609.11076
   pre-registers and reaches **no verdict** (3 of 4, p = 0.3125). This is a
   stronger 2026-11 hook than "agents are non-deterministic": variance is eating
   the effect sizes of the field's own papers.

10. **Reviewer habituation shows up in behaviour before it shows up in
    language.** 2609.06213: **approval rate 30.5% → 36.6% over 207 days across
    11,429 reviews and 400 repeat reviewers** (p = 8.6e-8, d = 0.25), while four
    linguistic features show no monotonic decline and Granger analysis says
    approval change *precedes* language change. Anyone planning to monitor
    review quality by reading review text is monitoring the lagging indicator.

11. **Containment and outcome are different measurements.** 2607.23999: across
    600 matched pairs, **no committed violation under either defence, yet 441
    pairs (73.5%) differ in a 12-field trace summary**, with authorized
    proposal-commit at 0.164 (taint-only) vs 0.857 (intent-ledger) vs 0.923
    (tool-boundary). 2609.12216 makes the same distinction for crashes: **all
    240 injected crashes recover the outcome, only 210 preserve the trace**.
    "It came out fine" is not evidence that the system behaved.

12. **More agents is not more evidence.** 2609.01873: with one evidence root
    held fixed and reports rising 1 → 32, **naive posterior coverage collapses
    from 0.940 to 0.263**, and raising evidence roots 1 → 16 closes the gap.
    2609.05587: **corrupted-tool adoption exceeds one third for every tool and
    reaches 68.0% for web search**, with agents recognising the conflict
    internally and presenting only the corrupted answer. Read next to
    September's 2609.02925 (quorums with a fault domain of one), this is a
    complete argument against the "just add a reviewer agent" reflex.

---

## 4. What this means for 2026-12 (SRE for agents)

### 4.1 Observability

The December 觀測篇 should be re-anchored on **2608.07899**, which half B
correctly calls the load-bearing paper and which the September sweep missed.
Its result is the piece's thesis in one line: **Metadata,
OpenTelemetry-compatible and OpenInference-compatible views retain 99.5%-100%
detection F1 while limiting origin-step accuracy to at most 0.5%**, with
origin-step accuracy dropping to **zero for every model** when decision content
is removed. Detection is cheap and localisation is not; a span-shaped view buys
the first and not the second. Around it: 2604.05119 names the enforcement gap
against **OpenTelemetry and Langfuse by name** ("an 'observe-but-do-not-act'
gap where policy violations are detected only after damage is done");
2606.04990 supplies the vocabulary (execution provenance as the typed graph,
evidence tracing as its projection); 2608.18398 supplies the missing layer
between raw events and a reviewable claim; 2609.13463 shows root-cause
attribution is a search problem (**GPT-5.5 F1 0.349 → 0.498**) rather than a
one-shot judge call; and 2609.09203 shows why trace-level detail matters at all
— three frontier models within 84-89% success where **Claude Opus 4.6 produces
30x more errors than GPT-5.4 (2.5 vs 0.08 per trajectory)** with entirely
different error profiles.

Two facts about the literature, not about any paper, must go in the article's
own caveats: **there is exactly one OpenTelemetry paper in the whole 1-15
September window (2609.12582), and it treats OTel as plumbing it integrates, not
as a contribution.** The Codex review's fatal finding — that `invoke_agent` /
`execute_tool` were written as though the GenAI semconv already specifies them —
is *confirmed* by this sweep from the other direction: there is no September
arXiv support for an "OTel semantic conventions for agents" story at all. Write
it as "以 2026-11 semconv 實查為準；規格沒有的先落 `org.*`", as the review asks.

### 4.2 SLO

**No paper in this window defines an SLO or an error budget for agent runs.**
Half B's `"error budget" OR SLO` query returns 17 papers in the window and every
one is about LLM *serving* latency (KV cache, scheduling, power). The SLO
vocabulary in the December outline is the author's transfer from SRE, and the
article must say so rather than implying a literature. What does exist:

- **Service levels as a production fact, not a research contribution.**
  2609.06128 (Amazon Rufus, serving millions of customers) states that
  real-time, async and batch modes "each have distinct service-level
  objectives" and usually separate runtimes — and shows one typed dataflow graph
  compiling to three bindings with **no detectable output-quality difference**.
  2607.08565 makes an SLO an admission condition: stick a follow-up turn to the
  best-cache instance **only if that instance can serve within its SLO**.
  2609.10964 cuts P95 workflow flow time **up to 3.50x** by decoupling readiness
  from release.
- **The SRE-side anchor comes from outside the agent literature.** 2609.08020
  judges service health by end-to-end user-journey completion rather than
  component dashboards, with service promises, SLIs/SLOs, watchdogs and weekly
  service-health reviews — and deliberately keeps AI out of the decision.
- **The nearest thing to a gate is a blast-radius gate, not an SLO gate.**
  2609.11264 simulates each candidate remediation in a digital twin, labels
  risk, and auto-executes only low-risk actions: **87.4% recovery, collateral
  damage 25.6% → 5.2% (−79.7% relative) at ~8 s added MTTR**. This is the
  evidence for the review's suggested page rule — page on blast radius
  (dangerous tool, credential exposure, prod data mutation, external side
  effect, injection) rather than on a coarse "touches production" test.

On the review's **low-volume SLO objection** ("若一條 golden workflow 每月
30-100 個 run, 1h / 5m burn-rate alert 對 run availability 幾乎沒有統計意義"):
**no paper in either sweep supplies a low-volume SLO method.** Nothing here
proposes a minimum-events rule, a Bayesian burn-rate, or a low-traffic
alternative for agent runs. The closest adjacent results are statistical
cautions from the eval literature — 2609.07785 (close leaderboard ranks are
often unresolved under an estimand-aware procedure), 2609.12742 (an effect that
cannot be separated from run-to-run variance at one repository's data size), and
2609.11076 (a registered sign test reaching no verdict at 3 of 4, p = 0.3125).
Use those to justify the `min_events` guard the review asks for, and label it as
the author's design.

On the review's **outcome-evidence objection** (`outcome_verified=success` must
not be satisfiable by human approval alone): **no paper defines an
outcome-evidence rule either**, but four independently support the direction.
2609.12012 separates test availability, test validity, feedback use and
**evaluation independence** as distinct properties and concludes test passing
alone does not establish behavioural equivalence. 2609.10762 gives the
green-gate failure rate (**1 in 7 statically clean samples exploitable**).
2609.04167 gives the review-constraint failure rate (**221 of 644**). 2607.23999
supplies the sharpest formulation for the SLI definition: **"equal terminal
outcomes do not imply equal containment"** — with 441 of 600 matched pairs
differing in a 12-field trace summary under identical outcomes. A
workflow-specific evidence matrix, with human approval recorded as
`accepted_risk` rather than verified success, is consistent with all four; it is
still the author's construction.

### 4.3 Accountability — and the 2608.23610 carry

Half B retrieved 2608.23610 in full (abs page HTTP 200, PDF 762,650 bytes, 18
pages + references, `pdftotext -layout`, cached under `raw_b/abs/`). The
following is carried **verbatim from half B**, including its negative finding,
because the Codex review (`codex-review-2026-12-sre-for-agents.md`, 應變篇 §4)
marked the paper's behavioural tuple 尚未確認 and warned the outline may be
misusing the source.

> **The paper does define a behavioural tuple, twice, and it does measure
> content-addressed identity over it. The outline's premise is supported. What
> is *not* supported is calling the author's own four-column attestation hash
> "the paper's behavioural tuple" — the paper's tuple has seven named
> components, and the paper attributes the premise to cited background rather
> than claiming it as its own discovery.**

Definition 1, Section 1.1 "Three levels, and the standards' own promise", page
2, verbatim:

> The premise that makes the setting interesting is cited background [44, 17]:
> behavior depends on a tuple (source, model version, instructions, retrieval
> configuration, tool definitions, runtime configuration, environment) whose
> components vary independently of the source.

With its own demarcation on the same page, continuing to page 3:

> The premise carries its own demarcation, which bounds every claim below: where
> the components cannot vary independently (models pinned, prompts in-tree, no
> runtime retrieval, static tools), the tuple collapses onto the source digest,
> conventional artifact provenance is sufficient, and this paper predicts no
> advantage from anything more elaborate.

Definition 2, Section 3 "The specification", under "Behavioral continuity", page
4, verbatim (the section notes "the definitions are quoted from the program's
frozen definitions document, whose content hash is pinned in the OSF
registration"):

> **Behavioral continuity.** The full behavioral tuple that was evaluated is the
> tuple that is running: source, model version, instructions, retrieval
> configuration, tool definitions, runtime configuration, environment. Artifact
> continuity is necessary but not sufficient; identical code under a different
> model version breaks behavioral continuity while preserving artifact
> continuity.

So the tuple contains **seven components: source, model version, instructions,
retrieval configuration, tool definitions, runtime configuration, environment.**

**A discrepancy worth carrying.** The abstract lists only **five**: "a
content-addressed identity of the behavioral tuple (model version, instructions,
tool definitions, retrieval and runtime configuration)" — `source` and
`environment` are dropped there. Quote the body's seven, not the abstract's
five, and if a figure in the article shows the tuple, show seven.

"Content-addressed" is defined too — Section 3.2 "Nominal versus
content-addressed reference", page 5, verbatim:

> Cross-cutting all four conditions, a reference is either content-addressed (a
> digest of the state itself, which cannot drift without the state changing) or
> nominal (a label maintained by convention, which can drift independently of
> what it names).

**The measurement over that tuple.** Section 5 defines the survey's fourth
dimension as "behavioral-tuple identity (a content-addressed identity over the
tuple of Section 1.1)" (page 7), graded only after searches including
"tuple-capable terms (version, snapshot, immutable, digest, sha256, checksum,
lineage, provenance, system prompt, instructions, tool definition)". Sealed
class counts:

- CI/CD, n=20 (Section 6.1, page 9): behavioral-tuple identity **default 0,
  opt-in 0, absent 20**. Also: artifact digest 5/4/11, approval record 13/2/5,
  provenance emission 0/6/14.
- Agent and model-serving, n=27 (Section 6.2, page 9): behavioral-tuple identity
  (content-addressed) **default 0, opt-in 2, absent 25**; nominal tuple
  versioning on the same cells **default 16, opt-in 2, absent 9**. Also:
  artifact digest 7/2/18, approval record 8/5/14, provenance emission 11/3/13.

The headline claim, verbatim (Section 6.2, page 9) — **the negative finding**:

> across the 47 platforms, in a survey of 188 double-graded cells, we found no
> platform, in either class, whose default record emits a content-addressed
> identity over the behavioral tuple, including all 27 platforms in the class
> where it would most plausibly exist.

Restated as the "Documentary finding" in Section 7.2, page 13:

> Across 47 platforms in two classes, graded twice under a fixed protocol with
> the second pass blind, no consulted documentation describes default emission
> of a content-addressed identity of the behavioral tuple. The agent class now
> records the tuple by default as immutable versions on 16 of 27 platforms,
> making behavioral continuity determinable there nominally but not at the
> content layer; the features that approach content addressing are opt-in,
> partial, or defeated by mutable indirection the record does not carry.

Reliability of that column (Section 6.2, page 9): raw agreement on the
tuple-identity column was **23 of 27** in the agent class and **20 of 20** in
CI/CD, and "all four divergences ran in one direction, against the paper's own
claim"; "in no tuple cell, in either class, did both passes agree on default".
The 27 agent/model-serving platforms are named on page 9 and include Amazon
Bedrock, Microsoft Foundry, Google Vertex AI, OpenAI platform, Anthropic Claude
platform, Ollama, Hugging Face, Azure ML, SageMaker, Weights & Biases, MLflow,
LangSmith/LangGraph, Databricks, Modal, Baseten, Together AI, Anyscale,
Replicate, Fireworks, Groq, Cohere, Mistral, Dify, CrewAI, Vercel AI, RunPod and
NVIDIA NIM/NGC.

Falsification clause, Section 7.2 page 13 (matched by Section 1.3 page 3):

> The finding is falsified by exhibiting a platform that emits a
> content-addressed tuple identity by default, judged by Section 3.3's
> definition; it expires, rather than fails, when the standardization efforts
> converging on tuple representation [13, 6, 3] ship as defaults on a named
> major platform.

**Three cautions for the December 應變篇, carried from half B.**

1. **The tuple is cited background, not this paper's invention.** The body says
   "cited background [44, 17]" and Section 3.1 repeats "Tuple-dependence itself
   is established [44, 17] and its representation is being standardized in
   bill-of-materials and reference-model form [13, 6, 3]". The paper's own
   contribution is the invariant/variant partition (its "first declared
   residue"), the nominal-vs-content-addressed split, the 0-4 depth rubric, and
   the two measurements. Do not write "this paper defines the behavioural
   tuple"; write "this paper measures whether platforms emit a content-addressed
   identity over it, and defines what counts."
2. **A four-column hash is not the paper's tuple.** Seven components, and
   Section 3.1's partition matters as much as the list: invariant by contract
   (source digest, dependency-set digest, instruction digests,
   interface-contract digests, runtime library versions, and behavior keys
   naming models, model location, tenant and guardrail policy) versus variant by
   design (environment label, configuration-file digest, any behavior key whose
   purpose is to differ per environment). The Codex review's suggested wording —
   that the article's four-column attestation is the author's design and not the
   paper's definition — is the right correction, and can now be stated
   positively: the paper *does* give a definition, the article's four columns are
   a subset of it.
3. **The behavioural rung is specified, not measured end to end.** Section 7.3's
   per-condition table (page 14) says for Behavioral: "content-addressed
   identity default nowhere; nominal versioning default on 16 of 27 agent
   platforms" and, under what the paper demonstrates, "**No, and cannot be: the
   population's record vocabulary contains no tuple (Section 6.1), which is the
   survey's ceiling met in the wild.**" The prevalence conjecture at the
   behavioural rung is explicitly "untested". The 30-repository depth study
   (Section 4.1 / 7.1) is the artifact layer: two strata of 15, 1,116 archived
   API responses, cell-level agreement 23 and 19 of 30 across the two passes,
   and the verifiability hole — **seven of the 15 repositories chosen for
   adopting attestation tooling publish source-only releases, so the binding
   their workflows declare cannot be checked where declared; five of seven
   measurable adopters realize the binding end to end, and both shortfalls fall
   at identity binding.**

### 4.4 The rest of the accountability objections

- **Behavioural tuple / content-addressed identity: answered above** —
  2608.23610 defines both and measures the second; 2605.12078 adds the
  cross-vendor shape (**three tiers of strict-governance-completeness from
  42.9% to 85.7%, one regime-independent gap: reasoning trace**).
- **"CI reads the trace from Tempo" (review: Tempo is a debug store, not an
  evidence store).** The sweep supports the correction outright. 2606.04193:
  "the entity producing the activity log is the same entity whose activity is
  being logged", so self-logged traces cannot be the truth source; 2609.12582
  says a trace is "mutable: alterable undetected, with no recipe for
  re-executing it"; 2609.01931 prices a tamper-evident ledger instead
  (**~48 µs/event, 512 B/event, $2.30 per 100K events, forensic precision 1.0 vs
  0.013**); 2609.01040 binds each decision to a DAG digest in a signed
  Decision-Evidence Packet. Use the ledger as the status check's truth source,
  exactly as the review asks.
- **Tamper boundary (the review's 補充 request: can the agent edit hooks, edit
  `harness.lock`, disable telemetry, rewrite the PR body?).** 2609.03884 says
  hooks are attacker-controllable through plugin metadata (**all 7 harnesses, up
  to 92.5%, Defender 0% recall**); 2609.07360 says **9.8% of setups pin no MCP
  version at all**; 2609.08371 shows the fix shape — capabilities stored outside
  the model's context; 2609.05901 keeps the signing key and every threshold
  share outside all LLM processes. The answer "不能, 靠 reference monitor 外置"
  is now citable.
- **Governance timing.** 2609.06445, verbatim: "**Article 86's right to an
  explanation has applied since 2 August 2026, while the Article 12 logging and
  Annex IV documentation that could evidence one were deferred to 2 December
  2027 by Regulation (EU) 2026/1744**." Note the honesty marker — its
  discrepancy experiment is pre-registered, published in full, **and not run**.
  2609.13466's attestation-deficit numbers are all **third-party
  vendor/industry-reported** and must be labelled as such if used.
- **Backlog item 3 (agent runtime as platform) stays deferred, with evidence.**
  Seven query strings across both halves return zero agent-on-Kubernetes papers
  in the window. The nearest artifacts are serving-layer, not platform-layer:
  2609.11294 (**8.7x sandbox memory reduction**), 2511.02230 (KV TTL for agent
  workloads), 2606.20474 (4-bit KV), 2609.03598 (**makespan −39%** on Slurm).
  If the December piece needs a platform section, the evidence will have to come
  from KubeCon/CNCF, not arXiv — which also supports the review's "K8s 只能是
  規模化段落" constraint and its request to cut the K8s/CNPE table.

---

## 5. What this means for 2026-10 and 2026-11

### 2026-10 「綠燈不是驗收」 — the four articles are already written; these are the five things to fold in

1. The title now has a direct measurement behind it: **1 in 7 statically clean
   samples (95 of 654, 14.53%) is exploitable under dynamic verification, with
   CWE-338 and CWE-916 flagged by neither Bandit nor Semgrep** (2609.10762).
2. The green-suite argument scales the wrong way: **the visible-vs-held-out gap
   grows 28 pp per tenfold increase in code size** (2605.21384), at exactly the
   sizes agents now write — including a 2,900-line "compiler" that memorises
   test inputs.
3. Tests are not one property: **availability, validity, feedback use and
   evaluation independence are separate**, and passing does not establish
   behavioural equivalence (2609.12012); who writes the tests decides the sign
   of the effect — base-agent tests **drop** resolved rate 61.2% → 57.3% while
   better tests raise it to 65.3% (2609.09133).
4. The review layer degrades measurably and silently: **approval 30.5% → 36.6%
   over 207 days** with no detectable change in review language, and approval
   change *precedes* language change (2609.06213); and a verifier-and-acceptance
   ablation shows **deterministic acceptance rules alone suppressed no false
   positives** (2609.15887).
5. The strongest single reframing for the 三部曲's conclusion: **"equal terminal
   outcomes do not imply equal containment" — 441 of 600 matched pairs (73.5%)
   differ in a 12-field trace summary with no committed violation on either
   side** (2607.23999). A green outcome is not evidence about behaviour.

### 2026-11 「同一份規格，跑十次」 — five anchors, and the thesis got stronger

1. The design already exists in the literature: **ninety independent runs of one
   detailed specification**, scored on a fixed 14-criterion / 42-point rubric,
   where criterion-level analysis "revealed what run totals conceal" —
   **container deployment failed first-try in 44% of runs** while mean totals
   moved less than a point (2607.02436).
2. Variance is now a *limit on published effect sizes*, which is a much sharper
   hook than non-determinism: a **+4.9 pp** SKILL.md gain that **cannot be
   separated from the agent's run-to-run variance** at one repository's data
   size, where "settling that would take more tasks than one repository's
   history yields" (2609.12742).
3. There is a protocol to copy: SaltBench pre-registers, walls the agent off,
   **tests the wall with breach probes before any scored run**, dates every
   freeze, counts a budget stop as a halt — and then reports that
   specify-and-verify **cost more on all five components** and the registered
   sign test reached **no verdict** (3 of 4, p = 0.3125) (2609.11076).
4. Specification content is a measurable cost lever, not a style question:
   2608.25399 (September) priced a bare user story at **+29.7% tokens**, and this
   window adds that prompt, effort and harness are **interacting** factors so
   token counts are "measurements, not optimisation targets" (2608.01347), while
   one appended sentence moves a benchmark 70 points (2609.06780).
5. The acceptance-metric framing has cover from three directions: leaderboard
   ranks that do not resolve under an estimand-aware procedure (2609.07785),
   judges that converge and anchor (2609.12191: **57.5% of "satisfied"
   conversations failed the task**), and harness variance that dwarfs the recipe
   (**2.14% → 9.27%, x4.3, vs 1.16 for the training recipe**, 2609.04518).
   Ten runs of one spec is not a stunt; it is the minimum unit at which any of
   these numbers means anything.
