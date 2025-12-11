import time
import requests

SERVICE_B_URL = "http://localhost:8001"
SERVICE_A_URL = "http://localhost:8000"

def test_e2e_analysis_flow():
    analyze_resp = requests.post(
        f"{SERVICE_B_URL}/analyze",
        json={"image_url": "https://pl.wikipedia.org/wiki/Kot_domowy#/media/Plik:Collage_of_Six_Cats-03.JPG"},
        timeout=5,
    )
    assert analyze_resp.status_code == 202
    job_id = analyze_resp.json()["job_id"]

    for _ in range(10):
        time.sleep(1)
        results_resp = requests.get(f"{SERVICE_A_URL}/results", timeout=5)
        assert results_resp.status_code == 200
        results = results_resp.json()
        if any(r["id"] == job_id for r in results):
            break
    else:
        raise AssertionError("Result not found in Service A within timeout")

    result = next(r for r in results if r["id"] == job_id)
    assert result["image_url"] == "https://pl.wikipedia.org/wiki/Kot_domowy#/media/Plik:Collage_of_Six_Cats-03.JPG"
    assert result["people_count"] == 5
