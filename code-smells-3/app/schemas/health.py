"""Small shared responses not tied to chat."""

from typing import Literal

from pydantic import BaseModel


class HealthStatusResponse(BaseModel):
    """``GET /health`` payload."""

    status: Literal["ok"] = "ok"
