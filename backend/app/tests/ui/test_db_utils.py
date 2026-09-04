import pytest
from unittest.mock import AsyncMock, patch
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import delete

from app.models.conversations import Conversation
from app.models.analyses import Analysis
from app.models.sources import Source
from ui.db_utils import _get_dashboard_metrics, _get_explorer_data

async def clear_db(db_session: AsyncSession):
    await db_session.execute(delete(Analysis))
    await db_session.execute(delete(Conversation))
    await db_session.execute(delete(Source))
    await db_session.commit()

import pytest_asyncio

@pytest_asyncio.fixture
async def setup_ui_data(db_session: AsyncSession):
    await clear_db(db_session)
    src = Source(platform="playstore", name="Google Play", base_url="play")
    db_session.add(src)
    await db_session.flush()

    # Create various conversations and analyses
    statuses = [
        "validated_relevant",
        "indirect_pre_purchase",
        "ai_unvalidated",
        "excluded_general",
        "api_failure",
        "schema_failure"
    ]
    
    convs = []
    analyses = []
    
    for i, status in enumerate(statuses):
        c = Conversation(source_id=src.id, external_id=str(i), raw_content=f"Test {status}")
        db_session.add(c)
        await db_session.flush()
        
        a = Analysis(
            conversation_id=c.id,
            validation_status=status,
            relevance="True",
            primary_barrier_category="Price"
        )
        db_session.add(a)
    
    await db_session.commit()

@pytest.mark.asyncio
async def test_dashboard_metrics_explicit_mapping(db_session: AsyncSession, setup_ui_data):
    # Mock AsyncSessionLocal to yield our test db_session
    class MockSessionManager:
        async def __aenter__(self):
            return db_session
        async def __aexit__(self, exc_type, exc_val, exc_tb):
            pass

    with patch('ui.db_utils.AsyncSessionLocal', return_value=MockSessionManager()):
        metrics = await _get_dashboard_metrics()
        
        val_counts = metrics["validation_status"]
        
        # Verify exactly one of each goes to the correct bucket
        assert val_counts["Direct Evidence"] == 1
        assert val_counts["Indirect Pre-Purchase"] == 1
        assert val_counts["Needs Validation"] == 1
        assert val_counts["Excluded"] == 1
        assert val_counts["API Failure"] == 1
        assert val_counts["Schema Failure"] == 1

@pytest.mark.asyncio
async def test_explorer_data_explicit_mapping(db_session: AsyncSession, setup_ui_data):
    class MockSessionManager:
        async def __aenter__(self):
            return db_session
        async def __aexit__(self, exc_type, exc_val, exc_tb):
            pass

    with patch('ui.db_utils.AsyncSessionLocal', return_value=MockSessionManager()):
        data = await _get_explorer_data()
        
        direct_count = sum(1 for d in data if d["direct_vs_indirect"] == "Direct Evidence")
        indirect_count = sum(1 for d in data if d["direct_vs_indirect"] == "Indirect Pre-Purchase")
        needs_val_count = sum(1 for d in data if d["direct_vs_indirect"] == "Needs Validation")
        excluded_count = sum(1 for d in data if d["direct_vs_indirect"] == "Excluded")
        api_count = sum(1 for d in data if d["direct_vs_indirect"] == "API Failure")
        schema_count = sum(1 for d in data if d["direct_vs_indirect"] == "Schema Failure")
        
        assert direct_count == 1
        assert indirect_count == 1
        assert needs_val_count == 1
        assert excluded_count == 1
        assert api_count == 1
        assert schema_count == 1

@pytest.mark.asyncio
async def test_explorer_excluded_filter(db_session: AsyncSession, setup_ui_data):
    class MockSessionManager:
        async def __aenter__(self):
            return db_session
        async def __aexit__(self, exc_type, exc_val, exc_tb):
            pass

    with patch('ui.db_utils.AsyncSessionLocal', return_value=MockSessionManager()):
        # When fetching "Excluded" tier, it should NOT pull api_failure or schema_failure
        data = await _get_explorer_data(filters={"tier": "Excluded"})
        assert len(data) == 1
        assert data[0]["validation_status"] == "excluded_general"
