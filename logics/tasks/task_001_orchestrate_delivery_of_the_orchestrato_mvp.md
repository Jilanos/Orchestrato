## task_001_orchestrate_delivery_of_the_orchestrato_mvp - Orchestrate delivery of the Orchestrato MVP
> From version: 1.0.0
> Schema version: 1.0
> Status: In progress
> Understanding: 90%
> Confidence: 85%
> Progress: 25%
> Complexity: Medium
> Theme: Implementation delivery
> Reminder: Update status/understanding/confidence/progress and linked request/backlog references when you edit this doc.
> Owner: codex

# Context
- Orchestrate the scaffolded request chain and keep sibling implementation slices linked.

# Plan
- [ ] 1. Confirm the product and architecture decisions before implementation.
- [ ] 2. Deliver the CLI and persisted domain model as the first vertical foundation.
- [ ] 3. Implement deterministic role routing and policy validation.
- [ ] 4. Integrate cdx-manager through fake contract tests before using live sessions.
- [ ] 5. Integrate Logics planning and bounded context handoffs.
- [ ] 6. Implement supervision, review, recovery, approvals, and writer locking.
- [ ] 7. Run contract, state-machine, lint, audit, and end-to-end fake-runtime validation.
- [ ] 8. Record validation evidence and close the linked workflow only after every acceptance criterion is traced.
- [ ] ADR 009 checkpoint: update affected Logics docs during each meaningful wave and leave the repo commit-ready.
- [ ] Keep commit creation under operator control; do not force one commit per micro-step.
- [ ] GATE: do not close until lint, audit, and scaffold validation pass.

# Backlog
- `item_001_build_the_repository_scoped_conversational_cli`
- `item_002_define_agent_profiles_and_deterministic_routing_policy`
- `item_003_integrate_the_cdx_manager_headless_execution_contract`
- `item_004_integrate_logics_planning_and_bounded_handoffs`
- `item_005_implement_finite_supervision_review_and_recovery`
- `item_006_add_local_persistence_observability_and_contract_tests`

# Definition of Done (DoD)
- [ ] The CLI supports one-shot, interactive, inspect, approval, and resume flows.
- [ ] Routing, cdx, and Logics adapters satisfy their linked backlog acceptance criteria.
- [ ] The finite supervisor enforces approvals, budgets, independent review, recovery, and one writer per worktree.
- [ ] SQLite persistence reconstructs state after interruption.
- [ ] The context-pack handoff is available for every implementation slice.
- [ ] Offline contract, transition, resume, failure, lint, and audit validation passes.
- [ ] Meaningful waves followed ADR 009: affected docs updated and the repo left commit-ready without automatic commits.

# AC Traceability
- request-AC1 -> This task via `item_001_build_the_repository_scoped_conversational_cli`. Evidence needed: CLI acceptance and resume tests.
- request-AC2 -> This task via `item_002_define_agent_profiles_and_deterministic_routing_policy`. Evidence needed: deterministic routing fixtures.
- request-AC3 -> This task via `item_003_integrate_the_cdx_manager_headless_execution_contract`. Evidence needed: fake cdx contract tests.
- request-AC4 -> This task via `item_004_integrate_logics_planning_and_bounded_handoffs`. Evidence needed: fake Logics lifecycle and context-pack tests.
- request-AC5 -> This task via `item_005_implement_finite_supervision_review_and_recovery`. Evidence needed: transition and budget tests.
- request-AC6 -> This task via `item_002_define_agent_profiles_and_deterministic_routing_policy` and `item_005_implement_finite_supervision_review_and_recovery`. Evidence needed: approval and writer-lock tests.
- request-AC7 -> This task via `item_003_integrate_the_cdx_manager_headless_execution_contract`, `item_004_integrate_logics_planning_and_bounded_handoffs`, and `item_005_implement_finite_supervision_review_and_recovery`. Evidence needed: failed-step recovery test.
- request-AC8 -> This task via `item_001_build_the_repository_scoped_conversational_cli` and `item_006_add_local_persistence_observability_and_contract_tests`. Evidence needed: restart and inspect tests.
- request-AC9 -> This task via `item_002_define_agent_profiles_and_deterministic_routing_policy` and `item_003_integrate_the_cdx_manager_headless_execution_contract`. Evidence needed: unavailable-provider fallback tests.
- request-AC10 -> This task via `item_006_add_local_persistence_observability_and_contract_tests`. Evidence needed: offline end-to-end suite.

# Validation
- Run the project unit and contract test suites.
- Run the offline fake-runtime end-to-end scenario.
- Run `logics-manager flow validate` for the active request chain.
- Run `logics-manager lint --require-status`.
- Run `logics-manager audit --group-by-doc`.
- Wave 1: 12 offline tests passed; CLI help, route, cdx fake contract, state persistence, and Logics adapter smoke checks passed.

# Report
- Not started. Record implementation waves and final evidence here.
- Wave 1 delivered the dependency-light CLI, deterministic role routing, SQLite event store, cdx/Logics JSON adapters, and offline tests. Live cdx execution remains the next validation wave.

# AI Context
- Summary: Orchestrate delivery of the Orchestrato MVP
- Keywords: scaffolded-task, request-chain-scaffold, orchestration
- Use when: Coordinating implementation of a scaffolded request chain.
- Skip when: Working on one isolated sibling slice.

# Links
- Request: `req_000_deliver_the_orchestrato_conversational_orchestration_mvp`
- Product brief(s): `prod_001_orchestrato_mvp_product_brief`
- Architecture decision(s): `adr_001_keep_orchestrato_behind_cli_contracts`, `adr_002_use_a_persisted_finite_orchestration_state_machine`
