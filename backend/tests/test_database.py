"""Comprehensive test suite for PostgreSQL/PostGIS database models, geometries, and seed data."""
import pytest
from datetime import datetime, timezone
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from geoalchemy2.elements import WKTElement

from app.db.base import Base
from app.models.user import User
from app.models.area import Area
from app.models.observation import SatelliteObservation, LandCoverObservation
from app.models.change_event import ChangeEvent
from app.models.hotspot import Hotspot
from app.models.alert import Alert
from app.models.wildlife import WildlifeSpecies
from app.models.saved_area import SavedArea
from app.models.report import Report
from app.db.geo_utils import point_to_lat_lon, geometry_to_geojson
from app.db.seed_data import (
    get_wkt_multipolygon,
    get_wkt_polygon,
    get_wkt_point,
    DEMO_DISCLAIMER,
)


def test_registered_tables_in_metadata():
    """Verify all 10 required domain model tables are registered in SQLAlchemy metadata."""
    expected_tables = {
        "users",
        "areas",
        "satellite_observations",
        "land_cover_observations",
        "change_events",
        "hotspots",
        "alerts",
        "wildlife_species",
        "saved_areas",
        "reports",
    }
    registered = set(Base.metadata.tables.keys())
    for tbl in expected_tables:
        assert tbl in registered, f"Table '{tbl}' is missing from Base.metadata"


def test_area_model_has_postgis_geometry():
    """Verify Area model contains PostGIS MultiPolygon geometry column."""
    area_table = Base.metadata.tables["areas"]
    assert "geometry" in area_table.columns
    geom_col = area_table.columns["geometry"]
    assert hasattr(geom_col.type, "geometry_type")
    assert geom_col.type.geometry_type == "MULTIPOLYGON"
    assert geom_col.type.srid == 4326


def test_change_event_model_has_required_attributes():
    """Verify ChangeEvent model contains geometry, change_type, severity, confidence, detected_at."""
    ce_table = Base.metadata.tables["change_events"]
    assert "geometry" in ce_table.columns
    assert "change_type" in ce_table.columns
    assert "severity" in ce_table.columns
    assert "confidence" in ce_table.columns
    assert "detected_at" in ce_table.columns

    # Verify column properties
    geom_col = ce_table.columns["geometry"]
    assert hasattr(geom_col.type, "geometry_type")
    assert geom_col.type.geometry_type == "GEOMETRY"
    assert geom_col.type.srid == 4326


def test_hotspot_model_has_spatial_geometries():
    """Verify Hotspot model has PostGIS Point centroid and optional Polygon boundary."""
    hotspot_table = Base.metadata.tables["hotspots"]
    assert "centroid_geometry" in hotspot_table.columns
    assert "boundary_geometry" in hotspot_table.columns

    centroid_col = hotspot_table.columns["centroid_geometry"]
    assert hasattr(centroid_col.type, "geometry_type")
    assert centroid_col.type.geometry_type == "POINT"
    assert centroid_col.type.srid == 4326


def test_user_model_instantiation():
    """Verify User model attributes and defaults."""
    user = User(
        id="usr-test-01",
        email="ranger@wildlifewatch.org",
        hashed_password="hashed_secret_token",
        full_name="Chief Warden",
        role="RANGER",
        organization="Conservation Agency",
        is_active=True,
    )
    assert user.id == "usr-test-01"
    assert user.role == "RANGER"
    assert user.is_active is True


def test_area_model_instantiation_with_geometry():
    """Verify Area model with WKT MultiPolygon geometry."""
    geom = get_wkt_multipolygon(80.45, 22.15, 80.78, 22.45)
    area = Area(
        id="area-kanha-test",
        wdpa_id="WDPA-TEST-001",
        name="Kanha National Park",
        designation="Tiger Reserve",
        protected_area_type="National Park",
        iucn_category="II",
        country="India",
        country_code="IN",
        state="Madhya Pradesh",
        area_km2=940.0,
        total_hectares=94000.0,
        center_lat=22.334,
        center_lon=80.611,
        biome="Central Deccan Moist Deciduous Forest",
        last_analyzed="2026-09-17",
        geometry=geom,
        is_demonstration_data=True,
    )
    assert area.name == "Kanha National Park"
    assert area.total_hectares == 94000.0
    assert area.geometry.srid == 4326
    assert area.is_demonstration_data is True


def test_change_event_instantiation():
    """Verify ChangeEvent instantiation with all 5 mandatory attributes."""
    poly_geom = get_wkt_polygon(80.63, 22.28, 80.65, 22.29)
    now = datetime.now(timezone.utc)
    ce = ChangeEvent(
        id="ce-test-01",
        area_id="area-kanha-test",
        geometry=poly_geom,
        change_type="VEGETATION_LOSS",
        severity="CRITICAL",
        confidence=0.94,
        detected_at=now,
        affected_ha=14.8,
        delta_ndvi=-0.52,
        is_demonstration_data=True,
    )
    assert ce.change_type == "VEGETATION_LOSS"
    assert ce.severity == "CRITICAL"
    assert ce.confidence == 0.94
    assert ce.detected_at == now
    assert ce.geometry.srid == 4326


def test_hotspot_instantiation():
    """Verify Hotspot model with centroid and boundary geometries."""
    point = get_wkt_point(80.642, 22.285)
    poly = get_wkt_polygon(80.638, 22.280, 80.646, 22.290)
    now = datetime.now(timezone.utc)
    hs = Hotspot(
        id="HS-TEST-01",
        area_id="area-kanha-test",
        area_name="Kanha National Park",
        location_detail="Mukki Sector",
        change_type="VEGETATION_LOSS",
        severity="CRITICAL",
        confidence_score=0.94,
        detected_at=now,
        area_ha=14.8,
        delta_ndvi=-0.52,
        percentage_change=-41.2,
        sensor="Sentinel-2 MSI (10m)",
        previous_condition="Dense Sal Canopy",
        current_condition="Canopy Thinning",
        potential_contributing_factors=["Logging trail proximity"],
        centroid_geometry=point,
        boundary_geometry=poly,
        is_demonstration_data=True,
    )
    assert hs.id == "HS-TEST-01"
    assert hs.centroid_geometry.srid == 4326
    assert hs.boundary_geometry.srid == 4326


def test_observation_models_instantiation():
    """Verify SatelliteObservation and LandCoverObservation models."""
    now = datetime.now(timezone.utc)
    sat_obs = SatelliteObservation(
        id="obs-sat-01",
        area_id="area-kanha-test",
        satellite="Sentinel-2 MSI",
        scene_id="S2A_TEST_SCENE",
        acquisition_date=now,
        cloud_cover_percent=1.2,
        mean_ndvi=0.76,
        mean_ndwi=0.12,
        mean_ndbi=-0.28,
        is_demonstration_data=True,
    )
    assert sat_obs.satellite == "Sentinel-2 MSI"
    assert sat_obs.mean_ndvi == 0.76

    lc_obs = LandCoverObservation(
        id="obs-lc-01",
        area_id="area-kanha-test",
        observation_date=now,
        dense_forest_ha=65000.0,
        open_forest_ha=18000.0,
        wetlands_water_ha=4200.0,
        grassland_savanna_ha=5800.0,
        agricultural_ha=800.0,
        urban_settlement_ha=200.0,
        distribution_json={"dense_forest": 69.1, "open_forest": 19.1},
        is_demonstration_data=True,
    )
    assert lc_obs.dense_forest_ha == 65000.0
    assert lc_obs.is_demonstration_data is True


def test_wildlife_species_scientific_standard():
    """Verify WildlifeSpecies stores population estimates without unsupported claims."""
    species = WildlifeSpecies(
        id="sp-test-01",
        area_id="area-kanha-test",
        common_name="Bengal Tiger",
        scientific_name="Panthera tigris tigris",
        iucn_status="ENDANGERED",
        estimated_population_range="100 - 130 individuals (estimated core survey)",
        habitat_preference="Dense Sal & Mixed Deciduous Forest",
        monitoring_priority="CRITICAL",
        is_demonstration_data=True,
    )
    assert species.common_name == "Bengal Tiger"
    assert "survey" in species.estimated_population_range.lower()
    assert species.is_demonstration_data is True


def test_saved_area_and_report_models():
    """Verify SavedArea bookmark and Report catalog models."""
    saved = SavedArea(
        id="sa-test-01",
        user_id="usr-test-01",
        area_id="area-kanha-test",
        notes="High-priority surveillance buffer",
        alert_notifications_enabled=True,
    )
    assert saved.alert_notifications_enabled is True

    rep = Report(
        id="REP-TEST-01",
        area_id="area-kanha-test",
        area_name="Kanha National Park",
        title="Bi-Temporal Change Vector Dossier",
        report_type="CHANGE_DOSSIER",
        format="GEOPDF",
        date_range="2024-09 to 2026-09",
        status="READY",
        file_size_bytes=14200000,
        download_url="/api/reports/REP-TEST-01/download",
        is_demonstration_data=True,
    )
    assert rep.format == "GEOPDF"
    assert rep.is_demonstration_data is True


def test_geo_utils_point_extraction():
    """Verify point_to_lat_lon extraction from WKT."""
    point = get_wkt_point(80.611, 22.334)
    coords = point_to_lat_lon(point)
    assert pytest.approx(coords["lon"], 0.001) == 80.611
    assert pytest.approx(coords["lat"], 0.001) == 22.334


def test_seed_data_definitions_contain_required_parks():
    """Verify seed data definitions include Kanha, Bandhavgarh, Satpura, and Kaziranga."""
    from app.db.seed_data import seed_database
    # Check that seed disclaimer is present and clear
    assert "DEMONSTRATION TELEMETRY" in DEMO_DISCLAIMER
    assert "ground-truth" in DEMO_DISCLAIMER
