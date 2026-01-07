import json
import time
import pika
import requests

RABBITMQ_HOST = "rabbitmq"
RABBITMQ_USER = "user"
RABBITMQ_PASS = "pass"
QUEUE_NAME = "analysis_requests"
SERVICE_A_URL = "http://service_a:8000/results"

def count_people_on_image(image_url: str) -> int:
  return 5

def callback(ch, method, properties, body):
  message = json.loads(body)
  job_id = message["job_id"]
  image_url = message["image_url"]

  print(f"Received job {job_id} for image {image_url}")

  people_count = count_people_on_image(image_url)

  payload = {
    "id": job_id,
    "image_url": image_url,
    "people_count": people_count,
  }

  try:
    resp = requests.post(SERVICE_A_URL, json=payload, timeout=5)
    resp.raise_for_status()
    print(f"Result for {job_id} sent to Service A")
    ch.basic_ack(delivery_tag=method.delivery_tag)
  except Exception as e:
    print(f"Error sending result for {job_id}: {e}.  Requeuing...")
    ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)

def main():
  credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASS)
  params = pika.ConnectionParameters(host=RABBITMQ_HOST, credentials=credentials)
  connection = pika.BlockingConnection(params)
  channel = connection.channel()

  channel.queue_declare(queue=QUEUE_NAME, durable=True)
  channel.basic_qos(prefetch_count=1)
  channel.basic_consume(queue=QUEUE_NAME, on_message_callback=callback, auto_ack=False)

  print("Worker started. Waiting for messages...")
  channel.start_consuming()

if __name__ == "__main__":
  main()

