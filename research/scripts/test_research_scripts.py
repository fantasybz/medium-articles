#!/usr/bin/env python3
"""Tests for the pure-Python research scripts. Stdlib only, no network, no browser.

    python3 -m unittest research/scripts/test_research_scripts.py -v
    python3 research/scripts/test_research_scripts.py

research/README.md keeps research/scripts out of tools/ because the extractors
depend on live DOMs. This covers the part that does not: the article -> paste
mapping and its figures.json, the outline <-> figures.md id matching, the codex
JSONL parser whose exit codes codex_review.sh branches on, the two merge
scripts whose printed count collect.sh reads, and the argument / keychain
guards of the Notion cookie export. Everything that needs a browser, a Codex
session or the macOS Keychain (collect.sh, extract_*.js, notion_*.js,
mermaid_check*.sh, render_images.sh, codex_review.sh) is deliberately absent.

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

    def test_double_em_dash_is_refused_in_prose_but_allowed_inside_code(self):
        # md2medium.py refuses it too; failing here saves a browser run.
        art = self.article_dir("# T\n\n這裡——會裂\n")
        out = run_script("article_to_paste", art)
        self.assertNotEqual(out.returncode, 0)
        self.assertIn("double em dash", out.stderr)
        self.assertFalse(os.path.exists(os.path.join(art, "publish")))
        art = self.article_dir("# T\n\n```\nprint('——')\n```\n")
        out = run_script("article_to_paste", art)
        self.assertEqual(out.returncode, 0, out.stderr)


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
        self.assertEqual(read(path), "**F1（封面）**—圖說，分類沿用 T2 的表\n\n" + fence(self.NEW_F1))
        self.assertIn("replaced 1: ['F1']", out.stdout)

    def test_without_a_label_the_last_id_mentioned_wins(self):
        src = "先講 F1，再講 T2 的表\n\n" + fence(self.OLD)
        path = self.outline(src)
        run_script("sync_figures", path)
        self.assertEqual(read(path), "先講 F1，再講 T2 的表\n\n" + fence(self.NEW_T2))

    def test_blocks_with_no_verified_counterpart_are_left_alone_and_listed(self):
        # The second block sits more than 600 characters after any id, so it has none.
        src = "圖 F9（figures.md 裡沒有）\n\n" + fence(self.OLD) + "\n" + "x" * 700 + "\n\n" + fence(self.OLD)
        path = self.outline(src)
        out = run_script("sync_figures", path)
        self.assertEqual(out.returncode, 0, out.stderr)
        self.assertEqual(read(path), src)
        self.assertIn("replaced 0: []", out.stdout)
        self.assertIn("unmatched 2: [(None, 'xxxx", out.stdout)
        self.assertIn("('F9', ", out.stdout)

    def test_two_blocks_resolving_to_the_same_id_are_flagged(self):
        src = "圖 F1（封面）\n\n" + fence(self.OLD) + "\n同一張 F1 再貼一次\n\n" + fence("flowchart TB\n    Q\n")
        path = self.outline(src)
        out = run_script("sync_figures", path)
        self.assertEqual(out.returncode, 0, out.stderr)
        # both were overwritten, so the report is the only signal
        self.assertEqual(read(path).count(self.NEW_F1), 2)
        self.assertIn("DUPLICATE assignments (fix by hand): ['F1']", out.stdout)

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

    def test_commands_are_logged_as_html_comments_cut_at_160_chars(self):
        cmd = "grep -rn " + "x" * 200
        out = self.parse(jsonl({"type": "item.completed",
                                "item": {"type": "command_execution", "command": cmd}}, DONE))
        self.assertEqual(out.returncode, 0, out.stderr)
        self.assertIn("<!-- codex ran: %s -->\n" % cmd[:160], out.stdout)
        self.assertNotIn(cmd, out.stdout)

    def test_blank_lines_non_json_and_other_events_are_skipped(self):
        out = self.parse("\n\nnot json\n{}\n" + jsonl(
            {"type": "item.started", "item": {"type": "agent_message", "text": "partial"}},
            {"type": "item.completed", "item": {"type": "agent_message"}},
            {"type": "item.completed", "item": {"type": "reasoning", "text": "hidden"}},
            {"type": "item.completed", "item": {"type": "command_execution"}},
            DONE))
        self.assertEqual(out.returncode, 0, out.stderr)
        self.assertEqual(out.stdout, "\n<!-- tokens: in 10 out 5 -->\n")
        self.assertEqual(out.stderr, "")

    def test_missing_usage_counts_as_zero_tokens(self):
        out = self.parse(jsonl({"type": "turn.completed"}))
        self.assertEqual(out.returncode, 0, out.stderr)
        self.assertEqual(out.stdout, "\n<!-- tokens: in 0 out 0 -->\n")

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
        out = self.parse(jsonl({"type": "error", "message": "refused"}, DONE))
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


# ---------------------------------------------------------------- merge.py / merge_users.py

class MergeContract:
    """Shared by both merge scripts; they differ only in the key field."""

    SCRIPT = None
    KEY = None

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

    def merge(self, current, batch):
        target, add = self.files(current, batch)
        out = run_script(self.SCRIPT, target, add)
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
                                [{"text": "orphan"}, self.rec(""), self.rec("b")])
        self.assertEqual(got, [self.rec("a"), self.rec("b")])
        self.assertEqual(count, "2")

    def test_a_missing_or_corrupt_target_starts_from_empty(self):
        for current in (None, "", "not json", json.dumps(self.rec("a"))):
            with self.subTest(current=current):
                count, got = self.merge(current, [self.rec("b")])
                self.assertEqual(got, [self.rec("b")])
                self.assertEqual(count, "1")

    def test_a_corrupt_batch_rewrites_the_target_unchanged(self):
        # The extractor returned garbage or nothing; what was already collected survives.
        for batch in ("", "not json"):
            with self.subTest(batch=batch):
                count, got = self.merge([self.rec("a", n=1)], batch)
                self.assertEqual(got, [self.rec("a", n=1)])
                self.assertEqual(count, "1")

    def test_non_ascii_is_stored_readable(self):
        target, add = self.files([], [self.rec("a", text="中文貼文")])
        out = run_script(self.SCRIPT, target, add)
        self.assertEqual(out.returncode, 0, out.stderr)
        raw = read(target)
        self.assertIn("中文貼文", raw)
        self.assertNotIn("\\u", raw)


class TestMergePosts(MergeContract, unittest.TestCase):
    SCRIPT = "merge"
    KEY = "link"


class TestMergeUsers(MergeContract, unittest.TestCase):
    SCRIPT = "merge_users"
    KEY = "handle"


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

    def test_keychain_refusal_or_empty_secret_exits_with_the_error(self):
        cases = ((1, "", "User interaction is not allowed."), (0, "\n", ""))
        for rc, stdout, stderr in cases:
            with self.subTest(rc=rc, stdout=stdout):
                fake = subprocess.CompletedProcess(args=[], returncode=rc, stdout=stdout, stderr=stderr)
                with mock.patch.object(notion_cookies.subprocess, "run", return_value=fake) as run:
                    with self.assertRaises(SystemExit) as cm:
                        notion_cookies.notion_key()
                self.assertIn("Notion Safe Storage", str(cm.exception))
                self.assertIn(stderr.strip(), str(cm.exception))
                self.assertEqual(run.call_args[0][0][:3], ["security", "find-generic-password", "-w"])

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
