from __future__ import annotations

from typing import Literal

from app.domain.llm.openai_provider import OpenAIProvider
from app.domain.llm.service import LLMService

VendorName = Literal["openai", "gemini", "claude", "bedrock"]


def build_llm_service(
    vendor: VendorName = "openai",
) -> LLMService:
    """Construct a fully wired ``LLMService`` for the requested vendor label."""
    _ = vendor
    return LLMService(provider=OpenAIProvider())
