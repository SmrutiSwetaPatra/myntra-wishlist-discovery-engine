import argparse
import asyncio
from typing import List

from app.core.config import settings
from app.db.session import AsyncSessionLocal
from app.collectors.youtube.config import DEFAULT_QUERIES, DEFAULT_REGION_CODE, DEFAULT_RELEVANCE_LANGUAGE
from app.collectors.youtube.collector import YouTubeCollector

async def run_cli():
    parser = argparse.ArgumentParser(description="YouTube Data Collector")
    parser.add_argument("--queries", nargs="+", default=DEFAULT_QUERIES, help="List of queries to search")
    parser.add_argument("--max-videos", type=int, default=5, help="Max videos per query")
    parser.add_argument("--max-comments", type=int, default=100, help="Max comments per video")
    parser.add_argument("--max-total", type=int, default=500, help="Max total comments per run")
    parser.add_argument("--dry-run", action="store_true", help="Do not save to database")
    
    args = parser.parse_args()

    api_key = settings.YOUTUBE_API_KEY
    if not api_key:
        print("ERROR: YOUTUBE_API_KEY environment variable is not set.")
        return

    async with AsyncSessionLocal() as db:
        collector = YouTubeCollector(
            api_key=api_key,
            db_session=db,
            queries=args.queries,
            region_code=DEFAULT_REGION_CODE,
            relevance_language=DEFAULT_RELEVANCE_LANGUAGE,
            max_videos_per_query=args.max_videos,
            max_comments_per_video=args.max_comments,
            max_total_comments_per_run=args.max_total,
            dry_run=args.dry_run
        )
        await collector.run()

if __name__ == "__main__":
    asyncio.run(run_cli())
