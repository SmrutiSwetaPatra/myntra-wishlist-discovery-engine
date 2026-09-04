import asyncio
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.engine.gemini import GeminiClient
from google import genai
from app.core.config import settings

async def test():
    client = genai.Client(api_key=settings.GEMINI_API_KEY)
    try:
        res = await client.aio.models.generate_content(
            model="gemini-1.5-flash",
            contents="hi"
        )
        print("1.5-flash Success:", res.text)
    except Exception as e:
        print("1.5-flash Failed:", e)
        
    try:
        res = await client.aio.models.generate_content(
            model="gemini-3.6-flash",
            contents="hi"
        )
        print("3.6-flash Success:", res.text)
    except Exception as e:
        print("3.6-flash Failed:", e)

if __name__ == "__main__":
    asyncio.run(test())
