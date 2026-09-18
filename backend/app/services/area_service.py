from typing import List, Optional
from app.database import db
from app.models.area import ProtectedAreaModel, AreaStatisticsModel, AreaTimelineModel
from app.models.hotspot import HotspotModel


class AreaService:
    @staticmethod
    def get_areas(
        country: Optional[str] = None,
        search: Optional[str] = None,
    ) -> List[ProtectedAreaModel]:
        results = list(db.areas.values())
        if country:
            results = [a for a in results if a.country.lower() == country.lower() or a.country_code.lower() == country.lower()]
        if search:
            q = search.lower()
            results = [a for a in results if q in a.name.lower() or q in a.country.lower() or q in a.biome.lower()]
        return results

    @staticmethod
    def get_area_by_id(area_id: str) -> Optional[ProtectedAreaModel]:
        # Support search by ID or WDPA ID
        if area_id in db.areas:
            return db.areas[area_id]
        for a in db.areas.values():
            if a.wdpa_id.lower() == area_id.lower():
                return a
        return None

    @staticmethod
    def get_area_statistics(area_id: str) -> Optional[AreaStatisticsModel]:
        area = AreaService.get_area_by_id(area_id)
        if not area:
            return None
        return db.statistics.get(area.id)

    @staticmethod
    def get_area_timeline(area_id: str) -> Optional[List[AreaTimelineModel]]:
        area = AreaService.get_area_by_id(area_id)
        if not area:
            return None
        return db.timelines.get(area.id, [])

    @staticmethod
    def get_area_hotspots(area_id: str) -> List[HotspotModel]:
        area = AreaService.get_area_by_id(area_id)
        if not area:
            return []
        return [h for h in db.hotspots.values() if h.area_id == area.id or h.area_name.lower() == area.name.lower()]
