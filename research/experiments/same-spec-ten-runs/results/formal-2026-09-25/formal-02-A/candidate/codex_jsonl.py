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
    6  a structurally malformed event arrived (per-line diagnostics on stderr)
"""
import json
import sys


class Malformed(Exception):
    """Raised internally when a decoded event has a structurally wrong field."""


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


def _out(text):
    print(text, flush=True)


def _err(text):
    print(text, file=sys.stderr, flush=True)


def _is_count(value):
    return isinstance(value, int) and not isinstance(value, bool) and value >= 0


def _optional_text(container, key, what):
    """Return a nonempty string, or None for absent/null/empty; raise Malformed otherwise."""
    if key not in container:
        return None
    value = container[key]
    if value is None:
        return None
    if not isinstance(value, str):
        raise Malformed("%s must be a string, got %s" % (what, _tname(value)))
    if value == "":
        return None
    return value


class State(object):
    def __init__(self):
        self.done = 0
        self.spoke = 0
        self.failed = False
        self.malformed = False

    def report_malformed(self, line_no, reason):
        self.malformed = True
        reason = " ".join(str(reason).split()) or "malformed event"
        _err("[codex malformed event] line %d: %s" % (line_no, reason))


def handle_item(obj, state):
    if "item" not in obj:
        return
    item = obj["item"]
    if not isinstance(item, dict):
        raise Malformed("item.completed item must be an object, got %s" % _tname(item))
    if "type" not in item:
        return
    itype = item["type"]
    if not isinstance(itype, str):
        raise Malformed("item type must be a string, got %s" % _tname(itype))
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


def handle_turn_completed(obj, state):
    usage = obj.get("usage", {})
    if not isinstance(usage, dict):
        raise Malformed("turn.completed usage must be an object, got %s" % _tname(usage))
    counts = []
    for key in ("input_tokens", "output_tokens"):
        if key in usage:
            value = usage[key]
            if not _is_count(value):
                if isinstance(value, int) and not isinstance(value, bool):
                    raise Malformed("usage %s must be a non-negative integer, got a negative integer" % key)
                raise Malformed("usage %s must be a non-negative integer, got %s" % (key, _tname(value)))
            counts.append(value)
        else:
            counts.append(0)
    state.done += 1
    _out("\n<!-- tokens: in %d out %d -->" % (counts[0], counts[1]))


def handle_error(obj, state):
    state.failed = True
    raw = obj.get("message", "")
    try:
        text = str(raw)
    except (RecursionError, ValueError):
        text = "<unprintable message>"
    _err("[codex error] " + text)


def handle_turn_failed(obj, state, line_no):
    state.failed = True
    msg = "no message"
    reason = None
    if "error" in obj and obj["error"] is not None:
        error = obj["error"]
        if not isinstance(error, dict):
            reason = "turn.failed error must be an object, got %s" % _tname(error)
        else:
            try:
                value = _optional_text(error, "message", "turn.failed error message")
            except Malformed as exc:
                reason = str(exc)
                value = None
            if value is not None:
                msg = value
    if reason is not None:
        state.report_malformed(line_no, reason)
    _err("[codex turn FAILED] " + msg)


def process_line(raw_line, line_no, state):
    line = raw_line.strip()
    if not line:
        return
    try:
        obj = json.loads(line)
    except (ValueError, RecursionError):
        return
    if not isinstance(obj, dict):
        state.report_malformed(line_no, "event must be a JSON object, got %s" % _tname(obj))
        return
    if "type" not in obj:
        return
    t = obj["type"]
    if not isinstance(t, str):
        state.report_malformed(line_no, "event type must be a string, got %s" % _tname(t))
        return
    try:
        if t == "item.completed":
            handle_item(obj, state)
        elif t == "error":
            handle_error(obj, state)
        elif t == "turn.completed":
            handle_turn_completed(obj, state)
        elif t == "turn.failed":
            handle_turn_failed(obj, state, line_no)
    except Malformed as exc:
        state.report_malformed(line_no, str(exc))


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

    state = State()
    line_no = 0
    while True:
        raw_line = sys.stdin.readline()
        if not raw_line:
            break
        line_no += 1
        process_line(raw_line, line_no, state)

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
