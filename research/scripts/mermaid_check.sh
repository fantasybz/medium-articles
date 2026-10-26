#!/usr/bin/env bash
# research/scripts/mermaid_check.sh — 用 gstack browse（headless）算繪一張 Mermaid 圖並依 MERMAID.md 檢查
#
#   research/scripts/mermaid_check.sh fig.mmd            # 印出尺寸與判定，並輸出 fig.png（2x）與 fig.svg
#   research/scripts/mermaid_check.sh fig.mmd out/name   # 指定輸出前綴
#
# 規則來源：MERMAID.md 第一節。寬 500–900 CSS px（讀 svg 的 viewBox，不讀 bounding rect）、
# 高／寬 0.5–1.5、節點 ≤ 12；區間兩端都算合格。判定在最下面的 python 區塊，數字也在那裡命名。
#
# 截圖尺寸：mermaid 11 輸出的 svg 是 width="100%" 加 style="max-width:<viewBox 寬>px"。頁面 CSS 拿掉 max-width 後，
# svg 在 inline-block 的 #wrap 裡沒有可解析的百分比寬度，瀏覽器退回替換元素的預設 300 CSS px，於是每張圖的 PNG 都是
# (300+16×2)×2 = 664 px 寬、文字只有一半解析度，而 viewBox 的檢查照樣 PASS（2026-10-26 /ship 的 Red Team 從可靠度篇
# 的 PNG 看出來：10/24 以別的方法算繪的 diagram-02 是 1468 px 寬，重繪後剩 664）。所以量完 viewBox 之後，先把 svg 的
# width／height 屬性設成 viewBox 的寬高再截圖，並核對 #wrap 的實際寬度與 PNG 的畫素寬度：對不上就是算繪失敗，不印 PASS。
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
WRAP_PAD=16                 # #wrap 的內距（CSS px）；HTML 與下面的尺寸核對共用這個數字
[ -f "$MMD" ] || { echo "no such file: $MMD" >&2; exit "$EX_USAGE"; }
W="$ROOT/.context/mermaid"; mkdir -p "$W"
HTML="$W/$(basename "$OUTP").html"

python3 - "$MMD" "$HTML" "$MERMAID_VERSION" "$WRAP_PAD" <<'EOF'
import html, sys
src = open(sys.argv[1]).read()
ver = sys.argv[3]
pad = int(sys.argv[4])
if not src.lstrip().startswith('---'):
    sys.exit("no frontmatter config: every figure starts with the MERMAID.md `---\\nconfig:` block")
page = f'''<!doctype html><html><head><meta charset="utf-8">
<style>body{{margin:0;background:#fff}} #wrap{{display:inline-block;padding:{pad}px}} .mermaid svg{{max-width:none!important}}</style></head>
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
INFO=$("$BROWSE" js "new Promise(res=>{const t0=Date.now();const tick=()=>{const s=document.querySelector('svg');const ready=s&&(s.getAttribute('viewBox')||'').split(' ').map(Number)[2]>0;if(ready||Date.now()-t0>15000||window.__err){if(!s||!ready)return res(JSON.stringify({err:window.__err||(s?'svg has no viewBox after 15s':'no svg after 15s')}));const vb=(s.getAttribute('viewBox')||'0 0 0 0').split(' ').map(Number);s.setAttribute('width',vb[2]);s.setAttribute('height',vb[3]);const wr=document.querySelector('#wrap').getBoundingClientRect();const lbl=s.querySelector('.nodeLabel, .label, text');return res(JSON.stringify({err:s.querySelector('.error-icon')?'mermaid rendered its error diagram (syntax error)':null,w:Math.round(vb[2]),h:Math.round(vb[3]),wrapW:Math.round(wr.width),wrapH:Math.round(wr.height),dpr:window.devicePixelRatio,nodes:s.querySelectorAll('.node').length,fontSize:lbl?getComputedStyle(lbl).fontSize:null}))}setTimeout(tick,300)};tick()})")
"$BROWSE" screenshot "$OUTP.png" --selector '#wrap' >/dev/null
"$BROWSE" js "document.querySelector('svg').outerHTML" --raw --out "$OUTP.svg" >/dev/null 2>&1 || true

python3 - "$INFO" "$OUTP" "$WRAP_PAD" "$HEADLESS_SCALE" <<'EOF'
import json, struct, sys
out = sys.argv[2]
pad, scale = int(sys.argv[3]), int(sys.argv[4])
try: info = json.loads(sys.argv[1])
except ValueError:
    # browse 回的不是我們的 JSON（daemon 的錯誤字串之類）：一樣是算繪失敗，不要丟 traceback
    print("RENDER ERROR: browse returned no measurement:", sys.argv[1][:200]); sys.exit(2)
# MERMAID.md 第一節的數字。每個區間兩端都含：寬 500 與 900、高／寬 0.5 與 1.5、12 個節點都 PASS。
W_MIN, W_MAX = 500, 900          # CSS px，svg viewBox 的寬
ASPECT_MIN, ASPECT_MAX = 0.5, 1.5  # 高／寬
NODES_MAX = 12
WRAP_TOL_PX = 2                  # #wrap 寬 vs viewBox 寬＋兩邊內距：getBoundingClientRect 與 viewBox 小數的取整
PNG_TOL_PX = 4                   # PNG 寬 vs scale × #wrap 寬：2x 截圖的畫素取整
if info.get('err'):
    print("RENDER ERROR:", info['err']); sys.exit(2)
w, h, n = info['w'], info['h'], info.get('nodes', 0)
if w <= 0 or h <= 0:
    # 空的 viewBox 是算繪失敗，不是一張「aspect 0.00」的圖
    print(f"RENDER ERROR: svg viewBox is {w}x{h}"); sys.exit(2)
# 截圖尺寸的核對（見檔頭）：#wrap 要是 svg 的 viewBox 寬加兩邊內距，PNG 要是 #wrap 的 scale 倍。
# 退回 300px 的 svg 會在第一關被擋下；daemon 不是 2x 時在第二關。兩種都算算繪失敗。
if 'wrapW' not in info:
    print("RENDER ERROR: browse measurement has no #wrap width (older daemon or script?)"); sys.exit(2)
wrap_w = int(info['wrapW'])
if abs(wrap_w - (w + 2 * pad)) > WRAP_TOL_PX:
    print(f"RENDER ERROR: svg drawn at {max(wrap_w - 2 * pad, 0)}px wide, not its viewBox width {w}px (fallback-width capture)"); sys.exit(2)
try:
    with open(out + '.png', 'rb') as f: head = f.read(24)
except OSError as e:
    print(f"RENDER ERROR: no screenshot: {e}"); sys.exit(2)
if head[:8] != b'\x89PNG\r\n\x1a\n' or len(head) < 24:
    print("RENDER ERROR: screenshot is not a PNG"); sys.exit(2)
png_w, png_h = struct.unpack('>II', head[16:24])
if abs(png_w - scale * wrap_w) > PNG_TOL_PX:
    print(f"RENDER ERROR: png is {png_w}px wide, expected {scale}x of the {wrap_w}px #wrap (dpr {info.get('dpr')})"); sys.exit(2)
aspect = h / w
problems = []
if w > W_MAX: problems.append(f"width {w}px > {W_MAX} (text will be < 12px at 700px column)")
if w < W_MIN: problems.append(f"width {w}px < {W_MIN} (will be upscaled and look coarse; use two columns or LR)")
if aspect > ASPECT_MAX: problems.append(f"aspect {aspect:.2f} > {ASPECT_MAX} (too tall; split or go two-column)")
if aspect < ASPECT_MIN: problems.append(f"aspect {aspect:.2f} < {ASPECT_MIN} (strip; go TB or stack)")
if n > NODES_MAX: problems.append(f"{n} nodes > {NODES_MAX} (split the figure)")
print(f"{out}.png  {w}x{h} css px (png {png_w}x{png_h}, {scale}x), aspect {aspect:.2f}, nodes {n}, font {info.get('fontSize')}")
print("PASS" if not problems else "FAIL:\n  - " + "\n  - ".join(problems))
sys.exit(0 if not problems else 1)
EOF
