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
    6  a JSON event had a structurally wrong field (see the per-line diagnostics)
"""
import json
import sys


class Malformed(Exception):
    """Raised while validating a single event whose fields have the wrong type."""


def _out(text):
    print(text, flush=True)


def _err(text):
    print(text, file=sys.stderr, flush=True)


def _malformed(lineno, reason):
    reason = " ".join(str(reason).split()) or "malformed event"
    _err("[codex malformed event] line %d: %s" % (lineno, reason))


def _optional_text(container, key, what):
    """Return a nonempty string, or None for absent/null/empty; raise on other types."""
    if key not in container:
        return None
    value = container[key]
    if value is None:
        return None
    if not isinstance(value, str):
        raise Malformed("%s must be a string, got %s" % (what, type(value).__name__))
    if value == "":
        return None
    return value


def _token_count(usage, key):
    if key not in usage:
        return 0
    value = usage[key]
    if isinstance(value, bool) or not isinstance(value, int):
        raise Malformed("usage.%s must be a non-negative integer, got %s"
                        % (key, type(value).__name__))
    if value < 0:
        raise Malformed("usage.%s must be a non-negative integer, got %d" % (key, value))
    return value


def _reconfigure():
    # The stream is UTF-8 whatever the locale says; a C locale would otherwise
    # choke on the first CJK character in a review.
    settings = (
        (sys.stdin, "replace"),
        (sys.stdout, "backslashreplace"),
        (sys.stderr, "backslashreplace"),
    )
    for stream, errors in settings:
        if stream is not None and hasattr(stream, "reconfigure"):
            try:
                stream.reconfigure(encoding="utf-8", errors=errors)
            except Exception:
                try:
                    stream.reconfigure(encoding="utf-8")
                except Exception:
                    pass


def main():
    _reconfigure()

    done = 0
    spoke = 0
    failed = False
    malformed = False
    lineno = 0

    for raw in iter(sys.stdin.readline, ""):
        lineno += 1
        line = raw.strip()
        if not line:
            continue
        try:
            obj = json.loads(line)
        except (ValueError, RecursionError):
            continue

        if not isinstance(obj, dict):
            malformed = True
            _malformed(lineno, "event must be a JSON object, got %s" % type(obj).__name__)
            continue

        if "type" not in obj:
            continue
        t = obj["type"]
        if not isinstance(t, str):
            malformed = True
            _malformed(lineno, "event type must be a string, got %s" % type(t).__name__)
            continue

        if t == "item.completed":
            try:
                item = obj.get("item", {})
                if not isinstance(item, dict):
                    raise Malformed("item must be an object, got %s" % type(item).__name__)
                if "type" not in item:
                    continue
                itype = item["type"]
                if not isinstance(itype, str):
                    raise Malformed("item type must be a string, got %s" % type(itype).__name__)
                if itype == "agent_message":
                    text = _optional_text(item, "text", "agent_message text")
                    if text is not None:
                        spoke += 1
                        _out(text)
                elif itype == "command_execution":
                    command = _optional_text(item, "command", "command_execution command")
                    if command is not None:
                        _out("<!-- codex ran: %s -->" % command[:160])
                elif itype == "error":
                    message = _optional_text(item, "message", "error item message")
                    if message is not None:
                        _err("[codex item error] " + message)
            except Malformed as exc:
                malformed = True
                _malformed(lineno, exc)
        elif t == "error":
            failed = True
            _err("[codex error] " + str(obj.get("message", "")))
        elif t == "turn.completed":
            try:
                usage = obj.get("usage", {})
                if not isinstance(usage, dict):
                    raise Malformed("usage must be an object, got %s" % type(usage).__name__)
                tin = _token_count(usage, "input_tokens")
                tout = _token_count(usage, "output_tokens")
            except Malformed as exc:
                malformed = True
                _malformed(lineno, exc)
                continue
            done += 1
            _out("\n<!-- tokens: in %s out %s -->" % (tin, tout))
        elif t == "turn.failed":
            failed = True
            msg = "no message"
            reason = None
            error = obj.get("error")
            if error is None:
                pass
            elif isinstance(error, dict):
                try:
                    text = _optional_text(error, "message", "turn.failed error.message")
                    if text is not None:
                        msg = text
                except Malformed as exc:
                    reason = str(exc)
            else:
                reason = "turn.failed error must be an object, got %s" % type(error).__name__
            if reason is not None:
                malformed = True
                _malformed(lineno, reason)
            _err("[codex turn FAILED] " + msg)
        # Unknown string event types are ignored without validating their payload.

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
    sys.exit(0)


if __name__ == "__main__":
    main()
