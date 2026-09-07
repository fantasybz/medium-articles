"""Overwrite the Mermaid blocks embedded in an outline with the verified versions from its <slug>.figures.md.

    python3 research/scripts/sync_figures.py research/2026-09/2026-11-same-spec-ten-runs.md

Matching is by figure id (F1, T2, P2-3a, C4 ...): for each ```mermaid block in the outline, the last id
mentioned in the 600 characters before it; in the figures file, the id in the nearest preceding heading.
Blocks with no match are left alone and listed. The figures file is canonical because mermaid_check_all.sh
was run on it; the outline's embedded copies come from the revise agent and are not checked.
"""
import re, sys

ID = re.compile(r'\b([FTRCPGI]\d{1,2}(?:-\d[a-z]?)?)\b')


def main():
    outline = sys.argv[1]
    figfile = re.sub(r'\.md$', '.figures.md', outline)
    S = open(outline).read(); F = open(figfile).read()

    fig_src = {}
    heads = [(m.start(), m.group(1)) for m in re.finditer(r"^#{1,6} +(.+)$", F, re.M)]
    for m in re.finditer(r"```mermaid\n(.*?)```", F, re.S):
        head = ''
        for pos, h in heads:
            if pos < m.start(): head = h
        ids = ID.findall(head)
        if ids: fig_src[ids[0]] = m.group(1)

    blocks = list(re.finditer(r"```mermaid\n(.*?)```", S, re.S))
    new = S; replaced = []; unmatched = []
    for m in reversed(blocks):
        ctx = S[max(0, m.start() - 600):m.start()]
        # prefer an explicit figure label right before the block: 「圖 G4（…」 or 「**F5（封面）**—圖說」; fall back to the last id mentioned
        lab = re.findall(r'(?:圖\s*|\*\*)([FTRCPGI]\d{1,2}(?:-\d[a-z]?)?)\b', ctx)
        ids = ID.findall(ctx)
        fid = lab[-1] if lab else (ids[-1] if ids else None)
        if fid in fig_src:
            new = new[:m.start(1)] + fig_src[fid] + new[m.end(1):]; replaced.append(fid)
        else:
            unmatched.append((fid, ctx[-100:].replace('\n', ' ')))
    open(outline, 'w').write(new)
    print(f"figures.md ids: {sorted(fig_src)}")
    print(f"replaced {len(replaced)}: {replaced[::-1]}")
    print(f"unmatched {len(unmatched)}: {unmatched}")
    dups = sorted({x for x in replaced if replaced.count(x) > 1})
    print(f"DUPLICATE assignments (fix by hand): {dups}" if dups else "no duplicate assignments")


if __name__ == "__main__":
    main()
