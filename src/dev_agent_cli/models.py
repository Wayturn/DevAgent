from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Literal


CommandName = Literal["explain", "fix", "gen-api"]


@dataclass(slots=True)
class CommandRequest:
    command: CommandName
    target_path: Path
    goal: str | None = None
    output_path: Path | None = None
    trace: bool = False


@dataclass(slots=True)
class PromptPackage:
    system_prompt: str
    user_prompt: str


@dataclass(slots=True)
class TraceStep:
    stage: str
    action: str
    observation: str


@dataclass(slots=True)
class AgentResult:
    command: CommandName
    target_path: Path
    content: str
    trace_steps: list[TraceStep] = field(default_factory=list)
