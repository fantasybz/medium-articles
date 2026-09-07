"""Merge one extractor batch into a collected JSON list, so overlapping scrolls do not duplicate.

    python3 research/scripts/merge.py OUT.json BATCH.json                   # posts, keyed by link
    python3 research/scripts/merge.py OUT.json BATCH.json --key handle      # accounts (x_following_users.json)
    python3 research/scripts/merge.py OUT.json BATCH.json --tag group:xyz   # stamp new items with t["source"]

Prints the resulting count; collect.sh reads it to notice when scrolling stops
yielding new items. The first copy of a key wins, so an item already collected
is never rewritten by a later scroll, and --tag never retags one.

A missing or empty OUT.json starts from nothing. An OUT.json that exists but is
not a JSON list is left untouched and the run fails: the alternative is to
overwrite a month of collection with one batch. A BATCH.json that is not a JSON
list (browse printed an error, or nothing) counts as an empty batch — the
extractor failing is routine, losing the store is not. The write goes through a
temp file and os.replace, so a crash mid-write leaves the old file whole.
"""
import argparse
import json
import os
import sys
import tempfile


def load_store(path, key):
    """key -> item for the collected file; fatal if the file exists and is not a list."""
    if not os.path.exists(path):
        return {}
    with open(path, encoding="utf-8") as fh:
        raw = fh.read()
    if not raw.strip():
        return {}
    try:
        items = json.loads(raw)
    except ValueError as e:
        sys.exit("%s is not JSON (%s); not touching it" % (path, e))
    if not isinstance(items, list):
        sys.exit("%s is not a JSON list (%s); not touching it" % (path, type(items).__name__))
    cur = {}
    for t in items:
        if isinstance(t, dict) and t.get(key) and t[key] not in cur:
            cur[t[key]] = t
    return cur


def load_batch(path):
    """The batch as a list; anything else is an empty batch, said on stderr."""
    try:
        with open(path, encoding="utf-8") as fh:
            raw = fh.read()
    except OSError as e:
        print("batch %s unreadable (%s); nothing merged" % (path, e), file=sys.stderr)
        return []
    if not raw.strip():
        return []
    try:
        items = json.loads(raw)
    except ValueError:
        print("batch %s is not JSON; nothing merged" % path, file=sys.stderr)
        return []
    if not isinstance(items, list):
        print("batch %s is not a JSON list (%s); nothing merged"
              % (path, type(items).__name__), file=sys.stderr)
        return []
    return items


def write_atomic(path, items):
    mode = os.stat(path).st_mode & 0o777 if os.path.exists(path) else 0o644
    fd, tmp = tempfile.mkstemp(prefix=os.path.basename(path) + ".", suffix=".tmp",
                               dir=os.path.dirname(os.path.abspath(path)))
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as fh:
            json.dump(items, fh, ensure_ascii=False, indent=1)
        os.chmod(tmp, mode)
        os.replace(tmp, path)
    except BaseException:
        try:
            os.unlink(tmp)
        except OSError:
            pass
        raise


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("store", help="the collected JSON list; created if missing")
    ap.add_argument("batch", help="one extractor run's JSON list")
    ap.add_argument("--key", choices=("link", "handle"), default="link",
                    help="field that identifies an item (default: link)")
    ap.add_argument("--tag", help="value for t['source'] on every item the batch adds")
    args = ap.parse_args()

    cur = load_store(args.store, args.key)
    for t in load_batch(args.batch):
        if not isinstance(t, dict) or not t.get(args.key):
            continue
        if t[args.key] in cur:
            continue
        if args.tag is not None:
            t["source"] = args.tag
        cur[t[args.key]] = t
    write_atomic(args.store, list(cur.values()))
    print(len(cur))


if __name__ == "__main__":
    main()
