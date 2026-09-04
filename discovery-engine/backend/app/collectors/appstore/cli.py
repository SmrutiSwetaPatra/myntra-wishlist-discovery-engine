import argparse
import asyncio
import logging

from app.db.session import AsyncSessionLocal
from app.collectors.appstore.collector import AppStoreCollector

logging.basicConfig(level=logging.INFO)

async def run_cli():
    parser = argparse.ArgumentParser(description="Apple App Store Data Collector")
    parser.add_argument("--app-name", type=str, default="myntra-fashion-shopping-app", help="App name")
    parser.add_argument("--app-id", type=int, default=907394059, help="App ID")
    parser.add_argument("--country", type=str, default="in", help="Country code")
    parser.add_argument("--max-reviews", type=int, default=1000, help="Max total reviews to collect")
    parser.add_argument("--dry-run", action="store_true", help="Do not save to database")
    
    args = parser.parse_args()

    async with AsyncSessionLocal() as db:
        collector = AppStoreCollector(
            db_session=db,
            app_name=args.app_name,
            app_id=args.app_id,
            country=args.country,
            max_reviews=args.max_reviews,
            dry_run=args.dry_run
        )
        await collector.run()

if __name__ == "__main__":
    asyncio.run(run_cli())
