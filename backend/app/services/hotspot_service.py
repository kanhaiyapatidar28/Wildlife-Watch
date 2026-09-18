"""Hotspot service interacting with PostgreSQL/PostGIS Hotspot models with resilient fallback."""
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.db.session import SessionLocal
from app.models.hotspot import Hotspot, HotspotModel, HotspotRelatedAlert
from app.db.geo_utils import point_to_lat_lon
from app.database import db as mock_db


class HotspotService:
    @staticmethod
    def _hotspot_to_dto(h: Hotspot) -> HotspotModel:
        """Transforms a PostgreSQL Hotspot ORM entity into HotspotModel."""
        coords = point_to_lat_lon(h.centroid_geometry)
        related_alerts = []
        if hasattr(h, "alerts") and h.alerts:
            related_alerts = [
                HotspotRelatedAlert(
                    id=a.id,
                    title=a.title,
                    severity=a.severity,
                    timestamp=a.triggered_at.isoformat() if hasattr(a.triggered_at, "isoformat") else str(a.triggered_at),
                )
                for a in h.alerts
            ]
        return HotspotModel(
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
            coordinates=coords,
            status=h.status,
            sensor=h.sensor,
            previous_condition=h.previous_condition,
            current_condition=h.current_condition,
            potential_contributing_factors=h.potential_contributing_factors or [],
            related_alerts=related_alerts,
        )

    @staticmethod
    def get_hotspots(
        change_type: Optional[str] = None,
        severity: Optional[str] = None,
        area_id: Optional[str] = None,
        min_confidence: Optional[float] = None,
        search: Optional[str] = None,
        db_session: Optional[Session] = None,
    ) -> List[HotspotModel]:
        """Retrieve filtered hotspots from PostgreSQL with fallback."""
        session = db_session or SessionLocal()
        try:
            query = session.query(Hotspot)
            if change_type and change_type.upper() != "ALL":
                ctype = change_type.upper()
                if ctype == "VEGETATION_LOSS":
                    query = query.filter(Hotspot.change_type.in_(["VEGETATION_LOSS", "DEFORESTATION", "CANOPY_THINNING"]))
                elif ctype == "URBAN_EXPANSION":
                    query = query.filter(Hotspot.change_type.in_(["URBAN_EXPANSION", "ENCROACHMENT"]))
                elif ctype == "FIRE":
                    query = query.filter(Hotspot.change_type.in_(["FIRE", "BURN_SCAR"]))
                else:
                    query = query.filter(Hotspot.change_type == ctype)

            if severity and severity.upper() != "ALL":
                query = query.filter(Hotspot.severity.ilike(severity))

            if area_id and area_id.upper() != "ALL":
                query = query.filter(Hotspot.area_id == area_id)

            if min_confidence is not None and min_confidence > 0:
                threshold = min_confidence / 100.0 if min_confidence > 1.0 else min_confidence
                query = query.filter(Hotspot.confidence_score >= threshold)

            if search:
                pattern = f"%{search}%"
                query = query.filter(
                    or_(
                        Hotspot.id.ilike(pattern),
                        Hotspot.area_name.ilike(pattern),
                        Hotspot.location_detail.ilike(pattern),
                        Hotspot.change_type.ilike(pattern),
                    )
                )

            records = query.all()
            if records:
                return [HotspotService._hotspot_to_dto(h) for h in records]
        except Exception:
            pass
        finally:
            if db_session is None:
                session.close()

        # Resilient fallback
        results = list(mock_db.hotspots.values())
        if change_type and change_type.upper() != "ALL":
            ctype = change_type.upper()
            if ctype == "VEGETATION_LOSS":
                results = [h for h in results if h.change_type in ["VEGETATION_LOSS", "DEFORESTATION", "CANOPY_THINNING"]]
            elif ctype == "URBAN_EXPANSION":
                results = [h for h in results if h.change_type in ["URBAN_EXPANSION", "ENCROACHMENT"]]
            elif ctype == "FIRE":
                results = [h for h in results if h.change_type in ["FIRE", "BURN_SCAR"]]
            elif ctype == "WATER_LOSS":
                results = [h for h in results if h.change_type == "WATER_LOSS"]
            else:
                results = [h for h in results if h.change_type == ctype]

        if severity and severity.upper() != "ALL":
            results = [h for h in results if h.severity.upper() == severity.upper()]

        if area_id and area_id.upper() != "ALL":
            results = [h for h in results if h.area_id == area_id]

        if min_confidence is not None and min_confidence > 0:
            threshold = min_confidence / 100.0 if min_confidence > 1.0 else min_confidence
            results = [h for h in results if h.confidence_score >= threshold]

        if search:
            q = search.lower()
            results = [
                h for h in results
                if q in h.id.lower() or q in h.area_name.lower() or q in (h.location_detail or "").lower() or q in h.change_type.lower()
            ]

        return results

    @staticmethod
    def get_hotspot_by_id(
        hotspot_id: str,
        db_session: Optional[Session] = None,
    ) -> Optional[HotspotModel]:
        """Retrieve single hotspot details by ID."""
        session = db_session or SessionLocal()
        try:
            h = session.query(Hotspot).filter(Hotspot.id.ilike(hotspot_id)).first()
            if h:
                return HotspotService._hotspot_to_dto(h)
        except Exception:
            pass
        finally:
            if db_session is None:
                session.close()

        # Resilient fallback
        if hotspot_id in mock_db.hotspots:
            return mock_db.hotspots[hotspot_id]
        for h in mock_db.hotspots.values():
            if h.id.lower() == hotspot_id.lower():
                return h
        return None
