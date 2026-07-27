## item_009_persist_and_test_cdx_failure_diagnostics - Persist and test cdx failure diagnostics
> From version: 1.0.0
> Schema version: 1.0
> Status: Done
> Understanding: 90%
> Confidence: 85%
> Progress: 100%
> Complexity: Medium
> Theme: Observability
> Reminder: Update status/understanding/confidence/progress and linked request/task references when you edit this doc.

# Problem
- The CLI and stored objective history do not currently give the operator enough evidence to resolve a failed live execution.

# Scope
- In:
  - Publish and persist safe cdx failure diagnostics as execution events.
  - Return the diagnostic from JSON failure output without corrupting stdout protocol behavior.
  - Add deterministic fake-cdx tests for populated and empty failure output plus redaction.
- Out:
  - Live provider-account tests or external telemetry.

# Acceptance criteria
- AC1: Inspect output reconstructs the safe cdx failure diagnostic after process exit.
- AC2: JSON error output exposes a concise safe diagnostic.
- AC3: Offline tests verify populated output, empty output, and secret redaction.

# AC Traceability
- request-AC2 -> This backlog slice. Proof: AC1: Inspect output reconstructs the safe cdx failure diagnostic after process exit.
- request-AC3 -> This backlog slice. Proof: AC2: JSON error output exposes a concise safe diagnostic.
- request-AC4 -> This backlog slice. Proof: AC3: Offline tests verify populated output, empty output, and secret redaction.

# Decision framing
- Product framing: Not needed
- Architecture framing: Not needed

# Links
- Product brief(s): `prod_002_actionable_cdx_failure_reporting`
- Architecture decision(s): (none yet)
- Request: `req_002_expose_actionable_cdx_execution_failure_diagnostics`
- Primary task(s): `task_003_deliver_actionable_cdx_execution_diagnostics`

# AI Context
- Summary: Persist and test cdx failure diagnostics
- Keywords: scaffolded-backlog, persist and test cdx failure diagnostics, implementation-ready
- Use when: Implementing the scaffolded slice for Persist and test cdx failure diagnostics.
- Skip when: The change belongs to another backlog slice.

# Priority
- Priority: High
- Rationale: Set by scaffold input or defaulted for grooming.

# Tasks
- `task_003_deliver_actionable_cdx_execution_diagnostics`

# Notes
- Task `task_003_deliver_actionable_cdx_execution_diagnostics` was finished via `logics-manager flow finish task` on 2026-07-27.
