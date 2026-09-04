#!/usr/bin/env python3
"""Tests for the publishing tools. Stdlib only, no network, no browser.

    python3 tools/test_tools.py

What these actually protect: the markdown conversion has mappings that are easy
to "clean up" and silently break (`###` must emit `<h4>`, blank lines inside a
code block must not stay blank), and the cookie filter has a regression that
already bit once. The browser-driving parts are not covered here — those need a
real Medium session, and `medium_draft.sh` verifies itself against the source
at the end of every run.
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
            "slot": medium_js.slot_js("a.png"),
            "image": medium_js.image_js(d.name, "a.png"),
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


class TestMediumDraftLangPack(unittest.TestCase):
    """Path resolution in medium_draft.sh, exercised without a browser.

    Every check here happens before the script touches `browse`, which is what
    makes it testable at all. The failure being guarded against is quiet: point
    the driver at a translated medium-paste.md while it still uploads
    publish/images and it ships the wrong figures, and every later gate —
    block diff, link count, figure-position check — still reports a match,
    because those compare against the payload, not against the language.
    """

    SCRIPT = os.path.join(TOOLS, "medium_draft.sh")

    def article(self, packs):
        """A throwaway repo root holding a copy of the driver and one article.

        The driver resolves paths from its OWN location (`dirname $0/..`), not
        from the cwd, so the copy has to live in the fake root or every path it
        builds would point back at the real repo.
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
                fh.write("# T\n\nbody\n")
            if has_images:
                os.makedirs(os.path.join(pub, "images"), exist_ok=True)
        return script, "2026-01-sample"

    def run_driver(self, script, *args):
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
                              env={**os.environ, "HOME": home.name})

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
            fh.write("# T\n\nbody\n")
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
