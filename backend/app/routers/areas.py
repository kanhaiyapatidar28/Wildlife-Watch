from typing import List, Optional
from fastapi import APIRouter, HTTPException, Query, status
from app.schemas.area import (
    ProtectedAreaResponse,
    AreaStatisticsResponse,
    AreaTimelineResponse,
    TimelinePointResponse,
)
from app.schemas.hotspot import HotspotResponse
from app.schemas.common import StandardResponse, ResponseMeta
from app.services.area_service import AreaService

router = APIRouter(prefix="/areas", tags=["Protected Areas"])


@router.get("", response_model=StandardResponse[List[ProtectedAreaResponse]])
def list_protected_areas(
    country: Optional[str] = Query(None, description="Filter by country name or ISO alpha-2"),
    search: Optional[str] = Query(None, description="Search by reserve name, biome, or country"),
):
    """Retrieve list of monitored protected areas with global and Indian biodiversity reserves."""
    areas = AreaService.get_areas(country=country, search=search)
    return StandardResponse(
        data=areas,
        meta=ResponseMeta(total_count=len(areas)),
    )


@router.get("/{id}", response_model=StandardResponse[ProtectedAreaResponse])
def get_protected_area(id: str):
    """Retrieve full details for a protected area by UUID or WDPA ID."""
    area = AreaService.get_area_by_id(id)
    if not area:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Protected area with identifier '{id}' not found.",
        )
    return StandardResponse(data=area)


@router.get("/{id}/statistics", response_model=StandardResponse[AreaStatisticsResponse])
def get_area_statistics(id: str):
    """Retrieve current habitat integrity, land cover distribution, and canopy loss statistics."""
    stats = AreaService.get_area_statistics(id)
    if not stats:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Statistics for area '{id}' not found.",
        )
    return StandardResponse(data=stats)


@router.get("/{id}/timeline", response_model=StandardResponse[AreaTimelineResponse])
def get_area_timeline(id: str):
    """Retrieve multi-month phenological trend, NDVI trajectory, and fire incidents timeline."""
    area = AreaService.get_area_by_id(id)
    if not area:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Protected area '{id}' not found.",
        )
    timeline_points = AreaService.get_area_timeline(id) or []
    return StandardResponse(
        data=AreaTimelineResponse(
            area_id=area.id,
            area_name=area.name,
            points=[TimelinePointResponse(**p.model_dump()) for p in timeline_points],
        ),
        meta=ResponseMeta(total_count=len(timeline_points)),
    )


@router.get("/{id}/hotspots", response_model=StandardResponse[List[HotspotResponse]])
def get_area_hotspots(id: str):
    """Retrieve active habitat degradation hotspots localized to this protected area."""
    area = AreaService.get_area_by_id(id)
    if not area:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Protected area '{id}' not found.",
        )
    hotspots = AreaService.get_area_hotspots(id)
    return StandardResponse(
        data=hotspots,
        meta=ResponseMeta(total_count=len(hotspots)),
    )
