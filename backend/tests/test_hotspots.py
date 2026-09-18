def test_list_hotspots(client):
    response = client.get("/api/hotspots")
    assert response.status_code == 200
    payload = response.json()
    assert payload["success"] is True
    assert isinstance(payload["data"], list)
    assert len(payload["data"]) >= 5
    assert payload["meta"]["total_count"] >= 5


def test_list_hotspots_filter_change_type(client):
    response = client.get("/api/hotspots?change_type=VEGETATION_LOSS")
    assert response.status_code == 200
    payload = response.json()
    assert payload["success"] is True
    for hs in payload["data"]:
        assert hs["change_type"] == "VEGETATION_LOSS"


def test_list_hotspots_filter_severity(client):
    response = client.get("/api/hotspots?severity=CRITICAL")
    assert response.status_code == 200
    payload = response.json()
    assert payload["success"] is True
    for hs in payload["data"]:
        assert hs["severity"] == "CRITICAL"


def test_list_hotspots_filter_min_confidence(client):
    response = client.get("/api/hotspots?min_confidence=0.90")
    assert response.status_code == 200
    payload = response.json()
    assert payload["success"] is True
    for hs in payload["data"]:
        assert hs["confidence_score"] >= 0.90


def test_list_hotspots_filter_area_id(client):
    response = client.get("/api/hotspots?area_id=area-kanha")
    assert response.status_code == 200
    payload = response.json()
    assert payload["success"] is True
    for hs in payload["data"]:
        assert hs["area_id"] == "area-kanha"


def test_get_hotspot_detail_success(client):
    response = client.get("/api/hotspots/HS-KANHA-01")
    assert response.status_code == 200
    payload = response.json()
    assert payload["success"] is True
    data = payload["data"]
    assert data["id"] == "HS-KANHA-01"
    assert data["area_id"] == "area-kanha"
    assert "coordinates" in data
    assert "lat" in data["coordinates"] and "lon" in data["coordinates"]
    assert "potential_contributing_factors" in data
    assert isinstance(data["potential_contributing_factors"], list)
    assert len(data["potential_contributing_factors"]) > 0
    assert "previous_condition" in data
    assert "current_condition" in data


def test_get_hotspot_detail_not_found(client):
    response = client.get("/api/hotspots/HS-NON-EXISTENT")
    assert response.status_code == 404
    payload = response.json()
    assert "detail" in payload
    assert "not found" in payload["detail"].lower()
