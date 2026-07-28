from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any


DEFAULT_MAX_CHARS = 12000
ROLE_FIELDS = {
    "planner": ("objective", "acceptance_criteria", "references", "constraints", "non_goals"),
    "executor": ("objective", "acceptance_criteria", "revision", "relevant_files", "validation", "constraints", "non_goals"),
    "reviewer": ("objective", "acceptance_criteria", "revision", "diff_summary", "validation", "risk_signals"),
    "recovery": ("objective", "acceptance_criteria", "revision", "failure", "diff_summary", "validation", "prior_attempts"),
}


@dataclass(frozen=True)
class HandoffPacket:
    role: str
    fields: dict[str, Any]
    truncated: bool = False
    truncation_reason: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "role": self.role,
            "context": self.fields,
            "truncated": self.truncated,
            "truncation_reason": self.truncation_reason,
        }

    def render(self) -> str:
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=2, sort_keys=True)


def build_handoff_packet(
    *,
    role: str,
    objective: str,
    context_pack: dict[str, Any] | None = None,
    max_chars: int = DEFAULT_MAX_CHARS,
    extra: dict[str, Any] | None = None,
) -> HandoffPacket:
    """Project a context pack into a role-specific, bounded handoff.

    The full workflow corpus is never copied into the prompt. Unknown fields
    remain available only through compact references and explicit role fields.
    """
    source = context_pack if isinstance(context_pack, dict) else {}
    merged = {**source, **(extra or {})}
    fields: dict[str, Any] = {"objective": objective}
    for field in ROLE_FIELDS.get(role, ROLE_FIELDS["executor"]):
        if field == "objective":
            continue
        if field in merged and merged[field] not in (None, "", [], {}):
            fields[field] = merged[field]
    fields.setdefault("references", source.get("refs", source.get("references", [])))
    packet = HandoffPacket(role, fields)
    encoded = packet.render()
    if max_chars <= 0:
        raise ValueError("max_chars must be positive")
    if len(encoded) <= max_chars:
        return packet
    compact = {
        "references": fields.get("references", []),
        "summary": source.get("summary", source.get("title", "Context reduced to references and summary.")),
    }
    reduced = HandoffPacket(role, {"objective": objective, **compact}, True, "max_chars_exceeded")
    reduced_encoded = reduced.render()
    if len(reduced_encoded) <= max_chars:
        return reduced
    summary = str(compact["summary"])
    budget = max(32, max_chars - len(reduced.render()) + len(summary))
    compact["summary"] = summary[:budget] + ("..." if len(summary) > budget else "")
    return HandoffPacket(role, {"objective": objective, **compact}, True, "max_chars_exceeded")
