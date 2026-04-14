from __future__ import annotations

from collections.abc import Sequence

from app.domain.llm.factory import build_llm_service
from app.exceptions import AuthorNotParticipantError, ThreadNotFoundError
from app.models.chat import ChatThread, ThreadMessage
from app.services.chat_domain_service import ChatDomainService


class ChatApplicationService:
    """Application boundary — collaborative threads and optional LLM turns."""

    def __init__(self) -> None:
        self._domain = ChatDomainService()
        self._llm = build_llm_service()

    async def create_thread(
        self,
        title: str,
        participant_user_ids: list[str],
    ) -> ChatThread:
        return await self._domain.create_thread(title, participant_user_ids)

    async def get_thread(self, thread_id: str) -> ChatThread:
        thread = await self._domain.get_thread(thread_id)
        if thread is None:
            raise ThreadNotFoundError(thread_id)
        return thread

    @staticmethod
    def _transcript_for_llm(thread: ChatThread) -> str:
        lines: list[str] = []
        for message in thread.messages:
            if message.role == "user":
                label = message.author_user_id or "user"
                lines.append(f"{label}: {message.text}")
            else:
                lines.append(f"assistant: {message.text}")
        return "\n".join(lines)

    async def post_collaborative_message(
        self,
        thread_id: str,
        *,
        author_user_id: str,
        text: str,
        request_llm_reply: bool,
        attachment_specs: Sequence[tuple[str, str, str]] = (),
    ) -> tuple[ChatThread, bool]:
        """
        Append a user-authored line. Calls the LLM **only** when ``request_llm_reply`` is true,
        then appends a single assistant message to the same embedded list.
        """
        thread = await self._domain.get_thread(thread_id)
        if thread is None:
            raise ThreadNotFoundError(thread_id)
        if author_user_id not in thread.participant_user_ids:
            raise AuthorNotParticipantError(author_user_id)

        user_message = ThreadMessage(
            role="user",
            author_user_id=author_user_id,
            text=text,
        )
        thread = await self._domain.append_message(thread_id, user_message)
        if thread is None:
            raise ThreadNotFoundError(thread_id)

        assistant_appended = False
        if request_llm_reply:
            prompt = self._transcript_for_llm(thread)
            assistant_text = self._llm.generate_from_user_turn(
                prompt,
                attachment_specs,
                preferred_vendor="claude",
            )
            assistant_message = ThreadMessage(
                role="assistant",
                author_user_id=None,
                text=assistant_text,
            )
            thread = await self._domain.append_message(thread_id, assistant_message)
            if thread is None:
                raise ThreadNotFoundError(thread_id)
            assistant_appended = True

        return thread, assistant_appended
