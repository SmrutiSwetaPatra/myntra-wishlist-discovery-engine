import logging
import asyncio
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models.conversations import Conversation
from app.models.analyses import Analysis
from app.engine.gemini import GeminiClient
from app.engine.cache import CacheManager
from app.engine.relevance import RelevanceGate
from app.engine.deep_analysis import DeepAnalyzer

logger = logging.getLogger(__name__)

class AIPipeline:
    def __init__(self, db_session: AsyncSession, model_name: str = "gemini-2.5-flash", dry_run: bool = False):
        self.db = db_session
        self.model_name = model_name
        self.dry_run = dry_run
        
        self.client = GeminiClient(model_name=self.model_name)
        self.cache = CacheManager(self.db)
        self.relevance_gate = RelevanceGate(self.client)
        self.deep_analyzer = DeepAnalyzer(self.client)
        
        self.semaphore = asyncio.Semaphore(3) # Max 3 concurrent LLM calls to prevent 429 errors on 15 RPM tier

    async def process_conversation(self, conv: Conversation) -> Optional[Analysis]:
        """
        Process a single conversation through the Relevance Gate and Deep Analysis.
        Returns the generated (or cached) Analysis object.
        """
        async with self.semaphore:
            # 1. Check if already processed with exact same prompt/schema versions
            # We use the deep_analysis versions since that's the final output stored in Analysis
            cached = await self.cache.get_cached_analysis(
                conversation_id=conv.id,
                model_name=self.model_name,
                prompt_version=self.deep_analyzer.prompt_version,
                schema_version=self.deep_analyzer.schema_version
            )
            if cached:
                logger.info(f"Cache hit for conversation {conv.id}")
                return cached

            logger.info(f"Processing conversation {conv.id} (Source ID: {conv.source_id})")
            
            # 2. Relevance Gate
            try:
                relevance_result = await self.relevance_gate.evaluate(conv.raw_content)
            except Exception as e:
                logger.error(f"Relevance gate failed for {conv.id}: {e}")
                error_status = "schema_failure" if "ValidationError" in str(type(e)) or "ValidationError" in str(e) else "api_failure"
                
                analysis_record = Analysis(
                    conversation_id=conv.id,
                    validation_status=error_status,
                    model_name=self.model_name
                )
                if not self.dry_run:
                    self.db.add(analysis_record)
                    await self.db.commit()
                return analysis_record

            analysis_record = Analysis(
                conversation_id=conv.id,
                relevance=str(relevance_result.is_relevant),
                relevance_reason=relevance_result.relevance_reason,
                evidence=relevance_result.evidence_span,
                ai_confidence=relevance_result.relevance_score,
                model_name=self.model_name,
                prompt_version=self.deep_analyzer.prompt_version,
                schema_version=self.deep_analyzer.schema_version
            )

            # 3. Deep Analysis (if relevant)
            if relevance_result.is_relevant:
                try:
                    deep_result = await self.deep_analyzer.analyze(conv.raw_content)
                    
                    # Populate fields
                    analysis_record.purchase_intent = deep_result.purchase_intent
                    analysis_record.shopping_stage = deep_result.shopping_stage
                    analysis_record.wishlist_intent = deep_result.wishlist_behavior
                    analysis_record.primary_barrier_category = deep_result.primary_barrier_category
                    analysis_record.primary_barrier_detail = deep_result.primary_barrier_detail
                    analysis_record.secondary_barriers = deep_result.secondary_barriers
                    analysis_record.uncertainty = deep_result.uncertainty
                    analysis_record.behavior = deep_result.behavior_type
                    analysis_record.workaround = deep_result.workaround
                    analysis_record.external_research = deep_result.external_research
                    analysis_record.product_category = deep_result.product_category
                    analysis_record.occasion = deep_result.occasion
                    analysis_record.comparison_behavior = deep_result.comparison_behavior
                    analysis_record.desired_information = deep_result.desired_information
                    analysis_record.unmet_need = deep_result.unmet_need
                    
                    # Store lowest confidence between relevance and deep analysis
                    analysis_record.ai_confidence = min(relevance_result.relevance_score, deep_result.ai_confidence)
                except Exception as e:
                    logger.error(f"Deep analysis failed for {conv.id}: {e}")
                    error_status = "schema_failure" if "ValidationError" in str(type(e)) or "ValidationError" in str(e) else "api_failure"
                    analysis_record.validation_status = error_status
                    if not self.dry_run:
                        self.db.add(analysis_record)
                        await self.db.commit()
                    return analysis_record
            
            if not self.dry_run:
                self.db.add(analysis_record)
                await self.db.commit()
                
            return analysis_record
