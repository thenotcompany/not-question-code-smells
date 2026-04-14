from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class FilePart:
    filename: str
    media_type: str
    data: bytes
