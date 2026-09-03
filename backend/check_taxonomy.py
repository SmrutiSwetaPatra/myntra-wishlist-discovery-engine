import asyncio
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.db.session import AsyncSessionLocal
from app.models.analyses import Analysis
from sqlalchemy.future import select

async def get_taxonomy():
    async with AsyncSessionLocal() as session:
        # Get stages
        res = await session.execute(select(Analysis.shopping_stage).distinct())
        print("Shopping Stages:", [r[0] for r in res.all()])
        
        # Get barriers
        res = await session.execute(select(Analysis.primary_barrier_category).distinct())
        print("Barriers:", [r[0] for r in res.all()])

if __name__ == "__main__":
    asyncio.run(get_taxonomy())
