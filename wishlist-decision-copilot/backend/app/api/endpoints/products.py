from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.schemas.product import ProductResponse, ProductListResponse
from app.services import product_service
import json

router = APIRouter()

@router.get("/", response_model=ProductListResponse)
def get_products(
    q: Optional[str] = None,
    category: Optional[str] = None,
    gender: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    min_rating: Optional[float] = None,
    brand: Optional[str] = None,
    sort: Optional[str] = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(12, ge=1, le=100),
    db: Session = Depends(get_db)
):
    result = product_service.search_products(
        db=db, q=q, category=category, gender=gender, min_price=min_price, 
        max_price=max_price, min_rating=min_rating, brand=brand, 
        sort=sort, page=page, page_size=page_size
    )
    
    # SQLite JSON columns return the actual JSON list/dict automatically in SQLAlchemy 2.0 when mapped with JSON
    # so we do not need json.loads here.
    return result

@router.get("/{product_id}", response_model=ProductResponse)
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = product_service.get_product(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    return product
