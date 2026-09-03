import asyncio
import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from app.db.session import AsyncSessionLocal
from app.models.analyses import Analysis
from app.models.conversations import Conversation

async def fetch_direct():
    async with AsyncSessionLocal() as session:
        stmt = (
            select(Analysis)
            .options(joinedload(Analysis.conversation).joinedload(Conversation.source))
            .where(Analysis.validation_status == "ai_direct_evidence")
        )
        
        records = await session.scalars(stmt)
        for idx, a in enumerate(records.all()):
            print(f"\n--- AI Direct Record {idx + 1} ---")
            print(f"ID: {a.id}")
            print(f"Primary Barrier: {a.primary_barrier_category}")
            print(f"Wishlist Intent: {a.wishlist_intent}")
            print(f"Comparison: {a.comparison_behavior}")
            print(f"Shopping Stage: {a.shopping_stage}")
            print(f"Raw Text: {a.conversation.raw_content}")

if __name__ == "__main__":
    asyncio.run(fetch_direct())
