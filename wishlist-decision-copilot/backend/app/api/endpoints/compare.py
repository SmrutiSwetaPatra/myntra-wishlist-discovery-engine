from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.decision import CompareRequest, CompareResponse
from app.services import decision_service

router = APIRouter()

@router.post("/", response_model=CompareResponse)
def compare_products(request: CompareRequest, db: Session = Depends(get_db)):
    if len(request.product_ids) < 2:
        raise HTTPException(status_code=400, detail="At least 2 product IDs required for comparison")
        
    comparison = decision_service.compare_products(db, request.product_ids)
    if not comparison:
        raise HTTPException(status_code=404, detail="One or more products not found")
    return comparison
