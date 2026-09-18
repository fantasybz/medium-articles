export const meta = {
  name: 'research-2026-10-december-figures',
  description: 'Bring the 2026-12 figures companion file in line with the re-cut outline: keep verified figures byte-identical, redraw the ones marked CHANGED, draw the NEW ones, drop the DROPPED ones; then a static reviewer checks every block against MERMAID.md before the local renderer runs.',
  phases: [
    { title: 'Figures', detail: 'update <outline>.figures.md from the FIGURE markers' },
    { title: 'Review', detail: 'static MERMAID.md check of every changed block' },
  ],
}

const ROOT = args.root
const TODAY = args.today
const OUTLINE = `${ROOT}/research/2026-10/2026-12-sre-for-agents.md`
const FIG = `${ROOT}/research/2026-10/2026-12-sre-for-agents.figures.md`

const MERMAID_RULES = `the YAML frontmatter config block at the top (theme base, the themeVariables colours, flowchart spacing, subGraphTitleMargin; NO fontFamily) — never %%{init}%%; classDef own/buy/bad/human applied with class, no per-node style lines; layout width 500–900 CSS px and aspect (height/width) 0.5–1.5; ≤ 12 nodes; ≤ 3 lines × 14 CJK chars per node using <br/>; edge labels ≤ 6 chars; TB for > 5 nodes, ≤ 4 nodes per rank; fontSize 16px; no emoji; when subgraphs use direction TB, wire subgraph to subgraph (an inner node connected to the outside breaks direction TB); the two-column pattern (LR with two direction-TB subgraphs) for short linear flows`

const FILE = { type: 'object', required: ['path', 'summary', 'applied', 'skipped'], properties: { path: { type: 'string' }, summary: { type: 'string' }, applied: { type: 'number' }, skipped: { type: 'array', items: { type: 'string' } } } }
const ISSUES = { type: 'object', required: ['issues', 'verdict'], properties: { verdict: { type: 'string' }, issues: { type: 'array', items: { type: 'object', required: ['figure', 'problem', 'fix'], properties: { figure: { type: 'string' }, problem: { type: 'string' }, fix: { type: 'string', description: 'corrected Mermaid source or caption' } } } } } }

phase('Figures')
const upd = await agent(`Today is ${TODAY}. Repo ${ROOT}. Read ${ROOT}/MERMAID.md in full (the standard: ${MERMAID_RULES}). Read ${FIG} in full: it is the verified companion file — every Mermaid block in it passed research/scripts/mermaid_check.sh, so a block you do not need to change must stay byte-identical. Read ${OUTLINE} in full and collect every marker line: '<!-- FIGURE CHANGED: <id> — … -->', '<!-- FIGURE DROPPED: <id> -->', '<!-- FIGURE NEW: <id> — <spec> -->'. Also compare the outline's 決策工件 / Mermaid 圖清單 sections with the figures file's 清單 to catch a figure whose spec changed without a marker.
Then update ${FIG} with Edit (or Write, keeping unchanged blocks verbatim): for CHANGED figures redraw the block from the outline's new caption / spec, keeping the id, heading, caption line and the same frontmatter config block; for NEW figures add a heading in the outline's order with 圖說 and a complete block; for DROPPED figures remove the heading and block; update the 清單 table at the end (counts of Mermaid figures vs 表格，不畫). Every block must follow the standard exactly; content (numbers, names) only from the outline. Then, in the OUTLINE, replace each marker line and the stale block under it as follows: for CHANGED, leave the marker in place (the local sync script overwrites embedded blocks from the figures file by id) but make sure the outline's caption matches the figures file; for DROPPED, delete the marker and the block; for NEW, leave the marker and add the new block below it (identical to the figures file). Return path, summary (list each id and what happened), applied count, skipped with reasons.`, { label: 'figures:update', phase: 'Figures', schema: FILE, effort: 'high' })
log(`figures: ${upd ? upd.summary.slice(0, 300) : 'NULL'}`)

phase('Review')
const rev = await agent(`Static Mermaid reviewer. Repo ${ROOT}. Read ${ROOT}/MERMAID.md (${MERMAID_RULES}) and ${FIG} in full. For every block, check the frontmatter is exactly the standard one (no fontFamily, no %%{init}%%), the four classDef lines, ≤ 12 nodes, label length (≤ 3 lines × 14 CJK), edge labels ≤ 6 chars, TB when > 5 nodes, subgraph wiring, no emoji; estimate the rendered width and aspect from the layout (LR chains > 5 nodes are too wide; a two-column subgraph layout is fine). Also confirm that each block that is not marked CHANGED/NEW in ${OUTLINE} is byte-identical to the one embedded in the outline (diff them with python). Report only concrete violations with corrected source. No rendering here — the local renderer runs next.`, { label: 'figures:review', phase: 'Review', schema: ISSUES, effort: 'high' })
if (rev && rev.issues.length) {
  await agent(`Apply these corrections to ${FIG} (and the same block in ${OUTLINE} if it is embedded there) with the Edit tool, nothing else.\n${JSON.stringify(rev.issues, null, 1)}`, { label: 'figures:fix', phase: 'Review', effort: 'low' })
}
return { update: upd, review: rev }
