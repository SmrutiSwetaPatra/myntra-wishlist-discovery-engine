import asyncio
import os
import sys
import logging

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from app.engine.copilot import DiscoveryCopilot
from app.db.session import AsyncSessionLocal
from app.engine.retriever import NumPyVectorStore
from app.engine.router import QueryRouter

async def test_live_qa():
    # Setup
    session = AsyncSessionLocal()
    copilot = DiscoveryCopilot()
    await copilot.initialize(session)
    queries = [
        "How do users decide between two similar dresses in their wishlist?",
        "How do users compare multiple shortlisted products?"
    ]
    
    for q in queries:
        print("\n" + "="*80)
        print(f"QUERY: {q}")
        print("="*80)
        
        # 1. Peek at Router
        router = QueryRouter()
        plan = await router.route(q)
        print(f"[ROUTER] validation_status_filter: {plan.validation_status_filter}")
        print(f"[ROUTER] metadata_filters: {plan.metadata_filters}")
        
        # 2. Peek at Retriever (Before Gate)
        docs_before = await copilot.retriever.search(
            query=plan.semantic_query,
            top_k=15,
            validation_status_in=plan.validation_status_filter,
            metadata_filters=plan.metadata_filters
        )
        # Apply fallback logic locally just to count
        if len(docs_before) < 15:
            fallback = await copilot.retriever.search(
                query=plan.semantic_query,
                top_k=15,
                validation_status_in=["validated_relevant", "ai_direct_evidence", "indirect_pre_purchase", "ai_indirect_evidence"],
                metadata_filters=None
            )
            seen = {d.conversation_id for d in docs_before}
            for d in fallback:
                if d.conversation_id not in seen:
                    docs_before.append(d)
                    seen.add(d.conversation_id)
            docs_before = docs_before[:15]
            
        print(f"[RETRIEVER] Documents passed to Gate: {len(docs_before)}")
        
        try:
            response = await copilot.query(q)
            
            accepted_docs = response.evidence_cards
            print(f"[GATE] Documents accepted by Gate: {len(accepted_docs)}")
            
            for idx, card in enumerate(accepted_docs):
                print(f"  -> Accepted {idx + 1}: Tier={card.validation_status}")
                print(f"     Preview: {card.raw_text[:100]}...")
                    
            print("\n[SYNTHESIS] Final Answer:")
            print(response.answer)
        except Exception as e:
            print(f"Error executing query {q}: {e}")
            import traceback
            traceback.print_exc()

    await session.close()

if __name__ == "__main__":
    # Suppress httpx info logs for cleaner output
    logging.getLogger("httpx").setLevel(logging.WARNING)
    print("--- RUN 1 (Event Loop 1) ---")
    asyncio.run(test_live_qa())
    print("\n\n--- RUN 2 (Event Loop 2) ---")
    asyncio.run(test_live_qa())
