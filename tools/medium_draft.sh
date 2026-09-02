#!/bin/bash
# Build a fully populated, verified Medium draft from an article directory.
#
#   ./tools/medium_draft.sh 2026-09-agentic-engineering-platform
#   ./tools/medium_draft.sh 2026-09-agentic-engineering-platform en
#
# Stops at a verified draft and prints its URL. It deliberately does NOT set
# topics, choose the preview image, or publish: those need a human look, and
# publishing mails every subscriber and cannot be undone.
#
# Prerequisites: logged into Medium in Chrome, and `browse` from gstack.

set -euo pipefail

# Tuning knobs, named so a reader can tell the tuned values from the guesses.
readonly UPLOAD_TIMEOUT_S=40     # largest image observed took ~8s to land
readonly EDITOR_SETTLE_S=3       # after the body paste, before touching grafs
readonly KEYPRESS_GAP_S=1        # the two Backspaces must not coalesce
readonly CHROME_PROFILE=Default   # the profile logged in to Medium
readonly EX_USAGE=64
readonly EX_UNAVAILABLE=69
readonly EX_TEMPFAIL=75


ARTICLE="${1:-}"
# Optional language pack. Empty means the default (Chinese) pack in publish/;
# anything else selects publish/<lang>/, which carries its own medium-paste.md
# AND its own images — the whole reason this argument exists is that pointing
# the driver at a translated paste file while it still uploads publish/images
# would ship the wrong figures with a clean-looking verification.
LANG_PACK="${2:-}"
if [ -z "$ARTICLE" ]; then
  echo "usage: $0 <article-dir> [lang]" >&2
  echo "       lang selects publish/<lang>/ (e.g. 'en'); omit for publish/" >&2
  exit "$EX_USAGE"
fi
# A directory name, not a path: 'en/../..' would walk out of the article.
case "$LANG_PACK" in
  *[!a-zA-Z0-9_-]*)
    echo "invalid lang '$LANG_PACK': letters, digits, - and _ only" >&2
    exit "$EX_USAGE" ;;
esac

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
TOOLS="$ROOT/tools"
if [ -n "$LANG_PACK" ]; then
  PUBLISH="$ROOT/$ARTICLE/publish/$LANG_PACK"
else
  PUBLISH="$ROOT/$ARTICLE/publish"
fi
IMAGES="$PUBLISH/images"
PASTE="$PUBLISH/medium-paste.md"
# Checked here rather than left to md2medium: a missing pack should say which
# pack, before anything opens a browser.
[ -f "$PASTE" ] || { echo "no such paste file: $PASTE" >&2; exit "$EX_USAGE"; }
[ -d "$IMAGES" ] || { echo "no such images dir: $IMAGES" >&2; exit "$EX_USAGE"; }
WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT

BROWSE="$ROOT/.claude/skills/gstack/browse/dist/browse"
[ -x "$BROWSE" ] || BROWSE="$HOME/.claude/skills/gstack/browse/dist/browse"
[ -x "$BROWSE" ] || { echo "browse not found; run gstack setup" >&2; exit "$EX_UNAVAILABLE"; }

# medium.com serves Cloudflare 403 to the default headless daemon, so every call
# needs --headed. The flag only takes effect on a fresh daemon.
B() { "$BROWSE" --headed "$@"; }

step() { printf '\n== %s\n' "$1"; }

step "converting markdown"
python3 "$TOOLS/md2medium.py" "$PASTE" --out "$WORK/payload.json"

step "starting headed browser"
"$BROWSE" disconnect >/dev/null 2>&1 || true
sleep 1
B goto https://medium.com >/dev/null

step "loading Medium session from Chrome"
python3 "$TOOLS/chrome_cookies.py" medium.com --profile "$CHROME_PROFILE" --out "$WORK/cookies.json"
B cookie-import "$WORK/cookies.json"
B goto https://medium.com/me/stories/drafts >/dev/null
drafts_page=$(B text) || { echo "could not read the drafts page" >&2; exit "$EX_TEMPFAIL"; }
case "$drafts_page" in
  *"you have been blocked"*)
    echo "Cloudflare blocked the session; retry, or run 'browse --headed handoff'" >&2
    exit "$EX_TEMPFAIL" ;;
esac
# A logged-out session renders a marketing page, not a blocked one, and would
# otherwise fail much later with an unrelated TypeError from the editor.
case "$drafts_page" in
  *Drafts*) ;;
  *) echo "Medium session is not logged in (profile $CHROME_PROFILE)." >&2
     echo "Check with: python3 $TOOLS/chrome_cookies.py medium.com --list" >&2
     exit "$EX_TEMPFAIL" ;;
esac

step "opening a new story"
B goto https://medium.com/new-story >/dev/null
sleep 2

step "setting the title"
python3 "$TOOLS/medium_js.py" title "$WORK/payload.json" > "$WORK/title.js"
title_result=$(B eval "$WORK/title.js") || { echo "could not set the title" >&2; exit 1; }
echo "$title_result"
case "$title_result" in
  *'"err"'*) echo "the editor did not load a title field" >&2; exit 1 ;;
esac

step "pasting the body"
python3 "$TOOLS/medium_js.py" body "$WORK/payload.json" > "$WORK/body.js"
B eval "$WORK/body.js"
sleep "$EDITOR_SETTLE_S"

DRAFT_URL=$(B url)
echo "draft: $DRAFT_URL"

step "inserting images"
# Selector and placeholder format come from Python so they are defined once.
selectors=$(python3 "$TOOLS/medium_js.py" selectors)
eval "$selectors"
python3 -c "import json,sys; print('\n'.join(json.load(open(sys.argv[1]))['images']))" \
  "$WORK/payload.json" > "$WORK/images.txt"
TOTAL_IMAGES=$(grep -c . "$WORK/images.txt")
EXPECTED_FIGURES=0

# read -r, not word splitting: a filename with a space must not become two names
while IFS= read -r name; do
  [ -n "$name" ] || continue
  printf '  %s ... ' "$name"
  EXPECTED_FIGURES=$((EXPECTED_FIGURES + 1))

  python3 "$TOOLS/medium_js.py" image "$IMAGES" "$name" > "$WORK/image.js"
  paste_result=$(B eval "$WORK/image.js") || {
    echo "FAILED: browse could not paste $name" >&2; exit 1; }
  case "$paste_result" in
    *'"err"'*) echo "FAILED: no placeholder for $name in the draft" >&2; exit 1 ;;
  esac

  # Wait for the upload. Until it finishes the <img> still points at a blob URL.
  # Count the figures too: checking only "no bad src" passes vacuously before
  # the new figure exists, and would then Backspace over real article text.
  uploaded=0
  for _ in $(seq 1 "$UPLOAD_TIMEOUT_S"); do
    if B js "(()=>{const i=[...document.querySelectorAll('$EDITOR_SEL figure img')];return JSON.stringify({n:i.length,bad:i.filter(x=>!/cdn-images|miro\.medium/.test(x.src)).length})})()" \
        | grep -q "\"n\":$EXPECTED_FIGURES,\"bad\":0"; then
      uploaded=1
      break
    fi
    sleep 1
  done
  if [ "$uploaded" -eq 0 ]; then
    echo "FAILED: $name did not finish uploading in ${UPLOAD_TIMEOUT_S}s" >&2
    exit 1
  fi

  # The figure lands above the placeholder paragraph; drop the placeholder.
  # First Backspace clears the selected text, second removes the empty graf.
  # If the slot was not found, these two presses would eat real body text.
  python3 "$TOOLS/medium_js.py" slot "$name" > "$WORK/slot.js"
  slot_result=$(B eval "$WORK/slot.js") || {
    echo "FAILED: browse could not select the placeholder for $name" >&2; exit 1; }
  case "$slot_result" in
    *"$SLOT_PREFIX$name"*) ;;   # the marker really is selected
    *) echo "FAILED: placeholder for $name was not selected; refusing to press" >&2
       echo "  browse returned: $slot_result" >&2
       exit 1 ;;
  esac
  B press Backspace >/dev/null
  sleep "$KEYPRESS_GAP_S"
  B press Backspace >/dev/null

  # Confirm per image. Checking once at the end means a Backspace that missed
  # on image 3 goes unnoticed until 22 more blind presses have landed.
  sleep "$KEYPRESS_GAP_S"
  left=$(B js "(()=>{const a=document.querySelector('$EDITOR_SEL');return (a.innerText.match(/$SLOT_PREFIX/g)||[]).length})()" | tr -dc '0-9')
  want_left=$((TOTAL_IMAGES - EXPECTED_FIGURES))
  # Numeric, not a glob: "*1*" would happily match 11.
  if [ "$left" != "$want_left" ]; then
    echo "FAILED: after $name, expected $want_left placeholders left, found '$left'" >&2
    exit 1
  fi
  echo "ok"
done < "$WORK/images.txt"

step "verifying against the converted payload"
B js "(()=>{const g=[...document.querySelectorAll('$EDITOR_SEL .graf')];return JSON.stringify({texts:g.filter(x=>x.tagName!=='FIGURE').map(x=>x.innerText),tags:g.map(x=>x.tagName),links:document.querySelectorAll('$EDITOR_SEL a').length})})()" > "$WORK/editor.json"
python3 "$TOOLS/verify_draft.py" "$WORK/payload.json" "$WORK/editor.json"

# Assert, do not just print: this reads like a gate, so it has to behave as one.
FINAL=$(B js "(()=>{const a=document.querySelector('$EDITOR_SEL');return JSON.stringify({figures:a.querySelectorAll('figure').length,leftoverSlots:(a.innerText.match(/$SLOT_PREFIX/g)||[]).length})})()")
echo "$FINAL"
echo "$FINAL" | grep -q "\"figures\":$EXPECTED_FIGURES," || {
  echo "FAILED: expected $EXPECTED_FIGURES figures" >&2; exit 1; }
echo "$FINAL" | grep -q '"leftoverSlots":0' || {
  echo "FAILED: placeholder text left in the draft" >&2; exit 1; }

step "draft ready"
B url
cat <<'NEXT'

Still to do by hand, in the Publish dialog:
  1. Topics: up to five. Medium normalises casing (Agentic AI -> Agentic Ai).
  2. Preview image: Medium defaults to the first figure, often a table
     screenshot that is unreadable at card size. Pick a diagram instead.
  3. "Notify your subscribers" mails every subscriber and cannot be recalled.
  4. Publish.
NEXT
