"""Mathematical spectral index calculations for Sentinel-2 / Landsat surface reflectance."""

from typing import Dict, Any


def calculate_ndvi(nir: float, red: float) -> float:
    """
    Normalized Difference Vegetation Index (NDVI)
    Formula: (NIR - Red) / (NIR + Red)
    Bands: Sentinel-2 B8 (842nm) and B4 (665nm)
    """
    denominator = nir + red
    if denominator == 0.0:
        return 0.0
    return round((nir - red) / denominator, 4)


def calculate_ndwi(green: float, nir: float) -> float:
    """
    Normalized Difference Water Index (NDWI - McFeeters)
    Formula: (Green - NIR) / (Green + NIR)
    Bands: Sentinel-2 B3 (560nm) and B8 (842nm)
    """
    denominator = green + nir
    if denominator == 0.0:
        return 0.0
    return round((green - nir) / denominator, 4)


def calculate_ndbi(swir: float, nir: float) -> float:
    """
    Normalized Difference Built-Up Index (NDBI)
    Formula: (SWIR - NIR) / (SWIR + NIR)
    Bands: Sentinel-2 B11 (1610nm) and B8 (842nm)
    """
    denominator = swir + nir
    if denominator == 0.0:
        return 0.0
    return round((swir - nir) / denominator, 4)
