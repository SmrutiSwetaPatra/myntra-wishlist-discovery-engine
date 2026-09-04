import asyncio
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.engine.gemini import GeminiClient

async def test():
    c = GeminiClient()
    res = await c.client.aio.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents="hi"
    )
    print("Success:", res.text)

if __name__ == "__main__":
    asyncio.run(test())
