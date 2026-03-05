import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers.pet import pet_router
from routers.basket import basket_router
from tortoise.contrib.fastapi import register_tortoise
from core.redis_manager import redis_listener

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    app.state.redis_task = asyncio.create_task(redis_listener())
    print("Redis listener started")
    yield
    # Shutdown
    app.state.redis_task.cancel()
    try:
        await app.state.redis_task
    except asyncio.CancelledError:
        print("Redis listener cancelled")


app = FastAPI()
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://192.168.1.86:5173",
    "http://192.168.1.110:5173",
    "*",


]
app.include_router(pet_router)
app.include_router(basket_router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Временно разрешаем всё для теста
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

register_tortoise(
    app,
    db_url="sqlite://db.sqlite3",  # Или "postgres://user:pass@host:port/db"
    modules={"models": ["models.pet","models.basket"]},  # Где искать модели
    generate_schemas=True,  # Создать таблицы автоматически (только для разработки)
    add_exception_handlers=True,
)
