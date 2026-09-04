from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.decision import DecisionRequest, DecisionResponse
from app.services import decision_service

router = APIRouter()

@router.post("/analyze", response_model=DecisionResponse)
def analyze_decision(request: DecisionRequest, db: Session = Depends(get_db)):
    decision = decision_service.analyze_product_decision(db, request.product_id)
    if not decision:
        raise HTTPException(status_code=404, detail="Product not found")
    return decision
