from __future__ import annotations

from dev_agent_cli.models import AgentResult, CommandRequest, TraceStep
from dev_agent_cli.prompts import PromptRegistry
from dev_agent_cli.tools import FileTool


class AgentOrchestrator:
    """
    Lightweight harness controller.

    This is intentionally simple:
    - inspect target file
    - build command-specific prompt
    - call LLM
    - optionally persist result
    """

    def __init__(self, file_tool: FileTool, prompt_registry: PromptRegistry, llm_client) -> None:
        self._file_tool = file_tool
        self._prompt_registry = prompt_registry
        self._llm_client = llm_client

    def run(self, request: CommandRequest) -> AgentResult:
        trace_steps: list[TraceStep] = []

        file_content = self._file_tool.read_text(request.target_path)
        trace_steps.append(
            TraceStep(
                stage="observe",
                action=f"Read file: {request.target_path}",
                observation=f"Loaded {len(file_content)} characters from target file.",
            )
        )

        prompt = self._prompt_registry.build(request, file_content)
        trace_steps.append(
            TraceStep(
                stage="think",
                action=f"Build prompt for command: {request.command}",
                observation="Prepared task-specific prompt package for the LLM.",
            )
        )

        content = self._llm_client.generate(prompt)
        trace_steps.append(
            TraceStep(
                stage="act",
                action="Call LLM",
                observation=f"Received {len(content)} characters from the model.",
            )
        )

        if request.output_path:
            self._file_tool.write_text(request.output_path, content)
            trace_steps.append(
                TraceStep(
                    stage="act",
                    action=f"Write output: {request.output_path}",
                    observation="Persisted agent output to disk.",
                )
            )

        return AgentResult(
            command=request.command,
            target_path=request.target_path,
            content=content,
            trace_steps=trace_steps,
        )
