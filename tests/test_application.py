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
    assert [event["kind"] for event in observed] == ["run_started", "handoff_written", "run_completed"]
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
