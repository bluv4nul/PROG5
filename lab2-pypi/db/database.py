from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

DATABASE_URL = "sqlite+aiosqlite:///db/database.db"

engine = create_async_engine(DATABASE_URL, echo=True)

Session = async_sessionmaker(engine, expire_on_commit=False)


async def init_db() -> None:
    """Инициализирует базу данных, создавая все необходимые таблицы."""
    from models.models import Base

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """Получает асинхронную сессию для взаимодействия с базой данных.

    Returns:
        Асинхронная сессия SQLAlchemy.
    """
    async with Session() as session:
        yield session
