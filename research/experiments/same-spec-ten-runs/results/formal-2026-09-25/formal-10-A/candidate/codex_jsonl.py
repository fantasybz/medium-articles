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


class Malformed(Exception):
    """Raised when a decoded JSON event has a structurally wrong value."""


def _is_nonneg_int(value):
    return isinstance(value, int) and not isinstance(value, bool) and value >= 0


def _optional_text(container, key, what):
    """Return a nonempty string, or None for missing/null/empty; raise on bad type."""
    value = container.get(key, _MISSING)
    if value is _MISSING or value is None:
        return None
    if not isinstance(value, str):
        raise Malformed("%s must be a string, got %s" % (what, type(value).__name__))
    if value == "":
        return None
    return value


def _report_malformed(lineno, reason):
    reason = " ".join(str(reason).splitlines()).strip() or "malformed event"
    sys.stderr.write("[codex malformed event] line %d: %s\n" % (lineno, reason))
    sys.stderr.flush()


def _configure_streams():
    # The stream is UTF-8 whatever the locale says; a C locale would otherwise
    # choke on the first CJK character in a review.
    settings = (
        (sys.stdin, "replace"),
        (sys.stdout, "replace"),
        (sys.stderr, "backslashreplace"),
    )
    for stream, errors in settings:
        if stream is not None and hasattr(stream, "reconfigure"):
            try:
                stream.reconfigure(encoding="utf-8", errors=errors)
            except Exception:
                pass


def main():
    _configure_streams()

    done = 0
    spoke = 0
    failed = False
    malformed = False
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
                        print(text, flush=True)
                elif itype == "command_execution":
                    command = _optional_text(item, "command", "command_execution command")
                    if command is not None:
                        print("<!-- codex ran: %s -->" % command[:160], flush=True)
                elif itype == "error":
                    message = _optional_text(item, "message", "error item message")
                    if message is not None:
                        print("[codex item error] " + message, file=sys.stderr, flush=True)
            elif t == "error":
                failed = True
                print("[codex error] " + str(obj.get("message", "")), file=sys.stderr, flush=True)
            elif t == "turn.completed":
                u = obj.get("usage", _MISSING)
                if u is _MISSING:
                    u = {}
                if not isinstance(u, dict):
                    raise Malformed("usage must be an object, got %s" % type(u).__name__)
                counts = []
                problems = []
                for key in ("input_tokens", "output_tokens"):
                    value = u.get(key, _MISSING)
                    if value is _MISSING:
                        counts.append(0)
                    elif _is_nonneg_int(value):
                        counts.append(value)
                    else:
                        problems.append("usage.%s must be a non-negative integer" % key)
                if problems:
                    raise Malformed("; ".join(problems))
                done += 1
                print("\n<!-- tokens: in %s out %s -->" % (counts[0], counts[1]), flush=True)
            elif t == "turn.failed":
                failed = True
                msg = "no message"
                reason = None
                err = obj.get("error", _MISSING)
                if err is _MISSING or err is None:
                    pass
                elif isinstance(err, dict):
                    m = err.get("message", _MISSING)
                    if m is _MISSING or m is None or m == "":
                        pass
                    elif isinstance(m, str):
                        msg = m
                    else:
                        reason = "turn.failed error.message must be a string, got %s" % type(m).__name__
                else:
                    reason = "turn.failed error must be an object, got %s" % type(err).__name__
                if reason is not None:
                    malformed = True
                    _report_malformed(lineno, reason)
                print("[codex turn FAILED] " + msg, file=sys.stderr, flush=True)
            # Any other string event type is an ignored extension.
        except Malformed as exc:
            malformed = True
            _report_malformed(lineno, exc)
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


if __name__ == "__main__":
    main()
