import sys
from pathlib import Path
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

sys.path.insert(0, str(Path(__file__).resolve().parent))
from core.config import settings # noqa

engine = create_async_engine(
    settings.POSTGRES_URL,
    # Установить False в production
    echo=True,
    future=True
)

# Создание асинхронной сессии
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False
)

