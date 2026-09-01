#!/usr/bin/env python3
"""Emit the browser snippets that drive Medium's editor, for `browse eval`.

Medium's classic editor does not check `event.isTrusted`, so a synthetic
ClipboardEvent carrying a DataTransfer is the whole trick: `text/html` on the
DataTransfer inserts formatted rich text in one shot, and a File added to
`dataTransfer.items` uploads an image. Typing the title character by character
does not work reliably (the placeholder span swallows the first few keystrokes),
so the title goes in as a paste too.

Usage:
    python3 tools/medium_js.py title  /tmp/payload.json        > /tmp/title.js
    python3 tools/medium_js.py body   /tmp/payload.json        > /tmp/body.js
    python3 tools/medium_js.py image  <images_dir> <file.png>  > /tmp/image.js
    python3 tools/medium_js.py slot   <file.png>               > /tmp/slot.js
    python3 tools/medium_js.py selectors                       # shell eval
"""

import base64
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from md2medium import SLOT_MARK  # one definition of the placeholder format

EDITOR = ".postArticle-content"

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


def title_js(payload):
    return """(() => {
  const target = document.querySelector('h3.graf--title');
  if (!target) return JSON.stringify({ err: 'no title field' });
%s
  const dt = new DataTransfer();
  dt.setData('text/plain', %s);
  target.dispatchEvent(new ClipboardEvent('paste', { clipboardData: dt, bubbles: true, cancelable: true }));
  return JSON.stringify({ title: document.querySelector('h3.graf--title').innerText });
})()
""" % (PASTE, json.dumps(payload["title"], ensure_ascii=False))


def body_js(payload):
    """Replace everything below the title with the article body.

    Selecting the existing body grafs first means this is safe to re-run: the
    paste overwrites the selection instead of appending a second copy.
    """
    return """(() => {
  const editor = document.querySelector('%s');
  const body = [...editor.querySelectorAll('.graf')].filter(g => !g.classList.contains('graf--title'));
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
""" % (EDITOR, json.dumps(payload["html"], ensure_ascii=False))


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


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    kind = sys.argv[1]
    if kind != "selectors" and len(sys.argv) < 3:
        sys.exit("%s needs an argument\n\n%s" % (kind, __doc__))
    if kind == "title":
        print(title_js(json.load(open(sys.argv[2], encoding="utf-8"))))
    elif kind == "body":
        print(body_js(json.load(open(sys.argv[2], encoding="utf-8"))))
    elif kind == "image":
        print(image_js(sys.argv[2], sys.argv[3]))
    elif kind == "slot":
        print(slot_js(sys.argv[2]))
    elif kind == "selectors":
        # So medium_draft.sh does not repeat these literals.
        # Not EDITOR: that is the standard text-editor variable.
        print("EDITOR_SEL=%s" % EDITOR)
        print("SLOT_PREFIX=%s" % SLOT_MARK.split("%s")[0])
    else:
        sys.exit("unknown snippet: " + kind)


if __name__ == "__main__":
    main()
