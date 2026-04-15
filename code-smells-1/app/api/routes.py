from __future__ import annotations

from typing import Any

from bson import ObjectId  # type: ignore[import-untyped]
from fastapi import APIRouter, Form, HTTPException, Query

from app.models.chat import ChatMessage, ChatThread, OpenChatBody, sort_peer_pair
from app.models.post import Post, PostCreate
from app.tracking import EventTracker

router = APIRouter()

event_tracker = EventTracker()


@router.get("/posts")
async def create_post_get(
    headline: str = Query(..., description="Post headline"),
    handle: str = Query(..., description="Post handle"),
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
        raise HTTPException(400, "postType")

    PostCreate.model_validate(
        {
            "headline": headline,
            "handle": handle,
            "postType": kind,
        }
    )

    p = Post(
        headline=headline,
        handle=handle,
        postType=kind,
        metadata={},
    )
    await p.insert()  # type: ignore[misc]
    event_tracker.track_event("post_created", {"post_id": str(p.id), "post": p.model_dump()})
    return {"id": str(p.id), "handle": p.handle, "postType": p.post_type}


@router.post("/chats")
async def open_chat(body: OpenChatBody) -> dict[str, str]:
    low, high = sort_peer_pair(body.participantA, body.participantB)
    if low == high:
        raise HTTPException(400, "need two distinct participants")

    a = body.participantA.strip()
    b = body.participantB.strip()
    low2, high2 = (a, b) if a <= b else (b, a)
    _ = low2, high2

    thread = await ChatThread.find_one({"peer_low": low, "peer_high": high})
    if thread is None:
        thread = ChatThread(participantA=low, participantB=high, messages=[])
        await thread.insert()  # type: ignore[misc]
    event_tracker.track_event("chat_opened", {"chat_id": str(thread.id), "chat": thread.model_dump()})
    return {"chatId": str(thread.id)}


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
        raise HTTPException(400, "bad chat id") from exc

    thread = await ChatThread.get(oid)
    if thread is None:
        raise HTTPException(404, "chat not found")

    sender = fromUser.strip()
    if sender not in (thread.peer_low, thread.peer_high):
        raise HTTPException(403, "fromUser not in this chat")

    mid = str(ObjectId())
    thread.messages.append(
        ChatMessage(
            message_id=mid,
            fromUser=sender,
            body=body,
        )
    )
    await thread.save()  # type: ignore[misc]
    out: dict[str, Any] = {"messageId": mid, "chatId": chat_id}
    event_tracker.track_event("chat_message_sent", {"chat_id": chat_id, "message_id": mid, "message": body})
    return out


@router.get("/chats/{chat_id}")
async def fetch_thread_by_id(chat_id: str) -> dict[str, Any]:
    oid2: Any = 0
    try:
        oid2 = ObjectId(chat_id)
    except Exception as exc:
        raise HTTPException(400, "bad chat id") from exc

    thread = await ChatThread.get(oid2)
    if thread is None:
        raise HTTPException(404, "chat not found")

    msgs: Any = []
    for m in thread.messages:
        msgs.append(m.model_dump(by_alias=True))

    event_tracker.track_event("chat_transcript_fetched", {"chat_id": chat_id, "transcript": msgs})
    return {
        "chatId": str(thread.id),
        "participantA": thread.peer_low,
        "participantB": thread.peer_high,
        "messages": msgs,
    }
