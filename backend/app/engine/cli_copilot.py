import asyncio
import argparse
import sys
from app.engine.copilot import DiscoveryCopilot
from app.db.session import AsyncSessionLocal
from app.core.logging import setup_logging

async def run_cli(require_validated: bool):
    setup_logging()
    print("Initializing Discovery Copilot...")
    copilot = DiscoveryCopilot()
    
    async with AsyncSessionLocal() as session:
        await copilot.initialize(session)
        
    print("\nCopilot is ready! Type 'exit' to quit.")
    print("Mode:", "Validated Evidence Only" if require_validated else "All Evidence")
    
    session_id = "cli_session"
    
    while True:
        try:
            query = input("\nYou: ")
            if query.lower() in ['exit', 'quit']:
                break
            if not query.strip():
                continue
                
            print("\nThinking...")
            response = await copilot.query(query, session_id=session_id, require_validated_only=require_validated)
            
            print(f"\n[Copilot] (Confidence: {response.confidence} | Type: {response.query_type})")
            print(f"{response.answer}\n")
            
            if response.metrics:
                print("--- Metrics ---")
                for m in response.metrics:
                    print(m)
                    
            if response.evidence_cards:
                print(f"\n--- Top Supporting Evidence ({len(response.evidence_cards)} cards) ---")
                for card in response.evidence_cards[:2]:
                    print(f"[{card.conversation_id}] ({card.validation_status}) - {card.source}")
                    text_snip = card.raw_text[:100].replace('\n', ' ')
                    print(f"  \"{text_snip}...\"")
                    
            if response.limitations:
                print("\n--- Limitations ---")
                for limit in response.limitations:
                    print(f"- {limit}")
                    
        except EOFError:
            break
        except Exception as e:
            print(f"\nError: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Discovery Copilot CLI")
    parser.add_argument("--validated-only", action="store_true", help="Restrict answers to validated evidence only")
    args = parser.parse_args()
    
    asyncio.run(run_cli(args.validated_only))
