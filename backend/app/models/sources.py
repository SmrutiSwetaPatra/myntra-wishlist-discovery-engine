import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, DateTime, Uuid, JSON
from sqlalchemy.orm import relationship
from app.db.base import Base

class Source(Base):
    __tablename__ = "sources"

    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    platform = Column(String, nullable=False, index=True)
    name = Column(String, nullable=False)
    base_url = Column(String, nullable=True)
    metadata_ = Column("metadata", JSON, default=dict)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    runs = relationship("CollectionRun", back_populates="source", cascade="all, delete-orphan")
    conversations = relationship("Conversation", back_populates="source", cascade="all, delete-orphan")
