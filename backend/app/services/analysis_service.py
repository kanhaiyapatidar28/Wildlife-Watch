from typing import Dict, Any, Optional
from datetime import datetime, timezone
from app.database import db
from app.models.analysis import SpectralIndexResultModel, ChangeDetectionResultModel
from app.analysis.change_detector import compute_change_detection
from app.geospatial.geometry import calculate_polygon_area_ha
from app.satellite.mock_scenes import generate_spectral_surface_reflectance


class AnalysisService:
    @staticmethod
    def calculate_index(
        index_type: str,
        area_id: Optional[str] = None,
        date: Optional[str] = None,
        geometry: Optional[Dict[str, Any]] = None,
    ) -> SpectralIndexResultModel:
        biome = "Central Deccan Moist Deciduous & Sal Woodlands"
        area_ha = 100.0

        if area_id and area_id in db.areas:
            area = db.areas[area_id]
            biome = area.biome
            area_ha = area.total_hectares
        elif geometry:
            area_ha = calculate_polygon_area_ha(geometry)

        stats = generate_spectral_surface_reflectance(biome, index_type)

        return SpectralIndexResultModel(
            index_name=index_type.upper(),
            area_id=area_id,
            mean=stats["mean"],
            median=stats["median"],
            min=stats["min"],
            max=stats["max"],
            std=stats["std"],
            surface_area_ha=area_ha,
            cloud_cover_percent=1.4,
            sensor="Sentinel-2 MSI Level-2A BOA",
            computed_at=datetime.now(timezone.utc).isoformat(),
        )

    @staticmethod
    def run_change_detection(
        area_id: str,
        start_date: str,
        end_date: str,
        analysis_type: str = "vegetation_ndvi",
    ) -> ChangeDetectionResultModel:
        area_name = "Monitored Protected Area"
        total_ha = 94000.0

        if area_id in db.areas:
            area = db.areas[area_id]
            area_name = area.name
            total_ha = area.total_hectares

        raw_result = compute_change_detection(
            area_id=area_id,
            area_name=area_name,
            start_date=start_date,
            end_date=end_date,
            analysis_type=analysis_type,
            total_area_ha=total_ha,
        )

        return ChangeDetectionResultModel(
            analysis_type=raw_result["analysis_type"],
            area_id=raw_result["area_id"],
            area_name=raw_result["area_name"],
            start_date=raw_result["start_date"],
            end_date=raw_result["end_date"],
            area_affected_ha=raw_result["area_affected_ha"],
            vegetation_loss_ha=raw_result["vegetation_loss_ha"],
            vegetation_gain_ha=raw_result["vegetation_gain_ha"],
            net_change_ha=raw_result["net_change_ha"],
            percentage_change=raw_result["percentage_change"],
            confidence_score=raw_result["confidence_score"],
            baseline_index_mean=raw_result["baseline_index_mean"],
            current_index_mean=raw_result["current_index_mean"],
            ndvi_distribution=raw_result["ndvi_distribution"],
            change_distribution=raw_result["change_distribution"],
            methodology_summary=raw_result["methodology_summary"],
            computed_at=datetime.now(timezone.utc).isoformat(),
        )
