import logging
import asyncio
import hashlib
import httpx
from datetime import datetime, timezone
from typing import List, Dict, Any, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError
from app_store_scraper import AppStore

from app.models.sources import Source
from app.models.collection_runs import CollectionRun
from app.models.conversations import Conversation

logger = logging.getLogger(__name__)

class AppStoreCollector:
    def __init__(
        self,
        db_session: AsyncSession,
        app_name: str = "myntra-fashion-shopping-app",
        app_id: int = 907394059,
        country: str = "in",
        max_reviews: int = 1000,
        dry_run: bool = False
    ):
        self.db = db_session
        self.app_name = app_name
        self.app_id = app_id
        self.country = country
        self.max_reviews = max_reviews
        self.dry_run = dry_run
        
        self.source = None
        self.run_record = None

    async def initialize_run(self) -> None:
        if self.dry_run:
            logger.info("DRY RUN: Skipping DB initialization")
            return

        result = await self.db.execute(select(Source).where(Source.platform == "appstore"))
        self.source = result.scalars().first()
        if not self.source:
            self.source = Source(
                platform="appstore",
                name="Apple App Store",
                base_url="https://apps.apple.com"
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

    def _fetch_reviews_primary_sync(self) -> List[Dict[str, Any]]:
        store = AppStore(country=self.country, app_name=self.app_name, app_id=self.app_id)
        store.review(how_many=self.max_reviews)
        return store.reviews

    async def _fetch_reviews_rss(self) -> List[Dict[str, Any]]:
        """Fallback method using public Apple RSS endpoint"""
        reviews = []
        # RSS supports up to 10 pages, 50 reviews each (max 500)
        pages = min(10, (self.max_reviews // 50) + (1 if self.max_reviews % 50 > 0 else 0))
        if pages == 0: pages = 1
        
        async with httpx.AsyncClient() as client:
            for page in range(1, pages + 1):
                url = f"https://itunes.apple.com/{self.country}/rss/customerreviews/page={page}/id={self.app_id}/sortBy=mostRecent/json"
                try:
                    r = await client.get(url, timeout=10.0)
                    r.raise_for_status()
                    data = r.json()
                    entries = data.get("feed", {}).get("entry", [])
                    
                    if not entries:
                        break
                        
                    # First entry in page 1 is often the app metadata itself, if it lacks author it's app data
                    for entry in entries:
                        if "author" not in entry:
                            continue
                            
                        # Normalize to match primary dict format as closely as possible for _is_valid_review
                        try:
                            # date parsing: "2023-11-20T03:52:13-07:00"
                            dt_str = entry.get("updated", {}).get("label")
                            dt = datetime.fromisoformat(dt_str).astimezone(timezone.utc) if dt_str else datetime.now(timezone.utc)
                            
                            reviews.append({
                                "id": entry.get("id", {}).get("label"),
                                "userName": entry.get("author", {}).get("name", {}).get("label"),
                                "title": entry.get("title", {}).get("label"),
                                "review": entry.get("content", {}).get("label"),
                                "rating": int(entry.get("im:rating", {}).get("label", 0)),
                                "isEdited": None,
                                "version": entry.get("im:version", {}).get("label"),
                                "date": dt,
                                "developerResponse": None  # RSS doesn't typically provide developer responses
                            })
                        except Exception as parse_e:
                            logger.warning(f"Error parsing RSS entry: {parse_e}")
                            
                    if len(entries) < 50:
                        break # Last page
                except Exception as e:
                    logger.error(f"Error fetching RSS page {page}: {e}")
                    break
                    
        return reviews

    def _is_valid_review(self, r: Dict[str, Any]) -> bool:
        if not r: return False
        content = r.get("review")
        if not content or not isinstance(content, str):
            return False
        if not content.strip():
            return False
        return True

    def _normalize(self, r: Dict[str, Any], method: str) -> Dict[str, Any]:
        dt = r.get("date")
        if dt and dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
            
        title = r.get("title", "").strip()
        review_text = r.get("review", "").strip()
        if title:
            raw_content = f"{title}\n\n{review_text}"
        else:
            raw_content = review_text
            
        dev_resp = r.get("developerResponse")
        
        return {
            "external_id": str(r.get("id", "")),
            "raw_content": raw_content,
            "author": r.get("userName", "Anonymous"),
            "timestamp": dt,
            "source_url": f"https://apps.apple.com/{self.country}/app/{self.app_name}/id{self.app_id}",
            "metadata_": {
                "rating": r.get("rating"),
                "is_edited": r.get("isEdited"),
                "app_version": r.get("version"),
                "reply_content": dev_resp.get("body") if dev_resp else None,
                "replied_at": dev_resp.get("modified").isoformat() if dev_resp and hasattr(dev_resp.get("modified"), 'isoformat') else str(dev_resp.get("modified")) if dev_resp and dev_resp.get("modified") else None,
                "app_id": self.app_id,
                "country": self.country,
                "acquisition_method": method
            }
        }

    async def run(self) -> None:
        await self.initialize_run()
        total_fetched = 0
        total_new = 0
        total_dup = 0
        error_msg = None

        try:
            logger.info(f"Fetching App Store reviews (max {self.max_reviews})...")
            
            method = "primary_app_store_scraper"
            reviews_list = []
            
            try:
                reviews_list = await asyncio.to_thread(self._fetch_reviews_primary_sync)
            except Exception as primary_e:
                logger.error(f"Primary scraper failed: {primary_e}. Falling back to RSS feed.")
                method = "fallback_apple_rss"
                reviews_list = await self._fetch_reviews_rss()
            
            # Additional safety check if it returns empty silently
            if not reviews_list and method == "primary_app_store_scraper":
                logger.warning("Primary scraper returned 0 reviews. Falling back to RSS feed just in case.")
                method = "fallback_apple_rss"
                reviews_list = await self._fetch_reviews_rss()
            
            for r in reviews_list:
                if total_fetched >= self.max_reviews:
                    break
                    
                if not self._is_valid_review(r):
                    continue

                normalized = self._normalize(r, method)
                
                if not normalized.get("external_id"):
                    hash_input = f"{normalized['author']}_{normalized['timestamp']}_{normalized['raw_content']}".encode('utf-8')
                    normalized["external_id"] = hashlib.sha256(hash_input).hexdigest()
                
                if not self.dry_run:
                    normalized["source_id"] = self.source.id
                    normalized["collection_run_id"] = self.run_record.id

                is_new = await self._insert_or_ignore_conversation(normalized)
                total_fetched += 1
                if is_new:
                    total_new += 1
                else:
                    total_dup += 1

        except Exception as e:
            logger.error(f"App Store Collection run failed: {str(e)}")
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
                f"App Store Run Finished. Fetched: {total_fetched}, New: {total_new}, "
                f"Dup: {total_dup}, DryRun: {self.dry_run}, Error: {error_msg}"
            )
