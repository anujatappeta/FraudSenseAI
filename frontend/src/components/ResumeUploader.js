import React, { useState } from "react";
import axios from "axios";
import "./ResumeUploader.css";

function ResumeUploader({ setResumeResult, setScoreResult }) {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleUpload = async () => {
    if (!file) {
      alert("Please select a resume file (.txt or .pdf)");
      return;
    }
    const formData = new FormData();
    formData.append("file", file);

    setLoading(true);
    try {
      const res = await axios.post("http://localhost:8000/resume/upload", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      setResumeResult(res.data);
      setScoreResult(null);
    } catch (error) {
      alert("Failed to analyze resume. " + (error.response?.data?.detail || error.message));
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="resume-container">
      <h2 className="resume-title">Upload Resume</h2>
      <input
        type="file"
        accept=".txt,.pdf"
        onChange={handleFileChange}
        className="resume-input"
      />
      <br />
      <button onClick={handleUpload} disabled={loading} className="resume-button">
        {loading ? "Analyzing..." : "Analyze Resume"}
      </button>
    </div>
  );
}

export default ResumeUploader;
