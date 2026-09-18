"""0001 initial PostGIS schema with all 10 domain models

Revision ID: 0001_initial_postgis_schema
Revises: 
Create Date: 2026-09-18 17:15:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from geoalchemy2 import Geometry

# revision identifiers, used by Alembic.
revision: str = "0001_initial_postgis_schema"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. Ensure PostGIS extension exists
    op.execute("CREATE EXTENSION IF NOT EXISTS postgis;")

    # 2. Users Table
    op.create_table(
        "users",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("hashed_password", sa.String(length=255), nullable=False),
        sa.Column("full_name", sa.String(length=150), nullable=False),
        sa.Column("role", sa.String(length=50), nullable=False, server_default="RANGER"),
        sa.Column("organization", sa.String(length=150), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_users_email"), "users", ["email"], unique=True)

    # 3. Areas Table with PostGIS MultiPolygon geometry
    op.create_table(
        "areas",
        sa.Column("id", sa.String(length=64), nullable=False),
        sa.Column("wdpa_id", sa.String(length=32), nullable=False),
        sa.Column("name", sa.String(length=150), nullable=False),
        sa.Column("designation", sa.String(length=100), nullable=False),
        sa.Column("protected_area_type", sa.String(length=100), nullable=False),
        sa.Column("iucn_category", sa.String(length=50), nullable=False),
        sa.Column("country", sa.String(length=100), nullable=False),
        sa.Column("country_code", sa.String(length=10), nullable=False),
        sa.Column("state", sa.String(length=100), nullable=True),
        sa.Column("area_km2", sa.Float(), nullable=False),
        sa.Column("total_hectares", sa.Float(), nullable=False),
        sa.Column("center_lat", sa.Float(), nullable=False),
        sa.Column("center_lon", sa.Float(), nullable=False),
        sa.Column("forest_cover_percent", sa.Float(), server_default="0.0", nullable=False),
        sa.Column("canopy_loss_year_ha", sa.Float(), server_default="0.0", nullable=False),
        sa.Column("active_fires_count", sa.Integer(), server_default="0", nullable=False),
        sa.Column("threat_index", sa.Integer(), server_default="0", nullable=False),
        sa.Column("biome", sa.String(length=150), nullable=False),
        sa.Column("last_analyzed", sa.String(length=50), nullable=False),
        sa.Column("geometry", Geometry(geometry_type="MULTIPOLYGON", srid=4326, from_text="ST_GeomFromEWKT", name="geometry"), nullable=True),
        sa.Column("is_demonstration_data", sa.Boolean(), server_default=sa.true(), nullable=False),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_areas_country"), "areas", ["country"], unique=False)
    op.create_index(op.f("ix_areas_country_code"), "areas", ["country_code"], unique=False)
    op.create_index(op.f("ix_areas_name"), "areas", ["name"], unique=False)
    op.create_index(op.f("ix_areas_wdpa_id"), "areas", ["wdpa_id"], unique=False)

    # 4. Satellite Observations Table
    op.create_table(
        "satellite_observations",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("area_id", sa.String(length=64), nullable=False),
        sa.Column("satellite", sa.String(length=50), nullable=False),
        sa.Column("scene_id", sa.String(length=100), nullable=False),
        sa.Column("acquisition_date", sa.DateTime(timezone=True), nullable=False),
        sa.Column("cloud_cover_percent", sa.Float(), server_default="0.0", nullable=False),
        sa.Column("mean_ndvi", sa.Float(), nullable=False),
        sa.Column("mean_ndwi", sa.Float(), nullable=False),
        sa.Column("mean_ndbi", sa.Float(), nullable=False),
        sa.Column("tile_url", sa.String(length=255), nullable=True),
        sa.Column("metadata_json", sa.JSON(), nullable=True),
        sa.Column("is_demonstration_data", sa.Boolean(), server_default=sa.true(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(["area_id"], ["areas.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_satellite_observations_area_id"), "satellite_observations", ["area_id"], unique=False)

    # 5. Land Cover Observations Table
    op.create_table(
        "land_cover_observations",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("area_id", sa.String(length=64), nullable=False),
        sa.Column("observation_date", sa.DateTime(timezone=True), nullable=False),
        sa.Column("dense_forest_ha", sa.Float(), nullable=False),
        sa.Column("open_forest_ha", sa.Float(), nullable=False),
        sa.Column("wetlands_water_ha", sa.Float(), nullable=False),
        sa.Column("grassland_savanna_ha", sa.Float(), nullable=False),
        sa.Column("agricultural_ha", sa.Float(), nullable=False),
        sa.Column("urban_settlement_ha", sa.Float(), nullable=False),
        sa.Column("distribution_json", sa.JSON(), nullable=False),
        sa.Column("is_demonstration_data", sa.Boolean(), server_default=sa.true(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(["area_id"], ["areas.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_land_cover_observations_area_id"), "land_cover_observations", ["area_id"], unique=False)

    # 6. Hotspots Table with PostGIS Point and Polygon Geometries
    op.create_table(
        "hotspots",
        sa.Column("id", sa.String(length=64), nullable=False),
        sa.Column("area_id", sa.String(length=64), nullable=False),
        sa.Column("area_name", sa.String(length=150), nullable=False),
        sa.Column("location_detail", sa.String(length=255), nullable=False),
        sa.Column("change_type", sa.String(length=50), nullable=False),
        sa.Column("severity", sa.String(length=20), nullable=False),
        sa.Column("confidence_score", sa.Float(), nullable=False),
        sa.Column("detected_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("area_ha", sa.Float(), nullable=False),
        sa.Column("delta_ndvi", sa.Float(), nullable=False),
        sa.Column("percentage_change", sa.Float(), nullable=False),
        sa.Column("status", sa.String(length=30), server_default="NEW", nullable=False),
        sa.Column("sensor", sa.String(length=100), nullable=False),
        sa.Column("previous_condition", sa.String(length=255), nullable=False),
        sa.Column("current_condition", sa.String(length=255), nullable=False),
        sa.Column("potential_contributing_factors", sa.JSON(), nullable=False),
        sa.Column("centroid_geometry", Geometry(geometry_type="POINT", srid=4326, from_text="ST_GeomFromEWKT", name="geometry"), nullable=False),
        sa.Column("boundary_geometry", Geometry(geometry_type="POLYGON", srid=4326, from_text="ST_GeomFromEWKT", name="geometry"), nullable=True),
        sa.Column("is_demonstration_data", sa.Boolean(), server_default=sa.true(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(["area_id"], ["areas.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_hotspots_area_id"), "hotspots", ["area_id"], unique=False)
    op.create_index(op.f("ix_hotspots_change_type"), "hotspots", ["change_type"], unique=False)
    op.create_index(op.f("ix_hotspots_severity"), "hotspots", ["severity"], unique=False)
    op.create_index(op.f("ix_hotspots_detected_at"), "hotspots", ["detected_at"], unique=False)

    # 7. Change Events Table with PostGIS Geometry, change_type, severity, confidence, detected_at
    op.create_table(
        "change_events",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("area_id", sa.String(length=64), nullable=False),
        sa.Column("hotspot_id", sa.String(length=64), nullable=True),
        sa.Column("geometry", Geometry(geometry_type="GEOMETRY", srid=4326, from_text="ST_GeomFromEWKT", name="geometry"), nullable=False),
        sa.Column("change_type", sa.String(length=50), nullable=False),
        sa.Column("severity", sa.String(length=20), nullable=False),
        sa.Column("confidence", sa.Float(), nullable=False),
        sa.Column("detected_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("affected_ha", sa.Float(), server_default="0.0", nullable=False),
        sa.Column("delta_ndvi", sa.Float(), nullable=True),
        sa.Column("baseline_period", sa.String(length=50), nullable=True),
        sa.Column("target_period", sa.String(length=50), nullable=True),
        sa.Column("is_demonstration_data", sa.Boolean(), server_default=sa.true(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(["area_id"], ["areas.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["hotspot_id"], ["hotspots.id"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_change_events_area_id"), "change_events", ["area_id"], unique=False)
    op.create_index(op.f("ix_change_events_change_type"), "change_events", ["change_type"], unique=False)
    op.create_index(op.f("ix_change_events_severity"), "change_events", ["severity"], unique=False)
    op.create_index(op.f("ix_change_events_detected_at"), "change_events", ["detected_at"], unique=False)

    # 8. Alerts Table
    op.create_table(
        "alerts",
        sa.Column("id", sa.String(length=64), nullable=False),
        sa.Column("area_id", sa.String(length=64), nullable=False),
        sa.Column("area_name", sa.String(length=150), nullable=False),
        sa.Column("hotspot_id", sa.String(length=64), nullable=True),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("message", sa.Text(), nullable=False),
        sa.Column("severity", sa.String(length=20), nullable=False),
        sa.Column("status", sa.String(length=30), server_default="UNREAD", nullable=False),
        sa.Column("triggered_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("acknowledged_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("acknowledged_by", sa.String(length=36), nullable=True),
        sa.Column("is_demonstration_data", sa.Boolean(), server_default=sa.true(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(["acknowledged_by"], ["users.id"], ondelete="SET NULL"),
        sa.ForeignKeyConstraint(["area_id"], ["areas.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["hotspot_id"], ["hotspots.id"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_alerts_area_id"), "alerts", ["area_id"], unique=False)
    op.create_index(op.f("ix_alerts_severity"), "alerts", ["severity"], unique=False)
    op.create_index(op.f("ix_alerts_status"), "alerts", ["status"], unique=False)

    # 9. Wildlife Species Table
    op.create_table(
        "wildlife_species",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("area_id", sa.String(length=64), nullable=False),
        sa.Column("common_name", sa.String(length=150), nullable=False),
        sa.Column("scientific_name", sa.String(length=150), nullable=False),
        sa.Column("iucn_status", sa.String(length=50), nullable=False),
        sa.Column("estimated_population_range", sa.String(length=100), nullable=False),
        sa.Column("habitat_preference", sa.String(length=255), nullable=False),
        sa.Column("monitoring_priority", sa.String(length=20), server_default="HIGH", nullable=False),
        sa.Column("is_demonstration_data", sa.Boolean(), server_default=sa.true(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(["area_id"], ["areas.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_wildlife_species_area_id"), "wildlife_species", ["area_id"], unique=False)
    op.create_index(op.f("ix_wildlife_species_common_name"), "wildlife_species", ["common_name"], unique=False)

    # 10. Saved Areas Table
    op.create_table(
        "saved_areas",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("user_id", sa.String(length=36), nullable=False),
        sa.Column("area_id", sa.String(length=64), nullable=False),
        sa.Column("notes", sa.String(length=255), nullable=True),
        sa.Column("alert_notifications_enabled", sa.Boolean(), server_default=sa.true(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(["area_id"], ["areas.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_saved_areas_area_id"), "saved_areas", ["area_id"], unique=False)
    op.create_index(op.f("ix_saved_areas_user_id"), "saved_areas", ["user_id"], unique=False)

    # 11. Reports Table
    op.create_table(
        "reports",
        sa.Column("id", sa.String(length=64), nullable=False),
        sa.Column("area_id", sa.String(length=64), nullable=True),
        sa.Column("area_name", sa.String(length=150), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("report_type", sa.String(length=50), server_default="HABITAT_AUDIT", nullable=False),
        sa.Column("format", sa.String(length=20), server_default="GEOPDF", nullable=False),
        sa.Column("date_range", sa.String(length=50), nullable=False),
        sa.Column("status", sa.String(length=20), server_default="READY", nullable=False),
        sa.Column("file_size_bytes", sa.Integer(), server_default="0", nullable=False),
        sa.Column("download_url", sa.String(length=255), nullable=False),
        sa.Column("generated_by", sa.String(length=36), nullable=True),
        sa.Column("is_demonstration_data", sa.Boolean(), server_default=sa.true(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(["area_id"], ["areas.id"], ondelete="SET NULL"),
        sa.ForeignKeyConstraint(["generated_by"], ["users.id"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_reports_area_id"), "reports", ["area_id"], unique=False)
    op.create_index(op.f("ix_reports_status"), "reports", ["status"], unique=False)


def downgrade() -> None:
    op.drop_table("reports")
    op.drop_table("saved_areas")
    op.drop_table("wildlife_species")
    op.drop_table("alerts")
    op.drop_table("change_events")
    op.drop_table("hotspots")
    op.drop_table("land_cover_observations")
    op.drop_table("satellite_observations")
    op.drop_table("areas")
    op.drop_table("users")
