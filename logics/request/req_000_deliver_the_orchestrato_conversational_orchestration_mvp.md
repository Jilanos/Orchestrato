## req_000_deliver_the_orchestrato_conversational_orchestration_mvp - Deliver the Orchestrato conversational orchestration MVP
> From version: 1.0.0
> Schema version: 1.0
> Status: Draft
> Understanding: 90%
> Confidence: 85%
> Complexity: High
> Theme: Agent orchestration
> Reminder: Update status/understanding/confidence and linked backlog/task references when you edit this doc.

# Needs
- Provide one conversational CLI where an operator can describe development work in natural language.
- Route planning, implementation, recovery, review, and routine repository operations to role-specific agents.
- Use cdx-manager for provider sessions, capacity-aware selection, model choice, permissions, reasoning effort, and run reports.
- Use Logics Manager for durable project intent, bounded context, implementation tasks, and workflow validation.
- Keep every routing decision, handoff, approval, and run outcome inspectable and resumable.

# Context
- cdx-manager already exposes JSON-first select, run, runs, run-status, and run-report commands for Codex and Claude providers.
- Logics Manager already exposes request-chain scaffolding, lifecycle transitions, context packs, status, lint, audit, and a local viewer.
- The MVP should integrate these CLIs through stable subprocess boundaries instead of importing their internal Python modules.
- Terra, Luna, Sol, Sonnet, Fable, and Opus are configurable orchestration roles or candidates, not hard-coded runtime assumptions.
- The initial operator surface is a local CLI with a compact live status view; a full TUI or web interface is deferred.

# Acceptance criteria
- AC1: An operator can start a repository-scoped conversation, submit a development objective, and receive concise progress and a final outcome.
- AC2: A declarative policy maps task intent and risk to an agent role, provider, model candidate, reasoning effort, and permission level, with medium effort as the default.
- AC3: Orchestrato invokes cdx-manager through its JSON CLI contract and records cdx run identifiers, reports, usage, errors, and artifacts without parsing interactive terminal output.
- AC4: Planning work can create or consume a bounded Logics request, backlog, task, and context pack before implementation begins.
- AC5: The supervisor enforces a finite plan-execute-verify-review-recover state machine with retry budgets and explicit stop conditions.
- AC6: Mutating or externally visible actions require policy-defined approval, and only one agent may write to a worktree at a time.
- AC7: A failed execution can produce a bounded diagnostic handoff for a recovery role and, when recovered, resume from the failed step without replaying completed work.
- AC8: Run events, routing decisions, approvals, Logics references, and cost or usage metadata are persisted locally and can be inspected after restart.
- AC9: Provider or model unavailability produces an explainable fallback decision or a clean blocked state instead of silent model substitution.
- AC10: Automated tests exercise orchestration behavior with fake cdx-manager and Logics Manager subprocesses; no live provider account is required for the default test suite.

# Definition of Ready (DoR)
- [x] Problem statement is explicit and user impact is clear.
- [x] Scope boundaries (in/out) are explicit.
- [x] Acceptance criteria are testable.
- [x] Dependencies and known risks are listed.

# Companion docs
- Product brief(s): `prod_001_orchestrato_mvp_product_brief`
- Architecture decision(s): `adr_001_keep_orchestrato_behind_cli_contracts`, `adr_002_use_a_persisted_finite_orchestration_state_machine`

# References
- README.md
- docs/product.md
- docs/architecture.md
- Sibling repository: cdx-manager headless automation product contract.
- Sibling repository: cdx-manager provider-native headless run boundary.

# AI Context
- Summary: Deliver the Orchestrato conversational orchestration MVP
- Keywords: request-chain-scaffold, deliver the orchestrato conversational orchestration mvp, development-ready
- Use when: You need to implement or review the scaffolded workflow for Deliver the Orchestrato conversational orchestration MVP.
- Skip when: The change is unrelated to this scaffolded request chain.

# Backlog
- `item_001_build_the_repository_scoped_conversational_cli`
- `item_002_define_agent_profiles_and_deterministic_routing_policy`
- `item_003_integrate_the_cdx_manager_headless_execution_contract`
- `item_004_integrate_logics_planning_and_bounded_handoffs`
- `item_005_implement_finite_supervision_review_and_recovery`
- `item_006_add_local_persistence_observability_and_contract_tests`
