import json
from sqlalchemy.orm import Session
from app.models.analytics import AnalyticsEvent
from app.schemas.analytics import AnalyticsEventRequest

def track_event(db: Session, event: AnalyticsEventRequest):
    db_event = AnalyticsEvent(
        event_type=event.event_type,
        user_id=event.user_id,
        product_id=event.product_id,
        event_data=json.dumps(event.event_data) if event.event_data else None
    )
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    
    # Return matched format
    return {
        "id": db_event.id,
        "event_type": db_event.event_type,
        "user_id": db_event.user_id,
        "product_id": db_event.product_id,
        "event_data": json.loads(db_event.event_data) if db_event.event_data else None,
        "timestamp": db_event.timestamp
    }

def get_insights(db: Session):
    # A simple stub to fetch recent events for MVP insights
    events = db.query(AnalyticsEvent).order_by(AnalyticsEvent.timestamp.desc()).limit(50).all()
    results = []
    for e in events:
        results.append({
            "id": e.id,
            "event_type": e.event_type,
            "user_id": e.user_id,
            "product_id": e.product_id,
            "event_data": json.loads(e.event_data) if e.event_data else None,
            "timestamp": e.timestamp
        })
    return results
