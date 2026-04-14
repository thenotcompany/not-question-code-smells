from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.chat import router as chat_router
from app.db import init_db
from app.schemas.health import HealthStatusResponse


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


app = FastAPI(title="Chat API", lifespan=lifespan)
app.include_router(chat_router)


@app.get("/health", response_model=HealthStatusResponse)
async def health() -> HealthStatusResponse:
    return HealthStatusResponse()
