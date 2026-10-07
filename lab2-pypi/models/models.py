from datetime import datetime
from typing import List
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey


class Base(DeclarativeBase):
    pass


class User(Base):
    """
    Структура таблицы User
    """

    __tablename__ = "User"

    # Столбцы
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(nullable=False, unique=True)
    email: Mapped[str] = mapped_column(nullable=False, unique=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)

    # Связи между отношениями
    subscriptions: Mapped[List["Subscription"]] = relationship(back_populates="user")

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, username={self.username!r}, email={self.email!r}, created_at={self.created_at!r})"

    def __init__(self, username: str, email: str):
        self.username = username
        self.email = email


class Currency(Base):
    """
    Структура таблицы Currency
    """

    __tablename__ = "Currency"

    # Столбцы
    id: Mapped[int] = mapped_column(primary_key=True)
    code: Mapped[str] = mapped_column(nullable=False, unique=True)
    name: Mapped[str] = mapped_column(nullable=False)
    value: Mapped[float] = mapped_column(nullable=False)

    # Связи между отношениями
    subscriptions: Mapped[List["Subscription"]] = relationship(
        back_populates="currency"
    )

    def __repr__(self) -> str:
        return f"Currency(id={self.id!r}, code={self.code!r}, name={self.name!r})"

    def __init__(self, code: str, name: str, value: float):
        self.code = code
        self.name = name
        self.value = value


class Subscription(Base):
    """
    Структура таблицы Subscription
    """

    __tablename__ = "Subscriptions"

    # Столбцы
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("User.id"), nullable=False)
    currency_id: Mapped[int] = mapped_column(ForeignKey("Currency.id"), nullable=False)

    # Связи между отношениями
    user: Mapped["User"] = relationship(back_populates="subscriptions")
    currency: Mapped["Currency"] = relationship(back_populates="subscriptions")

    def __repr__(self) -> str:
        return f"Subscription(id={self.id!r}, user_id={self.user_id!r}, currency_id={self.currency_id!r})"

    def __init__(self, user_id: int, currency_id: int):
        self.user_id = user_id
        self.currency_id = currency_id
