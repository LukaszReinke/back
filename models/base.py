import asyncio
import os

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.asyncio.engine import AsyncEngine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

DATABASE_URL = "postgresql+asyncpg://postgres_user:SportsApp123456@postgres:5432/hds_db_develop"


def create_engine(database_url: str | None = None) -> AsyncEngine:  # type: ignore
    global engine
    url = DATABASE_URL if database_url is None else database_url
    engine = create_async_engine(url, echo=False)
    return engine


def get_session_maker(engine: AsyncEngine) -> sessionmaker[AsyncSession]:  # type: ignore
    return sessionmaker(  # type: ignore
        bind=engine,  # type: ignore
        class_=AsyncSession,
        expire_on_commit=False,
        autoflush=False,
    )


def transactional(func):  # type: ignore
    async def wrapper(*args, **kwargs):  # type: ignore
        AsyncSessionLocal = get_session_maker(engine)
        async with AsyncSessionLocal() as session:
            async with session.begin():
                kwargs["session"] = session
                return await func(*args, **kwargs)  # type: ignore

    return wrapper  # type: ignore


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def reset_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


if __name__ == "__main__":
    database_url = os.getenv(
        "DATABASE_URL",
        "postgresql+asyncpg://postgres_user:SportsApp123456@postgres:5432/hds_db_develop",
    )

    create_engine(database_url)

    AsyncSessionLocal: sessionmaker[AsyncSession] = sessionmaker(  # type: ignore
        bind=engine,  # type: ignore
        class_=AsyncSession,
        expire_on_commit=False,
        autoflush=False,
    )

    asyncio.run(init_db())
