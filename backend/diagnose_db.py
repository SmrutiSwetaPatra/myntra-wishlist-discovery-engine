import asyncio
import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from sqlalchemy import select, and_, func
from sqlalchemy.orm import joinedload
from app.db.session import AsyncSessionLocal
from app.models.analyses import Analysis
from app.models.conversations import Conversation

async def diagnostic():
    async with AsyncSessionLocal() as session:
        # Total counts
        total_convs = await session.scalar(select(func.count(Conversation.id)))
        total_analyses = await session.scalar(select(func.count(Analysis.id)))
        
        established_tiers = [
            "validated_relevant",
            "ai_direct_evidence",
            "indirect_pre_purchase",
            "ai_indirect_evidence"
        ]
        
        established = await session.scalars(
            select(Analysis)
            .options(joinedload(Analysis.conversation))
            .where(Analysis.validation_status.in_(established_tiers))
        )
        established = established.all()
        
        print(f"Total Conversations: {total_convs}")
        print(f"Total Analyses: {total_analyses}")
        print(f"Total Established Evidence Records: {len(established)}")
        
        has_embedding = [a for a in established if a.embedding is not None]
        no_embedding = [a for a in established if a.embedding is None]
        
        print(f"  -> With Embeddings: {len(has_embedding)}")
        print(f"  -> Without Embeddings: {len(no_embedding)}")
        
        tier_counts_embedded = {t: 0 for t in established_tiers}
        tier_counts_unembedded = {t: 0 for t in established_tiers}
        
        for a in has_embedding:
            tier_counts_embedded[a.validation_status] += 1
            
        for a in no_embedding:
            tier_counts_unembedded[a.validation_status] += 1
            
        print("\nEmbedded breakdown by tier:")
        for t, c in tier_counts_embedded.items():
            print(f"  - {t}: {c}")
            
        print("\nUnembedded breakdown by tier:")
        for t, c in tier_counts_unembedded.items():
            print(f"  - {t}: {c}")
            
        # Is the wishlist-limit record embedded?
        wishlist_record = None
        for a in established:
            if a.validation_status == "validated_relevant":
                wishlist_record = a
                break
                
        if wishlist_record:
            print(f"\nWishlist-limit record (ID: {wishlist_record.id}):")
            print(f"  - Has Embedding: {wishlist_record.embedding is not None}")
            print(f"  - Text preview: {wishlist_record.conversation.raw_content[:150]}...")
        else:
            print("\nWishlist-limit record not found!")
            
        print("\n" + "="*50)
        print("MOCKED QUERY PIPELINE")
        print("="*50)
        
        queries = [
            {
                "id": 1,
                "q": "What prevents wishlisted products from being purchased?",
                "mock_router": {
                    "validation_status_filter": established_tiers,
                    "metadata_filters": {"shopping_stage": "consideration"}
                }
            },
            {
                "id": 2,
                "q": "Why do users save products but not buy them later?",
                "mock_router": {
                    "validation_status_filter": established_tiers,
                    "metadata_filters": None
                }
            },
            {
                "id": 3,
                "q": "How do users compare multiple shortlisted products?",
                "mock_router": {
                    "validation_status_filter": established_tiers,
                    "metadata_filters": {"comparison_behavior": "__not_null__"}
                }
            },
            {
                "id": 4,
                "q": "What do users need to know before buying a saved fashion product?",
                "mock_router": {
                    "validation_status_filter": established_tiers,
                    "metadata_filters": None
                }
            }
        ]
        
        for q in queries:
            print(f"\nQUERY {q['id']}: {q['q']}")
            print(f"  - Mock Router Output: {q['mock_router']}")
            
            # Count DB matches
            stmt = select(Analysis).where(Analysis.validation_status.in_(q["mock_router"]["validation_status_filter"]))
            
            if q["mock_router"]["metadata_filters"]:
                filters = q["mock_router"]["metadata_filters"]
                if "shopping_stage" in filters:
                    stmt = stmt.where(Analysis.shopping_stage == filters["shopping_stage"])
                if "comparison_behavior" in filters:
                    stmt = stmt.where(Analysis.comparison_behavior != None)
            
            matches = await session.scalars(stmt)
            matches = matches.all()
            
            print(f"  - DB Records matching router filters (all tiers): {len(matches)}")
            
            embedded_matches = [m for m in matches if m.embedding is not None]
            print(f"  - Matching records with NON-NULL embeddings: {len(embedded_matches)}")
            
            # Semantic fallback logic simulation
            passed_to_semantic = len(embedded_matches)
            if passed_to_semantic < 15:
                print("  - Semantic fallback triggered (docs < 15) -> padding to 15 without metadata filters!")
                fallback_matches = [m for m in has_embedding]  # All embedded usable tiers
                print(f"  - Padded pool size: {min(15, len(fallback_matches))}")
            else:
                print(f"  - Pool size: {passed_to_semantic}")

if __name__ == "__main__":
    asyncio.run(diagnostic())
