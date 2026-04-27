from typing import Any

from beanie import Document
from pydantic import ConfigDict, Field


class Post(Document):
    model_config = ConfigDict(populate_by_name=True)

    content: str
    author: str
    # image, text, video
    post_type: str = Field(alias="postType")
    metadata: dict[str, Any] = Field(default_factory=dict)

    class Settings:
        name = "posts"
