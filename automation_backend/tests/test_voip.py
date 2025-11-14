def test_voip_setup_and_teardown(client, base_url):
    # Setup call
    setup_req = {"callee": "1001", "app_path": "/usr/bin/fake-voip"}
    resp = client.post(f"{base_url}/tests/voip/call/setup", json=setup_req)
    assert resp.status_code == 200
    data = resp.json()
    assert data["ok"] is True
    assert "setup" in data["message"].lower()

    # Teardown call
    resp2 = client.post(f"{base_url}/tests/voip/call/teardown")
    assert resp2.status_code == 200
    data2 = resp2.json()
    assert data2["ok"] is True
    assert "teardown" in data2["message"].lower()
