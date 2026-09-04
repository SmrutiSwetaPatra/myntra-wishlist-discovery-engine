import asyncio
import logging
from app.db.session import AsyncSessionLocal
from app.engine.router import QueryRouter
from app.engine.retriever import NumPyVectorStore

logger = logging.getLogger(__name__)

TEST_QUESTIONS = [
    "Why do users add fashion products to their wishlist?",
    "What prevents wishlisted products from eventually being purchased?",
    "What uncertainties remain after users identify a product?",
    "What causes users to postpone purchases?",
    "How do users compare shortlisted products?",
    "What information do users seek outside Myntra before purchasing?",
    "What role do fit, size, styling, price, reviews, occasion and social validation play?",
    "When is wishlist usage genuine purchase intent vs bookmarking?",
    "How do behaviors differ across user segments?",
    "What unmet needs emerge consistently?",
    "What percentage of users abandon because of price?",
    "How does YouTube sentiment differ from Google Play?",
    "Show me only validated evidence about poor stitching.",
    "What is the exact conversion rate from wishlist to purchase?",
    "Are men or women more likely to complain about fit?",
    "Show me users with high purchase intent in the decision stage.",
    "What are the top 3 barriers overall?",
    "How many users use workarounds to fix issues?",
    "What do users do when their desired size is unavailable?",
    "Give me evidence of deceptive pricing during sales."
]

async def run_benchmark():
    print("--- Starting Eval Benchmark ---")
    
    router = QueryRouter()
    retriever = NumPyVectorStore()
    
    # Load vector store
    async with AsyncSessionLocal() as session:
        await retriever.load(session)
        
    print(f"Loaded {len(retriever.documents)} documents into vector store.\n")
    
    for i, q in enumerate(TEST_QUESTIONS, 1):
        print(f"Q{i}: {q}")
        
        # 1. Test Router
        plan = await router.route(q)
        print(f"  [Router Plan]:")
        print(f"    - Quantitative: {plan.is_quantitative}")
        print(f"    - Cross-Source: {plan.requires_cross_source}")
        print(f"    - Segmentation: {plan.requires_segmentation}")
        print(f"    - Insufficient Ev: {plan.insufficient_evidence_likely}")
        print(f"    - Metadata Filter: {plan.metadata_filters}")
        print(f"    - Validation Filter: {plan.validation_status_filter}")
        print(f"    - Semantic Query: {plan.semantic_query}")
        
        # 2. Test Retrieval (if semantic)
        if not plan.insufficient_evidence_likely:
            results = await retriever.search(
                query=plan.semantic_query, 
                top_k=3,
                validation_status_in=plan.validation_status_filter,
                metadata_filters=plan.metadata_filters
            )
            print(f"  [Retrieval Results ({len(results)} found)]:")
            for j, doc in enumerate(results, 1):
                score = doc.metadata.get('retrieval_score', 0)
                print(f"    {j}. [{doc.validation_status}] (Score: {score:.2f}) -> {doc.text[:60]}...")
        else:
            print("  [Retrieval Skipped]: Insufficient evidence likely.")
            
        print("-" * 50)

if __name__ == "__main__":
    asyncio.run(run_benchmark())
