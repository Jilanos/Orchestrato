from __future__ import annotations

from pathlib import Path
from typing import Any

from .subprocess import CommandRunner


class LogicsAdapter:
    def __init__(self, runner: CommandRunner | None = None, executable: str = "logics-manager") -> None:
        self.runner = runner or CommandRunner()
        self.executable = executable

    def status(self, *, cwd: Path) -> dict[str, Any]:
        result = self.runner.run([self.executable, "status", "--format", "json"], cwd=cwd)
        if result.returncode != 0:
            raise RuntimeError(result.stderr.strip() or "logics-manager status failed")
        return result.json()

    def validate(self, refs: list[str], *, cwd: Path) -> dict[str, Any]:
        result = self.runner.run([self.executable, "flow", "validate", *refs, "--format", "json"], cwd=cwd)
        if result.returncode != 0:
            raise RuntimeError(result.stderr.strip() or "logics-manager validation failed")
        return result.json()
