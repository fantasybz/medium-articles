"""Stream-parse `codex exec --json` output: print the agent's messages as they complete.

Kept in its own file because embedding this in a bash single-quoted `python3 -c`
string broke on the escaped quotes (the first run of codex_review.sh died with a
SyntaxError, which closed the pipe and made codex panic on stdout).

Prints agent messages to stdout (they become the review file), and everything
diagnostic (`turn.failed`, `error` events, missing `turn.completed`, malformed
events) to stderr so the caller can tell "Codex said nothing" from "Codex was
refused".

Valid JSON whose shape is wrong (a non-object event, a non-string type, a
non-string agent text, bad usage counts, ...) is reported per line as
`[codex malformed event] line N: REASON` and dropped; processing continues.

Exit codes codex_review.sh branches on:
    0  at least one agent message and a completed turn
    3  the turn failed or an error event arrived (refusal, usage limit)
    6  a malformed event was seen (and no explicit failure)
    4  no turn.completed: a mid-stream disconnect
    5  the turn completed but Codex never spoke; the "review" would be a token count
"""
import json
import sys


def _jtype(value):
    """Name the JSON type of a decoded value for diagnostics (single line)."""
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


class _State(object):
    def __init__(self):
        self.done = 0
        self.spoke = 0
        self.failed = False
        self.malformed = False


def _out(text):
    print(text, flush=True)


def _err(text):
    print(text, file=sys.stderr, flush=True)


def _malformed(state, lineno, reason):
    state.malformed = True
    reason = " ".join(str(reason).split()) or "malformed event"
    _err("[codex malformed event] line %d: %s" % (lineno, reason))


def _optional_text(container, key):
    """Return (text_or_None, reason_or_None) for an optional string field.

    Missing, null and empty string mean "no value"; any other non-string is
    malformed.
    """
    if key not in container:
        return None, None
    value = container[key]
    if value is None:
        return None, None
    if isinstance(value, str):
        if value == "":
            return None, None
        return value, None
    return None, "%s is a %s, not a string" % (key, _jtype(value))


def _handle_item(obj, lineno, state):
    if "item" not in obj:
        return
    item = obj["item"]
    if not isinstance(item, dict):
        _malformed(state, lineno, "item.completed item is a %s, not an object" % _jtype(item))
        return
    if "type" not in item:
        return
    itype = item["type"]
    if not isinstance(itype, str):
        _malformed(state, lineno, "item type is a %s, not a string" % _jtype(itype))
        return
    if itype == "agent_message":
        text, reason = _optional_text(item, "text")
        if reason:
            _malformed(state, lineno, "agent_message " + reason)
            return
        if text is not None:
            state.spoke += 1
            _out(text)
    elif itype == "command_execution":
        command, reason = _optional_text(item, "command")
        if reason:
            _malformed(state, lineno, "command_execution " + reason)
            return
        if command is not None:
            _out("<!-- codex ran: " + command[:160] + " -->")
    elif itype == "error":
        message, reason = _optional_text(item, "message")
        if reason:
            _malformed(state, lineno, "error item " + reason)
            return
        if message is not None:
            _err("[codex item error] " + message)


def _handle_turn_completed(obj, lineno, state):
    if "usage" in obj:
        usage = obj["usage"]
    else:
        usage = {}
    if not isinstance(usage, dict):
        _malformed(state, lineno, "turn.completed usage is a %s, not an object" % _jtype(usage))
        return
    counts = {}
    problems = []
    for key in ("input_tokens", "output_tokens"):
        if key not in usage:
            counts[key] = 0
            continue
        value = usage[key]
        if not _is_count(value):
            if isinstance(value, int) and not isinstance(value, bool):
                problems.append("usage %s is negative" % key)
            else:
                problems.append("usage %s is a %s, not a non-negative integer" % (key, _jtype(value)))
            continue
        counts[key] = value
    if problems:
        _malformed(state, lineno, "turn.completed " + "; ".join(problems))
        return
    state.done += 1
    _out("\n<!-- tokens: in %d out %d -->" % (counts["input_tokens"], counts["output_tokens"]))


def _handle_turn_failed(obj, lineno, state):
    state.failed = True
    msg = "no message"
    reason = None
    error = obj.get("error")
    if error is None:
        pass
    elif isinstance(error, dict):
        text, why = _optional_text(error, "message")
        if why:
            reason = "turn.failed error " + why
        elif text is not None:
            msg = text
    else:
        reason = "turn.failed error is a %s, not an object" % _jtype(error)
    if reason:
        _malformed(state, lineno, reason)
    _err("[codex turn FAILED] " + msg)


def _handle_error(obj, state):
    state.failed = True
    _err("[codex error] " + str(obj.get("message", "")))


def _process(obj, lineno, state):
    if not isinstance(obj, dict):
        _malformed(state, lineno, "event is a JSON %s, not an object" % _jtype(obj))
        return
    if "type" not in obj:
        return
    t = obj["type"]
    if not isinstance(t, str):
        _malformed(state, lineno, "event type is a %s, not a string" % _jtype(t))
        return
    if t == "item.completed":
        _handle_item(obj, lineno, state)
    elif t == "error":
        _handle_error(obj, state)
    elif t == "turn.completed":
        _handle_turn_completed(obj, lineno, state)
    elif t == "turn.failed":
        _handle_turn_failed(obj, lineno, state)
    # any other string type: an unknown extension, ignored


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
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            try:
                stream.reconfigure(encoding="utf-8", errors="replace")
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
