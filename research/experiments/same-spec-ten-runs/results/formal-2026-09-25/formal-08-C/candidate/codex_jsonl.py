"""Stream-parse `codex exec --json` output: print the agent's messages as they complete.

Kept in its own file because embedding this in a bash single-quoted `python3 -c`
string broke on the escaped quotes (the first run of codex_review.sh died with a
SyntaxError, which closed the pipe and made codex panic on stdout).

Prints agent messages to stdout (they become the review file), and everything
diagnostic (`turn.failed`, `error` events, missing `turn.completed`) to stderr so
the caller can tell "Codex said nothing" from "Codex was refused".

Valid JSON whose structure does not match what a recognized event requires is
reported on stderr as `[codex malformed event] line N: REASON` and dropped; the
stream keeps being processed so later remote errors are still observed.

Exit codes codex_review.sh branches on:
    0  at least one agent message and a completed turn
    3  the turn failed or an error event arrived (refusal, usage limit)
    4  no turn.completed: a mid-stream disconnect
    5  the turn completed but Codex never spoke; the "review" would be a token count
    6  a malformed event arrived (and no explicit remote failure)
"""
import json
import sys


_MISSING = object()


def _out(text):
    print(text, flush=True)


def _err(text):
    print(text, file=sys.stderr, flush=True)


def _report_malformed(lineno, reason):
    reason = " ".join(str(reason).split()) or "malformed event"
    _err("[codex malformed event] line %d: %s" % (lineno, reason))


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


def _optional_text(container, key):
    """Return (text, problem). text is '' for absent/null/empty; problem is a reason string."""
    value = container.get(key, _MISSING)
    if value is _MISSING or value is None:
        return "", None
    if isinstance(value, str):
        return value, None
    return "", "%s must be a string, got %s" % (key, _type_name(value))


def _token_count(usage, key):
    value = usage.get(key, _MISSING)
    if value is _MISSING:
        return 0, None
    if type(value) is int and value >= 0:
        return value, None
    if type(value) is int:
        return None, "usage.%s must be a non-negative integer, got a negative integer" % key
    return None, "usage.%s must be a non-negative integer, got %s" % (key, _type_name(value))


def _reconfigure():
    # The stream is UTF-8 whatever the locale says; a C locale would otherwise
    # choke on the first CJK character in a review.
    for stream, errors in ((sys.stdin, "replace"), (sys.stdout, "backslashreplace"),
                           (sys.stderr, "backslashreplace")):
        if hasattr(stream, "reconfigure"):
            try:
                stream.reconfigure(encoding="utf-8", errors=errors)
            except Exception:
                try:
                    stream.reconfigure(encoding="utf-8")
                except Exception:
                    pass


def main():
    _reconfigure()

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

        if not isinstance(obj, dict):
            malformed = True
            _report_malformed(lineno, "event must be a JSON object, got %s" % _type_name(obj))
            continue
        if "type" not in obj:
            continue
        t = obj["type"]
        if not isinstance(t, str):
            malformed = True
            _report_malformed(lineno, "event type must be a string, got %s" % _type_name(t))
            continue

        if t == "item.completed":
            item = obj.get("item", _MISSING)
            if item is _MISSING:
                continue
            if not isinstance(item, dict):
                malformed = True
                _report_malformed(lineno, "item must be an object, got %s" % _type_name(item))
                continue
            if "type" not in item:
                continue
            itype = item["type"]
            if not isinstance(itype, str):
                malformed = True
                _report_malformed(lineno, "item type must be a string, got %s" % _type_name(itype))
                continue
            if itype == "agent_message":
                text, problem = _optional_text(item, "text")
                if problem:
                    malformed = True
                    _report_malformed(lineno, "agent_message " + problem)
                    continue
                if text:
                    spoke += 1
                    _out(text)
            elif itype == "command_execution":
                command, problem = _optional_text(item, "command")
                if problem:
                    malformed = True
                    _report_malformed(lineno, "command_execution " + problem)
                    continue
                if command:
                    _out("<!-- codex ran: %s -->" % command[:160])
            elif itype == "error":
                message, problem = _optional_text(item, "message")
                if problem:
                    malformed = True
                    _report_malformed(lineno, "error item " + problem)
                    continue
                if message:
                    _err("[codex item error] " + message)
            # unknown string item types are ignored
        elif t == "error":
            failed = True
            _err("[codex error] " + str(obj.get("message", "")))
        elif t == "turn.completed":
            usage = obj.get("usage", _MISSING)
            if usage is _MISSING:
                usage = {}
            if not isinstance(usage, dict):
                malformed = True
                _report_malformed(lineno, "usage must be an object, got %s" % _type_name(usage))
                continue
            in_tokens, problem_in = _token_count(usage, "input_tokens")
            out_tokens, problem_out = _token_count(usage, "output_tokens")
            problem = problem_in or problem_out
            if problem:
                malformed = True
                _report_malformed(lineno, problem)
                continue
            done += 1
            _out("\n<!-- tokens: in %d out %d -->" % (in_tokens, out_tokens))
        elif t == "turn.failed":
            failed = True
            msg = "no message"
            problem = None
            error = obj.get("error", _MISSING)
            if error is _MISSING or error is None:
                pass
            elif isinstance(error, dict):
                message, problem = _optional_text(error, "message")
                if problem:
                    problem = "turn.failed error." + problem
                elif message:
                    msg = message
            else:
                problem = "turn.failed error must be an object, got %s" % _type_name(error)
            if problem:
                malformed = True
                _report_malformed(lineno, problem)
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
