import asyncio
import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from sqlalchemy import select, func
from sqlalchemy.orm import joinedload
from app.db.session import AsyncSessionLocal
from app.models.analyses import Analysis
from app.models.conversations import Conversation

async def fetch_comparison_behavior():
    async with AsyncSessionLocal() as session:
        stmt = (
            select(Analysis)
            .options(joinedload(Analysis.conversation).joinedload(Conversation.source))
            .where(Analysis.comparison_behavior != None)
        )
        
        records = await session.scalars(stmt)
        records = records.all()
        
        print(f"Total comparison_behavior NOT NULL records: {len(records)}")
        
        embedded = 0
        for idx, a in enumerate(records):
            print(f"\n--- Record {idx + 1} ---")
            print(f"ID: {a.id}")
            print(f"Validation Status: {a.validation_status}")
            print(f"Primary Barrier: {a.primary_barrier_category}")
            print(f"Comparison Behavior: {a.comparison_behavior}")
            print(f"Has Embedding: {a.embedding is not None}")
            if a.embedding is not None:
                embedded += 1
            print(f"Raw Text (First 200 chars): {a.conversation.raw_content[:200] if a.conversation.raw_content else ''}...")
            
        print(f"\nTotal embedded comparison_behavior records: {embedded}")

if __name__ == "__main__":
    asyncio.run(fetch_comparison_behavior())
