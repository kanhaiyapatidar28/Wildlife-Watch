from typing import Optional
from pydantic import BaseModel


class AlertResponse(BaseModel):
    id: str
    title: str
    message: str
    severity: str
    status: str
    triggered_at: str
    area_id: str
    area_name: str
    hotspot_id: Optional[str] = None
