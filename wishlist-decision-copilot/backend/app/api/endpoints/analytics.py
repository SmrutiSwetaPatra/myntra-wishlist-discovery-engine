from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.schemas.analytics import AnalyticsEventRequest, AnalyticsEventResponse
from app.services import analytics_service

router = APIRouter()

@router.post("/events", response_model=AnalyticsEventResponse)
def track_event(event: AnalyticsEventRequest, db: Session = Depends(get_db)):
    return analytics_service.track_event(db, event)

@router.get("/insights", response_model=List[AnalyticsEventResponse])
def get_insights(db: Session = Depends(get_db)):
    return analytics_service.get_insights(db)
