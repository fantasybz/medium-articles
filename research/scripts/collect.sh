#!/usr/bin/env bash
# research/scripts/collect.sh — 把這個月的原始訊號抓進 .context/research/<YYYY-MM>/
#
#   research/scripts/collect.sh all              # X + Facebook + LinkedIn + Medium + Notion
#   research/scripts/collect.sh x facebook       # 只跑指定來源
#   SINCE=2026-08-01 research/scripts/collect.sh x
#
# 這支腳本是把 2026-09-05 第一次人工跑通的指令整理成一份；它還沒有以「單一腳本」
# 的形式從頭到尾跑過一次，第一次跑請一段一段看輸出。
#
# 前置：macOS、Chrome 的 Default profile 已登入 X / Facebook / LinkedIn / Medium、
# gstack browse 已 build（~/.claude/skills/gstack/browse/dist/browse）。
#
# 為什麼是 headed：Cloudflare 會擋 headless Chromium（Medium 回 403、X 顯示錯誤頁），
# 所以每一次呼叫都帶 --headed，而且要先 disconnect 讓 daemon 重開。
#
# Cookie 的處理跟 tools/medium_draft.sh 一樣：解密到 0700 的暫存目錄、匯入完立刻刪。
# 匯出的檔就是一份可用的登入 session，永遠不要留在 repo 或固定的 /tmp 路徑。
#
# 已知會壞的地方：每個平台的 DOM 都會變，extract_*.js 裡的 selector 是 2026-09 的版本。
# 抓到 0 筆時先看 selector，不要先懷疑登入。

set -euo pipefail

HERE="$(cd "$(dirname "$0")" && pwd)"
ROOT="$(cd "$HERE/../.." && pwd)"
BROWSE="$HOME/.claude/skills/gstack/browse/dist/browse"
[ -x "$BROWSE" ] || { echo "browse not built: $BROWSE" >&2; exit 69; }

MONTH="${MONTH:-$(date +%Y-%m)}"
SINCE="${SINCE:-$(date -v-45d +%Y-%m-%d)}"           # X 搜尋的起點，預設往回 45 天
PROFILE="${PROFILE:-Default}"                        # Chrome profile；換帳號改這裡
OUT="$ROOT/.context/research/$MONTH"
mkdir -p "$OUT"
cd "$ROOT"

B() { "$BROWSE" --headed "$@"; }
sleep_js() { B js "new Promise(r=>setTimeout(r,$1)).then(()=>'ok')" >/dev/null 2>&1 || true; }
scroll() { B js "window.scrollBy(0, ${1:-2500}); new Promise(r=>setTimeout(r,${2:-2000})).then(()=>window.scrollY)" >/dev/null 2>&1 || true; }
step() { printf '\n== %s\n' "$*" >&2; }

# import_cookies <domain> <url-to-open-first> [--subdomains]
# browse 只接受「網域是目前頁面網域後綴」的 cookie，所以要先站到那個網域上再匯入。
import_cookies() {
  local dom="$1" url="$2" extra="${3:-}"
  local W; W="$(mktemp -d)"; chmod 700 "$W"
  python3 tools/chrome_cookies.py "$dom" --profile "$PROFILE" $extra --out "$W/c.json" >/dev/null
  B goto "$url" >/dev/null 2>&1 || true
  B cookie-import "$W/c.json" | tail -1
  rm -rf "$W"
}

# collect <extract.js> <out.json> <scrolls> [scroll-px] [wait-ms]
collect() {
  local js="$1" out="$2" n="$3" px="${4:-2500}" ms="${5:-2000}" total=0
  for _ in $(seq 1 "$n"); do
    B eval "$js" > "$OUT/_batch.json" 2>/dev/null || true
    total=$(python3 "$HERE/merge.py" "$out" "$OUT/_batch.json")
    scroll "$px" "$ms"
  done
  echo "  $(basename "$out"): $total"
}

xq() { python3 -c "import urllib.parse,sys;print('https://x.com/search?f=top&src=typed_query&q='+urllib.parse.quote(sys.argv[1]))" "$1"; }

do_x() {
  step "X: import cookies"
  import_cookies x.com https://x.com
  step "X: following timeline"
  B goto https://x.com/home >/dev/null 2>&1; sleep_js 2500
  B js "(()=>{const t=[...document.querySelectorAll('[role=\"tab\"]')].find(t=>/正在跟隨|Following/.test(t.innerText));if(t)t.click();return 'ok'})()" >/dev/null 2>&1 || true
  sleep_js 2500
  collect "$HERE/extract_tweets.js" "$OUT/x_following.json" 30 2500 1800
  step "X: bookmarks"
  B goto https://x.com/i/bookmarks >/dev/null 2>&1; sleep_js 3000
  collect "$HERE/extract_tweets.js" "$OUT/x_bookmarks.json" 25 2500 1800
  step "X: top posts from followed accounts since $SINCE"
  local q
  for q in \
    "filter:follows since:$SINCE min_faves:300 -filter:replies" \
    "filter:follows since:$SINCE min_faves:100 -filter:replies" \
    "filter:follows since:$SINCE (agent OR agents OR agentic) min_faves:50 -filter:replies" \
    "filter:follows since:$SINCE (harness OR AGENTS.md OR \"context engineering\" OR MCP OR \"Claude Code\" OR Codex OR Copilot OR Cursor) min_faves:30 -filter:replies" \
    "filter:follows since:$SINCE (eval OR evals OR benchmark OR SWE-bench OR \"code review\") min_faves:30 -filter:replies" \
    "filter:follows since:$SINCE (Kubernetes OR platform OR SRE OR observability OR testing OR QA) min_faves:30 -filter:replies" \
    "filter:follows since:$SINCE (security OR \"prompt injection\" OR sandbox OR permissions) min_faves:30 -filter:replies" \
    "filter:follows since:$SINCE (engineering manager OR org OR team OR hiring OR junior OR productivity) min_faves:50 -filter:replies"; do
    B goto "$(xq "$q")" >/dev/null 2>&1; sleep_js 3500
    collect "$HERE/extract_tweets.js" "$OUT/x_search_top.json" 10 2500 1800
  done
  step "X: following list（每月抓一次就好，變動不大）"
  B goto https://x.com/fantasybz/following >/dev/null 2>&1; sleep_js 3000
  local prev=0 same=0 n
  for _ in $(seq 1 60); do
    B eval "$HERE/extract_users.js" > "$OUT/_batch.json" 2>/dev/null || true
    n=$(python3 "$HERE/merge_users.py" "$OUT/x_following_users.json" "$OUT/_batch.json")
    if [ "$n" = "$prev" ]; then same=$((same+1)); else same=0; fi; prev=$n
    [ "$same" -ge 4 ] && break
    scroll 2000 1500
  done
  echo "  x_following_users.json: $n"
}

# 社團清單取自 2026-09 那次的 groups/joins；新加入的社團要手動補進來。
FB_GROUPS="${FB_GROUPS:-teddy.tw DevOpsTaiwan backendtw 179345672472 AgileNeihu dddesigntw 1224997379198346 690000220033563 4260325997553989 1381920156575940 153996481787947 twinkleai 1566209724424032 849593587436598}"
FB_PAGE="${FB_PAGE:-KochiLearningJourney}"      # 粉絲團 榮民叔叔的藏書筆記
FB_ME="${FB_ME:-kochi.chuang}"

do_facebook() {
  step "Facebook: import cookies"
  import_cookies facebook.com https://www.facebook.com/ --subdomains
  step "Facebook: groups"
  local g
  for g in $FB_GROUPS; do
    B goto "https://www.facebook.com/groups/$g/" >/dev/null 2>&1; sleep_js 5000
    for _ in $(seq 1 7); do
      B eval "$HERE/extract_fb2.js" > "$OUT/_batch.json" 2>/dev/null || true
      python3 - "$OUT/facebook_groups.json" "$OUT/_batch.json" "group:$g" <<'EOF'
import json, sys
path, add, tag = sys.argv[1:4]
try: cur = {t['link']: t for t in json.load(open(path))}
except Exception: cur = {}
try: new = json.loads(open(add).read())
except Exception: new = []
for t in new:
    t['source'] = tag; cur.setdefault(t['link'], t)
json.dump(list(cur.values()), open(path, 'w'), ensure_ascii=False, indent=1)
EOF
      scroll 2500 2200
    done
    echo "  $g -> $(python3 -c "import json;print(len(json.load(open('$OUT/facebook_groups.json'))))")"
  done
  step "Facebook: own posts + fan page（用作者名切文字，不靠 selector）"
  local who url
  for who in "榮民叔叔的藏書筆記|https://www.facebook.com/$FB_PAGE|fan_page" "莊軻齊|https://www.facebook.com/$FB_ME/|own_profile"; do
    IFS='|' read -r author url tag <<<"$who"
    B goto "$url" >/dev/null 2>&1; sleep_js 5000
    for _ in $(seq 1 15); do
      B js "window.__FB_AUTHOR=$(python3 -c 'import json,sys;print(json.dumps(sys.argv[1]))' "$author");'ok'" >/dev/null 2>&1 || true
      B eval "$HERE/extract_fb_timeline.js" > "$OUT/_batch.json" 2>/dev/null || true
      python3 - "$OUT/facebook_own.json" "$OUT/_batch.json" "$tag" <<'EOF'
import json, sys
path, add, tag = sys.argv[1:4]
try: cur = {t['link']: t for t in json.load(open(path))}
except Exception: cur = {}
try: new = json.loads(open(add).read())
except Exception: new = []
for t in new:
    t['source'] = tag; cur.setdefault(t['link'], t)
json.dump(list(cur.values()), open(path, 'w'), ensure_ascii=False, indent=1)
EOF
      scroll 2500 2500
    done
  done
  echo "  facebook_own.json: $(python3 -c "import json;print(len(json.load(open('$OUT/facebook_own.json'))))")"
}

do_linkedin() {
  step "LinkedIn: import cookies（li_at 在 .www.linkedin.com，所以要 --subdomains）"
  import_cookies linkedin.com https://www.linkedin.com/ --subdomains
  step "LinkedIn: feed（2026-09 只抓到 8 篇，selector 待改；saved posts 比較有價值）"
  B goto https://www.linkedin.com/feed/ >/dev/null 2>&1; sleep_js 5000
  collect "$HERE/extract_li2.js" "$OUT/linkedin_feed.json" 30 2200 2200
  step "LinkedIn: saved posts"
  B goto https://www.linkedin.com/my-items/saved-posts/ >/dev/null 2>&1; sleep_js 5000
  for _ in $(seq 1 8); do scroll 2500 2000; done
  B js "(document.querySelector('main')||document.body).innerText" > "$OUT/linkedin_saved.txt" 2>/dev/null || true
  echo "  linkedin_saved.txt: $(wc -c < "$OUT/linkedin_saved.txt") bytes"
}

do_medium() {
  step "Medium: import cookies"
  import_cookies medium.com https://medium.com
  step "Medium: stats（回饋迴圈的輸入：每篇 presentations / views / reads）"
  B goto "https://medium.com/me/stats?publishedAt=DESC" >/dev/null 2>&1; sleep_js 5000
  local prev=0 same=0 len
  for _ in $(seq 1 30); do
    B js "(()=>{const b=[...document.querySelectorAll('button')].find(b=>/show more|load more|顯示更多/i.test(b.innerText));if(b){b.click();return 'clicked'}window.scrollTo(0,document.body.scrollHeight);return 'scrolled'})()" >/dev/null 2>&1 || true
    sleep_js 2000
    len=$(B js "(document.querySelector('main')||document.body).innerText.length" 2>/dev/null || echo 0)
    if [ "$len" = "$prev" ]; then same=$((same+1)); else same=0; fi; prev=$len
    [ "$same" -ge 4 ] && break
  done
  B js "(document.querySelector('main')||document.body).innerText" > "$OUT/medium_stats.txt" 2>/dev/null || true
  echo "  medium_stats.txt: $(grep -c 'View story' "$OUT/medium_stats.txt") stories"
  step "Medium: profile listing"
  B goto https://medium.com/@fantasybz >/dev/null 2>&1; sleep_js 4000
  collect "$HERE/extract_medium.js" "$OUT/medium_articles.json" 12 3000 1800
}

# Notion：桌面版 app 的 cookie（Electron，同 Chromium 加密），第一次讀 Keychain 會跳授權視窗。
# token_v2 掛在 app.notion.com；browse 只收「網域是目前頁面後綴」的 cookie，所以分兩批匯入。
NOTION_PAGES="${NOTION_PAGES:-30}"     # 抓最近編輯的前 N 頁內文
do_notion() {
  step "Notion: decrypt desktop-app cookies（Keychain 視窗請按允許）"
  local W; W="$(mktemp -d)"; chmod 700 "$W"
  python3 "$HERE/notion_cookies.py" notion.com "$W/all.json" >/dev/null
  python3 - "$W" <<'EOF'
import json, sys, os
W = sys.argv[1]; cs = json.load(open(f"{W}/all.json"))
groups = {'root': ('.notion.com', 'notion.com', 'www.notion.com'), 'app': ('app.notion.com', '.app.notion.com')}
for name, doms in groups.items():           # msgstore-*.app.notion.com 的 AWSALB cookie 會讓整批被拒，直接丟掉
    grp = [c for c in cs if c['domain'] in doms]
    fd = os.open(f"{W}/{name}.json", os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600); os.write(fd, json.dumps(grp).encode()); os.close(fd)
EOF
  B goto https://www.notion.com/ >/dev/null 2>&1
  B cookie-import "$W/root.json" | tail -1
  B goto https://app.notion.com/ >/dev/null 2>&1; sleep_js 3000
  B cookie-import "$W/app.json" | tail -1
  rm -rf "$W"
  step "Notion: 最近編輯的 100 頁（內部 /api/v3/search）"
  B goto https://app.notion.com/ >/dev/null 2>&1; sleep_js 8000
  B eval "$HERE/notion_search.js" > "$OUT/notion_pages.json"
  python3 -c "import json,sys; d=json.load(open(sys.argv[1])); print('  spaceId', d['spaceId'], 'pages', len(d['pages']))" "$OUT/notion_pages.json"
  step "Notion: 前 $NOTION_PAGES 頁的內文（loadPageChunk）"
  local id
  python3 -c "import json,sys; [print(p['id']) for p in json.load(open(sys.argv[1]))['pages'] if p['type']=='page'][:int(sys.argv[2])]" "$OUT/notion_pages.json" "$NOTION_PAGES" | while read -r id; do
    B js "window.__NOTION_PAGE_ID='$id';'ok'" >/dev/null 2>&1 || true
    B eval "$HERE/notion_chunk.js" > "$OUT/_batch.json" 2>/dev/null || true
    python3 - "$OUT/notion_pages_content.json" "$OUT/_batch.json" "$id" <<'EOF'
import json, sys
path, add, pid = sys.argv[1:4]
try: cur = json.load(open(path))
except Exception: cur = {}
try: d = json.loads(open(add).read())
except Exception: d = {'text': ''}
cur[pid] = d
json.dump(cur, open(path, 'w'), ensure_ascii=False, indent=1)
EOF
  done
  echo "  notion_pages_content.json: $(python3 -c "import json,sys; print(len(json.load(open(sys.argv[1]))))" "$OUT/notion_pages_content.json") pages"
}

main() {
  local targets=("$@"); [ ${#targets[@]} -eq 0 ] && targets=(all)
  [[ " ${targets[*]} " == *" all "* ]] && targets=(x facebook linkedin medium notion)
  step "starting headed browser (SINCE=$SINCE, OUT=$OUT)"
  "$BROWSE" disconnect >/dev/null 2>&1 || true
  local t
  for t in "${targets[@]}"; do
    case "$t" in
      x) do_x ;; facebook) do_facebook ;; linkedin) do_linkedin ;; medium) do_medium ;; notion) do_notion ;;
      *) echo "unknown source: $t (x|facebook|linkedin|medium|notion|all)" >&2; exit 64 ;;
    esac
  done
  rm -f "$OUT/_batch.json"
  step "done → $OUT"
  ls -la "$OUT"
}
main "$@"
