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
    """Raised when a decoded JSON event has a structurally wrong value."""


def _out(text):
    print(text, flush=True)


def _err(text):
    print(text, file=sys.stderr, flush=True)


def _malformed(lineno, reason):
    reason = " ".join(str(reason).split()) or "malformed event"
    _err("[codex malformed event] line %d: %s" % (lineno, reason))


def _optional_text(container, key, what):
    """Return a nonempty string, or None for missing/null/empty.

    Any other provided value raises _Malformed.
    """
    value = container.get(key, _MISSING)
    if value is _MISSING or value is None:
        return None
    if not isinstance(value, str):
        raise _Malformed("%s must be a string, got %s" % (what, type(value).__name__))
    if value == "":
        return None
    return value


def _token_count(usage, key):
    value = usage.get(key, _MISSING)
    if value is _MISSING:
        return 0
    if isinstance(value, bool) or not isinstance(value, int):
        raise _Malformed("usage.%s must be a non-negative integer, got %s"
                         % (key, type(value).__name__))
    if value < 0:
        raise _Malformed("usage.%s must be a non-negative integer, got a negative value" % key)
    return value


class _State(object):
    def __init__(self):
        self.done = 0
        self.spoke = 0
        self.failed = False
        self.malformed = False


def _handle_item_completed(obj):
    """Validate and emit an item.completed event. Returns spoken increment."""
    item = obj.get("item", _MISSING)
    if item is _MISSING:
        return 0
    if not isinstance(item, dict):
        raise _Malformed("item must be an object, got %s" % type(item).__name__)
    itype = item.get("type", _MISSING)
    if itype is _MISSING:
        return 0
    if not isinstance(itype, str):
        raise _Malformed("item.type must be a string, got %s" % type(itype).__name__)
    if itype == "agent_message":
        text = _optional_text(item, "text", "item.text")
        if text is None:
            return 0
        _out(text)
        return 1
    if itype == "command_execution":
        command = _optional_text(item, "command", "item.command")
        if command is not None:
            _out("<!-- codex ran: %s -->" % command[:160])
        return 0
    if itype == "error":
        message = _optional_text(item, "message", "item.message")
        if message is not None:
            _err("[codex item error] " + message)
        return 0
    return 0


def _handle_turn_completed(obj):
    usage = obj.get("usage", _MISSING)
    if usage is _MISSING:
        usage = {}
    if not isinstance(usage, dict):
        raise _Malformed("usage must be an object, got %s" % type(usage).__name__)
    problems = []
    counts = []
    for key in ("input_tokens", "output_tokens"):
        try:
            counts.append(_token_count(usage, key))
        except _Malformed as exc:
            problems.append(str(exc))
    if problems:
        raise _Malformed("; ".join(problems))
    _out("\n<!-- tokens: in %s out %s -->" % (counts[0], counts[1]))


def _turn_failed_message(obj):
    """Return (message, reason) where reason is None unless malformed."""
    error = obj.get("error", _MISSING)
    if error is _MISSING or error is None:
        return "no message", None
    if not isinstance(error, dict):
        return "no message", "error must be an object, got %s" % type(error).__name__
    try:
        message = _optional_text(error, "message", "error.message")
    except _Malformed as exc:
        return "no message", str(exc)
    if message is None:
        return "no message", None
    return message, None


def _process(obj, lineno, state):
    if not isinstance(obj, dict):
        state.malformed = True
        _malformed(lineno, "event must be a JSON object, got %s" % type(obj).__name__)
        return
    t = obj.get("type", _MISSING)
    if t is _MISSING:
        return
    if not isinstance(t, str):
        state.malformed = True
        _malformed(lineno, "type must be a string, got %s" % type(t).__name__)
        return

    if t == "item.completed":
        try:
            state.spoke += _handle_item_completed(obj)
        except _Malformed as exc:
            state.malformed = True
            _malformed(lineno, str(exc))
    elif t == "turn.completed":
        try:
            _handle_turn_completed(obj)
        except _Malformed as exc:
            state.malformed = True
            _malformed(lineno, str(exc))
        else:
            state.done += 1
    elif t == "turn.failed":
        state.failed = True
        message, reason = _turn_failed_message(obj)
        if reason is not None:
            state.malformed = True
            _malformed(lineno, reason)
        _err("[codex turn FAILED] " + message)
    elif t == "error":
        state.failed = True
        _err("[codex error] " + str(obj.get("message", "")))
    # Unknown string event types are ignored without inspecting their payload.


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
    for raw in iter(sys.stdin.readline, ""):
        lineno += 1
        line = raw.strip()
        if not line:
            continue
        try:
            obj = json.loads(line)
        except (ValueError, RecursionError):
            continue
        _process(obj, lineno, state)

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
