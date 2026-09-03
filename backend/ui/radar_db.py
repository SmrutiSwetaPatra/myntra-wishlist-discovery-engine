from sqlalchemy import select, func, case
from app.models.analyses import Analysis
from app.models.conversations import Conversation
from app.models.sources import Source
from app.db.session import AsyncSessionLocal
from ui.db_utils import run_async

async def _get_opportunities():
    async with AsyncSessionLocal() as session:
        # Get counts grouped by barrier and unmet need
        valid_statuses = ['validated_relevant', 'indirect_pre_purchase', 'ai_direct_evidence', 'ai_indirect_evidence']
        
        query = (
            select(
                Analysis.primary_barrier_category,
                Analysis.unmet_need,
                Analysis.validation_status,
                Conversation.raw_content,
                Analysis.conversation_id
            )
            .join(Conversation, Analysis.conversation_id == Conversation.id)
            .where(Analysis.primary_barrier_category.is_not(None))
            .where(Analysis.validation_status.in_(valid_statuses))
        )
        
        result = await session.execute(query)
        rows = result.all()
        
        # Aggregate in python
        barriers = {}
        for row in rows:
            cat = row.primary_barrier_category
            if cat not in barriers:
                barriers[cat] = {
                    "volume": 0,
                    "direct_count": 0,
                    "indirect_count": 0,
                    "unmet_needs": set(),
                    "all_reviews": []
                }
            
            barriers[cat]["volume"] += 1
            if row.validation_status in ['validated_relevant', 'ai_direct_evidence']:
                barriers[cat]["direct_count"] += 1
            else:
                barriers[cat]["indirect_count"] += 1
                
            if row.unmet_need:
                barriers[cat]["unmet_needs"].add(row.unmet_need)
                
            barriers[cat]["all_reviews"].append({
                "text": row.raw_content,
                "tier": row.validation_status,
                "id": str(row.conversation_id),
                "unmet_need": row.unmet_need
            })
                
        opportunities = []
        for cat, data in sorted(barriers.items(), key=lambda x: x[1]["volume"], reverse=True):
            needs_list = list(data["unmet_needs"])
            if len(needs_list) > 1:
                # Combine up to 2 for readability
                display_need = f"{needs_list[0]} (and {len(needs_list)-1} other needs)"
            elif needs_list:
                display_need = needs_list[0]
            else:
                display_need = "Not specified"
                
            strength = "High" if data["direct_count"] > 0 else "Medium" if data["indirect_count"] > 1 else "Low"
            
            # Select representative evidence matching the primary need
            exact_matches = [
                r for r in data["all_reviews"] 
                if needs_list and r["unmet_need"] == needs_list[0]
            ]
            
            # Limit to top 3
            representative_reviews = exact_matches[:3]
            
            # Remove unmet_need from the dictionary for cleaner output
            for rev in representative_reviews:
                rev.pop("unmet_need", None)
            
            opportunities.append({
                "barrier": cat,
                "unmet_need": display_need,
                "volume": data["volume"],
                "direct_count": data["direct_count"],
                "indirect_count": data["indirect_count"],
                "strength": strength,
                "representative_reviews": representative_reviews
            })
            
        return opportunities

def get_opportunities():
    return run_async(_get_opportunities())
