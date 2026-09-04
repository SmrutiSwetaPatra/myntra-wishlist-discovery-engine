import asyncio
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db.session import AsyncSessionLocal
from app.engine.retriever import NumPyVectorStore

async def diagnose_retrieval():
    retriever = NumPyVectorStore()
    async with AsyncSessionLocal() as session:
        print("Loading documents...")
        await retriever.load(session)
        
    print(f"\n1. Total records loaded into Retriever: {len(retriever.documents)}")
    
    # Are the 73 Opportunity radar records available?
    # Count validation statuses
    counts = {}
    for doc in retriever.documents:
        counts[doc.validation_status] = counts.get(doc.validation_status, 0) + 1
        
    print("\n2. Breakdown of validation statuses loaded:")
    for k, v in counts.items():
        print(f"  {k}: {v}")
        
    queries = [
        "Why do users save fashion products to their wishlist?",
        "wishlist",
        "wishlist capacity",
        "compare saved products",
        "purchase barriers"
    ]
    
    print("\n3. Testing Semantic Search (No Filters)")
    for q in queries:
        print(f"\n--- Query: '{q}' ---")
        docs = await retriever.search(query=q, top_k=5, validation_status_in=None, metadata_filters=None)
        print(f"Retrieved {len(docs)} documents.")
        for i, d in enumerate(docs):
            print(f"  {i+1}. [ID: {d.conversation_id}] {d.validation_status} (Score: {d.metadata.get('retrieval_score', 0):.3f})")
            
    print("\n4. Testing Semantic Search (With metadata_filters = {'wishlist_behavior': '__not_null__'})")
    for q in queries:
        docs = await retriever.search(query=q, top_k=5, validation_status_in=None, metadata_filters={"wishlist_behavior": "__not_null__"})
        print(f"  Query '{q}': {len(docs)} docs returned.")
        
    print("\n5. Testing Semantic Search (With validation_status_filter = ['validated_relevant'])")
    for q in queries:
        docs = await retriever.search(query=q, top_k=5, validation_status_in=["validated_relevant"], metadata_filters=None)
        print(f"  Query '{q}': {len(docs)} docs returned.")

if __name__ == "__main__":
    asyncio.run(diagnose_retrieval())
