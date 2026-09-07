"""Overwrite the Mermaid blocks embedded in an outline with the verified versions from its <slug>.figures.md.

    python3 research/scripts/sync_figures.py research/2026-09/2026-11-same-spec-ten-runs.md
    python3 research/scripts/sync_figures.py research/2026-09/2026-11-same-spec-ten-runs.md --force

Matching is by figure id (F1, T2, P2-3a, C4 ...): for each ```mermaid block in the outline, the id in an
explicit label right before it (「圖 G4（…」 or 「**F5（封面）**」), else the last id mentioned in the 600
characters before it; in the figures file, the id in the nearest preceding heading. The figures file is
canonical because mermaid_check_all.sh was run on it; the outline's embedded copies come from the revise
agent and are not checked.

The mapping is computed first and printed in full. If any block has no verified counterpart, or two
blocks resolve to the same id, nothing is written and the exit code is 1: an outline half-synced with one
diagram duplicated is worse than an outline not synced, and the report is the fix list. --force writes
anyway, for when the unmatched block is one the figures file deliberately does not carry.
"""
import argparse
import os
import re
import sys

# One id pattern for both regexes below, or they would drift on what an id is.
ID_PAT = r"[FTRCPGI]\d{1,2}(?:-\d[a-z]?)?"
# Not \b: Python counts CJK as \w, so 圖F3 and T2圖說 would hide their id
# behind the character glued to it. Only a Latin letter or digit disqualifies
# (AF1, F123), which still lets P95 / G20 / R1 in prose read as ids; that is
# what the explicit-label rule is for.
_ID_BOUNDED = r"(?<![A-Za-z0-9])(" + ID_PAT + r")(?![A-Za-z0-9])"
ID = re.compile(_ID_BOUNDED)
LABEL = re.compile(r"(?:圖\s*|\*\*)(" + ID_PAT + r")(?![A-Za-z0-9])")
BLOCK = re.compile(r"```mermaid\n(.*?)```", re.S)
CONTEXT = 600


def verified_blocks(figures_text):
    """id -> mermaid source, keyed on the first id in the nearest preceding heading."""
    heads = [(m.start(), m.group(1)) for m in re.finditer(r"^#{1,6} +(.+)$", figures_text, re.M)]
    fig_src = {}
    for m in BLOCK.finditer(figures_text):
        head = ""
        for pos, h in heads:
            if pos < m.start():
                head = h
        ids = ID.findall(head)
        if ids:
            fig_src[ids[0]] = m.group(1)
    return fig_src


def plan(outline_text, fig_src):
    """(new outline text, ids replaced, unmatched blocks), all in document order.

    Replacement runs back to front so the offsets of earlier blocks stay valid.
    """
    blocks = list(BLOCK.finditer(outline_text))
    new, replaced, unmatched = outline_text, [], []
    for m in reversed(blocks):
        ctx = outline_text[max(0, m.start() - CONTEXT):m.start()]
        lab = LABEL.findall(ctx)
        ids = ID.findall(ctx)
        fid = lab[-1] if lab else (ids[-1] if ids else None)
        if fid in fig_src:
            new = new[:m.start(1)] + fig_src[fid] + new[m.end(1):]
            replaced.append(fid)
        else:
            unmatched.append((fid, ctx[-100:].replace("\n", " ")))
    return new, replaced[::-1], unmatched[::-1]


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("outline", help="the outline .md; its <slug>.figures.md sits next to it")
    ap.add_argument("--force", action="store_true",
                    help="write even when a block is unmatched or two blocks resolve to the same id")
    args = ap.parse_args()

    outline = args.outline
    figfile = re.sub(r"\.md$", ".figures.md", outline)
    if not os.path.isfile(figfile):
        sys.exit("no such figures file: " + figfile)
    with open(outline, encoding="utf-8") as fh:
        source = fh.read()
    with open(figfile, encoding="utf-8") as fh:
        figures = fh.read()

    fig_src = verified_blocks(figures)
    new, replaced, unmatched = plan(source, fig_src)
    dups = sorted({x for x in replaced if replaced.count(x) > 1})
    print(f"figures.md ids: {sorted(fig_src)}")
    print(f"replaced {len(replaced)}: {replaced}")
    print(f"unmatched {len(unmatched)}: {unmatched}")
    print(f"DUPLICATE assignments (fix by hand): {dups}" if dups else "no duplicate assignments")

    if (dups or unmatched) and not args.force:
        sys.exit("%s not written: %d unmatched block(s), duplicate ids %s. Fix the labels in the "
                 "outline (圖 F3 / **F3** right before the block), or pass --force to write anyway."
                 % (outline, len(unmatched), dups))
    with open(outline, "w", encoding="utf-8") as fh:
        fh.write(new)


if __name__ == "__main__":
    main()
