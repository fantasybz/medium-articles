export const meta = {
  name: 'research-2026-10-phase-a2',
  description: 'Finish phase A after the usage-limit cut: append the 19 missing Sep 10 afternoon items to notes_sep10.md, run the arXiv sweep, verify the five files the last session wrote but never checked (notes_sep11, notion, book, x, community), then write and verify the conference digest.',
  phases: [
    { title: 'Write', detail: 'Sep 10 afternoon notes; arXiv sweep' },
    { title: 'Check', detail: 'skeptic per existing file, sequential' },
    { title: 'Digest', detail: 'conference digest → verify → fix' },
  ],
}

const ROOT = args.root
const TODAY = args.today
const CONF = ROOT + '/.context/research/2026-09-conf'
const RAW = ROOT + '/.context/research/2026-10'
const OUT = ROOT + '/research/2026-10'
const PREV = ROOT + '/research/2026-09'

const COMMON = `
You are working inside the git repo at ${ROOT}. Use absolute paths only; never cd. Today is ${TODAY}.
The author is Kochi Chuang (Medium @fantasybz; Senior Software Engineer @ Appier; CNCF Kubestronaut; software-testing background; writes long-form Traditional-Chinese Medium articles for Engineering VPs / Staff engineers, one theme per month = 總論 + 三部曲).
The three planned themes (outlines in ${PREV}/): 2026-10 綠燈不是驗收 (testing / review / reliability of agent output — four articles ALREADY WRITTEN and scheduled on Medium but not yet published, in ${ROOT}/2026-10-green-*/article.md), 2026-11 同一份規格，跑十次 (output variance as a harness acceptance metric, spec-driven), 2026-12 把 Agent 當 Production Workload — Agent 的 SRE (observability / SLO / accountability of agents; outline ${PREV}/2026-12-sre-for-agents.md; a second-model review at ${PREV}/codex-review-2026-12-sre-for-agents.md said it must be re-cut around flight recorder / accountability).
Backlog items are numbered in ${PREV}/backlog.md (1 blast radius, 2 knowledge loss, 3 agent runtime as platform, 4 skills/memory/compaction, 5 exploratory testing of agents, 6 model supply, 7 brownfield DDD, 8 multi-agent topology, 9 deskilling).
Rules: quote numbers exactly as the source states them and say where (slide N / [hh:mm:ss] / file); never invent a number, id, name or quote; when a deck is image-only say so instead of guessing; label vendor-reported figures as such. Write in English with Chinese kept where the source is Chinese. Your final text reply is a 10-line summary; the FILE is the deliverable.`

// ---------------------------------------------------------------- schemas
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

const verifyFix = async (label, file, sources, must, n, effort) => {
  const v = await agent(verifyPrompt(file, sources, must, n), { label: `verify:${label}`, phase: 'Check', schema: ISSUES, effort: effort || 'high' })
  if (!v) { log(`${label}: verifier died`); return { label, file, verified: false } }
  log(`${label}: ${v.checked} claims checked, ${v.issues.length} issues, complete=${v.complete}, missing=${v.missing.length}`)
  if (v.issues.length || !v.complete || v.missing.length) {
    await agent(fixPrompt(file, { issues: v.issues, missing: v.missing, complete: v.complete }), { label: `fix:${label}`, phase: 'Check', effort: 'low' })
  }
  return { label, file, verified: true, checked: v.checked, issues: v.issues.length, missing: v.missing }
}

const NOTES_SOURCES = `${CONF}/sessions.md, ${CONF}/events.json, ${CONF}/files_txt/*.txt, ${CONF}/ocr/*/, ${CONF}/aaif_txt/*.txt, ${CONF}/yt/*.txt`

// ---------------------------------------------------------------- Write: Sep 10 afternoon
const SEP10 = `Attended (✅): 2RCwp, 2Qn4a, 2QlDL, 2TAFy, 2RpyS, 2QlDX, 2QlDg, 2QlGa. Not attended (▫️): all others. Time order and sources:
- 2QlDC ▫️ 13:30 Do Tools Still Matter? MCP Tool Design in the Age of Code Mode — Ruben Casas, Postman. Deck: ${CONF}/files_txt/2QlDC__do-tools-still-matter-agentcon-japan-template-applied.txt (keynote-parser export: slide order only approximate, master slides mixed in — say so).
- 2RCwp ✅ 13:30 Designing Trust Boundaries for Agent-to-Agent Systems — Ryuji Iijima (飯島竜児), SoftBank. Deck: ${CONF}/files_txt/2RCwp__AGNTCon_MCPCon_Japan2026登壇資料_SoftBank_Corp_飯島竜児.txt (Japanese deck; quote Japanese with an English gloss).
- 2RExH ▫️ 13:30–15:05 Workshop: Governing AI Agent Actions: MCP and Beyond — Shannon Williams & Chris (see sessions.md for full names/companies). No deck: sched description only.
- 2Qn4a ✅ 14:05 The Agent Builder Loop from Daily Work to OSS — Minoru Onda, KDDI Agile Development Center. Deck: ${CONF}/files_txt/2Qn4a__The_Agent_Builder_Loop_from_Daily_Work_to_OSS.txt
- 2Wbgx ▫️ 14:05 Who Owns the Agentic Loop? — Angie Jones, AAIF. No deck.
- 2QlDL ✅ 14:40 The Production Gap: Why Governing Agent Traffic Is the Key To Shipping Multi-Agent Systems — see sessions.md for the speaker. No deck.
- 2QlDO ▫️ 14:40 What Happens When Your MCP Tools Cost Money? — Prakash Rao (see sessions.md for company). Deck: ${CONF}/files_txt/2QlDO__agntconjapan2026_final-20260913215511.txt
- 2WbyL ▫️ 15:10 Sponsor Activity: Workato — Demo Session. One or two lines.
- 2QlDF ▫️ 15:35 Stop Giving Agents Tokens: Securing With Side-Car Proxies — Ritwik Ranjan. Deck: ${CONF}/files_txt/2QlDF__Aksh-AgentCon-Japan-Final.txt (PPTX export with '--- slide N' markers).
- 2QlDR ▫️ 15:35 Lessons From Building a Generative UI Runtime for MCP Apps — Rabi Guha, Thesys. No deck.
- 2TAFy ✅ 15:35 Architecting Agent-Native Data Layers: Managing Persistent State Across MCP Tools — see sessions.md. No deck.
- 2RcMn ▫️ 16:10 Tasks at Scale: How MCP's New Task Lifecycle Powers Long-Running Agentic Systems — see sessions.md. No deck. (This session was missing from the earlier list; it must be included.)
- 2RpyS ✅ 16:10–17:45 Workshop: Enterprise Agentic AI: Architecting Autonomous Java Systems for Production — Red Hat / IBM. Intro deck: ${CONF}/files_txt/2RpyS__Intro_-_Hands-on_workshop__Enterprise_Agentic_AI__Architecting_Autonomous_Java_Systems_for_Production.txt plus OCR under ${CONF}/ocr/2RpyS__*/ (page markers p-N).
- 2TjiE ▫️ 16:10 Building an AI for Security Exception Tickets: What Actually Worked — Juan Coren (see sessions.md). Deck: ${CONF}/files_txt/2TjiE__AIForSecurityExceptionTickets.txt
- 2QlDX ✅ 16:45 Intent as Code: Why Existing Permissions Aren't Enough for AI — Masaya Nakamura. Deck: ${CONF}/files_txt/2QlDX__Intent-as-Code_13_.txt
- 2QlDa ▫️ 16:45 Running an MCP Proxy at Scale — Camila Rondinini, Anthropic. Decks: ${CONF}/files_txt/2QlDa__Running_an_MCP_Proxy_at_Scale.txt (EN; use this) and the AI-translated JP copy next to it (mention it only).
- 2QlDd ▫️ 17:20 Accelerating the Autonomous Web With WebMCP — Vin Lim, StaffOS. Deck: ${CONF}/files_txt/2QlDd__Accelerating_the_Autonomous_Web_with_WebMCP_-_Tokyo.txt
- 2QlDg ✅ 17:20 Legacy Meets LLM: Giving Frontier Models a Telephone (PSTN) Over MCP — Shinya Saito. Deck: ${CONF}/files_txt/2QlDg__agntcon-mcpcon-japan_en_shinya-saito.txt plus OCR under ${CONF}/ocr/2QlDg__*/
- 2QlGa ✅ 17:45 Attendee Reception. One line.
Skip breaks (2QlQ9 coffee, 2QlMu lunch) and the all-day showcase (2TBxe).`

const notes10Prompt = `${COMMON}
TASK: the file ${CONF}/notes_sep10.md holds session notes for Thursday 10 September 2026 but only the keynote block and the morning breakouts (16 sessions, '## Part 1' and '## Part 2'); the agent writing it was cut off before the afternoon. Read the whole file first to learn its exact format (per-session block: '### ✅/▫️ Title — Speaker, Company  (\`id\`, time, hall, track, language)'; then bullets Materials / Thesis / Key claims & numbers / Mechanisms, architectures, specs, OSS named / Case study or data / Quotable lines / Relevance with theme tags (2026-10 / 2026-11 / 2026-12 / backlog#N / NEW) and a Signal 1–5 score). Then APPEND — do not rewrite or reorder anything that exists — a new section '## Part 3 — Afternoon breakouts (13:30–17:45)' with one block per item below, in time order, in that same format. Afternoon sessions were NOT livestreamed: the deck and the sched description (sessions.md / events.json, which also carry the full speaker line) are the only sources, so say 'Materials: deck only' or 'description only' honestly.
${SEP10}
After the sessions, append a final section '## Cross-cutting observations (Thursday 10 September 2026)' covering the WHOLE day (read Parts 1–2 again for this): (a) the 8–12 claims, numbers or mechanisms from this day that matter most for 2026-12 (observability, SLO, flight recorder, accountability, gateway / authorization, sandbox, memory, agent payments / cost attribution), each with session id + slide/timestamp; (b) the same for 2026-10's four written articles (testing / review / reliability) and for 2026-11 (variance, determinism, cost fluctuation); (c) contradictions between speakers; (d) what the author attended vs skipped and what the skipped sessions had that the attended ones did not; (e) new watch-list candidates (accounts, projects, dates, arXiv query strings) for the backlog. Use the Edit tool to append (anchor on the file's last line) or Write the whole file back with the existing text byte-identical; verify with tail -3 that it ends cleanly and with grep -c '^### ' that the count rose from 16 to 35.`

// ---------------------------------------------------------------- Write: arXiv
const arxivPrompt = `${COMMON}
TASK: arXiv sweep → ${OUT}/arxiv.md. The previous sweep is ${PREV}/arxiv.md (window 2026-05-01 → 2026-09-05; read its header, cluster codes and table format and reuse them). This sweep covers papers submitted 2026-09-01 → ${TODAY} (overlap is fine — mark rows already in the September file with '(seen 09)'), plus anything older that the new queries below surface and the September sweep missed.
Load WebFetch via ToolSearch first. Use the arXiv API, e.g. https://export.arxiv.org/api/query?search_query=all:%22coding+agent%22+AND+submittedDate:[202609010000+TO+${TODAY.replace(/-/g, '')}2359]&sortBy=submittedDate&sortOrder=descending&max_results=50 . If it returns 429, wait and retry once, then fall back to https://arxiv.org/search/?query=...&searchtype=all&order=-announced_date_first and https://arxiv.org/list/cs.SE/recent. Run at least 20 distinct queries: the 15 standard ones from ${ROOT}/research/prompts/arxiv.md, the watch-list strings in ${PREV}/backlog.md §訊號監看清單 (items 9–13), and these December-specific ones: "agent observability" OR "agent telemetry"; "OpenTelemetry" AND agent; "service level" AND agent; "flight recorder" OR "audit log" AND agent; "agent accountability" OR "attestation"; "MCP gateway" OR "agent gateway" OR "tool authorization"; "agent memory" AND (benchmark OR evaluation); "sandbox" AND agent AND (Kubernetes OR container); "trace-based evaluation" agent; "agent-to-agent" OR "A2A protocol". For the 20–30 most relevant papers fetch https://arxiv.org/abs/<id> and read the abstract properly (mark them * as the September file does).
Write: (1) header with method, date window and the full query list with hit counts; (2) the full table (arXiv id, title, date, one-line takeaway with the abstract's own numbers, cluster code) — aim for 35+ rows, relevance over volume; (3) 'Theme clusters' 6–10 with what is new since 2026-09-05; (4) 'Signals worth an article' 8–12 with ids; (5) 'What this means for 2026-12' mapping papers onto observability / SLO / accountability and onto the Codex objections in ${PREV}/codex-review-2026-12-sre-for-agents.md (does any paper define an outcome-evidence rule, a low-volume SLO method, a behavioural tuple / content-addressed agent identity? — 2608.23610 needs its full text: fetch https://arxiv.org/abs/2608.23610 and https://arxiv.org/pdf/2608.23610 and report exactly what the paper's tuple contains, quoting the definition); (6) 'What this means for 2026-10 and 2026-11' in five lines each. Only cite papers you actually saw; note submission vs announcement date gaps. Use Write; make sure the file ends cleanly.`

// ---------------------------------------------------------------- Digest
const confDigestPrompt = `${COMMON}
TASK: write ${OUT}/conference_digest.md following the prompt at ${ROOT}/research/prompts/conference_digest.md (read it) — the integrated digest of AGNTCon + MCPCon Japan 2026 (Tokyo, Sep 10–11; AAIF / Linux Foundation) for the monthly research loop. This file WILL be committed to a public repo: quote public conference material and public X/LinkedIn posts freely, but do not copy the author's Facebook friends-only posts verbatim (paraphrase them and cite reaction counts only).
Inputs (read all of them): ${CONF}/notes_sep10.md and ${CONF}/notes_sep11.md (per-session notes, both complete, each ending in a cross-cutting section), ${CONF}/sessions.md (77 items; ✅ = attended), ${CONF}/aaif_txt/*.txt (aaif.io blog/news: A2A joins AAIF, sandbox phase, Agent Router, EU AI Act, MCP stateless usage, Keycloak MCP authz, Dex on long-running coding agents), ${RAW}/x_conf_search.json (X posts about the conference, 'metrics' is Chinese aria-label text), ${RAW}/linkedin_conf_search.txt (LinkedIn search pages), the author's own conference posts in ${RAW}/facebook_own.json (grep AGNTCon / 東京 / Tokyo / demo), ${OUT}/arxiv.md (this fortnight's sweep), and ${OUT}/x_digest.md + ${OUT}/community_digest.md (already written; cross-reference only, do not repeat). The Codex review to close objections against: ${PREV}/codex-review-2026-12-sre-for-agents.md. The four October articles whose REAL section headings §4 must use: ${ROOT}/2026-10-green-overview/article.md, ${ROOT}/2026-10-green-testing/article.md, ${ROOT}/2026-10-green-review/article.md, ${ROOT}/2026-10-green-reliability/article.md (grep '^## ' in each).
Structure (Markdown, ~4,000–6,000 words; every claim cites session id + slide/timestamp or the aaif/X/LinkedIn source):
1. Header: what the event was, the organisers' numbers (companies, speakers, members, ambassadors), the four announcements, the author's attendance (count of ✅ sessions, the tracks chosen, what was skipped).
2. **Ecosystem map after Tokyo**: AAIF projects (MCP, goose, AGENTS.md, agentgateway, A2A, Agent Router), working groups, sandbox phase, the two-gateway situation, what the Amsterdam (Sep 17–18) and NA editions will add.
3. **Twelve to eighteen mechanisms with numbers** ranked by usefulness to 2026-12 (SRE for agents): each one paragraph: claim → number → source → which December section it feeds (總論 / 觀測篇 / 可靠篇 / 應變與追責篇) → whether it closes a Codex objection (e.g. OTel semconv span names, outcome evidence matrix, min_events, tamper boundary, signal availability matrix, who-vs-why audit gap).
4. **Insertion candidates for the four unpublished October articles**: a table — article (總論 / 測試篇 / Review 篇 / 可靠度篇), the real section heading, the claim to add (one sentence in Traditional Chinese as it could appear, ≤ 120 CJK chars), source session + slide, and why it strengthens rather than pads. 8–15 rows, each a genuinely new fact (not a restatement of arXiv evidence the articles already cite — grep the article's References first).
5. **For 2026-11 (variance)**: what speakers said about determinism, same-prompt-different-output, cost fluctuation, decision-surface shrinking.
6. **Tensions**: where speakers contradicted each other (e.g. skills vs MCP tools, gateway vs sidecar, stateless MCP vs stateful sandboxes, agent-as-oncall vs bounded AI, code mode vs tool calls).
7. **Social echo**: what X / LinkedIn / the author's own posts said, with counts; what Taiwanese communities did NOT say.
8. **Quotable lines** (15–25, attributed, with id + slide/timestamp).
9. **Backlog and watch-list updates**: new accounts / projects / dates / arXiv query strings; which backlog item each strengthens; anything that should become a new backlog item (e.g. agent identity / delegated authorization, carbon-aware agents, agent payments, PSTN/telephony, MCP task lifecycle).
10. **Book cross-check**: ${OUT}/book_ai_agent_book.md summarises Bojie Li's *AI Agents in Depth*; list 6–10 places where a conference talk and the book say the same thing (or the opposite), with the book's chapter § and the session id + slide — these are the strongest anchors for December.
Use Write to create the file; make sure it ends cleanly.`

// ---------------------------------------------------------------- run
phase('Write')
log('Sep 10 afternoon notes and the arXiv sweep run in parallel; the five unverified files are checked one after another; the conference digest starts once the Sep 10 notes pass')

const chainNotes10ThenDigest = async () => {
  const w = await agent(notes10Prompt, { label: 'write:notes-sep10-pm', phase: 'Write', effort: 'high' })
  if (w === null) { log('notes-sep10: writer died; digest skipped'); return { notes10: null, digest: null } }
  const v10 = await verifyFix('notes-sep10', `${CONF}/notes_sep10.md`, NOTES_SOURCES,
    `'## Part 3 — Afternoon breakouts' with one '### ' block for every id 2QlDC 2RCwp 2RExH 2Qn4a 2Wbgx 2QlDL 2QlDO 2WbyL 2QlDF 2QlDR 2TAFy 2RcMn 2RpyS 2TjiE 2QlDX 2QlDa 2QlDd 2QlDg 2QlGa (grep the backticked ids), and a final '## Cross-cutting observations (Thursday 10 September 2026)' section with parts (a)–(e); Parts 1–2 unchanged (16 blocks)`, 30)
  const d = await agent(confDigestPrompt, { label: 'write:conference-digest', phase: 'Digest', effort: 'high' })
  if (d === null) { log('conference digest: writer died'); return { notes10: v10, digest: null } }
  const vd = await agent(verifyPrompt(`${OUT}/conference_digest.md`,
    `${CONF}/notes_sep10.md, ${CONF}/notes_sep11.md, ${CONF}/sessions.md, ${CONF}/files_txt/*.txt, ${CONF}/aaif_txt/*.txt, ${RAW}/x_conf_search.json, ${RAW}/linkedin_conf_search.txt, ${RAW}/facebook_own.json, ${OUT}/book_ai_agent_book.md, ${OUT}/arxiv.md, and the four articles ${ROOT}/2026-10-green-*/article.md for the §4 headings`,
    `the ten numbered sections (header, ecosystem map, 12–18 mechanisms with numbers, October insertion table whose section headings really exist in the articles (grep '^## ' in each article.md), November material, tensions, social echo with counts, 15–25 quotable lines, backlog / watch-list updates, book cross-check with chapter §); no verbatim Facebook friends-only text (compare against ${RAW}/facebook_own.json)`, 40),
    { label: 'verify:conference-digest', phase: 'Digest', schema: ISSUES, effort: 'high' })
  if (vd && (vd.issues.length || !vd.complete || vd.missing.length)) {
    log(`conference digest: ${vd.checked} checked, ${vd.issues.length} issues, missing=${vd.missing.length}`)
    await agent(fixPrompt(`${OUT}/conference_digest.md`, { issues: vd.issues, missing: vd.missing, complete: vd.complete }), { label: 'fix:conference-digest', phase: 'Digest', effort: 'low' })
  } else if (vd) log(`conference digest: ${vd.checked} checked, clean`)
  return { notes10: v10, digest: vd ? { checked: vd.checked, issues: vd.issues.length, missing: vd.missing } : null }
}

const chainArxiv = async () => {
  const w = await agent(arxivPrompt, { label: 'write:arxiv', phase: 'Write', effort: 'high' })
  if (w === null) { log('arxiv: writer died'); return null }
  return verifyFix('arxiv', `${OUT}/arxiv.md`,
    `the arXiv API / abs pages the file cites (load WebFetch via ToolSearch and re-fetch https://arxiv.org/abs/<id> for at least 15 rows, favouring rows with numbers), and ${PREV}/arxiv.md for the '(seen 09)' marks`,
    `a method header with the query list, the table with 35+ rows, theme clusters, signals worth an article, 'What this means for 2026-12' including what 2608.23610's tuple actually contains, and the 2026-10 / 2026-11 section`, 25)
}

const chainChecks = async () => {
  const out = []
  out.push(await verifyFix('notes-sep11', `${CONF}/notes_sep11.md`, NOTES_SOURCES,
    `one '### ' block for every non-break Sep 11 item in ${CONF}/events.json (33 sessions; compare the backticked ids) and a final '## Cross-cutting observations' section; the agent that wrote the second half was cut off by a usage limit, so look for a block that stops early or repeats`, 30))
  out.push(await verifyFix('notion', `${OUT}/notion_digest.md`,
    `${RAW}/notion_pages.json, ${RAW}/notion_pages_content.json, ${ROOT}/.context/research/2026-09/notion_db_pages.json, ${PREV}/notion_digest.md, ${ROOT}/research/prompts/notion_digest.md`,
    `sections 1–7 as the prompt requires, the two stated caveats (db pages unusable this run — all six returned 'This page couldn't be found'; three key-holding pages redacted and 14 secret-looking lines masked), and a page id next to every page title; no API key, password or token reproduced anywhere in the file (grep for sk-, key, token, password)`, 30))
  out.push(await verifyFix('book', `${OUT}/book_ai_agent_book.md`,
    `${CONF}/ai-agent-book-en.txt (the EN PDF text; its table of contents lists every chapter and section) and the repo checkout ${CONF}/ai-agent-book/ (README.md, chapterN/README.md, docs/EXPERIMENT_STATUS.md, docs/EXPERIMENT_CONVENTIONS.md, extras/agent-lab/SCHEMA.md)`,
    `'## 2. Chapter by chapter' has a subsection for EVERY chapter in the EN PDF table of contents (list the chapters from the TOC first, then grep the file); every quoted number (e.g. the harness-only accuracy jump, experiment counts) and every chapter/§/EN-page reference resolves in the PDF text; no chapter summarised from the repo's stale index instead of the v2.0 text`, 30))
  out.push(await verifyFix('x-digest', `${OUT}/x_digest.md`,
    `${RAW}/x_following_users.json, ${RAW}/x_following.json, ${RAW}/x_search_top.json, ${RAW}/x_bookmarks.json, ${RAW}/x_conf_search.json, ${ROOT}/research/prompts/x_digest.md`,
    `the eight sections the prompt asks for; handles, like/bookmark counts and account totals (301 / 291) that match the JSON; nothing attributed to an account absent from the JSON`, 25, 'medium'))
  out.push(await verifyFix('community-digest', `${OUT}/community_digest.md`,
    `${RAW}/facebook_groups.json, ${RAW}/facebook_own.json, ${RAW}/linkedin_feed.json, ${RAW}/linkedin_saved.txt, ${RAW}/linkedin_conf_search.txt, ${RAW}/medium_stats.txt, ${RAW}/medium_articles.json, ${ROOT}/research/prompts/community_digest.md`,
    `the five sections the prompt asks for plus the watch-list check; reaction counts, group names, Medium views / reads / 完讀 percentages that match the raw files (recompute the percentages)`, 25, 'medium'))
  return out
}

const [confResult, arxivResult, checks] = await parallel([chainNotes10ThenDigest, chainArxiv, chainChecks])
return { conference: confResult, arxiv: arxivResult, checks }