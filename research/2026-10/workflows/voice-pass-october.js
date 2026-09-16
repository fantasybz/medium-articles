export const meta = {
  name: 'research-2026-10-voice-pass',
  description: 'Make every sentence inserted into the four October articles read as if the author wrote it: two lenses per article judge the new lines against the 91K-character voice manual and against the rhythm of the paragraph they landed in, then one reviser rewrites ONLY those lines and re-proves that the author original is byte-intact.',
  phases: [
    { title: 'Judge', detail: 'per article: voice-manual rules lens + ear/rhythm lens, zh and en' },
    { title: 'Revise', detail: 'rewrite only the inserted lines; prove the original is untouched' },
  ],
}

const ROOT = args.root
const TODAY = args.today
const VOICE = `${ROOT}/research/2026-09/voice_brief.md`
const STYLE = `${ROOT}/research/2026-09/style_brief.md`
const ARTICLES = args.articles

const CONTEXT = `Today is ${TODAY}. Repo root ${ROOT}; absolute paths only, never cd.
The author is Kochi Chuang (@fantasybz), writing long-form Traditional Chinese (Taiwan usage) for Engineering VPs / Staff engineers, plus an English edition of each piece.
A previous step inserted sentences carrying AGNTCon Tokyo and *AI Agents in Depth* evidence into four written-but-unpublished October articles. Those inserted lines are the ONLY lines you may touch. Everything else is the author's published prose and is off limits — not a word, not a comma, not a line break.
To see exactly what was inserted, run: cd ${ROOT} && git diff -U6 -- <dir>/article.md <dir>/article.en.md — lines prefixed '+' are the insertions, and the surrounding context lines are the author's own writing, which is your model for how the new line should sound.
The author's voice manual is ${VOICE} (91K characters — read the sections named below with sed, not the whole file) and ${STYLE}.`

const RULES = `The sections of ${VOICE} that govern an inserted, source-citing sentence:
- §1.2 「筆者」只剩三個合法位置; §1.3 「讀者」是禁詞（and the three usages it distinguishes）; §1.4 「我們」只有兩種合法用途; §1.6 從不對讀者下命令
- §2.2 連接詞：only 但／所以／也就是說／其實／實際上／事實上／相反 are allowed; 因此／然而／但是／於是／不過／當然／換句話說／首先／其次／再者／總之／綜上所述 are FORBIDDEN (note its own false-positive warning: 可靠度篇's 「任一條不過」 is not a conjunction). Continuity comes from 冒號導引句, 時間副詞 and 代詞回指 — not from connectives.
- §2.3 破折號：正確用法只有一種; §2.4 他真正的停頓工具：冒號與「」; §2.5 分號只做對稱對比
- §3.1 數字：四拍，缺一不可 — ① 宣告要用數字定錨 → ② 樣本數在數字之前 → ③ 數字本體 → ④ 「合起來讀」的收攏並指向後文. The manual records that October's four articles chronically ship only beat ③; an inserted sentence that is a bare number with a citation repeats exactly that failure.
- §3.2 引研究：名字與動詞在前，數字在後 — never a long noun phrase as the subject; the fixed three beats are 鋪陳句（≤1 句）→ 原文 → 解讀（1–2 句）
- §3.3 引書與名人：第一次出現一定給身分
- §6.2 允許的 hedge 只有五種; §6.3 禁用的 hedge; §6.1 事實／意見／hedge 的三層標記
- §5 the 40-entry verbatim phrase bank (A 導引與清單前導 / B 引用與歸因 / C 判斷與收束 / D 轉場 / E 版面標籤詞) — prefer a construction the author has actually used.`

const FINDINGS = {
  type: 'object', required: ['article', 'findings'],
  properties: {
    article: { type: 'string' },
    findings: { type: 'array', items: { type: 'object', required: ['lang', 'inserted', 'verdict', 'why', 'rewrite'], properties: {
      lang: { type: 'string', enum: ['zh', 'en'] },
      inserted: { type: 'string', description: 'the inserted line, verbatim as it appears in the file (copy-paste, unique enough to Edit on)' },
      verdict: { type: 'string', enum: ['reads-as-author', 'seam', 'rule-violation', 'drop'] },
      why: { type: 'string', description: 'which rule or which rhythm mismatch, quoting the manual section or the neighbouring sentence it clashes with' },
      rewrite: { type: 'string', description: 'the replacement line keeping every fact, number and citation intact; empty when verdict is reads-as-author; for drop, explain in why why no rewrite can save it' },
    } } },
  },
}

const judge = (a) => [
  () => agent(`${CONTEXT}
${RULES}
TASK — RULES LENS for ${a.name} (${ROOT}/${a.dir}). Run the git diff above to get the inserted lines for both languages. For EACH inserted line, check it against the manual sections listed, in this order: forbidden connective (grep the line for each of the twelve); dash usage; 筆者／讀者／我們; hedge; then §3.1 four beats and §3.2 word order for any line carrying a number or citing a study, a session or a book. Quote the manual's own rule text when you call a violation.
Be concrete about the most likely failure: a line of the shape 「<來源> 的 <數字>，<結論>」 has only beat ③ and is a rule-violation, not a style preference. The rewrite must keep the number, the source id / slide / chapter and the citation exactly as they are — you are changing how it is said, never what it says.
For the English lines, apply the register of the article's own English edition (read the surrounding EN context in the diff), not the Chinese rules.
Return one finding per inserted line — including the ones that pass, with verdict 'reads-as-author' and an empty rewrite.`, { label: `rules:${a.name}`, phase: 'Judge', schema: FINDINGS, effort: 'high' }),

  () => agent(`${CONTEXT}
TASK — EAR LENS for ${a.name} (${ROOT}/${a.dir}). Run the git diff above with generous context. Read each inserted line WHERE IT LANDED: the sentence before it and the sentence after it, and the paragraph's job in that section.
Ask only one question: if the author reread this page a year from now, would he stop at this line and know someone else wrote it? Things that give a seam away: it explains something the previous sentence already set up; it changes the temperature (the author is dry and declarative, an inserted line often arrives eager); it is a different length from everything around it; it introduces a speaker or company the paragraph has no room for; it repeats a connective or a construction used two sentences earlier; it ends flat where the author's paragraphs end on a judgement; it uses 「的」 three or more times in a chain; or it reads as a fact deposited rather than an argument advanced.
Also check the line does the work the paragraph needs: the author cites evidence to move an argument, never to decorate one. If the paragraph was already complete, the honest verdict is 'drop'.
For the English edition, judge the same way against the EN prose around it.
Read ${STYLE} for the series-level shape. Return one finding per inserted line, including the ones that pass.`, { label: `ear:${a.name}`, phase: 'Judge', schema: FINDINGS, effort: 'high' }),
]

const articles = pipeline(ARTICLES,
  a => parallel(judge(a)).then(vs => ({ a, panel: vs.filter(Boolean) })),
  (x, a) => {
    if (!x || !x.panel.length) { log(`${a.name}: both lenses died — leaving the article alone`); return null }
    const all = x.panel.flatMap(p => p.findings)
    const act = all.filter(f => f.verdict !== 'reads-as-author')
    log(`${a.name}: ${all.length} judgements, ${act.length} need work (${act.filter(f => f.verdict === 'drop').length} drop)`)
    if (!act.length) return { article: a.dir, changed: 0, note: 'every inserted line already reads as the author' }
    return agent(`${CONTEXT}
TASK — Revise ${ROOT}/${a.dir}/article.md and article.en.md so that every inserted line reads as the author's own.
Two lenses judged each inserted line. Where both propose a rewrite of the same line, merge them into one line that satisfies both; where they disagree on whether it is a problem at all, trust the one that quotes a manual rule or a neighbouring sentence. Where a finding says 'drop', delete the inserted line AND its References entry if that entry now has no citation in the body — then renumber only if the list requires it.
Apply with the Edit tool, one line at a time.
THE INVARIANT: you may only change lines that this project inserted. Prove it when you are done by running, and pasting the output of:
  cd ${ROOT} && python3 -c "import subprocess
for f in ['${a.dir}/article.md','${a.dir}/article.en.md']:
    old=subprocess.run(['git','show','HEAD:'+f],capture_output=True,text=True).stdout.splitlines()
    new=open(f).read().splitlines()
    missing=[l for l in old if l not in new]
    print(f,'author lines',len(old),'still present',len(old)-len(missing),'MISSING',len(missing))
    for m in missing[:5]: print('   ',m[:140])"
Every author line must still be present; MISSING must be 0. If it is not, restore from git show HEAD:<file> and redo the edit more narrowly.
Then regenerate both pastes and confirm the diff is prose-only:
  cd ${ROOT} && python3 research/scripts/article_to_paste.py ${a.dir} && python3 research/scripts/article_to_paste.py ${a.dir} --lang en && git diff --numstat -- ${a.dir}
Reply with the raw output of both commands and one line per revision applied.
FINDINGS:
${JSON.stringify(act, null, 1)}`, { label: `revise:${a.name}`, phase: 'Revise', effort: 'high' }).then(r => ({ article: a.dir, changed: act.length, proof: r ? String(r).slice(0, 1500) : null }))
  }
)

return { articles: (await articles).filter(Boolean) }
