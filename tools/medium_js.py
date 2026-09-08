#!/usr/bin/env python3
"""Emit the browser snippets that drive Medium's editor, for `browse eval`.

Medium's classic editor does not check `event.isTrusted`, so a synthetic
ClipboardEvent carrying a DataTransfer is the whole trick: `text/html` on the
DataTransfer inserts formatted rich text in one shot, and a File added to
`dataTransfer.items` uploads an image. Typing the title character by character
does not work reliably (the placeholder span swallows the first few keystrokes),
so the title goes in as a paste too.

Usage:
    python3 tools/medium_js.py title    /tmp/payload.json        > /tmp/title.js
    python3 tools/medium_js.py body     /tmp/payload.json        > /tmp/body.js
    python3 tools/medium_js.py identify /tmp/payload.json        > /tmp/ident.js
    python3 tools/medium_js.py refill   /tmp/payload.json        > /tmp/body.js
    python3 tools/medium_js.py image    <images_dir> <file.png>  > /tmp/image.js
    python3 tools/medium_js.py slot     <file.png>               > /tmp/slot.js
    python3 tools/medium_js.py state                             > /tmp/state.js
    python3 tools/medium_js.py selectors                         # shell eval

`identify` and `refill` are the two snippets `medium_draft.sh --post <id>` adds
on top of the new-draft path: one confirms the editor on screen really is the
post the payload belongs to, the other replaces that post's whole body — old
figures included — with this payload's. Everything after them is the same code
that fills a new draft.

`state` is the one read the driver takes at every checkpoint — after the body
paste, while an upload lands, after each placeholder is deleted, and at the end.
It used to be three inline queries in the shell that had drifted into counting
slightly different things; one snippet means a checkpoint cannot pass because it
happened to ask an easier question than the one next to it.
"""

import base64
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from md2medium import SLOT_MARK  # one definition of the placeholder format

EDITOR = ".postArticle-content"
# The title lives outside the body every snippet here rewrites, so it gets its
# own selector rather than a repeated literal: `refill` deletes everything this
# does NOT match, and a stale copy of the selector would delete the title too.
TITLE = "h3.graf--title"

# Select the contents of `target`, which the caller has already found, so the
# paste that follows replaces it. Declares nothing the callers also declare.
PASTE = """
  document.querySelector('%s').focus();
  const range = document.createRange();
  range.selectNodeContents(target);
  const sel = getSelection();
  sel.removeAllRanges();
  sel.addRange(range);
""" % EDITOR

# What "the body" is: everything below the title, and only that. Declares
# `body` for the callers, which have to have found `editor` and `titleEl`
# first. Defined once because both pastes select exactly this range and then
# replace it — and the two copies had already drifted: only refill's excluded a
# figure's caption, so `body_js`, whose docstring promises it is safe to re-run,
# would end its range inside a figure on any draft that already had one.
#
# Three terms: never the node identified as the title, never anything else
# Medium marks as a title graf, and never a graf nested inside another — a
# figure's caption is one, and setEndAfter() on a caption would end the range
# inside its figure and leave half the figure standing.
BODY_GRAFS = """
  const body = [...editor.querySelectorAll('.graf')]
    .filter(g => g !== titleEl && !g.classList.contains('graf--title')
                 && !g.parentElement.closest('.graf'));
"""

# Fold Medium's house typography out of a title before comparing it with the
# one in the payload. Declares `fold` for the callers.
#
# Not medium_patch.NORMALISE, which folds the invisibles and the em dash but
# leaves quotes alone: Medium curls an apostrophe, so "Don't Build Your Own
# Devin" comes back as "Don’t ..." and every English title in this repo
# would fail an identity check that did not fold it. The set is the one
# verify_draft.py folds on every graf, the title included (the caret rewrite
# too: a title carrying `pass^5` would come back superscripted) — a title that is
# only "different" here would fail there too, so folding fewer of them would
# just move the false alarm later. Escapes, not the literal characters, for
# the same reason medium_patch.py spells its class out: half of them are
# invisible in an editor, so a stray edit would silently change what counts
# as the same title.
#
# Every rule below has to fold the same way verify_draft.normalise() does, and
# test_tools.py asserts that, rule by rule, against the same inputs: this is a
# third hand copy of a set that grew one rule at a time as Medium added
# rewrites, and a rule that lands in only one copy shows up as an identity
# check failing on two titles that are identical on screen, which pushes the
# operator straight to --retitle. The lookarounds in the en dash rule are the
# first drift that assertion caught: the old `/(\d)\u2013(\d)/g` consumed the
# digit on each side, so a second en dash sharing a digit with the first was
# left standing. Python folds with lookarounds and folded both.
TITLE_FOLD = r"""
  const fold = s => s.replace(/[\u200A\u2009\uFEFF]/g, '')
                     .replace(/\u00A0/g, ' ')
                     .replace(/[\u2018\u2019]/g, "'")
                     .replace(/[\u201C\u201D]/g, '"')
                     .replace(/[ \t]*\u2014[ \t]*/g, '\u2014')
                     .replace(/(?<=\d)\u2013(?=\d)/g, '-')
                     .replace(/[\u2070\u00B9\u00B2\u00B3\u2074-\u2079]+/g,
                              m => '^' + [...m].map(
                                c => '\u2070\u00B9\u00B2\u00B3\u2074\u2075\u2076\u2077\u2078\u2079'.indexOf(c)).join(''))
                     .replace(/\s+/g, ' ')
                     .trim();
"""


def title_js(payload):
    return """(() => {
  const target = document.querySelector('%s');
  if (!target) return JSON.stringify({ err: 'no title field' });
%s
  const dt = new DataTransfer();
  dt.setData('text/plain', %s);
  target.dispatchEvent(new ClipboardEvent('paste', { clipboardData: dt, bubbles: true, cancelable: true }));
  return JSON.stringify({ title: document.querySelector('%s').innerText });
})()
""" % (TITLE, PASTE, json.dumps(payload["title"], ensure_ascii=False), TITLE)


def body_js(payload):
    """Replace everything below the title with the article body.

    Selecting the existing body grafs first means this is safe to re-run: the
    paste overwrites the selection instead of appending a second copy. Which
    grafs those are comes from BODY_GRAFS, the same expression `refill` uses,
    so the caption rule that keeps a range from ending inside a figure holds
    here too.
    """
    return """(() => {
  const editor = document.querySelector('%s');
  const titleEl = document.querySelector('%s');
  if (!editor || !titleEl) return JSON.stringify({ err: 'no Medium editor on this page' });
%s
  if (!body.length) return JSON.stringify({ err: 'no body grafs' });
  editor.focus();
  const range = document.createRange();
  range.setStartBefore(body[0]);
  range.setEndAfter(body[body.length - 1]);
  const sel = getSelection();
  sel.removeAllRanges();
  sel.addRange(range);
  const HTML = %s;
  const dt = new DataTransfer();
  dt.setData('text/html', HTML);
  dt.setData('text/plain', HTML.replace(/<[^>]+>/g, ''));
  body[0].dispatchEvent(new ClipboardEvent('paste', { clipboardData: dt, bubbles: true, cancelable: true }));
  return JSON.stringify({ replaced: body.length });
})()
""" % (EDITOR, TITLE, BODY_GRAFS, json.dumps(payload["html"], ensure_ascii=False))


def identify_js(payload):
    """Report whether the editor on screen is the post this payload belongs to.

    Read-only, and it runs before anything in `--post` mode is allowed to
    change a single graf: the whole risk of refilling by post id is that a
    mistyped id opens a *different* story and the refill silently overwrites
    it — on a post readers can already see.

    Two signals, both returned rather than judged here:

    * `err` — no editor on the page at all. A deleted or non-existent id
      renders a 404, and someone else's post renders the read view, so the
      absence of an editable title is by itself a stop.
    * `match` — the editor's title folds to the payload's. Titles are the only
      thing in the payload that a mistyped id can be checked against, since
      every other block may legitimately have been reworded since the post
      went out.

    `url`, `grafs` and `figures` come back with them, and all three are read in
    the same tick as the title. The caller checks the URL after its `goto` and
    again here for a reason: between those two reads the page can navigate, and
    "the editor is loaded" and "the editor is the one at that id" have to be
    one answer rather than two that were true at different moments. `grafs` and
    `figures` are what the caller polls on: a long post arrives graf by graf,
    and every one of the counts the run makes later assumes the body it is
    about to replace has finished arriving.

    `match: false` is deliberately NOT the same as "wrong post": a title can be
    reworded too, and this run would be exactly how that reaches Medium. So the
    verdict, both titles and the size of what would be overwritten all come
    back, and the caller decides — `medium_draft.sh` stops and makes a human
    pass `--retitle`. Anything looser (a prefix or a similarity score) is worse
    than useless here: these articles are a series whose titles share long
    prefixes, and the realistic mistake is picking the neighbouring row out of
    the id table in PUBLISHING.md.
    """
    return """(() => {
  const editor = document.querySelector('%s');
  const titleEl = document.querySelector('%s');
  if (!editor || !titleEl) return JSON.stringify({ err: 'no Medium editor on this page' });
%s
  const want = %s, got = titleEl.innerText;
  return JSON.stringify({
    match: fold(want) === fold(got),
    want, got,
    url: location.href,
    grafs: editor.querySelectorAll('.graf').length,
    figures: editor.querySelectorAll('figure').length
  });
})()
""" % (EDITOR, TITLE, TITLE_FOLD, json.dumps(payload["title"], ensure_ascii=False))


def refill_js(payload):
    """Replace an existing post's entire body — figures included — in one paste.

    The alternative, patching graf by graf with medium_patch.py, was measured
    on this repo's tone pass: 19-38 scattered edits per article, 5-13 of them
    pure insertions that `replace` cannot express at all, and every one of them
    an anchor that eats real text when it lands a graf off. Repasting the whole
    body has one anchor-free selection instead, and hands the result to the
    same verify_draft.py gate that a new draft goes through.

    No `pick()` and no anchors on purpose: the range is "everything that is not
    the title", so there is nothing to match and nothing to guess wrong. A DOM
    Range from before the first body graf to after the last one covers the
    figures sitting between them, which is why this does not need a separate
    clear-then-paste pass — the paste replaces the selection, figures and all.

    The title is left standing. By the time this runs it is already this
    pack's, either because it always was (`medium_draft.sh` leaves a matching
    title alone rather than writing over a live post for nothing) or because
    `title_js` has just set it under `--retitle`. The structural guards below
    exist because taking the title with the body is the one thing this snippet
    could get catastrophically wrong.

    Three numbers come back for the caller to gate on, and every one of them is
    read AFTER the paste, because a count taken before it says what the post
    used to be rather than what this snippet just did:

    * `figuresLeft` — figures still in the editor. The whole mode assumes the
      range took the old figures out with the old prose, and that assumption
      had never been checked: `figuresRemoved` used to be the count from before
      the paste, so it read as "14 removed" whether or not a single one went.
      Everything downstream counts figures from zero, so one survivor turns the
      first upload wait into a 40s timeout that blames the network.
    * `titleOk` — the title the editor still shows, folded, is still this
      pack's. Not "is it non-empty": `graf--title` is assigned by position, so
      a selection that reached over the title leaves the first pasted graf
      promoted to the title, and a body sentence is not empty.
    * `title` — the string itself, for the human reading the failure.
    """
    return """(() => {
  const editor = document.querySelector('%s');
  const titleEl = document.querySelector('%s');
  if (!editor || !titleEl) return JSON.stringify({ err: 'no Medium editor on this page' });
%s
%s
  if (!body.length) return JSON.stringify({ err: 'no body grafs' });
  const first = body[0], last = body[body.length - 1];
  // If Medium ever renames the title graf, `titleEl` would be null (caught
  // above) or the title would sort *after* the first body graf, and the range
  // would start above it. Refuse rather than paste the body over the title.
  if (!(titleEl.compareDocumentPosition(first) & Node.DOCUMENT_POSITION_FOLLOWING))
    return JSON.stringify({ err: 'the title is not above the body' });
  const figuresBefore = editor.querySelectorAll('figure').length;
  editor.focus();
  const range = document.createRange();
  range.setStartBefore(first);
  range.setEndAfter(last);
  const sel = getSelection();
  sel.removeAllRanges();
  sel.addRange(range);
  const HTML = %s;
  const dt = new DataTransfer();
  dt.setData('text/html', HTML);
  dt.setData('text/plain', HTML.replace(/<[^>]+>/g, ''));
  first.dispatchEvent(new ClipboardEvent('paste', { clipboardData: dt, bubbles: true, cancelable: true }));
  // Read back after the paste, not before: what the caller has to know is
  // what this snippet just did, and it has to know it here, while there is
  // still nothing uploaded and the post is one Save away from being undone.
  const titleNow = document.querySelector('%s');
  const wantTitle = %s;
  return JSON.stringify({
    replaced: body.length,
    figuresBefore,
    figuresLeft: editor.querySelectorAll('figure').length,
    title: titleNow ? titleNow.innerText : '',
    titleOk: !!titleNow && fold(titleNow.innerText) === fold(wantTitle)
  });
})()
""" % (EDITOR, TITLE, TITLE_FOLD, BODY_GRAFS,
       json.dumps(payload["html"], ensure_ascii=False), TITLE,
       json.dumps(payload["title"], ensure_ascii=False))


def image_js(images_dir, name):
    """Paste one PNG at its placeholder.

    Medium inserts the figure *before* the paragraph holding the caret and leaves
    that paragraph alone, so the caller still has to delete the placeholder.
    """
    with open(os.path.join(images_dir, name), "rb") as fh:
        data = base64.b64encode(fh.read()).decode()
    return """(() => {
  const b64 = %s, name = %s;
  const bin = atob(b64);
  const bytes = new Uint8Array(bin.length);
  for (let i = 0; i < bin.length; i++) bytes[i] = bin.charCodeAt(i);
  const file = new File([bytes], name, { type: 'image/png' });
  const target = [...document.querySelectorAll('%s .graf')]
    .find(g => g.innerText.includes(%s));
  if (!target) return JSON.stringify({ err: 'slot not found', name });
%s
  const dt = new DataTransfer();
  dt.items.add(file);
  target.dispatchEvent(new ClipboardEvent('paste', { clipboardData: dt, bubbles: true, cancelable: true }));
  return JSON.stringify({ name, bytes: bytes.length });
})()
""" % (json.dumps(data), json.dumps(name), EDITOR, json.dumps(SLOT_MARK % name), PASTE)


def slot_js(name):
    """Select a placeholder paragraph so two Backspace presses can remove it."""
    return """(() => {
  const marker = %s;
  const target = [...document.querySelectorAll('%s .graf')]
    .find(g => g.innerText.includes(marker));
  if (!target) return JSON.stringify({ err: 'slot not found' });
%s
  return JSON.stringify({ selected: sel.toString().slice(0, 60) });
})()
""" % (json.dumps(SLOT_MARK % name), EDITOR, PASTE)


def state_js():
    """Count everything the driver gates on, in one read.

    Every checkpoint after the body paste asks the same four questions, and
    they used to be three separate inline queries in the shell that had drifted
    into counting different things: the upload wait counted `figure img` while
    the final gate counted `figure`, so a figure whose <img> never arrived was
    invisible to one and present to the other. One snippet, one answer.

    * `figures` / `imgs` — both, deliberately. They agree on a healthy editor;
      when they do not, an image is missing from a figure that exists, which is
      exactly the state the upload wait is there to sit out.
    * `pending` — imgs still pointing at a blob: URL, i.e. not uploaded yet.
    * `slots` — placeholder markers still in the text. It is the count that
      decides whether two Backspaces are safe to send, so it has to come from
      the same definition of the marker that wrote it (md2medium.SLOT_MARK),
      not from a literal retyped in the shell.
    """
    return """(() => {
  const editor = document.querySelector('%s');
  if (!editor) return JSON.stringify({ err: 'no Medium editor on this page' });
  const imgs = [...editor.querySelectorAll('figure img')];
  return JSON.stringify({
    figures: editor.querySelectorAll('figure').length,
    imgs: imgs.length,
    pending: imgs.filter(x => !/cdn-images|miro\\.medium/.test(x.src)).length,
    slots: (editor.innerText.match(new RegExp(%s, 'g')) || []).length
  });
})()
""" % (EDITOR, json.dumps(SLOT_MARK.split("%s")[0]))


def saved_js():
    """What Medium's own metabar says about the save.

    Everything else in this file reads the DOM the browser is holding. That is
    not the same as what Medium stored: autosave is asynchronous, and a run
    that navigated away as soon as its in-editor checks passed lost the tail of
    it -- posts that had just been verified as complete came back from a reload
    with figures missing and IMGSLOT text still in them. `.js-metabarMessage`
    is the editor's own indicator, and it is the only thing on the page that
    knows whether the write finished.

    The message is returned raw as well as classified: "Saving failed because
    someone is also editing" has to reach the operator verbatim, because the
    fix for it (close the other editor) is not something the driver can do.

    Classifying here rather than by glob in the shell, because the raw text is
    not one word. A draft's metabar reads "DraftSaved" -- the "Draft" label and
    the status live in the same element, and textContent runs them together --
    while a published post's reads "Saved". Matching the literal "Saved" looked
    right and silently never matched a draft: eight scheduled posts polled to
    the timeout and reported failure after saving perfectly well.
    """
    return """(() => {
  const el = document.querySelector('.js-metabarMessage');
  if (!el) return JSON.stringify({ err: 'no save indicator on this page' });
  const message = (el.textContent || '').trim();
  return JSON.stringify({
    message,
    // "Saved" and "DraftSaved"; not "Saving…", not "Saving failed ...".
    saved: /Saved$/.test(message) && !/Saving/.test(message),
    failed: /failed/i.test(message)
  });
})()
"""


def mark_js(token):
    """Leave a token on `window` that only a real page load can clear.

    The re-read is only worth anything if the page actually reloaded, and every
    indirect way of establishing that has now failed on the real thing: `goto`
    to the current URL answers net::ERR_ABORTED, `goto about:blank` hits
    Medium's beforeunload, and `reload` overruns browse's 15s timeout on an
    editor this size while still, sometimes, reloading. Trusting the command's
    exit status would mean a timeout is read as "did not reload" when it did,
    and -- far worse -- a silent no-op read as "reloaded" when it did not,
    which puts the same DOM in front of both reads and passes vacuously.

    A token on `window` settles it directly: a document that survived carries
    it, a freshly parsed one cannot.
    """
    return "(() => { window.__mediumRefill = %s; return JSON.stringify({ marked: true }); })()\n" % json.dumps(token)


def stale_js(token):
    """Whether the page still carries the mark, i.e. never reloaded."""
    return "(() => JSON.stringify({ stale: window.__mediumRefill === %s }))()\n" % json.dumps(token)


def dump_js():
    """The editor's side of the block-by-block comparison, for verify_draft.py.

    This used to be a one-liner inlined in medium_draft.sh, which is how its
    divider count came to be wrong. Medium opens *every* section with a
    structural `<div class="section-divider"><hr></div>`, the first section
    included, so `querySelectorAll('hr')` returns one more than the number of
    breaks the article actually asks for: an 11-section post has 11 `<hr>` and
    10 breaks. Comparing that raw count against the payload's `<hr>` lines made
    a correct post fail by exactly one, every time.

    Counting sections and subtracting one says what is meant, and does not
    depend on how Medium marks the divider up. `Math.max(0, ...)` because an
    editor holding no section at all should report no breaks rather than -1.
    """
    return """(() => {
  const editor = document.querySelector('%s');
  if (!editor) return JSON.stringify({ err: 'no Medium editor on this page' });
  const g = [...editor.querySelectorAll('.graf')];
  return JSON.stringify({
    texts: g.filter(x => x.tagName !== 'FIGURE').map(x => x.innerText),
    tags: g.map(x => x.tagName),
    links: editor.querySelectorAll('a').length,
    dividers: Math.max(0, editor.querySelectorAll('section').length - 1)
  });
})()
""" % EDITOR


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    kind = sys.argv[1]
    if kind not in ("selectors", "state", "dump", "saved") and len(sys.argv) < 3:
        sys.exit("%s needs an argument\n\n%s" % (kind, __doc__))
    if kind == "title":
        print(title_js(json.load(open(sys.argv[2], encoding="utf-8"))))
    elif kind == "body":
        print(body_js(json.load(open(sys.argv[2], encoding="utf-8"))))
    elif kind == "identify":
        print(identify_js(json.load(open(sys.argv[2], encoding="utf-8"))))
    elif kind == "refill":
        print(refill_js(json.load(open(sys.argv[2], encoding="utf-8"))))
    elif kind == "image":
        print(image_js(sys.argv[2], sys.argv[3]))
    elif kind == "slot":
        print(slot_js(sys.argv[2]))
    elif kind == "state":
        print(state_js())
    elif kind == "dump":
        print(dump_js())
    elif kind == "saved":
        print(saved_js())
    elif kind == "mark":
        print(mark_js(sys.argv[2]))
    elif kind == "stale":
        print(stale_js(sys.argv[2]))
    elif kind == "selectors":
        # So medium_draft.sh does not repeat these literals.
        # Not EDITOR: that is the standard text-editor variable.
        print("EDITOR_SEL=%s" % EDITOR)
        print("SLOT_PREFIX=%s" % SLOT_MARK.split("%s")[0])
    else:
        sys.exit("unknown snippet: " + kind)


if __name__ == "__main__":
    main()
