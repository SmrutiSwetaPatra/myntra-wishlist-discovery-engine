import asyncio
from app.db.session import AsyncSessionLocal
from sqlalchemy import text

async def run():
    async with AsyncSessionLocal() as db:
        res = await db.execute(text("SELECT platform, COUNT(*) FROM conversations c JOIN sources s ON c.source_id = s.id GROUP BY platform"))
        print('--- COUNTS ---')
        for row in res:
            print(f'{row[0]}: {row[1]}')
            
        res = await db.execute(text("SELECT platform, external_id, raw_content, timestamp, source_url, c.metadata FROM conversations c JOIN sources s ON c.source_id = s.id"))
        rows = res.fetchall()
        from collections import defaultdict
        grouped = defaultdict(list)
        for r in rows:
            grouped[r[0]].append(r)
            
        print('\n--- SAMPLES ---')
        with open('dump_output.txt', 'w', encoding='utf-8') as f:
            for platform, items in grouped.items():
                f.write(f'\n=== {platform} ===\n')
                for i, r in enumerate(items[:5]):
                    f.write(f'Record {i+1}:\n')
                    f.write(f'external_id: {r[1]}\n')
                    f.write(f'timestamp: {r[3]}\n')
                    f.write(f'source_url: {r[4]}\n')
                    f.write(f'metadata: {r[5]}\n')
                    f.write(f'raw_content: {r[2][:200]}...\n\n')

if __name__ == "__main__":
    asyncio.run(run())
