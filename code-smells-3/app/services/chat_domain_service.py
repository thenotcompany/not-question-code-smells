from __future__ import annotations

from app.models.chat import ChatThread, ThreadMessage
from app.repositories.chat_repository import ChatRepository


class ChatDomainService:
    """Domain-level operations on threads."""

    def __init__(self, repository: ChatRepository | None = None) -> None:
        self._repository = repository or ChatRepository()

    async def create_thread(
        self,
        title: str,
        participant_user_ids: list[str],
    ) -> ChatThread:
        return await self._repository.create_thread(title, participant_user_ids)

    async def append_message(
        self,
        thread_id: str,
        message: ThreadMessage,
    ) -> ChatThread | None:
        return await self._repository.append_message(thread_id, message)

    async def get_thread(self, thread_id: str) -> ChatThread | None:
        return await self._repository.get_thread(thread_id)
