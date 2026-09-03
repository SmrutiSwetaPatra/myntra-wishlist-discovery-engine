import asyncio
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import select, func
from app.db.session import AsyncSessionLocal
from app.models.conversations import Conversation
from app.models.analyses import Analysis
from scripts.enrich_existing import passes_quality_gate

async def check_db():
    async with AsyncSessionLocal() as session:
        # Total conversations
        total_conv = await session.execute(select(func.count(Conversation.id)))
        total = total_conv.scalar()
        
        # Already processed (Analysis exists)
        query_processed = select(func.count(func.distinct(Analysis.conversation_id)))
        processed_res = await session.execute(query_processed)
        processed = processed_res.scalar()
        
        # Eligible (No Analysis exists)
        query_eligible = select(Conversation).where(
            ~Conversation.id.in_(
                select(Analysis.conversation_id)
            )
        )
        eligible_res = await session.execute(query_eligible)
        eligible_convs = eligible_res.scalars().all()
        
        eligible_count = len(eligible_convs)
        
        # Of the eligible, how many pass quality gate?
        passes = sum(1 for c in eligible_convs if passes_quality_gate(c.raw_content))
        fails = eligible_count - passes
        
        print(f"Total Conversations: {total}")
        print(f"Already Processed (Skipped): {processed}")
        print(f"Pending/Unprocessed: {eligible_count}")
        print(f"  - Passes Quality Gate (Sent to Gemini): {passes}")
        print(f"  - Fails Quality Gate (Excluded): {fails}")

if __name__ == "__main__":
    asyncio.run(check_db())
