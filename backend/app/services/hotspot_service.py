from typing import List, Optional
from app.database import db
from app.models.hotspot import HotspotModel


class HotspotService:
    @staticmethod
    def get_hotspots(
        change_type: Optional[str] = None,
        severity: Optional[str] = None,
        area_id: Optional[str] = None,
        min_confidence: Optional[float] = None,
        search: Optional[str] = None,
    ) -> List[HotspotModel]:
        results = list(db.hotspots.values())

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
            # Handle both 0.70 and 70 formats
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
    def get_hotspot_by_id(hotspot_id: str) -> Optional[HotspotModel]:
        if hotspot_id in db.hotspots:
            return db.hotspots[hotspot_id]
        for h in db.hotspots.values():
            if h.id.lower() == hotspot_id.lower():
                return h
        return None
