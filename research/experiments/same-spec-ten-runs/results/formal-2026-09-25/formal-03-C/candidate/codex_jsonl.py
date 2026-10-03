"""Stream-parse `codex exec --json` output: print the agent's messages as they complete.

Kept in its own file because embedding this in a bash single-quoted `python3 -c`
string broke on the escaped quotes (the first run of codex_review.sh died with a
SyntaxError, which closed the pipe and made codex panic on stdout).

Prints agent messages to stdout (they become the review file), and everything
diagnostic (`turn.failed`, `error` events, missing `turn.completed`, malformed
events) to stderr so the caller can tell "Codex said nothing" from "Codex was
refused".

Valid JSON whose structure does not match the expected event schema is reported
per line as `[codex malformed event] line N: REASON` and then skipped; the stream
keeps being processed so later remote errors are still observed.

Exit codes codex_review.sh branches on:
    0  at least one agent message and a completed turn
    3  the turn failed or an error event arrived (refusal, usage limit)
    6  a malformed event arrived (and no explicit remote failure)
    4  no turn.completed: a mid-stream disconnect
    5  the turn completed but Codex never spoke; the "review" would be a token count
"""
import json
import sys


class Malformed(Exception):
    """A decoded JSON line whose structure does not match the event schema."""


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


def _opt_text(mapping, key, label):
    """Return a nonempty string, or None for absent/null/empty; raise on wrong type."""
    value = mapping.get(key)
    if value is None:
        return None
    if not isinstance(value, str):
        raise Malformed("%s is %s, expected a string" % (label, _kind(value)))
    if value == "":
        return None
    return value


def _token_count(usage, key):
    if key not in usage:
        return 0
    value = usage[key]
    if type(value) is not int:
        raise Malformed("usage.%s is %s, expected a non-negative integer" % (key, _kind(value)))
    if value < 0:
        raise Malformed("usage.%s is negative, expected a non-negative integer" % key)
    return value


def _report_malformed(lineno, reason):
    reason = " ".join(str(reason).split()) or "malformed event"
    print("[codex malformed event] line %d: %s" % (lineno, reason), file=sys.stderr, flush=True)


def main():
    # The stream is UTF-8 whatever the locale says; a C locale would otherwise
    # choke on the first CJK character in a review.
    for stream in (sys.stdin, sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            try:
                stream.reconfigure(encoding="utf-8", errors="replace")
            except Exception:
                try:
                    stream.reconfigure(encoding="utf-8")
                except Exception:
                    pass

    done = 0
    spoke = 0
    failed = False
    malformed = False

    lineno = 0
    readline = sys.stdin.readline
    while True:
        raw = readline()
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
                raise Malformed("event is %s, expected an object" % _kind(obj))
            if "type" not in obj:
                continue
            t = obj["type"]
            if not isinstance(t, str):
                raise Malformed("event type is %s, expected a string" % _kind(t))

            if t == "item.completed":
                item = obj.get("item", {})
                if not isinstance(item, dict):
                    raise Malformed("item is %s, expected an object" % _kind(item))
                if "type" not in item:
                    continue
                itype = item["type"]
                if not isinstance(itype, str):
                    raise Malformed("item type is %s, expected a string" % _kind(itype))
                if itype == "agent_message":
                    text = _opt_text(item, "text", "agent_message text")
                    if text is not None:
                        spoke += 1
                        print(text, flush=True)
                elif itype == "command_execution":
                    command = _opt_text(item, "command", "command_execution command")
                    if command is not None:
                        print("<!-- codex ran: %s -->" % (command[:160],), flush=True)
                elif itype == "error":
                    message = _opt_text(item, "message", "error item message")
                    if message is not None:
                        print("[codex item error] " + message, file=sys.stderr, flush=True)
            elif t == "error":
                failed = True
                print("[codex error] " + str(obj.get("message", "")), file=sys.stderr, flush=True)
            elif t == "turn.completed":
                usage = obj.get("usage", {})
                if not isinstance(usage, dict):
                    raise Malformed("usage is %s, expected an object" % _kind(usage))
                tokens_in = _token_count(usage, "input_tokens")
                tokens_out = _token_count(usage, "output_tokens")
                done += 1
                print("\n<!-- tokens: in %d out %d -->" % (tokens_in, tokens_out), flush=True)
            elif t == "turn.failed":
                failed = True
                msg = "no message"
                problem = None
                err = obj.get("error")
                if err is None:
                    pass
                elif isinstance(err, dict):
                    m = err.get("message")
                    if m is None:
                        pass
                    elif isinstance(m, str):
                        if m != "":
                            msg = m
                    else:
                        problem = "turn.failed error.message is %s, expected a string" % _kind(m)
                else:
                    problem = "turn.failed error is %s, expected an object" % _kind(err)
                if problem is not None:
                    malformed = True
                    _report_malformed(lineno, problem)
                print("[codex turn FAILED] " + msg, file=sys.stderr, flush=True)
            # Any other string event type is an extension point: ignore it.
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
