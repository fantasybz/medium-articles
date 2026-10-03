"""Stream-parse `codex exec --json` output: print the agent's messages as they complete.

Kept in its own file because embedding this in a bash single-quoted `python3 -c`
string broke on the escaped quotes (the first run of codex_review.sh died with a
SyntaxError, which closed the pipe and made codex panic on stdout).

Prints agent messages to stdout (they become the review file), and everything
diagnostic (`turn.failed`, `error` events, missing `turn.completed`, malformed
events) to stderr so the caller can tell "Codex said nothing" from "Codex was
refused".

Valid JSON whose shape is wrong (a non-object line, a non-string type, a
non-object item or usage, a non-string text, bad token counts, ...) is reported
per line as `[codex malformed event] line N: REASON` and then skipped; the read
loop keeps going so a later remote failure is still observed.

Exit codes codex_review.sh branches on:
    0  at least one agent message and a completed turn
    3  the turn failed or an error event arrived (refusal, usage limit)
    4  no turn.completed: a mid-stream disconnect
    5  the turn completed but Codex never spoke; the "review" would be a token count
    6  at least one malformed event (and no explicit failure)
"""
import json
import sys

_NO_MESSAGE = "no message"


class _Malformed(Exception):
    """Raised while validating one event; carries a single-line reason."""


def _kind(value):
    if value is None:
        return "null"
    if isinstance(value, bool):
        return "boolean"
    if isinstance(value, int):
        return "integer"
    if isinstance(value, float):
        return "number"
    if isinstance(value, str):
        return "string"
    if isinstance(value, list):
        return "array"
    if isinstance(value, dict):
        return "object"
    return type(value).__name__


def _is_token_count(value):
    return isinstance(value, int) and not isinstance(value, bool) and value >= 0


def _out(text):
    print(text, flush=True)


def _err(text):
    print(text, file=sys.stderr, flush=True)


def _report_malformed(lineno, reason):
    reason = " ".join(str(reason).split()) or "malformed event"
    _err("[codex malformed event] line %d: %s" % (lineno, reason))


def _optional_string(container, key, what):
    """Return a nonempty string, or None for absent/null/empty; raise on other types."""
    if key not in container:
        return None
    value = container[key]
    if value is None:
        return None
    if not isinstance(value, str):
        raise _Malformed("%s must be a string, got %s" % (what, _kind(value)))
    if value == "":
        return None
    return value


class _State(object):
    def __init__(self):
        self.done = 0
        self.spoke = 0
        self.failed = False
        self.malformed = False


def _handle_item_completed(obj, state):
    if "item" not in obj:
        return
    item = obj["item"]
    if not isinstance(item, dict):
        raise _Malformed("item must be an object, got %s" % _kind(item))
    if "type" not in item:
        return
    itype = item["type"]
    if not isinstance(itype, str):
        raise _Malformed("item.type must be a string, got %s" % _kind(itype))
    if itype == "agent_message":
        text = _optional_string(item, "text", "item.text")
        if text is not None:
            state.spoke += 1
            _out(text)
    elif itype == "command_execution":
        command = _optional_string(item, "command", "item.command")
        if command is not None:
            _out("<!-- codex ran: %s -->" % command[:160])
    elif itype == "error":
        message = _optional_string(item, "message", "item.message")
        if message is not None:
            _err("[codex item error] " + message)
    # Unknown string item types are ignored without inspecting their payload.


def _handle_turn_completed(obj, state):
    usage = obj.get("usage", {}) if "usage" in obj else {}
    if not isinstance(usage, dict):
        raise _Malformed("usage must be an object, got %s" % _kind(usage))
    problems = []
    counts = {}
    for key in ("input_tokens", "output_tokens"):
        if key not in usage:
            counts[key] = 0
            continue
        value = usage[key]
        if not _is_token_count(value):
            if isinstance(value, int) and not isinstance(value, bool):
                problems.append("usage.%s must be a non-negative integer, got negative integer" % key)
            else:
                problems.append("usage.%s must be a non-negative integer, got %s" % (key, _kind(value)))
            continue
        counts[key] = value
    if problems:
        raise _Malformed("; ".join(problems))
    state.done += 1
    _out("\n<!-- tokens: in %d out %d -->" % (counts["input_tokens"], counts["output_tokens"]))


def _handle_turn_failed(obj, state, lineno):
    state.failed = True
    msg = _NO_MESSAGE
    reason = None
    error = obj.get("error") if "error" in obj else None
    if error is None:
        pass
    elif isinstance(error, dict):
        try:
            value = _optional_string(error, "message", "error.message")
        except _Malformed as exc:
            reason = str(exc)
            value = None
        if value is not None:
            msg = value
    else:
        reason = "error must be an object, got %s" % _kind(error)
    if reason is not None:
        state.malformed = True
        _report_malformed(lineno, reason)
    _err("[codex turn FAILED] " + msg)


def _handle_line(obj, state, lineno):
    if not isinstance(obj, dict):
        raise _Malformed("event must be a JSON object, got %s" % _kind(obj))
    if "type" not in obj:
        return
    t = obj["type"]
    if not isinstance(t, str):
        raise _Malformed("type must be a string, got %s" % _kind(t))
    if t == "item.completed":
        _handle_item_completed(obj, state)
    elif t == "error":
        state.failed = True
        _err("[codex error] " + str(obj.get("message", "")))
    elif t == "turn.completed":
        _handle_turn_completed(obj, state)
    elif t == "turn.failed":
        _handle_turn_failed(obj, state, lineno)
    # Unknown string event types are ignored without inspecting their payload.


def _configure_streams():
    # The stream is UTF-8 whatever the locale says; a C locale would otherwise
    # choke on the first CJK character in a review.
    if hasattr(sys.stdin, "reconfigure"):
        try:
            sys.stdin.reconfigure(encoding="utf-8", errors="replace", newline="\n")
        except Exception:
            try:
                sys.stdin.reconfigure(encoding="utf-8", errors="replace")
            except Exception:
                pass
    if hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass
    if hasattr(sys.stderr, "reconfigure"):
        try:
            sys.stderr.reconfigure(encoding="utf-8", errors="backslashreplace")
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
        line = raw.strip()
        if not line:
            continue
        try:
            obj = json.loads(line)
        except (ValueError, RecursionError):
            continue
        try:
            _handle_line(obj, state, lineno)
        except _Malformed as exc:
            state.malformed = True
            _report_malformed(lineno, str(exc))
        except RecursionError:
            state.malformed = True
            _report_malformed(lineno, "event is too deeply nested")

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
