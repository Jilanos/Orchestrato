from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .adapters.cdx import CdxAdapter
from .context import DEFAULT_MAX_CHARS, build_handoff_packet
from .models import Objective, RouteDecision, UsageRecord
from .policy import PolicyRouter
from .store import EventStore


class ExecutionError(RuntimeError):
    """A failed execution with a safe diagnostic for CLI and recovery flows."""

    def __init__(self, message: str, diagnostic: dict[str, Any]) -> None:
        self.diagnostic = diagnostic
        super().__init__(message)


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

    def cancel(self, objective_id: str) -> Objective:
        return self.store.transition(objective_id, "cancelled", {"actor": "operator"})

    def complete(self, objective_id: str, result: dict[str, Any] | None = None) -> Objective:
        objective = self.store.get(objective_id)
        if objective.state == "executing":
            self.store.transition(objective_id, "verifying", result or {})
            objective = self.store.get(objective_id)
        if objective.state == "verifying":
            if objective.route and objective.route.review_required:
                self.store.transition(objective_id, "reviewing", result or {})
            else:
                self.store.transition(objective_id, "completed", result or {})
        return self.store.get(objective_id)

    def finalize_review(self, objective_id: str, *, accepted: bool, evidence: dict[str, Any] | None = None) -> Objective:
        objective = self.store.get(objective_id)
        if objective.state != "reviewing":
            raise ValueError(f"Objective is not awaiting review: {objective.state}")
        payload = {"accepted": accepted, **(evidence or {})}
        self.store.transition(objective_id, "completed" if accepted else "recovering", payload)
        return self.store.get(objective_id)

    def execute(
        self,
        objective_id: str,
        *,
        root: Path,
        cdx: CdxAdapter | None = None,
        observer=None,
        context_pack: dict[str, Any] | None = None,
        context_max_chars: int = DEFAULT_MAX_CHARS,
        attempt: int = 1,
    ) -> Objective:
        objective = self.store.get(objective_id)
        if objective.state != "executing" or objective.route is None:
            raise ValueError(f"Objective is not executable: {objective.state}")
        handoff_dir = root / ".orchestrato" / "handoffs"
        handoff_dir.mkdir(parents=True, exist_ok=True)
        prompt_file = handoff_dir / f"{objective_id}.txt"
        packet = build_handoff_packet(
            role=objective.route.profile.role,
            objective=objective.text,
            context_pack=context_pack,
            max_chars=context_max_chars,
            extra={"effort": objective.route.effort, "permission": objective.route.profile.permission},
        )
        prompt_file.write_text(
            "Role: " + objective.route.profile.label + "\n"
            "Return a concise structured report with changed files, validation, blockers, and risks.\n"
            "Bounded task packet:\n" + packet.render() + "\n",
            encoding="utf-8",
        )
        self.publish(objective_id, "run_started", {
            "role": objective.route.profile.role,
            "provider": objective.route.profile.provider or "automatic",
            "model": objective.route.profile.model,
            "effort": objective.route.effort,
            "permission": objective.route.profile.permission,
            "cwd": str(root),
        }, observer)
        self.publish(objective_id, "handoff_written", {
            "prompt_file": str(prompt_file),
            "role": packet.role,
            "context_chars": len(packet.render()),
            "context_truncated": packet.truncated,
            "truncation_reason": packet.truncation_reason,
        }, observer)
        adapter = cdx or CdxAdapter(on_event=lambda kind, payload: self.publish(objective_id, kind, payload, observer))
        try:
            selection = adapter.select(objective.route, cwd=root)
            result = adapter.run(objective.route, prompt_file, cwd=root)
        except Exception as exc:
            diagnostic = getattr(exc, "diagnostic", {"message": str(exc)})
            self.publish(objective_id, "run_failed", diagnostic, observer)
            self.store.transition(objective_id, "recovering", {"diagnostic": diagnostic, "prompt_file": str(prompt_file)})
            raise ExecutionError(f"cdx execution failed: {diagnostic.get('message', str(exc))}", diagnostic) from exc
        result = {"selection": selection, "run": result, "prompt_file": str(prompt_file)}
        run_payload = result.get("run", {})
        usage = UsageRecord.from_payload(run_payload.get("usage", run_payload))
        validation_status = str(run_payload.get("validation_status", "not_reported"))
        cost_evidence = self.store.record_cost_evidence(
            objective_id,
            usage=usage,
            route=objective.route,
            duration_seconds=run_payload.get("duration_seconds"),
            retries=max(0, attempt - 1),
            validation_status=validation_status,
            raw_run_ref=run_payload.get("run_id"),
        )
        if observer:
            observer({
                "id": cost_evidence["id"],
                "objective_id": objective_id,
                "kind": "cost_of_pass",
                "payload": json_payload(cost_evidence),
                "created_at": cost_evidence["created_at"],
            })
        result["cost_of_pass"] = cost_evidence
        next_state = "reviewing" if objective.route.review_required else "completed"
        self.publish(objective_id, "run_completed", {"state": next_state, "run": result.get("run", {})}, observer)
        return self.complete(objective_id, result)

    def publish(self, objective_id: str, kind: str, payload: dict[str, Any], observer=None) -> None:
        event = self.store.record_event(objective_id, kind, payload)
        if observer:
            observer({
                "id": event["id"],
                "objective_id": objective_id,
                "kind": kind,
                "payload": payload,
                "created_at": event["created_at"],
            })

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


def json_payload(event: dict[str, Any]) -> dict[str, Any]:
    """Decode the bounded event payload without exposing store internals."""
    raw = event.get("payload_json", "{}")
    try:
        parsed = json.loads(raw)
    except (TypeError, json.JSONDecodeError):
        return {"event_id": event.get("id")}
    return {"event_id": event.get("id"), **parsed}
