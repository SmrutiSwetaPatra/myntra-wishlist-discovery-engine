import pytest
from unittest.mock import MagicMock, patch, AsyncMock
import asyncio
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.engine.copilot import DiscoveryCopilot
from app.engine.router import ExecutionPlan
from app.engine.schemas import QueryRelevanceDecision, CopilotResponse
from app.engine.gemini import GeminiClient
from app.db.session import AsyncSessionLocal
from app.engine.retriever import Document

# Create dummy documents
def make_doc(doc_id, text, status="validated_relevant"):
    return Document(
        conversation_id=doc_id,
        text=text,
        validation_status=status,
        metadata={"ai_confidence": 0.9, "source_url": "dummy"}
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
async def test_relevance_gate_filters_mixed_pool(mock_gemini, mock_retriever_search):
    copilot = DiscoveryCopilot()
    
    # Mock retriever to return 15 initial candidates
    docs = [
        make_doc("id_1", "Direct wishlist evidence"),  # Should pass
        make_doc("id_2", "Shortlisting/comparison evidence", "indirect_pre_purchase"), # Should pass
        make_doc("id_3", "Generic price complaint"),   # Should fail
        make_doc("id_4", "Generic quality complaint"), # Should fail
        make_doc("id_5", "Generic availability complaint"), # Should fail
        make_doc("id_6", "Unrelated app review"),      # Should fail
        make_doc("id_7", "API Failure record", "api_failure") # Should fail
    ]
    mock_retriever_search.return_value = docs
    
    # Mock LLM calls
    async def mock_extract(*args, **kwargs):
        schema = kwargs.get('schema') or (args[2] if len(args) > 2 else None)
        schema_name = schema.__name__ if hasattr(schema, '__name__') else str(schema)
        
        if "ExecutionPlan" in schema_name:
            return ExecutionPlan(
                is_quantitative=False,
                requires_cross_source=False,
                requires_segmentation=False,
                semantic_query="Why do users save fashion products to their wishlist?",
                insufficient_evidence_likely=False
            )
        
        elif "QueryRelevanceDecision" in schema_name:
            prompt = args[0] if len(args) > 0 else kwargs.get('prompt')
            # 1. Direct wishlist evidence -> PASS
            if "Direct wishlist evidence" in prompt:
                return QueryRelevanceDecision(relevant=True, relevance_score=0.9, reason="Relevant")
            # 2. Shortlisting/comparison evidence -> PASS
            # 9. Direct + indirect relevant evidence -> both can pass
            elif "Shortlisting/comparison" in prompt:
                return QueryRelevanceDecision(relevant=True, relevance_score=0.8, reason="Relevant")
            # 3. Generic price complaint -> FAIL
            elif "Generic price" in prompt:
                return QueryRelevanceDecision(relevant=False, relevance_score=0.2, reason="Irrelevant")
            # 4. Generic quality complaint -> FAIL
            elif "Generic quality" in prompt:
                return QueryRelevanceDecision(relevant=False, relevance_score=0.1, reason="Irrelevant")
            # 5. Generic availability complaint -> FAIL
            elif "Generic availability" in prompt:
                return QueryRelevanceDecision(relevant=False, relevance_score=0.2, reason="Irrelevant")
            # 6. Unrelated app/work-environment review -> FAIL
            elif "Unrelated app" in prompt:
                return QueryRelevanceDecision(relevant=False, relevance_score=0.0, reason="Irrelevant")
            # Excluded/API-failure -> FAIL
            elif "API Failure" in prompt:
                return QueryRelevanceDecision(relevant=False, relevance_score=0.0, reason="Irrelevant")
                
            return QueryRelevanceDecision(relevant=False, relevance_score=0.0, reason="Default Fallback")
            
        elif "CopilotResponse" in schema_name:
            return CopilotResponse(
                answer="Synthesized answer",
                query_type="Semantic",
                confidence="high",
                insufficient_evidence=False,
                metrics=[],
                evidence_cards=[],
                limitations=[],
                sources_used=[]
            )
            
    mock_gemini.side_effect = mock_extract
    copilot.router.client.extract_structured = mock_gemini
    copilot.client.extract_structured = mock_gemini
    
    # 7. Mixed candidate pool -> only relevant evidence reaches synthesis
    # 10. Existing valid evidence taxonomy remains unchanged (handled by retriever)
    response = await copilot.query("Why do users save fashion products to their wishlist?")
    
    # Check that synthesis was called and evidence cards correctly filtered
    assert not response.insufficient_evidence
    
    # The response evidence cards should only contain the 2 passing docs
    assert len(response.evidence_cards) == 2
    passing_ids = [card.conversation_id for card in response.evidence_cards]
    assert "id_1" in passing_ids
    assert "id_2" in passing_ids
    assert "id_3" not in passing_ids # Failed relevance gate
    assert "id_7" not in passing_ids # API failure excluded
    
    # Check that prompt used Evidence Index, not UUIDs
    # extract_structured was called multiple times. We need to check the last call (synthesis)
    synthesis_call_args = mock_gemini.call_args_list[-1]
    prompt_text = synthesis_call_args[0][0] if len(synthesis_call_args[0]) > 0 else synthesis_call_args[1].get('prompt')
    
    assert "[Evidence 1]" in prompt_text
    assert "id_1" not in prompt_text # internal conversation IDs are never exposed in the UI/LLM prompt
    
@pytest.mark.asyncio
async def test_relevance_gate_all_fail(mock_gemini, mock_retriever_search):
    copilot = DiscoveryCopilot()
    
    # Mock retriever to return 3 initial candidates
    docs = [
        make_doc("id_1", "Generic price complaint"),
        make_doc("id_2", "Generic quality complaint"),
        make_doc("id_3", "Generic app crash")
    ]
    mock_retriever_search.return_value = docs
    
    async def mock_extract(*args, **kwargs):
        schema = kwargs.get('schema') or (args[2] if len(args) > 2 else None)
        schema_name = schema.__name__ if hasattr(schema, '__name__') else str(schema)
        
        if "ExecutionPlan" in schema_name:
            return ExecutionPlan(
                is_quantitative=False,
                requires_cross_source=False,
                requires_segmentation=False,
                semantic_query="Why do users save fashion products to their wishlist?",
                insufficient_evidence_likely=False
            )
        elif "QueryRelevanceDecision" in schema_name:
            # 8. No relevant candidates -> evidence-insufficient response
            return QueryRelevanceDecision(relevant=False, relevance_score=0.1, reason="Irrelevant")
            
    mock_gemini.side_effect = mock_extract
    copilot.router.client.extract_structured = mock_gemini
    copilot.client.extract_structured = mock_gemini
    
    response = await copilot.query("Why do users save fashion products to their wishlist?")
    
    # Should hit insufficient evidence because all docs failed the relevance gate
    assert response.insufficient_evidence is True
    assert "I could not find any evidence" in response.answer
    assert len(response.evidence_cards) == 0
