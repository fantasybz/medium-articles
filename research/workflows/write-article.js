export const meta = {
  name: 'write-article',
  description: 'Write one Medium piece (zh) from its outline: draft → 3 lensed critics → revise → verify (≤2 rounds)',
  phases: [
    { title: 'Draft', detail: 'article.md from the outline section, figures.md and the digests' },
    { title: 'Critique', detail: 'evidence auditor + VP reader + editor' },
    { title: 'Revise', detail: 'apply blockers/majors in place; verify; loop ≤2' },
  ],
}

// args: { root, month: 'YYYY-MM', today: 'YYYY-MM-DD',
//         published: ['2026-09-agentic-engineering-platform', ...]   (dirs of the published articles; current list in research/README.md),
//         outline: 'research/YYYY-MM/<slug>.md', figures: 'research/YYYY-MM/<slug>.figures.md',
//         piece: '總論' | '一、測試篇' | ..., dir: '2026-10-green-overview', prev: [ 'dir-of-earlier-piece', ... ],
//         series: { titles: [..4 titles in order..], published_links: { '<title>': url } },
//         skipDraft?: bool   (the draft already exists at <dir>/article.md, e.g. written in the main loop; run only critique → revise → verify) }
// CONTEXT skeleton, ISSUES_SCHEMA, FILE_SCHEMA and VERIFY_SCHEMA are copies of review-outlines.js (the canonical copy;
// workflow scripts cannot import modules) — change them there first.
const ROOT = args.root
const DIR = `${ROOT}/research/${args.month}`
const OUTLINE = `${ROOT}/${args.outline}`
const FIGURES = `${ROOT}/${args.figures}`
const TARGET = `${ROOT}/${args.dir}/article.md`
const PREV = (args.prev || []).map(d => `${ROOT}/${d}/article.md`)
if (!args.today) throw new Error('args.today (YYYY-MM-DD) is required: workflow scripts have no Date')
if (!Array.isArray(args.published) || !args.published.length) throw new Error('args.published (array of published article dirs) is required; see research/README.md for the current list')
const PUBLISHED = args.published.map(d => `${ROOT}/${d}/article.md`)

const CONTEXT = `
Today is ${args.today}. You are writing for @fantasybz (Kochi Chuang): long-form Traditional-Chinese (Taiwan usage; English technical terms untranslated) Medium articles for Engineering VPs / EMs / Staff engineers in Taiwan. Voice, structure and tail conventions are in ${DIR}/style_brief.md — follow them exactly (TL;DR blockquote, 系列導覽 line, ## 一、二、… sections, 結語 with a quotable blockquote, ### 系列文章 → ### References → ### AI 協作說明 → italic signature line; single "—" only, never "——").
Sources you may cite: ONLY ${DIR}/arxiv.md, ${DIR}/x_digest.md, ${DIR}/community_digest.md, ${DIR}/notion_digest.md and the plan itself. Never invent a number, a paper or a quote.
The published pieces (voice reference; do not repeat their content): ${PUBLISHED.join(', ')}.
Figures: every figure is a \`\`\`mermaid block placed inline where the plan puts it, taken VERBATIM from ${FIGURES} (id-matched; do not redraw; keep the frontmatter config). Tables are markdown tables (they become PNGs at publish time). Code/config snippets go in fenced blocks (the "——" rule does not apply inside code).
Series links: pieces not yet published are referenced as plain text 「（即將發布）」 (no relative paths); already published pieces use their Medium URLs: ${JSON.stringify(args.series || {})}.
`

const DRAFT_SCHEMA = { type: 'object', required: ['path', 'chars', 'figures', 'summary'], properties: { path: { type: 'string' }, chars: { type: 'number' }, figures: { type: 'number' }, summary: { type: 'string' } } }
const ISSUES_SCHEMA = { type: 'object', required: ['issues', 'overall', 'verdict'], properties: { issues: { type: 'array', items: { type: 'object', required: ['severity', 'where', 'problem', 'fix'], properties: { severity: { type: 'string' }, where: { type: 'string' }, problem: { type: 'string' }, fix: { type: 'string' } } } }, overall: { type: 'string' }, verdict: { type: 'string' } } }
const FILE_SCHEMA = { type: 'object', required: ['path', 'summary', 'applied', 'skipped'], properties: { path: { type: 'string' }, summary: { type: 'string' }, applied: { type: 'number' }, skipped: { type: 'array', items: { type: 'string' } } } }
const VERIFY_SCHEMA = { type: 'object', required: ['pass', 'remaining', 'new_problems'], properties: { pass: { type: 'boolean' }, remaining: { type: 'array', items: { type: 'string' } }, new_problems: { type: 'array', items: { type: 'string' } } } }

phase('Draft')
const draft = args.skipDraft ? { path: TARGET, chars: 0, figures: 0, summary: 'pre-existing draft' } : await agent(
  `${CONTEXT}\nWrite the piece 「${args.piece}」 of the theme planned in ${OUTLINE} (read the whole plan first — the 主題總覽, the section outline for this piece, the 圖表清單, the 補證據 list and the 發布與推廣 notes — then the figures file ${FIGURES}). Write the full article to ${TARGET} (Write tool; create the directory). Length, calibrated on the published pieces (Medium counts CJK characters, English words and images): 總論 ≈ 18 min read = about 3,500–4,500 CJK characters of prose plus tables and 10–14 figures (the published 總論 is 3,629 CJK characters); a deep dive ≈ 8–12 min = 1,900–2,600 CJK characters plus 4–6 figures. Do not pad; every paragraph must carry a claim, a number or a decision. Every section in the plan must appear with real content; every claim that carries a number cites its source inline the way the published pieces do (org — [title](url) in References; arXiv ids as "arXiv 2609.04167" in prose only where the plan does). Use the plan's decision artefacts (tables, gates, checklists, Before/After snippets) as written. Keep the author's first-person, opinionated voice (「如果我是 Engineering VP」, 「我的建議值（不是業界標準）」). ${PREV.length ? 'Earlier pieces of this series are at ' + PREV.join(', ') + ' — keep terminology and cross-references consistent with them.' : ''} Do not write the English edition. Return the path, character count, figure count and a 5-line summary.`,
  { label: `draft:${args.dir}`, phase: 'Draft', schema: DRAFT_SCHEMA, effort: 'high' }
)
if (!draft) throw new Error('draft failed')
log(`draft: ${draft.chars} chars, ${draft.figures} figures`)

const LENSES = [
  { key: 'evidence', prompt: `LENS: Evidence auditor. Check every number, paper, post, quote and cross-reference in ${TARGET} against the four digests and the plan ${OUTLINE}. Flag anything invented, misquoted, out of domain, or stronger than the source (blocker/major). Also flag arithmetic in worked examples and any figure whose Mermaid source differs from ${FIGURES}.` },
  { key: 'reader', prompt: `LENS: The reader. (Read only the article, the plan's 主題總覽 and style_brief.md.) You are an Engineering VP at a 300-person Taiwanese software company who has read the author's published pieces. Would you finish it and forward it? Where does it drag, repeat, or lecture? Is the thesis argued or asserted? Which decision artefacts are real? Flag padding, hedging, and any paragraph that says nothing a VP can act on.` },
  { key: 'editor', prompt: `LENS: Senior tech editor. (Read the article, style_brief.md, the plan, and the published articles.) Check the format skeleton exactly (TL;DR / 系列導覽 / numbered sections / 結語 quotable / 系列文章 / References / AI 協作說明 / signature), single "—", Traditional Chinese Taiwan usage (flag mainland terms and translationese), reading time vs target (count CJK characters outside code blocks with python; 總論 target 3,500–4,500, the published 總論 has 3,629; say exactly which paragraphs to cut or demote to the deep dives if over), overlap with the published pieces and with sibling pieces of this theme, figure placement and captions, tables' width (≤ 5 columns for Medium), and that every link in the text is either a real URL or the plain-text 「（即將發布）」 marker.` },
]
phase('Critique')
const critiques = (await parallel(LENSES.map(l => () => agent(`${CONTEXT}\n${l.prompt}\n\nReport issues with severity blocker/major/minor, exact place, problem, and a concrete fix.`, { label: `critic:${l.key}:${args.dir}`, phase: 'Critique', schema: ISSUES_SCHEMA, effort: 'high' })))).filter(Boolean)
let issues = critiques.flatMap(c => c.issues.filter(i => i.severity === 'blocker' || i.severity === 'major'))
const minors = critiques.flatMap(c => c.issues.filter(i => i.severity === 'minor'))
log(`critique: ${issues.length} blocker/major, ${minors.length} minor`)

let rounds = 0, verify = null, revise = null
phase('Revise')
while (rounds < 2 && issues.length) {
  rounds++
  revise = await agent(`${CONTEXT}\nRevise ${TARGET} IN PLACE to resolve every issue below (keep the structure; if a critic flags reading time, cut to the target — 總論 ≈ 3,500–4,500 CJK prose characters, deep dive 1,900–2,600 — by removing redundancy and demoting detail to the deep dives, never by dropping a decision artefact; replace weak content with real content from the digests/plan; never keep an unverifiable number; fix arithmetic). Then re-read the whole file once for flow. Return path, summary, applied count, skipped with reasons.\n\nBLOCKER/MAJOR:\n${JSON.stringify(issues, null, 1)}\n\nMINOR (apply where cheap):\n${JSON.stringify(minors.slice(0, 25), null, 1)}`, { label: `revise${rounds}:${args.dir}`, phase: 'Revise', schema: FILE_SCHEMA, effort: 'high' })
  verify = await agent(`${CONTEXT}\nVerify the revision of ${TARGET}: for each issue below confirm it is resolved (quote briefly); re-audit changed passages for new problems (invented citations, "——", arithmetic, broken format skeleton). pass=true only if every blocker is resolved and nothing new was introduced.\n\nISSUES:\n${JSON.stringify(issues, null, 1)}`, { label: `verify${rounds}:${args.dir}`, phase: 'Revise', schema: VERIFY_SCHEMA, effort: 'high' })
  if (!verify || verify.pass) break
  issues = [...(verify.remaining || []), ...(verify.new_problems || [])].map(s => ({ severity: 'blocker', where: '', problem: s, fix: '' }))
}
return { path: TARGET, draft, critiques: critiques.map(c => ({ verdict: c.verdict, counts: { blocker: c.issues.filter(i => i.severity === 'blocker').length, major: c.issues.filter(i => i.severity === 'major').length, minor: c.issues.filter(i => i.severity === 'minor').length }, overall: c.overall })), rounds, revise, verify }
