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
    """Raised while validating one event; the message is the one-line reason."""


_MISSING = object()


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
    sys.stdout.write(text + "\n")
    sys.stdout.flush()


def _err(text):
    sys.stderr.write(text + "\n")
    sys.stderr.flush()


def _optional_text(obj, key, where):
    """Return a nonempty string, or None when absent/null/empty; raise if wrong type."""
    value = obj.get(key, _MISSING)
    if value is _MISSING or value is None:
        return None
    if not isinstance(value, str):
        raise Malformed("%s.%s must be a string, got %s" % (where, key, _tname(value)))
    if value == "":
        return None
    return value


def _token_count(usage, key):
    value = usage.get(key, _MISSING)
    if value is _MISSING:
        return 0
    if isinstance(value, bool) or not isinstance(value, int):
        raise Malformed("usage.%s must be a non-negative integer, got %s" % (key, _tname(value)))
    if value < 0:
        raise Malformed("usage.%s must be a non-negative integer, got a negative value" % key)
    return value


def main():
    # The stream is UTF-8 whatever the locale says; a C locale would otherwise
    # choke on the first CJK character in a review.
    for stream, errors in ((sys.stdin, "replace"), (sys.stdout, "backslashreplace"),
                           (sys.stderr, "backslashreplace")):
        if hasattr(stream, "reconfigure"):
            try:
                stream.reconfigure(encoding="utf-8", errors=errors)
            except Exception:
                pass

    done = 0
    spoke = 0
    failed = False
    malformed = False
    lineno = 0

    def report(n, reason):
        reason = " ".join(str(reason).split()) or "malformed event"
        _err("[codex malformed event] line %d: %s" % (n, reason))

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
            if not isinstance(obj, dict):
                raise Malformed("event must be a JSON object, got %s" % _tname(obj))
            t = obj.get("type", _MISSING)
            if t is _MISSING:
                continue
            if not isinstance(t, str):
                raise Malformed("event type must be a string, got %s" % _tname(t))

            if t == "item.completed":
                item = obj.get("item", _MISSING)
                if item is _MISSING:
                    continue
                if not isinstance(item, dict):
                    raise Malformed("item must be an object, got %s" % _tname(item))
                itype = item.get("type", _MISSING)
                if itype is _MISSING:
                    continue
                if not isinstance(itype, str):
                    raise Malformed("item.type must be a string, got %s" % _tname(itype))
                if itype == "agent_message":
                    text = _optional_text(item, "text", "item")
                    if text is not None:
                        spoke += 1
                        _out(text)
                elif itype == "command_execution":
                    command = _optional_text(item, "command", "item")
                    if command is not None:
                        _out("<!-- codex ran: %s -->" % command[:160])
                elif itype == "error":
                    message = _optional_text(item, "message", "item")
                    if message is not None:
                        _err("[codex item error] " + message)
            elif t == "error":
                failed = True
                _err("[codex error] " + str(obj.get("message", "")))
            elif t == "turn.completed":
                usage = obj.get("usage", _MISSING)
                if usage is _MISSING:
                    usage = {}
                if not isinstance(usage, dict):
                    raise Malformed("usage must be an object, got %s" % _tname(usage))
                tin = _token_count(usage, "input_tokens")
                tout = _token_count(usage, "output_tokens")
                done += 1
                _out("\n<!-- tokens: in %d out %d -->" % (tin, tout))
            elif t == "turn.failed":
                failed = True
                msg = "no message"
                reason = None
                error = obj.get("error", _MISSING)
                if error is _MISSING or error is None:
                    pass
                elif not isinstance(error, dict):
                    reason = "turn.failed error must be an object, got %s" % _tname(error)
                else:
                    m = error.get("message", _MISSING)
                    if m is _MISSING or m is None or m == "":
                        pass
                    elif isinstance(m, str):
                        msg = m
                    else:
                        reason = "turn.failed error.message must be a string, got %s" % _tname(m)
                if reason is not None:
                    malformed = True
                    report(lineno, reason)
                _err("[codex turn FAILED] " + msg)
            # Any other string type: an unknown event, ignored.
        except Malformed as exc:
            malformed = True
            report(lineno, str(exc))

    if failed:
        _err("[codex] the turn failed (reason above); no review was produced.")
        sys.exit(3)
    if malformed:
        sys.exit(6)
    if done == 0:
        _err("[codex] no turn.completed event: possible mid-stream disconnect.")
        sys.exit(4)
    if spoke == 0:
        _err("[codex] the turn completed without an agent message; no review was produced.")
        sys.exit(5)


if __name__ == "__main__":
    main()
