from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.wishlist import WishlistResponse, WishlistItemBase, WishlistItemResponse
from app.services import wishlist_service
from app.models.wishlist import User
from app.models.product import Product

router = APIRouter()

def get_demo_user_id(db: Session) -> int:
    demo_user = db.query(User).filter(User.username == "demo_user").first()
    if not demo_user:
        raise HTTPException(status_code=404, detail="Demo user not found. Did you run the seed script?")
    return demo_user.id

@router.get("/", response_model=WishlistResponse)
def get_my_wishlist(db: Session = Depends(get_db)):
    user_id = get_demo_user_id(db)
    wishlist = wishlist_service.get_wishlist(db, user_id)
    if not wishlist:
        raise HTTPException(status_code=404, detail="Wishlist not found")
        
    return wishlist

@router.post("/items", response_model=WishlistItemResponse)
def add_item_to_wishlist(item: WishlistItemBase, db: Session = Depends(get_db)):
    user_id = get_demo_user_id(db)
    wishlist = wishlist_service.get_wishlist(db, user_id)
    
    if not wishlist:
        raise HTTPException(status_code=404, detail="Wishlist not found")
        
    # verify product exists
    product = db.query(Product).filter(Product.id == item.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
        
    added_item = wishlist_service.add_to_wishlist(db, wishlist.id, item.product_id)
    return added_item

@router.delete("/items/{product_id}")
def remove_item_from_wishlist(product_id: int, db: Session = Depends(get_db)):
    user_id = get_demo_user_id(db)
    wishlist = wishlist_service.get_wishlist(db, user_id)
    
    if not wishlist:
        raise HTTPException(status_code=404, detail="Wishlist not found")
        
    success = wishlist_service.remove_from_wishlist(db, wishlist.id, product_id)
    if not success:
        raise HTTPException(status_code=404, detail="Item not found in wishlist")
        
    return {"message": "Item removed from wishlist"}
