"""Stream-parse `codex exec --json` output: print the agent's messages as they complete.

Kept in its own file because embedding this in a bash single-quoted `python3 -c`
string broke on the escaped quotes (the first run of codex_review.sh died with a
SyntaxError, which closed the pipe and made codex panic on stdout).

Prints agent messages to stdout (they become the review file), and everything
diagnostic (`turn.failed`, `error` events, missing `turn.completed`, malformed
events) to stderr so the caller can tell "Codex said nothing" from "Codex was
refused".

Exit codes codex_review.sh branches on:
    0  at least one agent message and a completed turn
    3  the turn failed or an error event arrived (refusal, usage limit)
    4  no turn.completed: a mid-stream disconnect
    5  the turn completed but Codex never spoke; the "review" would be a token count
    6  a valid-JSON event had the wrong shape (malformed event)
"""
import json
import sys


def _iter_lines():
    """Yield decoded physical lines from stdin as they arrive.

    Lines that are not valid UTF-8 are yielded as None (skipped like non-JSON).
    """
    stdin = sys.stdin
    buf = getattr(stdin, "buffer", None)
    if buf is not None:
        while True:
            raw = buf.readline()
            if not raw:
                break
            try:
                yield raw.decode("utf-8")
            except UnicodeDecodeError:
                yield None
    else:
        for line in stdin:
            yield line


def _is_token_count(v):
    return isinstance(v, int) and not isinstance(v, bool) and v >= 0


def main():
    # The stream is UTF-8 whatever the locale says; a C locale would otherwise
    # choke on the first CJK character in a review.
    for stream in (sys.stdin, sys.stdout):
        if hasattr(stream, "reconfigure"):
            try:
                stream.reconfigure(encoding="utf-8")
            except Exception:
                pass

    state = {"malformed": False}
    done = 0
    spoke = 0
    failed = False

    def malformed(lineno, reason):
        state["malformed"] = True
        print("[codex malformed event] line %d: %s" % (lineno, reason), file=sys.stderr, flush=True)

    lineno = 0
    for line in _iter_lines():
        lineno += 1
        if line is None:
            continue
        line = line.strip()
        if not line:
            continue
        try:
            obj = json.loads(line)
        except (ValueError, RecursionError):
            continue
        if not isinstance(obj, dict):
            malformed(lineno, "event is not a JSON object")
            continue
        if "type" not in obj:
            continue
        t = obj["type"]
        if not isinstance(t, str):
            malformed(lineno, "event type is not a string")
            continue

        if t == "item.completed":
            item = obj.get("item", {}) if "item" in obj else {}
            if not isinstance(item, dict):
                malformed(lineno, "item is not an object")
                continue
            if "type" not in item:
                continue
            itype = item["type"]
            if not isinstance(itype, str):
                malformed(lineno, "item type is not a string")
                continue
            if itype == "agent_message":
                text = item.get("text")
                if text is None:
                    continue
                if not isinstance(text, str):
                    malformed(lineno, "agent_message text is not a string")
                    continue
                if text == "":
                    continue
                spoke += 1
                print(text, flush=True)
            elif itype == "command_execution":
                cmd = item.get("command")
                if cmd is None:
                    continue
                if not isinstance(cmd, str):
                    malformed(lineno, "command_execution command is not a string")
                    continue
                if cmd == "":
                    continue
                print("<!-- codex ran: " + cmd[:160] + " -->", flush=True)
            elif itype == "error":
                msg = item.get("message")
                if msg is None:
                    continue
                if not isinstance(msg, str):
                    malformed(lineno, "item error message is not a string")
                    continue
                if msg == "":
                    continue
                print("[codex item error] " + msg, file=sys.stderr, flush=True)
        elif t == "error":
            failed = True
            print("[codex error] " + str(obj.get("message", "")), file=sys.stderr, flush=True)
        elif t == "turn.completed":
            u = obj.get("usage", {}) if "usage" in obj else {}
            if not isinstance(u, dict):
                malformed(lineno, "usage is not an object")
                continue
            bad = None
            for key in ("input_tokens", "output_tokens"):
                if key in u and not _is_token_count(u[key]):
                    bad = key
                    break
            if bad is not None:
                malformed(lineno, "usage %s is not a non-negative integer" % bad)
                continue
            done += 1
            print("\n<!-- tokens: in %d out %d -->" % (u.get("input_tokens", 0), u.get("output_tokens", 0)),
                  flush=True)
        elif t == "turn.failed":
            failed = True
            msg = "no message"
            err = obj.get("error")
            if err is None:
                pass
            elif not isinstance(err, dict):
                malformed(lineno, "turn.failed error is not an object")
            else:
                m = err.get("message")
                if m is None:
                    pass
                elif not isinstance(m, str):
                    malformed(lineno, "turn.failed error message is not a string")
                elif m != "":
                    msg = m
            print("[codex turn FAILED] " + msg, file=sys.stderr, flush=True)

    if failed:
        print("[codex] the turn failed (reason above); no review was produced.", file=sys.stderr, flush=True)
        sys.exit(3)
    if state["malformed"]:
        sys.exit(6)
    if done == 0:
        print("[codex] no turn.completed event: possible mid-stream disconnect.", file=sys.stderr, flush=True)
        sys.exit(4)
    if spoke == 0:
        print("[codex] the turn completed without an agent message; no review was produced.",
              file=sys.stderr, flush=True)
        sys.exit(5)
    sys.exit(0)


if __name__ == "__main__":
    main()
