import asyncio
from app.db.base import Base
from app.db.session import engine

# Import all models to register with Base
from app.models.conversations import Conversation
from app.models.analyses import Analysis
from app.models.insights import Insight

async def init():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

if __name__ == "__main__":
    asyncio.run(init())
