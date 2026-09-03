import uuid
from sqlalchemy import Column, String, DateTime, ForeignKey, Text, UniqueConstraint, Uuid, JSON
from sqlalchemy.orm import relationship
from app.db.base import Base

class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    source_id = Column(Uuid(as_uuid=True), ForeignKey("sources.id", ondelete="CASCADE"), nullable=False)
    collection_run_id = Column(Uuid(as_uuid=True), ForeignKey("collection_runs.id", ondelete="SET NULL"), nullable=True)
    
    external_id = Column(String, nullable=False, index=True)
    raw_content = Column(Text, nullable=False)
    author = Column(String, nullable=True)
    timestamp = Column(DateTime(timezone=True), nullable=True)
    source_url = Column(String, nullable=True)
    metadata_ = Column("metadata", JSON, default=dict)

    source = relationship("Source", back_populates="conversations")
    collection_run = relationship("CollectionRun", back_populates="conversations")
    analyses = relationship("Analysis", back_populates="conversation", cascade="all, delete-orphan")

    __table_args__ = (
        UniqueConstraint('source_id', 'external_id', name='uq_conversation_source_external_id'),
    )
