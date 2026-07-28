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
    planning_required: bool = False
    review_required: bool = False
    route_mode: str = "direct"
    risk_signals: tuple[str, ...] = ()

    def to_dict(self) -> dict[str, Any]:
        return {
            "intent": self.intent.to_dict(),
            "role": self.profile.role,
            "profile": self.profile.to_dict(),
            "effort": self.effort,
            "reason": self.reason,
            "approval_required": self.approval_required,
            "fallback_roles": list(self.fallback_roles),
            "planning_required": self.planning_required,
            "review_required": self.review_required,
            "route_mode": self.route_mode,
            "risk_signals": list(self.risk_signals),
        }


@dataclass(frozen=True)
class UsageRecord:
    """Provider usage normalized for route comparison and cost-of-pass."""

    input_tokens: int | None = None
    cached_input_tokens: int | None = None
    cache_write_tokens: int | None = None
    new_input_tokens: int | None = None
    output_tokens: int | None = None
    reasoning_tokens: int | None = None
    total_tokens: int | None = None

    @classmethod
    def from_payload(cls, payload: Any | None) -> "UsageRecord":
        raw = payload if isinstance(payload, dict) else {}
        nested = raw.get("usage") if isinstance(raw.get("usage"), dict) else raw

        def integer(*values: Any) -> int | None:
            found = []
            for value in values:
                try:
                    parsed = int(value)
                except (TypeError, ValueError):
                    continue
                if parsed >= 0:
                    found.append(parsed)
            return sum(found) if found else None

        output_details = nested.get("output_tokens_details") if isinstance(nested, dict) else {}
        input_details = nested.get("input_tokens_details") if isinstance(nested, dict) else {}
        cached = integer(
            nested.get("cached_input_tokens"), nested.get("cached_tokens"),
            nested.get("cache_read_input_tokens"),
            input_details.get("cached_tokens") if isinstance(input_details, dict) else None,
        )
        cache_write = integer(
            nested.get("cache_write_tokens"), nested.get("cache_creation_input_tokens"),
            input_details.get("cache_write_tokens") if isinstance(input_details, dict) else None,
        )
        input_tokens = integer(nested.get("input_tokens"), nested.get("prompt_tokens"))
        new_input = integer(nested.get("new_input_tokens"))
        if new_input is None and input_tokens is not None:
            new_input = max(input_tokens - (cached or 0), 0)
        reasoning = integer(
            nested.get("reasoning_tokens"), nested.get("reasoning_output_tokens"),
            output_details.get("reasoning_tokens") if isinstance(output_details, dict) else None,
        )
        output = integer(nested.get("output_tokens"), nested.get("completion_tokens"))
        total = integer(nested.get("total_tokens"))
        if total is None and input_tokens is not None and output is not None:
            total = input_tokens + output
        return cls(input_tokens, cached, cache_write, new_input, output, reasoning, total)

    def to_dict(self) -> dict[str, int | None]:
        return asdict(self)


@dataclass(frozen=True)
class Objective:
    objective_id: str
    text: str
    state: str
    created_at: str
    updated_at: str
    route: RouteDecision | None = None
