from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from src.core.config import settings


class DatabaseHelper:
    def __init__(
        self,
        url: str,
        echo: bool = False,
    ):
        self.engine = create_async_engine(
            url=url,
            echo=echo,
        )
        self.session_factory = async_sessionmaker(
            bind=self.engine,
            autoflush=False,
            expire_on_commit=False,
        )

    async def dispose(self):
        await self.engine.dispose()

    async def session_getter(self) -> AsyncGenerator[AsyncSession]:
        async with self.session_factory() as session:
            yield session


db_helper = DatabaseHelper(
    url=str(settings.db.url),
    echo=settings.db.echo,
)
