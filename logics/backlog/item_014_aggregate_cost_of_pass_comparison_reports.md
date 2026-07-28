## item_014_aggregate_cost_of_pass_comparison_reports - Aggregate cost-of-pass comparison reports
> From version: 1.0.0
> Schema version: 1.0
> Status: Done
> Understanding: 90%
> Confidence: 85%
> Progress: 100%
> Complexity: Medium
> Theme: Benchmark analysis
> Reminder: Update status/understanding/confidence/progress and linked request/task references when you edit this doc.

# Problem
- Route results need a common outcome-aware aggregation instead of a total-token-only comparison.

# Scope
- In:
  - Schema validation
  - aggregation
  - cost-of-pass calculations
  - CSV and Markdown reporting
  - confidence and limitation fields
- Out:
  - Pricing advice
  - statistical claims below the configured sample threshold

# Acceptance criteria
- AC1: A report exposes pass rate and each token category per route alongside latency, retries, and human-rework fields.
- AC2: Cost-of-pass is undefined and clearly reported when a route has no successful run.

# AC Traceability
- request-AC5 -> This backlog slice. Proof: AC1: A report exposes pass rate and each token category per route alongside latency, retries, and human-rework fields.
- request-AC2 -> This backlog slice. Evidence needed: Orchestrato builds role-specific bounded handoff packets from explicit task references and configurable limits, without injecting full workflow or transcript history by default.
- request-AC3 -> This backlog slice. Evidence needed: Policy can select direct execution by default and escalate planning, review, or recovery only from explicit risk, validation, or failure evidence.
- request-AC4 -> This backlog slice. Evidence needed: A reproducible benchmark harness compares direct minimal-context, direct expanded-context, adaptive orchestration, and fixed plan-implement-review routes without running providers by default.
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
- Summary: Aggregate cost-of-pass comparison reports
- Keywords: scaffolded-backlog, aggregate cost-of-pass comparison reports, implementation-ready
- Use when: Implementing the scaffolded slice for Aggregate cost-of-pass comparison reports.
- Skip when: The change belongs to another backlog slice.

# Priority
- Priority: Medium
- Rationale: Set by scaffold input or defaulted for grooming.

# Tasks
- `task_004_deliver_cost_of_pass_control_plane_and_benchmark_harness`

# Notes
- Task `task_004_deliver_cost_of_pass_control_plane_and_benchmark_harness` was finished via `logics-manager flow finish task` on 2026-07-28.
