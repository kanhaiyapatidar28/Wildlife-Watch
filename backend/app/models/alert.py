from typing import Optional
from pydantic import BaseModel


class AlertModel(BaseModel):
    id: str
    title: str
    message: str
    severity: str     # CRITICAL, HIGH, MEDIUM, LOW, INFO
    status: str       # UNREAD, ACKNOWLEDGED, DISMISSED
    triggered_at: str
    area_id: str
    area_name: str
    hotspot_id: Optional[str] = None
