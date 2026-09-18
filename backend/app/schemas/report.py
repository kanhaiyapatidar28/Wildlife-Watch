from typing import Optional
from pydantic import BaseModel


class ReportResponse(BaseModel):
    id: str
    title: str
    format: str
    date_range: str
    area_id: str
    area_name: str
    file_size_mb: float
    status: str
    generated_at: str
    download_url: Optional[str] = None
