export const meta = {
  name: 'plan-next-three-themes',
  description: 'Propose, judge, select and outline the next three monthly Medium themes (總論 + 三部曲) from the research digests',
  phases: [
    { title: 'Propose', detail: '5 lenses × 4 candidate themes each' },
    { title: 'Merge', detail: 'dedupe into ≤10 distinct candidates' },
    { title: 'Judge', detail: '2 lensed judges + 1 adversarial refuter per candidate' },
    { title: 'Select', detail: 'pick 3, sequence them over the next three months' },
    { title: 'Outline', detail: 'full 總論 + 三部曲 outline per theme, critic, revise' },
    { title: 'Backlog', detail: 'runner-up themes for later months' },
  ],
}

// args: { root: <repo root>, month: 'YYYY-MM' (the research round, e.g. 2026-09), today: 'YYYY-MM-DD',
//         published: ['2026-09-agentic-engineering-platform', ...]   (dirs of the published articles, in series order; current list in research/README.md),
//         months?: ['2026-10', '2026-11', '2026-12'] }                 (the three months to plan; default = the three after `month`)
// Workflow scripts have no Date and cannot import modules, so today comes in as an arg and the digests are read from
// research/<month>/ (the four digest agents write them there; notion_digest.md and community_digest.md are local-only,
// see research/README.md). The raw JSON collect.sh writes to .context/research/<month>/ is NOT read by this workflow.
const ROOT = args.root
const DIR = `${ROOT}/research/${args.month}`
const OUT = DIR
if (!args.today) throw new Error('args.today (YYYY-MM-DD) is required: workflow scripts have no Date')
if (!Array.isArray(args.published) || !args.published.length) throw new Error('args.published (array of published article dirs) is required; see research/README.md for the current list')
const PUBLISHED = args.published.map(d => `${ROOT}/${d}/article.md`)
const nextMonths = (ym, n) => Array.from({ length: n }, (_, i) => {
  const [y, m] = ym.split('-').map(Number)
  const t = y * 12 + (m - 1) + i + 1
  return `${Math.floor(t / 12)}-${String((t % 12) + 1).padStart(2, '0')}`
})
const TARGETS = args.months || nextMonths(args.month, 3)
const INPUTS = `
Read ALL of these files fully before doing anything (use the Read tool; they are long, read them in chunks if needed):
- ${DIR}/style_brief.md  (how the author writes, series format, audience, reception data)
- ${DIR}/x_digest.md  (X/Twitter: top posts from followed accounts, themes, debates, gaps — post count and date range are in the digest header)
- ${DIR}/arxiv.md  (arXiv papers of the last few months, clusters, signals — paper count and date range are in the digest header)
- ${DIR}/community_digest.md  (Taiwanese Facebook groups, the author's own FB/fan-page posts, LinkedIn, Medium stats)
- ${DIR}/notion_digest.md  (the author's OWN Notion: workshop notes, book notes, certification plans, drafts — first-hand material, and corrections to the themes)
Also skim the published articles so you know exactly what is already covered:
${PUBLISHED.map(p => `- ${p}`).join('\n')}
Context: today is ${args.today}. The author (@fantasybz, Kochi Chuang) publishes one THEME per month, each theme = one 總論 (overview, ~18 min read) + 三部曲 (three deep dives, ~8–12 min each), in Traditional Chinese (Taiwan) with an English edition. The next three themes are for ${TARGETS.join(', ')}. Audience: Engineering VPs / EMs / Staff engineers / platform, SRE and QA leads in Taiwan.
`

const PROPOSAL_SCHEMA = {
  type: 'object', required: ['themes'],
  properties: { themes: { type: 'array', minItems: 4, maxItems: 4, items: {
    type: 'object', required: ['slug', 'title_zh', 'title_en', 'thesis_zh', 'why_now', 'evidence', 'author_fit', 'parts', 'overlap_risk'],
    properties: {
      slug: { type: 'string' }, title_zh: { type: 'string' }, title_en: { type: 'string' },
      thesis_zh: { type: 'string', description: 'one-line quotable thesis in Traditional Chinese' },
      why_now: { type: 'string', description: '3–6 sentences: what happened in the last 3 months that makes this urgent' },
      evidence: { type: 'array', minItems: 4, items: { type: 'object', required: ['source', 'ref', 'claim'], properties: { source: { type: 'string', description: 'x | arxiv | facebook | linkedin | medium-stats | notion | article' }, ref: { type: 'string', description: 'URL, arXiv id, group name or post handle+date exactly as it appears in the digest' }, claim: { type: 'string' } } } },
      author_fit: { type: 'string' },
      parts: { type: 'array', minItems: 3, maxItems: 3, items: { type: 'object', required: ['title_zh', 'focus'], properties: { title_zh: { type: 'string' }, focus: { type: 'string' } } } },
      overlap_risk: { type: 'string', description: 'overlap with the published series or with saturated content; how to differentiate' },
    } } } },
}

const MERGE_SCHEMA = {
  type: 'object', required: ['candidates'],
  properties: { candidates: { type: 'array', minItems: 6, maxItems: 10, items: {
    type: 'object', required: ['slug', 'title_zh', 'title_en', 'thesis_zh', 'why_now', 'evidence', 'author_fit', 'parts', 'overlap_risk', 'merged_from'],
    properties: {
      slug: { type: 'string' }, title_zh: { type: 'string' }, title_en: { type: 'string' }, thesis_zh: { type: 'string' }, why_now: { type: 'string' },
      evidence: { type: 'array', items: { type: 'object', required: ['source', 'ref', 'claim'], properties: { source: { type: 'string' }, ref: { type: 'string' }, claim: { type: 'string' } } } },
      author_fit: { type: 'string' },
      parts: { type: 'array', minItems: 3, maxItems: 3, items: { type: 'object', required: ['title_zh', 'focus'], properties: { title_zh: { type: 'string' }, focus: { type: 'string' } } } },
      overlap_risk: { type: 'string' },
      merged_from: { type: 'array', items: { type: 'string' } },
    } } } },
}

const JUDGE_SCHEMA = {
  type: 'object', required: ['scores', 'rationale', 'must_fix'],
  properties: {
    scores: { type: 'object', required: ['demand', 'fit', 'differentiation', 'decomposability', 'durability'],
      properties: { demand: { type: 'number' }, fit: { type: 'number' }, differentiation: { type: 'number' }, decomposability: { type: 'number' }, durability: { type: 'number' } } },
    rationale: { type: 'string' }, must_fix: { type: 'string' },
  },
}
const REFUTE_SCHEMA = {
  type: 'object', required: ['refuted', 'strongest_objection', 'severity', 'fixable_by'],
  properties: { refuted: { type: 'boolean' }, strongest_objection: { type: 'string' }, severity: { type: 'number', description: '1 (nitpick) – 5 (fatal)' }, fixable_by: { type: 'string' } },
}
const SELECT_SCHEMA = {
  type: 'object', required: ['selected', 'runners_up', 'sequencing_rationale'],
  properties: {
    selected: { type: 'array', minItems: 3, maxItems: 3, items: { type: 'object', required: ['slug', 'month', 'title_zh', 'title_en', 'thesis_zh', 'why_this', 'adjustments', 'parts'],
      properties: { slug: { type: 'string' }, month: { type: 'string', description: TARGETS.join(' | ') }, title_zh: { type: 'string' }, title_en: { type: 'string' }, thesis_zh: { type: 'string' }, why_this: { type: 'string' }, adjustments: { type: 'string', description: 'changes made in response to judges/refuter' },
        parts: { type: 'array', minItems: 3, maxItems: 3, items: { type: 'object', required: ['title_zh', 'focus'], properties: { title_zh: { type: 'string' }, focus: { type: 'string' } } } } } } },
    runners_up: { type: 'array', items: { type: 'object', required: ['slug', 'title_zh', 'reason'], properties: { slug: { type: 'string' }, title_zh: { type: 'string' }, reason: { type: 'string' } } } },
    sequencing_rationale: { type: 'string' },
  },
}
const FILE_SCHEMA = { type: 'object', required: ['path', 'summary'], properties: { path: { type: 'string' }, summary: { type: 'string' } } }
const CRITIC_SCHEMA = { type: 'object', required: ['issues', 'overall'], properties: { issues: { type: 'array', items: { type: 'object', required: ['severity', 'where', 'problem', 'fix'], properties: { severity: { type: 'string', description: 'blocker | major | minor' }, where: { type: 'string' }, problem: { type: 'string' }, fix: { type: 'string' } } } }, overall: { type: 'string' } } }

const LENSES = [
  { key: 'sequel', prompt: 'LENS: Natural sequel. What does a reader who just finished the Agentic Engineering trilogy (org / harness / evals-economics) need NEXT, 1–3 months later, once the pilot is running? Follow the trilogy\'s own forward references and unanswered questions.' },
  { key: 'craft', prompt: 'LENS: The author\'s credible ground. Their proven strengths (Medium stats, FB voice) are software testing/QA philosophy, observability/SRE, Kubernetes/cloud-native, and engineering culture. Propose themes that apply that ground to the agent era, where the author can speak with more authority than generic AI commentators.' },
  { key: 'community', prompt: 'LENS: Taiwanese practitioner pain. Use the Facebook-group and Claude-Taiwan evidence: what are engineers in Taiwan actually struggling with or arguing about right now, and which of those has no serious Traditional-Chinese long-form treatment yet?' },
  { key: 'research', prompt: 'LENS: Research frontier vs industry folklore. Use the arXiv digest: where do controlled studies contradict what X influencers and vendors claim (context files, skills, MCP, code review, evals, security)? Propose themes that let the author be the person who reads the papers so the VP does not have to.' },
  { key: 'strategic', prompt: 'LENS: Contrarian strategist. What will an Engineering VP in Taiwan need to decide in Q4 2026 / Q1 2027 (budget season, vendor lock-in, seat economics, security incidents, hiring/junior pipeline, regulation) that nobody is writing about in Chinese? Prefer themes with a one-line thesis a VP can repeat in a steering meeting.' },
]

phase('Propose')
const proposals = await parallel(LENSES.map(l => () => agent(
  `${INPUTS}\n${l.prompt}\n\nPropose exactly 4 candidate THEMES for the author's next monthly series. Each theme must be big enough for one 總論 plus three distinct deep dives, must not re-cover what the four published articles already say (extending is fine, repeating is not), and must be backed by evidence you actually saw in the digests (quote refs exactly: URLs, arXiv ids, group names, handles). Titles and thesis in Traditional Chinese (Taiwan usage, keep English technical terms). Be concrete and opinionated; avoid generic "AI transformation" themes.`,
  { label: `propose:${l.key}`, phase: 'Propose', schema: PROPOSAL_SCHEMA }
)))
const allThemes = proposals.filter(Boolean).flatMap((p, i) => p.themes.map(t => ({ ...t, lens: LENSES[i].key })))
log(`${allThemes.length} candidate themes proposed`)

phase('Merge')
const merged = await agent(
  `${INPUTS}\nHere are ${allThemes.length} candidate themes proposed by five analysts with different lenses (JSON below). Merge duplicates and near-duplicates into a single list of 6–10 DISTINCT candidates. When merging, keep the strongest title/thesis, union the evidence (deduplicate refs), and record merged_from slugs. Do not drop a genuinely distinct candidate just to reach a count; do not invent new ones. Keep Traditional Chinese for title_zh/thesis_zh.\n\n${JSON.stringify(allThemes, null, 1)}`,
  { label: 'merge-dedupe', phase: 'Merge', schema: MERGE_SCHEMA, effort: 'high' }
)
const candidates = merged ? merged.candidates : []
log(`${candidates.length} distinct candidates after merge`)

phase('Judge')
const JUDGES = [
  { key: 'reader', prompt: 'You are an Engineering VP at a 300-person Taiwanese software company who reads this author. Score DEMAND (would you read all four pieces and forward them?) and FIT (does this author have standing to write it?) with the most weight; score the other three honestly.' },
  { key: 'editor', prompt: 'You are a senior tech editor. Score DIFFERENTIATION (vs the published series and vs what is already saturated on X/Medium), DECOMPOSABILITY (does it split cleanly into 總論 + three non-overlapping deep dives, each with a reference implementation or decision artefact?), and DURABILITY (still valuable when published 1–3 months from now, not a news reaction) with the most weight.' },
]
const judged = await pipeline(candidates,
  c => parallel([
    ...JUDGES.map(j => () => agent(
      `${INPUTS}\n${j.prompt}\n\nScore this candidate theme 1–10 on demand, fit, differentiation, decomposability, durability. Cite the digests for your claims. In must_fix, say what would have to change for it to score higher.\n\nCANDIDATE:\n${JSON.stringify(c, null, 1)}\n\nOTHER CANDIDATES (for relative judgement only):\n${JSON.stringify(candidates.filter(o => o.slug !== c.slug).map(o => ({ slug: o.slug, title_zh: o.title_zh, thesis_zh: o.thesis_zh })), null, 1)}`,
      { label: `judge:${j.key}:${c.slug}`, phase: 'Judge', schema: JUDGE_SCHEMA }
    )),
    () => agent(
      `${INPUTS}\nYou are an adversarial reviewer. Try to REFUTE this candidate theme as a choice for a monthly 總論+三部曲 series: is it already covered by the published articles? Is the evidence thinner than claimed (check the refs against the digests)? Is it a news reaction that will be stale by publication? Is it really four articles of material, or one? Is the author credible on it? Default to refuted=true if you are uncertain. Severity 5 = fatal, 1 = nitpick. If fixable, say how.\n\nCANDIDATE:\n${JSON.stringify(c, null, 1)}`,
      { label: `refute:${c.slug}`, phase: 'Judge', schema: REFUTE_SCHEMA, effort: 'high' }
    ),
  ]).then(([a, b, r]) => ({ candidate: c, judges: [a, b].filter(Boolean), refute: r }))
)
const scored = judged.filter(Boolean).map(j => {
  const totals = j.judges.map(x => x.scores.demand + x.scores.fit + x.scores.differentiation + x.scores.decomposability + x.scores.durability)
  const avg = totals.length ? totals.reduce((a, b) => a + b, 0) / totals.length : 0
  return { ...j, avg }
})
scored.sort((a, b) => b.avg - a.avg)
log('scores: ' + scored.map(s => `${s.candidate.slug}=${s.avg.toFixed(1)}${s.refute && s.refute.refuted ? '(refuted s' + s.refute.severity + ')' : ''}`).join(', '))

phase('Select')
const selection = await agent(
  `${INPUTS}\nBelow are the judged candidates (two lensed judges with scores + rationale, one adversarial refutation each). Select the THREE themes for ${TARGETS.join(', ')}. Rules: the three must be clearly different from each other (not three angles on the same subject); each must survive its refutation or be adjusted so it does (write the adjustment); sequence them by dependency and by season (e.g. Q4 = budget season, KubeCon NA in November, year-end retros; the published series' months are in their directory names). Refine title_zh / thesis_zh / the three part titles so they are ready for the outline writers. List every non-selected candidate under runners_up with a one-sentence reason (to seed a backlog). Traditional Chinese for all zh fields.\n\n${JSON.stringify(scored.map(s => ({ avg: s.avg, candidate: s.candidate, judges: s.judges, refute: s.refute })), null, 1)}`,
  { label: 'select-3', phase: 'Select', schema: SELECT_SCHEMA, effort: 'high' }
)
if (!selection) throw new Error('selection failed')
log('selected: ' + selection.selected.map(s => `${s.month} ${s.title_zh}`).join(' | '))

phase('Outline')
const outlined = await pipeline(selection.selected,
  s => agent(
    `${INPUTS}\nWrite the full article PLAN for this monthly theme as a Markdown file at ${OUT}/${s.month}-${s.slug}.md (use the Write tool; create the directory if needed). Write it in Traditional Chinese (Taiwan usage, English technical terms untranslated, single "—" dash only, never "——"). Follow the author's format from style_brief.md exactly. The file must contain:
1. 主題總覽: month, slug, title_zh, title_en, 一句話論點 (thesis), 目標讀者, 為什麼是現在 (with dated evidence), 與已發布三部曲的關係 (what it builds on, what it must NOT repeat), 反模式清單 (5–8 named anti-patterns the series will call out), 本主題的歷史類比 (DevOps/CI/testing-history analogy if a good one exists).
2. 總論 outline: title, draft TL;DR paragraph (in the author's voice), 系列導覽 line, then 10–12 sections numbered 一、二、… each with 3–6 bullet points of actual content (claims, numbers, sources), the decision artefacts (tables / decision tree / gate table / 90-day plan) and the mermaid figures to draw (name each figure and what it shows), the quotable one-liner, and the References list (only sources that appear in the digests: URLs, arXiv ids with titles, X posts with handle+date).
3. 三部曲 outlines: for each of the three deep dives: title, TL;DR draft, 6–8 sections with 3–5 bullets each, the reference implementation / code or config snippet ideas (Before/After style), tables and figures, references. Make sure the three parts do not overlap each other or the 總論 beyond a one-paragraph recap.
4. 寫作前要補的證據: 5–10 specific things to verify or collect before drafting (numbers to re-check, papers to read in full, community posts to quote with permission, own experiments to run).
5. 英文版注意事項: title_en and anything that needs adapting for the English edition.
6. 發布與推廣: suggested Medium topics (5 tags), which figure should be the cover, and the FB fan-page / X post hooks (the digest shows FB shares drive most reads).
Be concrete and opinionated; every section needs real content, not placeholders. Return the path and a 5-line summary.

THEME:\n${JSON.stringify(s, null, 1)}`,
    { label: `outline:${s.slug}`, phase: 'Outline', schema: FILE_SCHEMA, effort: 'high' }
  ),
  (f, s) => agent(
    `${INPUTS}\nYou are a rigorous critic. Read the article plan at ${f.path} and check it against: (a) style_brief.md (format, voice, series shape, dash rule, Traditional Chinese Taiwan usage); (b) the published articles (flag any section that repeats them instead of extending); (c) the four digests (every cited source/ref/number must actually exist there; flag anything invented or misquoted); (d) internal overlap between the 總論 and the three parts, and between the parts; (e) whether each part gives a Staff engineer or VP something they can act on (a reference implementation, a decision table, a gate); (f) whether the thesis is genuinely arguable and not a platitude. List issues with severity blocker/major/minor, where, problem, and a concrete fix.`,
    { label: `critic:${s.slug}`, phase: 'Outline', schema: CRITIC_SCHEMA, effort: 'high' }
  ).then(c => ({ file: f, critic: c })),
  (x, s) => agent(
    `${INPUTS}\nRevise the article plan at ${x.file.path} in place (Edit/Write tools) to resolve every blocker and major issue below, and the minor ones where cheap. Do not shorten the plan; keep the structure. Keep Traditional Chinese, single "—" dash. After editing, re-read the file once to confirm it is coherent. Return the path and a summary of what changed.\n\nISSUES:\n${JSON.stringify(x.critic, null, 1)}`,
    { label: `revise:${s.slug}`, phase: 'Outline', schema: FILE_SCHEMA, effort: 'high' }
  ).then(r => ({ theme: s, path: r ? r.path : x.file.path, summary: r ? r.summary : x.file.summary, critic: x.critic }))
)

phase('Backlog')
const backlog = await agent(
  `${INPUTS}\nWrite ${OUT}/backlog.md (Write tool) in Traditional Chinese: a topic backlog for months after ${TARGETS[TARGETS.length - 1]}. Input: the runner-up candidates and the selection rationale below, plus the "gaps"/"signals"/"opportunities" sections of the four digests. For each backlog entry: title_zh, one-paragraph pitch, why it did not make the top three, what evidence would promote it, and the earliest sensible month. Order by promise. Also add a short section "訊號監看清單": 10–15 concrete signals (accounts, arXiv queries, FB groups, conference dates) to watch so the backlog can be re-ranked monthly. Return path and summary.\n\nSELECTION:\n${JSON.stringify(selection, null, 1)}`,
  { label: 'backlog', phase: 'Backlog', schema: FILE_SCHEMA }
)

return { selection, outlined: outlined.filter(Boolean).map(o => ({ month: o.theme.month, slug: o.theme.slug, title_zh: o.theme.title_zh, path: o.path, summary: o.summary, critic_overall: o.critic ? o.critic.overall : '' })), backlog, candidates_considered: scored.map(s => ({ slug: s.candidate.slug, title_zh: s.candidate.title_zh, avg: s.avg, refuted: s.refute ? s.refute.refuted : null, severity: s.refute ? s.refute.severity : null })) }