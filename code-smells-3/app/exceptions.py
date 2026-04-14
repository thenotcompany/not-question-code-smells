from __future__ import annotations


class ChatServiceError(Exception):
    """Base exception for chat service errors."""


class ThreadNotFoundError(ChatServiceError):
    """Raised when a thread id does not resolve to a stored thread."""

    def __init__(self, thread_id: str) -> None:
        self.thread_id = thread_id
        super().__init__(f"Thread not found: {thread_id}")


class AuthorNotParticipantError(ChatServiceError):
    """Raised when ``author_user_id`` is not in the thread's participant list."""

    def __init__(self, author_user_id: str) -> None:
        self.author_user_id = author_user_id
        super().__init__(
            f"User {author_user_id!r} is not a participant in this thread.",
        )
