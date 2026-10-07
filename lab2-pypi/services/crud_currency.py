"""CRUD-операции для модели Currency."""

from sqlalchemy import select
from typing import Sequence
from sqlalchemy.ext.asyncio import AsyncSession

from models.models import Currency
from .get_currencies_from_api import get_currencies_from_api


async def get_currencies(session: AsyncSession) -> Sequence[Currency]:
    """Возвращает текущие курсы валют из базы данных."""

    stmt = select(Currency)
    result = await session.execute(stmt)
    return result.scalars().all()


async def update_currencies(session: AsyncSession) -> Sequence[Currency]:
    """Обновляет курсы валют из внешнего API и возвращает актуальные данные."""

    fetched = await get_currencies_from_api()

    for incoming in fetched:
        stmt = select(Currency).where(Currency.code == incoming.code)
        result = await session.execute(stmt)
        existing = result.scalar_one_or_none()

        if existing is None:
            session.add(incoming)
        else:
            existing.name = incoming.name
            existing.value = incoming.value

        await session.commit()

    return await get_currencies(session)
