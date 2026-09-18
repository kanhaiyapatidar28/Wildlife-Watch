"""Wildlife species entity SQLAlchemy model."""
import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship

from app.db.base import Base


class WildlifeSpecies(Base):
    __tablename__ = "wildlife_species"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    area_id = Column(String(64), ForeignKey("areas.id", ondelete="CASCADE"), nullable=False, index=True)
    common_name = Column(String(150), nullable=False, index=True)
    scientific_name = Column(String(150), nullable=False)
    iucn_status = Column(String(50), nullable=False, index=True)  # CRITICALLY_ENDANGERED, ENDANGERED, VULNERABLE, NEAR_THREATENED, LEAST_CONCERN
    estimated_population_range = Column(String(100), nullable=False)  # Clearly stated as survey estimate range
    habitat_preference = Column(String(255), nullable=False)
    monitoring_priority = Column(String(20), default="HIGH", nullable=False)  # CRITICAL, HIGH, MEDIUM, ROUTINE

    is_demonstration_data = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), server_default=func.now())

    # Relationship
    area = relationship("Area", back_populates="wildlife_species")
