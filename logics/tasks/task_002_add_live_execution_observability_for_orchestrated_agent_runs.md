## task_002_add_live_execution_observability_for_orchestrated_agent_runs - Add live execution observability for orchestrated agent runs
> From version: 1.0.0
> Schema version: 1.0
> Status: Done
> Understanding: 90%
> Confidence: 85%
> Progress: 100%
> Complexity: Medium
> Theme: Implementation delivery
> Reminder: Update status/understanding/confidence/progress and linked request/backlog references when you edit this doc.
> Owner: codex

# Definition of Done (DoD)
- [x] The backlog scope is implemented.
- [x] Acceptance criteria are covered.
- [x] Validation passes.
- [x] Meaningful waves followed ADR 009: affected docs updated and the repo left commit-ready without automatic commits.

# Backlog
- `item_007_add_live_execution_observability_for_orchestrated_agent_runs`

# Acceptance criteria
- AC1: Within one second of a run starting, the local live surface shows the objective ID, selected role, provider, model when known, reasoning effort, permission, worktree path, linked Logics refs, and current lifecycle state.
- AC2: The surface renders an ordered timeline of normalized events: route selected, approval requested or granted, cdx session selected, run started, agent phase or message, command started and finished when available, file or artifact change, validation result, retry or recovery decision, and terminal result.
- AC3: Every displayed event is persisted with a stable sequence, timestamp, source, correlation to objective/step/run, and bounded payload. Restarting Orchestrato reconstructs the same timeline and reconciles any in-flight cdx run before declaring an outcome.
- AC4: The UI distinguishes observed facts, inferred liveness, and unknown state. It may display a stale-run warning after a configurable silence interval, but may not display fabricated progress percentages or mark a phase complete without evidence.
- AC5: The operator can inspect live and completed run details, including elapsed duration, attempts, cdx run ID, usage and cost metadata when supplied, artifact paths, changed-file summary, validation commands and results, blockers, and residual risks.
- AC6: When cdx does not provide a stream, the supervisor falls back to bounded polling of stable cdx JSON status and incremental transcript/artifact collection. A failed or malformed external observation produces an explicit warning while the run continues to be reconciled safely.
- AC7: A compact Rich TUI is available from the CLI for local observation. It supports a concise summary mode and a detail mode without changing the existing machine-readable JSON command contract.
- AC8: The design defines a local event publication boundary so a future read-only browser viewer can consume the same timeline without duplicating state, polling cdx independently, or gaining authority to trigger transitions.
- AC9: Prompts, credentials, environment values, and unbounded provider output are redacted or summarized by default. The view clearly displays the active permission and never exposes secrets from subprocess output.
- AC10: Contract tests with fake cdx-manager and Logics Manager cover ordered events, reconnect/restart reconciliation, stream fallback, stale detection, redaction, terminal-state immutability, and rendering of success, failure, recovery, cancellation, and blocked runs.

# Validation
- Run `python3 -m logics_manager lint --require-status`.
- Use `python3 -m logics_manager flow progress task task_002_add_live_execution_observability_for_orchestrated_agent_runs.md --progress <n>%` during multi-wave work.
- Run `python3 -m logics_manager flow finish task task_002_add_live_execution_observability_for_orchestrated_agent_runs.md` after implementation.
- Finish workflow executed on 2026-07-27.
- Linked backlog/request close verification passed.

# Report
- Implementation complete.
- Finished on 2026-07-27.
- Linked backlog item(s): `item_007_add_live_execution_observability_for_orchestrated_agent_runs`
- Related request(s): `req_001_add_live_execution_observability_for_orchestrated_agent_runs`

# AI Context
- Summary: Implement add live execution observability for orchestrated agent runs.
- Keywords: task, implementation, backlog, runtime, python
- Use when: You need a bounded implementation task for a backlog item.
- Skip when: The work is still at the request or backlog shaping stage.

# Links
- Request: `req_001_add_live_execution_observability_for_orchestrated_agent_runs`
- Product brief(s): (none yet)
- Architecture decision(s): (none yet)

# AC Traceability
- request-AC1 -> This task. Proof: Within one second of a run starting, the local live surface shows the objective ID, selected role, provider, model when known, reasoning effort, permission, worktree path, linked Logics refs, and current lifecycle state.
- request-AC2 -> This task. Proof: The surface renders an ordered timeline of normalized events: route selected, approval requested or granted, cdx session selected, run started, agent phase or message, command started and finished when available, file or artifact change, validation result, retry or recovery decision, and terminal result.
- request-AC3 -> This task. Proof: Every displayed event is persisted with a stable sequence, timestamp, source, correlation to objective/step/run, and bounded payload. Restarting Orchestrato reconstructs the same timeline and reconciles any in-flight cdx run before declaring an outcome.
- request-AC4 -> This task. Proof: The UI distinguishes observed facts, inferred liveness, and unknown state. It may display a stale-run warning after a configurable silence interval, but may not display fabricated progress percentages or mark a phase complete without evidence.
- request-AC5 -> This task. Proof: The operator can inspect live and completed run details, including elapsed duration, attempts, cdx run ID, usage and cost metadata when supplied, artifact paths, changed-file summary, validation commands and results, blockers, and residual risks.
- request-AC6 -> This task. Proof: When cdx does not provide a stream, the supervisor falls back to bounded polling of stable cdx JSON status and incremental transcript/artifact collection. A failed or malformed external observation produces an explicit warning while the run continues to be reconciled safely.
- request-AC7 -> This task. Proof: A compact Rich TUI is available from the CLI for local observation. It supports a concise summary mode and a detail mode without changing the existing machine-readable JSON command contract.
- request-AC8 -> This task. Proof: The design defines a local event publication boundary so a future read-only browser viewer can consume the same timeline without duplicating state, polling cdx independently, or gaining authority to trigger transitions.
- request-AC9 -> This task. Proof: Prompts, credentials, environment values, and unbounded provider output are redacted or summarized by default. The view clearly displays the active permission and never exposes secrets from subprocess output.
- request-AC10 -> This task. Proof: Contract tests with fake cdx-manager and Logics Manager cover ordered events, reconnect/restart reconciliation, stream fallback, stale detection, redaction, terminal-state immutability, and rendering of success, failure, recovery, cancellation, and blocked runs.
- request-AC1 -> This task. Evidence needed: Within one second of a run starting, the local live surface shows the objective ID, selected role, provider, model when known, reasoning effort, permission, worktree path, linked Logics refs, and current lifecycle state.
- request-AC2 -> This task. Evidence needed: The surface renders an ordered timeline of normalized events: route selected, approval requested or granted, cdx session selected, run started, agent phase or message, command started and finished when available, file or artifact change, validation result, retry or recovery decision, and terminal result.
- request-AC3 -> This task. Evidence needed: Every displayed event is persisted with a stable sequence, timestamp, source, correlation to objective/step/run, and bounded payload. Restarting Orchestrato reconstructs the same timeline and reconciles any in-flight cdx run before declaring an outcome.
- request-AC4 -> This task. Evidence needed: The UI distinguishes observed facts, inferred liveness, and unknown state. It may display a stale-run warning after a configurable silence interval, but may not display fabricated progress percentages or mark a phase complete without evidence.
- request-AC5 -> This task. Evidence needed: The operator can inspect live and completed run details, including elapsed duration, attempts, cdx run ID, usage and cost metadata when supplied, artifact paths, changed-file summary, validation commands and results, blockers, and residual risks.
- request-AC6 -> This task. Evidence needed: When cdx does not provide a stream, the supervisor falls back to bounded polling of stable cdx JSON status and incremental transcript/artifact collection. A failed or malformed external observation produces an explicit warning while the run continues to be reconciled safely.
- request-AC7 -> This task. Evidence needed: A compact Rich TUI is available from the CLI for local observation. It supports a concise summary mode and a detail mode without changing the existing machine-readable JSON command contract.
- request-AC8 -> This task. Evidence needed: The design defines a local event publication boundary so a future read-only browser viewer can consume the same timeline without duplicating state, polling cdx independently, or gaining authority to trigger transitions.
- request-AC9 -> This task. Evidence needed: Prompts, credentials, environment values, and unbounded provider output are redacted or summarized by default. The view clearly displays the active permission and never exposes secrets from subprocess output.
- request-AC10 -> This task. Evidence needed: Contract tests with fake cdx-manager and Logics Manager cover ordered events, reconnect/restart reconciliation, stream fallback, stale detection, redaction, terminal-state immutability, and rendering of success, failure, recovery, cancellation, and blocked runs.
