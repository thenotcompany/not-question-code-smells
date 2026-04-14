from __future__ import annotations

import base64
from collections.abc import Sequence

from openai import OpenAI

from app.domain.llm.base import LLMProvider
from app.domain.llm.file_part import FilePart
from app.settings import settings


class OpenAIProvider(LLMProvider):
    """OpenAI-backed chat completion adapter."""

    def __init__(self) -> None:
        self._model = settings.openai_chat_model
        self._client: OpenAI | None = None
        key = settings.openai_api_key
        if key:
            self._client = OpenAI(
                api_key=key,
                base_url=settings.openai_base_url or None,
            )

    def complete(
        self,
        prompt: str,
        files: Sequence[FilePart] = (),
        *,
        model: str | None = None,
    ) -> str:
        use_model = model or self._model
        if self._client is None:
            out = f"[offline-model] {prompt[:80]}"
            for f in files:
                out += f" |file:{f.filename}|{f.media_type}|{len(f.data)}b"
            return out

        content: list[dict[str, object]] = [{"type": "text", "text": prompt}]
        for f in files:
            if f.media_type.startswith("image/"):
                b64 = base64.standard_b64encode(f.data).decode("ascii")
                content.append(
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:{f.media_type};base64,{b64}"},
                    },
                )
            else:
                content.append(
                    {
                        "type": "text",
                        "text": (
                            f"(Attachment: {f.filename}, {f.media_type}, "
                            f"{len(f.data)} bytes)"
                        ),
                    },
                )

        response = self._client.chat.completions.create(
            model=use_model,
            messages=[{"role": "user", "content": content}],
        )
        choice = response.choices[0]
        text = choice.message.content
        return (text or "").strip()
