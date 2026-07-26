# Orchestrato Product Definition

> Status: Proposed
> Updated: 2026-07-26

## Vision

Orchestrato should feel like talking to one strong coding partner while behaving like a well-run specialist team underneath. The operator describes outcomes in natural language; the system chooses an appropriate planning, implementation, recovery, or review role, keeps the project workflow current, and explains every consequential decision.

The product is local-first. It builds on existing authenticated CLI tools instead of becoming another provider gateway.

## User problem

A developer coordinating multiple agents currently has to:

- repeat repository and product context across sessions;
- choose provider, account, model, reasoning effort, and permissions manually;
- decide when planning is sufficient to begin implementation;
- detect stalled runs and construct recovery prompts;
- find an independent reviewer and translate findings back into tasks;
- remember which actions were approved and which work remains;
- infer cost and progress from several unrelated transcripts.

This overhead grows faster than the number of agents. More capable models do not solve the control problem by themselves.

## Product promise

From one project-scoped conversation, the operator can:

1. describe an objective;
2. inspect or adjust the proposed plan and agent route;
3. approve only the side effects that need approval;
4. observe concise progress while specialized agents work;
5. receive a verified, reviewed outcome with durable project state;
6. resume later without reconstructing the whole conversation.

## Product principles

### Explainable before clever

Known task classes use deterministic policy. An agent can help classify ambiguous work, but model judgment does not replace explicit permission, effort, fallback, or stop rules.

### Roles outlive models

Terra, Luna, Sol, specialist developer, reviewer, and operations are product roles. Their provider and model candidates live in configuration because commercial model names and availability change.

### Durable intent over transcript memory

Product decisions, architecture, acceptance criteria, and tasks belong in Logics. Orchestrato conversation history links to that corpus and does not become a second backlog.

### Evidence over confidence language

Completion requires command results, tests, review findings, changed-file evidence, and Logics validation. Agent confidence is useful metadata, not proof.

### Finite autonomy

Every objective has budgets, approval boundaries, and terminal states. A blocked result with a clear diagnosis is preferable to an expensive loop.

## Roles

| Role | Default purpose | Typical effort | Independence rule |
| --- | --- | --- | --- |
| Planner, "Terra" | Product framing, architecture, decomposition, Logics request chains | Medium | Does not edit production code during planning |
| Executor, "Luna" | General repository-aware implementation | Medium | Owns one write lease at a time |
| Specialist developer | Pure implementation where a configured provider is preferred | Medium | Selected by explicit routing criteria |
| Recovery, "Sol" | Diagnose complex or repeated failures | High | Receives evidence, not the full unbounded transcript |
| Reviewer or auditor | Code, architecture, security, or release review | Medium or High | Must be independent when policy requires it |
| Operations | Pull, push, formatting, status, and other bounded mechanics | Low | High-impact actions still require approval |

Names such as Sonnet, Fable, and Opus are provider/model candidates, not guaranteed product capabilities. Startup validation reports which configured candidates are actually usable.

## Reasoning effort policy

| Effort | Use | Examples |
| --- | --- | --- |
| Low | Bounded, mechanical, reversible work with a clear command | Repository status, formatting, approved pull or push |
| Medium | Default for planning, implementation, verification, and ordinary review | Feature slice, test repair, request-chain planning |
| High | Explicit escalation where additional reasoning justifies cost and latency | Novel architecture, persistent failure recovery, deep security audit |

Effort escalation never implies permission escalation.

## MVP scope

The MVP proves one complete local loop:

- repository-scoped one-shot and interactive CLI;
- typed objective, plan, step, route, approval, run, finding, and outcome models;
- declarative role and routing configuration;
- cdx JSON adapter for selection, execution, status, and reports;
- Logics adapter for workflow inspection, creation, context packs, lint, and audit;
- persisted finite-state supervision;
- independent review and bounded recovery;
- one writer per worktree;
- local SQLite event history and inspect/export commands;
- deterministic tests using fake external CLIs.

## Explicitly deferred

- full-screen TUI or browser control plane;
- background daemon and remote clients;
- distributed scheduling and multi-machine execution;
- parallel implementation and automatic branch merging;
- adaptive model scoring based on historical performance;
- unattended deployment, publication, billing, or credential management.

## Operator controls

The initial CLI should expose a small stable command set:

- start or continue a natural-language objective;
- show the current plan, route, budget, and active run;
- approve or reject a pending action;
- pause, cancel, resume, or mark work blocked;
- inspect decisions, Logics references, run reports, usage, and artifacts;
- override role or effort for the next step without silently changing global policy.

Routine read-only inspection can be pre-approved. Network publication, deployment, destructive actions, dependency changes, and permission escalation require an explicit policy decision and are visible before execution.

## Success criteria

The MVP is successful when:

- one operator completes a plan-implement-verify-review loop from a single conversation;
- a process restart resumes without repeating a completed external run;
- every role, effort, permission, and fallback decision has a machine-readable explanation;
- live provider output cannot corrupt Orchestrato protocol output;
- failure loops stop within configured attempt, time, and agent-switch budgets;
- default tests need no provider credentials;
- Logics lint and audit gate workflow closeout;
- high-effort usage remains an exception visible in the run history.

## Roadmap

- `0.1`: inspectable conversational CLI and fake-runtime vertical slice.
- `0.2`: live cdx and Logics integration with independent review and recovery.
- `0.3`: isolated parallel worktrees, richer TUI, and policy tuning.
- `1.0`: guarded long-running delivery with proven resume, budgets, and release evidence.

The canonical roadmap is `logics/roadmap/road_001_orchestrato_product_roadmap.md`.

## Open product questions

- Which measurable signals should choose the general executor versus a specialist developer?
- Which repository actions can safely become durable pre-approvals?
- Should the operator see estimated cost before every run or only above a threshold?
- What is the smallest useful conversation summary that preserves trust during long work?
- When should review findings automatically become Logics backlog items rather than remain advisory?
