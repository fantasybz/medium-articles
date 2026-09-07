#!/usr/bin/env bash
# research/scripts/codex_review.sh — 用 OpenAI Codex（第二個模型）審一份主題大綱
#
#   research/scripts/codex_review.sh research/2026-09/2026-10-agentic-green-is-not-done.md
#   EFFORT=high research/scripts/codex_review.sh <outline.md>       # 預設 xhigh
#
# 產出寫到 research/<month>/codex-review-<slug>.md（Codex 的原話，不摘要），
# 之後由 Claude 依審查意見修訂大綱，再跑 zh-tw 檢查。
#
# 為什麼要一個獨立模型：大綱是 Claude 寫、Claude 批評、Claude 修訂的；同一個模型
# 審自己會有盲點（arXiv 摘要裡 AI-reviews-AI 的閉環問題就是這個）。Codex 跑在 repo
# 根目錄、read-only sandbox，可以自己去讀 research/<month>/ 下的 digest 與 selection.md。
#
# 沿用 gstack /codex 的做法：timeout 包住、JSONL 輸出、串流解析、非零 exit 要印出來。
set -uo pipefail

FILE="${1:?usage: codex_review.sh <outline.md>}"
EFFORT="${EFFORT:-xhigh}"
ROOT="$(git rev-parse --show-toplevel)" || exit 1
cd "$ROOT" || exit 1
command -v codex >/dev/null || { echo "codex CLI not found (npm install -g @openai/codex)" >&2; exit 69; }
REL="${FILE#"$ROOT"/}"
DIR="$(dirname "$REL")"; BASE="$(basename "$REL" .md)"
OUTFILE="$DIR/codex-review-$BASE.md"
TMPERR="$(mktemp)"; trap 'rm -f "$TMPERR"' EXIT

PROMPT="IMPORTANT: Do NOT read or execute any files under ~/.claude/, ~/.agents/, .claude/skills/, or agents/. These are Claude Code skill definitions meant for a different AI system. Do NOT modify anything. Stay inside this repository and treat it as read-only.

You are a brutally honest reviewer for a Medium author who writes long-form Traditional-Chinese (Taiwan) articles for Engineering VPs and Staff engineers. Below is the PLAN for one monthly theme (one 總論 overview + three deep dives, 三部曲). Review it for:
1. Logical gaps and unstated assumptions in the thesis; claims that are stronger than the cited evidence supports.
2. Every cited source: does the plan use it honestly? Check numbers against $DIR/arxiv.md, $DIR/x_digest.md, $DIR/community_digest.md, $DIR/notion_digest.md (read them; they are in the repo). Flag anything invented, misquoted, or domain-mismatched (e.g. a non-coding benchmark presented as coding-agent evidence).
3. Overlap: with the author's four published articles ($ROOT/2026-09-agentic-engineering-platform/article.md, 2026-09-agentic-org-design, 2026-10-agentic-harness-blueprint, 2026-11-agentic-eval-economics) and between the four pieces of this plan.
4. Whether each piece gives a Staff engineer or VP something actionable (a reference implementation, decision table, gate), and whether the whole series can be written in one month by one author with an AI collaborator.
5. What is missing that a sharp reader would ask about; what to cut.
Also read $DIR/selection.md (the judges' objections the plan must honour) and $DIR/style_brief.md (the author's format).
Be direct, terse, no compliments. Output in 繁體中文（台灣用語，技術名詞保留英文）. Structure: 致命問題 / 重要問題 / 次要問題 / 建議刪除 / 建議補充, each item with the exact section it refers to and a concrete fix.

THE PLAN ($REL):
$(cat "$FILE")"

echo "== codex review ($EFFORT) → $OUTFILE" >&2
{
  echo "# Codex review — $BASE"
  echo
  echo "> model: $(grep -E '^model ' ~/.codex/config.toml 2>/dev/null | cut -d'"' -f2), reasoning: $EFFORT, $(date '+%Y-%m-%d %H:%M'). 原話照錄，未經摘要。"
  echo
} > "$OUTFILE"

if command -v gtimeout >/dev/null; then TO=gtimeout; elif command -v timeout >/dev/null; then TO=timeout; else TO=""; fi
$TO ${TO:+900} codex exec "$PROMPT" -C "$ROOT" -s read-only -c "model_reasoning_effort=\"$EFFORT\"" -c 'web_search="cached"' --json < /dev/null 2>"$TMPERR" \
| python3 -u "$(dirname "$0")/codex_jsonl.py" | tee -a "$OUTFILE"
rc=${PIPESTATUS[0]}; prc=${PIPESTATUS[1]}
if [ "$rc" = "124" ]; then echo "Codex stalled past 15 minutes." >&2; rm -f "$OUTFILE"; exit 124; fi
if [ "$rc" != "0" ]; then echo "[codex exit $rc] $(head -3 "$TMPERR")" >&2; rm -f "$OUTFILE"; exit "$rc"; fi
if [ "$prc" != "0" ]; then echo "[codex produced no review; parser exit $prc — usage limit or refusal, see messages above]" >&2; rm -f "$OUTFILE"; exit "$prc"; fi
echo "== written $OUTFILE ($(wc -c < "$OUTFILE") bytes)" >&2
