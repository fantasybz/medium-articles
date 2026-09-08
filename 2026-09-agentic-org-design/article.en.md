# Agentic Engineering, Part 1 — Who Does This? Platform Plus Federation in Practice

> **TL;DR** — The first deep dive from [Don't Build Your Own Devin](https://fantasybz.medium.com/dont-build-your-own-devin-org-strategy-and-a-90-day-blueprint-for-agentic-engineering-8187e7ec80f9). The overview's conclusion: don't stand up a central agent team, stand up a small Agentic Platform team. This piece takes "how do you actually organize it" down to the level you could walk into a headcount meeting with: real org charts at three company sizes, how to select and evaluate champions, how to merge with your existing DevEx or SRE function, and the budget narrative that works with a CFO.

> Series: [Overview](https://fantasybz.medium.com/dont-build-your-own-devin-org-strategy-and-a-90-day-blueprint-for-agentic-engineering-8187e7ec80f9) → **1. Org Design (this piece)** → [2. The Harness Blueprint](https://fantasybz.medium.com/agentic-engineering-part-2-the-harness-blueprint-making-your-system-legible-to-agents-3facc281f633) → [3. Evals and Unit Economics](https://fantasybz.medium.com/agentic-engineering-part-3-evals-unit-economics-and-scaling-running-agents-like-a-product-1cb1855a2046)

---

## 1. Why organizations drift into the wrong design

The overview named four failure modes. This piece starts with the central agent team. I picked it not because it's the most absurd of the four, but for the opposite reason: it's usually the option that goes down easiest in the room. It isn't a stupid decision. It's what organizational gravity produces on its own.

Three forces push you there:

- **Budget gravity.** AI money is usually new money, and new money needs a cost center to hang on. So: "let's create a team first and figure it out later."
- **Scarcity gravity.** Early on, few people understand agents, so concentrating them *looks* like the efficient allocation.
- **Control gravity.** Legal and security want a single point of contact they can govern. A central team hands them a convenient handle.

All three forces are real, and none of them is malicious. But what they optimize for is manageability, not output.

Conway's law says the system you build ends up shaped like the way your organization communicates. Here you have to run it in reverse: the delivery system you end up with will look like your org chart — and a central team's org chart produces a ticket-queue delivery system. By ticket queue I mean the domain team drops from owner to requester. Whatever it wants done gets written up, dropped into the central team's schedule, and then it waits.

> If you want a self-service system, you have to draw a self-service org chart first.

---

## 2. Platform plus federation, in full

The overview gave the concept. Here it is at RACI resolution across the three roles. RACI is four markers for assigning responsibility: R is who does the work, A is who is accountable for the result, C is who has to be consulted, and I is who only has to be informed. Start with what actually moves between the three roles:

```mermaid
flowchart LR
    subgraph PT["Agentic Platform Team (4–8 people)"]
        P1["Runtime integration and upgrades"]
        P2["MCP gateway and permissions"]
        P3["Eval framework"]
        P4["Cost and observability"]
    end
    subgraph CH["Embedded Champions (1 per team, 20% time)"]
        C1["Bring paved roads into the team"]
        C2["Bring pain points back to platform"]
    end
    subgraph DT["Domain Teams"]
        D1["AGENTS.md and domain context"]
        D2["Eval cases"]
        D3["Final quality of output"]
    end
    PT -->|paved roads / tooling / training| CH
    CH -->|feedback / requests / practices| PT
    CH -.->|embedded in| DT
    style PT fill:#d4edda,stroke:#2e7d32
```

The one thing to hold on to from that diagram is where the champion sits. They are embedded inside the domain team, not a liaison the platform team posted there, so the pain points they carry back are ones they hit themselves rather than ones they are relaying. A paved road is exactly what the name says. The shared pieces — runtime, sandbox, an AGENTS.md template, the eval framework — get built once, so an engineer who follows the road doesn't have to cut their own.

Put the three roles through RACI item by item and the split looks like this:

| Item | Platform Team | Champion | Domain Team |
|---|---|---|---|
| Runtime selection and upgrades | **R / A** | C | I |
| Sandbox and permission infrastructure | **R / A** | C | I |
| AGENTS.md template and standards | **A** | R (drives) | **R** (content) |
| Domain MCP tools | C | C | **R / A** |
| Eval framework | **R / A** | C | I |
| Eval cases (domain) | C | R (drives) | **R / A** |
| Cost and quota policy | **R / A** | I | C |
| Output quality and production ownership | I | I | **R / A** |

The most important cell in that table is the last row: **production ownership always stays with the domain team.** Any design that routes "the agent's code broke production" to the platform team will collapse into finger-pointing at the first incident.

---

## 3. Real org charts at three sizes

RACI tells you who is responsible for what, but it won't tell you how many people you need. Headcount depends on size, and the difference between the sizes isn't proportional scaling. The approach changes entirely.

### 50 engineers: the no-team version

- Zero dedicated headcount. Two champions at 20% time each, plus a sponsor (a VP or senior EM).
- Adopt a SaaS runtime and the vendor's default sandbox. Govern with a checklist; don't build a gateway.
- **Upgrade signal:** when champions are spending more than 30% of their time helping other teams wire up tooling, it's time to open a pod.

### 200 engineers: a 4–6 person platform pod

At this size champions can no longer carry it, and you need people on this full time. The chart below is my recommended shape, not the answer. Read it for two things: who reports to whom, and which roles are borrowed.

```mermaid
flowchart TB
    VP["VP Engineering"] --> PL["Platform Lead (1)"]
    VP --> G["Champions Guild<br/>(8–10 people, 20% time each)"]
    PL --> IE["Infra / Sandbox (1–2)"]
    PL --> DX["DX / Context engineering (1)"]
    PL --> EV["Eval / Observability (1)"]
    PL --> SEC["Security (0.5, borrowed from the security team)"]
    style PL fill:#d4edda,stroke:#2e7d32
```

The hard part of that chart isn't where the boxes go, it's the skill mix. And the skill mix comes down to one sentence: this is a **product team, not a research team**. Its product is the paved road described above, and its customers are internal engineers. So hire people who have built developer tooling, CI, and test infrastructure — not people with model research backgrounds.

Borrow that half-person of security: giving the security team a stake up front is far cheaper than getting sent back by an audit later. They still sit in the security team and are reviewed by the security team. They just spend a fixed slice of their time inside the platform's design discussions.

### 1,000 engineers: a platform group with specialization

- Platform grows to 8–12, split into three squads: **runtime and environment**, **context and tools**, **eval and FinOps**.
- Add a cross-functional virtual security council (one person each from security, legal, and platform; monthly is enough).
- What doesn't change: even at this size, there is no "team that writes code for other teams using agents."

The three tiers side by side:

| Size | Dedicated | Champions | Governance | Next upgrade signal |
|---:|---|---|---|---|
| ~50 | 0 | 2 (20% time) | Checklist plus vendor defaults | Champions overloaded |
| ~200 | 4–6 | 1 per team | Gateway plus policy as code | Evals and cost need dedicated people |
| ~1,000 | 8–12 (three squads) | Formalized guild | Full platform plus council | Absorbed into the IDP; the name disappears |

The column to read in that table is the last one. The three sizes aren't three identities, they're three stages. What tells you to move down a row is whether the upgrade signal has appeared, not whether the company has hit a headcount number.

---

## 4. The champion system, and how it usually gets broken

Once the headcount is settled, the thing most likely to collapse isn't the platform team. It's the line that connects platform and domain. The champion is that line.

A champion isn't a title. It's a job with a job description. The way it gets broken is always the same: name the most senior person, give them no time, put it in no one's review, and watch the whole thing become nominal within six months.

It usually looks good while it's happening. Name the people, open a channel, announce that the guild exists — every ceremony you need is done inside a day. But the time, the output, and the review take a whole quarter, so most organizations only ever do the first day's part.

**Selection criteria** (these matter more than seniority):

| Look for this | Avoid this |
|---|---|
| Already uses agents daily with real output to show | Wants to evaluate new tools, doesn't want to touch anyone else's repo |
| Has written the team's onboarding docs or test infrastructure | Treats champion as a promotion stepping stone, doesn't teach |
| Willing to spend time coaching; turns complaints into requirements | No patience for non-deterministic systems |

Read the two columns together and the direction is obvious: what you want in a champion is someone willing to give away how they work, not the person who is best with the tools.

**Time and evaluation:**

- Put the 20% in their OKRs. This isn't "passion after hours." It's work that goes into the quarterly goals, where a manager will track it. A champion system with no time commitment is not a champion system.
- Evaluate on **the team's adoption metrics**, not individual output: the team's percentage of tasks delegated, the drop in retry rate, the freshness of AGENTS.md. A champion succeeds when the team gets stronger, not when they personally get good at it.
- **Rotate half of them every quarter.** Rotation isn't a demotion, it's a knowledge diffusion mechanism. Two years out you don't want ten super-champions; you want half the engineering org to have done the job.

**How the guild runs:** biweekly, with only three kinds of content. The first is internal demos, so everyone gets to see how the paved road is actually used. The second is a pain-point list that takes whatever the domain teams are stuck on back into the platform backlog. The third, and the most valuable, is **failure stories.**

Where an agent screwed something up and why is the scarcest learning material in the entire organization. Every team eventually works out the successful patterns on its own. But if nobody tells the story of the time it went wrong, the next team just walks into it the same way.

---

## 5. Merging with what you already have

Most companies aren't starting from a blank page. You already have a DevEx team, a platform team, or SRE. So who owns agentic?

This turns into a political argument very easily, so pull it back to a question about organizational capability. There are only two things to decide. First, whether you have an internal developer platform (IDP) team — the internal, self-service platform your engineers already build on. Second, if you do, whether they have the room right now to take on another mission. Use this tree:

```mermaid
flowchart TD
    Q1{"Do you have an internal developer<br/>platform (IDP) team?"} -->|No| N1["Start an Agentic Platform Pod<br/>it becomes your platform team later"]
    Q1 -->|Yes| Q2{"Do they have capacity<br/>for a new mission?"}
    Q2 -->|Yes| A1["Fold agentic into the IDP mission<br/>add 2–3 headcount"]
    Q2 -->|No| A2["Start a separate pod<br/>merge back in 12–18 months"]
    A2 --> M["Merge conditions: runtime stable,<br/>governance in CI, champions self-sustaining"]
    style A1 fill:#d4edda,stroke:#2e7d32
```

The principle in one line: **an agentic platform is the next chapter of your IDP, not a parallel universe.** They will merge eventually. Separating is only a concession to startup speed, which is why an independent pod should share backlog tooling and design review with the IDP from day one. When the merge day arrives, the only thing you have to move is people, not two sets of process and two cultures.

SRE works the same way: reuse the existing observability stack for agent observability — traces, metrics, alerting. Don't let the platform team rebuild it. That stack is already running in production, and an agent is just one more kind of thing to observe.

The only difference is a handful of new signals. Run ID stitches one complete agent run together, tool call shows which external capabilities it reached for, retry shows how unstable it is, and token usage pulls cost into the same picture.

---

## 6. Budget and the pitch: what to tell a CFO

The hard part of pitching a CFO isn't the size of the number. It's that this money has three components that behave nothing like each other, and presenting them as one thing gets the whole proposal sent back.

Budget splits into three buckets, and the third is the one that gets left out:

| Bucket | Contents | Behavior |
|---|---|---|
| **Run** | Tokens, vendor subscriptions, sandbox compute | Grows linearly with adoption; needs quota management |
| **Build** | Platform team headcount | Fixed; 4–6 people to start |
| **Enable** | Champions' 20% time, training, the guild | An invisible cost — if you don't budget it, day-to-day work eats it |

Enable gets left out because it never appears on a quote. What it spends is the time of engineers you already employ, and nothing that wasn't budgeted gets reconciled at the end of the year.

**The ROI narrative.** Don't use "this replaces N engineers." It frightens the team, and it isn't accurate anyway. My claim is that agentic engineering redistributes engineering attention rather than removing people.

Use **attention leverage** instead: the drop in human review minutes per PR, multiplied by total PR volume, equals engineering attention freed. That is, what you're selling the CFO isn't saved salary, it's more capacity out of the same people. Pair it with evidence that production escape rate — the share of problems that only get caught once they've reached production — held flat, which proves you didn't buy speed with quality.

**Managing time expectations.** Don't promise cost reduction in year one. Promise a measurable curve on delivery speed and quality. Cost per successful task only becomes meaningful as a comparison in year two, because year one is still paying the retry tax: the tokens and the time burned on failed attempts. That number comes down as the harness and the context improve. Year one's retry tax is tuition, not waste (see part three).

One red line to close on: if the proposal contains "we will build our own agent runtime," delete it. The reasoning is in the overview's buy-versus-build section. In short, that's a bet against an entire industry's capital expenditure, and not one of the three buckets above can cover a seat at that table.

---

## 7. Talent: hiring, transitions, and the junior path

That's the money settled. What's left is the people: how you hire from outside, how you convert from inside, and how you grow juniors. Of the three, the third is the one that most often gets skipped.

**Hiring.** The keyword in the job description is not prompt engineering. Look for people who've built developer tooling, CI, test infrastructure, or documentation systems. The reason is that what this role handles every day is how engineers wire an agent into an existing workflow, not how to write a prompt that reads nicely.

On top of that you want one trait that's hard to quantify and matters enormously: **the temperament to debug non-deterministic systems.** Agent failures don't reproduce cleanly, and that's a very different experience from debugging traditional software. Suppose the same task runs twice, passes once, fails once, and the two diffs don't even match. The person you want is the one who goes and measures the distribution, not the one who loses their temper first.

**Internal transfers beat external hiring.** The first two or three people on the platform team come most smoothly from internal DevEx or infra, because they already understand the systems and the politics. Save external hiring for genuinely new skills: eval engineering and FinOps. The first has to be able to put a number on whether an agent's output is any good. The second has to manage token spend the way you'd manage a cloud bill.

**The junior path** (turning the overview's argument into a ladder):

1. **Month 1:** review agent PRs with a checklist. The goal isn't catching errors; it's building an instinct for what "correct" looks like.
2. **Months 2–3:** write eval cases. Defining what "right" means is the best training in technical judgment there is.
3. **Months 4–6:** own the maintenance of a golden workflow, and start contributing to the team's adoption metrics.

What this path produces isn't someone who is better with the tools. It's an engineer who can define problems and acceptance criteria — precisely the scarcest capability of the agent era. The implementation can be delegated, but someone still has to judge what counts as correct, where the risk sits, and which parts a human has to look at.

Organizations that skip it and reserve all review for seniors will discover in three years that they have no succession bench.

---

## 8. Closing

The goal of the org design compresses into one sentence:

> **Domain teams keep context and ownership. The platform team keeps leverage and guardrails. Champions keep the two talking.**

Go back to the three forms of organizational gravity from the first section. They don't go away. Budget, scarce talent, and the demand for control will push you again every quarter, and every time someone will suggest that you just stand up a team. What this org chart is really for is making sure that each time you get pushed, you can still answer the question: who owns this?

The next piece covers what the platform team actually builds: the three-tier AGENTS.md architecture, a minimum viable MCP gateway, sandbox selection, and the brownfield renovation playbook.

---

### The series

1. [Overview: Don't Build Your Own Devin](https://fantasybz.medium.com/dont-build-your-own-devin-org-strategy-and-a-90-day-blueprint-for-agentic-engineering-8187e7ec80f9)
2. **1. Org Design (this piece)**
3. [2. The Harness Blueprint: making your system legible to agents](https://fantasybz.medium.com/agentic-engineering-part-2-the-harness-blueprint-making-your-system-legible-to-agents-3facc281f633)
4. [3. Evals, Unit Economics, and Scaling: running agents like a product](https://fantasybz.medium.com/agentic-engineering-part-3-evals-unit-economics-and-scaling-running-agents-like-a-product-1cb1855a2046)

---

### On how this piece was made

The initial concept and chapter structure are the author's; the prose was drafted in collaboration with AI (Claude), then reviewed and revised section by section by the author before publication. The views and judgments are the author's own, as is responsibility for the content.

---

*Originally published in Chinese: [中文版](https://fantasybz.medium.com/agentic-engineering-%E4%B8%89%E9%83%A8%E6%9B%B2-%E4%B8%80-%E8%AA%B0%E4%BE%86%E5%81%9A-platform-federation-%E7%9A%84%E7%B5%84%E7%B9%94%E8%A8%AD%E8%A8%88%E5%AF%A6%E5%8B%99-9d9353ef7f3a). Also on [Medium @fantasybz](https://medium.com/@fantasybz) — if you're designing the org structure for Agentic Engineering, I'd like to hear from you.*
