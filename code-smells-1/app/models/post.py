from typing import Any
from uuid import UUID, uuid4

from beanie import Document
from pydantic import ConfigDict, Field


class PostDB(Document):
    model_config = ConfigDict(populate_by_name=True)

    uuid: UUID = Field(default_factory=uuid4)

    content: str
    author: str
    # image, text, video
    post_type: str = Field(alias="postType")
    metadata: dict[str, Any] = Field(default_factory=dict)

    class Settings:
        name = "posts"
