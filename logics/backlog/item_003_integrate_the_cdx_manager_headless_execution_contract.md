## item_003_integrate_the_cdx_manager_headless_execution_contract - Integrate the cdx-manager headless execution contract
> From version: 1.0.0
> Schema version: 1.0
> Status: In progress
> Understanding: 90%
> Confidence: 85%
> Progress: 40%
> Complexity: Medium
> Theme: Runtime integration
> Reminder: Update status/understanding/confidence/progress and linked request/task references when you edit this doc.

# Problem
- Orchestrato needs provider-neutral, observable agent execution without taking ownership of accounts or provider-specific launch flags.

# Scope
- In:
  - Typed adapters for cdx select, run, run-status, run-report, and cancellation or timeout handling available in the installed contract.
  - Prompt-file handoffs, structured result validation, run correlation, usage capture, and artifact references.
  - Session selection by provider and minimum reasoning effort.
- Out:
  - Direct Codex or Claude SDK integration, authentication storage, or quota scraping.

# Acceptance criteria
- AC1: All cdx invocations use JSON mode and validate their schema before changing orchestration state.
- AC2: Provider output is referenced through cdx artifacts and never mixed into Orchestrato protocol output.
- AC3: Timeout, malformed JSON, provider failure, and unavailable-session paths produce typed failures.

# AC Traceability
- request-AC3 -> This backlog slice. Proof: AC1: All cdx invocations use JSON mode and validate their schema before changing orchestration state.
- request-AC7 -> This backlog slice. Proof: AC2: Provider output is referenced through cdx artifacts and never mixed into Orchestrato protocol output.
- request-AC9 -> This backlog slice. Proof: AC3: Timeout, malformed JSON, provider failure, and unavailable-session paths produce typed failures.
- request-AC4 -> This backlog slice. Evidence needed: Planning work can create or consume a bounded Logics request, backlog, task, and context pack before implementation begins.
- request-AC5 -> This backlog slice. Evidence needed: The supervisor enforces a finite plan-execute-verify-review-recover state machine with retry budgets and explicit stop conditions.
- request-AC6 -> This backlog slice. Evidence needed: Mutating or externally visible actions require policy-defined approval, and only one agent may write to a worktree at a time.
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
- Summary: Integrate the cdx-manager headless execution contract
- Keywords: scaffolded-backlog, integrate the cdx-manager headless execution contract, implementation-ready
- Use when: Implementing the scaffolded slice for Integrate the cdx-manager headless execution contract.
- Skip when: The change belongs to another backlog slice.

# Priority
- Priority: High
- Rationale: Set by scaffold input or defaulted for grooming.

# Tasks
- `task_001_orchestrate_delivery_of_the_orchestrato_mvp`
