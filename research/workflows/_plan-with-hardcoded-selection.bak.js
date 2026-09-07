export const meta = {
  name: 'plan-next-three-themes',
  description: 'Propose, judge, select and outline the next three monthly Medium themes (總論 + 三部曲) from the research digests',
  phases: [
    { title: 'Propose', detail: '5 lenses × 4 candidate themes each' },
    { title: 'Merge', detail: 'dedupe into ≤10 distinct candidates' },
    { title: 'Judge', detail: '2 lensed judges + 1 adversarial refuter per candidate' },
    { title: 'Select', detail: 'pick 3, sequence Oct–Dec 2026' },
    { title: 'Outline', detail: 'full 總論 + 三部曲 outline per theme, critic, revise' },
    { title: 'Backlog', detail: 'runner-up themes for later months' },
  ],
}

const ROOT = '/Users/kochi.chuang/conductor/workspaces/medium-articles/yokohama'
const R = ROOT + '/.context/research'
const OUT = ROOT + '/research/2026-09'
const INPUTS = `
Read these files before doing anything (use the Read tool; they are long, read them in chunks if needed). Read style_brief.md and selection.md FULLY; for the three digests, read fully the sections relevant to the theme you are working on and skim the rest:
- /Users/kochi.chuang/conductor/workspaces/medium-articles/yokohama/research/2026-09/selection.md  (the final selection, with the judges' objections and the adjustments each theme must honour)
- ${R}/style_brief.md  (how the author writes, series format, audience, reception data)
- ${R}/x_digest.md  (X/Twitter: 355 top posts from followed accounts, 12 themes, debates, gaps)
- ${R}/arxiv.md  (232 arXiv papers May–Sept 2026, 10 clusters, 12 signals)
- ${R}/community_digest.md  (Taiwanese Facebook groups, the author's own FB/fan-page posts, LinkedIn, Medium stats)
- ${R}/notion_digest.md  (the author's OWN Notion: workshop notes, book notes, certification plans, drafts — read FULLY; this is the first-hand material each outline must draw on, and it flags corrections to the themes)
Also skim the four published articles so you know exactly what is already covered:
- ${ROOT}/2026-09-agentic-engineering-platform/article.md (總論)
- ${ROOT}/2026-09-agentic-org-design/article.md (一、組織篇)
- ${ROOT}/2026-10-agentic-harness-blueprint/article.md (二、技術篇)
- ${ROOT}/2026-11-agentic-eval-economics/article.md (三、營運篇)
Context: today is 2026-09-05. The author (@fantasybz, Kochi Chuang) publishes one THEME per month, each theme = one 總論 (overview, ~18 min read) + 三部曲 (three deep dives, ~8–12 min each), in Traditional Chinese (Taiwan) with an English edition. The next three themes are for 2026-10, 2026-11, 2026-12. Audience: Engineering VPs / EMs / Staff engineers / platform, SRE and QA leads in Taiwan.
`

const PROPOSAL_SCHEMA = {
  type: 'object', required: ['themes'],
  properties: { themes: { type: 'array', minItems: 4, maxItems: 4, items: {
    type: 'object', required: ['slug', 'title_zh', 'title_en', 'thesis_zh', 'why_now', 'evidence', 'author_fit', 'parts', 'overlap_risk'],
    properties: {
      slug: { type: 'string' }, title_zh: { type: 'string' }, title_en: { type: 'string' },
      thesis_zh: { type: 'string', description: 'one-line quotable thesis in Traditional Chinese' },
      why_now: { type: 'string', description: '3–6 sentences: what happened in the last 3 months that makes this urgent' },
      evidence: { type: 'array', minItems: 4, items: { type: 'object', required: ['source', 'ref', 'claim'], properties: { source: { type: 'string', description: 'x | arxiv | facebook | linkedin | medium-stats | article' }, ref: { type: 'string', description: 'URL, arXiv id, group name or post handle+date exactly as it appears in the digest' }, claim: { type: 'string' } } } },
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
      properties: { slug: { type: 'string' }, month: { type: 'string', description: '2026-10 | 2026-11 | 2026-12' }, title_zh: { type: 'string' }, title_en: { type: 'string' }, thesis_zh: { type: 'string' }, why_this: { type: 'string' }, adjustments: { type: 'string', description: 'changes made in response to judges/refuter' },
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
// Selection was made by the main loop on 2026-09-05 from the judged candidates (see research/2026-09/selection.md);
// the select agent hit the session usage limit twice, so it is hardcoded here to let Outline/Backlog resume.
const selection = {
 "selected": [
  {
   "slug": "agentic-green-is-not-done",
   "month": "2026-10",
   "title_zh": "綠燈不是驗收：agent 時代的測試、Review 與可靠度",
   "title_en": "Green Is Not Done: Testing, Review and Reliability for Agent Output",
   "thesis_zh": "CI 綠燈是 agent 的自我申報，不是驗收—別教 agent 怎麼測（TDD 儀式），去量它留下了什麼（mutation score、constraint tests、pass^k）；而 review 是決定 agent 對組織是加分還是負債的唯一控制點，重設計的重點不是讓人讀得更快，而是決定什麼值得人讀、誰審誰、AI 審 AI 何時該禁止。",
   "why_this": "合併兩個最高分候選 agentic-output-verification（38.5）與 review-is-the-control-point（37.0）；同一條驗證層：測試 → review → 可靠度閘門。作者最有立場的地盤（2023 測試系列、2025 雙層護欄、粉絲團的測試哲學）。",
   "adjustments": "(1) 標題級數字標領域：34% 寫成「在 SWE-Gate 的量測裡」；pass^k 的非 code 來源（Thinkingbox、READY）降為旁證，code 領域主幹用 SWE-Gate 2609.04167、SWE-NFI 2607.27409、OpenHarmony 2608.16022、2607.18057、2607.08885、escalation tool 2608.29460。(2) 總論以 James Bach《Taking Testing Seriously》為書錨（書評型長文完讀率最高 46–51%，方法清單型最低）。(3) 修正對自己數據的誤讀：與不確定性共舞是 619 views / 98 reads。(4) Review 篇的證據分兩層：真實 PR 資料集（2607.13196、2607.03316、2607.21997、2608.21311、2607.09902、2607.12428）驅動處方；實驗室異質配對（2607.21656）只說明原則並標明會隨 model 版本翻轉。(5) 台灣訊號誠實：DavidKo 貼文 9 與 3 反應；Uncle Bob mutation gate 40、Clean Code 2nd ed. 190/38 才是燒起來的。(6) 發布計畫含粉絲團分享。(7) 動筆前讀完全部引用 arXiv 的 abstract。",
   "parts": [
    {
     "title_zh": "一、測試篇：怎麼審一份 agent 寫的測試—斷言鬆綁、凍結 bug 與 mutation score",
     "focus": "「AI 說沒問題」之後 tester 要看什麼：assertion loosening、把現狀 bug 錄成 golden、覆蓋率是一條可以被改掉的斷言；mutation testing 當閘門而非 TDD 儀式；人對錯誤斷言判別只有 49%（2607.08885）所以要靠工具。"
    },
    {
     "title_zh": "二、Review 篇：Review 是控制點，不是瓶頸—分流、reviewer agent 艦隊與閉環禁令",
     "focus": "分流矩陣（人讀 intent 與 constraint，不讀 diff）、reviewer agent 的 YAML 與異質配對、社交工程 PR（「已預先核准」一句話讓 ~80% 外洩 PR 過關 2607.19267）、AI 審 AI 的禁用條件（2608.21311 兩季成長 100 倍）、approval artifact 綁人、每 +10pp 免審合併多 6% 維護負擔（2607.09902）。"
    },
    {
     "title_zh": "三、可靠度篇：綠燈是 34% 的謊言—constraint tests、pass^k 與授權擴張的閘門",
     "focus": "SWE-Gate：功能測試通過的修補有 221/644 違反 reviewer 實際加的約束 → 把 review 約束寫成可執行的 constraint tests；pass@1 與 pass^k 分開報；oversight budget（READY 2609.02095）；接回營運篇 G2 gate：授權擴張看 pass^k 與 escape rate，不看 pass@1。"
    }
   ]
  },
  {
   "slug": "same-spec-ten-runs",
   "month": "2026-11",
   "title_zh": "同一份規格，跑十次：把實作變異數當成 harness 的驗收指標",
   "title_en": "Same Spec, Ten Runs: Output Variance as the Acceptance Metric for Your Harness",
   "thesis_zh": "生成越便宜，「同樣的輸入會不會長出同樣的東西」越值錢。固定一份規格、不介入、跑 N 次，實作的變異數就是 harness 的驗收指標—變異數在 loop 裡，不在 spec 裡；spec 厚度、AGENTS.md conventions、Pattern Language skills 是三支調變異的槓桿，而不是上限。",
   "why_this": "台灣資料集分享數最高的技術訊號（搞笑談軟工 Teddy Chen 可重現性測試 298 反應 / 74 分享；Kim Kao bounded context 每次數量不同），已發布四篇沒碰，作者出席過工作坊有第一手材料。原候選 spec-is-the-new-source（37.0）被反方駁倒，駁倒理由全部採納：命題從「spec 決定上限」改成「變異在 loop、spec 是槓桿之一」。",
   "adjustments": "(1) 變異篇抬成總論脊椎：總論用 Teddy 的問題開場，決策工件是「固定 spec 跑 N 次」的變異門檻，接進營運篇 G2 gate 當第四軸。(2) 換題避開 Sean Grove「specs are the new code」與別人的「clean loop not clean code」留言。(3) 誠實引 2608.25399（spec 厚度改變 token +29.7% 但 run-to-run variance unchanged）與 2608.26197（deterministic planning constraints 做到 reproducibility 1.000）作為「變異在 loop」的證據。(4) 契約篇只做 spec → 可執行契約（2608.17177 contract-first、2606.27045 drift gate、2608.21208 spec 不可攜 F1 0.035、2608.25202 SpecMine）；ADR / 決策記憶縮成總論的 what / how / why（spec / AGENTS.md / ADR）地圖或第三篇一節。(5) 作者 10 月開跑自己的實驗：一個 repo、一份固定 spec、三種約束條件（無 / AGENTS.md conventions / Pattern Language skills）、每組 N≥10、量 AST 或結構相似度、測試通過率、review 約束違規數。(6) 社群訊號只用 Teddy 與 Kim Kao，不用 DavidKo 轉貼（7–13 反應）與 2025 年講題。",
   "parts": [
    {
     "title_zh": "一、規格篇：agent 與人都能驗收的規格長什麼樣—從 Example Mapping 到 agent 讀得懂的 spec",
     "focus": "BDD 是溝通不是工具（Dan North）；Example Mapping → Claude Code → Gherkin 與「四十條 Gherkin，然後呢」；user story 換完整 spec 讓 token +29.7% 但變異不變（2608.25399）；需求總是晚到、預先警告無效（2609.03028）。"
    },
    {
     "title_zh": "二、契約篇：spec 變成可執行的契約—contract-first、drift gate 與跨 vendor 的不可攜",
     "focus": "只做 what：contract-first tests（2608.17177）、drift gate（2606.27045）、SWE-Gate constraint tests 當非功能附件、spec 跨 agent 不可攜（F1 0.035，2608.21208）、SpecMine 47 萬份 spec（2608.25202）。"
    },
    {
     "title_zh": "三、變異篇：回答 Teddy 的問題—用「同一份規格的變異數」當 harness 的驗收指標",
     "focus": "作者自己的 N-run 實驗設計與結果；對照 2608.26197 證明變異在 loop；變異門檻接進營運篇 G2 scaling gate；三支槓桿（spec / conventions / Pattern Language）各降多少變異。"
    }
   ]
  },
  {
   "slug": "sre-for-agents",
   "month": "2026-12",
   "title_zh": "把 Agent 當 Production Workload：Agent 的 SRE—可觀測、可靠、可追責",
   "title_en": "Treat Agents as Production Workloads: SRE for Agents—Observable, Reliable, Accountable",
   "thesis_zh": "Agent 不是開發工具，是一個會花錢、會出事、會被打的 production workload—它需要 trace、SLO、error budget 與 on-call，而 SRE 十年來累積的方法剛好全部適用。Agent 的結案報告不是證據，trace 才是；沒裝儀表的 harness，你營運的不是產品，是傳聞。",
   "why_this": "與 coding-agent-blast-radius（34.8）幾乎同分（35.0），取 SRE：作者可信地盤（OTCA、Kubestronaut、2025 CNCF GenAI Observability 與觀測性反模式）在此而不在資安；反方指出非資安專職作者在資安題目被 CISO 抓到 overclaim 會傷整個系列。X digest 標記 agent observability 是 291 個追蹤帳號完全沒人寫的缺口—總論要正面承認「這題現在沒人在講」。排 12 月：接在 10、11 月之後交接點（pass^k、oversight budget、變異門檻）才有東西進 SLO；KubeCon NA 在 11 月。",
   "adjustments": "(1) 可靠篇砍到一個工件—agent SLO spec：SLI 只用 telemetry 拿得到的（run availability、tool-call error rate、latency、cost per successful task、oversight budget）；error budget 決定授權擴張；harness pin 與 diff 當 change management（2608.26218 28%→49%、2607.03691 每天兩版）。(2) 多 vendor failover、額度、被 ban、hybrid local 全部讓給 backlog 的席位經濟主題，只留一句。(3) K8s sandbox fleet（v1.37 scale-to-zero、pod certificates）壓成一節並標明 1,000 人規模。(4) 需求訊號誠實：不借 Claude Taiwan 席位抱怨；本主題訊號是 OTel GenAI semantic conventions（LinkedIn 儲存）、Alolita KubeCon Japan keynote、莊硯光 Grafana + Claude Code AIOps bot（17 分享，那是 agent 做 SRE 不是 SRE for agents，要說清楚）。(5) 資安面的 context 提權只留一段指向 backlog 的爆炸半徑主題。",
   "parts": [
    {
     "title_zh": "一、觀測篇：一次 agent run 的 trace 長什麼樣—OTel GenAI semantic conventions 落地",
     "focus": "把 harness 本身裝上儀表：run / tool-call / model-call span、cost per trace、eval-in-prod；結構化 trace 讓觀察者 token 少 14–15 倍（2609.01466）；Copilot cloud agent 6,400 萬筆日誌（2608.29204）當範例；復用既有 o11y stack，只加新 signal。"
    },
    {
     "title_zh": "二、可靠篇：Agent SLO—把 pass^k、oversight budget 與 harness 版本當 production dependency 管",
     "focus": "一個工件：agent SLO spec；error budget 決定授權擴張（接營運篇 gates）；harness pin / diff 當 change management；K8s sandbox 容量一節、標 1,000 人規模。"
    },
    {
     "title_zh": "三、應變與追責篇：Agent 出事的時候—incident response、flight recorder 與「誰批准了這個 PR」",
     "focus": "agent 當第一線 on-call 的邊界；agent 自己出事的 runbook；防竄改事件帳本（每事件 48µs、每 10 萬事件 $2.30 上鏈，2609.01931）；47 個平台 0 個預設輸出 content-addressed 身分（2608.23610）；vendor 條款對誰核准 agent PR 互相矛盾（2608.15678）。"
    }
   ]
  }
 ],
 "runners_up": [
  {
   "slug": "coding-agent-blast-radius",
   "title_zh": "Coding Agent 的爆炸半徑：漏洞在 harness，不在 model",
   "reason": "34.8，未駁倒；backlog 第一順位（最早 2027-01）。動筆前修：三個台灣案例都不是 coding-agent 事故（700 GB 國外故事、Zeabur 平台入侵、台新原文說不是 AI 失控）；2608.27443 是 113 位非技術使用者且 HITL 排名第一、2608.28502 平均 ASR 1.21%，不可 overclaim；先切分論文的 harness（vendor runtime）與系列的 harness layer。最好找資安協作者。"
  },
  {
   "slug": "context-engineering-evidence",
   "title_zh": "AGENTS.md 不會讓 agent 變聰明：Context、Skills 與 Memory 的實證報告",
   "reason": "33.5；命題調弱為「pass rate 對 context 檔不敏感，要配 quality 側指標成對讀」（2607.27250 僅 17 任務 / 288 run；2606.20512 +7.5pp 要誠實呈現）；compaction 部分與爆炸半徑衝突需二選一；skills 供應鏈可併入爆炸半徑。最早 2027-02。"
  },
  {
   "slug": "after-free-throughput-teams-people",
   "title_zh": "速度免費之後：規格、團隊與人的新瓶頸",
   "reason": "33.0，駁倒；規格篇已被 11 月吃掉，人篇證據撐不住（21x 是專案成長、N=21 質性研究）。若重建以「知識流失與維護債」為軸（2607.09902、2606.13298、2607.05677、2608.25241、DDDTW 66 反應、Kent Beck 91 反應），作為團隊層的組織篇續集。"
  },
  {
   "slug": "seat-economics-resilience-sovereignty",
   "title_zh": "別用座位數編 2027 預算：額度、斷線、被 ban 與 TOKEN 自由",
   "reason": "28.5；最強證據全是 Claude Taiwan 個人 Pro / Max 用戶抱怨，目標讀者買 Team / Enterprise seat 或 API；需要 3–5 家台灣公司企業層採購觀察才寫得動；作者地盤不含採購與 CFO 敘事。觀察中。"
  }
 ],
 "sequencing_rationale": "10 月先做驗證層：接在營運篇「eval 是唯一會複利的資產」之後最自然，作者立場最強、社群最需要中文材料。11 月的變異實驗要在 10 月開跑所以不能排第一；它與 10 月共用 constraint tests 與「量測不指示」的語言。12 月 SRE 需要前兩月產出的量（pass^k、oversight budget、變異門檻）才有 SLO 可定，並接 KubeCon NA 與年底 retro；預算季不適合它。"
}
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
    `${INPUTS}\nYou are a rigorous critic. Read the article plan at ${f.path} and check it against: (a) style_brief.md (format, voice, series shape, dash rule, Traditional Chinese Taiwan usage); (b) the four published articles (flag any section that repeats them instead of extending); (c) the three digests (every cited source/ref/number must actually exist there; flag anything invented or misquoted); (d) internal overlap between the 總論 and the three parts, and between the parts; (e) whether each part gives a Staff engineer or VP something they can act on (a reference implementation, a decision table, a gate); (f) whether the thesis is genuinely arguable and not a platitude. List issues with severity blocker/major/minor, where, problem, and a concrete fix.`,
    { label: `critic:${s.slug}`, phase: 'Outline', schema: CRITIC_SCHEMA, effort: 'high' }
  ).then(c => ({ file: f, critic: c })),
  (x, s) => agent(
    `${INPUTS}\nRevise the article plan at ${x.file.path} in place (Edit/Write tools) to resolve every blocker and major issue below, and the minor ones where cheap. Do not shorten the plan; keep the structure. Keep Traditional Chinese, single "—" dash. After editing, re-read the file once to confirm it is coherent. Return the path and a summary of what changed.\n\nISSUES:\n${JSON.stringify(x.critic, null, 1)}`,
    { label: `revise:${s.slug}`, phase: 'Outline', schema: FILE_SCHEMA, effort: 'high' }
  ).then(r => ({ theme: s, path: r ? r.path : x.file.path, summary: r ? r.summary : x.file.summary, critic: x.critic }))
)

phase('Backlog')
const backlog = await agent(
  `${INPUTS}\nWrite ${OUT}/backlog.md (Write tool) in Traditional Chinese: a topic backlog for months after 2026-12. Input: the runner-up candidates and the selection rationale below, plus the "gaps"/"signals"/"opportunities" sections of the three digests. For each backlog entry: title_zh, one-paragraph pitch, why it did not make the top three, what evidence would promote it, and the earliest sensible month. Order by promise. Also add a short section "訊號監看清單": 10–15 concrete signals (accounts, arXiv queries, FB groups, conference dates) to watch so the backlog can be re-ranked monthly. Return path and summary.\n\nSELECTION:\n${JSON.stringify(selection, null, 1)}`,
  { label: 'backlog', phase: 'Backlog', schema: FILE_SCHEMA }
)

return { selection, outlined: outlined.filter(Boolean).map(o => ({ month: o.theme.month, slug: o.theme.slug, title_zh: o.theme.title_zh, path: o.path, summary: o.summary, critic_overall: o.critic ? o.critic.overall : '' })), backlog, candidates_considered: scored.map(s => ({ slug: s.candidate.slug, title_zh: s.candidate.title_zh, avg: s.avg, refuted: s.refute ? s.refute.refuted : null, severity: s.refute ? s.refute.severity : null })) }