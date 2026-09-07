"""Stream-parse `codex exec --json` output: print the agent's messages as they complete.

Kept in its own file because embedding this in a bash single-quoted `python3 -c`
string broke on the escaped quotes (the first run of codex_review.sh died with a
SyntaxError, which closed the pipe and made codex panic on stdout).

Prints agent messages to stdout (they become the review file), and everything
diagnostic (`turn.failed`, `error` events, missing `turn.completed`) to stderr so
the caller can tell "Codex said nothing" from "Codex was refused".

Exit codes codex_review.sh branches on:
    0  at least one agent message and a completed turn
    3  the turn failed or an error event arrived (refusal, usage limit)
    4  no turn.completed: a mid-stream disconnect
    5  the turn completed but Codex never spoke; the "review" would be a token count
"""
import json
import sys


def main():
    # The stream is UTF-8 whatever the locale says; a C locale would otherwise
    # choke on the first CJK character in a review.
    for stream in (sys.stdin, sys.stdout):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8")

    done = 0
    spoke = 0
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
                spoke += 1
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
    if spoke == 0:
        print("[codex] the turn completed without an agent message; no review was produced.",
              file=sys.stderr, flush=True)
        sys.exit(5)


if __name__ == "__main__":
    main()
