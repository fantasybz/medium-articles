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
  name: 'research-2026-10-quality-final',
  description: 'HISTORICAL RECORD ONLY — do not run or reuse. The last seven reader-lens findings that fall inside the approved scope — the opening roadmap sentence, three passages read a second or fourth time, a self-referential clause, a counting ambiguity, and the Bach paragraph this pass pushed past the punchline — applied, verified and mirrored.',
  phases: [
    { title: 'Apply', detail: 'seven findings, one agent per article' },
    { title: 'Verify', detail: 'fidelity lens, then fix' },
    { title: 'Mirror', detail: 'English counterparts, regenerate pastes, run every gate' },
  ],
}

const ROOT = args.root
const Q = ROOT + '/.context/quality'
const VOICE = ROOT + '/research/2026-09/voice_brief.history.md'

const ITEMS = {
  '總論': [],
  '測試篇': [
    { q: '還有一件 testing 的事，Bach 說它不能自動化：對 agent 產出做探索式測試，不是讀它的測試，是去用它做出來的東西。那是另一篇文章的題目，這裡只點到為止。',
      p: '這一段本來在金句之前，這一輪把它搬到了金句之後，結果結語的最後三拍變成：金句落地 → 丟出一個新概念又立刻推走 → 下一篇預告。讀完金句最後留在腦裡的，變成一件本篇明說不做的事。',
      f: '把這一段併進後面那句下一篇預告，讓金句之後只剩一段。併法舉例（用詞可依作者慣例調整，破折號一律單一「—」）：「下一篇是 Review 篇：test gate 過了之後，這個 PR 誰要讀、讀什麼、誰審誰，以及 AI 審 AI 什麼時候該禁止。至於 Bach 說不能自動化的那一件—去用 agent 做出來的東西，而不是讀它的測試—留給另一篇。」原本那句「那是另一篇文章的題目，這裡只點到為止」的意思要留住（P17 對 11／12 月的收邊不受影響，這一句指的是「另一篇文章」，不是某個月份）。' },
    { q: '用途先限定。這是「綠燈但沒驗收」與「測錯對象」的實例',
      p: '第三節已經用過一模一樣的起手式（「用途要先限定。這個實驗量的是……」）。第二次看到同一個句型，讀者會以為自己捲回了第三節。',
      f: '先說這個例子能證明什麼、不能證明什麼。這是「綠燈但沒驗收」與「測錯對象」的實例' },
    { q: '本篇就是回答那一串的。回答的不是測試種類的清單，是三個 check 與門檻。要講 check 之前，得先知道它們各自在防什麼。',
      p: '第一節的路線圖只有兩格：終點（三個 check 與門檻）與下一步（第二節講壞法）。第三節的 49%、第六節的覆蓋率、第七節的實例都沒有被預告，所以讀者進到第三節時會以為要直接看 check 了。這條路線在 TL;DR 裡有，正文裡沒有。這是 §4.1 第④拍的路線圖句。',
      f: '本篇就是回答那一串的。回答的不是測試種類的清單，是三個 check 與門檻。順序是：先看 agent 寫的測試會壞在哪，再看為什麼人眼擋不住，然後才是三個 check 與它們的門檻，最後用一個我親手跑出來的例子畫出它們的邊界。（請先讀過本篇的章節標題，確認這句話描述的順序與實際章節相符再寫；不符就照實際章節改寫。）' },
  ],
  'Review 篇': [
    { q: '表裡最容易被誤讀的是第二列。同 vendor 不同 session 的 reviewer 不是被消音，它照樣可以指出問題，它只是不能替 merge 背書。',
      p: '同一條規則在本篇出現四次：第四節節尾、第五節散文「第二種是同 vendor 但不同 session…」、表格第二列，以及這一段，最後圖說又講一次，字面幾乎相同。第四節那句還預告「第五節的有條件允許表會用同一個判準把它寫死」，所以讀者已經等著它出現一次，不是四次。',
      f: '刪去這一段。刪之前先逐一確認：這一段沒有任何別處沒有的數字、出處、受保護主張或誠信裝置（`bash ' + ROOT + '/.context/quality/protected-check.sh 2026-10-green-review` 在刪後必須仍是 OK）。若發現它有別處沒有的內容，改成把那一點併進第五節既有的那一句，不要整段刪。' },
    { q: '五組數字如下，順序是從「為什麼 review 是控制點」，一路推到「人該把時間花在哪」：',
      p: '開節連三段都在講「我要怎麼寫這一節」—前一段「都應該有一筆真實 PR 資料撐著」、上一段的取捨、這一段的順序—第一個數字要到第四段才出現。承諾了五組資料的人在這裡空等。',
      f: '把順序那一句併進上一段，讓清單緊接著出現。併法：上一段改成「這一節是全系列唯一把真實 PR 資料引全的地方。取捨很簡單：每個數字後面緊接它推出的那一條處方，推不出處方的只進最後的總表。順序是從「為什麼 review 是控制點」，一路推到「人該把時間花在哪」：」，然後刪掉「五組數字如下…」這一段。' },
    { q: '走完這七節之後',
      p: '本篇有八節，結語自己是第八節；而且上一句剛講完「落地順序有七步」，兩個「七」貼在一起，讀者要數一下才確定這裡指的是第一到第七節。',
      f: '走完前面七節之後' },
  ],
  '可靠度篇': [
    { q: '人眼的抓錯率直接決定你要付多少人力，這條連結本身就是這一節的價值。',
      p: '後半句是對自己文章的評語，不是給讀者的內容，語氣跟全篇不同。而且 c 的起步值 0.6 在前兩段已經講了兩次，這一整段等於第三次繞回同一點。',
      f: '人眼的抓錯率直接決定你要付多少人力。' },
  ],
}

const ARTICLES = [
  { dir: '2026-10-green-testing', name: '測試篇' },
  { dir: '2026-10-green-review', name: 'Review 篇' },
  { dir: '2026-10-green-reliability', name: '可靠度篇' },
]

const ISSUES = { type: 'object', required: ['checked', 'issues'], properties: {
  checked: { type: 'integer' },
  issues: { type: 'array', items: { type: 'object', required: ['quote', 'problem', 'fix', 'severity'], properties: {
    quote: { type: 'string' }, problem: { type: 'string' }, fix: { type: 'string' },
    severity: { type: 'string', enum: ['meaning-changed', 'invariant', 'made-worse', 'other'] } } } },
} }

const apply = (a) => `Repo root ${ROOT}; absolute paths only; never cd. FILE: ${ROOT}/${a.dir}/article.md — ${a.name} of the October series, the author's own Traditional-Chinese prose.
A readability pass and a repair pass have already run; this is the last set. A reader lens read the finished article end to end and named these places. They are in the author's ORIGINAL prose, so be conservative: make the smallest change that fixes what is named, and keep the author's words wherever they still work.
METHOD: Edit tool, one change at a time, verbatim old_string located with grep -nF (never by line number). Read the paragraph before and after each edit. If a quote no longer matches verbatim, grep for its distinctive words and adapt — say so in your reply.
RULES that bind (voice_brief.history §9.2; the gates check them): every number and its precision unchanged (P1); a number's qualifier stays in the same sentence or paragraph (P2); names verbatim (P3/P4); links unchanged (P5); mermaid blocks and positions unchanged (P6); tables unchanged (P7); code blocks unchanged (P8); headings unchanged (P9); the §9.4 protected claims verbatim (P10); every 誠信裝置 stays — may move, never be deleted, merged or weakened (P11); the TL;DR untouched in both languages (P12); series navigation and 系列文章 block untouched (P13); References untouched (P14); the AI 協作說明 and closing Medium line untouched (P15/P16); the 11 月／12 月 deferrals untouched and no November/December material imported (P17); English technical terms stay English (P18) and new prose uses a single "—", never "——".
VOICE: allowed connectives are only 但／所以／也就是說／其實／實際上／事實上／相反 (never 因此／然而／但是／於是／不過／當然／換句話說／首先／其次／總之); new text says 我, never 筆者; 讀者 is forbidden in new text; no imperatives at the reader; a paragraph ends on a judgement. ${VOICE} §十 (line 659 to the end) has fifteen before/after pairs the author approved — imitate their shapes.
FINDINGS:
${JSON.stringify(ITEMS[a.name], null, 1)}
GATES — run all three at the end and paste the output; all must pass, fix before returning if not:
  bash ${Q}/p-check.sh ${a.dir}
  bash ${Q}/protected-check.sh ${a.dir}
  bash ${Q}/voice-check.sh ${a.dir}
Reply with one line per finding (applied / adapted / skipped + why) and the gate output.`

const verify = (a) => `You are a FIDELITY checker. Repo ${ROOT}; absolute paths; never cd.
A final pass just edited ${ROOT}/${a.dir}/article.md — it merged or deleted passages the reader had read a second or fourth time, added an opening roadmap sentence, and folded a stray closing paragraph into the next-article pointer. Read the WHOLE diff: git diff -U3 HEAD -- ${ROOT}/${a.dir}/article.md.
Judge: (1) did a deletion or merge take with it the ONLY occurrence of a number, a qualifier, a citation, a protected claim or a 誠信裝置? Search the rest of the file for each thing the deleted text carried before you accept the deletion; (2) does an added roadmap sentence describe the article's ACTUAL sections, in the actual order — check the headings; (3) did any claim change meaning, strength or scope; (4) does every 代詞回指 near an edit still point at something that precedes it; (5) any "——", any forbidden connective (因此／然而／但是／於是／不過／當然／換句話說／首先／其次／總之), any 筆者 in new text; (6) is the TL;DR still byte-identical to HEAD in both languages.
Also run and paste: bash ${Q}/p-check.sh ${a.dir} ; bash ${Q}/protected-check.sh ${a.dir} ; bash ${Q}/voice-check.sh ${a.dir}
Report with the current verbatim text in 'quote' and an exact replacement (or "REVERT-TO: <original>") in 'fix'. Report only real damage.`

const fixIt = (a, issues) => `Repo ${ROOT}; absolute paths; never cd. FILE ${ROOT}/${a.dir}/article.md.
Apply these verified issues with Edit, one at a time, verbatim old_string, nothing else. A "REVERT-TO" fix restores the original sentence verbatim. Every number, citation, protected claim and 誠信裝置 stays; a single "—", never "——"; allowed connectives only (但／所以／也就是說／其實／實際上／事實上／相反).
Then run and paste: bash ${Q}/p-check.sh ${a.dir} ; bash ${Q}/protected-check.sh ${a.dir} ; bash ${Q}/voice-check.sh ${a.dir}
ISSUES:
${JSON.stringify(issues, null, 1)}`

const mirror = (a) => `Repo ${ROOT}; absolute paths; never cd.
The Chinese ${ROOT}/${a.dir}/article.md was just edited; the English ${ROOT}/${a.dir}/article.en.md must stay a 1:1 mirror in content and structure. These edits are STRUCTURAL — a paragraph deleted, two paragraphs merged, a roadmap sentence added, a closing paragraph folded into the next-article pointer — so every one of them has an English counterpart.
Read both diffs in full: git diff -U3 HEAD -- ${ROOT}/${a.dir}/article.md and git diff -U3 HEAD -- ${ROOT}/${a.dir}/article.en.md, then run bash ${Q}/mirror-check.sh ${a.dir}, which compares the number of blank-line-separated blocks section by section and must end green.
Do NOT mirror anything that only fixed Chinese wording (a 的-stack untangled, a connective swapped, a Chinese-only gloss).
The English is the author's own English for an international VP reader, not a translation to be smoothed; read three paragraphs around each anchor before editing. Numbers, links, mermaid, code blocks, headings, tables, the TL;DR (byte-identical to HEAD), References, the series block and the AI-collaboration note are untouched.
Finish by regenerating both pastes and running every gate; paste all output:
  cd ${ROOT} && python3 research/scripts/article_to_paste.py ${a.dir} && python3 research/scripts/article_to_paste.py ${a.dir} --lang en && bash ${Q}/p-check.sh ${a.dir} && bash ${Q}/protected-check.sh ${a.dir} && bash ${Q}/mirror-check.sh ${a.dir} && bash ${Q}/voice-check.sh ${a.dir}
Do NOT run the full test suites. Reply with one line per edit mirrored and the outputs.`

log('Seven findings inside the approved scope. The four that are NOT here — moving the author\'s book caveat, rewording a paragraph whose numbers the figure repeats (blocked by P1), deleting a thank-you line, and unifying intent/意圖 (blocked by P18) — are held for the author.')

const results = await pipeline(ARTICLES,
  (_, a) => agent(apply(a), { label: 'apply:' + a.name, phase: 'Apply', effort: 'high' })
    .then(r => ({ a, log: [r === null ? 'apply: died' : 'apply: ok'] })),
  (x, a) => agent(verify(a), { label: 'verify:' + a.name, phase: 'Verify', schema: ISSUES, effort: 'high' })
    .then(v => {
      const n = v ? v.issues.length : 0
      log(a.name + ': verify — ' + (v ? n + ' issues' : 'died'))
      return { a, log: [...(x ? x.log : []), 'verify: ' + n], issues: v ? v.issues : [] }
    }),
  (x, a) => (x && x.issues.length)
    ? agent(fixIt(a, x.issues), { label: 'fix:' + a.name, phase: 'Verify', effort: 'high' }).then(r => ({ ...x, log: [...x.log, r === null ? 'fix: died' : 'fix: ok'] }))
    : Promise.resolve({ ...(x || {}), a, log: [...(x ? x.log : []), 'fix: none'] }),
  (x, a) => agent(mirror(a), { label: 'mirror:' + a.name, phase: 'Mirror', effort: 'high' })
    .then(r => ({ article: a.dir, name: a.name, stages: [...(x ? x.log : []), r === null ? 'mirror: died' : 'mirror: ok'], issues: x ? x.issues : [], mirror: r ? String(r).slice(0, 1500) : null })),
)

return results.filter(Boolean)
