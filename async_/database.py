from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_ASYNC_DATABASE_URL = "sqlite+aiosqlite:///./fastapitestasync.db"

engine = create_async_engine(
    SQLALCHEMY_ASYNC_DATABASE_URL,
    echo=True
)

async_session = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)

async def get_db() -> AsyncSession:
    async with async_session() as session:
        return session