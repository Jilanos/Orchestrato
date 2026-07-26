## prod_001_orchestrato_mvp_product_brief - Orchestrato MVP product brief
> Date: 2026-07-26
> Status: Settled
> Related request: `req_000_deliver_the_orchestrato_conversational_orchestration_mvp`
> Related backlog: `item_001_build_the_repository_scoped_conversational_cli`
> Related task: `task_001_orchestrate_delivery_of_the_orchestrato_mvp`
> Related architecture: (none yet)
> Reminder: Update status, linked refs, scope, decisions, success signals, and open questions when you edit this doc.

# Overview
A local, inspectable conversational supervisor that coordinates specialized coding agents through cdx-manager and durable delivery workflows through Logics Manager.

```mermaid
%% logics-kind: product
%% logics-signature: product|orchestrato-mvp-product-brief|pending
flowchart LR
    Operator[Operator objective] --> Route[Explainable role route]
    Route --> Execute[Bounded agent execution]
    Execute --> Evidence[Verification and review]
    Evidence --> Outcome[Durable outcome]
```

# Product problem
- A developer can already ask one capable agent to plan and edit a repository, but must manually decide when to change model, provider, effort, or reviewer.
- Multi-agent handoffs usually lose intent, duplicate repository context, and hide why a particular agent was selected.
- Long-running development needs durable task state, explicit approvals, bounded retries, and evidence that survives a terminal session.

# Primary user
- A local software operator who owns the repository and wants one conversational control surface.
- The operator remains accountable for high-impact actions while delegating planning, implementation, verification, review, and recovery.

# Goals
- Make multi-agent development feel like one continuous Codex-style conversation.
- Select agent capability and reasoning effort according to task value, risk, and runtime availability.
- Turn plans into durable Logics work before code execution when the task requires product or architecture shaping.
- Preserve enough state and evidence to resume, audit, and improve orchestration decisions.
- Deliver a useful local CLI before investing in a richer interface or remote daemon.

# MVP experience
1. The operator starts Orchestrato in a project directory and describes an objective.
2. Orchestrato classifies the work, shows the proposed route and any required approval, then selects or creates the relevant Logics work.
3. A role-specific agent receives a bounded handoff and runs through cdx-manager.
4. Orchestrato verifies the result, requests an independent review when policy requires it, and invokes recovery only for classified failures.
5. The operator receives one concise outcome with changed files, validation, remaining risks, run references, and the next Logics action.

# Role model
- Planner (Terra by default): shapes product, architecture, request chains, and implementation plans.
- Executor (Luna by default): performs general repository-aware implementation.
- Specialist developer (for example Sonnet): handles configured pure-development workloads where its capability or economics are preferred.
- Recovery (Sol by default): diagnoses repeated or complex failures from a bounded evidence packet.
- Reviewer or auditor (for example Fable or Opus): independently reviews code, architecture, security, or release readiness.
- Operations: handles bounded mechanical work such as repository synchronization with low reasoning effort and the applicable approval.

Role labels are stable product concepts. Provider and model identifiers are configuration values validated at runtime.

# Non-goals
- Reimplement provider authentication, quota handling, or native agent launch commands.
- Reimplement Logics document parsing, lifecycle transitions, validation, or the browser viewer.
- Run several write-capable agents concurrently in the same worktree.
- Provide unattended deployment, arbitrary destructive actions, or unrestricted long-running autonomy in the MVP.
- Guarantee a specific commercial model name remains available.

# Scope and guardrails
- In: local CLI, role and routing policy, cdx adapter, Logics adapter, finite supervisor, local persistence, approvals, review, recovery, and fake-runtime tests.
- Out: full-screen UI, hosted service, distributed workers, autonomous deployment, credential storage, and parallel writes to one worktree.
- Read-only inspection can run without approval.
- Repository mutations follow the configured project policy.
- Network publication, deployment, destructive operations, and permission escalation require explicit approval by default.

# Key product decisions
- Default reasoning effort is medium. Low is reserved for bounded routine work; high is an explicit escalation for difficult planning, recovery, or audit.
- Routing is deterministic and explainable for known task classes. A planner may resolve ambiguity, but does not sit on every trivial path.
- Orchestrato owns orchestration state and policy, cdx-manager owns provider execution, and Logics Manager owns delivery workflow state.
- Agent aliases are decoupled from commercial model names so the policy survives provider changes.
- Only one agent may write to a worktree at a time. Later parallelism uses isolated worktrees and an explicit merge step.
- An independent reviewer must not silently become the original implementation agent when policy requires separation.

# Success signals
- A new operator can complete one plan-implement-review loop from a single CLI session.
- Every external run and routing decision is inspectable after process restart.
- The default test suite exercises success and critical failure paths without live provider credentials.
- Routine tasks avoid high reasoning effort unless policy or operator intent requires it.
- Failed runs stop within configured budgets and leave an actionable blocked state.
- Logics lint and audit pass before workflow closeout.

# Open questions
- Which task signals should prefer the Codex executor over the Claude specialist after both are available?
- Which mutations can be pre-approved per repository without weakening operator control?
- What usage and latency thresholds should trigger a fallback versus a blocked state?
- How much transcript context is useful before summaries and Logics context packs should replace raw history?

# Architecture
- `adr_001_keep_orchestrato_behind_cli_contracts`
- `adr_002_use_a_persisted_finite_orchestration_state_machine`

# Delivery slices
- `item_001_build_the_repository_scoped_conversational_cli`
- `item_002_define_agent_profiles_and_deterministic_routing_policy`
- `item_003_integrate_the_cdx_manager_headless_execution_contract`
- `item_004_integrate_logics_planning_and_bounded_handoffs`
- `item_005_implement_finite_supervision_review_and_recovery`
- `item_006_add_local_persistence_observability_and_contract_tests`

# References
- Product back-reference: `item_001_build_the_repository_scoped_conversational_cli`
- Task back-reference: `task_001_orchestrate_delivery_of_the_orchestrato_mvp`
- Detailed product document: `docs/product.md`
- Product roadmap: `road_001_orchestrato_product_roadmap`
