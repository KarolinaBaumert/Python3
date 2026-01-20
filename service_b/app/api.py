from fastapi import FastAPI, File, UploadFile
from pydantic import BaseModel
import uuid
import json
import pika
import os
from pathlib import Path

RABBITMQ_HOST = "rabbitmq"
RABBITMQ_USER = "user"
RABBITMQ_PASS = "pass"
QUEUE_NAME = "analysis_requests"

# Photo storage configuration
# Use /app/uploads in production (Docker), or ./uploads locally for testing
UPLOAD_DIR = Path(os.environ.get("UPLOAD_DIR", "/app/uploads"))
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

app = FastAPI(title="Service B - Analysis API")

class AnalyzeRequest(BaseModel):
  image_url: str

class AnalyzeResponse(BaseModel):
  job_id: str

def get_rabbit_connection():
  credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASS)
  params = pika.ConnectionParameters(host=RABBITMQ_HOST, credentials=credentials)
  return pika.BlockingConnection(params)

@app.post("/analyze", response_model=AnalyzeResponse, status_code=202)
def analyze(req: AnalyzeRequest):
  job_id = str(uuid.uuid4())
  message = {
    "job_id": job_id,
    "image_url": req.image_url,
  }

  conn = get_rabbit_connection()
  ch = conn.channel()
  ch.queue_declare(queue=QUEUE_NAME, durable=True)

  ch.basic_publish(
    exchange="",
    routing_key=QUEUE_NAME,
    body=json.dumps(message),
    properties=pika.BasicProperties(
      delivery_mode=2
    )
  )
  conn.close()

  return AnalyzeResponse(job_id=job_id)

@app.post("/analyze/upload", response_model=AnalyzeResponse, status_code=202)
async def analyze_upload(file: UploadFile = File(...)):
  """Upload a photo and analyze it. Photo will be stored on the server."""
  job_id = str(uuid.uuid4())
  
  # Generate unique filename with original extension
  file_extension = Path(file.filename).suffix if file.filename else ".jpg"
  unique_filename = f"{job_id}{file_extension}"
  file_path = UPLOAD_DIR / unique_filename
  
  # Save the uploaded file
  with open(file_path, "wb") as buffer:
    content = await file.read()
    buffer.write(content)
  
  # Create message with local file path
  message = {
    "job_id": job_id,
    "image_url": f"file://{file_path}",
  }

  conn = get_rabbit_connection()
  ch = conn.channel()
  ch.queue_declare(queue=QUEUE_NAME, durable=True)

  ch.basic_publish(
    exchange="",
    routing_key=QUEUE_NAME,
    body=json.dumps(message),
    properties=pika.BasicProperties(
      delivery_mode=2
    )
  )
  conn.close()

  return AnalyzeResponse(job_id=job_id)
