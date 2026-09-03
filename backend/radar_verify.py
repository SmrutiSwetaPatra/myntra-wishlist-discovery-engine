import asyncio
from ui.radar_db import _get_opportunities

async def run_diagnostic():
    opportunities = await _get_opportunities()
    print("--- After Update ---")
    for opp in opportunities:
        print(f"\nCategory: {opp['barrier']}")
        print(f"Display Need: {opp['unmet_need']}")
        print(f"Total Volume: {opp['volume']}")
        print(f"Direct Evidence: {opp['direct_count']}")
        print(f"Indirect Evidence: {opp['indirect_count']}")
        print(f"Strength: {opp['strength']}")
        
        # Check exact matches in 'all_reviews' (simulating the inner logic to count available exact matches)
        # Note: the opp dict only gives us representative_reviews now, but we can infer exact matches >= len(rep)
        rep_count = len(opp['representative_reviews'])
        print(f"Representative Evidence Displayed: {rep_count}")
        
if __name__ == "__main__":
    asyncio.run(run_diagnostic())
