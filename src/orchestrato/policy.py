from __future__ import annotations

import tomllib
from pathlib import Path
from typing import Any

from .models import AgentProfile, RouteDecision, TaskIntent


EFFORTS = {"low", "medium", "high"}

DEFAULT_ROLES = {
    "planner": AgentProfile("planner", "Terra", "codex", "", "medium", "review"),
    "executor": AgentProfile("executor", "Luna", "codex", "", "medium", "workspace-write"),
    "recovery": AgentProfile("recovery", "Sol", "codex", "", "high", "workspace-write"),
    "specialist": AgentProfile("specialist", "Specialist developer", "claude", "", "medium", "workspace-write"),
    "reviewer": AgentProfile("reviewer", "Reviewer", "claude", "", "medium", "read-only"),
    "operations": AgentProfile("operations", "Operations", "", "", "low", "review"),
}


def load_config(path: Path | None) -> dict[str, Any]:
    if path is None or not path.exists():
        return {}
    with path.open("rb") as handle:
        return tomllib.load(handle)


def profiles_from_config(config: dict[str, Any]) -> dict[str, AgentProfile]:
    profiles = dict(DEFAULT_ROLES)
    for role, raw in config.get("roles", {}).items():
        if not isinstance(raw, dict) or role not in profiles:
            continue
        base = profiles[role]
        profiles[role] = AgentProfile(
            role=role,
            label=str(raw.get("label", base.label)),
            provider=str(raw.get("provider", base.provider)),
            model=str(raw.get("model", base.model)),
            effort=str(raw.get("effort", base.effort)),
            permission=str(raw.get("permission", base.permission)),
        )
    return profiles


def classify(text: str) -> TaskIntent:
    normalized = text.casefold()
    if any(word in normalized for word in ("pull", "push", "git status", "format", "sync")):
        return TaskIntent(text, "operations", "external" if "push" in normalized else "low", "push" in normalized)
    if any(word in normalized for word in ("review", "audit", "security", "vulnerability")):
        return TaskIntent(text, "review", "high" if "security" in normalized or "vulnerability" in normalized else "medium", False)
    if any(word in normalized for word in ("stuck", "blocked", "cannot", "failure", "failing", "broken")):
        return TaskIntent(text, "recovery", "high", True)
    if any(word in normalized for word in ("plan", "architecture", "roadmap", "design", "decompose")):
        return TaskIntent(text, "planning", "medium", False)
    high_risk = any(word in normalized for word in (
        "migration", "schema", "database", "concurrency", "distributed", "external integration", "release-critical",
    ))
    return TaskIntent(text, "implementation", "high" if high_risk else "medium", True)


class PolicyRouter:
    def __init__(self, config: dict[str, Any] | None = None) -> None:
        self.config = config or {}
        self.profiles = profiles_from_config(self.config)
        default_effort = self.config.get("policy", {}).get("default_effort", "medium")
        self.default_effort = default_effort if default_effort in EFFORTS else "medium"

    def route(self, text: str, *, role: str | None = None, effort: str | None = None) -> RouteDecision:
        intent = classify(text)
        selected_role = role or {
            "operations": "operations",
            "review": "reviewer",
            "recovery": "recovery",
            "planning": "planner",
            "implementation": "executor",
        }[intent.kind]
        if selected_role not in self.profiles:
            raise ValueError(f"Unknown role: {selected_role}")
        resolved_effort = effort or self.profiles[selected_role].effort or self.default_effort
        if resolved_effort not in EFFORTS:
            raise ValueError(f"Unsupported effort: {resolved_effort}")
        approval_required = intent.mutating or intent.risk == "external"
        fallback_roles = {
            "executor": ("specialist", "recovery"),
            "specialist": ("executor", "recovery"),
            "planner": ("executor",),
            "reviewer": ("planner",),
            "recovery": (),
            "operations": (),
        }[selected_role]
        risk_signals = tuple(signal for signal in (
            "high_risk", "review_requested", "planning_requested", "cross_system",
        ) if (
            signal == "high_risk" and intent.risk == "high"
        ) or (
            signal == "review_requested" and intent.kind == "review"
        ) or (
            signal == "planning_requested" and intent.kind == "planning"
        ) or (
            signal == "cross_system" and any(word in intent.text.casefold() for word in ("service", "integration", "distributed"))
        ))
        planning_required = intent.kind == "planning" or intent.risk == "high"
        review_required = intent.kind == "review" or intent.risk == "high"
        route_mode = "escalated" if planning_required or review_required else "direct"
        return RouteDecision(
            intent=intent,
            profile=self.profiles[selected_role],
            effort=resolved_effort,
            reason=f"Matched intent `{intent.kind}` with risk `{intent.risk}`; selected role `{selected_role}`.",
            approval_required=approval_required,
            fallback_roles=fallback_roles,
            planning_required=planning_required,
            review_required=review_required,
            route_mode=route_mode,
            risk_signals=risk_signals,
        )
