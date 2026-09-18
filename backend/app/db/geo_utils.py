"""Geospatial helper utilities for converting between PostGIS geometries and GeoJSON."""
from typing import Dict, Any, Optional
import shapely.wkb
import shapely.geometry
from geoalchemy2.elements import WKBElement, WKTElement


def geometry_to_geojson(geom: Any) -> Optional[Dict[str, Any]]:
    """Converts a GeoAlchemy2 geometry or Shapely geometry to a GeoJSON dictionary."""
    if geom is None:
        return None
    try:
        if isinstance(geom, WKBElement):
            shapely_obj = shapely.wkb.loads(bytes(geom.data))
            return shapely.geometry.mapping(shapely_obj)
        elif isinstance(geom, WKTElement):
            shapely_obj = shapely.wkt.loads(str(geom.data))
            return shapely.geometry.mapping(shapely_obj)
        elif hasattr(geom, "__geo_interface__"):
            return geom.__geo_interface__
    except Exception:
        pass
    return None


def point_to_lat_lon(point_geom: Any, fallback_lat: float = 0.0, fallback_lon: float = 0.0) -> Dict[str, float]:
    """Extracts latitude and longitude from a Point geometry."""
    if point_geom is None:
        return {"lat": fallback_lat, "lon": fallback_lon}
    try:
        if isinstance(point_geom, WKBElement):
            shapely_pt = shapely.wkb.loads(bytes(point_geom.data))
            return {"lat": shapely_pt.y, "lon": shapely_pt.x}
        elif isinstance(point_geom, WKTElement):
            shapely_pt = shapely.wkt.loads(str(point_geom.data))
            return {"lat": shapely_pt.y, "lon": shapely_pt.x}
    except Exception:
        pass
    return {"lat": fallback_lat, "lon": fallback_lon}
