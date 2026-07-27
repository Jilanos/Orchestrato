from pathlib import Path

import pytest

from orchestrato.policy import PolicyRouter
from orchestrato.store import EventStore


def test_store_persists_route_and_transitions(tmp_path: Path) -> None:
    store = EventStore(tmp_path / "state.db")
    route = PolicyRouter().route("Implement a feature")
    objective = store.create(route.intent.text)
    store.set_route(objective.objective_id, route)
    store.transition(objective.objective_id, "planning")
    store.transition(objective.objective_id, "awaiting_approval")
    store.transition(objective.objective_id, "executing", {"approval": "operator"})
    assert store.get(objective.objective_id).state == "executing"
    assert len(store.events(objective.objective_id)) == 5
    store.close()

    reopened = EventStore(tmp_path / "state.db")
    restored = reopened.get(objective.objective_id)
    assert restored.route is not None
    assert restored.route.profile.role == "executor"
    assert restored.state == "executing"
    reopened.close()


def test_store_rejects_invalid_transition(tmp_path: Path) -> None:
    store = EventStore(tmp_path / "state.db")
    objective = store.create("Plan a feature")
    with pytest.raises(ValueError, match="Invalid transition"):
        store.transition(objective.objective_id, "completed")
    store.close()


def test_store_reopens_live_evidence_events(tmp_path: Path) -> None:
    store = EventStore(tmp_path / "state.db")
    objective = store.create("Observe a feature")
    recorded = store.record_event(objective.objective_id, "agent_activity", {
        "phase": "validation",
        "output": "x" * 15000,
        "api_token": "secret-value",
    })
    assert recorded["kind"] == "agent_activity"
    store.close()

    reopened = EventStore(tmp_path / "state.db")
    payload = reopened.events(objective.objective_id)[-1]["payload_json"]
    assert "secret-value" not in payload
    assert '"output":' in payload
    assert "..." in payload
    reopened.close()
