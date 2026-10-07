from fastapi import APIRouter, Depends
from schemas.user_schema import UserCreate, UserDetailRead, UserRead, UserUpdate
from sqlalchemy.ext.asyncio import AsyncSession
from db.database import get_session
from services.crud_user import (
    create_user,
    get_users,
    get_user_by_id_details,
    delete_user_by_id,
    update_user,
)

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/", response_model=list[UserRead])
async def read_users_endpoint(session: AsyncSession = Depends(get_session)):
    """Получить список всех пользователей."""

    return await get_users(session)


@router.post("/", response_model=UserRead)
async def create_user_endpoint(
    user: UserCreate, session: AsyncSession = Depends(get_session)
):
    """Создать нового пользователя."""

    return await create_user(session, user.username, user.email)


@router.get("/{user_id}", response_model=UserDetailRead)
async def read_user_endpoint(
    user_id: int, session: AsyncSession = Depends(get_session)
):
    """Получить информацию о конкретном пользователе."""

    return await get_user_by_id_details(session, user_id)


@router.put("/{user_id}/", response_model=UserRead)
async def update_user_endpoint(
    user_id: int, user_update: UserUpdate, session: AsyncSession = Depends(get_session)
):
    """Обновить информацию о пользователе."""

    return await update_user(
        session, user_id, new_email=user_update.email, new_username=user_update.username
    )


@router.delete("/{user_id}/")
async def delete_user_endpoint(
    user_id: int, session: AsyncSession = Depends(get_session)
):
    """Удалить пользователя по идентификатору."""

    await delete_user_by_id(session, user_id)
    return {"detail": "Пользователь удален"}
