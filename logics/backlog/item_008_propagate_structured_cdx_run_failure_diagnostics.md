## item_008_propagate_structured_cdx_run_failure_diagnostics - Propagate structured cdx run failure diagnostics
> From version: 1.0.0
> Schema version: 1.0
> Status: Done
> Understanding: 90%
> Confidence: 85%
> Progress: 100%
> Complexity: Medium
> Theme: Runtime integration
> Reminder: Update status/understanding/confidence/progress and linked request/task references when you edit this doc.

# Problem
- The adapter discards the specific subprocess failure reason, leaving operators with only cdx run failed.

# Scope
- In:
  - Capture exit code and bounded stderr or stdout failure context from cdx run.
  - Represent the failure with a typed diagnostic that can be handled by the supervisor.
  - Apply existing redaction rules before emitting the diagnostic.
- Out:
  - Provider-specific SDK calls or authentication changes.

# Acceptance criteria
- AC1: A failing cdx run preserves its exit code and a safe, bounded diagnostic message.
- AC2: Empty subprocess output still results in a stable actionable fallback diagnostic.
- AC3: Diagnostic text is redacted before it can leave the adapter boundary.

# AC Traceability
- request-AC1 -> This backlog slice. Proof: AC1: A failing cdx run preserves its exit code and a safe, bounded diagnostic message.
- request-AC3 -> This backlog slice. Proof: AC2: Empty subprocess output still results in a stable actionable fallback diagnostic.
- request-AC4 -> This backlog slice. Evidence needed: Offline contract tests cover a cdx run failure with diagnostic output and a failure without diagnostic output.

# Decision framing
- Product framing: Not needed
- Architecture framing: Not needed

# Links
- Product brief(s): `prod_002_actionable_cdx_failure_reporting`
- Architecture decision(s): (none yet)
- Request: `req_002_expose_actionable_cdx_execution_failure_diagnostics`
- Primary task(s): `task_003_deliver_actionable_cdx_execution_diagnostics`

# AI Context
- Summary: Propagate structured cdx run failure diagnostics
- Keywords: scaffolded-backlog, propagate structured cdx run failure diagnostics, implementation-ready
- Use when: Implementing the scaffolded slice for Propagate structured cdx run failure diagnostics.
- Skip when: The change belongs to another backlog slice.

# Priority
- Priority: High
- Rationale: Set by scaffold input or defaulted for grooming.

# Tasks
- `task_003_deliver_actionable_cdx_execution_diagnostics`

# Notes
- Task `task_003_deliver_actionable_cdx_execution_diagnostics` was finished via `logics-manager flow finish task` on 2026-07-27.
