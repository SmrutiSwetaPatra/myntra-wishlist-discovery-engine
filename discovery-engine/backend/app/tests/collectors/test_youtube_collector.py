import pytest
from unittest.mock import AsyncMock, patch
from httpx import HTTPStatusError, Request, Response
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from sqlalchemy import delete
from app.collectors.youtube.collector import YouTubeCollector
from app.models.collection_runs import CollectionRun
from app.models.conversations import Conversation
from app.models.sources import Source

@pytest.fixture
def mock_search_response():
    return {
        "items": [
            {
                "id": {"videoId": "vid1"},
                "snippet": {"title": "Title 1", "channelTitle": "Channel 1"}
            }
        ]
    }

@pytest.fixture
def mock_comment_threads_response():
    return {
        "items": [
            {
                "id": "thread1",
                "snippet": {
                    "topLevelComment": {
                        "id": "comment1",
                        "snippet": {
                            "textDisplay": "Great dress!",
                            "authorDisplayName": "User1",
                            "publishedAt": "2023-10-01T12:00:00Z",
                            "likeCount": 5
                        }
                    }
                },
                "replies": {
                    "comments": [
                        {
                            "id": "reply1",
                            "snippet": {
                                "textDisplay": "I agree",
                                "authorDisplayName": "User2",
                                "publishedAt": "2023-10-01T13:00:00Z",
                                "likeCount": 1,
                                "parentId": "comment1"
                            }
                        }
                    ]
                }
            }
        ]
    }

async def clear_db(db_session: AsyncSession):
    await db_session.execute(delete(Conversation))
    await db_session.execute(delete(CollectionRun))
    await db_session.execute(delete(Source))
    await db_session.commit()

@pytest.mark.asyncio
async def test_collector_dry_run(db_session: AsyncSession, mock_search_response, mock_comment_threads_response):
    await clear_db(db_session)
    with patch("app.collectors.youtube.client.YouTubeAPIClient.search_videos", new_callable=AsyncMock) as mock_search:
        with patch("app.collectors.youtube.client.YouTubeAPIClient.get_comment_threads", new_callable=AsyncMock) as mock_comments:
            mock_search.return_value = mock_search_response
            mock_comments.return_value = mock_comment_threads_response
            
            collector = YouTubeCollector(
                api_key="fake",
                db_session=db_session,
                queries=["test"],
                dry_run=True
            )
            await collector.run()
            
            # Verify no DB inserts
            result = await db_session.execute(select(Conversation))
            assert len(result.scalars().all()) == 0

@pytest.mark.asyncio
async def test_collector_normal_run(db_session: AsyncSession, mock_search_response, mock_comment_threads_response):
    await clear_db(db_session)
    with patch("app.collectors.youtube.client.YouTubeAPIClient.search_videos", new_callable=AsyncMock) as mock_search:
        with patch("app.collectors.youtube.client.YouTubeAPIClient.get_comment_threads", new_callable=AsyncMock) as mock_comments:
            mock_search.return_value = mock_search_response
            mock_comments.return_value = mock_comment_threads_response
            
            collector = YouTubeCollector(
                api_key="fake",
                db_session=db_session,
                queries=["test"]
            )
            await collector.run()
            
            # Verify region and language config
            mock_search.assert_called_with(
                query="test",
                region_code="IN",
                relevance_language="en",
                max_results=5
            )
            
            # Verify data insertion (1 top level + 1 reply = 2)
            result = await db_session.execute(select(Conversation))
            conversations = result.scalars().all()
            assert len(conversations) == 2
            
            assert conversations[0].external_id == "comment1"
            assert conversations[0].metadata_["parent_comment_id"] is None
            assert conversations[0].metadata_["query_used"] == "test"
            
            assert conversations[1].external_id == "reply1"
            assert conversations[1].metadata_["parent_comment_id"] == "comment1"
            
            # Verify counters
            run = await db_session.execute(select(CollectionRun))
            run = run.scalars().first()
            assert run.records_fetched == 2
            assert run.records_new == 2
            assert run.records_duplicate == 0

@pytest.mark.asyncio
async def test_collector_duplicates_and_limits(db_session: AsyncSession, mock_search_response, mock_comment_threads_response):
    await clear_db(db_session)
    with patch("app.collectors.youtube.client.YouTubeAPIClient.search_videos", new_callable=AsyncMock) as mock_search:
        with patch("app.collectors.youtube.client.YouTubeAPIClient.get_comment_threads", new_callable=AsyncMock) as mock_comments:
            mock_search.return_value = mock_search_response
            mock_comments.return_value = mock_comment_threads_response
            
            # Run 1
            collector1 = YouTubeCollector(api_key="fake", db_session=db_session, queries=["test"])
            await collector1.run()
            
            # Run 2: Exact same data, so it should be marked as duplicate
            # Set max_total_comments_per_run to 1 to test quota limits
            collector2 = YouTubeCollector(
                api_key="fake", 
                db_session=db_session, 
                queries=["test"],
                max_total_comments_per_run=1
            )
            await collector2.run()
            
            runs_res = await db_session.execute(select(CollectionRun).order_by(CollectionRun.start_time.desc()))
            latest_run = runs_res.scalars().first()
            
            # Because max_total_comments is 1, it should fetch 1, which is a duplicate
            assert latest_run.records_fetched == 1
            assert latest_run.records_new == 0
            assert latest_run.records_duplicate == 1

@pytest.mark.asyncio
async def test_collector_api_error(db_session: AsyncSession, mock_search_response):
    await clear_db(db_session)
    with patch("app.collectors.youtube.client.YouTubeAPIClient.search_videos", new_callable=AsyncMock) as mock_search:
        with patch("app.collectors.youtube.client.YouTubeAPIClient.get_comment_threads", new_callable=AsyncMock) as mock_comments:
            mock_search.return_value = mock_search_response
            
            # Create a mock error response for Quota Exceeded
            resp = Response(403, request=Request("GET", "https://fake"), text='{"error": {"errors": [{"reason": "quotaExceeded"}]}}')
            req = Request("GET", "https://fake")
            mock_comments.side_effect = HTTPStatusError("Quota Exceeded", request=req, response=resp)
            
            collector = YouTubeCollector(api_key="fake", db_session=db_session, queries=["test"])
            
            # The quotaExceeded should raise and fail fast
            await collector.run()
            
            runs_res = await db_session.execute(select(CollectionRun).order_by(CollectionRun.start_time.desc()))
            latest_run = runs_res.scalars().first()
            
            assert latest_run.status == "error"
            assert "Quota Exceeded" in latest_run.error_message
