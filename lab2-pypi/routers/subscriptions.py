from fastapi import APIRouter, Depends
from db.database import get_session
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.subscription_schema import SubscriptionCreate, SubscriptionRead
from services.crud_subscription import create_subscription, delete_subscription
from models.models import Subscription

router = APIRouter(prefix="/subscriptions", tags=["subscriptions"])


@router.post("/", response_model=SubscriptionCreate)
async def create_subscription_endpoint(
    subscription: SubscriptionCreate, session: AsyncSession = Depends(get_session)
):
    """Создать новую подписку для пользователя на валюту."""

    return await create_subscription(
        session, subscription.user_id, subscription.currency_id
    )


@router.delete("/")
async def delete_subscription_endpoint(
    subscription: SubscriptionRead, session: AsyncSession = Depends(get_session)
):
    """Удалить существующую подписку пользователя на валюту."""

    await delete_subscription(session, subscription.user_id, subscription.currency_id)
    return subscription
