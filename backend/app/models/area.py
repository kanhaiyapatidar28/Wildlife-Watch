from typing import Dict, Any, Optional, List
from pydantic import BaseModel, Field


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
    coordinates: Dict[str, float]  # lat, lon
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
