from fastapi import FastAPI
from pydantic import BaseModel
import uuid
import json
import pika

RABBITMQ_HOST = "rabbitmq"
RABBITMQ_USER = "user"
RABBITMQ_PASS = "pass"
QUEUE_NAME = "analysis_requests"

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
