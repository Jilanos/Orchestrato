from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .adapters.cdx import CdxAdapter
from .models import Objective, RouteDecision
from .policy import PolicyRouter
from .store import EventStore


class Orchestrator:
    def __init__(self, store: EventStore, router: PolicyRouter) -> None:
        self.store = store
        self.router = router

    def plan(self, text: str, *, role: str | None = None, effort: str | None = None) -> Objective:
        route = self.router.route(text, role=role, effort=effort)
        objective = self.store.create(text)
        self.store.set_route(objective.objective_id, route)
        self.store.transition(objective.objective_id, "planning", {"route": route.to_dict()})
        return self.store.get(objective.objective_id)

    def approve_and_start(self, objective_id: str) -> Objective:
        objective = self.store.get(objective_id)
        if objective.route is None:
            raise ValueError("Objective has no route")
        if objective.state != "planning":
            raise ValueError(f"Objective is not awaiting execution: {objective.state}")
        if objective.route.approval_required:
            self.store.transition(objective_id, "awaiting_approval")
            self.store.transition(objective_id, "executing", {"approval": "operator"})
        else:
            self.store.transition(objective_id, "executing")
        return self.store.get(objective_id)

    def complete(self, objective_id: str, result: dict[str, Any] | None = None) -> Objective:
        objective = self.store.get(objective_id)
        if objective.state == "executing":
            self.store.transition(objective_id, "verifying", result or {})
            objective = self.store.get(objective_id)
        if objective.state == "verifying":
            self.store.transition(objective_id, "completed", result or {})
        return self.store.get(objective_id)

    def execute(self, objective_id: str, *, root: Path, cdx: CdxAdapter | None = None) -> Objective:
        objective = self.store.get(objective_id)
        if objective.state != "executing" or objective.route is None:
            raise ValueError(f"Objective is not executable: {objective.state}")
        handoff_dir = root / ".orchestrato" / "handoffs"
        handoff_dir.mkdir(parents=True, exist_ok=True)
        prompt_file = handoff_dir / f"{objective_id}.txt"
        prompt_file.write_text(
            "\n".join(
                [
                    f"Role: {objective.route.profile.label}",
                    f"Objective: {objective.text}",
                    f"Reasoning effort: {objective.route.effort}",
                    f"Permission: {objective.route.profile.permission}",
                    "Return a concise structured report with changed files, validation, blockers, and risks.",
                ]
            )
            + "\n",
            encoding="utf-8",
        )
        adapter = cdx or CdxAdapter()
        try:
            selection = adapter.select(objective.route, cwd=root)
            result = adapter.run(objective.route, prompt_file, cwd=root)
        except Exception as exc:
            self.store.transition(objective_id, "recovering", {"error": str(exc), "prompt_file": str(prompt_file)})
            self.store.transition(objective_id, "blocked", {"reason": "cdx execution failed"})
            raise RuntimeError(f"cdx execution failed: {exc}") from exc
        result = {"selection": selection, "run": result, "prompt_file": str(prompt_file)}
        return self.complete(objective_id, result)

    def render_plan(self, objective: Objective) -> dict[str, Any]:
        return {
            "objective_id": objective.objective_id,
            "text": objective.text,
            "state": objective.state,
            "route": objective.route.to_dict() if objective.route else None,
        }


def database_for(root: Path, config: dict[str, Any]) -> Path:
    configured = config.get("project", {}).get("database", ".orchestrato/state.db")
    path = Path(configured)
    return path if path.is_absolute() else root / path
