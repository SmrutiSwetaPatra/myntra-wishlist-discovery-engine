from sqlalchemy import Column, Integer, String, ForeignKey, Text, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.models.base import Base

class Decision(Base):
    __tablename__ = "decisions"
    
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    
    # Store these as JSON strings
    decision_factors = Column(Text, nullable=True)
    concerns = Column(Text, nullable=True)
    supporting_info = Column(Text, nullable=True)
    
    ai_summary = Column(Text, nullable=True)
    recommendation = Column(String, nullable=True)
    confidence = Column(String, nullable=True)
    
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    
    product = relationship("Product")

class Comparison(Base):
    __tablename__ = "comparisons"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Store JSON array of product IDs
    product_ids = Column(Text, nullable=False)
    
    # Store JSON strings
    comparison_factors = Column(Text, nullable=True)
    key_differences = Column(Text, nullable=True)
    recommendation = Column(Text, nullable=True)
    
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
