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
    """A decoded JSON line whose structure does not match the expected types."""


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


def _optional_text(container, key, where):
    """Return a nonempty string, or None for absent/null/empty; raise on wrong type."""
    if key not in container:
        return None
    value = container[key]
    if value is None:
        return None
    if not isinstance(value, str):
        raise Malformed("%s.%s must be a string, got %s" % (where, key, _type_name(value)))
    if value == "":
        return None
    return value


def _token_count(usage, key):
    if key not in usage:
        return 0
    value = usage[key]
    if type(value) is not int:
        raise Malformed("usage.%s must be a non-negative integer, got %s" % (key, _type_name(value)))
    if value < 0:
        raise Malformed("usage.%s must be a non-negative integer, got a negative value" % key)
    return value


def _malformed(lineno, reason):
    reason = " ".join(str(reason).split()) or "malformed event"
    sys.stderr.write("[codex malformed event] line %d: %s\n" % (lineno, reason))
    sys.stderr.flush()


def _out(text):
    print(text, flush=True)


def _err(text):
    print(text, file=sys.stderr, flush=True)


def main():
    # The stream is UTF-8 whatever the locale says; a C locale would otherwise
    # choke on the first CJK character in a review.
    if hasattr(sys.stdin, "reconfigure"):
        try:
            sys.stdin.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass
    if hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass
    if hasattr(sys.stderr, "reconfigure"):
        try:
            sys.stderr.reconfigure(encoding="utf-8", errors="backslashreplace")
        except Exception:
            pass

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

        if not isinstance(obj, dict):
            malformed = True
            _malformed(lineno, "event must be a JSON object, got %s" % _type_name(obj))
            continue
        if "type" not in obj:
            continue
        t = obj["type"]
        if not isinstance(t, str):
            malformed = True
            _malformed(lineno, "event type must be a string, got %s" % _type_name(t))
            continue

        if t == "item.completed":
            try:
                item = obj.get("item", {})
                if not isinstance(item, dict):
                    raise Malformed("item must be an object, got %s" % _type_name(item))
                if "type" not in item:
                    continue
                itype = item["type"]
                if not isinstance(itype, str):
                    raise Malformed("item.type must be a string, got %s" % _type_name(itype))
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
                    raise Malformed("usage must be an object, got %s" % _type_name(usage))
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
            problem = None
            if "error" in obj and obj["error"] is not None:
                err = obj["error"]
                if isinstance(err, dict):
                    try:
                        found = _optional_text(err, "message", "error")
                        if found is not None:
                            msg = found
                    except Malformed as exc:
                        problem = str(exc)
                else:
                    problem = "error must be an object, got %s" % _type_name(err)
            if problem is not None:
                malformed = True
                _malformed(lineno, problem)
            _err("[codex turn FAILED] " + msg)
        # Unknown string event types are ignored without inspecting payloads.

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
