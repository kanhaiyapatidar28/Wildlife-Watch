# Project Memory

## Project Overview
"Wildlife Watch" is a production-quality wildlife habitat monitoring and change detection platform built with Next.js, TypeScript, Tailwind CSS, and Lucide icons. The platform empowers conservation rangers, ecological scientists, and park directors to monitor protected area integrity, track habitat degradation, detect deforestation/encroachment hotspots, analyze multi-spectral vegetation indices (NDVI, NDWI, NDBI), and inspect incidents with high-precision satellite telemetry.

## Current Architecture
- **Frontend Framework**: Next.js 14 (App Router) with React 18 & TypeScript
- **Frontend Styling**: Tailwind CSS with dark GIS intelligence theme, glassmorphic HUD cards, subtle emerald/cyan/amber environmental accents
- **Visualization & Charts**: Recharts with SSR client mount guards
- **Map System**: Mapbox GL JS with high-fidelity simulated multi-spectral raster backdrops and vector GIS fallback layers
- **State Management & Mock Data**: Geospatial mock registry covering 8 global and Indian protected reserves (Kanha, Bandhavgarh, Satpura, Kaziranga, Serengeti, Yasuní, Mamirauá, Virunga)
- **Backend Framework**: FastAPI with Python 3.12, Uvicorn ASGI, and Pydantic v2 schemas
- **Backend Architecture**: Layered modular structure: `routers/` (REST endpoints), `services/` (business logic), `models/` (domain entities), `schemas/` (Pydantic validation & OpenAPI serialization), `geospatial/` (WGS84 distance & spherical polygon geometry), `satellite/` (spectral indices NDVI, NDWI, NDBI & synthetic reflectance), `analysis/` (bi-temporal change detection & phenology baseline normalization), and `ml/` (spatial clustering & isolation forest anomaly scoring).
- **API Features**: RFC 7807 problem details error handling, request timing & audit logging middleware, CORS origin validation for Next.js frontend, and OpenAPI documentation (/docs, /redoc).

## Important Decisions
- **Scientific Causation Standard**: The platform strictly avoids asserting unsupported causation for detected anomalies. It uses "Potential Contributing Factors" accompanied by explicit remote sensing intelligence disclaimers indicating that spatial correlations require ground-truth ranger patrol verification.
- **Recharts In Next.js App Router**: Avoid wrapping individual Recharts subcomponents in `next/dynamic`. Direct imports from `'recharts'` guarded with an `isMounted` state guarantee zero hydration mismatches.
- **Build Isolation**: Always terminate long-running Next.js production server tasks before executing `npm run build` to prevent Windows file lock conflicts on `.next`.
- **Backend Mock Services**: In accordance with system instructions, real Google Earth Engine credentials are not connected yet. High-fidelity synthetic surface reflectance and change detection engines generate deterministic, realistic telemetry matching Sentinel-2 Level-2A BOA and Landsat-9 bands.

## Current State
- **Pages Implemented**:
  - `/dashboard`: KPI cards, satellite map, layer toggles, alerts, NDVI trend chart, land cover chart.
  - `/explore`: Professional GIS workspace with 11 layers, before/after slider, hotspot popups, location search.
  - `/areas`: Reserve directory with biome and risk metrics.
  - `/areas/[id]`: Habitat profile with Overview, Analysis, Hotspots, Wildlife species cards, and Human Activity metrics.
  - `/change-analysis`: Dual-epoch temporal comparison with Left (Baseline), Right (Target), Bottom (Diverging Change Map with Gain, Stable, Loss), 5 core statistics, 2 distribution charts, and methodology panel.
  - `/hotspots`: Dual-pane monitoring interface with top multi-dimensional filters (Change Type, Severity, Date, Area, Confidence), Left (Hotspot Table), Right (Interactive Map with synced zoom and popup), and Slide-out Hotspot Detail Drawer with "potential contributing factors".
- **Backend Implemented**:
  - Full FastAPI REST API covering 13 core endpoints + health checks
  - In-memory geospatial database seeded with 8 protected areas, hotspots, alerts, and reports
  - Comprehensive 40-test automated test suite with 100% pass rate.

## Known Issues
- Real Copernicus Sentinel-2 / Landsat API integration pending; high-fidelity mock geospatial data is currently utilized.

## Pending Work
- Timeline & Trends page (`/timeline`)
- Reports generation & export page (`/reports`)
- Incident Alerts management page (`/alerts`)
- User Profile (`/profile`) and Platform Settings (`/settings`)

## Interaction History

### 2026-09-18 15:40

**User Request**
> Implement the Hotspots page. Create a professional monitoring interface with top filters (Change Type, Severity, Date, Area, Confidence), main split layout (LEFT: Hotspot table, RIGHT: Interactive map), table columns, row click interactions (zoom map, open popup, show detailed information), and Hotspot detail drawer with "potential contributing factors" rather than asserting causation.

**Exploration**
- Inspected `frontend/src/types/index.ts`, `frontend/src/lib/mock-data.ts`, and previous prototypes.
- Identified need for extended `ChangeEventHotspot` properties (`location_detail`, `previous_condition`, `current_condition`, `potential_contributing_factors`, `related_alerts`).
- Designed modular architecture under `frontend/src/components/hotspots/`.

**Work Done**
- Updated `frontend/src/types/index.ts` to support all requested change types and detail drawer fields.
- Enriched `MOCK_HOTSPOTS` in `frontend/src/lib/mock-data.ts` with complete data for Indian and global reserves.
- Created `frontend/src/components/hotspots/HotspotFilters.tsx` with multidimensional filtering.
- Created `frontend/src/components/hotspots/HotspotTable.tsx` with sortable columns and active selection.
- Created `frontend/src/components/hotspots/HotspotMapPane.tsx` with synced zoom, severity pins, and interactive popup.
- Created `frontend/src/components/hotspots/HotspotDetailDrawer.tsx` adhering to the causation standard with "potential contributing factors", condition comparisons, and dispatch action.
- Assembled the full interface in `frontend/src/app/hotspots/page.tsx`.
- Verified build (`npm run build` exited with code 0).
- Verified in browser with `chrome-devtools-mcp` and captured screenshots.

**Files Changed**
- `frontend/src/types/index.ts`
  - Added HotspotRelatedAlert, extended ChangeType and ChangeEventHotspot with drawer fields.
- `frontend/src/lib/mock-data.ts`
  - Enriched MOCK_HOTSPOTS with realistic coordinates, condition baselines, contributing indicators, and alerts.
- `frontend/src/components/hotspots/HotspotFilters.tsx`
  - New component for multidimensional filtering.
- `frontend/src/components/hotspots/HotspotTable.tsx`
  - New component for the high-density incident registry table.
- `frontend/src/components/hotspots/HotspotMapPane.tsx`
  - New component for the synchronized right-hand map viewport and popups.
- `frontend/src/components/hotspots/HotspotDetailDrawer.tsx`
  - New component for the detailed inspection drawer.
- `frontend/src/app/hotspots/page.tsx`
  - Assembled the complete Hotspots monitoring interface.
- `memory.md`
  - Initialized persistent project memory.

**Verification**
- `npm run build`: Succeeded with code 0 (17/17 pages generated cleanly).
- Browser UI verification: Filter switching, row selection, map zoom, popup opening, and detail drawer rendering verified via Chrome DevTools.

**Response**
- Summary of the implemented Hotspots monitoring workspace, filter controls, dual-pane architecture, detail drawer, and causation standard compliance.

**Git**
- Branch: N/A (User opted to pause git status command: "wait for next input")
- Commit: Deferred
- Push: Deferred

**Notes**
- Next recommended implementation: Timeline & Trends (`/timeline`) or Incident Alerts (`/alerts`).

### 2026-09-18 16:10

**User Request**
> what is done tiil now

**Exploration**
- Audited the entire codebase to summarize all implemented pages, components, GIS features, charts, and data models.

**Work Done**
- Formulated a comprehensive summary of completed architecture, pages, and interactive features.

**Files Changed**
- `memory.md`
  - Updated persistent interaction record.

**Verification**
- Verified all 17 routes compiled cleanly and verified Next.js server readiness.

**Response**
- Complete status breakdown of the Wildlife Watch platform delivered to the user.

**Git**
- Branch: N/A
- Commit: Deferred
- Push: Deferred

**Notes**
- Pending pages ready for implementation: Timeline & Trends (`/timeline`), Reports (`/reports`), Incident Alerts (`/alerts`), User Profile (`/profile`), and Settings (`/settings`).

### 2026-09-18 16:35

**User Request**
> Now implement the backend. Create `backend/app/` structure (`main.py`, `config.py`, `database.py`, `models/`, `schemas/`, `routers/`, `services/`, `geospatial/`, `satellite/`, `analysis/`, `ml/`). Use FastAPI. Create REST endpoints: `GET /api/areas`, `GET /api/areas/{id}`, `GET /api/areas/{id}/statistics`, `GET /api/areas/{id}/timeline`, `GET /api/areas/{id}/hotspots`, `GET /api/hotspots`, `GET /api/hotspots/{id}`, `POST /api/analysis/ndvi`, `POST /api/analysis/ndwi`, `POST /api/analysis/ndbi`, `POST /api/analysis/change-detection`, `GET /api/alerts`, `GET /api/reports`. Use Pydantic schemas. Add CORS, environment variables, logging, error handling, API documentation. Do not connect Earth Engine yet. Create mock service implementations so frontend can consume real API endpoints. Write tests for the main endpoints.

**Exploration**
- Verified Python 3.12 environment and installed `pytest` & `pydantic-settings`.
- Established modular backend architecture adhering precisely to the requested directory tree.
- Designed Pydantic v2 schemas (`app/schemas/`) with strict validation, response wrappers (`StandardResponse[T]`), and RFC 7807 problem details.
- Implemented high-fidelity mock services delivering deterministic reflectance, bi-temporal change detection, and spatial clustering without needing live Earth Engine credentials.

**Work Done**
- Implemented core infrastructure:
  - `backend/app/config.py`: Application settings, environment loading, CORS origins parser.
  - `backend/app/database.py`: In-memory spatial database seeded with 8 reserves (Kanha, Bandhavgarh, Satpura, Kaziranga, Serengeti, Yasuní, Mamirauá, Virunga), hotspots, alerts, and reports.
  - `backend/app/models/`: Internal domain entities (`area.py`, `hotspot.py`, `alert.py`, `report.py`, `analysis.py`).
  - `backend/app/schemas/`: Pydantic v2 API schemas (`common.py`, `area.py`, `hotspot.py`, `alert.py`, `report.py`, `analysis.py`).
  - `backend/app/geospatial/`: WGS84 coordinates validation, Haversine distance, and spherical polygon area computation (`coordinates.py`, `geometry.py`).
  - `backend/app/satellite/`: Mathematical spectral index formulas (NDVI, NDWI, NDBI) and synthetic surface reflectance simulator (`indices.py`, `mock_scenes.py`).
  - `backend/app/analysis/`: Bi-temporal change detection and phenology baseline normalization (`change_detector.py`, `phenology.py`).
  - `backend/app/ml/`: Spatial density clustering and isolation forest anomaly detection (`clustering.py`, `isolation_forest.py`).
  - `backend/app/services/`: Business logic services (`area_service.py`, `hotspot_service.py`, `analysis_service.py`, `alert_service.py`, `report_service.py`).
  - `backend/app/routers/`: 5 modular routers implementing all 13 requested REST endpoints (`areas.py`, `hotspots.py`, `analysis.py`, `alerts.py`, `reports.py`).
  - `backend/app/main.py`: FastAPI app entrypoint with CORS middleware, request timing & audit logging middleware, RFC 7807 problem details error handlers, health check endpoints, and OpenAPI docs.
- Created comprehensive test suite under `backend/tests/`:
  - `conftest.py`, `test_main.py`, `test_areas.py`, `test_hotspots.py`, `test_analysis.py`, `test_alerts.py`, `test_reports.py`, and `test_geospatial.py`.
- Created root `.gitignore` protecting secrets, virtualenvs, cache files, and Next.js artifacts.

**Files Changed**
- `backend/requirements.txt`: Python package requirements.
- `backend/.env.example`: Template environment variables.
- `backend/app/config.py`: BaseSettings configuration.
- `backend/app/database.py`: Seeded spatial database.
- `backend/app/main.py`: FastAPI application entrypoint.
- `backend/app/models/`: Domain entities.
- `backend/app/schemas/`: Pydantic request & response schemas.
- `backend/app/geospatial/`: Geospatial calculations.
- `backend/app/satellite/`: Multi-spectral indices.
- `backend/app/analysis/`: Change detection engine.
- `backend/app/ml/`: Machine learning anomaly scoring and clustering.
- `backend/app/services/`: Service layer implementations.
- `backend/app/routers/`: REST API route controllers.
- `backend/tests/`: 40-test pytest suite.
- `.gitignore`: Root Git ignore configuration.
- `memory.md`: Updated persistent memory.

**Verification**
- `pytest tests/ -v`: 40 tests executed, 40 passed (100% pass rate in 0.35s).
- OpenAPI documentation verification: 15 endpoints verified in schema.
- Health check: `GET /health` verified responding `{"status": "HEALTHY", "database": "IN_MEMORY_SEEDED"}`.

**Git**
- Branch: master
- Commit: successful (`697a6cf`) - feat: implement FastAPI backend with geospatial telemetry, analysis endpoints, and 40-test suite
- Push: failed
- Reason: No remote repository configured (`origin` does not exist; repository was initialized locally)

**Notes**
- All 13 endpoints are tested and ready for Next.js frontend consumption.
- Next recommended step: Connect Next.js frontend services/hooks to consume the FastAPI endpoints instead of local mock arrays.

### 2026-09-18 16:45

**User Request**
> open website

**Exploration**
- Checked status of background tasks and local network ports.
- Verified presence of Next.js production build and executed `npm run build` cleanly (17/17 routes compiled).
- Started Next.js production server on `http://localhost:3000`.
- Verified FastAPI backend running on `http://127.0.0.1:8000`.

**Work Done**
- Started Next.js frontend server (`npm run start`) on port 3000.
- Connected Chrome browser via `chrome-devtools-mcp` to `http://localhost:3000/dashboard`.
- Captured viewport visual screenshot of the operational Wildlife Watch GIS dashboard.

**Files Changed**
- `memory.md`
  - Recorded interaction and system status.

**Verification**
- Frontend: `http://localhost:3000/dashboard` loaded successfully with 200 OK.
- Backend: `http://127.0.0.1:8000/health` verified operational.
- Visual inspection: Captured and verified high-resolution screenshot displaying KPI telemetry cards, top navigation bar, protected area selector, and Mapbox geospatial canvas.

**Git**
- Branch: master
- Commit: Pending (staged and committed below)
- Push: failed (No remote repository configured)

**Notes**
- Both frontend and backend services are actively running in background daemon processes.


