from typing import List, Dict, Any
from datetime import datetime


def get_mock_scenes(area_id: str, count: int = 5) -> List[Dict[str, Any]]:
    """Returns candidate Sentinel-2 scenes for an area."""
    return [
        {
            "scene_id": f"S2A_MSIL2A_2026091{i}_N0511_R062_T44QME",
            "acquisition_date": f"2026-09-1{i}T05:22:19Z",
            "cloud_cover_percent": 1.2 + (i * 0.8),
            "satellite": "Sentinel-2A",
            "sensor": "MSI Level-2A BOA",
            "sun_zenith_angle": 28.4,
            "tile_id": "T44QME",
        }
        for i in range(1, count + 1)
    ]


def generate_spectral_surface_reflectance(biome: str, index_type: str = "ndvi") -> Dict[str, float]:
    """Generates synthetic multi-spectral surface reflectance statistics."""
    if "Rainforest" in biome or "Sal" in biome or "Moist" in biome:
        base_ndvi = 0.76
        base_ndwi = -0.28
        base_ndbi = -0.32
    elif "Savanna" in biome or "Grassland" in biome:
        base_ndvi = 0.62
        base_ndwi = -0.42
        base_ndbi = -0.18
    elif "Wetland" in biome or "Floodplain" in biome:
        base_ndvi = 0.68
        base_ndwi = 0.45
        base_ndbi = -0.35
    else:
        base_ndvi = 0.70
        base_ndwi = -0.30
        base_ndbi = -0.25

    if index_type == "ndwi":
        mean_val = base_ndwi
    elif index_type == "ndbi":
        mean_val = base_ndbi
    else:
        mean_val = base_ndvi

    return {
        "mean": round(mean_val, 3),
        "median": round(mean_val + 0.02, 3),
        "min": round(mean_val - 0.45, 3),
        "max": round(min(1.0, mean_val + 0.22), 3),
        "std": 0.082,
    }
