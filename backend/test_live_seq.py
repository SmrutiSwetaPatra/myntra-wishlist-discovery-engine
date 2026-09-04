import asyncio
import sys
import os

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
        try:
            res = await copilot.query(query, session_id="streamlit_session")
            print(f"Answer: {res.answer[:150]}...")
            print(f"Evidence retrieved: {len(res.evidence_cards)} records")
            for j, ev in enumerate(res.evidence_cards, 1):
                print(f"  [Evidence {j}] Tier: {ev.validation_status} | Category: {ev.metadata.get('primary_barrier_category')}")
        except Exception as e:
            print(f"Error executing query {i}: {e}")
        print("Sleeping to respect rate limit...")
        await asyncio.sleep(60)

if __name__ == "__main__":
    asyncio.run(run_sequence())
