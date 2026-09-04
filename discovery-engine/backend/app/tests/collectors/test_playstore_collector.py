import pytest
from unittest.mock import patch, MagicMock
from datetime import datetime, timezone
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from sqlalchemy import delete
from app.collectors.playstore.collector import PlayStoreCollector
from app.models.collection_runs import CollectionRun
from app.models.conversations import Conversation
from app.models.sources import Source

@pytest.fixture
def mock_playstore_reviews():
    return [
        {
            "reviewId": "r1",
            "userName": "User A",
            "content": "Great app",
            "score": 5,
            "thumbsUpCount": 10,
            "reviewCreatedVersion": "1.0",
            "at": datetime(2023, 1, 1),
            "replyContent": "Thanks!",
            "repliedAt": datetime(2023, 1, 2)
        },
        {
            "reviewId": "r2",
            "userName": "User B",
            "content": "  ", # Should be skipped
            "score": 1,
            "thumbsUpCount": 0,
            "reviewCreatedVersion": "1.0",
            "at": datetime(2023, 1, 3),
            "replyContent": None,
            "repliedAt": None
        },
        {
            "reviewId": "r3",
            "userName": "User C",
            "content": "Size issue",
            "score": 2,
            "thumbsUpCount": 0,
            "reviewCreatedVersion": "1.1",
            "at": datetime(2023, 1, 4),
            "replyContent": None,
            "repliedAt": None
        }
    ]

async def clear_db(db_session: AsyncSession):
    await db_session.execute(delete(Conversation))
    await db_session.execute(delete(CollectionRun))
    await db_session.execute(delete(Source))
    await db_session.commit()

@pytest.mark.asyncio
async def test_playstore_dry_run(db_session: AsyncSession, mock_playstore_reviews):
    await clear_db(db_session)
    with patch("app.collectors.playstore.collector.PlayStoreCollector._fetch_reviews_sync") as mock_fetch:
        mock_fetch.return_value = (mock_playstore_reviews, None)
        
        collector = PlayStoreCollector(db_session=db_session, dry_run=True, max_reviews=10)
        await collector.run()
        
        result = await db_session.execute(select(Conversation))
        assert len(result.scalars().all()) == 0

@pytest.mark.asyncio
async def test_playstore_normal_run(db_session: AsyncSession, mock_playstore_reviews):
    await clear_db(db_session)
    with patch("app.collectors.playstore.collector.PlayStoreCollector._fetch_reviews_sync") as mock_fetch:
        mock_fetch.return_value = (mock_playstore_reviews, None)
        
        collector = PlayStoreCollector(db_session=db_session, max_reviews=10)
        await collector.run()
        
        result = await db_session.execute(select(Conversation).order_by(Conversation.external_id))
        conversations = result.scalars().all()
        
        assert len(conversations) == 2
        
        assert conversations[0].external_id == "r1"
        assert conversations[0].raw_content == "Great app"
        assert conversations[0].metadata_["rating"] == 5
        
        assert conversations[1].external_id == "r3"
        assert conversations[1].raw_content == "Size issue"
        
        run = await db_session.execute(select(CollectionRun))
        run = run.scalars().first()
        assert run.records_fetched == 2
        assert run.records_new == 2
        assert run.records_duplicate == 0
