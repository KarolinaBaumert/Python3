import sys
import pathlib
from unittest.mock import patch, MagicMock

from fastapi.testclient import TestClient

ROOT = pathlib.Path(__file__).resolve().parents[1]
SERVICE_B_PATH = ROOT / "service_b"
sys.path.append(str(SERVICE_B_PATH))

from app.api import app

client = TestClient(app)

@patch("app.api.get_rabbit_connection")
def test_analyze_queues_message(mock_get_conn):
    mock_conn = mock_get_conn.return_value
    mock_channel = mock_conn.channel.return_value

    resp = client.post("/analyze", json={"image_url": "https://pl.wikipedia.org/wiki/Kot_domowy#/media/Plik:Collage_of_Six_Cats-03.JPG"})
    assert resp.status_code == 202
    body = resp.json()
    assert "job_id" in body

    mock_channel.queue_declare.assert_called_once()
    mock_channel.basic_publish.assert_called_once()
