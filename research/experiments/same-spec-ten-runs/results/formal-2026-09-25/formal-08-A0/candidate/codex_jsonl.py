"""Stream-parse `codex exec --json` output: print the agent's messages as they complete.

Kept in its own file because embedding this in a bash single-quoted `python3 -c`
string broke on the escaped quotes (the first run of codex_review.sh died with a
SyntaxError, which closed the pipe and made codex panic on stdout).

Prints agent messages to stdout (they become the review file), and everything
diagnostic (`turn.failed`, `error` events, missing `turn.completed`) to stderr so
the caller can tell "Codex said nothing" from "Codex was refused".

Valid JSON with the wrong shape (a non-object line, a non-string type, a
non-string message text, bad token counts, ...) is reported on stderr as
`[codex malformed event] line N: REASON` and never crashes the parser.

Exit codes codex_review.sh branches on:
    0  at least one agent message and a completed turn
    3  the turn failed or an error event arrived (refusal, usage limit)
    4  no turn.completed: a mid-stream disconnect
    5  the turn completed but Codex never spoke; the "review" would be a token count
    6  a malformed (valid JSON, wrong shape) event arrived and nothing failed explicitly
"""
import json
import sys


_MISSING = object()


class _Malformed(Exception):
    """Raised while validating an event whose JSON shape is wrong."""


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


def _out(text):
    try:
        print(text, flush=True)
    except BrokenPipeError:
        pass


def _err(text):
    try:
        print(text, file=sys.stderr, flush=True)
    except BrokenPipeError:
        pass


def _iter_lines():
    """Yield decoded lines one at a time as they arrive; None for undecodable bytes."""
    buf = getattr(sys.stdin, "buffer", None)
    if buf is not None:
        for raw in buf:
            try:
                yield raw.decode("utf-8")
            except UnicodeDecodeError:
                yield None
    else:
        for line in sys.stdin:
            yield line


def _is_token_count(value):
    return isinstance(value, int) and not isinstance(value, bool) and value >= 0


def main():
    # The stream is UTF-8 whatever the locale says; a C locale would otherwise
    # choke on the first CJK character in a review.
    for stream in (sys.stdin, sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            try:
                if stream is sys.stdin:
                    stream.reconfigure(encoding="utf-8")
                else:
                    stream.reconfigure(encoding="utf-8", errors="backslashreplace")
            except Exception:
                pass

    done = 0
    spoke = 0
    failed = False
    malformed = False

    lineno = 0
    for line in _iter_lines():
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

        def report(reason, _n=lineno):
            reason = " ".join(str(reason).split()) or "malformed event"
            _err("[codex malformed event] line %d: %s" % (_n, reason))

        if not isinstance(obj, dict):
            malformed = True
            report("event is a JSON %s, not an object" % _type_name(obj))
            continue

        t = obj.get("type", _MISSING)
        if t is _MISSING:
            continue
        if not isinstance(t, str):
            malformed = True
            report("event type is a %s, not a string" % _type_name(t))
            continue

        if t == "turn.failed":
            failed = True
            msg = "no message"
            err = obj.get("error", None)
            if err is None:
                pass
            elif not isinstance(err, dict):
                malformed = True
                report("turn.failed error is a %s, not an object" % _type_name(err))
            else:
                m = err.get("message", None)
                if m is None or m == "":
                    pass
                elif isinstance(m, str):
                    msg = m
                else:
                    malformed = True
                    report("turn.failed error message is a %s, not a string" % _type_name(m))
            _err("[codex turn FAILED] " + msg)
            continue

        if t == "error":
            failed = True
            _err("[codex error] " + str(obj.get("message", "")))
            continue

        try:
            if t == "item.completed":
                item = obj.get("item", _MISSING)
                if item is _MISSING:
                    item = {}
                if not isinstance(item, dict):
                    raise _Malformed("item is a %s, not an object" % _type_name(item))
                itype = item.get("type", _MISSING)
                if itype is _MISSING:
                    continue
                if not isinstance(itype, str):
                    raise _Malformed("item type is a %s, not a string" % _type_name(itype))
                if itype == "agent_message":
                    text = item.get("text", None)
                    if text is None or text == "":
                        continue
                    if not isinstance(text, str):
                        raise _Malformed("agent_message text is a %s, not a string" % _type_name(text))
                    spoke += 1
                    _out(text)
                elif itype == "command_execution":
                    cmd = item.get("command", None)
                    if cmd is None or cmd == "":
                        continue
                    if not isinstance(cmd, str):
                        raise _Malformed("command_execution command is a %s, not a string" % _type_name(cmd))
                    _out("<!-- codex ran: %s -->" % cmd[:160])
                elif itype == "error":
                    m = item.get("message", None)
                    if m is None or m == "":
                        continue
                    if not isinstance(m, str):
                        raise _Malformed("error item message is a %s, not a string" % _type_name(m))
                    _err("[codex item error] " + m)
            elif t == "turn.completed":
                u = obj.get("usage", _MISSING)
                if u is _MISSING:
                    u = {}
                if not isinstance(u, dict):
                    raise _Malformed("usage is a %s, not an object" % _type_name(u))
                counts = []
                for key in ("input_tokens", "output_tokens"):
                    v = u.get(key, 0)
                    if not _is_token_count(v):
                        if isinstance(v, int) and not isinstance(v, bool):
                            raise _Malformed("usage %s is negative" % key)
                        raise _Malformed("usage %s is a %s, not a non-negative integer" % (key, _type_name(v)))
                    counts.append(v)
                done += 1
                _out("\n<!-- tokens: in %d out %d -->" % (counts[0], counts[1]))
        except _Malformed as exc:
            malformed = True
            report(str(exc))
            continue

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
