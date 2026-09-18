def test_list_alerts(client):
    response = client.get("/api/alerts")
    assert response.status_code == 200
    payload = response.json()
    assert payload["success"] is True
    assert isinstance(payload["data"], list)
    assert len(payload["data"]) >= 5
    assert payload["meta"]["total_count"] >= 5


def test_list_alerts_filter_severity(client):
    response = client.get("/api/alerts?severity=CRITICAL")
    assert response.status_code == 200
    payload = response.json()
    assert payload["success"] is True
    for alert in payload["data"]:
        assert alert["severity"] == "CRITICAL"


def test_list_alerts_filter_status(client):
    response = client.get("/api/alerts?status=UNREAD")
    assert response.status_code == 200
    payload = response.json()
    assert payload["success"] is True
    for alert in payload["data"]:
        assert alert["status"] == "UNREAD"


def test_list_alerts_filter_area_id(client):
    response = client.get("/api/alerts?area_id=area-kanha")
    assert response.status_code == 200
    payload = response.json()
    assert payload["success"] is True
    for alert in payload["data"]:
        assert alert["area_id"] == "area-kanha"
