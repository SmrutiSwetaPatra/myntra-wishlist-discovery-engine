import asyncio
import json
from app.engine.copilot import DiscoveryCopilot
from app.db.session import AsyncSessionLocal
from app.core.logging import setup_logging

TEST_QUESTIONS = [
    "What prevents users from purchasing?", # A. Simple qualitative
    "What are the top barriers?", # B. Quantitative
    "Show high-intent users in the decision stage.", # C. Metadata
    "What is the actual wishlist-to-purchase conversion rate?", # F. Insufficient evidence
    "Use only human-validated evidence. Tell me about sizing issues." # E. Evidence restriction + Qualitative
]

async def run_live_test():
    setup_logging()
    print("--- Starting Phase 2 Copilot Live Test ---")
    copilot = DiscoveryCopilot()
    
    async with AsyncSessionLocal() as session:
        await copilot.initialize(session)
        
    print(f"Loaded {len(copilot.retriever.documents)} documents into vector store.\n")
    
    for i, q in enumerate(TEST_QUESTIONS, 1):
        print(f"\n======================================")
        print(f"Q{i}: {q}")
        print(f"======================================")
        
        # Test E triggers require_validated_only programmatically, or we rely on the router to catch it.
        # But we can also set the flag explicitly to be sure, based on the question string.
        require_validated = True if "validated evidence" in q else False
        
        response = await copilot.query(q, session_id="test_session", require_validated_only=require_validated)
        
        print(f"\n[Answer]")
        print(response.answer)
        print(f"\n[Type]: {response.query_type}")
        print(f"[Confidence]: {response.confidence}")
        print(f"[Insufficient Ev]: {response.insufficient_evidence}")
        
        if response.metrics:
            print("\n[Metrics]")
            for m in response.metrics:
                print(f"  - {m}")
                
        if response.limitations:
            print("\n[Limitations]")
            for limit in response.limitations:
                print(f"  - {limit}")

if __name__ == "__main__":
    asyncio.run(run_live_test())
