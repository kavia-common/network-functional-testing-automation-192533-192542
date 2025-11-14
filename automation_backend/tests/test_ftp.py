def test_ftp_keepalive(client, base_url):
    req = {"host": "ftp.example.com", "username": "user", "password": "pass", "interval_seconds": 1}
    resp = client.post(f"{base_url}/tests/ftp/keepalive", json=req)
    assert resp.status_code == 200
    data = resp.json()
    assert data["ok"] is True
    assert "keepalive" in data["message"].lower()
