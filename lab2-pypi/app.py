from fastapi import FastAPI
from contextlib import asynccontextmanager

from db.database import init_db
from routers.users import router as users_router
from routers.currencies import router as currencies_router
from routers.subscriptions import router as subscriptions_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(users_router)
app.include_router(currencies_router)
app.include_router(subscriptions_router)
