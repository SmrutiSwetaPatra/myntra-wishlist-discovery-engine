import pytest
import pytest_asyncio
import numpy as np
from app.engine.schemas import EvidenceCard, CopilotResponse
from app.engine.copilot import DiscoveryCopilot

# Mock the retriever and gemini client to run deterministic tests
class MockRetriever:
    async def search(self, query, top_k, validation_status_in=None, metadata_filters=None):
        from app.engine.retriever import Document
        # Simulate returning duplicate conversation_ids from vector store
        return [
            Document(conversation_id="conv_1", text="Duplicate text", validation_status="validated_relevant", metadata={"retrieval_score": 0.9}),
            Document(conversation_id="conv_1", text="Duplicate text", validation_status="validated_relevant", metadata={"retrieval_score": 0.85}),
            Document(conversation_id="conv_2", text="Valid distinct text", validation_status="ai_direct_evidence", metadata={"retrieval_score": 0.8}),
        ]

class MockClient:
    async def extract_structured(self, prompt, text, schema):
        from app.engine.schemas import QueryRelevanceDecision, CopilotResponse
        
        if schema.__name__ == "QueryRelevanceDecision":
            if "USER QUERY: How do users decide between two similar dresses" in prompt:
                if "EVIDENCE TEXT: I like to wishlist a lot to compare them" in prompt:
                    return schema(relevant=False, relevance_score=0.2, reason="Generic comparison, no criteria")
            elif "USER QUERY: How do users compare multiple shortlisted products?" in prompt:
                if "EVIDENCE TEXT: I like to wishlist a lot to compare them" in prompt:
                    return schema(relevant=True, relevance_score=0.9, reason="Describes mechanism")
            
            return schema(relevant=True, relevance_score=0.9, reason="Mock relevant")
            
        elif schema.__name__ == "CopilotResponse":
            return schema(
                answer="Mock answer.",
                query_type="Semantic",
                confidence="high",
                insufficient_evidence=False,
                metrics=[],
                evidence_cards=[],
                limitations=[],
                sources_used=[]
            )
        return None

@pytest.mark.asyncio
async def test_duplicate_candidate_removal():
    copilot = DiscoveryCopilot()
    copilot.retriever = MockRetriever()
    copilot.client = MockClient()
    
    # Mock quant engine to avoid DB
    class MockQuant:
        async def execute_metrics(self, metadata_filters, validation_status_filter):
            return []
    copilot.quant_engine = MockQuant()

    response = await copilot.query("How does price uncertainty affect purchase decisions?")
    
    # Check that conv_1 only appears ONCE in evidence_cards
    conv_ids = [card.conversation_id for card in response.evidence_cards]
    assert conv_ids.count("conv_1") == 1
    assert len(conv_ids) == 2

@pytest.mark.asyncio
async def test_relevance_gate_narrow_question_rejection():
    copilot = DiscoveryCopilot()
    # Override retriever to return something that just says "compare"
    class CompareRetriever:
        async def search(self, query, top_k, validation_status_in=None, metadata_filters=None):
            from app.engine.retriever import Document
            return [
                Document(conversation_id="conv_1", text="I like to wishlist a lot to compare them with each other before deciding what to buy.", validation_status="validated_relevant", metadata={"retrieval_score": 0.9}),
            ]
    
    copilot.retriever = CompareRetriever()
    copilot.client = MockClient()
    
    class MockQuant:
        async def execute_metrics(self, metadata_filters, validation_status_filter):
            return []
    copilot.quant_engine = MockQuant()
    
    response5 = await copilot.query("How do users decide between two similar dresses in their wishlist?")
    assert response5.insufficient_evidence is True
    assert len(response5.evidence_cards) == 0
    
    response6 = await copilot.query("How do users compare multiple shortlisted products?")
    assert response6.insufficient_evidence is False
    assert len(response6.evidence_cards) == 1
