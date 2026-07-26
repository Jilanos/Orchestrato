## item_002_define_agent_profiles_and_deterministic_routing_policy - Define agent profiles and deterministic routing policy
> From version: 1.0.0
> Schema version: 1.0
> Status: In progress
> Understanding: 90%
> Confidence: 85%
> Progress: 50%
> Complexity: High
> Theme: Routing policy
> Reminder: Update status/understanding/confidence/progress and linked request/task references when you edit this doc.

# Problem
- Agent names, provider models, effort, permissions, and fallbacks need one auditable policy rather than prompt-only conventions.

# Scope
- In:
  - Declarative role profiles for planner, executor, specialist developer, recovery, reviewer, and routine operations.
  - Intent, risk, effort, permission, fallback, and availability rules.
  - Medium effort by default, low for routine bounded operations, and high only for recovery or explicitly complex work.
  - Explainable routing decisions and clean blocked outcomes.
- Out:
  - Machine-learned routing, provider benchmarking, or automatic policy optimization.

# Acceptance criteria
- AC1: The same normalized task and runtime snapshot produce the same route.
- AC2: Every route records its matched rule, selected role, effort, permission, and fallback candidates.
- AC3: Unknown roles, unavailable candidates, and unsafe permission escalation fail closed with actionable diagnostics.

# AC Traceability
- request-AC2 -> This backlog slice. Proof: AC1: The same normalized task and runtime snapshot produce the same route.
- request-AC6 -> This backlog slice. Proof: AC2: Every route records its matched rule, selected role, effort, permission, and fallback candidates.
- request-AC9 -> This backlog slice. Proof: AC3: Unknown roles, unavailable candidates, and unsafe permission escalation fail closed with actionable diagnostics.
- request-AC4 -> This backlog slice. Evidence needed: Planning work can create or consume a bounded Logics request, backlog, task, and context pack before implementation begins.
- request-AC5 -> This backlog slice. Evidence needed: The supervisor enforces a finite plan-execute-verify-review-recover state machine with retry budgets and explicit stop conditions.
- request-AC7 -> This backlog slice. Evidence needed: A failed execution can produce a bounded diagnostic handoff for a recovery role and, when recovered, resume from the failed step without replaying completed work.
- request-AC8 -> This backlog slice. Evidence needed: Run events, routing decisions, approvals, Logics references, and cost or usage metadata are persisted locally and can be inspected after restart.
- request-AC10 -> This backlog slice. Evidence needed: Automated tests exercise orchestration behavior with fake cdx-manager and Logics Manager subprocesses; no live provider account is required for the default test suite.

# Decision framing
- Product framing: Not needed
- Architecture framing: Not needed

# Links
- Product brief(s): `prod_001_orchestrato_mvp_product_brief`
- Architecture decision(s): (none yet)
- Request: `req_000_deliver_the_orchestrato_conversational_orchestration_mvp`
- Primary task(s): `task_001_orchestrate_delivery_of_the_orchestrato_mvp`

# AI Context
- Summary: Define agent profiles and deterministic routing policy
- Keywords: scaffolded-backlog, define agent profiles and deterministic routing policy, implementation-ready
- Use when: Implementing the scaffolded slice for Define agent profiles and deterministic routing policy.
- Skip when: The change belongs to another backlog slice.

# Priority
- Priority: High
- Rationale: Set by scaffold input or defaulted for grooming.

# Tasks
- `task_001_orchestrate_delivery_of_the_orchestrato_mvp`
