# medium-articles

Long-form Medium articles, one folder per piece. See [README.md](README.md) for
the layout and [PUBLISHING.md](PUBLISHING.md) for how a post gets to Medium.

## Testing

```bash
python3 tools/test_tools.py
```

Stdlib `unittest`, no dependencies, no network, no browser. Covers the parts of
`tools/` that run without one: the markdown conversion, the draft verifier's
normalisation and figure-placement check, the cookie domain filter and v10
decryption, the generated browser snippets (both `medium_js.py` for new drafts
and `medium_patch.py` for edits to published posts), and each script's CLI
entry point.

The browser-driving half is deliberately not unit tested — it needs a real
logged-in Medium session. `tools/medium_draft.sh` covers itself instead: it
diffs the finished draft against the converted payload block by block, counts
links, checks each figure's position, and exits non-zero on any mismatch.

When adding a guard to the driver, capture the output first
(`out=$(B eval ...) || exit 1`) and test it. `if B eval ... | grep -q ...` can
never fire: browse writes failures to stderr with empty stdout, and a failing
left side makes the `if` false rather than true.

Expectations for changes in `tools/`:

- New function gets a test. Bug fix gets a regression test that fails without
  the fix (the subdomain cookie filter and the duplicate `const` in a snippet
  are both there because they broke a real run).
- Assert on behaviour, never `assertIsNotNone`.
- Never commit code that makes existing tests fail.

## Article content

`article.md` and `publish/medium-paste.md` are the author's prose. Fix the
tooling around them; do not reword the articles unless asked.
