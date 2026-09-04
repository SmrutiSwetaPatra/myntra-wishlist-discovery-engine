from pydantic import BaseModel
from typing import Optional, Any
from datetime import datetime

class AnalyticsEventRequest(BaseModel):
    event_type: str
    user_id: Optional[int] = None
    product_id: Optional[int] = None
    event_data: Optional[Any] = None

class AnalyticsEventResponse(AnalyticsEventRequest):
    id: int
    timestamp: datetime
    
    class Config:
        orm_mode = True
