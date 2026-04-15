from __future__ import annotations

from typing import Optional

from beanie import Document
from pydantic import BaseModel, ConfigDict, Field


class ChatMessage(BaseModel):
    """Chat message model.
    
    This model is used to store the chat message document in the database.
    """

    model_config = ConfigDict(populate_by_name=True)

    message_id: str
    from_user: str = Field(alias="fromUser")
    body: str


class ChatThread(Document):
    """Main chat thread document.
    
    This model is used to store the main chat thread document in the database.
    """

    model_config = ConfigDict(populate_by_name=True)

    peer_low: str = Field(alias="participantA")
    peer_high: str = Field(alias="participantB")
    messages: list[ChatMessage] = Field(default_factory=list)

    class Settings:
        name = "chat_threads"


class OpenChatBody(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    participantA: str
    participantB: str


def sort_peer_pair(a: str, b: str) -> tuple[str, str]:
    x, y = (a.strip(), b.strip())
    return (x, y) if x <= y else (y, x)
