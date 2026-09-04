import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload
from app.db.session import AsyncSessionLocal
from app.models.analyses import Analysis
from app.models.conversations import Conversation

async def dump_audit():
    async with AsyncSessionLocal() as session:
        valid_statuses = ['validated_relevant', 'indirect_pre_purchase', 'ai_direct_evidence', 'ai_indirect_evidence']
        
        query = (
            select(Analysis)
            .options(joinedload(Analysis.conversation))
            .where(Analysis.validation_status.in_(valid_statuses))
            .where(Analysis.primary_barrier_category.is_not(None))
        )
        res = await session.execute(query)
        records = res.scalars().all()
        
        with open("audit_dump.md", "w") as f:
            f.write(f"Total records found: {len(records)}\n")
            f.write("="*50 + "\n")
            
            for r in records:
                text_preview = r.conversation.raw_content[:200].replace('\n', ' ').encode('ascii', 'replace').decode('ascii')
                f.write(f"ID: {r.conversation_id}\n")
                f.write(f"Status: {r.validation_status}\n")
                f.write(f"Category: {r.primary_barrier_category}\n")
                f.write(f"Unmet Need: {r.unmet_need}\n")
                f.write(f"Secondary Barriers: {r.secondary_barriers}\n")
                f.write(f"Raw Text: {text_preview}\n")
                f.write("-" * 30 + "\n")

if __name__ == "__main__":
    asyncio.run(dump_audit())
