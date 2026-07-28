## item_010_persist_normalized_cost_of_pass_run_evidence - Persist normalized cost-of-pass run evidence
> From version: 1.0.0
> Schema version: 1.0
> Status: Done
> Understanding: 90%
> Confidence: 85%
> Progress: 100%
> Complexity: High
> Theme: Observability
> Reminder: Update status/understanding/confidence/progress and linked request/task references when you edit this doc.

# Problem
- Existing run persistence does not yet expose a complete, comparable usage and outcome record.

# Scope
- In:
  - Typed usage model
  - normalized cdx usage extraction
  - event-store persistence
  - safe inspection output
- Out:
  - Provider billing integration
  - storage of raw prompts or credentials

# Acceptance criteria
- AC1: Each completed execution persists normalized token categories, route, duration, retries, validation status, and raw run reference.

# AC Traceability
- request-AC1 -> This backlog slice. Proof: AC1: Each completed execution persists normalized token categories, route, duration, retries, validation status, and raw run reference.
- request-AC2 -> This backlog slice. Evidence needed: Orchestrato builds role-specific bounded handoff packets from explicit task references and configurable limits, without injecting full workflow or transcript history by default.
- request-AC3 -> This backlog slice. Evidence needed: Policy can select direct execution by default and escalate planning, review, or recovery only from explicit risk, validation, or failure evidence.
- request-AC4 -> This backlog slice. Evidence needed: A reproducible benchmark harness compares direct minimal-context, direct expanded-context, adaptive orchestration, and fixed plan-implement-review routes without running providers by default.
- request-AC5 -> This backlog slice. Evidence needed: Benchmark reports compute pass rate, cost-of-pass, total/new/cached/output tokens, latency, retries, and human-rework fields, and preserve raw run references.
- request-AC6 -> This backlog slice. Evidence needed: Contract and analysis tests cover usage normalization, context budgets, escalation gates, aggregation, and no-live-run defaults.

# Decision framing
- Product framing: Not needed
- Architecture framing: Not needed

# Links
- Product brief(s): `prod_003_cost_of_pass_control_plane`
- Architecture decision(s): (none yet)
- Request: `req_003_measure_and_optimize_orchestrato_cost_of_pass`
- Primary task(s): `task_004_deliver_cost_of_pass_control_plane_and_benchmark_harness`

# AI Context
- Summary: Persist normalized cost-of-pass run evidence
- Keywords: scaffolded-backlog, persist normalized cost-of-pass run evidence, implementation-ready
- Use when: Implementing the scaffolded slice for Persist normalized cost-of-pass run evidence.
- Skip when: The change belongs to another backlog slice.

# Priority
- Priority: High
- Rationale: Set by scaffold input or defaulted for grooming.

# Tasks
- `task_004_deliver_cost_of_pass_control_plane_and_benchmark_harness`

# Notes
- Task `task_004_deliver_cost_of_pass_control_plane_and_benchmark_harness` was finished via `logics-manager flow finish task` on 2026-07-28.
