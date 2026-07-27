from pathlib import Path

from orchestrato.adapters.cdx import CdxAdapter
from orchestrato.adapters.logics import LogicsAdapter
from orchestrato.adapters.subprocess import FakeRunner
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
