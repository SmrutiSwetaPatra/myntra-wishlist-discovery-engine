import uuid
from sqlalchemy import Column, String, Integer, Float, Text, Uuid, JSON
from app.db.base import Base

class Insight(Base):
    __tablename__ = "insights"

    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    category = Column(String, nullable=True)
    
    # Deterministic metrics
    evidence_count = Column(Integer, default=0)
    unique_conversation_count = Column(Integer, default=0)
    source_count = Column(Integer, default=0)
    source_diversity = Column(Float, default=0.0)
    
    # AI Qualitative metric
    ai_confidence = Column(Float, nullable=True)
    
    direct_vs_indirect = Column(String, nullable=True)
    supporting_conversation_ids = Column(JSON, default=list)
    
    sources_present = Column(JSON, default=list)
    metadata_ = Column("metadata", JSON, default=dict)
