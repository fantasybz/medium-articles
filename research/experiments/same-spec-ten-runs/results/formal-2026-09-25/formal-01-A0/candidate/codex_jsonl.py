"""Stream-parse `codex exec --json` output: print the agent's messages as they complete.

Kept in its own file because embedding this in a bash single-quoted `python3 -c`
string broke on the escaped quotes (the first run of codex_review.sh died with a
SyntaxError, which closed the pipe and made codex panic on stdout).

Prints agent messages to stdout (they become the review file), and everything
diagnostic (`turn.failed`, `error` events, missing `turn.completed`) to stderr so
the caller can tell "Codex said nothing" from "Codex was refused".

Valid JSON with the wrong shape (a non-object line, a non-string `type`, a
non-string agent `text`, bad token counts, ...) is reported on stderr as
`[codex malformed event] line N: REASON` and never becomes a successful review.

Exit codes codex_review.sh branches on:
    0  at least one agent message and a completed turn
    3  the turn failed or an error event arrived (refusal, usage limit)
    4  no turn.completed: a mid-stream disconnect
    5  the turn completed but Codex never spoke; the "review" would be a token count
    6  a malformed (valid JSON, wrong shape) event arrived
"""
import json
import sys


_MISSING = object()


def _out(text):
    sys.stdout.write(text)
    sys.stdout.flush()


def _err(text):
    sys.stderr.write(text)
    sys.stderr.flush()


def _single_line(text):
    text = " ".join(str(text).splitlines()).strip()
    return text or "malformed event"


def _is_token_count(value):
    return isinstance(value, int) and not isinstance(value, bool) and value >= 0


def _type_name(value):
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


def main():
    # The stream is UTF-8 whatever the locale says; a C locale would otherwise
    # choke on the first CJK character in a review.
    if hasattr(sys.stdin, "reconfigure"):
        sys.stdin.reconfigure(encoding="utf-8", errors="replace")
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="backslashreplace")

    state = {"malformed": False}
    done = 0
    spoke = 0
    failed = False

    def malformed(lineno, reason):
        state["malformed"] = True
        _err("[codex malformed event] line %d: %s\n" % (lineno, _single_line(reason)))

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
            malformed(lineno, "event is a JSON %s, not an object" % _type_name(obj))
            continue
        if "type" not in obj:
            continue
        t = obj["type"]
        if not isinstance(t, str):
            malformed(lineno, "event type is a %s, not a string" % _type_name(t))
            continue

        if t == "item.completed":
            item = obj.get("item", _MISSING)
            if item is _MISSING:
                item = {}
            if not isinstance(item, dict):
                malformed(lineno, "item.completed item is a %s, not an object" % _type_name(item))
                continue
            if "type" not in item:
                continue
            itype = item["type"]
            if not isinstance(itype, str):
                malformed(lineno, "item type is a %s, not a string" % _type_name(itype))
                continue
            if itype == "agent_message":
                text = item.get("text", None)
                if text is None:
                    continue
                if not isinstance(text, str):
                    malformed(lineno, "agent_message text is a %s, not a string" % _type_name(text))
                    continue
                if text == "":
                    continue
                spoke += 1
                _out(text + "\n")
            elif itype == "command_execution":
                command = item.get("command", None)
                if command is None:
                    continue
                if not isinstance(command, str):
                    malformed(lineno, "command_execution command is a %s, not a string" % _type_name(command))
                    continue
                if command == "":
                    continue
                _out("<!-- codex ran: " + command[:160] + " -->\n")
            elif itype == "error":
                message = item.get("message", None)
                if message is None:
                    continue
                if not isinstance(message, str):
                    malformed(lineno, "error item message is a %s, not a string" % _type_name(message))
                    continue
                if message == "":
                    continue
                _err("[codex item error] " + message + "\n")
            # Unknown item types are ignored.
        elif t == "error":
            failed = True
            _err("[codex error] " + str(obj.get("message", "")) + "\n")
        elif t == "turn.completed":
            usage = obj.get("usage", _MISSING)
            if usage is _MISSING:
                usage = {}
            if not isinstance(usage, dict):
                malformed(lineno, "turn.completed usage is a %s, not an object" % _type_name(usage))
                continue
            bad = None
            counts = []
            for key in ("input_tokens", "output_tokens"):
                value = usage.get(key, 0)
                if not _is_token_count(value):
                    bad = "usage %s is not a non-negative integer" % key
                    break
                counts.append(value)
            if bad is not None:
                malformed(lineno, bad)
                continue
            done += 1
            _out("\n<!-- tokens: in %d out %d -->\n" % (counts[0], counts[1]))
        elif t == "turn.failed":
            failed = True
            msg = "no message"
            error = obj.get("error", None)
            if error is None:
                pass
            elif not isinstance(error, dict):
                malformed(lineno, "turn.failed error is a %s, not an object" % _type_name(error))
            else:
                message = error.get("message", None)
                if message is None or message == "":
                    pass
                elif not isinstance(message, str):
                    malformed(lineno, "turn.failed error message is a %s, not a string" % _type_name(message))
                else:
                    msg = message
            _err("[codex turn FAILED] " + msg + "\n")
        # Unknown event types are ignored.

    if failed:
        _err("[codex] the turn failed (reason above); no review was produced.\n")
        sys.exit(3)
    if state["malformed"]:
        sys.exit(6)
    if done == 0:
        _err("[codex] no turn.completed event: possible mid-stream disconnect.\n")
        sys.exit(4)
    if spoke == 0:
        _err("[codex] the turn completed without an agent message; no review was produced.\n")
        sys.exit(5)
    sys.exit(0)


if __name__ == "__main__":
    main()
