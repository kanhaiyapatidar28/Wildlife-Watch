from typing import Dict, Optional, List
from pydantic import BaseModel, Field


class HotspotRelatedAlert(BaseModel):
    id: str
    title: str
    severity: str
    timestamp: str


class HotspotModel(BaseModel):
    id: str
    area_id: str
    area_name: str
    location_detail: Optional[str] = None
    detected_at: str
    area_ha: float
    delta_ndvi: float
    percentage_change: Optional[float] = None
    change_type: str  # VEGETATION_LOSS, WATER_LOSS, URBAN_EXPANSION, FIRE, OTHER
    severity: str     # CRITICAL, HIGH, MEDIUM, LOW
    confidence_score: float  # 0.0 - 1.0
    coordinates: Dict[str, float]  # lat, lon
    status: str       # NEW, VERIFIED, FALSE_POSITIVE, RESOLVED
    sensor: str
    previous_condition: Optional[str] = None
    current_condition: Optional[str] = None
    potential_contributing_factors: List[str] = Field(default_factory=list)
    related_alerts: List[HotspotRelatedAlert] = Field(default_factory=list)
