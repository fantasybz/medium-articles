#!/bin/bash
# Build a fully populated, verified Medium draft from an article directory,
# or refill an existing post with the same pipeline.
#
#   ./tools/medium_draft.sh 2026-09-agentic-engineering-platform
#   ./tools/medium_draft.sh 2026-09-agentic-engineering-platform en
#   ./tools/medium_draft.sh 2026-10-green-reliability --post 3c64a9622777
#   ./tools/medium_draft.sh 2026-10-green-reliability en --post 4b6d147bff0d
#
# Stops at a verified draft and prints its URL. It deliberately does NOT set
# topics, choose the preview image, or publish: those need a human look, and
# publishing mails every subscriber and cannot be undone.
#
# --post <id> opens https://medium.com/p/<id>/edit instead of a new story and
# replaces that post's body — old figures included — with this pack's. Two
# things differ from the new-draft path and nothing else does: where the
# browser goes, and one snippet (`refill` rather than `body`). Every image
# step, every placeholder check and the whole verify_draft.py gate are the
# same code, so a refill is held to exactly the same standard as a new draft.
#
# Use it instead of re-running the plain form when a post already exists: the
# Post ID is the article's identity here, every series link in the repo is a
# https://medium.com/p/<id> short URL, and building a new draft would strand
# all of them. Use it instead of medium_patch.py when the edit is a whole pass
# over the prose rather than a handful of grafs — patching cannot express an
# insertion at all, and every anchor that lands a graf off eats real text.
#
# The one thing --post can get catastrophically wrong is aiming at the wrong
# story, so the id is checked three times before anything is written: against
# the Post ID this pack records in its own PUBLISHED.md (offline, before a
# browser exists, and --retitle does NOT override it), against the URL the
# editor is actually sitting on, and against the title on screen. Only the
# third of those can be waved through, and only with --retitle.
#
# A failed run in --post mode leaves the post half-updated (Medium autosaves),
# and says so on the way out with what that means for a scheduled versus a
# published post. The recovery is this same command again: the refill does not
# append, it replaces.
#
# Prerequisites: logged into Medium in Chrome, and `browse` from gstack.

set -euo pipefail

# Tuning knobs, named so a reader can tell the tuned values from the guesses.
readonly UPLOAD_TIMEOUT_S=40     # largest image observed took ~8s to land
readonly EDITOR_SETTLE_S=3       # after the body paste, before polling grafs
readonly KEYPRESS_GAP_S=1        # the two Backspaces must not coalesce
# A new story renders instantly; an existing post has to fetch and lay out
# 149 grafs and 14 figures first, and asking it what it is too early looks
# exactly like "no editor here". The same budget covers the other two waits on
# a full editor: the redirect after `goto`, and the relayout after a refill has
# deleted 149 grafs and 14 figures and pasted 149 back.
readonly EDITOR_LOAD_TIMEOUT_S=20
readonly CHROME_PROFILE=Default   # the profile logged in to Medium
readonly EX_USAGE=64
readonly EX_UNAVAILABLE=69
readonly EX_TEMPFAIL=75
# Every https://medium.com/p/<id> link in the repo ends in one of these.
readonly POST_ID_HELP="twelve lowercase hex digits, e.g. 3c64a9622777 (the tail of https://medium.com/p/<id>/edit)"

usage() {
  echo "usage: $0 <article-dir> [lang] [--post <id>] [--retitle]" >&2
  echo "       lang selects publish/<lang>/ (e.g. 'en'); omit for publish/" >&2
  echo "       --post <id> refills that existing post in place; the Post ID," >&2
  echo "                   its URL and any schedule on it do not change." >&2
  echo "                   The id must be the one the pack's PUBLISHED.md" >&2
  echo "                   records, and no flag overrides that" >&2
  echo "       --retitle   proceed even though the post's title differs from" >&2
  echo "                   the paste file's (say so only after reading both)" >&2
}

# Checked here, before a browser opens, because in --post mode every
# destructive step below aims at whatever id it is handed. A glob cannot count,
# so the length and the alphabet are two cases.
check_post_id() {
  case "$1" in
    ????????????) ;;
    *) echo "invalid --post id '$1': expected $POST_ID_HELP" >&2; exit "$EX_USAGE" ;;
  esac
  case "$1" in
    *[!0-9a-f]*)
      echo "invalid --post id '$1': expected $POST_ID_HELP" >&2; exit "$EX_USAGE" ;;
  esac
}

ARTICLE=""
POSITIONALS=0    # how many were given, not how many are non-empty: see below
# Optional language pack. Empty means the default (Chinese) pack in publish/;
# anything else selects publish/<lang>/, which carries its own medium-paste.md
# AND its own images — the whole reason this argument exists is that pointing
# the driver at a translated paste file while it still uploads publish/images
# would ship the wrong figures with a clean-looking verification.
LANG_PACK=""
POST_ID=""
RETITLE=0
# Options are parsed anywhere in the line rather than positionally: the id is
# copied out of the table in PUBLISHING.md and pasted onto the end of a command
# that already reads `<article> en`.
while [ "$#" -gt 0 ]; do
  case "$1" in
    --post)
      [ "$#" -ge 2 ] || { echo "--post needs an id: $POST_ID_HELP" >&2; exit "$EX_USAGE"; }
      POST_ID="$2"
      check_post_id "$POST_ID"
      shift 2 ;;
    --post=*)
      POST_ID="${1#--post=}"
      check_post_id "$POST_ID"
      shift ;;
    --retitle)
      RETITLE=1
      shift ;;
    -*)
      echo "unknown option: $1" >&2; usage; exit "$EX_USAGE" ;;
    *)
      # Counted, not tested for emptiness. `"$dir" "$lang" "$id"` out of a
      # wrapper whose $lang is empty for the Chinese pack used to slide the id
      # into LANG_PACK and report it as a missing paste file, because an empty
      # second positional read as "not given yet".
      POSITIONALS=$((POSITIONALS + 1))
      case "$POSITIONALS" in
        1) ARTICLE="$1" ;;
        2) LANG_PACK="$1" ;;
        *)
          # Silently ignoring it is how a third positional meant as an option
          # ends up running the default new-draft path.
          echo "unexpected argument: $1" >&2; usage; exit "$EX_USAGE" ;;
      esac
      shift ;;
  esac
done

if [ -z "$ARTICLE" ]; then
  usage
  exit "$EX_USAGE"
fi
# A directory name, not a path: 'en/../..' would walk out of the article.
case "$LANG_PACK" in
  *[!a-zA-Z0-9_-]*)
    echo "invalid lang '$LANG_PACK': letters, digits, - and _ only" >&2
    exit "$EX_USAGE" ;;
esac
# On a new story there is no title to disagree with, so the flag would only
# read as approval for something this run never checks.
if [ "$RETITLE" -eq 1 ] && [ -z "$POST_ID" ]; then
  echo "--retitle only means something with --post" >&2
  exit "$EX_USAGE"
fi
# One word for what this run is producing, so the two modes cannot drift into
# calling a live post a draft in half their messages.
if [ -n "$POST_ID" ]; then WHAT=post; else WHAT=draft; fi

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
# $ARTICLE gets no charset check (article dirs are dated slugs, not a fixed
# set), so assert the resolved pack is actually inside the repo. Both guards
# above pass happily for '../../../tmp/whatever', and every PNG in that
# directory would then be base64'd into the draft and uploaded to Medium's
# public CDN. Resolve with pwd -P so symlinks cannot dodge the prefix test.
ROOT_ABS="$(cd "$ROOT" && pwd -P)"
PUBLISH_ABS="$(cd "$PUBLISH" && pwd -P)"
case "$PUBLISH_ABS/" in
  "$ROOT_ABS"/*) ;;
  *) echo "pack resolves outside the repo: $PUBLISH_ABS" >&2; exit "$EX_USAGE" ;;
esac

# Bind the id to this pack, offline, before a browser exists.
#
# This is the check that actually stands between a typo and a rewritten
# article. The two downstream ones cannot: the URL check only says the browser
# is where it was sent, and the title check - the only one that ever compares
# the id against *content* - is exactly what --retitle turns off. Ask for the
# neighbouring row of the table in PUBLISHING.md and everything downstream
# agrees, because everything downstream compares the editor against this
# pack's payload, which is precisely what a refill has just made it hold.
#
# Every pack records its own id, in its own PUBLISHED.md, on a line reading
#     **Post ID** `<id>`
# and the pack is per language, so the en pack's ledger is the one consulted
# for an en run. Matched on that line rather than anywhere in the file: the
# zh ledgers also mention the en post's id in a cross-reference, and a `grep
# "$POST_ID"` would take an en id as proof of a zh post.
#
# No ledger, or no id in it, is a refusal rather than a pass: --post refills a
# story that already exists, and in this repo every story that exists is
# recorded. There is no --force, on purpose. Adding the line to the ledger is
# the same amount of typing and leaves the repo true afterwards.
if [ -n "$POST_ID" ]; then
  LEDGER="$PUBLISH/PUBLISHED.md"
  if [ ! -f "$LEDGER" ]; then
    echo "no ledger for this pack: $LEDGER" >&2
    echo "  --post needs the pack to say which post it is. Add the line:" >&2
    echo "    **Post ID** \`$POST_ID\`" >&2
    exit "$EX_USAGE"
  fi
  RECORDED=$(sed -n 's/^\*\*Post ID\*\* `\([0-9a-f][0-9a-f]*\)`.*/\1/p' "$LEDGER" | head -1)
  if [ -z "$RECORDED" ]; then
    echo "$LEDGER records no Post ID" >&2
    echo "  expected a line reading: **Post ID** \`<id>\`" >&2
    exit "$EX_USAGE"
  fi
  if [ "$RECORDED" != "$POST_ID" ]; then
    echo "FAILED: --post $POST_ID is not the post this pack belongs to" >&2
    echo "  $LEDGER records $RECORDED" >&2
    echo "  Copying the neighbouring row out of the table in PUBLISHING.md is" >&2
    echo "  the way this happens. --retitle does not override this check." >&2
    exit "$EX_USAGE"
  fi
fi

WORK="$(mktemp -d)"
# Set before the trap that reads it, so an early exit cannot trip over `set -u`.
# 1 means the old body is already gone: past that point a failure leaves a real
# post in a state nobody asked for, and saying so is the difference between
# "that run did nothing" and "that post publishes with IMGSLOT- in it".
BODY_REPLACED=0
RERUN="$0 $ARTICLE${LANG_PACK:+ $LANG_PACK}${POST_ID:+ --post $POST_ID}"
cleanup() {
  status=$?
  rm -rf "$WORK"
  if [ "$status" -ne 0 ] && [ "$BODY_REPLACED" -eq 1 ]; then
    cat >&2 <<WARN

!! /p/$POST_ID was rewritten before this failed, and Medium autosaves. The run
   did NOT leave that post alone:
     - the new body is stored (the refill replaces, it never appends)
     - any image that did not make it in is still sitting in the text as an
       IMGSLOT-...-ENDSLOT placeholder
   What that means depends on the post:
     - scheduled: nobody has to press anything for it to go out, so it
       publishes on its slot exactly as it stands now, placeholders included.
     - published: readers still see the last published version. Nothing here
       presses "Save and publish", so what is stored is only the draft
       behind it.
   Open it and look before deciding. If the run got as far as verifying
   against the payload, the body and the images are all in and re-running is
   not the fix - read the failure above. Otherwise the recovery is the same
   command again:
     $RERUN
WARN
  fi
}
trap cleanup EXIT

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

# One number out of a flat JSON object: json_num <key> <json>. The keys these
# snippets emit are unique per object, and every value asserted on is an
# integer, so this stays a `sed` rather than a python3 start per poll tick.
json_num() {
  printf '%s' "$2" | sed -n "s/.*\"$1\":\\([0-9][0-9]*\\).*/\\1/p" | head -1
}

TITLE_MATCHED=0
if [ -n "$POST_ID" ]; then
  EDIT_URL="https://medium.com/p/$POST_ID/edit"
  step "opening post $POST_ID"
  B goto "$EDIT_URL" >/dev/null

  # Guard 1: the browser is on the edit URL for this id, and nothing else.
  #
  # Not `case $here in *$POST_ID*`, which is what this used to be and which
  # never fired: this repo's published URLs END in the same id
  # (https://fantasybz.medium.com/<slug>-<id>, see any PUBLISHED.md), and so
  # does the ?redirect= of a sign-in bounce, so the read view that Medium
  # sends a non-editable id to matched it. Matching the shape instead makes
  # "the id resolves, but not to an editor of yours" a first-second refusal
  # with an honest message, rather than 20 seconds of polling ending in "no
  # editor here".
  #
  # Polled rather than read once after a fixed sleep: `goto` returning is not
  # the redirect having happened, and reading too early reported the PREVIOUS
  # page as the redirect target - a wrong diagnosis pointing at a correct id.
  # Captured, not piped: browse reports failure on stderr with an empty
  # stdout, so `if B url | grep` would read as "no match" either way.
  here=""
  url_failed=0
  for _ in $(seq 1 "$EDITOR_LOAD_TIMEOUT_S"); do
    if here=$(B url); then
      url_failed=0
      case "$here" in
        "$EDIT_URL"|"$EDIT_URL"[?#]*) break ;;
      esac
    else
      url_failed=1
      here=""
    fi
    sleep 1
  done
  case "$here" in
    "$EDIT_URL"|"$EDIT_URL"[?#]*) ;;
    *)
      if [ "$url_failed" -eq 1 ]; then
        echo "could not read the editor URL; the browser or the daemon is gone" >&2
        exit "$EX_TEMPFAIL"
      fi
      echo "FAILED: $EDIT_URL did not open; the browser is at ${here:-<nothing>}" >&2
      case "$here" in
        *"$POST_ID"*)
          echo "  that id exists but did not open an editor. Medium sends a post" >&2
          echo "  you cannot edit to its read view, whose URL ends in the same id;" >&2
          echo "  check the Medium session, and that this account owns the post." >&2 ;;
        *)
          echo "  that id is not a post of yours, or the page never navigated." >&2 ;;
      esac
      exit "$EX_UNAVAILABLE" ;;
  esac

  # Guard 2: the editor has finished loading AND it is this article. Polled
  # with the same snippet that judges it, because "no editor yet" and "no
  # editor at all" arrive as the same answer; only the timeout tells them
  # apart.
  #
  # "Finished" is two consecutive reads agreeing on the graf and figure counts,
  # not the first answer that parses. identify returns as soon as the shell and
  # the title graf exist, which on a 149-graf post is true while the body is
  # still streaming in - and the refill that follows would then select the
  # handful of grafs that had arrived, leaving the other 140 and every old
  # figure standing underneath the new body. The counts needed for that test
  # were already in the reply and were being thrown away.
  step "confirming the post"
  python3 "$TOOLS/medium_js.py" identify "$WORK/payload.json" > "$WORK/identify.js"
  id_result=""
  eval_failed=0
  prev_shape=""
  settled=0
  for _ in $(seq 1 "$EDITOR_LOAD_TIMEOUT_S"); do
    if id_result=$(B eval "$WORK/identify.js"); then
      eval_failed=0
    else
      eval_failed=1
      id_result=""
    fi
    case "$id_result" in
      *'"match":'*)
        shape="$(json_num grafs "$id_result"):$(json_num figures "$id_result")"
        if [ "$shape" != ":" ] && [ "$shape" = "$prev_shape" ]; then
          settled=1
          break
        fi
        prev_shape="$shape" ;;
    esac
    sleep 1
  done
  if [ "$settled" -eq 0 ]; then
    # Three different failures, three different exits: a browser that stopped
    # answering is worth retrying, an editor that never appeared is not.
    if [ "$eval_failed" -eq 1 ]; then
      echo "FAILED: browse could not read the editor at $EDIT_URL" >&2
      echo "  the last call failed outright, so this is the browser, not the post" >&2
      exit "$EX_TEMPFAIL"
    fi
    case "$id_result" in
      *'"match":'*)
        echo "$id_result" >&2
        echo "FAILED: the post at $EDIT_URL was still growing after ${EDITOR_LOAD_TIMEOUT_S}s" >&2
        echo "  refusing to replace a body that has not finished arriving" >&2 ;;
      *)
        echo "FAILED: no Medium editor at $EDIT_URL after ${EDITOR_LOAD_TIMEOUT_S}s" >&2
        echo "  browse returned: ${id_result:-<nothing>}" >&2 ;;
    esac
    exit "$EX_UNAVAILABLE"
  fi
  echo "$id_result"

  # The URL again, from inside the same read as the title and the counts. Guard
  # 1 proved where the browser was a moment ago; between then and now the page
  # can navigate, and "an editor is loaded" and "the editor is the one at that
  # id" have to be one answer rather than two that were true at different times.
  case "$id_result" in
    *"\"url\":\"$EDIT_URL\""*|*"\"url\":\"$EDIT_URL?"*|*"\"url\":\"$EDIT_URL#"*) ;;
    *) echo "$id_result" >&2
       echo "FAILED: the editor answering is not the one at $EDIT_URL" >&2
       echo "  the page moved between opening it and reading it" >&2
       exit "$EX_UNAVAILABLE" ;;
  esac

  case "$id_result" in
    *'"match":true'*) TITLE_MATCHED=1 ;;
    *)
      # A reworded title is legitimate and this run is how it would ship, so
      # this is not automatically "wrong post". It is no longer the only thing
      # standing between a mistyped id and a rewritten article either - the
      # ledger check upstream is - but it is the only one that compares the id
      # against what is actually on screen. Both titles are printed, on stderr
      # as well, because reading them is the decision this stops for and a
      # `2>err.log` run would otherwise be told to compare two lines that went
      # to the other stream.
      if [ "$RETITLE" -eq 1 ]; then
        echo "  title differs from the paste file; --retitle given, continuing"
        echo "  --retitle only waives the title check: --post $POST_ID was still"
        echo "  matched against $LEDGER before the browser opened."
        echo "  The title is about to be overwritten with this pack's, so a"
        echo "  re-run will not be able to repeat this comparison."
      else
        echo "$id_result" >&2
        echo "FAILED: the post's title is not this pack's title" >&2
        echo "  compare 'want' and 'got' above. If the title really was" >&2
        echo "  reworded, re-run with --retitle; otherwise check the id." >&2
        exit "$EX_UNAVAILABLE"
      fi ;;
  esac
else
  step "opening a new story"
  B goto https://medium.com/new-story >/dev/null
  sleep 2
fi

# Writing the title is skipped when it already matches, and only in --post
# mode. Two reasons, both about a live post: a paste into the title field of a
# published article is a write that buys nothing when the strings already fold
# equal, and - the sharper one - the title is the run's only content-level
# check that the id opened the right story. Overwriting it first means a run
# that dies later has erased the evidence, and the re-run the operator is told
# to do would see a title that matches because the failed run put it there.
#
# Skipping it cannot make the verification at the end fail: identify folds the
# title with the same rules verify_draft.py normalises block 0 with, and
# test_tools.py asserts the two fold identically. A title left alone here is a
# title that already compares equal there.
if [ "$TITLE_MATCHED" -eq 1 ]; then
  step "title already matches this pack, leaving it alone"
else
  step "setting the title"
  python3 "$TOOLS/medium_js.py" title "$WORK/payload.json" > "$WORK/title.js"
  title_result=$(B eval "$WORK/title.js") || {
    echo "could not set the title" >&2; exit "$EX_TEMPFAIL"; }
  echo "$title_result"
  case "$title_result" in
    *'"err"'*) echo "the editor did not load a title field" >&2; exit "$EX_UNAVAILABLE" ;;
  esac
fi

step "pasting the body"
if [ -n "$POST_ID" ]; then
  # refill, not body: on an existing post the old body has to go, figures
  # included. One DOM Range over everything below the title does both — the
  # paste replaces the selection — so there is no window in which the post is
  # empty, and no anchor to land in the wrong place.
  python3 "$TOOLS/medium_js.py" refill "$WORK/payload.json" > "$WORK/body.js"
else
  python3 "$TOOLS/medium_js.py" body "$WORK/payload.json" > "$WORK/body.js"
fi
body_result=$(B eval "$WORK/body.js") || {
  echo "could not paste the body" >&2; exit "$EX_TEMPFAIL"; }
echo "$body_result"
case "$body_result" in
  *'"err"'*) echo "the body paste found nothing to replace" >&2
             exit "$EX_UNAVAILABLE" ;;
esac
if [ -n "$POST_ID" ]; then
  # Past here the old body is gone, so the trap has something to say if
  # anything below fails.
  BODY_REPLACED=1
  # Both of these are read back out of the editor AFTER the paste, and both
  # are refusals with nothing uploaded yet - one Save away from being undone.
  #
  # titleOk, not "the title is not empty". `graf--title` is assigned by
  # position (which is how title_js finds the title of a brand new story that
  # has never been typed in), so a selection that reached over the title does
  # not leave an empty one: it leaves the first pasted paragraph promoted to
  # the title. That is not empty, and the run would have gone on to upload 18
  # images before verify_draft.py noticed at block 0.
  case "$body_result" in
    *'"titleOk":true'*) ;;
    *) echo "FAILED: the title is not this pack's after the body paste" >&2
       echo "  the selection reached above the body and took the title with it" >&2
       exit "$EX_UNAVAILABLE" ;;
  esac
  # figuresLeft, not figuresRemoved. The whole mode rests on the range having
  # taken the old figures out with the old prose, and the number that used to
  # be reported was the count from BEFORE the paste - it said "14" whether or
  # not one of them went. Everything below counts figures up from zero, so a
  # survivor turns the first upload wait into a 40s timeout blaming the
  # network for a selection that did not do what this run assumed.
  case "$body_result" in
    *'"figuresLeft":0,'*) ;;
    *) echo "FAILED: the refill left old figures behind" >&2
       echo "  the paste did not take them with the old prose, which every" >&2
       echo "  figure count below assumes; stopping before anything is uploaded" >&2
       exit "$EX_UNAVAILABLE" ;;
  esac
fi

DRAFT_URL=$(B url) || {
  echo "could not read the $WHAT URL" >&2; exit "$EX_TEMPFAIL"; }
echo "$WHAT: $DRAFT_URL"

# Selector and placeholder format come from Python so they are defined once.
selectors=$(python3 "$TOOLS/medium_js.py" selectors)
eval "$selectors"
# The one read every checkpoint below takes: figures, imgs, pending uploads and
# placeholder markers, counted together by one snippet rather than by three
# inline queries that had drifted into counting different things.
python3 "$TOOLS/medium_js.py" state > "$WORK/state.js"
python3 -c "import json,sys; print('\n'.join(json.load(open(sys.argv[1]))['images']))" \
  "$WORK/payload.json" > "$WORK/images.txt"
# `|| true`: grep -c prints 0 and exits 1 on an article with no figures, and
# under `set -e` the assignment alone would end the run right here - after the
# body has been replaced, with no message at all.
TOTAL_IMAGES=$(grep -c . "$WORK/images.txt" || true)
EXPECTED_FIGURES=0

# Wait for the editor to settle, by asking rather than by sleeping. Both
# numbers are assertions, not diagnostics:
#
#   figures == 0   nothing carried over. A new story has none; a refill has
#                  none if its range did what the mode assumes. This is the
#                  same fact body_result already claimed, re-read after the
#                  relayout rather than in the tick the paste happened.
#   slots == N     every placeholder the payload asked for is in the document.
#                  The old fixed `sleep 3` was tuned on a new story; a refill
#                  has just deleted 149 grafs and 14 figures and pasted 149
#                  back, and finding no placeholder for diagram-01.png is how
#                  that ran out - on a published post whose body was already
#                  replaced.
step "waiting for the editor to settle"
sleep "$EDITOR_SETTLE_S"
state=""
settled=0
for _ in $(seq 1 "$EDITOR_LOAD_TIMEOUT_S"); do
  state=$(B eval "$WORK/state.js") || state=""
  case "$state" in
    *'"figures":0,'*'"slots":'"$TOTAL_IMAGES"'}'*) settled=1; break ;;
  esac
  sleep 1
done
if [ "$settled" -eq 0 ]; then
  echo "FAILED: the editor did not settle in ${EDITOR_LOAD_TIMEOUT_S}s after the paste" >&2
  echo "  wanted 0 figures and $TOTAL_IMAGES placeholders, browse returned: ${state:-<nothing>}" >&2
  exit "$EX_UNAVAILABLE"
fi
echo "$state"

step "inserting images"

# read -r, not word splitting: a filename with a space must not become two names
while IFS= read -r name; do
  [ -n "$name" ] || continue
  printf '  %s ... ' "$name"
  EXPECTED_FIGURES=$((EXPECTED_FIGURES + 1))

  python3 "$TOOLS/medium_js.py" image "$IMAGES" "$name" > "$WORK/image.js"
  paste_result=$(B eval "$WORK/image.js") || {
    echo "FAILED: browse could not paste $name" >&2; exit "$EX_TEMPFAIL"; }
  case "$paste_result" in
    *'"err"'*) echo "FAILED: no placeholder for $name in the $WHAT" >&2
               exit "$EX_UNAVAILABLE" ;;
  esac

  # Wait for the upload. Until it finishes the <img> still points at a blob URL.
  # Count the figures too: checking only "no bad src" passes vacuously before
  # the new figure exists, and would then Backspace over real article text.
  uploaded=0
  for _ in $(seq 1 "$UPLOAD_TIMEOUT_S"); do
    state=$(B eval "$WORK/state.js") || state=""
    case "$state" in
      *'"imgs":'"$EXPECTED_FIGURES"',"pending":0'*) uploaded=1; break ;;
    esac
    sleep 1
  done
  if [ "$uploaded" -eq 0 ]; then
    echo "FAILED: $name did not finish uploading in ${UPLOAD_TIMEOUT_S}s" >&2
    echo "  wanted $EXPECTED_FIGURES images, none pending; browse returned: ${state:-<nothing>}" >&2
    exit "$EX_UNAVAILABLE"
  fi

  # The figure lands above the placeholder paragraph; drop the placeholder.
  # First Backspace clears the selected text, second removes the empty graf.
  # If the slot was not found, these two presses would eat real body text.
  python3 "$TOOLS/medium_js.py" slot "$name" > "$WORK/slot.js"
  slot_result=$(B eval "$WORK/slot.js") || {
    echo "FAILED: browse could not select the placeholder for $name" >&2
    exit "$EX_TEMPFAIL"; }
  case "$slot_result" in
    *"$SLOT_PREFIX$name"*) ;;   # the marker really is selected
    *) echo "FAILED: placeholder for $name was not selected; refusing to press" >&2
       echo "  browse returned: $slot_result" >&2
       exit "$EX_UNAVAILABLE" ;;
  esac
  B press Backspace >/dev/null
  sleep "$KEYPRESS_GAP_S"
  B press Backspace >/dev/null

  # Confirm per image. Checking once at the end means a Backspace that missed
  # on image 3 goes unnoticed until 22 more blind presses have landed.
  sleep "$KEYPRESS_GAP_S"
  state=$(B eval "$WORK/state.js") || {
    echo "FAILED: browse could not count what is left after $name" >&2
    exit "$EX_TEMPFAIL"; }
  left=$(json_num slots "$state")
  want_left=$((TOTAL_IMAGES - EXPECTED_FIGURES))
  # Numeric, not a glob: "*1*" would happily match 11.
  if [ "$left" != "$want_left" ]; then
    echo "FAILED: after $name, expected $want_left placeholders left, found '${left:-<nothing>}'" >&2
    exit "$EX_UNAVAILABLE"
  fi
  echo "ok"
done < "$WORK/images.txt"

step "verifying against the converted payload"
# dividers travels with the grafs: a <hr> is not a .graf and carries no text,
# so neither the block diff nor the figure-placement check can see one, and a
# refill's range crosses every section wrapper in the article. verify_draft.py
# compares the count against the payload's.
python3 "$TOOLS/medium_js.py" dump > "$WORK/dump.js"
editor_dump=$(B eval "$WORK/dump.js") || {
  echo "could not read the editor back" >&2; exit "$EX_TEMPFAIL"; }
case "$editor_dump" in
  *'"err"'*) echo "the editor was gone when the verification read it" >&2; exit 1 ;;
esac
printf '%s' "$editor_dump" > "$WORK/editor.json"
python3 "$TOOLS/verify_draft.py" "$WORK/payload.json" "$WORK/editor.json"

# Assert, do not just print: this reads like a gate, so it has to behave as one.
FINAL=$(B eval "$WORK/state.js") || {
  echo "FAILED: browse could not read the final state" >&2; exit "$EX_TEMPFAIL"; }
echo "$FINAL"
case "$FINAL" in
  *'"figures":'"$EXPECTED_FIGURES"','*) ;;
  *) echo "FAILED: expected $EXPECTED_FIGURES figures" >&2; exit "$EX_UNAVAILABLE" ;;
esac
case "$FINAL" in
  *'"slots":0}'*) ;;
  *) echo "FAILED: placeholder text left in the $WHAT" >&2; exit "$EX_UNAVAILABLE" ;;
esac

step "$WHAT ready"
B url
if [ -n "$POST_ID" ]; then
  # A different list on purpose: topics and the cover were chosen when this
  # post first went out, and the one thing a refill really does need saying is
  # which button commits it.
  cat <<NEXT

Refilled in place. Still to do by hand, in the editor. Nothing below has
happened yet, and the two kinds of post are not in the same danger:

  1. Post ID $POST_ID is unchanged, so every https://medium.com/p/<id>
     cross-link in the series still resolves. Nothing was re-created.
  2. Already published: readers are still seeing the last published version.
     This new body is only the draft behind it until you press "Save and
     publish". Medium files that as postPublishedType=repub - same URL, no
     second mail to subscribers (measured; see publish/en/PUBLISHED.md).
  3. Scheduled: the opposite. Nobody has to press anything for this to go out,
     so whatever is stored now is what publishes on the slot. Not verified by
     this tool: whether editing a scheduled post keeps its schedule. Open
     Stories -> Scheduled, confirm this one is still queued for the same time,
     and write what you saw into publish/PUBLISHED.md.
  4. Preview image: every figure here was deleted and re-uploaded, so open the
     settings and check the cover is still the diagram you picked. Topics are
     believed to survive a refill; that has not been measured either, and the
     same settings panel shows them.
NEXT
else
  cat <<'NEXT'

Still to do by hand, in the Publish dialog:
  1. Topics: up to five. Medium normalises casing (Agentic AI -> Agentic Ai).
  2. Preview image: Medium defaults to the first figure, often a table
     screenshot that is unreadable at card size. Pick a diagram instead.
  3. "Notify your subscribers" mails every subscriber and cannot be recalled.
  4. Publish.
NEXT
fi
