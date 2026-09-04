from sqlalchemy.orm import Session
from app.models.wishlist import Wishlist, WishlistItem

def get_wishlist(db: Session, user_id: int):
    return db.query(Wishlist).filter(Wishlist.user_id == user_id).first()

def add_to_wishlist(db: Session, wishlist_id: int, product_id: int):
    # Prevent duplicate entries
    existing = db.query(WishlistItem).filter(
        WishlistItem.wishlist_id == wishlist_id,
        WishlistItem.product_id == product_id
    ).first()
    if existing:
        return existing
        
    db_item = WishlistItem(wishlist_id=wishlist_id, product_id=product_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def remove_from_wishlist(db: Session, wishlist_id: int, product_id: int):
    db_item = db.query(WishlistItem).filter(
        WishlistItem.wishlist_id == wishlist_id,
        WishlistItem.product_id == product_id
    ).first()
    if db_item:
        db.delete(db_item)
        db.commit()
        return True
    return False
