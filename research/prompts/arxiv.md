# arXiv 掃描 agent 的 prompt（每月改日期後照抄）

交給一個 general-purpose agent 在背景跑；不需要瀏覽器。產出 `.context/research/YYYY-MM/arxiv.md`。

```
You are a research agent. Today is {TODAY}. Do a thorough sweep of arXiv for recent papers
(submitted roughly {FROM} to {TODAY}) relevant to a Medium author who writes long-form
Traditional-Chinese articles for Engineering VPs / Staff engineers about "Agentic Engineering":
coding agents, agent harnesses, AGENTS.md/context engineering, MCP/tool gateways, sandboxes,
evals for agents, agent security (prompt injection, privilege escalation, supply chain in
harnesses), agent observability/audit, multi-agent orchestration, unit economics of agents,
AI code review, organizational impact of agents on software teams, developer productivity
studies with agents. {EXTRA_THEMES_FROM_BACKLOG}

Use the arXiv API via WebFetch, e.g.:
https://export.arxiv.org/api/query?search_query=all:%22coding+agent%22&sortBy=submittedDate&sortOrder=descending&max_results=50
Run at least 12 distinct queries covering the themes above ("agent harness", "AGENTS.md" OR
"context engineering", "Model Context Protocol" OR "MCP", "prompt injection agent",
"SWE-bench" OR "software engineering agent benchmark", "LLM-as-a-judge agent evaluation",
"multi-agent software development", "AI code review", "developer productivity LLM agent
empirical", "agent observability audit trail", "sandbox agent execution", "token cost agent
efficiency", "self-evolving agent harness", "spec-driven development LLM"). Also use
https://arxiv.org/list/cs.SE/recent. If export.arxiv.org returns 429, fall back to the
arxiv.org search pages. For the 15–25 most relevant papers, fetch https://arxiv.org/abs/<id>
and read the abstract properly.

Write to {OUT}/arxiv.md:
1. A table of ALL relevant papers (arXiv id, title, date, one-line takeaway, theme cluster).
   Aim for 40+ rows; relevance over volume.
2. "Theme clusters": 6–10 clusters, each with what the cluster collectively says, what is new
   in the last 3 months, and the anchor papers.
3. "Signals worth an article": 8–12 concrete, non-obvious findings or tensions across papers
   that an experienced engineering leader would find surprising or actionable. Cite ids.
Only cite papers you actually saw; never invent ids or numbers. Note when a paper's
submission date and announcement date differ by more than a few weeks.
Final reply: a 10-line summary; the file is the deliverable.
```
