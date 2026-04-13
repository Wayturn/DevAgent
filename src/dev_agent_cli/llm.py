from __future__ import annotations

from openai import OpenAI

from dev_agent_cli.config import AppConfig
from dev_agent_cli.models import PromptPackage


class OpenAILlmClient:
    """Thin wrapper over the OpenAI Responses API."""

    def __init__(self, config: AppConfig) -> None:
        self._client = OpenAI(api_key=config.openai_api_key)
        self._model = config.openai_model

    def generate(self, prompt: PromptPackage) -> str:
        response = self._client.responses.create(
            model=self._model,
            input=[
                {"role": "system", "content": prompt.system_prompt},
                {"role": "user", "content": prompt.user_prompt},
            ],
        )
        return response.output_text
