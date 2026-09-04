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

# Agentic Engineering, Part 1 — Who Does This? Platform Plus Federation in Practice

> **TL;DR** — The first deep dive from [Don't Build Your Own Devin](https://fantasybz.medium.com/dont-build-your-own-devin-org-strategy-and-a-90-day-blueprint-for-agentic-engineering-8187e7ec80f9). The overview's conclusion: don't stand up a central agent team, stand up a small Agentic Platform team. This piece takes "how do you actually organize it" down to the level you could walk into a headcount meeting with: real org charts at three company sizes, how to select and evaluate champions, how to merge with your existing DevEx or SRE function, and the budget narrative that works with a CFO.

> Series: [Overview](https://fantasybz.medium.com/dont-build-your-own-devin-org-strategy-and-a-90-day-blueprint-for-agentic-engineering-8187e7ec80f9) → **1. Org Design (this piece)** → [2. The Harness Blueprint](https://fantasybz.medium.com/agentic-engineering-part-2-the-harness-blueprint-making-your-system-legible-to-agents-3facc281f633) → 3. Evals and Unit Economics (coming soon)

---

## 1. Why organizations drift into the wrong design

The overview named four failure modes. The central agent team is the one worth unpacking — not because it's a stupid decision, but because it's what organizational gravity produces on its own. Three forces push you there:

- **Budget gravity.** AI money is usually new money, and new money needs a cost center to hang on. So: "let's create a team first and figure it out later."
- **Scarcity gravity.** Early on, few people understand agents, so concentrating them *looks* like the efficient allocation.
- **Control gravity.** Legal and security want a single point of contact they can govern. A central team hands them a convenient handle.

All three forces are real. But what they optimize for is manageability, not output. Conway's law applies in reverse here: the delivery system you end up with will look like your org chart — and a central team's org chart produces a ticket-queue delivery system.

> If you want a self-service system, you have to draw a self-service org chart first.

---

## 2. Platform plus federation, in full

The overview gave the concept. Here it is at RACI resolution across the three roles:

📌【在此插入圖 diagram-01.png】

📌【在此插入表 table-01.png】

The most important cell in that table is the last row: **production ownership always stays with the domain team.** Any design that routes "the agent's code broke production" to the platform team will collapse into finger-pointing at the first incident.

---

## 3. Real org charts at three sizes

### 50 engineers: the no-team version

- Zero dedicated headcount. Two champions at 20% time each, plus a sponsor (a VP or senior EM).
- Adopt a SaaS runtime and the vendor's default sandbox. Govern with a checklist; don't build a gateway.
- **Upgrade signal:** when champions are spending more than 30% of their time helping other teams wire up tooling, it's time to open a pod.

### 200 engineers: a 4–6 person platform pod

📌【在此插入圖 diagram-02.png】

The key thing about skill mix: this is a **product team, not a research team**. Its product is the paved road and its customers are internal engineers. So hire people who have built developer tooling, CI, and test infrastructure — not people with model research backgrounds. And borrow that half-person of security: giving the security team a stake up front is far cheaper than getting sent back by an audit later.

### 1,000 engineers: a platform group with specialization

- Platform grows to 8–12, split into three squads: **runtime and environment**, **context and tools**, **eval and FinOps**.
- Add a cross-functional virtual security council (one person each from security, legal, and platform; monthly is enough).
- What doesn't change: even at this size, there is no "team that writes code for other teams using agents."

The three tiers side by side:

📌【在此插入表 table-02.png】

---

## 4. The champion system, and how it usually gets broken

A champion isn't a title. It's a job with a job description. The way it gets broken is always the same: name the most senior person, give them no time, put it in no one's review, and watch the whole thing become nominal within six months.

**Selection criteria** (these matter more than seniority):

📌【在此插入表 table-03.png】

**Time and evaluation:**

- Put the 20% in their OKRs. Not "passion after hours." A champion system with no time commitment is not a champion system.
- Evaluate on **the team's adoption metrics**, not individual output: the team's percentage of tasks delegated, the drop in retry rate, the freshness of AGENTS.md. A champion succeeds when the team gets stronger, not when they personally get good at it.
- **Rotate half of them every quarter.** Rotation isn't a demotion, it's a knowledge diffusion mechanism. Two years out you don't want ten super-champions; you want half the engineering org to have done the job.

**How the guild runs:** biweekly, with only three kinds of content — internal demos, a pain-point list that goes back into the platform backlog, and the most valuable one: **failure stories.** Where an agent screwed something up and why is the scarcest learning material in the entire organization.

---

## 5. Merging with what you already have

Most companies already have a DevEx team, a platform team, or SRE. Who owns agentic? Use this tree:

📌【在此插入圖 diagram-03.png】

The principle in one line: **an agentic platform is the next chapter of your IDP, not a parallel universe.** They will merge eventually; separating is only a concession to startup speed. Which is why an independent pod should share backlog tooling and design review with the IDP from day one.

SRE works the same way: reuse the existing observability stack for agent observability — traces, metrics, alerting. Don't let the platform team rebuild it. The only difference is a handful of new signals: run ID, tool call, retry, and token usage.

---

## 6. Budget and the pitch: what to tell a CFO

Budget splits into three buckets, and the third is the one that gets left out:

📌【在此插入表 table-04.png】

**The ROI narrative.** Don't use "this replaces N engineers." It frightens the team, and it isn't accurate anyway. Use **attention leverage** instead: the drop in human review minutes per PR, multiplied by total PR volume, equals engineering attention freed. Pair it with evidence that production escape rate held flat, which proves you didn't buy speed with quality.

**Managing time expectations.** Don't promise cost reduction in year one. Promise a measurable curve on delivery speed and quality. Cost per successful task only becomes meaningful as a comparison in year two — year one's retry tax is tuition, not waste (see part three).

One red line to close on: if the proposal contains "we will build our own agent runtime," delete it. The reasoning is in the overview's buy-versus-build section — that's a bet against an entire industry's capital expenditure.

---

## 7. Talent: hiring, transitions, and the junior path

**Hiring.** The keyword in the job description is not prompt engineering. Look for people who've built developer tooling, CI, test infrastructure, or documentation systems — plus one trait that's hard to quantify and matters enormously: **the temperament to debug non-deterministic systems.** Agent failures don't reproduce cleanly, and that's a very different experience from debugging traditional software.

**Internal transfers beat external hiring.** The first two or three people on the platform team come most smoothly from internal DevEx or infra — they already understand the systems and the politics. Save external hiring for genuinely new skills: eval engineering and FinOps.

**The junior path** (turning the overview's argument into a ladder):

1. **Month 1:** review agent PRs with a checklist. The goal isn't catching errors; it's building an instinct for what "correct" looks like.
2. **Months 2–3:** write eval cases. Defining what "right" means is the best training in technical judgment there is.
3. **Months 4–6:** own the maintenance of a golden workflow, and start contributing to the team's adoption metrics.

What this path produces is an engineer who can define problems and acceptance criteria — precisely the scarcest capability of the agent era. Organizations that skip it and reserve all review for seniors will discover in three years that they have no succession bench.

---

## 8. Closing

The goal of the org design compresses into one sentence:

> **Domain teams keep context and ownership. The platform team keeps leverage and guardrails. Champions keep the two talking.**

The next piece covers what the platform team actually builds: the three-tier AGENTS.md architecture, a minimum viable MCP gateway, sandbox selection, and the brownfield renovation playbook.

---

### The series

1. [Overview: Don't Build Your Own Devin](https://fantasybz.medium.com/dont-build-your-own-devin-org-strategy-and-a-90-day-blueprint-for-agentic-engineering-8187e7ec80f9)
2. **1. Org Design (this piece)**
3. [2. The Harness Blueprint: making your system legible to agents](https://fantasybz.medium.com/agentic-engineering-part-2-the-harness-blueprint-making-your-system-legible-to-agents-3facc281f633)
4. 3. Evals, Unit Economics, and Scaling: running agents like a product (coming soon)

---

### On how this piece was made

The initial concept and chapter structure are the author's; the prose was drafted in collaboration with AI (Claude), then reviewed and revised section by section by the author before publication. The views and judgments are the author's own, as is responsibility for the content.

---

*Originally published in Chinese: [中文版](https://fantasybz.medium.com/agentic-engineering-%E4%B8%89%E9%83%A8%E6%9B%B2-%E4%B8%80-%E8%AA%B0%E4%BE%86%E5%81%9A-platform-federation-%E7%9A%84%E7%B5%84%E7%B9%94%E8%A8%AD%E8%A8%88%E5%AF%A6%E5%8B%99-9d9353ef7f3a). Also on [Medium @fantasybz](https://medium.com/@fantasybz) — if you're designing the org structure for Agentic Engineering, I'd like to hear from you.*
