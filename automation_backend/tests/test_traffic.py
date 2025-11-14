def test_traffic_upload_and_retrieve_result(client, base_url):
    # Trigger upload
    req = {"bytes": 1024, "duration_seconds": 1}
    resp = client.post(f"{base_url}/tests/traffic/upload", json=req)
    assert resp.status_code == 200
    result = resp.json()
    assert result["success"] is True
    assert result["direction"] == "upload"
    assert result["throughput_mbps"] >= 100.0  # dry-run uses 100.0
    test_id = result["id"]

    # Retrieve by id
    resp2 = client.get(f"{base_url}/tests/{test_id}/result")
    assert resp2.status_code == 200
    result2 = resp2.json()
    assert result2["id"] == test_id
    assert result2["direction"] == "upload"


def test_traffic_download(client, base_url):
    req = {"bytes": 2048}
    resp = client.post(f"{base_url}/tests/traffic/download", json=req)
    assert resp.status_code == 200
    data = resp.json()
    assert data["direction"] == "download"
    assert data["success"] is True
    assert data["details"]["dry_run"] is True
