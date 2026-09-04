<!--
Medium publishing guide (do NOT paste this comment block into Medium)

Automation: `./tools/medium_draft.sh <article-dir> en` builds the draft and diffs the
content, stopping one step before publish. See PUBLISHING.md. Manual flow below.

[Series status] English edition of the Agentic Engineering series. The Chinese
editions are published separately; cross-link the two once both are live.

[Manual flow]
1. New story: https://medium.com/new-story
2. Paste the content below (start at the title line; exclude this comment).
3. Where you see a marker line starting with the pin emoji: delete that line and
   use + to insert the matching PNG from the images/ folder next to this file.
   (The marker text is Chinese because the repo tooling parses that exact format;
   the line is deleted on insert, so it never reaches readers.)
4. Code blocks: select in Medium and press ``` to convert.
5. Cover image: pick a flow diagram, never a table screenshot (unreadable at card size).
6. Suggested tags: AI, Software Engineering, Engineering Management, Agentic AI, DevOps

[After publishing - skip this and the series breaks]
7. Record the Medium URL in the repo README index and publish/PUBLISHED.md.
8. Replace the series links in two places with real Medium URLs:
   (a) the "Series:" line near the top
   (b) the "The series" list at the end
   (an unpublished part appears here as plain text "(coming soon)", not as a relative path)
9. Go back and add links to this piece from the other parts already published.
10. Add a line to the Chinese edition pointing at this English version, and vice versa.
-->

# Don't Build Your Own Devin: Org Strategy and a 90-Day Blueprint for Agentic Engineering

> **TL;DR** — Most engineering groups don't need a silo whose job is "building agents for other teams." What they do need is a small **Agentic Engineering Platform / Enablement team**. And don't build a complete agent runtime from scratch: the winning strategy is **buy the generic agent runtime, build the organization-specific harness layer**. If you map it onto DevOps history, Agentic Engineering in September 2026 sits roughly where DevOps and Cloud Native sat in 2014–2016: the direction is settled, the primitives are arriving, but the best practices and org structures haven't crystallized. A 90-day action blueprint is at the end.

> Series: **Overview (this piece)** → [1. Org Design](https://fantasybz.medium.com/agentic-engineering-part-1-who-does-this-platform-plus-federation-in-practice-92343384d987) → [2. The Harness Blueprint](https://fantasybz.medium.com/agentic-engineering-part-2-the-harness-blueprint-making-your-system-legible-to-agents-3facc281f633) → 3. Evals and Unit Economics (coming soon)

---

## 1. The question every engineering VP is asking

Over the past year, nearly every engineering organization has been asking the same three questions:

- Should we stand up an AI Agent team?
- Should we build our own harness — or even our own agent?
- Is investing now too early, or already too late?

This piece is my complete answer. The conclusion first:

> **Own your Agentic Engineering Platform, but don't own the whole agent.**

What follows walks from the state of the market, through the lessons DevOps already taught us, into org design, the buy-vs-build call, and finally a concrete 90-day plan.

---

## 2. Where the market actually is in 2026

The whole industry has visibly shifted rightward, and the center of gravity is now pressing on the last two stages:

📌【在此插入圖 diagram-01.png】

Two surveys are worth anchoring on. Google's 2025 DORA report (nearly 5,000 respondents) found that **90% of engineers now use AI at work**, with a median of two hours a day spent on it — yet only about 24% report high trust in what it produces. Stack Overflow's data shows AI agent usage jumping from 31% to 59% in a single year, while 87% of developers worry about the correctness of agent output. Read together, the message is unambiguous: **adoption stopped being the bottleneck a while ago. Trust and verification are the bottleneck now** — which is exactly what the harness and eval sections below are about.

Here's what each ecosystem is pushing on, and the signal I think actually matters:

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

In December 2025 the Linux Foundation formed the [Agentic AI Foundation (AAIF)](https://www.linuxfoundation.org/press/linux-foundation-announces-the-formation-of-the-agentic-ai-foundation), bringing **MCP, AGENTS.md, and goose** under one roof; as of August 2026 it counts 247 member organizations. The industry is standardizing the interfaces between model, tools, and repository context, instead of every agent vendor shipping its own closed integrations — very much the moment the CNCF ecosystem started to converge.

---

## 3. DevOps already ran this experiment

The two eras map onto each other almost item for item:

📌【在此插入表 table-02.png】

Lay the two timelines on top of each other:

📌【在此插入圖 diagram-02.png】

My read is that **2026 is the Kubernetes moment**. Everyone already accepts that agents are here to stay. What's still being fought over is how they execute, how they get context, how they reach tools, how they collaborate, how they're constrained, and how they're observed.

And the biggest organizational lesson DevOps left behind:

> **Don't turn a culture-and-capability problem into another functional silo.**

Plenty of companies stood up standalone DevOps teams early on, only to convert "Dev → Ops ticket" into "Dev → DevOps ticket." It took years to evolve into platform teams, paved roads, and self-service. Agentic Engineering should **skip that wrong turn entirely**.

---

## 4. Don't build this team

📌【在此插入圖 diagram-03.png】

This design fails for two reasons:

1. It swaps a queue waiting on Ops for a queue waiting on the agent team. Same bottleneck, new name.
2. A central agent team will never understand business context better than the domain team — and context is precisely what determines the quality of what an agent produces.

Beyond the central agent team, three failure modes show up just as often and get named far less:

- **Building your own runtime.** Six to twelve months spent on an in-house Claude Code or Devin. The vendor's next release makes it obsolete. You are betting against the capital expenditure of an entire industry, and the odds of losing are close to certain.
- **The AGENTS.md graveyard.** A big push requiring every repo to have an AGENTS.md, with nobody owning maintenance and no evals confirming it actually improves agent output. Six months later it's as stale as the company wiki. Context is a living artifact that needs an owner, not a document you write once and archive.
- **Review becomes the new bottleneck.** Agents produce PRs ten times faster while the review process stays exactly the same. The result isn't faster delivery — it's an exploding review queue, reviewer fatigue, and rubber-stamped approvals that push the quality problem downstream into production. This is why agent-reviewing-agent and evals have to be funded in step with generation capacity.

---

## 5. Build this team instead

The right shape is **platform plus federation**: a central platform team paves roads, domain teams drive themselves onto them, and embedded champions connect the two.

📌【在此插入圖 diagram-04.png】

Ownership splits like this:

📌【在此插入表 table-03.png】

The single most important idea in that table:

> **The platform team builds the harness. The product team builds agent-legible software.**

Those are two entirely different jobs.

On sizing — these are my numbers, not an industry standard:

📌【在此插入表 table-04.png】

Even past 500 engineers, I would not put a central team in charge of "making agents for everyone else." For the actual org charts at each tier, the skill mix, and the signals that tell you it's time to move up a tier, see [the org design piece](https://fantasybz.medium.com/agentic-engineering-part-1-who-does-this-platform-plus-federation-in-practice-92343384d987).

One question that gets skipped: **how you pick champions, and how people transition.** A good agent champion is not "the person best at prompting." It's whoever was already good at developer experience — the engineer who writes tests, keeps documentation honest, and has taste in CI/CD and tooling. Harness engineering is DX engineering with the audience swapped from humans to agents.

As for junior engineers, my view runs against the fashionable pessimism. The scarcest skills of the agent era — decomposing problems, defining acceptance criteria, judging output quality — are built precisely by reviewing large volumes of agent output. Organizations should deliberately design "review the agent's PRs" into the junior training path, rather than reserving it for seniors and then wondering, three years later, why nobody is ready to step up.

---

## 6. A harness is not a prompt

Here's how I define the harness a company builds for itself:

📌【在此插入圖 diagram-05.png】

**The prompt may well be the least important piece in there.** Which is why the industry conversation has moved from prompt engineering to harness engineering.

### AGENTS.md: what good and bad look like

The "context" branch deserves something concrete. A good AGENTS.md is not a project overview — it's an operating manual written for an agent. Its purpose isn't to introduce; it's to prevent:

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

- **Identity and least privilege.** Every agent run should have its own identity and scoped credentials — access to the repos, secrets, and APIs this task needs, and nothing more. Never a shared human token. When something goes wrong, "which agent, which run, acting with what permissions" has to be answerable in five minutes.
- **Prompt injection is a real attack surface.** Agents read issues, PR comments, external web pages, and logs — all untrusted input. Tiered tool permissions and sandbox egress policy are table stakes, not extra credit.
- **Audit trail.** Every tool call by every agent must be traceable. Starting to build this when compliance asks "who decided this code should work this way" is starting far too late.

---

## 7. The real moat: agent legibility

In OpenAI's harness engineering piece, the most important thing isn't Codex. It's one sentence:

> **Make the system legible to agents.**

Turn logs, metrics, traces, browser state, DOM, screenshots, tests, architecture, dependency rules, CI, and PR feedback into things an agent can query, operate, and verify directly. Once you have, the delivery pipeline looks like this:

📌【在此插入圖 diagram-07.png】

What's left for humans is intent, architecture, constraints, taste, risk, prioritization, and acceptance. **That, to me, is the actual definition of Agentic Engineering.**

### What about brownfield?

That diagram assumes a system that already has tests, structured logs, and documented architecture. The reality at most companies is a fifteen-year-old legacy monolith with none of the three — which is exactly why legibility investment needs an order. Mine:

1. **Characterization tests first.** Give the agent feedback it can use to verify its own changes. Everything else depends on this.
2. **Then structured logs and traces.** Let the agent debug itself instead of pasting a stack trace back to a human every time.
3. **Architecture rules and documentation last.** This layer has the highest value, but without the first two, an agent can understand the rules and still get the work wrong.

The counterintuitive part: this ordering is identical to what you'd invest in to get new engineers productive quickly. Agent legibility and human legibility are the same thing. Which is why, even if the agent bet doesn't pan out, almost none of this spend is wasted.

---

## 8. What to buy and what to build

This may be the most consequential judgment in the whole piece:

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

1. **Pick pilots that are painful but not fatal** — internal tools, test coverage, bug backlog. Not the mission-critical path.
2. **Start without a baseline and you will be unable to prove anything three months later.** This is the most common and most expensive mistake.
3. **The platform team's first customer is the pilot team, not the whole company.** Chasing coverage too early is the most common way a platform team dies.

---

## 12. Closing

It is genuinely the right moment to invest in Agentic Engineering. But the thing to invest in isn't "our own agent." It's this:

> **Make any agent work well inside your engineering system.**

That will outlast whichever of Codex, Claude Code, Copilot, or Devin happens to win.

---

### The series

This is the overview of a four-part series on Agentic Engineering. Each deep dive takes one dimension — organization, technology, operations — down to the level where you can start work:

1. **Overview (this piece)**: market state, the DevOps parallel, the decision framework, and the 90-day blueprint
2. [1. Org Design: who does this? Platform plus federation in practice](https://fantasybz.medium.com/agentic-engineering-part-1-who-does-this-platform-plus-federation-in-practice-92343384d987) — headcount, the champion system, merge decisions, budget narrative
3. [2. The Harness Blueprint: making your system legible to agents](https://fantasybz.medium.com/agentic-engineering-part-2-the-harness-blueprint-making-your-system-legible-to-agents-3facc281f633) — three-tier AGENTS.md, MCP gateway, sandboxing, brownfield playbook
4. 3. Evals, Unit Economics, and Scaling: running agents like a product (coming soon) — eval pipeline, cost model, gaming-resistant metrics, scaling gates

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
