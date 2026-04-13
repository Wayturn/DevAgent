import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from dev_agent_cli.models import CommandRequest, PromptPackage
from dev_agent_cli.orchestrator import AgentOrchestrator
from dev_agent_cli.tools import FileTool


class FakePromptRegistry:
    def build(self, request: CommandRequest, file_content: str) -> PromptPackage:
        return PromptPackage(
            system_prompt="system",
            user_prompt=f"command={request.command};content={file_content}",
        )


class FakeLlmClient:
    def generate(self, prompt: PromptPackage) -> str:
        return f"LLM::{prompt.user_prompt}"


class OrchestratorTests(unittest.TestCase):
    def test_orchestrator_reads_file_and_returns_content(self) -> None:
        with TemporaryDirectory() as temp_dir:
            target = Path(temp_dir) / "service.py"
            target.write_text("print('hello')", encoding="utf-8")

            orchestrator = AgentOrchestrator(
                file_tool=FileTool(),
                prompt_registry=FakePromptRegistry(),
                llm_client=FakeLlmClient(),
            )

            result = orchestrator.run(
                CommandRequest(
                    command="explain",
                    target_path=target,
                    goal=None,
                    output_path=None,
                    trace=True,
                )
            )

            self.assertIn("command=explain", result.content)
            self.assertEqual(len(result.trace_steps), 3)

    def test_orchestrator_writes_output_when_requested(self) -> None:
        with TemporaryDirectory() as temp_dir:
            target = Path(temp_dir) / "controller.py"
            output = Path(temp_dir) / "out" / "result.md"
            target.write_text("return ok", encoding="utf-8")

            orchestrator = AgentOrchestrator(
                file_tool=FileTool(),
                prompt_registry=FakePromptRegistry(),
                llm_client=FakeLlmClient(),
            )

            orchestrator.run(
                CommandRequest(
                    command="fix",
                    target_path=target,
                    goal="Reduce duplication",
                    output_path=output,
                    trace=False,
                )
            )

            self.assertTrue(output.exists())
            self.assertIn("command=fix", output.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
