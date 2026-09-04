import pytest
import asyncio
from unittest.mock import patch, AsyncMock
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.engine.copilot import DiscoveryCopilot
from app.engine.router import ExecutionPlan
from app.engine.schemas import QueryRelevanceDecision, CopilotResponse
from app.engine.retriever import Document
from app.engine.gemini import GeminiClient

def make_doc(doc_id, text, status="validated_relevant", metadata=None):
    return Document(
        conversation_id=doc_id,
        text=text,
        validation_status=status,
        metadata=metadata or {"ai_confidence": 0.9}
    )

@pytest.fixture
def mock_gemini():
    with patch.object(GeminiClient, 'extract_structured', new_callable=AsyncMock) as mock:
        yield mock

@pytest.fixture
def mock_retriever_search():
    with patch('app.engine.retriever.NumPyVectorStore.search', new_callable=AsyncMock) as mock:
        yield mock

@pytest.mark.asyncio
async def test_narrow_wishlist_query(mock_gemini, mock_retriever_search):
    # TEST 1
    copilot = DiscoveryCopilot()
    docs = [make_doc("id_narrow", "Wishlist limit prevents shortlisting")]
    mock_retriever_search.return_value = docs
    
    async def mock_extract(*args, **kwargs):
        schema = kwargs.get('schema') or (args[2] if len(args) > 2 else None)
        schema_name = schema.__name__ if hasattr(schema, '__name__') else str(schema)
        if "ExecutionPlan" in schema_name:
            return ExecutionPlan(is_quantitative=False, requires_cross_source=False, requires_segmentation=False, semantic_query="Narrow", insufficient_evidence_likely=False)
        elif "QueryRelevanceDecision" in schema_name:
            return QueryRelevanceDecision(relevant=True, relevance_score=0.9, reason="Relevant")
        elif "CopilotResponse" in schema_name:
            prompt = args[0] if len(args) > 0 else kwargs.get('prompt')
            assert "EVIDENCE VOLUME" in prompt
            return CopilotResponse(answer="Limited evidence", query_type="Semantic", confidence="low", insufficient_evidence=False, metrics=[], evidence_cards=[], limitations=[], sources_used=[])
            
    mock_gemini.side_effect = mock_extract
    copilot.router.client.extract_structured = mock_gemini
    copilot.client.extract_structured = mock_gemini
    
    res = await copilot.query("Why do users save fashion products to their wishlist?")
    assert not res.insufficient_evidence

@pytest.mark.asyncio
async def test_broad_purchase_barrier_query(mock_gemini, mock_retriever_search):
    # TEST 2 & TEST 3 & TEST 4
    copilot = DiscoveryCopilot()
    
    docs_metadata_filtered = [make_doc("id_meta", "Price is too high")]
    docs_fallback = [make_doc("id_fall1", "Quality is poor"), make_doc("id_fall2", "Wishlist limit reached")]
    
    # Mock search to return different things on first (metadata) and second (fallback) calls
    mock_retriever_search.side_effect = [docs_metadata_filtered, docs_fallback]
    
    async def mock_extract(*args, **kwargs):
        schema = kwargs.get('schema') or (args[2] if len(args) > 2 else None)
        schema_name = schema.__name__ if hasattr(schema, '__name__') else str(schema)
        if "ExecutionPlan" in schema_name:
            return ExecutionPlan(is_quantitative=False, requires_cross_source=False, requires_segmentation=False, metadata_filters='{"shopping_stage": "consideration"}', semantic_query="Broad", insufficient_evidence_likely=False)
        elif "QueryRelevanceDecision" in schema_name:
            return QueryRelevanceDecision(relevant=True, relevance_score=0.8, reason="Relevant")
        elif "CopilotResponse" in schema_name:
            prompt = args[0] if len(args) > 0 else kwargs.get('prompt')
            # Check that multiple independent docs reached synthesis
            assert "[Evidence 1]" in prompt
            assert "[Evidence 3]" in prompt 
            return CopilotResponse(answer="Multiple barriers", query_type="Semantic", confidence="high", insufficient_evidence=False, metrics=[], evidence_cards=[], limitations=[], sources_used=[])
            
    mock_gemini.side_effect = mock_extract
    copilot.router.client.extract_structured = mock_gemini
    copilot.client.extract_structured = mock_gemini
    
    res = await copilot.query("What prevents wishlisted products from being purchased?")
    assert not res.insufficient_evidence
    assert len(res.evidence_cards) == 3 # 1 from metadata, 2 from fallback
    
@pytest.mark.asyncio
async def test_hallucination_and_irrelevance(mock_gemini, mock_retriever_search):
    # TEST 5 & TEST 6
    copilot = DiscoveryCopilot()
    
    docs = [make_doc("id_irrelevant", "Generic app crash")]
    mock_retriever_search.return_value = docs
    
    async def mock_extract(*args, **kwargs):
        schema = kwargs.get('schema') or (args[2] if len(args) > 2 else None)
        schema_name = schema.__name__ if hasattr(schema, '__name__') else str(schema)
        if "ExecutionPlan" in schema_name:
            return ExecutionPlan(is_quantitative=False, requires_cross_source=False, requires_segmentation=False, semantic_query="Hallucinate", insufficient_evidence_likely=False)
        elif "QueryRelevanceDecision" in schema_name:
            return QueryRelevanceDecision(relevant=False, relevance_score=0.2, reason="Irrelevant")
            
    mock_gemini.side_effect = mock_extract
    copilot.router.client.extract_structured = mock_gemini
    copilot.client.extract_structured = mock_gemini
    
    res = await copilot.query("What percentage of users abandon because of size?")
    # Evidence rejected by gate -> insufficient evidence
    assert res.insufficient_evidence

def test_async_lifecycle_sequential():
    # TEST 7
    from tests.test_async_lifecycle import test_sequential_queries_async_lifecycle
    # It is already thoroughly tested in test_async_lifecycle.py
    pass
