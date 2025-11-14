def test_streaming_check(client, base_url):
    req = {"url": "https://example.com/stream.m3u8"}
    resp = client.post(f"{base_url}/tests/streaming/check", json=req)
    assert resp.status_code == 200
    data = resp.json()
    assert data["url"].endswith("m3u8")
    assert data["reachable"] is True  # dry-run returns True
    assert data["details"]["dry_run"] is True
