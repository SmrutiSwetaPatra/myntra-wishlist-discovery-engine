import os
import json
import logging
import asyncio
from google import genai
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload
from app.core.config import settings
from app.db.session import AsyncSessionLocal
from app.models.analyses import Analysis
from app.models.conversations import Conversation
from app.engine.rate_limiter import global_limiter

logger = logging.getLogger(__name__)

class Embedder:
    def __init__(self, model_name: str = "models/gemini-embedding-2"):
        self.api_key = settings.GEMINI_API_KEY
        self.model_name = model_name

    def _create_dense_document(self, analysis: Analysis, conversation: Conversation) -> str:
        """
        Creates a highly-dense composite document containing the raw conversation plus 
        all the AI-extracted fields without mutating the original source of truth.
        """
        parts = []
        if conversation.raw_content:
            parts.append(f"RAW TEXT: {conversation.raw_content}")
        
        if conversation.source_url:
            parts.append(f"SOURCE URL: {conversation.source_url}")
            
        parts.append("--- AI BEHAVIORAL ANNOTATIONS ---")
        
        if analysis.primary_barrier_category:
            parts.append(f"Primary Barrier: {analysis.primary_barrier_category}")
        if analysis.primary_barrier_detail:
            parts.append(f"Barrier Detail: {analysis.primary_barrier_detail}")
        if analysis.purchase_intent:
            parts.append(f"Purchase Intent: {analysis.purchase_intent}")
        if analysis.shopping_stage:
            parts.append(f"Shopping Stage: {analysis.shopping_stage}")
        if analysis.wishlist_intent:
            parts.append(f"Wishlist Behavior: {analysis.wishlist_intent}")
        if analysis.uncertainty:
            parts.append(f"Uncertainty: {analysis.uncertainty}")
        if analysis.comparison_behavior:
            parts.append(f"Comparison Behavior: {analysis.comparison_behavior}")
        if analysis.external_research:
            parts.append(f"External Research: {analysis.external_research}")
        if analysis.occasion:
            parts.append(f"Occasion: {analysis.occasion}")
        if analysis.product_category:
            parts.append(f"Product Category: {analysis.product_category}")
        if analysis.unmet_need:
            parts.append(f"Unmet Need: {analysis.unmet_need}")
            
        return "\n".join(parts)

    async def generate_embedding(self, text: str) -> list[float]:
        await global_limiter.acquire()
        client = genai.Client(api_key=self.api_key)
        response = await client.aio.models.embed_content(
            model=self.model_name,
            contents=text,
        )
        # return the list of floats
        return response.embeddings[0].values

    async def backfill(self):
        async with AsyncSessionLocal() as session:
            established_tiers = [
                "validated_relevant",
                "ai_direct_evidence",
                "indirect_pre_purchase",
                "ai_indirect_evidence"
            ]

            result = await session.execute(
                select(Analysis)
                .options(joinedload(Analysis.conversation).joinedload(Conversation.source))
                .where(Analysis.validation_status.in_(established_tiers))
                .where(Analysis.embedding.is_(None))
                .order_by((Analysis.validation_status == "ai_direct_evidence").desc())
                .limit(5)
            )
            analyses = result.scalars().all()
            
            if not analyses:
                print("No records need embedding.")
                return

            print(f"Found {len(analyses)} records to embed.")
            
            for i, a in enumerate(analyses):
                if not a.conversation:
                    continue
                    
                doc = self._create_dense_document(a, a.conversation)
                try:
                    embedding = await self.generate_embedding(doc)
                    a.embedding = embedding
                    
                    if (i + 1) % 10 == 0:
                        await session.commit()
                        print(f"Embedded {i + 1}/{len(analyses)}")
                except Exception as e:
                    print(f"Error embedding {a.id}: {e}")
                    
            await session.commit()
            print("Backfill complete.")

if __name__ == "__main__":
    from app.core.logging import setup_logging
    setup_logging()
    
    embedder = Embedder()
    asyncio.run(embedder.backfill())
