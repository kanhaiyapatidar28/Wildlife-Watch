# Wildlife Watch - REST API Specification (v1)

OpenAPI 3.1 compatible specification for the Wildlife Habitat Monitoring and Change Detection Platform.

- **Base URL:** `https://api.wildlifewatch.org/api/v1` (Production) / `http://localhost:8000/api/v1` (Development)
- **Authentication:** Bearer JWT Token (`Authorization: Bearer <access_token>`)
- **Format:** JSON (`application/json`) & GeoJSON (`application/geo+json`)

---

## Standard Response & Error Formats

### Standard Success Envelope
```json
{
  "success": true,
  "data": {},
  "meta": {
    "timestamp": "2026-09-18T04:15:00Z",
    "request_id": "req_01j7abc123"
  }
}
```

### RFC 7807 Standard Error Problem Details
```json
{
  "type": "https://errors.wildlifewatch.org/validation-error",
  "title": "Invalid Spatial Query Parameters",
  "status": 422,
  "detail": "The bounding box coordinates exceed valid WGS84 range.",
  "instance": "/api/v1/areas/by-bbox",
  "errors": [
    { "field": "bbox", "message": "max_lat must be between -90 and 90." }
  ]
}
```

---

## 1. Authentication & Profile Endpoints

### `POST /auth/register`
Register a new conservation practitioner, ranger, or researcher.
- **Request Body:**
  ```json
  {
    "email": "sarah.connor@kenyawildlife.org",
    "password": "SecurePassword123!",
    "full_name": "Dr. Sarah Connor",
    "organization": "Kenya Wildlife Service",
    "role": "PARK_RANGER"
  }
  ```
- **Response (201 Created):**
  ```json
  {
    "user_id": "7c9e6679-7425-40de-944b-e07fc1f90ae7",
    "email": "sarah.connor@kenyawildlife.org",
    "full_name": "Dr. Sarah Connor",
    "role": "PARK_RANGER",
    "created_at": "2026-09-18T04:15:00Z"
  }
  ```

### `POST /auth/login`
Authenticate user with credentials and receive JWT key pair.
- **Request Body:** `application/x-www-form-urlencoded`
  ```text
  username=sarah.connor@kenyawildlife.org&password=SecurePassword123!
  ```
- **Response (200 OK):**
  ```json
  {
    "access_token": "eyJhbGciOiJSUzI1NiIsIn...",
    "refresh_token": "eyJhbGciOiJSUzI1NiIsIn...",
    "token_type": "bearer",
    "expires_in": 3600
  }
  ```

### `POST /auth/refresh`
Refresh expired access token.
- **Request Body:** `{"refresh_token": "eyJhbGciOiJSUzI1NiIsIn..."}`
- **Response (200 OK):** New access token and refresh token.

### `GET /auth/me`
Retrieve currently authenticated user profile and permissions.
- **Headers:** `Authorization: Bearer <token>`
- **Response (200 OK):** User entity with organization and subscribed alert counters.

---

## 2. Location Search & Protected Areas

### `GET /search/places`
Search globally for parks, reserves, biomes, or coordinates (uses Nominatim + PostGIS WDPA cache).
- **Query Parameters:**
  - `q` (string, required): e.g. `"Serengeti"` or `"Kaziranga"`
  - `limit` (integer, default: 10)
  - `country` (string, optional ISO 3166-1 alpha-2, e.g. `"TZ"`)
- **Response (200 OK):**
  ```json
  {
    "results": [
      {
        "id": "wdpa_1234",
        "name": "Serengeti National Park",
        "category": "National Park",
        "iucn_category": "II",
        "country": "Tanzania",
        "area_km2": 14763.0,
        "centroid": { "lat": -2.333, "lon": 34.833 },
        "bbox": [34.0, -3.5, 35.5, -1.5]
      }
    ]
  }
  ```

### `GET /areas/protected`
List official protected areas with optional spatial or attribute filters.
- **Query Parameters:**
  - `iucn_category` (string, optional: `Ia`, `Ib`, `II`, `IV`)
  - `country_code` (string, optional)
  - `page` (int, default: 1), `limit` (int, default: 20)
- **Response (200 OK):** Paginated collection of protected areas.

### `GET /areas/{id}`
Get full boundary geometry, area stats, and habitat overview for a protected area.
- **Response (200 OK):** GeoJSON Feature with properties (WDPA ID, biome, total area in hectares, baseline forest cover).

### `GET /areas/{id}/boundary.geojson`
Optimized vector boundary in standard GeoJSON for Mapbox rendering.

---

## 3. Saved & Monitored Areas (User Portfolios)

### `POST /saved-areas`
Add an existing protected reserve or custom drawn polygon to user's active monitoring list.
- **Request Body:**
  ```json
  {
    "area_id": "wdpa_1234",
    "custom_name": "Serengeti Northern Corridor Sector 4",
    "custom_geom": null,
    "alert_enabled": true,
    "alert_threshold_ndvi": -0.25,
    "fire_alerts_enabled": true
  }
  ```
- **Response (201 Created):** Created SavedArea record with assigned UUID.

### `GET /saved-areas`
List all areas monitored by the logged-in user with current risk status badges.

### `DELETE /saved-areas/{id}`
Remove an area from continuous monitoring.

---

## 4. Satellite Imagery & Spectral Indices Endpoints

### `GET /satellite/scenes`
Query available Sentinel-2 or Landsat scenes covering an Area of Interest (AOI).
- **Query Parameters:**
  - `area_id` (UUID, optional) or `bbox` (min_lon, min_lat, max_lon, max_lat)
  - `start_date` (ISO date, e.g. `2026-06-01`)
  - `end_date` (ISO date, e.g. `2026-09-01`)
  - `satellite` (`sentinel-2` | `landsat-8` | `landsat-9`, default: `sentinel-2`)
  - `max_cloud_cover` (integer percentage, e.g. `20`)
- **Response (200 OK):** List of candidate scenes with acquisition timestamp, cloud percentage, tile identifiers, and preview thumbnail URLs.

### `GET /satellite/tiles/{z}/{x}/{y}`
Dynamic raster tile server delivering on-the-fly rendered indices directly into Mapbox GL JS raster layers.
- **Path Parameters:** `z`, `x`, `y` (Slippy map tile coordinates)
- **Query Parameters:**
  - `scene_id` (string, required) or `composite_id`
  - `index` (string, enum: `true_color`, `ndvi`, `ndwi`, `ndbi`, `false_color`)
  - `colormap` (string, optional: `viridis`, `rdylgn`, `blues`, `magma`)
  - `format` (string: `webp` | `png`, default: `webp`)
- **Response (200 OK):** Binary image stream (`image/webp` or `image/png`).

### `POST /satellite/indices/calculate`
Calculate spatial statistics for NDVI / NDWI / NDBI over an arbitrary polygon.
- **Request Body:**
  ```json
  {
    "geometry": {
      "type": "Polygon",
      "coordinates": [[[34.8, -2.3], [34.9, -2.3], [34.9, -2.4], [34.8, -2.4], [34.8, -2.3]]]
    },
    "date_range": { "start": "2026-08-01", "end": "2026-08-31" },
    "satellite": "sentinel-2",
    "indices": ["ndvi", "ndwi", "ndbi"]
  }
  ```
- **Response (200 OK):**
  ```json
  {
    "ndvi": { "mean": 0.68, "median": 0.71, "min": 0.12, "max": 0.89, "std": 0.08 },
    "ndwi": { "mean": -0.35, "median": -0.38, "min": -0.65, "max": 0.78, "water_surface_ha": 142.5 },
    "ndbi": { "mean": -0.22, "median": -0.24, "min": -0.55, "max": 0.15, "builtup_surface_ha": 3.1 }
  }
  ```

---

## 5. Change Detection & Dual-Epoch Comparison

### `POST /change-detection/analyze`
Trigger an asynchronous multi-spectral change detection analysis comparing Epoch 1 (Baseline) vs Epoch 2 (Target).
- **Request Body:**
  ```json
  {
    "area_id": "wdpa_1234",
    "epoch_baseline": {
      "start": "2025-08-01",
      "end": "2025-08-31",
      "max_cloud_cover": 15
    },
    "epoch_target": {
      "start": "2026-08-01",
      "end": "2026-08-31",
      "max_cloud_cover": 15
    },
    "sensitivity_threshold": 0.20,
    "min_cluster_size_ha": 0.1,
    "apply_seasonal_correction": true
  }
  ```
- **Response (202 Accepted):**
  ```json
  {
    "job_id": "job_cd_8f93e110",
    "status": "QUEUED",
    "created_at": "2026-09-18T04:18:00Z",
    "poll_url": "/api/v1/change-detection/jobs/job_cd_8f93e110"
  }
  ```

### `GET /change-detection/jobs/{job_id}`
Poll execution status of a change detection worker task.
- **Response (200 OK):**
  ```json
  {
    "job_id": "job_cd_8f93e110",
    "status": "COMPLETED",
    "progress_percent": 100,
    "execution_time_seconds": 18.4,
    "result_summary": {
      "total_area_analyzed_ha": 14200.0,
      "total_degradation_ha": 84.3,
      "total_gain_ha": 12.1,
      "hotspots_detected": 14,
      "critical_hotspots": 3
    }
  }
  ```

### `GET /change-detection/hotspots`
Fetch discrete vectorized change polygons detected across monitored areas.
- **Query Parameters:**
  - `area_id` (UUID, optional)
  - `severity` (`CRITICAL` | `HIGH` | `MEDIUM` | `LOW`)
  - `min_confidence` (float, e.g. `0.70`)
  - `change_type` (`DEFORESTATION` | `WATER_LOSS` | `ENCROACHMENT` | `BURN_SCAR`)
- **Response (200 OK):** GeoJSON FeatureCollection with polygon geometries and properties:
  - `delta_ndvi`
  - `area_ha`
  - `severity`
  - `confidence_score`
  - `first_detected`

---

## 6. Fire & Thermal Hotspots (NASA FIRMS)

### `GET /fires/active`
Retrieve near-real-time active thermal detections (last 24 to 72 hours).
- **Query Parameters:**
  - `bbox` or `area_id`
  - `hours_ago` (integer: `24`, `48`, `72`, default: `24`)
  - `min_confidence` (integer: `0` to `100`, default: `50`)
- **Response (200 OK):** GeoJSON FeatureCollection of Point geometries with brightness temperature (Kelvin), Fire Radiative Power (MW), satellite source (`VIIRS_NOAA20`, `MODIS`), and detection timestamp.

### `GET /fires/historical-summary`
Aggregated fire frequency and burn recurrence matrix per reserve.

---

## 7. Wildlife & Biodiversity Overlay

### `GET /wildlife/species`
Lookup species profile and IUCN conservation status.
- **Query Parameters:**
  - `search` (common name or scientific name)
  - `iucn_status` (`CR`, `EN`, `VU`, `NT`, `LC`)
- **Response (200 OK):** List of wildlife species with taxonomy, IUCN status, and habitat vulnerability descriptors.

### `GET /wildlife/occurrences/{area_id}`
Fetch recent GBIF-verified sightings and GPS telemetry coordinates within a given habitat boundary.
- **Response (200 OK):** GeoJSON Point FeatureCollection with species details, observation date, and threat impact radius.

---

## 8. Human Activity & Infrastructure Encroachment

### `GET /human-activity/{area_id}`
Extract human encroachment markers within and bordering the reserve from OpenStreetMap.
- **Returns:**
  - `road_network`: GeoJSON LineStrings of primary, secondary, and logging tracks.
  - `road_density_km_per_km2`: Quantitative habitat fragmentation index.
  - `settlement_clusters`: GeoJSON MultiPolygons of agricultural conversion and building clusters.

---

## 9. Timeline & Trends Analytics

### `GET /analytics/timeline`
Retrieve longitudinal multi-year phenology metrics.
- **Query Parameters:**
  - `area_id` (UUID, required)
  - `index` (`ndvi` | `ndwi` | `ndbi`)
  - `interval` (`monthly` | `quarterly` | `yearly`)
  - `from_year` (e.g. `2018`), `to_year` (e.g. `2026`)
- **Response (200 OK):**
  ```json
  {
    "area_id": "wdpa_1234",
    "series": [
      { "date": "2024-01-01", "mean_index": 0.72, "std_dev": 0.05, "anomaly_score": 0.01 },
      { "date": "2024-02-01", "mean_index": 0.69, "std_dev": 0.06, "anomaly_score": -0.04 }
    ]
  }
  ```

---

## 10. Alerts & Incident Notification

### `GET /alerts`
Query triggered alerts for the logged-in user's assigned/saved habitats.
- **Query Parameters:**
  - `status` (`UNREAD` | `ACKNOWLEDGED` | `DISMISSED`)
  - `severity` (`CRITICAL`, `HIGH`, etc.)
  - `limit`, `offset`
- **Response (200 OK):** Paginated alert cards with direct link to spatial coordinates and change event ID.

### `PATCH /alerts/{id}`
Update alert state (mark read, acknowledge, assign field team).
- **Request Body:** `{"status": "ACKNOWLEDGED", "notes": "Patrol dispatched to Sector 3."}`

---

## 11. Reports & Audit Exports

### `POST /reports/generate`
Request generation of an official conservation audit report.
- **Request Body:**
  ```json
  {
    "area_id": "wdpa_1234",
    "report_title": "Q3 2026 Habitat Integrity & Deforestation Audit",
    "format": "GEOPDF",
    "date_range": { "start": "2026-06-01", "end": "2026-09-01" },
    "include_satellite_maps": true,
    "include_species_impact": true,
    "include_fire_events": true
  }
  ```
- **Response (202 Accepted):** Returns `report_id` and download URL once generated.

### `GET /reports/{id}/download`
Stream generated GeoPDF, GeoPackage, or CSV report file.

---

## 12. Settings & Alert Configuration

### `GET /settings/alerts`
Retrieve user-level and organization-level alert thresholds and dispatch webhooks.

### `PUT /settings/alerts`
Update alert thresholds (e.g., trigger email when critical change exceeds 1.0 ha).
