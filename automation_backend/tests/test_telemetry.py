def test_telemetry_ingest_and_last_and_metrics(client, base_url):
    items = [
        {"metric": "cpu", "value": 0.5, "tags": {"host": "nuc"}},
        {"metric": "mem", "value": 0.7, "tags": {"host": "nuc"}},
        {"metric": "cpu", "value": 0.6, "tags": {"host": "rpi"}},
    ]
    resp = client.post(f"{base_url}/telemetry/ingest", json={"items": items})
    assert resp.status_code == 200
    count = resp.json()
    assert count == len(items)

    # Get last 2
    resp2 = client.get(f"{base_url}/telemetry/last", params={"n": 2})
    assert resp2.status_code == 200
    last_items = resp2.json()
    assert len(last_items) == 2
    assert all("metric" in it and "value" in it for it in last_items)

    # Metrics list should include unique metric names
    resp3 = client.get(f"{base_url}/telemetry/metrics")
    assert resp3.status_code == 200
    metrics = resp3.json()
    assert "cpu" in metrics and "mem" in metrics
