from .areas import router as areas_router
from .hotspots import router as hotspots_router
from .analysis import router as analysis_router
from .alerts import router as alerts_router
from .reports import router as reports_router

__all__ = [
    "areas_router",
    "hotspots_router",
    "analysis_router",
    "alerts_router",
    "reports_router",
]
