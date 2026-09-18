"""Satellite and Land Cover observation SQLAlchemy models."""
import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Float, Boolean, DateTime, ForeignKey, JSON, func
from sqlalchemy.orm import relationship

from app.db.base import Base


class SatelliteObservation(Base):
    __tablename__ = "satellite_observations"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    area_id = Column(String(64), ForeignKey("areas.id", ondelete="CASCADE"), nullable=False, index=True)
    satellite = Column(String(50), nullable=False, default="Sentinel-2 MSI")
    scene_id = Column(String(100), nullable=False)
    acquisition_date = Column(DateTime(timezone=True), nullable=False)
    cloud_cover_percent = Column(Float, default=0.0)
    mean_ndvi = Column(Float, nullable=False)
    mean_ndwi = Column(Float, nullable=False)
    mean_ndbi = Column(Float, nullable=False)
    tile_url = Column(String(255), nullable=True)
    metadata_json = Column(JSON, nullable=True)
    is_demonstration_data = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), server_default=func.now())

    # Relationship
    area = relationship("Area", back_populates="satellite_observations")


class LandCoverObservation(Base):
    __tablename__ = "land_cover_observations"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    area_id = Column(String(64), ForeignKey("areas.id", ondelete="CASCADE"), nullable=False, index=True)
    observation_date = Column(DateTime(timezone=True), nullable=False)
    dense_forest_ha = Column(Float, nullable=False)
    open_forest_ha = Column(Float, nullable=False)
    wetlands_water_ha = Column(Float, nullable=False)
    grassland_savanna_ha = Column(Float, nullable=False)
    agricultural_ha = Column(Float, nullable=False)
    urban_settlement_ha = Column(Float, nullable=False)
    distribution_json = Column(JSON, nullable=False)
    is_demonstration_data = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), server_default=func.now())

    # Relationship
    area = relationship("Area", back_populates="land_cover_observations")
