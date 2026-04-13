from __future__ import annotations

from pathlib import Path

from dev_agent_cli.models import CommandRequest, PromptPackage
from dev_agent_cli.tools import FileTool


BASE_SYSTEM_PROMPT = """You are a practical AI application engineer assistant.
You operate inside a controllable developer agent harness.
Always optimize for:
- clear reasoning
- practical backend engineering value
- simple, explainable solutions
- structured output that a developer can review quickly

Do not be vague. Do not over-engineer.
When suggesting changes, explain trade-offs briefly.
"""


class PromptRegistry:
    """Maps CLI commands to explicit prompt templates."""

    def __init__(self, file_tool: FileTool | None = None) -> None:
        self._file_tool = file_tool or FileTool()

    def build(self, request: CommandRequest, file_content: str) -> PromptPackage:
        command_handlers = {
            "explain": self._build_explain_prompt,
            "fix": self._build_fix_prompt,
            "gen-api": self._build_gen_api_prompt,
        }
        return command_handlers[request.command](request, file_content)

    def _build_repo_context(self, target_path: Path) -> str:
        parent_dir = target_path.parent
        try:
            return self._file_tool.read_directory_summary(parent_dir)
        except (FileNotFoundError, NotADirectoryError, PermissionError):
            return f"Directory summary unavailable for: {parent_dir}"

    def _build_explain_prompt(self, request: CommandRequest, file_content: str) -> PromptPackage:
        repo_context = self._build_repo_context(request.target_path)
        user_prompt = f"""Task: Explain this file in practical backend engineering language.

Target file: {request.target_path}
User goal: {request.goal or "Understand what the code does and how it is structured."}
Target directory context:
{repo_context}

Please respond with:
1. Purpose
2. Core flow
3. Important implementation details
4. Risks or improvement points

File content:
```text
{file_content}
```"""
        return PromptPackage(
            template_name="explain_v1",
            system_prompt=BASE_SYSTEM_PROMPT,
            user_prompt=user_prompt,
        )

    def _build_fix_prompt(self, request: CommandRequest, file_content: str) -> PromptPackage:
        repo_context = self._build_repo_context(request.target_path)
        user_prompt = f"""Task: Review this file and propose a practical fix.

Target file: {request.target_path}
User goal: {request.goal or "Identify problems and propose a safe, maintainable fix."}
Target directory context:
{repo_context}

Respond using exactly these stable markdown headings:
## Problem Summary
## Root Cause
## Recommended Fix
## Revised Code
## Trade-offs / Notes

Requirements:
- Keep each section present even if the answer is short.
- In `Revised Code`, provide one fenced code block.
- Focus on practical, minimal, backend-friendly fixes.
- Keep the output consistent and easy to parse.

File content:
```text
{file_content}
```"""
        return PromptPackage(
            template_name="fix_v2_structured_markdown",
            system_prompt=BASE_SYSTEM_PROMPT,
            user_prompt=user_prompt,
        )

    def _build_gen_api_prompt(self, request: CommandRequest, file_content: str) -> PromptPackage:
        repo_context = self._build_repo_context(request.target_path)
        user_prompt = f"""Task: Generate a practical backend API design from this input.

Target file: {request.target_path}
User goal: {request.goal or "Design a clean RESTful API and the minimum backend structure needed."}
Target directory context:
{repo_context}

Please respond with:
1. API purpose
2. Endpoint design
3. Request and response models
4. Validation rules
5. Suggested service and repository responsibilities

If the input looks like requirements, infer the API design from it.
If the input looks like code, derive the API design from the code context.

File content:
```text
{file_content}
```"""
        return PromptPackage(
            template_name="gen_api_v1",
            system_prompt=BASE_SYSTEM_PROMPT,
            user_prompt=user_prompt,
        )
