def test_list_reports(client):
    response = client.get("/api/reports")
    assert response.status_code == 200
    payload = response.json()
    assert payload["success"] is True
    assert isinstance(payload["data"], list)
    assert len(payload["data"]) >= 3
    assert payload["meta"]["total_count"] >= 3

    first_report = payload["data"][0]
    assert "id" in first_report
    assert "title" in first_report
    assert "area_name" in first_report
    assert "status" in first_report
    assert "download_url" in first_report


def test_list_reports_filter_status(client):
    response = client.get("/api/reports?status=READY")
    assert response.status_code == 200
    payload = response.json()
    assert payload["success"] is True
    for report in payload["data"]:
        assert report["status"] == "READY"


def test_list_reports_filter_area_id(client):
    response = client.get("/api/reports?area_id=area-kanha")
    assert response.status_code == 200
    payload = response.json()
    assert payload["success"] is True
    for report in payload["data"]:
        assert report["area_id"] == "area-kanha"
