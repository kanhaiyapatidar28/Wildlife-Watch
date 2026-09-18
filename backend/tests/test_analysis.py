def test_compute_ndvi_success(client):
    payload = {
        "area_id": "area-kanha",
        "date": "2026-09-15",
    }
    response = client.post("/api/analysis/ndvi", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    res = data["data"]
    assert res["index_name"] == "NDVI"
    assert res["area_id"] == "area-kanha"
    assert "mean" in res
    assert "min" in res
    assert "max" in res
    assert "std" in res
    assert "surface_area_ha" in res


def test_compute_ndwi_success(client):
    payload = {
        "area_id": "area-kanha",
        "date": "2026-09-15",
    }
    response = client.post("/api/analysis/ndwi", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    res = data["data"]
    assert res["index_name"] == "NDWI"
    assert "mean" in res


def test_compute_ndbi_success(client):
    payload = {
        "area_id": "area-kanha",
        "date": "2026-09-15",
    }
    response = client.post("/api/analysis/ndbi", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    res = data["data"]
    assert res["index_name"] == "NDBI"
    assert "mean" in res


def test_compute_index_invalid_area_404(client):
    payload = {
        "area_id": "non-existent-area",
        "date": "2026-09-15",
    }
    response = client.post("/api/analysis/ndvi", json=payload)
    assert response.status_code == 404


def test_change_detection_success(client):
    payload = {
        "area_id": "area-kanha",
        "start_date": "2024-09-01",
        "end_date": "2026-09-01",
        "analysis_type": "vegetation_ndvi",
    }
    response = client.post("/api/analysis/change-detection", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    res = data["data"]
    assert res["area_id"] == "area-kanha"
    assert res["analysis_type"] == "vegetation_ndvi"
    assert "area_affected_ha" in res
    assert "vegetation_loss_ha" in res
    assert "vegetation_gain_ha" in res
    assert "net_change_ha" in res
    assert "percentage_change" in res
    assert "confidence_score" in res
    assert "ndvi_distribution" in res
    assert len(res["ndvi_distribution"]) > 0
    assert "change_distribution" in res
    assert len(res["change_distribution"]) > 0


def test_change_detection_different_types(client):
    types = ["water_ndwi", "builtup_ndbi", "fire_activity", "land_cover"]
    for atype in types:
        payload = {
            "area_id": "area-kanha",
            "start_date": "2024-09-01",
            "end_date": "2026-09-01",
            "analysis_type": atype,
        }
        response = client.post("/api/analysis/change-detection", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert data["data"]["analysis_type"] == atype


def test_change_detection_invalid_area_404(client):
    payload = {
        "area_id": "non-existent-area",
        "start_date": "2024-09-01",
        "end_date": "2026-09-01",
    }
    response = client.post("/api/analysis/change-detection", json=payload)
    assert response.status_code == 404


def test_validation_error_missing_payload(client):
    response = client.post("/api/analysis/change-detection", json={})
    assert response.status_code == 422
    payload = response.json()
    assert payload["status"] == 422
    assert "errors" in payload
