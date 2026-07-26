from __future__ import annotations

import json
import sqlite3
import uuid
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from .models import Objective, RouteDecision


TRANSITIONS = {
    "intake": {"planning", "awaiting_approval", "cancelled"},
    "planning": {"awaiting_approval", "executing", "blocked", "cancelled"},
    "awaiting_approval": {"executing", "cancelled", "blocked"},
    "executing": {"verifying", "recovering", "completed", "failed", "cancelled"},
    "verifying": {"reviewing", "completed", "recovering", "blocked"},
    "reviewing": {"completed", "planning", "recovering", "blocked"},
    "recovering": {"executing", "blocked", "failed"},
}


def now() -> str:
    return datetime.now(UTC).isoformat()


class EventStore:
    def __init__(self, path: Path) -> None:
        self.path = path
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._db = sqlite3.connect(path)
        self._db.row_factory = sqlite3.Row
        self._db.executescript(
            """
            CREATE TABLE IF NOT EXISTS objectives (
                id TEXT PRIMARY KEY,
                text TEXT NOT NULL,
                state TEXT NOT NULL,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                route_json TEXT
            );
            CREATE TABLE IF NOT EXISTS events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                objective_id TEXT NOT NULL,
                kind TEXT NOT NULL,
                from_state TEXT,
                to_state TEXT,
                payload_json TEXT NOT NULL,
                created_at TEXT NOT NULL
            );
            """
        )
        self._db.commit()

    def close(self) -> None:
        self._db.close()

    def create(self, text: str, route: RouteDecision | None = None) -> Objective:
        timestamp = now()
        objective_id = uuid.uuid4().hex[:12]
        self._db.execute(
            "INSERT INTO objectives VALUES (?, ?, ?, ?, ?, ?)",
            (objective_id, text, "intake", timestamp, timestamp, json.dumps(route.to_dict() if route else None)),
        )
        self._event(objective_id, "objective_created", None, "intake", {"text": text})
        self._db.commit()
        return self.get(objective_id)

    def set_route(self, objective_id: str, route: RouteDecision) -> Objective:
        self._db.execute(
            "UPDATE objectives SET route_json = ?, updated_at = ? WHERE id = ?",
            (json.dumps(route.to_dict()), now(), objective_id),
        )
        self._event(objective_id, "route_selected", None, None, route.to_dict())
        self._db.commit()
        return self.get(objective_id)

    def transition(self, objective_id: str, target: str, payload: dict[str, Any] | None = None) -> Objective:
        current = self.get(objective_id)
        if target not in TRANSITIONS.get(current.state, set()):
            raise ValueError(f"Invalid transition: {current.state} -> {target}")
        timestamp = now()
        self._db.execute("UPDATE objectives SET state = ?, updated_at = ? WHERE id = ?", (target, timestamp, objective_id))
        self._event(objective_id, "state_changed", current.state, target, payload or {})
        self._db.commit()
        return self.get(objective_id)

    def get(self, objective_id: str) -> Objective:
        row = self._db.execute("SELECT * FROM objectives WHERE id = ?", (objective_id,)).fetchone()
        if row is None:
            raise KeyError(f"Unknown objective: {objective_id}")
        route = json.loads(row["route_json"]) if row["route_json"] else None
        return Objective(
            objective_id=row["id"], text=row["text"], state=row["state"],
            created_at=row["created_at"], updated_at=row["updated_at"], route=_route_from_dict(route),
        )

    def list(self, limit: int = 20) -> list[Objective]:
        rows = self._db.execute("SELECT id FROM objectives ORDER BY updated_at DESC LIMIT ?", (limit,)).fetchall()
        return [self.get(row["id"]) for row in rows]

    def events(self, objective_id: str) -> list[dict[str, Any]]:
        rows = self._db.execute("SELECT * FROM events WHERE objective_id = ? ORDER BY id", (objective_id,)).fetchall()
        return [dict(row) for row in rows]

    def _event(self, objective_id: str, kind: str, from_state: str | None, to_state: str | None, payload: dict[str, Any]) -> None:
        self._db.execute(
            "INSERT INTO events(objective_id, kind, from_state, to_state, payload_json, created_at) VALUES (?, ?, ?, ?, ?, ?)",
            (objective_id, kind, from_state, to_state, json.dumps(payload), now()),
        )


def _route_from_dict(raw: dict[str, Any] | None) -> RouteDecision | None:
    if raw is None:
        return None
    profile_raw = raw["profile"]
    from .models import AgentProfile, TaskIntent
    return RouteDecision(
        intent=TaskIntent(**raw["intent"]),
        profile=AgentProfile(**profile_raw),
        effort=raw["effort"], reason=raw["reason"],
        approval_required=raw["approval_required"], fallback_roles=tuple(raw["fallback_roles"]),
    )
