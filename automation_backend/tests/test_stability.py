import time


def test_stability_start_and_status(client, base_url):
    # Start job with minimal duration to complete quickly in dry-run
    resp = client.post(f"{base_url}/tests/stability/start", json={"duration_seconds": 1, "note": "quick"})
    assert resp.status_code == 200
    job = resp.json()
    assert "id" in job and job["status"] in {"pending", "running", "completed"}
    job_id = job["id"]

    # Poll for completion with a short timeout budget (dry-run uses tiny sleeps)
    deadline = time.time() + 2.0
    last_status = job["status"]
    while time.time() < deadline:
        r = client.get(f"{base_url}/tests/stability/status", params={"id": job_id})
        assert r.status_code == 200
        ji = r.json()
        last_status = ji["status"]
        if last_status == "completed":
            break
        time.sleep(0.05)

    assert last_status in {"running", "completed"}
