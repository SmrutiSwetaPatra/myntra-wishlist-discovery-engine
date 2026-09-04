from pydantic import BaseModel
from typing import Optional, List, Any

class ProductBase(BaseModel):
    name: str
    brand: str
    category: str
    gender: Optional[str] = None
    
    price: float
    original_price: Optional[float] = None
    
    rating: Optional[float] = None
    review_count: int = 0
    
    fit: Optional[str] = None
    material: Optional[str] = None
    color: Optional[str] = None
    availability: Optional[str] = "In Stock"
    description: Optional[str] = None
    
    images: Optional[List[str]] = None
    sizes: Optional[List[str]] = None
    
    quality_signals: Optional[Any] = None
    value_signals: Optional[Any] = None
    review_signals: Optional[Any] = None

class ProductResponse(ProductBase):
    id: int
    
    class Config:
        orm_mode = True

class ProductListResponse(BaseModel):
    products: List[ProductResponse]
    total_count: int
    page: int
    page_size: int
    total_pages: int
