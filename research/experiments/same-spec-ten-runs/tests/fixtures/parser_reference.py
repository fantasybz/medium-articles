"""AI-authored TOOLING FIXTURE for R01--R13, not a study implementation.

Used only to validate the external evaluator and known-fault mutations. This is
not a human baseline, a formal model run, or a proposed production change.
"""
import json
import sys


class MalformedEvent(ValueError):
    pass


def optional_text(mapping, field):
    value = mapping.get(field)
    if value is None or value == "":
        return None
    if not isinstance(value, str):
        raise MalformedEvent(field + " must be a string or null")
    return value


def bad(line_number, reason):
    print(f"[codex malformed event] line {line_number}: {reason}",
          file=sys.stderr, flush=True)


def main():
    for stream in (sys.stdin, sys.stdout):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8")
    done = 0
    spoke = 0
    failed = False
    malformed = False
    for line_number, line in enumerate(sys.stdin, 1):
        line = line.strip()
        if not line:
            continue
        try:
            obj = json.loads(line)
        except ValueError:
            continue
        try:
            if not isinstance(obj, dict):
                raise MalformedEvent("event must be an object")
            kind = obj.get("type", "")
            if not isinstance(kind, str):
                raise MalformedEvent("event type must be a string")
            if kind == "turn.failed":
                failed = True  # A failed-turn event retains failure even if its payload is malformed.
                try:
                    error = obj.get("error")
                    if error is None:
                        diagnostic = "no message"
                    elif not isinstance(error, dict):
                        raise MalformedEvent("turn.failed error must be an object or null")
                    else:
                        diagnostic = optional_text(error, "message") or "no message"
                except MalformedEvent as exc:
                    malformed = True
                    bad(line_number, str(exc))
                    diagnostic = "no message"
                print("[codex turn FAILED] " + diagnostic, file=sys.stderr, flush=True)
            elif kind == "error":
                failed = True
                print("[codex error] " + str(obj.get("message", "")), file=sys.stderr, flush=True)
            elif kind == "item.completed":
                item = obj.get("item", {})
                if not isinstance(item, dict):
                    raise MalformedEvent("item must be an object")
                item_kind = item.get("type", "")
                if not isinstance(item_kind, str):
                    raise MalformedEvent("item type must be a string")
                if item_kind == "agent_message":
                    text = optional_text(item, "text")
                    if text:
                        spoke += 1
                        print(text, flush=True)
                elif item_kind == "command_execution":
                    command = optional_text(item, "command")
                    if command:
                        print("<!-- codex ran: %s -->" % command[:160], flush=True)
                elif item_kind == "error":
                    diagnostic = optional_text(item, "message")
                    if diagnostic:
                        print("[codex item error] " + diagnostic, file=sys.stderr, flush=True)
            elif kind == "turn.completed":
                usage = obj.get("usage", {})
                if not isinstance(usage, dict):
                    raise MalformedEvent("usage must be an object")
                counts = []
                for field in ("input_tokens", "output_tokens"):
                    value = usage.get(field, 0)
                    if type(value) is not int or value < 0:
                        raise MalformedEvent(field + " must be a nonnegative integer")
                    counts.append(value)
                done += 1
                print("\n<!-- tokens: in %s out %s -->" % tuple(counts), flush=True)
        except MalformedEvent as exc:
            malformed = True
            bad(line_number, str(exc))
    if failed:
        print("[codex] the turn failed (reason above); no review was produced.",
              file=sys.stderr, flush=True)
        return 3
    if malformed:
        return 6
    if done == 0:
        print("[codex] no turn.completed event: possible mid-stream disconnect.",
              file=sys.stderr, flush=True)
        return 4
    if spoke == 0:
        print("[codex] the turn completed without an agent message; no review was produced.",
              file=sys.stderr, flush=True)
        return 5
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
