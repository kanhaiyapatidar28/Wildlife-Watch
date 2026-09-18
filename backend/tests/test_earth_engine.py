"""
Unit and Integration Tests for Google Earth Engine (GEE) Integration.

Validates:
- Module loading and graceful fallback when unauthenticated
- Secure credential initialization
- In-memory thread-safe TTL caching
- Geometry parsing and validation (GeoJSON, Bounding Box, Coordinate rings)
- Date range and parameter validation
- Spectral index algorithms (NDVI, NDWI, NDBI)
- Cloud masking (QA60 & SCL)
- Composite reduction and MapID generation
- Bi-temporal change detection and area classification
- Exception hierarchy
"""

import pytest
import time
from unittest.mock import MagicMock, patch

from app.satellite.earth_engine import (
    initialize_earth_engine,
    is_earth_engine_initialized,
    get_initialization_error,
    get_sentinel_images,
    mask_clouds,
    calculate_ndvi,
    calculate_ndwi,
    calculate_ndbi,
    calculate_composite,
    calculate_change,
    parse_ee_geometry,
    EarthEngineCache,
    EarthEngineError,
    EarthEngineNotInitializedError,
    EarthEngineAuthError,
    EarthEngineQueryError,
    EarthEngineExecutionError,
    _ee_cache,
)


# =====================================================================
# 1. Initialization and Auth Tests
# =====================================================================

def test_earth_engine_not_initialized_by_default():
    """Verify default state is uninitialized if no GCP credentials were provided."""
    # When initialized without credentials or project in test env, returns False
    with patch("app.satellite.earth_engine.HAS_EE", False):
        res = initialize_earth_engine(force_reinit=True)
        assert res is False
        assert is_earth_engine_initialized() is False
        assert "not installed" in get_initialization_error()


def test_require_initialized_guard_raises_custom_error():
    """Verify functions raise EarthEngineNotInitializedError when invoked uninitialized."""
    with patch("app.satellite.earth_engine._is_initialized", False):
        with patch("app.satellite.earth_engine.initialize_earth_engine", return_value=False):
            with pytest.raises(EarthEngineNotInitializedError) as exc_info:
                get_sentinel_images([78.0, 22.0, 79.0, 23.0], "2026-01-01", "2026-02-01")
            assert "Google Earth Engine is not initialized" in str(exc_info.value)


def test_exception_hierarchy():
    """Verify custom exception inheritance from EarthEngineError."""
    assert issubclass(EarthEngineNotInitializedError, EarthEngineError)
    assert issubclass(EarthEngineAuthError, EarthEngineError)
    assert issubclass(EarthEngineQueryError, EarthEngineError)
    assert issubclass(EarthEngineExecutionError, EarthEngineError)


# =====================================================================
# 2. TTL Cache Tests
# =====================================================================

def test_earth_engine_cache_operations():
    """Verify cache store, retrieve, key generation, and clearing."""
    cache = EarthEngineCache(default_ttl_seconds=10, max_entries=5)

    key1 = cache._make_key("test", area="kanha", index="ndvi")
    key2 = cache._make_key("test", area="kanha", index="ndvi")
    key3 = cache._make_key("test", area="kaziranga", index="ndvi")

    # Deterministic keys
    assert key1 == key2
    assert key1 != key3

    # Miss
    assert cache.get(key1) is None

    # Set and Hit
    sample_data = {"mean_ndvi": 0.65, "status": "OK"}
    cache.set(key1, sample_data)
    assert cache.get(key1) == sample_data
    assert cache.size() == 1

    # Clear
    cache.clear()
    assert cache.size() == 0
    assert cache.get(key1) is None


def test_earth_engine_cache_ttl_expiration():
    """Verify cache entries expire after TTL elapsed."""
    cache = EarthEngineCache(default_ttl_seconds=1, max_entries=10)
    key = cache._make_key("ttl_test", id=1)
    cache.set(key, "fresh_data")
    assert cache.get(key) == "fresh_data"

    # Simulate time lapse
    time.sleep(1.05)
    assert cache.get(key) is None


def test_earth_engine_cache_capacity_eviction():
    """Verify oldest entries are evicted when max capacity is reached."""
    cache = EarthEngineCache(default_ttl_seconds=60, max_entries=3)
    for i in range(3):
        cache.set(f"key_{i}", f"value_{i}")

    assert cache.size() == 3
    # Add a 4th item, should evict key_0
    cache.set("key_3", "value_3")
    assert cache.size() == 3
    assert cache.get("key_0") is None
    assert cache.get("key_3") == "value_3"


# =====================================================================
# 3. Geometry and Query Parameter Validation
# =====================================================================

def test_query_invalid_date_ordering():
    """Verify error raised when start_date is after end_date."""
    with patch("app.satellite.earth_engine._is_initialized", True):
        with pytest.raises(EarthEngineQueryError) as exc_info:
            get_sentinel_images([78.0, 22.0, 79.0, 23.0], "2026-05-01", "2026-01-01")
        assert "start_date cannot be later than end_date" in str(exc_info.value)


def test_query_malformed_date():
    """Verify error raised when date format is not YYYY-MM-DD."""
    with patch("app.satellite.earth_engine._is_initialized", True):
        with pytest.raises(EarthEngineQueryError) as exc_info:
            get_sentinel_images([78.0, 22.0, 79.0, 23.0], "invalid-date", "2026-02-01")
        assert "Invalid date format" in str(exc_info.value)


def test_parse_geometry_formats():
    """Verify parsing of bounding boxes, GeoJSON dicts, and invalid formats."""
    mock_ee = MagicMock()
    with patch("app.satellite.earth_engine.ee", mock_ee):
        with patch("app.satellite.earth_engine._is_initialized", True):
            # 1. Bounding box [min_lon, min_lat, max_lon, max_lat]
            parse_ee_geometry([78.0, 22.0, 79.0, 23.0])
            mock_ee.Geometry.BBox.assert_called_with(78.0, 22.0, 79.0, 23.0)

            # 2. Coordinate list polygon
            ring = [[78.0, 22.0], [79.0, 22.0], [79.0, 23.0], [78.0, 23.0], [78.0, 22.0]]
            parse_ee_geometry(ring)
            mock_ee.Geometry.Polygon.assert_called_with(ring)

            # 3. GeoJSON Polygon dict
            geojson = {"type": "Polygon", "coordinates": [ring]}
            parse_ee_geometry(geojson)
            mock_ee.Geometry.assert_called_with(geojson)

            # 4. Invalid geometry format raises EarthEngineQueryError
            with pytest.raises(EarthEngineQueryError):
                parse_ee_geometry("invalid_string_geom")


# =====================================================================
# 4. Spectral Index Calculations (Mock EE Engine)
# =====================================================================

def test_calculate_ndvi_calls_normalized_difference():
    """Verify calculate_ndvi calls normalizedDifference(['B8', 'B4'])."""
    mock_image = MagicMock()
    mock_ndvi = MagicMock()
    mock_image.normalizedDifference.return_value = mock_ndvi
    mock_ndvi.rename.return_value = mock_ndvi
    mock_ndvi.clamp.return_value = "clamped_ndvi"

    with patch("app.satellite.earth_engine._is_initialized", True):
        result = calculate_ndvi(mock_image)
        mock_image.normalizedDifference.assert_called_with(["B8", "B4"])
        mock_ndvi.rename.assert_called_with("NDVI")
        assert result == "clamped_ndvi"


def test_calculate_ndwi_calls_normalized_difference():
    """Verify calculate_ndwi calls normalizedDifference(['B3', 'B8'])."""
    mock_image = MagicMock()
    mock_ndwi = MagicMock()
    mock_image.normalizedDifference.return_value = mock_ndwi
    mock_ndwi.rename.return_value = mock_ndwi
    mock_ndwi.clamp.return_value = "clamped_ndwi"

    with patch("app.satellite.earth_engine._is_initialized", True):
        result = calculate_ndwi(mock_image)
        mock_image.normalizedDifference.assert_called_with(["B3", "B8"])
        mock_ndwi.rename.assert_called_with("NDWI")
        assert result == "clamped_ndwi"


def test_calculate_ndbi_calls_normalized_difference():
    """Verify calculate_ndbi calls normalizedDifference(['B11', 'B8'])."""
    mock_image = MagicMock()
    mock_ndbi = MagicMock()
    mock_image.normalizedDifference.return_value = mock_ndbi
    mock_ndbi.rename.return_value = mock_ndbi
    mock_ndbi.clamp.return_value = "clamped_ndbi"

    with patch("app.satellite.earth_engine._is_initialized", True):
        result = calculate_ndbi(mock_image)
        mock_image.normalizedDifference.assert_called_with(["B11", "B8"])
        mock_ndbi.rename.assert_called_with("NDBI")
        assert result == "clamped_ndbi"


# =====================================================================
# 5. Cloud Masking Pipeline
# =====================================================================

def test_mask_clouds_pipeline():
    """Verify mask_clouds executes QA60 bitwise operations and band scaling."""
    mock_ee = MagicMock()
    mock_image = MagicMock()
    mock_qa = MagicMock()
    mock_image.select.return_value = mock_qa
    mock_image.bandNames.return_value = MagicMock(contains=MagicMock(return_value=True))

    with patch("app.satellite.earth_engine.ee", mock_ee):
        with patch("app.satellite.earth_engine._is_initialized", True):
            mask_clouds(mock_image)
            # Must select QA60
            mock_image.select.assert_any_call("QA60")
            # Must update mask and scale bands
            mock_image.updateMask.assert_called()


# =====================================================================
# 6. Composite Reduction & Metadata
# =====================================================================

def test_calculate_composite_returns_valid_metadata():
    """Verify calculate_composite performs server-side reduction and returns metadata."""
    mock_ee = MagicMock()
    mock_collection = MagicMock()
    mock_composite = MagicMock()
    mock_collection.median.return_value = mock_composite
    mock_composite.clip.return_value = mock_composite

    # Mock server-side evaluation
    mock_stats_ee = MagicMock()
    mock_stats_ee.getInfo.return_value = {
        "NDVI_mean": 0.684,
        "NDVI_min": 0.120,
        "NDVI_max": 0.895,
        "NDVI_median": 0.710,
        "NDVI_stdDev": 0.095,
    }
    mock_area_ee = MagicMock()
    mock_area_ee.getInfo.return_value = 94000.0

    mock_multiband = MagicMock()
    mock_composite.addBands.return_value = mock_multiband
    mock_target_band = MagicMock()
    mock_multiband.select.return_value = mock_target_band
    mock_target_band.reduceRegion.return_value = mock_stats_ee
    mock_target_band.getMapId.return_value = {
        "mapid": "projects/earthengine-legacy/maps/test-map-id",
        "urlFormat": "https://earthengine.googleapis.com/v1/projects/maps/test-map-id/tiles/{z}/{x}/{y}",
    }

    mock_geom = MagicMock()
    mock_geom.area.return_value.divide.return_value = mock_area_ee

    with patch("app.satellite.earth_engine.ee", mock_ee):
        with patch("app.satellite.earth_engine._is_initialized", True):
            with patch("app.satellite.earth_engine.parse_ee_geometry", return_value=mock_geom):
                with patch("app.satellite.earth_engine.calculate_ndvi", return_value=MagicMock()):
                    with patch("app.satellite.earth_engine.calculate_ndwi", return_value=MagicMock()):
                        with patch("app.satellite.earth_engine.calculate_ndbi", return_value=MagicMock()):
                            res = calculate_composite(
                                mock_collection,
                                geometry=[78.0, 22.0, 79.0, 23.0],
                                reducer="median",
                                index_type="ndvi",
                            )

                            assert res["index_name"] == "NDVI"
                            assert res["reducer"] == "median"
                            assert res["mean"] == 0.684
                            assert res["min"] == 0.120
                            assert res["max"] == 0.895
                            assert res["surface_area_ha"] == 94000.0
                            assert res["tile_url"].startswith("https://earthengine.googleapis.com")
                            assert "computed_at" in res


# =====================================================================
# 7. Bi-Temporal Change Detection & Caching
# =====================================================================

def test_calculate_change_classification_and_caching():
    """Verify calculate_change derives loss/gain metrics and utilizes cache."""
    _ee_cache.clear()

    mock_ee = MagicMock()
    mock_col = MagicMock()
    mock_comp = MagicMock()
    mock_col.median.return_value = mock_comp
    mock_comp.clip.return_value = mock_comp

    # Mock evaluation
    mock_delta_stats = MagicMock()
    mock_delta_stats.getInfo.return_value = {
        "delta_mean": -0.042,
        "delta_min": -0.320,
        "delta_max": 0.180,
        "delta_stdDev": 0.065,
    }

    mock_loss_eval = MagicMock()
    mock_loss_eval.getInfo.return_value = {"area": 320.5}
    mock_gain_eval = MagicMock()
    mock_gain_eval.getInfo.return_value = {"area": 110.2}
    mock_total_eval = MagicMock()
    mock_total_eval.getInfo.return_value = 94000.0

    mock_base_eval = MagicMock()
    mock_base_eval.getInfo.return_value = {"NDVI": 0.68}
    mock_curr_eval = MagicMock()
    mock_curr_eval.getInfo.return_value = {"NDVI": 0.64}

    mock_geom = MagicMock()
    mock_geom.area.return_value.divide.return_value = mock_total_eval

    with patch("app.satellite.earth_engine.ee", mock_ee):
        with patch("app.satellite.earth_engine._is_initialized", True):
            with patch("app.satellite.earth_engine.parse_ee_geometry", return_value=mock_geom):
                with patch("app.satellite.earth_engine.get_sentinel_images", return_value=mock_col):
                    with patch("app.satellite.earth_engine.calculate_ndvi") as mock_ndvi_fn:
                        mock_delta = MagicMock()
                        mock_idx_base = MagicMock()
                        mock_idx_curr = MagicMock()
                        mock_idx_curr.subtract.return_value = mock_delta
                        mock_delta.rename.return_value = mock_delta
                        mock_delta.reduceRegion.return_value = mock_delta_stats
                        mock_delta.getMapId.return_value = {
                            "mapid": "test-change-mapid",
                            "urlFormat": "https://earthengine.googleapis.com/tiles/change/{z}/{x}/{y}",
                        }

                        mock_idx_base.reduceRegion.return_value = mock_base_eval
                        mock_idx_curr.reduceRegion.return_value = mock_curr_eval
                        mock_ndvi_fn.side_effect = [mock_idx_base, mock_idx_curr]

                        mock_pixel_area = MagicMock()
                        mock_ee.Image.pixelArea.return_value.divide.return_value = mock_pixel_area
                        mock_pixel_area.updateMask.return_value.reduceRegion.side_effect = [
                            mock_loss_eval,
                            mock_gain_eval,
                        ]

                        res1 = calculate_change(
                            geometry=[78.0, 22.0, 79.0, 23.0],
                            baseline_start="2025-01-01",
                            baseline_end="2025-03-31",
                            target_start="2026-01-01",
                            target_end="2026-03-31",
                            index_type="ndvi",
                        )

                        assert res1["analysis_type"] == "ndvi_change_detection"
                        assert res1["vegetation_loss_ha"] == 320.5
                        assert res1["vegetation_gain_ha"] == 110.2
                        assert res1["net_change_ha"] == round(110.2 - 320.5, 2)
                        assert res1["area_affected_ha"] == round(320.5 + 110.2, 2)
                        assert "methodology_summary" in res1
                        assert "change_tile_url" in res1

                        # Test that 2nd call hits cache without calling get_sentinel_images again
                        with patch("app.satellite.earth_engine.get_sentinel_images") as mock_get_s2:
                            res2 = calculate_change(
                                geometry=[78.0, 22.0, 79.0, 23.0],
                                baseline_start="2025-01-01",
                                baseline_end="2025-03-31",
                                target_start="2026-01-01",
                                target_end="2026-03-31",
                                index_type="ndvi",
                            )
                            mock_get_s2.assert_not_called()
                            assert res2 == res1
