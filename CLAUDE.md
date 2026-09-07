# medium-articles

Long-form Medium articles, one folder per piece. See [README.md](README.md) for
the layout, [PUBLISHING.md](PUBLISHING.md) for how a post gets to Medium,
[MERMAID.md](MERMAID.md) for the diagram rules every figure is checked against,
and [research/README.md](research/README.md) for the monthly loop that picks the
next theme.

## Testing

```bash
python3 tools/test_tools.py
python3 -m unittest research/scripts/test_research_scripts.py
```

Stdlib `unittest`, no dependencies, no network, no browser. Covers the parts of
`tools/` that run without one: the markdown conversion, the draft verifier's
normalisation and figure-placement check, the cookie domain filter and v10
decryption, the generated browser snippets (both `medium_js.py` for new drafts
and `medium_patch.py` for edits to published posts), and each script's CLI
entry point. Two suites reach past the Python modules: `medium_draft.sh`'s
pre-flight (language-pack path resolution, the repo-boundary guard, the
sysexits codes) is exercised by running the script itself under an empty
`HOME`, so a regressed guard fails the test instead of reaching a browser; and
a repo-content scan keeps every `article*.md` in lockstep with the
`medium-paste.md` it generates, on both the link list and the count of
unpublished markers.

Everything past that pre-flight is deliberately not unit tested — it needs a
real logged-in Medium session. `tools/medium_draft.sh` covers itself instead: it
diffs the finished draft against the converted payload block by block, counts
links, checks each figure's position, and exits non-zero on any mismatch.

When adding a guard to the driver, capture the output first
(`out=$(B eval ...) || exit 1`) and test it. `if B eval ... | grep -q ...` can
never fire: browse writes failures to stderr with empty stdout, and a failing
left side makes the `if` false rather than true.

The second command covers `research/scripts/` the same way: stdlib `unittest`,
no network, no browser. It tests the pure-Python scripts — the
`article_to_paste.py` conversion, including a corpus check that every committed
`medium-paste.md` is exactly `convert()` of its article (body only: the
`<!-- -->` header of the older, hand-made pastes predates the script) and that
each `figures.json` still matches; `sync_figures.py`'s id matching; the
`codex_jsonl.py` parser whose exit codes `codex_review.sh` branches on;
`merge.py`; and the argument and Keychain guards of `notion_cookies.py`.
`codex_review.sh` gets the same treatment as `medium_draft.sh`: its pre-flight
runs against a throwaway git repo with a fake `codex` first on `PATH`, so the
missing-digest guard (exit 64 before Codex is called) and the happy path that
writes `codex-review-<slug>.md` are both covered without a Codex session. The
extractors, `collect.sh`, `mermaid_check*.sh` and `render_images.sh` need a
browser or the macOS Keychain, so they are not in it; like `medium_draft.sh`,
they check their own output at run time.

Expectations for changes in `tools/`, and for any `research/scripts/` code that
runs offline (the pure Python the second suite imports):

- New function gets a test. Bug fix gets a regression test that fails without
  the fix (the subdomain cookie filter and the duplicate `const` in a snippet
  are both there because they broke a real run).
- Assert on behaviour, never `assertIsNotNone`.
- Never commit code that makes existing tests fail.

## Article content

`article.md`, `article.en.md`, and the `publish/` and `publish/en/`
`medium-paste.md` generated from them are the author's prose. Fix the tooling
around them; do not reword the articles unless asked.

Two exceptions, both documentation rather than prose: the `<!-- ... -->`
publishing checklist at the top of each paste file (stripped before anything
reaches Medium, and stripped again before the lockstep comparison), and the
`publish/PUBLISHED.md` / `publish/en/PUBLISHED.md` ledgers. On a paste that
`research/scripts/article_to_paste.py` generated, the checklist is the script's
`HEADER` template and is rewritten on every run, so a change meant to last goes
in the script, not the file.

A link edit always lands in two files — the article and its paste file. Change
one and the lockstep test fails, which is the point.
