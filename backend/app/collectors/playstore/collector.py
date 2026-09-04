import logging
import asyncio
from datetime import datetime, timezone
from typing import List, Dict, Any, Optional, Tuple
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError
from google_play_scraper import reviews, Sort

from app.models.sources import Source
from app.models.collection_runs import CollectionRun
from app.models.conversations import Conversation

logger = logging.getLogger(__name__)

class PlayStoreCollector:
    def __init__(
        self,
        db_session: AsyncSession,
        app_id: str = "com.myntra.android",
        lang: str = "en",
        country: str = "in",
        max_reviews: int = 1000,
        dry_run: bool = False
    ):
        self.db = db_session
        self.app_id = app_id
        self.lang = lang
        self.country = country
        self.max_reviews = max_reviews
        self.dry_run = dry_run
        
        self.source = None
        self.run_record = None

    async def initialize_run(self) -> None:
        if self.dry_run:
            logger.info("DRY RUN: Skipping DB initialization")
            return

        result = await self.db.execute(select(Source).where(Source.platform == "playstore"))
        self.source = result.scalars().first()
        if not self.source:
            self.source = Source(
                platform="playstore",
                name="Google Play Store",
                base_url="https://play.google.com/store/apps"
            )
            self.db.add(self.source)
            await self.db.flush()

        self.run_record = CollectionRun(
            source_id=self.source.id,
            status="running"
        )
        self.db.add(self.run_record)
        await self.db.commit()

    async def _insert_or_ignore_conversation(self, conv_data: Dict[str, Any]) -> int:
        if self.dry_run:
            return 1

        try:
            async with self.db.begin_nested():
                conv = Conversation(**conv_data)
                self.db.add(conv)
                await self.db.flush()
                return 1
        except IntegrityError:
            return 0

    def _fetch_reviews_sync(self, continuation_token=None) -> Tuple[List[Dict[str, Any]], Any]:
        result, continuation = reviews(
            self.app_id,
            lang=self.lang,
            country=self.country,
            sort=Sort.NEWEST,
            count=min(200, self.max_reviews), # Fetch in chunks of 200
            continuation_token=continuation_token
        )
        return result, continuation

    def _is_valid_review(self, r: Dict[str, Any]) -> bool:
        if not r: return False
        content = r.get("content")
        if not content or not isinstance(content, str):
            return False
        if not content.strip():
            return False
        return True

    def _normalize(self, r: Dict[str, Any]) -> Dict[str, Any]:
        dt = r.get("at")
        if dt and dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
            
        return {
            "external_id": str(r.get("reviewId")),
            "raw_content": r.get("content").strip(),
            "author": r.get("userName", "Anonymous"),
            "timestamp": dt,
            "source_url": f"https://play.google.com/store/apps/details?id={self.app_id}&reviewId={r.get('reviewId')}",
            "metadata_": {
                "rating": r.get("score"),
                "app_version": r.get("reviewCreatedVersion"),
                "thumbs_up_count": r.get("thumbsUpCount", 0),
                "reply_content": r.get("replyContent"),
                "replied_at": r.get("repliedAt").isoformat() if r.get("repliedAt") else None,
                "app_id": self.app_id
            }
        }

    async def run(self) -> None:
        await self.initialize_run()
        total_fetched = 0
        total_new = 0
        total_dup = 0
        error_msg = None
        
        continuation = None

        try:
            while total_fetched < self.max_reviews:
                logger.info(f"Fetching chunk from Play Store... Current total: {total_fetched}")
                
                result, continuation = await asyncio.to_thread(self._fetch_reviews_sync, continuation)
                
                if not result:
                    break
                    
                for r in result:
                    if total_fetched >= self.max_reviews:
                        break
                        
                    if not self._is_valid_review(r):
                        continue

                    normalized = self._normalize(r)
                    
                    if not self.dry_run:
                        normalized["source_id"] = self.source.id
                        normalized["collection_run_id"] = self.run_record.id

                    is_new = await self._insert_or_ignore_conversation(normalized)
                    total_fetched += 1
                    if is_new:
                        total_new += 1
                    else:
                        total_dup += 1

                if not continuation:
                    break

        except Exception as e:
            logger.error(f"Play Store Collection run failed: {str(e)}")
            error_msg = str(e)
        finally:
            if not self.dry_run and self.run_record:
                self.run_record.end_time = datetime.now(timezone.utc)
                self.run_record.status = "error" if error_msg else "completed"
                self.run_record.records_fetched = total_fetched
                self.run_record.records_new = total_new
                self.run_record.records_duplicate = total_dup
                self.run_record.error_message = error_msg
                await self.db.commit()

            logger.info(
                f"Play Store Run Finished. Fetched: {total_fetched}, New: {total_new}, "
                f"Dup: {total_dup}, DryRun: {self.dry_run}, Error: {error_msg}"
            )
