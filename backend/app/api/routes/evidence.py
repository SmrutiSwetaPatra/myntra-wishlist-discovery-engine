from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload
from app.db.session import AsyncSessionLocal
from app.models.analyses import Analysis
from app.models.conversations import Conversation
from typing import List
import json

router = APIRouter(tags=["evidence"])

@router.get("/")
async def get_evidence():
    async with AsyncSessionLocal() as session:
        valid_statuses = ['validated_relevant', 'indirect_pre_purchase', 'ai_direct_evidence', 'ai_indirect_evidence']
        
        # We need to fetch analyses joined with their conversation and source
        query = (
            select(Analysis)
            .where(Analysis.validation_status.in_(valid_statuses))
            .options(
                joinedload(Analysis.conversation).joinedload(Conversation.source)
            )
        )
        
        result = await session.execute(query)
        analyses = result.scalars().all()
        
        evidence_list = []
        for a in analyses:
            # Safely handle secondary barriers
            sec_barrier = None
            if a.secondary_barriers and isinstance(a.secondary_barriers, list) and len(a.secondary_barriers) > 0:
                sec_barrier = a.secondary_barriers[0]
                
            evidence_list.append({
                "id": str(a.id),
                "source": a.conversation.source.platform,
                "stage": a.shopping_stage,
                "type": a.validation_status,
                "area": a.primary_barrier_category,
                "text": a.conversation.raw_content,
                "primaryBarrier": a.primary_barrier_category,
                "secondaryBarrier": a.primary_barrier_detail or sec_barrier,
                "intent": a.purchase_intent,
                "isDirect": a.validation_status in ['validated_relevant', 'ai_direct_evidence']
            })
            
        return evidence_list
