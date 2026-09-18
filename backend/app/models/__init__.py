"""Export all SQLAlchemy domain models and backward-compatible schemas."""
from app.models.user import User
from app.models.area import Area, ProtectedAreaModel, AreaStatisticsModel, AreaTimelineModel
from app.models.observation import SatelliteObservation, LandCoverObservation
from app.models.change_event import ChangeEvent
from app.models.hotspot import Hotspot, HotspotModel, HotspotRelatedAlert
from app.models.alert import Alert, AlertModel
from app.models.wildlife import WildlifeSpecies
from app.models.saved_area import SavedArea
from app.models.report import Report, ReportModel
from app.models.analysis import AnalysisJobModel

__all__ = [
    # 10 Core SQLAlchemy ORM Models with PostGIS Geometries
    "User",
    "Area",
    "SatelliteObservation",
    "LandCoverObservation",
    "ChangeEvent",
    "Hotspot",
    "Alert",
    "WildlifeSpecies",
    "SavedArea",
    "Report",
    # Legacy compatibility schemas
    "ProtectedAreaModel",
    "AreaStatisticsModel",
    "AreaTimelineModel",
    "HotspotModel",
    "HotspotRelatedAlert",
    "AlertModel",
    "ReportModel",
    "AnalysisJobModel",
]
