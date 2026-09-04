import json
import os
from sqlalchemy.orm import Session
from app.models.product import Product
from app.models.wishlist import User, Wishlist, WishlistItem

def seed_database(db: Session):
    # Check if products already exist
    if db.query(Product).first():
        return # Data already seeded
        
    print("Seeding DEMO data into database...")
    
    # Load from json file
    json_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "demo_products.json")
    with open(json_path, "r") as f:
        demo_products = json.load(f)
    
    # 1. Insert Products
    for p_data in demo_products:
        product = Product(**p_data)
        db.add(product)
    
    # 2. Insert Demo User & Wishlist
    demo_user = User(username="demo_user")
    db.add(demo_user)
    db.commit()
    db.refresh(demo_user)
    
    demo_wishlist = Wishlist(user_id=demo_user.id)
    db.add(demo_wishlist)
    db.commit()
    db.refresh(demo_wishlist)
    
    # 3. Add a few products to the demo wishlist (e.g. first 3 products)
    products = db.query(Product).limit(3).all()
    for p in products:
        item = WishlistItem(wishlist_id=demo_wishlist.id, product_id=p.id)
        db.add(item)
    
    db.commit()
    print("DEMO data successfully seeded.")
