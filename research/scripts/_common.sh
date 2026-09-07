#!/usr/bin/env bash
# research/scripts/_common.sh — 給 browse 驅動腳本 source 的共用片段；不要直接執行。
#
#   HERE="$(cd "$(dirname "$0")" && pwd)"
#   . "$HERE/_common.sh"
#
# 提供：ROOT、EX_* 離開碼、BROWSE（repo 內優先、再退到 $HOME）、collect.sh 的鎖、
# headless 算繪前的 viewport 準備。這幾段原本各自散在 collect.sh / mermaid_check.sh /
# render_images.sh 裡，改一處漏一處，所以收攏到這裡。呼叫端自己決定要不要 set -e。

# 呼叫端可先設 ROOT；沒設就從這個檔案的位置往上兩層（research/scripts/ → repo 根）。
_COMMON_HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="${ROOT:-$(cd "$_COMMON_HERE/../.." && pwd)}"

# sysexits(3)，跟 tools/medium_draft.sh 同一組
EX_USAGE=64        # 參數錯
EX_UNAVAILABLE=69  # 少了外部程式（browse、codex）
EX_TEMPFAIL=75     # 暫時不能跑（collect.sh 正持有瀏覽器），稍後重試

# browse：repo 內的 .claude/skills 優先，再退到 $HOME（同 tools/medium_draft.sh）
BROWSE="$ROOT/.claude/skills/gstack/browse/dist/browse"
[ -x "$BROWSE" ] || BROWSE="$HOME/.claude/skills/gstack/browse/dist/browse"
[ -x "$BROWSE" ] || { echo "browse not found; run gstack setup" >&2; exit "$EX_UNAVAILABLE"; }

# collect.sh 跑的時候 browse daemon 是 headed 且帶著登入 cookie；別的腳本若在這時
# disconnect 它，登入 session 就沒了，收集會中途死掉。所以 collect.sh 用 mkdir 取鎖
# （mkdir 是原子的），其餘腳本看到鎖就退出 75：不是失敗，是「等它跑完再來」。
COLLECT_LOCK="$ROOT/.context/collect.lock"

# 印出持鎖的 pid；沒有活著的持有者就回傳 1。collect.sh 被 kill -9 時 EXIT trap 不會跑，
# 留下的殘鎖靠這裡的 kill -0 認出來、順手清掉。
collect_lock_holder() {
  local pid
  [ -d "$COLLECT_LOCK" ] || return 1
  pid="$(cat "$COLLECT_LOCK/pid" 2>/dev/null || true)"
  if [ -z "$pid" ]; then echo "?"; return 0; fi        # 剛 mkdir、pid 還沒寫進去：當作活的
  if kill -0 "$pid" 2>/dev/null; then echo "$pid"; return 0; fi
  echo "removing stale $COLLECT_LOCK (pid $pid is gone)" >&2
  rm -rf "$COLLECT_LOCK"
  return 1
}

refuse_if_collecting() {
  local pid
  if pid="$(collect_lock_holder)"; then
    echo "collect.sh (pid $pid) is using the headed browser session; wait for it to finish." >&2
    echo "If it is not running, remove $COLLECT_LOCK by hand." >&2
    exit "$EX_TEMPFAIL"
  fi
}

# collect.sh 用；拿不到就 75。呼叫端負責在 EXIT trap 裡 release_collect_lock。
acquire_collect_lock() {
  local pid
  if pid="$(collect_lock_holder)"; then
    echo "another collect.sh (pid $pid) holds $COLLECT_LOCK" >&2
    exit "$EX_TEMPFAIL"
  fi
  mkdir -p "$(dirname "$COLLECT_LOCK")"
  mkdir "$COLLECT_LOCK" 2>/dev/null || { echo "lost the race for $COLLECT_LOCK" >&2; exit "$EX_TEMPFAIL"; }
  echo $$ > "$COLLECT_LOCK/pid"
}

release_collect_lock() {
  if [ "$(cat "$COLLECT_LOCK/pid" 2>/dev/null)" = "$$" ]; then rm -rf "$COLLECT_LOCK"; fi
}

# mermaid 與表格都在 headless daemon 上以 1400x1400、2x 截圖。
# daemon 若還是 headed（medium_draft.sh 留下的），對 file:// 頁面會拒絕執行 JS，先 disconnect 讓它以 headless 重開。
# `viewport --scale` 會重建 browser context 並重播上一個 load-html；緊接著再 load-html 會撞在一起，
# mermaid 在被換掉一半的 DOM 上跑就會丟 null error。所以只在需要時改，改完等一下再載入。
HEADLESS_VIEWPORT=1400x1400
HEADLESS_SCALE=2
prepare_headless_viewport() {
  refuse_if_collecting
  local status cur
  # 先接住輸出再判斷：`if cmd | grep -q` 在 cmd 失敗時永遠不會成立（CLAUDE.md）
  status="$("$BROWSE" status 2>/dev/null)" || status=""
  case "$status" in *"Mode: headed"*) "$BROWSE" disconnect >/dev/null 2>&1 || true ;; esac
  cur="$("$BROWSE" js "window.innerWidth+'@'+window.devicePixelRatio" 2>/dev/null)" || cur=""
  if [ "$cur" != "${HEADLESS_VIEWPORT%x*}@$HEADLESS_SCALE" ]; then
    "$BROWSE" viewport "$HEADLESS_VIEWPORT" --scale "$HEADLESS_SCALE" >/dev/null 2>&1 || true
    "$BROWSE" js "new Promise(r=>setTimeout(r,1500)).then(()=>'ok')" >/dev/null 2>&1 || true
  fi
}
