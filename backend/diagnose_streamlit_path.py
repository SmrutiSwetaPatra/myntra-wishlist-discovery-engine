import asyncio
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db.session import AsyncSessionLocal
from app.engine.copilot import DiscoveryCopilot

async def run_sequence():
    copilot = DiscoveryCopilot()
    async with AsyncSessionLocal() as session:
        await copilot.initialize(session)
        
    queries = [
        "Why do users save fashion products to their wishlist?",
        "What prevents wishlisted products from being purchased?",
        "What are the biggest pre-purchase barriers?"
    ]
    
    for i, query in enumerate(queries, 1):
        print(f"\n{'='*50}\nEXECUTING QUERY {i}: {query}\n{'='*50}")
        
        # Manually trace the steps of copilot.query()
        plan = await copilot.router.route(query, False)
        print("1. ROUTER OUTPUT:")
        print(f"   Semantic Query: {plan.semantic_query}")
        print(f"   Metadata Filters: {plan.metadata_filters}")
        print(f"   Validation Filter: {plan.validation_status_filter}")
        
        # Initial retrieval
        import numpy as np
        from app.engine.retriever import cosine_similarity
        
        query_embedding = await copilot.retriever.embedder.generate_embedding(plan.semantic_query)
        q_vec = np.array(query_embedding, dtype=np.float32)
        similarities = cosine_similarity(q_vec, copilot.retriever.embeddings)
        
        for idx, doc in enumerate(copilot.retriever.documents):
            if doc.validation_status in ['validated_relevant', 'ai_direct_evidence']:
                similarities[idx] += 0.15
            elif doc.validation_status in ['indirect_pre_purchase', 'ai_indirect_evidence']:
                similarities[idx] += 0.05
            elif doc.validation_status.startswith('excluded'):
                similarities[idx] -= 0.50
                
        valid_indices = np.argsort(similarities)[::-1]
        print(f"\n2. CANDIDATE COUNT BEFORE METADATA FILTERING: {len(valid_indices)}")
        
        docs = []
        for idx in valid_indices:
            doc = copilot.retriever.documents[idx]
            if plan.validation_status_filter and doc.validation_status not in plan.validation_status_filter:
                continue
            if plan.metadata_filters:
                match = True
                for k, v in plan.metadata_filters.items():
                    if doc.metadata.get(k) != v:
                        match = False
                        break
                if not match:
                    continue
            docs.append(doc)
            if len(docs) >= 15:
                break
                
        print(f"3. CANDIDATE COUNT AFTER METADATA FILTERING: {len(docs)}")
        print("4. INITIAL CANDIDATES:")
        for doc in docs:
            idx = copilot.retriever.documents.index(doc)
            print(f"   - ID: {doc.conversation_id[:8]} | Barrier: {doc.metadata.get('primary_barrier_category')} | Status: {doc.validation_status}")
            
        print(f"5. CANDIDATE COUNT RETURNED BY SEMANTIC VECTOR SEARCH: {len(docs)}")
        
        print("\n6. TOP 15 SEMANTIC CANDIDATES (Regardless of Metadata):")
        top_15 = []
        for idx in valid_indices[:15]:
            doc = copilot.retriever.documents[idx]
            top_15.append(doc)
            print(f"   - ID: {doc.conversation_id[:8]} | Barrier: {doc.metadata.get('primary_barrier_category')} | Sim: {similarities[idx]:.3f} | {doc.validation_status}")
            
        # Fallback padding
        if len(docs) < 15 and plan.metadata_filters:
            print("\nSEMANTIC FALLBACK TRIGGERED (Padding to 15 without metadata filters)")
            fallback_docs = []
            for idx in valid_indices:
                doc = copilot.retriever.documents[idx]
                if plan.validation_status_filter and doc.validation_status not in plan.validation_status_filter:
                    continue
                fallback_docs.append(doc)
                if len(fallback_docs) >= 15:
                    break
                    
            seen = {d.conversation_id for d in docs}
            for d in fallback_docs:
                if d.conversation_id not in seen:
                    docs.append(d)
                    seen.add(d.conversation_id)
            docs = docs[:15]
            
        print(f"\n7. CANDIDATE COUNT AFTER MERGE/PADDING: {len(docs)}")
        
        print(f"\n8. PASSED INTO RELEVANCE GATE: {len(docs)}")
        
        from app.engine.schemas import QueryRelevanceDecision
        from app.engine.prompts import QUERY_RELEVANCE_PROMPT
        
        surviving = []
        print("\n9. RELEVANCE GATE DECISIONS:")
        for doc in docs:
            prompt = QUERY_RELEVANCE_PROMPT.format(query=query, evidence=doc.text)
            try:
                decision = await copilot.client.extract_structured(prompt, "", QueryRelevanceDecision)
                if decision.relevant and decision.relevance_score >= 0.6:
                    surviving.append((doc, decision))
                    print(f"   [PASS] ID: {doc.conversation_id[:8]} | Score: {decision.relevance_score:.2f} | Reason: {decision.reason}")
                else:
                    print(f"   [FAIL] ID: {doc.conversation_id[:8]} | Score: {decision.relevance_score:.2f} | Reason: {decision.reason}")
            except Exception as e:
                print(f"   [ERROR] ID: {doc.conversation_id[:8]} | {e}")
                
        print(f"\n10. SURVIVED RELEVANCE GATE: {len(surviving)}")
        
        final_docs = [d[0] for d in surviving][:5]
        print(f"\n11. FINAL PASSED TO SYNTHESIS: {len(final_docs)}")
        
        print("\n12. FINAL EVIDENCE LIST:")
        for doc in final_docs:
            print(f"   - ID: {doc.conversation_id[:8]} | Barrier: {doc.metadata.get('primary_barrier_category')} | Status: {doc.validation_status}")
            
        # Mock actual query state update
        res = await copilot.query(query, session_id="streamlit_session")
        print(f"\nACTUAL COPILOT SYNTHESIS RETURNED {len(res.evidence_cards)} CARDS")

if __name__ == "__main__":
    asyncio.run(run_sequence())
