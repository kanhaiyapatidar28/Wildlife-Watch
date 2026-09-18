"""Alert entity SQLAlchemy model."""
from datetime import datetime, timezone
from typing import Optional
from sqlalchemy import Column, String, Text, Boolean, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from pydantic import BaseModel

from app.db.base import Base


class Alert(Base):
    __tablename__ = "alerts"

    id = Column(String(64), primary_key=True)  # e.g., "ALT-KANHA-881"
    area_id = Column(String(64), ForeignKey("areas.id", ondelete="CASCADE"), nullable=False, index=True)
    area_name = Column(String(150), nullable=False)
    hotspot_id = Column(String(64), ForeignKey("hotspots.id", ondelete="SET NULL"), nullable=True, index=True)
    title = Column(String(255), nullable=False)
    message = Column(Text, nullable=False)
    severity = Column(String(20), nullable=False, index=True)
    status = Column(String(30), default="UNREAD", nullable=False, index=True)
    triggered_at = Column(DateTime(timezone=True), nullable=False, index=True)
    acknowledged_at = Column(DateTime(timezone=True), nullable=True)
    acknowledged_by = Column(String(36), ForeignKey("users.id", ondelete="SET NULL"), nullable=True)

    is_demonstration_data = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), server_default=func.now())

    # Relationships
    area = relationship("Area", back_populates="alerts")
    hotspot = relationship("Hotspot", back_populates="alerts")
    user = relationship("User")


# Pydantic Schemas kept for backward compatibility in mock layers
class AlertModel(BaseModel):
    id: str
    title: str
    message: str
    severity: str
    status: str
    triggered_at: str
    area_id: str
    area_name: str
    hotspot_id: Optional[str] = None
