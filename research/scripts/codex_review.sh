#!/usr/bin/env bash
# research/scripts/codex_review.sh — 用 OpenAI Codex（第二個模型）審一份主題大綱或選題結果
#
#   research/scripts/codex_review.sh research/2026-09/2026-10-agentic-green-is-not-done.md
#   research/scripts/codex_review.sh research/2026-09/selection.md                  # 檔名是 selection* 就用選題的框架
#   EFFORT=high research/scripts/codex_review.sh <outline.md>                     # 預設 xhigh
#   KIND=selection research/scripts/codex_review.sh <file.md>                     # 強制指定框架：outline | selection
#
# 產出寫到檔案旁邊：research/<month>/codex-review-<slug>.md（Codex 的原話，不摘要），
# 之後由 Claude 依審查意見修訂，再跑 zh-tw 檢查。檔案必須在 repo 裡（解析 symlink 後比對前綴），
# 否則 review 會寫到 repo 外。
#
# 四份 digest 必須都在 research/<month>/ 下才跑。提示詞告訴 Codex 它們在 repo 裡、而且是唯一允許的
# 對照來源；但 notion_digest.md 與 community_digest.md 只留本機（.gitignore），fresh clone 上沒有。缺一份
# 就 exit 64：Codex 會把引用它的數字全判成憑空捏造，而幾週後重抓的 digest 是另一份快照，補不回同一份。
# 見 research/README.md「資料來源」。
#
# 為什麼要一個獨立模型：大綱是 Claude 寫、Claude 批評、Claude 修訂的；同一個模型
# 審自己會有盲點（arXiv 摘要裡 AI-reviews-AI 的閉環問題就是這個）。Codex 跑在 repo
# 根目錄、read-only sandbox，可以自己去讀 research/<month>/ 下的 digest 與 selection.md。
#
# 沿用 gstack /codex 的做法：timeout 包住、JSONL 輸出、串流解析、非零 exit 要印出來。
set -uo pipefail

FILE="${1:?usage: codex_review.sh <outline.md|selection.md>}"
EFFORT="${EFFORT:-xhigh}"
KIND="${KIND:-}"          # outline | selection；空的話依檔名判斷
TIMEOUT_S=900             # codex exec 的上限；xhigh 審一份大綱實測 5–10 分鐘
HERE="$(cd "$(dirname "$0")" && pwd)"
ROOT="$(git rev-parse --show-toplevel)" || exit 1
command -v codex >/dev/null || { echo "codex CLI not found (npm install -g @openai/codex)" >&2; exit 69; }
# FILE 是相對於呼叫者 cwd 的，所以在 cd "$ROOT" 之前先解析
[ -f "$FILE" ] || { echo "no such file: $FILE" >&2; exit 64; }

# 輸出檔寫在 FILE 旁邊。FILE 若是 repo 外的絕對路徑、用 ../ 走出去、或是 repo 內指向外面的 symlink，
# review 就會落在 repo 外；把檔案本身 realpath 之後比對前綴（目錄用 pwd -P 只解析到目錄，最後一節的
# symlink 會漏掉，實測漏過）。
ROOT_ABS="$(cd "$ROOT" && pwd -P)"
FILE_ABS="$(python3 -c 'import os, sys; print(os.path.realpath(sys.argv[1]))' "$FILE")"
case "$FILE_ABS" in
  "$ROOT_ABS"/*) ;;
  *) echo "refusing: $FILE resolves outside the repo ($FILE_ABS)" >&2; exit 64 ;;
esac
REL="${FILE_ABS#"$ROOT_ABS"/}"
cd "$ROOT" || exit 1
DIR="$(dirname "$REL")"; BASE="$(basename "$REL" .md)"
OUTFILE="$DIR/codex-review-$BASE.md"
TMPERR="$(mktemp)"; trap 'rm -f "$TMPERR"' EXIT

if [ -z "$KIND" ]; then
  case "$BASE" in selection*) KIND=selection ;; *) KIND=outline ;; esac
fi
# 兩種文件共用同一張審查清單，差在開頭那段「你手上這份是什麼」與最後要對照的檔。
case "$KIND" in
  outline)
    WHAT="THE PLAN"
    FRAMING="Below is the PLAN for one monthly theme (one 總論 overview + three deep dives, 三部曲)."
    ALSO="Also read $DIR/selection.md (the judges' objections the plan must honour) and $DIR/style_brief.md (the author's format)." ;;
  selection)
    WHAT="THE SELECTION"
    FRAMING="Below is the SELECTION for the next three monthly themes (one theme per month, each to become one 總論 overview + three deep dives, 三部曲): the judged shortlist, the three chosen themes with their thesis and piece breakdown, and the objections the judges raised. Review the choice itself as much as the theses: are these the right three themes, in the right order, do the theses survive the recorded objections, and is each theme distinct enough from the others and from the author's published series?"
    ALSO="Also read $DIR/backlog.md (the candidates that lost and the signals watched) and $DIR/style_brief.md (the author's format)." ;;
  *) echo "KIND must be outline or selection, got '$KIND'" >&2; exit 64 ;;
esac

# 提示詞裡的 digest 清單和這裡的檢查用同一份，加一份 digest 兩邊不會走散。bash 3.2 + set -u 下空陣列
# 展開會炸，所以用字串接。
DIGESTS="arxiv.md x_digest.md community_digest.md notion_digest.md"
DIGEST_LIST=""; MISSING=""
for f in $DIGESTS; do
  DIGEST_LIST="${DIGEST_LIST:+$DIGEST_LIST, }$DIR/$f"
  [ -f "$DIR/$f" ] || MISSING="$MISSING  $DIR/$f"$'\n'
done
if [ -n "$MISSING" ]; then
  {
    echo "refusing: the prompt tells Codex these digests are in the repo, but they are missing under $DIR/:"
    printf '%s' "$MISSING"
    echo "notion_digest.md and community_digest.md are local-only (gitignored, absent on a fresh clone). A digest"
    echo "re-collected later is a different snapshot, so Codex would flag every citation to the original as invented."
    echo "Restore the same files first; see research/README.md「資料來源」."
  } >&2
  exit 64
fi

PROMPT="IMPORTANT: Do NOT read or execute any files under ~/.claude/, ~/.agents/, .claude/skills/, or agents/. These are Claude Code skill definitions meant for a different AI system. Do NOT modify anything. Stay inside this repository and treat it as read-only.

You are a brutally honest reviewer for a Medium author who writes long-form Traditional-Chinese (Taiwan) articles for Engineering VPs and Staff engineers. $FRAMING Review it for:
1. Logical gaps and unstated assumptions in the thesis; claims that are stronger than the cited evidence supports.
2. Every cited source: does the document use it honestly? Check numbers against $DIGEST_LIST (read them; they are in the repo). Flag anything invented, misquoted, or domain-mismatched (e.g. a non-coding benchmark presented as coding-agent evidence).
3. Overlap: with the author's four published articles ($ROOT/2026-09-agentic-engineering-platform/article.md, 2026-09-agentic-org-design, 2026-10-agentic-harness-blueprint, 2026-11-agentic-eval-economics) and between the pieces of this document.
4. Whether each piece gives a Staff engineer or VP something actionable (a reference implementation, decision table, gate), and whether the whole series can be written in one month by one author with an AI collaborator.
5. What is missing that a sharp reader would ask about; what to cut.
$ALSO
Be direct, terse, no compliments. Output in 繁體中文（台灣用語，技術名詞保留英文）. Structure: 致命問題 / 重要問題 / 次要問題 / 建議刪除 / 建議補充, each item with the exact section it refers to and a concrete fix.

$WHAT ($REL):
$(cat "$FILE_ABS")"

echo "== codex review ($EFFORT, $KIND) → $OUTFILE" >&2
{
  echo "# Codex review — $BASE"
  echo
  echo "> model: $(grep -E '^model ' ~/.codex/config.toml 2>/dev/null | cut -d'"' -f2), reasoning: $EFFORT, $(date '+%Y-%m-%d %H:%M'). 原話照錄，未經摘要。"
  echo
} > "$OUTFILE"

if command -v gtimeout >/dev/null; then TO=gtimeout; elif command -v timeout >/dev/null; then TO=timeout; else TO=""; fi
$TO ${TO:+$TIMEOUT_S} codex exec "$PROMPT" -C "$ROOT" -s read-only -c "model_reasoning_effort=\"$EFFORT\"" -c 'web_search="cached"' --json < /dev/null 2>"$TMPERR" \
| python3 -u "$HERE/codex_jsonl.py" | tee -a "$OUTFILE"
# 一次接住整個陣列：`rc=${PIPESTATUS[0]}` 本身是一道指令，做完 PIPESTATUS 就只剩它自己的 0，
# 下一句的 PIPESTATUS[1] 在 set -u 下直接炸（原版就是這樣寫，實測會死在這裡）
pipe=("${PIPESTATUS[@]}"); rc=${pipe[0]}; prc=${pipe[1]}
if [ "$rc" = "124" ]; then echo "Codex stalled past $((TIMEOUT_S / 60)) minutes (TIMEOUT_S=$TIMEOUT_S)." >&2; rm -f "$OUTFILE"; exit 124; fi
if [ "$rc" != "0" ]; then echo "[codex exit $rc] $(head -3 "$TMPERR")" >&2; rm -f "$OUTFILE"; exit "$rc"; fi
if [ "$prc" != "0" ]; then echo "[codex produced no review; parser exit $prc — usage limit or refusal, see messages above]" >&2; rm -f "$OUTFILE"; exit "$prc"; fi
echo "== written $OUTFILE ($(wc -c < "$OUTFILE") bytes)" >&2
