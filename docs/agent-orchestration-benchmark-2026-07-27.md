# Agent orchestration benchmark — 2026-07-27

This is a single-run exploratory benchmark, recorded to inform Orchestrato's
future routing and multi-agent control-plane work. It is evidence, not a
general model ranking or a pricing estimate.

## Question

For a medium-sized greenfield implementation, when does a planning and review
chain earn back its additional latency and token use compared with one direct
coding-agent call?

## Benchmark task

Each variant started from the same Git commit and received the same `SPEC.md`.
The task was to implement a standard-library Python CLI that:

- reads integer PCM WAV files (8/16/24/32 bit) and mixes channels to mono;
- creates an SVG spectrogram over the audible range using a logarithmic
  frequency axis;
- emits a JSON summary with required signal metadata;
- validates invalid input and dimensions; and
- includes tests and documentation.

An evaluator outside the worktrees ran seven acceptance checks: valid WAV
execution, SVG creation, JSON creation and schema, metadata, duration, and
failure on invalid input.

## Variants and observed results

| Variant | Agent sequence | Acceptance | Duration | Total tokens | New input tokens |
| --- | --- | ---: | ---: | ---: | ---: |
| Luna direct | `gpt-5.6-luna`, medium | 7/7 | 171.1 s | 209,897 | 20,074 |
| Terra direct | `gpt-5.6-terra`, medium | 7/7 | 125.7 s | 160,088 | 12,566 |
| Luna plan, Terra implementation, Luna review | Luna low → Terra medium → Luna low | 7/7 | 284.6 s | 517,507 | 46,376 |
| Terra plan, Luna implementation | Terra low → Luna medium | 7/7 | 216.4 s | 302,897 | 30,477 |

`New input tokens` means `input_tokens - cached_input_tokens`. Total-token
figures include cached input and are useful for provider load visibility, but
are not a direct billing calculation.

## Follow-up: automatic RTK and Logics context disabled

On the same date, the direct Luna, direct Terra, and Terra-plan/Luna-implementation
variants were repeated using dedicated `cdx` profiles with both `rtk=off` and
`logics=off`. The prompt, model, effort, base commit, external evaluator, and
fresh worktree remained the same. This is a one-run comparison, not an isolated
causal measurement: agent paths and provider cache state are still variable.

| Variant | Acceptance | Duration | Total tokens | Cached input | New input tokens | Test outcome |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| Luna direct, context off | 7/7 | 121.6 s | 132,382 | 106,496 | 20,081 | 3 `unittest` tests passed |
| Terra direct, context off | 7/7 | 122.7 s | 138,584 | 118,272 | 14,344 | no discoverable `unittest` suite |
| Terra plan low, context off | n/a (planning) | 61.5 s | 78,862 | 67,328 | 8,842 | plan written to `PLAN.md` |
| Luna implementation medium, context off | 7/7 | 208.5 s | 301,720 | 252,672 | 38,733 | 7 `unittest` tests passed |
| Terra plan → Luna implementation, context off (sum) | 7/7 | 270.1 s | 380,582 | 320,000 | 47,575 | 7 `unittest` tests passed |

Compared with the original direct Luna run, disabling the two automatic
contexts coincided with a 37% reduction in total tokens and a 29% reduction in
elapsed time, while new input remained virtually unchanged (20,081 vs 20,074).
That points to repeated/cached context and changed interaction trajectory—not
to the automatic context being the entire prompt cost. Direct Terra also used
fewer total tokens (138,584 vs 160,088), but its new input was higher and it
did not leave a standard-library test suite. The two-step chain was worse in
this repeat: 25% more total tokens and 25% more time than its original run,
because the Luna implementation took more corrective iterations. Therefore do
not use the flags as a universal performance switch; reproduce the test in
randomized order before changing defaults.

## Qualitative findings

- The direct Terra run was the fastest and lowest-token successful variant.
- The direct Luna run also passed the external evaluator, but its tests used
  `pytest`; the application had no runtime dependency, yet the test command
  depended on a tool not declared by the benchmark.
- The Luna-plan/Terra-implementation/review chain had the richest evidence:
  eight standard-library tests, a plan, and an independent review. Its review
  found no blocking or important defect, so no repair pass was run.
- The Terra-plan/Luna-implementation chain added useful implementation detail,
  including atomic output writing and a guard against 32-bit floating-point
  WAV containers. It still cost substantially more than direct Terra without a
  measurable acceptance-score increase on this task.

## Interpretation

For a self-contained feature of a few files, direct Terra was the best
observed trade-off. A multi-agent chain should be selected for work where a
separate plan or review can plausibly prevent a costly defect, for example:

- security-sensitive changes;
- schema or data migrations;
- concurrency and distributed-state work;
- architecture spanning several modules or services;
- external integrations; or
- release-critical changes.

The current multi-agent variants were manually sequenced through `cdx`; the
MVP Orchestrato execution path currently invokes one executor and does not yet
automatically run a planner, reviewer, or repair wave. This benchmark therefore
identifies a product gap as well as a routing signal.

## Method limitations and next experiment

- This is one trial per variant, run sequentially through the same provider
  session; cache warmth and provider state can affect the figures.
- The benchmark does not measure monetary cost because no pricing data was
  recorded.
- All variants passed the same small external evaluator, so its acceptance
  score cannot distinguish more subtle quality differences.

Repeat this experiment at least three times per variant with randomized order,
fresh worktrees, and a broader hidden evaluator. Record run IDs, token usage,
elapsed time, retries, review findings, and required human corrections. The
decision criterion should be defects prevented or human rework avoided—not
token count alone.

## Reproducibility artifacts

The local worktrees and external evaluator are under `/home/paulm/dev/Work/`:

- `orchestrato-benchmark-audio` (base specification)
- `orchestrato-benchmark-luna`
- `orchestrato-benchmark-terra`
- `orchestrato-benchmark-multi`
- `orchestrato-benchmark-terra-plan-luna-impl`
- `orchestrato-benchmark-luna-no-context`
- `orchestrato-benchmark-terra-no-context`
- `orchestrato-benchmark-terra-plan-luna-no-context`
- `orchestrato-benchmark-evaluate.py`

These paths are deliberately not part of the repository contract; this report
contains the durable findings needed for later design work.
