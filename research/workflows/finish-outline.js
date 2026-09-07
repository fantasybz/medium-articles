export const meta = {
  name: 'finish-outline',
  description: 'Finish one outline whose critique stage already ran: verify the (already revised) file against the saved issues, revise if needed (≤2 rounds), then write the Mermaid figures companion file',
  phases: [
    { title: 'Verify', detail: 'check the saved blocker/major issues are resolved in the current file' },
    { title: 'Revise', detail: 'only if verify fails' },
    { title: 'Figures', detail: 'write <outline>.figures.md with Mermaid for every figure' },
  ],
}

// args: { root, month, file: 'research/YYYY-MM/<slug>.md', issues: [ {severity, where, problem, fix}, ... ], skipFigures?: bool }
const ROOT = args.root
const DIR = `${ROOT}/research/${args.month}`
const f = args.file.startsWith('/') ? args.file : `${ROOT}/${args.file}`
const figPath = f.replace(/\.md$/, '.figures.md')
// issues may be passed inline (args.issues) or as a JSON file the agents read themselves (args.issuesFile: { "<basename>": [issue, ...] })
const issuesAll = args.issues || []
let issues = issuesAll.filter(i => i.severity === 'blocker' || i.severity === 'major')
const minors = issuesAll.filter(i => i.severity === 'minor')
const ISSUES_REF = args.issuesFile ? `Read the issues from ${args.issuesFile} (JSON, keyed by the outline's basename; each issue has severity/where/problem/fix). Treat blocker and major as must-fix, minor as apply-where-cheap.` : ''

const CONTEXT = `
Today is 2026-09-06. The author (@fantasybz, Kochi Chuang) publishes one THEME per month on Medium: one 總論 + 三部曲, in Traditional Chinese (Taiwan usage, English technical terms kept), plus an English edition. Audience: Engineering VPs / EMs / Staff engineers in Taiwan.
Reference files:
- ${DIR}/style_brief.md, ${DIR}/selection.md (judges' objections and the adjustments the theme must honour, incl. the Notion 補充)
- ${DIR}/arxiv.md, ${DIR}/x_digest.md, ${DIR}/community_digest.md, ${DIR}/notion_digest.md (the ONLY allowed sources for numbers; read the parts you need)
- ${ROOT}/MERMAID.md (the Mermaid standard every figure must follow)
- Published articles not to be repeated: ${ROOT}/2026-09-agentic-engineering-platform/article.md, ${ROOT}/2026-09-agentic-org-design/article.md, ${ROOT}/2026-10-agentic-harness-blueprint/article.md, ${ROOT}/2026-11-agentic-eval-economics/article.md
Standard: the highest. Single "—" dash only, never "——".
`
const FILE_SCHEMA = { type: 'object', required: ['path', 'summary', 'applied', 'skipped'], properties: { path: { type: 'string' }, summary: { type: 'string' }, applied: { type: 'number' }, skipped: { type: 'array', items: { type: 'string' } } } }
const VERIFY_SCHEMA = { type: 'object', required: ['pass', 'remaining', 'new_problems'], properties: { pass: { type: 'boolean' }, remaining: { type: 'array', items: { type: 'string' } }, new_problems: { type: 'array', items: { type: 'string' } } } }

log(`${f.split('/').pop()}: ${issues.length} blocker/major, ${minors.length} minor inline${args.issuesFile ? ' + issues file ' + args.issuesFile : ''}`)
let rounds = 0, verify = null, revise = null
phase('Verify')
verify = await agent(
  `${CONTEXT}\nThe outline at ${f} was revised by an earlier agent whose run was cut off before it could report. Verify it against the issues below: for each blocker/major, check in the file whether it is actually resolved (quote the fixed text briefly). Then re-audit the changed passages for new problems: invented citations, numbers not in the digests, mainland-Chinese terms, "——", contradictions with selection.md, arithmetic errors in any worked example. pass=true only if every blocker is resolved, at most 2 majors remain, and no new blocker was introduced. Put every unresolved item in remaining, verbatim enough that a reviser can act on it.\n\n${ISSUES_REF}\nISSUES (inline, may be empty if issuesFile is used):\n${JSON.stringify(issues, null, 1)}`,
  { label: `verify0:${f.split('/').pop().slice(0, 18)}`, phase: 'Verify', schema: VERIFY_SCHEMA, effort: 'high' }
)
while (verify && !verify.pass && rounds < 2) {
  rounds++
  const todo = [...(verify.remaining || []), ...(verify.new_problems || [])].map(s => ({ severity: 'blocker', where: '', problem: s, fix: '' }))
  phase('Revise')
  revise = await agent(
    `${CONTEXT}\nRevise the outline at ${f} IN PLACE (Edit/Write) to resolve every issue below. Keep the structure and length; replace weak content with real content drawn from the digests; never keep an unverifiable number; fix arithmetic. Keep Traditional Chinese, single "—". Re-read the whole file once for coherence afterwards. Return path, summary, count applied, and skipped with reasons.\n\nISSUES:\n${JSON.stringify(todo, null, 1)}\n\nMINOR ISSUES (apply where cheap):\n${JSON.stringify(minors.slice(0, 20), null, 1)}`,
    { label: `revise${rounds}:${f.split('/').pop().slice(0, 18)}`, phase: 'Revise', schema: FILE_SCHEMA, effort: 'high' }
  )
  phase('Verify')
  verify = await agent(
    `${CONTEXT}\nVerify the revision of ${f}. For each issue below, check whether it is resolved (quote briefly); re-audit changed passages for new problems (invented citations, numbers not in the digests, "——", arithmetic). pass=true only if every item is resolved and nothing new was introduced.\n\nISSUES:\n${JSON.stringify(todo, null, 1)}`,
    { label: `verify${rounds}:${f.split('/').pop().slice(0, 18)}`, phase: 'Verify', schema: VERIFY_SCHEMA, effort: 'high' }
  )
}

let figures = null
if (!args.skipFigures) {
  phase('Figures')
  figures = await agent(
    `${CONTEXT}\nRead ${f} in full and ${ROOT}/MERMAID.md in full. Write ${figPath} (Write tool) containing, for EVERY figure the outline plans (總論 and each of the three parts, in order): a heading with the figure id and which piece/section it belongs to, the one-sentence caption (圖說), an expected-size line (TB/LR, node count, estimated aspect), and complete Mermaid source in a \`\`\`mermaid block that follows MERMAID.md exactly: the frontmatter config block (theme base, the themeVariables colours, flowchart spacing, subGraphTitleMargin; NO fontFamily), classDef own/buy/bad/human, TB for > 5 nodes, ≤ 12 nodes, ≤ 3 lines × 14 CJK chars per node using <br/>, edge labels ≤ 6 chars, no emoji, no per-node style lines, subgraph-to-subgraph edges when using direction TB inside subgraphs, target width 500–900px and aspect 0.5–1.5 (use the two-column pattern for short linear flows; inside an LR subgraph, chain unconnected nodes with invisible edges a ~~~ b so they sit side by side; a diamond is taller than a hexagon). If the outline already embeds Mermaid source for a figure, start from it and fix it to the standard rather than redrawing from scratch. Where a figure would be clearer as a table, say so in one line and skip the diagram. Content must come from the outline itself — do not invent. Return the path, a summary, the number of figures written, and any figure you skipped with the reason.`,
    { label: `figures:${f.split('/').pop().slice(0, 18)}`, phase: 'Figures', schema: FILE_SCHEMA, effort: 'high' }
  )
}
return { file: f, rounds, verify, revise, figures: figures ? figures.path : null, figures_summary: figures ? figures.summary : null }
