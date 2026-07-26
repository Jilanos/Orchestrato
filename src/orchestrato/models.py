from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any


STATES = (
    "intake",
    "planning",
    "awaiting_approval",
    "executing",
    "verifying",
    "reviewing",
    "recovering",
    "completed",
    "blocked",
    "cancelled",
    "failed",
)

TERMINAL_STATES = {"completed", "blocked", "cancelled", "failed"}


@dataclass(frozen=True)
class AgentProfile:
    role: str
    label: str
    provider: str
    model: str
    effort: str
    permission: str

    def to_dict(self) -> dict[str, str]:
        return asdict(self)


@dataclass(frozen=True)
class TaskIntent:
    text: str
    kind: str
    risk: str
    mutating: bool

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class RouteDecision:
    intent: TaskIntent
    profile: AgentProfile
    effort: str
    reason: str
    approval_required: bool
    fallback_roles: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        return {
            "intent": self.intent.to_dict(),
            "role": self.profile.role,
            "profile": self.profile.to_dict(),
            "effort": self.effort,
            "reason": self.reason,
            "approval_required": self.approval_required,
            "fallback_roles": list(self.fallback_roles),
        }


@dataclass(frozen=True)
class Objective:
    objective_id: str
    text: str
    state: str
    created_at: str
    updated_at: str
    route: RouteDecision | None = None
