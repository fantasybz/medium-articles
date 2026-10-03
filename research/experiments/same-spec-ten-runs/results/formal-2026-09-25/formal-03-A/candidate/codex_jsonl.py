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


def _type_name(value):
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


def _is_count(value):
    return isinstance(value, int) and not isinstance(value, bool) and value >= 0


def _out(text):
    print(text, flush=True)


def _err(text):
    print(text, file=sys.stderr, flush=True)


class _State(object):
    def __init__(self):
        self.done = 0
        self.spoke = 0
        self.failed = False
        self.malformed = False

    def report_malformed(self, lineno, reason):
        self.malformed = True
        reason = " ".join(str(reason).split()) or "malformed event"
        _err("[codex malformed event] line %d: %s" % (lineno, reason))


def _handle_item_completed(obj, lineno, state):
    item = obj.get("item", _MISSING)
    if item is _MISSING:
        return
    if not isinstance(item, dict):
        state.report_malformed(lineno, "item.completed 'item' must be an object, got %s" % _type_name(item))
        return
    itype = item.get("type", _MISSING)
    if itype is _MISSING:
        return
    if not isinstance(itype, str):
        state.report_malformed(lineno, "item 'type' must be a string, got %s" % _type_name(itype))
        return

    if itype == "agent_message":
        text = item.get("text", _MISSING)
        if text is _MISSING or text is None or (isinstance(text, str) and text == ""):
            return
        if not isinstance(text, str):
            state.report_malformed(lineno, "agent_message 'text' must be a string, got %s" % _type_name(text))
            return
        state.spoke += 1
        _out(text)
    elif itype == "command_execution":
        command = item.get("command", _MISSING)
        if command is _MISSING or command is None or (isinstance(command, str) and command == ""):
            return
        if not isinstance(command, str):
            state.report_malformed(lineno, "command_execution 'command' must be a string, got %s"
                                   % _type_name(command))
            return
        _out("<!-- codex ran: %s -->" % command[:160])
    elif itype == "error":
        message = item.get("message", _MISSING)
        if message is _MISSING or message is None or (isinstance(message, str) and message == ""):
            return
        if not isinstance(message, str):
            state.report_malformed(lineno, "error item 'message' must be a string, got %s" % _type_name(message))
            return
        _err("[codex item error] " + message)
    # Unknown string item types are ignored without inspecting their payload.


def _handle_turn_completed(obj, lineno, state):
    usage = obj.get("usage", _MISSING)
    if usage is _MISSING:
        usage = {}
    if not isinstance(usage, dict):
        state.report_malformed(lineno, "turn.completed 'usage' must be an object, got %s" % _type_name(usage))
        return
    counts = {}
    problems = []
    for key in ("input_tokens", "output_tokens"):
        value = usage.get(key, _MISSING)
        if value is _MISSING:
            counts[key] = 0
        elif _is_count(value):
            counts[key] = value
        else:
            if isinstance(value, int) and not isinstance(value, bool):
                problems.append("usage '%s' must be a non-negative integer, got a negative integer" % key)
            else:
                problems.append("usage '%s' must be a non-negative integer, got %s" % (key, _type_name(value)))
    if problems:
        state.report_malformed(lineno, "; ".join(problems))
        return
    state.done += 1
    _out("\n<!-- tokens: in %d out %d -->" % (counts["input_tokens"], counts["output_tokens"]))


def _handle_error(obj, lineno, state):
    state.failed = True
    _err("[codex error] " + str(obj.get("message", "")))


def _handle_turn_failed(obj, lineno, state):
    state.failed = True
    msg = "no message"
    problem = None
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
            problem = "turn.failed error 'message' must be a string, got %s" % _type_name(message)
    else:
        problem = "turn.failed 'error' must be an object, got %s" % _type_name(error)
    if problem is not None:
        state.report_malformed(lineno, problem)
    _err("[codex turn FAILED] " + msg)


_HANDLERS = {
    "item.completed": _handle_item_completed,
    "turn.completed": _handle_turn_completed,
    "turn.failed": _handle_turn_failed,
    "error": _handle_error,
}


def _process_line(line, lineno, state):
    line = line.strip()
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
        state.report_malformed(lineno, "event 'type' must be a string, got %s" % _type_name(t))
        return
    handler = _HANDLERS.get(t)
    if handler is None:
        return
    handler(obj, lineno, state)


def _iter_lines():
    """Yield decoded lines one at a time, without buffering the whole input.

    Lines that are not valid UTF-8 are yielded as None so they still count
    toward the physical line number but are otherwise skipped.
    """
    raw = getattr(sys.stdin, "buffer", None)
    if raw is not None and hasattr(raw, "readline"):
        while True:
            chunk = raw.readline()
            if not chunk:
                break
            try:
                yield chunk.decode("utf-8")
            except UnicodeDecodeError:
                yield None
    else:
        while True:
            text = sys.stdin.readline()
            if not text:
                break
            yield text


def main():
    # The stream is UTF-8 whatever the locale says; a C locale would otherwise
    # choke on the first CJK character in a review.
    for stream, errors in ((sys.stdin, "strict"), (sys.stdout, "replace"), (sys.stderr, "backslashreplace")):
        if hasattr(stream, "reconfigure"):
            try:
                stream.reconfigure(encoding="utf-8", errors=errors)
            except Exception:
                pass

    state = _State()
    lineno = 0
    for line in _iter_lines():
        lineno += 1
        if line is None:
            continue
        _process_line(line, lineno, state)

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
