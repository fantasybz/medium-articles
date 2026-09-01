#!/usr/bin/env python3
"""Diff what is actually in the Medium editor against the converted payload.

Run this before publishing. It is the only way to know that a 100+ block paste
landed intact, and it catches the failure that matters most: content silently
dropped or reordered somewhere in the middle of a long article.

Scope, stated honestly: this compares the editor against md2medium.py's output,
not against medium-paste.md. A conversion bug is invisible here by construction
— that is what tools/test_tools.py covers. What this catches is everything that
can go wrong between the converted payload and the editor.

Usage:
    browse --headed js "JSON.stringify([...document.querySelectorAll(
        '.postArticle-content .graf')].filter(g => g.tagName !== 'FIGURE')
        .map(g => g.innerText))" > /tmp/grafs.json
    python3 tools/verify_draft.py /tmp/payload.json /tmp/grafs.json

Exits non-zero on any mismatch.

Medium rewrites some whitespace on purpose: it wraps every em dash in hair
spaces (U+200A), so the article's `——` comes back looking like `— —`. That is
its house typography applied to every author, not lost content. Only that
rewrite is normalised away — ordinary word spacing is still compared, so a
paste that silently welds words together is still a mismatch.

Links are counted separately. innerText cannot see an <a>, so a paste that
lost every hyperlink in the article reads as identical text; the anchor count
is the only signal that it happened.

Figure placement is checked separately too, for the same reason: the text
comparison skips figures entirely, so an image landing in the wrong section
still reports "all blocks match". Getting each image next to its own paragraph
is the whole point of the placeholder dance, so the positions are compared.

The editor side can be either a bare JSON array of graf texts, or an object
{"texts": [...], "tags": [...], "links": N} to enable the extra checks.
"""

import html
import json
import re
import sys

# Medium's code blocks carry a language-picker label in innerText.
LANG_LABEL = re.compile(r"\nAuto \([^)]*\)$")
TAGS = re.compile(r"</?(p|h\d|blockquote|pre|code|strong|em|a|li|ul|ol)\b[^>]*>")
SLOT_P = re.compile(r"^<p>IMGSLOT-.*-ENDSLOT</p>$")
ANCHOR = re.compile(r"<a\b[^>]*>")

THIN_SPACE = "\u2009"
HAIR_SPACE = "\u200a"   # what Medium packs around an em dash
BOM = "\ufeff"
NBSP = "\u00a0"
EM_DASH = "\u2014"
# Collapse whatever Medium put around an em dash back to the bare dash.
EM_DASH_RUN = re.compile(r"[ \t]*%s[ \t]*" % EM_DASH)


def graf_sequence(payload):
    """Every graf Medium will create, in order, slots included.

    Both the text comparison and the figure-placement check read from this one
    list; computing them separately is how they drift apart.
    """
    blocks = []
    for line in payload["html"].split("\n"):
        if line == "<hr>":
            continue          # a divider is a section break, not a graf
        if blocks and blocks[-1].startswith("<pre>") \
                and not blocks[-1].rstrip().endswith("</pre>"):
            blocks[-1] += "\n" + line   # still inside a multi-line code block
        elif line.startswith("<ul>") or line.startswith("<ol>"):
            blocks += re.findall(r"<li>(.*?)</li>", line, re.S)
        else:
            blocks.append(line)
    # Escaped so the from_html unescape round-trips back to the raw title.
    return [html.escape(payload["title"], quote=False)] + blocks


def expected_blocks(payload):
    """The text grafs only — slots become figures and carry no text."""
    return [b for b in graf_sequence(payload) if not SLOT_P.match(b)]


def expected_figure_positions(payload):
    """Indices, among ALL grafs, where a figure should sit."""
    return [i for i, b in enumerate(graf_sequence(payload)) if SLOT_P.match(b)]


def normalise(text, from_html):
    if from_html:
        # Strip tags BEFORE unescaping, so a code block quoting <p>hi</p> keeps
        # its own content instead of having it eaten as markup.
        text = html.unescape(TAGS.sub("", text))
    text = LANG_LABEL.sub("", text)
    for spacer in (THIN_SPACE, HAIR_SPACE, BOM):
        text = text.replace(spacer, "")
    text = text.replace(NBSP, " ").replace("\u2019", "'").replace("\u2018", "'")
    text = EM_DASH_RUN.sub(EM_DASH, text)
    # Collapse runs of spaces, but never delete them: welded-together words are
    # a real content loss and must not compare equal.
    text = re.sub(r"[ \t]+", " ", text)
    return re.sub(r"[ \t]*\n[ \t]*", "\n", text).strip()


def anchor_count(payload):
    return len(ANCHOR.findall(payload["html"]))


def load_editor(path):
    """Read what the browser reported back.

    Accepts a bare array of graf texts, or an object carrying the tag list and
    link count as well so the placement and link checks can run.
    """
    with open(path, encoding="utf-8") as fh:
        raw = fh.read()
    # browse wraps some page output in UNTRUSTED CONTENT markers.
    found = re.search(r"(\{.*\}|\[.*\])", raw, re.S)
    if not found:
        sys.exit("no JSON in %s — did the browse js call fail?" % path)
    try:
        data = json.loads(found.group(1))
    except ValueError as exc:
        sys.exit("could not parse %s: %s" % (path, exc))
    return {"texts": data} if isinstance(data, list) else data


def main():
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    with open(sys.argv[1], encoding="utf-8") as fh:
        payload = json.load(fh)
    editor = load_editor(sys.argv[2])
    actual = editor.get("texts", [])

    expected = [normalise(b, True) for b in expected_blocks(payload)]
    got = [normalise(g, False) for g in actual]

    print("expected %d text blocks, editor has %d" % (len(expected), len(got)))
    bad = 0
    for i in range(max(len(expected), len(got))):
        want = expected[i] if i < len(expected) else "<missing>"
        have = got[i] if i < len(got) else "<missing>"
        if want != have:
            bad += 1
            print("\nblock %d differs" % i)
            print("  source: %r" % want[:200])
            print("  editor: %r" % have[:200])

    problems = bad

    # innerText is blind to <a>, so link loss looks like a perfect match.
    want_links = anchor_count(payload)
    if "links" in editor:
        got_links = editor["links"]
        if got_links != want_links:
            print("\nlinks: expected %d, editor has %d" % (want_links, got_links))
            problems += 1
        else:
            print("links: %d, all present" % want_links)
    elif want_links:
        print("links: %d expected — editor payload carried no count, not checked"
              % want_links)

    # Placement, not just count: the text pass skips figures entirely.
    want_figs = expected_figure_positions(payload)
    if "tags" in editor:
        got_figs = [i for i, t in enumerate(editor["tags"]) if t == "FIGURE"]
        if got_figs != want_figs:
            print("\nfigures: expected at graf %s, editor has %s"
                  % (want_figs, got_figs))
            problems += 1
        else:
            print("figures: %d, each in its own slot" % len(want_figs))
    elif want_figs:
        print("figures: %d expected — editor payload carried no tag list, "
              "placement not checked" % len(want_figs))

    if problems:
        print("\n%d problem(s): %d block mismatch(es)" % (problems, bad))
        sys.exit(1)
    print("all blocks match")


if __name__ == "__main__":
    main()
