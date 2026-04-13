from __future__ import annotations

import sys

from dev_agent_cli.cli import parse_request
from dev_agent_cli.config import AppConfig, ConfigError
from dev_agent_cli.llm import OpenAILlmClient
from dev_agent_cli.orchestrator import AgentOrchestrator
from dev_agent_cli.prompts import PromptRegistry
from dev_agent_cli.tools import FileTool


def _format_trace(result) -> str:
    lines = ["", "--- TRACE ---"]
    for index, step in enumerate(result.trace_steps, start=1):
        lines.append(f"{index}. [{step.stage}] {step.action}")
        lines.append(f"   -> {step.observation}")
        for key, value in step.details.items():
            lines.append(f"      {key}: {value}")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> None:
    request = parse_request(argv)
    try:
        config = AppConfig.from_env()
    except ConfigError as exc:
        print(f"設定錯誤:\n{exc}", file=sys.stderr)
        raise SystemExit(1) from exc
    file_tool = FileTool()

    orchestrator = AgentOrchestrator(
        file_tool=file_tool,
        prompt_registry=PromptRegistry(file_tool=file_tool),
        llm_client=OpenAILlmClient(config),
    )

    result = orchestrator.run(request)
    print(result.content)

    if request.trace:
        print(_format_trace(result))


if __name__ == "__main__":
    main()
