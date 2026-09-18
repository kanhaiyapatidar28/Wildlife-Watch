def test_list_areas(client):
    response = client.get("/api/areas")
    assert response.status_code == 200
    payload = response.json()
    assert payload["success"] is True
    assert isinstance(payload["data"], list)
    assert len(payload["data"]) >= 8
    assert payload["meta"]["total_count"] >= 8

    # Verify structure of first item
    first_area = payload["data"][0]
    assert "id" in first_area
    assert "name" in first_area
    assert "country" in first_area
    assert "total_hectares" in first_area
    assert "coordinates" in first_area


def test_list_areas_filter_by_country(client):
    response = client.get("/api/areas?country=India")
    assert response.status_code == 200
    payload = response.json()
    assert payload["success"] is True
    for area in payload["data"]:
        assert "India" in area["country"]


def test_list_areas_search(client):
    response = client.get("/api/areas?search=Bandhavgarh")
    assert response.status_code == 200
    payload = response.json()
    assert payload["success"] is True
    assert len(payload["data"]) >= 1
    assert "Bandhavgarh" in payload["data"][0]["name"]


def test_get_area_by_id_success(client):
    response = client.get("/api/areas/area-kanha")
    assert response.status_code == 200
    payload = response.json()
    assert payload["success"] is True
    assert payload["data"]["id"] == "area-kanha"
    assert "Kanha" in payload["data"]["name"]
    assert "wdpa_id" in payload["data"]
    assert "biome" in payload["data"]
    assert "forest_cover_percent" in payload["data"]


def test_get_area_by_id_not_found(client):
    response = client.get("/api/areas/non-existent-area-id")
    assert response.status_code == 404
    payload = response.json()
    assert "detail" in payload
    assert "not found" in payload["detail"].lower()


def test_get_area_statistics_success(client):
    response = client.get("/api/areas/area-kanha/statistics")
    assert response.status_code == 200
    payload = response.json()
    assert payload["success"] is True
    data = payload["data"]
    assert data["area_id"] == "area-kanha"
    assert "forest_cover_percent" in data
    assert "water_bodies_ha" in data
    assert "urban_builtup_ha" in data
    assert "habitat_change_score" in data
    assert "land_cover_distribution" in data
    assert isinstance(data["land_cover_distribution"], dict)


def test_get_area_statistics_not_found(client):
    response = client.get("/api/areas/non-existent-area/statistics")
    assert response.status_code == 404


def test_get_area_timeline_success(client):
    response = client.get("/api/areas/area-kanha/timeline")
    assert response.status_code == 200
    payload = response.json()
    assert payload["success"] is True
    data = payload["data"]
    assert data["area_id"] == "area-kanha"
    assert len(data["points"]) > 0
    point = data["points"][0]
    assert "date" in point
    assert "ndvi" in point
    assert "baseline" in point
    assert "fire_incidents" in point


def test_get_area_timeline_not_found(client):
    response = client.get("/api/areas/invalid-id/timeline")
    assert response.status_code == 404


def test_get_area_hotspots_success(client):
    response = client.get("/api/areas/area-kanha/hotspots")
    assert response.status_code == 200
    payload = response.json()
    assert payload["success"] is True
    assert isinstance(payload["data"], list)
    for hs in payload["data"]:
        assert hs["area_id"] == "area-kanha"


def test_get_area_hotspots_not_found(client):
    response = client.get("/api/areas/invalid-id/hotspots")
    assert response.status_code == 404
