from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


class ConfigError(ValueError):
    """Raised when required application configuration is missing."""


def _parse_dotenv(env_file: Path) -> dict[str, str]:
    if not env_file.exists():
        return {}

    values: dict[str, str] = {}
    for raw_line in env_file.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue

        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key:
            values[key] = value

    return values


@dataclass(slots=True)
class AppConfig:
    openai_api_key: str
    openai_model: str = "gpt-4.1-mini"

    @classmethod
    def from_env(
        cls,
        env: dict[str, str] | None = None,
        env_file: Path | None = None,
    ) -> "AppConfig":
        runtime_env = env or dict(os.environ)
        dotenv_path = env_file or (Path.cwd() / ".env")
        dotenv_values = _parse_dotenv(dotenv_path)

        api_key = runtime_env.get("OPENAI_API_KEY", "").strip() or dotenv_values.get("OPENAI_API_KEY", "").strip()
        if not api_key:
            raise ConfigError(
                "缺少 OPENAI_API_KEY 設定。\n"
                "你可以用兩種方式提供：\n"
                "1. 在目前的 PowerShell 視窗設定：\n"
                '$env:OPENAI_API_KEY="你的 OpenAI API Key"\n'
                '$env:OPENAI_MODEL="gpt-4.1-mini"\n'
                "2. 在專案根目錄建立 .env 檔案：\n"
                "OPENAI_API_KEY=你的 OpenAI API Key\n"
                "OPENAI_MODEL=gpt-4.1-mini\n"
                "設定完成後，再重新執行 dev-agent 指令。"
            )

        model = runtime_env.get("OPENAI_MODEL", "").strip() or dotenv_values.get("OPENAI_MODEL", "").strip() or "gpt-4.1-mini"
        return cls(openai_api_key=api_key, openai_model=model)
