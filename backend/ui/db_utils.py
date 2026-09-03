import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, text
from sqlalchemy.orm import joinedload
from app.db.session import AsyncSessionLocal
from app.models.analyses import Analysis
from app.models.conversations import Conversation
from app.models.sources import Source

import threading

def run_async(coro):
    """Utility to run async functions in Streamlit safely without nest_asyncio"""
    result = None
    exception = None
    def target():
        nonlocal result, exception
        try:
            result = asyncio.run(coro)
        except Exception as e:
            exception = e
            
    t = threading.Thread(target=target)
    t.start()
    t.join()
    
    if exception:
        raise exception
    return result

async def _get_dashboard_metrics():
    async with AsyncSessionLocal() as session:
        # Total Reviews
        total_conv = await session.execute(select(func.count(Conversation.id)))
        total_reviews = total_conv.scalar()
        
        # Sources Count
        sources_res = await session.execute(
            select(Source.platform, func.count(Conversation.id))
            .join(Conversation, Source.id == Conversation.source_id)
            .group_by(Source.platform)
        )
        sources_count = {}
        mapping = {"playstore": "Google Play", "appstore": "Apple App Store", "youtube": "YouTube"}
        for row in sources_res.all():
            display_name = mapping.get(row[0], row[0])
            sources_count[display_name] = row[1]
        
        # Analyzed Count
        total_analyzed = await session.execute(select(func.count(Analysis.id)))
        analyzed = total_analyzed.scalar()
        
        # Validation Status Counts
        val_res = await session.execute(
            select(Analysis.validation_status, func.count(Analysis.id))
            .group_by(Analysis.validation_status)
        )
        
        val_counts = {
            "Direct Evidence": 0,
            "Indirect Pre-Purchase": 0,
            "Needs Validation": 0,
            "Excluded": 0,
            "API Failure": 0,
            "Schema Failure": 0
        }
        
        for row in val_res.all():
            v = row[0]
            if v in ["validated_relevant", "ai_direct_evidence"]:
                val_counts["Direct Evidence"] += row[1]
            elif v in ["indirect_pre_purchase", "ai_indirect_evidence"]:
                val_counts["Indirect Pre-Purchase"] += row[1]
            elif v in ["ai_unvalidated", "needs_review"]:
                val_counts["Needs Validation"] += row[1]
            elif v in ["excluded_general", "excluded_post_purchase", "excluded_ambiguous"]:
                val_counts["Excluded"] += row[1]
            elif v == "api_failure":
                val_counts["API Failure"] += row[1]
            elif v == "schema_failure":
                val_counts["Schema Failure"] += row[1]
        
        # Evidence Quality Distribution
        quality_res = await session.execute(
            select(Analysis.relevance, func.count(Analysis.id))
            .where(Analysis.validation_status.is_not(None))
            .group_by(Analysis.relevance)
        )
        quality_dist = {row[0]: row[1] for row in quality_res.all()}
        
        # Top Barriers
        barrier_res = await session.execute(
            select(Analysis.primary_barrier_category, func.count(Analysis.id))
            .where(Analysis.primary_barrier_category.is_not(None))
            .group_by(Analysis.primary_barrier_category)
            .order_by(func.count(Analysis.id).desc())
            .limit(10)
        )
        barriers = {row[0]: row[1] for row in barrier_res.all()}
        
        # Shopping Stage
        stage_res = await session.execute(
            select(Analysis.shopping_stage, func.count(Analysis.id))
            .where(Analysis.shopping_stage.is_not(None))
            .group_by(Analysis.shopping_stage)
        )
        stages = {row[0]: row[1] for row in stage_res.all()}
        
        # Purchase Intent
        intent_res = await session.execute(
            select(Analysis.purchase_intent, func.count(Analysis.id))
            .where(Analysis.purchase_intent.is_not(None))
            .group_by(Analysis.purchase_intent)
        )
        intents = {row[0]: row[1] for row in intent_res.all()}
        
        return {
            "total_reviews": total_reviews,
            "sources": sources_count,
            "analyzed": analyzed,
            "validation_status": val_counts,
            "quality": quality_dist,
            "barriers": barriers,
            "stages": stages,
            "intents": intents
        }

def get_dashboard_metrics():
    return run_async(_get_dashboard_metrics())
async def _get_explorer_data(filters: dict = None):
    async with AsyncSessionLocal() as session:
        query = (
            select(Analysis, Conversation, Source)
            .join(Conversation, Analysis.conversation_id == Conversation.id)
            .join(Source, Conversation.source_id == Source.id)
        )
        
        if filters:
            if filters.get("search_text"):
                query = query.where(Conversation.raw_content.ilike(f"%{filters['search_text']}%"))
            if filters.get("source") and filters["source"] != "All":
                reverse_mapping = {"Google Play": "playstore", "Apple App Store": "appstore", "YouTube": "youtube"}
                db_source = reverse_mapping.get(filters["source"], filters["source"])
                query = query.where(Source.platform == db_source)
            if filters.get("tier") and filters["tier"] != "All":
                tier_label = filters["tier"]
                if tier_label == "All Valid Evidence":
                    query = query.where(
                        Analysis.validation_status.in_([
                            "validated_relevant",
                            "ai_direct_evidence",
                            "indirect_pre_purchase",
                            "ai_indirect_evidence",
                            "ai_unvalidated",
                            "needs_review"
                        ])
                    )
                elif tier_label == "Direct Evidence":
                    query = query.where(
                        Analysis.validation_status.in_([
                            "validated_relevant",
                            "ai_direct_evidence"
                        ])
                    )
                elif tier_label == "Indirect Pre-Purchase":
                    query = query.where(
                        Analysis.validation_status.in_([
                            "indirect_pre_purchase",
                            "ai_indirect_evidence"
                        ])
                    )
                elif tier_label == "Needs Validation":
                    query = query.where(
                        Analysis.validation_status.in_([
                            "ai_unvalidated",
                            "needs_review"
                        ])
                    )
                elif tier_label == "Excluded":
                    query = query.where(
                        Analysis.validation_status.in_([
                            "excluded_general", 
                            "excluded_post_purchase", 
                            "excluded_ambiguous"
                        ])
                    )

            if filters.get("barrier") and filters["barrier"] != "All":
                query = query.where(Analysis.primary_barrier_category == filters["barrier"])
            if filters.get("intent") and filters["intent"] != "All":
                query = query.where(Analysis.purchase_intent == filters["intent"])
            if filters.get("stage") and filters["stage"] != "All":
                query = query.where(Analysis.shopping_stage == filters["stage"])
                
        query = query.order_by(Analysis.analyzed_at.desc())
        
        result = await session.execute(query)
        
        data = []
        mapping = {"playstore": "Google Play", "appstore": "Apple App Store", "youtube": "YouTube"}
        for a, c, s in result.all():
            if a.validation_status in [
                "validated_relevant",
                "ai_direct_evidence"
            ]:
                dvi = "Direct Evidence"
            elif a.validation_status in [
                "indirect_pre_purchase",
                "ai_indirect_evidence"
            ]:
                dvi = "Indirect Pre-Purchase"
            elif a.validation_status in [
                "ai_unvalidated",
                "needs_review"
            ]:
                dvi = "Needs Validation"
            elif a.validation_status in [
                "excluded_general", 
                "excluded_post_purchase", 
                "excluded_ambiguous"
            ]:
                dvi = "Excluded"
            elif a.validation_status == "api_failure":
                dvi = "API Failure"
            elif a.validation_status == "schema_failure":
                dvi = "Schema Failure"
            else:
                dvi = "Other"
                
            data.append({
                "id": str(a.conversation_id),
                "text": c.raw_content,
                "timestamp": c.metadata_.get("timestamp", "Unknown") if c.metadata_ else "Unknown",
                "source": mapping.get(s.platform, s.platform),
                "url": c.metadata_.get("url", "") if c.metadata_ else "",
                "validation_status": a.validation_status,
                "relevance": a.relevance,
                "purchase_intent": a.purchase_intent,
                "shopping_stage": a.shopping_stage,
                "primary_barrier": a.primary_barrier_category,
                "secondary_barrier": ", ".join(a.secondary_barriers) if a.secondary_barriers else a.uncertainty,
                "ai_confidence": a.ai_confidence,
                "direct_vs_indirect": dvi
            })
        return data

def get_explorer_data(filters: dict = None):
    return run_async(_get_explorer_data(filters))
