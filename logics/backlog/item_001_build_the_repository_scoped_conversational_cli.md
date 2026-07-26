## item_001_build_the_repository_scoped_conversational_cli - Build the repository-scoped conversational CLI
> From version: 1.0.0
> Schema version: 1.0
> Status: Ready
> Understanding: 90%
> Confidence: 85%
> Progress: 0%
> Complexity: Medium
> Theme: Operator experience
> Reminder: Update status/understanding/confidence/progress and linked request/task references when you edit this doc.

# Problem
- The operator needs one low-friction surface for objectives, progress, approvals, status, and resume.

# Scope
- In:
  - A Python CLI with one-shot and interactive conversation modes.
  - Repository discovery, conversation identifiers, slash commands, concise live progress, and final summaries.
  - Commands for status, plan, run, approve, reject, resume, and inspect.
- Out:
  - A full-screen TUI, browser application, remote server, or multi-user authentication.

# Acceptance criteria
- AC1: The CLI accepts an objective in one-shot and interactive modes.
- AC2: The CLI renders stable states and approval prompts without exposing raw provider streams.
- AC3: A previous conversation can be selected and resumed.

# AC Traceability
- request-AC1 -> This backlog slice. Proof: AC1: The CLI accepts an objective in one-shot and interactive modes.
- request-AC8 -> This backlog slice. Proof: AC2: The CLI renders stable states and approval prompts without exposing raw provider streams.
- request-AC3 -> This backlog slice. Evidence needed: Orchestrato invokes cdx-manager through its JSON CLI contract and records cdx run identifiers, reports, usage, errors, and artifacts without parsing interactive terminal output.
- request-AC4 -> This backlog slice. Evidence needed: Planning work can create or consume a bounded Logics request, backlog, task, and context pack before implementation begins.
- request-AC5 -> This backlog slice. Evidence needed: The supervisor enforces a finite plan-execute-verify-review-recover state machine with retry budgets and explicit stop conditions.
- request-AC6 -> This backlog slice. Evidence needed: Mutating or externally visible actions require policy-defined approval, and only one agent may write to a worktree at a time.
- request-AC7 -> This backlog slice. Evidence needed: A failed execution can produce a bounded diagnostic handoff for a recovery role and, when recovered, resume from the failed step without replaying completed work.
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
- Summary: Build the repository-scoped conversational CLI
- Keywords: scaffolded-backlog, build the repository-scoped conversational cli, implementation-ready
- Use when: Implementing the scaffolded slice for Build the repository-scoped conversational CLI.
- Skip when: The change belongs to another backlog slice.

# Priority
- Priority: High
- Rationale: Set by scaffold input or defaulted for grooming.

# Tasks
- `task_001_orchestrate_delivery_of_the_orchestrato_mvp`
