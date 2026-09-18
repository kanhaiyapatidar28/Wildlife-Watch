from typing import List, Optional
from fastapi import APIRouter, Query
from app.schemas.alert import AlertResponse
from app.schemas.common import StandardResponse, ResponseMeta
from app.services.alert_service import AlertService

router = APIRouter(prefix="/alerts", tags=["Incident Alerts"])


@router.get("", response_model=StandardResponse[List[AlertResponse]])
def list_incident_alerts(
    severity: Optional[str] = Query(None, description="Filter by severity: CRITICAL, HIGH, MEDIUM, LOW"),
    status: Optional[str] = Query(None, description="Filter by status: UNREAD, ACKNOWLEDGED, DISMISSED"),
    area_id: Optional[str] = Query(None, description="Filter by protected area ID"),
):
    """Retrieve real-time incident notifications and ranger alerts."""
    alerts = AlertService.get_alerts(severity=severity, status=status, area_id=area_id)
    return StandardResponse(
        data=alerts,
        meta=ResponseMeta(total_count=len(alerts)),
    )
