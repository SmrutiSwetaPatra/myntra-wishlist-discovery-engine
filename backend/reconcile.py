import asyncio
import os
import sys
from datetime import datetime, timezone

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import select, func
from app.db.session import AsyncSessionLocal
from app.models.conversations import Conversation
from app.models.analyses import Analysis

async def reconcile():
    async with AsyncSessionLocal() as session:
        # 1. Total Pending Records
        # Conversations that do NOT have any Analysis record
        query_eligible = select(func.count(Conversation.id)).where(
            ~Conversation.id.in_(select(Analysis.conversation_id))
        )
        res_eligible = await session.execute(query_eligible)
        pending_records = res_eligible.scalar()
        
        # Total Conversations
        total_conv = (await session.execute(select(func.count(Conversation.id)))).scalar()
        
        # Conversations with at least one Analysis
        processed_convs = (await session.execute(select(func.count(func.distinct(Analysis.conversation_id))))).scalar()

        # 4. Distinguish NEW vs HISTORICAL
        # Let's say NEW is analyzed_at >= '2026-09-02 10:00:00+00:00' (adjusting for timezones)
        run_start = datetime(2026, 9, 2, 4, 30, tzinfo=timezone.utc) # 10:00 AM IST is 4:30 AM UTC
        
        all_analyses = (await session.execute(select(Analysis))).scalars().all()
        
        new_analyses = []
        historical_analyses = []
        for a in all_analyses:
            if not a.analyzed_at:
                historical_analyses.append(a)
                continue
            
            dt = a.analyzed_at
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
                
            if dt >= run_start:
                new_analyses.append(a)
            else:
                historical_analyses.append(a)
        
        # Reconcile the 314 (312 to Gemini + 2 quality gate) new records
        # Wait, if 2 were quality gate, they should be in new_analyses.
        # Let's check status of new_analyses.
        new_dist = {}
        for a in new_analyses:
            new_dist[a.validation_status] = new_dist.get(a.validation_status, 0) + 1
            
        hist_dist = {}
        for a in historical_analyses:
            hist_dist[a.validation_status] = hist_dist.get(a.validation_status, 0) + 1
            
        print(f"Total Conversations: {total_conv}")
        print(f"Distinct Processed Conversations: {processed_convs}")
        print(f"1. Exact pending remaining: {pending_records}")
        
        print(f"\n2. Reconcile 542 vs 544: pending is {pending_records}")
        
        print(f"\n3/4. NEW Records Created in this run: {len(new_analyses)}")
        for k, v in new_dist.items():
            print(f"  {k}: {v}")
            
        print(f"\nHISTORICAL Records (Before this run): {len(historical_analyses)}")
        for k, v in hist_dist.items():
            print(f"  {k}: {v}")
            
        # 6. Duplicates check
        # Check if any conversation has more than 1 Analysis record in this run?
        # Actually, let's just check if ANY conversation has multiple analysis records in the DB
        conv_counts = {}
        for a in all_analyses:
            conv_counts[str(a.conversation_id)] = conv_counts.get(str(a.conversation_id), 0) + 1
            
        duplicates = {k: v for k, v in conv_counts.items() if v > 1}
        print(f"\n6. Conversations with multiple Analysis records: {len(duplicates)}")
        if duplicates:
            print(f"   Historical duplicates exist, but did the new run create any?")
            new_convs = {str(a.conversation_id) for a in new_analyses}
            new_duplicates = {k: v for k, v in duplicates.items() if k in new_convs}
            print(f"   New duplicates created in this run: {len(new_duplicates)}")

if __name__ == "__main__":
    asyncio.run(reconcile())
