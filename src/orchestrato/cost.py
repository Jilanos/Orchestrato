from __future__ import annotations

from collections import defaultdict
from typing import Any, Iterable


TOKEN_FIELDS = (
    "total_tokens", "input_tokens", "new_input_tokens", "cached_input_tokens",
    "cache_write_tokens", "output_tokens", "reasoning_tokens",
)


def aggregate_cost_of_pass(records: Iterable[dict[str, Any]]) -> list[dict[str, Any]]:
    """Aggregate normalized run evidence by route without assuming prices."""
    groups: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for record in records:
        groups[str(record.get("route", "unknown"))].append(record)
    result = []
    for route, runs in sorted(groups.items()):
        passes = sum(bool(run.get("passed", run.get("validation_status") == "passed")) for run in runs)
        totals = {field: sum(int((run.get("usage") or run).get(field) or 0) for run in runs) for field in TOKEN_FIELDS}
        result.append({
            "route": route,
            "runs": len(runs),
            "passes": passes,
            "pass_rate": passes / len(runs) if runs else 0.0,
            "cost_of_pass_tokens": totals["total_tokens"] / passes if passes else None,
            **{f"mean_{field}": totals[field] / len(runs) if runs else 0.0 for field in TOKEN_FIELDS},
        })
    return result
