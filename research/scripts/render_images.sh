#!/usr/bin/env bash
# research/scripts/render_images.sh — 依 publish/<lang>/figures.json 把每張 Mermaid 圖與每個表格算繪成 PNG
#
#   research/scripts/render_images.sh 2026-10-green-overview        # publish/images/
#   research/scripts/render_images.sh 2026-10-green-overview en     # publish/en/images/
#
# 先跑 article_to_paste.py 產生 figures.json。圖走 mermaid_check.sh（含 MERMAID.md 的合規判定，
# FAIL 就不會寫進 images/），表格用同一套字型與 700px 欄寬的 HTML 算繪、2x 截圖。
# browse 是單一 daemon，所以一張一張跑。
set -uo pipefail
DIR="${1:?usage: render_images.sh <article-dir> [en]}"; LANG_="${2:-}"
ROOT="$(git rev-parse --show-toplevel)"; HERE="$(cd "$(dirname "$0")" && pwd)"
PUB="$ROOT/$DIR/publish${LANG_:+/$LANG_}"; IMG="$PUB/images"; mkdir -p "$IMG"
B="$HOME/.claude/skills/gstack/browse/dist/browse"
W="$ROOT/.context/render/$DIR${LANG_:+-$LANG_}"; rm -rf "$W"; mkdir -p "$W"
[ -f "$PUB/figures.json" ] || { echo "no $PUB/figures.json — run article_to_paste.py first" >&2; exit 64; }

python3 - "$PUB/figures.json" "$W" "$ROOT/MERMAID.md" <<'EOF'
import json, sys, html, re
spec, w = json.load(open(sys.argv[1])), sys.argv[2]
# a block without the MERMAID.md frontmatter (older articles, or a hand-written figure) gets the standard config
std = re.search(r"```mermaid\n(---\n.*?\n---\n)", open(sys.argv[3]).read(), re.S).group(1)
for f in spec["figures"]:
    src = f["mermaid"]
    if not src.lstrip().startswith('---'): src = std + src
    open(f"{w}/{f['file'][:-4]}.mmd", "w").write(src)
def md_table_to_html(md):
    rows = [r.strip().strip('|').split('|') for r in md.strip().split('\n')]
    head, body = rows[0], [r for r in rows[2:]]
    def cell(c):
        c = html.escape(c.strip())
        c = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', c); c = re.sub(r'`(.+?)`', r'<code>\1</code>', c)
        c = re.sub(r'\[(.+?)\]\((.+?)\)', r'\1', c); c = c.replace('&lt;br/&gt;', '<br/>').replace('&lt;br&gt;', '<br/>')
        return c
    # short cells (≤ 8 chars) must not wrap character by character: 「第 1 個月」 stacked four lines high reads badly
    nw = lambda c: ' class="nw"' if len(re.sub(r'\*|`', '', c.strip())) <= 8 else ''
    th = ''.join(f'<th{nw(c)}>{cell(c)}</th>' for c in head)
    trs = ''.join('<tr>' + ''.join(f'<td{nw(c)}>{cell(c)}</td>' for c in r) + '</tr>' for r in body)
    return f'<table><thead><tr>{th}</tr></thead><tbody>{trs}</tbody></table>'
for t in spec["tables"]:
    page = f'''<!doctype html><html><head><meta charset="utf-8"><style>
body{{margin:0;background:#fff}} #wrap{{display:inline-block;padding:16px;font-family:"Noto Sans TC","PingFang TC","Helvetica Neue",Arial,sans-serif;font-size:16px;color:#1f2933}}
table{{border-collapse:collapse;max-width:868px}} th,td{{border:1px solid #d1d5db;padding:8px 12px;vertical-align:top;text-align:left;line-height:1.5}}
th{{background:#f3f4f6;font-weight:600}} .nw{{white-space:nowrap}} code{{font-family:Menlo,Consolas,monospace;font-size:14px;background:#f3f4f6;padding:1px 4px;border-radius:3px}}
</style></head><body><div id="wrap">{md_table_to_html(t["markdown"])}</div></body></html>'''
    open(f"{w}/{t['file'][:-4]}.html", "w").write(page)
print(len(spec["figures"]), "figures,", len(spec["tables"]), "tables prepared")
EOF

fail=0
for m in "$W"/diagram-*.mmd; do
  [ -e "$m" ] || break
  n="$(basename "$m" .mmd)"
  if out="$("$HERE/mermaid_check.sh" "$m" "$W/$n" 2>&1)"; then cp "$W/$n.png" "$IMG/$n.png"; echo "  $n: $(echo "$out" | head -1 | sed 's/.*png  //')"
  else echo "  $n: FAIL"; echo "$out" | sed 's/^/     /'; fail=$((fail+1)); fi
done
if "$B" status 2>/dev/null | grep -q "Mode: headed"; then "$B" disconnect >/dev/null 2>&1 || true; fi
CUR=$("$B" js "window.innerWidth+'@'+window.devicePixelRatio" 2>/dev/null || echo "")
if [ "$CUR" != "1400@2" ]; then "$B" viewport 1400x1400 --scale 2 >/dev/null 2>&1 || true; "$B" js "new Promise(r=>setTimeout(r,1500)).then(()=>'ok')" >/dev/null 2>&1 || true; fi
for h in "$W"/table-*.html; do
  [ -e "$h" ] || break
  n="$(basename "$h" .html)"
  "$B" load-html "$h" >/dev/null 2>&1
  "$B" js "new Promise(r=>setTimeout(r,800)).then(()=>'ok')" >/dev/null 2>&1
  wpx=$("$B" js "Math.round(document.querySelector('#wrap').getBoundingClientRect().width)" 2>/dev/null)
  "$B" screenshot "$IMG/$n.png" --selector '#wrap' >/dev/null 2>&1 && echo "  $n: ${wpx}px wide"
done
echo "== images in $IMG: $(ls "$IMG" | wc -l | tr -d ' ')  (figure FAILs: $fail)"
[ "$fail" = "0" ]
