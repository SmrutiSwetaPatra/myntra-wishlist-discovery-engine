import logging
from typing import List, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func
from sqlalchemy.orm import joinedload
from app.models.analyses import Analysis
from app.models.conversations import Conversation
from app.engine.gemini import GeminiClient
from app.engine.schemas import InsightSchema
from app.engine.prompts import AGGREGATION_PROMPT_V1
from app.models.insights import Insight

logger = logging.getLogger(__name__)

class InsightAggregator:
    def __init__(self, db_session: AsyncSession, client: GeminiClient, dry_run: bool = False):
        self.db = db_session
        self.client = client
        self.dry_run = dry_run

    async def _compute_metrics(self) -> Dict[str, Any]:
        """Stage 3A: Deterministic Metrics from SQLite"""
        logger.info("Computing deterministic metrics for aggregation")
        
        # Load all relevant analyses with joined relations to avoid lazy loading MissingGreenlet
        result = await self.db.execute(
            select(Analysis)
            .options(joinedload(Analysis.conversation).joinedload(Conversation.source))
            .where(Analysis.validation_status.in_([
                "validated_relevant", 
                "indirect_pre_purchase",
                "ai_direct_evidence",
                "ai_indirect_evidence"
            ]))
        )
        analyses = result.scalars().all()
        
        metrics = {
            "total_relevant": len(analyses),
            "sources": {},
            "barriers": {},
            "behaviors": {},
            "uncertainties": {}
        }
        
        for a in analyses:
            src = a.conversation.source.platform if a.conversation and a.conversation.source else "unknown"
            metrics["sources"][src] = metrics["sources"].get(src, 0) + 1
            
            cat = a.primary_barrier_category
            if cat:
                if cat not in metrics["barriers"]:
                    metrics["barriers"][cat] = {"count": 0, "sources": set()}
                metrics["barriers"][cat]["count"] += 1
                metrics["barriers"][cat]["sources"].add(src)
                
            beh = a.behavior
            if beh:
                if beh not in metrics["behaviors"]:
                    metrics["behaviors"][beh] = {"count": 0, "sources": set()}
                metrics["behaviors"][beh]["count"] += 1
                metrics["behaviors"][beh]["sources"].add(src)
                
            unc = a.uncertainty
            if unc:
                if unc not in metrics["uncertainties"]:
                    metrics["uncertainties"][unc] = {"count": 0, "sources": set()}
                metrics["uncertainties"][unc]["count"] += 1
                metrics["uncertainties"][unc]["sources"].add(src)
                
        # Convert sets to lists for JSON serialization
        for k in metrics["barriers"]:
            metrics["barriers"][k]["sources"] = list(metrics["barriers"][k]["sources"])
        for k in metrics["behaviors"]:
            metrics["behaviors"][k]["sources"] = list(metrics["behaviors"][k]["sources"])
        for k in metrics["uncertainties"]:
            metrics["uncertainties"][k]["sources"] = list(metrics["uncertainties"][k]["sources"])
            
        # Add the raw records to the payload so the LLM can extract IDs and classify direct/indirect
        metrics["records"] = []
        for a in analyses:
            metrics["records"].append({
                "conversation_id": str(a.conversation_id),
                "validation_status": a.validation_status,
                "evidence": a.evidence,
                "raw_content": a.conversation.raw_content if a.conversation else None,
                "primary_barrier": f"{a.primary_barrier_category} - {a.primary_barrier_detail}",
                "uncertainty": a.uncertainty,
                "behavior": a.behavior
            })
            
        return metrics

    async def _synthesize_insights(self, metrics: Dict[str, Any]) -> List[InsightSchema]:
        """Stage 3B: AI Synthesis"""
        # We need a schema for multiple insights, so we'll wrap InsightSchema in a list via a parent schema
        from pydantic import BaseModel
        
        class InsightCollection(BaseModel):
            insights: List[InsightSchema]
            
        import json
        metrics_text = json.dumps(metrics, indent=2)
        
        collection = await self.client.extract_structured(
            prompt=AGGREGATION_PROMPT_V1,
            text=metrics_text,
            schema=InsightCollection
        )
        return collection.insights

    async def run(self) -> None:
        metrics = await self._compute_metrics()
        if metrics["total_relevant"] == 0:
            logger.info("No relevant analyses to aggregate.")
            return

        logger.info("Running AI synthesis on computed metrics")
        insights = await self._synthesize_insights(metrics)
        
        if not self.dry_run:
            # Clear old insights
            from sqlalchemy import delete
            await self.db.execute(delete(Insight))
            
            for insight_schema in insights:
                insight = Insight(
                    title=insight_schema.title,
                    description=insight_schema.description,
                    category=insight_schema.category,
                    evidence_count=insight_schema.evidence_count,
                    unique_conversation_count=insight_schema.evidence_count, # Simplified
                    source_count=len(insight_schema.sources_present),
                    source_diversity=len(insight_schema.sources_present) / len(metrics["sources"]) if len(metrics["sources"]) > 0 else 0,
                    ai_confidence=insight_schema.confidence_score,
                    direct_vs_indirect=insight_schema.direct_vs_indirect,
                    supporting_conversation_ids=insight_schema.supporting_conversation_ids,
                    sources_present=insight_schema.sources_present
                )
                self.db.add(insight)
            await self.db.commit()
            logger.info(f"Saved {len(insights)} synthesized insights to DB.")
        else:
            logger.info(f"DRY RUN: Generated {len(insights)} insights.")
