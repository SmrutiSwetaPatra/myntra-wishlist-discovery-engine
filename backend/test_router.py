import asyncio
import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from app.engine.router import QueryRouter

async def test():
    r = QueryRouter()
    q1 = 'What prevents wishlisted products from being purchased?'
    q2 = 'Why do users save products but not buy them later?'
    
    print("Q1:", q1)
    plan1 = await r.route(q1)
    print(plan1.model_dump_json(indent=2))
    
    print("\nQ2:", q2)
    plan2 = await r.route(q2)
    print(plan2.model_dump_json(indent=2))

if __name__ == "__main__":
    asyncio.run(test())
