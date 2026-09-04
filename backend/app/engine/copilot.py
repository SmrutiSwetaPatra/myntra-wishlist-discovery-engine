import logging
import json
from typing import Dict, List, Optional
from app.engine.gemini import GeminiClient
from app.engine.router import QueryRouter
from app.engine.retriever import NumPyVectorStore
from app.engine.quantitative import QuantitativeEngine
from app.engine.schemas import CopilotResponse, EvidenceCard
from app.engine.prompts import COPILOT_SYNTHESIS_PROMPT

logger = logging.getLogger(__name__)

class DiscoveryCopilot:
    def __init__(self):
        self.router = QueryRouter()
        self.retriever = NumPyVectorStore()
        self.quant_engine = QuantitativeEngine()
        self.client = GeminiClient()
        self.sessions: Dict[str, List[dict]] = {} # Simple in-memory history
        self.synthesis_cache: Dict[str, CopilotResponse] = {} # Query + doc_ids cache

    async def initialize(self, session):
        await self.retriever.load(session)
        
    def _format_context(self, docs, metrics) -> str:
        parts = []
        if metrics:
            parts.append("--- DETERMINISTIC METRICS ---")
            parts.extend(metrics)
            parts.append("\n")
            
        parts.append("--- RETRIEVED EVIDENCE ---")
        for i, d in enumerate(docs, 1):
            parts.append(f"[Evidence {i}]")
            parts.append(f"Validation Tier: {d.validation_status}")
            parts.append(f"Metadata: {json.dumps(d.metadata)}")
            parts.append(f"Text: {d.text}\n")
            
        return "\n".join(parts)

    def _format_history(self, session_id: str) -> str:
        if session_id not in self.sessions:
            return "No previous history."
        
        history = self.sessions[session_id]
        # Keep last 5 turns
        history = history[-10:] 
        
        parts = []
        for msg in history:
            role = msg.get("role", "user")
            parts.append(f"{role.upper()}: {msg.get('content')}")
        return "\n".join(parts)

    async def query(self, user_query: str, session_id: str = "default", require_validated_only: bool = False) -> CopilotResponse:
        try:
            # 1. Routing
            try:
                plan = await self.router.route(user_query, require_validated_only)
            except Exception as e:
                logger.warning(f"Router failed: {e}. Falling back to default plan.")
                from app.engine.router import ExecutionPlan
                plan = ExecutionPlan(
                    is_quantitative=False,
                    requires_cross_source=False,
                    requires_segmentation=False,
                    validation_status_filter=None,
                    metadata_filters=None,
                    semantic_query=user_query,
                    insufficient_evidence_likely=False
                )
            
            # Insufficient Evidence Mode (Routing level)
            if plan.insufficient_evidence_likely:
                return CopilotResponse(
                    answer="I cannot answer this question based on the available evidence. The dataset consists of public conversations and does not contain behavioral conversion metrics, complete demographic data, or exact population statistics.",
                    query_type="Refusal",
                    confidence="low",
                    insufficient_evidence=True,
                    metrics=[],
                    evidence_cards=[],
                    limitations=["Missing behavioral funnel data or demographics."],
                    sources_used=[]
                )
            
            # 2. Execution
            docs = []
            metrics = []
            
            if plan.is_quantitative or plan.requires_segmentation:
                metrics = await self.quant_engine.execute_metrics(
                    metadata_filters=plan.metadata_filters,
                    validation_status_filter=plan.validation_status_filter
                )
                
            docs = await self.retriever.search(
                query=plan.semantic_query,
                top_k=15,
                validation_status_in=plan.validation_status_filter,
                metadata_filters=plan.metadata_filters
            )
            
            # Semantic fallback: if exact metadata filtering or narrow validation filtering yields fewer than 15 results
            if len(docs) < 15:
                logger.info("Semantic fallback triggered: padding search without metadata filters and expanding validation tiers.")
                
                expanded_tiers = ["validated_relevant", "ai_direct_evidence", "indirect_pre_purchase", "ai_indirect_evidence"]
                
                fallback_docs = await self.retriever.search(
                    query=plan.semantic_query,
                    top_k=15,
                    validation_status_in=expanded_tiers,
                    metadata_filters=None
                )
                seen = {d.conversation_id for d in docs}
                for d in fallback_docs:
                    if d.conversation_id not in seen:
                        docs.append(d)
                        seen.add(d.conversation_id)
                docs = docs[:15]
                
            # Deduplicate by conversation_id to preserve highest ranked unique sources
            unique_docs = []
            seen = set()
            for d in docs:
                if d.conversation_id not in seen:
                    unique_docs.append(d)
                    seen.add(d.conversation_id)
            docs = unique_docs

            # Keep top 5 strictly relevant ones from vector search directly
            docs = docs[:5]
            
            # 2. Insufficient Evidence Mode (Retrieval level fallback)
            if not docs and not metrics:
                return CopilotResponse(
                    answer="I could not find any evidence in the dataset matching your criteria.",
                    query_type="Semantic",
                    confidence="low",
                    insufficient_evidence=True,
                    metrics=[],
                    evidence_cards=[],
                    limitations=["No matching records found in the corpus."],
                    sources_used=[]
                )
            
            # Check Cache
            doc_ids = ",".join(sorted([d.conversation_id for d in docs]))
            cache_key = f"{user_query.strip().lower()}_{doc_ids}"
            if cache_key in self.synthesis_cache:
                logger.info(f"Returning cached synthesis for query: {user_query}")
                return self.synthesis_cache[cache_key]

            # 3. Synthesis
            context = self._format_context(docs, metrics)
            history = self._format_history(session_id)
            
            prompt = COPILOT_SYNTHESIS_PROMPT.format(
                context=context,
                history=history,
                question=user_query
            )
            
            try:
                response = await self.client.extract_structured(prompt, "", CopilotResponse)
                response.metrics = metrics
            except Exception as e:
                logger.warning(f"Synthesis failed: {e}. Returning fallback response.")
                response = CopilotResponse(
                    answer="AI synthesis is temporarily unavailable due to API capacity limits. Please review the retrieved evidence below.",
                    query_type="Semantic (Fallback)",
                    confidence="low",
                    insufficient_evidence=False,
                    metrics=metrics,
                    evidence_cards=[],
                    limitations=["AI synthesis unavailable", "Showing raw retrieved evidence"],
                    sources_used=[]
                )
            
            # Build Evidence Cards
            cards = []
            sources_used = set()
            for d in docs:
                source = d.metadata.get("source_url", "Unknown")
                if "youtube" in source: src = "YouTube"
                elif "play.google" in source: src = "Google Play"
                else: src = "Apple App Store"
                
                sources_used.add(src)
                
                cards.append(EvidenceCard(
                    conversation_id=d.conversation_id,
                    source=src,
                    source_url=source,
                    raw_text=d.text,
                    validation_status=d.validation_status,
                    ai_confidence=d.metadata.get("ai_confidence"),
                    direct_indirect_classification="direct" if d.validation_status == "validated_relevant" else ("indirect" if d.validation_status == "indirect_pre_purchase" else "unvalidated"),
                    relevance_score=d.metadata.get("retrieval_score")
                ))
                
            response.evidence_cards = cards
            response.sources_used = list(sources_used)
            
            # 4. Save to history
            if session_id not in self.sessions:
                self.sessions[session_id] = []
            self.sessions[session_id].append({"role": "user", "content": user_query})
            self.sessions[session_id].append({"role": "assistant", "content": response.answer})
            
            # Save to Cache
            self.synthesis_cache[cache_key] = response
            
            return response
            
        except Exception as e:
            logger.error(f"Copilot query failed: {e}")
            raise
