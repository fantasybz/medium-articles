# Harden the repository's Codex JSONL review parser (expanded specification)

Modify only the supplied `codex_jsonl.py`, copied unchanged from medium-articles commit `37f6c0ce9b536f95132d5e01a387f380bbb9639c`. The repository uses this parser to turn Codex JSONL output into a review while keeping diagnostics separate. Valid JSON with unexpected types currently can crash the parser, and a numeric agent text can be mistaken for a successful review. Fix these defects while preserving the existing permissive streaming behavior. The following requirements are the complete contract; evaluation adds no additional requirements.

### R01 — Artifact and CLI

The candidate artifact is exactly one regular Python file, `codex_jsonl.py`, not a symlink. Retain the current command-line/main entrypoint and use only the standard library. No new arguments or dependencies are required, and the shell wrapper is outside this change.

Read a sequence of lines from stdin as UTF-8 and write review content to UTF-8 stdout. Diagnostics belong on stderr. The parser must continue processing incrementally: it must not read or buffer the complete input before producing output. Flush output for each emitted message, comment or diagnostic so it is visible before stdin EOF. CJK text must survive even when the process locale is C.

Object schemas are open with respect to unrelated extra fields. Ignore fields not described below rather than rejecting their presence.

### R02 — Lines and event dispatch

The physical first line of input is line 1. Count every physical line, including blank lines and ignored non-JSON lines, so diagnostics point to the actual input location. Strip each line as the original parser does. Skip an empty line silently. If decoding a nonempty line as JSON fails, skip that text silently as well; this existing tolerance is intentionally retained.

A successfully decoded JSON value must be an object. Arrays, null, strings, numbers and booleans are malformed events under R03. Within a root object, an absent `type` means an ignored unknown event. If `type` is supplied, it must be a string; null, booleans, numeric values and containers are malformed.

Dispatch the recognized string values `item.completed`, `turn.completed`, `turn.failed` and `error` according to R04–R10. An unrecognized **string** event type is ignored, and none of its payload fields are validated. This distinction keeps unknown event extensions compatible while making structurally wrong event types visible.

### R03 — Malformed event handling

Each malformed input line contributes exactly one stderr diagnostic with this shape:

```text
[codex malformed event] line N: REASON
```

Terminate the diagnostic with one newline. N is the physical, one-based line number from R02. REASON can be any nonempty explanation on a single line; its wording is not prescribed. Multiple wrong fields on the same line still produce only one malformed-event diagnostic.

Record that a malformed event was encountered, then continue processing subsequent input lines. It must not raise a traceback, terminate the read loop, or hide later remote errors. Except for the explicit-failure effect of a turn.failed event described in R10, drop only that line's malformed event: it emits no stdout, contributes no spoken-agent count, and contributes no completed-turn count. Validate the relevant fields before producing that event's ordinary output.

The malformed flag affects final exit-code precedence (R11). Do not add a new summary for exit 6: the per-line diagnostics are the explanation. Existing failure summaries in R12 still apply when an explicit remote failure wins with exit 3.

### R04 — Completed-item envelope

For an `item.completed` event, the nested `item` field behaves as follows:

| Input | Behavior |
|---|---|
| `item` missing | Treat as `{}`; ignore the item |
| `item` is an object | Inspect its type |
| `item` is null or any other non-object | Malformed event |

Within an item object, a missing `type` is ignored. A provided `type` must be a string; a provided null or other non-string is malformed. Recognized item types are `agent_message`, `command_execution` and `error`. Unknown string item types are ignored without checking text, command, message or any other payload field.

### R05 — Agent text

For an agent_message item, absent `text`, null and the empty string mean there is no spoken message. They emit no output and do not count toward the spoken-agent count. Every other provided non-string value is malformed, even if it is false-like in Python: this includes 0, false, empty arrays and empty objects.

For a nonempty string, print the string unchanged followed by the newline added by print, and flush stdout. Count it as one spoken message. Do not trim or normalize it. For compatibility, a string containing only whitespace is still a nonempty string, and embedded newlines or CJK characters remain intact.

### R06 — Command comment

For a command_execution item, missing command, null and empty string produce no output. Every other provided non-string command is malformed.

For a nonempty string, take its first 160 characters using character indexing, not byte truncation. Emit exactly `<!-- codex ran: S -->` followed by one newline on stdout, substituting the truncated string for S, and flush. This output is a diagnostic HTML comment in the review stream; it does not count as a spoken agent message.

### R07 — Item error diagnostic

For an item whose type is error, missing message, null and empty string produce no output. Every other provided non-string message is malformed.

For a nonempty string, emit exactly `[codex item error] MESSAGE` plus a newline on stderr, substituting the unchanged string, and flush. This preserves the old distinction between an item error and a failed turn: an item error does **not** set the explicit remote-failure flag. It is also not an agent message.

### R08 — Completed turn and usage

A missing `usage` on turn.completed is equivalent to an empty object. A supplied usage value must be an object: null and all other non-object values are malformed. Ignore unrelated fields inside the usage object.

Only input_tokens and output_tokens are interpreted. Each missing field defaults independently to integer zero. If either field is present, its value must be an integer greater than or equal to zero. Booleans are not integers for this contract. A float remains invalid even if numerically integral. Strings, null, containers and negative integers are invalid too.

Validate the entire usage object before counting the completed turn or writing its token comment. A valid turn.completed contributes one completed turn and emits exactly a leading newline, `<!-- tokens: in I out O -->`, and a trailing newline on stdout, flushed, where I/O are the validated counts. A malformed usage must not produce a partial token comment or count as a valid completion.

### R09 — Top-level error

A top-level event of type error always marks the run as an explicit remote failure. Preserve the old conversion rule exactly: obtain `event.get("message", "")`, convert it with Python str, and emit `[codex error] M` plus one newline to stderr, flushed.

Unlike item errors and failed-turn nested messages, this event imposes no message-type constraint. Null, numbers, booleans, arrays and objects are all converted using the legacy str rule; they are not malformed merely because of the message value. An absent message converts the default empty string.

### R10 — Failed turn

Every turn.failed event marks explicit failure, even if its nested diagnostic fields have a wrong type. Read its error field using these rules:

| Input | Message/handling |
|---|---|
| error missing or null | Use `no message` |
| error is an object | Read its message as below |
| error is any other value | Mark malformed, use `no message` |

Within an error object, absent message, null or empty string uses `no message`. A nonempty string is used unchanged. Every provided non-string/non-null message is malformed, including 0, false, empty arrays and empty objects; use `no message` as the fallback.

If malformed, emit the R03 line first. Then, for every turn.failed event, emit `[codex turn FAILED] MESSAGE` plus one newline to stderr, flushed. This means a malformed failed-turn event has both its line-level malformed diagnostic and the legacy failure diagnostic. Its explicit-failure flag still outranks malformed status at EOF.

### R11 — Exit-code precedence

After all input has been consumed, choose the first applicable row:

| Priority | Condition | Exit |
|---|---|---:|
| 1 | Any top-level error or turn.failed event | 3 |
| 2 | Otherwise, any malformed event | 6 |
| 3 | Otherwise, no valid turn.completed | 4 |
| 4 | Otherwise, no nonempty string agent message | 5 |
| 5 | Otherwise | 0 |

These flags reflect the full stream. Do not exit early when malformed input is seen, because an explicit remote failure later in the stream must still return 3. Likewise, an error after a completed turn must be recognized. Streaming stdout already produced is retained; the nonzero exit tells the existing caller that it is not a valid completed review.

### R12 — Legacy end diagnostics

For exit 3, append this exact stderr line:

```text
[codex] the turn failed (reason above); no review was produced.
```

For exit 4, append this exact stderr line:

```text
[codex] no turn.completed event: possible mid-stream disconnect.
```

For exit 5, append this exact stderr line:

```text
[codex] the turn completed without an agent message; no review was produced.
```

Each line ends with a newline. Exits 0 and 6 have no end-of-stream summary. Apart from the new malformed diagnostics, preserve the existing valid output and legacy diagnostic text.

### R13 — Preserve permissive stream behavior

This change validates value types; it does not introduce a protocol state machine or a strict mode. Do not add uniqueness or sequence checks. Identical repeated agent messages are each emitted and count separately. Multiple valid turn.completed events each produce their own token comment. Continue dispatching events after completion, including messages and errors.

Keep the earlier compatibility rules for extra fields, unknown string event/item types, missing optional values, blank lines and undecodable text. Rejecting duplicate terminals, suppressing duplicated text, enforcing terminal ordering, changing the shell wrapper or adding CLI options is outside this task.

## Non-normative rationale and checklist (B)

R01–R13 above remain the entire contract. This section adds no requirement and does not prescribe a class layout or helper names.

JSON decoding guarantees a JSON value, not an object or the nested types the parser expects. Python truthiness also differs from the contract: 0, false and empty containers must be diagnosed in selected fields even though the old truthiness check skipped them. Presence, null, empty string and wrong type therefore deserve separate consideration. Checking all usage values before output avoids printing a token comment for a malformed completion.

It is useful to distinguish per-event validation from final run status. A bad event should not erase prior streamed content or stop a later remote refusal from being observed. In particular, turn.failed expresses failure even when its attached message is malformed. Unknown string event types, on the other hand, remain an extension point and do not require inspecting unfamiliar payloads.

Possible self-review questions, referring only to the published contract:

- R01–R03: Does output arrive before EOF, and do malformed diagnostics use physical line numbers while ignored text remains silent?
- R04–R08: Are missing, null, empty and wrong-type values distinguished for each field according to its own rules?
- R08: Are bool, float and negative token values rejected before a token comment appears?
- R09–R10: Is top-level error's legacy str conversion retained, and can malformed turn.failed still produce exit 3?
- R11–R12: Does final precedence remain 3, then 6, then 4, then 5, then 0 with unchanged legacy summaries?
- R13: Do repeated messages/completions and unknown string types remain accepted without new sequence rules?

## Non-normative implementation pattern (C)

This is an optional plain-text implementation pattern, not a runtime skill, installed plugin, hook or tool invocation. R01–R13 are unchanged. Any implementation meeting the same contract is acceptable.

One possible design keeps the original streaming loop and separates a line's validation result from the accumulated flags:

```text
for physical_line_number, raw_line in stdin:
    strip and try JSON decoding
    validate root and the recognized event's relevant fields
    emit one malformed diagnostic if needed
    otherwise emit that event's legacy stdout/stderr
    retain explicit turn.failed even when its diagnostic fields are malformed
at EOF:
    choose 3 > 6 > 4 > 5 > 0 and the matching legacy summary
```

A helper for optional text can distinguish absent/null/empty from wrong-type values, but top-level error must retain its separate str conversion rather than sharing that stricter helper. Another helper can validate a usage mapping and return either both integer counts or a single validation problem, avoiding partial event output. Python bool is a subclass of int, so an exact type check or an explicit bool exclusion can express the token rule.

An event handler can return a small result describing stdout/stderr output, whether an agent spoke, whether a valid turn completed, and whether remote failure occurred. Alternatively, retaining the existing branch structure with local validation is equally acceptable. Either approach should preserve flushing and avoid buffering the stream. Validation errors can be reported through one common function taking the physical line number and a short explanation, so a line with multiple invalid fields still receives exactly one malformed diagnostic.

The malformed flag and explicit-failure flag are independent. Checking the explicit-failure flag first at EOF preserves remote error visibility even when malformed data occurred earlier or within turn.failed itself. Unknown string types should return without inspecting fields whose schema is not known.
