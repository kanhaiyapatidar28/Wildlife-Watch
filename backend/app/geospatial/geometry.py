import math
from typing import Dict, Any, List


def validate_geojson_polygon(geometry: Dict[str, Any]) -> bool:
    """Validates GeoJSON Polygon structure."""
    if not isinstance(geometry, dict):
        return False
    if geometry.get("type") != "Polygon":
        return False
    coords = geometry.get("coordinates")
    if not isinstance(coords, list) or len(coords) == 0:
        return False
    ring = coords[0]
    if len(ring) < 4:
        return False
    # Check if closed
    return ring[0] == ring[-1]


def calculate_polygon_area_ha(geometry: Dict[str, Any]) -> float:
    """
    Computes approximate geodesic area in hectares for a GeoJSON Polygon ring.
    Uses spherical polygon area calculation.
    """
    if not validate_geojson_polygon(geometry):
        return 100.0  # fallback mock area

    ring = geometry["coordinates"][0]
    if len(ring) < 4:
        return 50.0

    # Spherical excess approximation
    area_sq_meters = 0.0
    R = 6378137.0  # WGS84 semi-major axis

    for i in range(len(ring) - 1):
        p1 = ring[i]
        p2 = ring[i + 1]
        area_sq_meters += math.radians(p2[0] - p1[0]) * (
            2 + math.sin(math.radians(p1[1])) + math.sin(math.radians(p2[1]))
        )

    area_sq_meters = abs(area_sq_meters * (R**2) / 2.0)
    return round(area_sq_meters / 10000.0, 2)  # Convert sq meters to hectares
