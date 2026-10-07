"""Модели для Subscriptions"""

from pydantic import BaseModel, ConfigDict


class SubscriptionCreate(BaseModel):
    user_id: int
    currency_id: int


class SubscriptionRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    currency_id: int
