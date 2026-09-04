import asyncio
import logging
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import select
from app.db.session import AsyncSessionLocal
from app.models.conversations import Conversation
from app.models.analyses import Analysis
from app.engine.pipeline import AIPipeline

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Quality Gate Rules
NOISE_KEYWORDS = {"good", "nice", "awesome", "great app", "love it", "nice app", "super", "excellent", "very good", "great"}

def passes_quality_gate(text: str) -> bool:
    if not text:
        return False
    text = text.strip().lower()
    if not text:
        return False
    # Check exact match for generic noise
    if text in NOISE_KEYWORDS:
        return False
    return True

async def enrich_existing():
    metrics = {
        "total_candidates": 0,
        "quality_gate_excluded": 0,
        "duplicate_skipped": 0,
        "sent_to_gemini": 0,
        "successful_enrichment": 0,
        "schema_failure": 0,
        "api_failure": 0,
        "excluded_irrelevant": 0
    }
    
    async with AsyncSessionLocal() as session:
        query = select(Conversation)
        result = await session.execute(query)
        conversations = result.scalars().all()
        
        metrics["total_candidates"] = len(conversations)
        logger.info(f"Found {len(conversations)} conversations to process.")
        
        pipeline = AIPipeline(session)
        
        for conv in conversations:
            # 1. Deterministic Duplicate Detection (Already processed)
            existing = await session.execute(
                select(Analysis)
                .where(Analysis.conversation_id == conv.id)
                .limit(1)
            )
            if existing.scalar():
                logger.info(f"Skipping {conv.id} - already processed.")
                metrics["duplicate_skipped"] += 1
                continue
                
            # 2. Quality Gate
            if not passes_quality_gate(conv.raw_content):
                logger.info(f"Skipping {conv.id} - failed quality gate.")
                metrics["quality_gate_excluded"] += 1
                continue
                
            # 3. Process via Gemini Pipeline
            metrics["sent_to_gemini"] += 1
            logger.info(f"Enriching {conv.id}...")
            analysis_record = await pipeline.process_conversation(conv)
            
            if analysis_record:
                if analysis_record.validation_status in ["api_failure", "schema_failure"]:
                    # Already handled by pipeline.py exception block
                    metrics[analysis_record.validation_status] += 1
                else:
                    if analysis_record.relevance == "False" or analysis_record.relevance == "false":
                        analysis_record.validation_status = "excluded_general"
                        metrics["excluded_irrelevant"] += 1
                    elif analysis_record.wishlist_intent and analysis_record.wishlist_intent.lower() not in ["none", "null", ""]:
                        analysis_record.validation_status = "ai_direct_evidence"
                        metrics["successful_enrichment"] += 1
                    elif analysis_record.primary_barrier_category:
                        analysis_record.validation_status = "ai_indirect_evidence"
                        metrics["successful_enrichment"] += 1
                    else:
                        analysis_record.validation_status = "ai_unvalidated"
                        metrics["successful_enrichment"] += 1
                    
                    # Update status in db if pipeline didn't save the final status
                    session.add(analysis_record)
                    await session.commit()
                
        logger.info("--- ENRICHMENT METRICS ---")
        for k, v in metrics.items():
            logger.info(f"{k}: {v}")
        logger.info("Enrichment complete.")

if __name__ == "__main__":
    asyncio.run(enrich_existing())
