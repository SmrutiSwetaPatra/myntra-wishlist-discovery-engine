import asyncio
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.engine.copilot import DiscoveryCopilot

async def test_copilot():
    copilot = DiscoveryCopilot()
    
    questions = [
        "What are the biggest pre-purchase barriers?",
        "Why do users postpone purchases?",
        "What are the biggest sizing problems?",
        "What are the biggest pricing problems?",
        "What trust issues do users have?",
        "Show me evidence related to sizing.",
        "Show me evidence related to pricing.",
        "Compare pricing vs sizing.",
        "Which problem has the strongest direct evidence?",
        "Which problem has the highest evidence volume?",
        "What unmet needs appear repeatedly?",
        "What workarounds do users use?",
        "Compare Google Play and Apple App Store.",
        "What evidence directly connects wishlist behavior to purchase decisions?",
        "What can this dataset tell us about wishlist-to-purchase conversion?"
    ]
    
    for i, q in enumerate(questions):
        print(f"\n--- Q{i+1}: {q} ---")
        try:
            res = await copilot.query(q, "test_session")
            print(f"ANSWER:\n{res.answer[:300]}...\n")
            print(f"METRICS: {res.metrics}")
            print(f"EVIDENCE: {[c['id'] for c in res.evidence_cards]}")
        except Exception as e:
            print(f"ERROR: {e}")

if __name__ == "__main__":
    asyncio.run(test_copilot())
