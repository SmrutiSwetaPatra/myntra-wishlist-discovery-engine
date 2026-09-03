import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload
from app.db.session import AsyncSessionLocal
from app.models.analyses import Analysis
from app.models.conversations import Conversation

async def run_diagnostic():
    async with AsyncSessionLocal() as session:
        valid_statuses = ['validated_relevant', 'indirect_pre_purchase', 'ai_direct_evidence', 'ai_indirect_evidence']
        
        # A. Aggregation Source
        print("--- A. Aggregation Source ---")
        query = select(Analysis.primary_barrier_category).where(Analysis.validation_status.in_(valid_statuses)).distinct()
        res = await session.execute(query)
        categories = [r[0] for r in res.all() if r[0] is not None]
        print(f"Distinct primary_barrier_category values in valid set: {categories}")
        
        # C. "Other" specifically
        print("\n--- C. 'Other' Records Inspect ---")
        query_other = (
            select(Analysis)
            .options(joinedload(Analysis.conversation))
            .where(Analysis.primary_barrier_category == 'Other')
            .where(Analysis.validation_status.in_(valid_statuses))
        )
        res_other = await session.execute(query_other)
        other_records = res_other.scalars().all()
        
        for i, rec in enumerate(other_records):
            print(f"[{i+1}] conversation_id: {rec.conversation_id}")
            print(f"    validation_status: {rec.validation_status}")
            print(f"    primary_barrier: {rec.primary_barrier_category}")
            print(f"    secondary_barrier: {rec.secondary_barriers}")
            print(f"    text_preview: {rec.conversation.raw_content[:150].replace(chr(10), ' ').encode('ascii', 'replace').decode('ascii')}")
            
        print(f"\nTotal 'Other' records: {len(other_records)}")

if __name__ == "__main__":
    asyncio.run(run_diagnostic())
