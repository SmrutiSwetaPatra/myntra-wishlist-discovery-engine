from sqlalchemy import Column, Integer, String, Float, Text, JSON
from app.models.base import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    brand = Column(String, index=True, nullable=False)
    category = Column(String, index=True, nullable=False)
    gender = Column(String, index=True, nullable=True)
    
    price = Column(Float, nullable=False)
    original_price = Column(Float, nullable=True)
    
    rating = Column(Float, nullable=True)
    review_count = Column(Integer, default=0)
    
    # Text metadata
    fit = Column(String, nullable=True)
    material = Column(String, nullable=True)
    color = Column(String, nullable=True)
    availability = Column(String, default="In Stock")
    description = Column(Text, nullable=True)

    # JSON fields for arrays/objects (supported seamlessly by SQLAlchemy SQLite)
    images = Column(JSON, nullable=True) # array of strings
    sizes = Column(JSON, nullable=True) # array of strings
    
    quality_signals = Column(JSON, nullable=True)
    value_signals = Column(JSON, nullable=True)
    review_signals = Column(JSON, nullable=True)
