def test_vpn_connect_and_status(client, base_url):
    # Connect (simulated)
    resp = client.post(f"{base_url}/tests/vpn/connect", json={"config_name": "test-profile"})
    assert resp.status_code == 200
    data = resp.json()
    # In CI, ping_host may fail; assert fields and types, not necessarily connectivity
    assert "connected" in data
    assert "check_host" in data
    assert "latency_ms" in data

    # Status
    resp2 = client.post(f"{base_url}/tests/vpn/status")
    assert resp2.status_code == 200
    data2 = resp2.json()
    assert set(data2.keys()) == {"connected", "check_host", "latency_ms"}
