import asyncio
import json
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload
from app.db.session import AsyncSessionLocal
from app.models.analyses import Analysis
from app.models.conversations import Conversation
from app.engine.copilot import DiscoveryCopilot
from app.engine.schemas import QueryRelevanceDecision
from app.engine.router import ExecutionPlan
from app.engine.prompts import QUERY_RELEVANCE_PROMPT

async def diagnostic():
    print("--- 1. Router Output ---")
    copilot = DiscoveryCopilot()
    query = "How do users compare multiple shortlisted products?"
    
    plan = ExecutionPlan(
        is_quantitative=False,
        requires_cross_source=False,
        requires_segmentation=False,
        validation_status_filter=['validated_relevant', 'ai_direct_evidence', 'indirect_pre_purchase', 'ai_indirect_evidence'],
        metadata_filters='{"comparison_behavior": "__not_null__"}',
        semantic_query="How do users compare multiple shortlisted products?",
        insufficient_evidence_likely=False
    )
    if plan.metadata_filters and isinstance(plan.metadata_filters, str):
        plan.metadata_filters = json.loads(plan.metadata_filters)
        
    print(f"is_quantitative: {plan.is_quantitative}")

    print("\n--- 2. Database Record Inspect ---")
    async with AsyncSessionLocal() as session:
        # Find the specific wishlist-limit record
        result = await session.execute(
            select(Analysis)
            .options(joinedload(Analysis.conversation))
            .where(Analysis.validation_status == "validated_relevant")
        )
        analyses = result.scalars().all()
        target_a = None
        for a in analyses:
            if "LIMIT on how many items you can add to your WISHLIST" in str(a.conversation.raw_content):
                target_a = a
                break
                
        if not target_a:
            print("Wishlist-limit record not found!")
            return
            
        print(f"conversation_id: {target_a.conversation.id}")
        print(f"validation_status: {target_a.validation_status}")
        print(f"comparison_behavior: {target_a.comparison_behavior}")
        print(f"embedding exists: {target_a.embedding is not None}")
        print(f"raw_text preview: {target_a.conversation.raw_content[:150]}...")
        
        await copilot.initialize(session)
        
    print("\n--- 3. Vector Retrieval ---")
    docs = await copilot.retriever.search(
        query=plan.semantic_query,
        top_k=15,
        validation_status_in=plan.validation_status_filter,
        metadata_filters=plan.metadata_filters
    )
    
    # Simulate the fallback that copilot does internally
    if len(docs) < 15:
        expanded_tiers = ["validated_relevant", "ai_direct_evidence", "indirect_pre_purchase", "ai_indirect_evidence"]
        fallback_docs = await copilot.retriever.search(
            query=plan.semantic_query,
            top_k=15,
            validation_status_in=expanded_tiers,
            metadata_filters=None
        )
        seen = {d.conversation_id for d in docs}
        for d in fallback_docs:
            if d.conversation_id not in seen:
                docs.append(d)
                seen.add(d.conversation_id)
        docs = docs[:15]
        
    target_doc = None
    target_idx = -1
    for i, d in enumerate(docs):
        if str(target_a.conversation.id) == d.conversation_id:
            target_doc = d
            target_idx = i
            break
            
    if target_doc:
        print(f"Record found in Top 15! Rank: {target_idx + 1}, Score: {target_doc.metadata.get('retrieval_score')}")
    else:
        print("Record NOT found in Top 15 candidates. Top 15 scores:")
        for i, d in enumerate(docs):
            print(f"  {i+1}: Score={d.metadata.get('retrieval_score')} - {d.text[:50]}...")
            
    print("\n--- 4. QueryRelevanceGate ---")
    if target_doc:
        prompt = QUERY_RELEVANCE_PROMPT.format(query=query, evidence=target_doc.text)
        print(f"Prompt that WOULD be sent:\n{prompt}")
    else:
        # Evaluate it manually even if not retrieved
        prompt = QUERY_RELEVANCE_PROMPT.format(query=query, evidence=target_a.conversation.raw_content)
        print(f"Prompt that WOULD be sent:\n{prompt}")

if __name__ == "__main__":
    import logging
    logging.getLogger("httpx").setLevel(logging.WARNING)
    asyncio.run(diagnostic())
