"""HTTP request bodies for chat / thread endpoints."""

from __future__ import annotations

from pydantic import BaseModel, Field, HttpUrl, field_validator, model_validator


class CreateThreadRequest(BaseModel):
    """Payload for ``POST /threads`` — opens a collaborative thread."""

    title: str = Field(
        ...,
        min_length=1,
        max_length=200,
        description="Title shown in clients and admin tools.",
    )
    participant_user_ids: list[str] = Field(
        ...,
        min_length=1,
        max_length=64,
        description="External user ids that may post user-role messages.",
    )

    @field_validator("participant_user_ids")
    @classmethod
    def normalize_participants(cls, value: list[str]) -> list[str]:
        cleaned = [p.strip() for p in value]
        if any(not p for p in cleaned):
            raise ValueError("participant_user_ids must be non-empty strings.")
        if len(set(cleaned)) != len(cleaned):
            raise ValueError("participant_user_ids must be unique.")
        return cleaned


class MessageAttachment(BaseModel):
    """Reference to a user-supplied file reachable at a public or signed URL."""

    filename: str = Field(..., min_length=1, max_length=255)
    media_type: str = Field(
        default="application/octet-stream",
        max_length=128,
    )
    url: HttpUrl = Field(
        ...,
        description="HTTPS (or HTTP) URL to fetch the attachment bytes, e.g. a public object or signed link.",
    )


class PostMessageRequest(BaseModel):
    """Payload for ``POST /threads/{thread_id}/messages`` — appends a user-authored line."""

    author_user_id: str = Field(
        ...,
        min_length=1,
        max_length=128,
        description="Must match one of the thread's participant_user_ids.",
    )
    text: str = Field(
        ...,
        min_length=1,
        max_length=16_000,
        description="User-authored message body.",
    )
    request_llm_reply: bool = Field(
        default=False,
        description="When true, runs the LLM after persisting this user message and appends the assistant turn.",
    )
    attachments: list[MessageAttachment] = Field(
        default_factory=list,
        description="Optional files included with this user turn.",
    )

    @field_validator("author_user_id")
    @classmethod
    def strip_author(cls, v: str) -> str:
        s = v.strip()
        if not s:
            raise ValueError("author_user_id must be non-empty.")
        return s

    @model_validator(mode="after")
    def attachments_require_llm(self) -> PostMessageRequest:
        if self.attachments and not self.request_llm_reply:
            raise ValueError("attachments require request_llm_reply to be true")
        return self
