from __future__ import annotations

from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    mongodb_url: str = "mongodb://localhost:27018"
    database_name: str = "chat_api"

    openai_api_key: Optional[str] = None
    openai_base_url: Optional[str] = None
    openai_chat_model: str = "gpt-4o-mini"


settings = Settings()
