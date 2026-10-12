from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from src.api import router as api_router
from src.core import db_helper
from src.core.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await db_helper.dispose()


main_app = FastAPI(lifespan=lifespan)
main_app.include_router(
    api_router,
)

if __name__ == "__main__":
    uvicorn.run(
        "src.main:main_app",
        host=settings.run.host,
        port=settings.run.port,
        reload=True,
    )
