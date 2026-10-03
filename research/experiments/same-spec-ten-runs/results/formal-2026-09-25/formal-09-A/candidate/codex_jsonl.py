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


class Malformed(Exception):
    """A decoded JSON line whose structure has the wrong value types."""


def _is_count(value):
    return isinstance(value, int) and not isinstance(value, bool) and value >= 0


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


def _err(text):
    print(text, file=sys.stderr, flush=True)


class State(object):
    def __init__(self):
        self.done = 0
        self.spoke = 0
        self.failed = False
        self.malformed = False

    def report_malformed(self, lineno, reason):
        self.malformed = True
        reason = " ".join(str(reason).split()) or "malformed event"
        _err("[codex malformed event] line %d: %s" % (lineno, reason))


def _handle_item(obj):
    """Validate an item.completed event; return an action tuple or None."""
    if "item" in obj:
        item = obj["item"]
        if not isinstance(item, dict):
            raise Malformed("item.completed item must be an object, got %s" % _type_name(item))
    else:
        item = {}
    if "type" not in item:
        return None
    itype = item["type"]
    if not isinstance(itype, str):
        raise Malformed("item type must be a string, got %s" % _type_name(itype))
    if itype == "agent_message":
        text = item.get("text")
        if text is None:
            return None
        if not isinstance(text, str):
            raise Malformed("agent_message text must be a string, got %s" % _type_name(text))
        if text == "":
            return None
        return ("agent", text)
    if itype == "command_execution":
        command = item.get("command")
        if command is None:
            return None
        if not isinstance(command, str):
            raise Malformed("command_execution command must be a string, got %s" % _type_name(command))
        if command == "":
            return None
        return ("command", command)
    if itype == "error":
        message = item.get("message")
        if message is None:
            return None
        if not isinstance(message, str):
            raise Malformed("error item message must be a string, got %s" % _type_name(message))
        if message == "":
            return None
        return ("item_error", message)
    return None


def _handle_usage(obj):
    if "usage" in obj:
        usage = obj["usage"]
        if not isinstance(usage, dict):
            raise Malformed("turn.completed usage must be an object, got %s" % _type_name(usage))
    else:
        usage = {}
    counts = []
    bad = []
    for key in ("input_tokens", "output_tokens"):
        if key in usage:
            value = usage[key]
            if not _is_count(value):
                bad.append("%s must be a non-negative integer, got %s" % (key, _type_name(value)))
                counts.append(0)
                continue
            counts.append(value)
        else:
            counts.append(0)
    if bad:
        raise Malformed("; ".join(bad))
    return counts[0], counts[1]


def _handle_failed(obj):
    """Return (message, malformed_reason_or_None) for a turn.failed event."""
    error = obj.get("error")
    if error is None:
        return "no message", None
    if not isinstance(error, dict):
        return "no message", "turn.failed error must be an object, got %s" % _type_name(error)
    message = error.get("message")
    if message is None:
        return "no message", None
    if not isinstance(message, str):
        return "no message", "turn.failed error message must be a string, got %s" % _type_name(message)
    if message == "":
        return "no message", None
    return message, None


def _process(obj, lineno, state):
    if not isinstance(obj, dict):
        raise Malformed("event must be a JSON object, got %s" % _type_name(obj))
    if "type" not in obj:
        return
    t = obj["type"]
    if not isinstance(t, str):
        raise Malformed("event type must be a string, got %s" % _type_name(t))

    if t == "item.completed":
        action = _handle_item(obj)
        if action is None:
            return
        kind, value = action
        if kind == "agent":
            state.spoke += 1
            print(value, flush=True)
        elif kind == "command":
            print("<!-- codex ran: %s -->" % value[:160], flush=True)
        elif kind == "item_error":
            _err("[codex item error] " + value)
    elif t == "error":
        state.failed = True
        try:
            msg = str(obj.get("message", ""))
        except (RecursionError, ValueError):
            msg = "<unprintable message>"
        _err("[codex error] " + msg)
    elif t == "turn.completed":
        tokens_in, tokens_out = _handle_usage(obj)
        state.done += 1
        print("\n<!-- tokens: in %d out %d -->" % (tokens_in, tokens_out), flush=True)
    elif t == "turn.failed":
        state.failed = True
        msg, reason = _handle_failed(obj)
        if reason is not None:
            state.report_malformed(lineno, reason)
        _err("[codex turn FAILED] " + msg)
    # Unknown string event types are ignored without payload validation.


def main():
    # The stream is UTF-8 whatever the locale says; a C locale would otherwise
    # choke on the first CJK character in a review.
    if sys.stdin is not None and hasattr(sys.stdin, "reconfigure"):
        try:
            sys.stdin.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass
    for stream in (sys.stdout, sys.stderr):
        if stream is not None and hasattr(stream, "reconfigure"):
            try:
                stream.reconfigure(encoding="utf-8", errors="backslashreplace")
            except Exception:
                pass

    state = State()
    lineno = 0
    if sys.stdin is not None:
        # readline keeps processing incremental: each line is handled as it arrives.
        for raw in iter(sys.stdin.readline, ""):
            lineno += 1
            line = raw.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
            except (ValueError, RecursionError):
                continue
            try:
                _process(obj, lineno, state)
            except Malformed as exc:
                state.report_malformed(lineno, str(exc))

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
