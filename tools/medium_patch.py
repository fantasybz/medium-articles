#!/usr/bin/env python3
"""Emit browser snippets that edit an *already published* Medium post.

`medium_draft.sh` can only build a new draft. Once a post is live the only way
to change it is Medium's editor, and the same synthetic-paste trick that fills a
draft (see `medium_js.py`) also works surgically: select a run of grafs, paste
replacement HTML over the selection.

The dangerous part is the selection, not the paste. An anchor that matches two
grafs — or none — would silently select the wrong run and the paste would eat
real article text, on a post readers can already see. So every snippet here
resolves its anchors to *exactly one* graf each and returns an error instead of
guessing, and `--dry` reports what would be replaced without touching anything.

Usage:
    python3 tools/medium_patch.py html   <fragment.md>              > /tmp/frag.html
    python3 tools/medium_patch.py find   <anchor>                   > /tmp/find.js
    python3 tools/medium_patch.py replace <start> <end> <html-file> > /tmp/rep.js
    python3 tools/medium_patch.py replace <start> <end> <f> --dry   > /tmp/rep.js
    python3 tools/medium_patch.py image  <anchor> <file.png>        > /tmp/img.js
    python3 tools/medium_patch.py drop   <anchor>                   > /tmp/drop.js
    python3 tools/medium_patch.py subst  <from> <to>                > /tmp/sub.js

`start` and `end` are substrings of the first and last graf to replace; pass the
same string twice to replace a single graf. Anchors are matched against
`innerText`, so use text as it renders, not as it appears in markdown.
"""

import base64
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from md2medium import convert

EDITOR = ".postArticle-content"

# Medium pads em dashes with a hair space (see PUBLISHING.md), so an anchor
# copied from article.md would not match the rendered innerText. Callers get a
# clearer failure if they simply avoid em dashes in anchors, but normalising the
# common invisibles costs nothing and removes a whole class of near-misses.
# Escapes, not the literal characters: they are invisible in an editor, so a
# stray edit to the class would silently change what every anchor matches.
# Same set verify_draft.py folds away (hair space, thin space, BOM, NBSP).
#
# Spacing around an em dash goes too, for the same reason verify_draft.py does
# it. Medium renders `A — B` as `A<hair>—<hair>B` with no ordinary spaces, so
# dropping the hair spaces alone leaves `A—B` in the editor against `A — B` in
# an anchor copied from article.md, and the anchor silently matches nothing.
NORMALISE = r"""
  const norm = s => s.replace(/[\u200A\u2009\uFEFF\u00A0]/g, '')
                     .replace(/[ \t]*\u2014[ \t]*/g, '\u2014')
                     .replace(/\s+/g, ' ').trim();
"""

# Resolve one anchor to exactly one graf index. Declares `pick` for the callers.
PICK = r"""
  const grafs = [...document.querySelectorAll('%s .graf')];
  const pick = (anchor) => {
    const want = norm(anchor);
    const hits = [];
    grafs.forEach((g, i) => { if (norm(g.innerText).includes(want)) hits.push(i); });
    return hits;
  };
""" % EDITOR


def fragment_html(markdown):
    """Markdown fragment to Medium HTML, using the same converter as the body.

    `convert` wants a title line and returns it separately, so a throwaway one
    is prepended and dropped; that keeps one implementation of every block rule
    rather than a second, subtly different one for patches.
    """
    return convert("# _\n\n" + markdown.lstrip("\n"))["html"]


def find_js(anchor):
    return """(() => {
%s%s
  const found = pick(%s);
  return JSON.stringify({
    count: found.length,
    at: found,
    texts: found.map(i => grafs[i].innerText.slice(0, 90)),
    tags: found.map(i => grafs[i].tagName + '.' + grafs[i].className.split(' ').find(c => c.startsWith('graf--')))
  });
})()
""" % (NORMALISE, PICK, json.dumps(anchor, ensure_ascii=False))


def replace_js(start, end, html, dry=False):
    """Select grafs [start..end] inclusive and paste `html` over them."""
    return """(() => {
%s%s
  const a = pick(%s), b = pick(%s);
  if (a.length !== 1) return JSON.stringify({ err: 'start anchor matched ' + a.length, at: a });
  if (b.length !== 1) return JSON.stringify({ err: 'end anchor matched ' + b.length, at: b });
  if (b[0] < a[0]) return JSON.stringify({ err: 'end graf is before start graf', a: a[0], b: b[0] });
  const firstGraf = grafs[a[0]], lastGraf = grafs[b[0]];
  const covered = grafs.slice(a[0], b[0] + 1).map(g => g.innerText.slice(0, 70));
  if (%s) return JSON.stringify({ dry: true, from: a[0], to: b[0], count: covered.length, covered });
  document.querySelector('%s').focus();
  const range = document.createRange();
  range.setStartBefore(firstGraf);
  range.setEndAfter(lastGraf);
  const sel = getSelection();
  sel.removeAllRanges();
  sel.addRange(range);
  const HTML = %s;
  const dt = new DataTransfer();
  dt.setData('text/html', HTML);
  dt.setData('text/plain', HTML.replace(/<[^>]+>/g, ''));
  firstGraf.dispatchEvent(new ClipboardEvent('paste', { clipboardData: dt, bubbles: true, cancelable: true }));
  return JSON.stringify({ replaced: covered.length, from: a[0], to: b[0] });
})()
""" % (NORMALISE, PICK,
       json.dumps(start, ensure_ascii=False), json.dumps(end, ensure_ascii=False),
       "true" if dry else "false", EDITOR, json.dumps(html, ensure_ascii=False))


def image_js(anchor, path):
    """Paste a PNG just above the graf matching `anchor`.

    Replacing a live figure is a two-step move: this puts the new image in, and
    `drop_js` removes the old one afterwards. Medium inserts the figure *before*
    the caret's graf and leaves that graf untouched, so the anchor should be the
    paragraph following the figure being replaced.
    """
    with open(path, "rb") as fh:
        data = base64.b64encode(fh.read()).decode()
    return """(() => {
%s%s
  const hit = pick(%s);
  if (hit.length !== 1) return JSON.stringify({ err: 'anchor matched ' + hit.length, at: hit });
  const target = grafs[hit[0]];
  const bin = atob(%s);
  const bytes = new Uint8Array(bin.length);
  for (let i = 0; i < bin.length; i++) bytes[i] = bin.charCodeAt(i);
  const file = new File([bytes], %s, { type: 'image/png' });
  document.querySelector('%s').focus();
  const range = document.createRange();
  range.selectNodeContents(target);
  const sel = getSelection();
  sel.removeAllRanges();
  sel.addRange(range);
  const dt = new DataTransfer();
  dt.items.add(file);
  target.dispatchEvent(new ClipboardEvent('paste', { clipboardData: dt, bubbles: true, cancelable: true }));
  return JSON.stringify({ at: hit[0], bytes: bytes.length });
})()
""" % (NORMALISE, PICK, json.dumps(anchor, ensure_ascii=False), json.dumps(data),
       json.dumps(os.path.basename(path)), EDITOR)


def drop_js(anchor):
    """Select the figure whose <img> src matches `anchor`, ready for Backspace.

    Figures hold no text, so they cannot be found the way every other graf is;
    the anchor here is matched against the image src instead. As with `replace`,
    an anchor that hits two figures is an error rather than a guess — a stray
    Backspace on the wrong node eats a real image on a published post.
    """
    return """(() => {
  const figs = [...document.querySelectorAll('%s figure')];
  const want = %s;
  const hits = figs.filter(f => ((f.querySelector('img') || {}).src || '').includes(want));
  if (hits.length !== 1) return JSON.stringify({ err: 'src matched ' + hits.length });
  document.querySelector('%s').focus();
  const range = document.createRange();
  range.selectNode(hits[0]);
  const sel = getSelection();
  sel.removeAllRanges();
  sel.addRange(range);
  return JSON.stringify({ selected: ((hits[0].querySelector('img') || {}).src || '').split('/').pop() });
})()
""" % (EDITOR, json.dumps(anchor, ensure_ascii=False), EDITOR)


def subst_js(old, new):
    """Replace the first literal `old` with `new`, reporting how many remain.

    For fixing a string that recurs all through a story — `——` was the case
    this exists for — where re-pasting whole grafs would be absurd and would
    also have to rebuild every figure. This selects just the offending
    characters inside their own text node, so inline links, marks and code
    blocks either side are untouched.

    One at a time, on purpose: the caller loops until `remaining` is 0, and
    each pass re-reads the DOM, so an edit that shifts the tree cannot make
    a stale offset point at the wrong characters.
    """
    return """(() => {
  const editor = document.querySelector('%s');
  const OLD = %s, NEW = %s;
  const walk = () => {
    const w = document.createTreeWalker(editor, NodeFilter.SHOW_TEXT);
    const found = [];
    let node;
    while ((node = w.nextNode())) {
      let at = node.data.indexOf(OLD);
      while (at !== -1) { found.push([node, at]); at = node.data.indexOf(OLD, at + OLD.length); }
    }
    return found;
  };
  const hits = walk();
  if (!hits.length) {
    // innerText still showing it means the match straddles two text nodes,
    // which this cannot fix — say so rather than reporting a clean finish.
    const split = editor.innerText.includes(OLD);
    return JSON.stringify({ remaining: 0, split });
  }
  const [node, at] = hits[0];
  editor.focus();
  const range = document.createRange();
  range.setStart(node, at);
  range.setEnd(node, at + OLD.length);
  const sel = getSelection();
  sel.removeAllRanges();
  sel.addRange(range);
  if (sel.toString() !== OLD) return JSON.stringify({ err: 'selected ' + JSON.stringify(sel.toString()) });
  const dt = new DataTransfer();
  dt.setData('text/plain', NEW);
  node.parentElement.dispatchEvent(new ClipboardEvent('paste', { clipboardData: dt, bubbles: true, cancelable: true }));
  return JSON.stringify({ replaced: 1, remaining: walk().length });
})()
""" % (EDITOR, json.dumps(old, ensure_ascii=False), json.dumps(new, ensure_ascii=False))


def main():
    args = [a for a in sys.argv[1:] if a != "--dry"]
    dry = "--dry" in sys.argv
    if not args:
        sys.exit(__doc__)
    kind = args[0]
    if kind == "html":
        if len(args) != 2:
            sys.exit("html needs a markdown file")
        with open(args[1], encoding="utf-8") as fh:
            sys.stdout.write(fragment_html(fh.read()))
    elif kind == "find":
        if len(args) != 2:
            sys.exit("find needs an anchor")
        print(find_js(args[1]))
    elif kind == "image":
        if len(args) != 3:
            sys.exit("image needs <anchor> <file.png>")
        print(image_js(args[1], args[2]))
    elif kind == "subst":
        if len(args) != 3:
            sys.exit("subst needs <from> <to>")
        print(subst_js(args[1], args[2]))
    elif kind == "drop":
        if len(args) != 2:
            sys.exit("drop needs a figure src fragment")
        print(drop_js(args[1]))
    elif kind == "replace":
        if len(args) != 4:
            sys.exit("replace needs <start> <end> <html-file>")
        with open(args[3], encoding="utf-8") as fh:
            print(replace_js(args[1], args[2], fh.read(), dry))
    else:
        sys.exit("unknown snippet: " + kind)


if __name__ == "__main__":
    main()
