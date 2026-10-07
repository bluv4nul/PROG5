"""Модели ответов для User"""

from pydantic import BaseModel, ConfigDict, EmailStr
from schemas.currency_schema import CurrencySchema


class UserCreate(BaseModel):
    """Модель для создания пользователя"""

    username: str
    email: EmailStr


class UserRead(BaseModel):
    """Модель для получении данных о пользователе"""

    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    email: EmailStr


class UserDetailRead(BaseModel):
    """Модель для получения полной информации о пользователе"""

    model_config = ConfigDict(from_attributes=True)

    user: UserRead
    subscriptions: list[CurrencySchema] | str


class UserUpdate(BaseModel):
    """Модель для обновления информации пользователя"""

    username: str | None = None
    email: EmailStr | None = None
