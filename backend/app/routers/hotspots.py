from typing import List, Optional
from fastapi import APIRouter, HTTPException, Query, status
from app.schemas.hotspot import HotspotResponse
from app.schemas.common import StandardResponse, ResponseMeta
from app.services.hotspot_service import HotspotService

router = APIRouter(prefix="/hotspots", tags=["Hotspots & Change Detection"])


@router.get("", response_model=StandardResponse[List[HotspotResponse]])
def list_hotspots(
    change_type: Optional[str] = Query(None, description="Filter by change type: VEGETATION_LOSS, WATER_LOSS, URBAN_EXPANSION, FIRE, OTHER"),
    severity: Optional[str] = Query(None, description="Filter by severity: CRITICAL, HIGH, MEDIUM, LOW"),
    area_id: Optional[str] = Query(None, description="Filter by protected area ID"),
    min_confidence: Optional[float] = Query(None, description="Minimum confidence score threshold (e.g. 70 or 0.70)"),
    search: Optional[str] = Query(None, description="Search across ID, area name, location detail"),
):
    """Retrieve filtered list of vectorized habitat change hotspots ranked by severity and confidence."""
    hotspots = HotspotService.get_hotspots(
        change_type=change_type,
        severity=severity,
        area_id=area_id,
        min_confidence=min_confidence,
        search=search,
    )
    return StandardResponse(
        data=hotspots,
        meta=ResponseMeta(total_count=len(hotspots)),
    )


@router.get("/{id}", response_model=StandardResponse[HotspotResponse])
def get_hotspot_detail(id: str):
    """Retrieve full inspection dossier for a specific degradation hotspot."""
    hotspot = HotspotService.get_hotspot_by_id(id)
    if not hotspot:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Hotspot with identifier '{id}' not found.",
        )
    return StandardResponse(data=hotspot)
