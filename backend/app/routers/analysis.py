from fastapi import APIRouter, HTTPException, status
from app.schemas.analysis import (
    SpectralIndexRequest,
    SpectralIndexResponse,
    ChangeDetectionRequest,
    ChangeDetectionResponse,
)
from app.schemas.common import StandardResponse
from app.services.analysis_service import AnalysisService
from app.services.area_service import AreaService

router = APIRouter(prefix="/analysis", tags=["Spectral & Change Analysis"])


@router.post("/ndvi", response_model=StandardResponse[SpectralIndexResponse])
def compute_ndvi(request: SpectralIndexRequest):
    """
    Compute Normalized Difference Vegetation Index (NDVI) statistics over an area or custom polygon.
    Formula: (NIR - Red) / (NIR + Red)
    """
    if request.area_id and not AreaService.get_area_by_id(request.area_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Protected area '{request.area_id}' not found.",
        )

    result = AnalysisService.calculate_index(
        index_type="ndvi",
        area_id=request.area_id,
        date=request.date,
        geometry=request.geometry,
    )
    return StandardResponse(data=result)


@router.post("/ndwi", response_model=StandardResponse[SpectralIndexResponse])
def compute_ndwi(request: SpectralIndexRequest):
    """
    Compute Normalized Difference Water Index (NDWI) statistics for surface water and wetland moisture.
    Formula: (Green - NIR) / (Green + NIR)
    """
    if request.area_id and not AreaService.get_area_by_id(request.area_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Protected area '{request.area_id}' not found.",
        )

    result = AnalysisService.calculate_index(
        index_type="ndwi",
        area_id=request.area_id,
        date=request.date,
        geometry=request.geometry,
    )
    return StandardResponse(data=result)


@router.post("/ndbi", response_model=StandardResponse[SpectralIndexResponse])
def compute_ndbi(request: SpectralIndexRequest):
    """
    Compute Normalized Difference Built-Up Index (NDBI) for infrastructure and road encroachment.
    Formula: (SWIR - NIR) / (SWIR + NIR)
    """
    if request.area_id and not AreaService.get_area_by_id(request.area_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Protected area '{request.area_id}' not found.",
        )

    result = AnalysisService.calculate_index(
        index_type="ndbi",
        area_id=request.area_id,
        date=request.date,
        geometry=request.geometry,
    )
    return StandardResponse(data=result)


@router.post("/change-detection", response_model=StandardResponse[ChangeDetectionResponse])
def run_change_detection_analysis(request: ChangeDetectionRequest):
    """
    Execute bi-temporal change detection analysis between baseline and target observation epochs.
    Returns affected area, loss/gain hectares, net change, NDVI distributions, and severity bins.
    """
    area = AreaService.get_area_by_id(request.area_id)
    if not area:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Protected area '{request.area_id}' not found.",
        )

    result = AnalysisService.run_change_detection(
        area_id=area.id,
        start_date=request.start_date,
        end_date=request.end_date,
        analysis_type=request.analysis_type,
    )
    return StandardResponse(data=result)
