from __future__ import annotations

from bson import ObjectId  # type: ignore[import-untyped]

from app.models.chat import ChatThread, ThreadMessage


class ChatRepository:
    """Persistence for ``ChatThread`` documents."""

    async def get_thread(self, thread_id: str) -> ChatThread | None:
        try:
            object_id = ObjectId(thread_id)
        except Exception:
            return None
        return await ChatThread.get(object_id)

    async def create_thread(
        self,
        title: str,
        participant_user_ids: list[str],
    ) -> ChatThread:
        thread = ChatThread(
            title=title,
            participant_user_ids=participant_user_ids,
            messages=[],
        )
        await thread.insert()  # type: ignore[misc]
        return thread

    async def append_message(
        self,
        thread_id: str,
        message: ThreadMessage,
    ) -> ChatThread | None:
        thread = await self.get_thread(thread_id)
        if thread is None:
            return None
        thread.messages.append(message)
        await thread.save()  # type: ignore[misc]
        return thread
