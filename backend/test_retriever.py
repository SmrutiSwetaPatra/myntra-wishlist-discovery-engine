import asyncio
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db.session import AsyncSessionLocal
from app.engine.retriever import NumPyVectorStore

async def test_retriever():
    retriever = NumPyVectorStore()
    async with AsyncSessionLocal() as session:
        await retriever.load(session)
        
    print(f"Loaded {len(retriever.documents)} documents.")
    
    query = "Why do users save fashion products to their wishlist?"
    query_emb = await retriever.embedder.generate_embedding(query)
    
    import numpy as np
    q_vec = np.array(query_emb, dtype=np.float32)
    from app.engine.retriever import cosine_similarity
    
    similarities = cosine_similarity(q_vec, retriever.embeddings)
    
    sorted_idx = np.argsort(similarities)[::-1]
    
    print("\n--- Top 10 Raw Similarities ---")
    for i in range(10):
        idx = sorted_idx[i]
        doc = retriever.documents[idx]
        print(f"{doc.validation_status}: {similarities[idx]:.3f} - {doc.text[:50]}")

if __name__ == "__main__":
    asyncio.run(test_retriever())
