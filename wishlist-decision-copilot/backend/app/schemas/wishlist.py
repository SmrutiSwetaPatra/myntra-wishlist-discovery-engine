from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional
from app.schemas.product import ProductResponse

class WishlistItemBase(BaseModel):
    product_id: int

class WishlistItemResponse(WishlistItemBase):
    id: int
    wishlist_id: int
    added_at: datetime
    product: ProductResponse
    
    class Config:
        orm_mode = True

class WishlistResponse(BaseModel):
    id: int
    user_id: int
    items: List[WishlistItemResponse] = []
    
    class Config:
        orm_mode = True
