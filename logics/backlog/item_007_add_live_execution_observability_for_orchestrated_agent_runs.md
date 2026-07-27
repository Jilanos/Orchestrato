## item_007_add_live_execution_observability_for_orchestrated_agent_runs - Add live execution observability for orchestrated agent runs
> From version: 1.0.0
> Schema version: 1.0
> Status: Done
> Understanding: 90%
> Confidence: 85%
> Progress: 100%
> Complexity: High
> Theme: Operator workflow and runtime integration
> Reminder: Update status/understanding/confidence/progress and linked request/task references when you edit this doc.

# Problem
Give operators a live, trustworthy view of every Orchestrato execution. Once an objective is approved, the current CLI becomes a black box until `cdx run` returns; the operator cannot see which agent was selected, what it is doing, whether it is blocked, or whether work is still progressing.
Make the execution path observable without treating agent prose as control input. The view must expose route selection, permissions, provider/session references, lifecycle transitions, live work evidence, validation activity, failures, retries, usage, and the final outcome.
Deliver a local operator experience first. A Rich TUI is the primary surface; a browser viewer may consume the same local event stream later without creating a separate orchestration model.

# Scope
- In:
  - one coherent delivery slice from the source request
- Out:
  - unrelated sibling slices that should stay in separate backlog items instead of widening this doc

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

# AC Traceability
- request-AC1 -> This backlog slice. Proof: AC1: Within one second of a run starting, the local live surface shows the objective ID, selected role, provider, model when known, reasoning effort, permission, worktree path, linked Logics refs, and current lifecycle state.
- request-AC2 -> This backlog slice. Proof: AC2: The surface renders an ordered timeline of normalized events: route selected, approval requested or granted, cdx session selected, run started, agent phase or message, command started and finished when available, file or artifact change, validation result, retry or recovery decision, and terminal result.
- request-AC3 -> This backlog slice. Proof: AC3: Every displayed event is persisted with a stable sequence, timestamp, source, correlation to objective/step/run, and bounded payload. Restarting Orchestrato reconstructs the same timeline and reconciles any in-flight cdx run before declaring an outcome.
- request-AC4 -> This backlog slice. Proof: AC4: The UI distinguishes observed facts, inferred liveness, and unknown state. It may display a stale-run warning after a configurable silence interval, but may not display fabricated progress percentages or mark a phase complete without evidence.
- request-AC5 -> This backlog slice. Proof: AC5: The operator can inspect live and completed run details, including elapsed duration, attempts, cdx run ID, usage and cost metadata when supplied, artifact paths, changed-file summary, validation commands and results, blockers, and residual risks.
- request-AC6 -> This backlog slice. Proof: AC6: When cdx does not provide a stream, the supervisor falls back to bounded polling of stable cdx JSON status and incremental transcript/artifact collection. A failed or malformed external observation produces an explicit warning while the run continues to be reconciled safely.
- request-AC7 -> This backlog slice. Proof: AC7: A compact Rich TUI is available from the CLI for local observation. It supports a concise summary mode and a detail mode without changing the existing machine-readable JSON command contract.
- request-AC8 -> This backlog slice. Proof: AC8: The design defines a local event publication boundary so a future read-only browser viewer can consume the same timeline without duplicating state, polling cdx independently, or gaining authority to trigger transitions.
- request-AC9 -> This backlog slice. Proof: AC9: Prompts, credentials, environment values, and unbounded provider output are redacted or summarized by default. The view clearly displays the active permission and never exposes secrets from subprocess output.
- request-AC10 -> This backlog slice. Proof: AC10: Contract tests with fake cdx-manager and Logics Manager cover ordered events, reconnect/restart reconciliation, stream fallback, stale detection, redaction, terminal-state immutability, and rendering of success, failure, recovery, cancellation, and blocked runs.

# Decision framing
- Product framing: Not needed
- Product signals: (none detected)
- Product follow-up: No product brief follow-up is expected based on current signals.
- Architecture framing: Not needed
- Architecture signals: (none detected)
- Architecture follow-up: No architecture decision follow-up is expected based on current signals.

# Links
- Product brief(s): (none yet)
- Architecture decision(s): (none yet)
- Request: `req_001_add_live_execution_observability_for_orchestrated_agent_runs`
- Primary task(s): `task_002_add_live_execution_observability_for_orchestrated_agent_runs`

# AI Context
- Summary: Add live execution observability for orchestrated agent runs
- Keywords: backlog-groom, request, add live execution observability for orchestrated agent runs, bounded slice
- Use when: Use when implementing or reviewing the delivery slice for Add live execution observability for orchestrated agent runs.
- Skip when: Skip when the change is unrelated to this delivery slice or its linked request.

# Priority
- Priority: Medium
- Rationale: Default until groomed.

# Notes
- Hybrid rationale: Derived from request `req_001_add_live_execution_observability_for_orchestrated_agent_runs` and kept bounded to one coherent delivery slice.
- Source file: `logics/request/req_001_add_live_execution_observability_for_orchestrated_agent_runs.md`.
- Generated locally by logics-manager.
- Task `task_002_add_live_execution_observability_for_orchestrated_agent_runs` was finished via `logics-manager flow finish task` on 2026-07-27.

# Tasks
- `task_002_add_live_execution_observability_for_orchestrated_agent_runs`
