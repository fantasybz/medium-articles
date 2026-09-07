#!/usr/bin/env bash
# research/scripts/mermaid_check.sh — 用 gstack browse（headless）算繪一張 Mermaid 圖並依 MERMAID.md 檢查
#
#   research/scripts/mermaid_check.sh fig.mmd            # 印出尺寸與判定，並輸出 fig.png（2x）與 fig.svg
#   research/scripts/mermaid_check.sh fig.mmd out/name   # 指定輸出前綴
#
# 規則來源：MERMAID.md 第一節。寬 500–900 CSS px（讀 svg 的 viewBox，不讀 bounding rect—mermaid 會用 max-width 把 svg 縮進容器）、
# 高／寬 0.5–1.5、節點 ≤ 12；區間兩端都算合格。判定在最下面的 python 區塊，數字也在那裡命名。
#
# 不需要安裝 mermaid-cli：mermaid 從 jsdelivr 載入（要有網路），瀏覽器是 gstack 已經有的那顆。
# 版本釘在 MERMAID_VERSION：版面尺寸來自 mermaid 的排版演算法，PASS／FAIL 會跟著版本漂；
# 目前 research/ 下所有 PASS 是 11.17.2 算出來的（2026-09-07 jsdelivr 對 mermaid@11 解析到的版本）。
# 升版要把全部的圖重跑一遍（mermaid_check_all.sh），不要只改數字。
#
# 注意：browse daemon 若正處於 --headed 且匯入了 cookie，會拒絕在 file:// 頁面執行 JS；此時先 disconnect
# 讓它以 headless 重開（_common.sh 的 prepare_headless_viewport 會做）。但 collect.sh 跑的時候不能這樣做——
# 那會把它的登入 session 踢掉，所以看到 .context/collect.lock 就退出 75。
set -euo pipefail
MMD="${1:?usage: mermaid_check.sh <fig.mmd> [out-prefix]}"
OUTP="${2:-${MMD%.mmd}}"
HERE="$(cd "$(dirname "$0")" && pwd)"
. "$HERE/_common.sh"        # ROOT、EX_*、BROWSE、prepare_headless_viewport
MERMAID_VERSION=11.17.2
[ -f "$MMD" ] || { echo "no such file: $MMD" >&2; exit "$EX_USAGE"; }
W="$ROOT/.context/mermaid"; mkdir -p "$W"
HTML="$W/$(basename "$OUTP").html"

python3 - "$MMD" "$HTML" "$MERMAID_VERSION" <<'EOF'
import html, sys
src = open(sys.argv[1]).read()
ver = sys.argv[3]
if not src.lstrip().startswith('---'):
    sys.exit("no frontmatter config: every figure starts with the MERMAID.md `---\\nconfig:` block")
page = f'''<!doctype html><html><head><meta charset="utf-8">
<style>body{{margin:0;background:#fff}} #wrap{{display:inline-block;padding:16px}} .mermaid svg{{max-width:none!important}}</style></head>
<body><div id="wrap"><div class="mermaid">{html.escape(src)}</div></div>
<script type="module">
window.__ready=false; window.__err=null;
import mermaid from "https://cdn.jsdelivr.net/npm/mermaid@{ver}/dist/mermaid.esm.min.mjs";
// 字型由這裡統一注入：frontmatter 的 themeVariables.fontFamily 會被 mermaid 11 忽略（CSS 仍是 trebuchet ms），
// 而量測用 mermaid 自己的 CSS 字型、算繪用容器繼承的字型，兩邊不一致就會裁字。initialize 走的是同一條路。
mermaid.initialize({{ startOnLoad: false, themeVariables: {{ fontFamily: "Noto Sans TC, PingFang TC, Helvetica Neue, Arial, sans-serif" }} }});
try {{ await mermaid.run({{querySelector:'.mermaid'}}); window.__ready=true; }} catch(e) {{ window.__err=String(e && (e.message||e.str||JSON.stringify(e))||e); }}
</script></body></html>'''
open(sys.argv[2], 'w').write(page)
EOF

prepare_headless_viewport
"$BROWSE" load-html "$HTML" >/dev/null
# 等到 svg 出現或 15 秒；不靠頁面裡的旗標判斷成功
INFO=$("$BROWSE" js "new Promise(res=>{const t0=Date.now();const tick=()=>{const s=document.querySelector('svg');const ready=s&&(s.getAttribute('viewBox')||'').split(' ').map(Number)[2]>0;if(ready||Date.now()-t0>15000||window.__err){if(!s||!ready)return res(JSON.stringify({err:window.__err||(s?'svg has no viewBox after 15s':'no svg after 15s')}));const vb=(s.getAttribute('viewBox')||'0 0 0 0').split(' ').map(Number);const lbl=s.querySelector('.nodeLabel, .label, text');return res(JSON.stringify({err:s.querySelector('.error-icon')?'mermaid rendered its error diagram (syntax error)':null,w:Math.round(vb[2]),h:Math.round(vb[3]),nodes:s.querySelectorAll('.node').length,fontSize:lbl?getComputedStyle(lbl).fontSize:null}))}setTimeout(tick,300)};tick()})")
"$BROWSE" screenshot "$OUTP.png" --selector '#wrap' >/dev/null
"$BROWSE" js "document.querySelector('svg').outerHTML" --raw --out "$OUTP.svg" >/dev/null 2>&1 || true

python3 - "$INFO" "$OUTP" <<'EOF'
import json, sys
out = sys.argv[2]
try: info = json.loads(sys.argv[1])
except ValueError:
    # browse 回的不是我們的 JSON（daemon 的錯誤字串之類）：一樣是算繪失敗，不要丟 traceback
    print("RENDER ERROR: browse returned no measurement:", sys.argv[1][:200]); sys.exit(2)
# MERMAID.md 第一節的數字。每個區間兩端都含：寬 500 與 900、高／寬 0.5 與 1.5、12 個節點都 PASS。
W_MIN, W_MAX = 500, 900          # CSS px，svg viewBox 的寬
ASPECT_MIN, ASPECT_MAX = 0.5, 1.5  # 高／寬
NODES_MAX = 12
if info.get('err'):
    print("RENDER ERROR:", info['err']); sys.exit(2)
w, h, n = info['w'], info['h'], info.get('nodes', 0)
if w <= 0 or h <= 0:
    # 空的 viewBox 是算繪失敗，不是一張「aspect 0.00」的圖
    print(f"RENDER ERROR: svg viewBox is {w}x{h}"); sys.exit(2)
aspect = h / w
problems = []
if w > W_MAX: problems.append(f"width {w}px > {W_MAX} (text will be < 12px at 700px column)")
if w < W_MIN: problems.append(f"width {w}px < {W_MIN} (will be upscaled and look coarse; use two columns or LR)")
if aspect > ASPECT_MAX: problems.append(f"aspect {aspect:.2f} > {ASPECT_MAX} (too tall; split or go two-column)")
if aspect < ASPECT_MIN: problems.append(f"aspect {aspect:.2f} < {ASPECT_MIN} (strip; go TB or stack)")
if n > NODES_MAX: problems.append(f"{n} nodes > {NODES_MAX} (split the figure)")
print(f"{out}.png  {w}x{h} css px, aspect {aspect:.2f}, nodes {n}, font {info.get('fontSize')}")
print("PASS" if not problems else "FAIL:\n  - " + "\n  - ".join(problems))
sys.exit(0 if not problems else 1)
EOF
