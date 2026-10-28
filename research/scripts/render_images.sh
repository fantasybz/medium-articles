#!/usr/bin/env bash
# research/scripts/render_images.sh — 依 publish/<lang>/figures.json 把每張 Mermaid 圖與每個表格算繪成 PNG
#
#   research/scripts/render_images.sh 2026-10-green-overview        # publish/images/
#   research/scripts/render_images.sh 2026-10-green-overview en     # publish/en/images/
#
# 先跑 article_to_paste.py 產生 figures.json。圖走 mermaid_check.sh（含 MERMAID.md 的合規判定，
# FAIL 就不會寫進 images/），表格用同一套字型與 700px 欄寬的 HTML 算繪、2x 截圖。
# assets 裡的本機 PNG 核對 SHA-256 後原樣複製，不經瀏覽器、不重新算繪。
# 開始算繪前先把上一輪的 diagram-*.png / table-*.png 清掉：FAIL 的圖沒有新檔，舊檔留著會像 PASS。
# 圖與表任何一個 FAIL 都以非零離開。browse 是單一 daemon，所以一張一張跑。
set -uo pipefail
DIR="${1:?usage: render_images.sh <article-dir> [en]}"; LANG_="${2:-}"
HERE="$(cd "$(dirname "$0")" && pwd)"
. "$HERE/_common.sh"        # ROOT、EX_*、BROWSE、prepare_headless_viewport

# 兩個參數都會進 rm -rf 與 mkdir 的路徑，先驗完再碰檔案系統。
# DIR 是 repo 根目錄下的文章資料夾名（不是路徑）；LANG_ 是 publish/ 下的語言包名（同 medium_draft.sh 的規則）。
case "$DIR" in
  ''|.|..|*/*) echo "article-dir must be a directory name under the repo root, got '$DIR'" >&2; exit "$EX_USAGE" ;;
esac
case "$LANG_" in
  *[!a-zA-Z0-9_-]*) echo "invalid lang '$LANG_': letters, digits, - and _ only" >&2; exit "$EX_USAGE" ;;
esac
[ -d "$ROOT/$DIR" ] || { echo "no such article dir: $ROOT/$DIR" >&2; exit "$EX_USAGE"; }
PUB="$ROOT/$DIR/publish${LANG_:+/$LANG_}"; IMG="$PUB/images"
[ -f "$PUB/figures.json" ] || { echo "no $PUB/figures.json — run article_to_paste.py first" >&2; exit "$EX_USAGE"; }
refuse_if_collecting
W="$ROOT/.context/render/$DIR${LANG_:+-$LANG_}"; rm -rf "$W"; mkdir -p "$W" "$IMG"

python3 - "$PUB/figures.json" "$W" "$ROOT/MERMAID.md" "$ROOT/$DIR" "$HERE" <<'EOF' || { echo "could not prepare the render inputs from $PUB/figures.json" >&2; exit 1; }
import hashlib, json, sys, html, re
from pathlib import Path
sys.path.insert(0, sys.argv[5])
from article_to_paste import read_local_png
spec, w = json.load(open(sys.argv[1])), sys.argv[2]
# Validate and stage every asset before clearing the previous output. A changed
# source requires regenerating figures.json, so its digest remains useful evidence.
assets = spec.get("assets", [])
for i, asset in enumerate(assets, 1):
    if asset["file"] != "asset-%02d.png" % i:
        sys.exit("invalid local PNG slot filename: %r" % asset["file"])
    data = read_local_png(sys.argv[4], asset["source"])
    if hashlib.sha256(data).hexdigest() != asset["sha256"]:
        sys.exit("local PNG changed since figures.json: %s; rerun article_to_paste.py" % asset["source"])
    Path(w, asset["file"]).write_bytes(data)
Path(w, "assets.json").write_text(json.dumps(assets, ensure_ascii=False, indent=1), encoding="utf-8")
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

# 輸入都備妥了才清舊檔：figures.json 壞掉時不該連上一輪的成品一起沒了。
# 瀏覽器也要先確認拿得到：daemon 屬於別的 session 時 prepare_headless_viewport 以 75 退出，舊 PNG 必須還在。
if compgen -G "$W/diagram-*.mmd" >/dev/null || compgen -G "$W/table-*.html" >/dev/null; then prepare_headless_viewport; fi
rm -f "$IMG"/diagram-*.png "$IMG"/table-*.png "$IMG"/asset-*.png "$PUB/.rendered-assets.json"

python3 - "$W" "$IMG" "$PUB/.rendered-assets.json" <<'EOF' || exit 1
import hashlib, json, shutil, sys
from pathlib import Path
assets = json.loads(Path(sys.argv[1], "assets.json").read_text(encoding="utf-8"))
verified = []
for asset in assets:
    target = Path(sys.argv[2], asset["file"])
    shutil.copyfile(Path(sys.argv[1], asset["file"]), target)
    copied = hashlib.sha256(target.read_bytes()).hexdigest()
    if copied != asset["sha256"]:
        target.unlink()
        sys.exit("local PNG copy checksum mismatch: %s" % target)
    # Evidence about bytes only: file, source, both digests. The caption that
    # figures.json also records is prose, and rewording it must not make the
    # copy evidence read as stale.
    verified.append({"file": asset["file"], "source": asset["source"],
                     "sha256": asset["sha256"], "copied_sha256": copied})
    print("  %s: copied unchanged (SHA-256 %s)" % (asset["file"], copied))
if verified:
    Path(sys.argv[3]).write_text(json.dumps({"method": "byte-copy", "assets": verified},
                                          ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
EOF

fail=0
for m in "$W"/diagram-*.mmd; do
  [ -e "$m" ] || break
  n="$(basename "$m" .mmd)"
  if out="$("$HERE/mermaid_check.sh" "$m" "$W/$n" 2>&1)"; then
    if cp "$W/$n.png" "$IMG/$n.png"; then echo "  $n: $(echo "$out" | head -1 | sed 's/.*png  //')"; else echo "  $n: FAIL (copy)"; fail=$((fail+1)); fi
  else echo "  $n: FAIL"; echo "$out" | sed 's/^/     /'; fail=$((fail+1)); fi
done

# 瀏覽器已在清舊檔之前由 prepare_headless_viewport 準備好（只有表格的發布包也走那一次）。
# 表格截圖走與 mermaid_check.sh 同一道 PNG 檔頭核對：寬、高都要是 #wrap 的 HEADLESS_SCALE 倍，否則是 1x 或裁切，
# 不能進 images/。先截到 $W（FAIL 的截圖留在那裡供檢視），核對過才複製。印出「png WxH, Nx」並以 0 退出；否則印原因、非 0 退出。
table_png_verdict() {
  python3 - "$1" "$2" "$HEADLESS_SCALE" <<'EOF'
import struct, sys
path, wrap, scale = sys.argv[1], sys.argv[2], int(sys.argv[3])
PNG_TOL_PX = 4   # 2x 截圖的畫素取整，同 mermaid_check.sh
try:
    head = open(path, 'rb').read(24)
except OSError as e:
    print(f"no screenshot: {e}"); sys.exit(1)
if head[:8] != b'\x89PNG\r\n\x1a\n' or len(head) < 24:
    print("screenshot is not a PNG"); sys.exit(1)
w, h = struct.unpack('>II', head[16:24])
ww, _, wh = wrap.partition('@')
if not (ww.isdigit() and wh.isdigit()):
    print(f"png {w}x{h}, but the #wrap size is unknown ({wrap})"); sys.exit(1)
if abs(w - scale * int(ww)) > PNG_TOL_PX:
    print(f"png {w}px wide, expected {scale}x of the {ww}px #wrap"); sys.exit(1)
if abs(h - scale * int(wh)) > PNG_TOL_PX:
    print(f"png {h}px tall, expected {scale}x of the {wh}px #wrap (clipped screenshot?)"); sys.exit(1)
print(f"png {w}x{h}, {scale}x")
EOF
}
for h in "$W"/table-*.html; do
  [ -e "$h" ] || break
  n="$(basename "$h" .html)"
  # browse 把失敗原因寫在 stderr：收下來印在 FAIL 列下面，不要只剩一個括號
  if ! err="$("$BROWSE" load-html "$h" 2>&1 >/dev/null)"; then
    echo "  $n: FAIL (load-html)"; printf '%s\n' "$err" | sed '/^$/d; s/^/     /'; fail=$((fail+1)); continue
  fi
  "$BROWSE" js "new Promise(r=>setTimeout(r,800)).then(()=>'ok')" >/dev/null 2>&1 || true
  wrap=$("$BROWSE" js "(()=>{const r=document.querySelector('#wrap').getBoundingClientRect();return Math.round(r.width)+'@'+Math.round(r.height)})()" 2>/dev/null) || wrap="?"
  verdict=""; err="$("$BROWSE" screenshot "$W/$n.png" --selector '#wrap' 2>&1 >/dev/null)"; rc=$?
  if [ "$rc" = "0" ] && verdict="$(table_png_verdict "$W/$n.png" "$wrap")"; then
    if cp "$W/$n.png" "$IMG/$n.png"; then echo "  $n: ${wrap%@*}px wide ($verdict)"; else echo "  $n: FAIL (copy)"; fail=$((fail+1)); fi
  else
    echo "  $n: FAIL (${verdict:-screenshot})"; printf '%s\n' "$err" | sed '/^$/d; s/^/     /'; fail=$((fail+1))
  fi
done
# 最後數一次：images/ 裡的 PNG 要正好等於 figures.json 的圖＋表＋本機資產數，少一張就是 FAIL（cp 或清檔出了問題）
expected=$(python3 -c "import json,sys; s=json.load(open(sys.argv[1])); print(len(s.get('figures',[]))+len(s.get('tables',[]))+len(s.get('assets',[])))" "$PUB/figures.json")
actual=$(find "$IMG" -maxdepth 1 -name '*.png' | wc -l | tr -d ' ')
echo "== images in $IMG: $actual of $expected  (FAILs: $fail)"
[ "$actual" = "$expected" ] || { echo "  images/ holds $actual PNGs, figures.json expects $expected"; fail=$((fail+1)); }
[ "$fail" = "0" ]
