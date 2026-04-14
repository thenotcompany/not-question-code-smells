from __future__ import annotations

from datetime import datetime, timezone
from typing import Literal, Optional

from beanie import Document
from pydantic import BaseModel, Field, model_validator


class ThreadMessage(BaseModel):
    """
    One transcript row stored inside ``ChatThread.messages`` (embedded list).

    * ``role`` ``user`` — human collaborator; ``author_user_id`` must be set.
    * ``role`` ``assistant`` — model turn; ``author_user_id`` must be unset.
    """

    role: Literal["user", "assistant"]
    author_user_id: Optional[str] = Field(
        default=None,
        description="External user id for human messages; omitted for assistant turns.",
    )
    text: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    @model_validator(mode="after")
    def validate_author_for_role(self) -> ThreadMessage:
        if self.role == "user":
            if not self.author_user_id:
                raise ValueError("user messages require author_user_id")
        elif self.author_user_id is not None:
            raise ValueError("assistant messages must not set author_user_id")
        return self


class ChatThread(Document):
    """
    This is a model for a chat thread.
    It contains a title, a list of participant user ids, and a list of messages.
    """

    title: str
    participant_user_ids: list[str] = Field(
        default_factory=list,
        description="External user ids allowed to post user-role messages.",
    )
    messages: list[ThreadMessage] = Field(default_factory=list)

    class Settings:
        name = "chat_threads"
