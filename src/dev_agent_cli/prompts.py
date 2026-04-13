from __future__ import annotations

from dev_agent_cli.models import CommandRequest, PromptPackage


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

    def build(self, request: CommandRequest, file_content: str) -> PromptPackage:
        command_handlers = {
            "explain": self._build_explain_prompt,
            "fix": self._build_fix_prompt,
            "gen-api": self._build_gen_api_prompt,
        }
        return command_handlers[request.command](request, file_content)

    def _build_explain_prompt(self, request: CommandRequest, file_content: str) -> PromptPackage:
        user_prompt = f"""Task: Explain this file in practical backend engineering language.

Target file: {request.target_path}
User goal: {request.goal or "Understand what the code does and how it is structured."}

Please respond with:
1. Purpose
2. Core flow
3. Important implementation details
4. Risks or improvement points

File content:
```text
{file_content}
```"""
        return PromptPackage(system_prompt=BASE_SYSTEM_PROMPT, user_prompt=user_prompt)

    def _build_fix_prompt(self, request: CommandRequest, file_content: str) -> PromptPackage:
        user_prompt = f"""Task: Review this file and propose a practical fix.

Target file: {request.target_path}
User goal: {request.goal or "Identify problems and propose a safe, maintainable fix."}

Please respond with:
1. Problem summary
2. Root cause
3. Recommended fix
4. Example revised code
5. Trade-offs or follow-up checks

File content:
```text
{file_content}
```"""
        return PromptPackage(system_prompt=BASE_SYSTEM_PROMPT, user_prompt=user_prompt)

    def _build_gen_api_prompt(self, request: CommandRequest, file_content: str) -> PromptPackage:
        user_prompt = f"""Task: Generate a practical backend API design from this input.

Target file: {request.target_path}
User goal: {request.goal or "Design a clean RESTful API and the minimum backend structure needed."}

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
        return PromptPackage(system_prompt=BASE_SYSTEM_PROMPT, user_prompt=user_prompt)
