from typing import Optional, List
from pydantic import BaseModel, Field

class RelevanceDecision(BaseModel):
    is_relevant: bool = Field(description="Whether the conversation provides meaningful evidence for understanding wishlist to purchase conversion behavior")
    relevance_score: float = Field(description="Score between 0.0 and 1.0 indicating confidence in the relevance decision")
    relevance_reason: str = Field(description="Brief explanation of why the conversation is or is not relevant")
    evidence_span: Optional[str] = Field(None, description="The exact text snippet that supports the relevance decision, if applicable")

class QueryRelevanceDecision(BaseModel):
    relevant: bool = Field(description="True if the evidence actually helps answer the user's specific question.")
    relevance_score: float = Field(description="Score between 0.0 and 1.0 indicating how strongly the evidence answers the question.")
    reason: str = Field(description="Short explanation of why this evidence is or isn't relevant to the specific question.")

class DeepAnalysis(BaseModel):
    purchase_intent: Optional[str] = Field(None, description="The user's intent to purchase (e.g. high, medium, low, unknown)")
    shopping_stage: Optional[str] = Field(None, description="Where the user is in their shopping journey (e.g. discovery, consideration, decision)")
    wishlist_behavior: Optional[str] = Field(None, description="How the user interacts with the wishlist or saved items")
    primary_barrier_category: Optional[str] = Field(None, description="The main category of the barrier preventing purchase (e.g. Price, Fit, Quality, Availability, Other)")
    primary_barrier_detail: Optional[str] = Field(None, description="Specific detail about the primary barrier")
    secondary_barriers: List[str] = Field(default_factory=list, description="Other barriers mentioned that prevent purchase")
    uncertainty: Optional[str] = Field(None, description="What the user is uncertain about")
    behavior_type: Optional[str] = Field(None, description="Observed user behavior (e.g. purchase postponement, cart abandonment, workaround)")
    product_category: Optional[str] = Field(None, description="The category of the fashion product mentioned")
    occasion: Optional[str] = Field(None, description="The occasion the product is for")
    comparison_behavior: Optional[str] = Field(None, description="How the user compares this product with others or across platforms")
    external_research: Optional[str] = Field(None, description="Research the user does outside the app (e.g. checking YouTube reviews)")
    workaround: Optional[str] = Field(None, description="Actions the user takes to overcome a barrier")
    desired_information: Optional[str] = Field(None, description="Information the user wishes they had to make a decision")
    unmet_need: Optional[str] = Field(None, description="A need that the product or platform is failing to fulfill")
    evidence: Optional[str] = Field(None, description="Direct quote or specific evidence from the text supporting this analysis")
    ai_confidence: float = Field(description="AI's assessed confidence in this extraction between 0.0 and 1.0")

class InsightSchema(BaseModel):
    title: str = Field(description="A concise, actionable title for the insight")
    description: str = Field(description="A detailed description of the synthesized insight")
    category: str = Field(description="The category of insight (e.g. 'Barrier', 'Behavior', 'Uncertainty', 'Opportunity')")
    evidence_count: int = Field(description="The number of underlying conversations/records that support this insight")
    confidence_score: float = Field(description="AI confidence in this insight synthesis (0.0 to 1.0)")
    sources_present: List[str] = Field(description="List of platforms where this insight was observed")
    direct_vs_indirect: str = Field(description="'validated_direct_evidence' if based on direct wishlist records, 'supporting_indirect_evidence' if based on general pre-purchase barriers")
    supporting_conversation_ids: Optional[List[str]] = Field(None, description="List of specific conversation IDs that support this insight")

class EvidenceCard(BaseModel):
    conversation_id: str
    source: str
    source_url: Optional[str]
    raw_text: str
    validation_status: str
    ai_confidence: Optional[float]
    direct_indirect_classification: Optional[str]
    relevance_score: Optional[float]

class CopilotResponse(BaseModel):
    answer: str = Field(description="The synthesized answer grounded entirely in the provided evidence. Use markdown.")
    query_type: str = Field(description="The type of query executed (Semantic, Quantitative, etc).")
    confidence: str = Field(description="'high', 'medium', or 'low' based on evidence quality and volume.")
    insufficient_evidence: bool = Field(description="True if the dataset cannot reliably answer this question.")
    metrics: List[str] = Field(description="Any deterministic metrics calculated (e.g. '3 out of 7 validated records mention price'). Empty if qualitative.")
    evidence_cards: List[EvidenceCard] = Field(description="Structured evidence supporting the answer.")
    limitations: List[str] = Field(description="Warnings about sample size, missing demographics, or lack of direct evidence.")
    sources_used: List[str] = Field(description="List of sources (e.g. 'Google Play', 'YouTube') where evidence was found.")
