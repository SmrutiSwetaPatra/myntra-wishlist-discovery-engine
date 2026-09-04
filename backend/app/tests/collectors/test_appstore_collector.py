import pytest
from unittest.mock import patch, AsyncMock
from datetime import datetime, timezone
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from sqlalchemy import delete
from app.collectors.appstore.collector import AppStoreCollector
from app.models.collection_runs import CollectionRun
from app.models.conversations import Conversation
from app.models.sources import Source

@pytest.fixture
def mock_appstore_reviews():
    return [
        {
            "id": "111",
            "userName": "User X",
            "title": "Buggy",
            "review": "Very buggy",
            "rating": 2,
            "isEdited": False,
            "date": datetime(2023, 1, 1),
            "developerResponse": {"body": "Sorry", "modified": datetime(2023, 1, 2)}
        },
        {
            "id": "222",
            "userName": "User Y",
            "title": "",
            "review": "  ", # Should be skipped
            "rating": 1,
            "isEdited": False,
            "date": datetime(2023, 1, 3),
            "developerResponse": None
        },
        {
            "userName": "User Z",
            "title": "Needs work",
            "review": "Missing my size",
            "rating": 3,
            "isEdited": False,
            "date": datetime(2023, 1, 4),
            "developerResponse": None
            # No ID to test hash fallback
        }
    ]

async def clear_db(db_session: AsyncSession):
    await db_session.execute(delete(Conversation))
    await db_session.execute(delete(CollectionRun))
    await db_session.execute(delete(Source))
    await db_session.commit()

@pytest.mark.asyncio
async def test_appstore_dry_run(db_session: AsyncSession, mock_appstore_reviews):
    await clear_db(db_session)
    with patch("app.collectors.appstore.collector.AppStoreCollector._fetch_reviews_primary_sync") as mock_fetch:
        mock_fetch.return_value = mock_appstore_reviews
        
        collector = AppStoreCollector(db_session=db_session, dry_run=True, max_reviews=10)
        await collector.run()
        
        result = await db_session.execute(select(Conversation))
        assert len(result.scalars().all()) == 0

@pytest.mark.asyncio
async def test_appstore_normal_run(db_session: AsyncSession, mock_appstore_reviews):
    await clear_db(db_session)
    with patch("app.collectors.appstore.collector.AppStoreCollector._fetch_reviews_primary_sync") as mock_fetch:
        mock_fetch.return_value = mock_appstore_reviews
        
        collector = AppStoreCollector(db_session=db_session, max_reviews=10)
        await collector.run()
        
        result = await db_session.execute(select(Conversation).order_by(Conversation.author))
        conversations = result.scalars().all()
        
        assert len(conversations) == 2
        
        user_x = next(c for c in conversations if c.author == "User X")
        user_z = next(c for c in conversations if c.author == "User Z")
        
        assert user_x.external_id == "111"
        assert user_x.raw_content == "Buggy\n\nVery buggy"
        assert user_x.metadata_["rating"] == 2
        assert user_x.metadata_["acquisition_method"] == "primary_app_store_scraper"
        
        assert user_z.external_id != "" # Hash generated
        assert user_z.raw_content == "Needs work\n\nMissing my size"
        
        run = await db_session.execute(select(CollectionRun))
        run = run.scalars().first()
        assert run.records_fetched == 2
        assert run.records_new == 2
        assert run.records_duplicate == 0

@pytest.mark.asyncio
async def test_appstore_fallback_run(db_session: AsyncSession, mock_appstore_reviews):
    await clear_db(db_session)
    with patch("app.collectors.appstore.collector.AppStoreCollector._fetch_reviews_primary_sync") as mock_primary:
        mock_primary.side_effect = Exception("Primary blocked")
        with patch("app.collectors.appstore.collector.AppStoreCollector._fetch_reviews_rss", new_callable=AsyncMock) as mock_rss:
            mock_rss.return_value = mock_appstore_reviews
            
            collector = AppStoreCollector(db_session=db_session, max_reviews=10)
            await collector.run()
            
            result = await db_session.execute(select(Conversation).order_by(Conversation.author))
            conversations = result.scalars().all()
            
            assert len(conversations) == 2
            
            user_x = next(c for c in conversations if c.author == "User X")
            assert user_x.metadata_["acquisition_method"] == "fallback_apple_rss"
