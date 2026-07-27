import json
from pathlib import Path

from orchestrato.cli import main


def test_cli_plan_and_status_are_resumable(tmp_path: Path, capsys) -> None:
    assert main(["--root", str(tmp_path), "--json", "plan", "Plan the CLI architecture"]) == 0
    planned = json.loads(capsys.readouterr().out)
    objective_id = planned["objective_id"]
    assert planned["state"] == "planning"

    assert main(["--root", str(tmp_path), "--json", "status"]) == 0
    status = json.loads(capsys.readouterr().out)
    assert status["objectives"][0]["objective_id"] == objective_id


def test_cli_requires_approval_for_mutating_run(tmp_path: Path, capsys) -> None:
    assert main(["--root", str(tmp_path), "--json", "run", "Implement the feature"]) == 2
    payload = json.loads(capsys.readouterr().out)
    assert payload["error"] == "approval_required"


def test_cli_can_approve_a_planned_objective(tmp_path: Path, capsys) -> None:
    assert main(["--root", str(tmp_path), "--json", "plan", "Implement the feature"]) == 0
    objective_id = json.loads(capsys.readouterr().out)["objective_id"]
    assert main(["--root", str(tmp_path), "--json", "approve", objective_id]) == 0
    approved = json.loads(capsys.readouterr().out)
    assert approved["state"] == "executing"


def test_cli_live_flag_is_available_without_corrupting_json(tmp_path: Path, capsys) -> None:
    assert main(["--root", str(tmp_path), "--json", "run", "Implement the feature", "--live"]) == 2
    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    assert payload["error"] == "approval_required"
    assert "route_selected" in captured.err


def test_cli_json_run_failure_includes_safe_diagnostic(tmp_path: Path, capsys, monkeypatch) -> None:
    class FailingCdx:
        def __init__(self, on_event=None):
            self.on_event = on_event

        def select(self, route, *, cwd):
            return {"session": "fake", "provider": "codex"}

        def run(self, route, prompt_file, *, cwd):
            from orchestrato.adapters.cdx import CdxRunError
            diagnostic = {"exit_code": 9, "message": "provider rejected api_key=[redacted]"}
            raise CdxRunError(diagnostic)

    monkeypatch.setattr("orchestrato.application.CdxAdapter", FailingCdx)
    result = main([
        "--root", str(tmp_path), "--json", "run", "Implement the feature", "--yes", "--execute",
    ])
    payload = json.loads(capsys.readouterr().out)
    assert result == 1
    assert payload["ok"] is False
    assert payload["diagnostic"] == {"exit_code": 9, "message": "provider rejected api_key=[redacted]"}
