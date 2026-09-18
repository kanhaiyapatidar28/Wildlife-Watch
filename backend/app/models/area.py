"""Area entity SQLAlchemy model with PostGIS MultiPolygon geometry."""
from datetime import datetime, timezone
from typing import Dict, Any, Optional, List
from sqlalchemy import Column, String, Float, Integer, Boolean, DateTime, func, Text
from sqlalchemy.orm import relationship
from geoalchemy2 import Geometry
from pydantic import BaseModel

from app.db.base import Base


class Area(Base):
    __tablename__ = "areas"

    id = Column(String(64), primary_key=True)  # e.g., "area-kanha"
    wdpa_id = Column(String(32), index=True, nullable=False)
    name = Column(String(150), index=True, nullable=False)
    designation = Column(String(100), nullable=False)
    protected_area_type = Column(String(100), nullable=False)
    iucn_category = Column(String(50), nullable=False)
    country = Column(String(100), index=True, nullable=False)
    country_code = Column(String(10), index=True, nullable=False)
    state = Column(String(100), nullable=True)
    area_km2 = Column(Float, nullable=False)
    total_hectares = Column(Float, nullable=False)
    center_lat = Column(Float, nullable=False)
    center_lon = Column(Float, nullable=False)
    forest_cover_percent = Column(Float, default=0.0)
    canopy_loss_year_ha = Column(Float, default=0.0)
    active_fires_count = Column(Integer, default=0)
    threat_index = Column(Integer, default=0)
    biome = Column(String(150), nullable=False)
    last_analyzed = Column(String(50), nullable=False)

    # PostGIS Geographic Geometry (MultiPolygon, WGS84 SRID 4326)
    geometry = Column(
        Geometry(geometry_type="MULTIPOLYGON", srid=4326, spatial_index=True),
        nullable=True,
    )

    # Demonstration metadata flag
    is_demonstration_data = Column(Boolean, default=True, nullable=False)
    notes = Column(Text, default="Demonstration telemetry for spatial modeling; requires ground-truth verification.")

    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    # Relationships
    satellite_observations = relationship("SatelliteObservation", back_populates="area", cascade="all, delete-orphan")
    land_cover_observations = relationship("LandCoverObservation", back_populates="area", cascade="all, delete-orphan")
    change_events = relationship("ChangeEvent", back_populates="area", cascade="all, delete-orphan")
    hotspots = relationship("Hotspot", back_populates="area", cascade="all, delete-orphan")
    alerts = relationship("Alert", back_populates="area", cascade="all, delete-orphan")
    wildlife_species = relationship("WildlifeSpecies", back_populates="area", cascade="all, delete-orphan")
    saved_areas = relationship("SavedArea", back_populates="area", cascade="all, delete-orphan")
    reports = relationship("Report", back_populates="area")


# Pydantic Schemas kept for backward compatibility in mock layers
class ProtectedAreaModel(BaseModel):
    id: str
    wdpa_id: str
    name: str
    designation: str
    protected_area_type: str
    iucn_category: str
    country: str
    country_code: str
    state: Optional[str] = None
    area_km2: float
    total_hectares: float
    coordinates: Dict[str, float]
    forest_cover_percent: float
    canopy_loss_year_ha: float
    active_fires_count: int
    threat_index: int
    biome: str
    last_analyzed: str


class AreaStatisticsModel(BaseModel):
    area_id: str
    area_name: str
    forest_cover_percent: float
    canopy_loss_year_ha: float
    water_bodies_ha: float
    urban_builtup_ha: float
    habitat_change_score: float
    active_fires_count: int
    threat_index: int
    last_cloud_free_pass: str
    land_cover_distribution: Dict[str, float]
    sensor_telemetry: Dict[str, Any]


class AreaTimelineModel(BaseModel):
    date: str
    ndvi: float
    baseline: float
    water_cover_ha: float
    fire_incidents: int
    canopy_loss_ha: float
