from __future__ import annotations

import json
import subprocess
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class CommandResult:
    command: tuple[str, ...]
    returncode: int
    stdout: str
    stderr: str

    def json(self) -> dict:
        try:
            payload = json.loads(self.stdout)
        except json.JSONDecodeError as exc:
            raise ValueError(f"External command returned invalid JSON: {exc}") from exc
        if not isinstance(payload, dict):
            raise ValueError("External command JSON payload must be an object")
        return payload


class CommandRunner:
    def run(self, command: list[str], *, cwd: Path, timeout: float = 300) -> CommandResult:
        completed = subprocess.run(
            command, cwd=cwd, capture_output=True, text=True, timeout=timeout, check=False,
        )
        return CommandResult(tuple(command), completed.returncode, completed.stdout, completed.stderr)


class FakeRunner:
    def __init__(self, payload: dict, returncode: int = 0) -> None:
        self.payload = payload
        self.returncode = returncode
        self.commands: list[list[str]] = []

    def run(self, command: list[str], *, cwd: Path, timeout: float = 300) -> CommandResult:
        self.commands.append(command)
        return CommandResult(tuple(command), self.returncode, json.dumps(self.payload), "")
