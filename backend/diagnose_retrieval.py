import asyncio
import os
import sys
from collections import Counter

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db.session import AsyncSessionLocal
from app.engine.copilot import DiscoveryCopilot
from sqlalchemy.future import select
from app.models.analyses import Analysis

async def run_diagnosis():
    # 1. Database Coverage
    async with AsyncSessionLocal() as session:
        # Check usable records (all non-excluded, non-failure)
        usable_statuses = [
            "ai_direct_evidence", 
            "ai_indirect_evidence", 
            "validated_relevant", 
            "indirect_pre_purchase",
            "ai_unvalidated"
        ]
        
        result = await session.execute(
            select(Analysis).where(Analysis.validation_status.in_(usable_statuses))
        )
        usable_analyses = result.scalars().all()
        
        total_usable = len(usable_analyses)
        with_embeddings = len([a for a in usable_analyses if a.embedding is not None])
        without_embeddings = total_usable - with_embeddings
        
        print("=== A. DATABASE COVERAGE ===")
        print(f"Total usable records: {total_usable}")
        print(f"With embeddings: {with_embeddings}")
        print(f"Without embeddings: {without_embeddings}")
        print()

    # 2. Copilot Retrieval
    copilot = DiscoveryCopilot()
    async with AsyncSessionLocal() as session:
        await copilot.initialize(session)
        
    print("=== B. ACTUAL SEARCHABLE DOCUMENTS ===")
    print(f"Loaded documents in memory: {len(copilot.retriever.documents)}")
    print()
    
    # 3. Analyze query "What prevents wishlisted products from being purchased?"
    print("=== C & D. RETRIEVAL TRACE ===")
    query = "What prevents wishlisted products from being purchased?"
    plan = await copilot.router.route(query, False)
    
    # Get top 15 candidates WITHOUT metadata filtering
    docs = await copilot.retriever.search(
        query=plan.semantic_query,
        top_k=15,
        validation_status_in=plan.validation_status_filter,
        metadata_filters=None
    )
    
    print(f"Query: {query}")
    print(f"Semantic Query: {plan.semantic_query}")
    print(f"Found {len(docs)} initial semantic candidates:")
    
    # Calculate similarity scores by reproducing the search exactly
    query_embedding = await copilot.retriever.embedder.generate_embedding(plan.semantic_query)
    import numpy as np
    from app.engine.retriever import cosine_similarity
    q_vec = np.array(query_embedding, dtype=np.float32)
    similarities = cosine_similarity(q_vec, copilot.retriever.embeddings)
    
    # Track reasons
    from app.engine.schemas import QueryRelevanceDecision
    from app.engine.prompts import QUERY_RELEVANCE_PROMPT
    
    for doc in docs:
        # Find index to get exact score
        idx = -1
        for i, d in enumerate(copilot.retriever.documents):
            if d.conversation_id == doc.conversation_id:
                idx = i
                break
                
        base_score = similarities[idx]
        
        # Apply same boosts as retriever.py
        boosted_score = base_score
        if doc.validation_status in ['validated_relevant', 'ai_direct_evidence']:
            boosted_score += 0.15
        elif doc.validation_status in ['indirect_pre_purchase', 'ai_indirect_evidence']:
            boosted_score += 0.05
            
        print(f"\n- ID: {doc.conversation_id[:8]} | Status: {doc.validation_status} | Barrier: {doc.metadata.get('primary_barrier_category')}")
        print(f"  Base Sim: {base_score:.3f} | Boosted: {boosted_score:.3f}")
        print(f"  Text excerpt: {doc.text[:100]}...")
        
        # Run Relevance Gate manually
        prompt = QUERY_RELEVANCE_PROMPT.format(query=query, evidence=doc.text)
        try:
            decision = await copilot.client.extract_structured(prompt, "", QueryRelevanceDecision)
            print(f"  GATE: {'PASS' if decision.relevant and decision.relevance_score >= 0.6 else 'FAIL'} | Score: {decision.relevance_score:.2f} | Reason: {decision.reason}")
        except Exception as e:
            print(f"  GATE ERROR: {e}")

if __name__ == "__main__":
    asyncio.run(run_diagnosis())
