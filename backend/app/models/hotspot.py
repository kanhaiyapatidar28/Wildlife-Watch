"""Hotspot entity SQLAlchemy model with PostGIS Point and Polygon geometries."""
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional
from sqlalchemy import Column, String, Float, Boolean, DateTime, ForeignKey, JSON, func
from sqlalchemy.orm import relationship
from geoalchemy2 import Geometry
from pydantic import BaseModel

from app.db.base import Base


class Hotspot(Base):
    __tablename__ = "hotspots"

    id = Column(String(64), primary_key=True)  # e.g., "HS-KANHA-01"
    area_id = Column(String(64), ForeignKey("areas.id", ondelete="CASCADE"), nullable=False, index=True)
    area_name = Column(String(150), nullable=False)
    location_detail = Column(String(255), nullable=False)
    change_type = Column(String(50), nullable=False, index=True)
    severity = Column(String(20), nullable=False, index=True)
    confidence_score = Column(Float, nullable=False)
    detected_at = Column(DateTime(timezone=True), nullable=False, index=True)
    area_ha = Column(Float, nullable=False)
    delta_ndvi = Column(Float, nullable=False)
    percentage_change = Column(Float, nullable=False)
    status = Column(String(30), default="NEW", nullable=False)
    sensor = Column(String(100), default="Sentinel-2 MSI (10m)", nullable=False)
    previous_condition = Column(String(255), nullable=False)
    current_condition = Column(String(255), nullable=False)
    potential_contributing_factors = Column(JSON, nullable=False)

    # PostGIS Geometries (WGS84 SRID 4326)
    centroid_geometry = Column(
        Geometry(geometry_type="POINT", srid=4326, spatial_index=True),
        nullable=False,
    )
    boundary_geometry = Column(
        Geometry(geometry_type="POLYGON", srid=4326, spatial_index=True),
        nullable=True,
    )

    is_demonstration_data = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), server_default=func.now())

    # Relationships
    area = relationship("Area", back_populates="hotspots")
    change_events = relationship("ChangeEvent", back_populates="hotspot")
    alerts = relationship("Alert", back_populates="hotspot")


# Pydantic Schemas kept for backward compatibility in mock layers
class HotspotRelatedAlert(BaseModel):
    id: str
    title: str
    severity: str
    timestamp: str


class HotspotModel(BaseModel):
    id: str
    area_id: str
    area_name: str
    location_detail: str
    detected_at: str
    area_ha: float
    delta_ndvi: float
    percentage_change: float
    change_type: str
    severity: str
    confidence_score: float
    coordinates: Dict[str, float]
    status: str
    sensor: str
    previous_condition: str
    current_condition: str
    potential_contributing_factors: List[str]
    related_alerts: List[HotspotRelatedAlert] = []
