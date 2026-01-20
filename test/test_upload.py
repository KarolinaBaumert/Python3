import sys
import pathlib
import io
from unittest.mock import patch, MagicMock

from fastapi.testclient import TestClient

ROOT = pathlib.Path(__file__).resolve().parents[1]
SERVICE_B_PATH = ROOT / "service_b"
sys.path.append(str(SERVICE_B_PATH))

from app.api import app

client = TestClient(app)

@patch("app.api.get_rabbit_connection")
def test_analyze_upload(mock_get_conn):
    """Test that file upload endpoint accepts and stores photos"""
    mock_conn = mock_get_conn.return_value
    mock_channel = mock_conn.channel.return_value

    # Create a fake image file
    fake_image = io.BytesIO(b"fake image content")
    fake_image.name = "test_image.jpg"

    resp = client.post(
        "/analyze/upload",
        files={"file": ("test_image.jpg", fake_image, "image/jpeg")}
    )
    
    assert resp.status_code == 202
    body = resp.json()
    assert "job_id" in body
    
    # Verify RabbitMQ interaction
    mock_channel.queue_declare.assert_called_once()
    mock_channel.basic_publish.assert_called_once()
    
    # Verify the message contains a file:// URL
    call_args = mock_channel.basic_publish.call_args
    import json
    message = json.loads(call_args.kwargs['body'])
    assert message['image_url'].startswith('file://')
    assert message['job_id'] == body['job_id']
