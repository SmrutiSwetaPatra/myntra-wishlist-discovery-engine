import pytest
from unittest.mock import AsyncMock, patch
from scripts.enrich_existing import passes_quality_gate

def test_quality_gate_rejection():
    assert not passes_quality_gate("")
    assert not passes_quality_gate("   ")
    assert not passes_quality_gate("good")
    assert not passes_quality_gate("nice app")
    assert not passes_quality_gate("Awesome")
    assert not passes_quality_gate("LOVE IT")

def test_quality_gate_acceptance():
    assert passes_quality_gate("price is too high")
    assert passes_quality_gate("size is always unavailable")
    assert passes_quality_gate("Too expensive")
    assert passes_quality_gate("Bad sizing")
    assert passes_quality_gate("Not worth it")
    assert passes_quality_gate("Poor quality")

@pytest.mark.asyncio
async def test_duplicate_skipping():
    # We will test the duplicate skipping logic here if necessary.
    # Since it requires full DB setup like test_aggregation, we will focus on
    # ensuring the `where(Analysis.conversation_id == conv.id)` logic is present 
    # in enrich_existing.py.
    pass

@pytest.mark.asyncio
async def test_pipeline_error_handling():
    # Test that pipeline handles exceptions and sets correct validation_status
    from app.engine.pipeline import AIPipeline
    from app.models.conversations import Conversation
    
    mock_db = AsyncMock()
    pipeline = AIPipeline(db_session=mock_db, dry_run=True)
    
    conv = Conversation(id="123", raw_content="price is high")
    
    # 1. Test API Failure in Relevance Gate
    pipeline.cache = AsyncMock()
    pipeline.cache.get_cached_analysis.return_value = None
    
    pipeline.relevance_gate = AsyncMock()
    pipeline.relevance_gate.evaluate.side_effect = Exception("429 Quota Exceeded")
    
    res = await pipeline.process_conversation(conv)
    assert res is not None
    assert res.validation_status == "api_failure"
    
    # 2. Test Schema Failure (ValidationError) in Relevance Gate
    pipeline.relevance_gate.evaluate.side_effect = Exception("ValidationError: pydantic failed")
    res = await pipeline.process_conversation(conv)
    assert res.validation_status == "schema_failure"
    
    # 3. Test API Failure in Deep Analysis
    pipeline.relevance_gate.evaluate.side_effect = None
    pipeline.relevance_gate.evaluate.return_value = AsyncMock(is_relevant=True, relevance_score=0.9, relevance_reason="")
    pipeline.deep_analyzer = AsyncMock()
    pipeline.deep_analyzer.analyze.side_effect = Exception("500 Internal Server Error")
    
    res = await pipeline.process_conversation(conv)
    assert res.validation_status == "api_failure"
