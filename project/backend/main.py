import os
import shutil
import asyncio
import uvicorn
import pika
from fastapi import FastAPI, WebSocket, UploadFile, File
from fastapi.responses import JSONResponse
from typing import Dict

app = FastAPI()

# Storage directories
UPLOAD_DIR = "videos/"
PROCESSED_DIR = "processed_videos/"
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(PROCESSED_DIR, exist_ok=True)

# Store client WebSockets and processing statuses
clients: Dict[str, WebSocket] = {}
video_status: Dict[str, str] = {}

# Setup RabbitMQ connection
RABBITMQ_HOST = "localhost"
EXCHANGE_NAME = "video_tasks"

def publish_task(video_name: str):
    """Publishes a video processing task to RabbitMQ."""
    connection = pika.BlockingConnection(pika.ConnectionParameters(RABBITMQ_HOST))
    channel = connection.channel()
    channel.exchange_declare(exchange=EXCHANGE_NAME, exchange_type="fanout")
    
    channel.basic_publish(exchange=EXCHANGE_NAME, routing_key="", body=video_name)
    connection.close()

@app.post("/upload/")
async def upload_video(file: UploadFile = File(...)):
    """Handles video uploads and publishes tasks to RabbitMQ."""
    video_path = os.path.join(UPLOAD_DIR, file.filename)
    
    with open(video_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # Update status and publish task
    video_status[file.filename] = "processing"
    publish_task(file.filename)

    return JSONResponse({"message": "Video uploaded successfully!", "filename": file.filename})

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """Handles WebSocket connections from clients."""
    await websocket.accept()
    client_id = str(id(websocket))
    clients[client_id] = websocket
    
    try:
        while True:
            await asyncio.sleep(1)
    except Exception as e:
        print(f"WebSocket error: {e}")
    finally:
        del clients[client_id]

@app.post("/internal/video-enhancement-status/")
async def update_enhancement_status(video_name: str):
    """Receives video enhancement status updates."""
    video_status[video_name] = "enhanced"
    await notify_clients(video_name, "enhanced")
    return {"message": "Enhancement status updated"}

@app.post("/internal/metadata-extraction-status/")
async def update_metadata_status(video_name: str, metadata: dict):
    """Receives metadata extraction updates."""
    video_status[video_name] = "metadata_extracted"
    await notify_clients(video_name, "metadata_extracted", metadata)
    return {"message": "Metadata status updated"}

async def notify_clients(video_name: str, status: str, metadata: dict = None):
    """Sends updates to connected WebSocket clients."""
    for client in clients.values():
        await client.send_json({"filename": video_name, "status": status, "metadata": metadata})

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
