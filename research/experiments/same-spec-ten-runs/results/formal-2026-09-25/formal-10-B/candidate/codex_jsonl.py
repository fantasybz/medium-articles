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
    6  a structurally malformed event arrived (valid JSON of the wrong shape)
"""
import json
import sys


class _State(object):
    def __init__(self):
        self.done = 0
        self.spoke = 0
        self.failed = False
        self.malformed = False


class _Malformed(Exception):
    """Raised internally when an event has a structurally wrong field."""


def _out(text):
    print(text, file=sys.stdout, flush=True)


def _err(text):
    print(text, file=sys.stderr, flush=True)


def _single_line(text):
    return " ".join(str(text).splitlines()) or "malformed event"


def _report_malformed(state, lineno, reason):
    state.malformed = True
    _err("[codex malformed event] line %d: %s" % (lineno, _single_line(reason)))


def _tname(value):
    if value is None:
        return "null"
    if isinstance(value, bool):
        return "boolean"
    if isinstance(value, (int, float)):
        return "number"
    if isinstance(value, str):
        return "string"
    if isinstance(value, list):
        return "array"
    if isinstance(value, dict):
        return "object"
    return type(value).__name__


def _optional_text(container, key, what):
    """Return a nonempty string, or None for missing/null/empty; raise on wrong type."""
    if key not in container:
        return None
    value = container[key]
    if value is None:
        return None
    if not isinstance(value, str):
        raise _Malformed("%s must be a string, got %s" % (what, _tname(value)))
    if value == "":
        return None
    return value


def _token_count(usage, key):
    if key not in usage:
        return 0
    value = usage[key]
    if isinstance(value, bool) or not isinstance(value, int):
        raise _Malformed("usage.%s must be a non-negative integer, got %s" % (key, _tname(value)))
    if value < 0:
        raise _Malformed("usage.%s must be a non-negative integer, got a negative value" % key)
    return value


def _handle_item_completed(obj, state):
    if "item" not in obj:
        return
    item = obj["item"]
    if not isinstance(item, dict):
        raise _Malformed("item.completed item must be an object, got %s" % _tname(item))
    if "type" not in item:
        return
    itype = item["type"]
    if not isinstance(itype, str):
        raise _Malformed("item type must be a string, got %s" % _tname(itype))
    if itype == "agent_message":
        text = _optional_text(item, "text", "agent_message text")
        if text is not None:
            state.spoke += 1
            _out(text)
    elif itype == "command_execution":
        command = _optional_text(item, "command", "command_execution command")
        if command is not None:
            _out("<!-- codex ran: %s -->" % command[:160])
    elif itype == "error":
        message = _optional_text(item, "message", "error item message")
        if message is not None:
            _err("[codex item error] " + message)
    # Unknown string item types are ignored without inspecting their payload.


def _handle_turn_completed(obj, state):
    if "usage" in obj:
        usage = obj["usage"]
        if not isinstance(usage, dict):
            raise _Malformed("turn.completed usage must be an object, got %s" % _tname(usage))
    else:
        usage = {}
    reasons = []
    counts = []
    for key in ("input_tokens", "output_tokens"):
        try:
            counts.append(_token_count(usage, key))
        except _Malformed as exc:
            reasons.append(str(exc))
    if reasons:
        raise _Malformed("; ".join(reasons))
    state.done += 1
    _out("\n<!-- tokens: in %s out %s -->" % (counts[0], counts[1]))


def _handle_turn_failed(obj, state, lineno):
    state.failed = True
    msg = "no message"
    reason = None
    err = obj.get("error")
    if err is None:
        pass
    elif isinstance(err, dict):
        if "message" in err:
            m = err["message"]
            if m is None or m == "":
                pass
            elif isinstance(m, str):
                msg = m
            else:
                reason = "turn.failed error.message must be a string, got %s" % _tname(m)
    else:
        reason = "turn.failed error must be an object, got %s" % _tname(err)
    if reason is not None:
        _report_malformed(state, lineno, reason)
    _err("[codex turn FAILED] " + msg)


def _handle_line(raw, lineno, state):
    line = raw.strip()
    if not line:
        return
    try:
        obj = json.loads(line)
    except (ValueError, RecursionError):
        return
    try:
        if not isinstance(obj, dict):
            raise _Malformed("event must be a JSON object, got %s" % _tname(obj))
        if "type" not in obj:
            return
        t = obj["type"]
        if not isinstance(t, str):
            raise _Malformed("event type must be a string, got %s" % _tname(t))
        if t == "item.completed":
            _handle_item_completed(obj, state)
        elif t == "error":
            state.failed = True
            _err("[codex error] " + str(obj.get("message", "")))
        elif t == "turn.completed":
            _handle_turn_completed(obj, state)
        elif t == "turn.failed":
            _handle_turn_failed(obj, state, lineno)
        # Unknown string event types are ignored.
    except _Malformed as exc:
        _report_malformed(state, lineno, str(exc))


def _configure_streams():
    # The stream is UTF-8 whatever the locale says; a C locale would otherwise
    # choke on the first CJK character in a review.
    if hasattr(sys.stdin, "reconfigure"):
        try:
            sys.stdin.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            try:
                sys.stdin.reconfigure(encoding="utf-8")
            except Exception:
                pass
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            try:
                stream.reconfigure(encoding="utf-8", errors="backslashreplace")
            except Exception:
                try:
                    stream.reconfigure(encoding="utf-8")
                except Exception:
                    pass


def main():
    _configure_streams()

    state = _State()
    lineno = 0
    readline = sys.stdin.readline
    while True:
        raw = readline()
        if not raw:
            break
        lineno += 1
        _handle_line(raw, lineno, state)

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


if __name__ == "__main__":
    main()
