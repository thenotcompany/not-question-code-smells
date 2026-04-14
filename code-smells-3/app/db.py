from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

from app.models.chat import ChatThread
from app.settings import settings


async def init_db() -> None:
    client = AsyncIOMotorClient(settings.mongodb_url)
    await init_beanie(
        database=client[settings.database_name],
        document_models=[ChatThread],
    )
