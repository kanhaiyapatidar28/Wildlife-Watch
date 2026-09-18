from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field


class SpectralIndexResultModel(BaseModel):
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


class ChangeDetectionResultModel(BaseModel):
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
    ndvi_distribution: List[Dict[str, Any]]
    change_distribution: List[Dict[str, Any]]
    methodology_summary: Dict[str, str]
    computed_at: str


class AnalysisJobModel(BaseModel):
    job_id: str
    status: str       # QUEUED, PROCESSING, COMPLETED, FAILED
    analysis_type: str
    created_at: str
    completed_at: Optional[str] = None
    result: Optional[ChangeDetectionResultModel] = None
