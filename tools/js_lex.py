#!/usr/bin/env python3
"""The one JS comment scanner both test suites use.

`browse eval` takes a JavaScript expression. The gstack browse build of 2026-09
prints nothing and exits 0 when a comment inside that expression contains an
apostrophe, so the failure arrives as an empty result rather than an error — on
2026-09-15 it reached us as a `json.load` traceback in collect.sh, three steps
downstream (notion_search.js said "the user's main Notion workspace").

Two suites hold files to that rule: research/scripts/test_research_scripts.py
for the extractors, tools/test_tools.py for the snippets medium_draft.sh and
medium_patch.py generate. The scanner lived in both and drifted immediately —
a lockstep test that compared only the function bodies passed while the two
copies disagreed about REGEX_MAY_FOLLOW, which is half the lexer. One module,
imported by both, has no drift surface to test.

Stdlib only, no I/O: CLAUDE.md's "no dependencies" rules out third-party,
network and browser, not an import from inside the repo.
"""

# `/` starts a regex literal only after a character that cannot END a value.
# Without this gate, `"10" / 2;  // don't` and `i++ / 2;  // don't` lex as a regex
# that runs to the `//`, so the scanner returns [] — "this file has no comments" —
# and the guard passes a file it should fail. No file in the repo divides today
# (30 regex literals, no division), so this is for the JS that gets written next,
# not a shape that has already broken a run.
REGEX_MAY_FOLLOW = set("(,=:[!&|?;{>") | {""}
# Punctuation is not the whole story: `return /re/` and `typeof /re/` are regexes
# after a WORD. Without these, `return /'/.test(s)` lexes as division and the
# apostrophe opens a phantom string that swallows the rest of the file — a silent
# miss, which is the one failure mode this module exists to prevent.
REGEX_MAY_FOLLOW_WORD = frozenset((
    "return", "typeof", "case", "in", "of", "new", "delete", "void",
    "yield", "await", "do", "else", "instanceof",
))


def comments(src):
    r"""Every comment in a JS source: `/* ... */` and `//` to end of line.

    Hand-scanned, not regexed. The two cheap regexes both fail on this corpus:
    `^\s*//` misses a trailing `const x = 1;  // don't`, the exact shape that
    broke the Notion step; and a bare `//.*$` calls the tail of a regex literal
    (`/\/posts\/|[^/]+/.test(h)`, extract_fb2.js:10) a comment. Blanking string
    literals first does not work either — the apostrophe this exists to catch
    would open a phantom string and swallow the rest of the file.

    An unterminated `/*` or regex literal raises rather than returning []: an
    empty list reads as "this file has no comments", which is exactly how a
    broken scanner passes its own guard. (An unterminated string can still close
    on a later quote and is indistinguishable here; JS rejects that file
    outright, so `browse eval` fails on it either way.)
    """
    out, i, n, prev, word = [], 0, len(src), "", ""
    while i < n:
        c = src[i]
        if c in "'\"`":                       # string literal: skip it whole,
            q, i = c, i + 1                   # so https:// inside one is not a comment
            while i < n and src[i] != q:
                i += 2 if src[i] == "\\" else 1
            if i >= n:
                raise ValueError("unterminated %s string" % q)
            i, prev, word = i + 1, ")", ""    # a string is a VALUE: a following / is division
        elif c == "/" and src[i + 1:i + 2] == "*":
            j = src.find("*/", i + 2)
            if j == -1:
                raise ValueError("unterminated /* comment")
            out.append(src[i:j + 2])
            i = j + 2                         # prev unchanged: a comment is not a token
        elif c == "/" and src[i + 1:i + 2] == "/":
            j = src.find("\n", i)
            j = n if j == -1 else j
            out.append(src[i:j])
            i = j                             # prev unchanged
        elif c == "/" and (prev in REGEX_MAY_FOLLOW or word in REGEX_MAY_FOLLOW_WORD):
            j, in_class = i + 1, False
            while j < n and src[j] != "\n":
                ch = src[j]
                if ch == "\\":
                    j += 2
                    continue
                if ch == "[":
                    in_class = True
                elif ch == "]":
                    in_class = False
                elif ch == "/" and not in_class:
                    break
                j += 1
            if j >= n or src[j] != "/":
                raise ValueError("unterminated regex literal")
            i, prev, word = j + 1, ")", ""
        else:
            if c.isalpha() or c == "_" or c == "$":
                word += c
            elif not c.isspace():
                word = ""
            if not c.isspace():
                prev = c
            i += 1
    return out
