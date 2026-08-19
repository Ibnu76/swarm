"""LLM provider abstraction."""

from __future__ import annotations
from dataclasses import dataclass


@dataclass
class Provider:
    """Configuration for an LLM provider."""

    name: str
    api_key: str | None = None
    base_url: str | None = None
    default_model: str | None = None
    max_retries: int = 3
    timeout: int = 60

    def __post_init__(self):
        # Set default base URLs
        defaults = {
            "openai": "https://api.openai.com/v1",
            "anthropic": "https://api.anthropic.com/v1",
            "ollama": "http://localhost:11434",
            "deepseek": "https://api.deepseek.com/v1",
            "together": "https://api.together.xyz/v1",
        }
        if not self.base_url and self.name in defaults:
            self.base_url = defaults[self.name]
