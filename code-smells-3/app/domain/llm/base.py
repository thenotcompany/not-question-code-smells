from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Sequence
from typing import Literal

from app.domain.llm.file_part import FilePart

Vendor = Literal["openai", "gemini", "claude", "cohere", "mistral"]


class LLMProvider(ABC):
    """Pluggable provider surface for heterogeneous model vendors."""

    @abstractmethod
    def complete(
        self,
        prompt: str,
        files: Sequence[FilePart] = (),
        *,
        model: str | None = None,
    ) -> str:
        raise NotImplementedError
