#!/usr/bin/env python3
"""Tests for the pure-Python research scripts. Stdlib only, no network, no browser.

    python3 -m unittest research/scripts/test_research_scripts.py -v
    python3 research/scripts/test_research_scripts.py

research/README.md keeps research/scripts out of tools/ because the extractors
depend on live DOMs. This covers the part that does not: the article -> paste
mapping and its figures.json, the outline <-> figures.md id matching, the codex
JSONL parser whose exit codes codex_review.sh branches on, codex_review.sh's own
pre-flight (run against a throwaway git repo with a fake `codex` first on PATH,
the way tools/test_tools.py runs medium_draft.sh's pre-flight under an empty
HOME), the merge script whose printed count collect.sh reads, and the argument /
keychain guards of the Notion cookie export. Everything that needs a browser, a
real Codex session or the macOS Keychain (collect.sh, extract_*.js, notion_*.js,
mermaid_check*.sh, render_images.sh, codex_review.sh past its pre-flight) is
deliberately absent.

The scripts are not a package, so they are loaded by path; the ones that are
only ever run from a shell are exercised through their CLI so the tests pin
the exit codes and the exact stdout/stderr the callers parse.
"""

import glob
import hashlib
import importlib.util
import io
import json
import os
import re
import shlex
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))


def load(name):
    spec = importlib.util.spec_from_file_location(name, os.path.join(HERE, name + ".py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


article_to_paste = load("article_to_paste")
sync_figures = load("sync_figures")
notion_cookies = load("notion_cookies")
md2medium = article_to_paste.md2medium


def run_script(name, *args, stdin=""):
    return subprocess.run([sys.executable, os.path.join(HERE, name + ".py")] + list(args),
                          input=stdin, capture_output=True, text=True, encoding="utf-8")


def write(path, text):
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(text)


def read(path):
    with open(path, encoding="utf-8") as fh:
        return fh.read()


MERMAID_A = "flowchart TB\n    A --> B\n"
MERMAID_B = "flowchart LR\n    C --> D\n"
TABLE = "| a | b |\n|---|---|\n| 1 | 2 |\n"
TABLE_2 = "| c | d |\n|:--|--:|\n| 3 | 4 |\n| 5 | 6 |\n"


def fence(body):
    return "```mermaid\n" + body + "```\n"


# ---------------------------------------------------------------- article_to_paste.py

class TestConvert(unittest.TestCase):
    def test_mermaid_blocks_become_figure_markers_numbered_in_document_order(self):
        text, figures, tables = article_to_paste.convert(
            "intro\n\n" + fence(MERMAID_A) + "\nmid\n\n" + fence(MERMAID_B))
        self.assertEqual(text, "intro\n\n📌【在此插入圖 diagram-01.png】\n\nmid\n\n📌【在此插入圖 diagram-02.png】\n")
        self.assertEqual(figures, [MERMAID_A, MERMAID_B])
        self.assertEqual(tables, [])

    def test_tables_become_table_markers_and_count_separately_from_figures(self):
        text, figures, tables = article_to_paste.convert(
            "before\n\n" + TABLE + "\n" + fence(MERMAID_A) + "\nafter\n\n" + TABLE)
        self.assertEqual(text, "before\n\n📌【在此插入表 table-01.png】\n\n📌【在此插入圖 diagram-01.png】\n\n"
                               "after\n\n📌【在此插入表 table-02.png】\n")
        self.assertEqual(tables, [TABLE, TABLE])
        self.assertEqual(figures, [MERMAID_A])

    def test_everything_else_is_byte_identical(self):
        # Links included: the lockstep scan in tools/test_tools.py compares the
        # link lists of article and paste, so the mapping may not touch them.
        src = ("# T\n\n見 [a](https://x.test/?q=1&r=2) 與 [b](../other/article.md)（即將發布）。\n\n"
               "```python\nprint('|' + x)\n```\n\n> quote\n\n- 1\n- 2\n")
        text, figures, tables = article_to_paste.convert(src)
        self.assertEqual(text, src)
        self.assertEqual((figures, tables), ([], []))

    def test_the_markers_are_the_lines_md2medium_reads_back(self):
        # The paste is consumed by tools/md2medium.py; each 📌 line has to be
        # one its slot pattern accepts, or the draft ships the marker as prose.
        text, _, _ = article_to_paste.convert(fence(MERMAID_A) + "\n" + TABLE)
        markers = [l for l in text.split("\n") if l.startswith("📌")]
        self.assertEqual(len(markers), 2)
        for line in markers:
            self.assertTrue(md2medium.SLOT_RE.match(line), line)
        self.assertEqual(md2medium.convert("# T\n\n" + text)["images"],
                         ["diagram-01.png", "table-01.png"])

    def test_a_mermaid_sample_quoted_inside_another_fence_stays_code(self):
        # A ```mermaid line that is content of a ```text block used to open a
        # figure anyway, leaving a ghost diagram in figures.json.
        src = "說明：\n\n```text\n```mermaid\nflowchart TB\n    A --> B\n```\n\n然後。\n"
        text, figures, tables = article_to_paste.convert(src)
        self.assertEqual(text, src)
        self.assertEqual((figures, tables), ([], []))

    def test_a_pipe_line_inside_a_code_fence_is_not_a_table(self):
        src = "```bash\ncat x \\\n| grep y\n|---|\n```\n"
        text, figures, tables = article_to_paste.convert(src)
        self.assertEqual(text, src)
        self.assertEqual(tables, [])

    def test_an_unterminated_fence_is_an_error_not_a_figure_that_eats_the_article(self):
        # The regex version swallowed everything up to the next fence of any
        # kind; here the prose after the open fence would have vanished.
        with self.assertRaises(SystemExit) as cm:
            article_to_paste.convert("# T\n\n```mermaid\nflowchart TB\n\n正文還在這裡\n")
        self.assertIn("line 3", str(cm.exception))
        self.assertIn("never closed", str(cm.exception))

    def test_only_a_fence_opened_in_column_zero_becomes_a_figure(self):
        # An indented ```mermaid is a fence to md2medium (it strips before
        # matching) but not a figure here: it stays code in the paste.
        src = "- item\n\n  ```mermaid\n  flowchart TB\n  ```\n\n| a |\n|---|\n"
        text, figures, tables = article_to_paste.convert(src)
        self.assertEqual(text, "- item\n\n  ```mermaid\n  flowchart TB\n  ```\n\n📌【在此插入表 table-01.png】\n")
        self.assertEqual(figures, [])
        self.assertEqual(tables, ["| a |\n|---|\n"])

    def test_a_table_at_the_end_of_the_file_keeps_its_last_row(self):
        # Without a trailing newline the old `^\|.*\n` never matched the last
        # row, which then shipped as a paragraph under the table marker.
        text, _, tables = article_to_paste.convert("x\n\n" + TABLE.rstrip("\n"))
        self.assertEqual(text, "x\n\n📌【在此插入表 table-01.png】")
        self.assertEqual(tables, [TABLE])

    def test_two_tables_touching_are_split_at_the_second_delimiter_row(self):
        text, _, tables = article_to_paste.convert("x\n\n" + TABLE + TABLE_2 + "\ny\n")
        self.assertEqual(text, "x\n\n📌【在此插入表 table-01.png】\n📌【在此插入表 table-02.png】\n\ny\n")
        self.assertEqual(tables, [TABLE, TABLE_2])

    def test_a_table_with_one_delimiter_row_is_never_split(self):
        # The split rule must not fire on the table's own header/body line,
        # nor on a delimiter-looking row with nothing before it.
        for src in (TABLE, "|---|\n| 1 |\n", "|---|\n|---|\n| 1 |\n"):
            with self.subTest(src=src):
                self.assertEqual(article_to_paste.convert(src)[2], [src])

    def test_a_link_in_a_table_cell_is_refused_with_the_table_number_and_the_cell(self):
        # The table becomes a PNG and the link goes with it. Without this the
        # paste was written and tools/test_tools.py's lockstep scan failed on
        # it later, with no hint that a table cell was the cause.
        src = "x\n\n" + TABLE + "\n| c | d |\n|---|---|\n| 3 | 見 [b](https://y.test/p) |\n"
        with self.assertRaises(SystemExit) as cm:
            article_to_paste.convert(src)
        msg = str(cm.exception)
        self.assertIn("table 2 (table-02.png), line 9, cell: 見 [b](https://y.test/p)", msg)
        self.assertNotIn("table 1", msg)
        self.assertIn("lockstep", msg)
        self.assertIn("prose or References", msg)

    def test_every_link_form_the_lockstep_scan_counts_is_refused_in_a_table(self):
        for target in ("http://x.test", "https://x.test/?a=1&b=2", "../other/article.md", "./images/a.png"):
            with self.subTest(target=target):
                with self.assertRaises(SystemExit) as cm:
                    article_to_paste.convert("| a |\n|---|\n| [l](%s) |\n" % target)
                self.assertIn("table 1 (table-01.png), line 3, cell: [l](%s)" % target, str(cm.exception))

    def test_a_link_in_a_mermaid_block_is_refused_with_the_figure_number(self):
        src = "# T\n\n" + fence(MERMAID_A) + "\n" + fence('flowchart TB\n    A["見 [x](https://x.test)"]\n')
        with self.assertRaises(SystemExit) as cm:
            article_to_paste.convert(src)
        msg = str(cm.exception)
        self.assertIn('diagram 2 (diagram-02.png), line 10: A["見 [x](https://x.test)"]', msg)
        self.assertNotIn("diagram 1", msg)

    def test_every_lost_link_is_reported_at_once(self):
        src = "| [a](https://a.test) |\n|---|\n\n" + fence('flowchart TB\n    B["[b](./b.png)"]\n')
        with self.assertRaises(SystemExit) as cm:
            article_to_paste.convert(src)
        msg = str(cm.exception)
        self.assertTrue(msg.startswith("2 markdown link(s)"), msg)
        self.assertIn("table 1 (table-01.png), line 1, cell: [a](https://a.test)", msg)
        self.assertIn('diagram 1 (diagram-01.png), line 6: B["[b](./b.png)"]', msg)

    def test_a_link_in_prose_right_above_a_table_or_inside_code_still_passes(self):
        # Only the captured block is checked: the prose line touching the
        # table keeps its links, and a `](http` inside a code fence is code.
        src = ("見 [a](https://x.test) 與 [b](../o/article.md)：\n" + TABLE
               + "\n```text\n| [c](https://c.test) |\n```\n")
        text, figures, tables = article_to_paste.convert(src)
        self.assertEqual(text, "見 [a](https://x.test) 與 [b](../o/article.md)：\n📌【在此插入表 table-01.png】\n\n"
                               "```text\n| [c](https://c.test) |\n```\n")
        self.assertEqual((figures, tables), ([], [TABLE]))


class TestArticleToPasteCLI(unittest.TestCase):
    ARTICLE = ("# 標題\n\n開場，見 [系列](https://medium.com/@x/a)。\n\n" + fence(MERMAID_A) + "\n"
               + TABLE + "\n結尾（即將發布）\n")
    DEFAULT_TAGS = "AI, Software Engineering, Engineering Management, Agentic AI, DevOps"

    def article_dir(self, text=ARTICLE, name="article.md"):
        root = tempfile.TemporaryDirectory()
        self.addCleanup(root.cleanup)
        write(os.path.join(root.name, name), text)
        return root.name

    def test_writes_the_paste_the_figure_list_and_the_images_dir(self):
        art = self.article_dir()
        out = run_script("article_to_paste", art)
        self.assertEqual(out.returncode, 0, out.stderr)
        self.assertIn("1 figures, 1 tables", out.stdout)
        paste = read(os.path.join(art, "publish", "medium-paste.md"))
        self.assertTrue(paste.startswith("<!--\nMedium 發布指南"), paste[:60])
        header, body = paste.split("-->\n\n", 1)
        self.assertIn("`./tools/medium_draft.sh <article-dir>`", header)
        self.assertIn("Tags 建議：" + self.DEFAULT_TAGS, header)
        self.assertEqual(body, article_to_paste.convert(self.ARTICLE)[0])
        self.assertIn("📌【在此插入圖 diagram-01.png】\n\n📌【在此插入表 table-01.png】\n", body)
        self.assertIn("[系列](https://medium.com/@x/a)", body)
        spec = json.loads(read(os.path.join(art, "publish", "figures.json")))
        self.assertEqual(spec, {"figures": [{"file": "diagram-01.png", "mermaid": MERMAID_A}],
                                "tables": [{"file": "table-01.png", "markdown": TABLE}]})
        self.assertTrue(os.path.isdir(os.path.join(art, "publish", "images")))

    def test_figures_json_keeps_cjk_readable_for_review(self):
        # render_images.sh feeds the mermaid straight to the renderer; \uXXXX
        # would still parse, but a diff of the file would be unreviewable.
        art = self.article_dir("# T\n\n" + fence('flowchart TB\n    A["中文節點"]\n'))
        out = run_script("article_to_paste", art)
        self.assertEqual(out.returncode, 0, out.stderr)
        raw = read(os.path.join(art, "publish", "figures.json"))
        self.assertIn("中文節點", raw)
        self.assertNotIn("\\u4e2d", raw)

    def test_lang_en_reads_article_en_and_writes_publish_en(self):
        art = self.article_dir(name="article.en.md")
        out = run_script("article_to_paste", art, "--lang", "en")
        self.assertEqual(out.returncode, 0, out.stderr)
        paste = read(os.path.join(art, "publish", "en", "medium-paste.md"))
        self.assertIn("`./tools/medium_draft.sh <article-dir> en`", paste)
        self.assertTrue(os.path.isfile(os.path.join(art, "publish", "en", "figures.json")))
        self.assertTrue(os.path.isdir(os.path.join(art, "publish", "en", "images")))
        self.assertFalse(os.path.exists(os.path.join(art, "publish", "medium-paste.md")))

    def test_any_lang_follows_the_same_rule_as_en(self):
        # One rule, not a special case for "en": article.<lang>.md -> publish/<lang>/,
        # and the header's medium_draft.sh hint carries the same lang.
        art = self.article_dir(name="article.zh-TW.md")
        out = run_script("article_to_paste", art, "--lang", "zh-TW")
        self.assertEqual(out.returncode, 0, out.stderr)
        paste = read(os.path.join(art, "publish", "zh-TW", "medium-paste.md"))
        self.assertIn("`./tools/medium_draft.sh <article-dir> zh-TW`", paste)

    def test_a_lang_with_no_source_fails_instead_of_republishing_article_md(self):
        # --lang fr used to read article.md and write publish/fr with an empty
        # lang flag in the header: a Chinese "translation" nobody asked for.
        art = self.article_dir()  # only article.md exists
        out = run_script("article_to_paste", art, "--lang", "fr")
        self.assertNotEqual(out.returncode, 0)
        self.assertIn("no such article", out.stderr)
        self.assertIn("article.fr.md", out.stderr)
        self.assertFalse(os.path.exists(os.path.join(art, "publish")))

    def test_a_lang_that_is_a_path_is_refused(self):
        art = self.article_dir()
        for bad in ("../x", "en/..", "a/b"):
            out = run_script("article_to_paste", art, "--lang", bad)
            self.assertNotEqual(out.returncode, 0, bad)
            self.assertIn("invalid lang", out.stderr, bad)
        self.assertFalse(os.path.exists(os.path.join(art, "publish")))

    def test_custom_tags_land_in_the_header(self):
        art = self.article_dir()
        out = run_script("article_to_paste", art, "--tags", "Testing, QA")
        self.assertEqual(out.returncode, 0, out.stderr)
        self.assertIn("Tags 建議：Testing, QA\n", read(os.path.join(art, "publish", "medium-paste.md")))

    def test_missing_article_fails_before_writing_anything(self):
        art = self.article_dir(name="article.en.md")  # only the English source exists
        out = run_script("article_to_paste", art)
        self.assertNotEqual(out.returncode, 0)
        self.assertIn("no such article", out.stderr)
        self.assertFalse(os.path.exists(os.path.join(art, "publish")))

    def test_a_c_label_in_prose_is_refused_before_anything_is_written(self):
        # Medium autocorrects (c) into ©; the guard lives in md2medium and this
        # CLI refuses the same way it refuses a double em dash.
        art = self.article_dir("# T\n\n(a) fine, (b) fine, (c) not fine\n")
        out = run_script("article_to_paste", art)
        self.assertNotEqual(out.returncode, 0)
        self.assertIn("autocorrect", out.stderr)
        self.assertFalse(os.path.exists(os.path.join(art, "publish")))
        art = self.article_dir("# T\n\n（c） and c) are fine\n\n```\n(c) in code\n```\n")
        out = run_script("article_to_paste", art)
        self.assertEqual(out.returncode, 0, out.stderr)

    def test_double_em_dash_is_refused_in_prose_but_allowed_inside_code(self):
        # md2medium.py refuses it too; failing here saves a browser run. Same
        # fence-aware scan as md2medium, so the two cannot disagree.
        art = self.article_dir("# T\n\n這裡——會裂\n")
        out = run_script("article_to_paste", art)
        self.assertNotEqual(out.returncode, 0)
        self.assertIn("double em dash", out.stderr)
        self.assertIn("line 3: 這裡——會裂", out.stderr)
        self.assertFalse(os.path.exists(os.path.join(art, "publish")))
        art = self.article_dir("# T\n\n```\nprint('——')\n```\n")
        out = run_script("article_to_paste", art)
        self.assertEqual(out.returncode, 0, out.stderr)

    def test_an_unterminated_fence_fails_before_writing_anything(self):
        art = self.article_dir("# T\n\n```mermaid\nflowchart TB\n\n正文\n")
        out = run_script("article_to_paste", art)
        self.assertNotEqual(out.returncode, 0)
        self.assertIn("never closed", out.stderr)
        self.assertFalse(os.path.exists(os.path.join(art, "publish")))

    def test_a_link_inside_a_table_fails_before_writing_anything(self):
        art = self.article_dir("# T\n\n| a |\n|---|\n| [l](https://x.test) |\n")
        out = run_script("article_to_paste", art)
        self.assertNotEqual(out.returncode, 0)
        self.assertIn("table 1 (table-01.png), line 5, cell: [l](https://x.test)", out.stderr)
        self.assertIn("lockstep", out.stderr)
        self.assertFalse(os.path.exists(os.path.join(art, "publish")))


class TestCommittedPastesAreReproducible(unittest.TestCase):
    """Every medium-paste.md in the repo is article*.md after the mapping.

    tools/test_tools.py compares the link lists and the unpublished-marker
    counts of each pair; this compares the whole body, so a paste edited by
    hand, or an article edited after its paste was generated, fails here.
    Only the body is compared: the <!-- --> header of the older, hand-made
    pastes predates the script.
    """

    MARKER = re.compile(r"📌【在此插入[圖表] ([\w.-]+)】")

    def pairs(self):
        found = []
        for article in sorted(glob.glob(os.path.join(REPO, "*", "article*.md"))):
            en = article.endswith("article.en.md")
            paste = os.path.join(os.path.dirname(article), "publish", "en" if en else "", "medium-paste.md")
            if os.path.exists(paste):
                found.append((article, paste))
        return found

    def body(self, paste):
        raw = read(paste)
        self.assertTrue(raw.startswith("<!--"), paste)
        return raw[raw.index("-->") + 3:]

    def test_there_are_pairs_to_check(self):
        self.assertGreaterEqual(len(self.pairs()), 8)

    def test_every_paste_body_is_exactly_the_converted_article(self):
        for article, paste in self.pairs():
            text = article_to_paste.convert(read(article))[0]
            self.assertEqual(self.body(paste), "\n\n" + text,
                             "%s is not article_to_paste.convert() of its article"
                             % os.path.relpath(paste, REPO))

    def test_every_figure_marker_has_its_png_and_matches_figures_json(self):
        # md2medium.py would refuse a missing PNG at draft time; catching it
        # here is one browser session earlier. figures.json only exists for
        # pastes the script generated.
        with_spec = 0
        for article, paste in self.pairs():
            pack = os.path.dirname(paste)
            markers = self.MARKER.findall(self.body(paste))
            for name in markers:
                self.assertTrue(os.path.isfile(os.path.join(pack, "images", name)),
                                "%s: %s has no PNG" % (os.path.relpath(pack, REPO), name))
            spec_path = os.path.join(pack, "figures.json")
            if os.path.exists(spec_path):
                with_spec += 1
                spec = json.loads(read(spec_path))
                listed = [f["file"] for f in spec["figures"]] + [t["file"] for t in spec["tables"]]
                self.assertEqual(sorted(markers), sorted(listed), os.path.relpath(pack, REPO))
                self.assertEqual([f["mermaid"] for f in spec["figures"]],
                                 article_to_paste.convert(read(article))[1],
                                 "%s: figures.json is stale" % os.path.relpath(pack, REPO))
        self.assertGreaterEqual(with_spec, 4)


# ---------------------------------------------------------------- sync_figures.py

class TestSyncFigures(unittest.TestCase):
    OLD = "flowchart TB\n    A --> B\n"
    NEW_F1 = 'flowchart TB\n    A["verified"] --> B\n'
    NEW_T2 = "flowchart LR\n    T --> U\n"
    FIGURES = ("# 圖檔\n\n## F1 封面\n\n" + fence(NEW_F1) + "\n## T2 表（接 F1）\n\n" + fence(NEW_T2)
               + "\n## 沒有編號的段\n\n" + fence("flowchart TB\n    Z\n"))

    def test_id_pattern_accepts_every_series_and_rejects_lookalikes(self):
        self.assertEqual(sync_figures.ID.findall("F1 T12 R3 C4 P2-3a G1 I7 F5-1"),
                         ["F1", "T12", "R3", "C4", "P2-3a", "G1", "I7", "F5-1"])
        # 2026-12's G/I series were added after a figures file warned they were
        # missing; other letters, three digits and word prefixes stay out.
        self.assertEqual(sync_figures.ID.findall("X9 F123 AF1 F1b"), [])

    def test_an_id_glued_to_cjk_is_still_an_id(self):
        # \b treated 圖 and 說 as word characters, so 圖F3 and T2圖說 hid
        # their ids; only a Latin letter or digit may touch one.
        self.assertEqual(sync_figures.ID.findall("圖F3、T2圖說、（C4）"), ["F3", "T2", "C4"])
        self.assertEqual(sync_figures.LABEL.findall("圖F3 **T2圖說** 圖 G4（"), ["F3", "T2", "G4"])
        self.assertEqual(sync_figures.LABEL.findall("**AF1** 圖F123"), [])

    def test_both_regexes_share_one_id_definition(self):
        # Extend ID_PAT (a new series letter) and both have to follow.
        for sample in ("F1", "T12", "P2-3a", "G1", "I7"):
            self.assertEqual(sync_figures.ID.findall("圖 " + sample), [sample])
            self.assertEqual(sync_figures.LABEL.findall("圖 " + sample), [sample])
        self.assertIn(sync_figures.ID_PAT, sync_figures.ID.pattern)
        self.assertIn(sync_figures.ID_PAT, sync_figures.LABEL.pattern)

    def outline(self, outline_text, figures_text=FIGURES):
        root = tempfile.TemporaryDirectory()
        self.addCleanup(root.cleanup)
        path = os.path.join(root.name, "2026-11-slug.md")
        write(path, outline_text)
        if figures_text is not None:
            write(os.path.join(root.name, "2026-11-slug.figures.md"), figures_text)
        return path

    def test_replaces_each_block_with_the_verified_version_of_the_same_id(self):
        src = "# 大綱\n\n圖 F1（封面）\n\n" + fence(self.OLD) + "\n圖 T2（表）\n\n" + fence(self.OLD)
        path = self.outline(src)
        out = run_script("sync_figures", path)
        self.assertEqual(out.returncode, 0, out.stderr)
        self.assertEqual(read(path), "# 大綱\n\n圖 F1（封面）\n\n" + fence(self.NEW_F1)
                                     + "\n圖 T2（表）\n\n" + fence(self.NEW_T2))
        # the heading with two ids keys on its first; the heading without an id contributes nothing
        self.assertIn("figures.md ids: ['F1', 'T2']", out.stdout)
        # processed back to front so offsets stay valid, reported in document order
        self.assertIn("replaced 2: ['F1', 'T2']", out.stdout)
        self.assertIn("unmatched 0: []", out.stdout)
        self.assertIn("no duplicate assignments", out.stdout)

    def test_an_explicit_label_beats_the_last_id_mentioned(self):
        src = "**F1（封面）**—圖說，分類沿用 T2 的表\n\n" + fence(self.OLD)
        path = self.outline(src)
        out = run_script("sync_figures", path)
        self.assertEqual(out.returncode, 0, out.stderr)
        self.assertEqual(read(path), "**F1（封面）**—圖說，分類沿用 T2 的表\n\n" + fence(self.NEW_F1))
        self.assertIn("replaced 1: ['F1']", out.stdout)

    def test_an_id_glued_to_cjk_is_found_as_a_label_and_as_a_mention(self):
        # Two outlines, because in one the 圖F1 label would still be inside the
        # second block's 600-character window and win over the bare T2 mention.
        for src, new in (("圖F1（封面）\n\n" + fence(self.OLD), self.NEW_F1),
                         ("T2圖說\n\n" + fence(self.OLD), self.NEW_T2)):
            with self.subTest(src=src.split("\n")[0]):
                path = self.outline(src)
                out = run_script("sync_figures", path)
                self.assertEqual(out.returncode, 0, out.stderr)
                self.assertEqual(read(path), src.replace(fence(self.OLD), fence(new)))

    def test_without_a_label_the_last_id_mentioned_wins(self):
        src = "先講 F1，再講 T2 的表\n\n" + fence(self.OLD)
        path = self.outline(src)
        out = run_script("sync_figures", path)
        self.assertEqual(out.returncode, 0, out.stderr)
        self.assertEqual(read(path), "先講 F1，再講 T2 的表\n\n" + fence(self.NEW_T2))

    def test_a_metric_in_prose_reads_as_an_id_unless_a_label_says_otherwise(self):
        # P95 / G20 / R1 look exactly like ids; the label rule exists so the
        # author can override them, and this pins that they do need to.
        src = "圖 F1，量測 P95 延遲\n\n" + fence(self.OLD)
        path = self.outline(src)
        self.assertEqual(run_script("sync_figures", path).returncode, 0)
        self.assertEqual(read(path), "圖 F1，量測 P95 延遲\n\n" + fence(self.NEW_F1))
        src = "F1 的 P95 延遲\n\n" + fence(self.OLD)
        path = self.outline(src)
        out = run_script("sync_figures", path)
        self.assertEqual(out.returncode, 1)
        self.assertIn("unmatched 1: [('P95', ", out.stdout)
        self.assertEqual(read(path), src)

    def test_an_unmatched_block_stops_the_write_and_exits_1(self):
        # The second block sits more than 600 characters after any id, so it has none.
        src = ("圖 F1（封面）\n\n" + fence(self.OLD) + "\n圖 F9（figures.md 裡沒有）\n\n" + fence(self.OLD)
               + "\n" + "x" * 700 + "\n\n" + fence(self.OLD))
        path = self.outline(src)
        out = run_script("sync_figures", path)
        self.assertEqual(out.returncode, 1, out.stdout)
        # nothing written: not even the F1 block that did match
        self.assertEqual(read(path), src)
        # the report is still printed, in document order, and says why
        self.assertIn("replaced 1: ['F1']", out.stdout)
        self.assertIn("unmatched 2: [('F9', ", out.stdout)
        self.assertIn("(None, 'xxxx", out.stdout)
        self.assertIn("not written", out.stderr)
        self.assertIn("--force", out.stderr)

    def test_force_writes_what_matched_and_leaves_the_rest_alone(self):
        src = "圖 F1（封面）\n\n" + fence(self.OLD) + "\n圖 F9（figures.md 裡沒有）\n\n" + fence(self.OLD)
        path = self.outline(src)
        out = run_script("sync_figures", path, "--force")
        self.assertEqual(out.returncode, 0, out.stderr)
        self.assertEqual(read(path), "圖 F1（封面）\n\n" + fence(self.NEW_F1)
                                     + "\n圖 F9（figures.md 裡沒有）\n\n" + fence(self.OLD))
        self.assertIn("unmatched 1: [('F9', ", out.stdout)

    def test_two_blocks_resolving_to_the_same_id_stop_the_write(self):
        src = "圖 F1（封面）\n\n" + fence(self.OLD) + "\n同一張 F1 再貼一次\n\n" + fence("flowchart TB\n    Q\n")
        path = self.outline(src)
        out = run_script("sync_figures", path)
        self.assertEqual(out.returncode, 1, out.stdout)
        self.assertEqual(read(path), src)
        self.assertIn("DUPLICATE assignments (fix by hand): ['F1']", out.stdout)
        self.assertIn("duplicate ids ['F1']", out.stderr)
        out = run_script("sync_figures", path, "--force")
        self.assertEqual(out.returncode, 0, out.stderr)
        self.assertEqual(read(path).count(self.NEW_F1), 2)

    def test_missing_figures_file_fails_before_touching_the_outline(self):
        src = "圖 F1\n\n" + fence(self.OLD)
        path = self.outline(src, figures_text=None)
        out = run_script("sync_figures", path)
        self.assertNotEqual(out.returncode, 0)
        self.assertIn("2026-11-slug.figures.md", out.stderr)
        self.assertEqual(read(path), src)


# ---------------------------------------------------------------- codex_jsonl.py

def jsonl(*objs):
    return "".join(json.dumps(o) + "\n" for o in objs)


def message(text):
    return {"type": "item.completed", "item": {"type": "agent_message", "text": text}}


DONE = {"type": "turn.completed", "usage": {"input_tokens": 10, "output_tokens": 5}}


class TestCodexJsonl(unittest.TestCase):
    def parse(self, text):
        return run_script("codex_jsonl", stdin=text)

    def test_agent_messages_become_the_review_and_the_turn_appends_a_token_count(self):
        out = self.parse(jsonl(message("first"), message("second"), DONE))
        self.assertEqual(out.returncode, 0, out.stderr)
        self.assertEqual(out.stdout, "first\nsecond\n\n<!-- tokens: in 10 out 5 -->\n")
        self.assertEqual(out.stderr, "")

    def test_cjk_survives_whatever_the_locale_says(self):
        out = subprocess.run([sys.executable, os.path.join(HERE, "codex_jsonl.py")],
                             input=jsonl(message("審查：沒問題"), DONE).encode("utf-8"),
                             capture_output=True, env={**os.environ, "LC_ALL": "C", "LANG": "C",
                                                       "PYTHONIOENCODING": "", "PYTHONUTF8": "0"})
        self.assertEqual(out.returncode, 0, out.stderr)
        self.assertTrue(out.stdout.startswith("審查：沒問題\n".encode("utf-8")), out.stdout)

    def test_commands_are_logged_as_html_comments_cut_at_160_chars(self):
        cmd = "grep -rn " + "x" * 200
        out = self.parse(jsonl({"type": "item.completed",
                                "item": {"type": "command_execution", "command": cmd}},
                               message("ok"), DONE))
        self.assertEqual(out.returncode, 0, out.stderr)
        self.assertIn("<!-- codex ran: %s -->\n" % cmd[:160], out.stdout)
        self.assertNotIn(cmd, out.stdout)

    def test_blank_lines_non_json_and_other_events_are_skipped(self):
        out = self.parse("\n\nnot json\n{}\n" + jsonl(
            {"type": "item.started", "item": {"type": "agent_message", "text": "partial"}},
            {"type": "item.completed", "item": {"type": "agent_message"}},
            {"type": "item.completed", "item": {"type": "reasoning", "text": "hidden"}},
            {"type": "item.completed", "item": {"type": "command_execution"}},
            message("ok"), DONE))
        self.assertEqual(out.returncode, 0, out.stderr)
        self.assertEqual(out.stdout, "ok\n\n<!-- tokens: in 10 out 5 -->\n")
        self.assertEqual(out.stderr, "")

    def test_missing_usage_counts_as_zero_tokens(self):
        out = self.parse(jsonl(message("ok"), {"type": "turn.completed"}))
        self.assertEqual(out.returncode, 0, out.stderr)
        self.assertEqual(out.stdout, "ok\n\n<!-- tokens: in 0 out 0 -->\n")

    def test_item_errors_go_to_stderr_not_into_the_review(self):
        out = self.parse(jsonl({"type": "item.completed", "item": {"type": "error", "message": "tool blew up"}},
                               message("ok"), DONE))
        self.assertEqual(out.returncode, 0, out.stderr)
        self.assertIn("[codex item error] tool blew up\n", out.stderr)
        self.assertEqual(out.stdout, "ok\n\n<!-- tokens: in 10 out 5 -->\n")

    def test_a_failed_turn_exits_3_with_the_reason_on_stderr(self):
        # codex_review.sh deletes the review file on a non-zero parser exit, so
        # the code is what separates "Codex said nothing" from "Codex was refused".
        out = self.parse(jsonl(message("partial"), {"type": "turn.failed", "error": {"message": "usage limit reached"}}))
        self.assertEqual(out.returncode, 3)
        self.assertIn("[codex turn FAILED] usage limit reached\n", out.stderr)
        self.assertIn("no review was produced", out.stderr)
        self.assertEqual(out.stdout, "partial\n")
        out = self.parse(jsonl({"type": "turn.failed"}))
        self.assertEqual(out.returncode, 3)
        self.assertIn("[codex turn FAILED] no message\n", out.stderr)

    def test_an_error_event_fails_the_run_even_if_the_turn_then_completes(self):
        out = self.parse(jsonl({"type": "error", "message": "refused"}, message("ok"), DONE))
        self.assertEqual(out.returncode, 3)
        self.assertIn("[codex error] refused\n", out.stderr)

    def test_no_turn_completed_exits_4(self):
        # A mid-stream disconnect looks like a short review; only the exit code tells.
        out = self.parse(jsonl(message("looks complete")))
        self.assertEqual(out.returncode, 4)
        self.assertIn("no turn.completed", out.stderr)
        self.assertEqual(out.stdout, "looks complete\n")
        out = self.parse("")
        self.assertEqual(out.returncode, 4)
        self.assertEqual(out.stdout, "")

    def test_a_completed_turn_with_no_message_exits_5(self):
        # Used to exit 0: the "review" was one HTML comment with a token count,
        # and codex_review.sh kept it as if Codex had answered.
        for stream in (jsonl(DONE),
                       jsonl({"type": "item.completed", "item": {"type": "command_execution", "command": "ls"}}, DONE),
                       jsonl({"type": "item.completed", "item": {"type": "agent_message", "text": ""}}, DONE)):
            with self.subTest(stream=stream):
                out = self.parse(stream)
                self.assertEqual(out.returncode, 5)
                self.assertIn("without an agent message", out.stderr)
                self.assertIn("<!-- tokens: in 10 out 5 -->\n", out.stdout)

    def test_a_failure_outranks_the_silence_code(self):
        # 3 and 4 keep their meaning; 5 only applies to a turn that finished cleanly.
        self.assertEqual(self.parse(jsonl({"type": "error", "message": "refused"}, DONE)).returncode, 3)
        self.assertEqual(self.parse(jsonl({"type": "item.completed",
                                           "item": {"type": "command_execution", "command": "ls"}})).returncode, 4)


# ---------------------------------------------------------------- codex_review.sh

class TestCodexReviewPreflight(unittest.TestCase):
    """codex_review.sh up to the point it would call codex.

    A throwaway git repo stands in for this one and a fake `codex` sits first
    on PATH, so a guard that lets a run through is caught by the sentinel the
    fake drops, not by a real Codex session.
    """

    SCRIPT = os.path.join(HERE, "codex_review.sh")
    DIGESTS = ("arxiv.md", "x_digest.md", "community_digest.md", "notion_digest.md")
    JSONL_OK = ('{"type":"item.completed","item":{"type":"agent_message","text":"審查 ok"}}\n'
                '{"type":"turn.completed","usage":{"input_tokens":1,"output_tokens":2}}\n')

    def repo(self, digests):
        root = tempfile.TemporaryDirectory()
        self.addCleanup(root.cleanup)
        subprocess.run(["git", "init", "-q", root.name], check=True)
        month = os.path.join(root.name, "research", "2026-01")
        os.makedirs(month)
        write(os.path.join(month, "outline.md"), "# 大綱\n")
        for name in ("selection.md", "style_brief.md") + tuple(digests):
            write(os.path.join(month, name), "x\n")
        fake_bin = os.path.join(root.name, "bin")
        os.makedirs(fake_bin)
        sentinel = os.path.join(root.name, "codex-was-called")
        fake = os.path.join(fake_bin, "codex")
        write(fake, "#!/bin/sh\ntouch %s\ncat <<'EOF'\n%sEOF\n" % (shlex.quote(sentinel), self.JSONL_OK))
        os.chmod(fake, 0o755)
        return root.name, month, sentinel, fake_bin

    def review(self, root, fake_bin, target="research/2026-01/outline.md"):
        env = {**os.environ, "PATH": fake_bin + os.pathsep + os.environ.get("PATH", ""), "HOME": root}
        return subprocess.run(["bash", self.SCRIPT, target], cwd=root, env=env,
                              capture_output=True, text=True, encoding="utf-8")

    def test_missing_digests_exit_64_before_codex_runs(self):
        # The prompt tells Codex the four digests are in the repo and are the
        # only allowed sources; two are gitignored, so a fresh clone lacks them
        # and Codex would call every citation to them invented.
        root, month, sentinel, fake_bin = self.repo(digests=("arxiv.md", "x_digest.md"))
        out = self.review(root, fake_bin)
        self.assertEqual(out.returncode, 64, out.stderr)
        self.assertIn("research/2026-01/community_digest.md", out.stderr)
        self.assertIn("research/2026-01/notion_digest.md", out.stderr)
        self.assertNotIn("research/2026-01/arxiv.md", out.stderr)
        self.assertIn("research/README.md「資料來源」", out.stderr)
        self.assertFalse(os.path.exists(sentinel))
        self.assertFalse(os.path.exists(os.path.join(month, "codex-review-outline.md")))

    def test_with_every_digest_present_the_review_reaches_codex_and_is_written(self):
        root, month, sentinel, fake_bin = self.repo(digests=self.DIGESTS)
        out = self.review(root, fake_bin)
        self.assertEqual(out.returncode, 0, out.stderr)
        self.assertTrue(os.path.exists(sentinel))
        review = read(os.path.join(month, "codex-review-outline.md"))
        self.assertIn("# Codex review — outline", review)
        self.assertIn("審查 ok\n", review)
        self.assertIn("<!-- tokens: in 1 out 2 -->", review)


# ---------------------------------------------------------------- merge.py

class MergeContract:
    """The merge as collect.sh drives it, once per key field."""

    KEY = None
    ARGS = ()

    def rec(self, key, **extra):
        item = {self.KEY: key}
        item.update(extra)
        return item

    def files(self, current, batch):
        root = tempfile.TemporaryDirectory()
        self.addCleanup(root.cleanup)
        target = os.path.join(root.name, "all.json")
        add = os.path.join(root.name, "_batch.json")
        if current is not None:
            write(target, current if isinstance(current, str) else json.dumps(current))
        write(add, batch if isinstance(batch, str) else json.dumps(batch))
        return target, add

    def merge_cmd(self, target, add, *extra):
        return run_script("merge", target, add, *self.ARGS, *extra)

    def merge(self, current, batch, *extra):
        target, add = self.files(current, batch)
        out = self.merge_cmd(target, add, *extra)
        self.assertEqual(out.returncode, 0, out.stderr)
        return out.stdout.strip(), json.loads(read(target))

    def test_new_keys_are_appended_and_the_first_copy_of_a_key_wins(self):
        count, got = self.merge([self.rec("a", text="old")],
                                [self.rec("a", text="new"), self.rec("b"), self.rec("b", text="dup")])
        self.assertEqual(got, [self.rec("a", text="old"), self.rec("b")])
        # collect.sh reads this number to notice when scrolling stops yielding new items
        self.assertEqual(count, "2")

    def test_entries_without_a_key_are_dropped_from_both_sides(self):
        count, got = self.merge([{"text": "orphan"}, self.rec("a")],
                                [{"text": "orphan"}, self.rec(""), "not even a dict", 7, self.rec("b")])
        self.assertEqual(got, [self.rec("a"), self.rec("b")])
        self.assertEqual(count, "2")

    def test_a_missing_or_empty_target_starts_from_empty(self):
        for current in (None, "", " \n"):
            with self.subTest(current=current):
                count, got = self.merge(current, [self.rec("b")])
                self.assertEqual(got, [self.rec("b")])
                self.assertEqual(count, "1")

    def test_a_corrupt_target_is_fatal_and_left_exactly_as_it_was(self):
        # The old script reset a corrupt store to {} and then wrote the batch
        # over it: a month of collection replaced by one scroll's worth.
        for current in ("not json", "[1, 2", json.dumps(self.rec("a")), json.dumps({"items": []})):
            with self.subTest(current=current):
                target, add = self.files(current, [self.rec("b")])
                out = self.merge_cmd(target, add)
                self.assertNotEqual(out.returncode, 0)
                self.assertIn("not touching it", out.stderr)
                self.assertIn(target, out.stderr)
                self.assertEqual(out.stdout, "")
                self.assertEqual(read(target), current)
                self.assertEqual(sorted(os.listdir(os.path.dirname(target))), ["_batch.json", "all.json"])

    def test_a_corrupt_batch_rewrites_the_target_unchanged(self):
        # The extractor returned garbage or nothing; what was already collected survives.
        for batch in ("", "not json", json.dumps({"error": "timeout"}), json.dumps("str")):
            with self.subTest(batch=batch):
                count, got = self.merge([self.rec("a", n=1)], batch)
                self.assertEqual(got, [self.rec("a", n=1)])
                self.assertEqual(count, "1")

    def test_a_batch_that_is_not_a_list_is_said_on_stderr_not_stdout(self):
        # collect.sh captures stdout as the count; a warning there would break
        # its `[ "$n" = "$prev" ]` comparison.
        target, add = self.files([self.rec("a")], {"error": "timeout"})
        out = self.merge_cmd(target, add)
        self.assertEqual(out.returncode, 0, out.stderr)
        self.assertEqual(out.stdout, "1\n")
        self.assertIn("not a JSON list", out.stderr)
        target, add = self.files([self.rec("a")], "")
        out = self.merge_cmd(target, add)
        self.assertEqual((out.returncode, out.stdout, out.stderr), (0, "1\n", ""))

    def test_a_missing_batch_file_counts_as_empty(self):
        target, add = self.files([self.rec("a")], [])
        os.unlink(add)
        out = self.merge_cmd(target, add)
        self.assertEqual((out.returncode, out.stdout), (0, "1\n"), out.stderr)
        self.assertIn("unreadable", out.stderr)

    def test_tag_stamps_only_the_items_the_batch_adds(self):
        # The inline merges in collect.sh set t['source'] before setdefault, so
        # an item already collected under another tag kept its tag.
        count, got = self.merge([self.rec("a", source="old")],
                                [self.rec("a"), self.rec("b", source="wrong"), self.rec("c")],
                                "--tag", "group:xyz")
        self.assertEqual(got, [self.rec("a", source="old"), self.rec("b", source="group:xyz"),
                               self.rec("c", source="group:xyz")])
        self.assertEqual(count, "3")

    def test_without_tag_no_source_field_is_invented(self):
        _, got = self.merge([], [self.rec("a")])
        self.assertEqual(got, [self.rec("a")])

    def test_non_ascii_is_stored_readable(self):
        target, add = self.files([], [self.rec("a", text="中文貼文")])
        out = self.merge_cmd(target, add)
        self.assertEqual(out.returncode, 0, out.stderr)
        raw = read(target)
        self.assertIn("中文貼文", raw)
        self.assertNotIn("\\u", raw)

    def test_the_write_leaves_no_temp_file_behind(self):
        target, add = self.files([self.rec("a")], [self.rec("b")])
        out = self.merge_cmd(target, add)
        self.assertEqual(out.returncode, 0, out.stderr)
        self.assertEqual(sorted(os.listdir(os.path.dirname(target))), ["_batch.json", "all.json"])


class TestMergePosts(MergeContract, unittest.TestCase):
    KEY = "link"


class TestMergeAccounts(MergeContract, unittest.TestCase):
    """x_following_users.json: the same merge keyed on the handle (was merge_users.py)."""
    KEY = "handle"
    ARGS = ("--key", "handle")

    def test_the_default_key_would_drop_every_account(self):
        # Pins that --key is load-bearing: accounts carry no link.
        target, add = self.files([], [self.rec("alice"), self.rec("bob")])
        out = run_script("merge", target, add)
        self.assertEqual((out.returncode, out.stdout), (0, "0\n"), out.stderr)


class TestMergeCLI(unittest.TestCase):
    def test_an_unknown_key_field_is_refused(self):
        with tempfile.TemporaryDirectory() as root:
            write(os.path.join(root, "b.json"), "[]")
            out = run_script("merge", os.path.join(root, "a.json"), os.path.join(root, "b.json"), "--key", "email")
            self.assertNotEqual(out.returncode, 0)
            self.assertIn("invalid choice", out.stderr)
            self.assertFalse(os.path.exists(os.path.join(root, "a.json")))

    def test_merge_users_is_gone_so_there_is_one_merge_to_maintain(self):
        self.assertFalse(os.path.exists(os.path.join(HERE, "merge_users.py")))


# ---------------------------------------------------------------- notion_cookies.py

class TestNotionCookies(unittest.TestCase):
    def test_usage_error_exits_before_the_keychain_is_touched(self):
        out = run_script("notion_cookies", "notion.com")
        self.assertNotEqual(out.returncode, 0)
        self.assertIn("usage: notion_cookies.py <domain> <out.json>", out.stderr)

    def test_reuses_chrome_cookies_but_points_it_at_the_notion_app(self):
        cc = notion_cookies.cc
        self.assertEqual(cc.__file__, os.path.join(REPO, "tools", "chrome_cookies.py"))
        self.assertTrue(cc.CHROME_DIR.endswith("/Library/Application Support/Notion/Partitions"), cc.CHROME_DIR)
        self.assertEqual(cc.CHROME_DIR, notion_cookies.NOTION_DIR)

    def test_keychain_refusal_or_empty_secret_exits_with_the_error(self):
        # The lookup is chrome_cookies.safe_storage_key with Notion's item names,
        # so it is that module's subprocess that has to be faked.
        cases = ((1, "", "User interaction is not allowed."), (0, "\n", ""))
        for rc, stdout, stderr in cases:
            with self.subTest(rc=rc, stdout=stdout):
                fake = subprocess.CompletedProcess(args=[], returncode=rc, stdout=stdout, stderr=stderr)
                with mock.patch.object(notion_cookies.cc.subprocess, "run", return_value=fake) as run:
                    with self.assertRaises(SystemExit) as cm:
                        notion_cookies.notion_key()
                self.assertIn("Notion Safe Storage", str(cm.exception))
                self.assertIn(stderr.strip(), str(cm.exception))
                self.assertEqual(run.call_args[0][0], ["security", "find-generic-password", "-w",
                                                       "-s", "Notion Safe Storage", "-a", "Notion Key"])

    def test_the_secret_is_stretched_like_chrome_and_an_empty_export_is_refused(self):
        seen = {}

        def fake_read_profile(profile, domain, hexkey, hexiv, subdomains=False):
            seen.update(profile=profile, domain=domain, hexkey=hexkey, hexiv=hexiv, subdomains=subdomains)
            return []

        with mock.patch.object(notion_cookies, "notion_key", return_value=b"secret"), \
                mock.patch.object(notion_cookies.cc, "read_profile", fake_read_profile), \
                mock.patch.object(sys, "argv", ["notion_cookies.py", "notion.com", "/nonexistent/out.json"]), \
                mock.patch("sys.stdout", new_callable=io.StringIO):
            with self.assertRaises(SystemExit) as cm:
                notion_cookies.main()
        self.assertEqual(str(cm.exception), "no cookies for notion.com")
        cc = notion_cookies.cc
        expected = hashlib.pbkdf2_hmac("sha1", b"secret", b"saltysalt", cc.PBKDF2_ITERATIONS, cc.AES_KEY_BYTES).hex()
        self.assertEqual(seen, {"profile": "notion", "domain": "notion.com", "hexkey": expected,
                                "hexiv": (b" " * 16).hex(), "subdomains": True})
        # and it is chrome_cookies' derivation, not a private copy
        self.assertEqual(cc.derive_key(b"secret"), (expected, (b" " * 16).hex()))

    def test_cookies_found_are_written_with_the_private_writer(self):
        cookies = [{"name": "token_v2", "domain": "app.notion.com"}, {"name": "notion_user_id", "domain": ".notion.com"}]
        written = {}
        with mock.patch.object(notion_cookies, "notion_key", return_value=b"secret"), \
                mock.patch.object(notion_cookies.cc, "read_profile", return_value=cookies), \
                mock.patch.object(notion_cookies.cc, "write_private",
                                  lambda path, cs: written.update(path=path, cookies=cs)), \
                mock.patch.object(sys, "argv", ["notion_cookies.py", "notion.so", "/tmp/w/nso.json"]), \
                mock.patch("sys.stdout", new_callable=io.StringIO) as out:
            notion_cookies.main()
        self.assertEqual(written, {"path": "/tmp/w/nso.json", "cookies": cookies})
        self.assertIn("notion.so -> 2 cookies: ['notion_user_id', 'token_v2']", out.getvalue())
        self.assertIn("live session", out.getvalue())


if __name__ == "__main__":
    unittest.main(verbosity=2)
