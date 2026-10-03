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


def _optional_text(mapping, key, where):
    """Return (text_or_None, problem_or_None).

    Absent, null and empty string mean "no text" without a problem. A
    nonempty string is returned unchanged. Any other value is a problem.
    """
    value = mapping.get(key, _MISSING)
    if value is _MISSING or value is None:
        return None, None
    if isinstance(value, str):
        if value == "":
            return None, None
        return value, None
    return None, "%s.%s must be a string, got %s" % (where, key, _type_name(value))


def _validate_usage(event):
    """Return ((in_tokens, out_tokens), None) or (None, problem)."""
    usage = event.get("usage", _MISSING)
    if usage is _MISSING:
        usage = {}
    if not isinstance(usage, dict):
        return None, "turn.completed usage must be an object, got %s" % _type_name(usage)
    counts = []
    for key in ("input_tokens", "output_tokens"):
        value = usage.get(key, _MISSING)
        if value is _MISSING:
            counts.append(0)
            continue
        if type(value) is not int or value < 0:
            if type(value) is int:
                return None, "usage.%s must be a non-negative integer, got a negative integer" % key
            return None, "usage.%s must be a non-negative integer, got %s" % (key, _type_name(value))
        counts.append(value)
    return (counts[0], counts[1]), None


def _malformed(line_no, reason):
    reason = " ".join(str(reason).split()) or "malformed event"
    sys.stderr.write("[codex malformed event] line %d: %s\n" % (line_no, reason))
    sys.stderr.flush()


def _out(text):
    sys.stdout.write(text + "\n")
    sys.stdout.flush()


def _err(text):
    sys.stderr.write(text + "\n")
    sys.stderr.flush()


def main():
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

    done = 0
    spoke = 0
    failed = False
    malformed = False
    line_no = 0

    while True:
        raw = sys.stdin.readline()
        if raw == "":
            break
        line_no += 1
        line = raw.strip()
        if not line:
            continue
        try:
            obj = json.loads(line)
        except (ValueError, RecursionError):
            continue

        if not isinstance(obj, dict):
            malformed = True
            _malformed(line_no, "event must be a JSON object, got %s" % _type_name(obj))
            continue

        t = obj.get("type", _MISSING)
        if t is _MISSING:
            continue
        if not isinstance(t, str):
            malformed = True
            _malformed(line_no, "event type must be a string, got %s" % _type_name(t))
            continue

        if t == "item.completed":
            item = obj.get("item", _MISSING)
            if item is _MISSING:
                continue
            if not isinstance(item, dict):
                malformed = True
                _malformed(line_no, "item.completed item must be an object, got %s" % _type_name(item))
                continue
            itype = item.get("type", _MISSING)
            if itype is _MISSING:
                continue
            if not isinstance(itype, str):
                malformed = True
                _malformed(line_no, "item type must be a string, got %s" % _type_name(itype))
                continue
            if itype == "agent_message":
                text, problem = _optional_text(item, "text", "item")
                if problem:
                    malformed = True
                    _malformed(line_no, problem)
                    continue
                if text is not None:
                    spoke += 1
                    _out(text)
            elif itype == "command_execution":
                command, problem = _optional_text(item, "command", "item")
                if problem:
                    malformed = True
                    _malformed(line_no, problem)
                    continue
                if command is not None:
                    _out("<!-- codex ran: %s -->" % command[:160])
            elif itype == "error":
                message, problem = _optional_text(item, "message", "item")
                if problem:
                    malformed = True
                    _malformed(line_no, problem)
                    continue
                if message is not None:
                    _err("[codex item error] " + message)
            # unknown string item types are ignored
        elif t == "error":
            failed = True
            _err("[codex error] " + str(obj.get("message", "")))
        elif t == "turn.completed":
            counts, problem = _validate_usage(obj)
            if problem:
                malformed = True
                _malformed(line_no, problem)
                continue
            done += 1
            _out("\n<!-- tokens: in %d out %d -->" % counts)
        elif t == "turn.failed":
            failed = True
            msg = "no message"
            problem = None
            err = obj.get("error", _MISSING)
            if err is _MISSING or err is None:
                pass
            elif isinstance(err, dict):
                text, problem = _optional_text(err, "message", "error")
                if text is not None:
                    msg = text
            else:
                problem = "turn.failed error must be an object, got %s" % _type_name(err)
            if problem:
                malformed = True
                _malformed(line_no, problem)
            _err("[codex turn FAILED] " + msg)
        # unknown string event types are ignored

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
