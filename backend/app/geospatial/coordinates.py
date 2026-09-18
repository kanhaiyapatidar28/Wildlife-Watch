import math
from typing import Tuple
from pydantic import BaseModel, Field


class BoundingBox(BaseModel):
    min_lon: float = Field(..., ge=-180.0, le=180.0)
    min_lat: float = Field(..., ge=-90.0, le=90.0)
    max_lon: float = Field(..., ge=-180.0, le=180.0)
    max_lat: float = Field(..., ge=-90.0, le=90.0)


def validate_lat_lon(lat: float, lon: float) -> bool:
    """Validates if latitude is between -90 and 90 and longitude between -180 and 180."""
    return -90.0 <= lat <= 90.0 and -180.0 <= lon <= 180.0


def calculate_haversine_distance(
    coord1: Tuple[float, float], coord2: Tuple[float, float]
) -> float:
    """
    Calculates great-circle distance between two points on the Earth (WGS84 sphere approximation).
    Returns distance in kilometers.
    """
    lat1, lon1 = coord1
    lat2, lon2 = coord2

    R = 6371.0  # Earth's radius in kilometers

    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)

    a = (
        math.sin(dlat / 2) ** 2
        + math.cos(math.radians(lat1))
        * math.cos(math.radians(lat2))
        * math.sin(dlon / 2) ** 2
    )
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return R * c
