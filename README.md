# 🎥 Video Processing Pipeline (FastAPI + RabbitMQ + React)

This project is a **distributed, event-driven video processing system** that allows users to:  
✅ Upload videos via a web interface  
✅ Process videos asynchronously (Enhancement & Metadata Extraction)  
✅ Receive real-time updates via WebSockets  
✅ View enhanced videos after processing  

The system mimics real-world platforms like **YouTube and Instagram**, where videos are enhanced and metadata is extracted before being made available.

---

## 📂 **Project Folder Structure**
```
📦 video-processing-pipeline
├── backend/                # FastAPI Backend
│   ├── main.py             # FastAPI server (handles uploads & WebSockets)
│   ├── workers/            # RabbitMQ Workers
│   │   ├── video_worker.py        # Enhances videos
│   │   ├── metadata_worker.py     # Extracts metadata
│   ├── videos/             # (Empty Folder) Stores uploaded videos
│   ├── processed_videos/   # (Empty Folder) Stores enhanced videos
│   ├── requirements.txt    # Python dependencies
│
├── frontend/               # React Frontend
│   ├── src/
│   │   ├── App.js          # React UI (Main component)
│   │   ├── index.js
│   │   ├── styles.css
│   ├── package.json        # React dependencies
│   ├── public/             # Contains index.html
```

---

## 🔧 **Installation & Setup**

### **1️⃣ Install Required Software**
- **Python (3.8+)** → Install from [python.org](https://www.python.org/)  
- **Node.js (LTS Version)** → Install from [nodejs.org](https://nodejs.org/)  
- **RabbitMQ** → Install from [rabbitmq.com](https://www.rabbitmq.com/download.html)  

Check if they are installed:
```bash
python --version  # Should print Python 3.x.x
node -v           # Should print Node.js version
npm -v            # Should print npm version
```

### **2️⃣ Install Backend Dependencies**
1️⃣ Open a terminal inside **backend/**:
```bash
cd backend
pip install -r requirements.txt
```

### **3️⃣ Install Frontend (React) Dependencies**
1️⃣ Open a new terminal inside **frontend/**:
```bash
cd frontend
npm install
```

### **4️⃣ Start RabbitMQ**
Check if RabbitMQ is running:
```bash
rabbitmqctl status
```
If not, start it manually:
```bash
rabbitmq-server
```

### **5️⃣ Start the Backend Server**
```bash
cd backend
python main.py
```
✅ **Output:**  
```
Running on http://127.0.0.1:8000
```

### **6️⃣ Start Workers (RabbitMQ Consumers)**
✅ **Open a second terminal** and start the **video enhancement worker**:
```bash
cd backend/workers
python video_worker.py
```
✅ **Open a third terminal** and start the **metadata extraction worker**:
```bash
cd backend/workers
python metadata_worker.py
```

### **7️⃣ Start the Frontend (React)**
```bash
cd frontend
npm start
```
✅ This should open **http://localhost:3000/** in your browser.

---

## 📤 **Uploading Videos**

Users can upload videos in **two ways**:  

### **1️⃣ Using the React Web UI (Recommended)**
- Open **http://localhost:3000/** in a browser.  
- Click **"Choose File"**, select a video file, and click **"Upload"**.  
- The backend automatically saves the video and starts processing.

### **2️⃣ Using API (Postman or cURL)**
- **Postman:**  
  - Open **Postman** → Set method to **POST**  
  - URL: `http://127.0.0.1:8000/upload/`  
  - Go to **Body → form-data** → Key = **file** (Choose a video file)  
  - Click **Send**  

- **cURL Command:**  
  ```bash
  curl -X POST "http://127.0.0.1:8000/upload/" -F "file=@your_video.mp4"
  ```

---

## 🖥 **Viewing the Results**
- **Metadata (Resolution, FPS, Duration)** appears in the React UI.  
- **Enhanced Video** appears once processing is complete.  
- The WebSocket connection sends real-time updates to the frontend.

---

## 📌 **Troubleshooting Errors**

### ❌ `ModuleNotFoundError: No module named 'requests'`
✅ Run:
```bash
pip install requests
```

### ❌ `pika.exceptions.AMQPConnectionError`
✅ Ensure **RabbitMQ is running**:
```bash
rabbitmqctl status
```

### ❌ `npm: command not found`
✅ Install **Node.js** and verify:
```bash
node -v
npm -v
```

---

## 📜 License
This project is open-source. Feel free to use and modify it! 🚀
