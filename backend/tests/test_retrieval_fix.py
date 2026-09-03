import pytest
from unittest.mock import MagicMock, patch
import asyncio
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.engine.copilot import DiscoveryCopilot
from app.engine.router import QueryRouter, ExecutionPlan
from app.engine.retriever import NumPyVectorStore
from app.engine.gemini import GeminiClient
from app.db.session import AsyncSessionLocal
from ui.copilot_ui import render_copilot
import streamlit as st

@pytest.fixture
def mock_gemini():
    with patch.object(GeminiClient, 'extract_structured') as mock:
        yield mock

class AttrDict(dict):
    def __init__(self, *args, **kwargs):
        super(AttrDict, self).__init__(*args, **kwargs)
        self.__dict__ = self

@pytest.fixture
def mock_streamlit():
    with patch('ui.copilot_ui.st') as mock_st:
        mock_st.session_state = AttrDict()
        yield mock_st

@pytest.mark.asyncio
async def test_copilot_initialization_loads_embeddings():
    copilot = DiscoveryCopilot()
    async with AsyncSessionLocal() as session:
        await copilot.initialize(session)
    
    assert copilot.retriever.is_loaded is True
    # 2. Initialization loads the available non-null embeddings
    assert len(copilot.retriever.documents) == 236

@patch('ui.copilot_ui.run_async')
def test_streamlit_session_initializes_copilot(mock_run_async, mock_streamlit):
    # 1. A new Streamlit session initializes the DiscoveryCopilot before the first query.
    mock_streamlit.session_state = AttrDict()
    mock_streamlit.chat_input.return_value = None
    
    render_copilot()
    
    assert "copilot" in mock_streamlit.session_state
    mock_run_async.assert_called_once()
    assert isinstance(mock_streamlit.session_state["copilot"], DiscoveryCopilot)

@pytest.mark.asyncio
async def test_retrieval_query_flow_and_eligibility(mock_gemini):
    # Setup copilot and load data (READ-ONLY)
    copilot = DiscoveryCopilot()
    async with AsyncSessionLocal() as session:
        await copilot.initialize(session)
        
    # Mock Gemini to avoid real API calls (7. No Gemini API calls are made)
    from app.engine.schemas import CopilotResponse
    
    mock_plan = ExecutionPlan(
        is_quantitative=False,
        requires_cross_source=False,
        requires_segmentation=False,
        validation_status_filter=None,
        metadata_filters=None,
        semantic_query="Why do users save fashion products to their wishlist?",
        insufficient_evidence_likely=False
    )
    
    mock_response = CopilotResponse(
        answer="Users save products due to purchase barriers.",
        query_type="Semantic",
        confidence="high",
        insufficient_evidence=False,
        metrics=[],
        evidence_cards=[],
        limitations=[],
        sources_used=[]
    )
    
    async def mock_extract(*args, **kwargs):
        schema = kwargs.get('schema') or (args[2] if len(args) > 2 else None)
        schema_name = schema.__name__ if hasattr(schema, '__name__') else str(schema)
        if "ExecutionPlan" in schema_name:
            return mock_plan
        elif "QueryRelevanceDecision" in schema_name:
            from app.engine.schemas import QueryRelevanceDecision
            return QueryRelevanceDecision(relevant=True, relevance_score=0.9, reason="Relevant")
        elif "CopilotResponse" in schema_name:
            return mock_response
            
    mock_gemini.side_effect = mock_extract
    copilot.router.client.extract_structured = mock_gemini
    copilot.client.extract_structured = mock_gemini
    
    # 3. The query reaches the retrieval layer instead of immediately returning empty fallback
    response = await copilot.query("Why do users save fashion products to their wishlist?")
    
    assert response.insufficient_evidence is False
    assert response.answer != "I could not find any evidence in the dataset matching your criteria."
    assert len(response.evidence_cards) > 0
    
    # Analyze retrieved evidence cards
    retrieved_statuses = [card.validation_status for card in response.evidence_cards]
    
    # 4. Both ai_direct_evidence and ai_indirect_evidence are eligible for retrieval.
    # 6. Existing old valid statuses continue to work.
    allowed_statuses = ["validated_relevant", "ai_direct_evidence", "indirect_pre_purchase", "ai_indirect_evidence"]
    for status in retrieved_statuses:
        # We only expect relevant docs to have high enough score to be returned at top 5
        assert status in allowed_statuses
        
    # 5. Excluded, API failure, Schema failure, and Needs Validation cannot be treated as valid evidence
    invalid_statuses = ["excluded_general", "excluded_post_purchase", "excluded_ambiguous", "api_failure", "schema_failure", "ai_unvalidated"]
    for status in retrieved_statuses:
        assert status not in invalid_statuses

@patch('ui.copilot_ui.run_async')
def test_evidence_card_rendering_regression(mock_run_async, mock_streamlit):
    # Proves that EvidenceCard objects can be rendered without throwing .get() exceptions
    from app.engine.schemas import EvidenceCard
    
    # Create mock evidence cards as objects
    cards = [
        EvidenceCard(
            conversation_id="123",
            source="YouTube",
            source_url="youtube.com",
            raw_text="This is a test",
            validation_status="validated_relevant",
            ai_confidence=0.9,
            direct_indirect_classification="direct",
            relevance_score=0.8
        )
    ]
    
    mock_streamlit.session_state = AttrDict()
    mock_streamlit.session_state.messages = [
        {"role": "assistant", "content": "Test answer", "evidence": cards}
    ]
    mock_streamlit.chat_input.return_value = None
    
    # This will throw an AttributeError if the UI tries to use .get() on the Pydantic object
    try:
        render_copilot()
    except Exception as e:
        pytest.fail(f"render_copilot raised an exception during rendering: {e}")
