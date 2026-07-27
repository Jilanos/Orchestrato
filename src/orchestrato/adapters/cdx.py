from __future__ import annotations

import time
from threading import Thread
from pathlib import Path
from typing import Any, Callable

from .subprocess import CommandRunner
from ..models import RouteDecision
from ..observability import bounded_payload


class CdxRunError(RuntimeError):
    """A safe, structured diagnostic returned by a failed cdx run."""

    def __init__(self, diagnostic: dict[str, Any]) -> None:
        self.diagnostic = diagnostic
        super().__init__(diagnostic["message"])


class CdxAdapter:
    def __init__(self, runner: CommandRunner | None = None, executable: str = "cdx", on_event: Callable[[str, dict[str, Any]], None] | None = None) -> None:
        self.runner = runner or CommandRunner()
        self.executable = executable
        self.on_event = on_event

    def _emit(self, kind: str, payload: dict[str, Any]) -> None:
        if self.on_event:
            self.on_event(kind, payload)

    def select(self, route: RouteDecision, *, cwd: Path) -> dict[str, Any]:
        command = [self.executable, "select", "--json"]
        if route.profile.provider:
            command.extend(["--provider", route.profile.provider])
        command.extend(["--min-reasoning-effort", route.effort])
        self._emit("cdx_selection_started", {"provider": route.profile.provider or "automatic", "effort": route.effort})
        result = self.runner.run(command, cwd=cwd)
        if result.returncode != 0:
            raise RuntimeError(result.stderr.strip() or "cdx select failed")
        payload = result.json()
        self._emit("cdx_selection_completed", payload)
        return payload

    def run(self, route: RouteDecision, prompt_file: Path, *, cwd: Path, timeout: float = 900) -> dict[str, Any]:
        command = [
            self.executable, "run", "--cwd", str(cwd), "--prompt-file", str(prompt_file),
            "--reasoning-effort", route.effort, "--permission", route.profile.permission, "--json",
        ]
        if route.profile.provider:
            command.extend(["--provider", route.profile.provider])
        if route.profile.model:
            command.extend(["--model", route.profile.model])
        self._emit("cdx_run_started", {"cwd": str(cwd), "reasoning_effort": route.effort, "permission": route.profile.permission})
        result_box = []
        error_box: list[BaseException] = []

        def invoke() -> None:
            try:
                result_box.append(self.runner.run(command, cwd=cwd, timeout=timeout))
            except BaseException as exc:  # Re-raise in the caller thread after reporting liveness.
                error_box.append(exc)

        worker = Thread(target=invoke, daemon=True)
        worker.start()
        started_at = time.monotonic()
        while worker.is_alive():
            worker.join(timeout=2.0)
            if worker.is_alive():
                self._emit("cdx_run_waiting", {
                    "status": "provider_execution",
                    "elapsed_seconds": round(time.monotonic() - started_at, 1),
                })
                self._poll_runs(cwd)
        if error_box:
            raise error_box[0]
        result = result_box[0]
        if result.returncode != 0:
            diagnostic = bounded_payload({
                "exit_code": result.returncode,
                "message": result.stderr.strip() or result.stdout.strip() or (
                    f"cdx run exited with code {result.returncode} and produced no diagnostic output"
                ),
            })
            self._emit("cdx_run_failed", diagnostic)
            raise CdxRunError(diagnostic)
        payload = result.json()
        self._emit("cdx_run_completed", payload)
        return payload

    def _poll_runs(self, cwd: Path) -> None:
        """Use cdx's JSON status contract when the provider stream is unavailable."""
        try:
            result = self.runner.run([self.executable, "runs", "--limit", "5", "--json"], cwd=cwd, timeout=10)
            if result.returncode != 0:
                return
            payload = result.json()
            runs = payload.get("runs", [])
            active = next((item for item in runs if item.get("status") in {"running", "active", "started"}), None)
            if active:
                self._emit("cdx_run_observation", {
                    "status": active.get("status"),
                    "run_id": active.get("run_id"),
                })
        except (RuntimeError, ValueError, KeyError, TypeError):
            # The main run remains authoritative; a monitoring failure is observable through the heartbeat.
            return

    def run_status(self, run_id: str, *, cwd: Path) -> dict[str, Any]:
        result = self.runner.run([self.executable, "run-status", run_id, "--json"], cwd=cwd)
        if result.returncode != 0:
            raise RuntimeError(result.stderr.strip() or "cdx run-status failed")
        return result.json()

    def run_report(self, run_id: str, *, cwd: Path) -> dict[str, Any]:
        result = self.runner.run([self.executable, "run-report", run_id, "--json"], cwd=cwd)
        if result.returncode != 0:
            raise RuntimeError(result.stderr.strip() or "cdx run-report failed")
        return result.json()
