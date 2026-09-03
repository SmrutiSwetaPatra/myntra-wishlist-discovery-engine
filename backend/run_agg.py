import asyncio
import os
from dotenv import load_dotenv

load_dotenv()

from app.engine.aggregation import InsightAggregator
from app.engine.gemini import GeminiClient
from app.db.session import AsyncSessionLocal
from app.models.insights import Insight
from sqlalchemy.future import select

async def run():
    async with AsyncSessionLocal() as db:
        aggregator = InsightAggregator(db, GeminiClient())
        await aggregator.run()
        
        print("\n=== FINAL AGGREGATION OUTPUT ===")
        res = await db.execute(select(Insight))
        insights = res.scalars().all()
        for i, ins in enumerate(insights, 1):
            print(f"\nOpportunity {i}: {ins.title}")
            print(f"Category: {ins.category}")
            print(f"Direct vs Indirect: {ins.direct_vs_indirect}")
            print(f"Evidence Count: {ins.evidence_count}")
            print(f"Description: {ins.description}")

if __name__ == "__main__":
    asyncio.run(run())
