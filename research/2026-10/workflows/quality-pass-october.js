// HISTORICAL RECORD ONLY (superseded 2026-09-23): do not run or reuse this workflow.
// Its prompts preserve the retired voice rules for traceability, not current guidance.
// Historical handbook references point to research/2026-09/voice_brief.history.md.
// For new writing or review, read STYLE.md and research/2026-09/voice_brief.md,
// then the current month's style_brief.md; use the reusable research/workflows/ scripts.
// REQUIRES (not in the repo): the mechanical gates this run was verified with live in
// .context/quality/, which is gitignored — p-check.sh (voice_brief.history §9.2 invariants vs git
// HEAD, plus num-exceptions.txt), protected-check.sh (+ protected.json), mirror-check.sh,
// voice-check.sh. So this file is a readable record, not a runnable template. Promoting
// them into research/scripts/ is worth doing and is NOT a copy job: p-check.sh diffs
// against git HEAD, so once the articles are committed it passes trivially — it needs a
// base-ref argument and a test before it becomes repo API.
export const meta = {
  name: 'research-2026-10-quality-pass',
  description: 'HISTORICAL RECORD ONLY — do not run or reuse. Readability and flow pass over the four unreleased October articles, driven by the four per-article audits: three sequential in-place passes per article (terms → flow → the inserted paragraphs), a two-lens verify, the English mirror, a voice pass and the zh-tw gate — every stage ending with the voice_brief.history §9.2 mechanical invariants and the §9.4 protected-sentence check.',
  phases: [
    { title: 'Gloss', detail: 'per article: first-occurrence definitions, plain-Chinese replacements, identities' },
    { title: 'Flow', detail: 'per article: seams, broken references, opening/closing beats, long sentences, duplicates' },
    { title: 'Insert', detail: 'per article with insertions: rewrite as scene + payoff, move to the audited position' },
    { title: 'Verify', detail: 'fidelity lens + reader lens, then fix' },
    { title: 'Mirror', detail: 'apply the zh diff to the English edition; regenerate pastes' },
    { title: 'Voice', detail: 'rules + ear lenses over the changed lines; revise' },
    { title: 'zh-tw', detail: 'Taiwan-usage gate over the changed lines' },
  ],
}

const ROOT = args.root
const TODAY = args.today
const Q = `${ROOT}/.context/quality`
const VOICE = `${ROOT}/research/2026-09/voice_brief.history.md`
const STYLE = `${ROOT}/research/2026-09/style_brief.md`
const DIGEST = `${ROOT}/research/2026-10/conference_digest.md`
const NOTES = `${ROOT}/.context/research/2026-09-conf/notes_sep10.md and ${ROOT}/.context/research/2026-09-conf/notes_sep11.md`
const ARTICLES = [
  { dir: '2026-10-green-overview', name: '總論', insert: false },
  { dir: '2026-10-green-testing', name: '測試篇', insert: true },
  { dir: '2026-10-green-review', name: 'Review 篇', insert: true },
  { dir: '2026-10-green-reliability', name: '可靠度篇', insert: true },
]

const common = (a) => `Repo root ${ROOT}; absolute paths only; never cd. Today is ${TODAY}.
FILE: ${ROOT}/${a.dir}/article.md — ${a.name} of the October series, the author's own Traditional-Chinese prose, written and scheduled on Medium but not yet published. The English edition ${ROOT}/${a.dir}/article.en.md is mirrored by a LATER stage; do not touch it in this stage.
DIAGNOSIS: ${Q}/${a.dir}.zh.md — an editor's audit of this file, with verbatim quotes and line numbers. Line numbers were taken at git HEAD and earlier stages may have shifted them: ALWAYS locate a finding by its verbatim quote (grep -nF), never by line number.
STANDARDS: ${VOICE} — read with sed: §9.2 (lines 564–605, the eighteen untouchables), §9.3 (606–613, how a gloss is written), §9.4 (614–625, the protected claims), and §十 (665 to end: fifteen before/after examples the author approved in September — imitate their shapes, do not invent new ones). ${STYLE} for the series voice.
HARD RULES (voice_brief.history §9.2; the gates below check them mechanically): P1 every number and its precision unchanged; P2 a number's qualifier stays in the same sentence or paragraph; P3 names of studies, tools, communities stay verbatim — add "what it is" beside a name, never replace it; P4 Uncle Bob, Teddy, Böckeler, James Bach keep their names; P5 every link unchanged; P6 mermaid blocks and their positions unchanged; P7 tables keep columns, rows and order (an overlong cell may be lifted into prose); P8 code/yaml/text blocks unchanged to the character; P9 headings unchanged; P10/§9.4 the protected claims stay verbatim — never add 可能／或許／建議／在某些情況下, never 只能→最好, never 不看→較不倚重; P11 every 誠信裝置 (self-disclosure, hedge on evidence, "筆者的判斷") stays — may be split into its own sentence, never deleted, merged or weakened; P12 the TL;DR block is untouched entirely; P13 the series navigation line and the 系列文章 block untouched; P14 References untouched; P15/P16 the AI 協作說明 and the closing Medium line untouched; P17 the lines that defer to 11 月／12 月 untouched — do not import November or December material; P18 English technical terms stay English; new prose uses the single "—", never "——".
VOICE: allowed connectives are only 但／所以／也就是說／其實／實際上／事實上／相反 (never 因此／然而／但是／於是／不過／當然／換句話說／首先／其次／總之); continuity comes from 冒號導引句, 時間副詞 and 代詞回指; new text says 我, not 筆者; 讀者 is a forbidden word; no imperatives at the reader; a paragraph ends on a judgement, not on a deposited fact.
METHOD: Edit tool, one change at a time, verbatim old_string; never Write the whole file. Reply with one line per change (diagnosis item → what you did) and the two gate outputs.
GATES — run both at the end and paste the output; both must pass, fix before returning if not:
  bash ${Q}/p-check.sh ${a.dir}
  bash ${Q}/protected-check.sh ${a.dir}`

const ISSUES = { type: 'object', required: ['checked', 'issues'], properties: {
  checked: { type: 'integer' },
  issues: { type: 'array', items: { type: 'object', required: ['quote', 'problem', 'fix', 'severity'], properties: {
    quote: { type: 'string', description: 'verbatim current text, unique enough to Edit on' },
    problem: { type: 'string' },
    fix: { type: 'string', description: 'exact replacement text, or "REVERT-TO: <original sentence>"' },
    severity: { type: 'string', enum: ['meaning-changed', 'wrong-gloss', 'invariant', 'still-unclear', 'made-worse', 'style'] },
  } } },
} }

const gloss = (a) => `${common(a)}
STAGE 1 of 3 — 術語. Apply the diagnosis sections A1 (可直接改成白話), A2 (必須保留，但第一次出現要給定義) and the identity items in E3／D4 (人名、機構、書第一次出現要給身分).
- A1: replace the flagged wording with the plain Chinese the diagnosis directs — unless P3 protects a name, in which case keep the name and add the plain words beside it.
- A2: add a parenthetical gloss at the FIRST editable prose occurrence (括號一句，不開新段, §9.3 style); keep the original term. If the first occurrence is inside a protected quote, a table, the TL;DR, a heading or a code block, the diagnosis names the prose place to use — follow it.
- A gloss must be TRUE. Derive it from the article's own later definition, from the References source, or from the cited notes/digest; when unsure, reuse the article's own words from where the term is defined. A wrong gloss is worse than none.
- Unify inconsistent renderings (e.g. intent／意圖, constraint／約束, escalation／舉手) exactly as the diagnosis decides; keep proper names (constraint tests) as names.
Do not do the B/C/D/E items — later stages handle them.`

const flow = (a) => `${common(a)}
STAGE 2 of 3 — 脈絡與句子. Apply, in this order, the diagnosis sections:
- B (接不上的段落): add the half-sentence back-reference, lead-in or bridge the diagnosis directs; fix broken references (a pronoun pointing at something not yet introduced); reorder or move sentences/paragraphs only where the diagnosis says so, and only within the same section.
- C (起承轉合): add the 路線圖句 where directed (never inside the TL;DR or a protected quote); after the closing blockquote add the 「這比什麼更長期」 sentence the diagnosis asks for; fix the "三" mismatches; keep the 下一篇 pointer.
- D (既有的「放下就走」段落 — NOT the AGNTCon/book insertion paragraphs, which stage 3 handles): add the one sentence of 鋪陳 or 解讀 the diagnosis asks for, in the author's judgement voice.
- E (可讀性熱點): split the flagged long sentences at the places suggested; untangle 的-stacks; rewrite the passive stacks; merge the flagged duplicates keeping ONE occurrence — when merging, every number with its qualifier (P2), every protected claim (P10) and every 誠信裝置 (P11) must survive; if a merge would lose one, keep both passages instead.
Follow the §十 examples' shapes. Do not add glosses here (stage 1 did) and do not touch the insertion paragraphs (stage 3).`

const insert = (a) => `${common(a)}
STAGE 3 of 3 — the inserted paragraph(s). This file carries one or two paragraphs inserted on 2026-09-16 with AGNTCon Tokyo / book evidence; find them with: git show b15506b -- ${ROOT}/${a.dir}/article.md (the '+' lines; earlier stages may have edited their wording — locate the CURRENT paragraph by its distinctive proper nouns). Follow diagnosis section D exactly:
1. MOVE the paragraph to the position D recommends (anchor on verbatim sentences); if D says the position is right, leave it.
2. REWRITE it as two short paragraphs. First, 場景鋪陳: who, when, what they built, what they admitted on stage — a scene, not a citation; the material is in ${DIGEST} and ${NOTES}, and every quoted line you use must exist verbatim there (grep -F to confirm). A slide quote follows §3.2's three beats: one lead-in sentence → the original (中英並列 when the source is English or Japanese) → one or two sentences of reading. Second, 證據與收攏: the fact with its citation → the 誠信註記 ("我沒讀原文…" / "觀察值，不是門檻") kept but as a concession clause, not the final beat → one closing sentence that says what this advances for THIS section, in the author's judgement voice, on the exact angle D names (e.g. "四條量的都是產出品質，沒有一條量它多常想越界").
3. Keep every number, session id, slide number and every References entry unchanged (P1, P5, P14). Give the company and the conference their identity once (A2 may already have done it — do not double it).
4. Add the bridge sentence(s) D asks for so the following paragraph or section connects (e.g. the next section's opener picks up the thread).
5. Each of the two paragraphs ≤ 4 sentences; ≤ 120 CJK characters per sentence; single "—".
Then re-read the whole section once for flow and fix anything the move broke (a 「這四種」 that lost its antecedent, a 「表裡的一列」 now pointing across a paragraph).`

const lensFidelity = (a) => `You are a FIDELITY checker. Repo ${ROOT}; absolute paths; never cd.
Compare git HEAD with the working tree: git diff -U0 HEAD -- ${ROOT}/${a.dir}/article.md (read all of it). For every changed hunk judge, sentence by sentence: (1) did the meaning, strength or scope of any claim change? A reworded sentence must say the same thing with the same confidence; (2) is every added gloss factually right — check it against the article's own definition of the term, the References source, or ${DIGEST}; (3) did any number, or a qualifier next to a number (領域、樣本、"相關非因果"、"不是巢狀"), move to another paragraph or vanish? (4) was any protected claim (voice_brief lines 608–619) or any 誠信裝置 altered, merged or softened? (5) any November/December content imported? any "——"? any 因此／然而／但是／換句話說／可能／或許／建議 introduced? (6) any quote attributed to a slide or a speaker that does not exist verbatim in ${DIGEST} or ${NOTES}?
Also run and paste: bash ${Q}/p-check.sh ${a.dir} ; bash ${Q}/protected-check.sh ${a.dir}
Report only with the current verbatim text in 'quote' and an exact replacement (or "REVERT-TO: <original>") in 'fix'. Do not flag style.`

const lensReader = (a) => `You are the target READER: a Taiwanese Engineering VP who knows engineering but not the agent circle's jargon. Repo ${ROOT}; absolute paths; never cd.
Read the CURRENT ${ROOT}/${a.dir}/article.md from the first line to the last, in order, at reading speed. Then read section F (三行總結) of ${Q}/${a.dir}.zh.md to know what the edit was supposed to fix.
Report, with verbatim quotes: (1) any term you still could not understand at its first prose occurrence; (2) any paragraph whose first sentence still does not connect to the previous one (quote both); (3) any content you read twice; (4) the AGNTCon / book paragraphs — do they now read as a scene that advances the section's argument, or still as a fact deposited and left? quote the seam if any remains; (5) any place where the edit made it WORSE: over-explaining, a gloss inside a punchline, a broken rhythm, a sentence that now reads like a translator wrote it, a section opener that lost its shape; (6) the opening — do you know where the article is going after the first section; the closing — does it land.
Severity: still-unclear / made-worse / style. Do not propose stylistic preferences; report what stopped you.`

const fixPrompt = (a, issues) => `${common(a)}
FIX — apply these verified issues, one at a time, nothing else. A "REVERT-TO" fix restores the original sentence verbatim. Where two issues touch the same sentence, apply the fidelity one first. After all edits run both gates and paste the output.
ISSUES:
${JSON.stringify(issues, null, 1)}`

const mirror = (a) => `Repo ${ROOT}; absolute paths; never cd. Today ${TODAY}.
The English edition ${ROOT}/${a.dir}/article.en.md must mirror the Chinese ${ROOT}/${a.dir}/article.md 1:1. The Chinese was just revised; the spec for what to change is: git diff HEAD -- ${ROOT}/${a.dir}/article.md (read the whole diff first).
For every hunk apply the equivalent edit to the English file at the corresponding place — the two files are paragraph-aligned; find the English sentence that corresponds to the zh anchor (proper nouns and numbers are the same in both) and read three paragraphs around it before editing so the register matches the EN edition (international VP reader; the EN text is the author's own English, not a translation to be smoothed).
Rules: glosses that explain a concept are kept in English; glosses that only fixed a Chinese rendering (intent／意圖) have no English counterpart — skip them; moved paragraphs move the same way; rewritten insertion paragraphs are rewritten in English with the same scene, the same quotes (English slide quotes verbatim, Japanese ones with the same English gloss the zh uses), the same concession clause and the same closing judgement. Numbers, links, mermaid, code blocks, headings, tables, TL;DR, References, the 系列文章 block and the AI-collaboration note are untouched (the gate checks them).
Then regenerate both pastes and run the gate, and paste all output:
  cd ${ROOT} && python3 research/scripts/article_to_paste.py ${a.dir} && python3 research/scripts/article_to_paste.py ${a.dir} --lang en && bash ${Q}/p-check.sh ${a.dir}
Do NOT run the full test suites (the main loop runs them once at the end). Reply with one line per hunk mirrored and the outputs.`

const voiceRules = (a) => `Repo ${ROOT}; absolute paths; never cd. The author's voice manual is ${VOICE}. Only the CHANGED lines of ${ROOT}/${a.dir}/article.md are in scope: get them with git diff -U3 HEAD -- ${ROOT}/${a.dir}/article.md ('+' lines are the new text; context lines are the author's own writing and your model).
RULES LENS. Check every '+' line against: §1.2 筆者 (new text uses 我), §1.3 讀者 is forbidden, §1.4 我們, §1.6 no imperatives at the reader; §2.2 connectives (only 但／所以／也就是說／其實／實際上／事實上／相反); §2.3 dash usage; §2.4 the author's real pause tools are 冒號 and 「」; §2.5 semicolons only for symmetric contrast; §3.1 a number needs four beats (宣告→樣本→數字→收攏); §3.2 name and verb before the numbers; §3.3 identity at first appearance; §6.2 the five allowed hedges, §6.3 the forbidden ones; §5 the phrase bank — prefer constructions the author has used. Quote the rule when you call a violation. Return one finding per '+' line that needs work, with a rewrite that keeps every fact, number and citation.`

const voiceEar = (a) => `Repo ${ROOT}; absolute paths; never cd. Only the CHANGED lines of ${ROOT}/${a.dir}/article.md are in scope: git diff -U6 HEAD -- ${ROOT}/${a.dir}/article.md.
EAR LENS. Read each '+' line where it landed — the sentence before and after are the author's. One question: would the author, rereading a year from now, stop at this line and know someone else wrote it? Seams: it explains what the previous sentence already set up; it changes temperature (the author is dry and declarative; new lines often arrive eager or explanatory); it is a different length from its neighbours; three 的 in a chain; it ends flat where the author ends on a judgement; a gloss that interrupts a punchline; a bridge sentence that announces instead of connecting. Read ${STYLE} for the series shape. Return one finding per '+' line that needs work, with a rewrite that keeps every fact, number and citation; 'reads-as-author' lines are not reported.`

const VOICE_FINDINGS = { type: 'object', required: ['findings'], properties: { findings: { type: 'array', items: { type: 'object', required: ['quote', 'why', 'rewrite'], properties: { quote: { type: 'string', description: 'the current + line, verbatim' }, why: { type: 'string' }, rewrite: { type: 'string' } } } } } }

const voiceRevise = (a, findings) => `${common(a)}
VOICE REVISION — two lenses judged the lines this pass added or changed. Apply the rewrites below with Edit, one at a time; where both lenses rewrote the same line, merge into one line that satisfies both. Only lines that appear as '+' in git diff HEAD -- ${ROOT}/${a.dir}/article.md may change; every fact, number, citation, protected claim and 誠信裝置 stays. After editing: run both gates, then regenerate the zh paste: cd ${ROOT} && python3 research/scripts/article_to_paste.py ${a.dir}
FINDINGS:
${JSON.stringify(findings, null, 1)}`

const zhtw = (a) => `${common(a)}
zh-tw GATE over the changed lines only. Get them with git diff -U0 HEAD -- ${ROOT}/${a.dir}/article.md. Load the checker via ToolSearch "select:mcp__zhtw-mcp__zhtw". Run each changed paragraph through mcp__zhtw-mcp__zhtw (content_type="markdown", fix_mode="lexical_safe", fix_output="search_replace", translationese_domain="technical", detect_ai=false, output="compact"), one paragraph per call, never the whole file.
Apply suggestions ONE AT A TIME with judgment. ACCEPT: 用戶→使用者, 後綴→字尾, 是一個→是 (when grammatical), 信息→資訊, 軟件→軟體, 質量→品質, 缺省→預設, 屏幕→螢幕, 網絡→網路, 視頻→影片, 服務器→伺服器. REJECT (measured false positives): 通過→透過 when 通過 means passed; 縮進→縮排; 原始碼→原始程式碼; 導入→匯入 when it means adoption; 構建→建構 in a quoted title; 轉發→轉寄; 數據→資料 (this author keeps 數據 for statistics); 前綴→字首; 斷點→中斷點; 只讀→唯讀 when it means "only reads"; anything inside a quotation, code span, id, URL, number, English term or book title. Translationese warnings (的的不休, 定語堆疊 ≥ 40 chars) are the valuable part: split or add a comma without changing meaning. Never introduce "——".
Then run both gates and regenerate the zh paste: cd ${ROOT} && python3 research/scripts/article_to_paste.py ${a.dir}. Report accepted / rejected suggestions with reasons and the gate outputs.`

// ---------------------------------------------------------------- pipeline
log('Four article pipelines run in parallel; within an article every stage is sequential (same file). Each stage ends with the §9.2 invariants and the §9.4 protected-sentence gate.')

const results = await pipeline(ARTICLES,
  (_, a) => agent(gloss(a), { label: `gloss:${a.name}`, phase: 'Gloss', effort: 'high' }).then(r => ({ a, log: [r === null ? 'gloss: died' : 'gloss: ok'] })),
  (x, a) => agent(flow(a), { label: `flow:${a.name}`, phase: 'Flow', effort: 'high' }).then(r => ({ a, log: [...(x ? x.log : []), r === null ? 'flow: died' : 'flow: ok'] })),
  (x, a) => a.insert
    ? agent(insert(a), { label: `insert:${a.name}`, phase: 'Insert', effort: 'high' }).then(r => ({ a, log: [...(x ? x.log : []), r === null ? 'insert: died' : 'insert: ok'] }))
    : Promise.resolve({ a, log: [...(x ? x.log : []), 'insert: n/a'] }),
  (x, a) => parallel([
      () => agent(lensFidelity(a), { label: `fidelity:${a.name}`, phase: 'Verify', schema: ISSUES, effort: 'high' }),
      () => agent(lensReader(a), { label: `reader:${a.name}`, phase: 'Verify', schema: ISSUES, effort: 'high' }),
    ]).then(vs => {
      const issues = vs.filter(Boolean).flatMap(v => v.issues)
      log(`${a.name}: verify — fidelity ${vs[0] ? vs[0].issues.length : 'died'}, reader ${vs[1] ? vs[1].issues.length : 'died'}`)
      return { a, log: [...(x ? x.log : []), `verify: ${issues.length} issues`], issues }
    }),
  (x, a) => (x && x.issues && x.issues.length)
    ? agent(fixPrompt(a, x.issues), { label: `fix:${a.name}`, phase: 'Verify', effort: 'high' }).then(r => ({ a, log: [...x.log, r === null ? 'fix: died' : 'fix: ok'] }))
    : Promise.resolve({ a, log: [...(x ? x.log : []), 'fix: none needed'] }),
  (x, a) => agent(mirror(a), { label: `mirror:${a.name}`, phase: 'Mirror', effort: 'high' }).then(r => ({ a, log: [...(x ? x.log : []), r === null ? 'mirror: died' : 'mirror: ok'] })),
  (x, a) => parallel([
      () => agent(voiceRules(a), { label: `voice-rules:${a.name}`, phase: 'Voice', schema: VOICE_FINDINGS, effort: 'high' }),
      () => agent(voiceEar(a), { label: `voice-ear:${a.name}`, phase: 'Voice', schema: VOICE_FINDINGS, effort: 'high' }),
    ]).then(vs => {
      const f = vs.filter(Boolean).flatMap(v => v.findings)
      log(`${a.name}: voice — ${f.length} lines to revise`)
      return { a, log: [...(x ? x.log : []), `voice: ${f.length} findings`], findings: f }
    }),
  (x, a) => (x && x.findings && x.findings.length)
    ? agent(voiceRevise(a, x.findings), { label: `voice-revise:${a.name}`, phase: 'Voice', effort: 'high' }).then(r => ({ a, log: [...x.log, r === null ? 'voice-revise: died' : 'voice-revise: ok'] }))
    : Promise.resolve({ a, log: [...(x ? x.log : []), 'voice-revise: none'] }),
  (x, a) => agent(zhtw(a), { label: `zhtw:${a.name}`, phase: 'zh-tw', effort: 'medium' }).then(r => ({ a, log: [...(x ? x.log : []), r === null ? 'zhtw: died' : 'zhtw: ok'], report: r ? String(r).slice(0, 1500) : null })),
)

return results.filter(Boolean).map(r => ({ article: r.a.dir, stages: r.log, zhtw: r.report }))
