from __future__ import annotations

import urllib.request
from collections.abc import Sequence

from app.domain.llm.base import LLMProvider, Vendor
from app.domain.llm.file_part import FilePart
from app.domain.llm.openai_provider import OpenAIProvider


def _read_bytes_from_http_url(url: str) -> bytes:
    request = urllib.request.Request(
        url,
        headers={"User-Agent": "code-smells-3/0.1"},
        method="GET",
    )
    with urllib.request.urlopen(request, timeout=120) as response:
        return response.read()


class LLMService:
    """
    Vendor-neutral orchestration entrypoint.
    Designed so we can swap with future implementations.
    """

    def __init__(self, provider: LLMProvider | None = None) -> None:
        self._provider = provider or OpenAIProvider()

    def generate(
        self,
        prompt: str,
        files: Sequence[FilePart] = (),
        *,
        preferred_vendor: Vendor = "openai",
        model: str | None = None,
    ) -> str:
        _ = preferred_vendor
        return self._provider.complete(prompt, files, model=model)

    def generate_from_user_turn(
        self,
        prompt: str,
        attachment_specs: Sequence[tuple[str, str, str]] = (),
        *,
        preferred_vendor: Vendor = "openai",
        model: str | None = None,
    ) -> str:
        files = tuple(
            FilePart(
                filename=fn,
                media_type=mt,
                data=_read_bytes_from_http_url(url),
            )
            for fn, mt, url in attachment_specs
        )
        return self.generate(
            prompt,
            files,
            preferred_vendor=preferred_vendor,
            model=model,
        )
