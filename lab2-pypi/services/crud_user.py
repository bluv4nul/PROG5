"""CRUD-операции для модели User."""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Sequence

from models.models import Subscription, User, Currency


async def create_user(session: AsyncSession, username: str, email: str) -> User:
    """Создает нового пользователя и сохраняет его в базе данных."""

    user = User(username=username, email=email)

    session.add(user)
    await session.commit()
    await session.refresh(user)

    return user


async def get_users(session: AsyncSession) -> Sequence[User]:
    """Возвращает всех пользователей, хранящихся в базе данных."""

    stmt = select(User)
    result = await session.execute(stmt)

    return result.scalars().all()


async def get_user_by_id_details(session: AsyncSession, user_id: int) -> dict | None:
    """Возвращает информацию о пользователе и о его подписках"""

    user_info = (
        await session.execute(select(User).where(User.id == user_id))
    ).scalar_one_or_none()

    subscriptions = (
        (
            await session.execute(
                select(Subscription).where(Subscription.user_id == user_id)
            )
        )
        .scalars()
        .all()
    )

    if len(subscriptions) == 0:
        return {
            "user": user_info,
            "subscriptions": "Пользователь не подписан на валюты",
        }

    currency_ids = list({s.currency_id for s in subscriptions})

    currencies_info = (
        (await session.execute(select(Currency).where(Currency.id.in_(currency_ids))))
        .scalars()
        .all()
    )

    return {
        "user": user_info,
        "subscriptions": currencies_info,
    }


async def delete_user_by_id(session: AsyncSession, user_id: int) -> None:
    """Удаляет пользователя по идентификатору."""

    user = (
        await session.execute(select(User).where(User.id == user_id))
    ).scalar_one_or_none()

    if user is None:
        raise ValueError("Пользователь не найден")

    await session.delete(user)
    await session.commit()


async def update_user(
    session: AsyncSession,
    user_id: int,
    new_email: str | None = None,
    new_username: str | None = None,
) -> User:
    """Обновляет информацию о пользователе."""

    user = (
        await session.execute(select(User).where(User.id == user_id))
    ).scalar_one_or_none()

    if user is None:
        raise ValueError("Пользователь не найден")

    if new_email is not None:
        user.email = new_email
    if new_username is not None:
        user.username = new_username

    await session.commit()
    await session.refresh(user)
    return user
