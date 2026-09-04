import logging
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from app.db.session import AsyncSessionLocal
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

class QuantitativeEngine:
    async def execute_metrics(self, metadata_filters: dict = None, validation_status_filter: List[str] = None) -> List[str]:
        """
        Executes basic quantitative aggregations and returns strings representing the metrics.
        """
        metrics = []
        
        async with AsyncSessionLocal() as session:
            # Base query
            query_str = """
                SELECT 
                    a.primary_barrier_category, 
                    COUNT(*) as count
                FROM analyses a
                JOIN conversations c ON a.conversation_id = c.id
                WHERE 1=1
            """
            params = {}
            
            if validation_status_filter:
                # safe substitution for lists
                placeholders = ", ".join([f":v{i}" for i in range(len(validation_status_filter))])
                query_str += f" AND a.validation_status IN ({placeholders})"
                for i, v in enumerate(validation_status_filter):
                    params[f"v{i}"] = v
            
            if metadata_filters:
                for k, v in metadata_filters.items():
                    if k in ['primary_barrier_category', 'shopping_stage', 'purchase_intent', 'behavior_type', 'comparison_behavior', 'external_research', 'unmet_need']:
                        if v == '__not_null__':
                            query_str += f" AND a.{k} IS NOT NULL"
                        else:
                            query_str += f" AND a.{k} = :{k}"
                            params[k] = v
                            
            query_str += " GROUP BY a.primary_barrier_category ORDER BY count DESC"
            
            try:
                result = await session.execute(text(query_str), params)
                rows = result.fetchall()
                
                if rows:
                    metrics.append("Primary Barrier Distribution (Deterministic SQL):")
                    for r in rows:
                        cat = r[0] if r[0] else 'Uncategorized'
                        metrics.append(f"- {cat}: {r[1]} occurrences")
                
                # Get total denominator matching filters
                count_query = "SELECT COUNT(*) FROM analyses a WHERE 1=1"
                if validation_status_filter:
                    count_query += f" AND a.validation_status IN ({placeholders})"
                if metadata_filters:
                    for k, v in metadata_filters.items():
                        if k in ['primary_barrier_category', 'shopping_stage', 'purchase_intent', 'behavior_type', 'comparison_behavior', 'external_research', 'unmet_need']:
                            if v == '__not_null__':
                                count_query += f" AND a.{k} IS NOT NULL"
                            else:
                                count_query += f" AND a.{k} = :{k}"
                
                total_res = await session.execute(text(count_query), params)
                total = total_res.scalar()
                metrics.append(f"Total records matching criteria: {total}")
                
            except Exception as e:
                logger.error(f"Error calculating quantitative metrics: {e}")
                
        return metrics
