<!--
Medium 發布指南（此註解區塊不要貼進 Medium）

自動化：`./tools/medium_draft.sh <article-dir> en` 會建好草稿並比對內容，停在發布前一步。
細節見 repo 根目錄的 PUBLISHING.md。以下是手動流程與發布後必做的收尾。

【系列狀態】以各篇 publish/PUBLISHED.md 為準。Medium 限制同一作者 24 小時內最多發布或排程 2 篇，
見 PUBLISHING.md 的〈發文數量上限〉。

【手動流程】
1. 開新 story：https://medium.com/new-story
2. 貼上下方內容（從標題那行開始，不含本註解）。
3. 看到 📌【在此插入…】的行：刪掉該行，按 + 插入同目錄 images/ 裡對應的 PNG。
4. code block：在 Medium 選取後按 ``` 轉成 code block。
5. 封面圖選流程圖，不要選表格截圖（縮到卡片尺寸看不清）。
6. Tags 建議：AI, Software Engineering, Engineering Management, Agentic AI, DevOps

【發布後收尾—不做的話系列會斷】
7. 記下本篇 Medium URL，補進 repo 的 README 索引與 publish/PUBLISHED.md。
8. 把本篇兩處的系列連結換成真正的 Medium URL：
   (a) 開頭「系列導覽」那一行
   (b) 文末「系列文章」清單
   （尚未發布的篇在這裡是純文字「（即將發布）」，不是相對路徑；上線後換成真正的 URL）
9. 回頭編輯已發布的其他篇，把指向本篇的連結補上。
-->

# Don't Build Your Own Devin: Org Strategy and a 90-Day Blueprint for Agentic Engineering

> **TL;DR** — Most engineering groups don't need a silo whose job is "building agents for other teams." What they do need is a small **Agentic Engineering Platform / Enablement team**. And don't build a complete agent runtime from scratch: the winning strategy is **buy the generic agent runtime, build the organization-specific harness layer**. If you map it onto DevOps history, Agentic Engineering in September 2026 sits roughly where DevOps and Cloud Native sat in 2014–2016: the direction is settled, the primitives are arriving, but the best practices and org structures haven't crystallized. A 90-day action blueprint is at the end.

> Series: **Overview (this piece)** → [1. Org Design](https://fantasybz.medium.com/agentic-engineering-part-1-who-does-this-platform-plus-federation-in-practice-92343384d987) → [2. The Harness Blueprint](https://fantasybz.medium.com/agentic-engineering-part-2-the-harness-blueprint-making-your-system-legible-to-agents-3facc281f633) → [3. Evals and Unit Economics](https://fantasybz.medium.com/agentic-engineering-part-3-evals-unit-economics-and-scaling-running-agents-like-a-product-1cb1855a2046)

---

## 1. The question every engineering VP is asking

Over the past year, nearly every engineering organization has been asking the same three questions:

- Should we stand up an AI Agent team?
- Should we build our own harness — or even our own agent?
- Is investing now too early, or already too late?

This piece is my complete answer. The conclusion first:

> **Own your Agentic Engineering Platform, but don't own the whole agent.**

What follows walks from the state of the market, through the lessons DevOps already taught us, into org design, the buy-vs-build call, and finally a concrete 90-day plan.

That order is deliberate. If you haven't established where the industry actually is, and haven't looked at the holes DevOps fell into on the way, then the org design and the buy-vs-build call are just picking a side on instinct, and you're one step away from another AI initiative that exists because everyone else has one.

---

## 2. Where the market actually is in 2026

Start by locating yourself on a rough maturity ladder. The axis here isn't how capable the models are; it's how much of the work people are willing to hand over.

The whole industry has visibly shifted rightward, and the center of gravity is now pressing on the last two stages:

📌【在此插入圖 diagram-01.png】

Two surveys are worth anchoring on. Google's 2025 DORA report (nearly 5,000 respondents) found that **90% of engineers now use AI at work**, with a median of two hours a day spent on it — yet only about 24% report high trust in what it produces. Stack Overflow's data shows AI agent usage jumping from 31% to 59% in a single year, while 87% of developers worry about the correctness of agent output. Read together, the message is unambiguous: **adoption stopped being the bottleneck a while ago. Trust and verification are the bottleneck now** — which is exactly what the harness and eval sections below are about.

The table below isn't a scoreboard of who wins. Here's what each ecosystem is pushing on, and the signal I think actually matters:

📌【在此插入表 table-01.png】

A few of these deserve unpacking.

### OpenAI: engineering becomes environment design

OpenAI's published [harness engineering experiment](https://openai.com/index/harness-engineering/) is the one to study: three engineers, working through Codex, produced roughly a million lines of code and about 1,500 PRs in five months. But the headline isn't the LOC. It's that their job shifted into **designing environments, constraints, and feedback loops** rather than writing code directly. Symphony went further still, turning a Linear backlog into the control plane for agent orchestration.

### Anthropic: separating brain from hands

Anthropic landed in nearly the same place. In [Effective harnesses for long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents) they decompose long-running application development into planner / generator / evaluator, and in Managed Agents they split **brain, hands, and session**: model plus harness is the brain; container, device, and MCP tools are the hands.

Anthropic also offers a warning worth taking seriously: a harness encodes assumptions about what the model can do — and those assumptions go stale fast as models improve. **That is the core reason I don't advise enterprises to build a complete agent runtime from scratch.**

### GitHub: the repository becomes the agent's work management system

GitHub's trajectory looks a lot like the platformization of CI/CD a decade ago. [Copilot cloud agent](https://github.blog/changelog/2026-04-01-research-plan-and-code-with-copilot-cloud-agent/) already works inside its own development environment: researching the codebase, producing a plan, writing the code. [Custom agents](https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/customize-cloud-agent/create-custom-agents) let you define tools, MCP servers, and prompts inside the repo, then have a parent agent invoke them as sub-agents. This isn't "Copilot" anymore — it's turning the GitHub repository into an agent work management system.

### Cursor: the CI runner story, repeating

Cursor is solving the same problem from another angle. Every [cloud agent](https://cursor.com/blog/cloud-agent-lessons) gets a dedicated VM, repo, dependencies, secrets, and network policy, and when it finishes it hands back screenshots, video, and logs — so humans verify the *result* instead of watching every step. They've even started [caching ready-to-use development environments](https://cursor.com/blog/cloud-agent-environment), because startup time for agent infrastructure has become the bottleneck. Which is precisely the arc CI runners took: cold runs → containerized CI → warm pools.

### The biggest signal: standards are converging

In December 2025 the Linux Foundation formed the [Agentic AI Foundation (AAIF)](https://www.linuxfoundation.org/press/linux-foundation-announces-the-formation-of-the-agentic-ai-foundation), bringing **MCP, AGENTS.md, and goose** under one roof; as of August 2026 it counts 247 member organizations. The industry is standardizing the interfaces between model, tools, and repository context, instead of every agent vendor shipping its own closed integrations. This looks very much like the moment the CNCF ecosystem started to converge.

---

## 3. DevOps already ran this experiment

First, what this comparison is for. I'm not claiming Agentic Engineering will repeat DevOps step by step. I want to borrow what DevOps and Cloud Native went through, so we can tell which parts of today are only new names and which are old problems handed to a new kind of worker.

Seen that way, the two eras map onto each other almost item for item:

📌【在此插入表 table-02.png】

The row worth staring at is the last one. Everything above it lines up component against component and practice against practice. What the last row changes isn't a component at all, it's the responsibility model. The act of delivering gets handed to agents, while the responsibility stays with the same people.

Lay the two timelines on top of each other:

📌【在此插入圖 diagram-02.png】

My read is that **2026 is the Kubernetes moment**. Everyone already accepts that agents are here to stay. What's still being fought over is how they execute, how they get context, how they reach tools, how they collaborate, how they're constrained, and how they're observed.

And the biggest organizational lesson DevOps left behind:

> **Don't turn a culture-and-capability problem into another functional silo.**

Plenty of companies stood up standalone DevOps teams early on, only to convert "Dev → Ops ticket" into "Dev → DevOps ticket." It took years to evolve into platform teams, paved roads, and self-service. Agentic Engineering should **skip that wrong turn entirely**.

---

## 4. Don't build this team

Start with the wrong answer that gets reached for most often. The organization's first move is usually to stand up a central agent team and let every other team throw its requests over the wall:

📌【在此插入圖 diagram-03.png】

It's not that the central team lacks the smarts. The position itself doesn't hold. This design fails for two reasons:

1. It swaps a queue waiting on Ops for a queue waiting on the agent team. Same bottleneck, new name.
2. A central agent team will never understand business context better than the domain team — and context is precisely what determines the quality of what an agent produces.

Beyond the central agent team, three failure modes show up just as often and get named far less:

- **Building your own runtime.** Six to twelve months spent on an in-house Claude Code or Devin. The vendor's next release makes it obsolete. You are betting against the capital expenditure of an entire industry, and the odds of losing are close to certain.
- **The AGENTS.md graveyard.** A big push requiring every repo to have an AGENTS.md, with nobody owning maintenance and no evals confirming it actually improves agent output. Six months later it's as stale as the company wiki. Context is a living artifact that needs an owner, not a document you write once and archive.
- **Review becomes the new bottleneck.** Agents produce PRs ten times faster while the review process stays exactly the same. The result isn't faster delivery. It's an exploding review queue, reviewer fatigue, and eventually rubber-stamped approvals. The quality problem hasn't gone anywhere; it has moved downstream into production. This is why agent-reviewing-agent and evals have to be funded in step with generation capacity.

---

## 5. Build this team instead

The right shape is **platform plus federation**: a central platform team paves roads, domain teams drive themselves onto them, and embedded champions connect the two. By a paved road I mean that security, environments, tooling, and evals are wired up in advance, so the default path is also the safe one; the champions are engineers scattered across the product teams who still build product day to day:

📌【在此插入圖 diagram-04.png】

The part of this model that starts the most arguments is ownership. My rule for splitting it: anything that crosses repos, crosses teams, or touches security and infrastructure consistency belongs to the Agentic Platform Team, and anything that decides product correctness or takes domain judgment stays with the Product Engineering Team.

Ownership splits like this:

📌【在此插入表 table-03.png】

The single most important idea in that table:

> **The platform team builds the harness. The product team builds agent-legible software.**

Those are two entirely different jobs.

The harness answers whether an agent can work safely, reliably, and observably. Agent-legible software answers a different question: whether your own system carries tests, documentation, logs, traces, and rules clear enough for the agent to get the work right. The first is paving the road. The second is putting up the signs along it.

On sizing — these are my numbers, not an industry standard:

📌【在此插入表 table-04.png】

Even past 500 engineers, I would not put a central team in charge of "making agents for everyone else." For the actual org charts at each tier, the skill mix, and the signals that tell you it's time to move up a tier, see [the org design piece](https://fantasybz.medium.com/agentic-engineering-part-1-who-does-this-platform-plus-federation-in-practice-92343384d987).

One question that gets skipped: **how you pick champions, and how people transition.** A good agent champion is not "the person best at prompting." It's whoever was already good at developer experience — the engineer who writes tests, keeps documentation honest, and has taste in CI/CD and tooling. Harness engineering is DX engineering with the audience swapped from humans to agents.

As for junior engineers, my view runs against the fashionable pessimism. The scarcest skills of the agent era are decomposing problems, defining acceptance criteria, and judging output quality, and all three are built precisely by reviewing large volumes of agent output. So organizations should deliberately design "review the agent's PRs" into the junior training path, rather than reserving it for seniors and then wondering, three years later, why nobody is ready to step up.

---

## 6. A harness is not a prompt

Follow the org design far enough and it lands on a technical question: what is the platform team actually supposed to build? If the answer turns out to be a handful of prompt templates, the division of labor above has nothing to stand on.

The harness here is not a few more paragraphs of prompt, and it isn't rebuilding an agent of your own from scratch. More precisely, it's the layer where a company wires together context, tools, environment, feedback, guardrails, and evals, so an agent can actually finish work inside your engineering system instead of only producing code.

Here's how I define the harness a company builds for itself:

📌【在此插入圖 diagram-05.png】

**The prompt may well be the least important piece in there.** Which is why the industry conversation has moved from prompt engineering to harness engineering.

### AGENTS.md: what good and bad look like

The "context" branch deserves something concrete. A good AGENTS.md is not a project overview. It's an operating manual written for an agent. Its purpose isn't to introduce, it's to prevent:

```text
# Wrong: describing the current state
This is an order management service written in Go and PostgreSQL, following clean architecture.

# Right: preventing mistakes
- Run only affected tests: `make test FILTER=<path>` — the full suite is slow, don't default to it
- `legacy/` is read-only: call into it, never modify it. To change it, open an issue for @platform-team
```

Every sentence in the first block is true, and an agent that reads it can do exactly nothing more than before. Every line in the second block corresponds to a mistake somebody actually made.

There's only one test for quality: **can a new agent — or a new engineer — take this and ship a correct first PR on day one without asking anyone?**

Put the harness into the wider system, and you get the layer a company should genuinely own:

📌【在此插入圖 diagram-06.png】

Note carefully: **owning that middle layer is not the same as writing your own Claude Code.**

### Guardrails are not optional

The policy, identity, and guardrails boxes deserve their own callout, because they are exactly what you'll be asked about the moment you take this architecture to a CISO:

- **Identity and least privilege.** Every agent run should have its own identity and scoped credentials. That is, it gets the repos, secrets, and APIs this task needs and nothing more, not a shared human token. When something goes wrong, "which agent, which run, acting with what permissions" has to be answerable in five minutes.
- **Prompt injection is a real attack surface.** Agents read issues, PR comments, external web pages, and logs — all untrusted input. Tiered tool permissions and sandbox egress policy are table stakes, not extra credit.
- **Audit trail.** Every tool call by every agent must be traceable. Starting to build this when compliance asks "who decided this code should work this way" is starting far too late.

---

## 7. The real moat: agent legibility

In OpenAI's harness engineering piece, the most important thing isn't Codex. It's one sentence:

> **Make the system legible to agents.**

Legible here does not mean writing more documentation for the agent to read. It means that the clues a human digs through while debugging or reviewing have to be clues the agent can dig through on its own.

Turn logs, metrics, traces, browser state, DOM, screenshots, tests, architecture, dependency rules, CI, and PR feedback into things an agent can query, operate, and verify directly. Once you have, the delivery pipeline looks like this:

📌【在此插入圖 diagram-07.png】

What's left for humans is intent, architecture, constraints, taste, risk, prioritization, and acceptance.

The center of gravity for people moves upstream. You stop spending most of your time on each line of the implementation, and take responsibility instead for setting the direction, the constraints, and the bar for what counts as done. **That, to me, is the actual definition of Agentic Engineering.**

### What about brownfield?

That diagram assumes a system that already has tests, structured logs, and documented architecture. The reality at most companies is a fifteen-year-old legacy monolith with none of the three — which is exactly why legibility investment needs an order. Mine:

1. **Characterization tests first.** Give the agent feedback it can use to verify its own changes. Everything else depends on this.
2. **Then structured logs and traces.** Let the agent debug itself instead of pasting a stack trace back to a human every time.
3. **Architecture rules and documentation last.** This layer has the highest value, but without the first two, an agent can understand the rules and still get the work wrong.

The counterintuitive part: this ordering is identical to what you'd invest in to get new engineers productive quickly. Agent legibility and human legibility are the same thing. Which is why, even if the agent bet doesn't pan out, almost none of this spend is wasted.

---

## 8. What to buy and what to build

This may be the most consequential judgment in the whole piece. The diagram below splits into two boxes. The top one holds everything the market will keep upgrading on your behalf; the bottom one holds everything that only you will build, because only you need it:

📌【在此插入圖 diagram-08.png】

Compressed into one line:

> **Buy the intelligence. Build the environment. Own the feedback loop.**

The reasoning goes back to Anthropic's warning: a harness encodes assumptions about model capability, and every six months a new model invalidates some of them. Generic capability — the agent loop, planning, sandbox technology — is the layer where vendors compete furiously and upgrade you for free. Your context, your conventions, your eval dataset, your feedback loop: those are the assets no model release can erase.

---

## 9. Evals: the only asset that compounds

I've claimed the eval dataset is the moat a model release can't erase. Most teams stall on the first step: where do evals come from? The answer: **they're already sitting in your engineering history.**

- **Harvest from incidents.** Every post-mortem is a ready-made eval case — give the agent the context and symptoms from that day and see whether it finds the root cause.
- **Harvest from PR history.** An agent PR a reviewer sent back, together with the review comment, is the most authentic negative example you will ever get. The ones that sailed through are your golden paths.
- **Golden tasks.** Pick 10–20 representative completed tasks — a few bug fixes, a few small features, a few refactors — and freeze their context and acceptance criteria. Re-run them every time the model or the harness changes.

The maintenance cost is lower than people expect. Evals don't have to be fully automated from day one; a monthly round of human scoring is enough to answer the two most expensive questions you face — "a new model shipped, should we switch?" and "did that harness change make things better or worse?" Organizations without evals can only answer those on instinct, and instinct doesn't survive contact with vendor marketing and a good demo.

That's what compounding means here: every model upgrade and every vendor price war increases the value of your eval dataset, because you're the only one who can validate a new option against your own workload in a day. Everyone else is reading benchmarks and guessing.

---

## 10. If I were the engineering VP

I would **not** approve this:

> "Stand up a 10-person AI agent team and build our own Devin."

I **would** approve this:

> "Stand up a 4–6 person Agentic Engineering Platform team, and within six months let every engineering team use Codex, Claude, or Copilot safely and self-service."

The North Star for year one shouldn't be AI-generated LOC, and it shouldn't be PR count. It should look closer to this:

```text
% tasks successfully delegated
        ×
end-to-end completion rate
        ×
human attention saved
        ×
production correctness
```

A North Star can only tell you whether the direction is right, which isn't enough to run the operation day to day. What a weekly or monthly review needs is something plainer: numbers that show whether speed, human attention, output quality, and cost are all improving together.

Paired with a set of operating metrics:

📌【在此插入表 table-05.png】

**Cost per successful task** deserves unpacking, because agent unit economics behave nothing like headcount. A single successful autonomous run can cost anywhere from tens of cents to tens of dollars, and the driver is retry count and context size — not how hard the task was. Two practical rules:

- **Model routing.** Use the strongest model for planning and review; use cheap models for bulk generation and eval runs. That routing logic belongs in the platform, so teams don't each invent their own.
- **Treat agent retry rate as a leading indicator.** Money burned on retries is almost entirely a tax on context and feedback loops you haven't fixed. If retry rate won't come down, fix the harness before blaming the model.

This is how you avoid re-running the vanity metrics of early DevOps — "we deploy a lot, therefore our DevOps is good."

One prediction while we're here: by 2028–2030, the name "Agentic Engineering team" will likely fade out, the way mature engineering organizations today don't have a "Git team" or a "CI team." Agentic capability gets absorbed into developer platform, SRE, security, and engineering productivity.

---

## 11. The first 90 days

If you decide to do this, here's how I'd sequence the first 90 days:

📌【在此插入表 table-06.png】

Three warnings:

1. **Pick pilots that are painful but not fatal**: internal tools, test coverage, bug backlog. Not the mission-critical path.
2. **Start without a baseline and you will be unable to prove anything three months later.** This is the most common and most expensive mistake.
3. **The platform team's first customer is the pilot team, not the whole company.** Chasing coverage too early is the most common way a platform team dies.

---

## 12. Closing

Having walked through all of that, I'll reduce the whole argument to one thing. It is genuinely the right moment to invest in Agentic Engineering. But the thing to invest in isn't "our own agent." It's this:

> **Make any agent work well inside your engineering system.**

That will outlast whichever of Codex, Claude Code, Copilot, or Devin happens to win.

---

### The series

This is the overview of a four-part series on Agentic Engineering. Each deep dive takes one dimension — organization, technology, operations — down to the level where you can start work:

1. **Overview (this piece)**: market state, the DevOps parallel, the decision framework, and the 90-day blueprint
2. [1. Org Design: who does this? Platform plus federation in practice](https://fantasybz.medium.com/agentic-engineering-part-1-who-does-this-platform-plus-federation-in-practice-92343384d987) — headcount, the champion system, merge decisions, budget narrative
3. [2. The Harness Blueprint: making your system legible to agents](https://fantasybz.medium.com/agentic-engineering-part-2-the-harness-blueprint-making-your-system-legible-to-agents-3facc281f633) — three-tier AGENTS.md, MCP gateway, sandboxing, brownfield playbook
4. [3. Evals, Unit Economics, and Scaling: running agents like a product](https://fantasybz.medium.com/agentic-engineering-part-3-evals-unit-economics-and-scaling-running-agents-like-a-product-1cb1855a2046) — eval pipeline, cost model, gaming-resistant metrics, scaling gates

---

### References

1. OpenAI — [Harness engineering: leveraging Codex in an agent-first world](https://openai.com/index/harness-engineering/)
2. Anthropic — [Effective harnesses for long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)
3. GitHub — [Research, plan, and code with Copilot cloud agent](https://github.blog/changelog/2026-04-01-research-plan-and-code-with-copilot-cloud-agent/), [Creating custom agents for Copilot cloud agent](https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/customize-cloud-agent/create-custom-agents)
4. Cursor — [What we've learned building cloud agents](https://cursor.com/blog/cloud-agent-lessons), [How we set up our cloud agent environment](https://cursor.com/blog/cloud-agent-environment)
5. Linux Foundation — [Announcing the Agentic AI Foundation (AAIF)](https://www.linuxfoundation.org/press/linux-foundation-announces-the-formation-of-the-agentic-ai-foundation)
6. Google — [2025 DORA report: How are developers using AI?](https://blog.google/innovation-and-ai/technology/developers-tools/dora-report-2025/)
7. Stack Overflow — [Agents on a leash: Agentic AI remains mostly monitored at work](https://stackoverflow.blog/2026/05/27/agents-on-a-leash-agentic-ai-remains-mostly-monitored-at-work/)

---

### On how this piece was made

The initial concept and chapter structure are the author's; the prose was drafted in collaboration with AI (Claude), then reviewed and revised section by section by the author before publication. The views and judgments are the author's own, as is responsibility for the content.

---

*Originally published in Chinese: [中文版](https://fantasybz.medium.com/%E5%88%A5%E6%80%A5%E8%91%97%E6%89%93%E9%80%A0%E4%BD%A0%E7%9A%84-devin-agentic-engineering-%E7%9A%84%E7%B5%84%E7%B9%94%E7%AD%96%E7%95%A5%E8%88%87-90-%E5%A4%A9%E8%A1%8C%E5%8B%95%E8%97%8D%E5%9C%96-7342ababc417). Also on [Medium @fantasybz](https://medium.com/@fantasybz) — if you're building Agentic Engineering capability in your organization, I'd like to hear from you.*
