"""ChangeEvent entity SQLAlchemy model with PostGIS geometry."""
import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Float, Boolean, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from geoalchemy2 import Geometry

from app.db.base import Base


class ChangeEvent(Base):
    __tablename__ = "change_events"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    area_id = Column(String(64), ForeignKey("areas.id", ondelete="CASCADE"), nullable=False, index=True)
    hotspot_id = Column(String(64), ForeignKey("hotspots.id", ondelete="SET NULL"), nullable=True, index=True)

    # PostGIS Geographic Geometry (Polygon, MultiPolygon, or GeometryCollection in SRID 4326)
    geometry = Column(
        Geometry(geometry_type="GEOMETRY", srid=4326, spatial_index=True),
        nullable=False,
    )

    # Required attributes from specification
    change_type = Column(String(50), nullable=False, index=True)  # VEGETATION_LOSS, WATER_LOSS, URBAN_EXPANSION, FIRE, OTHER
    severity = Column(String(20), nullable=False, index=True)      # CRITICAL, HIGH, MEDIUM, LOW
    confidence = Column(Float, nullable=False)                     # 0.0 to 1.0 (e.g. 0.94)
    detected_at = Column(DateTime(timezone=True), nullable=False, index=True)

    # Metrics
    affected_ha = Column(Float, nullable=False, default=0.0)
    delta_ndvi = Column(Float, nullable=True)
    baseline_period = Column(String(50), nullable=True)
    target_period = Column(String(50), nullable=True)
    is_demonstration_data = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), server_default=func.now())

    # Relationships
    area = relationship("Area", back_populates="change_events")
    hotspot = relationship("Hotspot", back_populates="change_events")
