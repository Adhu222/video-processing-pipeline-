import React, { useState, useEffect } from "react";
import axios from "axios";

const API_URL = "http://localhost:8000"; // FastAPI Server

function App() {
  const [file, setFile] = useState(null);
  const [status, setStatus] = useState("");
  const [metadata, setMetadata] = useState(null);
  const [enhancedVideo, setEnhancedVideo] = useState(null);

  useEffect(() => {
    const ws = new WebSocket("ws://localhost:8000/ws");

    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      if (data.status === "metadata_extracted") {
        setMetadata(data.metadata);
      } else if (data.status === "enhanced") {
        setEnhancedVideo(`http://localhost:8000/processed_videos/enhanced_${data.filename}`);
      }
      setStatus(data.status);
    };

    return () => ws.close();
  }, []);

  const handleFileChange = (event) => {
    setFile(event.target.files[0]);
  };

  const handleUpload = async () => {
    if (!file) {
      alert("Please select a file!");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    try {
      await axios.post(`${API_URL}/upload/`, formData);
      setStatus("Processing...");
    } catch (error) {
      console.error("Upload failed:", error);
    }
  };

  return (
    <div>
      <h1>Video Processing App</h1>
      <input type="file" onChange={handleFileChange} />
      <button onClick={handleUpload}>Upload</button>
      <p>Status: {status}</p>

      {metadata && (
        <div>
          <h3>Metadata</h3>
          <p>Resolution: {metadata.resolution}</p>
          <p>FPS: {metadata.fps}</p>
          <p>Duration: {metadata.duration} seconds</p>
        </div>
      )}

      {enhancedVideo && (
        <div>
          <h3>Enhanced Video</h3>
          <video src={enhancedVideo} controls width="600" />
        </div>
      )}
    </div>
  );
}

export default App;
