## req_002_expose_actionable_cdx_execution_failure_diagnostics - Expose actionable cdx execution failure diagnostics
> From version: 1.0.0
> Schema version: 1.0
> Status: Done
> Understanding: 90%
> Confidence: 85%
> Complexity: Medium
> Theme: Runtime reliability
> Reminder: Update status/understanding/confidence and linked backlog/task references when you edit this doc.

# Needs
- An operator needs the actual cdx execution failure to diagnose a rejected live run without rerunning the command manually.

# Context
- CdxAdapter currently raises a generic cdx run failed error when subprocess stderr is empty or unavailable to the outer reporter.
- The failure must remain safe for JSON output and must not expose credentials or prompt secrets.

# Acceptance criteria
- AC1: A non-zero cdx run result produces a structured, actionable diagnostic containing the exit code and bounded safe stderr or stdout context when available.
- AC2: Orchestrato persists the safe diagnostic in its event history and returns it through the JSON CLI failure response.
- AC3: Credential-like values and prompt content are redacted from diagnostics before persistence or display.
- AC4: Offline contract tests cover a cdx run failure with diagnostic output and a failure without diagnostic output.

# Definition of Ready (DoR)
- [x] Problem statement is explicit and user impact is clear.
- [x] Scope boundaries (in/out) are explicit.
- [x] Acceptance criteria are testable.
- [x] Dependencies and known risks are listed.

# Companion docs
- Product brief(s): `prod_002_actionable_cdx_failure_reporting`
- Architecture decision(s): (none yet)

# References
- src/orchestrato/adapters/cdx.py
- src/orchestrato/cli.py
- tests/test_adapters.py
- tests/test_cli.py

# AI Context
- Summary: Expose actionable cdx execution failure diagnostics
- Keywords: request-chain-scaffold, expose actionable cdx execution failure diagnostics, development-ready
- Use when: You need to implement or review the scaffolded workflow for Expose actionable cdx execution failure diagnostics.
- Skip when: The change is unrelated to this scaffolded request chain.

# Backlog
- `item_008_propagate_structured_cdx_run_failure_diagnostics`
- `item_009_persist_and_test_cdx_failure_diagnostics`
