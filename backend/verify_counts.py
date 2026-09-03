import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload
from sqlalchemy import func
from app.db.session import AsyncSessionLocal
from app.models.analyses import Analysis
from app.models.conversations import Conversation

async def run_verification():
    async with AsyncSessionLocal() as session:
        valid_statuses = ['validated_relevant', 'indirect_pre_purchase', 'ai_direct_evidence', 'ai_indirect_evidence']
        
        # 1. Total established evidence records
        query_total = select(func.count(Analysis.id)).where(Analysis.validation_status.in_(valid_statuses))
        res_total = await session.execute(query_total)
        total_records = res_total.scalar()
        print(f"1. Total established evidence records: {total_records}")
        
        # 2. Counts by validation_status
        query_status = select(Analysis.validation_status, func.count(Analysis.id)).where(Analysis.validation_status.in_(valid_statuses)).group_by(Analysis.validation_status)
        res_status = await session.execute(query_status)
        print("\n2. Counts by validation_status:")
        for status, count in res_status:
            print(f"   - {status}: {count}")
            
        # 3. Counts by primary_barrier_category AND validation_status
        query_cat_status = select(Analysis.primary_barrier_category, Analysis.validation_status, func.count(Analysis.id)).where(Analysis.validation_status.in_(valid_statuses)).group_by(Analysis.primary_barrier_category, Analysis.validation_status)
        res_cat_status = await session.execute(query_cat_status)
        print("\n3. Counts by primary_barrier_category AND validation_status:")
        for cat, status, count in res_cat_status:
            print(f"   - {cat} | {status}: {count}")
            
        # 4 & 5. Exact conversation IDs for every direct evidence record
        direct_statuses = ['validated_relevant', 'ai_direct_evidence']
        query_direct = select(Analysis).where(Analysis.validation_status.in_(direct_statuses))
        res_direct = await session.execute(query_direct)
        direct_records = res_direct.scalars().all()
        print("\n4 & 5. Exact conversation IDs for direct evidence records:")
        for rec in direct_records:
            print(f"   - ID: {rec.conversation_id} | Status: {rec.validation_status} | Category: {rec.primary_barrier_category}")

if __name__ == "__main__":
    asyncio.run(run_verification())
