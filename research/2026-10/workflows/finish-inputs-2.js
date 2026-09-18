export const meta = {
  name: 'research-2026-10-phase-a3',
  description: 'Finish phase A after the second usage-limit cut: write the 19 missing Sep 10 afternoon session blocks (split three ways) plus the day cross-cutting section, run the arXiv sweep (two sweepers + one composer), verify the three digests the last run never checked (book, x, community), then write the conference digest in three passes and verify it.',
  phases: [
    { title: 'Notes', detail: 'Sep 10 afternoon: 3 writers → assemble → cross-cutting → verify' },
    { title: 'ArXiv', detail: '2 sweepers → composer → verify' },
    { title: 'Check', detail: 'skeptic per unverified digest, sequential' },
    { title: 'Digest', detail: 'conference digest in 3 passes → verify → fix' },
  ],
}

const ROOT = args.root
const TODAY = args.today
const CONF = ROOT + '/.context/research/2026-09-conf'
const RAW = ROOT + '/.context/research/2026-10'
const OUT = ROOT + '/research/2026-10'
const PREV = ROOT + '/research/2026-09'
const NOTES10 = CONF + '/notes_sep10.md'
const DIGEST = OUT + '/conference_digest.md'

const COMMON = `
You are working inside the git repo at ${ROOT}. Use absolute paths only; never cd. Today is ${TODAY}.
The author is Kochi Chuang (Medium @fantasybz; Senior Software Engineer @ Appier; CNCF Kubestronaut; software-testing background; writes long-form Traditional-Chinese Medium articles for Engineering VPs / Staff engineers, one theme per month = 總論 + 三部曲).
The three planned themes (outlines in ${PREV}/): 2026-10 綠燈不是驗收 (testing / review / reliability of agent output — four articles ALREADY WRITTEN and scheduled on Medium but not yet published, in ${ROOT}/2026-10-green-*/article.md), 2026-11 同一份規格，跑十次 (output variance as a harness acceptance metric, spec-driven), 2026-12 把 Agent 當 Production Workload — Agent 的 SRE (observability / SLO / accountability of agents; outline ${PREV}/2026-12-sre-for-agents.md; a second-model review at ${PREV}/codex-review-2026-12-sre-for-agents.md said it must be re-cut around flight recorder / accountability).
Backlog items are numbered in ${PREV}/backlog.md (1 blast radius, 2 knowledge loss, 3 agent runtime as platform, 4 skills/memory/compaction, 5 exploratory testing of agents, 6 model supply, 7 brownfield DDD, 8 multi-agent topology, 9 deskilling).
Rules: quote numbers exactly as the source states them and say where (slide N / [hh:mm:ss] / file); never invent a number, id, name or quote; when a deck is image-only say so instead of guessing; label vendor-reported figures as such. Write in English with Chinese kept where the source is Chinese. Your final text reply is a 10-line summary; the FILE is the deliverable.`

// ---------------------------------------------------------------- schemas + helpers
const ISSUES = {
  type: 'object',
  properties: {
    checked: { type: 'integer', description: 'number of claims sampled and checked' },
    issues: { type: 'array', items: { type: 'object', properties: {
      quote: { type: 'string', description: 'the exact text in the file that is wrong or unsupported' },
      problem: { type: 'string', description: 'what the source actually says, with file + slide/timestamp/line' },
      fix: { type: 'string', description: 'the corrected text, or DELETE' },
      severity: { type: 'string', enum: ['wrong-number', 'unsupported', 'misattributed', 'format', 'truncated'] },
    }, required: ['quote', 'problem', 'fix', 'severity'] } },
    complete: { type: 'boolean', description: 'file ends cleanly and covers everything the task asked for' },
    missing: { type: 'array', items: { type: 'string' }, description: 'sections, chapters or sessions the file should cover but does not' },
  },
  required: ['checked', 'issues', 'complete', 'missing'],
}

const verifyPrompt = (file, sources, must, n) => `You are a skeptical fact-checker. Today is ${TODAY}. Repo root ${ROOT}; absolute paths only, never cd.
File under review: ${file}. Sources it must be faithful to: ${sources}.
Do this: (1) read the file end to end; confirm it ends cleanly (not mid-sentence, no dangling heading) and that it contains: ${must}. (2) Sample at least ${n} concrete claims — numbers, quoted lines, attributions (speaker, company, slide, timestamp, arXiv id, page id, handle, reaction count, chapter §) — favouring the ones most likely to be reused in an article — and check each against the source text with grep/sed. A claim is an issue if the number differs, the quote is not in the source, the attribution is wrong, or the source is image-only and the file states a figure anyway. Do NOT flag stylistic choices or paraphrases that keep the meaning. Report an issue only when you have the source line in front of you. Return the structured result.`

const fixPrompt = (file, issues) => `Apply these fact-check corrections to ${file} (repo ${ROOT}; absolute paths, never cd) with the Edit tool, one at a time, changing nothing else. If a fix says DELETE remove just that clause or sentence. If 'missing' lists absent sections, chapters or sessions, add them from the sources named (read the surrounding file to match its format exactly). Afterwards run tail -3 on the file to confirm it ends cleanly. Reply with one line per correction applied.
${JSON.stringify(issues, null, 2)}`

const verifyFix = async (label, phase, file, sources, must, n, effort) => {
  const v = await agent(verifyPrompt(file, sources, must, n), { label: `verify:${label}`, phase, schema: ISSUES, effort: effort || 'high' })
  if (!v) { log(`${label}: verifier died`); return { label, file, verified: false } }
  log(`${label}: ${v.checked} claims checked, ${v.issues.length} issues, complete=${v.complete}, missing=${v.missing.length}`)
  if (v.issues.length || !v.complete || v.missing.length) {
    await agent(fixPrompt(file, { issues: v.issues, missing: v.missing, complete: v.complete }), { label: `fix:${label}`, phase, effort: 'low' })
  }
  return { label, file, verified: true, checked: v.checked, issues: v.issues.length, missing: v.missing }
}

// one retry for the long writers: a session-limit death is not always permanent
const writeOnce = async (prompt, label, phase, effort) => {
  const a = await agent(prompt, { label, phase, effort })
  if (a !== null) return a
  log(`${label}: died, retrying once`)
  return agent(prompt, { label: `${label}:retry`, phase, effort })
}

const NOTES_SOURCES = `${CONF}/sessions.md, ${CONF}/events.json, ${CONF}/files_txt/*.txt, ${CONF}/ocr/*/, ${CONF}/aaif_txt/*.txt, ${CONF}/yt/*.txt`

// ---------------------------------------------------------------- Notes: Sep 10 afternoon, split three ways
const NOTES_FORMAT = `The file ${NOTES10} already holds the Thursday 10 September 2026 keynote block and morning breakouts (16 '### ' blocks under '## Part 1' and '## Part 2'). Read its header (lines 1-12, for the legend on slide numbering and transcript conventions) and at least three full existing blocks (e.g. sed -n '115,190p') and copy that format EXACTLY: a heading '### ✅/▫️ Title — Speaker, Company  (\`id\`, time, hall, track, language[, level])', then the bullets: Materials / Thesis / Key claims & numbers (indented sub-bullets, numbers quoted verbatim with slide or page markers) / Mechanisms, specs, projects named / Case study or data / Quotable lines / Cross-references (to other sessions in either day's notes, where a real link exists) / Relevance with theme tags (2026-10 / 2026-11 / 2026-12 / backlog#N / NEW) and a Signal 1-5 score. Depth should match the existing blocks: a talk with a real deck gets a long block, a description-only talk gets a short honest one.
Afternoon sessions were NOT livestreamed: the attached deck plus the sched description (${CONF}/sessions.md and ${CONF}/events.json, which also carry the full speaker line, track, hall, language and level) are the only sources. Say 'Materials: deck only' or 'Materials: description only' honestly and never invent a figure for an image-only deck.`

const pmWriter = (n, range, items) => `${COMMON}
${NOTES_FORMAT}
TASK: do NOT touch ${NOTES10}. Write a NEW file ${CONF}/_pm_part${n}.md containing ONLY the session blocks below, in the time order given, in that exact format, with no file header and no '## ' heading — just the '### ' blocks, separated by a blank line. Another agent will concatenate your file into the notes.
Sessions for you (${range}):
${items}
Before you finish, run grep -c '^### ' on your file and confirm the count matches the number of sessions listed above, and tail -3 to confirm it ends cleanly.`

const PM1 = `- 2QlDC ▫️ 13:30 Do Tools Still Matter? MCP Tool Design in the Age of Code Mode — Ruben Casas, Postman. Deck: ${CONF}/files_txt/2QlDC__do-tools-still-matter-agentcon-japan-template-applied.txt (keynote-parser export: slide order only approximate, master slides mixed in — say so).
- 2RCwp ✅ 13:30 Designing Trust Boundaries for Agent-to-Agent Systems — Ryuji Iijima (飯島竜児), SoftBank. Deck: ${CONF}/files_txt/2RCwp__AGNTCon_MCPCon_Japan2026登壇資料_SoftBank_Corp_飯島竜児.txt (Japanese deck; quote Japanese with an English gloss).
- 2RExH ▫️ 13:30–15:05 Workshop: Governing AI Agent Actions: MCP and Beyond — Shannon Williams & Chris (see sessions.md for full names/companies). No deck: sched description only.
- 2Qn4a ✅ 14:05 The Agent Builder Loop from Daily Work to OSS — Minoru Onda, KDDI Agile Development Center. Deck: ${CONF}/files_txt/2Qn4a__The_Agent_Builder_Loop_from_Daily_Work_to_OSS.txt
- 2Wbgx ▫️ 14:05 Who Owns the Agentic Loop? — Angie Jones, AAIF. No deck.`

const PM2 = `- 2QlDL ✅ 14:40 The Production Gap: Why Governing Agent Traffic Is the Key To Shipping Multi-Agent Systems — see sessions.md for the speaker. No deck.
- 2QlDO ▫️ 14:40 What Happens When Your MCP Tools Cost Money? — Prakash Rao (see sessions.md for company). Deck: ${CONF}/files_txt/2QlDO__agntconjapan2026_final-20260913215511.txt
- 2WbyL ▫️ 15:10 Sponsor Activity: Workato — Demo Session. One or two lines.
- 2QlDF ▫️ 15:35 Stop Giving Agents Tokens: Securing With Side-Car Proxies — Ritwik Ranjan. Deck: ${CONF}/files_txt/2QlDF__Aksh-AgentCon-Japan-Final.txt (PPTX export with '--- slide N' markers).
- 2QlDR ▫️ 15:35 Lessons From Building a Generative UI Runtime for MCP Apps — Rabi Guha, Thesys. No deck.
- 2TAFy ✅ 15:35 Architecting Agent-Native Data Layers: Managing Persistent State Across MCP Tools — see sessions.md. No deck.`

const PM3 = `- 2RcMn ▫️ 16:10 Tasks at Scale: How MCP's New Task Lifecycle Powers Long-Running Agentic Systems — see sessions.md. No deck.
- 2RpyS ✅ 16:10–17:45 Workshop: Enterprise Agentic AI: Architecting Autonomous Java Systems for Production — Red Hat / IBM. Intro deck: ${CONF}/files_txt/2RpyS__Intro_-_Hands-on_workshop__Enterprise_Agentic_AI__Architecting_Autonomous_Java_Systems_for_Production.txt plus OCR under ${CONF}/ocr/2RpyS__*/ (page markers p-N).
- 2TjiE ▫️ 16:10 Building an AI for Security Exception Tickets: What Actually Worked — Juan Coren (see sessions.md). Deck: ${CONF}/files_txt/2TjiE__AIForSecurityExceptionTickets.txt
- 2QlDX ✅ 16:45 Intent as Code: Why Existing Permissions Aren't Enough for AI — Masaya Nakamura. Deck: ${CONF}/files_txt/2QlDX__Intent-as-Code_13_.txt
- 2QlDa ▫️ 16:45 Running an MCP Proxy at Scale — Camila Rondinini, Anthropic. Decks: ${CONF}/files_txt/2QlDa__Running_an_MCP_Proxy_at_Scale.txt (EN; use this) and the AI-translated JP copy next to it (mention it only).
- 2QlDd ▫️ 17:20 Accelerating the Autonomous Web With WebMCP — Vin Lim, StaffOS. Deck: ${CONF}/files_txt/2QlDd__Accelerating_the_Autonomous_Web_with_WebMCP_-_Tokyo.txt
- 2QlDg ✅ 17:20 Legacy Meets LLM: Giving Frontier Models a Telephone (PSTN) Over MCP — Shinya Saito. Deck: ${CONF}/files_txt/2QlDg__agntcon-mcpcon-japan_en_shinya-saito.txt plus OCR under ${CONF}/ocr/2QlDg__*/
- 2QlGa ✅ 17:45 Attendee Reception. One line.`

const assemblePrompt = `${COMMON}
TASK: assemble the Sep 10 afternoon notes into ${NOTES10} WITHOUT rewriting or reordering anything that already exists.
Run exactly this, with Bash, after confirming all three part files exist and each ends cleanly:
  f=${NOTES10}
  test -s ${CONF}/_pm_part1.md && test -s ${CONF}/_pm_part2.md && test -s ${CONF}/_pm_part3.md || { echo MISSING; exit 1; }
  before=$(grep -c '^### ' "$f")
  printf '\\n## Part 3 — Afternoon breakouts (13:30–17:45)\\n\\n' >> "$f"
  cat ${CONF}/_pm_part1.md ${CONF}/_pm_part2.md ${CONF}/_pm_part3.md >> "$f"
  after=$(grep -c '^### ' "$f"); echo "blocks $before -> $after"
Then check: the count must go 16 -> 35; every one of these ids must appear backticked exactly once in the file — 2QlDC 2RCwp 2RExH 2Qn4a 2Wbgx 2QlDL 2QlDO 2WbyL 2QlDF 2QlDR 2TAFy 2RcMn 2RpyS 2TjiE 2QlDX 2QlDa 2QlDd 2QlDg 2QlGa (grep -c for each); blocks are in time order; and there is exactly one blank line between blocks, matching the spacing used in Part 2. Fix spacing or ordering with Edit if it is off; do not change block content. Report the before/after counts and any id that is missing or duplicated.`

const crossCutPrompt = `${COMMON}
TASK: append the final section to ${NOTES10}. Read the WHOLE file first (Parts 1, 2 and 3 — 35 session blocks) and also read the tail of ${CONF}/notes_sep11.md so Thursday's section does not duplicate Friday's. Then append, with Edit anchored on the file's last line, a section '## Cross-cutting observations (Thursday 10 September 2026)' covering the whole day, with these labelled parts:
(a) the 8–12 claims, numbers or mechanisms from this day that matter most for 2026-12 (observability, SLO, flight recorder, accountability, gateway / authorization, sandbox, memory, agent payments / cost attribution), each with session id + slide/timestamp;
(b) the same for 2026-10's four already-written articles (testing / review / reliability) and for 2026-11 (variance, determinism, cost fluctuation);
(c) contradictions between speakers on Thursday;
(d) what the author attended (✅) vs skipped, and what the skipped sessions had that the attended ones did not;
(e) new watch-list candidates (accounts, projects, dates, arXiv query strings) for ${PREV}/backlog.md.
Match the tone and density of the '## Cross-cutting observations (Friday 11 September 2026)' section at the end of ${CONF}/notes_sep11.md. Every claim carries its session id and slide/timestamp. Verify with tail -3 that the file ends cleanly and with grep -c '^### ' that the count is still 35.`

const chainNotes10 = async () => {
  const parts = await parallel([
    () => writeOnce(pmWriter(1, '13:30–14:30', PM1), 'write:sep10-pm-1', 'Notes', 'high'),
    () => writeOnce(pmWriter(2, '14:40–16:00', PM2), 'write:sep10-pm-2', 'Notes', 'high'),
    () => writeOnce(pmWriter(3, '16:10–17:45', PM3), 'write:sep10-pm-3', 'Notes', 'high'),
  ])
  const dead = parts.filter(p => p === null).length
  if (dead) { log(`sep10 afternoon: ${dead}/3 part writers died — not assembling`); return null }
  const asm = await agent(assemblePrompt, { label: 'assemble:sep10-pm', phase: 'Notes', effort: 'low' })
  log(`sep10 assemble: ${asm ? String(asm).slice(0, 200) : 'NULL'}`)
  if (asm === null) return null
  const cc = await writeOnce(crossCutPrompt, 'write:sep10-crosscut', 'Notes', 'high')
  if (cc === null) log('sep10 cross-cutting: died')
  return verifyFix('notes-sep10', 'Notes', NOTES10, NOTES_SOURCES,
    `'## Part 3 — Afternoon breakouts' with one '### ' block for every id 2QlDC 2RCwp 2RExH 2Qn4a 2Wbgx 2QlDL 2QlDO 2WbyL 2QlDF 2QlDR 2TAFy 2RcMn 2RpyS 2TjiE 2QlDX 2QlDa 2QlDd 2QlDg 2QlGa (grep the backticked ids; 35 '### ' blocks in total), every Part 3 block carrying the full bullet set that Part 1–2 blocks carry, and a final '## Cross-cutting observations (Thursday 10 September 2026)' section with labelled parts (a)–(e); Parts 1–2 unchanged (16 blocks, byte-identical — check with git diff or by reading them)`, 30)
}

// ---------------------------------------------------------------- ArXiv: two sweepers + composer
const SWEEP_COMMON = `${COMMON}
Load WebFetch via ToolSearch first; curl through Bash also works and is usually faster for the API.
Use the arXiv API, e.g. https://export.arxiv.org/api/query?search_query=all:%22coding+agent%22+AND+submittedDate:[202609010000+TO+${TODAY.replace(/-/g, '')}2359]&sortBy=submittedDate&sortOrder=descending&max_results=50 . If it returns 429, wait and retry once, then fall back to https://arxiv.org/search/?query=...&searchtype=all&order=-announced_date_first and https://arxiv.org/list/cs.SE/recent.
Window: papers submitted 2026-09-01 → ${TODAY}, plus anything older a query surfaces that the September sweep (${PREV}/arxiv.md) missed. Note submission vs announcement date gaps. Only record papers you actually retrieved.`

const sweepA = `${SWEEP_COMMON}
TASK: half A of the arXiv sweep → write ${RAW}/arxiv_sweep_a.md (a working file, not the final digest).
Run the 15 standard queries in ${ROOT}/research/prompts/arxiv.md (read it) plus the watch-list query strings in ${PREV}/backlog.md §訊號監看清單 (items 9–13; read that section and use its strings verbatim).
Write: (1) a query log — one line per query: the exact search_query string, the endpoint used, the hit count; (2) a table of every relevant paper found (arXiv id, title, submitted date, announced date if different, primary category, a one-line takeaway using the abstract's own numbers) — relevance over volume, but do not drop a paper just because it is borderline; (3) for the 12–15 most relevant, fetch https://arxiv.org/abs/<id> and write a 3–5 line summary under the table with the abstract's numbers quoted, marking each with *. Mark rows that already appear in ${PREV}/arxiv.md with '(seen 09)' (grep the id in that file).`

const sweepB = `${SWEEP_COMMON}
TASK: half B of the arXiv sweep → write ${RAW}/arxiv_sweep_b.md (a working file, not the final digest).
Run these December-specific queries: "agent observability" OR "agent telemetry"; "OpenTelemetry" AND agent; "service level" AND agent; "flight recorder" OR "audit log" AND agent; "agent accountability" OR "attestation"; "MCP gateway" OR "agent gateway" OR "tool authorization"; "agent memory" AND (benchmark OR evaluation); "sandbox" AND agent AND (Kubernetes OR container); "trace-based evaluation" agent; "agent-to-agent" OR "A2A protocol".
Same output shape as half A: (1) query log with hit counts; (2) table with one-line takeaways; (3) 12–15 starred deep reads from the abs pages. Mark rows already in ${PREV}/arxiv.md with '(seen 09)'.
PLUS, as a separate final section '## 2608.23610 full text': fetch https://arxiv.org/abs/2608.23610 and https://arxiv.org/pdf/2608.23610 and report EXACTLY what that paper's tuple contains, quoting the definition verbatim with the section/page it is on. ${PREV}/codex-review-2026-12-sre-for-agents.md turns on whether this paper really defines a behavioural tuple / content-addressed agent identity — answer that question with the paper's own words, and say so plainly if the PDF is unreachable or the paper does not say what the outline claims.`

const composeArxiv = `${COMMON}
TASK: compose ${OUT}/arxiv.md from the two sweep files ${RAW}/arxiv_sweep_a.md and ${RAW}/arxiv_sweep_b.md (read both in full). The previous sweep is ${PREV}/arxiv.md — read its header, cluster codes and table format and reuse them exactly. Window: 2026-09-01 → ${TODAY}.
Do not invent rows: every row must come from one of the two sweep files. Dedupe by arXiv id (a paper found by both halves gets one row listing both queries). If a sweep file is missing or short, say so in the header rather than padding.
Write: (1) header with method, date window and the full query list with hit counts (merged from both query logs); (2) the full table (arXiv id, title, date, one-line takeaway with the abstract's own numbers, cluster code) — 35+ rows if the sweeps found that many, starring the ones whose abstracts were read; (3) 'Theme clusters' 6–10 with what is new since 2026-09-05; (4) 'Signals worth an article' 8–12 with ids; (5) 'What this means for 2026-12' mapping papers onto observability / SLO / accountability and onto the objections in ${PREV}/codex-review-2026-12-sre-for-agents.md (does any paper define an outcome-evidence rule, a low-volume SLO method, a behavioural tuple / content-addressed agent identity? — carry the 2608.23610 finding from sweep B verbatim, including a negative finding); (6) 'What this means for 2026-10 and 2026-11' in five lines each. Use Write; make sure the file ends cleanly.`

const chainArxiv = async () => {
  const sw = await parallel([
    () => writeOnce(sweepA, 'sweep:arxiv-a', 'ArXiv', 'high'),
    () => writeOnce(sweepB, 'sweep:arxiv-b', 'ArXiv', 'high'),
  ])
  log(`arxiv sweeps: ${sw.filter(Boolean).length}/2 returned`)
  if (!sw.filter(Boolean).length) { log('arxiv: both sweepers died; composer skipped'); return null }
  const c = await writeOnce(composeArxiv, 'compose:arxiv', 'ArXiv', 'high')
  if (c === null) { log('arxiv: composer died'); return null }
  return verifyFix('arxiv', 'ArXiv', `${OUT}/arxiv.md`,
    `${RAW}/arxiv_sweep_a.md and ${RAW}/arxiv_sweep_b.md (every row must trace to one of them), the arXiv abs pages themselves (load WebFetch via ToolSearch and re-fetch https://arxiv.org/abs/<id> for at least 15 rows, favouring rows with numbers — an id that 404s or whose title differs is an issue), and ${PREV}/arxiv.md for the '(seen 09)' marks`,
    `a method header with the merged query list and hit counts, the table with 35+ rows (or an honest statement of why fewer), theme clusters, signals worth an article, 'What this means for 2026-12' including what 2608.23610's tuple actually contains, and the 2026-10 / 2026-11 section`, 25)
}

// ---------------------------------------------------------------- Check: the three digests never verified
const chainChecks = async () => {
  const out = []
  out.push(await verifyFix('book', 'Check', `${OUT}/book_ai_agent_book.md`,
    `${CONF}/ai-agent-book-en.txt (the EN PDF text; its table of contents lists every chapter and section) and the repo checkout ${CONF}/ai-agent-book/ (README.md, chapterN/README.md, docs/EXPERIMENT_STATUS.md, docs/EXPERIMENT_CONVENTIONS.md, extras/agent-lab/SCHEMA.md)`,
    `'## 2. Chapter by chapter' has a subsection for EVERY chapter in the EN PDF table of contents (list the chapters from the TOC first, then grep the file); every quoted number (e.g. the harness-only accuracy jump, experiment counts) and every chapter/§/EN-page reference resolves in the PDF text; no chapter summarised from the repo's stale index instead of the v2.0 text`, 30))
  out.push(await verifyFix('x-digest', 'Check', `${OUT}/x_digest.md`,
    `${RAW}/x_following_users.json, ${RAW}/x_following.json, ${RAW}/x_search_top.json, ${RAW}/x_bookmarks.json, ${RAW}/x_conf_search.json, ${ROOT}/research/prompts/x_digest.md`,
    `the eight sections the prompt asks for; handles, like/bookmark counts and account totals (301 / 291) that match the JSON; nothing attributed to an account absent from the JSON`, 25, 'medium'))
  out.push(await verifyFix('community-digest', 'Check', `${OUT}/community_digest.md`,
    `${RAW}/facebook_groups.json, ${RAW}/facebook_own.json, ${RAW}/linkedin_feed.json, ${RAW}/linkedin_saved.txt, ${RAW}/linkedin_conf_search.txt, ${RAW}/medium_stats.txt, ${RAW}/medium_articles.json, ${ROOT}/research/prompts/community_digest.md`,
    `the five sections the prompt asks for plus the watch-list check; reaction counts, group names, Medium views / reads / 完讀 percentages that match the raw files (recompute the percentages)`, 25, 'medium'))
  return out
}

// ---------------------------------------------------------------- Digest: three passes over one file
const DIGEST_COMMON = `${COMMON}
You are writing ${DIGEST} — the integrated digest of AGNTCon + MCPCon Japan 2026 (Tokyo, Sep 10–11; AAIF / Linux Foundation) for the monthly research loop, following the prompt at ${ROOT}/research/prompts/conference_digest.md (read it). This file WILL be committed to a public repo: quote public conference material and public X/LinkedIn posts freely, but do NOT copy the author's Facebook friends-only posts verbatim — paraphrase them and cite reaction counts only.
Inputs: ${CONF}/notes_sep10.md and ${CONF}/notes_sep11.md (per-session notes, both complete, each ending in a cross-cutting section — these are the ground truth), ${CONF}/sessions.md (77 items; ✅ = attended), ${CONF}/events.json, ${CONF}/aaif_txt/*.txt (aaif.io blog/news: A2A joins AAIF, sandbox phase, Agent Router, EU AI Act, MCP stateless usage, Keycloak MCP authz, Dex on long-running coding agents), ${RAW}/x_conf_search.json (X posts about the conference, 'metrics' is Chinese aria-label text), ${RAW}/linkedin_conf_search.txt (LinkedIn search pages), the author's own conference posts in ${RAW}/facebook_own.json (grep AGNTCon / 東京 / Tokyo / demo), ${OUT}/arxiv.md (this fortnight's sweep — if it does not exist yet, say so where you would have cited it instead of inventing), ${OUT}/book_ai_agent_book.md (Bojie Li's *AI Agents in Depth*, chapter §), and ${OUT}/x_digest.md + ${OUT}/community_digest.md (cross-reference only, do not repeat). The Codex review to close objections against: ${PREV}/codex-review-2026-12-sre-for-agents.md.
Every claim cites session id + slide/timestamp, or the aaif/X/LinkedIn source. Markdown. The whole file is ~4,000–6,000 words across ten numbered sections; you are writing part of it.`

const digest1 = `${DIGEST_COMMON}
TASK (pass 1 of 3): CREATE the file with Write, containing a title line and sections 1–3 only. Do not write sections 4–10; another pass appends them.
1. Header: what the event was, the organisers' numbers (companies, speakers, members, ambassadors), the four announcements, the author's attendance (count of ✅ sessions, the tracks chosen, what was skipped). Say which sources this digest rests on and their limits (afternoon Sep 10 not livestreamed, image-only decks, etc.).
2. **Ecosystem map after Tokyo**: AAIF projects (MCP, goose, AGENTS.md, agentgateway, A2A, Agent Router), working groups, sandbox phase, the two-gateway situation, what the Amsterdam (Sep 17–18) and NA (San Jose, Oct 22–23) editions will add.
3. **Twelve to eighteen mechanisms with numbers**, ranked by usefulness to 2026-12 (SRE for agents): each one paragraph: claim → number → source → which December section it feeds (總論 / 觀測篇 / 可靠篇 / 應變與追責篇) → whether it closes a Codex objection (e.g. OTel semconv span names, outcome evidence matrix, min_events, tamper boundary, signal availability matrix, who-vs-why audit gap).
End with tail -3 to confirm the file ends cleanly.`

const digest2 = `${DIGEST_COMMON}
TASK (pass 2 of 3): APPEND sections 4–6 to the existing ${DIGEST} (read what pass 1 wrote first, so you do not repeat it; append with Edit anchored on the last line, never rewrite sections 1–3).
4. **Insertion candidates for the four unpublished October articles**: a table — article (總論 / 測試篇 / Review 篇 / 可靠度篇), the real section heading, the claim to add (one sentence in Traditional Chinese as it could appear, ≤ 120 CJK chars), source session + slide, and why it strengthens rather than pads. 8–15 rows, each a genuinely new fact. The section headings MUST be real: grep '^## ' in ${ROOT}/2026-10-green-overview/article.md, ${ROOT}/2026-10-green-testing/article.md, ${ROOT}/2026-10-green-review/article.md, ${ROOT}/2026-10-green-reliability/article.md and quote them exactly. Before proposing a row, grep that article's References and body so you do not restate evidence it already carries.
5. **For 2026-11 (variance)**: what speakers said about determinism, same-prompt-different-output, cost fluctuation, decision-surface shrinking.
6. **Tensions**: where speakers contradicted each other (skills vs MCP tools, gateway vs sidecar, stateless MCP vs stateful sandboxes, agent-as-oncall vs bounded AI, code mode vs tool calls), with both sides' ids and slides.
End with tail -3 to confirm the file ends cleanly.`

const digest3 = `${DIGEST_COMMON}
TASK (pass 3 of 3): APPEND sections 7–10 to the existing ${DIGEST} (read what passes 1–2 wrote first; append with Edit anchored on the last line, never rewrite earlier sections).
7. **Social echo**: what X / LinkedIn / the author's own posts said, with counts; what Taiwanese communities did NOT say (cross-check ${OUT}/community_digest.md). Paraphrase the author's friends-only Facebook posts; reaction counts only.
8. **Quotable lines** (15–25, attributed, with id + slide/timestamp), drawn from both days' notes.
9. **Backlog and watch-list updates**: new accounts / projects / dates / arXiv query strings; which backlog item in ${PREV}/backlog.md each strengthens; anything that should become a NEW backlog item (agent identity / delegated authorization, carbon-aware agents, agent payments, PSTN/telephony, MCP task lifecycle).
10. **Book cross-check**: ${OUT}/book_ai_agent_book.md summarises Bojie Li's *AI Agents in Depth*; list 6–10 places where a conference talk and the book say the same thing (or the opposite), with the book's chapter § and the session id + slide — these are the strongest anchors for December.
End with tail -3 to confirm the file ends cleanly.`

const chainDigest = async (notesOk) => {
  if (!notesOk) { log('conference digest: Sep 10 notes are not complete; digest skipped') ; return null }
  const p1 = await writeOnce(digest1, 'write:digest-1-3', 'Digest', 'high')
  if (p1 === null) { log('conference digest: pass 1 died'); return null }
  const p2 = await writeOnce(digest2, 'write:digest-4-6', 'Digest', 'high')
  if (p2 === null) log('conference digest: pass 2 died')
  const p3 = await writeOnce(digest3, 'write:digest-7-10', 'Digest', 'high')
  if (p3 === null) log('conference digest: pass 3 died')
  return verifyFix('conference-digest', 'Digest', DIGEST,
    `${CONF}/notes_sep10.md, ${CONF}/notes_sep11.md, ${CONF}/sessions.md, ${CONF}/files_txt/*.txt, ${CONF}/aaif_txt/*.txt, ${RAW}/x_conf_search.json, ${RAW}/linkedin_conf_search.txt, ${RAW}/facebook_own.json, ${OUT}/book_ai_agent_book.md, ${OUT}/arxiv.md, and the four articles ${ROOT}/2026-10-green-*/article.md for the §4 headings`,
    `the ten numbered sections (header, ecosystem map, 12–18 mechanisms with numbers, October insertion table whose section headings really exist in the articles (grep '^## ' in each article.md — a heading that is not there verbatim is an issue), November material, tensions, social echo with counts, 15–25 quotable lines, backlog / watch-list updates, book cross-check with chapter §); no verbatim Facebook friends-only text (compare against ${RAW}/facebook_own.json)`, 40)
}

// ---------------------------------------------------------------- run
log('Sep 10 afternoon notes (3 writers → assemble → cross-cutting), the arXiv sweep (2 sweepers → composer) and the three unverified digests run in parallel; the conference digest starts once the notes and the sweep are in')

const [notes10, arxivRes, checks] = await parallel([
  chainNotes10,
  chainArxiv,
  chainChecks,
])

const notesOk = !!(notes10 && notes10.verified)
const digest = await chainDigest(notesOk)

return { notes10, arxiv: arxivRes, checks, digest }
