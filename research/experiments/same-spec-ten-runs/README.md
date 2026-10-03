# Same specification, ten runs

A reproducible experiment using a real repair in this repository's research tools.
The frozen source is `research/scripts/codex_jsonl.py` at commit
`37f6c0ce9b536f95132d5e01a387f380bbb9639c`. The production file is not replaced by an
experimental candidate. See [the protocol](PROTOCOL.md), [task provenance](task.json),
and [the source audit](../../2026-10/same-spec-ten-runs/evidence-audit.md).

The model receives the source snapshot and instructions, with no tools. Four
instruction packages are organized around requirements R01–R13; they are not
fully semantically equivalent because A adds a CLI scope restriction inherited
by B and C. See the [four frozen specifications and comparison guide](SPECS.md)
for the full texts, line-by-line diffs and complete task packets. The formal schedule has ten
fresh generations per package, followed by external evaluation. These observations describe this single-file
maintenance case, not general autonomous-agent reliability.

## Reproduce

Requirements: Python 3.10+, macOS with `/usr/bin/sandbox-exec`, an authenticated
Claude Code CLI supporting the pinned model and recorded flags. No Python packages
are required. Other operating systems fail closed until a tested execution boundary
is implemented. Hosted inference has nondeterminism and may change availability.

From this directory:

```sh
python3 -m unittest discover -p 'test_*.py'
python3 sandbox.py
python3 run_study.py freeze /tmp/same-spec-pilot --phase pilot
python3 run_study.py run /tmp/same-spec-pilot
# Inspect the pilot and design review before starting formal generation.
python3 run_study.py freeze /tmp/same-spec-formal --phase formal
python3 run_study.py run /tmp/same-spec-formal
python3 /tmp/same-spec-formal/source/analyze.py /tmp/same-spec-formal
# For a halted or incomplete campaign (reports slots, no confidence intervals):
python3 /tmp/same-spec-formal/source/campaign_status.py /tmp/same-spec-formal
# Export a NEW public data directory (formal, complete, non-halted campaigns only).
python3 -B archive.py export /tmp/same-spec-formal /tmp/same-spec-public
# Re-evaluate every available candidate without modifying original evidence.
python3 -B /tmp/same-spec-public/source/archive.py rescore /tmp/same-spec-public --output /tmp/same-spec-rescore.json
```

Use an explicit interpreter path if your shell selects different Python versions
in different directories.

Campaign paths must be new and outside this source directory. A freeze captures
source hashes, all four packets, settings and the complete schedule. `run` may resume
unstarted slots; a started slot is never regenerated. Raw JSONL traces, stderr,
launch metadata, candidate files and external scores are retained beside the
manifest. `records.jsonl` separates CLI completion, artifact validity and acceptance.

The public archive includes the exact source bundle, packets, candidates, case
outcomes and resource records. Public traces are explicitly labeled projections:
thinking payloads, transport identifiers and local session metadata are omitted;
raw/projection hashes and preserved parser decisions are recorded. Original raw
traces stay in the local campaign. This is not general secret scanning of arbitrary
generated text. Source, manifest and archive integrity checks precede rescoring.
The rescore path requires the original Python build and macOS platform recorded
in the manifest; it does not require Claude Code or another model request.

Optional F2 rendering uses an isolated environment and exact dependency pins:

```sh
python3 -m venv /tmp/same-spec-figures-env
/tmp/same-spec-figures-env/bin/pip install -r /tmp/same-spec-formal/source/requirements-figures.txt
/tmp/same-spec-figures-env/bin/python /tmp/same-spec-formal/source/render_results.py /tmp/same-spec-formal --output-dir /tmp/same-spec-figures
```

The core generation, evaluation and analysis tools use Python's standard library;
the optional plotting environment is separate. The renderer refuses pilot or
incomplete data, fixes both axes to 0–1 and preserves every parseable artifact.

The budget flag defaults to a USD 5 stop threshold per slot in CLI list-price accounting; a request can exceed it before the CLI stops. It is not a strict monetary cap. A formal
campaign has forty slots; inspect local account terms before independently rerunning
it. Reported list-price usage is not a subscription charge. A different model or
effort is a new campaign, not a replacement for a failed slot.

## Research status

The formal 40-slot campaign completed on 2026-09-25: all four arms had 10/10
accepted completions, with ten different normalized AST hashes per arm. The public
[results and limitations](RESULTS.md) link the frozen bundle, all candidates,
external case outcomes, reproducible analysis, reviews and validation. All 40 public candidates were rescored without Claude CLI; every case outcome
matched. Independent data checks and their evidence are recorded in the results.
AI-authored oracle/mutation fixtures are tooling tests, never human baselines or
experimental generations. This small tool-free case does not establish equivalence,
production reliability, native Skill effects or maintenance savings.
