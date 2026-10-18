# Same specification, ten runs: pre-execution protocol v1 (local freeze; no third-party registration)

This is a controlled study of a real maintenance task in `fantasybz/medium-articles`.
It is not a synthetic payment application, a production deployment trial, or a
measurement of autonomous tool use. The user selected the current repository on
2026-09-25. No claim to being the first repeated coding study is made.

## Question and scope

For one frozen Python parser repair, what accepted completions, source differences,
and reported costs occur across ten fresh generations under each of four instruction
packages? The task fixes real malformed-event handling in
`research/scripts/codex_jsonl.py` at commit
`37f6c0ce9b536f95132d5e01a387f380bbb9639c`. The existing parser crashes on JSON `null`
or `[]`, and accepts a numeric agent message as a successful review. The seed is an
exact copy, not an injected defect. `task.json` records provenance and SHA-256.

All arms implement the same normative requirements. A0 is compact; A explains the
same requirements in detail; B adds reasons and a checklist; C adds a textual
implementation pattern. Each packet is self-contained. This is a comparison of
specific instruction packages, not a general estimate of document length. C does
not install or execute a Skill. Tools, hooks, runtime permissions, model and effort
are not experimental factors.

## Generation boundary

- Generation model: `claude-opus-5-5`, effort `high`, fixed across every arm. Review
  effort may be higher and is never pooled with generation observations.
- Claude Code is invoked with a fixed system input, no tools, no MCP, safe mode,
  disabled skills, empty setting sources, no session persistence, and a new empty
  temporary working directory. The packet contains only seed source and that arm's
  instructions. It contains no oracle, reference patch, sibling output or score.
- Each response must contain a JSON object with exactly one `codex_jsonl.py` source
  string. No repair prompt, parsing cleanup, retry, or best-of selection is allowed.
- An accepted completion must have an observed initialization trace showing the specified model, zero tools,
  zero MCP servers, zero skills and zero slash commands; assistant tool calls or
  a different generation model invalidate the boundary and halt the campaign.
- Missing initialization/model evidence, truncated traces and synthetic API error
  messages are incomplete or operational failures, not observed model drift.
  They cannot be CLI successes, but remain in their original slots. An actually
  observed different model, exposed tool or tool call still halts the campaign,
  even if a later trace line is malformed. Artifact validity is scored separately.
- Child processes set `DISABLE_AUTOUPDATER=1`. The manifest records allowlisted
  numeric token-control values and only the names of `ANTHROPIC_*` environment
  variables, never their secret values. Other inherited context is not fully pinned.
- Safe mode still exposes built-in CLI components in its metadata. Their identities
  are recorded. We do not claim to hash invisible provider context, pin temperature,
  control a model seed, or prove that the provider's implementation is immutable.
  Packet hashes identify explicit inputs only. The CLI executable is resolved to
  an absolute path; its binary hash and version are checked as part of the freeze.
  A hosted model cannot guarantee byte-identical reproduction even with the same
  model name.

## Schedule, stopping, and outcomes

Two pilot slots (A0 and C) validate transport and evaluation. They are excluded from
formal results and cannot later be relabeled. All four packets receive offline
schema and requirement checks; two pilots alone do not validate all interventions.
Changes motivated by a pilot require a fresh freeze before formal execution.
Separate operational probe campaigns deliberately trigger a short timeout and a
very low CLI budget. They test failure recording, remain labeled pilot-phase
development probes, and are never part of the original two pilots or formal forty.

Formal execution has ten blocks, each containing one A0, A, B and C in a shuffled
order, with Python RNG seed 20260925. Forty slots are frozen in advance. Up to four
generations run concurrently; observed launch order, timestamps and durations are
retained. This reduces gross arm/time separation but does not eliminate provider
load or cache interactions. There is one task, not forty independently sampled tasks.
Blocks define the balanced launch queue, not synchronized execution windows:
the next queued slot can start as soon as a worker is free, so adjacent blocks
may overlap. No paired estimator relies on a common block completion time.

Each slot has a 600-second generation limit and a Claude CLI USD 5 list-price budget
stop threshold. The CLI may report cost above that threshold before stopping,
as demonstrated by the low-budget probe; it is not a strict monetary cap or an
estimate of a subscription invoice. No
data-dependent sample extension is permitted. A disconnect, malformed response,
budget stop or timeout remains in its original slot; it is never silently replaced.
An interrupted started slot is labeled interrupted on resume. A boundary breach
halts the campaign and is reported as incomplete; it does not authorize weakening
the boundary or pretending the remaining slots ran.
On resume, already recorded boundary failures and generated-but-unscored traces
are audited before any new launch, so interruption between trace storage and
writing the halt marker cannot silently bypass an observed violation.

The primary endpoint is **accepted completion** (`cli_success && artifact_success`): normal CLI completion within the
limit, an intact generation boundary, and an artifact passing every external check.
The `cli_success` field includes the intact generation-boundary requirement.
Record `boundary_ok`, `cli_success`, `artifact_success`, and `accepted_completion` separately.
Artifact success evaluates the source sealed after process termination, including
a possible five-second termination grace period. It may therefore be true even
when the source was not available within the generation limit; it is not an
on-time completion measure. Operational stops are not called functional defects.

## External acceptance and integrity

The candidate does not receive the held-out event sequences, expected outputs, or
scoring code. All tested behavior is specified publicly. The external driver sends
one input stream to the sealed candidate process and compares stdout, stderr and
exit status outside that process. It tests legacy behavior as well as the repair.
The event stream itself is necessarily visible to the candidate while executing.
There are 102 batch cases and one incremental streaming probe per candidate.
The streaming probe writes a message, requires its stdout before stdin EOF,
and only then writes the terminal event and closes stdin; buffering until EOF fails.
Passing means passing these 103 external checks, not a proof of every possible
behavior. The suite does not inspect whether an implementation literally retains
a `main()` function or rejects every extra command-line argument. Its C-locale
Unicode round-trip also does not distinguish every internal encoding strategy.
The reference patch and mutation fixtures test the evaluator; they are AI-authored
tooling fixtures, not human baselines or experimental generations.

Only the candidate file, Python runtime and required system runtime paths are readable inside the evaluator's
macOS Seatbelt sandbox. Network access and filesystem writes are denied. Before a
campaign, probes must demonstrate ordinary execution and denial of oracle-file
reads, file writes and network binding. Unsupported systems fail closed. This is
a tested local boundary, not a proof against all OS or IPC vulnerabilities.
Candidate source is hashed before and after evaluation. Symlinks and unexpected
output filenames are rejected. No candidate-controlled test command is executed.

## Analysis fixed before formal execution

`analyze.py` requires all forty scheduled records, one per slot, and verifies source
hashes before computing results. Report primary and secondary counts with two-sided
95% Clopper–Pearson intervals per arm. Ten successes out of ten still have a lower
confidence bound near 69.15%; zero observed failures is not a high-reliability claim.
There is no primary or secondary between-arm contrast estimator, paired
hypothesis test, superiority, equivalence or noninferiority decision rule. Only
per-arm summaries are planned; no post hoc winning comparison is selected.

For an incomplete or halted campaign, `campaign_status.py` reports every planned
slot (including not_started and generated_not_scored), with no confidence intervals.
`analyze.py` deliberately refuses incomplete data instead of substituting failures
or silently changing denominators. Evaluation errors halt as measurement failures.

Structural measures are exploratory: AST node-type multiset cosine similarity,
identifier-normalized AST hashes, and function/class counts. Add per-artifact
`seed_ast_node_type_cosine` against the hash-verified frozen seed; report observed,
missing, minimum, median and maximum by arm to expose shared-seed ceiling effects. Report available and
unparseable artifact denominators. Ten parsed files produce 45 within-arm pairs,
which share files and are not 45 independent observations. Similarity is conditional
on available parseable artifacts and does not measure correctness or maintainability.

Report generation wall time and provider-reported token/cost fields with their
denominators, including failed slots when those fields exist. Do not impute missing
usage as zero or call list-price estimates actual charges. Cost summaries also expose cache token categories and launch order; cache is
not experimentally reset, and no no-cache price counterfactual or causal dollar
saving is claimed. No human review minutes,
human-written baseline, maintenance savings, production permissions or causal link
from structural difference to quality will be inferred.

Token summaries use the CLI terminal `usage` fields as reported; `modelUsage`
breakdowns are retained separately. The CLI also reports an auxiliary bookkeeping
model in cost accounting. That is not a candidate-generation model response, and
its tokens need not appear in the terminal usage totals. Do not reconstruct a bill
by multiplying that token table by one model's price.

## Release gates and limitations

Before a formal freeze: pass offline regression/mutation tests, perform real sandbox
and CLI probes, check requirement equivalence, conduct independent design review,
and resolve blocking findings. Freeze an executable source bundle, packets, schedule, analysis and tool
versions before seeing formal outcomes. Run and analyze from that bundle. An
exclusive process lock prevents concurrent runners from corrupting one campaign;
a persistent halt cannot be resumed. Recheck source and Python runtime before each
launch and each score. Check the pinned absolute CLI binary/version when launching
generation, but do not make scoring depend on the CLI still being installed or
unchanged. Generate all candidates before evaluation so slow
evaluation cannot delay generation-timeout supervision. Completion times are
observed by polling, with a nominal 0.5-second interval; a result first observed
after the limit is conservatively labeled timed out. Keep raw terminal traces and failures.
Normal runner cleanup terminates its child process groups. An uncatchable runner
kill or machine failure may leave a CLI request running; such interruption requires
checking and terminating orphan processes before any restart. Started slots are
still not regenerated. Partial scoring writes require an explicit measurement
amendment rather than an automatic candidate repair or silent restart.

This small tool-free, single-file task may have a ceiling effect. It cannot establish
behavior of large repositories, long-horizon agents, other languages, runtime skills,
or humans. Public release of the cases makes later replications non-secret; label
them replications and do not claim hidden-test novelty. Any post-freeze correction
must be logged as an amendment, preserve the original run, and clearly separate
rescoring from new generation. Article claims must follow observations, including
null results, measurement failures and unfinished campaigns.
