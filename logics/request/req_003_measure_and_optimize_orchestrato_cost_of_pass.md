## req_003_measure_and_optimize_orchestrato_cost_of_pass - Measure and optimize Orchestrato cost of pass
> From version: 1.0.0
> Schema version: 1.0
> Status: Done
> Understanding: 90%
> Confidence: 85%
> Complexity: High
> Theme: Token-efficient orchestration
> Reminder: Update status/understanding/confidence and linked backlog/task references when you edit this doc.

# Needs
- Measure the token, latency, and quality cost of each orchestration route.
- Select the least expensive route that still passes task-specific acceptance checks.
- Keep agent handoffs sufficient for execution without replaying whole transcripts.

# Context
- The 2026-07-27 exploratory benchmark found direct Terra lower-token than fixed multi-agent chains on a bounded coding task.
- Total tokens include cached input and must not be treated as a direct billing value.
- Live provider runs are opt-in; deterministic tests must not require provider accounts.

# Acceptance criteria
- AC1: Orchestrato persists normalized per-run usage including new input, cached input, cache writes when available, output, reasoning, duration, route, retries, and validation outcome.
- AC2: Orchestrato builds role-specific bounded handoff packets from explicit task references and configurable limits, without injecting full workflow or transcript history by default.
- AC3: Policy can select direct execution by default and escalate planning, review, or recovery only from explicit risk, validation, or failure evidence.
- AC4: A reproducible benchmark harness compares direct minimal-context, direct expanded-context, adaptive orchestration, and fixed plan-implement-review routes without running providers by default.
- AC5: Benchmark reports compute pass rate, cost-of-pass, total/new/cached/output tokens, latency, retries, and human-rework fields, and preserve raw run references.
- AC6: Contract and analysis tests cover usage normalization, context budgets, escalation gates, aggregation, and no-live-run defaults.

# Definition of Ready (DoR)
- [x] Problem statement is explicit and user impact is clear.
- [x] Scope boundaries (in/out) are explicit.
- [x] Acceptance criteria are testable.
- [x] Dependencies and known risks are listed.

# Companion docs
- Product brief(s): `prod_003_cost_of_pass_control_plane`
- Architecture decision(s): (none yet)

# References
- docs/agent-orchestration-benchmark-2026-07-27.md
- docs/architecture.md
- /home/paul/dev/WORK/orchestrato-cost-of-pass

# AI Context
- Summary: Measure and optimize Orchestrato cost of pass
- Keywords: request-chain-scaffold, measure and optimize orchestrato cost of pass, development-ready
- Use when: You need to implement or review the scaffolded workflow for Measure and optimize Orchestrato cost of pass.
- Skip when: The change is unrelated to this scaffolded request chain.

# Backlog
- `item_010_persist_normalized_cost_of_pass_run_evidence`
- `item_011_build_bounded_role_specific_context_packets`
- `item_012_add_adaptive_route_and_escalation_gates`
- `item_013_create_reproducible_route_comparison_harness`
- `item_014_aggregate_cost_of_pass_comparison_reports`
- `item_015_test_cost_aware_orchestration_contracts`
