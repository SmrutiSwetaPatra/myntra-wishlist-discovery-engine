import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, DateTime, ForeignKey, Uuid, Integer, Text
from sqlalchemy.orm import relationship
from app.db.base import Base

class CollectionRun(Base):
    __tablename__ = "collection_runs"

    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    source_id = Column(Uuid(as_uuid=True), ForeignKey("sources.id", ondelete="CASCADE"), nullable=False)
    start_time = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    end_time = Column(DateTime(timezone=True), nullable=True)
    status = Column(String, nullable=False, default="running")
    records_fetched = Column(Integer, default=0)
    records_new = Column(Integer, default=0)
    records_duplicate = Column(Integer, default=0)
    error_message = Column(Text, nullable=True)

    source = relationship("Source", back_populates="runs")
    conversations = relationship("Conversation", back_populates="collection_run", cascade="all, delete-orphan")
