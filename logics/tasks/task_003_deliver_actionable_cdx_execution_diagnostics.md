## task_003_deliver_actionable_cdx_execution_diagnostics - Deliver actionable cdx execution diagnostics
> From version: 1.0.0
> Schema version: 1.0
> Status: Done
> Understanding: 90%
> Confidence: 85%
> Progress: 100%
> Complexity: Medium
> Theme: Implementation delivery
> Reminder: Update status/understanding/confidence/progress and linked request/backlog references when you edit this doc.
> Owner: codex

# Context
- Orchestrate the scaffolded request chain and keep sibling implementation slices linked.

# Plan
- [x] 1. Define the typed failure diagnostic and redaction boundary in the cdx adapter.
- [x] 2. Propagate the diagnostic through supervision, events, persistence, and JSON CLI reporting.
- [x] 3. Add fake-runtime contract tests for populated, empty, and redacted diagnostics.
- [x] 4. Run pytest plus Logics lint and audit, then record validation evidence.
- [x] ADR 009 checkpoint: update affected Logics docs during each meaningful wave and leave the repo commit-ready.
- [x] Keep commit creation under operator control; do not force one commit per micro-step.
- [x] GATE: do not close until lint, audit, and scaffold validation pass.

# Backlog
- `item_008_propagate_structured_cdx_run_failure_diagnostics`
- `item_009_persist_and_test_cdx_failure_diagnostics`

# Definition of Done (DoD)
- [x] Generated request, product, backlog, and task docs are present.
- [x] Context-pack handoff is available when requested.
- [x] Validation passes.
- [x] Meaningful waves followed ADR 009: affected docs updated and the repo left commit-ready without automatic commits.

# AC Traceability
- request-AC1 -> This task. Proof: scaffold command generated the request-chain corpus.
- request-AC2 -> This task. Proof: `test_execute_persists_cdx_failure_diagnostic` verifies persisted `run_failed` evidence and `test_cli_json_run_failure_includes_safe_diagnostic` verifies JSON output.
- request-AC3 -> This task. Proof: `test_cdx_adapter_exposes_safe_failure_diagnostic` and application persistence assertions verify credential-like values are redacted.
- request-AC4 -> This task. Proof: optional context-pack handoff is supported.
- request-AC6 -> This task. Proof: dry-run and collision checks bound file changes.
- request-AC8 -> This task. Proof: CLI help documents the one-pass scaffold workflow.

# Validation
- `python3 -m pytest`: 23 passed.
- `logics-manager flow validate`: 0 findings for this chain.
- `logics-manager lint --require-status`: OK.
- `logics-manager audit --group-by-doc`: 0 blocking issues (existing deferred warnings only).
- python3 -m pytest: 23 passed; flow validate: 0 findings; lint: OK; audit: 0 blocking issues
- Finish workflow executed on 2026-07-27.
- Linked backlog/request close verification passed.

# Report
- Implemented typed cdx failure diagnostics, safe redaction, event persistence, JSON CLI propagation, and offline coverage for populated and empty failures.
- Finished on 2026-07-27.
- Linked backlog item(s): `item_008_propagate_structured_cdx_run_failure_diagnostics`, `item_009_persist_and_test_cdx_failure_diagnostics`
- Related request(s): `req_002_expose_actionable_cdx_execution_failure_diagnostics`

# AI Context
- Summary: Deliver actionable cdx execution diagnostics
- Keywords: scaffolded-task, request-chain-scaffold, orchestration
- Use when: Coordinating implementation of a scaffolded request chain.
- Skip when: Working on one isolated sibling slice.

# Links
- Request: `req_002_expose_actionable_cdx_execution_failure_diagnostics`
- Product brief(s): `prod_002_actionable_cdx_failure_reporting`
- Architecture decision(s): (none yet)
