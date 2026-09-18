"""SavedArea bookmark entity SQLAlchemy model."""
import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship

from app.db.base import Base


class SavedArea(Base):
    __tablename__ = "saved_areas"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    area_id = Column(String(64), ForeignKey("areas.id", ondelete="CASCADE"), nullable=False, index=True)
    notes = Column(String(255), nullable=True)
    alert_notifications_enabled = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), server_default=func.now())

    # Relationships
    user = relationship("User", back_populates="saved_areas")
    area = relationship("Area", back_populates="saved_areas")
