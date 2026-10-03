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


def _describe(value):
    """Name a decoded JSON value's type for a single-line diagnostic."""
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


def _optional_text(container, key, label):
    """Return (text_or_None, problem_or_None).

    Absent, null and empty string all mean "no text"; any other non-string is a
    problem. A nonempty string is returned unchanged.
    """
    if key not in container:
        return None, None
    value = container[key]
    if value is None:
        return None, None
    if isinstance(value, str):
        if value == "":
            return None, None
        return value, None
    return None, "%s must be a string, got %s" % (label, _describe(value))


def _token_count(usage, key):
    """Return (count, problem_or_None) for a usage token field."""
    if key not in usage:
        return 0, None
    value = usage[key]
    if type(value) is not int:
        return None, "usage.%s must be a non-negative integer, got %s" % (key, _describe(value))
    if value < 0:
        return None, "usage.%s must be a non-negative integer, got a negative value" % key
    return value, None


def _reconfigure():
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
                stream.reconfigure(encoding="utf-8", errors="backslashreplace")
            except Exception:
                pass


def main():
    _reconfigure()

    state = {"malformed": False}

    def malformed(lineno, reason):
        state["malformed"] = True
        reason = " ".join(str(reason).split()) or "malformed event"
        sys.stderr.write("[codex malformed event] line %d: %s\n" % (lineno, reason))
        sys.stderr.flush()

    done = 0
    spoke = 0
    failed = False
    lineno = 0
    readline = sys.stdin.readline
    while True:
        raw = readline()
        if raw == "":
            break
        lineno += 1
        line = raw.strip()
        if not line:
            continue
        try:
            obj = json.loads(line)
        except (ValueError, RecursionError):
            continue

        if not isinstance(obj, dict):
            malformed(lineno, "event must be a JSON object, got %s" % _describe(obj))
            continue
        if "type" not in obj:
            continue
        t = obj["type"]
        if not isinstance(t, str):
            malformed(lineno, "event type must be a string, got %s" % _describe(t))
            continue

        if t == "item.completed":
            if "item" not in obj:
                continue
            item = obj["item"]
            if not isinstance(item, dict):
                malformed(lineno, "item must be an object, got %s" % _describe(item))
                continue
            if "type" not in item:
                continue
            itype = item["type"]
            if not isinstance(itype, str):
                malformed(lineno, "item type must be a string, got %s" % _describe(itype))
                continue
            if itype == "agent_message":
                text, problem = _optional_text(item, "text", "agent_message text")
                if problem:
                    malformed(lineno, problem)
                    continue
                if text is not None:
                    spoke += 1
                    print(text, flush=True)
            elif itype == "command_execution":
                command, problem = _optional_text(item, "command", "command_execution command")
                if problem:
                    malformed(lineno, problem)
                    continue
                if command is not None:
                    print("<!-- codex ran: %s -->" % command[:160], flush=True)
            elif itype == "error":
                message, problem = _optional_text(item, "message", "error item message")
                if problem:
                    malformed(lineno, problem)
                    continue
                if message is not None:
                    print("[codex item error] " + message, file=sys.stderr, flush=True)
            # Unknown string item types are ignored without inspection.
        elif t == "error":
            failed = True
            print("[codex error] " + str(obj.get("message", "")), file=sys.stderr, flush=True)
        elif t == "turn.completed":
            if "usage" in obj:
                usage = obj["usage"]
            else:
                usage = {}
            if not isinstance(usage, dict):
                malformed(lineno, "usage must be an object, got %s" % _describe(usage))
                continue
            tin, problem = _token_count(usage, "input_tokens")
            if problem:
                malformed(lineno, problem)
                continue
            tout, problem = _token_count(usage, "output_tokens")
            if problem:
                malformed(lineno, problem)
                continue
            done += 1
            print("\n<!-- tokens: in %s out %s -->" % (tin, tout), flush=True)
        elif t == "turn.failed":
            failed = True
            msg = "no message"
            problem = None
            if "error" in obj and obj["error"] is not None:
                err = obj["error"]
                if isinstance(err, dict):
                    text, problem = _optional_text(err, "message", "turn.failed error.message")
                    if problem is None and text is not None:
                        msg = text
                else:
                    problem = "turn.failed error must be an object, got %s" % _describe(err)
            if problem:
                malformed(lineno, problem)
            print("[codex turn FAILED] " + msg, file=sys.stderr, flush=True)
        # Unknown string event types are ignored without inspecting their payload.

    if failed:
        print("[codex] the turn failed (reason above); no review was produced.", file=sys.stderr, flush=True)
        sys.exit(3)
    if state["malformed"]:
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
