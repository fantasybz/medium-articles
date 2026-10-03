# Independent formal data audit

Verdict: **READY** for the recorded formal-01 dataset. 1903/1903 audit checks passed.

Frozen manifest SHA-256: `ba30398118ecde62b2f682884c1e882b2864c22d70faf99549ceab0d7c0a55f2`.

The audit read source, records and traces without editing them or executing candidates. The public export and recorded full rescoring without Claude on PATH were also checked; the auditor did not rerun candidates.

## Denominators and provenance

- Exactly 40 frozen slots, 40 launch files, 40 unique CLI sessions and working directories, and 40 formal records; four arms each have ten slots. Launch order matches the seeded schedule; observed concurrency was four.
- No extra campaign run directories, replacement slots, missing records, pilot records or HALTED marker were observed. Every generation completed before the first scoring record. This conclusion is bounded to the recorded campaign.
- The manifest, all frozen source files, four packets and system input match their hashes; packet bytes reconstruct exactly from frozen seed/spec. The seed equals the declared repository commit/path. Every artifact matches terminal source, ledger, seal and evaluator candidate hash.
- Every evaluation uses the frozen evaluator/requirements hashes and exact 103-case inventory; R01–R13 have coverage, every check passed, including streaming before EOF and C-locale handling. The 4,120 case executions are checks on 40 candidates, not 4,120 independent samples.

## Outcomes and descriptive structure

| Arm | Accepted / planned | Exact 95% CI | Unique normalized ASTs | Pair cosine min / median / max | Seed cosine min / median / max |
|---|---:|---|---:|---|---|
| A0 | 10/10 | 69.1503%–100% | 10 | 0.983119 / 0.994710 / 0.998213 | 0.949927 / 0.965595 / 0.978295 |
| A | 10/10 | 69.1503%–100% | 10 | 0.991281 / 0.996975 / 0.999600 | 0.951163 / 0.962484 / 0.970361 |
| B | 10/10 | 69.1503%–100% | 10 | 0.993698 / 0.997509 / 0.999708 | 0.955575 / 0.959382 / 0.966537 |
| C | 10/10 | 69.1503%–100% | 10 | 0.990320 / 0.996477 / 0.999664 | 0.952907 / 0.965676 / 0.970697 |

The lower bound was independently calculated as `0.025 ** (1/10) = 0.6915028921812392`. All 40 files parse; all 40 source hashes and all 40 normalized AST hashes are distinct. Each arm contributes 45 pairs, totaling 180 pairs that reuse 40 files (nine pairs per file). They are not independent observations. Shared seed scaffolding and a coarse node-type representation can produce high cosine without semantic equivalence.

## Trace and resource accounting

Every recorded process exited normally before its timeout; each trace contains one init, one successful terminal and one turn. All observed assistant envelopes identify `claude-opus-5-5`; tools, MCP servers, skills and slash commands are empty, with no observed tool calls or boundary violations. The CLI version is 2.1.282. Two assistant envelopes per run are observed within one turn; they are not separate prescheduled attempts.

All 40 costs, durations and four terminal token categories are observed, with zero missing values. CLI-reported total cost is **USD 5.692342**, comprising Opus **USD 5.512612** plus Haiku **USD 0.179730**. Haiku appears only in modelUsage accounting, not candidate-generation assistant messages. Its exact internal role cannot be established from these traces. Terminal usage matches the Opus accounting fields; the cost total includes both models. `costBasis=list` is not a billing invoice.

## Claim boundaries

The frozen report and protocol make descriptive per-arm claims only: no superiority, equivalence, production reliability, human calibration/review savings, native Skill or full agent-loop conclusion. Repository provenance does not prove human authorship; reference/mutation cases are apparatus, not human samples. Ten successes still leave a lower 95% bound near 69.15% under the stated Bernoulli assumptions.

Manifest/launch timestamps and hashes support the local freeze chronology, without an external timestamp authority. Evaluation hashes in this audit capture the reviewed bytes; they are not previously signed evidence. No thinking text is included in this report or audit JSON.

The public export and complete no-Claude-PATH rescoring evidence are now verified as described below.

Machine-readable checks, per-run artifact/evaluation/trace hashes, resource totals and metric values are in `formal-data-audit.json`.


## Public export and no-Claude-PATH rescoring followup

Verified all **317 public archive file hashes**, byte equality for every copied private input, and 40 trace projections reconstructed exactly from the local raw traces. Each sidecar links original/projection hashes and preserves parser decisions. No thinking/signature payload is present in the public projections. The raw traces are omitted.

Read `results/validation-2026-09-25/public-rescore.json` and `public-rescore-execution.json`; the latter matches the recorded execution-log hash. It records a new empty working directory, `PATH=/usr/bin:/bin`, exit 0, and 2026-09-25 04:35:49–04:39:41 UTC. Every one of the 40 public candidates has 103 successful checks with the same case outcomes as its original evaluation, verified individually; only timing observations differ. Provenance hashes and sandbox checks also agree. This is rescoring of the same 40 artifacts, with no additional model samples. The auditor did not rerun them.

`RESULTS.md` outcome, CI, cost, AST and seed-similarity numbers match the audit. Its inferential and human/native-Skill limits are appropriate. Nonblocking precision note: Haiku is observable only in modelUsage; its internal role cannot be established from these traces.

Final verdict: **READY**; **1903/1903** checks passed, no data-integrity blocker.
