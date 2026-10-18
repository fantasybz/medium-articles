"""Stream-parse `codex exec --json` output: print the agent's messages as they complete.

Kept in its own file because embedding this in a bash single-quoted `python3 -c`
string broke on the escaped quotes (the first run of codex_review.sh died with a
SyntaxError, which closed the pipe and made codex panic on stdout).

Prints agent messages to stdout (they become the review file), and everything
diagnostic (`turn.failed`, `error` events, missing `turn.completed`, malformed
events) to stderr so the caller can tell "Codex said nothing" from "Codex was
refused".

Valid JSON whose shape is wrong (a non-object root, a non-string type, a
non-string agent text, a bad usage block, ...) is reported once per line as
`[codex malformed event] line N: REASON` and dropped; processing continues.

Exit codes codex_review.sh branches on:
    0  at least one agent message and a completed turn
    3  the turn failed or an error event arrived (refusal, usage limit)
    4  no turn.completed: a mid-stream disconnect
    5  the turn completed but Codex never spoke; the "review" would be a token count
    6  no explicit failure, but at least one malformed event was seen
"""
import json
import sys


def _emit(text, stream):
    print(text, file=stream, flush=True)


def _type_name(value):
    if value is None:
        return 'null'
    if isinstance(value, bool):
        return 'boolean'
    if isinstance(value, int):
        return 'integer %d' % value
    if isinstance(value, float):
        return 'number'
    if isinstance(value, str):
        return 'string'
    if isinstance(value, list):
        return 'array'
    if isinstance(value, dict):
        return 'object'
    return type(value).__name__


def _optional_text(container, key):
    """Return (text_or_None, problem_or_None).

    Absent, null and empty string mean "no text"; other non-strings are a problem.
    """
    if key not in container:
        return None, None
    value = container[key]
    if value is None:
        return None, None
    if isinstance(value, str):
        return (value if value else None), None
    return None, '%s must be a string, got %s' % (key, _type_name(value))


def _usage_counts(event):
    """Return ((input, output), None) or (None, problem)."""
    if 'usage' not in event:
        return (0, 0), None
    usage = event['usage']
    if not isinstance(usage, dict):
        return None, 'usage must be an object, got %s' % _type_name(usage)
    counts = []
    for key in ('input_tokens', 'output_tokens'):
        if key not in usage:
            counts.append(0)
            continue
        value = usage[key]
        if type(value) is not int or value < 0:
            return None, 'usage.%s must be a non-negative integer, got %s' % (key, _type_name(value))
        counts.append(value)
    return (counts[0], counts[1]), None


class _State(object):
    def __init__(self):
        self.done = 0
        self.spoke = 0
        self.failed = False
        self.malformed = False

    def bad(self, lineno, reason):
        self.malformed = True
        reason = ' '.join(str(reason).split()) or 'malformed event'
        _emit('[codex malformed event] line %d: %s' % (lineno, reason), sys.stderr)


def _handle_item(obj, lineno, state):
    if 'item' not in obj:
        return
    item = obj['item']
    if not isinstance(item, dict):
        state.bad(lineno, 'item must be an object, got %s' % _type_name(item))
        return
    if 'type' not in item:
        return
    itype = item['type']
    if not isinstance(itype, str):
        state.bad(lineno, 'item.type must be a string, got %s' % _type_name(itype))
        return
    if itype == 'agent_message':
        text, problem = _optional_text(item, 'text')
        if problem:
            state.bad(lineno, 'item.' + problem)
            return
        if text is not None:
            state.spoke += 1
            _emit(text, sys.stdout)
    elif itype == 'command_execution':
        command, problem = _optional_text(item, 'command')
        if problem:
            state.bad(lineno, 'item.' + problem)
            return
        if command is not None:
            _emit('<!-- codex ran: %s -->' % command[:160], sys.stdout)
    elif itype == 'error':
        message, problem = _optional_text(item, 'message')
        if problem:
            state.bad(lineno, 'item.' + problem)
            return
        if message is not None:
            _emit('[codex item error] ' + message, sys.stderr)


def _handle_turn_failed(obj, lineno, state):
    state.failed = True
    msg = 'no message'
    problem = None
    err = obj.get('error')
    if err is None:
        pass
    elif isinstance(err, dict):
        text, text_problem = _optional_text(err, 'message')
        if text_problem:
            problem = 'error.' + text_problem
        elif text is not None:
            msg = text
    else:
        problem = 'error must be an object, got %s' % _type_name(err)
    if problem:
        state.bad(lineno, problem)
    _emit('[codex turn FAILED] ' + msg, sys.stderr)


def _handle(obj, lineno, state):
    if not isinstance(obj, dict):
        state.bad(lineno, 'event must be a JSON object, got %s' % _type_name(obj))
        return
    if 'type' not in obj:
        return
    etype = obj['type']
    if not isinstance(etype, str):
        state.bad(lineno, 'type must be a string, got %s' % _type_name(etype))
        return
    if etype == 'item.completed':
        _handle_item(obj, lineno, state)
    elif etype == 'error':
        state.failed = True
        _emit('[codex error] ' + str(obj.get('message', '')), sys.stderr)
    elif etype == 'turn.completed':
        counts, problem = _usage_counts(obj)
        if problem:
            state.bad(lineno, problem)
            return
        state.done += 1
        _emit('\n<!-- tokens: in %d out %d -->' % counts, sys.stdout)
    elif etype == 'turn.failed':
        _handle_turn_failed(obj, lineno, state)


def main():
    # The stream is UTF-8 whatever the locale says; a C locale would otherwise
    # choke on the first CJK character in a review.
    if hasattr(sys.stdin, 'reconfigure'):
        sys.stdin.reconfigure(encoding='utf-8', errors='replace')
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    if hasattr(sys.stderr, 'reconfigure'):
        sys.stderr.reconfigure(encoding='utf-8', errors='backslashreplace')

    state = _State()
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
        _handle(obj, lineno, state)

    if state.failed:
        _emit('[codex] the turn failed (reason above); no review was produced.', sys.stderr)
        sys.exit(3)
    if state.malformed:
        sys.exit(6)
    if state.done == 0:
        _emit('[codex] no turn.completed event: possible mid-stream disconnect.', sys.stderr)
        sys.exit(4)
    if state.spoke == 0:
        _emit('[codex] the turn completed without an agent message; no review was produced.', sys.stderr)
        sys.exit(5)


if __name__ == '__main__':
    main()
