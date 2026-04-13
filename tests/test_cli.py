import unittest
from pathlib import Path

from dev_agent_cli.cli import parse_request


class ParseRequestTests(unittest.TestCase):
    def test_parse_request_explain(self) -> None:
        request = parse_request(["explain", "demo.py", "--goal", "Explain code", "--trace"])

        self.assertEqual(request.command, "explain")
        self.assertEqual(request.target_path, Path("demo.py"))
        self.assertEqual(request.goal, "Explain code")
        self.assertTrue(request.trace)


if __name__ == "__main__":
    unittest.main()
