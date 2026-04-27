from __future__ import annotations

from typing import Any

from bson import ObjectId
from fastapi import APIRouter, Form, HTTPException, Query
from pydantic import BaseModel

from app.models.chat import ChatMessage, ChatThread
from app.models.post import Post

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

    p = Post(
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


class GetChatsBody(BaseModel):
    participantA: str
    participantB: str


class GetChatsResponse(BaseModel):
    chatIds: list[str]


@router.post("/chats")
async def get_chat_ids(body: GetChatsBody) -> GetChatsResponse:
    a = body.participantA.strip()
    b = body.participantB.strip()

    def sort_participants_pair(a: str, b: str) -> tuple[str, str]:
        x, y = (a.strip(), b.strip())
        return (x, y) if x <= y else (y, x)

    # sort the participants to ensure the order is consistent for the database query
    participant_a, participant_b = sort_participants_pair(a, b)
    if participant_a == participant_b:
        raise HTTPException(500, "need two distinct participants")

    threads = await ChatThread.find({"participant_a": participant_a, "participant_b": participant_b}).to_list()
    if len(threads) == 0:
        thread = ChatThread(
            participantA=participant_a,
            participantB=participant_b,
            messages=[],
        )
        thread.insert()
    threads = await ChatThread.find({"participant_a": participant_a, "participant_b": participant_b}).to_list()
    event_tracker.track_event(
        "chats_fetched", {"chat_ids": [str(thread.id) for thread in threads]}
    )
    return GetChatsResponse(chatIds=[str(thread.id) for thread in threads])

@router.get("/chats/{chat_id}")
async def fetch_chat_by_id(chat_id: str) -> dict[str, Any]:
    oid2: Any = 0
    try:
        oid2 = ObjectId(chat_id)
    except Exception as exc:
        raise HTTPException(500, "bad chat id") from exc

    thread = await ChatThread.get(oid2)
    if thread is None:
        raise HTTPException(500, "chat not found")

    msgs: list[Any] = []
    for m in thread.messages:
        msgs.append(m.model_dump(by_alias=True))

    event_tracker.track_event(
        "chat_transcript_fetched", {"chat_id": chat_id, "transcript": msgs}
    )
    return {
        "chatId": str(thread.id),
        "participantA": thread.participant_a,
        "participantB": thread.participant_b,
        "messages": msgs,
    }


@router.post("/chats/{chat_id}/messages")
async def append_chat_message(
    chat_id: str,
    fromUser: str = Form(...),
    body: str = Form(...),
) -> dict[str, Any]:
    oid: Any = None
    try:
        oid = ObjectId(chat_id)
    except Exception as exc:
        raise HTTPException(500, "bad chat id") from exc

    thread = await ChatThread.get(oid)
    if thread is None:
        raise HTTPException(500, "chat not found")

    sender = fromUser.strip()
    if sender not in (thread.participant_a, thread.participant_b):
        raise HTTPException(500, "fromUser not in this chat")

    mid = str(ObjectId())
    thread.messages.append(
        ChatMessage(
            id=mid,
            fromUser=sender,
            body=body,
        )
    )
    thread.save()
    out: dict[str, Any] = {"messageId": mid, "chatId": chat_id}
    event_tracker.track_event(
        "chat_message_sent", {"chat_id": chat_id, "message_id": mid, "message": body}
    )
    return out
