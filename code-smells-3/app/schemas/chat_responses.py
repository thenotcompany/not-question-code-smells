"""HTTP response bodies for chat / thread endpoints."""

from __future__ import annotations

from datetime import datetime
from typing import Literal, Optional

from pydantic import BaseModel, Field

from app.models.chat import ChatThread, ThreadMessage


class ChatMessageResponse(BaseModel):
    """One persisted message in a thread, as exposed on the wire."""

    role: Literal["user", "assistant"]
    author_user_id: Optional[str] = Field(
        default=None,
        description="Human author for user turns; null for assistant turns.",
    )
    text: str
    created_at: datetime = Field(description="UTC instant the message was stored.")

    @classmethod
    def from_thread_message(cls, message: ThreadMessage) -> ChatMessageResponse:
        return cls(
            role=message.role,
            author_user_id=message.author_user_id,
            text=message.text,
            created_at=message.created_at,
        )


class ThreadCreatedResponse(BaseModel):
    """Returned after a thread is created."""

    thread_id: str = Field(description="Mongo ObjectId string for the new thread.")
    title: str
    participant_user_ids: list[str]
    message_count: int = Field(ge=0, description="Number of messages (starts at 0).")

    @classmethod
    def from_chat_thread(cls, thread: ChatThread) -> ThreadCreatedResponse:
        return cls(
            thread_id=str(thread.id),
            title=thread.title,
            participant_user_ids=list(thread.participant_user_ids),
            message_count=len(thread.messages),
        )


class ThreadDetailResponse(BaseModel):
    """Full thread including ordered transcript and collaborator ids."""

    thread_id: str
    title: str
    participant_user_ids: list[str]
    messages: list[ChatMessageResponse]

    @classmethod
    def from_chat_thread(cls, thread: ChatThread) -> ThreadDetailResponse:
        return cls(
            thread_id=str(thread.id),
            title=thread.title,
            participant_user_ids=list(thread.participant_user_ids),
            messages=[ChatMessageResponse.from_thread_message(m) for m in thread.messages],
        )


class PostMessageResponse(BaseModel):
    """Returned after posting a user message (and optionally an assistant follow-up)."""

    thread_id: str
    message_count: int = Field(ge=0)
    assistant_reply_appended: bool = Field(
        description="True when ``request_llm_reply`` was set on the request and an assistant message was stored.",
    )

    @classmethod
    def from_result(
        cls,
        thread: ChatThread,
        *,
        assistant_reply_appended: bool,
    ) -> PostMessageResponse:
        return cls(
            thread_id=str(thread.id),
            message_count=len(thread.messages),
            assistant_reply_appended=assistant_reply_appended,
        )
