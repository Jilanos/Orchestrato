from __future__ import annotations

from pathlib import Path
from typing import Any

from .subprocess import CommandRunner
from ..models import RouteDecision


class CdxAdapter:
    def __init__(self, runner: CommandRunner | None = None, executable: str = "cdx") -> None:
        self.runner = runner or CommandRunner()
        self.executable = executable

    def select(self, route: RouteDecision, *, cwd: Path) -> dict[str, Any]:
        command = [self.executable, "select", "--json"]
        if route.profile.provider:
            command.extend(["--provider", route.profile.provider])
        command.extend(["--min-reasoning-effort", route.effort])
        result = self.runner.run(command, cwd=cwd)
        if result.returncode != 0:
            raise RuntimeError(result.stderr.strip() or "cdx select failed")
        return result.json()

    def run(self, route: RouteDecision, prompt_file: Path, *, cwd: Path, timeout: float = 900) -> dict[str, Any]:
        command = [
            self.executable, "run", "--cwd", str(cwd), "--prompt-file", str(prompt_file),
            "--reasoning-effort", route.effort, "--permission", route.profile.permission, "--json",
        ]
        if route.profile.provider:
            command.extend(["--provider", route.profile.provider])
        if route.profile.model:
            command.extend(["--model", route.profile.model])
        result = self.runner.run(command, cwd=cwd, timeout=timeout)
        if result.returncode != 0:
            raise RuntimeError(result.stderr.strip() or "cdx run failed")
        return result.json()
