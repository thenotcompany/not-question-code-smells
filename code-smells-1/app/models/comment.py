from datetime import datetime, timezone
from uuid import UUID, uuid4

from beanie import Document
from pydantic import ConfigDict, Field


class CommentDB(Document):
    """Comment on a post (stored in its own collection; N comments per post)."""

    uuid: UUID = Field(default_factory=uuid4)
    model_config = ConfigDict(populate_by_name=True)


    text: str
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        alias="createdAt",
    )
    post_uuid: UUID = Field(alias="postUuid")

    class Settings:
        name = "comments"
