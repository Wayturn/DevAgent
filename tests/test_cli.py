import unittest
from io import StringIO
from pathlib import Path
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
        self.assertIn("缺少 OPENAI_API_KEY 環境變數", message)
        self.assertIn('$env:OPENAI_API_KEY="你的 OpenAI API Key"', message)

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
