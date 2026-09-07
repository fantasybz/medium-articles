#!/usr/bin/env bash
# research/scripts/mermaid_check.sh — 用 gstack browse（headless）算繪一張 Mermaid 圖並依 MERMAID.md 檢查
#
#   research/scripts/mermaid_check.sh fig.mmd            # 印出尺寸與判定，並輸出 fig.png（2x）與 fig.svg
#   research/scripts/mermaid_check.sh fig.mmd out/name   # 指定輸出前綴
#
# 規則來源：MERMAID.md 第一節。寬 500–900 CSS px（讀 svg 的 viewBox，不讀 bounding rect—mermaid 會用 max-width 把 svg 縮進容器）、高／寬 0.5–1.5、節點 ≤ 12。
# 不需要安裝 mermaid-cli：mermaid 11 從 jsdelivr 載入（要有網路），瀏覽器是 gstack 已經有的那顆。
#
# 注意：browse daemon 若正處於 --headed 且匯入了 cookie，會拒絕在 file:// 頁面執行 JS；
# 此時先 `browse disconnect` 讓它以 headless 重開（本腳本會自動做）。
set -euo pipefail
MMD="${1:?usage: mermaid_check.sh <fig.mmd> [out-prefix]}"
OUTP="${2:-${MMD%.mmd}}"
B="$HOME/.claude/skills/gstack/browse/dist/browse"
[ -x "$B" ] || { echo "browse not built: $B" >&2; exit 69; }
ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
W="$ROOT/.context/mermaid"; mkdir -p "$W"
HTML="$W/$(basename "$OUTP").html"

python3 - "$MMD" "$HTML" <<'EOF'
import html, sys
src = open(sys.argv[1]).read()
if not src.lstrip().startswith('---'):
    sys.exit("no frontmatter config: every figure starts with the MERMAID.md `---\\nconfig:` block")
page = f'''<!doctype html><html><head><meta charset="utf-8">
<style>body{{margin:0;background:#fff}} #wrap{{display:inline-block;padding:16px}} .mermaid svg{{max-width:none!important}}</style></head>
<body><div id="wrap"><div class="mermaid">{html.escape(src)}</div></div>
<script type="module">
window.__ready=false; window.__err=null;
import mermaid from "https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.esm.min.mjs";
// 字型由這裡統一注入：frontmatter 的 themeVariables.fontFamily 會被 mermaid 11 忽略（CSS 仍是 trebuchet ms），
// 而量測用 mermaid 自己的 CSS 字型、算繪用容器繼承的字型，兩邊不一致就會裁字。initialize 走的是同一條路。
mermaid.initialize({{ startOnLoad: false, themeVariables: {{ fontFamily: "Noto Sans TC, PingFang TC, Helvetica Neue, Arial, sans-serif" }} }});
try {{ await mermaid.run({{querySelector:'.mermaid'}}); window.__ready=true; }} catch(e) {{ window.__err=String(e && (e.message||e.str||JSON.stringify(e))||e); }}
</script></body></html>'''
open(sys.argv[2], 'w').write(page)
EOF

if "$B" status 2>/dev/null | grep -q "Mode: headed"; then "$B" disconnect >/dev/null 2>&1 || true; fi
# `viewport --scale` 會重建 browser context 並重播上一個 load-html；緊接著再 load-html 會撞在一起，
# mermaid 在被換掉一半的 DOM 上跑就會丟 null error。所以只在需要時改，改完等一下再載入。
CUR=$("$B" js "window.innerWidth+'@'+window.devicePixelRatio" 2>/dev/null || echo "")
if [ "$CUR" != "1400@2" ]; then "$B" viewport 1400x1400 --scale 2 >/dev/null 2>&1 || true; "$B" js "new Promise(r=>setTimeout(r,1500)).then(()=>'ok')" >/dev/null 2>&1 || true; fi
"$B" load-html "$HTML" >/dev/null
# 等到 svg 出現或 15 秒；不靠頁面裡的旗標判斷成功
INFO=$("$B" js "new Promise(res=>{const t0=Date.now();const tick=()=>{const s=document.querySelector('svg');const ready=s&&(s.getAttribute('viewBox')||'').split(' ').map(Number)[2]>0;if(ready||Date.now()-t0>15000||window.__err){if(!s||!ready)return res(JSON.stringify({err:window.__err||(s?'svg has no viewBox after 15s':'no svg after 15s')}));const vb=(s.getAttribute('viewBox')||'0 0 0 0').split(' ').map(Number);const lbl=s.querySelector('.nodeLabel, .label, text');return res(JSON.stringify({err:s.querySelector('.error-icon')?'mermaid rendered its error diagram (syntax error)':null,w:Math.round(vb[2]),h:Math.round(vb[3]),nodes:s.querySelectorAll('.node').length,fontSize:lbl?getComputedStyle(lbl).fontSize:null}))}setTimeout(tick,300)};tick()})")
"$B" screenshot "$OUTP.png" --selector '#wrap' >/dev/null
"$B" js "document.querySelector('svg').outerHTML" --raw --out "$OUTP.svg" >/dev/null 2>&1 || true

python3 - "$INFO" "$OUTP" <<'EOF'
import json, sys
info = json.loads(sys.argv[1]); out = sys.argv[2]
if info.get('err'):
    print("RENDER ERROR:", info['err']); sys.exit(2)
w, h, n = info['w'], info['h'], info.get('nodes', 0)
aspect = h / w if w else 0
problems = []
if w > 900: problems.append(f"width {w}px > 900 (text will be < 12px at 700px column)")
if w < 500: problems.append(f"width {w}px < 500 (will be upscaled and look coarse; use two columns or LR)")
if aspect > 1.5: problems.append(f"aspect {aspect:.2f} > 1.5 (too tall; split or go two-column)")
if aspect < 0.5: problems.append(f"aspect {aspect:.2f} < 0.5 (strip; go TB or stack)")
if n > 12: problems.append(f"{n} nodes > 12 (split the figure)")
print(f"{out}.png  {w}x{h} css px, aspect {aspect:.2f}, nodes {n}, font {info.get('fontSize')}")
print("PASS" if not problems else "FAIL:\n  - " + "\n  - ".join(problems))
sys.exit(0 if not problems else 1)
EOF
