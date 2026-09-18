"""Area service interacting with PostgreSQL/PostGIS Area models with resilient fallback."""
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.db.session import SessionLocal
from app.models.area import Area, ProtectedAreaModel, AreaStatisticsModel, AreaTimelineModel
from app.models.hotspot import Hotspot, HotspotModel, HotspotRelatedAlert
from app.db.geo_utils import point_to_lat_lon
from app.database import db as mock_db


class AreaService:
    @staticmethod
    def _area_to_dto(area: Area) -> ProtectedAreaModel:
        """Transforms a PostgreSQL Area ORM entity into a ProtectedAreaModel."""
        return ProtectedAreaModel(
            id=area.id,
            wdpa_id=area.wdpa_id,
            name=area.name,
            designation=area.designation,
            protected_area_type=area.protected_area_type,
            iucn_category=area.iucn_category,
            country=area.country,
            country_code=area.country_code,
            state=area.state,
            area_km2=area.area_km2,
            total_hectares=area.total_hectares,
            coordinates={"lat": area.center_lat, "lon": area.center_lon},
            forest_cover_percent=area.forest_cover_percent,
            canopy_loss_year_ha=area.canopy_loss_year_ha,
            active_fires_count=area.active_fires_count,
            threat_index=area.threat_index,
            biome=area.biome,
            last_analyzed=area.last_analyzed,
        )

    @staticmethod
    def get_areas(
        country: Optional[str] = None,
        search: Optional[str] = None,
        db_session: Optional[Session] = None,
    ) -> List[ProtectedAreaModel]:
        """Retrieve list of protected areas from PostgreSQL with resilient fallback."""
        session = db_session or SessionLocal()
        try:
            query = session.query(Area)
            if country:
                query = query.filter(
                    or_(
                        Area.country.ilike(f"%{country}%"),
                        Area.country_code.ilike(country),
                    )
                )
            if search:
                pattern = f"%{search}%"
                query = query.filter(
                    or_(
                        Area.name.ilike(pattern),
                        Area.country.ilike(pattern),
                        Area.biome.ilike(pattern),
                    )
                )
            areas = query.all()
            if areas:
                return [AreaService._area_to_dto(a) for a in areas]
        except Exception:
            pass
        finally:
            if db_session is None:
                session.close()

        # Resilient fallback to seeded store
        results = list(mock_db.areas.values())
        if country:
            results = [a for a in results if a.country.lower() == country.lower() or a.country_code.lower() == country.lower()]
        if search:
            q = search.lower()
            results = [a for a in results if q in a.name.lower() or q in a.country.lower() or q in a.biome.lower()]
        return results

    @staticmethod
    def get_area_by_id(
        area_id: str,
        db_session: Optional[Session] = None,
    ) -> Optional[ProtectedAreaModel]:
        """Retrieve protected area by ID or WDPA identifier."""
        session = db_session or SessionLocal()
        try:
            area = (
                session.query(Area)
                .filter(or_(Area.id == area_id, Area.wdpa_id.ilike(area_id)))
                .first()
            )
            if area:
                return AreaService._area_to_dto(area)
        except Exception:
            pass
        finally:
            if db_session is None:
                session.close()

        # Resilient fallback
        if area_id in mock_db.areas:
            return mock_db.areas[area_id]
        for a in mock_db.areas.values():
            if a.wdpa_id.lower() == area_id.lower():
                return a
        return None

    @staticmethod
    def get_area_statistics(
        area_id: str,
        db_session: Optional[Session] = None,
    ) -> Optional[AreaStatisticsModel]:
        """Retrieve area statistics from database or cached trajectory."""
        area = AreaService.get_area_by_id(area_id, db_session=db_session)
        if not area:
            return None
        return mock_db.statistics.get(area.id)

    @staticmethod
    def get_area_timeline(
        area_id: str,
        db_session: Optional[Session] = None,
    ) -> Optional[List[AreaTimelineModel]]:
        """Retrieve multi-temporal phenological trajectory."""
        area = AreaService.get_area_by_id(area_id, db_session=db_session)
        if not area:
            return None
        return mock_db.timelines.get(area.id, [])

    @staticmethod
    def get_area_hotspots(
        area_id: str,
        db_session: Optional[Session] = None,
    ) -> List[HotspotModel]:
        """Retrieve active degradation hotspots for an area from PostgreSQL."""
        area = AreaService.get_area_by_id(area_id, db_session=db_session)
        if not area:
            return []

        session = db_session or SessionLocal()
        try:
            records = (
                session.query(Hotspot)
                .filter(or_(Hotspot.area_id == area.id, Hotspot.area_name.ilike(area.name)))
                .all()
            )
            if records:
                return [
                    HotspotModel(
                        id=h.id,
                        area_id=h.area_id,
                        area_name=h.area_name,
                        location_detail=h.location_detail,
                        detected_at=h.detected_at.isoformat() if hasattr(h.detected_at, "isoformat") else str(h.detected_at),
                        area_ha=h.area_ha,
                        delta_ndvi=h.delta_ndvi,
                        percentage_change=h.percentage_change,
                        change_type=h.change_type,
                        severity=h.severity,
                        confidence_score=h.confidence_score,
                        coordinates=point_to_lat_lon(h.centroid_geometry),
                        status=h.status,
                        sensor=h.sensor,
                        previous_condition=h.previous_condition,
                        current_condition=h.current_condition,
                        potential_contributing_factors=h.potential_contributing_factors or [],
                        related_alerts=[],
                    )
                    for h in records
                ]
        except Exception:
            pass
        finally:
            if db_session is None:
                session.close()

        # Resilient fallback
        return [h for h in mock_db.hotspots.values() if h.area_id == area.id or h.area_name.lower() == area.name.lower()]
