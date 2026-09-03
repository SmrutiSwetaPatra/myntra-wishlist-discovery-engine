import asyncio
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import select, func
from app.db.session import AsyncSessionLocal
from app.models.conversations import Conversation
from app.models.analyses import Analysis

async def get_final_metrics():
    async with AsyncSessionLocal() as session:
        # 1. Total Analysis Records
        total_analysis_res = await session.execute(select(func.count(Analysis.id)))
        total_analysis = total_analysis_res.scalar()
        
        # 2. Status Distribution
        status_res = await session.execute(
            select(Analysis.validation_status, func.count(Analysis.id))
            .group_by(Analysis.validation_status)
        )
        distribution = {row[0]: row[1] for row in status_res.all()}
        
        # Breakdown
        api_failures = distribution.get("api_failure", 0)
        schema_failures = distribution.get("schema_failure", 0)
        
        irrelevant_keys = ["excluded_general", "excluded_post_purchase", "excluded_ambiguous"]
        irrelevant = sum(distribution.get(k, 0) for k in irrelevant_keys)
        
        successful_keys = [
            "validated_relevant", "ai_direct_evidence", 
            "indirect_pre_purchase", "ai_indirect_evidence", 
            "ai_unvalidated", "needs_review"
        ]
        successful = sum(distribution.get(k, 0) for k in successful_keys)
        
        print(f"Final Total Analysis Records: {total_analysis}")
        print(f"Successfully Enriched: {successful}")
        print(f"Irrelevant/Excluded: {irrelevant}")
        print(f"API Failures: {api_failures}")
        print(f"Schema Failures: {schema_failures}")
        print("\n--- Final Status Distribution ---")
        for k, v in distribution.items():
            print(f"  {k}: {v}")

if __name__ == "__main__":
    asyncio.run(get_final_metrics())
