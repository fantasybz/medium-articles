# Same-spec controlled generation: descriptive report

Phase: **formal**. Planned and recorded: **40**.

Primary outcome: `accepted_completion = cli_success AND artifact_success`.
All prescheduled failures remain in the denominator. Intervals are two-sided 95% Clopper–Pearson.

| Arm | Accepted / planned | Exact 95% CI | Artifact successes | CLI successes |
|---|---:|---|---:|---:|
| A0 | 10/10 | 69.15%–100.00% | 10/10 | 10/10 |
| A | 10/10 | 69.15%–100.00% | 10/10 | 10/10 |
| B | 10/10 | 69.15%–100.00% | 10/10 | 10/10 |
| C | 10/10 | 69.15%–100.00% | 10/10 | 10/10 |

## Observed resources

Costs are reported CLI estimates, not billing invoices. Missing values are not zero; capped and failed runs remain included.

| Arm | Wall seconds, median (observed/planned) | Reported USD total | Cost observed / planned | Input tokens total | Output tokens total | Cache read / creation totals |
|---|---:|---:|---:|---:|---:|---:|
| A0 | 37.273 (10/10) | 1.248397 | 10/10 | 20 (10/10) | 44935 (10/10) | 0 (10/10) / 39339 (10/10) |
| A | 37.300 (10/10) | 1.382626 | 10/10 | 20 (10/10) | 46037 (10/10) | 0 (10/10) / 52202 (10/10) |
| B | 40.277 (10/10) | 1.513502 | 10/10 | 20 (10/10) | 50161 (10/10) | 0 (10/10) / 57749 (10/10) |
| C | 37.161 (10/10) | 1.547817 | 10/10 | 20 (10/10) | 49072 (10/10) | 0 (10/10) / 64234 (10/10) |

## Exploratory AST description

Metric: AST node-type multiset cosine. This ignores order and many semantic differences. Only produced, hash-verified, nonempty parsed artifacts contribute; unsuccessful runs can contribute artifacts.

| Arm | Produced / planned | Parsed / planned | Pairs observed / possible | Median cosine | Min cosine | Unique normalized AST hashes | Seed cosine: median [min, max]; observed/planned |
|---|---:|---:|---:|---:|---:|---:|---|
| A0 | 10/10 | 10/10 | 45/45 | 0.995 | 0.983 | 10 | 0.966 [0.950, 0.978]; 10/10 |
| A | 10/10 | 10/10 | 45/45 | 0.997 | 0.991 | 10 | 0.962 [0.951, 0.970]; 10/10 |
| B | 10/10 | 10/10 | 45/45 | 0.998 | 0.994 | 10 | 0.959 [0.956, 0.967]; 10/10 |
| C | 10/10 | 10/10 | 45/45 | 0.996 | 0.990 | 10 | 0.966 [0.953, 0.971]; 10/10 |

Seed-relative cosine uses `source/seed/codex_jsonl.py`, verified against `manifest.task_provenance.seed_sha256`. High similarity can reflect shared seed scaffolding; this description does not subtract shared code or support an inferential conclusion.

Pairs share runs; 45 pairs are not 45 independent observations. No pair bootstrap, significance, equivalence, human-calibration or review-cost claim is made.

## Completion status

- A0: completed=10
- A: completed=10
- B: completed=10
- C: completed=10

Ten accepted results do not establish production reliability or a pass^10 probability. Binomial intervals depend on stability and independence assumptions. This tool-free task snapshot does not measure a native agent tool loop or runtime skill enforcement.

Complete ledger validation does not establish preregistration timing, model pinning, sandbox enforcement or oracle validity; audit those separately.

Per-run AST hashes/counts, every pair, resource missingness and input hashes are in `summary.json`.
