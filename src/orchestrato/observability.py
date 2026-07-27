from __future__ import annotations

import json
import re
import sys
from datetime import datetime, timezone
from typing import Any, TextIO


SENSITIVE_KEYS = ("token", "secret", "password", "authorization", "credential", "env")
MAX_STRING_LENGTH = 2000
MAX_PAYLOAD_LENGTH = 12000

_SENSITIVE_TEXT = re.compile(
    r"(?i)(\b(?:api[_-]?key|access[_-]?token|refresh[_-]?token|password|secret|authorization|credential)\b\s*[:=]\s*)([^\s,;]+)"
)


def bounded_payload(payload: dict[str, Any]) -> dict[str, Any]:
    """Keep event evidence useful without persisting secrets or huge output."""
    value = _redact(payload)
    encoded = json.dumps(value, ensure_ascii=True, default=str)
    if len(encoded) <= MAX_PAYLOAD_LENGTH:
        return value
    return {"summary": encoded[:MAX_PAYLOAD_LENGTH], "truncated": True}


def _redact(value: Any, key: str = "") -> Any:
    if any(marker in key.lower() for marker in SENSITIVE_KEYS):
        return "[redacted]"
    if isinstance(value, dict):
        return {str(item_key): _redact(item_value, str(item_key)) for item_key, item_value in value.items()}
    if isinstance(value, (list, tuple)):
        return [_redact(item, key) for item in value]
    if isinstance(value, str):
        value = _SENSITIVE_TEXT.sub(r"\1[redacted]", value)
        if len(value) > MAX_STRING_LENGTH:
            return value[:MAX_STRING_LENGTH] + "..."
    return value


class LiveReporter:
    """Dependency-free event reporter suitable for terminals and stderr."""

    def __init__(self, stream: TextIO | None = None) -> None:
        self.stream = stream or sys.stderr
        self._events: list[dict[str, Any]] = []
        self._live = None
        self._table = None

    def start(self) -> None:
        try:
            from rich.console import Console
            from rich.live import Live
            from rich.table import Table
        except ImportError:
            return
        self._table = Table(title="Orchestrato live execution")
        self._table.add_column("Time", style="dim")
        self._table.add_column("Event")
        self._table.add_column("Details")
        self._live = Live(self._table, console=Console(file=self.stream), refresh_per_second=4)
        self._live.start()

    def close(self) -> None:
        if self._live:
            self._live.stop()

    def __call__(self, event: dict[str, Any]) -> None:
        timestamp = datetime.now(timezone.utc).strftime("%H:%M:%S")
        kind = event.get("kind", "event")
        payload = event.get("payload", {})
        objective_id = event.get("objective_id", "-")
        detail = self._detail(kind, payload)
        if self._live and self._table:
            self._events.append(event)
            self._table.rows.clear()
            for item in self._events[-8:]:
                item_time = item.get("created_at", timestamp)[11:19]
                item_kind = item.get("kind", "event")
                self._table.add_row(item_time, item_kind, self._detail(item_kind, item.get("payload", {})))
            self._live.refresh()
            return
        print(f"[{timestamp}] {objective_id} {kind}: {detail}", file=self.stream, flush=True)

    def _detail(self, kind: str, payload: dict[str, Any]) -> str:
        if kind == "route_selected":
            return f"role={payload.get('role')} provider={payload.get('provider')} effort={payload.get('effort')} permission={payload.get('permission')}"
        if kind == "approval_granted":
            return f"state={payload.get('state')}"
        if kind == "run_started":
            return f"role={payload.get('role')} provider={payload.get('provider')} model={payload.get('model') or 'default'} permission={payload.get('permission')}"
        if kind == "cdx_selection_completed":
            return f"session={payload.get('session', 'unknown')} provider={payload.get('provider', 'unknown')} availability={payload.get('available_pct', '?')}%"
        if kind == "cdx_run_started":
            return f"effort={payload.get('reasoning_effort', '?')} cwd={payload.get('cwd', '?')}"
        if kind == "cdx_run_waiting":
            return f"status={payload.get('status', 'unknown')} elapsed={payload.get('elapsed_seconds', '?')}s"
        if kind == "cdx_run_observation":
            return f"status={payload.get('status', 'unknown')} run_id={payload.get('run_id', 'unknown')}"
        if kind == "cdx_run_completed":
            return f"run_id={payload.get('run_id', 'unknown')} exit_code={payload.get('exit_code', '?')} duration={payload.get('duration_seconds', '?')}s"
        if kind == "cdx_run_failed":
            return f"exit_code={payload.get('exit_code', '?')} message={payload.get('message', 'unknown error')}"
        if kind == "retry_scheduled":
            return f"attempt={payload.get('attempt')} reason={payload.get('reason', 'unknown')}"
        if kind == "run_failed":
            return str(payload.get("error", "unknown error"))
        if kind == "run_completed":
            return f"state={payload.get('state', 'completed')}"
        if kind == "handoff_written":
            return f"prompt={payload.get('prompt_file', '?')}"
        return json.dumps(bounded_payload(payload), ensure_ascii=False, sort_keys=True)
