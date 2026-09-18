"""Seed database with demonstration protected reserves, observations, change events, and hotspots.
All telemetry is explicitly identified as demonstration data for spatial simulation purposes.
"""
import logging
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from geoalchemy2.elements import WKTElement

from app.db.session import SessionLocal
from app.models.user import User
from app.models.area import Area
from app.models.observation import SatelliteObservation, LandCoverObservation
from app.models.change_event import ChangeEvent
from app.models.hotspot import Hotspot
from app.models.alert import Alert
from app.models.wildlife import WildlifeSpecies
from app.models.saved_area import SavedArea
from app.models.report import Report

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("wildlife_watch.seed_data")

DEMO_DISCLAIMER = (
    "DEMONSTRATION TELEMETRY: Synthetic remote sensing and ecological records generated "
    "for spatial intelligence interface validation. Spatial correlations require ground-truth "
    "ranger patrol inspection before asserting environmental causation."
)


def get_wkt_multipolygon(min_lon: float, min_lat: float, max_lon: float, max_lat: float) -> WKTElement:
    """Generate WGS84 MultiPolygon WKT for reserve boundary."""
    wkt = (
        f"MULTIPOLYGON((({min_lon} {min_lat}, {max_lon} {min_lat}, "
        f"{max_lon} {max_lat}, {min_lon} {max_lat}, {min_lon} {min_lat})))"
    )
    return WKTElement(wkt, srid=4326)


def get_wkt_polygon(min_lon: float, min_lat: float, max_lon: float, max_lat: float) -> WKTElement:
    """Generate WGS84 Polygon WKT for disturbance polygon."""
    wkt = (
        f"POLYGON(({min_lon} {min_lat}, {max_lon} {min_lat}, "
        f"{max_lon} {max_lat}, {min_lon} {max_lat}, {min_lon} {min_lat}))"
    )
    return WKTElement(wkt, srid=4326)


def get_wkt_point(lon: float, lat: float) -> WKTElement:
    """Generate WGS84 Point WKT for hotspot centroid."""
    return WKTElement(f"POINT({lon} {lat})", srid=4326)


def seed_database(db: Session = None) -> bool:
    """Seeds the database with required demonstration datasets."""
    close_db = False
    if db is None:
        db = SessionLocal()
        close_db = True

    try:
        logger.info("Seeding database with demonstration entities...")

        # 1. Seed Demonstration Users
        user_connor = db.query(User).filter(User.email == "sarah.connor@wildlifewatch.org").first()
        if not user_connor:
            user_connor = User(
                id="usr-sarah-connor",
                email="sarah.connor@wildlifewatch.org",
                hashed_password="demo_hashed_token_wildlife_watch_2026",
                full_name="Dr. Sarah Connor",
                role="RANGER",
                organization="Kenya Wildlife Service (KWS)",
                is_active=True,
            )
            db.add(user_connor)

        # 2. Seed 4 Core Indian Reserves (+ additional global reserves)
        areas_data = [
            {
                "id": "area-kanha",
                "wdpa_id": "WDPA-IND-001",
                "name": "Kanha National Park",
                "designation": "Tiger Reserve & National Park",
                "protected_area_type": "National Park",
                "iucn_category": "II",
                "country": "India",
                "country_code": "IN",
                "state": "Madhya Pradesh",
                "area_km2": 940.0,
                "total_hectares": 94000.0,
                "center_lat": 22.334,
                "center_lon": 80.611,
                "forest_cover_percent": 88.4,
                "canopy_loss_year_ha": 34.2,
                "active_fires_count": 0,
                "threat_index": 28,
                "biome": "Central Deccan Moist Deciduous Forest",
                "last_analyzed": "2026-09-17",
                "bbox": (80.45, 22.15, 80.78, 22.45),
            },
            {
                "id": "area-bandhavgarh",
                "wdpa_id": "WDPA-IND-002",
                "name": "Bandhavgarh National Park",
                "designation": "Tiger Reserve & National Park",
                "protected_area_type": "National Park",
                "iucn_category": "II",
                "country": "India",
                "country_code": "IN",
                "state": "Madhya Pradesh",
                "area_km2": 453.0,
                "total_hectares": 45300.0,
                "center_lat": 23.718,
                "center_lon": 81.015,
                "forest_cover_percent": 76.5,
                "canopy_loss_year_ha": 52.8,
                "active_fires_count": 1,
                "threat_index": 44,
                "biome": "Vindhyan Dry Deciduous & Bamboo Woodlands",
                "last_analyzed": "2026-09-17",
                "bbox": (80.85, 23.55, 81.18, 23.85),
            },
            {
                "id": "area-satpura",
                "wdpa_id": "WDPA-IND-003",
                "name": "Satpura Tiger Reserve",
                "designation": "Tiger Reserve & Biosphere Core",
                "protected_area_type": "National Park",
                "iucn_category": "II",
                "country": "India",
                "country_code": "IN",
                "state": "Madhya Pradesh",
                "area_km2": 1333.0,
                "total_hectares": 133300.0,
                "center_lat": 22.495,
                "center_lon": 78.249,
                "forest_cover_percent": 82.1,
                "canopy_loss_year_ha": 41.5,
                "active_fires_count": 3,
                "threat_index": 56,
                "biome": "Satpura Hill Range Mixed Deciduous Canopy",
                "last_analyzed": "2026-09-16",
                "bbox": (78.05, 22.30, 78.50, 22.70),
            },
            {
                "id": "area-2",  # Kaziranga National Park
                "wdpa_id": "WDPA-IND-004",
                "name": "Kaziranga National Park",
                "designation": "UNESCO World Heritage Site & National Park",
                "protected_area_type": "National Park",
                "iucn_category": "II",
                "country": "India",
                "country_code": "IN",
                "state": "Assam",
                "area_km2": 858.0,
                "total_hectares": 85800.0,
                "center_lat": 26.589,
                "center_lon": 93.182,
                "forest_cover_percent": 62.3,
                "canopy_loss_year_ha": 18.5,
                "active_fires_count": 0,
                "threat_index": 35,
                "biome": "Brahmaputra Alluvial Plain Grasslands & Wetlands",
                "last_analyzed": "2026-09-17",
                "bbox": (93.00, 26.50, 93.45, 26.75),
            },
            {
                "id": "area-1",
                "wdpa_id": "WDPA-TZA-001",
                "name": "Serengeti National Park",
                "designation": "National Park & Biosphere Reserve",
                "protected_area_type": "National Park",
                "iucn_category": "II",
                "country": "Tanzania",
                "country_code": "TZ",
                "state": "Mara",
                "area_km2": 14763.0,
                "total_hectares": 1476300.0,
                "center_lat": -2.333,
                "center_lon": 34.833,
                "forest_cover_percent": 34.2,
                "canopy_loss_year_ha": 86.4,
                "active_fires_count": 2,
                "threat_index": 31,
                "biome": "Serengeti Volcanic Grasslands & Savannas",
                "last_analyzed": "2026-09-16",
                "bbox": (34.50, -2.60, 35.10, -2.10),
            },
            {
                "id": "area-5",
                "wdpa_id": "WDPA-COD-001",
                "name": "Virunga National Park",
                "designation": "National Park & World Heritage Site",
                "protected_area_type": "National Park",
                "iucn_category": "II",
                "country": "Democratic Republic of the Congo",
                "country_code": "CD",
                "state": "North Kivu",
                "area_km2": 7800.0,
                "total_hectares": 780000.0,
                "center_lat": -0.0572,
                "center_lon": 29.5085,
                "forest_cover_percent": 74.2,
                "canopy_loss_year_ha": 124.5,
                "active_fires_count": 8,
                "threat_index": 78,
                "biome": "Albertine Rift Montane & Lowland Forests",
                "last_analyzed": "2026-09-17",
                "bbox": (29.20, -0.30, 29.80, 0.20),
            },
        ]

        for item in areas_data:
            existing_area = db.query(Area).filter(Area.id == item["id"]).first()
            bbox = item["bbox"]
            geom = get_wkt_multipolygon(bbox[0], bbox[1], bbox[2], bbox[3])

            if not existing_area:
                new_area = Area(
                    id=item["id"],
                    wdpa_id=item["wdpa_id"],
                    name=item["name"],
                    designation=item["designation"],
                    protected_area_type=item["protected_area_type"],
                    iucn_category=item["iucn_category"],
                    country=item["country"],
                    country_code=item["country_code"],
                    state=item["state"],
                    area_km2=item["area_km2"],
                    total_hectares=item["total_hectares"],
                    center_lat=item["center_lat"],
                    center_lon=item["center_lon"],
                    forest_cover_percent=item["forest_cover_percent"],
                    canopy_loss_year_ha=item["canopy_loss_year_ha"],
                    active_fires_count=item["active_fires_count"],
                    threat_index=item["threat_index"],
                    biome=item["biome"],
                    last_analyzed=item["last_analyzed"],
                    geometry=geom,
                    is_demonstration_data=True,
                    notes=DEMO_DISCLAIMER,
                )
                db.add(new_area)
            else:
                existing_area.geometry = geom
                existing_area.is_demonstration_data = True
                existing_area.notes = DEMO_DISCLAIMER

        db.flush()

        # 3. Seed Wildlife Species (Demonstration Survey Ranges)
        species_data = [
            ("sp-1", "area-kanha", "Bengal Tiger", "Panthera tigris tigris", "ENDANGERED", "100 - 130 individuals (estimated core survey)", "Dense Sal & Mixed Deciduous Forest", "CRITICAL"),
            ("sp-2", "area-kanha", "Hard Ground Barasingha", "Rucervus duvaucelii branderi", "VULNERABLE", "750 - 850 individuals (savanna meadow survey)", "Tall Grassland & Meadow Clearings", "HIGH"),
            ("sp-3", "area-kanha", "Indian Leopard", "Panthera pardus fusca", "VULNERABLE", "80 - 110 individuals (camera-trap estimate)", "Rugged Hills & Buffer Woodland", "HIGH"),
            ("sp-4", "area-bandhavgarh", "Bengal Tiger", "Panthera tigris tigris", "ENDANGERED", "60 - 75 individuals (high density core survey)", "Bamboo Clumps & Valley Basins", "CRITICAL"),
            ("sp-5", "area-bandhavgarh", "Sloth Bear", "Melursus ursinus", "VULNERABLE", "40 - 60 individuals (estimated range)", "Rocky Outcrops & Scrub Woodlands", "HIGH"),
            ("sp-6", "area-satpura", "Indian Giant Squirrel", "Ratufa indica", "LEAST_CONCERN", "Abundant canopy indicator (survey sample)", "High Dense Teak & Sal Crown Canopy", "MEDIUM"),
            ("sp-7", "area-satpura", "Malabar Pied Hornbill", "Anthracoceros coronatus", "NEAR_THREATENED", "Breeding pairs documented in gorge valleys", "Riparian Riverine Forest Corridors", "HIGH"),
            ("sp-8", "area-2", "Great Indian One-Horned Rhinoceros", "Rhinoceros unicornis", "VULNERABLE", "2,400 - 2,600 individuals (census range estimate)", "Tall Elephant Grasslands & Beels", "CRITICAL"),
            ("sp-9", "area-2", "Asian Elephant", "Elephas maximus", "ENDANGERED", "1,000 - 1,200 individuals (floodplain migratory herd)", "Alluvial Grasslands & Riverine Channels", "HIGH"),
        ]

        for sp_id, area_id, c_name, s_name, iucn, pop_range, habit, prio in species_data:
            if not db.query(WildlifeSpecies).filter(WildlifeSpecies.id == sp_id).first():
                db.add(
                    WildlifeSpecies(
                        id=sp_id,
                        area_id=area_id,
                        common_name=c_name,
                        scientific_name=s_name,
                        iucn_status=iucn,
                        estimated_population_range=pop_range,
                        habitat_preference=habit,
                        monitoring_priority=prio,
                        is_demonstration_data=True,
                    )
                )

        # 4. Seed Hotspots & Change Events with PostGIS Geometries
        hotspots_data = [
            {
                "id": "HS-KANHA-01",
                "area_id": "area-kanha",
                "area_name": "Kanha National Park",
                "location_detail": "Mukki Sector, South-Eastern Buffer",
                "detected_at": datetime(2026, 9, 17, 6, 30, tzinfo=timezone.utc),
                "area_ha": 14.8,
                "delta_ndvi": -0.52,
                "percentage_change": -41.2,
                "change_type": "VEGETATION_LOSS",
                "severity": "CRITICAL",
                "confidence_score": 0.94,
                "lat": 22.285,
                "lon": 80.642,
                "sensor": "Sentinel-2 MSI (10m)",
                "previous_condition": "Dense Mixed Sal Canopy (Mean NDVI: 0.81)",
                "current_condition": "Canopy Clearance & Exposed Laterite Soil (Mean NDVI: 0.29)",
                "factors": [
                    "Linear road/haulage track geometry detected on shortwave infrared (B11/B8)",
                    "Gentle slope accessibility (< 6°) allowing vehicular transit",
                    "Recent dry season soil moisture deficit observed across sector",
                ],
                "bbox": (80.638, 22.280, 80.646, 22.290),
            },
            {
                "id": "HS-BANDH-02",
                "area_id": "area-bandhavgarh",
                "area_name": "Bandhavgarh National Park",
                "location_detail": "Tala Core Zone, Eastern Boundary",
                "detected_at": datetime(2026, 9, 17, 14, 45, tzinfo=timezone.utc),
                "area_ha": 9.7,
                "delta_ndvi": -0.45,
                "percentage_change": -37.8,
                "change_type": "URBAN_EXPANSION",
                "severity": "HIGH",
                "confidence_score": 0.91,
                "lat": 23.718,
                "lon": 81.015,
                "sensor": "Sentinel-2 MSI (10m)",
                "previous_condition": "Mixed Deciduous Forest with Bamboo Understory (Mean NDVI: 0.72)",
                "current_condition": "Cleared Clearing with Linear Built Structures (NDBI: +0.28, NDVI: 0.35)",
                "factors": [
                    "Contiguous extension from existing rural settlement road network",
                    "High NDBI spectral signature indicating compacted soil and impervious materials",
                ],
                "bbox": (81.010, 23.712, 81.020, 23.724),
            },
            {
                "id": "HS-SATP-03",
                "area_id": "area-satpura",
                "area_name": "Satpura Tiger Reserve",
                "location_detail": "Bori Wildlife Sanctuary Zone, Pachmarhi Slopes",
                "detected_at": datetime(2026, 9, 16, 17, 20, tzinfo=timezone.utc),
                "area_ha": 16.3,
                "delta_ndvi": -0.54,
                "percentage_change": -46.2,
                "change_type": "FIRE",
                "severity": "CRITICAL",
                "confidence_score": 0.97,
                "lat": 22.495,
                "lon": 78.249,
                "sensor": "VIIRS 375m / S2 MSI",
                "previous_condition": "Dry Deciduous Teak & Bamboo Canopy (Mean NDVI: 0.68)",
                "current_condition": "Active Thermal Scar with Carbon Residuals (Normalized Burn Ratio: -0.42)",
                "factors": [
                    "VIIRS active thermal detection (42.6 MW FRP) recorded 6 hours prior to pass",
                    "Elevated fuel load accumulated following prolonged dry spell",
                ],
                "bbox": (78.240, 22.490, 78.258, 22.500),
            },
            {
                "id": "HS-KAZI-04",
                "area_id": "area-2",
                "area_name": "Kaziranga National Park",
                "location_detail": "Bagori Range, Brahmaputra Floodplain",
                "detected_at": datetime(2026, 9, 17, 11, 5, tzinfo=timezone.utc),
                "area_ha": 6.8,
                "delta_ndvi": -0.39,
                "percentage_change": -33.4,
                "change_type": "WATER_LOSS",
                "severity": "HIGH",
                "confidence_score": 0.92,
                "lat": 26.589,
                "lon": 93.182,
                "sensor": "Sentinel-2 MSI (10m)",
                "previous_condition": "Perennial Wetland Channel & Oxbow Beel (Mean NDWI: +0.52)",
                "current_condition": "Desiccated Silt Splay and Silt Deposition (Mean NDWI: -0.18)",
                "factors": [
                    "Post-monsoon river course silt deposition along main river braiding channel",
                    "Reduced upstream tributary discharge following dry seasonal cycle",
                ],
                "bbox": (93.175, 26.584, 93.189, 26.594),
            },
        ]

        for h in hotspots_data:
            existing_hs = db.query(Hotspot).filter(Hotspot.id == h["id"]).first()
            c_geom = get_wkt_point(h["lon"], h["lat"])
            b_box = h["bbox"]
            b_geom = get_wkt_polygon(b_box[0], b_box[1], b_box[2], b_box[3])

            if not existing_hs:
                hs_record = Hotspot(
                    id=h["id"],
                    area_id=h["area_id"],
                    area_name=h["area_name"],
                    location_detail=h["location_detail"],
                    change_type=h["change_type"],
                    severity=h["severity"],
                    confidence_score=h["confidence_score"],
                    detected_at=h["detected_at"],
                    area_ha=h["area_ha"],
                    delta_ndvi=h["delta_ndvi"],
                    percentage_change=h["percentage_change"],
                    status="NEW",
                    sensor=h["sensor"],
                    previous_condition=h["previous_condition"],
                    current_condition=h["current_condition"],
                    potential_contributing_factors=h["factors"],
                    centroid_geometry=c_geom,
                    boundary_geometry=b_geom,
                    is_demonstration_data=True,
                )
                db.add(hs_record)

            # Seed matching ChangeEvent
            ce_id = f"CE-{h['id']}"
            if not db.query(ChangeEvent).filter(ChangeEvent.id == ce_id).first():
                ce_record = ChangeEvent(
                    id=ce_id,
                    area_id=h["area_id"],
                    hotspot_id=h["id"],
                    geometry=b_geom,
                    change_type=h["change_type"],
                    severity=h["severity"],
                    confidence=h["confidence_score"],
                    detected_at=h["detected_at"],
                    affected_ha=h["area_ha"],
                    delta_ndvi=h["delta_ndvi"],
                    baseline_period="2024-09",
                    target_period="2026-09",
                    is_demonstration_data=True,
                )
                db.add(ce_record)

        # 5. Seed Demonstration Alerts
        alerts_data = [
            ("ALT-KANHA-881", "area-kanha", "Kanha National Park", "HS-KANHA-01", "Critical Canopy Deficit Detected in Mukki Sector", "Sentinel-2 Level-2A pass recorded a 14.8 ha acute canopy loss patch with -0.52 ΔNDVI.", "CRITICAL", datetime(2026, 9, 17, 7, 15, tzinfo=timezone.utc)),
            ("ALT-SATP-912", "area-satpura", "Satpura Tiger Reserve", "HS-SATP-03", "Thermal Anomaly (VIIRS 42.6 MW) Confirmed by Sentinel-2 Burn Scar", "VIIRS thermal hotspot verified by 16.3 ha burn scar polygon on Pachmarhi slopes.", "CRITICAL", datetime(2026, 9, 16, 17, 45, tzinfo=timezone.utc)),
            ("ALT-BANDH-402", "area-bandhavgarh", "Bandhavgarh National Park", "HS-BANDH-02", "Encroachment Signature Identified near Tala Sector", "SWIR-derived NDBI spike indicates 9.7 ha soil compaction and linear road construction.", "HIGH", datetime(2026, 9, 17, 15, 20, tzinfo=timezone.utc)),
            ("ALT-KAZI-304", "area-2", "Kaziranga National Park", "HS-KAZI-04", "Oxbow Wetland Desiccation in Bagori Range", "Surface water reduction of 6.8 ha detected following Brahmaputra silt deposition.", "HIGH", datetime(2026, 9, 17, 12, 0, tzinfo=timezone.utc)),
        ]

        for a_id, area_id, a_name, hs_id, title, msg, sev, trig_at in alerts_data:
            if not db.query(Alert).filter(Alert.id == a_id).first():
                db.add(
                    Alert(
                        id=a_id,
                        area_id=area_id,
                        area_name=a_name,
                        hotspot_id=hs_id,
                        title=title,
                        message=msg,
                        severity=sev,
                        status="UNREAD",
                        triggered_at=trig_at,
                        is_demonstration_data=True,
                    )
                )

        # 6. Seed Demonstration Observations
        obs_data = [
            ("OBS-KANHA-01", "area-kanha", "Sentinel-2 MSI", "S2A_MSIL2A_20260915T052641_R019_T44QME", datetime(2026, 9, 15, 5, 26, tzinfo=timezone.utc), 1.2, 0.76, 0.12, -0.28),
            ("OBS-BANDH-01", "area-bandhavgarh", "Sentinel-2 MSI", "S2B_MSIL2A_20260914T051659_R019_T44QNE", datetime(2026, 9, 14, 5, 16, tzinfo=timezone.utc), 2.4, 0.68, 0.08, -0.19),
            ("OBS-SATP-01", "area-satpura", "Sentinel-2 MSI", "S2A_MSIL2A_20260916T053651_R062_T43QGF", datetime(2026, 9, 16, 5, 36, tzinfo=timezone.utc), 0.8, 0.71, 0.14, -0.22),
            ("OBS-KAZI-01", "area-2", "Sentinel-2 MSI", "S2B_MSIL2A_20260913T044649_R090_T46RDP", datetime(2026, 9, 13, 4, 46, tzinfo=timezone.utc), 3.1, 0.58, 0.44, -0.31),
        ]

        for o_id, area_id, sat, scene, acq, cloud, ndvi, ndwi, ndbi in obs_data:
            if not db.query(SatelliteObservation).filter(SatelliteObservation.id == o_id).first():
                db.add(
                    SatelliteObservation(
                        id=o_id,
                        area_id=area_id,
                        satellite=sat,
                        scene_id=scene,
                        acquisition_date=acq,
                        cloud_cover_percent=cloud,
                        mean_ndvi=ndvi,
                        mean_ndwi=ndwi,
                        mean_ndbi=ndbi,
                        is_demonstration_data=True,
                    )
                )

        # 7. Seed Reports
        reports_data = [
            ("REP-2026-09-01", "area-kanha", "Kanha National Park", "Monthly Habitat Integrity Audit - September 2026", "HABITAT_AUDIT", "GEOPDF", "2026-08-15 to 2026-09-15", "READY", 18452000, "/api/reports/REP-2026-09-01/download"),
            ("REP-2026-09-02", "area-bandhavgarh", "Bandhavgarh National Park", "Bi-Temporal Change Vector Dossier - Tala Encroachment", "CHANGE_DOSSIER", "GEOPACKAGE", "2024-09-01 to 2026-09-01", "READY", 45890000, "/api/reports/REP-2026-09-02/download"),
            ("REP-2026-09-03", None, "Pan-Reserve Monitoring Network", "Quarterly Hotspot Incidents CSV Export", "INCIDENT_EXPORT", "CSV", "2026-06-01 to 2026-09-15", "READY", 845000, "/api/reports/REP-2026-09-03/download"),
        ]

        for r_id, a_id, a_name, title, r_type, fmt, d_range, st, size, url in reports_data:
            if not db.query(Report).filter(Report.id == r_id).first():
                db.add(
                    Report(
                        id=r_id,
                        area_id=a_id,
                        area_name=a_name,
                        title=title,
                        report_type=r_type,
                        format=fmt,
                        date_range=d_range,
                        status=st,
                        file_size_bytes=size,
                        download_url=url,
                        is_demonstration_data=True,
                    )
                )

        db.commit()
        logger.info("Successfully seeded database with demonstration entities!")
        return True
    except Exception as e:
        logger.error("Failed to seed database: %s", e)
        db.rollback()
        return False
    finally:
        if close_db:
            db.close()


if __name__ == "__main__":
    seed_database()
