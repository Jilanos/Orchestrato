## item_006_add_local_persistence_observability_and_contract_tests - Add local persistence, observability, and contract tests
> From version: 1.0.0
> Schema version: 1.0
> Status: In progress
> Understanding: 90%
> Confidence: 85%
> Progress: 50%
> Complexity: Medium
> Theme: Reliability
> Reminder: Update status/understanding/confidence/progress and linked request/task references when you edit this doc.

# Problem
- The orchestration engine needs durable evidence and deterministic tests before live multi-agent use is trustworthy.

# Scope
- In:
  - SQLite event storage for conversations, decisions, steps, approvals, external run references, and usage metadata.
  - Structured logs with secret redaction and inspect/export commands.
  - Fake executable fixtures for cdx-manager and Logics Manager contracts.
  - State transition, routing, timeout, resume, approval, and fallback tests.
- Out:
  - Cloud telemetry, hosted dashboards, billing, or provider credential storage.

# Acceptance criteria
- AC1: A process restart can reconstruct the latest valid conversation state from local events.
- AC2: Logs and exports do not persist prompt secrets or provider credentials by default.
- AC3: The default test suite is deterministic, offline, and covers success plus critical failure paths.

# AC Traceability
- request-AC8 -> This backlog slice. Proof: AC1: A process restart can reconstruct the latest valid conversation state from local events.
- request-AC10 -> This backlog slice. Proof: AC2: Logs and exports do not persist prompt secrets or provider credentials by default.
- request-AC3 -> This backlog slice. Evidence needed: Orchestrato invokes cdx-manager through its JSON CLI contract and records cdx run identifiers, reports, usage, errors, and artifacts without parsing interactive terminal output.
- request-AC4 -> This backlog slice. Evidence needed: Planning work can create or consume a bounded Logics request, backlog, task, and context pack before implementation begins.
- request-AC5 -> This backlog slice. Evidence needed: The supervisor enforces a finite plan-execute-verify-review-recover state machine with retry budgets and explicit stop conditions.
- request-AC6 -> This backlog slice. Evidence needed: Mutating or externally visible actions require policy-defined approval, and only one agent may write to a worktree at a time.
- request-AC7 -> This backlog slice. Evidence needed: A failed execution can produce a bounded diagnostic handoff for a recovery role and, when recovered, resume from the failed step without replaying completed work.
- request-AC9 -> This backlog slice. Evidence needed: Provider or model unavailability produces an explainable fallback decision or a clean blocked state instead of silent model substitution.

# Decision framing
- Product framing: Not needed
- Architecture framing: Not needed

# Links
- Product brief(s): `prod_001_orchestrato_mvp_product_brief`
- Architecture decision(s): (none yet)
- Request: `req_000_deliver_the_orchestrato_conversational_orchestration_mvp`
- Primary task(s): `task_001_orchestrate_delivery_of_the_orchestrato_mvp`

# AI Context
- Summary: Add local persistence, observability, and contract tests
- Keywords: scaffolded-backlog, add local persistence, observability, and contract tests, implementation-ready
- Use when: Implementing the scaffolded slice for Add local persistence, observability, and contract tests.
- Skip when: The change belongs to another backlog slice.

# Priority
- Priority: Medium
- Rationale: Set by scaffold input or defaulted for grooming.

# Tasks
- `task_001_orchestrate_delivery_of_the_orchestrato_mvp`
