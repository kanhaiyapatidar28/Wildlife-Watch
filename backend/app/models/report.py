"""Report catalog entity SQLAlchemy model."""
from datetime import datetime, timezone
from typing import Optional
from sqlalchemy import Column, String, Integer, Boolean, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from pydantic import BaseModel

from app.db.base import Base


class Report(Base):
    __tablename__ = "reports"

    id = Column(String(64), primary_key=True)  # e.g., "REP-2026-09-01"
    area_id = Column(String(64), ForeignKey("areas.id", ondelete="SET NULL"), nullable=True, index=True)
    area_name = Column(String(150), nullable=False)
    title = Column(String(255), nullable=False)
    report_type = Column(String(50), default="HABITAT_AUDIT", nullable=False)  # HABITAT_AUDIT, CHANGE_DOSSIER, INCIDENT_EXPORT
    format = Column(String(20), default="GEOPDF", nullable=False)              # GEOPDF, GEOPACKAGE, CSV
    date_range = Column(String(50), nullable=False)
    status = Column(String(20), default="READY", nullable=False, index=True)  # READY, GENERATING, FAILED
    file_size_bytes = Column(Integer, default=0, nullable=False)
    download_url = Column(String(255), nullable=False)
    generated_by = Column(String(36), ForeignKey("users.id", ondelete="SET NULL"), nullable=True)

    is_demonstration_data = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), server_default=func.now())

    # Relationships
    area = relationship("Area", back_populates="reports")
    user = relationship("User", back_populates="reports")


# Pydantic Schemas kept for backward compatibility in mock layers
class ReportModel(BaseModel):
    id: str
    title: str
    area_name: str
    format: str
    date_range: str
    status: str
    download_url: str
    area_id: Optional[str] = "ALL"
    file_size_mb: float = 14.5
    generated_at: str = "2026-09-17T12:00:00Z"
