from pathlib import Path

from orchestrato.adapters.cdx import CdxAdapter, CdxRunError
from orchestrato.adapters.logics import LogicsAdapter
from orchestrato.adapters.subprocess import CommandResult, FakeRunner
from orchestrato.policy import PolicyRouter


def test_cdx_adapter_emits_json_contract_command(tmp_path: Path) -> None:
    runner = FakeRunner({"ok": True, "action": "run"})
    adapter = CdxAdapter(runner=runner)
    route = PolicyRouter().route("Implement a feature")
    result = adapter.run(route, tmp_path / "prompt.txt", cwd=tmp_path)
    assert result["action"] == "run"
    assert runner.commands[0][:3] == ["cdx", "run", "--cwd"]
    assert "--json" in runner.commands[0]


def test_logics_adapter_uses_machine_readable_status(tmp_path: Path) -> None:
    runner = FakeRunner({"ok": True, "action": "status"})
    result = LogicsAdapter(runner=runner).status(cwd=tmp_path)
    assert result["action"] == "status"
    assert runner.commands[0] == ["logics-manager", "status", "--format", "json"]


def test_cdx_selection_precedes_execution(tmp_path: Path) -> None:
    runner = FakeRunner({"ok": True, "action": "run"})
    adapter = CdxAdapter(runner=runner)
    route = PolicyRouter().route("Implement a feature")
    adapter.select(route, cwd=tmp_path)
    adapter.run(route, tmp_path / "prompt.txt", cwd=tmp_path)
    assert runner.commands[0][:3] == ["cdx", "select", "--json"]
    assert runner.commands[1][0:2] == ["cdx", "run"]


def test_cdx_adapter_reports_selection_and_run_events(tmp_path: Path) -> None:
    runner = FakeRunner({"ok": True, "action": "run", "run_id": "run-1"})
    observed: list[tuple[str, dict]] = []
    adapter = CdxAdapter(runner=runner, on_event=lambda kind, payload: observed.append((kind, payload)))
    route = PolicyRouter().route("Implement a feature")
    adapter.select(route, cwd=tmp_path)
    adapter.run(route, tmp_path / "prompt.txt", cwd=tmp_path)
    assert [kind for kind, _ in observed] == [
        "cdx_selection_started", "cdx_selection_completed", "cdx_run_started", "cdx_run_completed",
    ]


def test_cdx_adapter_exposes_safe_failure_diagnostic(tmp_path: Path) -> None:
    class FailingRunner:
        def run(self, command, *, cwd, timeout=300):
            return CommandResult(tuple(command), 1, "", "provider rejected api_key=super-secret")

    observed: list[tuple[str, dict]] = []
    adapter = CdxAdapter(runner=FailingRunner(), on_event=lambda kind, payload: observed.append((kind, payload)))
    route = PolicyRouter().route("Implement a feature")

    diagnostic = None
    try:
        adapter.run(route, tmp_path / "prompt.txt", cwd=tmp_path)
    except CdxRunError as exc:
        diagnostic = exc.diagnostic
        assert diagnostic == {"exit_code": 1, "message": "provider rejected api_key=[redacted]"}
        assert "super-secret" not in str(exc)
    else:
        raise AssertionError("expected cdx run failure")
    assert observed[-1] == ("cdx_run_failed", diagnostic)


def test_cdx_adapter_uses_stable_fallback_when_failure_is_empty(tmp_path: Path) -> None:
    class EmptyFailingRunner:
        def run(self, command, *, cwd, timeout=300):
            return CommandResult(tuple(command), 7, "", "")

    route = PolicyRouter().route("Implement a feature")
    try:
        CdxAdapter(runner=EmptyFailingRunner()).run(route, tmp_path / "prompt.txt", cwd=tmp_path)
    except CdxRunError as exc:
        assert exc.diagnostic["exit_code"] == 7
        assert "no diagnostic output" in exc.diagnostic["message"]
    else:
        raise AssertionError("expected cdx run failure")
