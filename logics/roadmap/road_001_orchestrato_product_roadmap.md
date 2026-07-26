## road_001_orchestrato_product_roadmap - Orchestrato product roadmap
> Date: 2026-07-26
> Status: Proposed
> Related product: `prod_001_orchestrato_mvp_product_brief`
> Related request: `req_000_deliver_the_orchestrato_conversational_orchestration_mvp`
> Reminder: Update status, milestone scope, linked refs, risks, and success signals when you edit this doc.

# Summary
Deliver Orchestrato as a sequence of independently useful control-plane increments. Reliability, evidence, and bounded autonomy precede parallelism or richer presentation.

# Milestones
## 0.1 - Inspectable conversational CLI and fake-runtime vertical slice
- Goal: Prove the complete orchestration loop without live provider credentials.
- Scope: `item_001_build_the_repository_scoped_conversational_cli`, `item_002_define_agent_profiles_and_deterministic_routing_policy`, and the persistence foundation from `item_006_add_local_persistence_observability_and_contract_tests`.
- Exit signal: One offline objective moves through intake, route, approval, fake execution, verification, review, persistence, restart, and completion with inspectable evidence.

## 0.2 - Live cdx and Logics integration with review and recovery
- Goal: Complete a real repository change through the supported cdx and Logics CLI contracts.
- Scope: `item_003_integrate_the_cdx_manager_headless_execution_contract`, `item_004_integrate_logics_planning_and_bounded_handoffs`, and `item_005_implement_finite_supervision_review_and_recovery`.
- Exit signal: A live plan-implement-verify-review flow records cdx runs, Logics refs, usage, approvals, validation, and a bounded recovery scenario.

## 0.3 - Parallel worktrees, richer TUI, and policy tuning
- Goal: Improve throughput and operator ergonomics without weakening isolation.
- Scope: Git worktree leasing, explicit integration reviews, a Textual interface over the same application service, and policy outcome metrics.
- Exit signal: Independent tasks can run concurrently in isolated worktrees and integrate through a reviewed, resumable workflow.

## 1.0 - Guarded long-running autonomous delivery
- Goal: Accept a broad development objective and advance it over multiple bounded work sessions.
- Scope: Durable scheduling, budget windows, release evidence, pause and resume, operator notification, and explicit publication gates.
- Exit signal: A multi-task objective can survive interruption, capacity changes, failed runs, and review findings while never bypassing approval or release policy.

# Sequencing
- Deliver milestones in ascending version order unless dependencies force a documented exception.
- Keep each increment independently reviewable and linked to concrete workflow docs.
- Do not begin parallel write execution until single-writer crash recovery is proven.
- Do not begin unattended release work until release evidence and approval contracts are validated.

# Risks
- Prompt-driven behavior can bypass architecture unless state transitions and policies remain code-owned.
- Provider names, model availability, and pricing can change; roles must remain configurable.
- Concurrent repository writes can corrupt work or invalidate review evidence without worktree isolation.
- Transcript growth can erase efficiency gains unless context packs and summaries stay bounded.
- Long-running autonomy can amplify a wrong objective unless budgets and approval scopes expire.
- Version labels are planning targets, not release promises.

# References
- Product brief(s): `prod_001_orchestrato_mvp_product_brief`
- Request(s): `req_000_deliver_the_orchestrato_conversational_orchestration_mvp`
- Backlog item(s): `item_001_build_the_repository_scoped_conversational_cli`, `item_002_define_agent_profiles_and_deterministic_routing_policy`, `item_003_integrate_the_cdx_manager_headless_execution_contract`, `item_004_integrate_logics_planning_and_bounded_handoffs`, `item_005_implement_finite_supervision_review_and_recovery`, `item_006_add_local_persistence_observability_and_contract_tests`
- Task(s): `task_001_orchestrate_delivery_of_the_orchestrato_mvp`

# AI Context
- Summary: Sequence Orchestrato from an offline vertical slice to guarded long-running delivery.
- Keywords: roadmap, orchestration, fake-runtime, live-integration, worktrees, autonomy
- Use when: Planning scope, dependencies, or release boundaries across Orchestrato versions.
- Skip when: You need execution details for a single backlog item or task.
