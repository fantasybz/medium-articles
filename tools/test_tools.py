#!/usr/bin/env python3
"""Tests for the publishing tools. Stdlib only, no network, no browser.

    python3 tools/test_tools.py

What these actually protect: the markdown conversion has mappings that are easy
to "clean up" and silently break (`###` must emit `<h4>`, blank lines inside a
code block must not stay blank), and the cookie filter has a regression that
already bit once. What happens inside Medium's own editor is not covered here —
that needs a real session, and `medium_draft.sh` verifies itself against the
source at the end of every run.

The driver's decisions are covered, though, and have to be: `--post <id>`
refills a live post, so which page it opens, which snippet it pastes and which
guard stops it are not things to find out on a published article. `browse` is
replaced by a recorder (see FAKE_BROWSE) and the run is driven either until a
guard fires or all the way to the closing message, which is as far as any of
that can be seen without a browser. What is NOT covered is everything on the
far side of that recorder: what Medium's own editor does with a paste is still
only checked at run time, by the driver, against the converted payload.
"""

import base64
import glob
import json
import os
import re
import shutil
import sqlite3
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import chrome_cookies
import md2medium
import medium_js
import medium_patch
import verify_draft


class TestInline(unittest.TestCase):
    def test_link_bold_italic_code(self):
        got = md2medium.inline(
            "see [docs](https://x.test/a?b=1) and **bold** and *em* and `code`")
        self.assertIn('<a href="https://x.test/a?b=1">docs</a>', got)
        self.assertIn("<strong>bold</strong>", got)
        self.assertIn("<em>em</em>", got)
        self.assertIn("<code>code</code>", got)

    def test_code_span_contents_are_escaped_not_parsed(self):
        # `<path>` inside a code span must survive as text, not become a tag.
        got = md2medium.inline("run `make test FILTER=<path>`")
        self.assertIn("<code>make test FILTER=&lt;path&gt;</code>", got)

    def test_bare_angle_brackets_are_escaped(self):
        self.assertEqual(md2medium.inline("a < b > c"), "a &lt; b &gt; c")

    def test_asterisk_inside_bold_is_not_re_italicised(self):
        self.assertEqual(md2medium.inline("**a b**"), "<strong>a b</strong>")

    def test_url_with_query_ampersand_is_escaped_once(self):
        # The line has already been through html.escape; escaping the captured
        # URL again ships &amp;amp; and a link that 404s.
        got = md2medium.inline("[a](https://x.test/?b=1&c=2)")
        self.assertIn('<a href="https://x.test/?b=1&amp;c=2">a</a>', got)
        self.assertNotIn("&amp;amp;", got)

    def test_url_may_contain_a_balanced_paren(self):
        # Wikipedia titles do this constantly, and the truncated href 404s
        # while the anchor count and the visible text both still match.
        got = md2medium.inline("[Foo](https://en.wikipedia.org/wiki/Foo_(bar))")
        self.assertIn('href="https://en.wikipedia.org/wiki/Foo_(bar)"', got)
        self.assertNotIn(")</p>", got)

    def test_quote_in_url_cannot_close_the_href_attribute(self):
        got = md2medium.inline('[a](https://x.test/"onerror=x)')
        self.assertNotIn('"onerror', got)
        self.assertIn("&quot;", got)


class TestConvert(unittest.TestCase):
    def convert(self, text):
        return md2medium.convert(text)

    def test_title_comes_from_h1_and_is_not_in_the_body(self):
        out = self.convert("# Hello\n\nbody\n")
        self.assertEqual(out["title"], "Hello")
        self.assertNotIn("Hello", out["html"])

    def test_missing_title_is_an_error(self):
        with self.assertRaises(SystemExit):
            self.convert("no heading here\n")

    def test_guide_comment_is_stripped(self):
        out = self.convert("<!--\nchecklist\n-->\n\n# T\n\nbody\n")
        self.assertNotIn("checklist", out["html"])

    def test_heading_levels_map_to_mediums_two_sizes(self):
        # Medium collapses h1/h2/h3 onto graf--h3 and only drops to graf--h4
        # at h4, so a section title must be h2 and a subheading must be h4.
        out = self.convert("# T\n\n## Section\n\n### Sub\n")
        self.assertIn("<h2>Section</h2>", out["html"])
        self.assertIn("<h4>Sub</h4>", out["html"])

    def test_blank_line_inside_code_block_becomes_a_space(self):
        # A truly blank line splits the graf into separate code boxes.
        out = self.convert("# T\n\n```\na\n\nb\n```\n")
        self.assertIn("<pre><code>a\n \nb</code></pre>", out["html"])

    def test_code_block_is_escaped_and_stays_one_block(self):
        out = self.convert("# T\n\n```\n<tag> & co\n```\n")
        self.assertEqual(out["html"].count("<pre>"), 1)
        self.assertIn("&lt;tag&gt; &amp; co", out["html"])

    def test_image_slot_becomes_a_findable_marker(self):
        out = self.convert("# T\n\n📌【在此插入圖 diagram-01.png】\n")
        self.assertEqual(out["images"], ["diagram-01.png"])
        self.assertIn("<p>IMGSLOT-diagram-01.png-ENDSLOT</p>", out["html"])

    def test_a_slot_line_the_pattern_rejects_is_not_demoted_to_body_text(self):
        # It used to become a paragraph: the figure went missing, a raw Chinese
        # instruction line shipped, and every downstream check stayed green.
        for bad in ("📌【在此插入圖 my_image.png】",
                    "📌【在此插入圖 chart.jpg】",
                    "📌【在此插入圖 fig 01.png】"):
            with self.assertRaises(SystemExit, msg=bad):
                self.convert("# T\n\n%s\n" % bad)

    def test_table_slots_are_recognised_too(self):
        out = self.convert("# T\n\n📌【在此插入表 table-06.png】\n")
        self.assertEqual(out["images"], ["table-06.png"])

    def test_lists_blockquotes_and_rules(self):
        out = self.convert(
            "# T\n\n- one\n- two\n\n1. first\n2. second\n\n> quoted\n\n---\n")
        self.assertIn("<ul><li>one</li><li>two</li></ul>", out["html"])
        self.assertIn("<ol><li>first</li><li>second</li></ol>", out["html"])
        self.assertIn("<blockquote>quoted</blockquote>", out["html"])
        self.assertIn("<hr>", out["html"])

    def test_wrapped_list_item_continuation_joins_the_item(self):
        out = self.convert("# T\n\n- one\n  continued\n- two\n")
        self.assertIn("<li>one continued</li>", out["html"])

    def test_wrapped_paragraph_lines_join(self):
        out = self.convert("# T\n\nline one\nline two\n")
        self.assertIn("<p>line one line two</p>", out["html"])

    def test_slot_after_paragraph_is_not_swallowed_into_it(self):
        out = self.convert("# T\n\nlead in:\n📌【在此插入圖 d.png】\n")
        self.assertIn("<p>lead in:</p>", out["html"])
        self.assertEqual(out["images"], ["d.png"])


class TestSlotLine(unittest.TestCase):
    """slot_line writes what SLOT_RE reads; article_to_paste.py relies on it."""

    def test_both_kinds_round_trip_through_the_slot_pattern(self):
        for kind, name in (("圖", "diagram-01.png"), ("表", "table-12.png")):
            line = md2medium.slot_line(kind, name)
            m = md2medium.SLOT_RE.match(line)
            self.assertIsNotNone(m, line)
            self.assertEqual(m.group(1), name)
            self.assertIn(kind, line)

    def test_the_converter_treats_the_written_line_as_a_figure(self):
        # Not just the regex: the whole pipeline has to see an image slot, not
        # a paragraph of body text.
        body = "\n\n".join(["# T", md2medium.slot_line("圖", "diagram-01.png"),
                            md2medium.slot_line("表", "table-01.png")])
        out = md2medium.convert(body + "\n")
        self.assertEqual(out["images"], ["diagram-01.png", "table-01.png"])
        self.assertNotIn("📌", out["html"])

    def test_an_unknown_kind_is_refused(self):
        with self.assertRaises(ValueError):
            md2medium.slot_line("image", "diagram-01.png")

    def test_a_name_the_pattern_would_reject_is_refused_at_write_time(self):
        # Emitting it would put a 📌 line in the paste that convert() later
        # dies on; better to fail where the name is chosen.
        for bad in ("diagram 01.png", "diagram-01.jpg", "圖.png", ""):
            with self.assertRaises(ValueError, msg=bad):
                md2medium.slot_line("圖", bad)


class TestAutocorrectGuard(unittest.TestCase):
    # Medium turns (c) into © on paste; the October 總論 lost its third
    # evidence label that way before verify_draft noticed.
    def test_c_r_tm_in_prose_are_flagged_with_their_line(self):
        lines = ["intro", "the (c) label", "and (R) here", "fine (a) and (b)", "a (TM) mark"]
        self.assertEqual([k for k, _ in md2medium.autocorrect_lines(lines)], [2, 3, 5])

    def test_inside_a_code_fence_they_are_left_alone(self):
        lines = ["```python", "print('(c)')", "```", "after"]
        self.assertEqual(md2medium.autocorrect_lines(lines), [])

    def test_convert_refuses_a_paste_with_a_c_label(self):
        with self.assertRaises(SystemExit) as cm:
            md2medium.convert("# T\n\nonly (c) counts\n")
        self.assertIn("autocorrect", str(cm.exception))

    def test_full_width_and_bracketless_labels_pass(self):
        payload = md2medium.convert("# T\n\n（c） and c) are fine\n")
        self.assertIn("（c） and c) are fine", payload["html"])


class TestVerifyDraft(unittest.TestCase):
    payload = {
        "title": "T",
        "html": "\n".join([
            "<p>alpha</p>",
            "<hr>",
            "<p>IMGSLOT-a.png-ENDSLOT</p>",
            "<ul><li>one</li><li>two</li></ul>",
            "<pre><code>x",
            "y</code></pre>",
        ]),
    }

    def blocks(self):
        return verify_draft.expected_blocks(self.payload)

    def test_dividers_and_slots_are_not_grafs(self):
        # A <hr> is a section divider and a slot becomes a figure; neither
        # shows up in the text grafs the editor reports back.
        joined = "\n".join(self.blocks())
        self.assertNotIn("<hr>", joined)
        self.assertNotIn("IMGSLOT", joined)

    def test_list_items_become_separate_blocks(self):
        self.assertIn("one", [verify_draft.normalise(b, True) for b in self.blocks()])
        self.assertIn("two", [verify_draft.normalise(b, True) for b in self.blocks()])

    def test_multi_line_pre_stays_one_block(self):
        norm = [verify_draft.normalise(b, True) for b in self.blocks()]
        self.assertIn("x\ny", norm)

    def test_title_leads(self):
        self.assertEqual(self.blocks()[0], "T")

    def test_medium_en_dash_in_dates_is_folded_back_to_a_hyphen(self):
        # Medium rewrites 2026-07-10 as 2026–07–10 (U+2013 between digits); the
        # October References carry dates outside the link text, so the first
        # draft reported 15 false mismatches on nothing but that dash.
        source = verify_draft.normalise("<p>arXiv（2026-07-10）</p>", True)
        editor = verify_draft.normalise("arXiv（2026\u201307\u201310）", False)
        self.assertEqual(source, editor)
        # Between words the en dash is the author's own character: keep it.
        self.assertNotEqual(verify_draft.normalise("a\u2013b", False), "a-b")

    def test_medium_superscript_digits_fold_back_to_the_caret(self):
        # Medium renders pass^5 as pass⁵ and pass^20 as pass²⁰ (pass^k stays);
        # the 可靠度篇 draft reported five false mismatches on that alone.
        source = verify_draft.normalise("<p>pass^5 與 pass^20，pass^k 不變</p>", True)
        editor = verify_draft.normalise("pass\u2075 與 pass\u00b2\u2070，pass^k 不變", False)
        self.assertEqual(source, editor)

    def test_medium_typography_is_normalised_away(self):
        # Medium wraps em dashes in hair spaces; that is not lost content.
        source = verify_draft.normalise("<p>a——b</p>", True)
        editor = verify_draft.normalise("a — —  b", False)
        self.assertEqual(source, editor)

    def test_code_language_label_is_ignored(self):
        self.assertEqual(verify_draft.normalise("x\nAuto (VB.NET)", False), "x")

    def test_curly_double_quotes_are_normalised(self):
        # Medium curls both kinds of quote as house typography, exactly like
        # the hair space around an em dash. Only the singles were folded, which
        # held up while every article was Chinese and quoted with 「」; the
        # first English draft failed 15 correct blocks on quote shape alone.
        self.assertEqual(verify_draft.normalise('say "hi"', False),
                         verify_draft.normalise("say \u201chi\u201d", False))

    def test_curly_quotes_do_not_make_different_text_compare_equal(self):
        self.assertNotEqual(verify_draft.normalise('say "hi"', False),
                            verify_draft.normalise("say \u201cbye\u201d", False))

    def test_nbsp_and_curly_quote_are_normalised(self):
        self.assertEqual(verify_draft.normalise("<p>don’t go</p>", True),
                         verify_draft.normalise("don't go", False))

    def test_title_containing_a_literal_entity_round_trips(self):
        # The title is stored raw for the paste but normalised as HTML, so a
        # title with a literal "&amp;" in it got unescaped to "&" on one side
        # only and false-failed on the very first block.
        title = "Tips &amp; tricks"
        blocks = verify_draft.expected_blocks({"title": title, "html": ""})
        self.assertEqual(verify_draft.normalise(blocks[0], True),
                         verify_draft.normalise(title, False))

    def test_em_dash_normalisation_does_not_eat_newlines(self):
        # \s would swallow a dropped line break inside a code block.
        self.assertNotEqual(verify_draft.normalise("a\n—b", False),
                            verify_draft.normalise("a—b", False))

    def test_word_spacing_loss_is_a_mismatch(self):
        # Deleting all whitespace made welded-together words compare equal, so
        # a real paste failure read as "all blocks match".
        self.assertNotEqual(verify_draft.normalise("a b c", False),
                            verify_draft.normalise("abc", False))

    def test_escaped_markup_in_a_code_block_round_trips(self):
        # Tags must be stripped BEFORE unescaping, or a code block quoting HTML
        # has its own content eaten and the gate false-fails.
        html_out = md2medium.convert("# T\n\n```\n<p>hi</p>\n```\n")["html"]
        self.assertEqual(verify_draft.normalise(html_out, True),
                         verify_draft.normalise("<p>hi</p>", False))

    def test_single_line_pre_does_not_swallow_the_next_block(self):
        blocks = verify_draft.expected_blocks(
            {"title": "T", "html": "<pre><code>x</code></pre>\n<p>after</p>"})
        self.assertEqual(len(blocks), 3)
        self.assertEqual(verify_draft.normalise(blocks[2], True), "after")

    def test_anchor_count_sees_every_link(self):
        payload = md2medium.convert(
            "# T\n\n[a](https://x.test) and [b](https://y.test)\n")
        self.assertEqual(verify_draft.anchor_count(payload), 2)

    def test_angle_brackets_in_code_survive_normalisation(self):
        # innerText gives back a literal <path>; stripping it as a tag would
        # make a real content loss look like a match.
        self.assertEqual(verify_draft.normalise("FILTER=<path>", False), "FILTER=<path>")


class TestFigurePlacement(unittest.TestCase):
    """Order, not just count: the text pass skips figures entirely."""

    payload = {
        "title": "T",
        "html": "\n".join([
            "<p>a</p>",
            "<p>IMGSLOT-one.png-ENDSLOT</p>",
            "<hr>",
            "<ul><li>x</li><li>y</li></ul>",
            "<pre><code>c1",
            "c2</code></pre>",
            "<p>IMGSLOT-two.png-ENDSLOT</p>",
            "<p>b</p>",
        ]),
    }

    def test_positions_account_for_lists_dividers_and_multiline_code(self):
        # title, a, FIG, x, y, pre, FIG, b
        self.assertEqual(verify_draft.expected_figure_positions(self.payload), [2, 6])

    def test_text_blocks_exclude_the_slots(self):
        self.assertEqual(
            [verify_draft.normalise(b, True)
             for b in verify_draft.expected_blocks(self.payload)],
            ["T", "a", "x", "y", "c1\nc2", "b"])

    def test_the_two_views_stay_consistent(self):
        seq = verify_draft.graf_sequence(self.payload)
        self.assertEqual(
            len(seq),
            len(verify_draft.expected_blocks(self.payload))
            + len(verify_draft.expected_figure_positions(self.payload)))


class TestGateCatchesWhatTextCannotSee(unittest.TestCase):
    def gate(self, editor):
        root = tempfile.TemporaryDirectory()
        self.addCleanup(root.cleanup)
        p = os.path.join(root.name, "p.json")
        g = os.path.join(root.name, "g.json")
        payload = md2medium.convert(
            "# T\n\nsee [docs](https://x.test) now\n\n"
            "📌【在此插入圖 a.png】\n\ntail\n")
        with open(p, "w", encoding="utf-8") as fh:
            json.dump(payload, fh, ensure_ascii=False)
        with open(g, "w", encoding="utf-8") as fh:
            json.dump(editor, fh, ensure_ascii=False)
        return run_tool(os.path.join(TOOLS, "verify_draft.py"), p, g)

    def full(self, **over):
        base = {"texts": ["T", "see docs now", "tail"],
                "tags": ["P", "P", "FIGURE", "P"], "links": 1}
        base.update(over)
        return base

    def test_a_correct_draft_passes(self):
        out = self.gate(self.full())
        self.assertEqual(out.returncode, 0, out.stdout)

    def test_lost_hyperlinks_are_caught(self):
        # innerText is identical; only the anchor count differs.
        out = self.gate(self.full(links=0))
        self.assertEqual(out.returncode, 1)
        self.assertIn("links: expected 1", out.stdout)

    def test_a_figure_in_the_wrong_place_is_caught(self):
        out = self.gate(self.full(tags=["P", "FIGURE", "P", "P"]))
        self.assertEqual(out.returncode, 1)
        self.assertIn("figures: expected at graf", out.stdout)

    def test_a_divider_that_should_not_be_there_is_caught(self):
        # A <hr> is not a .graf and has no text, so both passes above are blind
        # to one. Harmless while the only way in was a paste into an empty new
        # story; a refill's range crosses every section wrapper in the article
        # and can leave one behind at either end.
        out = self.gate(self.full(dividers=1))
        self.assertEqual(out.returncode, 1)
        self.assertIn("dividers: expected 0 section breaks, editor has 1", out.stdout)

    def test_a_present_count_is_reported_as_checked(self):
        # "all blocks match" with nothing said about dividers is what this
        # looked like before, and it is indistinguishable from a check that ran
        # and passed. The three extras each name themselves.
        out = self.gate(self.full(dividers=0))
        self.assertEqual(out.returncode, 0, out.stdout)
        self.assertIn("dividers: 0, all accounted for", out.stdout)

    def test_the_dividers_the_payload_asks_for_are_required(self):
        root = tempfile.TemporaryDirectory()
        self.addCleanup(root.cleanup)
        p = os.path.join(root.name, "p.json")
        g = os.path.join(root.name, "g.json")
        payload = md2medium.convert("# T\n\na\n\n---\n\nb\n")
        self.assertEqual(verify_draft.expected_dividers(payload), 1)
        with open(p, "w", encoding="utf-8") as fh:
            json.dump(payload, fh, ensure_ascii=False)
        for dividers, code in ((1, 0), (0, 1), (2, 1)):
            with open(g, "w", encoding="utf-8") as fh:
                json.dump({"texts": ["T", "a", "b"], "tags": ["P", "P", "P"],
                           "links": 0, "dividers": dividers}, fh)
            out = run_tool(os.path.join(TOOLS, "verify_draft.py"), p, g)
            self.assertEqual(out.returncode, code, "%d: %s" % (dividers, out.stdout))
        # An editor payload with no count at all still runs — the usage line in
        # this script pastes a bare array of graf texts — but says out loud
        # that the check did not happen, rather than reading as a match.
        with open(g, "w", encoding="utf-8") as fh:
            json.dump({"texts": ["T", "a", "b"], "tags": ["P", "P", "P"]}, fh)
        out = run_tool(os.path.join(TOOLS, "verify_draft.py"), p, g)
        self.assertEqual(out.returncode, 0, out.stdout)
        self.assertIn("dividers: 1 expected", out.stdout)
        self.assertIn("not checked", out.stdout)

    def test_malformed_editor_output_fails_loudly(self):
        root = tempfile.TemporaryDirectory()
        self.addCleanup(root.cleanup)
        p = os.path.join(root.name, "p.json")
        g = os.path.join(root.name, "g.json")
        with open(p, "w", encoding="utf-8") as fh:
            json.dump({"title": "T", "html": "<p>a</p>"}, fh)
        with open(g, "w", encoding="utf-8") as fh:
            fh.write("browse: command failed")
        out = run_tool(os.path.join(TOOLS, "verify_draft.py"), p, g)
        self.assertEqual(out.returncode, 1)
        self.assertIn("no JSON", out.stderr + out.stdout)


class TestCookieFilter(unittest.TestCase):
    def read(self, hosts, **kw):
        """Stand up a fake ~/Chrome/Default/Cookies and read it back.

        Every row stores a plaintext `value`, so decryption never runs and the
        test needs no keychain.
        """
        root = tempfile.TemporaryDirectory()
        self.addCleanup(root.cleanup)
        profile = os.path.join(root.name, "Default")
        os.makedirs(profile)

        con = sqlite3.connect(os.path.join(profile, "Cookies"))
        con.execute(
            "create table cookies (host_key text, name text, encrypted_value blob,"
            " value text, path text, expires_utc integer, is_secure integer,"
            " is_httponly integer, samesite integer)")
        for host in hosts:
            con.execute("insert into cookies values (?,?,?,?,?,?,?,?,?)",
                        (host, "sid", b"", "v", "/", 0, 1, 1, 1))
        con.commit()
        con.close()

        orig = chrome_cookies.CHROME_DIR
        chrome_cookies.CHROME_DIR = root.name
        self.addCleanup(setattr, chrome_cookies, "CHROME_DIR", orig)
        return chrome_cookies.read_profile(
            "Default", "medium.com", "00" * 16, "20" * 16, **kw)

    def read_rows(self, rows, encrypted=b"", plain="v",
                  hexkey="00" * 16, hexiv="20" * 16):
        """Like read(), but the caller controls the flag and expiry columns."""
        root = tempfile.TemporaryDirectory()
        self.addCleanup(root.cleanup)
        profile = os.path.join(root.name, "Default")
        os.makedirs(profile)
        con = sqlite3.connect(os.path.join(profile, "Cookies"))
        con.execute(
            "create table cookies (host_key text, name text, encrypted_value blob,"
            " value text, path text, expires_utc integer, is_secure integer,"
            " is_httponly integer, samesite integer)")
        for host, samesite, secure, httponly, expires in rows:
            con.execute("insert into cookies values (?,?,?,?,?,?,?,?,?)",
                        (host, "sid", encrypted, plain, "/", expires,
                         secure, httponly, samesite))
        con.commit()
        con.close()
        orig = chrome_cookies.CHROME_DIR
        chrome_cookies.CHROME_DIR = root.name
        self.addCleanup(setattr, chrome_cookies, "CHROME_DIR", orig)
        return chrome_cookies.read_profile("Default", "medium.com", hexkey, hexiv)

    def test_subdomain_cookies_are_dropped_by_default(self):
        # browse cookie-import rejects the whole file if any cookie's domain
        # is not a suffix of the page domain, and reading a published post
        # leaves a fantasybz.medium.com cookie behind.
        got = self.read(["medium.com", ".medium.com", "fantasybz.medium.com"])
        self.assertEqual(sorted(c["domain"] for c in got), [".medium.com", "medium.com"])

    def test_subdomains_flag_keeps_them(self):
        got = self.read(["medium.com", "fantasybz.medium.com"], subdomains=True)
        self.assertEqual(len(got), 2)

    def test_unrelated_domain_is_never_matched(self):
        self.assertEqual(self.read(["notmedium.com"]), [])

    def test_subdomains_flag_still_rejects_lookalike_domains(self):
        # LIKE '%medium.com' also matches notmedium.com, and --subdomains used
        # to skip the guard that caught it.
        got = self.read(["medium.com", "blog.medium.com", "notmedium.com",
                         "evil-medium.com"], subdomains=True)
        self.assertEqual(sorted(c["domain"] for c in got),
                         ["blog.medium.com", "medium.com"])

    def test_flags_and_expiry_are_mapped_through(self):
        got = self.read_rows([("medium.com", 2, 1, 0, 13380000000000000),
                              ("medium.com", 0, 0, 1, 0),
                              ("medium.com", 99, 0, 0, 0)])
        self.assertEqual([c["sameSite"] for c in got], ["Strict", "None", "Lax"])
        self.assertEqual([c["secure"] for c in got], [True, False, False])
        self.assertEqual([c["httpOnly"] for c in got], [False, True, False])
        # Chrome stores microseconds since 1601; Unix epoch is 11644473600 later.
        self.assertEqual([c["expires"] for c in got], [1735526400.0, -1, -1])

    def test_encrypted_values_are_decrypted_not_skipped(self):
        """The whole reason this tool exists: browse's importer drops these."""
        if not shutil.which("openssl"):
            self.skipTest("openssl unavailable")
        hexkey = "00112233445566778899aabbccddeeff"
        hexiv = base64.b16encode(b" " * 16).decode().lower()
        enc = subprocess.run(
            ["openssl", "enc", "-aes-128-cbc", "-K", hexkey, "-iv", hexiv],
            input=b"1:sid-value", capture_output=True)
        got = self.read_rows([("medium.com", 1, 1, 1, 0)],
                             encrypted=b"v10" + enc.stdout, plain="",
                             hexkey=hexkey, hexiv=hexiv)
        self.assertEqual([c["value"] for c in got], ["1:sid-value"])


class TestSnippets(unittest.TestCase):
    payload = {"title": "T", "html": "<p>a</p>", "images": ["a.png"]}

    def all_snippets(self):
        """Every snippet, including image_js — which needs a PNG on disk."""
        d = tempfile.TemporaryDirectory()
        self.addCleanup(d.cleanup)
        with open(os.path.join(d.name, "a.png"), "wb") as fh:
            fh.write(b"\x89PNG\r\n\x1a\n")
        return {
            "title": medium_js.title_js(self.payload),
            "body": medium_js.body_js(self.payload),
            "identify": medium_js.identify_js(self.payload),
            "refill": medium_js.refill_js(self.payload),
            "slot": medium_js.slot_js("a.png"),
            "image": medium_js.image_js(d.name, "a.png"),
            "state": medium_js.state_js(),
        }

    def test_no_duplicate_const_declarations(self):
        # The shared paste block and its callers both used to declare `editor`,
        # which throws SyntaxError at eval time, not at generation time. It was
        # image_js that hit it, so every snippet has to be checked, not most.
        for label, js in self.all_snippets().items():
            declared = const_names(js)
            dupes = {n for n in declared if declared.count(n) > 1}
            self.assertEqual(dupes, set(),
                             "%s redeclares %s:\n%s" % (label, sorted(dupes), js))

    def test_every_snippet_is_a_self_invoking_expression(self):
        # browse eval takes an expression; a snippet that is not called
        # returns the function itself and silently does nothing.
        for label, js in self.all_snippets().items():
            self.assertTrue(js.strip().startswith("(() =>"), label)
            self.assertTrue(js.strip().endswith(")()"), label)

    def test_payload_is_embedded_as_valid_json(self):
        js = medium_js.body_js({"title": "T", "html": '<p>"quoted" & <b>x</b></p>'})
        self.assertIn(json.dumps('<p>"quoted" & <b>x</b></p>'), js)

    def test_title_snippet_carries_the_title(self):
        self.assertIn(json.dumps("T"), medium_js.title_js(self.payload))

    def test_slot_snippet_targets_the_right_marker(self):
        self.assertIn("IMGSLOT-a.png-ENDSLOT", medium_js.slot_js("a.png"))

    def test_a_name_cannot_break_out_of_the_js_string_literal(self):
        # medium_js is also callable straight from argv, which validates nothing.
        # The marker is emitted as a JSON string, so the payload must come back
        # out of json.loads intact rather than becoming code.
        evil = 'a";fetch("https://evil.test");//\\.png'
        js = medium_js.slot_js(evil)
        literal = js.split("const marker = ")[1].split(";\n")[0]
        self.assertEqual(json.loads(literal), "IMGSLOT-%s-ENDSLOT" % evil)

    def test_image_snippet_embeds_decodable_bytes(self):
        with tempfile.TemporaryDirectory() as d:
            raw = b"\x89PNG\r\n\x1a\nnot-a-real-png"
            open(os.path.join(d, "a.png"), "wb").write(raw)
            js = medium_js.image_js(d, "a.png")
        encoded = js.split('const b64 = ')[1].split(', name')[0]
        self.assertEqual(base64.b64decode(json.loads(encoded)), raw)

    @unittest.skipUnless(shutil.which("node"), "node unavailable")
    def test_every_snippet_parses_as_javascript(self):
        # A snippet is assembled by %-formatting strings together, so a stray
        # bracket is not a Python error — it is a SyntaxError inside the
        # browser, after the run has already opened the post.
        for label, js in self.all_snippets().items():
            node_check(self, js, label)


def node_check(case, js, label):
    """Parse `js` with node, without running it."""
    d = tempfile.TemporaryDirectory()
    case.addCleanup(d.cleanup)
    path = os.path.join(d.name, "snippet.js")
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(js)
    out = subprocess.run(["node", "--check", path], capture_output=True, text=True)
    case.assertEqual(out.returncode, 0, "%s is not valid JS:\n%s" % (label, out.stderr))


def node_eval(case, source):
    """Run a scrap of JS and return what it printed, parsed as JSON."""
    d = tempfile.TemporaryDirectory()
    case.addCleanup(d.cleanup)
    path = os.path.join(d.name, "scrap.js")
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(source)
    out = subprocess.run(["node", path], capture_output=True, text=True)
    case.assertEqual(out.returncode, 0, out.stderr)
    return json.loads(out.stdout)


class TestRefillSnippet(unittest.TestCase):
    """`refill` — the only snippet that ever runs against a published post.

    What makes it different from `body` is that the page it lands on is full:
    the old prose, and figures Medium has already uploaded. It replaces all of
    that in one paste, so the two things worth pinning are that the selection
    is positional (no anchor to land in the wrong place) and that the title is
    not in it.
    """

    payload = {"title": "T", "html": "<p>a</p>\n<p>b</p>"}

    def js(self):
        return medium_js.refill_js(self.payload)

    def test_the_selection_is_positional_and_matches_no_text(self):
        # The reason this mode exists at all: patching by anchor was measured
        # at 19-38 scattered edits per article, and an anchor that lands a graf
        # off eats real text. A range from the first body graf to the last has
        # nothing to match.
        js = self.js()
        self.assertIn("range.setStartBefore(first)", js)
        self.assertIn("range.setEndAfter(last)", js)
        for anchor_ish in ("innerText.includes", "textContent", ".find(", ".match("):
            self.assertNotIn(anchor_ish, js, "refill should not match text: " + anchor_ish)

    def test_it_pastes_once_and_never_empties_the_post_first(self):
        # A clear-then-paste pair would leave a window where the post is empty,
        # and Medium autosaves. The paste replaces the selection instead, which
        # is also what takes the old figures out.
        js = self.js()
        self.assertEqual(js.count("dispatchEvent"), 1, js)
        for destructive in (".remove()", "deleteContents", "innerHTML =", "execCommand"):
            self.assertNotIn(destructive, js, destructive)

    def test_every_number_the_caller_gates_on_is_read_after_the_paste(self):
        # Order is the whole point of these reads, and getting it wrong is not
        # visible in the output: `figuresRemoved: hadFigures` was the count
        # taken BEFORE the paste, so it reported "14 removed" whether or not
        # one of them went, and the driver had nothing to assert. The figure
        # count and the title both have to be re-read afterwards, because what
        # the caller has to decide is whether this paste did what it promised.
        js = self.js()
        paste = js.index("dispatchEvent")
        for after in ("figuresLeft: editor.querySelectorAll('figure').length",
                      "const titleNow", "title: titleNow", "titleOk"):
            self.assertIn(after, js)
            self.assertLess(paste, js.index(after), after)
        # The before-count is kept, but only as context in the report: it is
        # what the post used to hold, not evidence about the paste.
        self.assertLess(js.index("const figuresBefore"), paste)
        self.assertIn("figuresBefore,", js)

    def test_the_title_check_is_a_comparison_not_a_non_empty_test(self):
        # `graf--title` is assigned by position — that is how title_js finds
        # the title of a story nobody has typed in yet — so a selection that
        # reached over the title does not leave an empty one. It leaves the
        # first pasted paragraph promoted to title, which is not empty, and the
        # old `"title":""` guard passed it straight through to 18 uploads.
        js = medium_js.refill_js({"title": "Green Is Not Done", "html": "<p>a</p>"})
        self.assertIn("titleOk: !!titleNow && fold(titleNow.innerText) === fold(wantTitle)",
                      js)
        self.assertIn('const wantTitle = "Green Is Not Done"', js)
        # The comparison folds, and folds with the one definition of the fold:
        # Medium curls quotes and pads em dashes in a title it is only
        # re-rendering, and a byte comparison would call that a lost title.
        self.assertIn(medium_js.TITLE_FOLD.strip(), js)

    def test_the_body_html_is_one_json_string_literal(self):
        # The payload is article prose: quotes, angle brackets, backslashes and
        # full-width punctuation all appear in it, and the snippet is written
        # to a file and eval'd, so a raw newline inside the literal is a
        # SyntaxError rather than a mangled paragraph.
        html = ('<p>a "quoted" 、 （full-width） &amp; <b>x</b></p>\n'
                '<pre>path\\to\\thing</pre>\n<p>「引用」</p>')
        js = medium_js.refill_js({"title": "T", "html": html})
        literal = js.split("const HTML = ")[1].split(";\n")[0]
        self.assertEqual(json.loads(literal), html)
        self.assertNotIn("\n", literal)
        self.assertEqual(js.count("const HTML = "), 1)

    def test_every_refusal_is_reported_under_the_err_key(self):
        # The driver stops on `"err"` and nothing else, so a refusal spelled
        # any other way would read as a successful paste. (That the driver
        # really does stop is TestMediumDraftPostDrive's job.)
        keys = re.findall(r"return JSON\.stringify\(\{\s*(\w+)", self.js())
        self.assertEqual(keys[:-1], ["err"] * (len(keys) - 1), keys)
        self.assertGreaterEqual(len(keys), 4, keys)      # three refusals and the result
        self.assertEqual(keys[-1], "replaced")

    def test_both_title_reads_come_from_the_one_selector(self):
        # refill deletes everything this selector does NOT match. A second,
        # drifted copy of the literal would delete the title along with the
        # body, or read the title back off a node it never protected.
        with mock.patch.object(medium_js, "TITLE", "h9.made-up-title"):
            js = medium_js.refill_js(self.payload)
        self.assertEqual(js.count("h9.made-up-title"), 2, js)
        self.assertNotIn("h3.graf--title", js)

    def test_the_body_selection_is_the_same_one_body_js_uses(self):
        # They had drifted: body_js filtered on `graf--title` alone, so the
        # caption rule below — and the "never the node we identified as the
        # title" rule — held in only one of the two snippets that select a
        # range and then replace it. body_js's own docstring promises it is
        # safe to re-run, which is precisely the case with figures on the page.
        self.assertIn(medium_js.BODY_GRAFS.strip(), self.js())
        self.assertIn(medium_js.BODY_GRAFS.strip(), medium_js.body_js(self.payload))

    @unittest.skipUnless(shutil.which("node"), "node unavailable")
    def test_a_caption_is_not_mistaken_for_the_last_body_graf(self):
        # Medium marks a figure's caption as a `.graf` too, nested inside the
        # figure. An article that ends with a figure would then end its body
        # range at the caption — setEndAfter() inside the figure — and the
        # paste would leave half a figure standing. The shipped predicate is
        # lifted out and run over a caption to prove it excludes one.
        for label, js in (("refill", self.js()),
                          ("body", medium_js.body_js(self.payload))):
            self.check_caption_predicate(label, js)

    def check_caption_predicate(self, label, js):
        start = js.index(".filter(") + len(".filter(")
        pred = js[start:js.index(");", start)]
        self.assertTrue(pred.startswith("g =>"), pred)     # the right expression
        self.assertIn("closest", pred, "%s: %s" % (label, pred))
        got = node_eval(self, """
const node = (id, classes, parent) => ({
  id, classes, parent,
  classList: { contains: c => classes.includes(c) },
  get parentElement() { return this.parent; },
  // The DOM's own rule: closest() starts at the node itself, then walks up.
  closest(sel) {
    for (let n = this; n; n = n.parent) if (n.classes.includes(sel.slice(1))) return n;
    return null;
  },
});
const editor = node('editor', ['postArticle-content'], null);
const titleEl = node('title', ['graf', 'graf--title'], editor);
const para = node('para', ['graf'], editor);
const figure = node('figure', ['graf', 'graf--figure'], editor);
const caption = node('caption', ['graf', 'graf--figureCaption'], figure);
const grafs = [titleEl, para, figure, caption];   // an article ending in a figure
console.log(JSON.stringify(grafs.filter(%s).map(g => g.id)));
""" % pred)
        self.assertEqual(got, ["para", "figure"], label)


class TestIdentifySnippet(unittest.TestCase):
    """`identify` — the read-only check that the id opened the right story."""

    payload = {"title": "Green Is Not Done, Part 2 — Review", "html": "<p>a</p>"}

    def js(self):
        return medium_js.identify_js(self.payload)

    def test_it_changes_nothing_on_the_page(self):
        # It runs on a live post before any decision has been made. Anything
        # that writes would be an edit made on the strength of an id that has
        # not been confirmed yet.
        js = self.js()
        for writing in ("ClipboardEvent", "DataTransfer", "dispatchEvent",
                        "addRange", "execCommand", "focus()", ".remove()",
                        "innerHTML =", "setStartBefore"):
            self.assertNotIn(writing, js, writing)

    def test_it_reports_the_verdict_and_both_titles_rather_than_deciding(self):
        # The caller has to be able to tell "wrong post" from "title reworded",
        # and only a human can. So both strings come back for printing, and
        # nothing here throws or exits.
        js = self.js()
        self.assertIn("match: fold(want) === fold(got)", js)
        self.assertIn("want, got,", js)
        self.assertNotIn("throw", js)
        self.assertIn(json.dumps(self.payload["title"], ensure_ascii=False), js)

    def test_the_verdict_is_json_the_driver_can_poll_on(self):
        # The driver polls until the answer contains `"match":`, because "not
        # loaded yet" and "no editor at all" look the same. An error path that
        # also carried a `match` key would end the poll on the wrong answer.
        js = self.js()
        keys = re.findall(r"return JSON\.stringify\(\{\s*(\w+)", js)
        self.assertEqual(keys, ["err", "match"], keys)

    def test_it_reports_where_it_ran_and_how_big_the_post_is(self):
        # Three values the caller cannot get any other way at the moment the
        # title was read: which URL answered (the page can navigate between the
        # driver's own `browse url` and this), and the two counts it polls on
        # to tell a post that has finished loading from one still streaming in.
        for field in ("url: location.href",
                      "grafs: editor.querySelectorAll('.graf').length",
                      "figures: editor.querySelectorAll('figure').length"):
            self.assertIn(field, self.js(), field)


class TestStateSnippet(unittest.TestCase):
    """`state` — the one read every checkpoint after the body paste takes.

    It used to be three inline queries in medium_draft.sh that had drifted
    apart: the upload wait counted `figure img`, the final gate counted
    `figure`, and the placeholder count came from a marker prefix retyped in
    the shell. One snippet is one definition of what is on the page.
    """

    def js(self):
        return medium_js.state_js()

    def test_it_changes_nothing(self):
        # It runs on a live post, repeatedly, including inside a poll.
        for writing in ("ClipboardEvent", "DataTransfer", "dispatchEvent",
                        "addRange", "execCommand", "focus()", ".remove()",
                        "innerHTML ="):
            self.assertNotIn(writing, self.js(), writing)

    def test_the_marker_comes_from_the_converter_that_wrote_it(self):
        # The count decides whether two Backspaces are safe to send. A prefix
        # retyped in the shell would drift from md2medium's and the count would
        # be 0 forever, which reads exactly like "every placeholder is gone".
        with mock.patch.object(medium_js, "SLOT_MARK", "MARKER-%s-END"):
            self.assertIn('new RegExp("MARKER-"', medium_js.state_js())

    def test_both_figure_counts_come_back(self):
        # `figure` and `figure img` are not the same number while an upload is
        # in flight, and the two gates that used to ask separately disagreed
        # about which one they meant.
        js = self.js()
        self.assertIn("figures: editor.querySelectorAll('figure').length", js)
        self.assertIn("imgs: imgs.length", js)

    def test_a_blob_src_is_pending_and_a_cdn_src_is_not(self):
        # Until the upload finishes the <img> still points at a blob: URL.
        # Checking "no bad src" alone passes vacuously before the new figure
        # exists at all, which is why the driver compares the count too.
        pending = re.search(r"pending: imgs\.filter\(x => !(/[^/]+/)\.test", self.js())
        self.assertTrue(pending, self.js())
        rule = re.compile(pending.group(1)[1:-1].replace("\\.", r"\."))
        self.assertTrue(rule.search("https://cdn-images-1.medium.com/x.png"))
        self.assertTrue(rule.search("https://miro.medium.com/x.png"))
        self.assertFalse(rule.search("blob:https://medium.com/2b1c-4d"))

    @unittest.skipUnless(shutil.which("node"), "node unavailable")
    def test_it_counts_a_real_editor_the_way_the_driver_reads_it(self):
        # The driver globs on `"figures":0,` and on `"slots":N}`, so both the
        # values and their order in the object are load-bearing.
        got = node_eval(self, """
const figure = src => ({ tag: 'FIGURE', img: { src } });
const editor = {
  innerText: 'a IMGSLOT-one.png-ENDSLOT b IMGSLOT-two.png-ENDSLOT c',
  figs: [figure('https://cdn-images-1.medium.com/a.png'), figure('blob:x')],
  querySelectorAll(sel) {
    return sel === 'figure img' ? this.figs.map(f => f.img) : this.figs;
  },
};
const document = { querySelector: () => editor };
const location = { href: 'https://medium.com/p/x/edit' };
console.log(JSON.stringify(%s));
""" % self.js().strip())
        self.assertEqual(json.loads(got), {"figures": 2, "imgs": 2,
                                           "pending": 1, "slots": 2})
        self.assertEqual(list(json.loads(got)), ["figures", "imgs", "pending", "slots"])


class TestDumpSnippet(unittest.TestCase):
    """`dump` — what verify_draft.py compares the payload against."""

    def js(self):
        return medium_js.dump_js()

    def test_it_counts_breaks_as_sections_minus_one(self):
        # The regression this class exists for. Medium opens every section with
        # a structural <div class="section-divider"><hr></div>, the first one
        # included, so a post with 10 breaks has 11 sections AND 11 <hr>.
        # Counting <hr> made a correct 10-divider post report 11 and fail the
        # verification by exactly one -- observed on the real editor for
        # /p/3c64a9622777, whose 148 blocks, 19 links and 7 figures all matched.
        self.assertNotIn("'hr'", self.js())
        self.assertNotIn('"hr"', self.js())
        self.assertIn("querySelectorAll('section').length - 1", self.js())

    @unittest.skipUnless(shutil.which("node"), "node unavailable")
    def test_eleven_sections_are_ten_dividers(self):
        got = json.loads(node_eval(self, """
const graf = (tag, innerText) => ({ tagName: tag, innerText });
const grafs = [graf('H3', 'title'), graf('P', 'body'), graf('FIGURE', '')];
const editor = {
  querySelectorAll(sel) {
    if (sel === '.graf') return grafs;
    // 11 sections, and the 11 structural <hr> that come with them.
    if (sel === 'section') return new Array(11);
    if (sel === 'hr') return new Array(11);
    if (sel === 'a') return new Array(19);
    return [];
  },
};
const document = { querySelector: () => editor };
console.log(JSON.stringify(%s));
""" % self.js().strip()))
        self.assertEqual(got["dividers"], 10)
        self.assertEqual(got["links"], 19)
        # FIGURE grafs carry no text and must not enter the block comparison,
        # but they still count as grafs for the placement check.
        self.assertEqual(got["texts"], ["title", "body"])
        self.assertEqual(got["tags"], ["H3", "P", "FIGURE"])

    @unittest.skipUnless(shutil.which("node"), "node unavailable")
    def test_an_empty_editor_reports_no_breaks_rather_than_minus_one(self):
        got = json.loads(node_eval(self, """
const editor = { querySelectorAll: () => [] };
const document = { querySelector: () => editor };
console.log(JSON.stringify(%s));
""" % self.js().strip()))
        self.assertEqual(got["dividers"], 0)

    @unittest.skipUnless(shutil.which("node"), "node unavailable")
    def test_a_missing_editor_is_an_error_not_a_zero_count(self):
        # Reporting {dividers: 0, texts: []} for a page with no editor would
        # let the driver "verify" a post it never opened.
        got = node_eval(self, """
const document = { querySelector: () => null };
console.log(JSON.stringify(%s));
""" % self.js().strip())
        self.assertIn("err", got)


def title_fold_rules():
    r"""The `.replace()` rules in medium_js.TITLE_FOLD, in order, as written.

    Lifted from the shipped source rather than restated here: a copy would go
    on passing after someone edits the fold, which is the one thing these tests
    exist to notice. The replacement is either a quoted literal or the arrow
    that maps superscripts back to `^digits`, so both forms are returned raw
    and interpreted by the caller.
    """
    src = medium_js.TITLE_FOLD
    rules, i = [], 0
    while True:
        start = src.find(".replace(/", i)
        if start < 0:
            return rules
        pattern_at = start + len(".replace(/")
        end = src.index("/g,", pattern_at)
        i, depth = end + len("/g,"), 1
        while depth:                      # to the paren that closes this replace(
            if src[i] == "(":
                depth += 1
            elif src[i] == ")":
                depth -= 1
                if not depth:
                    break
            i += 1
        rules.append((src[pattern_at:end], src[end + len("/g,"):i].strip()))


def unescape_js_unicode(text):
    """Turn the `\\uXXXX` escapes into characters, leaving `\\d` and `\\s` alone."""
    return re.sub(r"\\u([0-9A-Fa-f]{4})", lambda m: chr(int(m.group(1), 16)), text)


class TestTitleFold(unittest.TestCase):
    """The fold that decides whether the post on screen is this article.

    No browser here, so the JS cannot run — but the regexes can be lifted out
    of the shipped constant and applied with Python's `re`, which agrees with
    JS on every construct used. Same trick as TestPatchAnchorNormalisation, and
    for the same reason: the test has to fail when medium_js changes, not when
    a copy of it in this file changes.
    """

    def fold(self, text):
        rules = title_fold_rules()
        self.assertTrue(rules, "no replace() rules found in TITLE_FOLD")
        for pattern, repl in rules:
            pattern = unescape_js_unicode(pattern)
            if repl[:1] in ("'", '"') and repl[-1:] == repl[:1]:
                # JS spells its backreferences $1; Python spells them \1.
                text = re.sub(pattern,
                              unescape_js_unicode(repl[1:-1]).replace("$", "\\"), text)
            else:
                prefix = re.search(r"=>\s*'([^']*)'\s*\+", repl).group(1)
                digits = unescape_js_unicode(
                    re.search(r"'((?:\\u[0-9A-Fa-f]{4})+)'\.indexOf", repl).group(1))
                text = re.sub(pattern, lambda m: prefix + "".join(
                    str(digits.index(c)) for c in m.group(0)), text)
        return text.strip()      # the .trim() at the end of the chain

    def test_it_is_written_in_escapes_not_the_characters_themselves(self):
        # Half of what it folds is invisible in an editor, so a literal hair
        # space in this constant could be deleted by an unrelated edit and
        # nothing would look different in the diff.
        self.assertTrue(medium_js.TITLE_FOLD.isascii(), medium_js.TITLE_FOLD)

    def test_a_curled_apostrophe_still_reads_as_the_same_title(self):
        # THE reason this is not medium_patch.NORMALISE, which leaves quotes
        # alone: Medium curls the apostrophe, so the English opener comes back
        # as "Don’t" and would fail an identity check that did not fold it.
        authored = "Don't Build Your Own Devin"
        self.assertEqual(self.fold(authored.replace("'", "’")),
                         self.fold(authored))

    def test_mediums_em_dash_padding_reads_as_the_same_title(self):
        # Every series title has one: "Part 2 — Review ...". Medium renders it
        # with hair spaces and no ordinary spaces at all.
        rendered = "Green Is Not Done, Part 2\u200a\u2014\u200aReview"
        self.assertEqual(self.fold(rendered),
                         self.fold("Green Is Not Done, Part 2 — Review"))

    def test_an_en_dash_between_digits_reads_as_the_same_title(self):
        self.assertEqual(self.fold("Retro 2026–07–10"), self.fold("Retro 2026-07-10"))

    def test_superscript_digits_read_as_the_caret_the_author_typed(self):
        # A title carrying pass^5 comes back superscripted; the same fold runs
        # in verify_draft.py on every graf, so not folding it here would only
        # move the false alarm later.
        self.assertEqual(self.fold("SWE-Gate, pass⁵ and pass²⁰"),
                         self.fold("SWE-Gate, pass^5 and pass^20"))

    def test_a_nbsp_is_a_space_and_the_invisibles_are_nothing(self):
        self.assertEqual(self.fold("\ufeffAGENTS.md\u00a0：寫對"),
                         self.fold("AGENTS.md ：寫對"))

    def test_the_neighbouring_row_of_the_id_table_does_not_fold_equal(self):
        # The realistic mistake this whole check exists for. These titles share
        # everything but one character, so a fold that reached any further —
        # a prefix match, a similarity score, stripping punctuation — would
        # wave through the id of the sibling article.
        for a, b in (("綠燈不是驗收（二）Review 篇",
                      "綠燈不是驗收（三）Review 篇"),
                     ("Green Is Not Done, Part 2 — Review",
                      "Green Is Not Done, Part 3 — Review")):
            self.assertNotEqual(self.fold(a), self.fold(b))

    def test_word_spacing_is_still_significant(self):
        self.assertNotEqual(self.fold("Green Is Not Done"), self.fold("GreenIsNotDone"))

    def test_it_folds_exactly_what_verify_draft_folds(self):
        # This is the third hand copy of one set of rules, and the previous two
        # grew a rule at a time as Medium added rewrites (curly doubles, the en
        # dash in dates, the superscript caret — each one arrived on its own).
        # Nothing was comparing the copies, and they had already diverged: the
        # old `/(\d)–(\d)/g` consumed the digit on each side, so the second en
        # dash in `1–2–3` found no digit in front of it and survived, while
        # verify_draft's lookarounds folded both. A title that folds one way
        # here and another there stops --post on two titles that are identical
        # on screen, and the only way past that is --retitle, which is the flag
        # that turns the check off.
        cases = [
            "Green Is Not Done, Part 2  —  Review",
            "Don’t Build Your Own Devin",
            "“Green” Is Not ‘Done’",
            "Retro 2026–07–10",
            "1–2–3",                    # the one that already differed
            "SWE-Gate, pass⁵ and pass²⁰",
            "﻿AGENTS.md ：寫對",
            "a  b\tc",
            "— leading dash",
        ]
        for paste in sorted(glob.glob(os.path.join(REPO, "*/publish/medium-paste.md"))) \
                + sorted(glob.glob(os.path.join(REPO, LANG_PASTE_GLOB))):
            with open(paste, encoding="utf-8") as fh:
                cases.append(md2medium.convert(fh.read())["title"])
        self.assertGreater(len(cases), 20, "the corpus went missing")
        for text in cases:
            self.assertEqual(self.fold(text), verify_draft.normalise(text, False),
                             "TITLE_FOLD and verify_draft.normalise disagree on %r"
                             % text)

    def test_every_shipped_title_still_folds_to_something_unique(self):
        # The corpus this runs against: 16 titles across two languages, four of
        # them differing only in a part number. If the fold ever collapses two
        # of them, --post could overwrite the wrong article and the identity
        # check would report a match.
        titles = []
        for paste in sorted(glob.glob(os.path.join(REPO, "*/publish/medium-paste.md"))) \
                + sorted(glob.glob(os.path.join(REPO, LANG_PASTE_GLOB))):
            with open(paste, encoding="utf-8") as fh:
                titles.append(md2medium.convert(fh.read())["title"])
        self.assertGreater(len(titles), 10, "the corpus went missing")
        folded = [self.fold(t) for t in titles]
        self.assertEqual(len(set(folded)), len(folded),
                         sorted(t for t in folded if folded.count(t) > 1))
        # And each still folds to itself, so a match is a match for the right
        # reason rather than because everything folds to the same mush.
        for title, f in zip(titles, folded):
            self.assertEqual(self.fold(title), f)


@unittest.skipUnless(shutil.which("openssl"), "openssl unavailable")
class TestDecrypt(unittest.TestCase):
    """Chrome's v10 scheme: AES-128-CBC, IV of 16 spaces, PKCS7."""

    HEXKEY = "00112233445566778899aabbccddeeff"
    HEXIV = base64.b16encode(b" " * 16).decode().lower()

    def encrypt(self, plaintext):
        out = subprocess.run(
            ["openssl", "enc", "-aes-128-cbc", "-K", self.HEXKEY, "-iv", self.HEXIV],
            input=plaintext, capture_output=True)
        if out.returncode != 0:
            self.skipTest("openssl unavailable")
        return b"v10" + out.stdout

    def decrypt(self, blob):
        return chrome_cookies.decrypt(blob, self.HEXKEY, self.HEXIV)

    def test_round_trip(self):
        self.assertEqual(self.decrypt(self.encrypt(b"1:sid-value")), "1:sid-value")

    def test_padding_is_stripped_exactly(self):
        # A value that lands on a block boundary gets a full block of padding.
        self.assertEqual(self.decrypt(self.encrypt(b"0123456789abcdef")),
                         "0123456789abcdef")

    def test_domain_hash_prefix_is_dropped(self):
        # Newer Chrome prepends 32 bytes of hash; it is not valid UTF-8, which
        # is exactly how the fallback detects it.
        self.assertEqual(self.decrypt(self.encrypt(b"\xff" * 32 + b"hello")), "hello")

    def test_non_v10_blob_is_refused(self):
        self.assertIsNone(self.decrypt(b"v20somethingelse"))

    def test_empty_blob_is_refused(self):
        self.assertIsNone(self.decrypt(b""))

    def test_full_pkcs7_pad_is_validated(self):
        # Noise from a wrong key routinely ends in a plausible length byte.
        blob = b"v10" + subprocess.run(
            ["openssl", "enc", "-aes-128-cbc", "-K", self.HEXKEY, "-iv", self.HEXIV,
             "-nopad"], input=b"A" * 15 + bytes([3]), capture_output=True).stdout
        # 3 does not repeat 3 times, so it is not padding and must be kept.
        self.assertEqual(self.decrypt(blob), "A" * 15 + chr(3))

    def test_domain_hash_prefix_is_stripped_when_the_host_is_known(self):
        import hashlib
        host = ".medium.com"
        blob = self.encrypt(hashlib.sha256(host.encode()).digest() + b"1:real")
        self.assertEqual(chrome_cookies.decrypt(blob, self.HEXKEY, self.HEXIV, host),
                         "1:real")

    def test_wrong_key_is_refused_not_silently_mangled(self):
        # A stale keychain key used to decrypt to noise and export a cookie
        # with an empty value, which authenticates as logged out.
        got = chrome_cookies.decrypt(self.encrypt(b"1:sid-value"),
                                     "ff" * 16, self.HEXIV)
        self.assertIsNone(got, "a bad key must fail loudly, got %r" % got)


class TestDeriveKey(unittest.TestCase):
    """The PBKDF2 stretch, pinned to what the tool produced before it was a function.

    research/scripts/notion_cookies.py used to carry its own copy of this; a
    drift in either would decrypt every cookie to noise and export nothing.
    """

    def test_fixed_password_gives_the_values_the_tool_always_produced(self):
        # pbkdf2_hmac("sha1", b"secret", b"saltysalt", 1003, 16), computed once
        # from the pre-refactor code and hardcoded so the test cannot just
        # re-derive the same mistake.
        self.assertEqual(chrome_cookies.derive_key(b"secret"),
                         ("1a7404704ee35b4506624ed49171a534",
                          "20202020202020202020202020202020"))

    def test_the_hex_pair_is_what_openssl_accepts(self):
        if not shutil.which("openssl"):
            self.skipTest("openssl unavailable")
        hexkey, hexiv = chrome_cookies.derive_key(b"correct horse battery staple")
        enc = subprocess.run(
            ["openssl", "enc", "-aes-128-cbc", "-K", hexkey, "-iv", hexiv],
            input=b"1:sid-value", capture_output=True)
        self.assertEqual(enc.returncode, 0, enc.stderr)
        self.assertEqual(chrome_cookies.decrypt(b"v10" + enc.stdout, hexkey, hexiv),
                         "1:sid-value")


class TestSafeStorageKey(unittest.TestCase):
    """The keychain lookup, with `security` faked so no prompt can appear."""

    def lookup(self, stdout="pw\n", returncode=0, *args):
        fake = subprocess.CompletedProcess(args=[], returncode=returncode,
                                           stdout=stdout, stderr="denied")
        with mock.patch.object(chrome_cookies.subprocess, "run", return_value=fake) as run:
            key = chrome_cookies.safe_storage_key(*args)
        return key, run.call_args[0][0]

    def test_defaults_to_chromes_item(self):
        key, argv = self.lookup()
        self.assertEqual(key, b"pw")
        self.assertEqual(argv, ["security", "find-generic-password", "-w",
                                "-s", "Chrome Safe Storage", "-a", "Chrome"])

    def test_another_app_names_its_own_item(self):
        _, argv = self.lookup("pw\n", 0, "Notion Safe Storage", "Notion Key")
        self.assertEqual(argv[3:], ["-s", "Notion Safe Storage", "-a", "Notion Key"])

    def test_a_refusal_or_empty_secret_exits_naming_the_item(self):
        for stdout, rc in (("", 1), ("\n", 0)):
            with self.assertRaises(SystemExit) as cm:
                self.lookup(stdout, rc, "Notion Safe Storage", "Notion Key")
            self.assertIn("Notion Safe Storage", str(cm.exception))
            self.assertIn("denied", str(cm.exception))


class TestProfiles(unittest.TestCase):
    def test_lists_only_dirs_that_have_a_cookie_db(self):
        with tempfile.TemporaryDirectory() as root:
            os.makedirs(os.path.join(root, "Default"))
            os.makedirs(os.path.join(root, "Profile 1"))
            os.makedirs(os.path.join(root, "NoCookies"))
            open(os.path.join(root, "Default", "Cookies"), "wb").close()
            open(os.path.join(root, "Profile 1", "Cookies"), "wb").close()
            orig = chrome_cookies.CHROME_DIR
            chrome_cookies.CHROME_DIR = root
            self.addCleanup(setattr, chrome_cookies, "CHROME_DIR", orig)
            self.assertEqual(chrome_cookies.profiles(), ["Default", "Profile 1"])

    def test_missing_chrome_dir_exits(self):
        orig = chrome_cookies.CHROME_DIR
        chrome_cookies.CHROME_DIR = "/nonexistent-chrome-dir"
        self.addCleanup(setattr, chrome_cookies, "CHROME_DIR", orig)
        with self.assertRaises(SystemExit):
            chrome_cookies.profiles()


TOOLS = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(TOOLS)
# publish/<lang>/ packs. One definition: three sweeps used to carry their own
# copy, so a layout change would have left one of them matching nothing.
LANG_PASTE_GLOB = "*/publish/*/medium-paste.md"
# Mirrors the readonly values in tools/medium_draft.sh.
EX_USAGE = 64
EX_UNAVAILABLE = 69
EX_TEMPFAIL = 75



def const_names(js):
    r"""Every name a `const` binds, including 2nd declarators and destructuring.

    `re.findall(r"const\s+(\w+)")` sees only the first declarator, so it is
    blind to `const a = .., b = ..` and to `const [node, at] = ..` — which is
    most of what these snippets actually declare. A guard that cannot see the
    collision it exists to catch is worse than no guard.
    """
    names = []
    for line in js.splitlines():
        m = re.search(r"\bconst\s+(.*)$", line)
        if not m:
            continue
        rest = m.group(1)
        for group in re.findall(r"\[([^\]]*)\]\s*=", rest):
            names += re.findall(r"[A-Za-z_$][\w$]*", group)
        names += re.findall(r"(?:^|,)\s*([A-Za-z_$][\w$]*)\s*=(?!=)", rest)
    return names


def run_tool(*args):
    return subprocess.run([sys.executable] + list(args), capture_output=True, text=True)


class TestMd2MediumCLI(unittest.TestCase):
    def article(self, slots=(), images=()):
        root = tempfile.TemporaryDirectory()
        self.addCleanup(root.cleanup)
        pub = os.path.join(root.name, "publish")
        os.makedirs(os.path.join(pub, "images"))
        body = "# T\n\n" + "".join("📌【在此插入圖 %s】\n\n" % s for s in slots)
        with open(os.path.join(pub, "medium-paste.md"), "w", encoding="utf-8") as fh:
            fh.write(body)
        for name in images:
            open(os.path.join(pub, "images", name), "wb").close()
        return root.name

    def test_missing_image_file_fails_before_the_browser_opens(self):
        # Finding this halfway through a 14-image run means a half-built draft.
        art = self.article(slots=["a.png"], images=[])
        out = run_tool(os.path.join(TOOLS, "md2medium.py"), art,
                       "--out", os.path.join(art, "p.json"))
        self.assertNotEqual(out.returncode, 0)
        self.assertIn("missing image", out.stderr)

    def test_happy_path_writes_the_payload(self):
        art = self.article(slots=["a.png"], images=["a.png"])
        dest = os.path.join(art, "p.json")
        out = run_tool(os.path.join(TOOLS, "md2medium.py"), art, "--out", dest)
        self.assertEqual(out.returncode, 0, out.stderr)
        with open(dest, encoding="utf-8") as fh:
            payload = json.load(fh)
        self.assertEqual(payload["title"], "T")
        self.assertEqual(payload["images"], ["a.png"])

    def test_accepts_a_direct_file_path_too(self):
        art = self.article(images=[])
        dest = os.path.join(art, "p.json")
        out = run_tool(os.path.join(TOOLS, "md2medium.py"),
                       os.path.join(art, "publish", "medium-paste.md"), "--out", dest)
        self.assertEqual(out.returncode, 0, out.stderr)

    def test_nonexistent_path_fails(self):
        out = run_tool(os.path.join(TOOLS, "md2medium.py"), "/nope/nothing")
        self.assertNotEqual(out.returncode, 0)

    def lang_article(self, lang, default_images=(), lang_images=()):
        """An article with a default pack and a <lang> pack, each with its own
        images/ dir. Both packs declare the SAME slot, which is the point: the
        real packs use identical figure filenames in both languages, so a
        driver that fed the translated paste file while resolving images from
        the default pack would ship the wrong figures and every later check —
        block diff, link count, figure position — would still say "match".
        """
        root = tempfile.TemporaryDirectory()
        self.addCleanup(root.cleanup)
        body = "# T\n\n\U0001F4CC【在此插入圖 a.png】\n\n"
        for pack, images in ((None, default_images), (lang, lang_images)):
            pub = os.path.join(root.name, "publish", pack) if pack \
                else os.path.join(root.name, "publish")
            os.makedirs(os.path.join(pub, "images"), exist_ok=True)
            with open(os.path.join(pub, "medium-paste.md"), "w", encoding="utf-8") as fh:
                fh.write(body)
            for name in images:
                open(os.path.join(pub, "images", name), "wb").close()
        return root.name

    def test_a_lang_pack_resolves_images_from_its_own_dir(self):
        # Image present ONLY in publish/en/images: converting the en paste
        # must succeed.
        art = self.lang_article("en", default_images=[], lang_images=["a.png"])
        out = run_tool(os.path.join(TOOLS, "md2medium.py"),
                       os.path.join(art, "publish", "en", "medium-paste.md"),
                       "--out", os.path.join(art, "p.json"))
        self.assertEqual(out.returncode, 0, out.stderr)

    def test_a_lang_pack_does_not_fall_back_to_the_default_images(self):
        # Mirror, and the one that actually catches the bug: the image exists
        # in publish/images but NOT in publish/en/images. Resolving from the
        # default pack would pass here and ship Chinese figures on an English
        # article; it has to fail and name the en dir.
        art = self.lang_article("en", default_images=["a.png"], lang_images=[])
        out = run_tool(os.path.join(TOOLS, "md2medium.py"),
                       os.path.join(art, "publish", "en", "medium-paste.md"),
                       "--out", os.path.join(art, "p.json"))
        self.assertNotEqual(out.returncode, 0)
        self.assertIn("missing image", out.stderr)
        self.assertIn(os.path.join("publish", "en", "images"), out.stderr)


class TestVerifyDraftCLI(unittest.TestCase):
    """The exit code is the gate: a mismatch must never exit 0."""

    def files(self, grafs):
        root = tempfile.TemporaryDirectory()
        self.addCleanup(root.cleanup)
        p = os.path.join(root.name, "payload.json")
        g = os.path.join(root.name, "grafs.json")
        with open(p, "w", encoding="utf-8") as fh:
            json.dump({"title": "T", "html": "<p>alpha</p>\n<p>beta</p>"},
                      fh, ensure_ascii=False)
        # browse wraps page output in UNTRUSTED markers; the parser must cope.
        with open(g, "w", encoding="utf-8") as fh:
            fh.write("--- BEGIN UNTRUSTED EXTERNAL CONTENT ---\n"
                     + json.dumps(grafs, ensure_ascii=False)
                     + "\n--- END UNTRUSTED EXTERNAL CONTENT ---\n")
        return p, g

    def test_exits_zero_when_everything_matches(self):
        p, g = self.files(["T", "alpha", "beta"])
        out = run_tool(os.path.join(TOOLS, "verify_draft.py"), p, g)
        self.assertEqual(out.returncode, 0, out.stdout + out.stderr)
        self.assertIn("all blocks match", out.stdout)

    def test_exits_nonzero_when_a_block_is_missing(self):
        p, g = self.files(["T", "alpha"])
        out = run_tool(os.path.join(TOOLS, "verify_draft.py"), p, g)
        self.assertEqual(out.returncode, 1)
        self.assertIn("mismatch", out.stdout)

    def test_exits_nonzero_when_a_block_differs(self):
        p, g = self.files(["T", "alpha", "WRONG"])
        out = run_tool(os.path.join(TOOLS, "verify_draft.py"), p, g)
        self.assertEqual(out.returncode, 1)

    def test_wrong_argument_count_exits(self):
        out = run_tool(os.path.join(TOOLS, "verify_draft.py"), "only-one")
        self.assertNotEqual(out.returncode, 0)


class TestCookieFileIsPrivate(unittest.TestCase):
    def test_created_owner_only_and_never_wider(self):
        d = tempfile.TemporaryDirectory()
        self.addCleanup(d.cleanup)
        out = os.path.join(d.name, "cookies.json")
        chrome_cookies.write_private(out, [{"name": "sid", "value": "SECRET"}])
        self.assertEqual(os.stat(out).st_mode & 0o777, 0o600)

    def test_refuses_to_write_through_a_preexisting_symlink(self):
        d = tempfile.TemporaryDirectory()
        self.addCleanup(d.cleanup)
        victim = os.path.join(d.name, "victim")
        open(victim, "w").close()
        out = os.path.join(d.name, "cookies.json")
        os.symlink(victim, out)
        with self.assertRaises(SystemExit):
            chrome_cookies.write_private(out, [{"name": "sid", "value": "SECRET"}])
        with open(victim) as fh:
            self.assertNotIn("SECRET", fh.read())


class TestMediumJsCLI(unittest.TestCase):
    def test_unknown_snippet_name_exits(self):
        out = run_tool(os.path.join(TOOLS, "medium_js.py"), "bogus", "x")
        self.assertNotEqual(out.returncode, 0)
        self.assertIn("unknown snippet", out.stderr)

    def test_selectors_needs_no_argument(self):
        out = run_tool(os.path.join(TOOLS, "medium_js.py"), "selectors")
        self.assertEqual(out.returncode, 0, out.stderr)
        self.assertIn("EDITOR_SEL=", out.stdout)
        self.assertIn("SLOT_PREFIX=", out.stdout)

    def test_slot_snippet_prints_to_stdout(self):
        out = run_tool(os.path.join(TOOLS, "medium_js.py"), "slot", "a.png")
        self.assertEqual(out.returncode, 0, out.stderr)
        self.assertIn("IMGSLOT-a.png-ENDSLOT", out.stdout)

    def payload_file(self):
        d = tempfile.TemporaryDirectory()
        self.addCleanup(d.cleanup)
        path = os.path.join(d.name, "payload.json")
        with open(path, "w", encoding="utf-8") as fh:
            json.dump({"title": "T", "html": "<p>a</p>", "images": []}, fh)
        return path

    def test_the_post_mode_snippets_are_reachable_from_the_command_line(self):
        # medium_draft.sh shells out for these by name; a subcommand the
        # dispatch table does not know exits with the usage text, and the
        # driver would report it as "could not paste the body".
        for kind, marker in (("identify", "match: fold(want) === fold(got)"),
                             ("refill", "figuresLeft: editor.querySelectorAll")):
            out = run_tool(os.path.join(TOOLS, "medium_js.py"), kind, self.payload_file())
            self.assertEqual(out.returncode, 0, out.stderr)
            self.assertIn(marker, out.stdout)

    def test_the_post_mode_snippets_need_a_payload(self):
        for kind in ("identify", "refill"):
            out = run_tool(os.path.join(TOOLS, "medium_js.py"), kind)
            self.assertNotEqual(out.returncode, 0)
            self.assertIn("%s needs an argument" % kind, out.stderr)

    def test_state_needs_no_payload_and_prints_a_snippet(self):
        # It counts what is on the page; there is nothing from the article in
        # it. Asking it for a payload it does not use would make the driver
        # write a file per call for no reason.
        out = run_tool(os.path.join(TOOLS, "medium_js.py"), "state")
        self.assertEqual(out.returncode, 0, out.stderr)
        self.assertIn("slots:", out.stdout)
        self.assertIn(medium_js.EDITOR, out.stdout)




class TestPatchFragment(unittest.TestCase):
    """fragment_html has to agree with the converter that built the live post.

    A patch is pasted next to grafs produced by md2medium, so any divergence in
    block mapping shows up as one subheading rendering a different size from its
    neighbours — visible to readers, invisible in the diff.
    """

    def test_subheading_maps_to_h4_like_the_body_converter(self):
        # ### is graf--h4 in the body; a patch emitting <h3> would render big.
        self.assertIn("<h4>系列文章</h4>",
                      medium_patch.fragment_html("### 系列文章\n"))

    def test_section_heading_maps_to_h2_like_the_body_converter(self):
        self.assertIn("<h2>", medium_patch.fragment_html("## 十二、結語\n"))

    def test_throwaway_title_does_not_leak_into_the_output(self):
        # fragment_html prepends "# _" to satisfy convert(); if that ever landed
        # in html the patch would paste a stray heading into the article.
        out = medium_patch.fragment_html("一般段落\n")
        self.assertNotIn("_", out)
        self.assertEqual(out, "<p>一般段落</p>")

    def test_links_and_ordered_lists_survive(self):
        out = medium_patch.fragment_html(
            "1. [組織篇](https://example.com/a)—編制\n2. 技術篇（尚未發布）\n")
        self.assertIn('<a href="https://example.com/a">組織篇</a>', out)
        self.assertEqual(out.count("<li>"), 2)

    def test_blank_line_in_a_code_block_stays_one_block(self):
        # Same rule as the body: a split <pre> becomes two boxes in the editor.
        out = medium_patch.fragment_html("```text\na\n\nb\n```\n")
        self.assertEqual(out.count("<pre>"), 1)


class TestPatchSnippets(unittest.TestCase):
    def snippets(self):
        return {
            "find": medium_patch.find_js("anchor"),
            "replace": medium_patch.replace_js("a", "b", "<p>x</p>"),
            "dry": medium_patch.replace_js("a", "b", "<p>x</p>", dry=True),
        }

    def test_every_snippet_is_a_self_invoking_expression(self):
        for label, js in self.snippets().items():
            self.assertTrue(js.strip().startswith("(() =>"), label)
            self.assertTrue(js.strip().endswith(")()"), label)

    def test_no_duplicate_const_declarations(self):
        # The shared NORMALISE/PICK blocks and the callers all declare names;
        # a collision is a SyntaxError at eval time, not at generation time.
        for label, js in self.snippets().items():
            declared = const_names(js)
            dupes = {n for n in declared if declared.count(n) > 1}
            self.assertEqual(dupes, set(),
                             "%s redeclares %s" % (label, sorted(dupes)))

    def test_dry_run_never_dispatches_a_paste(self):
        # The whole point of --dry is that it is safe to fire at a live post.
        self.assertNotIn("dispatchEvent",
                         medium_patch.replace_js("a", "b", "<p>x</p>", dry=True)
                         .split("if (true)")[0] + "")
        dry = medium_patch.replace_js("a", "b", "<p>x</p>", dry=True)
        before_guard, after_guard = dry.split("if (true) return", 1)
        self.assertNotIn("dispatchEvent", before_guard)

    def test_live_run_does_dispatch_a_paste(self):
        self.assertIn("dispatchEvent", medium_patch.replace_js("a", "b", "<p>x</p>"))
        self.assertIn("if (false) return",
                      medium_patch.replace_js("a", "b", "<p>x</p>"))

    def test_refuses_an_ambiguous_or_missing_anchor(self):
        js = medium_patch.replace_js("a", "b", "<p>x</p>")
        self.assertIn("a.length !== 1", js)
        self.assertIn("b.length !== 1", js)

    def test_refuses_a_backwards_range(self):
        self.assertIn("b[0] < a[0]", medium_patch.replace_js("a", "b", "<p>x</p>"))

    def test_anchor_cannot_break_out_of_the_js_string_literal(self):
        # Anchors come from argv and are not validated anywhere.
        evil = 'x");fetch("https://evil.test");//'
        js = medium_patch.replace_js(evil, "b", "<p>x</p>")
        literal = js.split("const a = pick(")[1].split("), b = pick(")[0]
        self.assertEqual(json.loads(literal), evil)

    def test_replacement_html_cannot_break_out_of_the_js_string_literal(self):
        evil = '</p>";fetch("https://evil.test");//'
        js = medium_patch.replace_js("a", "b", evil)
        literal = js.split("const HTML = ")[1].split(";\n")[0]
        self.assertEqual(json.loads(literal), evil)

    def test_a_percent_sign_in_the_replacement_survives_formatting(self):
        # The snippet is built with %-formatting; a stray % in a URL-encoded
        # Medium link would blow up or corrupt the payload if interpolated.
        html = '<a href="https://x.test/%E5%88%A5">別</a>'
        js = medium_patch.replace_js("a", "b", html)
        literal = js.split("const HTML = ")[1].split(";\n")[0]
        self.assertEqual(json.loads(literal), html)


class TestMediumPatchCLI(unittest.TestCase):
    def test_unknown_snippet_name_exits(self):
        out = run_tool(os.path.join(TOOLS, "medium_patch.py"), "bogus", "x")
        self.assertNotEqual(out.returncode, 0)
        self.assertIn("unknown snippet", out.stderr)

    def test_replace_requires_all_three_arguments(self):
        out = run_tool(os.path.join(TOOLS, "medium_patch.py"), "replace", "a")
        self.assertNotEqual(out.returncode, 0)

    def test_html_subcommand_converts_a_file(self):
        d = tempfile.TemporaryDirectory()
        self.addCleanup(d.cleanup)
        frag = os.path.join(d.name, "f.md")
        with open(frag, "w", encoding="utf-8") as fh:
            fh.write("### 系列文章\n")
        out = run_tool(os.path.join(TOOLS, "medium_patch.py"), "html", frag)
        self.assertEqual(out.returncode, 0)
        self.assertEqual(out.stdout.strip(), "<h4>系列文章</h4>")


class TestPatchImageSnippets(unittest.TestCase):
    def png(self):
        d = tempfile.TemporaryDirectory()
        self.addCleanup(d.cleanup)
        path = os.path.join(d.name, "table-04.png")
        with open(path, "wb") as fh:
            fh.write(b"\x89PNG\r\n\x1a\nnot-a-real-png")
        return path

    def test_image_snippet_embeds_decodable_bytes(self):
        path = self.png()
        with open(path, "rb") as fh:
            raw = fh.read()
        js = medium_patch.image_js("anchor", path)
        encoded = js.split("const bin = atob(")[1].split(");")[0]
        self.assertEqual(base64.b64decode(json.loads(encoded)), raw)

    def test_image_snippet_uses_the_basename_not_the_temp_path(self):
        # The File name becomes the upload's filename; a temp path would leak
        # the whole directory into Medium.
        js = medium_patch.image_js("anchor", self.png())
        self.assertIn(json.dumps("table-04.png"), js)
        self.assertNotIn(tempfile.gettempdir(), js.split("const file")[1][:200])

    def test_image_and_drop_refuse_an_ambiguous_anchor(self):
        self.assertIn("hit.length !== 1", medium_patch.image_js("a", self.png()))
        self.assertIn("hits.length !== 1", medium_patch.drop_js("a.png"))

    def test_drop_only_selects_and_never_presses(self):
        # medium_draft.sh learned this the hard way: the snippet must confirm
        # what is selected and leave the Backspace to the caller, so a miss
        # cannot eat article content.
        js = medium_patch.drop_js("a.png")
        self.assertNotIn("Backspace", js)
        self.assertIn("selected", js)

    def test_drop_reports_which_figure_it_selected(self):
        js = medium_patch.drop_js("a.png")
        self.assertIn("split('/').pop()", js)

    def test_image_and_drop_are_self_invoking_expressions(self):
        for label, js in {"image": medium_patch.image_js("a", self.png()),
                          "drop": medium_patch.drop_js("a.png")}.items():
            self.assertTrue(js.strip().startswith("(() =>"), label)
            self.assertTrue(js.strip().endswith(")()"), label)

    def test_image_and_drop_have_no_duplicate_const_declarations(self):
        for label, js in {"image": medium_patch.image_js("a", self.png()),
                          "drop": medium_patch.drop_js("a.png")}.items():
            declared = const_names(js)
            dupes = {n for n in declared if declared.count(n) > 1}
            self.assertEqual(dupes, set(), "%s redeclares %s" % (label, sorted(dupes)))


class TestPatchAnchorNormalisation(unittest.TestCase):
    """The anchor normaliser, exercised through the patterns actually shipped.

    There is no browser here, so the JS cannot be run — but the regexes can be
    lifted out of the emitted snippet and applied with Python's `re`, which has
    the same semantics for these three character classes. That keeps the test
    honest: it fails if someone edits the pattern in medium_patch, not if
    someone edits a copy of it in the test.
    """

    def norm(self, text):
        rules = re.findall(r"\.replace\(/(.+?)/g, '(.*?)'\)", medium_patch.NORMALISE)
        # Deliberately not a count assertion: the rules may be merged or split
        # without changing behaviour, and pinning the number would make every
        # test here fail on the guard instead of on what it actually checks.
        self.assertTrue(rules, "no replace() rules found in NORMALISE")
        for pattern, repl in rules:
            text = re.sub(pattern.encode().decode("unicode_escape"),
                          repl.encode().decode("unicode_escape"), text)
        return text.strip()

    def test_hair_spaced_em_dash_matches_an_anchor_written_with_spaces(self):
        # The real miss: Medium renders "A — B" as "A<hair>—<hair>B" with no
        # ordinary spaces, so an anchor copied from article.md found nothing.
        rendered = "Stack Overflow\u200a\u2014\u200aAgents on a leash"
        authored = "Stack Overflow \u2014 Agents on a leash"
        self.assertEqual(self.norm(rendered), self.norm(authored))

    def test_double_em_dash_in_a_title_also_lines_up(self):
        rendered = "Harness \u200a\u2014\u200a \u200a\u2014\u200a \u628a\u7cfb\u7d71"
        authored = "Harness\u2014\u2014\u628a\u7cfb\u7d71"
        self.assertEqual(self.norm(rendered), self.norm(authored))

    def test_nbsp_and_bom_do_not_defeat_an_anchor(self):
        self.assertEqual(self.norm("\ufeffAGENTS.md\u00a0\uff1a\u5beb\u5c0d"),
                         self.norm("AGENTS.md\uff1a\u5beb\u5c0d"))

    def test_ordinary_word_spacing_is_still_significant(self):
        # Collapsing runs is fine; deleting spaces entirely would make anchors
        # match text that does not actually read the same.
        self.assertNotEqual(self.norm("make test FILTER"), self.norm("maketestFILTER"))

    def test_runs_of_whitespace_collapse_to_one(self):
        self.assertEqual(self.norm("a\n\n  b"), self.norm("a b"))


class TestDoubleDashCheck(unittest.TestCase):
    """`——` must never reach Medium: it renders as `— —`, a gap mid-stroke.

    This has to be caught at conversion, because nothing downstream can see it.
    verify_draft.py deliberately folds em-dash spacing away so Medium's hair
    spaces do not read as a paste failure — which means a double dash sails
    through every later check and only shows up to readers.
    """

    def test_double_dash_is_rejected(self):
        with self.assertRaises(SystemExit) as cm:
            md2medium.convert("# T\n\n\u4e00\u2014\u2014\u4e8c\n")
        self.assertIn("——", str(cm.exception))

    def test_the_line_number_accounts_for_the_stripped_checklist(self):
        # Every real publish/medium-paste.md opens with an HTML comment block
        # that convert() removes before numbering. Reporting the post-strip
        # index sends the author to the wrong line of the file they must edit.
        src = "<!--\nchecklist\nmore\n-->\n\n# T\n\nfine\n\n\u4e00\u2014\u2014\u4e8c\n"
        self.assertEqual(src.split("\n").index("\u4e00\u2014\u2014\u4e8c") + 1, 10)
        with self.assertRaises(SystemExit) as cm:
            md2medium.convert(src)
        self.assertIn("line 10", str(cm.exception))

    def test_the_error_points_at_the_offending_line(self):
        with self.assertRaises(SystemExit) as cm:
            md2medium.convert("# T\n\nfine\n\n\u4e00\u2014\u2014\u4e8c\n")
        msg = str(cm.exception)
        self.assertIn("line 5", msg)
        self.assertIn("\u4e00\u2014\u2014\u4e8c", msg)

    def test_a_single_em_dash_is_left_alone(self):
        self.assertEqual(md2medium.convert("# T\n\n\u4e00\u2014\u4e8c\n")["html"],
                         "<p>\u4e00\u2014\u4e8c</p>")

    def test_en_dash_is_not_mistaken_for_it(self):
        # 2014-2016 style ranges use U+2013 and are fine.
        self.assertEqual(md2medium.convert("# T\n\n2014\u20132016\n")["html"],
                         "<p>2014\u20132016</p>")

    def test_two_em_dashes_in_one_line_but_apart_are_fine(self):
        out = md2medium.convert("# T\n\n\u4e00\u2014\u4e8c\u3001\u4e09\u2014\u56db\n")["html"]
        self.assertEqual(out, "<p>\u4e00\u2014\u4e8c\u3001\u4e09\u2014\u56db</p>")

    def test_a_run_of_three_is_rejected_too(self):
        with self.assertRaises(SystemExit):
            md2medium.convert("# T\n\n\u4e00\u2014\u2014\u2014\u4e8c\n")

    def test_a_code_block_is_exempt(self):
        # Medium adds no hair spaces inside a <pre>, so `——` renders there
        # exactly as written and is the correct CJK dash. Flagging it would
        # force the AGENTS.md sample to use punctuation it is not teaching.
        out = md2medium.convert("# T\n\n```text\na\u2014\u2014b\n```\n")["html"]
        self.assertEqual(out, "<pre><code>a\u2014\u2014b</code></pre>")

    def test_the_exemption_ends_with_the_fence(self):
        # The obvious way to get the exemption wrong is to latch it on and
        # stop checking the rest of the file.
        with self.assertRaises(SystemExit) as cm:
            md2medium.convert("# T\n\n```text\na\u2014\u2014b\n```\n\n\u4e00\u2014\u2014\u4e8c\n")
        self.assertIn("\u4e00\u2014\u2014\u4e8c", str(cm.exception))

    def test_the_fence_scan_agrees_with_the_converter(self):
        # double_dash_lines is what the repo sweep below uses; if it drifted
        # from the fence rules convert() applies, the sweep would pass on a
        # file convert() rejects.
        lines = ["prose ok", "```text", "a\u2014\u2014b", "```", "\u4e00\u2014\u2014\u4e8c"]
        self.assertEqual([k for k, _ in md2medium.double_dash_lines(lines)], [5])

    def test_every_shipped_article_is_clean(self):
        # The regression guard for the actual fix: all four articles were
        # rewritten from —— to —, and every file of each pack must stay that way.
        # Globbed rather than a fixed list of two names: the English editions
        # arrived as article.en.md + publish/en/medium-paste.md and would have
        # sat outside a hardcoded pair, unchecked.
        root = os.path.dirname(TOOLS)
        found = []
        for pattern in ("*/article*.md", "*/publish/medium-paste.md",
                        "*/publish/*/medium-paste.md"):
            for path in sorted(glob.glob(os.path.join(root, pattern))):
                with open(path, encoding="utf-8") as fh:
                    lines = fh.read().split("\n")
                # Same fence-aware scan convert() gates on, not a second copy
                # of the rule: code blocks legitimately keep their `——`.
                for k, _ in md2medium.double_dash_lines(lines):
                    found.append("%s:%d" % (os.path.relpath(path, root), k))
        self.assertEqual(found, [])

    def test_the_guard_actually_looks_at_the_english_packs(self):
        # A glob that silently matches nothing would make the test above pass
        # forever. Assert the English editions are really in its scope.
        root = os.path.dirname(TOOLS)
        seen = [os.path.relpath(p, root) for p in glob.glob(os.path.join(root, "*/article*.md"))]
        self.assertTrue([p for p in seen if p.endswith("article.en.md")],
                        "no article.en.md matched; the guard would not cover them")
        seen_paste = glob.glob(os.path.join(root, "*/publish/*/medium-paste.md"))
        self.assertTrue(seen_paste, "no publish/<lang>/medium-paste.md matched")


class TestPatchSubst(unittest.TestCase):
    def js(self):
        return medium_patch.subst_js("\u2014\u2014", "\u2014")

    def test_is_a_self_invoking_expression(self):
        js = self.js()
        self.assertTrue(js.strip().startswith("(() =>"))
        self.assertTrue(js.strip().endswith(")()"))

    def test_no_duplicate_const_declarations(self):
        declared = const_names(self.js())
        dupes = {n for n in declared if declared.count(n) > 1}
        self.assertEqual(dupes, set(), "redeclares %s" % sorted(dupes))

    def test_both_strings_are_embedded_as_json(self):
        js = medium_patch.subst_js("a\"b", "c\\d")
        self.assertIn(json.dumps("a\"b"), js)
        self.assertIn(json.dumps("c\\d"), js)

    def test_it_verifies_the_selection_before_pasting(self):
        # A range built from a stale offset would otherwise replace whatever
        # happens to sit there. Same reason drop_js reports what it selected.
        self.assertIn("sel.toString() !== OLD", self.js())

    def test_the_success_path_recounts_what_is_left(self):
        # `remaining` in the no-hit early return is not enough: the caller
        # loops on the value returned *after* a substitution, so asserting on
        # the snippet as a whole passes even if that recount is deleted.
        after_early_return = self.js().split("const [node, at] = hits[0];", 1)[1]
        self.assertIn("remaining: walk().length", after_early_return)

    def test_a_literal_miss_is_not_reported_as_a_clean_finish(self):
        # Medium stores `——` as HAIR — HAIR — SPACE, so the literal never
        # matches in prose and a bare `remaining: 0` would say "done" on an
        # article that still has every one of them.
        early = self.js().split("const [node, at] = hits[0];", 1)[0]
        # Not just the word "rendered": the count has to be DERIVED from the
        # invisible-stripped text, or a constant 0 would satisfy the assertion
        # and restore exactly the false clean this exists to prevent.
        self.assertIn("strip(raw).split(bare).length - 1", early)
        self.assertIn("\\u200A", early)

    def test_it_flags_a_match_split_across_text_nodes(self):
        # Reporting remaining:0 while innerText still shows the string would
        # look like a clean finish and silently leave the article wrong.
        self.assertIn("split", self.js())

    def test_it_replaces_only_one_occurrence_per_call(self):
        self.assertIn("hits[0]", self.js())
        self.assertIn("replaced: 1", self.js())


class TestConstNameExtractor(unittest.TestCase):
    """Guards the guard: a blind extractor makes every dupe check vacuous."""

    def test_sees_a_second_declarator(self):
        self.assertEqual(const_names("  const a = f(), b = g();"), ["a", "b"])

    def test_sees_destructured_bindings(self):
        self.assertEqual(const_names("  const [node, at] = hits[0];"), ["node", "at"])

    def test_does_not_invent_names_from_arrow_params_or_calls(self):
        self.assertEqual(const_names("  const norm = s => s.replace(/x/g, '');"), ["norm"])

    def test_it_catches_a_collision_the_old_regex_missed(self):
        js = medium_patch.replace_js("a", "b", "<p>x</p>") + "\n  const b = 1;"
        names = const_names(js)
        self.assertGreater(names.count("b"), 1)


class TestPatchCLI(unittest.TestCase):
    """The CLI is the surface an operator actually points at a published post."""

    def files(self):
        d = tempfile.TemporaryDirectory()
        self.addCleanup(d.cleanup)
        html = os.path.join(d.name, "f.html")
        with open(html, "w", encoding="utf-8") as fh:
            fh.write("<p>x</p>")
        png = os.path.join(d.name, "a.png")
        with open(png, "wb") as fh:
            fh.write(b"\x89PNG\r\n\x1a\n")
        return html, png

    def patch(self, *args):
        return run_tool(os.path.join(TOOLS, "medium_patch.py"), *args)

    def test_the_dry_flag_reaches_the_generated_snippet(self):
        # dry is read straight off sys.argv; without this the flag can be
        # broken while every unit test still passes, and --dry is the only
        # rehearsal an operator gets before editing a live article.
        html, _ = self.files()
        out = self.patch("replace", "a", "b", html, "--dry")
        self.assertEqual(out.returncode, 0, out.stderr)
        self.assertIn("if (true) return", out.stdout)
        self.assertNotIn("dispatchEvent", out.stdout.split("if (true) return")[0])

    def test_without_the_flag_the_snippet_is_live(self):
        html, _ = self.files()
        out = self.patch("replace", "a", "b", html)
        self.assertEqual(out.returncode, 0, out.stderr)
        self.assertIn("if (false) return", out.stdout)
        self.assertIn("dispatchEvent", out.stdout)

    def test_dry_is_refused_for_subcommands_that_do_not_honour_it(self):
        # Silently ignoring it would run the live action for someone who
        # believed they had asked for a rehearsal.
        for args in (["subst", "a", "b"], ["find", "a"], ["drop", "a.png"]):
            out = self.patch(*args, "--dry")
            self.assertNotEqual(out.returncode, 0, args)
            self.assertIn("--dry only applies to replace", out.stderr)

    def test_find_and_drop_carry_their_argument(self):
        out = self.patch("find", "導言")
        self.assertEqual(out.returncode, 0, out.stderr)
        self.assertIn(json.dumps("導言", ensure_ascii=False), out.stdout)
        out = self.patch("drop", "table-04.png")
        self.assertEqual(out.returncode, 0, out.stderr)
        self.assertIn("table-04.png", out.stdout)

    def test_subst_emits_a_snippet_that_reports_remaining(self):
        out = self.patch("subst", "——", "—")
        self.assertEqual(out.returncode, 0, out.stderr)
        self.assertIn("remaining", out.stdout)

    def test_image_embeds_the_file(self):
        _, png = self.files()
        out = self.patch("image", "導言", png)
        self.assertEqual(out.returncode, 0, out.stderr)
        self.assertIn("atob(", out.stdout)

    def test_image_refuses_a_file_that_is_not_a_png(self):
        # The snippet hardcodes image/png and uploads to a public CDN; a wrong
        # path would otherwise post arbitrary local bytes to the article.
        d = tempfile.TemporaryDirectory()
        self.addCleanup(d.cleanup)
        bogus = os.path.join(d.name, "cookies.json")
        with open(bogus, "w", encoding="utf-8") as fh:
            fh.write('{"sid":"SECRET"}')
        out = self.patch("image", "導言", bogus)
        self.assertNotEqual(out.returncode, 0)
        self.assertIn("not a PNG", out.stderr)
        self.assertNotIn("SECRET", out.stdout)

    def test_no_arguments_exits_nonzero(self):
        out = self.patch()
        self.assertNotEqual(out.returncode, 0)

    def test_each_subcommand_rejects_a_wrong_argument_count(self):
        for args in (["find"], ["find", "a", "b"], ["drop"], ["subst", "a"],
                     ["html"], ["replace", "a"]):
            self.assertNotEqual(self.patch(*args).returncode, 0, "%s" % args)


PASTE_BODY = "# T\n\nbody\n"      # the fixture article every driver test drives
# One figure, so a drive can go all the way through the image loop. The 📌 line
# is written by md2medium.slot_line() rather than typed, so this fixture cannot
# drift out of the pattern the converter accepts.
PASTE_WITH_FIGURE = "# T\n\nbody\n\n%s\n" % md2medium.slot_line("圖", "a.png")
GOOD_ID = "3c64a9622777"      # shape of every https://medium.com/p/<id> in the repo
OTHER_ID = "ccbf0cbe2691"     # a real id from a different pack: the neighbouring row
# How every pack records which post it is. --post refuses an id this line does
# not name, and that refusal is the only check --retitle cannot switch off.
LEDGER_LINE = "**Post ID** `%s`"


class DriverFixture:
    """A throwaway repo holding a copy of medium_draft.sh, run under an empty HOME.

    Shared by the three driver suites below rather than copied into each: the
    fake root has to mirror the real layout exactly (the driver resolves every
    path from `dirname $0/..`), and three private copies of that layout is how
    one of them ends up testing a directory shape the driver no longer uses.
    """

    SCRIPT = os.path.join(TOOLS, "medium_draft.sh")

    def article(self, packs, ledger=GOOD_ID, paste=PASTE_BODY, images=()):
        """A throwaway repo root holding a copy of the driver and one article.

        The driver resolves paths from its OWN location (`dirname $0/..`), not
        from the cwd, so the copy has to live in the fake root or every path it
        builds would point back at the real repo.

        `ledger` is the Post ID each pack records, since --post refuses an id
        no PUBLISHED.md names; pass None for a pack that has no ledger at all.
        `images` are files to drop in publish[/lang]/images, which md2medium
        insists exist before a browser opens.
        """
        d = tempfile.TemporaryDirectory()
        self.addCleanup(d.cleanup)
        os.makedirs(os.path.join(d.name, "tools"))
        script = os.path.join(d.name, "tools", "medium_draft.sh")
        shutil.copy(self.SCRIPT, script)
        root = os.path.join(d.name, "2026-01-sample")
        for pack, has_images in packs.items():
            pub = os.path.join(root, "publish", pack) if pack else os.path.join(root, "publish")
            os.makedirs(pub, exist_ok=True)
            with open(os.path.join(pub, "medium-paste.md"), "w", encoding="utf-8") as fh:
                fh.write(paste)
            if ledger is not None:
                with open(os.path.join(pub, "PUBLISHED.md"), "w", encoding="utf-8") as fh:
                    fh.write("# Published\n\n%s\n" % (LEDGER_LINE % ledger))
            if has_images:
                os.makedirs(os.path.join(pub, "images"), exist_ok=True)
                for name in images:
                    with open(os.path.join(pub, "images", name), "wb") as fh:
                        fh.write(b"\x89PNG\r\n\x1a\n")
        return script, "2026-01-sample"

    def run_driver(self, script, *args, env=None):
        # Isolated HOME on purpose. The driver resolves browse from
        # $HOME/.claude/skills/gstack/browse/dist/browse, which exists on a
        # developer machine — so if a path guard ever regresses, these tests
        # would reach `browse goto https://medium.com` and the suite's "no
        # network, no browser" promise would quietly depend on the very code
        # under test. An empty HOME makes that failure mode impossible.
        home = tempfile.TemporaryDirectory()
        self.addCleanup(home.cleanup)
        return subprocess.run(["bash", script] + list(args),
                              capture_output=True, text=True,
                              env={**os.environ, "HOME": home.name, **(env or {})})


class TestMediumDraftLangPack(DriverFixture, unittest.TestCase):
    """Path resolution in medium_draft.sh, exercised without a browser.

    Every check here happens before the script touches `browse`, which is what
    makes it testable at all. The failure being guarded against is quiet: point
    the driver at a translated medium-paste.md while it still uploads
    publish/images and it ships the wrong figures, and every later gate —
    block diff, link count, figure-position check — still reports a match,
    because those compare against the payload, not against the language.
    """

    def test_usage_mentions_the_lang_argument(self):
        out = self.run_driver(self.SCRIPT)
        self.assertNotEqual(out.returncode, 0)
        self.assertIn("[lang]", out.stderr)

    def test_a_lang_that_is_a_path_is_refused(self):
        # 'en/../..' would walk out of the article directory entirely.
        for bad in ("../etc", "en/../..", "a/b", "en;rm"):
            out = self.run_driver(self.SCRIPT, "any-article", bad)
            self.assertNotEqual(out.returncode, 0, bad)
            self.assertIn("invalid lang", out.stderr, bad)

    def test_the_lang_pack_uses_its_own_images_not_the_default_pack(self):
        # THE regression: publish/images exists and is valid, publish/en/images
        # does not. Resolving images from the default pack would sail past
        # validation; resolving them from the lang pack must fail loudly.
        script, name = self.article({"": True, "en": False})
        out = self.run_driver(script, name, "en")
        self.assertNotEqual(out.returncode, 0)
        self.assertIn("no such images dir", out.stderr)
        self.assertIn(os.path.join("publish", "en", "images"), out.stderr)

    def test_omitting_the_lang_uses_the_default_pack(self):
        # Mirror: only the en pack exists, so the no-lang run must look for
        # publish/medium-paste.md and say so.
        script, name = self.article({"en": True})
        out = self.run_driver(script, name)
        self.assertNotEqual(out.returncode, 0)
        self.assertIn("no such paste file", out.stderr)
        self.assertIn(os.path.join("publish", "medium-paste.md"), out.stderr)
        self.assertNotIn(os.path.join("publish", "en"), out.stderr)

    def test_a_missing_lang_pack_names_the_pack_it_wanted(self):
        script, name = self.article({"": True})
        out = self.run_driver(script, name, "fr")
        self.assertNotEqual(out.returncode, 0)
        self.assertIn(os.path.join("publish", "fr", "medium-paste.md"), out.stderr)

    def test_a_hyphenated_or_underscored_lang_is_accepted(self):
        # Only rejections were covered, so `-` and `_` in the charset were
        # dead weight: narrowing it to [a-zA-Z0-9] passed the whole suite while
        # silently refusing a future zh-TW or pt_BR pack. A complete pack gets
        # past validation and dies at the browse lookup instead (EX_UNAVAILABLE),
        # which is exactly the boundary this asserts.
        for lang in ("zh-TW", "pt_BR"):
            script, name = self.article({lang: True})
            out = self.run_driver(script, name, lang)
            self.assertNotIn("invalid lang", out.stderr, lang)
            self.assertNotIn("no such paste file", out.stderr, lang)
            self.assertEqual(out.returncode, EX_UNAVAILABLE, "%s: %s" % (lang, out.stderr))

    def test_usage_and_validation_failures_exit_with_EX_USAGE(self):
        # Every other driver test only asserts "not zero". The script defines
        # sysexits codes deliberately, so `exit "$EX_USAGE"` could become
        # `exit 1` unnoticed.
        script, name = self.article({"": True})
        self.assertEqual(self.run_driver(script).returncode, EX_USAGE)
        self.assertEqual(self.run_driver(script, name, "../etc").returncode, EX_USAGE)
        self.assertEqual(self.run_driver(script, name, "fr").returncode, EX_USAGE)

    def test_a_pack_resolving_outside_the_repo_is_refused(self):
        # $ARTICLE gets no charset check, so both pre-flight guards pass
        # happily for '../somewhere-else' — and every PNG in that directory
        # would be base64'd into the draft and uploaded to a public CDN.
        outside = tempfile.TemporaryDirectory()
        self.addCleanup(outside.cleanup)
        pub = os.path.join(outside.name, "publish")
        os.makedirs(os.path.join(pub, "images"))
        with open(os.path.join(pub, "medium-paste.md"), "w", encoding="utf-8") as fh:
            fh.write(PASTE_BODY)
        script, _ = self.article({"": True})
        fake_root = os.path.dirname(os.path.dirname(script))
        rel = os.path.relpath(outside.name, fake_root)
        self.assertTrue(rel.startswith(".."), rel)   # the fixture must really escape
        out = self.run_driver(script, rel)
        self.assertEqual(out.returncode, EX_USAGE, out.stderr)
        self.assertIn("outside the repo", out.stderr)

    def test_every_shipped_lang_pack_is_complete(self):
        # Each publish/<lang>/ must carry both halves; a pack with a paste file
        # and no images dir would only fail at drive time.
        root = os.path.dirname(TOOLS)
        for paste in sorted(glob.glob(os.path.join(root, "*/publish/*/medium-paste.md"))):
            pack = os.path.dirname(paste)
            self.assertTrue(os.path.isdir(os.path.join(pack, "images")),
                            "%s has no images/" % os.path.relpath(pack, root))


class TestMediumDraftPostArguments(DriverFixture, unittest.TestCase):
    """`--post` parsing, all of it before a browser exists.

    In `--post` mode every destructive step downstream aims at whatever id the
    command line handed over, on a story readers can already see. So the id is
    checked at parse time, and these tests hold that boundary: a refusal must
    arrive as EX_USAGE with nothing opened, never as a run that starts and
    discovers the problem in the editor.
    """

    def test_usage_mentions_post_and_retitle(self):
        out = self.run_driver(self.SCRIPT)
        self.assertEqual(out.returncode, EX_USAGE)
        self.assertIn("--post <id>", out.stderr)
        self.assertIn("--retitle", out.stderr)

    def test_post_without_an_id_is_refused(self):
        # `--post` last on the line: reading $2 blind would set POST_ID to the
        # empty string and go on to open https://medium.com/p//edit.
        script, name = self.article({"": True})
        out = self.run_driver(script, name, "--post")
        self.assertEqual(out.returncode, EX_USAGE, out.stderr)
        self.assertIn("--post needs an id", out.stderr)

    def test_a_malformed_id_is_refused_with_the_expected_shape(self):
        # A glob cannot count, so length and alphabet are two separate cases in
        # the script and both are exercised here. The uppercase one is the
        # realistic paste: Medium's own URLs are lowercase, but an id retyped
        # from a screenshot is not, and /p/3C64A9622777/edit is not a post.
        script, name = self.article({"": True})
        for bad in ("abc", "3c64a9622777f", "3C64A9622777", "3c64a962777g",
                    "3c64-a962777", "", "3c64 a9622777"):
            for form in ([("--post", bad)], [("--post=%s" % bad,)]):
                out = self.run_driver(script, name, *form[0])
                self.assertEqual(out.returncode, EX_USAGE, "%r: %s" % (bad, out.stderr))
                self.assertIn("invalid --post id", out.stderr, repr(bad))
                self.assertIn("twelve lowercase hex digits", out.stderr, repr(bad))

    def test_the_id_is_checked_before_anything_is_resolved_or_opened(self):
        # The pack here is complete, so a run that got past parsing would go
        # all the way to the browse lookup (EX_UNAVAILABLE). EX_USAGE plus the
        # id message is the proof that the id check comes first.
        script, name = self.article({"": True})
        out = self.run_driver(script, name, "--post", "nope")
        self.assertEqual(out.returncode, EX_USAGE, out.stderr)
        self.assertIn("invalid --post id", out.stderr)
        self.assertNotIn("browse not found", out.stderr)

    def test_a_valid_id_with_a_missing_article_still_exits_EX_USAGE(self):
        # A good id does not excuse a bad pack: this has to fail the same way
        # a plain run does, naming the paste file it wanted.
        script, _ = self.article({"": True})
        out = self.run_driver(script, "2026-01-nonexistent", "--post", GOOD_ID)
        self.assertEqual(out.returncode, EX_USAGE, out.stderr)
        self.assertIn("no such paste file", out.stderr)
        self.assertIn(os.path.join("2026-01-nonexistent", "publish"), out.stderr)

    def test_the_flag_parses_anywhere_in_the_line(self):
        # The id is copied out of the table in PUBLISHING.md onto the end of a
        # command that already reads `<article> en`, so every position has to
        # land the same way. A `shift` that forgot the id would leave it as the
        # article name and the run would die on the pack instead.
        script, name = self.article({"en": True})
        for args in (["--post", GOOD_ID, name, "en"],
                     [name, "--post", GOOD_ID, "en"],
                     [name, "en", "--post", GOOD_ID],
                     [name, "en", "--post=%s" % GOOD_ID],
                     ["--post=%s" % GOOD_ID, name, "en"]):
            out = self.run_driver(script, *args)
            self.assertNotIn("no such paste file", out.stderr, args)
            self.assertNotIn("unexpected argument", out.stderr, args)
            self.assertNotIn("invalid lang", out.stderr, args)
            # Everything resolved; the run stops at the browse lookup, which is
            # the first thing an empty HOME cannot provide.
            self.assertEqual(out.returncode, EX_UNAVAILABLE, "%s: %s" % (args, out.stderr))

    def test_the_lang_is_still_the_second_positional_with_post_in_front(self):
        # Mirror of the above with the pack missing: whichever position --post
        # took, `en` must still have been read as the language pack.
        script, name = self.article({"": True})
        for args in (["--post", GOOD_ID, name, "en"], [name, "--post", GOOD_ID, "en"]):
            out = self.run_driver(script, *args)
            self.assertEqual(out.returncode, EX_USAGE, "%s: %s" % (args, out.stderr))
            self.assertIn(os.path.join("publish", "en", "medium-paste.md"), out.stderr, args)

    def test_retitle_alone_is_refused(self):
        # On a new story there is no title to disagree with, so the flag could
        # only read as approval for something the run never checks.
        script, name = self.article({"": True})
        out = self.run_driver(script, name, "--retitle")
        self.assertEqual(out.returncode, EX_USAGE, out.stderr)
        self.assertIn("--retitle only means something with --post", out.stderr)

    def test_retitle_with_post_gets_through_parsing(self):
        script, name = self.article({"": True})
        out = self.run_driver(script, name, "--post", GOOD_ID, "--retitle")
        self.assertNotIn("--retitle", out.stderr)
        self.assertEqual(out.returncode, EX_UNAVAILABLE, out.stderr)

    def test_an_unknown_option_is_refused(self):
        script, name = self.article({"": True})
        for bad in ("--nope", "-p", "--post-id"):
            out = self.run_driver(script, name, bad)
            self.assertEqual(out.returncode, EX_USAGE, "%s: %s" % (bad, out.stderr))
            self.assertIn("unknown option: %s" % bad, out.stderr)

    def test_a_third_positional_is_refused(self):
        # It used to be ignored, which is how `<article> en --post <id>` typed
        # as `<article> en <id>` would quietly build a brand new draft and
        # strand every /p/<id> cross-link in the series.
        script, name = self.article({"": True})
        out = self.run_driver(script, name, "en", GOOD_ID)
        self.assertEqual(out.returncode, EX_USAGE, out.stderr)
        self.assertIn("unexpected argument: %s" % GOOD_ID, out.stderr)

    def test_an_empty_positional_still_counts_as_one(self):
        # `"$dir" "$lang" "$id"` out of a wrapper, with $lang empty for the
        # Chinese pack: the guard above tested "has LANG_PACK been filled in",
        # and an empty string is indistinguishable from "not given", so the id
        # slid into LANG_PACK and the run failed on a paste file at
        # publish/3c64a9622777/ instead of on the flag that was never typed.
        script, name = self.article({"": True})
        out = self.run_driver(script, name, "", GOOD_ID)
        self.assertEqual(out.returncode, EX_USAGE, out.stderr)
        self.assertIn("unexpected argument: %s" % GOOD_ID, out.stderr)
        self.assertNotIn("no such paste file", out.stderr)
        # And an empty FIRST positional does not silently promote the language
        # pack into the article name.
        out = self.run_driver(script, "", "en")
        self.assertEqual(out.returncode, EX_USAGE, out.stderr)
        self.assertNotIn(os.path.join("en", "publish"), out.stderr)


    def test_the_plain_form_is_untouched(self):
        # No --post: the two positional arguments still resolve exactly as they
        # did before the flag existed, and nothing about posts is mentioned.
        script, name = self.article({"": True, "en": True})
        for args in ([name], [name, "en"]):
            out = self.run_driver(script, *args)
            self.assertEqual(out.returncode, EX_UNAVAILABLE, "%s: %s" % (args, out.stderr))
            self.assertNotIn("--post", out.stderr, args)
            self.assertNotIn("--retitle", out.stderr, args)


class TestMediumDraftPostLedger(DriverFixture, unittest.TestCase):
    """--post is bound to the pack's own PUBLISHED.md before a browser opens.

    This is the check that stands between a mistyped id and a rewritten
    article, and it is the only one of the three that --retitle cannot switch
    off. It has to be, because every gate downstream compares the editor
    against THIS pack's payload: point the run at the neighbouring row of the
    table in PUBLISHING.md and, once the refill has finished, every one of them
    honestly reports a match on an article that has just been overwritten.
    """

    def test_an_id_the_pack_does_not_record_is_refused_before_the_browser(self):
        script, name = self.article({"": True}, ledger=GOOD_ID)
        out = self.run_driver(script, name, "--post", OTHER_ID)
        self.assertEqual(out.returncode, EX_USAGE, out.stderr)
        self.assertIn("is not the post this pack belongs to", out.stderr)
        self.assertIn(GOOD_ID, out.stderr)          # what it should have been
        # Nothing was opened: a complete pack would otherwise reach the browse
        # lookup, which is the first thing an empty HOME cannot provide.
        self.assertNotIn("browse not found", out.stderr)

    def test_retitle_does_not_override_it(self):
        # The realistic sequence: the first run stops on the title, the
        # operator reads that as "the title was reworded this round" and adds
        # --retitle. That must not turn the id check off too.
        script, name = self.article({"": True}, ledger=GOOD_ID)
        out = self.run_driver(script, name, "--post", OTHER_ID, "--retitle")
        self.assertEqual(out.returncode, EX_USAGE, out.stderr)
        self.assertIn("is not the post this pack belongs to", out.stderr)
        self.assertIn("--retitle does not override", out.stderr)

    def test_the_matching_id_gets_through(self):
        script, name = self.article({"": True}, ledger=GOOD_ID)
        out = self.run_driver(script, name, "--post", GOOD_ID)
        self.assertNotIn("this pack belongs to", out.stderr)
        self.assertEqual(out.returncode, EX_UNAVAILABLE, out.stderr)

    def test_a_pack_with_no_ledger_is_refused_rather_than_waved_through(self):
        # --post refills a story that already exists, and in this repo every
        # story that exists is recorded. "No ledger" is the state of a pack
        # nobody has published, so an id for it came from somewhere else.
        script, name = self.article({"": True}, ledger=None)
        out = self.run_driver(script, name, "--post", GOOD_ID)
        self.assertEqual(out.returncode, EX_USAGE, out.stderr)
        self.assertIn("no ledger for this pack", out.stderr)
        self.assertIn(LEDGER_LINE % GOOD_ID, out.stderr)   # says how to fix it

    def test_a_ledger_that_records_no_id_is_refused(self):
        script, name = self.article({"": True}, ledger=None)
        pack = os.path.join(os.path.dirname(os.path.dirname(script)),
                            name, "publish")
        with open(os.path.join(pack, "PUBLISHED.md"), "w", encoding="utf-8") as fh:
            fh.write("# Published\n\nno id here\n")
        out = self.run_driver(script, name, "--post", GOOD_ID)
        self.assertEqual(out.returncode, EX_USAGE, out.stderr)
        self.assertIn("records no Post ID", out.stderr)

    def test_the_id_has_to_be_on_the_Post_ID_line_not_anywhere_in_the_file(self):
        # THE reason this is not `grep -q "$POST_ID" PUBLISHED.md`: the Chinese
        # ledgers carry a cross-reference to the English post's id, so a plain
        # grep would accept the English id for a Chinese run, and the title
        # check that would have caught the mixup is the one --retitle turns
        # off. Line-anchored, so a mention is not a claim.
        script, name = self.article({"": True}, ledger=GOOD_ID)
        pack = os.path.join(os.path.dirname(os.path.dirname(script)),
                            name, "publish")
        with open(os.path.join(pack, "PUBLISHED.md"), "a", encoding="utf-8") as fh:
            fh.write("\n- English edition: publish/en/ (Post ID `%s`)\n" % OTHER_ID)
        out = self.run_driver(script, name, "--post", OTHER_ID)
        self.assertEqual(out.returncode, EX_USAGE, out.stderr)
        self.assertIn("is not the post this pack belongs to", out.stderr)

    def test_each_language_pack_is_bound_to_its_own_ledger(self):
        script, name = self.article({"": True, "en": True}, ledger=GOOD_ID)
        pack = os.path.join(os.path.dirname(os.path.dirname(script)),
                            name, "publish", "en")
        with open(os.path.join(pack, "PUBLISHED.md"), "w", encoding="utf-8") as fh:
            fh.write("# Published\n\n%s\n" % (LEDGER_LINE % OTHER_ID))
        # The en pack's id is refused for the zh run and vice versa.
        out = self.run_driver(script, name, "--post", OTHER_ID)
        self.assertEqual(out.returncode, EX_USAGE, out.stderr)
        out = self.run_driver(script, name, "en", "--post", GOOD_ID)
        self.assertEqual(out.returncode, EX_USAGE, out.stderr)
        # And each one's own id gets through to the browse lookup.
        self.assertEqual(self.run_driver(script, name, "--post", GOOD_ID).returncode,
                         EX_UNAVAILABLE)
        self.assertEqual(self.run_driver(script, name, "en", "--post", OTHER_ID).returncode,
                         EX_UNAVAILABLE)

    def test_every_shipped_pack_records_an_id_this_guard_can_read(self):
        # The guard is only as good as the corpus it reads. Sixteen packs, each
        # with a Post ID line, all distinct — a duplicate would mean two packs
        # claiming the same live post, and both would pass their own check.
        found = {}
        for ledger in sorted(glob.glob(os.path.join(REPO, "*/publish/PUBLISHED.md"))) \
                + sorted(glob.glob(os.path.join(REPO, "*/publish/*/PUBLISHED.md"))):
            with open(ledger, encoding="utf-8") as fh:
                ids = re.findall(r"^\*\*Post ID\*\* `([0-9a-f]+)`", fh.read(), re.M)
            rel = os.path.relpath(ledger, REPO)
            self.assertTrue(ids, "%s records no Post ID" % rel)
            self.assertEqual(len(ids[0]), 12, "%s: %r is not 12 hex digits" % (rel, ids[0]))
            found[rel] = ids[0]
        self.assertGreaterEqual(len(found), 16, found)
        self.assertEqual(len(set(found.values())), len(found),
                         "two packs claim the same post: %s" % sorted(found.items()))


# A stand-in for `browse`, so the driver's two modes can be driven far enough
# to see which page they open and which guards fire. It records every call and
# answers from a directory of canned replies; anything it was not told about
# exits non-zero, because a silent default is how a new browser step would slip
# past this suite. Written in sh, not Python: a drive makes a dozen of these
# calls and an interpreter start each time is most of the suite's runtime.
FAKE_BROWSE = r'''#!/bin/sh
[ "$1" = --headed ] && shift
verb=$1
note=$2
key=$verb
if [ "$verb" = eval ]; then             # keep the snippet the driver generated
  note=${2##*/}
  key="eval:$note"
  cp "$2" "$FAKE_BROWSE_EVALED/$note"
elif [ "$verb" = js ]; then             # an inline snippet, too long to log
  note=""
fi
if [ -n "$note" ]; then
  echo "$verb $note" >> "$FAKE_BROWSE_LOG"
else
  echo "$verb" >> "$FAKE_BROWSE_LOG"
fi
# A canned reply of several lines answers successive calls, one line per call,
# and its last line then repeats. The driver reads `state` at every checkpoint
# and polls two of them, so a test about what happens as the page changes has
# to be able to hand back a different answer the second time.
if [ -f "$FAKE_BROWSE_RULES/$key" ]; then
  reply=$(head -1 "$FAKE_BROWSE_RULES/$key")
  if [ "$(wc -l < "$FAKE_BROWSE_RULES/$key")" -gt 1 ]; then
    tail -n +2 "$FAKE_BROWSE_RULES/$key" > "$FAKE_BROWSE_RULES/$key.rest"
    mv "$FAKE_BROWSE_RULES/$key.rest" "$FAKE_BROWSE_RULES/$key"
  fi
  # The real browse reports a failure on stderr with an empty stdout, which is
  # the shape every guard in the driver has to be written against.
  if [ "$reply" = "!fail" ]; then
    echo "browse: the daemon went away" >&2
    exit 1
  fi
  echo "$reply"
  exit 0
fi
case "$key" in
  disconnect|goto|cookie-import|press) echo "" ;;
  text) echo "Drafts" ;;
  url) sed -n 's/^goto //p' "$FAKE_BROWSE_LOG" | tail -1 ;;
  # The URL comes back from the page the driver was sent to, not from a
  # literal: the driver checks it against the id it asked for, and a hardcoded
  # answer here would agree with itself whatever the driver did.
  eval:identify.js)
    echo "{\"match\":true,\"want\":\"T\",\"got\":\"T\",\"url\":\"$(sed -n 's/^goto //p' "$FAKE_BROWSE_LOG" | tail -1)\",\"grafs\":2,\"figures\":0}" ;;
  eval:title.js) echo '{"title":"T"}' ;;
  # Stops every drive at the same place: after both modes have opened their
  # page, set the title and generated a body snippet, and before any image is
  # uploaded. Tests that want the guards past this point say so.
  eval:body.js) echo '{"err":"no body grafs"}' ;;
  *) echo "fake browse: unscripted call $*" >&2; exit 3 ;;
esac
'''

# A refill that did everything it promises: the body replaced, the old figures
# gone with it, the title still this pack's.
REFILL_OK = '{"replaced":149,"figuresBefore":14,"figuresLeft":0,"title":"T","titleOk":true}'


def state(figures=0, imgs=None, pending=0, slots=0):
    """One `state` reply, in the key order the driver's globs depend on."""
    return json.dumps({"figures": figures,
                       "imgs": figures if imgs is None else imgs,
                       "pending": pending, "slots": slots},
                      separators=(",", ":"))

# The driver calls `sleep` between browser steps (up to 20 times while it waits
# for a long post to lay out). Nothing here is racing, so they only cost wall
# clock. Overriding it on PATH rather than editing the script keeps the timing
# constants under test.
FAKE_SLEEP = "#!/bin/sh\nexit 0\n"

# The real one reads the login Keychain, which no test may touch.
FAKE_COOKIES = ('#!/usr/bin/env python3\nimport sys\n'
                'open(sys.argv[sys.argv.index("--out") + 1], "w").write("[]")\n')


class Drive:
    """One finished run of the driver against the fake browser."""

    def __init__(self, out, calls, evaled):
        self.out, self.calls, self.evaled = out, calls, evaled

    def js(self, name):
        """The snippet the driver actually handed to `browse eval`."""
        path = os.path.join(self.evaled, name)
        if not os.path.exists(path):
            raise AssertionError("%s was never eval'd; calls: %s" % (name, self.calls))
        with open(path, encoding="utf-8") as fh:
            return fh.read()


class Driven(DriverFixture):
    """One drive of the whole driver against the recorder, and what it saw.

    Two suites use it: the guard tests, which stop the run somewhere and read
    the refusal, and the finishing tests, which let it reach the end. Shared
    rather than copied for the reason the fixture above is: a second private
    copy of the browser stand-in is how one suite ends up testing a driver step
    the other one no longer takes.
    """

    def drive(self, *args, rules=None, packs=None, **fixture):
        script, name = self.article(packs or {"": True}, **fixture)
        root = os.path.dirname(os.path.dirname(script))
        # The driver runs the real ones: what a snippet says and what
        # verify_draft.py makes of the answer are the behaviour under test.
        for mod in ("md2medium.py", "medium_js.py", "verify_draft.py"):
            shutil.copy(os.path.join(TOOLS, mod), os.path.join(root, "tools", mod))
        self.write(os.path.join(root, "tools", "chrome_cookies.py"), FAKE_COOKIES)
        browse = os.path.join(root, ".claude", "skills", "gstack", "browse", "dist", "browse")
        self.write(browse, FAKE_BROWSE)
        binned = self.write(os.path.join(root, "bin", "sleep"), FAKE_SLEEP)
        log = os.path.join(root, "browse.log")
        evaled = os.path.join(root, "evaled")
        os.makedirs(evaled)
        canned = os.path.join(root, "rules")
        os.makedirs(canned)
        # Medium's save indicator answers "Saved" unless a test says otherwise:
        # every run reaches it, and restating it in each happy-path case would
        # only bury the cases that are actually about the save.
        rules = dict({"eval:saved.js": '{"message":"Saved"}'}, **(rules or {}))
        for key, reply in rules.items():
            # A list is a reply per call, in order; the last one repeats.
            lines = reply if isinstance(reply, list) else [reply]
            with open(os.path.join(canned, key), "w", encoding="utf-8") as fh:
                fh.write("".join(line + "\n" for line in lines))
        out = self.run_driver(script, name, *args, env={
            "PATH": os.path.dirname(binned) + os.pathsep + os.environ["PATH"],
            "FAKE_BROWSE_LOG": log,
            "FAKE_BROWSE_EVALED": evaled,
            "FAKE_BROWSE_RULES": canned,
        })
        calls = []
        if os.path.exists(log):
            with open(log, encoding="utf-8") as fh:
                calls = fh.read().splitlines()
        self.assertNotIn("unscripted call", out.stderr, out.stderr)
        return Drive(out, calls, evaled)

    def write(self, path, text):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(text)
        os.chmod(path, 0o755)
        return path

    def gotos(self, drive):
        return [c[5:] for c in drive.calls if c.startswith("goto ")]

    def timeout(self):
        """EDITOR_LOAD_TIMEOUT_S, read from the script rather than restated."""
        with open(self.SCRIPT, encoding="utf-8") as fh:
            return int(re.search(r"EDITOR_LOAD_TIMEOUT_S=(\d+)", fh.read()).group(1))

    def editor(self, texts, tags, links=0, dividers=0):
        """What `medium_js.py dump` would report for a draft that came out right.

        `dividers` is the number of section *breaks*, not the `<hr>` count:
        Medium emits one structural `<hr>` per section including the first, so
        the snippet reports `sections - 1`. See TestDumpSnippet.
        """
        return json.dumps({"texts": texts, "tags": tags,
                           "links": links, "dividers": dividers})


class TestMediumDraftPostDrive(Driven, unittest.TestCase):
    """Which page each mode opens, and which guards stop it, with a fake browser.

    Everything in the `--post` path that matters happens in the browser, so a
    pre-flight test cannot see it: that the id — not a new story — is what
    gets opened, that a redirect or a different title stops the run *before* a
    graf is touched, and that the body paste it sends is the one that clears
    the old figures. `browse` is replaced by a recorder, so those are all
    observable without a Medium session.
    """

    def test_without_post_it_opens_a_new_story(self):
        d = self.drive()
        self.assertIn("https://medium.com/new-story", self.gotos(d))
        self.assertEqual([g for g in self.gotos(d) if "/p/" in g], [])
        self.assertNotIn("eval identify.js", d.calls)   # nothing to identify

    def test_post_opens_that_posts_editor_and_never_a_new_story(self):
        # The whole point of the mode: a new draft would get a new Post ID, and
        # every https://medium.com/p/<id> cross-link in the series points at
        # the old one.
        d = self.drive("--post", GOOD_ID)
        self.assertIn("https://medium.com/p/%s/edit" % GOOD_ID, self.gotos(d))
        self.assertNotIn("https://medium.com/new-story", self.gotos(d))

    def test_post_identifies_the_story_before_touching_it(self):
        d = self.drive("--post", GOOD_ID)
        self.assertIn("eval identify.js", d.calls)
        self.assertLess(d.calls.index("eval identify.js"), d.calls.index("eval body.js"),
                        d.calls)
        payload = md2medium.convert(PASTE_BODY)
        self.assertEqual(d.js("identify.js").strip(), medium_js.identify_js(payload).strip())

    def test_a_redirect_away_from_the_id_stops_before_any_edit(self):
        # Medium bounces an id that is not yours, or no longer exists, to the
        # read view or the drafts list. Landing there and pasting would rewrite
        # whatever story it landed on.
        elsewhere = "https://medium.com/me/stories/drafts"
        d = self.drive("--post", GOOD_ID, rules={"url": elsewhere})
        self.assertEqual(d.out.returncode, EX_UNAVAILABLE, d.out.stderr)
        self.assertIn("did not open", d.out.stderr)
        self.assertIn(elsewhere, d.out.stderr)
        self.assertIn("not a post of yours, or the page never navigated", d.out.stderr)
        self.assertEqual([c for c in d.calls if c.startswith("eval ")], [], d.calls)

    def test_the_read_view_for_the_same_id_is_a_redirect_too(self):
        # THE case the URL check used to miss. It was `case $here in *$id*`,
        # and every published URL in this repo ENDS in the same id
        # (https://fantasybz.medium.com/<slug>-<id>), which is exactly where
        # Medium sends an id you cannot edit. So the one redirect the check was
        # written for was the one it waved through, and the run went on to
        # spend 20s polling for an editor and blame the post.
        read_view = "https://fantasybz.medium.com/some-slug-%s" % GOOD_ID
        d = self.drive("--post", GOOD_ID, rules={"url": read_view})
        self.assertEqual(d.out.returncode, EX_UNAVAILABLE, d.out.stderr)
        self.assertIn(read_view, d.out.stderr)
        self.assertIn("did not open an editor", d.out.stderr)
        self.assertEqual([c for c in d.calls if c.startswith("eval ")], [], d.calls)

    def test_a_signin_bounce_carrying_the_id_is_a_redirect_too(self):
        # Same shape, different cause: an expired session goes to /m/signin
        # with the edit URL in the query string, id included.
        bounce = ("https://medium.com/m/signin?redirect=https%%3A%%2F%%2Fmedium.com"
                  "%%2Fp%%2F%s%%2Fedit" % GOOD_ID)
        d = self.drive("--post", GOOD_ID, rules={"url": bounce})
        self.assertEqual(d.out.returncode, EX_UNAVAILABLE, d.out.stderr)
        self.assertEqual([c for c in d.calls if c.startswith("eval ")], [], d.calls)

    def test_the_editor_url_is_read_again_from_inside_identify(self):
        # Guard 1 says where the browser was; this says where the answer came
        # from. A page that navigated in between would otherwise be identified
        # on the strength of a URL read before it moved.
        d = self.drive("--post", GOOD_ID, rules={
            "eval:identify.js": '{"match":true,"want":"T","got":"T",'
                                '"url":"https://medium.com/p/%s/edit",'
                                '"grafs":2,"figures":0}' % OTHER_ID})
        self.assertEqual(d.out.returncode, EX_UNAVAILABLE, d.out.stderr)
        self.assertIn("is not the one at", d.out.stderr)
        self.assertNotIn("eval body.js", d.calls)

    def test_a_title_that_is_not_this_articles_stops_before_any_edit(self):
        # The realistic mistake is the neighbouring row of the id table, and
        # these titles share long prefixes, so this is the only check that
        # compares the id against what is on the screen.
        d = self.drive("--post", GOOD_ID, rules={
            "eval:identify.js": '{"match":false,"want":"T","got":"Some Other Story",'
                                '"url":"https://medium.com/p/%s/edit",'
                                '"grafs":2,"figures":0}' % GOOD_ID})
        self.assertEqual(d.out.returncode, EX_UNAVAILABLE, d.out.stderr)
        self.assertIn("the post's title is not this pack's title", d.out.stderr)
        self.assertIn("--retitle", d.out.stderr)
        # Printed for a human to read, on the stream the instruction to read it
        # went to: `2>err.log` used to be told to compare two lines that had
        # gone to stdout.
        self.assertIn("Some Other Story", d.out.stdout)
        self.assertIn("Some Other Story", d.out.stderr)
        self.assertNotIn("eval title.js", d.calls)
        self.assertNotIn("eval body.js", d.calls)

    def test_retitle_lets_a_reworded_title_through(self):
        d = self.drive("--post", GOOD_ID, "--retitle", rules={
            "eval:identify.js": '{"match":false,"want":"T","got":"Renamed",'
                                '"url":"https://medium.com/p/%s/edit",'
                                '"grafs":2,"figures":0}' % GOOD_ID})
        self.assertIn("--retitle given, continuing", d.out.stdout)
        self.assertIn("eval title.js", d.calls)
        self.assertIn("eval body.js", d.calls)
        # And it says what it did and did not waive: the id was still bound to
        # the pack's ledger, and this run destroys the evidence for the next
        # one by overwriting the title it just disagreed with.
        self.assertIn("PUBLISHED.md", d.out.stdout)
        self.assertIn("re-run will not be able to repeat", d.out.stdout)

    def test_a_title_that_already_matches_is_not_pasted_over(self):
        # A write on a published post that buys nothing, and worse: the title
        # is the run's only content-level check that the id opened the right
        # story, so overwriting it first means a run that dies later has erased
        # the evidence — and the re-run it recommends would then see a title
        # that matches because the failed run put it there.
        d = self.drive("--post", GOOD_ID)
        self.assertNotIn("eval title.js", d.calls)
        self.assertIn("title already matches this pack", d.out.stdout)
        # A new story has no title to compare, so it is always written there.
        self.assertIn("eval title.js", self.drive().calls)

    def test_an_editor_that_never_appears_is_polled_then_refused(self):
        # "not loaded yet" and "not an editor at all" arrive as the same
        # answer; only the timeout tells them apart, so it has to keep asking.
        d = self.drive("--post", GOOD_ID, rules={
            "eval:identify.js": '{"err":"no Medium editor on this page"}'})
        self.assertEqual(d.out.returncode, EX_UNAVAILABLE, d.out.stderr)
        self.assertIn("no Medium editor at https://medium.com/p/%s/edit" % GOOD_ID,
                      d.out.stderr)
        self.assertEqual(d.calls.count("eval identify.js"), self.timeout(), d.calls)
        self.assertNotIn("eval title.js", d.calls)

    def test_an_editor_still_filling_up_is_polled_rather_than_pasted_over(self):
        # THE reason the poll asks twice. identify answers as soon as the shell
        # and the title graf exist, which on a 149-graf post is true while the
        # body is still streaming in. Breaking on the first answer meant the
        # refill selected the handful of grafs that had arrived and left the
        # other 140 and every old figure standing under the new body — and the
        # first upload wait then timed out counting 19 figures, blaming the
        # network. The counts were already in the reply, unused.
        growing = ['{"match":true,"want":"T","got":"T",'
                   '"url":"https://medium.com/p/%s/edit","grafs":%d,"figures":0}'
                   % (GOOD_ID, n) for n in range(6, 6 + self.timeout() + 1)]
        d = self.drive("--post", GOOD_ID, rules={"eval:identify.js": growing})
        self.assertEqual(d.out.returncode, EX_UNAVAILABLE, d.out.stderr)
        self.assertIn("still growing", d.out.stderr)
        self.assertNotIn("eval body.js", d.calls)
        # It settles as soon as two consecutive reads agree, and does not wait
        # out the whole timeout to do it.
        steady = growing[:3] + ['{"match":true,"want":"T","got":"T",'
                                '"url":"https://medium.com/p/%s/edit",'
                                '"grafs":149,"figures":14}' % GOOD_ID]
        d = self.drive("--post", GOOD_ID, rules={"eval:identify.js": steady})
        self.assertIn("eval body.js", d.calls)
        self.assertLess(d.calls.count("eval identify.js"), self.timeout(), d.calls)

    def test_a_browse_that_stops_answering_is_a_tempfail_not_a_bad_post(self):
        # `|| id_result=""` threw the diagnosis away and reported every one of
        # these as "no Medium editor at /p/<id>/edit", sending the operator to
        # check an id that was fine. A dead browser is worth retrying; a post
        # that is not yours is not, and the exit codes have to say which.
        d = self.drive("--post", GOOD_ID, rules={"eval:identify.js": "!fail"})
        self.assertEqual(d.out.returncode, EX_TEMPFAIL, d.out.stderr)
        self.assertIn("browse could not read the editor", d.out.stderr)
        self.assertIn("this is the browser, not the post", d.out.stderr)

    def test_post_mode_pastes_refill_and_a_new_draft_pastes_body(self):
        # The one snippet that differs between the modes, and the reason it
        # does: refill takes the old figures out with the old prose, and
        # running it on a new story would be pointless — running body on an
        # existing post would leave 14 orphaned figures behind.
        payload = md2medium.convert(PASTE_BODY)
        post = self.drive("--post", GOOD_ID)
        self.assertEqual(post.js("body.js").strip(), medium_js.refill_js(payload).strip())
        fresh = self.drive()
        self.assertEqual(fresh.js("body.js").strip(), medium_js.body_js(payload).strip())

    def test_a_body_paste_that_took_the_title_stops_with_nothing_uploaded(self):
        # refill reports the title it can still see afterwards, folded against
        # the payload's. Not "is it empty": `graf--title` is assigned by
        # position, so a selection that reached over the title leaves the first
        # pasted paragraph promoted to title — non-empty, and the old guard
        # waved it through to 18 uploads and a block 0 mismatch at the end.
        d = self.drive("--post", GOOD_ID, rules={
            "eval:body.js": '{"replaced":149,"figuresBefore":14,"figuresLeft":0,'
                            '"title":"This series opens with...","titleOk":false}'})
        self.assertEqual(d.out.returncode, EX_UNAVAILABLE, d.out.stderr)
        self.assertIn("the title is not this pack's after the body paste", d.out.stderr)
        self.assertEqual([c for c in d.calls if c.startswith("press")], [], d.calls)
        self.assertNotIn("eval image.js", d.calls)

    def test_old_figures_left_behind_stop_the_run_before_any_upload(self):
        # The assumption the whole mode rests on: the range took the old
        # figures out with the old prose. It had never been checked — the
        # number reported was the count from BEFORE the paste, so it said
        # "14 removed" either way — and everything downstream counts figures up
        # from zero. One survivor turned the first upload wait into a 40s
        # timeout that named the image and blamed the network.
        d = self.drive("--post", GOOD_ID, rules={
            "eval:body.js": '{"replaced":149,"figuresBefore":14,"figuresLeft":1,'
                            '"title":"T","titleOk":true}'})
        self.assertEqual(d.out.returncode, EX_UNAVAILABLE, d.out.stderr)
        self.assertIn("the refill left old figures behind", d.out.stderr)
        self.assertNotIn("eval image.js", d.calls)
        self.assertEqual([c for c in d.calls if c.startswith("press")], [], d.calls)

    def test_a_refusal_from_refill_stops_the_run(self):
        # refill_js refuses rather than pastes when the title graf is not where
        # it expects — the case that exists because pasting anyway would put
        # the whole body on top of the title. (That every refusal it can emit
        # is shaped like this one is checked in TestRefillSnippet.)
        d = self.drive("--post", GOOD_ID, rules={
            "eval:body.js": '{"err":"the title is not above the body"}'})
        self.assertEqual(d.out.returncode, EX_UNAVAILABLE, d.out.stderr)
        self.assertIn("the body paste found nothing to replace", d.out.stderr)
        self.assertNotIn("eval image.js", d.calls)

    def test_an_editor_that_never_settles_after_the_paste_stops_the_run(self):
        # The old fixed `sleep 3` was tuned on a new story. A refill has just
        # deleted 149 grafs and 14 figures and pasted 149 back, and the next
        # thing it did was look for a placeholder — "no placeholder for
        # diagram-01.png" on a published post whose body was already gone.
        d = self.drive("--post", GOOD_ID, packs={"": True},
                       paste=PASTE_WITH_FIGURE, images=["a.png"],
                       rules={"eval:body.js": REFILL_OK,
                              "eval:state.js": state(figures=0, slots=0)})
        self.assertEqual(d.out.returncode, EX_UNAVAILABLE, d.out.stderr)
        self.assertIn("did not settle", d.out.stderr)
        self.assertIn("wanted 0 figures and 1 placeholders", d.out.stderr)
        self.assertNotIn("eval image.js", d.calls)

    def test_a_failure_after_the_body_paste_says_the_post_is_half_replaced(self):
        # "The run failed, so it did nothing" is the wrong conclusion and the
        # natural one. Medium autosaves: the new body is already stored, and a
        # scheduled post publishes what is stored, placeholders and all.
        d = self.drive("--post", GOOD_ID, paste=PASTE_WITH_FIGURE, images=["a.png"],
                       rules={"eval:body.js": REFILL_OK,
                              "eval:state.js": state(figures=0, slots=0)})
        self.assertNotEqual(d.out.returncode, 0)
        self.assertIn("did NOT leave that post alone", d.out.stderr)
        self.assertIn("IMGSLOT", d.out.stderr)              # what would publish
        self.assertIn("scheduled:", d.out.stderr)
        self.assertIn("published:", d.out.stderr)
        self.assertIn("--post %s" % GOOD_ID, d.out.stderr)  # the re-run command

    def test_a_failure_before_the_body_paste_does_not(self):
        # The other half of the same guard: nothing was written, so saying the
        # post is half replaced would send someone to check a post that is
        # untouched — and would be noise on every id typo.
        d = self.drive("--post", GOOD_ID, rules={
            "eval:body.js": '{"err":"the title is not above the body"}'})
        self.assertNotIn("did NOT leave that post alone", d.out.stderr)

    def test_a_new_draft_never_says_it_is_half_replaced(self):
        d = self.drive(rules={"eval:body.js": '{"err":"no body grafs"}'})
        self.assertNotIn("did NOT leave that post alone", d.out.stderr)


class TestMediumDraftFinishes(Driven, unittest.TestCase):
    """A whole run, both modes, through every gate to the closing message.

    The guard tests above each stop the driver somewhere; nothing was checking
    that a run which should succeed does, which is how a gate that can only
    fail gets shipped. These drive to the end and read what comes out.
    """

    def test_an_article_with_no_figures_runs_to_the_end(self):
        # `TOTAL_IMAGES=$(grep -c . images.txt)`: grep prints 0 and exits 1 on
        # an empty file, and under `set -e` the assignment alone ended the run
        # right there — after the body was replaced, with no message at all.
        # Sixteen articles all have figures, so nothing hit it; --post makes
        # "refill a plain-text post" an ordinary thing to ask for.
        d = self.drive("--post", GOOD_ID, rules={
            "eval:body.js": REFILL_OK,
            "eval:state.js": state(figures=0, slots=0),
            "eval:dump.js": self.editor(["T", "body"], ["H3", "P"])})
        self.assertEqual(d.out.returncode, 0, d.out.stderr + d.out.stdout)
        self.assertIn("all blocks match", d.out.stdout)
        self.assertIn("post ready", d.out.stdout)
        self.assertNotIn("did NOT leave that post alone", d.out.stderr)
        self.assertEqual([c for c in d.calls if c.startswith("eval image")], [])

    def test_a_figure_is_inserted_confirmed_and_verified(self):
        # The whole image loop: paste, wait for the upload, select the
        # placeholder, two Backspaces, count what is left, and the final gate.
        d = self.drive("--post", GOOD_ID, paste=PASTE_WITH_FIGURE, images=["a.png"],
                       rules={
            "eval:body.js": REFILL_OK,
            "eval:state.js": [state(figures=0, slots=1),      # settled, slot there
                              state(figures=1, slots=1),      # uploaded
                              state(figures=1, slots=0)],     # placeholder gone
            "eval:image.js": '{"name":"a.png","bytes":8}',
            "eval:slot.js": '{"selected":"IMGSLOT-a.png-ENDSLOT"}',
            "eval:dump.js": self.editor(["T", "body"], ["H3", "P", "FIGURE"])})
        self.assertEqual(d.out.returncode, 0, d.out.stderr + d.out.stdout)
        self.assertEqual(d.calls.count("eval image.js"), 1, d.calls)
        self.assertEqual(d.calls.count("press Backspace"), 2, d.calls)
        self.assertIn("figures: 1, each in its own slot", d.out.stdout)
        self.assertIn("post ready", d.out.stdout)

    def test_a_new_draft_runs_to_the_end_too(self):
        # The same pipeline with no post: the mode must not have grown a step
        # that only works when there is an id.
        d = self.drive(rules={
            "eval:body.js": '{"replaced":2}',
            "eval:state.js": state(figures=0, slots=0),
            "eval:dump.js": self.editor(["T", "body"], ["H3", "P"])})
        self.assertEqual(d.out.returncode, 0, d.out.stderr + d.out.stdout)
        self.assertIn("draft ready", d.out.stdout)
        self.assertIn("Publish dialog", d.out.stdout)

    def test_a_leftover_section_divider_fails_the_run(self):
        # A <hr> is not a .graf and carries no text, so the block diff and the
        # figure-placement check are both blind to one. A refill's range runs
        # across every section in the article, and a divider left orphaned at
        # either end of it would otherwise ship with every gate reporting a
        # match. The payload here asks for none, so one is one too many.
        d = self.drive("--post", GOOD_ID, rules={
            "eval:body.js": REFILL_OK,
            "eval:state.js": state(figures=0, slots=0),
            "eval:dump.js": self.editor(["T", "body"], ["H3", "P"], dividers=1)})
        self.assertNotEqual(d.out.returncode, 0)
        self.assertIn("dividers: expected 0 section breaks, editor has 1", d.out.stdout)
        # And what state that leaves the post in, including the fact that a
        # failure at the verification step is the one that must NOT be met by
        # running the whole refill again.
        self.assertIn("did NOT leave that post alone", d.out.stderr)
        self.assertIn("re-running is\n   not the fix", d.out.stderr)

    def test_the_dividers_the_payload_asks_for_are_counted_and_passed(self):
        # The mirror: an article with a rule in it needs that many dividers,
        # and a run that has them says so rather than staying silent.
        paste = "# T\n\nbody\n\n---\n\nmore\n"
        d = self.drive("--post", GOOD_ID, paste=paste, rules={
            "eval:body.js": REFILL_OK,
            "eval:state.js": state(figures=0, slots=0),
            "eval:dump.js": self.editor(["T", "body", "more"], ["H3", "P", "P"], dividers=1)})
        self.assertEqual(d.out.returncode, 0, d.out.stderr + d.out.stdout)
        self.assertIn("dividers: 1, all accounted for", d.out.stdout)

    def test_a_placeholder_left_in_the_text_fails_the_final_gate(self):
        d = self.drive("--post", GOOD_ID, paste=PASTE_WITH_FIGURE, images=["a.png"],
                       rules={
            "eval:body.js": REFILL_OK,
            "eval:state.js": [state(figures=0, slots=1),
                              state(figures=1, slots=1),
                              state(figures=1, slots=0),
                              state(figures=1, slots=1)],   # one crept back in
            "eval:image.js": '{"name":"a.png","bytes":8}',
            "eval:slot.js": '{"selected":"IMGSLOT-a.png-ENDSLOT"}',
            "eval:dump.js": self.editor(["T", "body"], ["H3", "P", "FIGURE"])})
        self.assertNotEqual(d.out.returncode, 0)
        self.assertIn("placeholder text left in the post", d.out.stderr)


class TestMediumStoredIt(Driven, unittest.TestCase):
    """The reload pass. Every one of these shipped broken once.

    The in-editor checks passed on 16 posts in a row and 13 of them came back
    from a reload with figures missing and IMGSLOT text in the stored copy.
    Medium autosaves asynchronously; the batch navigated to the next post as
    soon as "all blocks match" printed, and the write never finished. Nothing
    before this class could see that, because everything before it reads the
    DOM the browser is holding rather than what the server kept.
    """

    def refill(self, **rules):
        base = {"eval:body.js": REFILL_OK,
                "eval:state.js": state(figures=0, slots=0),
                "eval:dump.js": self.editor(["T", "body"], ["H3", "P"])}
        base.update(rules)
        return self.drive("--post", GOOD_ID, paste="# T\n\nbody\n", rules=base)

    def test_a_save_that_never_finishes_is_not_reported_as_ready(self):
        d = self.refill(**{"eval:saved.js": '{"message":"Saving"}'})
        self.assertNotEqual(d.out.returncode, 0)
        self.assertIn("never reported the post saved", d.out.stderr)
        self.assertNotIn("post ready", d.out.stdout)

    def test_a_concurrent_editor_is_reported_verbatim_and_stops_the_run(self):
        # The message that actually appeared. The fix is to close the other
        # editor, which the driver cannot do, so it must not swallow it.
        medium = "Saving failed because someone is also editing. Reload to see their changes."
        d = self.refill(**{"eval:saved.js": '{"message":"%s"}' % medium})
        self.assertNotEqual(d.out.returncode, 0)
        self.assertIn("also editing", d.out.stderr)

    def test_figures_lost_in_the_save_fail_after_the_reload(self):
        # The exact shape of the incident: the editor agrees, the reload does
        # not. Two figures short of the one this article asks for.
        d = self.drive("--post", GOOD_ID, paste=PASTE_WITH_FIGURE, images=["a.png"],
                       rules={
            "eval:body.js": REFILL_OK,
            "eval:state.js": [state(figures=0, slots=1),
                              state(figures=1, slots=1),
                              state(figures=1, slots=0),
                              state(figures=1, slots=0),   # the in-editor gate
                              state(figures=0, slots=0)],  # what came back
            "eval:image.js": '{"name":"a.png","bytes":8}',
            "eval:slot.js": '{"selected":"IMGSLOT-a.png-ENDSLOT"}',
            "eval:dump.js": self.editor(["T", "body"], ["H3", "P", "FIGURE"])})
        self.assertNotEqual(d.out.returncode, 0)
        self.assertIn("Medium stored a post with the wrong figure count", d.out.stderr)
        self.assertIn("the save is what lost them", d.out.stderr)

    def test_placeholders_that_survived_the_save_fail_after_the_reload(self):
        d = self.drive("--post", GOOD_ID, paste=PASTE_WITH_FIGURE, images=["a.png"],
                       rules={
            "eval:body.js": REFILL_OK,
            "eval:state.js": [state(figures=0, slots=1),
                              state(figures=1, slots=1),
                              state(figures=1, slots=0),
                              state(figures=1, slots=0),
                              state(figures=1, slots=1)],   # IMGSLOT text stored
            "eval:image.js": '{"name":"a.png","bytes":8}',
            "eval:slot.js": '{"selected":"IMGSLOT-a.png-ENDSLOT"}',
            "eval:dump.js": self.editor(["T", "body"], ["H3", "P", "FIGURE"])})
        self.assertNotEqual(d.out.returncode, 0)
        self.assertIn("Medium stored placeholder text", d.out.stderr)

    def test_the_page_is_actually_reloaded_before_it_is_believed(self):
        # Without the goto this whole class is theatre: the same live DOM would
        # answer the second round of checks and agree with itself every time.
        d = self.refill()
        self.assertEqual(d.out.returncode, 0, d.out.stderr + d.out.stdout)
        edits = [g for g in self.gotos(d) if GOOD_ID in g]
        self.assertGreaterEqual(len(edits), 2, self.gotos(d))


class TestCodeBlocksAreNotTypographyFolded(unittest.TestCase):
    """Medium applies no typography inside a <pre>, so folding there can only hide.

    The folds exist to stop Medium's own rewrites reading as paste failures.
    Inside a code block Medium makes no such rewrite (that is why a CJK `——`
    survives there), so a curled quote in a shipped snippet is real corruption —
    and a syntax error for whoever copies it.
    """

    def test_prose_still_folds_curly_quotes(self):
        self.assertEqual(verify_draft.normalise('say "hi"', False),
                         verify_draft.normalise("say \u201chi\u201d", False))

    def test_a_code_block_does_not_fold_curly_quotes(self):
        self.assertNotEqual(verify_draft.normalise('say "hi"', False, True),
                            verify_draft.normalise("say \u201chi\u201d", False, True))

    def test_a_code_block_does_not_fold_em_dash_spacing(self):
        self.assertNotEqual(verify_draft.normalise("a \u2014 b", False, True),
                            verify_draft.normalise("a\u2014b", False, True))

    def test_a_code_block_still_loses_the_language_label(self):
        # That label is Medium chrome, not content, and it appears in <pre> too.
        self.assertEqual(verify_draft.normalise("x\nAuto (Bash)", False, True), "x")


class TestArticleAndPasteStayInLockstep(unittest.TestCase):
    """article*.md is the source; medium-paste.md is generated from it.

    Every ledger states that invariant, and this whole branch was link edits
    that had to be applied to BOTH copies of eight files by hand. Nothing
    checked it, so a one-sided edit would ship a live post whose links disagree
    with the repo — which already happened once.
    """

    HREF = re.compile(r"\]\((https?://[^)]+|\.\./[^)]+)\)")

    def pairs(self):
        found = []
        for article in sorted(glob.glob(os.path.join(REPO, "*/article*.md"))):
            lang = ".en" if article.endswith("article.en.md") else ""
            pack = os.path.join(os.path.dirname(article), "publish", "en" if lang else "")
            paste = os.path.join(pack, "medium-paste.md")
            if os.path.exists(paste):
                found.append((article, paste))
        return found

    def body(self, path):
        """The paste file minus its leading <!-- checklist --> header."""
        with open(path, encoding="utf-8") as fh:
            text = fh.read()
        if text.lstrip().startswith("<!--"):
            text = text[text.index("-->") + 3:]
        return text

    def test_there_are_pairs_to_check(self):
        # A glob that matched nothing would make every assertion below vacuous.
        self.assertGreaterEqual(len(self.pairs()), 8)

    def test_every_pair_carries_the_same_links(self):
        for article, paste in self.pairs():
            a = sorted(self.HREF.findall(self.body(article)))
            p = sorted(self.HREF.findall(self.body(paste)))
            self.assertEqual(a, p, "%s and its paste file disagree on links"
                             % os.path.relpath(article, REPO))

    def test_every_pair_agrees_on_what_is_still_unpublished(self):
        for article, paste in self.pairs():
            for marker in ("(coming soon)", "\uff08\u5373\u5c07\u767c\u5e03\uff09"):
                self.assertEqual(self.body(article).count(marker),
                                 self.body(paste).count(marker),
                                 "%s: %s count differs from its paste file"
                                 % (os.path.relpath(article, REPO), marker))


if __name__ == "__main__":
    unittest.main(verbosity=2)
