#!/usr/bin/env python3
"""Turn a `publish/medium-paste.md` into the payload the Medium editor wants.

Medium's editor accepts pasted HTML, so the reliable way in is one paste of the
whole body rather than typing or pasting plain text and fixing formatting by hand.
This emits that HTML plus the title and the ordered image list.

Usage:
    python3 tools/md2medium.py 2026-09-agentic-engineering-platform --out /tmp/payload.json

Output JSON: {"title": str, "html": str, "images": [filename, ...]}

Two mappings worth knowing, both learned the hard way:

* Medium collapses <h1>, <h2> and <h3> onto the same `graf--h3` (big heading) and
  only drops to `graf--h4` (small heading) at <h4>. So `##` emits <h2> and `###`
  emits <h4>, or every subheading comes out the same size as its section title.
  Every other level (a second `#`, or `####` and deeper) also becomes <h4> —
  Medium has exactly two heading sizes, so there is nowhere else to put them.
* A blank line inside <pre> splits the code block into several separate boxes.
  Blank lines become a single space to keep one block.
"""

import argparse
import html
import json
import os
import re
import sys

# The 📌 lines in medium-paste.md, e.g. 📌【在此插入圖 diagram-01.png】
SLOT_RE = re.compile(r"^📌【在此插入[圖表]\s*([A-Za-z0-9\-]+\.png)】$")
# Marker left in the pasted body; the image insert step finds and replaces it.
SLOT_MARK = "IMGSLOT-%s-ENDSLOT"

BLOCK_START = re.compile(r"^(#{1,6}\s|[-*]\s|\d+\.\s|>|```|-{3,}$|📌)")

# Medium pads every em dash with a hair space (U+200A), so a CJK double dash
# `——` renders as `— —`: a visible gap in the middle of what should be one
# unbroken stroke. Nothing downstream can undo it — verify_draft.py folds that
# spacing away precisely so it does not read as a paste failure, which means a
# double dash would otherwise ship unnoticed. Use a single `—` instead.
DOUBLE_DASH = re.compile("\u2014{2,}")


def inline(text):
    """Markdown inline syntax to HTML, code spans protected from escaping."""
    codes = []

    def stash(m):
        codes.append(m.group(1))
        return "\x00%d\x00" % (len(codes) - 1)

    text = re.sub(r"`([^`]+)`", stash, text)
    text = html.escape(text, quote=False)
    # `text` has already been through html.escape, so & is already &amp; in the
    # URL too. Escaping it again ships &amp;amp; and a link that 404s; only the
    # quote still needs handling, because it closes the href attribute.
    text = re.sub(
        r"\[([^\]]+)\]\(((?:[^()]|\([^()]*\))*)\)",
        lambda m: '<a href="%s">%s</a>' % (m.group(2).replace('"', "&quot;"), m.group(1)),
        text,
    )
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"(?<![\*\w])\*([^*\n]+?)\*(?!\*)", r"<em>\1</em>", text)
    return re.sub(
        r"\x00(\d+)\x00",
        lambda m: "<code>%s</code>" % html.escape(codes[int(m.group(1))], quote=False),
        text,
    )


def convert(markdown):
    # The leading HTML comment is the human checklist, not article content.
    markdown = re.sub(r"^<!--.*?-->\s*", "", markdown, flags=re.S)
    lines = markdown.split("\n")

    # Checked before anything is emitted, and fatal rather than a warning: the
    # damage is cosmetic but it lands on every reader, and a warning printed
    # mid-run is exactly the kind of thing that scrolls past unread.
    bad = [(k + 1, l) for k, l in enumerate(lines) if DOUBLE_DASH.search(l)]
    if bad:
        sys.exit("double em dash (——) found on %d line(s); Medium renders it "
                 "as `— —`. Use a single —:\n%s"
                 % (len(bad), "\n".join("  line %d: %s" % (k, l.strip()[:78])
                                        for k, l in bad[:10])))

    out, images = [], []
    title = None
    i, n = 0, len(lines)

    while i < n:
        stripped = lines[i].strip()
        if not stripped:
            i += 1
            continue

        if re.match(r"^```(\w*)\s*$", stripped):
            i += 1
            buf = []
            while i < n and not re.match(r"^```\s*$", lines[i].strip()):
                buf.append(lines[i])
                i += 1
            i += 1
            buf = [line if line.strip() else " " for line in buf]
            out.append("<pre><code>%s</code></pre>"
                       % html.escape("\n".join(buf), quote=False))
            continue

        if re.match(r"^-{3,}$", stripped):
            out.append("<hr>")
            i += 1
            continue

        heading = re.match(r"^(#{1,6})\s+(.*)$", stripped)
        if heading:
            level, text = len(heading.group(1)), heading.group(2)
            if level == 1 and title is None:
                title = text
            else:
                tag = "h2" if level == 2 else "h4"
                out.append("<%s>%s</%s>" % (tag, inline(text), tag))
            i += 1
            continue

        slot = SLOT_RE.match(stripped)
        if slot:
            images.append(slot.group(1))
            out.append("<p>%s</p>" % (SLOT_MARK % slot.group(1)))
            i += 1
            continue
        if stripped.startswith("\U0001F4CC"):
            # Never fall through to the paragraph branch: a 📌 line this regex
            # does not understand would ship as literal body text with a
            # missing figure, and every later check would still pass.
            sys.exit("line %d is a 📌 line the slot pattern does not accept:\n"
                     "  %s\n"
                     "expected 📌【在此插入圖 name.png】 with a name matching "
                     "[A-Za-z0-9-]+.png" % (i + 1, stripped))

        if stripped.startswith(">"):
            buf = []
            while i < n and lines[i].strip().startswith(">"):
                buf.append(re.sub(r"^>\s?", "", lines[i].strip()))
                i += 1
            out.append("<blockquote>%s</blockquote>"
                       % inline(" ".join(x for x in buf if x)))
            continue

        for marker, tag in ((r"^[-*]\s+", "ul"), (r"^\d+\.\s+", "ol")):
            if re.match(marker, stripped):
                items = []
                while i < n:
                    line = lines[i].strip()
                    if re.match(marker, line):
                        items.append(re.sub(marker, "", line))
                        i += 1
                    elif line and items and not BLOCK_START.match(line):
                        items[-1] += " " + line  # wrapped continuation line
                        i += 1
                    else:
                        break
                out.append("<%s>%s</%s>"
                           % (tag, "".join("<li>%s</li>" % inline(x) for x in items), tag))
                break
        else:
            buf = [stripped]
            i += 1
            while i < n:
                line = lines[i].strip()
                if not line or BLOCK_START.match(line):
                    break
                buf.append(line)
                i += 1
            out.append("<p>%s</p>" % inline(" ".join(buf)))
            continue
        continue

    if title is None:
        sys.exit("no '# Title' line found")
    return {"title": title, "html": "\n".join(out), "images": images}


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("article", help="article directory, or a path to medium-paste.md")
    ap.add_argument("--out", default="/tmp/medium-payload.json")
    args = ap.parse_args()

    src = args.article
    if os.path.isdir(src):
        src = os.path.join(src, "publish", "medium-paste.md")
    if not os.path.isfile(src):
        sys.exit("no such file: " + src)

    payload = convert(open(src, encoding="utf-8").read())

    images_dir = os.path.join(os.path.dirname(src), "images")
    missing = [f for f in payload["images"]
               if not os.path.isfile(os.path.join(images_dir, f))]
    if missing:
        sys.exit("missing image files in %s: %s" % (images_dir, ", ".join(missing)))

    with open(args.out, "w", encoding="utf-8") as fh:
        json.dump(payload, fh, ensure_ascii=False)

    lines = payload["html"].count("\n") + 1
    print("title:  %s" % payload["title"])
    print("html lines: %d" % lines)
    print("images: %d (%s)" % (len(payload["images"]), ", ".join(payload["images"])))
    print("wrote:  %s" % args.out)


if __name__ == "__main__":
    main()
