## item_015_test_cost_aware_orchestration_contracts - Test cost-aware orchestration contracts
> From version: 1.0.0
> Schema version: 1.0
> Status: Done
> Understanding: 90%
> Confidence: 85%
> Progress: 100%
> Complexity: Medium
> Theme: Quality assurance
> Reminder: Update status/understanding/confidence/progress and linked request/task references when you edit this doc.

# Problem
- Cost and context controls need deterministic regression coverage before live benchmarking is trusted.

# Scope
- In:
  - Unit tests
  - fake cdx and Logics contracts
  - fixture run records
  - harness dry-run tests
- Out:
  - Live provider accounts
  - acceptance claims from synthetic fixtures

# Acceptance criteria
- AC1: Tests cover normalized usage, packet limits, route gates, aggregation, and explicit live-run opt-in.
- AC2: The default test command performs no provider call and passes with fake executables.

# AC Traceability
- request-AC6 -> This backlog slice. Proof: AC1: Tests cover normalized usage, packet limits, route gates, aggregation, and explicit live-run opt-in.
- request-AC2 -> This backlog slice. Evidence needed: Orchestrato builds role-specific bounded handoff packets from explicit task references and configurable limits, without injecting full workflow or transcript history by default.
- request-AC3 -> This backlog slice. Evidence needed: Policy can select direct execution by default and escalate planning, review, or recovery only from explicit risk, validation, or failure evidence.
- request-AC4 -> This backlog slice. Evidence needed: A reproducible benchmark harness compares direct minimal-context, direct expanded-context, adaptive orchestration, and fixed plan-implement-review routes without running providers by default.
- request-AC5 -> This backlog slice. Evidence needed: Benchmark reports compute pass rate, cost-of-pass, total/new/cached/output tokens, latency, retries, and human-rework fields, and preserve raw run references.

# Decision framing
- Product framing: Not needed
- Architecture framing: Not needed

# Links
- Product brief(s): `prod_003_cost_of_pass_control_plane`
- Architecture decision(s): (none yet)
- Request: `req_003_measure_and_optimize_orchestrato_cost_of_pass`
- Primary task(s): `task_004_deliver_cost_of_pass_control_plane_and_benchmark_harness`

# AI Context
- Summary: Test cost-aware orchestration contracts
- Keywords: scaffolded-backlog, test cost-aware orchestration contracts, implementation-ready
- Use when: Implementing the scaffolded slice for Test cost-aware orchestration contracts.
- Skip when: The change belongs to another backlog slice.

# Priority
- Priority: High
- Rationale: Set by scaffold input or defaulted for grooming.

# Tasks
- `task_004_deliver_cost_of_pass_control_plane_and_benchmark_harness`

# Notes
- Task `task_004_deliver_cost_of_pass_control_plane_and_benchmark_harness` was finished via `logics-manager flow finish task` on 2026-07-28.
