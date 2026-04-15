import os

from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

from app.models.chat import ChatThread
from app.models.post import Post

# Environment variables for the MongoDB connection
_MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
_DATABASE_NAME = os.getenv("DATABASE_NAME", "social_api")


async def init_db() -> None:
    client = AsyncIOMotorClient(_MONGODB_URL)
    await init_beanie(
        database=client[_DATABASE_NAME],
        document_models=[Post, ChatThread],
    )
