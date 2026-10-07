"""Модели ответов для Currency"""

from pydantic import BaseModel, ConfigDict


class CurrencySchema(BaseModel):
    """Модель для валюты, возвращаемые данные одинаковы и в случае получения с БД и в случае с обновлением"""

    model_config = ConfigDict(from_attributes=True)

    id: int
    code: str
    name: str
    value: float
