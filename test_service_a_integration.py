import sys
import pathlib

from fastapi.testclient import TestClient

ROOT = pathlib.Path(__file__).resolve().parents[1]
SERVICE_A_PATH = ROOT / "service_a"
sys.path.append(str(SERVICE_A_PATH))

from app.main import app, RESULTS_DB

client = TestClient(app)

def test_save_and_list_results():
    RESULTS_DB.clear()

    payload = {
        "image_url": "https://pl.wikipedia.org/wiki/Kot_domowy#/media/Plik:Collage_of_Six_Cats-03.JPG",
        "people_count": 3
    }

    resp = client.post("/results", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    assert "id" in data
    assert data["image_url"] == payload["image_url"]
    assert data["people_count"] == payload["people_count"]

    resp_list = client.get("/results")
    assert resp_list.status_code == 200
    results = resp_list.json()
    assert len(results) == 1
    assert results[0]["id"] == data["id"]
