export const meta = {
  name: 'review-outlines',
  description: 'Second-pass adversarial review of the monthly theme outlines: 4 lensed critics per outline → revise → verify (loop ≤2) → Mermaid figures companion file',
  phases: [
    { title: 'Critique', detail: 'evidence auditor + VP reader + editor + diagram designer per outline' },
    { title: 'Revise', detail: 'apply blockers/majors in place (≤2 rounds with Verify); then write <outline>.figures.md with Mermaid for every figure' },
    { title: 'Verify', detail: 'check fixes landed, no new invented citations' },
  ],
}

// args: { root: <repo root>, month: 'YYYY-MM', today: 'YYYY-MM-DD',
//         published: ['2026-09-agentic-engineering-platform', ...]   (dirs of the published articles; current list in research/README.md),
//         files: ['research/YYYY-MM/2026-10-....md', ...]            (one outline per run: 12 critics on a 100K-char outline hit the session limit),
//         lenses?: ['evidence', 'reader', 'diagram', 'editor']       (default: all four),
//         skipFigures?: bool                                          (skip the .figures.md stage),
//         preIssues?: { '<basename>.md': [ {severity, where, problem, fix}, ... ] }  (critiques saved from an interrupted run, merged in so that lens need not rerun) }
// Workflow scripts have no Date and cannot import modules: `today` comes in as an arg, and the CONTEXT skeleton, MERMAID_RULES
// and the three schemas below are the CANONICAL copy that finish-outline.js and write-article.js duplicate — change them here first.
const ROOT = args.root
const DIR = `${ROOT}/research/${args.month}`
const FILES = args.files.map(f => (f.startsWith('/') ? f : `${ROOT}/${f}`))
if (!args.today) throw new Error('args.today (YYYY-MM-DD) is required: workflow scripts have no Date')
if (!Array.isArray(args.published) || !args.published.length) throw new Error('args.published (array of published article dirs) is required; see research/README.md for the current list')
const PUBLISHED = args.published.map(d => `${ROOT}/${d}/article.md`)

// The MERMAID.md numbers, written once and interpolated into every prompt below so the diagram lens, the revise step and
// the figures step cannot drift from each other. Same numbers research/scripts/mermaid_check.sh enforces.
const MERMAID_RULES = `the YAML frontmatter config block at the top (theme base, the themeVariables colours, flowchart spacing, subGraphTitleMargin; NO fontFamily) — never %%{init}%%; classDef own/buy/bad/human applied with class, no per-node style lines; layout width 500–900 CSS px and aspect (height/width) 0.5–1.5; ≤ 12 nodes; ≤ 3 lines × 14 CJK chars per node using <br/>; edge labels ≤ 6 chars; TB for > 5 nodes, ≤ 4 nodes per rank; fontSize 16px; no emoji; when subgraphs use direction TB, wire subgraph to subgraph (an inner node connected to the outside breaks direction TB); the two-column pattern (LR with two direction-TB subgraphs) for short linear flows`

const CONTEXT = `
Today is ${args.today}. The author (@fantasybz, Kochi Chuang) publishes one THEME per month on Medium: one 總論 (overview, ~18 min read) + 三部曲 (three deep dives, 8–12 min each), in Traditional Chinese (Taiwan usage, English technical terms kept), plus an English edition. Audience: Engineering VPs / EMs / Staff engineers / platform, SRE and QA leads in Taiwan.
Reference files (Read them; long files can be read in chunks):
- ${DIR}/style_brief.md   (format and voice the outline must follow)
- ${DIR}/selection.md     (why this theme was chosen, the judges' objections, the adjustments it must honour, and the Notion 補充 section with first-hand material and corrections)
- ${DIR}/arxiv.md, ${DIR}/x_digest.md, ${DIR}/community_digest.md, ${DIR}/notion_digest.md  (the ONLY allowed sources for numbers and citations; ONLY the evidence-auditor lens and the revise agent read these in full — other lenses must NOT read them, to keep token use down)
- ${ROOT}/MERMAID.md  (the Mermaid diagram standard every figure must follow)
- Published articles that must not be repeated: ${PUBLISHED.join(', ')}
Standard: the highest. This plan will be handed to the author to write four long-form pieces from; every claim must be traceable, every section must carry real content, and the Traditional Chinese must read like a Taiwanese engineer wrote it (single "—" dash only, never "——").
`

const ISSUES_SCHEMA = {
  type: 'object', required: ['issues', 'overall', 'verdict'],
  properties: {
    issues: { type: 'array', items: { type: 'object', required: ['severity', 'where', 'problem', 'fix'],
      properties: { severity: { type: 'string', description: 'blocker | major | minor' }, where: { type: 'string', description: 'exact heading / table row / sentence' }, problem: { type: 'string' }, fix: { type: 'string', description: 'concrete replacement text or action' } } } },
    overall: { type: 'string' },
    verdict: { type: 'string', description: 'ready | needs-revision | rewrite' },
  },
}
const FILE_SCHEMA = { type: 'object', required: ['path', 'summary', 'applied', 'skipped'], properties: { path: { type: 'string' }, summary: { type: 'string' }, applied: { type: 'number' }, skipped: { type: 'array', items: { type: 'string' } } } }
const VERIFY_SCHEMA = { type: 'object', required: ['pass', 'remaining', 'new_problems'], properties: { pass: { type: 'boolean' }, remaining: { type: 'array', items: { type: 'string' } }, new_problems: { type: 'array', items: { type: 'string' } } } }

const LENSES = [
  { key: 'evidence', effort: 'high', prompt: `LENS: Evidence auditor. Go through the outline claim by claim. For EVERY number, arXiv id, X post, Facebook post, Medium stat or Notion note it cites, find it in the digests and check: does the digest actually say that? Is the domain right (a non-coding benchmark presented as coding-agent evidence is a blocker)? Is the number rounded or inflated? Is the source's own caveat dropped? List anything invented, misquoted, mismatched, or uncheckable as blocker/major. Also flag claims stated as fact with no source at all.` },
  { key: 'reader', effort: 'high', prompt: `LENS: The reader. (Read only the outline, style_brief.md and selection.md — do not open the digests.) You are an Engineering VP at a 300-person Taiwanese software company who has read the author's published pieces. For each of the four planned pieces: would you read it to the end and forward it to your staff engineers? Where does it lose you? Is the thesis genuinely arguable or a platitude? What question would you ask that the plan cannot answer? Which decision artefacts (tables, gates, checklists, reference implementations) are real and which are placeholders? Name the single most valuable and the single weakest section of each piece.` },
  { key: 'diagram', effort: 'high', prompt: `LENS: Diagram designer. (Read only the outline and MERMAID.md — do not open the digests.) Read ${ROOT}/MERMAID.md (the Mermaid standard: ${MERMAID_RULES}). For EVERY figure the outline plans: does it have complete Mermaid source that follows the standard? Would it be readable on a phone at 700px? Is the figure actually needed (would a table or a sentence be clearer)? Does the 總論 have 10–14 figures and each part 4–6, each with a one-sentence caption? Mermaid source will be written to a companion <outline>.figures.md by a later stage, so do NOT flag missing source; instead flag figure SPECS that cannot be drawn within the standard (too many nodes, no clear caption, duplicates another figure, better as a table) as major, and layout violations (wide LR chains, > 12 nodes, long labels, per-node style instead of classDef, emoji, %%{init}%% or fontFamily inside the frontmatter, subgraph inner nodes wired to outside nodes which breaks direction TB) as major, and propose the corrected Mermaid source in the fix field. Do NOT try to render anything (no browser, no mermaid-cli): this is a static review; the author runs research/scripts/mermaid_check.sh on every figure afterwards.` },
  { key: 'editor', effort: 'high', prompt: `LENS: Senior tech editor. (Read only the outline, style_brief.md, selection.md and the published articles' headings — do not open the digests.) Check (a) format against style_brief.md: TL;DR, 系列導覽, Chinese-numeral section numbering, 結語 with a quotable line, 系列文章 / References / AI 協作說明 tail, single "—" dash, Traditional Chinese Taiwan usage (flag mainland terms and translationese); (b) overlap with the published articles (repeating instead of extending is a major) and between the 總論 and the three parts and among the parts; (c) whether the four pieces plus an English edition can realistically be written in one month by one author with an AI collaborator — flag over-scoped sections and say what to cut; (d) the figure/table plan: is each figure specified well enough to draw, and are there 10–14 for the 總論 and 4–6 per part; (e) the References list: only sources present in the digests, formatted as the author does.` },
]

const ACTIVE = args.lenses ? LENSES.filter(l => args.lenses.includes(l.key)) : LENSES
phase('Critique')
const results = await pipeline(FILES,
  f => parallel(ACTIVE.map(l => () => agent(
    `${CONTEXT}\n${l.prompt}\n\nRead the outline at ${f} in full first. Report issues with severity blocker/major/minor, the exact place, the problem, and a concrete fix (replacement text where possible). Do not pad; only real problems.`,
    { label: `critic:${l.key}:${f.split('/').pop().slice(0, 18)}`, phase: 'Critique', schema: ISSUES_SCHEMA, effort: l.effort }
  ))).then(cs => ({ file: f, critiques: cs.filter(Boolean) })),
  async (x, f) => {
    // Revise → verify, up to two rounds. Plain code merges the issue lists; no barrier across files.
    // args.preIssues: { "<basename>.md": [issue, ...] } — critiques saved from an earlier (interrupted) run, merged in so the lens need not rerun
    const pre = (args.preIssues && args.preIssues[f.split('/').pop()]) || []
    const all = [...x.critiques.flatMap(c => c.issues), ...pre]
    let issues = all.filter(i => i.severity === 'blocker' || i.severity === 'major')
    const minors = all.filter(i => i.severity === 'minor')
    log(`${f.split('/').pop()}: ${issues.length} blocker/major, ${minors.length} minor`)
    let rounds = 0, verify = null, revise = null
    while (rounds < 2 && issues.length) {
      rounds++
      revise = await agent(
        `${CONTEXT}\nRevise the outline at ${f} IN PLACE (Edit/Write) to resolve every issue below. Keep the structure and length (do not shorten to dodge a problem; replace weak content with real content drawn from the digests). Where an issue says a citation is wrong or invented, fix the citation or delete the claim — never keep an unverifiable number. Every figure in the plan must end up with a one-sentence caption AND complete Mermaid source that follows ${ROOT}/MERMAID.md (${MERMAID_RULES}); convert prose figure descriptions into Mermaid, and split any figure that would exceed 900px width or a 1.5 aspect ratio into two. Keep Traditional Chinese (Taiwan), single "—" dash. After editing, re-read the whole file once for coherence. Return the path, a summary, how many issues you applied, and which you skipped with the reason.\n\nBLOCKER/MAJOR ISSUES:\n${JSON.stringify(issues, null, 1)}\n\nMINOR ISSUES (apply where cheap):\n${JSON.stringify(minors.slice(0, 25), null, 1)}`,
        { label: `revise${rounds}:${f.split('/').pop().slice(0, 18)}`, phase: 'Revise', schema: FILE_SCHEMA, effort: 'high' }
      )
      verify = await agent(
        `${CONTEXT}\nVerify the revision of ${f}. For each issue below, check in the file whether it is actually resolved (quote the fixed text). Then re-audit ONLY the changed or newly added passages for new problems: invented citations, numbers not in the digests, mainland-Chinese terms, "——", contradictions with selection.md. pass=true only if every blocker is resolved and no new blocker was introduced.\n\nISSUES THAT WERE TO BE FIXED:\n${JSON.stringify(issues, null, 1)}`,
        { label: `verify${rounds}:${f.split('/').pop().slice(0, 18)}`, phase: 'Verify', schema: VERIFY_SCHEMA, effort: 'high' }
      )
      if (!verify || verify.pass) break
      issues = [...(verify.remaining || []), ...(verify.new_problems || [])].map(s => ({ severity: 'blocker', where: '', problem: s, fix: '' }))
    }
    // Figures: a dedicated agent turns every figure spec in the (revised) outline into Mermaid source in a companion file.
    const figPath = f.replace(/\.md$/, '.figures.md')
    const figures = args.skipFigures ? null : await agent(
      `${CONTEXT}\nRead ${f} in full and ${ROOT}/MERMAID.md in full. Write ${figPath} (Write tool) containing, for EVERY figure the outline plans (總論 and each of the three parts, in order): a heading with the figure id and which piece/section it belongs to, the one-sentence caption (圖說), and complete Mermaid source in a \`\`\`mermaid block that follows MERMAID.md exactly: ${MERMAID_RULES}. Prefer flowchart; use timeline for timelines, mindmap only for taxonomies, sequenceDiagram for protocols. Where the outline's figure would be clearer as a table, say so in one line and skip the diagram. Content must come from the outline itself (numbers, names) — do not invent. Return the path, a summary, the number of figures written, and any figure you skipped with the reason.`,
      { label: `figures:${f.split('/').pop().slice(0, 18)}`, phase: 'Revise', schema: FILE_SCHEMA, effort: 'high' }
    )
    return { file: f, figures: figures ? figures.path : null, figures_summary: figures ? figures.summary : null, critiques: x.critiques.map(c => ({ verdict: c.verdict, overall: c.overall, counts: { blocker: c.issues.filter(i => i.severity === 'blocker').length, major: c.issues.filter(i => i.severity === 'major').length, minor: c.issues.filter(i => i.severity === 'minor').length } })), rounds, revise, verify }
  }
)

return results.filter(Boolean)
