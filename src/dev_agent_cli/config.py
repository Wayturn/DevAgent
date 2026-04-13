from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(slots=True)
class AppConfig:
    openai_api_key: str
    openai_model: str = "gpt-4.1-mini"

    @classmethod
    def from_env(cls) -> "AppConfig":
        api_key = os.getenv("OPENAI_API_KEY", "").strip()
        if not api_key:
            raise ValueError("Missing OPENAI_API_KEY environment variable.")

        model = os.getenv("OPENAI_MODEL", "gpt-4.1-mini").strip() or "gpt-4.1-mini"
        return cls(openai_api_key=api_key, openai_model=model)
