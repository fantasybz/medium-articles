export const meta = {
  name: 'research-2026-10-zhtw-pass',
  description: 'Final Traditional-Chinese (Taiwan) gate for everything this mid-month cycle produced: one editor agent per file, chunked and judged suggestion by suggestion, with hard no-go zones for Mermaid sources, verbatim foreign-language quotes and the author’s own prose.',
  phases: [
    { title: 'Pass', detail: 'one zh-tw editor per file, in parallel' },
    { title: 'Recheck', detail: 're-run the checker and prove the no-go zones held' },
  ],
}

const ROOT = args.root
const TODAY = args.today
const DIR = `${ROOT}/research/2026-10`

const PROCEDURE = `Load the checker via ToolSearch "select:mcp__zhtw-mcp__zhtw". Split the file into chunks of at most 30,000 characters at "## " / "### " boundaries — never call the tool with the whole file, and never paste the whole file back as output. For each chunk call mcp__zhtw-mcp__zhtw with content_type="markdown", fix_mode="lexical_safe", fix_output="search_replace", translationese_domain="technical", detect_ai=false, max_warnings=60, output="compact".
Apply fixes to the ORIGINAL file with the Edit tool by exact replacement, ONE SUGGESTION AT A TIME, with judgment — never write the checker's full-text output back over the file.
ACCEPT: 用戶→使用者, 後綴→字尾, 是一個→是 (when still grammatical), 信息→資訊, 軟件→軟體, 質量→品質 (quality), 缺省→預設, 屏幕→螢幕, 網絡→網路, 視頻→影片, 服務器→伺服器.
REJECT — these are known false positives on this material, measured on 2026-09-06: 通過→透過 when 通過 means passed (測試通過／未通過／通過率／閘門通過); 縮進→縮排 when it means shrink-into; 原始碼→原始程式碼; 導入→匯入 when 導入 means adoption; 構建→建構 inside a quoted title; 轉發→轉寄; 數據→資料 (this author keeps 數據 for statistics); 文檔→文件 when the match is inside 中文檔; 禁用→停用 when it means ban; anything inside a quotation, a code span, an arXiv id, a URL, a number, an English term or a book title; "!"→"！" inside quoted English.
Translationese WARNINGS (S3 的的不休, ZY5 定語堆疊 ≥ 40 characters with no comma) are the valuable part: split the sentence or add a comma without changing the meaning. Leave table cells alone unless the fix is a single comma. Ignore INFO.
Never introduce "——"; this project uses the single "—" only. Re-run the checker on any chunk you changed heavily; errors must end at 0.
Report: chunks processed, each distinct lexical fix with its count, every rejected suggestion with the reason, warnings before and after, and any sentence you were unsure about.`

const FILES = [
  {
    key: 'outline', path: `${DIR}/2026-12-sre-for-agents.md`,
    guard: `HARD NO-GO ZONES in this file. (1) Never edit a single character inside a \`\`\`mermaid block — the 14 figures were render-verified at measured pixel sizes on 2026-09-16 and changing a node label changes the layout. (2) Never edit inside a \`\`\`yaml / \`\`\`bash / \`\`\`json block, an inline code span, an arXiv id, a session id like \`2QlDa\`, a URL, or an HTML comment marker \`<!-- FIGURE ... -->\`. (3) Quoted Japanese and English source lines stay verbatim — they are evidence. (4) The 圖說 / caption prose OUTSIDE the mermaid fences is in scope. This is a 186,000-character file: chunk it properly and work through every chunk.`,
  },
  {
    key: 'figures', path: `${DIR}/2026-12-sre-for-agents.figures.md`,
    guard: `HARD NO-GO ZONE: this file is mostly \`\`\`mermaid source. Every one of the 14 blocks was rendered and measured on 2026-09-16 (PASS 14 / FAIL 0) and the recorded 預期尺寸 lines are those measurements. Editing any character inside a fence invalidates the render. ONLY the prose outside the fences — headings, 圖說, 說明 and the 清單 table — is in scope. If the checker proposes a fix whose text sits inside a fence, reject it and say so.`,
  },
  { key: 'publish', path: `${DIR}/2026-12-sre-for-agents.publish.md`, guard: `Quoted post drafts are prose and in scope. Leave URLs, post ids, hashtags and English platform names alone.` },
  { key: 'selection', path: `${DIR}/selection.md`, guard: `Leave session ids, arXiv ids, file paths and the English book title alone.` },
  {
    key: 'backlog', path: `${DIR}/backlog.md`,
    guard: `Leave untouched: session ids, arXiv ids, handles (@...), query strings in the 訊號監看清單, URLs, and the numbers in the 成效權重 table. Quoted post titles — including Simplified-Chinese ones quoted from Facebook groups or from mainland sources — are evidence and stay verbatim; the checker will want to convert them, and that is exactly what you must refuse.`,
  },
  {
    key: 'digest', path: `${DIR}/conference_digest.md`,
    guard: `This file is mostly English with Chinese only in §4 (the October insertion table) and a few glosses. Only that Chinese prose is in scope. Every quoted line from a deck — Japanese, English or Chinese — is evidence and stays verbatim, as do speaker names, company names, session ids and slide numbers. Do not "fix" the English.`,
  },
  {
    key: 'readme', path: `${ROOT}/research/README.md`,
    guard: `Leave file paths, script names, flags, env-var names, the Mermaid block and the directory tree alone. Only the explanatory prose is in scope.`,
  },
]

const REPORT = {
  type: 'object', required: ['file', 'chunks', 'accepted', 'rejected', 'warnings_before', 'warnings_after', 'errors_after'],
  properties: {
    file: { type: 'string' },
    chunks: { type: 'integer' },
    accepted: { type: 'array', items: { type: 'string', description: 'e.g. "用戶→使用者 ×3"' } },
    rejected: { type: 'array', items: { type: 'string', description: 'e.g. "通過→透過 ×7 — 通過 here means passed"' } },
    warnings_before: { type: 'integer' }, warnings_after: { type: 'integer' }, errors_after: { type: 'integer' },
    unsure: { type: 'array', items: { type: 'string' } },
  },
}

phase('Pass')
log(`zh-tw gate over ${FILES.length} files plus the four inserted article sentences`)

const fileJobs = FILES.map(f => () => agent(`You are a Traditional-Chinese (Taiwan) copy editor with one tool job. Today is ${TODAY}. Repo root: ${ROOT}. Absolute paths only, never cd.
FILE: ${f.path}
${f.guard}
${PROCEDURE}`, { label: `zhtw:${f.key}`, phase: 'Pass', schema: REPORT, effort: 'high' }))

// The articles are a different problem: only the sentences this cycle inserted may change.
const ARTICLES = [
  { dir: '2026-10-green-testing', n: 2 },
  { dir: '2026-10-green-review', n: 1 },
  { dir: '2026-10-green-reliability', n: 1 },
]
const articleJob = () => agent(`You are a Traditional-Chinese (Taiwan) copy editor. Today is ${TODAY}. Repo root: ${ROOT}. Absolute paths only, never cd.
SCOPE: this cycle inserted four Chinese sentences (plus References rows) into three published-but-unreleased articles. ONLY those inserted lines may be edited. Everything else is the author's own published prose and is absolutely off limits.
Get the inserted lines with: cd ${ROOT} && git diff -U0 -- ${ARTICLES.map(a => a.dir + '/article.md').join(' ')} — lines prefixed '+' are yours. (${ARTICLES.map(a => `${a.dir}: ${a.n}`).join(', ')} body sentences.)
Load the checker via ToolSearch "select:mcp__zhtw-mcp__zhtw". Run each inserted line through mcp__zhtw-mcp__zhtw individually (content_type="markdown", fix_mode="lexical_safe", fix_output="search_replace", translationese_domain="technical", detect_ai=false, output="compact"). These lines already went through a voice pass against the author's 91K-character voice manual, so treat a suggestion that changes the register as suspect: only take a genuine Taiwan-usage or translationese fix.
${PROCEDURE.split('ACCEPT:')[1] ? 'ACCEPT:' + PROCEDURE.split('ACCEPT:')[1] : ''}
Additionally REJECT anything that would touch: a References row's title, URL, session id or date; the quoted paper title 「Habituation at the Gate…」; 「hack 驗證環境」 and the other verbatim terms quoted from 李博杰's book; the self-reported-evidence disclaimers (「我沒讀原文…」「是觀察值，不是門檻」) — those wordings were deliberate.
When done, PROVE you touched nothing else by running and pasting:
  cd ${ROOT} && python3 -c "import subprocess,glob
bad=0
for f in sorted(glob.glob('2026-10-green-*/article.md'))+sorted(glob.glob('2026-10-green-*/article.en.md')):
    old=subprocess.run(['git','show','HEAD:'+f],capture_output=True,text=True).stdout.splitlines()
    new=open(f).read().splitlines()
    missing=[l for l in old if l not in new]; bad+=len(missing)
    print(f,'author lines',len(old),'MISSING',len(missing))
print('VERDICT','AUTHOR PROSE INTACT' if bad==0 else 'AUTHOR PROSE CHANGED')"
MISSING must be 0 for every file. Then regenerate the pastes for any article you changed:
  cd ${ROOT} && python3 research/scripts/article_to_paste.py <dir> && python3 research/scripts/article_to_paste.py <dir> --lang en
Report as the schema asks; put the proof output in 'unsure' if there is nothing else to say there.`, { label: 'zhtw:articles', phase: 'Pass', schema: REPORT, effort: 'high' })

const reports = (await parallel([...fileJobs, articleJob])).filter(Boolean)
reports.forEach(r => log(`${r.file}: ${r.chunks} chunks, ${r.accepted.length} fix kinds applied, ${r.rejected.length} rejected, warnings ${r.warnings_before}→${r.warnings_after}, errors ${r.errors_after}`))

phase('Recheck')
const recheck = await agent(`Final gate check. Today is ${TODAY}. Repo ${ROOT}; absolute paths, never cd. Load ToolSearch "select:mcp__zhtw-mcp__zhtw".
Another set of editors just ran the zh-tw pass over these files:
${FILES.map(f => '  ' + f.path).join('\n')}
  plus the inserted sentences in 2026-10-green-{testing,review,reliability}/article.md
Do three things and report each with raw output.
(1) SPOT-CHECK: for each file, take two chunks you pick yourself (prefer the densest prose, not headings) and re-run the checker with the same settings. Report the error and warning counts. Errors must be 0.
(2) PROVE THE NO-GO ZONES HELD:
  cd ${ROOT} && python3 -c "import re,subprocess
for f in ['research/2026-10/2026-12-sre-for-agents.md','research/2026-10/2026-12-sre-for-agents.figures.md']:
    old=subprocess.run(['git','stash','list'],capture_output=True,text=True)
    t=open(f).read()
    print(f,'mermaid blocks',len(re.findall(r'^\`\`\`mermaid',t,re.M)),'double-dash',t.count('——'))"
  and re-render the figures to confirm nothing inside a fence moved:
  cd ${ROOT} && research/scripts/mermaid_check_all.sh research/2026-10/2026-12-sre-for-agents.figures.md
  That must still report PASS 14 / FAIL 0. If it does not, the zh-tw pass edited a Mermaid source: find the changed block and restore it.
  Then the author-prose invariant:
  cd ${ROOT} && python3 -c "import subprocess,glob
bad=0
for f in sorted(glob.glob('2026-10-green-*/article.md'))+sorted(glob.glob('2026-10-green-*/article.en.md')):
    old=subprocess.run(['git','show','HEAD:'+f],capture_output=True,text=True).stdout.splitlines()
    new=open(f).read().splitlines(); missing=[l for l in old if l not in new]; bad+=len(missing)
    print(f,'MISSING',len(missing))
print('VERDICT','AUTHOR PROSE INTACT' if bad==0 else 'AUTHOR PROSE CHANGED')"
(3) TESTS: cd ${ROOT} && python3 tools/test_tools.py 2>&1 | tail -3 && python3 -m unittest research/scripts/test_research_scripts.py 2>&1 | tail -3
Reply with the raw output of everything and a one-line VERDICT: PASS only if errors are 0 everywhere, the figures still render 14/14, author prose is intact and both suites are OK.`, { label: 'zhtw:recheck', phase: 'Recheck', effort: 'high' })

return { reports, recheck: recheck ? String(recheck).slice(0, 4000) : null }
