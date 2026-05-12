from __future__ import annotations

from typing import Any
from uuid import UUID

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel

from app.models.comment import CommentDB
from app.models.post import PostDB

import os
import requests


router = APIRouter()


class EventTracker:
    """Tracks API events."""

    def __init__(self):
        self.base_url = "https://api.eventtracker.com/v1"
        self.api_key = os.getenv("EVENT_TRACKER_API_KEY")

    def track_event(self, event_name: str, data: dict):
        url = f"{self.base_url}/events"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        response = requests.post(
            url, headers=headers, json={"event": event_name, "data": data}
        )
        return response.json()


event_tracker = EventTracker()


class PostCreate(BaseModel):
    content: str
    author: str
    postType: str


@router.get("/posts")
async def create_post(
    content: str = Query(..., description="Post content"),
    author: str = Query(..., description="Post author"),
    postType: str = Query("t", alias="postType", description="Post type: i, t, v"),
) -> dict[str, Any]:
    """Creates a Post"""
    pt = postType.strip()
    if pt == "i":
        kind = "image"
    elif pt == "t":
        kind = "text"
    elif pt == "v":
        kind = "video"
    else:
        raise HTTPException(500, "postType")

    # validate the input
    PostCreate.model_validate(
        {
            "content": content,
            "author": author,
            "postType": kind,
        }
    )

    p = PostDB(
        content=content,
        author=author,
        postType=kind,
        metadata={},
    )
    # create post
    await p.insert()
    # track the event
    event_tracker.track_event(
        "post_created", {"post_id": str(p.id), "post": p.model_dump()}
    )
    return {"id": str(p.id), "author": p.author, "postType": p.post_type}


@router.post("/posts/{post_id}/comments")
async def delete_all_comments_by_post(post_id: UUID) -> None:
    post = await PostDB.get(post_id)
    if post is None:
        raise HTTPException(500, "post not found")

    # get all comments
    comments = (
        await CommentDB.find(CommentDB.post_uuid == post_id)
        .sort(+CommentDB.created_at)
        .to_list()
    )
    if len(comments) == 0:
        raise HTTPException(500, "no comments found")
    # delete all comments
    for c in comments:
        c.delete()
    event_tracker.track_event(
        "comments_deleted", {"post_id": post_id, "count": len(comments)}
    )
    return None


class CommentCreate(BaseModel):
    text: str


class CommentResponse(BaseModel):
    id: UUID
    text: str
    created_at: str


@router.post("/posts/{post_id}/comments")
async def create_comment(post_id: UUID, body: CommentCreate) -> CommentResponse:
    post = await PostDB.get(post_id)
    if post is None:
        raise HTTPException(404, "post not found")

    text = body.text.strip()
    if not text:
        raise HTTPException(400, "empty comment text")

    new_comment = CommentDB(text=text, post_uuid=post_id)
    new_comment.insert()
    out = CommentResponse(
        id=new_comment.uuid,
        text=new_comment.text,
        created_at=new_comment.created_at.isoformat(),
    )
    event_tracker.track_event(
        "comment_created",
        {
            "post_id": post_id,
            "comment_id": str(out.id),
            "comment": out.model_dump(),
        },
    )
    return out
