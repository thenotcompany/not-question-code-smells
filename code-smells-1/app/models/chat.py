from __future__ import annotations

from beanie import Document
from pydantic import BaseModel, ConfigDict, Field


class ChatMessage(BaseModel):
    """Chat message model.
    
    This model is used to store the chat message document in the database.
    """

    model_config = ConfigDict(populate_by_name=True)

    id: str
    from_user: str = Field(alias="fromUser")
    body: str


class ChatThread(Document):
    """Main chat thread document.
    
    This model is used to store the main chat thread document in the database.
    """

    model_config = ConfigDict(populate_by_name=True)

    participant_a: str = Field(alias="participantA")
    participant_b: str = Field(alias="participantB")
    messages: list[ChatMessage] = Field(default_factory=list)

    class Settings:
        name = "chat_threads"
