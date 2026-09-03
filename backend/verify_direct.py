import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload
from app.db.session import AsyncSessionLocal
from app.models.analyses import Analysis
from app.models.conversations import Conversation

async def verify_direct():
    async with AsyncSessionLocal() as session:
        direct_statuses = ['validated_relevant', 'ai_direct_evidence']
        
        query = (
            select(Analysis)
            .options(joinedload(Analysis.conversation))
            .where(Analysis.validation_status.in_(direct_statuses))
        )
        res = await session.execute(query)
        records = res.scalars().all()
        
        for r in records:
            print(f"Analysis ID: {r.id}")
            print(f"Conversation ID: {r.conversation_id}")
            print(f"Source ID: {r.conversation.source_id}")
            print(f"Status: {r.validation_status}")
            print(f"Category: {r.primary_barrier_category}")
            print("-" * 40)

if __name__ == "__main__":
    asyncio.run(verify_direct())
