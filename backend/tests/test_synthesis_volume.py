import pytest
from unittest.mock import patch, AsyncMock
import asyncio
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.engine.copilot import DiscoveryCopilot
from app.engine.router import ExecutionPlan
from app.engine.schemas import QueryRelevanceDecision, CopilotResponse
from app.engine.gemini import GeminiClient
from app.engine.retriever import Document

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
async def test_synthesis_volume_rules_in_prompt(mock_gemini, mock_retriever_search):
    copilot = DiscoveryCopilot()
    
    # Provide 1 direct evidence record
    docs = [
        make_doc("id_1", "I use the wishlist to shortlist items.", "validated_relevant")
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
                semantic_query="Mocked query",
                insufficient_evidence_likely=False
            )
        elif "QueryRelevanceDecision" in schema_name:
            return QueryRelevanceDecision(relevant=True, relevance_score=0.9, reason="Relevant")
        elif "CopilotResponse" in schema_name:
            return CopilotResponse(
                answer="The available evidence suggests...",
                query_type="Semantic",
                confidence="low",
                insufficient_evidence=False,
                metrics=[],
                evidence_cards=[],
                limitations=["Only one record available"],
                sources_used=[]
            )
            
    mock_gemini.side_effect = mock_extract
    copilot.router.client.extract_structured = mock_gemini
    copilot.client.extract_structured = mock_gemini
    
    response = await copilot.query("Why do users save fashion products to their wishlist?")
    
    # Check what was sent to synthesis
    synthesis_call_args = mock_gemini.call_args_list[-1]
    prompt_text = synthesis_call_args[0][0] if len(synthesis_call_args[0]) > 0 else synthesis_call_args[1].get('prompt')
    
    # Assert the prompt strictly contains the new volume-aware rules
    assert "EVIDENCE VOLUME & GENERALIZATION" in prompt_text
    assert "Never use \"users\" as a broad/general claim when only one or very few records support the finding" in prompt_text
    assert "If only one direct record is relevant, say so clearly" in prompt_text
    
    # Assert context formatting uses Evidence Index
    assert "[Evidence 1]" in prompt_text
    assert "id_1" not in prompt_text

@pytest.mark.asyncio
async def test_synthesis_indirect_evidence(mock_gemini, mock_retriever_search):
    copilot = DiscoveryCopilot()
    
    # 3. One indirect record
    docs = [
        make_doc("id_2", "I didn't buy it because it was too expensive.", "indirect_pre_purchase")
    ]
    mock_retriever_search.return_value = docs
    
    async def mock_extract(*args, **kwargs):
        schema = kwargs.get('schema') or (args[2] if len(args) > 2 else None)
        schema_name = schema.__name__ if hasattr(schema, '__name__') else str(schema)
        if "ExecutionPlan" in schema_name:
            return ExecutionPlan(is_quantitative=False, requires_cross_source=False, requires_segmentation=False, semantic_query="Mocked", insufficient_evidence_likely=False)
        elif "QueryRelevanceDecision" in schema_name:
            return QueryRelevanceDecision(relevant=True, relevance_score=0.9, reason="Relevant")
        elif "CopilotResponse" in schema_name:
            return CopilotResponse(answer="Indirect evidence shows...", query_type="Semantic", confidence="low", insufficient_evidence=False, metrics=[], evidence_cards=[], limitations=[], sources_used=[])
            
    mock_gemini.side_effect = mock_extract
    copilot.router.client.extract_structured = mock_gemini
    copilot.client.extract_structured = mock_gemini
    
    response = await copilot.query("What are the barriers?")
    
    synthesis_call_args = mock_gemini.call_args_list[-1]
    prompt_text = synthesis_call_args[0][0] if len(synthesis_call_args[0]) > 0 else synthesis_call_args[1].get('prompt')
    
    assert "Validation Tier: indirect_pre_purchase" in prompt_text
    assert "Distinguish clearly between \"validated_relevant\" (direct wishlist-to-purchase evidence) and \"indirect_pre_purchase\"" in prompt_text

@pytest.mark.asyncio
async def test_synthesis_no_evidence(mock_gemini, mock_retriever_search):
    copilot = DiscoveryCopilot()
    
    # 4. Generic unrelated evidence -> fails relevance gate
    # 5. No relevant evidence -> evidence-insufficient response
    docs = [
        make_doc("id_3", "Generic review about app crash")
    ]
    mock_retriever_search.return_value = docs
    
    async def mock_extract(*args, **kwargs):
        schema = kwargs.get('schema') or (args[2] if len(args) > 2 else None)
        schema_name = schema.__name__ if hasattr(schema, '__name__') else str(schema)
        if "ExecutionPlan" in schema_name:
            return ExecutionPlan(is_quantitative=False, requires_cross_source=False, requires_segmentation=False, semantic_query="Mocked", insufficient_evidence_likely=False)
        elif "QueryRelevanceDecision" in schema_name:
            return QueryRelevanceDecision(relevant=False, relevance_score=0.1, reason="Irrelevant")
            
    mock_gemini.side_effect = mock_extract
    copilot.router.client.extract_structured = mock_gemini
    copilot.client.extract_structured = mock_gemini
    
    response = await copilot.query("Why do users wishlist?")
    assert response.insufficient_evidence is True
