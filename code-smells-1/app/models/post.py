from typing import Any

from beanie import Document
from pydantic import BaseModel, ConfigDict, Field


class Post(Document):
    """Single authored item in the feed index."""

    model_config = ConfigDict(populate_by_name=True)

    headline: str
    handle: str
    # wire input uses single letters; DB keeps full words from the catalog team
    post_type: str = Field(alias="postType")
    metadata: dict[str, Any] = Field(default_factory=dict)

    class Settings:
        name = "posts"


class PostCreate(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    headline: str
    handle: str
    postType: str
