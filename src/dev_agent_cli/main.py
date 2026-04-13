from __future__ import annotations

from dev_agent_cli.cli import parse_request
from dev_agent_cli.config import AppConfig
from dev_agent_cli.llm import OpenAILlmClient
from dev_agent_cli.orchestrator import AgentOrchestrator
from dev_agent_cli.prompts import PromptRegistry
from dev_agent_cli.tools import FileTool


def _format_trace(result) -> str:
    lines = ["", "--- TRACE ---"]
    for index, step in enumerate(result.trace_steps, start=1):
        lines.append(f"{index}. [{step.stage}] {step.action}")
        lines.append(f"   -> {step.observation}")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> None:
    request = parse_request(argv)
    config = AppConfig.from_env()

    orchestrator = AgentOrchestrator(
        file_tool=FileTool(),
        prompt_registry=PromptRegistry(),
        llm_client=OpenAILlmClient(config),
    )

    result = orchestrator.run(request)
    print(result.content)

    if request.trace:
        print(_format_trace(result))


if __name__ == "__main__":
    main()
