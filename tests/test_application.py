from pathlib import Path

from orchestrato.adapters.cdx import CdxAdapter
from orchestrato.adapters.subprocess import CommandResult, FakeRunner
from orchestrato.application import Orchestrator
from orchestrato.policy import PolicyRouter
from orchestrato.store import EventStore
from orchestrato.supervisor import Supervisor, WorktreeLease


def test_execute_persists_handoff_and_completes(tmp_path: Path) -> None:
    store = EventStore(tmp_path / "state.db")
    app = Orchestrator(store, PolicyRouter())
    planned = app.plan("Implement the first feature")
    started = app.approve_and_start(planned.objective_id)
    assert started.state == "executing"
    completed = app.execute(
        planned.objective_id,
        root=tmp_path,
        cdx=CdxAdapter(runner=FakeRunner({"ok": True, "action": "run"})),
    )
    assert completed.state == "completed"
    assert (tmp_path / ".orchestrato/handoffs" / f"{planned.objective_id}.txt").exists()
    assert [event["to_state"] for event in store.events(planned.objective_id)][-2:] == ["verifying", "completed"]
    store.close()


def test_execute_persists_usage_and_stops_for_required_review(tmp_path: Path) -> None:
    store = EventStore(tmp_path / "state.db")
    app = Orchestrator(store, PolicyRouter())
    planned = app.plan("Implement a database schema migration")
    app.approve_and_start(planned.objective_id)
    completed = app.execute(
        planned.objective_id,
        root=tmp_path,
        cdx=CdxAdapter(runner=FakeRunner({
            "ok": True,
            "action": "run",
            "run_id": "run-cost-1",
            "duration_seconds": 4.2,
            "usage": {
                "input_tokens": 100,
                "cached_input_tokens": 80,
                "output_tokens": 20,
                "reasoning_tokens": 5,
                "total_tokens": 120,
            },
        })),
    )
    assert completed.state == "reviewing"
    evidence = [event for event in store.events(planned.objective_id) if event["kind"] == "cost_of_pass"]
    assert len(evidence) == 1
    assert "run-cost-1" in evidence[0]["payload_json"]
    assert "new_input_tokens" in evidence[0]["payload_json"]
    accepted = app.finalize_review(planned.objective_id, accepted=True)
    assert accepted.state == "completed"
    store.close()


def test_execute_publishes_live_events_and_redacts_payload(tmp_path: Path) -> None:
    store = EventStore(tmp_path / "state.db")
    app = Orchestrator(store, PolicyRouter())
    planned = app.plan("Implement the first feature")
    app.approve_and_start(planned.objective_id)
    observed: list[dict] = []

    completed = app.execute(
        planned.objective_id,
        root=tmp_path,
        cdx=CdxAdapter(runner=FakeRunner({"ok": True, "action": "run"})),
        observer=observed.append,
    )

    assert completed.state == "completed"
    assert [event["kind"] for event in observed] == ["run_started", "handoff_written", "cost_of_pass", "run_completed"]
    handoff = (tmp_path / ".orchestrato/handoffs" / f"{planned.objective_id}.txt").read_text()
    assert '"objective": "Implement the first feature"' in handoff
    assert any(event["kind"] == "cost_of_pass" for event in store.events(planned.objective_id))
    persisted = store.events(planned.objective_id)
    assert any(event["kind"] == "run_started" for event in persisted)
    store.record_event(planned.objective_id, "provider_evidence", {"access_token": "do-not-store"})
    assert "[redacted]" in store.events(planned.objective_id)[-1]["payload_json"]
    store.close()


def test_supervisor_retries_once_then_blocks(tmp_path: Path) -> None:
    store = EventStore(tmp_path / "state.db")
    app = Orchestrator(store, PolicyRouter())
    planned = app.plan("Implement the feature")
    app.approve_and_start(planned.objective_id)
    class SelectThenFailRunner:
        def __init__(self) -> None:
            self.commands: list[list[str]] = []

        def run(self, command, *, cwd, timeout=300):
            self.commands.append(command)
            if command[1] == "select":
                return CommandResult(tuple(command), 0, '{"ok": true}', "")
            return CommandResult(tuple(command), 1, "", "provider failed")

    runner = SelectThenFailRunner()
    try:
        Supervisor(app, max_attempts=2).execute(
            planned.objective_id,
            root=tmp_path,
            cdx=CdxAdapter(runner=runner),
        )
    except RuntimeError:
        pass
    assert store.get(planned.objective_id).state == "blocked"
    assert len(runner.commands) == 4
    store.close()


def test_execute_persists_cdx_failure_diagnostic(tmp_path: Path) -> None:
    store = EventStore(tmp_path / "state.db")
    app = Orchestrator(store, PolicyRouter())
    planned = app.plan("Implement the feature")
    app.approve_and_start(planned.objective_id)

    class FailingRunner:
        def run(self, command, *, cwd, timeout=300):
            if command[1] == "select":
                return CommandResult(tuple(command), 0, '{"ok": true}', "")
            return CommandResult(tuple(command), 1, "", "provider rejected password=hidden-value")

    try:
        app.execute(planned.objective_id, root=tmp_path, cdx=CdxAdapter(runner=FailingRunner()))
    except RuntimeError as exc:
        assert "provider rejected password=[redacted]" in str(exc)
        assert "hidden-value" not in str(exc)
        assert getattr(exc, "diagnostic")["exit_code"] == 1
    else:
        raise AssertionError("expected execution failure")

    failed = [event for event in store.events(planned.objective_id) if event["kind"] == "run_failed"]
    assert len(failed) == 1
    assert "password=[redacted]" in failed[0]["payload_json"]
    assert "hidden-value" not in failed[0]["payload_json"]
    assert store.get(planned.objective_id).state == "recovering"
    store.close()


def test_worktree_lease_is_exclusive(tmp_path: Path) -> None:
    first = WorktreeLease(tmp_path)
    first.__enter__()
    try:
        try:
            WorktreeLease(tmp_path).__enter__()
        except RuntimeError as exc:
            assert "already locked" in str(exc)
        else:
            raise AssertionError("second lease unexpectedly acquired")
    finally:
        first.__exit__(None, None, None)
