from pathlib import Path

from orchestrato.adapters.cdx import CdxAdapter
from orchestrato.adapters.subprocess import FakeRunner
from orchestrato.application import Orchestrator
from orchestrato.policy import PolicyRouter
from orchestrato.store import EventStore


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
