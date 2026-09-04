from sqlalchemy.orm import Session
from sqlalchemy import or_, desc, asc
from app.models.product import Product
from typing import Optional
import math

def get_product(db: Session, product_id: int):
    return db.query(Product).filter(Product.id == product_id).first()

def search_products(
    db: Session, 
    q: Optional[str] = None,
    category: Optional[str] = None,
    gender: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    min_rating: Optional[float] = None,
    brand: Optional[str] = None,
    sort: Optional[str] = None,
    page: int = 1,
    page_size: int = 12
):
    query = db.query(Product)
    
    if q:
        # SQLite case-insensitive search using like() and lower() is generally handled by SQLite natively for ASCII,
        # but SQLAlchemy's ilike() provides cross-db compatibility. We can use ilike().
        search_term = f"%{q}%"
        query = query.filter(
            or_(
                Product.name.ilike(search_term),
                Product.brand.ilike(search_term),
                Product.category.ilike(search_term),
                Product.description.ilike(search_term)
            )
        )
        
    if category:
        query = query.filter(Product.category.ilike(category))
    if gender:
        query = query.filter(Product.gender.ilike(gender))
    if brand:
        query = query.filter(Product.brand.ilike(brand))
    if min_price is not None:
        query = query.filter(Product.price >= min_price)
    if max_price is not None:
        query = query.filter(Product.price <= max_price)
    if min_rating is not None:
        query = query.filter(Product.rating >= min_rating)
        
    # Sorting
    if sort == "price_asc":
        query = query.order_by(asc(Product.price))
    elif sort == "price_desc":
        query = query.order_by(desc(Product.price))
    elif sort == "rating":
        query = query.order_by(desc(Product.rating))
    elif sort == "reviews":
        query = query.order_by(desc(Product.review_count))
    else:
        # Default sort by id or relevance
        query = query.order_by(Product.id)
        
    total_count = query.count()
    total_pages = math.ceil(total_count / page_size) if total_count > 0 else 1
    
    offset = (page - 1) * page_size
    products = query.offset(offset).limit(page_size).all()
    
    return {
        "products": products,
        "total_count": total_count,
        "page": page,
        "page_size": page_size,
        "total_pages": total_pages
    }
