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
    6  a structurally malformed event arrived (valid JSON with the wrong shape)
"""
import json
import sys


def _err(msg):
    print(msg, file=sys.stderr, flush=True)


def _out(msg):
    print(msg, flush=True)


def _is_token_count(v):
    return isinstance(v, int) and not isinstance(v, bool) and v >= 0


def main():
    # The stream is UTF-8 whatever the locale says; a C locale would otherwise
    # choke on the first CJK character in a review.
    if hasattr(sys.stdin, "reconfigure"):
        try:
            sys.stdin.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            try:
                stream.reconfigure(encoding="utf-8", errors="backslashreplace")
            except Exception:
                pass

    done = 0
    spoke = 0
    failed = False
    malformed = False

    def bad(lineno, reason):
        nonlocal malformed
        malformed = True
        reason = " ".join(str(reason).split()) or "malformed event"
        _err("[codex malformed event] line %d: %s" % (lineno, reason))

    lineno = 0
    while True:
        raw = sys.stdin.readline()
        if not raw:
            break
        lineno += 1
        line = raw.strip()
        if not line:
            continue
        try:
            obj = json.loads(line)
        except (ValueError, RecursionError):
            continue
        except Exception:
            continue

        if not isinstance(obj, dict):
            bad(lineno, "event is not a JSON object")
            continue
        if "type" not in obj:
            continue
        t = obj["type"]
        if not isinstance(t, str):
            bad(lineno, "event type is not a string")
            continue

        if t == "item.completed":
            item = obj.get("item", {})
            if not isinstance(item, dict):
                bad(lineno, "item.completed item is not an object")
                continue
            if "type" not in item:
                continue
            itype = item["type"]
            if not isinstance(itype, str):
                bad(lineno, "item type is not a string")
                continue
            if itype == "agent_message":
                text = item.get("text")
                if text is None or (isinstance(text, str) and text == ""):
                    continue
                if not isinstance(text, str):
                    bad(lineno, "agent_message text is not a string")
                    continue
                spoke += 1
                _out(text)
            elif itype == "command_execution":
                cmd = item.get("command")
                if cmd is None or (isinstance(cmd, str) and cmd == ""):
                    continue
                if not isinstance(cmd, str):
                    bad(lineno, "command_execution command is not a string")
                    continue
                _out("<!-- codex ran: %s -->" % (cmd[:160],))
            elif itype == "error":
                msg = item.get("message")
                if msg is None or (isinstance(msg, str) and msg == ""):
                    continue
                if not isinstance(msg, str):
                    bad(lineno, "item error message is not a string")
                    continue
                _err("[codex item error] " + msg)
            # unknown item types are ignored
        elif t == "error":
            failed = True
            _err("[codex error] " + str(obj.get("message", "")))
        elif t == "turn.completed":
            u = obj.get("usage", {})
            if not isinstance(u, dict):
                bad(lineno, "turn.completed usage is not an object")
                continue
            in_tok = u.get("input_tokens", 0)
            out_tok = u.get("output_tokens", 0)
            if not _is_token_count(in_tok):
                bad(lineno, "usage input_tokens is not a non-negative integer")
                continue
            if not _is_token_count(out_tok):
                bad(lineno, "usage output_tokens is not a non-negative integer")
                continue
            done += 1
            _out("\n<!-- tokens: in %d out %d -->" % (in_tok, out_tok))
        elif t == "turn.failed":
            failed = True
            msg = "no message"
            error = obj.get("error")
            if error is None:
                pass
            elif not isinstance(error, dict):
                bad(lineno, "turn.failed error is not an object")
            else:
                m = error.get("message")
                if m is None or (isinstance(m, str) and m == ""):
                    pass
                elif isinstance(m, str):
                    msg = m
                else:
                    bad(lineno, "turn.failed error message is not a string")
            _err("[codex turn FAILED] " + msg)
        # unknown event types are ignored

    if failed:
        _err("[codex] the turn failed (reason above); no review was produced.")
        sys.exit(3)
    if malformed:
        sys.exit(6)
    if done == 0:
        _err("[codex] no turn.completed event: possible mid-stream disconnect.")
        sys.exit(4)
    if spoke == 0:
        _err("[codex] the turn completed without an agent message; no review was produced.")
        sys.exit(5)
    sys.exit(0)


if __name__ == "__main__":
    main()
