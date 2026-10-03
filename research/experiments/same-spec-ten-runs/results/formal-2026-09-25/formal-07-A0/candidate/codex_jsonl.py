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
    6  a valid-JSON event had the wrong shape (malformed event)
"""
import json
import sys

_MISSING = object()


class Malformed(Exception):
    """Raised when a decoded JSON event has the wrong shape."""


def _is_token_count(value):
    return isinstance(value, int) and not isinstance(value, bool) and value >= 0


def _malformed_line(lineno, reason):
    reason = " ".join(str(reason).split()) or "malformed event"
    print("[codex malformed event] line %d: %s" % (lineno, reason), file=sys.stderr, flush=True)


def _optional_text(container, key, what):
    """Return a nonempty string, or None for missing/null/empty; raise on other types."""
    value = container.get(key, None)
    if value is None:
        return None
    if not isinstance(value, str):
        raise Malformed("%s must be a string, got %s" % (what, type(value).__name__))
    if value == "":
        return None
    return value


def _handle_item(obj):
    """Process an item.completed event. Returns 1 if an agent message was spoken."""
    item = obj.get("item", _MISSING)
    if item is _MISSING:
        return 0
    if not isinstance(item, dict):
        raise Malformed("item must be an object, got %s" % type(item).__name__)
    itype = item.get("type", _MISSING)
    if itype is _MISSING:
        return 0
    if not isinstance(itype, str):
        raise Malformed("item type must be a string, got %s" % type(itype).__name__)
    if itype == "agent_message":
        text = _optional_text(item, "text", "agent_message text")
        if text is None:
            return 0
        print(text, flush=True)
        return 1
    if itype == "command_execution":
        command = _optional_text(item, "command", "command_execution command")
        if command is None:
            return 0
        print("<!-- codex ran: %s -->" % command[:160], flush=True)
        return 0
    if itype == "error":
        message = _optional_text(item, "message", "item error message")
        if message is None:
            return 0
        print("[codex item error] " + message, file=sys.stderr, flush=True)
        return 0
    return 0


def _handle_turn_completed(obj):
    usage = obj.get("usage", _MISSING)
    if usage is _MISSING:
        usage = {}
    if not isinstance(usage, dict):
        raise Malformed("usage must be an object, got %s" % type(usage).__name__)
    counts = []
    for key in ("input_tokens", "output_tokens"):
        value = usage.get(key, _MISSING)
        if value is _MISSING:
            value = 0
        if not _is_token_count(value):
            raise Malformed("usage %s must be a non-negative integer, got %s"
                            % (key, type(value).__name__))
        counts.append(value)
    print("\n<!-- tokens: in %d out %d -->" % (counts[0], counts[1]), flush=True)


def _turn_failed_message(obj):
    """Return (message, malformed_reason_or_None)."""
    err = obj.get("error", None)
    if err is None:
        return "no message", None
    if not isinstance(err, dict):
        return "no message", "turn.failed error must be an object, got %s" % type(err).__name__
    msg = err.get("message", None)
    if msg is None or msg == "":
        return "no message", None
    if not isinstance(msg, str):
        return "no message", "turn.failed error message must be a string, got %s" % type(msg).__name__
    return msg, None


def main():
    # The stream is UTF-8 whatever the locale says; a C locale would otherwise
    # choke on the first CJK character in a review.
    for stream, errors in ((sys.stdin, "replace"), (sys.stdout, "replace"),
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
    for raw in sys.stdin:
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
            _malformed_line(lineno, "event must be a JSON object, got %s" % type(obj).__name__)
            continue
        t = obj.get("type", _MISSING)
        if t is _MISSING:
            continue
        if not isinstance(t, str):
            malformed = True
            _malformed_line(lineno, "event type must be a string, got %s" % type(t).__name__)
            continue
        try:
            if t == "item.completed":
                spoke += _handle_item(obj)
            elif t == "error":
                failed = True
                print("[codex error] " + str(obj.get("message", "")), file=sys.stderr, flush=True)
            elif t == "turn.completed":
                _handle_turn_completed(obj)
                done += 1
            elif t == "turn.failed":
                failed = True
                msg, reason = _turn_failed_message(obj)
                if reason is not None:
                    malformed = True
                    _malformed_line(lineno, reason)
                print("[codex turn FAILED] " + msg, file=sys.stderr, flush=True)
        except Malformed as exc:
            malformed = True
            _malformed_line(lineno, str(exc))
            continue

    if failed:
        print("[codex] the turn failed (reason above); no review was produced.", file=sys.stderr, flush=True)
        sys.exit(3)
    if malformed:
        sys.exit(6)
    if done == 0:
        print("[codex] no turn.completed event: possible mid-stream disconnect.", file=sys.stderr, flush=True)
        sys.exit(4)
    if spoke == 0:
        print("[codex] the turn completed without an agent message; no review was produced.",
              file=sys.stderr, flush=True)
        sys.exit(5)
    sys.exit(0)


if __name__ == "__main__":
    main()
