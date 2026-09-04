import asyncio
import json
from app.engine.copilot import DiscoveryCopilot
from app.db.session import AsyncSessionLocal
from app.core.logging import setup_logging

TEST_QUESTIONS = [
    {"id": "q02", "question": "How often do users review their wishlist before making a final purchase?", "expected": "partially_answerable"},
    {"id": "q06", "question": "Are shipping delays a major pre-purchase barrier compared to quality issues?", "expected": "partially_answerable"},
    {"id": "q16", "question": "How do sizing issues prevent users from converting?", "expected": "answerable"},
    {"id": "q18", "question": "Are fit issues more prominent in formal wear (suits/blazers) than in casual clothing?", "expected": "partially_answerable"},
    {"id": "q19", "question": "How do hidden fees at checkout impact user behavior?", "expected": "answerable"},
    {"id": "q34", "question": "How do the barriers faced by users in the 'decision' stage differ from those in the 'discovery' stage?", "expected": "answerable"},
    {"id": "q38", "question": "Are trust issues mentioned more frequently on the App Store or YouTube?", "expected": "partially_answerable"},
    {"id": "q45", "question": "Based on sizing friction, what feature could be implemented to increase conversion?", "expected": "answerable"},
    {"id": "q56", "question": "What evidence supports the claim that hidden fees cause cart abandonment?", "expected": "partially_answerable"},
    {"id": "q61", "question": "What evidence directly connects wishlist behavior to purchase decisions?", "expected": "partially_answerable"}
]

async def run_regression_test():
    setup_logging()
    print("--- Starting Targeted 10-Question Regression Test ---")
    copilot = DiscoveryCopilot()
    
    async with AsyncSessionLocal() as session:
        await copilot.initialize(session)
        
    print(f"Loaded {len(copilot.retriever.documents)} documents into vector store.\n")
    
    for i, q in enumerate(TEST_QUESTIONS, 1):
        print(f"\n======================================")
        print(f"Q{i} ({q['id']}): {q['question']}")
        print(f"Expected: {q['expected']}")
        print(f"======================================")
        
        response = await copilot.query(q['question'], session_id="test_session")
        
        print(f"\n[Answer]")
        print(response.answer)
        print(f"\n[Type]: {response.query_type}")
        print(f"[Insufficient Ev]: {response.insufficient_evidence}")
        
        retrieved_ids = [c.conversation_id for c in response.evidence_cards]
        print(f"[Retrieved IDs ({len(retrieved_ids)})]: {retrieved_ids}")
        
        if response.metrics:
            print("\n[Metrics]")
            for m in response.metrics:
                print(f"  - {m}")
                
if __name__ == "__main__":
    asyncio.run(run_regression_test())
