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
  name: 'research-2026-10-quality-repair',
  description: 'HISTORICAL RECORD ONLY — do not run or reuse. Undo the sixteen regressions this readability pass introduced — openers that lost their judgement, assertions buried under explanation, a punchline followed by a cold shower, duplicated glosses — restoring the author shapes the reader lens named, then re-verify and re-mirror.',
  phases: [
    { title: 'Repair', detail: 'apply the reader-lens restorations, one article each' },
    { title: 'Verify', detail: 'fidelity lens over the repair hunks, then fix' },
    { title: 'Mirror', detail: 'carry structural repairs to English, regenerate pastes, run every gate' },
  ],
}

const ROOT = args.root
const Q = ROOT + '/.context/quality'
const VOICE = ROOT + '/research/2026-09/voice_brief.history.md'

const ITEMS = {
  '總論': [
    { q: '用語也在這裡定調。mutation score、constraint tests、pass^k（k 次全過的比例）後面各有一節，它們都是**更好的 check**，不是 testing 的替代品。',
      p: '第一節已經說過「前兩個後面各有一節」，這裡再宣告一次，同一個行政資訊讀兩次。',
      f: '用語在這裡定調。mutation score、constraint tests 與 pass^k（k 次全過的比例）都是**更好的 check**，不是 testing 的替代品。' },
    { q: '表裡的名詞留到各自那一節定義，只有 constraint tests 例外，因為三道閘都用它。',
      p: '原本第一句就給讀者東西（三道閘共用的零件是 constraint tests），改完之後第一句變成編輯體例說明。',
      f: '表裡有一個零件是三道閘共用的：constraint tests；其他名詞留到各自那一節定義。' },
    { q: 'Martin Fowler 9 月 2 日轉了一篇「Maybe we shouldn\'t be reviewing all this code」，把這個問題問得比我直接，它的說法是：',
      p: '節首句的「這個問題」沒有先行詞；主詞在 Fowler 與那篇文章之間晃。',
      f: '人的時間該花在哪裡，Martin Fowler 9 月 2 日轉的那一篇「Maybe we shouldn\'t be reviewing all this code」問得比我直接：' },
    { q: '免審合併率指的是沒有任何人類 approve 就 merge 的比例。它給出的關聯是這樣的：免審合併率每高 10 個百分點，維護負擔約高 6%。',
      p: '定義句插在「研究發現什麼」與「它給出的關聯」中間，而且定義的詞在本段還沒出現過。定義該補，位置錯了。',
      f: '它給出的關聯是這樣的：免審合併率—沒有任何人類 approve 就 merge 的比例—每高 10 個百分點，維護負擔約高 6%。' },
    { q: '先看一個最不可能放棄 TDD 的人：Uncle Bob（Robert C. Martin），TDD 最主要的推廣者。',
      p: '節開場從一句判斷改成一句舞台指示，氣勢掉了一階；而且「這兩則貼文」是前指，貼文要到後面兩句才出現。',
      f: 'Uncle Bob（Robert C. Martin）大概是這個行業裡最不可能放棄 TDD 的人，TDD 最主要的推廣者就是他。（下一句的「這兩則貼文」同時改成「下面這兩則貼文」。）' },
    { q: '第二條在右邊。mutation testing 貴在要把整套測試跑成千上萬次，它等了四十年的經濟理由，agent 給了。',
      p: '「等了四十年的經濟理由，agent 給了」原本是一句乾淨的斷語，現在前面掛了一段解釋，主詞還換了一次。補「為什麼貴」是對的，跟斷語擠在同一句就把力道吃掉了。',
      f: '第二條在右邊。mutation testing 貴在要把整套測試跑成千上萬次。它等了四十年的那個經濟理由，agent 給了。' },
    { q: '11 月的主題「同一份規格跑十次」，會把 pass^k 往 harness 的變異數再推一步；harness 是上一季技術篇講的那一層，agent 周圍的工具與流程。',
      p: '結語在前一段就落地了（「工具會換，這個決定不會。」）。最後這一段是下個月的預告，又在分號後插一個 harness 的定義，收束之後再補課，尾勁散掉；而且本篇之後的三篇深掘只在文末列表出現，散文沒有指過去。',
      f: '三道閘各一篇，先從測試篇開始。再往後，11 月的主題「同一份規格跑十次」會把 pass^k 往 harness 的變異數再推一步—harness 就是上一季技術篇講的那一層，agent 周圍的工具與流程。（注意：這一句是結構性新增，鏡像階段必須把對應的英文句加回 article.en.md 的同一位置。）' },
  ],
  '測試篇': [
    { q: '他們的示範跑在 kind（本機模擬用的 Kubernetes）叢集上，這一課在 production 付過什麼代價，投影片沒寫。',
      p: '這段誠實的但書卡在故事的斷語與它落回本篇的那一段之間，punchline 剛出手就先被自己澆一盆冷水。',
      f: '把這一句從現在的位置移走，原句一字不改，接在「兩個量到的都是自己搆得到的範圍，不是報告上寫的那個範圍。」之後。它是誠信裝置（P11），只能移位，不能刪、不能弱化。' },
    { q: '所以第一個月不阻擋，要校準的不只是噪音，還有這三個 check 自己抽到了什麼、漏了什麼。',
      p: '「第一個月只報告不阻擋」到這裡是全篇第六次、本節第三次出現。要補的新訊息只有後半句。',
      f: '校準的清單因此要多一條：這三個 check 自己抽到了什麼、漏了什麼。' },
    { q: '左半防的是測試被改弱，右半防的是測試沒測到。',
      p: '這兩個名字就印在圖裡兩個 subgraph 的標題上，圖說等於把剛看完的圖念一遍；而「兩件事」該在進圖之前就點名。',
      f: '把名字移到進圖之前：前面承諾「兩件事」的那一句改成「人要防的其實只有兩件事：測試被改弱，與測試沒測到。」，圖說只留「四種壞法各有一個便宜的對策：三個 check，加一個 PR template 欄位。」注意 mermaid 區塊本身一個字都不能動（P6），只改它前後的散文。' },
  ],
  'Review 篇': [
    { q: '依據是第 16 張投影片引的一篇論文',
      p: '頁碼是 References 的事（第 25 條已寫 slide 16），出現在正文讓這句從場景掉回書目格式，而且同段已有「我沒讀原文」的誠信註記在處理同一件事。',
      f: '依據是投影片裡引的一篇論文' },
    { q: '回到那份設定檔。Before 是多數團隊現在的設定，一個 runner、一個 session、自動放行：',
      p: '「回到」指向一個還沒出現過的東西——本節開頭寫的是「設定」不是「設定檔」，而且隔了三十多行。',
      f: '三條原則講完，回到本節開頭答應的那份設定。Before 是多數團隊現在的設定，一個 runner、一個 session、自動放行：' },
    { q: '第三節留給這裡的定義：approval artifact 是每一次 approve 留下的那筆紀錄，最小版本只要三樣東西。',
      p: '「每次 approve 留下的那筆紀錄」在第三節已經一字不差講過；前綴既然標明是接手，定義就不必再抄一次。',
      f: '第三節留給這裡的定義：approval artifact 的最小版本只要三樣東西。' },
    { q: '拒絕的原因是 false positive（誤報）、重複、超出範圍、intent 錯位。',
      p: '同一串四個原因裡只有「intent 錯位」兩個詞都沒交代，而這是 intent 在正文的第一次出現。',
      f: '拒絕的原因是 false positive（誤報）、重複、超出範圍，以及看錯這個 PR 想做什麼（intent 錯位）。' },
  ],
  '可靠度篇': [
    { q: '上一節給的是兩個數字，這一節處理它們的帳單',
      p: '第二到第六節五個開場全是同一個模子（「上一節說…這一節做的是」「上一節處理的是…這一節處理另一件事」「上一節給的是…這一節處理」…），第三次之後過場等於失效：全文的「承」只剩一種句型，「轉」沒有了。第四節最容易換，因為它本來就有現成的定義句可以起頭。',
      f: '可靠度目標訂得越高，要付多少人去讀，就跟著往上走。這是前兩個數字的帳單' },
    { q: '講者 Inês Bolaños 給它的定位是副駕駛，不是船長',
      p: '副駕駛配的是機長，不是船長；中文讀起來像直譯 co-pilot / captain 沒有落地。',
      f: '講者 Inês Bolaños 給它的定位是副駕駛，不是機長' },
  ],
}

const ARTICLES = [
  { dir: '2026-10-green-overview', name: '總論' },
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

const repair = (a) => `Repo root ${ROOT}; absolute paths only; never cd. FILE: ${ROOT}/${a.dir}/article.md — ${a.name} of the October series, the author's own Traditional-Chinese prose.
WHAT HAPPENED: a readability pass rewrote parts of this article. A reader lens then read the finished article end to end and named the places where the pass made it WORSE — an opener that went from a judgement to a stage direction, an assertion buried under the explanation that now precedes it in the same sentence, a punchline immediately followed by its own caveat, a gloss repeated from an earlier section. Your job is to undo exactly those, restoring the shape the reader names. Nothing else.
METHOD: Edit tool, one change at a time, verbatim old_string located with grep -nF (never by line number). If a quote below no longer matches the file verbatim, grep for its distinctive words, read the surrounding paragraph, and apply the repair to what is actually there — say so in your reply. Read the paragraph before and after each edit so the restored sentence still connects.
RULES that still bind (voice_brief.history §9.2; the gates check them): every number and its precision unchanged (P1); a number's qualifier stays in the same sentence or paragraph (P2); names of studies, tools, people verbatim (P3/P4); links unchanged (P5); mermaid blocks and their positions unchanged to the character (P6); tables keep columns, rows, order and cell text (P7); code/yaml blocks unchanged (P8); headings unchanged (P9); the §9.4 protected claims verbatim (P10); every 誠信裝置 stays — it may MOVE, never be deleted, merged or weakened (P11); the TL;DR block is untouched entirely, in both languages (P12); the series navigation and 系列文章 block untouched (P13); References untouched (P14); the AI 協作說明 and closing Medium line untouched (P15/P16); the lines deferring to 11 月／12 月 untouched, and no November or December material imported (P17); new prose uses the single "—", NEVER the double "——" (P18) — some of the proposed fixes below are written with "——"; convert every one to a single "—" before you write it.
VOICE: allowed connectives are only 但／所以／也就是說／其實／實際上／事實上／相反 (never 因此／然而／但是／於是／不過／當然／換句話說／首先／其次／總之); new text says 我, never 筆者; 讀者 is forbidden in new text; no imperatives at the reader; a paragraph ends on a judgement, not on a deposited fact. ${VOICE} §十 (line 659 to the end) has fifteen before/after pairs the author approved — imitate their shapes.
REPAIRS (each: the current text, why it is worse, and the restoration to apply):
${JSON.stringify(ITEMS[a.name], null, 1)}
GATES — run all three at the end and paste the output; all must pass, fix before returning if not:
  bash ${Q}/p-check.sh ${a.dir}
  bash ${Q}/protected-check.sh ${a.dir}
  bash ${Q}/voice-check.sh ${a.dir}
Reply with one line per repair (applied / adapted because the quote had shifted / skipped + why) and the gate output.`

const verify = (a) => `You are a FIDELITY checker. Repo ${ROOT}; absolute paths; never cd.
A repair pass just restored sentence shapes in ${ROOT}/${a.dir}/article.md. Read the WHOLE diff: git diff -U3 HEAD -- ${ROOT}/${a.dir}/article.md, and pay closest attention to the hunks the repair just touched (they are the ones whose '+' lines you can also find quoted in ${Q}/held-ours.json).
Judge: (1) did any restoration change the meaning, strength or scope of a claim? (2) did a moved sentence leave a 代詞回指 ("這兩則貼文"、"那份設定"、"這個問題"、"它") pointing at something that no longer precedes it — check both the moved sentence AND the place it came from; (3) did a deleted duplicate take with it the only occurrence of a number, a qualifier, a citation or a 誠信裝置? (4) any protected claim (${VOICE} lines 608–619) altered? (5) any "——" introduced? any 因此／然而／但是／於是／不過／當然／換句話說 introduced? (6) is the TL;DR still byte-identical to HEAD in BOTH languages: git diff HEAD -- ${ROOT}/${a.dir}/article.md ${ROOT}/${a.dir}/article.en.md | grep 'TL;DR' should print nothing.
Also run and paste: bash ${Q}/p-check.sh ${a.dir} ; bash ${Q}/protected-check.sh ${a.dir} ; bash ${Q}/voice-check.sh ${a.dir}
Report with the current verbatim text in 'quote' and an exact replacement (or "REVERT-TO: <original>") in 'fix'. Report only real damage; do not propose style preferences.`

const fixIt = (a, issues) => `Repo ${ROOT}; absolute paths; never cd. FILE ${ROOT}/${a.dir}/article.md.
A fidelity checker found damage in the repair pass. Apply these with Edit, one at a time, verbatim old_string, nothing else. A "REVERT-TO" fix restores the original sentence verbatim. Every number, citation, protected claim and 誠信裝置 stays; new prose uses the single "—", never "——"; allowed connectives only (但／所以／也就是說／其實／實際上／事實上／相反).
Then run and paste: bash ${Q}/p-check.sh ${a.dir} ; bash ${Q}/protected-check.sh ${a.dir} ; bash ${Q}/voice-check.sh ${a.dir}
ISSUES:
${JSON.stringify(issues, null, 1)}`

const mirror = (a) => `Repo ${ROOT}; absolute paths; never cd.
The Chinese ${ROOT}/${a.dir}/article.md was just repaired; the English ${ROOT}/${a.dir}/article.en.md must stay a 1:1 mirror in content and structure.
Read both diffs in full: git diff -U3 HEAD -- ${ROOT}/${a.dir}/article.md and git diff -U3 HEAD -- ${ROOT}/${a.dir}/article.en.md. Then run bash ${Q}/mirror-check.sh ${a.dir}, which compares the number of blank-line-separated blocks section by section.
MIRROR these repairs: a sentence added, deleted or MOVED to another paragraph; a duplicated definition removed; a clause promoted out of a parenthesis; an opener rebuilt so the judgement comes first. Specifically for 總論: the Chinese closing now opens with a prose pointer to the three deep dives ("三道閘各一篇，先從測試篇開始。") — the English needs the same sentence in the same place, folded into the same paragraph as the November look-ahead rather than standing alone.
Do NOT mirror: anything that only fixed Chinese wording — a 的-stack untangled, a connective swapped, 船長→機長 (the English already says "captain"), a Chinese-only gloss.
The English is the author's own English for an international VP reader, not a translation to be smoothed; read three paragraphs around each anchor before editing. Numbers, links, mermaid, code blocks, headings, tables, the TL;DR (byte-identical to HEAD), References, the series block and the AI-collaboration note are untouched.
Finish by regenerating both pastes and running every gate; paste all output:
  cd ${ROOT} && python3 research/scripts/article_to_paste.py ${a.dir} && python3 research/scripts/article_to_paste.py ${a.dir} --lang en && bash ${Q}/p-check.sh ${a.dir} && bash ${Q}/protected-check.sh ${a.dir} && bash ${Q}/mirror-check.sh ${a.dir} && bash ${Q}/voice-check.sh ${a.dir}
Do NOT run the full test suites. Reply with one line per repair judged (mirrored / Chinese-only, why) and the outputs.`

log('Sixteen regressions from the readability pass, restored one article at a time, then fidelity-verified and re-mirrored. The eleven findings that are problems in the author\'s ORIGINAL prose are deliberately NOT in this run — those are the author\'s call.')

const results = await pipeline(ARTICLES,
  (_, a) => agent(repair(a), { label: 'repair:' + a.name, phase: 'Repair', effort: 'high' })
    .then(r => ({ a, log: [r === null ? 'repair: died' : 'repair: ok'] })),
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
    .then(r => ({ article: a.dir, name: a.name, stages: [...(x ? x.log : []), r === null ? 'mirror: died' : 'mirror: ok'], issues: x ? x.issues : [], mirror: r ? String(r).slice(0, 2000) : null })),
)

return results.filter(Boolean)
