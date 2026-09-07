#!/usr/bin/env bash
# research/scripts/mermaid_check_all.sh — 把一份 markdown 裡所有 ```mermaid 區塊抽出來，逐張跑 mermaid_check.sh
#
#   research/scripts/mermaid_check_all.sh research/2026-09/2026-10-agentic-green-is-not-done.figures.md
#
# 區塊會寫到 .context/mermaid/<檔名>/NN.mmd（含前一行的標題當註解），PNG／SVG 也放在那裡。
# 逐張跑是因為 browse 是單一 daemon；結果最後列成一張表，FAIL 的行帶原因。
# 一張圖都沒有時印 `0 mermaid blocks` 就結束（exit 0）：沒有東西可以 FAIL。
set -uo pipefail
MD="${1:?usage: mermaid_check_all.sh <file.md>}"
HERE="$(cd "$(dirname "$0")" && pwd)"
. "$HERE/_common.sh"        # ROOT、EX_*、refuse_if_collecting
[ -f "$MD" ] || { echo "no such file: $MD" >&2; exit "$EX_USAGE"; }
BASE="$(basename "$MD" .md)"
# 工作目錄會被 rm -rf。BASE 出自 basename 所以不會含 /，但 `.`／`..`／空字串會讓它指到
# .context/mermaid 本身或更上層，所以還是擋一次。
case "$BASE" in
  ''|.|..|*/*) echo "refusing to use '$BASE' as a work directory name" >&2; exit "$EX_USAGE" ;;
esac
refuse_if_collecting        # 逐張才發現會印一排 FAIL；在這裡一次說清楚
W="$ROOT/.context/mermaid/$BASE"; rm -rf "$W"; mkdir -p "$W"

n=$(python3 - "$MD" "$W" <<'EOF'
import re, sys
md, out = sys.argv[1], sys.argv[2]
text = open(md).read()
# capture the nearest preceding heading as the figure's label
blocks = list(re.finditer(r"```mermaid\n(.*?)```", text, re.S))
heads = [(m.start(), m.group(1).strip()) for m in re.finditer(r"^#{1,6} +(.+)$", text, re.M)]
for i, m in enumerate(blocks, 1):
    label = ''
    for pos, h in heads:
        if pos < m.start(): label = h
    with open(f"{out}/{i:02d}.mmd", "w") as fh:
        fh.write(m.group(1))
    with open(f"{out}/{i:02d}.label", "w") as fh:
        fh.write(label)
print(len(blocks))
EOF
) || { echo "could not extract mermaid blocks from $MD" >&2; exit 1; }

echo "== $MD: $n mermaid blocks"
[ "$n" != "0" ] || exit 0
pass=0; fail=0
printf '%-4s %-8s %-7s %-6s %-5s %s\n' '#' 'size' 'aspect' 'nodes' 'ok' 'figure'
for f in "$W"/*.mmd; do
  [ -e "$f" ] || break        # 沒有 nullglob 時，空目錄會把字面上的 * 交給迴圈
  i="$(basename "$f" .mmd)"; label="$(cut -c1-60 "$W/$i.label" 2>/dev/null)"
  res="$("$HERE/mermaid_check.sh" "$f" "$W/$i" 2>/dev/null)"; rc=$?
  size="$(echo "$res" | sed -n 's/.* \([0-9]*x[0-9]*\) css px.*/\1/p')"
  aspect="$(echo "$res" | sed -n 's/.*aspect \([0-9.]*\).*/\1/p')"
  nodes="$(echo "$res" | sed -n 's/.*nodes \([0-9]*\).*/\1/p')"
  if [ "$rc" = "0" ]; then ok=PASS; pass=$((pass+1)); else ok=FAIL; fail=$((fail+1)); fi
  printf '%-4s %-8s %-7s %-6s %-5s %s\n' "$i" "${size:-?}" "${aspect:-?}" "${nodes:-?}" "$ok" "$label"
  if [ "$rc" != "0" ]; then echo "$res" | grep -E '^(  - |RENDER ERROR)' | sed 's/^/       /'; fi
done
echo "== PASS $pass / FAIL $fail  (renders in $W)"
[ "$fail" = "0" ]
