import unittest
from io import StringIO
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from dev_agent_cli.cli import parse_request
from dev_agent_cli.config import AppConfig, ConfigError
from dev_agent_cli.main import main


class ParseRequestTests(unittest.TestCase):
    def test_parse_request_explain(self) -> None:
        request = parse_request(["explain", "demo.py", "--goal", "Explain code", "--trace"])

        self.assertEqual(request.command, "explain")
        self.assertEqual(request.target_path, Path("demo.py"))
        self.assertEqual(request.goal, "Explain code")
        self.assertTrue(request.trace)

    def test_app_config_missing_api_key_shows_friendly_message(self) -> None:
        with patch.dict("os.environ", {}, clear=True):
            with self.assertRaises(ConfigError) as context:
                AppConfig.from_env()

        message = str(context.exception)
        self.assertIn("缺少 OPENAI_API_KEY 設定", message)
        self.assertIn("在專案根目錄建立 .env 檔案", message)

    def test_app_config_loads_from_dotenv(self) -> None:
        with TemporaryDirectory() as temp_dir:
            env_file = Path(temp_dir) / ".env"
            env_file.write_text(
                "OPENAI_API_KEY=test-key\nOPENAI_MODEL=gpt-4.1\n",
                encoding="utf-8",
            )

            config = AppConfig.from_env(env={}, env_file=env_file)

        self.assertEqual(config.openai_api_key, "test-key")
        self.assertEqual(config.openai_model, "gpt-4.1")

    def test_environment_variables_override_dotenv(self) -> None:
        with TemporaryDirectory() as temp_dir:
            env_file = Path(temp_dir) / ".env"
            env_file.write_text(
                "OPENAI_API_KEY=file-key\nOPENAI_MODEL=file-model\n",
                encoding="utf-8",
            )

            config = AppConfig.from_env(
                env={"OPENAI_API_KEY": "env-key", "OPENAI_MODEL": "env-model"},
                env_file=env_file,
            )

        self.assertEqual(config.openai_api_key, "env-key")
        self.assertEqual(config.openai_model, "env-model")

    def test_main_exits_cleanly_when_api_key_is_missing(self) -> None:
        stderr = StringIO()

        with patch.dict("os.environ", {}, clear=True):
            with patch("sys.stderr", stderr):
                with self.assertRaises(SystemExit) as context:
                    main(["explain", "demo.py"])

        self.assertEqual(context.exception.code, 1)
        self.assertIn("設定錯誤", stderr.getvalue())
        self.assertIn("OPENAI_API_KEY", stderr.getvalue())


if __name__ == "__main__":
    unittest.main()
