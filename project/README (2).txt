# Video Processing Pipeline (Backend + React Frontend)

This project is a **distributed, event-driven video processing system** that allows users to:
✅ Upload videos via a web interface  
✅ Process videos asynchronously (Enhancement & Metadata Extraction)  
✅ Receive real-time updates via WebSockets  
✅ View enhanced videos after processing  

It is built using **FastAPI (Python)**, **RabbitMQ (Messaging Queue)**, and **React (Frontend UI)**.  

---

## 📂 **Project Folder Structure**
```
H:/project/
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

##  **Step 1: Install Required Software**
### ✅ Install Python & Node.js
- **Python (3.8+)**: Download & Install from [https://www.python.org/](https://www.python.org/)
- **Node.js (LTS Version)**: Install from [https://nodejs.org/](https://nodejs.org/)
- **RabbitMQ (Message Queue Server)**: Download & install from [https://www.rabbitmq.com/download.html](https://www.rabbitmq.com/download.html)

Once installed, verify them by running:
```bash
python --version  # Should print Python 3.x.x
node -v           # Should print Node.js version
npm -v            # Should print npm version
```

---

## 🛠 **Step 2: Install Backend Dependencies**
1️⃣ Open **Command Prompt / Terminal**  
2️⃣ Navigate to the **backend folder**:  
```bash
cd "H:/college/New folder/backend"
```
3️⃣ Install required Python libraries:
```bash
pip install -r requirements.txt
```

---

## 🛠 **Step 3: Install Frontend (React) Dependencies**
1️⃣ Open **a new terminal** and navigate to the frontend folder:
```bash
cd "H:/college/project/frontend"
```
2️⃣ Install React dependencies:
```bash
npm install
```

---

##  **Step 4: Start RabbitMQ (IMPORTANT)**
RabbitMQ is required for processing messages between the backend and workers.  
Run the following command to check if RabbitMQ is running:
```bash
rabbitmqctl status
```
✅ If it **prints server details**, RabbitMQ is running.  
❌ If you get an error, start RabbitMQ manually:  
```bash
rabbitmq-server
```

---

##  **Step 5: Start the Backend Server**
1️⃣ Open **a terminal inside `backend/`**  
2️⃣ Run the FastAPI server:
```bash
python main.py
```
✅ **Output Should Be:**  
```
Running on http://127.0.0.1:8000
```

---

##  **Step 6: Start Workers (RabbitMQ Consumers)**
These workers process the uploaded videos.

✅ **Open a second terminal** and start the **video enhancement worker**:
```bash
cd "H:/college/project/backend/workers"
python video_worker.py
```

✅ **Open a third terminal** and start the **metadata extraction worker**:
```bash
cd "H:/college/project/backend/workers"
python metadata_worker.py
```

✅ You should see:
```
Video Enhancement Worker is waiting for tasks...
Metadata Extraction Worker is waiting for tasks...
```

---

##  **Step 7: Start the React Frontend**
1️⃣ Open a **new terminal inside `frontend/`**  
2️⃣ Run:
```bash
npm start
```
✅ This should open **http://localhost:3000/** in your browser.

---

##  **Step 8: Upload a Video**
### 📌 Where to Upload the Video in Code?
- **Manually via API:**  
  Open **Postman** or use **cURL**:  
  ```bash
  curl -X POST "http://127.0.0.1:8000/upload/" -F "file=@your_video.mp4"
  ```
- **Using the React UI:**  
  - Open **http://localhost:3000/**
  - Click **"Choose File"** and **Upload**
  - The backend will process the video

---

## 🖥 **Step 9: Viewing the Results**
- **Metadata (Resolution, FPS, Duration)** appears on the React UI  
- **Enhanced Video** appears when processing is complete  
- The WebSocket connection sends real-time updates  

---

##  **Troubleshooting Errors**
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
