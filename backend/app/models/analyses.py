import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Float, ForeignKey, DateTime, Uuid, JSON
from sqlalchemy.orm import relationship
from app.db.base import Base

class Analysis(Base):
    __tablename__ = "analyses"

    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    conversation_id = Column(Uuid(as_uuid=True), ForeignKey("conversations.id", ondelete="CASCADE"), nullable=False)
    
    relevance = Column(String, nullable=True)
    relevance_reason = Column(String, nullable=True)
    purchase_intent = Column(String, nullable=True)
    shopping_stage = Column(String, nullable=True)
    wishlist_intent = Column(String, nullable=True)
    primary_barrier_category = Column(String, nullable=True)
    primary_barrier_detail = Column(String, nullable=True)
    secondary_barriers = Column(JSON, default=list)
    uncertainty = Column(String, nullable=True)
    behavior = Column(String, nullable=True)
    workaround = Column(String, nullable=True)
    external_research = Column(String, nullable=True)
    product_category = Column(String, nullable=True)
    occasion = Column(String, nullable=True)
    unmet_need = Column(String, nullable=True)
    comparison_behavior = Column(String, nullable=True)
    desired_information = Column(String, nullable=True)
    evidence = Column(String, nullable=True)
    
    ai_confidence = Column(Float, nullable=True)
    
    # Provenance
    model_name = Column(String, nullable=True)
    model_version = Column(String, nullable=True)
    prompt_version = Column(String, nullable=True)
    schema_version = Column(String, nullable=True)
    
    validation_status = Column(String, nullable=True)
    embedding = Column(JSON, nullable=True)
    
    analyzed_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    
    metadata_ = Column("metadata", JSON, default=dict)

    conversation = relationship("Conversation", back_populates="analyses")
