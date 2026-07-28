from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Any

from .adapters.cdx import CdxAdapter
from .application import Orchestrator


class WorktreeLease:
    """Small single-host write lease using an atomic lock-file create."""

    def __init__(self, root: Path) -> None:
        self.root = root
        digest = hashlib.sha256(str(root.resolve()).encode()).hexdigest()[:16]
        self.path = root / ".orchestrato" / "locks" / f"{digest}.lock"
        self.acquired = False

    def __enter__(self) -> "WorktreeLease":
        self.path.parent.mkdir(parents=True, exist_ok=True)
        try:
            handle = self.path.open("x", encoding="utf-8")
        except FileExistsError as exc:
            raise RuntimeError(f"worktree is already locked: {self.root}") from exc
        handle.write("orchestrato\n")
        handle.close()
        self.acquired = True
        return self

    def __exit__(self, exc_type, exc, traceback) -> None:
        if self.acquired:
            self.path.unlink(missing_ok=True)
            self.acquired = False


class Supervisor:
    def __init__(self, app: Orchestrator, max_attempts: int = 2) -> None:
        self.app = app
        self.max_attempts = max(1, max_attempts)

    def execute(
        self,
        objective_id: str,
        *,
        root: Path,
        cdx: CdxAdapter | None = None,
        observer=None,
        context_pack: dict[str, Any] | None = None,
        context_max_chars: int = 12000,
    ):
        last_error: RuntimeError | None = None
        for attempt in range(1, self.max_attempts + 1):
            try:
                with WorktreeLease(root):
                    return self.app.execute(
                        objective_id,
                        root=root,
                        cdx=cdx,
                        observer=observer,
                        attempt=attempt,
                        context_pack=context_pack,
                        context_max_chars=context_max_chars,
                    )
            except RuntimeError as exc:
                last_error = exc
                objective = self.app.store.get(objective_id)
                if objective.state != "recovering" or attempt >= self.max_attempts:
                    if objective.state == "recovering":
                        self.app.store.transition(objective_id, "blocked", {"attempt": attempt, "error": str(exc)})
                    break
                self.app.publish(objective_id, "retry_scheduled", {"attempt": attempt + 1, "reason": str(exc)}, observer)
                self.app.store.transition(objective_id, "executing", {"attempt": attempt + 1, "recovery": "bounded_retry"})
        raise last_error or RuntimeError("execution failed")
