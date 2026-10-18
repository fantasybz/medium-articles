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


class _State(object):
    def __init__(self):
        self.done = 0
        self.spoke = 0
        self.failed = False
        self.malformed = False


def _err(text):
    print(text, file=sys.stderr, flush=True)


def _malformed(state, lineno, reason):
    state.malformed = True
    reason = " ".join(str(reason).split()) or "malformed event"
    _err("[codex malformed event] line %d: %s" % (lineno, reason))


def _is_count(v):
    return isinstance(v, int) and not isinstance(v, bool) and v >= 0


def _handle_item(obj, lineno, state):
    if "item" not in obj:
        return
    item = obj["item"]
    if not isinstance(item, dict):
        _malformed(state, lineno, "item.completed 'item' is not an object")
        return
    if "type" not in item:
        return
    itype = item["type"]
    if not isinstance(itype, str):
        _malformed(state, lineno, "item 'type' is not a string")
        return
    if itype == "agent_message":
        text = item.get("text")
        if text is None:
            return
        if not isinstance(text, str):
            _malformed(state, lineno, "agent_message 'text' is not a string")
            return
        if text == "":
            return
        state.spoke += 1
        print(text, flush=True)
    elif itype == "command_execution":
        cmd = item.get("command")
        if cmd is None:
            return
        if not isinstance(cmd, str):
            _malformed(state, lineno, "command_execution 'command' is not a string")
            return
        if cmd == "":
            return
        print("<!-- codex ran: %s -->" % cmd[:160], flush=True)
    elif itype == "error":
        msg = item.get("message")
        if msg is None:
            return
        if not isinstance(msg, str):
            _malformed(state, lineno, "item error 'message' is not a string")
            return
        if msg == "":
            return
        _err("[codex item error] " + msg)
    # unknown string item types are ignored


def _handle_turn_completed(obj, lineno, state):
    if "usage" in obj:
        u = obj["usage"]
        if not isinstance(u, dict):
            _malformed(state, lineno, "turn.completed 'usage' is not an object")
            return
    else:
        u = {}
    values = []
    for key in ("input_tokens", "output_tokens"):
        if key in u:
            v = u[key]
            if not _is_count(v):
                _malformed(state, lineno, "usage '%s' is not a non-negative integer" % key)
                return
        else:
            v = 0
        values.append(v)
    state.done += 1
    print("\n<!-- tokens: in %d out %d -->" % (values[0], values[1]), flush=True)


def _handle_turn_failed(obj, lineno, state):
    state.failed = True
    msg = "no message"
    err = obj.get("error")
    if err is None:
        pass
    elif not isinstance(err, dict):
        _malformed(state, lineno, "turn.failed 'error' is not an object")
    else:
        m = err.get("message")
        if m is None or (isinstance(m, str) and m == ""):
            pass
        elif isinstance(m, str):
            msg = m
        else:
            _malformed(state, lineno, "turn.failed error 'message' is not a string")
    _err("[codex turn FAILED] " + msg)


def _handle(obj, lineno, state):
    if not isinstance(obj, dict):
        _malformed(state, lineno, "event is not a JSON object")
        return
    if "type" not in obj:
        return
    t = obj["type"]
    if not isinstance(t, str):
        _malformed(state, lineno, "event 'type' is not a string")
        return
    if t == "item.completed":
        _handle_item(obj, lineno, state)
    elif t == "error":
        state.failed = True
        try:
            m = str(obj.get("message", ""))
        except Exception:
            m = ""
        _err("[codex error] " + m)
    elif t == "turn.completed":
        _handle_turn_completed(obj, lineno, state)
    elif t == "turn.failed":
        _handle_turn_failed(obj, lineno, state)
    # unknown string event types are ignored


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

    state = _State()
    lineno = 0
    while True:
        raw = sys.stdin.readline()
        if raw == "":
            break
        lineno += 1
        line = raw.strip()
        if not line:
            continue
        try:
            obj = json.loads(line)
        except (ValueError, RecursionError):
            continue
        try:
            _handle(obj, lineno, state)
        except RecursionError:
            _malformed(state, lineno, "event could not be processed")

    if state.failed:
        _err("[codex] the turn failed (reason above); no review was produced.")
        sys.exit(3)
    if state.malformed:
        sys.exit(6)
    if state.done == 0:
        _err("[codex] no turn.completed event: possible mid-stream disconnect.")
        sys.exit(4)
    if state.spoke == 0:
        _err("[codex] the turn completed without an agent message; no review was produced.")
        sys.exit(5)
    sys.exit(0)


if __name__ == "__main__":
    main()
