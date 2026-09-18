from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field


# Request Schemas
class SpectralIndexRequest(BaseModel):
    area_id: Optional[str] = None
    date: Optional[str] = None
    satellite: Optional[str] = "sentinel-2"
    geometry: Optional[Dict[str, Any]] = None  # Optional GeoJSON Polygon


class ChangeDetectionRequest(BaseModel):
    area_id: str
    start_date: str = Field(..., description="Baseline epoch start date (YYYY-MM-DD)")
    end_date: str = Field(..., description="Target epoch end date (YYYY-MM-DD)")
    analysis_type: str = Field(
        default="vegetation_ndvi",
        description="Type of analysis: vegetation_ndvi, water_ndwi, builtup_ndbi, land_cover, fire_activity",
    )


# Response Schemas
class SpectralIndexResponse(BaseModel):
    index_name: str
    area_id: Optional[str] = None
    mean: float
    median: float
    min: float
    max: float
    std: float
    surface_area_ha: float
    cloud_cover_percent: float
    sensor: str
    computed_at: str


class NdviDistributionBin(BaseModel):
    ndvi: str
    baseline: int
    current: int


class ChangeDistributionBin(BaseModel):
    interval: str
    label: str
    areaHa: float
    color: str
    desc: str


class ChangeDetectionResponse(BaseModel):
    analysis_type: str
    area_id: str
    area_name: str
    start_date: str
    end_date: str
    area_affected_ha: float
    vegetation_loss_ha: float
    vegetation_gain_ha: float
    net_change_ha: float
    percentage_change: float
    confidence_score: float
    baseline_index_mean: float
    current_index_mean: float
    ndvi_distribution: List[NdviDistributionBin]
    change_distribution: List[ChangeDistributionBin]
    methodology_summary: Dict[str, str]
    computed_at: str
