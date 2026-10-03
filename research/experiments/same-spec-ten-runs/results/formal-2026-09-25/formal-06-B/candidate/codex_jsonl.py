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
    6  a structurally malformed event arrived (see the per-line diagnostics)
"""
import json
import sys


_MISSING = object()


class _Malformed(Exception):
    """Raised while validating one event; carries a one-line reason."""


def _one_line(text):
    text = " ".join(str(text).split())
    return text or "malformed event"


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


def _is_count(value):
    return isinstance(value, int) and not isinstance(value, bool) and value >= 0


def _optional_text(obj, key, where):
    """Return a nonempty string, or None for missing/null/empty; raise if wrong type."""
    value = obj.get(key, _MISSING)
    if value is _MISSING or value is None:
        return None
    if not isinstance(value, str):
        raise _Malformed("%s.%s must be a string, got %s" % (where, key, _type_name(value)))
    if value == "":
        return None
    return value


class _State(object):
    def __init__(self):
        self.done = 0
        self.spoke = 0
        self.failed = False
        self.malformed = False

    def report_malformed(self, lineno, reason):
        self.malformed = True
        print("[codex malformed event] line %d: %s" % (lineno, _one_line(reason)),
              file=sys.stderr, flush=True)


def _handle_item(obj):
    item = obj.get("item", _MISSING)
    if item is _MISSING:
        return
    if not isinstance(item, dict):
        raise _Malformed("item must be an object, got %s" % _type_name(item))
    itype = item.get("type", _MISSING)
    if itype is _MISSING:
        return
    if not isinstance(itype, str):
        raise _Malformed("item.type must be a string, got %s" % _type_name(itype))
    if itype == "agent_message":
        text = _optional_text(item, "text", "item")
        if text is not None:
            print(text, flush=True)
            return "spoke"
    elif itype == "command_execution":
        command = _optional_text(item, "command", "item")
        if command is not None:
            print("<!-- codex ran: %s -->" % command[:160], flush=True)
    elif itype == "error":
        message = _optional_text(item, "message", "item")
        if message is not None:
            print("[codex item error] " + message, file=sys.stderr, flush=True)
    return None


def _handle_turn_completed(obj):
    usage = obj.get("usage", _MISSING)
    if usage is _MISSING:
        usage = {}
    if not isinstance(usage, dict):
        raise _Malformed("usage must be an object, got %s" % _type_name(usage))
    counts = []
    problems = []
    for key in ("input_tokens", "output_tokens"):
        value = usage.get(key, _MISSING)
        if value is _MISSING:
            counts.append(0)
        elif _is_count(value):
            counts.append(value)
        else:
            if isinstance(value, int) and not isinstance(value, bool):
                problems.append("usage.%s must be a non-negative integer, got a negative value" % key)
            else:
                problems.append("usage.%s must be a non-negative integer, got %s"
                                % (key, _type_name(value)))
            counts.append(None)
    if problems:
        raise _Malformed("; ".join(problems))
    print("\n<!-- tokens: in %d out %d -->" % (counts[0], counts[1]), flush=True)


def _handle_turn_failed(obj, state, lineno):
    state.failed = True
    msg = "no message"
    reason = None
    error = obj.get("error", _MISSING)
    if error is _MISSING or error is None:
        pass
    elif isinstance(error, dict):
        message = error.get("message", _MISSING)
        if message is _MISSING or message is None:
            pass
        elif isinstance(message, str):
            if message != "":
                msg = message
        else:
            reason = "error.message must be a string, got %s" % _type_name(message)
    else:
        reason = "error must be an object, got %s" % _type_name(error)
    if reason is not None:
        state.report_malformed(lineno, reason)
    print("[codex turn FAILED] " + msg, file=sys.stderr, flush=True)


def _process_line(raw, lineno, state):
    line = raw.strip()
    if not line:
        return
    try:
        obj = json.loads(line)
    except (ValueError, RecursionError):
        return
    if not isinstance(obj, dict):
        state.report_malformed(lineno, "event must be a JSON object, got %s" % _type_name(obj))
        return
    t = obj.get("type", _MISSING)
    if t is _MISSING:
        return
    if not isinstance(t, str):
        state.report_malformed(lineno, "type must be a string, got %s" % _type_name(t))
        return
    try:
        if t == "item.completed":
            if _handle_item(obj) == "spoke":
                state.spoke += 1
        elif t == "error":
            state.failed = True
            print("[codex error] " + str(obj.get("message", "")), file=sys.stderr, flush=True)
        elif t == "turn.completed":
            _handle_turn_completed(obj)
            state.done += 1
        elif t == "turn.failed":
            _handle_turn_failed(obj, state, lineno)
    except _Malformed as exc:
        state.report_malformed(lineno, str(exc))


def _configure_streams():
    # The stream is UTF-8 whatever the locale says; a C locale would otherwise
    # choke on the first CJK character in a review.
    settings = (
        (sys.stdin, "replace"),
        (sys.stdout, "replace"),
        (sys.stderr, "backslashreplace"),
    )
    for stream, errors in settings:
        if hasattr(stream, "reconfigure"):
            try:
                stream.reconfigure(encoding="utf-8", errors=errors)
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
        _process_line(raw, lineno, state)

    if state.failed:
        print("[codex] the turn failed (reason above); no review was produced.", file=sys.stderr, flush=True)
        sys.exit(3)
    if state.malformed:
        sys.exit(6)
    if state.done == 0:
        print("[codex] no turn.completed event: possible mid-stream disconnect.", file=sys.stderr, flush=True)
        sys.exit(4)
    if state.spoke == 0:
        print("[codex] the turn completed without an agent message; no review was produced.",
              file=sys.stderr, flush=True)
        sys.exit(5)


if __name__ == "__main__":
    main()
