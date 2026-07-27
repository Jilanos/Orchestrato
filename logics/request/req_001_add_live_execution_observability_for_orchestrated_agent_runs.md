## req_001_add_live_execution_observability_for_orchestrated_agent_runs - Add live execution observability for orchestrated agent runs
> From version: 1.0.0
> Schema version: 1.0
> Status: Done
> Understanding: 95
> Confidence: 85
> Complexity: High
> Theme: Execution observability
> Reminder: Update status/understanding/confidence and linked backlog/task references when you edit this doc.

# Needs
- Give operators a live, trustworthy view of every Orchestrato execution. Once an objective is approved, the current CLI becomes a black box until `cdx run` returns; the operator cannot see which agent was selected, what it is doing, whether it is blocked, or whether work is still progressing.
- Make the execution path observable without treating agent prose as control input. The view must expose route selection, permissions, provider/session references, lifecycle transitions, live work evidence, validation activity, failures, retries, usage, and the final outcome.
- Deliver a local operator experience first. A Rich TUI is the primary surface; a browser viewer may consume the same local event stream later without creating a separate orchestration model.

# Context
- Orchestrato already persists objectives, routes, and state transitions in SQLite, but its cdx adapter calls `cdx run` synchronously and only receives the final JSON response.
- cdx-manager exposes run identifiers, `runs`, `run-status`, `run-report`, and per-run transcript/stdout/stderr artifacts. These are the initial sources for live evidence; a provider-native streaming surface may be added when cdx exposes a stable contract for it.
- Logics Manager owns requests, backlog, tasks, context packs, and validation. The live view should display linked Logics references and their acceptance criteria, but must not mutate workflow state merely because an agent emitted text.
- The existing product brief deferred a full-screen TUI and browser control plane from the MVP. This request scopes a local, read-only execution-observability capability as a subsequent product increment.
- Progress must be evidence-based. A UI may show completed phases and a current activity, but must never fabricate a percentage from elapsed time or free-form agent claims.

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

# Definition of Ready (DoR)
- [x] Problem statement is explicit and user impact is clear.
- [x] Scope boundaries (in/out) are explicit.
- [x] Acceptance criteria are testable.
- [x] Dependencies and known risks are listed.

# Companion docs
- Product brief(s): `prod_001_orchestrato_mvp_product_brief`
- Architecture decision(s): `adr_001_keep_orchestrato_behind_cli_contracts`, `adr_002_use_a_persisted_finite_orchestration_state_machine`

# References
- `README.md`
- `docs/product.md`
- `docs/architecture.md`
- `src/orchestrato/application.py`
- `src/orchestrato/supervisor.py`
- `src/orchestrato/store.py`
- `src/orchestrato/adapters/cdx.py`
- cdx-manager JSON contracts: `select`, `run`, `runs`, `run-status`, and `run-report`
- Logics Manager local viewer and bounded context contracts

# AI Context
- Summary: Add evidence-based live observability for Orchestrato runs through a persisted normalized event timeline, local Rich TUI, cdx polling/transcript fallback, safe redaction, and a future viewer publication boundary.
- Keywords: live-observability, run-timeline, rich-tui, cdx-run-status, cdx-transcript, event-store, event-stream, stale-detection, redaction, reconciliation
- Use when: You need to plan, implement, review, or test the operator-visible execution timeline for Orchestrato.
- Skip when: The work only changes routing policy, static Logics documents, or cdx provider selection without affecting operator-visible live run state.

# Backlog
- none
- `item_007_add_live_execution_observability_for_orchestrated_agent_runs`
