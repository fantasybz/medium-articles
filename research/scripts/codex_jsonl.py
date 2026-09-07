"""Stream-parse `codex exec --json` output: print the agent's messages as they complete.

Kept in its own file because embedding this in a bash single-quoted `python3 -c`
string broke on the escaped quotes (the first run of codex_review.sh died with a
SyntaxError, which closed the pipe and made codex panic on stdout).

Prints agent messages to stdout (they become the review file), and everything
diagnostic (`turn.failed`, `error` events, missing `turn.completed`) to stderr so
the caller can tell "Codex said nothing" from "Codex was refused".
"""
import json
import sys

done = 0
failed = False
for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    try:
        obj = json.loads(line)
    except ValueError:
        continue
    t = obj.get("type", "")
    if t == "item.completed":
        item = obj.get("item", {})
        itype = item.get("type", "")
        if itype == "agent_message" and item.get("text"):
            print(item["text"], flush=True)
        elif itype == "command_execution" and item.get("command"):
            print("<!-- codex ran: %s -->" % item["command"][:160], flush=True)
        elif itype == "error" and item.get("message"):
            print("[codex item error] " + item["message"], file=sys.stderr, flush=True)
    elif t == "error":
        failed = True
        print("[codex error] " + str(obj.get("message", "")), file=sys.stderr, flush=True)
    elif t == "turn.completed":
        done += 1
        u = obj.get("usage", {})
        print("\n<!-- tokens: in %s out %s -->" % (u.get("input_tokens", 0), u.get("output_tokens", 0)), flush=True)
    elif t == "turn.failed":
        failed = True
        msg = (obj.get("error") or {}).get("message", "") or "no message"
        print("[codex turn FAILED] " + msg, file=sys.stderr, flush=True)

if failed:
    print("[codex] the turn failed (reason above); no review was produced.", file=sys.stderr, flush=True)
    sys.exit(3)
if done == 0:
    print("[codex] no turn.completed event: possible mid-stream disconnect.", file=sys.stderr, flush=True)
    sys.exit(4)
