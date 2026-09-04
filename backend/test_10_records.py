import asyncio
import logging
from app.engine.pipeline import AIPipeline
from app.db.session import AsyncSessionLocal
from app.models.analyses import Analysis
from app.models.conversations import Conversation
from sqlalchemy.future import select

logging.basicConfig(level=logging.INFO)

async def test_10_records():
    async with AsyncSessionLocal() as db:
        pipeline = AIPipeline(db)
        
        # Get processed ids (all of them)
        result = await db.execute(select(Analysis.conversation_id))
        processed_ids = {str(row[0]) for row in result.all()}
        
        # Get all conversations
        result_convs = await db.execute(select(Conversation))
        all_convs = result_convs.scalars().all()
        
        to_process = [c for c in all_convs if str(c.id) not in processed_ids][:10]
        
        print(f"Starting test with {len(to_process)} records...")
        
        tasks = []
        for conv in to_process:
            tasks.append(pipeline.process_conversation(conv))
            
        await asyncio.gather(*tasks)
        
        print("Test finished.")

if __name__ == '__main__':
    asyncio.run(test_10_records())
