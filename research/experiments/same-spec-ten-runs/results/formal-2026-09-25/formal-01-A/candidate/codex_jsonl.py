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
    6  a malformed event (valid JSON with the wrong shape) was seen
"""
import json
import sys

_MISSING = object()


class Malformed(Exception):
    """Raised when a decoded JSON event has a structurally wrong value."""


def _out(text):
    sys.stdout.write(text + "\n")
    sys.stdout.flush()


def _err(text):
    sys.stderr.write(text + "\n")
    sys.stderr.flush()


def _malformed(lineno, reason):
    reason = " ".join(str(reason).split()) or "malformed event"
    _err("[codex malformed event] line %d: %s" % (lineno, reason))


def _lines():
    """Yield each physical input line as text (None if it is not valid UTF-8).

    Reads one line at a time so output is produced before stdin EOF.
    """
    buf = getattr(sys.stdin, "buffer", None)
    if buf is not None:
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


def _optional_text(container, key, what):
    """Return a nonempty string, or None for absent/null/empty; raise if wrong type."""
    value = container.get(key, _MISSING)
    if value is _MISSING or value is None:
        return None
    if not isinstance(value, str):
        raise Malformed("%s must be a string, got %s" % (what, type(value).__name__))
    if value == "":
        return None
    return value


def _token_count(usage, key):
    value = usage.get(key, _MISSING)
    if value is _MISSING:
        return 0
    if isinstance(value, bool) or not isinstance(value, int):
        raise Malformed("usage.%s must be a non-negative integer, got %s"
                        % (key, type(value).__name__))
    if value < 0:
        raise Malformed("usage.%s must be a non-negative integer, got a negative value" % key)
    return value


def main():
    # The stream is UTF-8 whatever the locale says; a C locale would otherwise
    # choke on the first CJK character in a review.
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            try:
                stream.reconfigure(encoding="utf-8", errors="backslashreplace")
            except Exception:
                pass
    if getattr(sys.stdin, "buffer", None) is None and hasattr(sys.stdin, "reconfigure"):
        try:
            sys.stdin.reconfigure(encoding="utf-8")
        except Exception:
            pass

    done = 0
    spoke = 0
    failed = False
    malformed = False
    lineno = 0

    for line in _lines():
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

        try:
            if not isinstance(obj, dict):
                raise Malformed("event must be a JSON object, got %s" % type(obj).__name__)
            t = obj.get("type", _MISSING)
            if t is _MISSING:
                continue
            if not isinstance(t, str):
                raise Malformed("event type must be a string, got %s" % type(t).__name__)

            if t == "item.completed":
                item = obj.get("item", _MISSING)
                if item is _MISSING:
                    item = {}
                if not isinstance(item, dict):
                    raise Malformed("item must be an object, got %s" % type(item).__name__)
                itype = item.get("type", _MISSING)
                if itype is _MISSING:
                    continue
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
            elif t == "error":
                failed = True
                _err("[codex error] " + str(obj.get("message", "")))
            elif t == "turn.completed":
                usage = obj.get("usage", _MISSING)
                if usage is _MISSING:
                    usage = {}
                if not isinstance(usage, dict):
                    raise Malformed("usage must be an object, got %s" % type(usage).__name__)
                tin = _token_count(usage, "input_tokens")
                tout = _token_count(usage, "output_tokens")
                done += 1
                _out("\n<!-- tokens: in %d out %d -->" % (tin, tout))
            elif t == "turn.failed":
                failed = True
                msg = "no message"
                reason = None
                err = obj.get("error", _MISSING)
                if err is _MISSING or err is None:
                    pass
                elif isinstance(err, dict):
                    m = err.get("message", _MISSING)
                    if m is _MISSING or m is None:
                        pass
                    elif isinstance(m, str):
                        if m:
                            msg = m
                    else:
                        reason = "turn.failed error.message must be a string, got %s" % type(m).__name__
                else:
                    reason = "turn.failed error must be an object, got %s" % type(err).__name__
                if reason is not None:
                    malformed = True
                    _malformed(lineno, reason)
                _err("[codex turn FAILED] " + msg)
            # Unknown string event types are ignored without validation.
        except Malformed as exc:
            malformed = True
            _malformed(lineno, str(exc))

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
