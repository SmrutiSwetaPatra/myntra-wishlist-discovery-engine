import asyncio
import os
from dotenv import load_dotenv
from google import genai
from pydantic import BaseModel

load_dotenv()
client = genai.Client(api_key=os.getenv('GEMINI_API_KEY'))

class Output(BaseModel):
    message: str

async def test():
    resp = await client.aio.models.generate_content(
        model='gemini-3.5-flash-lite',
        contents='Say hello in JSON',
        config=genai.types.GenerateContentConfig(
            response_mime_type='application/json',
            response_schema=Output
        )
    )
    print(resp.text)

if __name__ == '__main__':
    asyncio.run(test())
