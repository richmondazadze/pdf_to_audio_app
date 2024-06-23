import React, { useState } from "react";
import axios from "axios";

function UploadForm() {
  const [file, setFile] = useState(null);
  const [audioUrl, setAudioUrl] = useState("");

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleUpload = async () => {
    const formData = new FormData();
    formData.append("file", file);
    try {
      const response = await axios.post(
        "http://localhost:5000/upload",
        formData,
        {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        }
      );
      setAudioUrl(response.data.audio_url);
    } catch (error) {
      console.error("Error uploading file:", error);
    }
  };

  return (
    <div>
      <input type="file" onChange={handleFileChange} />
      <button onClick={handleUpload}>Upload and Convert</button>
      {audioUrl && (
        <div>
          <h3>Audio File:</h3>
          <audio controls src={`http://localhost:5000${audioUrl}`} />
          <a href={`http://localhost:5000${audioUrl}`} download>
            Download
          </a>
        </div>
      )}
    </div>
  );
}

export default UploadForm;
