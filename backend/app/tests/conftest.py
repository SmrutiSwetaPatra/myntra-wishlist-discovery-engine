import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from app.db.base import Base
from app.core.config import settings
import os

TEST_SQLALCHEMY_DATABASE_URI = "sqlite+aiosqlite:///./data/test_myntra_copilot.db"

# Ensure data dir exists
os.makedirs("data", exist_ok=True)

engine = create_async_engine(TEST_SQLALCHEMY_DATABASE_URI, echo=False, future=True)
TestingSessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

@pytest_asyncio.fixture(scope="session")
async def db_engine():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()
    
    # Clean up test DB file
    if os.path.exists("data/test_myntra_copilot.db"):
        os.remove("data/test_myntra_copilot.db")

@pytest_asyncio.fixture
async def db_session(db_engine) -> AsyncSession:
    async with TestingSessionLocal() as session:
        yield session
