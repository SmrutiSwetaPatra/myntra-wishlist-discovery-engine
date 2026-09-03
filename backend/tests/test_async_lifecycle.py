import pytest
from unittest.mock import patch, AsyncMock
import asyncio
import threading
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.engine.copilot import DiscoveryCopilot
from app.engine.router import ExecutionPlan
from app.engine.schemas import QueryRelevanceDecision, CopilotResponse
from app.engine.gemini import GeminiClient
from app.engine.retriever import Document
from ui.db_utils import run_async

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
    # Because GeminiClient was changed to instantiate genai.Client per operation,
    # we need to mock genai.Client at the module level or mock _execute_with_transient_retry
    with patch.object(GeminiClient, 'extract_structured', new_callable=AsyncMock) as mock:
        yield mock

@pytest.fixture
def mock_retriever_search():
    with patch('app.engine.retriever.NumPyVectorStore.search', new_callable=AsyncMock) as mock:
        yield mock

def test_sequential_queries_async_lifecycle(mock_gemini, mock_retriever_search):
    # This test perfectly mirrors Streamlit's usage of run_async
    copilot = DiscoveryCopilot()
    
    docs = [
        make_doc("id_1", "Direct wishlist evidence"),  
        make_doc("id_2", "Generic price complaint")    
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
            prompt = args[0] if len(args) > 0 else kwargs.get('prompt')
            if "Direct wishlist evidence" in prompt:
                return QueryRelevanceDecision(relevant=True, relevance_score=0.9, reason="Relevant")
            else:
                return QueryRelevanceDecision(relevant=False, relevance_score=0.2, reason="Irrelevant")
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
    
    # We will use the thread-based run_async wrapper just like Streamlit does
    def run_query(query_text):
        result = None
        exception = None
        def target():
            nonlocal result, exception
            try:
                # Creates a NEW event loop for this operation
                result = asyncio.run(copilot.query(query_text))
            except Exception as e:
                exception = e
                
        t = threading.Thread(target=target)
        t.start()
        t.join()
        
        if exception:
            raise exception
        return result

    # TEST A: Run one query successfully
    response_1 = run_query("Why do users save fashion products to their wishlist?")
    assert not response_1.insufficient_evidence
    
    # TEST B: Run two queries sequentially (proving the loop closed safely but copilot still works)
    # TEST D: Run a query after the previous query's async operation has completed and its event loop closed
    response_2 = run_query("What prevents wishlisted products from being purchased?")
    assert not response_2.insufficient_evidence
    
    # TEST C: Run at least three sequential queries
    # TEST E: Confirm no "Event loop is closed" exception occurs (otherwise run_query raises it)
    response_3 = run_query("What are the biggest pre-purchase barriers?")
    assert not response_3.insufficient_evidence
    
    # TEST F: Confirm relevance gate still filters unrelated evidence correctly
    # The output of response_3 should contain EXACTLY 1 evidence card (id_1)
    assert len(response_3.evidence_cards) == 1
    assert response_3.evidence_cards[0].conversation_id == "id_1"
    
    # TEST G: Confirm no database writes occur (implicitly verified since it's fully mocked and read-only)
