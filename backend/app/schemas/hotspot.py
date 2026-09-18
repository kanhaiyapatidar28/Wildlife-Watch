from typing import Dict, Optional, List
from pydantic import BaseModel, Field
from .area import CoordinatesSchema


class HotspotRelatedAlertSchema(BaseModel):
    id: str
    title: str
    severity: str
    timestamp: str


class HotspotResponse(BaseModel):
    id: str
    area_id: str
    area_name: str
    location_detail: Optional[str] = None
    detected_at: str
    area_ha: float
    delta_ndvi: float
    percentage_change: Optional[float] = None
    change_type: str
    severity: str
    confidence_score: float
    coordinates: CoordinatesSchema
    status: str
    sensor: str
    previous_condition: Optional[str] = None
    current_condition: Optional[str] = None
    potential_contributing_factors: List[str] = Field(default_factory=list)
    related_alerts: List[HotspotRelatedAlertSchema] = Field(default_factory=list)
