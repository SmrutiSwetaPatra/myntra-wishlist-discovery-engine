from pydantic import BaseModel
from typing import List, Any, Optional
from datetime import datetime

class DecisionRequest(BaseModel):
    product_id: int

class DecisionResponse(BaseModel):
    id: int
    product_id: int
    decision_factors: Any
    concerns: Any
    supporting_info: Any
    ai_summary: Optional[str] = None
    recommendation: Optional[str] = None
    confidence: Optional[str] = None
    timestamp: datetime
    
    class Config:
        orm_mode = True

class CompareRequest(BaseModel):
    product_ids: List[int]

class CompareResponse(BaseModel):
    id: int
    product_ids: List[int]
    comparison_factors: Any
    key_differences: Any
    recommendation: Any
    timestamp: datetime
    
    class Config:
        orm_mode = True
