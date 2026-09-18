from typing import List, Optional
from fastapi import APIRouter, Query
from app.schemas.report import ReportResponse
from app.schemas.common import StandardResponse, ResponseMeta
from app.services.report_service import ReportService

router = APIRouter(prefix="/reports", tags=["Reports & Export Registry"])


@router.get("", response_model=StandardResponse[List[ReportResponse]])
def list_generated_reports(
    area_id: Optional[str] = Query(None, description="Filter by protected area ID"),
    status: Optional[str] = Query(None, description="Filter by status: READY, GENERATING, FAILED"),
):
    """Retrieve catalog of generated habitat integrity audit reports and geospatial dossiers."""
    reports = ReportService.get_reports(area_id=area_id, status=status)
    return StandardResponse(
        data=reports,
        meta=ResponseMeta(total_count=len(reports)),
    )
