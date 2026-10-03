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
    6  a valid-JSON event had the wrong shape (malformed event); not a review
"""
import json
import sys


_MISSING = object()


def _is_count(value):
    return isinstance(value, int) and not isinstance(value, bool) and value >= 0


def _describe(value):
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


class _Parser(object):
    def __init__(self):
        self.done = 0
        self.spoke = 0
        self.failed = False
        self.malformed = False

    def report_malformed(self, lineno, reason):
        self.malformed = True
        reason = " ".join(str(reason).split()) or "malformed event"
        print("[codex malformed event] line %d: %s" % (lineno, reason), file=sys.stderr, flush=True)

    def handle_line(self, lineno, line):
        line = line.strip()
        if not line:
            return
        try:
            obj = json.loads(line)
        except (ValueError, RecursionError):
            return
        if not isinstance(obj, dict):
            self.report_malformed(lineno, "event is a JSON %s, not an object" % _describe(obj))
            return
        t = obj.get("type", _MISSING)
        if t is _MISSING:
            return
        if not isinstance(t, str):
            self.report_malformed(lineno, "event type is a %s, not a string" % _describe(t))
            return
        if t == "item.completed":
            self.handle_item(lineno, obj)
        elif t == "error":
            self.failed = True
            print("[codex error] " + str(obj.get("message", "")), file=sys.stderr, flush=True)
        elif t == "turn.completed":
            self.handle_turn_completed(lineno, obj)
        elif t == "turn.failed":
            self.handle_turn_failed(lineno, obj)

    def handle_item(self, lineno, obj):
        item = obj.get("item", _MISSING)
        if item is _MISSING:
            return
        if not isinstance(item, dict):
            self.report_malformed(lineno, "item.completed item is a %s, not an object" % _describe(item))
            return
        itype = item.get("type", _MISSING)
        if itype is _MISSING:
            return
        if not isinstance(itype, str):
            self.report_malformed(lineno, "item type is a %s, not a string" % _describe(itype))
            return
        if itype == "agent_message":
            text = item.get("text", None)
            if text is None or text == "":
                return
            if not isinstance(text, str):
                self.report_malformed(lineno, "agent_message text is a %s, not a string" % _describe(text))
                return
            self.spoke += 1
            print(text, flush=True)
        elif itype == "command_execution":
            command = item.get("command", None)
            if command is None or command == "":
                return
            if not isinstance(command, str):
                self.report_malformed(lineno, "command_execution command is a %s, not a string"
                                      % _describe(command))
                return
            print("<!-- codex ran: %s -->" % command[:160], flush=True)
        elif itype == "error":
            message = item.get("message", None)
            if message is None or message == "":
                return
            if not isinstance(message, str):
                self.report_malformed(lineno, "error item message is a %s, not a string" % _describe(message))
                return
            print("[codex item error] " + message, file=sys.stderr, flush=True)

    def handle_turn_completed(self, lineno, obj):
        usage = obj.get("usage", _MISSING)
        if usage is _MISSING:
            usage = {}
        if not isinstance(usage, dict):
            self.report_malformed(lineno, "turn.completed usage is a %s, not an object" % _describe(usage))
            return
        counts = []
        for key in ("input_tokens", "output_tokens"):
            value = usage.get(key, _MISSING)
            if value is _MISSING:
                value = 0
            if not _is_count(value):
                self.report_malformed(lineno, "usage %s is not a non-negative integer (%s)"
                                      % (key, _describe(value)))
                return
            counts.append(value)
        self.done += 1
        print("\n<!-- tokens: in %s out %s -->" % (counts[0], counts[1]), flush=True)

    def handle_turn_failed(self, lineno, obj):
        self.failed = True
        msg = "no message"
        error = obj.get("error", None)
        if error is not None:
            if not isinstance(error, dict):
                self.report_malformed(lineno, "turn.failed error is a %s, not an object" % _describe(error))
            else:
                message = error.get("message", None)
                if message is None or message == "":
                    pass
                elif isinstance(message, str):
                    msg = message
                else:
                    self.report_malformed(lineno, "turn.failed error message is a %s, not a string"
                                          % _describe(message))
        print("[codex turn FAILED] " + msg, file=sys.stderr, flush=True)


def _reconfigure(stream, errors):
    if hasattr(stream, "reconfigure"):
        try:
            stream.reconfigure(encoding="utf-8", errors=errors)
        except Exception:
            try:
                stream.reconfigure(encoding="utf-8")
            except Exception:
                pass


def main():
    # The stream is UTF-8 whatever the locale says; a C locale would otherwise
    # choke on the first CJK character in a review.
    _reconfigure(sys.stdin, "replace")
    _reconfigure(sys.stdout, "replace")
    _reconfigure(sys.stderr, "backslashreplace")

    parser = _Parser()
    for lineno, line in enumerate(sys.stdin, 1):
        try:
            parser.handle_line(lineno, line)
        except (BrokenPipeError, KeyboardInterrupt):
            raise
        except Exception as exc:  # never let one event kill the stream
            parser.report_malformed(lineno, "could not process event (%s)" % type(exc).__name__)

    if parser.failed:
        print("[codex] the turn failed (reason above); no review was produced.", file=sys.stderr, flush=True)
        sys.exit(3)
    if parser.malformed:
        sys.exit(6)
    if parser.done == 0:
        print("[codex] no turn.completed event: possible mid-stream disconnect.", file=sys.stderr, flush=True)
        sys.exit(4)
    if parser.spoke == 0:
        print("[codex] the turn completed without an agent message; no review was produced.",
              file=sys.stderr, flush=True)
        sys.exit(5)


if __name__ == "__main__":
    main()
