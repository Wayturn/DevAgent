import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from dev_agent_cli.models import CommandRequest, PromptPackage
from dev_agent_cli.orchestrator import AgentOrchestrator
from dev_agent_cli.prompts import PromptRegistry
from dev_agent_cli.tools import FileTool


class FakePromptRegistry:
    def build(self, request: CommandRequest, file_content: str) -> PromptPackage:
        return PromptPackage(
            template_name="fake_template",
            system_prompt="system",
            user_prompt=f"command={request.command};content={file_content}",
        )


class FakeLlmClient:
    model_name = "fake-model"

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
            self.assertEqual(len(result.trace_steps), 4)
            self.assertEqual(result.trace_steps[0].details["target_extension"], ".py")
            self.assertEqual(result.trace_steps[2].details["prompt_template"], "fake_template")
            self.assertEqual(result.trace_steps[3].details["model_name"], "fake-model")

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

    def test_fix_prompt_uses_stable_markdown_sections(self) -> None:
        with TemporaryDirectory() as temp_dir:
            target = Path(temp_dir) / "service.py"
            target.write_text("def run():\n    return True\n", encoding="utf-8")

            prompt = PromptRegistry(file_tool=FileTool()).build(
                CommandRequest(command="fix", target_path=target),
                target.read_text(encoding="utf-8"),
            )

            self.assertEqual(prompt.template_name, "fix_v2_structured_markdown")
            self.assertIn("## Problem Summary", prompt.user_prompt)
            self.assertIn("## Root Cause", prompt.user_prompt)
            self.assertIn("## Recommended Fix", prompt.user_prompt)
            self.assertIn("## Revised Code", prompt.user_prompt)
            self.assertIn("## Trade-offs / Notes", prompt.user_prompt)

    def test_file_tool_directory_summary_lists_project_files(self) -> None:
        with TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            (root / "app").mkdir()
            (root / "app" / "service.py").write_text("pass", encoding="utf-8")
            (root / "README.md").write_text("# demo", encoding="utf-8")

            summary = FileTool().read_directory_summary(root)

            self.assertIn("Directory summary for:", summary)
            self.assertIn("app\\service.py", summary)
            self.assertIn("README.md", summary)


if __name__ == "__main__":
    unittest.main()
