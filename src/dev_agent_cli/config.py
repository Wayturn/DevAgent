from __future__ import annotations

import os
from dataclasses import dataclass


class ConfigError(ValueError):
    """Raised when required application configuration is missing."""


@dataclass(slots=True)
class AppConfig:
    openai_api_key: str
    openai_model: str = "gpt-4.1-mini"

    @classmethod
    def from_env(cls) -> "AppConfig":
        api_key = os.getenv("OPENAI_API_KEY", "").strip()
        if not api_key:
            raise ConfigError(
                "缺少 OPENAI_API_KEY 環境變數。\n"
                "請先在目前的 PowerShell 視窗設定：\n"
                '$env:OPENAI_API_KEY="你的 OpenAI API Key"\n'
                '$env:OPENAI_MODEL="gpt-4.1-mini"\n'
                "設定完成後，再重新執行 dev-agent 指令。"
            )

        model = os.getenv("OPENAI_MODEL", "gpt-4.1-mini").strip() or "gpt-4.1-mini"
        return cls(openai_api_key=api_key, openai_model=model)
