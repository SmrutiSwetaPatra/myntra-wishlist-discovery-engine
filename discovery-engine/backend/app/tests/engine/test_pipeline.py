import pytest
from unittest.mock import AsyncMock, patch
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import delete
from sqlalchemy.future import select

from app.models.conversations import Conversation
from app.models.analyses import Analysis
from app.models.sources import Source
from app.engine.pipeline import AIPipeline
from app.engine.schemas import RelevanceDecision, DeepAnalysis

import pytest_asyncio

async def clear_db(db_session: AsyncSession):
    await db_session.execute(delete(Analysis))
    await db_session.execute(delete(Conversation))
    await db_session.execute(delete(Source))
    await db_session.commit()

@pytest_asyncio.fixture
async def sample_conversation(db_session: AsyncSession):
    await clear_db(db_session)
    src = Source(platform="test", name="test", base_url="test")
    db_session.add(src)
    await db_session.flush()
    
    conv = Conversation(
        source_id=src.id,
        external_id="123",
        raw_content="Every time I come back, my size is gone.",
        author="User A",
        timestamp=None,
        source_url="test",
        metadata_={}
    )
    db_session.add(conv)
    await db_session.commit()
    return conv

@pytest.mark.asyncio
@patch('os.getenv', return_value="fake_api_key")
async def test_pipeline_relevant(mock_env, db_session: AsyncSession, sample_conversation):
    pipeline = AIPipeline(db_session=db_session, model_name="test-model")
    
    # Mock Relevance
    mock_rel = RelevanceDecision(is_relevant=True, relevance_score=0.9, relevance_reason="Implies stock issue", evidence_span="size is gone")
    pipeline.relevance_gate.evaluate = AsyncMock(return_value=mock_rel)
    
    # Mock Deep Analysis
    mock_deep = DeepAnalysis(
        primary_barrier_category="Availability",
        primary_barrier_detail="Size out of stock",
        ai_confidence=0.85,
        secondary_barriers=[]
    )
    pipeline.deep_analyzer.analyze = AsyncMock(return_value=mock_deep)
    
    # Run
    analysis = await pipeline.process_conversation(sample_conversation)
    
    assert analysis is not None
    assert analysis.relevance == "True"
    assert analysis.primary_barrier_category == "Availability"
    assert analysis.ai_confidence == 0.85 # min(0.9, 0.85)
    
    # Verify DB
    res = await db_session.execute(select(Analysis))
    saved = res.scalars().first()
    assert saved.model_name == "test-model"

@pytest.mark.asyncio
@patch('os.getenv', return_value="fake_api_key")
async def test_pipeline_irrelevant(mock_env, db_session: AsyncSession, sample_conversation):
    pipeline = AIPipeline(db_session=db_session, model_name="test-model")
    
    mock_rel = RelevanceDecision(is_relevant=False, relevance_score=0.99, relevance_reason="Irrelevant praise", evidence_span=None)
    pipeline.relevance_gate.evaluate = AsyncMock(return_value=mock_rel)
    pipeline.deep_analyzer.analyze = AsyncMock() # Should not be called
    
    analysis = await pipeline.process_conversation(sample_conversation)
    
    assert analysis.relevance == "False"
    assert analysis.primary_barrier_category is None
    pipeline.deep_analyzer.analyze.assert_not_called()

@pytest.mark.asyncio
@patch('os.getenv', return_value="fake_api_key")
async def test_pipeline_cache_hit(mock_env, db_session: AsyncSession, sample_conversation):
    pipeline = AIPipeline(db_session=db_session, model_name="test-model")
    
    # Pre-populate DB with existing analysis
    existing = Analysis(
        conversation_id=sample_conversation.id,
        relevance="True",
        model_name="test-model",
        prompt_version=pipeline.deep_analyzer.prompt_version,
        schema_version=pipeline.deep_analyzer.schema_version
    )
    db_session.add(existing)
    await db_session.commit()
    
    pipeline.relevance_gate.evaluate = AsyncMock()
    pipeline.deep_analyzer.analyze = AsyncMock()
    
    analysis = await pipeline.process_conversation(sample_conversation)
    
    assert analysis.id == existing.id
    pipeline.relevance_gate.evaluate.assert_not_called()
    pipeline.deep_analyzer.analyze.assert_not_called()
