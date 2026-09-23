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
  name: 'research-2026-10-quality-finish',
  description: 'HISTORICAL RECORD ONLY — do not run or reuse. Finish the October readability pass: the voice pass for the two articles whose lenses died, the recovered voice revision for Review, the zh-tw gate for all four, a final fidelity+reader verification, and a zh/en mirror audit that closes the one EN-only orphan sentence.',
  phases: [
    { title: 'Voice', detail: 'the two articles whose lenses died, plus the recovered findings for Review' },
    { title: 'zh-tw', detail: 'Taiwan-usage gate over the changed lines — all four' },
    { title: 'Final verify', detail: 'fidelity + reader over the whole diff, then fix' },
    { title: 'Mirror audit', detail: 'zh/en 1:1, regenerate both pastes, run every gate' },
  ],
}

const ROOT = args.root
const TODAY = args.today
const Q = ROOT + '/.context/quality'
const REC = Q + '/recovered'
const VOICE = ROOT + '/research/2026-09/voice_brief.history.md'
const STYLE = ROOT + '/research/2026-09/style_brief.md'
const DIGEST = ROOT + '/research/2026-10/conference_digest.md'
const NOTES = ROOT + '/.context/research/2026-09-conf/notes_sep10.md and ' + ROOT + '/.context/research/2026-09-conf/notes_sep11.md'

const ARTICLES = [
  { dir: '2026-10-green-overview', name: '總論', voice: 'done' },
  { dir: '2026-10-green-testing', name: '測試篇', voice: 'lenses' },
  { dir: '2026-10-green-review', name: 'Review 篇', voice: 'recovered' },
  { dir: '2026-10-green-reliability', name: '可靠度篇', voice: 'lenses' },
]

const common = (a) => `Repo root ${ROOT}; absolute paths only; never cd out of it. Today is ${TODAY}.
FILE: ${ROOT}/${a.dir}/article.md — ${a.name} of the October series, the author's own Traditional-Chinese prose, already written and scheduled on Medium but not yet published. The English edition ${ROOT}/${a.dir}/article.en.md is handled by the LAST stage of this run; do not touch it in this stage.
WHERE THIS RUN IS: a readability pass already applied, in this order, 術語 gloss → 脈絡與句子 → the AGNTCon/book insertion paragraphs → a two-lens verification and fix → the English mirror. All of that is in the working tree (git diff HEAD shows it). What is left is the voice pass, the zh-tw gate, one last verification and the mirror audit. Do not redo earlier stages.
DIAGNOSIS: ${Q}/${a.dir}.zh.md — the editor's audit that drove the pass, with verbatim quotes and line numbers. Line numbers were taken at git HEAD and every stage since has shifted them: ALWAYS locate text by verbatim quote (grep -nF), never by line number.
STANDARDS: ${VOICE} — read with sed: §9.2 (lines 564–605, the eighteen untouchables), §9.3 (606–613, how a gloss is written), §9.4 (614–625, the protected claims), and §十 (665 to end: fifteen before/after examples the author approved in September — imitate their shapes, do not invent new ones). ${STYLE} for the series voice.
HARD RULES (voice_brief.history §9.2; the gates below check them mechanically): P1 every number and its precision unchanged; P2 a number's qualifier stays in the same sentence or paragraph; P3 names of studies, tools, communities stay verbatim — add "what it is" beside a name, never replace it; P4 Uncle Bob, Teddy, Böckeler, James Bach keep their names; P5 every link unchanged; P6 mermaid blocks and their positions unchanged; P7 tables keep columns, rows, order and cell text (an overlong cell may be lifted into prose); P8 code/yaml/text blocks unchanged to the character; P9 headings unchanged; P10/§9.4 the protected claims stay verbatim — never add 可能／或許／建議／在某些情況下, never 只能→最好, never 不看→較不倚重; P11 every 誠信裝置 (self-disclosure, hedge on evidence, "筆者的判斷") stays — may be split into its own sentence, never deleted, merged or weakened; P12 the TL;DR block is untouched entirely; P13 the series navigation line and the 系列文章 block untouched; P14 References untouched; P15/P16 the AI 協作說明 and the closing Medium line untouched; P17 the lines that defer to 11 月／12 月 untouched — do not import November or December material; P18 English technical terms stay English; new prose uses the single "—", never "——".
VOICE: allowed connectives are only 但／所以／也就是說／其實／實際上／事實上／相反 (never 因此／然而／但是／於是／不過／當然／換句話說／首先／其次／總之); continuity comes from 冒號導引句, 時間副詞 and 代詞回指; new text says 我, not 筆者; 讀者 is a forbidden word except where it names real people who replied; no imperatives at the reader; a paragraph ends on a judgement, not on a deposited fact.
METHOD: Edit tool, one change at a time, verbatim old_string; never Write the whole file, never a sed/python rewrite script.
GATES — run both at the end and paste the output; both must pass, fix before returning if not:
  bash ${Q}/p-check.sh ${a.dir}
  bash ${Q}/protected-check.sh ${a.dir}`

const VOICE_FINDINGS = { type: 'object', required: ['findings'], properties: { findings: { type: 'array', items: { type: 'object', required: ['quote', 'why', 'rewrite'], properties: {
  quote: { type: 'string', description: 'the current + line, verbatim' }, why: { type: 'string' }, rewrite: { type: 'string' } } } } } }

const ISSUES = { type: 'object', required: ['checked', 'issues'], properties: {
  checked: { type: 'integer' },
  issues: { type: 'array', items: { type: 'object', required: ['quote', 'problem', 'fix', 'severity'], properties: {
    quote: { type: 'string', description: 'verbatim current text, unique enough to Edit on' },
    problem: { type: 'string' },
    fix: { type: 'string', description: 'exact replacement text, or "REVERT-TO: <original sentence>"' },
    severity: { type: 'string', enum: ['meaning-changed', 'wrong-gloss', 'invariant', 'still-unclear', 'made-worse', 'style'] },
  } } },
} }

const voiceRules = (a) => `Repo ${ROOT}; absolute paths; never cd. The author's voice manual is ${VOICE}. Only the CHANGED lines of ${ROOT}/${a.dir}/article.md are in scope: get them with git diff -U3 HEAD -- ${ROOT}/${a.dir}/article.md ('+' lines are the new text; context lines are the author's own writing and your model).
RULES LENS. Check every '+' line against: §1.2 筆者 (new text uses 我), §1.3 讀者 is forbidden, §1.4 我們, §1.6 no imperatives at the reader; §2.2 connectives (only 但／所以／也就是說／其實／實際上／事實上／相反); §2.3 dash usage; §2.4 the author's real pause tools are 冒號 and 「」; §2.5 semicolons only for symmetric contrast; §3.1 a number needs four beats (宣告→樣本→數字→收攏); §3.2 name and verb before the numbers; §3.3 identity at first appearance; §6.2 the five allowed hedges, §6.3 the forbidden ones; §5 the phrase bank — prefer constructions the author has used. Quote the rule when you call a violation. Return one finding per '+' line that needs work, with a rewrite that keeps every fact, number and citation. Report nothing for lines that already read as the author.`

const voiceEar = (a) => `Repo ${ROOT}; absolute paths; never cd. Only the CHANGED lines of ${ROOT}/${a.dir}/article.md are in scope: git diff -U6 HEAD -- ${ROOT}/${a.dir}/article.md.
EAR LENS. Read each '+' line where it landed — the sentence before and after are the author's. One question: would the author, rereading a year from now, stop at this line and know someone else wrote it? Seams: it explains what the previous sentence already set up; it changes temperature (the author is dry and declarative; new lines often arrive eager or explanatory); it is a different length from its neighbours; three 的 in a chain; it ends flat where the author ends on a judgement; a gloss that interrupts a punchline; a bridge sentence that announces instead of connecting. Read ${STYLE} for the series shape, and §十 of ${VOICE} for fifteen before/after pairs the author approved. Return one finding per '+' line that needs work, with a rewrite that keeps every fact, number and citation; lines that read as the author are not reported.`

const voiceRevise = (a, findings) => `${common(a)}
VOICE REVISION — two lenses judged the lines this pass added or changed. Apply the rewrites below with Edit, one at a time; where both lenses rewrote the same line, merge into ONE line that satisfies both rather than applying them in sequence. A lens may be wrong: if a rewrite would lose a fact, weaken a 誠信裝置, break a protected claim or read worse in place, keep the current line and say why in your reply. Only lines that appear as '+' in git diff HEAD -- ${ROOT}/${a.dir}/article.md may change; every fact, number, citation, protected claim and 誠信裝置 stays.
After editing: run both gates, then regenerate the zh paste: cd ${ROOT} && python3 research/scripts/article_to_paste.py ${a.dir}
Reply with one line per finding (applied / merged with #n / rejected + reason) and the gate output.
FINDINGS:
${JSON.stringify(findings, null, 1)}`

const voiceReviseRecovered = (a) => `${common(a)}
VOICE REVISION — the two lenses for this article finished in an earlier run and their findings were recovered from the workflow journal:
  ${REC}/voice-rules_Review篇.json   (12 findings)
  ${REC}/voice-ear_Review篇.json     (16 findings)
Read both files in full first. NOTE: the revision itself never ran, so none of these have been applied — every 'quote' should still be present verbatim in the article; grep -F each one to confirm before editing, and say so if one is missing.
Apply the rewrites with Edit, one at a time; where both lenses rewrote the same line, merge into ONE line that satisfies both rather than applying them in sequence. A lens may be wrong: if a rewrite would lose a fact, weaken a 誠信裝置, break a protected claim or read worse in place, keep the current line and say why in your reply. Only lines that appear as '+' in git diff HEAD -- ${ROOT}/${a.dir}/article.md may change; every fact, number, citation, protected claim and 誠信裝置 stays.
After editing: run both gates, then regenerate the zh paste: cd ${ROOT} && python3 research/scripts/article_to_paste.py ${a.dir}
Reply with one line per finding (applied / merged with #n / rejected + reason) and the gate output.`

const zhtw = (a) => `${common(a)}
zh-tw GATE over the changed lines only. Get them with git diff -U0 HEAD -- ${ROOT}/${a.dir}/article.md. Load the checker via ToolSearch "select:mcp__zhtw-mcp__zhtw". Run each changed paragraph through mcp__zhtw-mcp__zhtw (content_type="markdown", fix_mode="lexical_safe", fix_output="search_replace", translationese_domain="technical", detect_ai=false, output="compact"), one paragraph per call, never the whole file.
Apply suggestions ONE AT A TIME with judgment. ACCEPT: 用戶→使用者, 後綴→字尾, 是一個→是 (when grammatical), 信息→資訊, 軟件→軟體, 質量→品質, 缺省→預設, 屏幕→螢幕, 網絡→網路, 視頻→影片, 服務器→伺服器. REJECT (measured false positives): 通過→透過 when 通過 means passed; 縮進→縮排; 原始碼→原始程式碼; 導入→匯入 when it means adoption; 構建→建構 in a quoted title; 轉發→轉寄; 數據→資料 (this author keeps 數據 for statistics); 前綴→字首; 斷點→中斷點; 只讀→唯讀 when it means "only reads"; anything inside a quotation, code span, id, URL, number, English term or book title. Translationese warnings (的的不休, 定語堆疊 ≥ 40 chars) are the valuable part: split or add a comma without changing meaning. Never introduce "——".
Then run both gates and regenerate the zh paste: cd ${ROOT} && python3 research/scripts/article_to_paste.py ${a.dir}. Report accepted / rejected suggestions with reasons and the gate outputs.`

const lensFidelity = (a) => `You are a FIDELITY checker, the last one before this work is committed. Repo ${ROOT}; absolute paths; never cd.
Compare git HEAD with the working tree: git diff -U0 HEAD -- ${ROOT}/${a.dir}/article.md (read all of it — it is the whole readability pass, gloss through zh-tw). For every changed hunk judge, sentence by sentence: (1) did the meaning, strength or scope of any claim change? A reworded sentence must say the same thing with the same confidence; (2) is every added gloss factually right — check it against the article's own definition of the term, the References source, or ${DIGEST}; (3) did any number, or a qualifier next to a number (領域、樣本、"相關非因果"、"不是巢狀"), move to another paragraph or vanish? (4) was any protected claim (voice_brief lines 608–619) or any 誠信裝置 altered, merged or softened? (5) any November/December content imported? any "——"? any 因此／然而／但是／換句話說／可能／或許／建議 introduced? (6) any quote attributed to a slide or a speaker that does not exist verbatim in ${DIGEST} or ${NOTES}? (7) a sentence that was MOVED — does its 代詞回指 ("這句話"、"那幾格"、"這四種"、"上一段") still point at something that now precedes it?
Also run and paste: bash ${Q}/p-check.sh ${a.dir} ; bash ${Q}/protected-check.sh ${a.dir}
Report only with the current verbatim text in 'quote' and an exact replacement (or "REVERT-TO: <original>") in 'fix'. Do not flag style.`

const lensReader = (a) => `You are the target READER: a Taiwanese Engineering VP who knows engineering but not the agent circle's jargon. Repo ${ROOT}; absolute paths; never cd.
Read the CURRENT ${ROOT}/${a.dir}/article.md from the first line to the last, in order, at reading speed. Then read section F (三行總結) of ${Q}/${a.dir}.zh.md to know what the edit was supposed to fix.
Report, with verbatim quotes: (1) any term you still could not understand at its first prose occurrence; (2) any paragraph whose first sentence still does not connect to the previous one (quote both); (3) any content you read twice; (4) the AGNTCon / book paragraphs — do they now read as a scene that advances the section's argument, or still as a fact deposited and left? quote the seam if any remains; (5) any place where the edit made it WORSE: over-explaining, a gloss inside a punchline, a broken rhythm, a sentence that now reads like a translator wrote it, a section opener that lost its shape; (6) the opening — do you know where the article is going after the first section; the closing — does it land.
Severity: still-unclear / made-worse / style. Do not propose stylistic preferences; report what stopped you.`

const fixPrompt = (a, issues) => `${common(a)}
FINAL FIX — two lenses verified the finished article. Apply these issues with Edit, one at a time, nothing else. A "REVERT-TO" fix restores the original sentence verbatim. Where two issues touch the same sentence, apply the fidelity one first. An issue may be wrong: if applying it would lose a fact or weaken a 誠信裝置, leave the line and say why.
Anything you write here must already satisfy the zh-tw gate (Taiwan usage, no 用戶／信息／質量／軟件, no 的的不休) — the gate already ran and will not run again.
This stage edits the Chinese only; the mirror audit that follows carries structural changes to the English.
After all edits: run both gates and regenerate the zh paste: cd ${ROOT} && python3 research/scripts/article_to_paste.py ${a.dir}
ISSUES:
${JSON.stringify(issues, null, 1)}`

const mirrorAudit = (a) => `Repo ${ROOT}; absolute paths; never cd. Today ${TODAY}.
MIRROR AUDIT — the last stage. The English edition ${ROOT}/${a.dir}/article.en.md must mirror the Chinese ${ROOT}/${a.dir}/article.md 1:1 in content and structure. The English was mirrored mid-run; three stages have edited the Chinese since (voice pass, zh-tw, final fix), so it may have drifted.
Start with the mechanical check: bash ${Q}/mirror-check.sh ${a.dir} — it compares, section by section, the number of blank-line-separated blocks in the two files. Then read both diffs in full: git diff -U2 HEAD -- ${ROOT}/${a.dir}/article.md and git diff -U2 HEAD -- ${ROOT}/${a.dir}/article.en.md.
Judge every difference between the two diffs:
- MUST mirror: a sentence or paragraph added, deleted or moved; an insertion paragraph rewritten; a gloss that explains a concept; a bridge sentence; an opening roadmap sentence; a closing beat; a merged duplicate.
- MUST NOT be mirrored (Chinese-only by design): anything that only fixed Chinese wording — 筆者→我, a forbidden connective swapped, a 的-stack untangled, a semicolon split, a zh-tw lexical fix, a gloss that only settled a Chinese rendering (intent／意圖).
- EN-ONLY CONTENT IS A DEFECT: any sentence added to the English that has no counterpart in the Chinese. The Chinese is the source of truth — delete it, unless it is genuinely needed in English and the Chinese is the one that is missing something, in which case say so in your reply and do NOT invent Chinese prose.
- KNOWN DEFECT, fix it: in 2026-10-green-overview/article.en.md the line "Next come the three gates, one piece each, starting with testing." was added by the mirror stage, has no Chinese counterpart, and immediately precedes the series block that already says "Three deep dives, one gate each". (Only applies to the overview; ignore for the other three.)
When you edit the English: it is the author's own English for an international VP reader, not a translation to be smoothed. Read three paragraphs around the anchor first so the register matches. Numbers, links, mermaid, code blocks, headings, tables, TL;DR, References, the series block and the AI-collaboration note are untouched — the gate checks them.
Finish by regenerating both pastes and running every gate; paste all output:
  cd ${ROOT} && python3 research/scripts/article_to_paste.py ${a.dir} && python3 research/scripts/article_to_paste.py ${a.dir} --lang en && bash ${Q}/p-check.sh ${a.dir} && bash ${Q}/protected-check.sh ${a.dir} && bash ${Q}/mirror-check.sh ${a.dir}
Do NOT run the full test suites — the main loop runs them once at the end. Reply with one line per difference judged (mirrored / Chinese-only, why / deleted as EN-only) and the outputs.`

// ------------------------------------------------------------------ pipeline
log('Four articles in parallel; inside an article every stage is sequential (one file). Voice ran already for 總論; Review 篇 uses findings recovered from the dead run journal.')

const results = await pipeline(ARTICLES,
  // 1. voice lenses
  (_, a) => {
    if (a.voice === 'done') { log(a.name + ': voice pass already applied in the dead run — skipping the lenses'); return Promise.resolve({ a, log: ['voice: already applied'], findings: [] }) }
    if (a.voice === 'recovered') { log(a.name + ': using the 28 findings recovered from the journal'); return Promise.resolve({ a, log: ['voice-lenses: recovered'], recovered: true }) }
    return parallel([
      () => agent(voiceRules(a), { label: 'voice-rules:' + a.name, phase: 'Voice', schema: VOICE_FINDINGS, effort: 'high' }),
      () => agent(voiceEar(a), { label: 'voice-ear:' + a.name, phase: 'Voice', schema: VOICE_FINDINGS, effort: 'high' }),
    ]).then(vs => {
      const f = vs.filter(Boolean).flatMap(v => v.findings)
      log(a.name + ': voice — rules ' + (vs[0] ? vs[0].findings.length : 'died') + ', ear ' + (vs[1] ? vs[1].findings.length : 'died'))
      return { a, log: ['voice: ' + f.length + ' findings'], findings: f }
    })
  },
  // 2. voice revision
  (x, a) => {
    if (x && x.recovered) return agent(voiceReviseRecovered(a), { label: 'voice-revise:' + a.name, phase: 'Voice', effort: 'high' }).then(r => ({ a, log: [...x.log, r === null ? 'voice-revise: died' : 'voice-revise: ok'] }))
    if (x && x.findings && x.findings.length) return agent(voiceRevise(a, x.findings), { label: 'voice-revise:' + a.name, phase: 'Voice', effort: 'high' }).then(r => ({ a, log: [...x.log, r === null ? 'voice-revise: died' : 'voice-revise: ok'] }))
    return Promise.resolve({ a, log: [...(x ? x.log : []), 'voice-revise: none'] })
  },
  // 3. zh-tw
  (x, a) => agent(zhtw(a), { label: 'zhtw:' + a.name, phase: 'zh-tw', effort: 'medium' })
    .then(r => ({ a, log: [...(x ? x.log : []), r === null ? 'zhtw: died' : 'zhtw: ok'], zhtw: r ? String(r).slice(0, 2500) : null })),
  // 4. final verification, two lenses
  (x, a) => parallel([
      () => agent(lensFidelity(a), { label: 'fidelity:' + a.name, phase: 'Final verify', schema: ISSUES, effort: 'high' }),
      () => agent(lensReader(a), { label: 'reader:' + a.name, phase: 'Final verify', schema: ISSUES, effort: 'high' }),
    ]).then(vs => {
      const all = vs.filter(Boolean).flatMap(v => v.issues)
      const act = all.filter(i => i.severity !== 'style')
      const held = all.filter(i => i.severity === 'style')
      if (held.length) log(a.name + ': final verify — ' + act.length + ' to fix, ' + held.length + ' style-only findings HELD BACK for the human (the voice pass already ruled on style)')
      else log(a.name + ': final verify — ' + act.length + ' to fix')
      return { a, log: [...(x ? x.log : []), 'verify: ' + act.length + ' fix / ' + held.length + ' held'], zhtw: x ? x.zhtw : null, issues: act, held }
    }),
  // 5. fix
  (x, a) => (x && x.issues && x.issues.length)
    ? agent(fixPrompt(a, x.issues), { label: 'fix:' + a.name, phase: 'Final verify', effort: 'high' }).then(r => ({ ...x, log: [...x.log, r === null ? 'fix: died' : 'fix: ok'] }))
    : Promise.resolve({ ...(x || {}), a, log: [...(x ? x.log : []), 'fix: none needed'] }),
  // 6. mirror audit
  (x, a) => agent(mirrorAudit(a), { label: 'mirror-audit:' + a.name, phase: 'Mirror audit', effort: 'high' })
    .then(r => ({ article: a.dir, name: a.name, stages: [...(x ? x.log : []), r === null ? 'mirror-audit: died' : 'mirror-audit: ok'], zhtw: x ? x.zhtw : null, held: x ? x.held : [], mirror: r ? String(r).slice(0, 2500) : null })),
)

return results.filter(Boolean)
