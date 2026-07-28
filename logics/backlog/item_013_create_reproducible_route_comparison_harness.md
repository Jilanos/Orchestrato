## item_013_create_reproducible_route_comparison_harness - Create reproducible route-comparison harness
> From version: 1.0.0
> Schema version: 1.0
> Status: Done
> Understanding: 90%
> Confidence: 85%
> Progress: 100%
> Complexity: Medium
> Theme: Benchmarking
> Reminder: Update status/understanding/confidence/progress and linked request/task references when you edit this doc.

# Problem
- The exploratory benchmark is valuable but lacks a versioned harness and a no-cost dry-run workflow.

# Scope
- In:
  - Scenario manifest
  - route matrix
  - dry-run validation
  - opt-in live launcher
  - isolated artifacts under WORK
- Out:
  - Automatic paid live execution
  - benchmarking unrelated repositories without explicit setup

# Acceptance criteria
- AC1: The harness defines the four comparison routes and validates all manifests without provider execution.
- AC2: Live execution requires an explicit --execute flag and writes only under the designated WORK directory.

# AC Traceability
- request-AC4 -> This backlog slice. Proof: AC1: The harness defines the four comparison routes and validates all manifests without provider execution.
- request-AC2 -> This backlog slice. Evidence needed: Orchestrato builds role-specific bounded handoff packets from explicit task references and configurable limits, without injecting full workflow or transcript history by default.
- request-AC3 -> This backlog slice. Evidence needed: Policy can select direct execution by default and escalate planning, review, or recovery only from explicit risk, validation, or failure evidence.
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
- Summary: Create reproducible route-comparison harness
- Keywords: scaffolded-backlog, create reproducible route-comparison harness, implementation-ready
- Use when: Implementing the scaffolded slice for Create reproducible route-comparison harness.
- Skip when: The change belongs to another backlog slice.

# Priority
- Priority: High
- Rationale: Set by scaffold input or defaulted for grooming.

# Tasks
- `task_004_deliver_cost_of_pass_control_plane_and_benchmark_harness`

# Notes
- Task `task_004_deliver_cost_of_pass_control_plane_and_benchmark_harness` was finished via `logics-manager flow finish task` on 2026-07-28.
