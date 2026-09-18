import pytest
from app.geospatial.coordinates import validate_lat_lon, calculate_haversine_distance
from app.geospatial.geometry import calculate_polygon_area_ha
from app.satellite.indices import calculate_ndvi, calculate_ndwi, calculate_ndbi


def test_coordinate_validation():
    assert validate_lat_lon(22.33, 80.61) is True
    assert validate_lat_lon(-0.08, 29.49) is True
    assert validate_lat_lon(95.0, 80.0) is False
    assert validate_lat_lon(22.0, 190.0) is False


def test_haversine_distance():
    # Distance between Kanha (22.33, 80.61) and Bandhavgarh (23.72, 81.02) is ~160 km
    dist = calculate_haversine_distance((22.33, 80.61), (23.72, 81.02))
    assert 140.0 < dist < 180.0


def test_polygon_area_ha():
    # Simple 1-degree square around equator has substantial area (> 1,000,000 ha)
    geometry = {
        "type": "Polygon",
        "coordinates": [
            [
                [0.0, 0.0],
                [1.0, 0.0],
                [1.0, 1.0],
                [0.0, 1.0],
                [0.0, 0.0],
            ]
        ],
    }
    area = calculate_polygon_area_ha(geometry)
    assert area > 1000000.0


def test_spectral_indices_formulas():
    # NDVI: (0.8 - 0.2) / (0.8 + 0.2) = 0.6 / 1.0 = 0.6
    assert calculate_ndvi(0.8, 0.2) == 0.6000

    # NDWI: (0.5 - 0.2) / (0.5 + 0.2) = 0.3 / 0.7 = 0.4286
    assert calculate_ndwi(0.5, 0.2) == 0.4286

    # NDBI: (0.6 - 0.4) / (0.6 + 0.4) = 0.2 / 1.0 = 0.2
    assert calculate_ndbi(0.6, 0.4) == 0.2000

    # Zero denominator edge case
    assert calculate_ndvi(0.0, 0.0) == 0.0
    assert calculate_ndwi(0.0, 0.0) == 0.0
    assert calculate_ndbi(0.0, 0.0) == 0.0
