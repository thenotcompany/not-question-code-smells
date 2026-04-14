from fastapi import APIRouter, HTTPException, status

from app.exceptions import AuthorNotParticipantError, ChatServiceError, ThreadNotFoundError
from app.schemas.chat_requests import CreateThreadRequest, PostMessageRequest
from app.schemas.chat_responses import (
    PostMessageResponse,
    ThreadCreatedResponse,
    ThreadDetailResponse,
)
from app.services.chat_application_service import ChatApplicationService

router = APIRouter(prefix="/threads", tags=["chat"])

_chat_application = ChatApplicationService()


@router.post(
    "",
    response_model=ThreadCreatedResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_thread(request_body: CreateThreadRequest) -> ThreadCreatedResponse:
    try:
        thread = await _chat_application.create_thread(
            request_body.title,
            request_body.participant_user_ids,
        )
        return ThreadCreatedResponse.from_chat_thread(thread)
    except ChatServiceError as exc:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc


@router.get(
    "/{thread_id}",
    response_model=ThreadDetailResponse,
)
async def get_thread(thread_id: str) -> ThreadDetailResponse:
    try:
        thread = await _chat_application.get_thread(thread_id)
        return ThreadDetailResponse.from_chat_thread(thread)
    except ThreadNotFoundError as exc:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail="Thread not found.",
        ) from exc
    except ChatServiceError as exc:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc


@router.post(
    "/{thread_id}/messages",
    response_model=PostMessageResponse,
)
async def post_message(
    thread_id: str,
    request_body: PostMessageRequest,
) -> PostMessageResponse:
    try:
        attachment_specs = tuple(
            (a.filename, a.media_type, str(a.url))
            for a in request_body.attachments
        )
        thread, assistant_appended = await _chat_application.post_collaborative_message(
            thread_id,
            author_user_id=request_body.author_user_id,
            text=request_body.text,
            request_llm_reply=request_body.request_llm_reply,
            attachment_specs=attachment_specs,
        )
        return PostMessageResponse.from_result(
            thread,
            assistant_reply_appended=assistant_appended,
        )
    except ThreadNotFoundError as exc:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail="Thread not found.",
        ) from exc
    except AuthorNotParticipantError as exc:
        raise HTTPException(
            status.HTTP_403_FORBIDDEN,
            detail=str(exc),
        ) from exc
    except ChatServiceError as exc:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc
