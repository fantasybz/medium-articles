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
    """Raised when a decoded JSON event has a field of the wrong type."""


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


def _out(text):
    print(text, flush=True)


def _err(text):
    print(text, file=sys.stderr, flush=True)


def _optional_text(container, key, what):
    """Return a nonempty string, or None for absent/null/empty; raise on other types."""
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


def _token_count(usage, key):
    if key not in usage:
        return 0
    value = usage[key]
    if isinstance(value, bool) or not isinstance(value, int):
        raise Malformed("usage.%s must be a non-negative integer, got %s" % (key, _tname(value)))
    if value < 0:
        raise Malformed("usage.%s must be a non-negative integer, got a negative value" % key)
    return value


def _iter_lines():
    """Yield decoded lines one at a time (None for undecodable bytes)."""
    buf = getattr(sys.stdin, "buffer", None)
    if buf is not None and hasattr(buf, "readline"):
        while True:
            raw = buf.readline()
            if not raw:
                return
            try:
                yield raw.decode("utf-8")
            except UnicodeDecodeError:
                yield None
    else:
        while True:
            line = sys.stdin.readline()
            if not line:
                return
            yield line


def main():
    # The stream is UTF-8 whatever the locale says; a C locale would otherwise
    # choke on the first CJK character in a review.
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            try:
                stream.reconfigure(encoding="utf-8", errors="backslashreplace")
            except Exception:
                pass
    if not hasattr(getattr(sys.stdin, "buffer", None), "readline") and hasattr(sys.stdin, "reconfigure"):
        try:
            sys.stdin.reconfigure(encoding="utf-8")
        except Exception:
            pass

    state = {"done": 0, "spoke": 0, "failed": False, "malformed": False}

    def malformed(lineno, reason):
        state["malformed"] = True
        reason = " ".join(str(reason).split()) or "malformed event"
        _err("[codex malformed event] line %d: %s" % (lineno, reason))

    def handle_item(obj):
        if "item" in obj:
            item = obj["item"]
        else:
            item = {}
        if not isinstance(item, dict):
            raise Malformed("item must be an object, got %s" % _tname(item))
        if "type" not in item:
            return
        itype = item["type"]
        if not isinstance(itype, str):
            raise Malformed("item.type must be a string, got %s" % _tname(itype))
        if itype == "agent_message":
            text = _optional_text(item, "text", "item.text")
            if text is not None:
                state["spoke"] += 1
                _out(text)
        elif itype == "command_execution":
            command = _optional_text(item, "command", "item.command")
            if command is not None:
                _out("<!-- codex ran: %s -->" % command[:160])
        elif itype == "error":
            message = _optional_text(item, "message", "item.message")
            if message is not None:
                _err("[codex item error] " + message)

    def handle_turn_completed(obj):
        if "usage" in obj:
            usage = obj["usage"]
        else:
            usage = {}
        if not isinstance(usage, dict):
            raise Malformed("usage must be an object, got %s" % _tname(usage))
        tin = _token_count(usage, "input_tokens")
        tout = _token_count(usage, "output_tokens")
        state["done"] += 1
        _out("\n<!-- tokens: in %d out %d -->" % (tin, tout))

    def handle_turn_failed(obj, lineno):
        state["failed"] = True
        msg = "no message"
        reason = None
        error = obj.get("error")
        if error is None:
            pass
        elif isinstance(error, dict):
            try:
                value = _optional_text(error, "message", "error.message")
                if value is not None:
                    msg = value
            except Malformed as exc:
                reason = str(exc)
        else:
            reason = "error must be an object, got %s" % _tname(error)
        if reason is not None:
            malformed(lineno, reason)
        _err("[codex turn FAILED] " + msg)

    def handle_error(obj):
        state["failed"] = True
        message = obj.get("message", "")
        try:
            text = str(message)
        except Exception:
            text = "<unprintable message>"
        _err("[codex error] " + text)

    lineno = 0
    for line in _iter_lines():
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
        if not isinstance(obj, dict):
            malformed(lineno, "event must be a JSON object, got %s" % _tname(obj))
            continue
        if "type" not in obj:
            continue
        t = obj["type"]
        if not isinstance(t, str):
            malformed(lineno, "event type must be a string, got %s" % _tname(t))
            continue
        try:
            if t == "item.completed":
                handle_item(obj)
            elif t == "error":
                handle_error(obj)
            elif t == "turn.completed":
                handle_turn_completed(obj)
            elif t == "turn.failed":
                handle_turn_failed(obj, lineno)
        except Malformed as exc:
            malformed(lineno, str(exc))

    if state["failed"]:
        _err("[codex] the turn failed (reason above); no review was produced.")
        sys.exit(3)
    if state["malformed"]:
        sys.exit(6)
    if state["done"] == 0:
        _err("[codex] no turn.completed event: possible mid-stream disconnect.")
        sys.exit(4)
    if state["spoke"] == 0:
        _err("[codex] the turn completed without an agent message; no review was produced.")
        sys.exit(5)


if __name__ == "__main__":
    main()
