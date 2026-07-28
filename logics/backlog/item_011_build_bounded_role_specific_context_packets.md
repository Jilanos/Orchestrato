## item_011_build_bounded_role_specific_context_packets - Build bounded role-specific context packets
> From version: 1.0.0
> Schema version: 1.0
> Status: Done
> Understanding: 90%
> Confidence: 85%
> Progress: 100%
> Complexity: High
> Theme: Context engineering
> Reminder: Update status/understanding/confidence/progress and linked request/task references when you edit this doc.

# Problem
- Current execution writes a minimal prompt and does not integrate the available Logics context-pack adapter.

# Scope
- In:
  - Task-packet schema
  - Logics context-pack consumption
  - per-role projections
  - size limits
  - structured summaries
- Out:
  - Full transcript replay
  - automatic semantic retrieval service

# Acceptance criteria
- AC1: Planner, executor, reviewer, and recovery prompts receive only their role-relevant packet within configured limits.
- AC2: Oversized context is reduced to references and a structured summary with an observable truncation reason.

# AC Traceability
- request-AC2 -> This backlog slice. Proof: AC1: Planner, executor, reviewer, and recovery prompts receive only their role-relevant packet within configured limits.
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
- Summary: Build bounded role-specific context packets
- Keywords: scaffolded-backlog, build bounded role-specific context packets, implementation-ready
- Use when: Implementing the scaffolded slice for Build bounded role-specific context packets.
- Skip when: The change belongs to another backlog slice.

# Priority
- Priority: High
- Rationale: Set by scaffold input or defaulted for grooming.

# Tasks
- `task_004_deliver_cost_of_pass_control_plane_and_benchmark_harness`

# Notes
- Task `task_004_deliver_cost_of_pass_control_plane_and_benchmark_harness` was finished via `logics-manager flow finish task` on 2026-07-28.
