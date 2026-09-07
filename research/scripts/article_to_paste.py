"""Derive publish/medium-paste.md from article.md (or publish/en/medium-paste.md from article.en.md).

    python3 research/scripts/article_to_paste.py 2026-10-green-overview          # zh: publish/medium-paste.md
    python3 research/scripts/article_to_paste.py 2026-10-green-overview --lang en

The mapping is the one every published piece already follows (checked on 2026-09-06 against
2026-09-agentic-org-design: zero diff after mapping):

* a ```mermaid block        -> 📌【在此插入圖 diagram-NN.png】   (NN counts from 01 in document order)
* a markdown table          -> 📌【在此插入表 table-NN.png】
* everything else           -> byte for byte the same (links included — tools/test_tools.py's lockstep
                               scan compares the link list and the 「（即將發布）」 count of both files)
* a publishing-guide HTML comment is prepended; it is stripped before anything reaches Medium.

It also writes publish/<lang>/figures.json listing which mermaid block / table becomes which PNG, so
render_images.sh can produce the PNGs from the same source. Nothing here touches article.md.
"""
import argparse
import json
import os
import re
import sys

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

MERMAID = re.compile(r"```mermaid\n(.*?)```", re.S)
TABLE = re.compile(r"(?:^\|.*\n)+", re.M)


def convert(article_text):
    figures = []
    tables = []

    def fig(m):
        figures.append(m.group(1))
        return "📌【在此插入圖 diagram-%02d.png】" % len(figures)

    text = MERMAID.sub(fig, article_text)

    def tab(m):
        tables.append(m.group(0))
        return "📌【在此插入表 table-%02d.png】\n" % len(tables)

    text = TABLE.sub(tab, text)
    return text, figures, tables


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("article_dir")
    ap.add_argument("--lang", default="", help="'' for article.md → publish/, 'en' for article.en.md → publish/en/")
    ap.add_argument("--tags", default="AI, Software Engineering, Engineering Management, Agentic AI, DevOps")
    args = ap.parse_args()

    src = os.path.join(args.article_dir, "article.en.md" if args.lang == "en" else "article.md")
    out_dir = os.path.join(args.article_dir, "publish", args.lang) if args.lang else os.path.join(args.article_dir, "publish")
    if not os.path.isfile(src):
        sys.exit("no such article: " + src)
    if "——" in re.sub(r"```.*?```", "", open(src).read(), flags=re.S):
        sys.exit("double em dash (——) in prose; use a single — (md2medium.py refuses it too)")
    text, figures, tables = convert(open(src).read())
    os.makedirs(os.path.join(out_dir, "images"), exist_ok=True)
    with open(os.path.join(out_dir, "medium-paste.md"), "w") as fh:
        fh.write(HEADER.format(lang_flag=" en" if args.lang == "en" else "", tags=args.tags) + text)
    with open(os.path.join(out_dir, "figures.json"), "w") as fh:
        json.dump({"figures": [{"file": "diagram-%02d.png" % (i + 1), "mermaid": m} for i, m in enumerate(figures)],
                   "tables": [{"file": "table-%02d.png" % (i + 1), "markdown": t} for i, t in enumerate(tables)]},
                  fh, ensure_ascii=False, indent=1)
    print("wrote %s/medium-paste.md: %d figures, %d tables (list in figures.json)" % (out_dir, len(figures), len(tables)))


if __name__ == "__main__":
    main()
