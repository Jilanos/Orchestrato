## item_004_integrate_logics_planning_and_bounded_handoffs - Integrate Logics planning and bounded handoffs
> From version: 1.0.0
> Schema version: 1.0
> Status: In progress
> Understanding: 90%
> Confidence: 85%
> Progress: 50%
> Complexity: High
> Theme: Workflow integration
> Reminder: Update status/understanding/confidence/progress and linked request/task references when you edit this doc.

# Problem
- Plans and task boundaries must survive agent changes and process restarts instead of existing only in conversation transcripts.

# Scope
- In:
  - Typed adapters for Logics status, health, flow lifecycle, sync context-pack, lint, and audit commands.
  - A planning gate that can reuse existing work or create a request chain before implementation.
  - Bounded handoff packets containing objective, active Logics refs, acceptance criteria, relevant diffs, and prior run evidence.
- Out:
  - Manual parsing or mutation of Logics indicators, lineage links, Mermaid signatures, or status fields.
  - A replacement Logics viewer.

# Acceptance criteria
- AC1: Planning produces or selects explicit Logics references before an implementation run starts.
- AC2: Agent prompts receive context packs within configurable size limits.
- AC3: Lint and audit failures block closeout and remain visible to the operator.

# AC Traceability
- request-AC4 -> This backlog slice. Proof: AC1: Planning produces or selects explicit Logics references before an implementation run starts.
- request-AC7 -> This backlog slice. Proof: AC2: Agent prompts receive context packs within configurable size limits.
- request-AC3 -> This backlog slice. Evidence needed: Orchestrato invokes cdx-manager through its JSON CLI contract and records cdx run identifiers, reports, usage, errors, and artifacts without parsing interactive terminal output.
- request-AC5 -> This backlog slice. Evidence needed: The supervisor enforces a finite plan-execute-verify-review-recover state machine with retry budgets and explicit stop conditions.
- request-AC6 -> This backlog slice. Evidence needed: Mutating or externally visible actions require policy-defined approval, and only one agent may write to a worktree at a time.
- request-AC8 -> This backlog slice. Evidence needed: Run events, routing decisions, approvals, Logics references, and cost or usage metadata are persisted locally and can be inspected after restart.
- request-AC9 -> This backlog slice. Evidence needed: Provider or model unavailability produces an explainable fallback decision or a clean blocked state instead of silent model substitution.
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
- Summary: Integrate Logics planning and bounded handoffs
- Keywords: scaffolded-backlog, integrate logics planning and bounded handoffs, implementation-ready
- Use when: Implementing the scaffolded slice for Integrate Logics planning and bounded handoffs.
- Skip when: The change belongs to another backlog slice.

# Priority
- Priority: High
- Rationale: Set by scaffold input or defaulted for grooming.

# Tasks
- `task_001_orchestrate_delivery_of_the_orchestrato_mvp`
