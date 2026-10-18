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
    6  a structurally malformed event arrived (valid JSON, wrong shape/types)
"""
import json
import sys


_MISSING = object()


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


def _tname(value):
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


def _malformed(state, lineno, reason):
    state.malformed = True
    reason = " ".join(str(reason).split()) or "malformed event"
    _err("[codex malformed event] line %d: %s" % (lineno, reason))


def _is_token_count(value):
    return isinstance(value, int) and not isinstance(value, bool) and value >= 0


def _handle_item(state, lineno, obj):
    item = obj.get("item", _MISSING)
    if item is _MISSING:
        item = {}
    if not isinstance(item, dict):
        _malformed(state, lineno, "item.completed 'item' must be an object, got %s" % _tname(item))
        return
    if "type" not in item:
        return
    itype = item["type"]
    if not isinstance(itype, str):
        _malformed(state, lineno, "item 'type' must be a string, got %s" % _tname(itype))
        return
    if itype == "agent_message":
        text = item.get("text", None)
        if text is None or (isinstance(text, str) and text == ""):
            return
        if not isinstance(text, str):
            _malformed(state, lineno, "agent_message 'text' must be a string, got %s" % _tname(text))
            return
        state.spoke += 1
        _out(text)
    elif itype == "command_execution":
        command = item.get("command", None)
        if command is None or (isinstance(command, str) and command == ""):
            return
        if not isinstance(command, str):
            _malformed(state, lineno,
                       "command_execution 'command' must be a string, got %s" % _tname(command))
            return
        _out("<!-- codex ran: %s -->" % command[:160])
    elif itype == "error":
        message = item.get("message", None)
        if message is None or (isinstance(message, str) and message == ""):
            return
        if not isinstance(message, str):
            _malformed(state, lineno, "error item 'message' must be a string, got %s" % _tname(message))
            return
        _err("[codex item error] " + message)
    # Unknown item types are ignored.


def _handle_turn_completed(state, lineno, obj):
    usage = obj.get("usage", _MISSING)
    if usage is _MISSING:
        usage = {}
    if not isinstance(usage, dict):
        _malformed(state, lineno, "turn.completed 'usage' must be an object, got %s" % _tname(usage))
        return
    counts = []
    for key in ("input_tokens", "output_tokens"):
        value = usage.get(key, _MISSING)
        if value is _MISSING:
            value = 0
        elif not _is_token_count(value):
            _malformed(state, lineno,
                       "usage '%s' must be a non-negative integer, got %s" % (key, _tname(value)))
            return
        counts.append(value)
    state.done += 1
    _out("\n<!-- tokens: in %s out %s -->" % (counts[0], counts[1]))


def _handle_turn_failed(state, lineno, obj):
    state.failed = True
    msg = "no message"
    error = obj.get("error", None)
    if error is not None:
        if not isinstance(error, dict):
            _malformed(state, lineno, "turn.failed 'error' must be an object, got %s" % _tname(error))
        else:
            message = error.get("message", None)
            if message is None or (isinstance(message, str) and message == ""):
                pass
            elif isinstance(message, str):
                msg = message
            else:
                _malformed(state, lineno,
                           "turn.failed error 'message' must be a string, got %s" % _tname(message))
    _err("[codex turn FAILED] " + msg)


def _handle_line(state, lineno, raw):
    if isinstance(raw, bytes):
        try:
            line = raw.decode("utf-8")
        except UnicodeDecodeError:
            return
    else:
        line = raw
    line = line.strip()
    if not line:
        return
    try:
        obj = json.loads(line)
    except (ValueError, RecursionError):
        return
    if not isinstance(obj, dict):
        _malformed(state, lineno, "event must be a JSON object, got %s" % _tname(obj))
        return
    if "type" not in obj:
        return
    t = obj["type"]
    if not isinstance(t, str):
        _malformed(state, lineno, "event 'type' must be a string, got %s" % _tname(t))
        return
    if t == "item.completed":
        _handle_item(state, lineno, obj)
    elif t == "error":
        state.failed = True
        _err("[codex error] " + str(obj.get("message", "")))
    elif t == "turn.completed":
        _handle_turn_completed(state, lineno, obj)
    elif t == "turn.failed":
        _handle_turn_failed(state, lineno, obj)
    # Unknown event types are ignored.


def _configure_streams():
    # The stream is UTF-8 whatever the locale says; a C locale would otherwise
    # choke on the first CJK character in a review.
    for stream in (sys.stdin,):
        if hasattr(stream, "reconfigure"):
            try:
                stream.reconfigure(encoding="utf-8")
            except Exception:
                pass
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            try:
                stream.reconfigure(encoding="utf-8", errors="backslashreplace")
            except Exception:
                pass


def main():
    _configure_streams()

    state = _State()
    source = getattr(sys.stdin, "buffer", None)
    if source is None:
        source = sys.stdin

    lineno = 0
    for raw in source:
        lineno += 1
        try:
            _handle_line(state, lineno, raw)
        except (BrokenPipeError, KeyboardInterrupt):
            raise
        except Exception as exc:  # never let one event kill the stream
            _malformed(state, lineno, "unexpected %s while handling event" % type(exc).__name__)

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
