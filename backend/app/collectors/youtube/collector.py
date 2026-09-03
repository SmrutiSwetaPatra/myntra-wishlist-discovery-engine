import logging
from datetime import datetime, timezone
from typing import List, Dict, Any, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError
from httpx import HTTPStatusError

from app.collectors.youtube.client import YouTubeAPIClient
from app.models.sources import Source
from app.models.collection_runs import CollectionRun
from app.models.conversations import Conversation

logger = logging.getLogger(__name__)

class YouTubeCollector:
    def __init__(
        self,
        api_key: str,
        db_session: AsyncSession,
        queries: List[str],
        region_code: str = "IN",
        relevance_language: str = "en",
        max_videos_per_query: int = 5,
        max_comments_per_video: int = 100,
        max_total_comments_per_run: int = 500,
        dry_run: bool = False
    ):
        self.client = YouTubeAPIClient(api_key=api_key)
        self.db = db_session
        self.queries = queries
        self.region_code = region_code
        self.relevance_language = relevance_language
        self.max_videos_per_query = max_videos_per_query
        self.max_comments_per_video = max_comments_per_video
        self.max_total_comments_per_run = max_total_comments_per_run
        self.dry_run = dry_run

        self.source = None
        self.run_record = None

    async def initialize_run(self) -> None:
        if self.dry_run:
            logger.info("DRY RUN: Skipping DB initialization")
            return

        result = await self.db.execute(select(Source).where(Source.platform == "youtube"))
        self.source = result.scalars().first()
        if not self.source:
            self.source = Source(
                platform="youtube",
                name="YouTube",
                base_url="https://www.youtube.com"
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
        """Returns 1 if inserted, 0 if duplicate"""
        if self.dry_run:
            return 1 # Pretend it's new for counting in dry run

        try:
            async with self.db.begin_nested():
                conv = Conversation(**conv_data)
                self.db.add(conv)
                await self.db.flush()
                return 1
        except IntegrityError:
            return 0

    def parse_datetime(self, iso_str: str) -> Optional[datetime]:
        try:
            return datetime.fromisoformat(iso_str.replace('Z', '+00:00'))
        except (ValueError, TypeError):
            return None

    def _extract_comments(self, item: Dict[str, Any], query: str, video_info: Dict[str, str]) -> List[Dict[str, Any]]:
        comments_data = []
        
        snippet = item.get("snippet", {})
        top_level = snippet.get("topLevelComment", {})
        tl_snippet = top_level.get("snippet", {})
        
        comments_data.append({
            "external_id": top_level.get("id"),
            "raw_content": tl_snippet.get("textDisplay", ""),
            "author": tl_snippet.get("authorDisplayName", ""),
            "timestamp": self.parse_datetime(tl_snippet.get("publishedAt", "")),
            "source_url": f"https://www.youtube.com/watch?v={video_info['video_id']}&lc={top_level.get('id')}",
            "metadata_": {
                "parent_comment_id": None,
                "comment_like_count": tl_snippet.get("likeCount", 0),
                "query_used": query,
                **video_info
            }
        })

        replies = item.get("replies", {}).get("comments", [])
        for reply in replies:
            r_snippet = reply.get("snippet", {})
            comments_data.append({
                "external_id": reply.get("id"),
                "raw_content": r_snippet.get("textDisplay", ""),
                "author": r_snippet.get("authorDisplayName", ""),
                "timestamp": self.parse_datetime(r_snippet.get("publishedAt", "")),
                "source_url": f"https://www.youtube.com/watch?v={video_info['video_id']}&lc={reply.get('id')}",
                "metadata_": {
                    "parent_comment_id": r_snippet.get("parentId"),
                    "comment_like_count": r_snippet.get("likeCount", 0),
                    "query_used": query,
                    **video_info
                }
            })
            
        return comments_data

    async def run(self) -> None:
        await self.initialize_run()
        total_fetched = 0
        total_new = 0
        total_dup = 0
        error_msg = None

        try:
            for query in self.queries:
                if total_fetched >= self.max_total_comments_per_run:
                    logger.info("Reached max_total_comments_per_run limit.")
                    break

                logger.info(f"Searching videos for query: {query}")
                search_resp = await self.client.search_videos(
                    query=query,
                    region_code=self.region_code,
                    relevance_language=self.relevance_language,
                    max_results=self.max_videos_per_query
                )

                videos = search_resp.get("items", [])
                for video in videos:
                    if total_fetched >= self.max_total_comments_per_run:
                        break

                    video_id = video["id"].get("videoId")
                    if not video_id:
                        continue

                    video_info = {
                        "video_id": video_id,
                        "video_title": video.get("snippet", {}).get("title", ""),
                        "channel": video.get("snippet", {}).get("channelTitle", ""),
                        "video_url": f"https://www.youtube.com/watch?v={video_id}"
                    }

                    logger.info(f"Fetching comments for video {video_id}")
                    try:
                        comments_resp = await self.client.get_comment_threads(
                            video_id=video_id,
                            max_results=self.max_comments_per_video
                        )
                        
                        items = comments_resp.get("items", [])
                        for item in items:
                            if total_fetched >= self.max_total_comments_per_run:
                                break

                            extracted = self._extract_comments(item, query, video_info)
                            for comment_dict in extracted:
                                if total_fetched >= self.max_total_comments_per_run:
                                    break
                                    
                                if not self.dry_run:
                                    comment_dict["source_id"] = self.source.id
                                    comment_dict["collection_run_id"] = self.run_record.id

                                is_new = await self._insert_or_ignore_conversation(comment_dict)
                                total_fetched += 1
                                if is_new:
                                    total_new += 1
                                else:
                                    total_dup += 1

                    except HTTPStatusError as e:
                        if e.response.status_code == 403 and "quotaExceeded" in e.response.text:
                            raise e
                        logger.warning(f"Error fetching comments for video {video_id}: {e}")
                        continue
                        
        except Exception as e:
            logger.error(f"Collection run failed: {str(e)}")
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
            await self.client.close()

            logger.info(
                f"Run Finished. Fetched: {total_fetched}, New: {total_new}, "
                f"Dup: {total_dup}, DryRun: {self.dry_run}, Error: {error_msg}"
            )
