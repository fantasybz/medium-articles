export const meta = {
  name: 'research-2026-10-december-repair',
  description: 'Close the two gaps the recut left: recover the promo/English-edition content the tail reviser moved into a file it never created, and sweep the renumbered outline for dangling cross-references, figure ids and References rows.',
  phases: [
    { title: 'Recover', detail: 'write the missing .publish.md, verify nothing was lost' },
    { title: 'Sweep', detail: 'three lenses over the recut outline: sections, figures, references' },
    { title: 'Fix', detail: 'apply confirmed issues in place' },
  ],
}

const ROOT = args.root
const TODAY = args.today
const DIR = `${ROOT}/research/2026-10`
const PREV = `${ROOT}/research/2026-09`
const OUTLINE = `${DIR}/2026-12-sre-for-agents.md`
const ORIG = `${PREV}/2026-12-sre-for-agents.md`
const PUBFILE = `${DIR}/2026-12-sre-for-agents.publish.md`
const PLAN = `${ROOT}/.context/research/2026-10/dec-recut-plan.json`

const CONTEXT = `Today is ${TODAY}. Repo root ${ROOT}; absolute paths only, never cd.
The author (@fantasybz, Kochi Chuang) publishes one THEME per month on Medium in Traditional Chinese (Taiwan usage; English technical terms kept; single "—" dash, NEVER "——"), plus an English edition.
${OUTLINE} is the 2026-12 outline, just re-cut in place from ${ORIG} (the pre-recut copy, still on disk and unchanged — use it as the "before" side of any comparison). The edit plan that drove the re-cut is ${PLAN} (JSON: structure, pieces[].edits[], figures, open_questions).
The re-cut renumbered sections heavily: 可靠篇 went 8 sections → 7, 應變篇 7 → 6, 觀測篇 was re-ordered into 7, and several figures were dropped (F2, G5, R5, plus markers) or added (F14, G7, G8, R6, R7, I6). Mermaid code blocks must NEVER be edited — a figure whose source needs changing carries a '<!-- FIGURE CHANGED: <id> — <what> -->' marker instead, and the separate renderer step acts on it later.`

const ISSUES = {
  type: 'object', required: ['checked', 'issues'],
  properties: {
    checked: { type: 'integer', description: 'how many references/ids/rows were resolved' },
    issues: { type: 'array', items: { type: 'object', required: ['quote', 'problem', 'fix', 'severity'], properties: {
      quote: { type: 'string', description: 'the exact text in the outline that is wrong (copy-paste, unique enough to Edit on)' },
      problem: { type: 'string', description: 'what it points at and why that does not resolve, with line numbers on both sides' },
      fix: { type: 'string', description: 'the exact replacement text, or DELETE' },
      severity: { type: 'string', enum: ['dangling', 'miscount', 'orphan', 'duplicate'] },
    } } },
  },
}
const FILE = { type: 'object', required: ['path', 'summary'], properties: { path: { type: 'string' }, summary: { type: 'string' }, recovered: { type: 'array', items: { type: 'string' } } } }

// ---------------------------------------------------------------- Recover
const recover = async () => {
  const w = await agent(`${CONTEXT}
TASK: the tail reviser of the re-cut moved the promotion and English-edition material OUT of the outline and wrote a pointer to ${PUBFILE} — but never created that file, so the content is currently lost from the repo and the pointer dangles. Recover it.
Steps: (1) grep the current ${OUTLINE} for the pointer sentence and read its whole surrounding section, so you know exactly what the outline still keeps versus what it says was moved out. (2) Read §5 英文版與推廣 and §6 發布 of the PRE-RECUT copy ${ORIG} in full — that is the material that existed before. (3) Read ${PLAN} and find the tail piece's edits that split this content (they say what should stay in the main plan and what moves out). (4) Read the re-cut outline's header blockquote and §1 so the promo copy matches the NEW spine ("trace 是除錯用的，ledger 才是證據用的") rather than the old one — a hook that sells a section the re-cut deleted must be rewritten or dropped, and say which you did.
Then Write ${PUBFILE}: a standalone Traditional-Chinese file titled for the December series, holding everything the outline delegated to it — the English-edition plan, Medium topics, cover-image decisions, publishing order and dates, the X / LinkedIn / Facebook post drafts and hooks, and the community follow-up. Open it with a one-line pointer back to ${OUTLINE} so the two files are navigable in both directions. Keep the author's voice; single "—" only. Do not invent a new promotion idea that has no basis in ${ORIG} or ${PLAN}; if something in the old copy is now obsolete because the re-cut deleted the section it advertised, keep it but mark it 「（原 §X 已刪，此則作廢）」.
Return path, summary, and 'recovered' = one line per block of content you carried over, naming where it came from.`, { label: 'recover:publish-file', phase: 'Recover', schema: FILE, effort: 'high' })
  if (!w) { log('recover: writer died'); return null }
  const v = await agent(`${CONTEXT}
You are a skeptical checker. Compare ${PUBFILE} (just written) against §5 and §6 of ${ORIG} (the pre-recut copy) and against what ${OUTLINE} still keeps.
Check: (1) every distinct item in the old §5/§6 is either present in ${PUBFILE}, still present in ${OUTLINE}, or explicitly marked obsolete — list anything that is in NONE of the three (that is lost content, severity 'orphan'); (2) nothing appears in BOTH ${PUBFILE} and ${OUTLINE} in full (severity 'duplicate' — the outline should keep only the one-line pointer plus whatever the plan said stays); (3) the pointer in ${OUTLINE} resolves to the file's real path; (4) dates, post ids and URLs in ${PUBFILE} match ${ORIG} or the articles' publish/PUBLISHED.md ledgers — no invented schedule. Report only what you have both source lines for.`, { label: 'verify:publish-file', phase: 'Recover', schema: ISSUES, effort: 'high' })
  if (v) log(`publish file: ${v.checked} checked, ${v.issues.length} issues`)
  if (v && v.issues.length) {
    await agent(`Apply these corrections to ${PUBFILE} (and to ${OUTLINE} only where the issue says the outline duplicates the moved content) with the Edit tool, one at a time, nothing else. Never touch a \`\`\`mermaid block.\n${JSON.stringify(v.issues, null, 1)}`, { label: 'fix:publish-file', phase: 'Recover', effort: 'low' })
  }
  return { file: PUBFILE, checked: v ? v.checked : null, issues: v ? v.issues.length : null }
}

// ---------------------------------------------------------------- Sweep (three lenses, parallel)
const LENSES = [
  { key: 'sections', prompt: `Sweep ${OUTLINE} for DANGLING SECTION CROSS-REFERENCES. The re-cut renumbered sections, so a pointer written before the re-cut can now aim at the wrong place or at nothing.
Method: first build the ground truth — list every heading in the file with its line number (grep -n '^#\\{1,4\\} ' and the numbered 「§N」/「一、二、三…」 headings inside each piece). Then find every cross-reference in the prose: 「見 §N」「§N 的」「本篇 §N」「總論 §N」「觀測篇 §N」「可靠篇 §N」「應變篇 §N」「移至…」「已移到…」「原 §N」「下一節」「上一節」. For each, resolve it against the ground truth and report a 'dangling' issue when the target section does not exist, is a different topic than the sentence claims, or the piece named is wrong. Quote the sentence verbatim and give the corrected pointer as 'fix'. A reference written as 「原 §N（已刪／已移至 X）」 is correct by design — do not flag it.` },
  { key: 'figures', prompt: `Sweep ${OUTLINE} for FIGURE / TABLE ID problems. Ground truth: the figure ids in ${DIR}/2026-12-sre-for-agents.figures.md, the '<!-- FIGURE CHANGED/DROPPED/NEW: <id> -->' markers in the outline, and each piece's 「圖與表」 list.
Check: (1) every figure id mentioned in prose (F1–F14, G1–G8, R1–R7, I1–I6) either has a marker, a block, or a row in the piece's list — an id mentioned nowhere else is an 'orphan'; (2) every DROPPED id no longer appears as a live reference in prose (only as 「已刪」); (3) each piece's 「圖與表（N 張）」 count equals the number of entries actually listed under it — a mismatch is a 'miscount'; recompute and give the right number in 'fix'; (4) the 圖清單 at the top of the file agrees with the per-piece lists on which ids exist. Do NOT edit or propose edits to any \`\`\`mermaid source — if a figure's content is wrong, the fix is a marker line, not a block edit.` },
  { key: 'references', prompt: `Sweep ${OUTLINE} for REFERENCES and 來源對照 problems. Each piece has a numbered References list and the file has 來源對照 tables.
Check: (1) every numbered reference is cited at least once in that piece's body — an uncited row is an 'orphan'; (2) every inline citation (arXiv id, session id like \`2QlDa\`, book chapter §) has a matching References row or 來源對照 entry — a citation with no row is 'dangling'; (3) the file declares some sources deleted (grep 「本次刪除的來源」) — a deleted source still carrying a 來源對照 row or a body citation is 'dangling'; (4) References numbering is contiguous with no repeats; (5) the 總論 References honours the stated 8–12 條 cap, or the text says why not. Check arXiv ids against ${DIR}/arxiv.md and session ids against ${DIR}/conference_digest.md — an id in neither is 'dangling'.` },
]

const sweep = async () => {
  const found = await parallel(LENSES.map(l => () =>
    agent(`${CONTEXT}\n${l.prompt}\nReturn the structured result. Report an issue only when you have both sides in front of you (the reference and what it points at). Do not flag style.`,
      { label: `sweep:${l.key}`, phase: 'Sweep', schema: ISSUES, effort: 'high' })))
  const all = found.filter(Boolean).flatMap((r, i) => r.issues.map(x => ({ ...x, lens: LENSES[i].key })))
  log(`sweep: ${found.filter(Boolean).map((r, i) => `${LENSES[i].key}=${r.issues.length}/${r.checked}`).join(' ')}`)
  return all
}

// ---------------------------------------------------------------- run
const [rec, issues] = await parallel([recover, sweep])

let fixed = null
if (issues && issues.length) {
  phase('Fix')
  fixed = await agent(`${CONTEXT}
TASK: apply these confirmed cross-reference problems to ${OUTLINE} in place with the Edit tool, one at a time, changing nothing else. NEVER touch a \`\`\`mermaid block — a figure-content problem is fixed by editing or adding its '<!-- FIGURE ... -->' marker line. If a 'fix' says DELETE, remove just that clause or row. If two issues contradict each other, apply the one whose 'problem' cites line numbers you can confirm, and say in your reply which you skipped and why.
Afterwards re-run the three cheap self-checks and paste their output: python3 -c "import re;t=open('${OUTLINE}').read();print('fences',t.count('\`\`\`')%2==0,'dashes',t.count('——'))" ; grep -c '^### ' ${OUTLINE} ; tail -3 ${OUTLINE}
ISSUES:
${JSON.stringify(issues, null, 1)}`, { label: 'fix:sweep', phase: 'Fix', effort: 'high' })
}

return { recover: rec, issueCount: issues ? issues.length : 0, byLens: (issues || []).reduce((a, x) => ({ ...a, [x.lens]: (a[x.lens] || 0) + 1 }), {}), fixed: fixed ? String(fixed).slice(0, 2000) : null }
