"""Derive publish/medium-paste.md from article.md (or publish/<lang>/medium-paste.md from article.<lang>.md).

    python3 research/scripts/article_to_paste.py 2026-10-green-overview          # article.md    -> publish/
    python3 research/scripts/article_to_paste.py 2026-10-green-overview --lang en # article.en.md -> publish/en/

The mapping is the one every published piece already follows (checked on 2026-09-06 against
2026-09-agentic-org-design: zero diff after mapping):

* a ```mermaid block        -> 📌【在此插入圖 diagram-NN.png】   (NN counts from 01 in document order)
* a markdown table          -> 📌【在此插入表 table-NN.png】
* everything else           -> byte for byte the same (links included — tools/test_tools.py's lockstep
                               scan compares the link list and the 「（即將發布）」 count of both files)
* a markdown link inside a captured table cell or mermaid block (`](http`, `](https`, `](../`, `](./`)
  is refused, naming the table/figure and the cell: the PNG cannot carry it, so the paste would lack
  a link the article has and the lockstep scan would fail with no hint why. Put the link in the prose
  around the table, or in References.
* a publishing-guide HTML comment is prepended; it is stripped before anything reaches Medium.

Fences are tracked with tools/md2medium.py's own definitions, so what this treats as a code block is
exactly what the converter will: a ```mermaid sample quoted inside another fence, or a `|` line inside
one, stays code; a fence the author never closed is an error, not a diagram that swallows the rest of
the article. The 📌 line comes from md2medium.slot_line(), so it can only be one md2medium reads back.

It also writes publish/<lang>/figures.json listing which mermaid block / table becomes which PNG, so
render_images.sh can produce the PNGs from the same source. Nothing here touches article.md.
"""
import argparse
import importlib.util
import json
import os
import re
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))


def _load_md2medium():
    # research/scripts is not a package and tools/ is not on sys.path; load
    # the converter by path, the way notion_cookies.py loads chrome_cookies.
    spec = importlib.util.spec_from_file_location(
        "md2medium", os.path.join(ROOT, "tools", "md2medium.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


md2medium = _load_md2medium()

HEADER = """<!--
Medium 發布指南（此註解區塊不要貼進 Medium）

自動化：`./tools/medium_draft.sh <article-dir>{lang_flag}` 會建好草稿並比對內容，停在發布前一步。
細節見 repo 根目錄的 PUBLISHING.md。以下是手動流程與發布後必做的收尾。

【系列狀態】以各篇 publish/PUBLISHED.md 為準。Medium 限制同一作者 24 小時內最多發布或排程 2 篇，
見 PUBLISHING.md 的〈發文數量上限〉。

【手動流程】
1. 開新 story：https://medium.com/new-story
2. 貼上下方內容（從標題那行開始，不含本註解）。
3. 看到 📌【在此插入…】的行：刪掉該行，按 + 插入同目錄 images/ 裡對應的 PNG。
4. code block：在 Medium 選取後按 ``` 轉成 code block。
5. 封面圖選流程圖，不要選表格截圖（縮到卡片尺寸看不清）。
6. Tags 建議：{tags}

【發布後收尾—不做的話系列會斷】
7. 記下本篇 Medium URL，補進 repo 的 README 索引與 publish/PUBLISHED.md。
8. 把本篇兩處的系列連結換成真正的 Medium URL：
   (a) 開頭「系列導覽」那一行
   (b) 文末「系列文章」清單
   （尚未發布的篇在這裡是純文字「（即將發布）」，不是相對路徑；上線後換成真正的 URL）
9. 回頭編輯已發布的其他篇，把指向本篇的連結補上。
-->

"""

# A table row is a line starting with a pipe, in column 0 like every table in
# the repo. Only consulted outside a fence.
TABLE_ROW = re.compile(r"^\|")
# The header/body delimiter of a GFM table: |---|:--:|. Markdown puts no gap
# between two tables that touch, so a renderer shows the second header and its
# delimiter as two more body rows of the first; a delimiter row past the first
# one in a run is the only sign a new table started, and the row before it is
# that table's header.
TABLE_SEP = re.compile(r"^\|[\s:|-]*-[\s:|-]*$")
# The link forms tools/test_tools.py's lockstep scan counts. Inside a table or
# mermaid block the link would vanish with the PNG, so convert() refuses them.
CAPTURED_LINK = re.compile(r"\]\((?:http|\.\./|\./)")
# The publish/<lang>/ directory is named after --lang, so it has to be a name.
LANG_RE = re.compile(r"[A-Za-z0-9_-]+")


def split_tables(rows):
    """One run of `|` lines as the list of tables it holds."""
    tables, cur = [], []
    for row in rows:
        starts_new = (TABLE_SEP.match(row) and len(cur) >= 2
                      and any(TABLE_SEP.match(r) for r in cur)
                      and not TABLE_SEP.match(cur[-1]))
        if starts_new:
            header = cur.pop()
            tables.append(cur)
            cur = [header]
        cur.append(row)
    if cur:
        tables.append(cur)
    return tables


def convert(article_text):
    """(paste body, mermaid sources, table sources) for one article.

    A line walk, not two regex passes over the whole text: the fence state is
    md2medium's, so substitution happens only outside a code block and only
    for a block opened by ```mermaid in column 0. A link inside a captured
    block is an error: the PNG that replaces the block cannot carry it.
    """
    lines = article_text.split("\n")
    out, figures, tables, lost = [], [], [], []
    i, n = 0, len(lines)
    while i < n:
        line = lines[i]
        opened = md2medium.FENCE_OPEN.match(line.strip())
        if opened:
            start = i
            i += 1
            while i < n and not md2medium.FENCE_CLOSE.match(lines[i].strip()):
                i += 1
            if i >= n:
                sys.exit("line %d opens a ``` fence that is never closed; everything "
                         "after it would become code" % (start + 1))
            if line.startswith("```") and opened.group(1) == "mermaid":
                figures.append("".join(l + "\n" for l in lines[start + 1:i]))
                name = "diagram-%02d.png" % len(figures)
                lost += [("diagram %d (%s), line %d" % (len(figures), name, k + 1), lines[k].strip())
                         for k in range(start + 1, i) if CAPTURED_LINK.search(lines[k])]
                out.append(md2medium.slot_line("圖", name))
            else:
                out.extend(lines[start:i + 1])
            i += 1
            continue
        if TABLE_ROW.match(line):
            start = i
            while i < n and TABLE_ROW.match(lines[i]):
                i += 1
            k = start
            for rows in split_tables(lines[start:i]):
                tables.append("".join(r + "\n" for r in rows))
                name = "table-%02d.png" % len(tables)
                for row in rows:
                    k += 1
                    lost += [("table %d (%s), line %d, cell" % (len(tables), name, k), cell.strip())
                             for cell in row.split("|") if CAPTURED_LINK.search(cell)]
                out.append(md2medium.slot_line("表", name))
            continue
        out.append(line)
        i += 1
    if lost:
        sys.exit("%d markdown link(s) inside a table or mermaid block. The block becomes a PNG and the "
                 "link goes with it, so the paste would lack a link the article has and tools/test_tools.py's "
                 "lockstep link scan would fail without saying why. Move each link into the prose or "
                 "References:\n%s" % (len(lost), "\n".join("  %s: %s" % (where, what[:78]) for where, what in lost)))
    return "\n".join(out), figures, tables


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("article_dir")
    ap.add_argument("--lang", default="",
                    help="language pack: article.<lang>.md -> publish/<lang>/ (default: article.md -> publish/)")
    ap.add_argument("--tags", default="AI, Software Engineering, Engineering Management, Agentic AI, DevOps")
    args = ap.parse_args()

    lang = args.lang
    if lang and not LANG_RE.fullmatch(lang):
        sys.exit("invalid lang %r: letters, digits, - and _ only (it names publish/<lang>/)" % lang)
    # One rule for both ends, so a --lang nobody wrote for cannot read article.md
    # and publish it under a new directory as if it were a translation.
    src = os.path.join(args.article_dir, "article.%s.md" % lang if lang else "article.md")
    out_dir = os.path.join(args.article_dir, "publish", lang) if lang else os.path.join(args.article_dir, "publish")
    if not os.path.isfile(src):
        sys.exit("no such article: " + src)
    with open(src, encoding="utf-8") as fh:
        source = fh.read()

    # Same fence-aware scan md2medium.py gates on; failing here saves a browser run.
    bad = md2medium.double_dash_lines(source.split("\n"))
    if bad:
        sys.exit("double em dash (——) in prose on %d line(s); Medium renders it as `— —`. "
                 "Use a single — (md2medium.py refuses it too):\n%s"
                 % (len(bad), "\n".join("  line %d: %s" % (k, l.strip()[:78]) for k, l in bad[:10])))

    text, figures, tables = convert(source)
    os.makedirs(os.path.join(out_dir, "images"), exist_ok=True)
    with open(os.path.join(out_dir, "medium-paste.md"), "w", encoding="utf-8") as fh:
        fh.write(HEADER.format(lang_flag=" " + lang if lang else "", tags=args.tags) + text)
    with open(os.path.join(out_dir, "figures.json"), "w", encoding="utf-8") as fh:
        json.dump({"figures": [{"file": "diagram-%02d.png" % (i + 1), "mermaid": m} for i, m in enumerate(figures)],
                   "tables": [{"file": "table-%02d.png" % (i + 1), "markdown": t} for i, t in enumerate(tables)]},
                  fh, ensure_ascii=False, indent=1)
    print("wrote %s/medium-paste.md: %d figures, %d tables (list in figures.json)" % (out_dir, len(figures), len(tables)))


if __name__ == "__main__":
    main()
