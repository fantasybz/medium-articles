"""Stream-parse `codex exec --json` output: print the agent's messages as they complete.

Kept in its own file because embedding this in a bash single-quoted `python3 -c`
string broke on the escaped quotes (the first run of codex_review.sh died with a
SyntaxError, which closed the pipe and made codex panic on stdout).

Prints agent messages to stdout (they become the review file), and everything
diagnostic (`turn.failed`, `error` events, missing `turn.completed`, malformed
events) to stderr so the caller can tell "Codex said nothing" from "Codex was
refused".

Valid JSON whose structure is wrong (a non-object root, a non-string `type`, a
non-string agent text, a bad usage value, ...) is reported per line as
`[codex malformed event] line N: REASON` and dropped; processing continues.

Exit codes codex_review.sh branches on (first applicable wins):
    3  the turn failed or an error event arrived (refusal, usage limit)
    6  at least one malformed event was seen
    4  no valid turn.completed: a mid-stream disconnect
    5  the turn completed but Codex never spoke; the "review" would be a token count
    0  at least one agent message and a completed turn
"""
import json
import sys


_MISSING = object()


def _out(text):
    print(text, flush=True)


def _err(text):
    print(text, file=sys.stderr, flush=True)


def _type_name(value):
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


def _optional_text(obj, key):
    """Return (text_or_None, reason_or_None) for an optional string field.

    Missing, null and empty string all mean "no text". Any other non-string is
    malformed.
    """
    value = obj.get(key, _MISSING)
    if value is _MISSING or value is None:
        return None, None
    if not isinstance(value, str):
        return None, "%s must be a string, got %s" % (key, _type_name(value))
    if value == "":
        return None, None
    return value, None


def _token_count(usage, key):
    value = usage.get(key, _MISSING)
    if value is _MISSING:
        return 0, None
    if isinstance(value, bool) or not isinstance(value, int):
        return None, "usage.%s must be a non-negative integer, got %s" % (key, _type_name(value))
    if value < 0:
        return None, "usage.%s must be a non-negative integer, got a negative value" % key
    return value, None


def _safe_str(value):
    try:
        return str(value)
    except (RecursionError, ValueError):
        return "<unrepresentable message>"


class _State(object):
    def __init__(self):
        self.done = 0
        self.spoke = 0
        self.failed = False
        self.malformed = False

    def malformed_line(self, lineno, reason):
        self.malformed = True
        reason = " ".join(str(reason).split()) or "malformed event"
        _err("[codex malformed event] line %d: %s" % (lineno, reason))


def _handle_item_completed(state, obj, lineno):
    item = obj.get("item", _MISSING)
    if item is _MISSING:
        return
    if not isinstance(item, dict):
        state.malformed_line(lineno, "item must be an object, got %s" % _type_name(item))
        return
    itype = item.get("type", _MISSING)
    if itype is _MISSING:
        return
    if not isinstance(itype, str):
        state.malformed_line(lineno, "item.type must be a string, got %s" % _type_name(itype))
        return
    if itype == "agent_message":
        text, reason = _optional_text(item, "text")
        if reason is not None:
            state.malformed_line(lineno, "item." + reason)
            return
        if text is not None:
            state.spoke += 1
            _out(text)
    elif itype == "command_execution":
        command, reason = _optional_text(item, "command")
        if reason is not None:
            state.malformed_line(lineno, "item." + reason)
            return
        if command is not None:
            _out("<!-- codex ran: %s -->" % command[:160])
    elif itype == "error":
        message, reason = _optional_text(item, "message")
        if reason is not None:
            state.malformed_line(lineno, "item." + reason)
            return
        if message is not None:
            _err("[codex item error] " + message)
    # Unknown string item types are ignored without inspecting their payload.


def _handle_turn_completed(state, obj, lineno):
    usage = obj.get("usage", _MISSING)
    if usage is _MISSING:
        usage = {}
    if not isinstance(usage, dict):
        state.malformed_line(lineno, "usage must be an object, got %s" % _type_name(usage))
        return
    tin, reason_in = _token_count(usage, "input_tokens")
    tout, reason_out = _token_count(usage, "output_tokens")
    reasons = [r for r in (reason_in, reason_out) if r is not None]
    if reasons:
        state.malformed_line(lineno, "; ".join(reasons))
        return
    state.done += 1
    _out("\n<!-- tokens: in %d out %d -->" % (tin, tout))


def _handle_turn_failed(state, obj, lineno):
    state.failed = True
    msg = "no message"
    reason = None
    error = obj.get("error", _MISSING)
    if error is _MISSING or error is None:
        pass
    elif isinstance(error, dict):
        text, text_reason = _optional_text(error, "message")
        if text_reason is not None:
            reason = "error." + text_reason
        elif text is not None:
            msg = text
    else:
        reason = "error must be an object, got %s" % _type_name(error)
    if reason is not None:
        state.malformed_line(lineno, reason)
    _err("[codex turn FAILED] " + msg)


def _handle_error(state, obj, lineno):
    state.failed = True
    _err("[codex error] " + _safe_str(obj.get("message", "")))


_HANDLERS = {
    "item.completed": _handle_item_completed,
    "turn.completed": _handle_turn_completed,
    "turn.failed": _handle_turn_failed,
    "error": _handle_error,
}


def _reconfigure():
    # The stream is UTF-8 whatever the locale says; a C locale would otherwise
    # choke on the first CJK character in a review.
    for stream, errors in ((sys.stdin, "replace"),
                           (sys.stdout, "backslashreplace"),
                           (sys.stderr, "backslashreplace")):
        if hasattr(stream, "reconfigure"):
            try:
                stream.reconfigure(encoding="utf-8", errors=errors)
            except Exception:
                pass


def main():
    _reconfigure()

    state = _State()
    lineno = 0
    readline = sys.stdin.readline
    while True:
        raw = readline()
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
        if not isinstance(obj, dict):
            state.malformed_line(lineno, "event must be a JSON object, got %s" % _type_name(obj))
            continue
        t = obj.get("type", _MISSING)
        if t is _MISSING:
            continue
        if not isinstance(t, str):
            state.malformed_line(lineno, "type must be a string, got %s" % _type_name(t))
            continue
        handler = _HANDLERS.get(t)
        if handler is None:
            continue
        handler(state, obj, lineno)

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
