"""Stream-parse `codex exec --json` output: print the agent's messages as they complete.

Kept in its own file because embedding this in a bash single-quoted `python3 -c`
string broke on the escaped quotes (the first run of codex_review.sh died with a
SyntaxError, which closed the pipe and made codex panic on stdout).

Prints agent messages to stdout (they become the review file), and everything
diagnostic (`turn.failed`, `error` events, missing `turn.completed`) to stderr so
the caller can tell "Codex said nothing" from "Codex was refused".

Valid JSON whose shape is wrong (a non-object event, a non-string type, a
non-string agent text, a non-integer token count, ...) is reported on stderr as
`[codex malformed event] line N: REASON` and dropped; processing continues.

Exit codes codex_review.sh branches on:
    0  at least one agent message and a completed turn
    3  the turn failed or an error event arrived (refusal, usage limit)
    4  no turn.completed: a mid-stream disconnect
    5  the turn completed but Codex never spoke; the "review" would be a token count
    6  a malformed event was seen (and no explicit remote failure)
"""
import json
import sys


NO_MESSAGE = "no message"


class _State(object):
    def __init__(self):
        self.done = 0
        self.spoke = 0
        self.failed = False
        self.malformed = False

    def bad(self, lineno, reason):
        self.malformed = True
        reason = " ".join(str(reason).split()) or "malformed event"
        print("[codex malformed event] line %d: %s" % (lineno, reason),
              file=sys.stderr, flush=True)


def _kind(value):
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


def _optional_text(container, key):
    """Return (text_or_None, problem_or_None).

    Absent, null and the empty string all mean "no text"; any other non-string
    value is a problem.
    """
    if key not in container:
        return None, None
    value = container[key]
    if value is None:
        return None, None
    if isinstance(value, str):
        return (value if value else None), None
    return None, "field '%s' must be a string, got %s" % (key, _kind(value))


def _token_count(usage, key):
    if key not in usage:
        return 0, None
    value = usage[key]
    if type(value) is not int or value < 0:
        if type(value) is int:
            desc = "negative integer"
        else:
            desc = _kind(value)
        return None, "usage.%s must be a non-negative integer, got %s" % (key, desc)
    return value, None


def _handle_item(obj, lineno, state):
    if "item" not in obj:
        return
    item = obj["item"]
    if not isinstance(item, dict):
        state.bad(lineno, "item.completed 'item' must be an object, got %s" % _kind(item))
        return
    if "type" not in item:
        return
    itype = item["type"]
    if not isinstance(itype, str):
        state.bad(lineno, "item 'type' must be a string, got %s" % _kind(itype))
        return
    if itype == "agent_message":
        text, problem = _optional_text(item, "text")
        if problem:
            state.bad(lineno, "agent_message " + problem)
            return
        if text is not None:
            state.spoke += 1
            print(text, flush=True)
    elif itype == "command_execution":
        command, problem = _optional_text(item, "command")
        if problem:
            state.bad(lineno, "command_execution " + problem)
            return
        if command is not None:
            print("<!-- codex ran: %s -->" % command[:160], flush=True)
    elif itype == "error":
        message, problem = _optional_text(item, "message")
        if problem:
            state.bad(lineno, "error item " + problem)
            return
        if message is not None:
            print("[codex item error] " + message, file=sys.stderr, flush=True)
    # Unknown string item types are ignored without inspecting their payload.


def _handle_turn_completed(obj, lineno, state):
    if "usage" in obj:
        usage = obj["usage"]
        if not isinstance(usage, dict):
            state.bad(lineno, "turn.completed 'usage' must be an object, got %s" % _kind(usage))
            return
    else:
        usage = {}
    tokens_in, problem = _token_count(usage, "input_tokens")
    if problem:
        state.bad(lineno, "turn.completed " + problem)
        return
    tokens_out, problem = _token_count(usage, "output_tokens")
    if problem:
        state.bad(lineno, "turn.completed " + problem)
        return
    state.done += 1
    print("\n<!-- tokens: in %d out %d -->" % (tokens_in, tokens_out), flush=True)


def _handle_turn_failed(obj, lineno, state):
    state.failed = True
    message = NO_MESSAGE
    problem = None
    error = obj.get("error")
    if error is None:
        pass
    elif isinstance(error, dict):
        text, text_problem = _optional_text(error, "message")
        if text_problem:
            problem = "turn.failed error " + text_problem
        elif text is not None:
            message = text
    else:
        problem = "turn.failed 'error' must be an object, got %s" % _kind(error)
    if problem:
        state.bad(lineno, problem)
    print("[codex turn FAILED] " + message, file=sys.stderr, flush=True)


def _handle_error(obj, state):
    state.failed = True
    print("[codex error] " + str(obj.get("message", "")), file=sys.stderr, flush=True)


def _handle(obj, lineno, state):
    if not isinstance(obj, dict):
        state.bad(lineno, "event must be a JSON object, got %s" % _kind(obj))
        return
    if "type" not in obj:
        return
    t = obj["type"]
    if not isinstance(t, str):
        state.bad(lineno, "event 'type' must be a string, got %s" % _kind(t))
        return
    if t == "item.completed":
        _handle_item(obj, lineno, state)
    elif t == "error":
        _handle_error(obj, state)
    elif t == "turn.completed":
        _handle_turn_completed(obj, lineno, state)
    elif t == "turn.failed":
        _handle_turn_failed(obj, lineno, state)
    # Unknown string event types are ignored without inspecting their payload.


def _lines(stream):
    """Yield one decoded physical line at a time (None if it is not UTF-8)."""
    if stream is None:
        return
    raw_stream = getattr(stream, "buffer", None)
    if raw_stream is not None:
        while True:
            raw = raw_stream.readline()
            if not raw:
                return
            try:
                yield raw.decode("utf-8")
            except UnicodeDecodeError:
                yield None
    else:
        while True:
            line = stream.readline()
            if not line:
                return
            if isinstance(line, bytes):
                try:
                    line = line.decode("utf-8")
                except UnicodeDecodeError:
                    line = None
            yield line


def _configure_output():
    # The stream is UTF-8 whatever the locale says; a C locale would otherwise
    # choke on the first CJK character in a review.
    for stream, errors in ((sys.stdout, "replace"), (sys.stderr, "backslashreplace")):
        if stream is not None and hasattr(stream, "reconfigure"):
            try:
                stream.reconfigure(encoding="utf-8", errors=errors)
            except Exception:
                pass


def main():
    _configure_output()

    state = _State()
    lineno = 0
    for line in _lines(sys.stdin):
        lineno += 1
        if line is None:
            continue
        line = line.strip()
        if not line:
            continue
        try:
            obj = json.loads(line)
        except (ValueError, RecursionError):
            continue
        _handle(obj, lineno, state)

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
