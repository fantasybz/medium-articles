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
    6  a structurally malformed event arrived (see per-line diagnostics)
"""
import json
import sys


_MISSING = object()


class Malformed(Exception):
    """Raised while validating one event; carries a single-line reason."""


def _out(text):
    print(text, flush=True)


def _err(text):
    print(text, file=sys.stderr, flush=True)


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


def _optional_text(obj, key, where):
    """Return a nonempty string, or None for absent/null/empty; raise if wrong type."""
    value = obj.get(key, _MISSING)
    if value is _MISSING or value is None:
        return None
    if not isinstance(value, str):
        raise Malformed("%s field '%s' must be a string, got %s" % (where, key, _tname(value)))
    if value == "":
        return None
    return value


def _token_count(usage, key):
    value = usage.get(key, _MISSING)
    if value is _MISSING:
        return 0
    if isinstance(value, bool) or not isinstance(value, int):
        raise Malformed("usage field '%s' must be a non-negative integer, got %s" % (key, _tname(value)))
    if value < 0:
        raise Malformed("usage field '%s' must be a non-negative integer, got a negative value" % key)
    return value


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
                stream.reconfigure(encoding="utf-8")
            except Exception:
                pass

    state = {"done": 0, "spoke": 0, "failed": False, "malformed": False}

    def malformed(lineno, reason):
        state["malformed"] = True
        reason = " ".join(str(reason).split()) or "malformed event"
        _err("[codex malformed event] line %d: %s" % (lineno, reason))

    def handle_item(obj):
        item = obj.get("item", _MISSING)
        if item is _MISSING:
            return
        if not isinstance(item, dict):
            raise Malformed("item.completed field 'item' must be an object, got %s" % _tname(item))
        itype = item.get("type", _MISSING)
        if itype is _MISSING:
            return
        if not isinstance(itype, str):
            raise Malformed("item field 'type' must be a string, got %s" % _tname(itype))
        if itype == "agent_message":
            text = _optional_text(item, "text", "agent_message")
            if text is not None:
                state["spoke"] += 1
                _out(text)
        elif itype == "command_execution":
            command = _optional_text(item, "command", "command_execution")
            if command is not None:
                _out("<!-- codex ran: %s -->" % command[:160])
        elif itype == "error":
            message = _optional_text(item, "message", "error item")
            if message is not None:
                _err("[codex item error] " + message)

    def handle_turn_completed(obj):
        usage = obj.get("usage", _MISSING)
        if usage is _MISSING:
            usage = {}
        if not isinstance(usage, dict):
            raise Malformed("turn.completed field 'usage' must be an object, got %s" % _tname(usage))
        tin = _token_count(usage, "input_tokens")
        tout = _token_count(usage, "output_tokens")
        state["done"] += 1
        _out("\n<!-- tokens: in %s out %s -->" % (tin, tout))

    def handle_turn_failed(obj, lineno):
        state["failed"] = True
        msg = "no message"
        reason = None
        error = obj.get("error", _MISSING)
        if error is _MISSING or error is None:
            pass
        elif isinstance(error, dict):
            message = error.get("message", _MISSING)
            if message is _MISSING or message is None or message == "":
                pass
            elif isinstance(message, str):
                msg = message
            else:
                reason = "turn.failed field 'error.message' must be a string, got %s" % _tname(message)
        else:
            reason = "turn.failed field 'error' must be an object, got %s" % _tname(error)
        if reason is not None:
            malformed(lineno, reason)
        _err("[codex turn FAILED] " + msg)

    lineno = 0
    while True:
        raw = sys.stdin.readline()
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
            if not isinstance(obj, dict):
                raise Malformed("event must be a JSON object, got %s" % _tname(obj))
            t = obj.get("type", _MISSING)
            if t is _MISSING:
                continue
            if not isinstance(t, str):
                raise Malformed("event field 'type' must be a string, got %s" % _tname(t))
            if t == "item.completed":
                handle_item(obj)
            elif t == "error":
                state["failed"] = True
                _err("[codex error] " + str(obj.get("message", "")))
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
