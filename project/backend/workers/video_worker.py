import os
import pika
import cv2
import requests

UPLOAD_DIR = "videos/"
PROCESSED_DIR = "processed_videos/"
os.makedirs(PROCESSED_DIR, exist_ok=True)

RABBITMQ_HOST = "localhost"
EXCHANGE_NAME = "video_tasks"
FASTAPI_SERVER = "http://localhost:8000"

def process_video(video_name):
    """Applies video enhancements like increasing brightness and FPS."""
    input_path = os.path.join(UPLOAD_DIR, video_name)
    output_path = os.path.join(PROCESSED_DIR, f"enhanced_{video_name}")

    cap = cv2.VideoCapture(input_path)
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    out = cv2.VideoWriter(output_path, fourcc, 30.0, (640, 480))

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        frame = cv2.convertScaleAbs(frame, alpha=1.2, beta=30)  # Brightness adjustment
        out.write(frame)

    cap.release()
    out.release()

    # Notify FastAPI
    requests.post(f"{FASTAPI_SERVER}/internal/video-enhancement-status/", json={"video_name": video_name})

def callback(ch, method, properties, body):
    """Consumes video processing tasks from RabbitMQ."""
    video_name = body.decode()
    process_video(video_name)

# Setup RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters(RABBITMQ_HOST))
channel = connection.channel()
channel.exchange_declare(exchange=EXCHANGE_NAME, exchange_type="fanout")

queue = channel.queue_declare(queue="", exclusive=True)
channel.queue_bind(exchange=EXCHANGE_NAME, queue=queue.method.queue)

channel.basic_consume(queue=queue.method.queue, on_message_callback=callback, auto_ack=True)

print("Video Enhancement Worker is waiting for tasks...")
channel.start_consuming()
