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
spaces (U+200A), so `A — B` comes back with invisible padding around the dash.
That is its house typography applied to every author, not lost content. Only
that rewrite is normalised away — ordinary word spacing is still compared, so a
paste that silently welds words together is still a mismatch.

A double dash `——` never reaches here: md2medium.py rejects it at conversion
time, because this very normalisation would hide it. Folding the spacing is
what makes Medium's padding invisible to the comparison, so a `——` rendered
as `— —` would compare equal and ship unnoticed.

Links are counted separately. innerText cannot see an <a>, so a paste that
lost every hyperlink in the article reads as identical text; the anchor count
is the only signal that it happened.

Figure placement is checked separately too, for the same reason: the text
comparison skips figures entirely, so an image landing in the wrong section
still reports "all blocks match". Getting each image next to its own paragraph
is the whole point of the placeholder dance, so the positions are compared.

Section dividers are counted for a third variant of the same reason. A `<hr>`
is not a graf, so neither the text pass nor the placement pass can see one: an
article with a divider too many or too few compared equal on every check here.
That was harmless while the only way in was a paste into an empty new story,
which builds every section from the payload. `medium_draft.sh --post` is not
that: its range runs from the first body graf to the last, across the 11 to 17
`<section>` wrappers Medium makes out of these articles' 10 to 16 dividers,
and both ends of that range are partially selected containers. An empty
section or an orphan divider left behind at either end is invisible to
everything else in this file.

The editor side can be either a bare JSON array of graf texts, or an object
{"texts": [...], "tags": [...], "links": N, "dividers": N} to enable the extra
checks. Each of the three extras is skipped, with a note, when the editor
payload does not carry its count.
"""

import html
import json
import re
import sys

# Medium's code blocks carry a language-picker label in innerText.
LANG_LABEL = re.compile(r"\nAuto \([^)]*\)$")
TAGS = re.compile(r"</?(p|h\d|blockquote|pre|code|strong|em|a|li|ul|ol)\b[^>]*>")
# A figure reaches the payload one of two ways: as a placeholder the driver
# will replace with an upload, or -- with --reuse-figures -- already written as
# a <figure> pointing at an image Medium is serving for this post. Both occupy
# one graf slot and carry no text, so both have to count here. Recognising only
# the placeholder made the reuse mode's figure-placement check expect no
# figures at all, and then report the correct ones as a mismatch.
SLOT_P = re.compile(r"^(?:<p>IMGSLOT-.*-ENDSLOT</p>|<figure>.*</figure>)$")
ANCHOR = re.compile(r"<a\b[^>]*>")

THIN_SPACE = "\u2009"
HAIR_SPACE = "\u200a"   # what Medium packs around an em dash
BOM = "\ufeff"
NBSP = "\u00a0"
EM_DASH = "\u2014"
# Collapse whatever Medium put around an em dash back to the bare dash.
EM_DASH_RUN = re.compile(r"[ \t]*%s[ \t]*" % EM_DASH)
# Medium also turns the hyphen between two digits into an en dash (2026-07-10
# comes back as 2026–07–10). Typography, not content: fold it on the editor
# side. Only between digits, so an en dash the author typed between words is
# still compared as-is.
EN_DASH_BETWEEN_DIGITS = re.compile(r"(?<=\d)\u2013(?=\d)")
# And a caret followed by digits becomes superscript digits (pass^5 -> pass⁵,
# pass^20 -> pass²⁰; pass^k is left alone). Fold the superscripts back.
SUPERSCRIPT_DIGITS = re.compile("[\u2070\u00b9\u00b2\u00b3\u2074-\u2079]+")
SUPERSCRIPT_TO_DIGIT = str.maketrans("\u2070\u00b9\u00b2\u00b3\u2074\u2075\u2076\u2077\u2078\u2079", "0123456789")


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


def expected_dividers(payload):
    """How many section breaks the payload asks for.

    Read from the same lines graf_sequence() drops on the way past, so the two
    cannot disagree about what a divider is.
    """
    return sum(1 for line in payload["html"].split("\n") if line == "<hr>")


def normalise(text, from_html, in_code=False):
    """Fold the rewrites Medium applies, so only real differences remain.

    `in_code` turns the typography folds OFF. Medium applies none of them
    inside a <pre> (that is why a CJK `——` survives there intact), so folding
    them in a code block cannot fix a Medium rewrite — it can only hide a real
    one. A curled quote in a shipped snippet is a syntax error for whoever
    copies it, and this comparison is the only thing that would catch it.
    """
    if from_html:
        # Strip tags BEFORE unescaping, so a code block quoting <p>hi</p> keeps
        # its own content instead of having it eaten as markup.
        text = html.unescape(TAGS.sub("", text))
    text = LANG_LABEL.sub("", text)   # the language picker label is real, even in code
    if in_code:
        # Whitespace still collapses: Medium's own indentation handling is not
        # something this gate has ever policed, and tightening it here would be
        # a separate change with its own failure modes.
        text = re.sub(r"[ \t]+", " ", text)
        return re.sub(r"[ \t]*\n[ \t]*", "\n", text).strip()
    for spacer in (THIN_SPACE, HAIR_SPACE, BOM):
        text = text.replace(spacer, "")
    text = text.replace(NBSP, " ").replace("\u2019", "'").replace("\u2018", "'")
    # Curly doubles too. Medium curls both kinds; only the singles were folded
    # here, which held up for as long as every article was Chinese and quoted
    # with 「」. The first English draft turned 15 correct blocks into
    # mismatches on nothing but quote shape.
    text = text.replace("\u201c", '"').replace("\u201d", '"')
    text = EM_DASH_RUN.sub(EM_DASH, text)
    text = EN_DASH_BETWEEN_DIGITS.sub("-", text)
    text = SUPERSCRIPT_DIGITS.sub(lambda m: "^" + m.group(0).translate(SUPERSCRIPT_TO_DIGIT), text)
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

    # Which blocks are code is decided from the payload (the editor side has
    # had its tags stripped by then), and applied to both sides by position.
    raw = expected_blocks(payload)
    in_code = [b.startswith("<pre>") for b in raw]
    expected = [normalise(b, True, c) for b, c in zip(raw, in_code)]
    got = [normalise(g, False, in_code[i] if i < len(in_code) else False)
           for i, g in enumerate(actual)]

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

    # Neither pass above can see a divider: it is not a graf and carries no
    # text. A refill's range crosses every section in the article, so a section
    # left empty or a divider left orphaned at either end of it would otherwise
    # ship with every other check reporting a match.
    want_hrs = expected_dividers(payload)
    if "dividers" in editor:
        got_hrs = editor["dividers"]
        if got_hrs != want_hrs:
            print("\ndividers: expected %d section breaks, editor has %d"
                  % (want_hrs, got_hrs))
            problems += 1
        else:
            print("dividers: %d, all accounted for" % want_hrs)
    elif want_hrs:
        print("dividers: %d expected — editor payload carried no count, "
              "not checked" % want_hrs)

    if problems:
        print("\n%d problem(s): %d block mismatch(es)" % (problems, bad))
        sys.exit(1)
    print("all blocks match")


if __name__ == "__main__":
    main()
