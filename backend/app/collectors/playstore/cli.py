import argparse
import asyncio
import logging

from app.db.session import AsyncSessionLocal
from app.collectors.playstore.collector import PlayStoreCollector

logging.basicConfig(level=logging.INFO)

async def run_cli():
    parser = argparse.ArgumentParser(description="Google Play Store Data Collector")
    parser.add_argument("--app-id", type=str, default="com.myntra.android", help="App package ID")
    parser.add_argument("--lang", type=str, default="en", help="Language code")
    parser.add_argument("--country", type=str, default="in", help="Country code")
    parser.add_argument("--max-reviews", type=int, default=1000, help="Max total reviews to collect")
    parser.add_argument("--dry-run", action="store_true", help="Do not save to database")
    
    args = parser.parse_args()

    async with AsyncSessionLocal() as db:
        collector = PlayStoreCollector(
            db_session=db,
            app_id=args.app_id,
            lang=args.lang,
            country=args.country,
            max_reviews=args.max_reviews,
            dry_run=args.dry_run
        )
        await collector.run()

if __name__ == "__main__":
    asyncio.run(run_cli())
