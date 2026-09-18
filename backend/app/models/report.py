from typing import Optional
from pydantic import BaseModel


class ReportModel(BaseModel):
    id: str
    title: str
    format: str       # GEOPDF, CSV, GEOPACKAGE
    date_range: str
    area_id: str
    area_name: str
    file_size_mb: float
    status: str       # READY, GENERATING, FAILED
    generated_at: str
    download_url: Optional[str] = None
