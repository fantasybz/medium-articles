export const meta = {
  name: 'research-2026-10-december-recut',
  description: 'Re-cut the 2026-12 SRE-for-agents outline with the AGNTCon Tokyo material, the AI Agents in Depth book, the mid-September arXiv sweep and the Codex objections: five mappers → one edit plan → four sequential in-place revisers → structural verify → selection.md decision record.',
  phases: [
    { title: 'Map', detail: 'Codex closure · conference · book · arXiv+Notion · re-cut architect' },
    { title: 'Synthesize', detail: 'one ordered edit plan (JSON) from the five maps' },
    { title: 'Revise', detail: '總論 → 觀測篇 → 可靠篇 → 應變篇+tail, in place' },
    { title: 'Verify', detail: 'structure and Codex closure check; selection.md decision record' },
  ],
}

const ROOT = args.root
const TODAY = args.today
const DIR = `${ROOT}/research/2026-10`
const PREV = `${ROOT}/research/2026-09`
const OUTLINE = `${DIR}/2026-12-sre-for-agents.md`
const FIG = `${DIR}/2026-12-sre-for-agents.figures.md`
const CODEX = `${PREV}/codex-review-2026-12-sre-for-agents.md`
const CONF = `${ROOT}/.context/research/2026-09-conf`
const PLAN = `${ROOT}/.context/research/2026-10/dec-recut-plan.json`
const PUBLISHED = ['2026-09-agentic-engineering-platform', '2026-09-agentic-org-design', '2026-10-agentic-harness-blueprint', '2026-11-agentic-eval-economics']
const UNPUBLISHED = ['2026-10-green-overview', '2026-10-green-testing', '2026-10-green-review', '2026-10-green-reliability']

const CONTEXT = `
Today is ${TODAY}. Repo root ${ROOT}; use absolute paths. The author (@fantasybz, Kochi Chuang) publishes one THEME per month on Medium: one 總論 (~18 min) + 三部曲 (8–12 min each) in Traditional Chinese (Taiwan usage; English technical terms kept; single "—" dash, never "——"), plus an English edition. Audience: Engineering VPs / EMs / Staff engineers / platform, SRE and QA leads in Taiwan.
The 2026-12 theme is 把 Agent 當 Production Workload：Agent 的 SRE. Its outline is ${OUTLINE} (a copy of the 2026-09-05 version, ~150K chars; its companion figures file is ${FIG}, 14 Mermaid figures already verified). A second-model review, ${CODEX}, judged it 不合格 and said it must be re-cut around flight recorder / accountability, keep only three artefacts (trace schema + Collector config, agent-slo.yaml, attestation status check), fix the outcome-evidence logic, add min_events to burn-rate rules, and add a signal-availability matrix, a tamper boundary, a workflow evidence matrix, an SLI → action table, a ledger-backed attestation flow and a data-governance table.
Since then the author attended AGNTCon + MCPCon Japan (Tokyo, Sep 10–11) and read Bojie Li's *AI Agents in Depth* v2.0. New sources, all in ${DIR}/: conference_digest.md (integrated conference digest; per-session detail with slide numbers in ${CONF}/notes_sep10.md and ${CONF}/notes_sep11.md), book_ai_agent_book.md (book notes with chapter/§ refs), arxiv.md (sweep 2026-09-01→15, incl. what 2608.23610's tuple actually contains), notion_digest.md (the author's own notes), x_digest.md, community_digest.md. The 2026-09 digests (${PREV}/arxiv.md etc.) remain valid for the citations the outline already carries.
Constraints that still bind (from ${PREV}/selection.md, 2026-12 section and the Notion 補充): 可靠篇 keeps ONE artefact (agent SLO spec); K8s sandbox fleet is one section at most and marked as a 1,000-person problem; no Claude Taiwan seat complaints as evidence; the series must exceed the author's two 2025 observability pieces (model-call layer) by moving the span up to run / tool-call / approval; Google's "Agent Ops" is the naming rival to be named; nothing already published (${PUBLISHED.map(d => `${ROOT}/${d}/article.md`).join(', ')}) or already written for October (${UNPUBLISHED.map(d => `${ROOT}/${d}/article.md`).join(', ')}) may be repeated — December extends, it does not restate. Style: ${PREV}/style_brief.md.
Every number, name and quote you add must come from one of the digest / notes files above, cited the way the outline already cites (arXiv id, session id + slide, book chapter §). Never invent.`

const EDITS = {
  type: 'object', required: ['edits', 'summary'],
  properties: {
    summary: { type: 'string' },
    edits: { type: 'array', items: { type: 'object', required: ['piece', 'section', 'action', 'text_zh', 'source', 'why', 'priority'], properties: {
      piece: { type: 'string', enum: ['總論', '觀測篇', '可靠篇', '應變篇', '全系列'] },
      section: { type: 'string', description: 'the exact heading or numbered item in the outline (quote its first words)' },
      action: { type: 'string', enum: ['add', 'replace', 'delete', 'merge'] },
      anchor: { type: 'string', description: 'for add/replace: an exact sentence from the outline next to which the edit lands' },
      text_zh: { type: 'string', description: 'the exact Traditional Chinese text to insert or use as replacement, citations inline as the outline does; empty for delete' },
      source: { type: 'string', description: 'file + slide/§/id' },
      why: { type: 'string' },
      priority: { type: 'string', enum: ['must', 'should', 'nice'] },
    } } },
  },
}

const CLOSURE = {
  type: 'object', required: ['items', 'summary'],
  properties: {
    summary: { type: 'string' },
    items: { type: 'array', items: { type: 'object', required: ['objection', 'tier', 'resolution', 'sources', 'structural', 'text_zh'], properties: {
      objection: { type: 'string', description: 'the Codex item heading, verbatim' },
      tier: { type: 'string', enum: ['致命', '重要', '次要', '刪除', '補充'] },
      resolution: { type: 'string', description: 'accept as-is / accept with new evidence / modify / reject with reason' },
      sources: { type: 'array', items: { type: 'string' } },
      structural: { type: 'boolean', description: 'true if it changes which sections exist' },
      text_zh: { type: 'string', description: 'the replacement text or new table rows in Traditional Chinese, ready to paste; empty if reject' },
      where: { type: 'string', description: 'piece + section' },
    } } },
  },
}

const STRUCTURE = {
  type: 'object', required: ['overview', 'parts', 'artefacts', 'figures', 'schedule', 'rationale', 'must_not'],
  properties: {
    overview: { type: 'array', items: { type: 'object', required: ['n', 'title', 'status', 'note'], properties: { n: { type: 'string' }, title: { type: 'string' }, status: { type: 'string', enum: ['keep', 'trim', 'merge', 'cut', 'new', 'rewrite'] }, note: { type: 'string' } } } },
    parts: { type: 'array', items: { type: 'object', required: ['title', 'sections'], properties: { title: { type: 'string' }, sections: { type: 'array', items: { type: 'object', required: ['n', 'title', 'status', 'note'], properties: { n: { type: 'string' }, title: { type: 'string' }, status: { type: 'string', enum: ['keep', 'trim', 'merge', 'cut', 'new', 'rewrite'] }, note: { type: 'string' } } } } } } },
    artefacts: { type: 'array', items: { type: 'string' }, description: 'the artefacts the series ships, ≤ 3 + the SLO spec' },
    figures: { type: 'array', items: { type: 'object', required: ['id', 'status', 'spec'], properties: { id: { type: 'string' }, status: { type: 'string', enum: ['keep', 'change', 'drop', 'new'] }, spec: { type: 'string', description: 'for change/new: caption + what the nodes are; for keep/drop: one line' } } } },
    schedule: { type: 'string' },
    word_budget: { type: 'string' },
    rationale: { type: 'string' },
    must_not: { type: 'array', items: { type: 'string' } },
  },
}

const VERIFY = { type: 'object', required: ['pass', 'remaining', 'new_problems'], properties: { pass: { type: 'boolean' }, remaining: { type: 'array', items: { type: 'string' } }, new_problems: { type: 'array', items: { type: 'string' } } } }
const FILE = { type: 'object', required: ['path', 'summary', 'applied', 'skipped'], properties: { path: { type: 'string' }, summary: { type: 'string' }, applied: { type: 'number' }, skipped: { type: 'array', items: { type: 'string' } } } }

// ---------------------------------------------------------------- Map
phase('Map')
log('Five mappers read the outline against the Codex review, the conference, the book, and the new arXiv / Notion digests')
const [closure, conf, book, arxivNotion, structure] = await parallel([
  () => agent(`${CONTEXT}
TASK — Codex closure map. Read ${CODEX} in full (致命 6 / 重要 12 / 次要 5 / 建議刪除 6 / 建議補充 7 items). Then read ${OUTLINE} in full and the new sources (${DIR}/conference_digest.md, ${DIR}/book_ai_agent_book.md, ${DIR}/arxiv.md — especially what it reports about 2608.23610's behavioural tuple —, ${DIR}/notion_digest.md §7). For EVERY Codex item decide: accept as-is, accept with the new evidence that now supports it (cite it), modify (say how), or reject (only with a concrete reason from selection.md constraints). Write the replacement text in Traditional Chinese ready to paste — e.g. the workflow evidence matrix rows, the min_events clause, the signal-availability matrix rows (fill it from what the conference and book say each vendor exposes: agentgateway / Agent Router / Uber's 11 MCP servers / NTT DOCOMO trace-based eval / PagerDuty eval pipeline / Claude Code hooks per the book), the tamper boundary paragraph, the outcome-evidence rule. Mark items that change which sections exist as structural.`, { label: 'map:codex-closure', phase: 'Map', schema: CLOSURE, effort: 'high' }),
  () => agent(`${CONTEXT}
TASK — Conference → outline map. Read ${DIR}/conference_digest.md in full, then ${CONF}/notes_sep10.md and ${CONF}/notes_sep11.md (the cross-cutting sections first, then the sessions they point at), then ${OUTLINE} in full. Produce the edits that bring the conference into the outline: for each section of 總論 (§一–§十二 + 決策工件 + References + 來源對照) and each numbered section of 觀測篇 / 可靠篇 / 應變篇, what to add or replace — the exact Traditional Chinese text with the citation (session id + slide / timestamp, speaker, company) inline as the outline cites. Priorities: the who-vs-why audit gap and per-hop delegation gap (Hitachi), Mazin Gilbert's "we don't measure task completion at cost" keynote line, agentgateway / Agent Router as the AAIF answer to "where does the trace come from", Uber's MCP crash investigation, NTT DOCOMO trace-based evaluation, PagerDuty's open-source eval pipeline, Quartic's agent upgrading production Kubernetes without a 3 AM page, Adobe's 3 AM page bounded AI, Intent as Code / delegated authorization (AuthZed, Keycloak workshop), stateful sandboxes (Juicedata), Aggre's logs-to-proofs, Raytone's 30× cost fluctuation, agent identity (Bitso), Runlayer's shadow AI stack, carbon-aware agents (NTT) — but only where they genuinely strengthen a December section; say 'nice' for colour. Also propose References rows (org — [title](url) using the sched URL or slide URL) and 來源對照 rows. Do not propose edits about testing/review that belong to October.`, { label: 'map:conference', phase: 'Map', schema: EDITS, effort: 'high' }),
  () => agent(`${CONTEXT}
TASK — Book → outline map. Read ${DIR}/book_ai_agent_book.md in full (Bojie Li, *AI Agents in Depth* v2.0; the notes give chapter, §, EN page and Chinese heading), then ${OUTLINE} in full. Produce the edits that bring the book into the outline where it is the best anchor: ch.1 §1.2 the five harness functions (Constrain / Verify / Correct — "安全檢查只看結構化資料…不看模型自由生成的文字" is the outcome-evidence rule in the book's words), §1.1.5 trajectories as the debuggable unit and "上下文 = 靜態前綴 + 軌跡", §1.2.5 three guardrail layers and "處在同一個上下文裡的 Agent 很難判斷自己是否已被注入" (tamper boundary), §1.3 patterns 提議者—審核者 / 只增不改 ("可快取、可重放、可稽核" = ledger) / 邊界集 + 保留集 / 最小 diff + 可回滾, ch.7 evaluation ("Did the agent improve — or did the numbers move?", the bad-case pipeline, eval from trajectories, honest negative results in EXPERIMENT_STATUS.md), docs/EXPERIMENT_CONVENTIONS.md as an evidence rule ("Successful authentication, model listing, installation, or browser launch is not task-completion evidence"), extras/agent-lab/SCHEMA.md as a citable trajectory format (outcome: success | failure | loop | timeout; never edit the tool calls), ch.9 continual evolution (harness as production dependency), ch.10 multi-agent. Also decide whether the book can be the 總論's 書錨 (selection.md wanted a book anchor; the outline currently has none — the SRE book and Kent Beck were candidates): argue for or against in the summary, and if for, write the 書錨 paragraph. Exact Traditional Chinese text with 《深入理解 AI Agent》第 N 章〈…〉 citations; for the English edition note the EN §. Mark what is 'must'.`, { label: 'map:book', phase: 'Map', schema: EDITS, effort: 'high' }),
  () => agent(`${CONTEXT}
TASK — arXiv + Notion → outline map. Read ${DIR}/arxiv.md in full (the 2026-09-01→15 sweep; its 'What this means for 2026-12' section and the 2608.23610 tuple finding are the important parts), ${DIR}/notion_digest.md (§6 delta and §7 what Notion offers the December re-cut), and ${OUTLINE} in full. Produce edits ONLY for things that are new relative to what the outline already cites: new papers that answer a Codex objection (outcome evidence, low-volume SLO, agent identity / attestation, OTel GenAI semconv status, agent observability datasets, gateway/authorization), corrections where the new sweep contradicts a number the outline uses, the 2608.23610 tuple alignment sentence, and first-hand material from Notion (CNPE / OTel Collector / Jaeger / Kyverno labs, Appier work notes, CCA-F notes) that gives the author a real reference implementation for the trace schema, the Collector config or the status check. Exact Traditional Chinese text with citations.`, { label: 'map:arxiv-notion', phase: 'Map', schema: EDITS, effort: 'high' }),
  () => agent(`${CONTEXT}
TASK — Re-cut architect. Read ${CODEX} in full, ${PREV}/selection.md (2026-12 section + Notion 補充), ${PREV}/style_brief.md, ${OUTLINE} in full (note every section, table, figure and the §4 evidence list / §6 schedule), and ONLY sections 1–3 and 9 of ${DIR}/conference_digest.md plus §1 of ${DIR}/book_ai_agent_book.md. Decide the new structure that satisfies Codex's structural verdict — keep only three artefacts (trace schema + Collector config; agent-slo.yaml; ledger-backed attestation status check) plus the SLO spec that selection.md already fixed as 可靠篇's single artefact; cut or fold the sections Codex listed (CNPE opening to one sentence, F2 timeline, K8s/CNPE table to backlog, 資安段 to one paragraph, AgentLogs dashboard residue, EN/promotion detail out of the main plan); add the sections Codex asked for (signal availability matrix before 觀測篇 §2, minimal reference implementation, workflow evidence matrix, SLI → action table, tamper boundary, ledger-backed attestation flow, data governance table) and decide which piece each lives in; keep the 總論 at 10–12 sections and each part at 5–7; decide which of the 14 figures + 12 tables stay / change / drop and specify any new figure (≤ 12 nodes, caption); re-derive the schedule so one author can write four pieces + EN in December with instrumentation started in October; set a word budget per piece (總論 ≈ 3,600 CJK chars ≈ 18 min; parts 1,800–2,300). List what the re-cut must NOT do (selection.md constraints; no repeat of the 8 written articles). Give the rationale in Traditional Chinese.`, { label: 'map:recut-architect', phase: 'Map', schema: STRUCTURE, effort: 'high' }),
])
const maps = { closure, conf, book, arxivNotion, structure }
for (const [k, v] of Object.entries(maps)) log(`${k}: ${v ? (v.edits ? v.edits.length + ' edits' : v.items ? v.items.length + ' items' : 'structure ok') : 'NULL'}`)
if (!structure || !closure) throw new Error('re-cut architect or Codex closure returned null; nothing to synthesize')

// ---------------------------------------------------------------- Synthesize (barrier: needs all five)
phase('Synthesize')
const synth = await agent(`${CONTEXT}
TASK — Synthesize one ordered edit plan. You are given five maps (JSON below): the Codex closure decisions, the conference edits, the book edits, the arXiv/Notion edits, and the re-cut structure. Merge them into ONE plan and Write it to ${PLAN} as JSON with this shape:
{ "structure": <the STRUCTURE object, adjusted if a map contradicts it>, "pieces": [ { "piece": "總論" | "觀測篇" | "可靠篇" | "應變篇" | "tail", "edits": [ { "order": n, "section": "...", "action": "add|replace|delete|merge|restructure", "anchor": "...", "text_zh": "...", "source": "...", "why": "...", "from": "codex|conference|book|arxiv|notion|architect" } ] } ], "figures": [...], "open_questions": [...] }.
Rules: (1) structural decisions come first in each piece (cut / merge / new section), then content edits in document order; (2) when two maps propose text for the same place, merge into one text (do not duplicate a citation); (3) every 'must' edit is in; 'should' in unless it breaks the word budget; 'nice' only where a section would otherwise be thin; (4) the tail piece covers 決策工件清單, Mermaid 圖清單 header line, 可引用的一句話, References, 來源對照, 總論與三篇之間的不重疊檢查, §4 寫作前要補的證據 (drop items the conference or book now settles, add the instrumentation experiment as the first item), §5 英文版 (trim to a short list), §6 發布與推廣 (only the schedule and the three FB hooks; move the rest to a one-line pointer), and the header blockquote at the top of the outline, which must record this revision (date ${TODAY}, basis: Codex review + AGNTCon Tokyo + AI Agents in Depth + arXiv 09-15 sweep) and restate the three main lines; (5) keep every existing Mermaid code block untouched — for a figure whose spec changes, the edit replaces only the caption / prose spec and adds the line '<!-- FIGURE CHANGED: <id> — <what> -->' right above its \`\`\`mermaid block so the figures step can find it; for a dropped figure, the edit removes its prose and marks '<!-- FIGURE DROPPED: <id> -->' above the block (the block itself stays until the figures step); a new figure gets a prose spec and '<!-- FIGURE NEW: <id> — <spec> -->' with no mermaid block. Read ${OUTLINE} to get anchors exact (copy sentences verbatim). Return the path, a summary, the number of edits per piece, and the open questions.
MAPS:
${JSON.stringify(maps).slice(0, 400000)}`, { label: 'synthesize:plan', phase: 'Synthesize', schema: FILE, effort: 'high' })
log(`plan: ${synth ? synth.summary : 'NULL'}`)
if (!synth) throw new Error('synthesizer returned null')

// ---------------------------------------------------------------- Revise (sequential: same file)
phase('Revise')
const revised = []
for (const piece of ['總論', '觀測篇', '可靠篇', '應變篇', 'tail']) {
  const r = await agent(`${CONTEXT}
TASK — Apply the plan for piece "${piece}". Read ${PLAN} (JSON; take pieces[].piece == "${piece}" — for "tail" that is the header blockquote and everything after the three parts). Then open ${OUTLINE} and apply the edits IN PLACE with the Edit tool, in the given order: structural edits first, then content. Keep the outline's conventions: numbered sections with bold titles, bullet sub-points, tables in Markdown, figure captions as 「圖說：…」, citations inline; Traditional Chinese (Taiwan), single "—". Never touch a \`\`\`mermaid block (only add the '<!-- FIGURE … -->' marker lines the plan specifies). Where an anchor cannot be found verbatim, find the sentence it clearly refers to and apply there; if genuinely absent, skip and say so. After applying, re-read the piece you edited once for coherence: no dangling references to cut sections, the 不重疊 rule (every number lands in exactly one place) holds, and a section you trimmed does not still promise content that moved. Return path, summary, applied count, skipped with reasons.`, { label: `revise:${piece}`, phase: 'Revise', schema: FILE, effort: 'high' })
  revised.push({ piece, r })
  log(`${piece}: ${r ? `${r.applied} applied, ${r.skipped.length} skipped` : 'NULL'}`)
}

// ---------------------------------------------------------------- Verify structure + decision record
phase('Verify')
const verify = await agent(`${CONTEXT}
TASK — Structural verification of the revised ${OUTLINE}. Read ${PLAN} (structure + open_questions) and ${CODEX}, then the revised outline in full. Check: (1) every 致命 and 重要 Codex item is either resolved in the text (quote the passage) or explicitly rejected with a reason recorded in the header blockquote; (2) the structure matches the plan (sections present / cut / merged; three artefacts + SLO spec; schedule; word budget stated); (3) every Mermaid block is unchanged except for marker comments, and every figure marked CHANGED / DROPPED / NEW has a matching entry in the plan; (4) no dangling cross-reference ("見 §七" to a section that no longer exists; a 來源對照 row for a source no longer cited; a References row for a source not in the body); (5) no number appears in two pieces (the 不重疊 rule); (6) nothing restates the eight written articles; (7) only sources present in the digest / notes files are cited (spot-check 20 new citations against ${DIR}/conference_digest.md, ${DIR}/book_ai_agent_book.md, ${DIR}/arxiv.md, ${CONF}/notes_sep10.md, ${CONF}/notes_sep11.md). pass=true only if (1)–(4) and (7) hold; list everything else in remaining / new_problems, verbatim enough that a reviser can act.`, { label: 'verify:structure', phase: 'Verify', schema: VERIFY, effort: 'high' })
log(`verify: pass=${verify ? verify.pass : 'NULL'}, remaining=${verify ? verify.remaining.length : '?'}, new=${verify ? verify.new_problems.length : '?'}`)
let fix = null
if (verify && !verify.pass) {
  fix = await agent(`${CONTEXT}
TASK — Fix the remaining structural problems in ${OUTLINE} IN PLACE (Edit tool), nothing else. Never touch a \`\`\`mermaid block. Return path, summary, applied, skipped.
PROBLEMS:
${JSON.stringify([...(verify.remaining || []), ...(verify.new_problems || [])], null, 1)}`, { label: 'fix:structure', phase: 'Verify', schema: FILE, effort: 'high' })
}

const record = await agent(`${CONTEXT}
TASK — Write ${DIR}/selection.md: the decision record of this mid-month cycle (期中加圈). It is NOT a new selection: the three themes stay. Read ${PREV}/selection.md (format), ${PLAN}, the revised ${OUTLINE} header and §1, ${DIR}/conference_digest.md §1–3 and §4, ${DIR}/book_ai_agent_book.md §1. Write in Traditional Chinese (Taiwan), single "—": (1) a header blockquote: date ${TODAY}, trigger (AGNTCon + MCPCon Japan Sep 10–11; AI Agents in Depth v2.0; Codex review of 2026-09-07), and a pointer that the 2026-09 selection remains the base; (2) 「12 月改了什麼」— the re-cut in one table (before → after per piece), the three artefacts, the schedule, the Codex items accepted / modified / rejected with one-line reasons, the new anchors (conference sessions and book chapters) in a table with ids; (3) 「10 月四篇要插什麼」— one paragraph pointing to conference_digest.md §4 (the insertion table) and the rule that insertions add evidence and never reword the author's prose; (4) 「11 月的備忘」— the conference / book material that November's outline should pick up (from conference_digest.md §5 and the book's ch.7 / ch.2), as a short list, no outline edits made; (5) 「這一圈的限制」— what stays true from the 2026-09 judges (the four 修正 for 2026-12) plus anything the conference contradicted. Keep it under 2,500 CJK characters. Return path and summary.`, { label: 'record:selection', phase: 'Verify', schema: FILE, effort: 'medium' })

return { maps: Object.fromEntries(Object.entries(maps).map(([k, v]) => [k, v ? (v.summary || v.rationale || 'ok') : null])), plan: synth, revised: revised.map(x => ({ piece: x.piece, applied: x.r ? x.r.applied : null, skipped: x.r ? x.r.skipped : null })), verify, fix, record }
