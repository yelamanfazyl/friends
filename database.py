from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from config import get_settings
from contextlib import asynccontextmanager
from models.base import Base
import asyncio

settings = get_settings()

async_engine = create_async_engine(
    settings.database_url,
    echo=settings.debug,
    pool_size=10,
    max_overflow=20,
)

async_session = async_sessionmaker(
    async_engine,
    expire_on_commit=False,
    class_=AsyncSession,
)

# Импорт моделей — обязательно, чтобы они зарегистрировались в Base.metadata
import models # type: ignore


@asynccontextmanager
async def get_async_session():
    async with async_session() as session:
        yield session

# хочу подметить, что это не обязательно, но я предпочитаю создавать таблицы в базе данных при запуске приложения
# это позволяет избежать проблем с отсутствующими таблицами при первом запуске
async def init_models():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


if __name__ == "__main__":
    asyncio.run(init_models())