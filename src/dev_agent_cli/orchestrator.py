from __future__ import annotations

from pathlib import Path

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
        model_name = getattr(self._llm_client, "model_name", "unknown")
        target_extension = request.target_path.suffix or "(no extension)"
        target_directory = request.target_path.parent

        file_content = self._file_tool.read_text(request.target_path)
        trace_steps.append(
            TraceStep(
                stage="observe",
                action=f"Read file: {request.target_path}",
                observation=f"Loaded {len(file_content)} characters from target file.",
                details={
                    "command": request.command,
                    "target_path": str(request.target_path),
                    "target_extension": target_extension,
                    "target_directory": str(target_directory),
                    "input_chars": str(len(file_content)),
                },
            )
        )

        directory_summary = self._safe_directory_summary(target_directory)
        trace_steps.append(
            TraceStep(
                stage="observe",
                action=f"Inspect directory: {target_directory}",
                observation="Collected lightweight directory summary for repo context.",
                details={
                    "directory_summary_chars": str(len(directory_summary)),
                    "directory_summary_preview": directory_summary[:120].replace("\n", " "),
                },
            )
        )

        prompt = self._prompt_registry.build(request, file_content)
        trace_steps.append(
            TraceStep(
                stage="think",
                action=f"Build prompt for command: {request.command}",
                observation="Prepared task-specific prompt package for the LLM.",
                details={
                    "prompt_template": prompt.template_name,
                    "model_name": model_name,
                    "prompt_chars": str(len(prompt.system_prompt) + len(prompt.user_prompt)),
                },
            )
        )

        content = self._llm_client.generate(prompt)
        trace_steps.append(
            TraceStep(
                stage="act",
                action="Call LLM",
                observation=f"Received {len(content)} characters from the model.",
                details={
                    "model_name": model_name,
                    "output_chars": str(len(content)),
                    "write_back_requested": str(bool(request.output_path)).lower(),
                },
            )
        )

        if request.output_path:
            self._file_tool.write_text(request.output_path, content)
            trace_steps.append(
                TraceStep(
                    stage="act",
                    action=f"Write output: {request.output_path}",
                    observation="Persisted agent output to disk.",
                    details={
                        "output_path": str(request.output_path),
                        "output_chars": str(len(content)),
                    },
                )
            )

        return AgentResult(
            command=request.command,
            target_path=request.target_path,
            content=content,
            trace_steps=trace_steps,
        )

    def _safe_directory_summary(self, directory: Path) -> str:
        try:
            return self._file_tool.read_directory_summary(directory)
        except (FileNotFoundError, NotADirectoryError, PermissionError):
            return f"Directory summary unavailable for: {directory}"
