import logging
from typing import List, Optional
from pydantic import BaseModel, Field
from app.engine.gemini import GeminiClient
from app.engine.prompts import ROUTER_PROMPT

logger = logging.getLogger(__name__)

class ExecutionPlan(BaseModel):
    is_quantitative: bool = Field(description="True if the user is asking for exact counts, percentages, or statistical distributions.")
    requires_cross_source: bool = Field(description="True if comparing platforms (e.g., YouTube vs Google Play).")
    requires_segmentation: bool = Field(description="True if comparing user groups (e.g., high intent vs low intent).")
    
    validation_status_filter: Optional[List[str]] = Field(
        None, 
        description="List of validation statuses to filter by. Options: ['validated_relevant', 'ai_direct_evidence', 'indirect_pre_purchase', 'ai_indirect_evidence', 'ai_unvalidated']. Output null if no restriction requested. CRITICAL: For broad queries, output null to allow both direct and indirect evidence."
    )
    
    metadata_filters: Optional[str] = Field(
        None,
        description="A JSON string representing exact match filters to apply to metadata. E.g. '{\"shopping_stage\": \"decision\"}' or '{\"unmet_need\": \"__not_null__\"}'. Supported fields: shopping_stage, purchase_intent, primary_barrier_category, behavior_type, comparison_behavior, external_research, unmet_need. Return null if none."
    )
    
    semantic_query: str = Field(description="The underlying intent to search for in vector space. Often just the user's query.")
    
    insufficient_evidence_likely: bool = Field(description="True if the query asks for impossible stats like exact real-world conversion rates or demographic data we do not possess.")

class QueryRouter:
    def __init__(self, client: GeminiClient = None):
        self.client = client or GeminiClient()
        
    async def route(self, user_query: str, require_validated_only: bool = False) -> ExecutionPlan:
        # Ask LLM to parse the intent
        plan = await self.client.extract_structured(
            prompt=ROUTER_PROMPT,
            text=user_query,
            schema=ExecutionPlan
        )
        
        import json
        
        # Override with explicit API-level toggle if true
        if require_validated_only:
            plan.validation_status_filter = ["validated_relevant", "ai_direct_evidence", "indirect_pre_purchase", "ai_indirect_evidence"]
        elif not plan.validation_status_filter:
            # For broad queries where LLM outputs null, default to all usable evidence tiers
            plan.validation_status_filter = ["validated_relevant", "ai_direct_evidence", "indirect_pre_purchase", "ai_indirect_evidence"]
            
        # Parse the JSON string into a dict if present
        if plan.metadata_filters and isinstance(plan.metadata_filters, str):
            try:
                plan.metadata_filters = json.loads(plan.metadata_filters)
            except json.JSONDecodeError:
                plan.metadata_filters = None
                
        logger.info(f"Router produced execution plan: {plan.model_dump_json()}")
        return plan
