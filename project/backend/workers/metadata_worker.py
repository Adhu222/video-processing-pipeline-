import os
import pika
import cv2
import requests

UPLOAD_DIR = "videos/"
RABBITMQ_HOST = "localhost"
EXCHANGE_NAME = "video_tasks"
FASTAPI_SERVER = "http://localhost:8000"

def extract_metadata(video_name):
    """Extracts metadata like resolution and duration."""
    video_path = os.path.join(UPLOAD_DIR, video_name)
    cap = cv2.VideoCapture(video_path)

    metadata = {
        "resolution": f"{int(cap.get(3))}x{int(cap.get(4))}",
        "fps": cap.get(5),
        "duration": cap.get(7) / cap.get(5)  # Total frames / FPS
    }

    cap.release()

    # Notify FastAPI
    requests.post(f"{FASTAPI_SERVER}/internal/metadata-extraction-status/",
                  json={"video_name": video_name, "metadata": metadata})

def callback(ch, method, properties, body):
    """Consumes metadata extraction tasks from RabbitMQ."""
    video_name = body.decode()
    extract_metadata(video_name)

# Setup RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters(RABBITMQ_HOST))
channel = connection.channel()
channel.exchange_declare(exchange=EXCHANGE_NAME, exchange_type="fanout")

queue = channel.queue_declare(queue="", exclusive=True)
channel.queue_bind(exchange=EXCHANGE_NAME, queue=queue.method.queue)

channel.basic_consume(queue=queue.method.queue, on_message_callback=callback, auto_ack=True)

print("Metadata Extraction Worker is waiting for tasks...")
channel.start_consuming()
