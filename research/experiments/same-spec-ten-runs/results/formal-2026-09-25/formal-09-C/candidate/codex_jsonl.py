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
    """Raised to report a single malformed-event reason for one line."""


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


def _optional_text(container, key, where):
    """Return a nonempty string, or None for absent/null/empty; raise on wrong type."""
    value = container.get(key, _MISSING)
    if value is _MISSING or value is None:
        return None
    if isinstance(value, str):
        return value if value else None
    raise Malformed("%s.%s must be a string, got %s" % (where, key, _type_name(value)))


def _usage_counts(event):
    """Validate the whole usage object; return (input_tokens, output_tokens)."""
    usage = event.get("usage", _MISSING)
    if usage is _MISSING:
        usage = {}
    if not isinstance(usage, dict):
        raise Malformed("usage must be an object, got %s" % _type_name(usage))
    counts = []
    problems = []
    for key in ("input_tokens", "output_tokens"):
        value = usage.get(key, _MISSING)
        if value is _MISSING:
            counts.append(0)
            continue
        if type(value) is not int or value < 0:
            problems.append("usage.%s must be a non-negative integer, got %s"
                            % (key, _type_name(value)))
            continue
        counts.append(value)
    if problems:
        raise Malformed("; ".join(problems))
    return counts[0], counts[1]


def _malformed(lineno, reason):
    reason = " ".join(str(reason).split()) or "malformed event"
    print("[codex malformed event] line %d: %s" % (lineno, reason), file=sys.stderr, flush=True)


def _setup_streams():
    # The stream is UTF-8 whatever the locale says; a C locale would otherwise
    # choke on the first CJK character in a review.
    if hasattr(sys.stdin, "reconfigure"):
        sys.stdin.reconfigure(encoding="utf-8")
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8", errors="backslashreplace")


def main():
    _setup_streams()

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
                raise Malformed("event must be a JSON object, got %s" % _type_name(obj))
            t = obj.get("type", _MISSING)
            if t is _MISSING:
                continue
            if not isinstance(t, str):
                raise Malformed("event type must be a string, got %s" % _type_name(t))

            if t == "item.completed":
                item = obj.get("item", _MISSING)
                if item is _MISSING:
                    item = {}
                if not isinstance(item, dict):
                    raise Malformed("item must be an object, got %s" % _type_name(item))
                itype = item.get("type", _MISSING)
                if itype is _MISSING:
                    continue
                if not isinstance(itype, str):
                    raise Malformed("item.type must be a string, got %s" % _type_name(itype))
                if itype == "agent_message":
                    text = _optional_text(item, "text", "item")
                    if text is not None:
                        spoke += 1
                        print(text, flush=True)
                elif itype == "command_execution":
                    command = _optional_text(item, "command", "item")
                    if command is not None:
                        print("<!-- codex ran: %s -->" % command[:160], flush=True)
                elif itype == "error":
                    message = _optional_text(item, "message", "item")
                    if message is not None:
                        print("[codex item error] " + message, file=sys.stderr, flush=True)

            elif t == "error":
                failed = True
                print("[codex error] " + str(obj.get("message", "")), file=sys.stderr, flush=True)

            elif t == "turn.completed":
                in_tokens, out_tokens = _usage_counts(obj)
                done += 1
                print("\n<!-- tokens: in %s out %s -->" % (in_tokens, out_tokens), flush=True)

            elif t == "turn.failed":
                failed = True
                msg = "no message"
                problem = None
                err = obj.get("error", _MISSING)
                if err is _MISSING or err is None:
                    pass
                elif isinstance(err, dict):
                    try:
                        text = _optional_text(err, "message", "error")
                    except Malformed as exc:
                        problem = str(exc)
                    else:
                        if text is not None:
                            msg = text
                else:
                    problem = "error must be an object, got %s" % _type_name(err)
                if problem is not None:
                    malformed = True
                    _malformed(lineno, problem)
                print("[codex turn FAILED] " + msg, file=sys.stderr, flush=True)
            # Any other string event type is an extension point: ignore it.
        except Malformed as exc:
            malformed = True
            _malformed(lineno, str(exc))

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
