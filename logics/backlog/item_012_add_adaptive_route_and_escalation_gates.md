## item_012_add_adaptive_route_and_escalation_gates - Add adaptive route and escalation gates
> From version: 1.0.0
> Schema version: 1.0
> Status: Done
> Understanding: 90%
> Confidence: 85%
> Progress: 100%
> Complexity: High
> Theme: Routing policy
> Reminder: Update status/understanding/confidence/progress and linked request/task references when you edit this doc.

# Problem
- The routing policy identifies roles but does not yet optimize the direct path and conditional escalation around risk and evidence.

# Scope
- In:
  - Task-risk signals
  - direct path
  - planning/review gates
  - bounded recovery
  - explainable route decisions
- Out:
  - Unbounded multi-agent swarms
  - model-provider pricing predictions

# Acceptance criteria
- AC1: Low-risk bounded work takes a direct path unless an explicit policy signal requires escalation.
- AC2: Review and recovery run only after policy-required risk evidence or failed deterministic validation.

# AC Traceability
- request-AC3 -> This backlog slice. Proof: AC1: Low-risk bounded work takes a direct path unless an explicit policy signal requires escalation.
- request-AC2 -> This backlog slice. Evidence needed: Orchestrato builds role-specific bounded handoff packets from explicit task references and configurable limits, without injecting full workflow or transcript history by default.
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
- Summary: Add adaptive route and escalation gates
- Keywords: scaffolded-backlog, add adaptive route and escalation gates, implementation-ready
- Use when: Implementing the scaffolded slice for Add adaptive route and escalation gates.
- Skip when: The change belongs to another backlog slice.

# Priority
- Priority: High
- Rationale: Set by scaffold input or defaulted for grooming.

# Tasks
- `task_004_deliver_cost_of_pass_control_plane_and_benchmark_harness`

# Notes
- Task `task_004_deliver_cost_of_pass_control_plane_and_benchmark_harness` was finished via `logics-manager flow finish task` on 2026-07-28.
