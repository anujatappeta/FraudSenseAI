import React, { useState } from "react";
import ResumeUploader from "../components/ResumeUploader";
import ProfileInput from "../components/ProfileInput";
import ScoreDisplay from "../components/ScoreDisplay";
import TrustGraph from "../components/TrustGraph"; // ✅ Import TrustGraph

function Home() {
  const [resumeResult, setResumeResult] = useState(null);
  const [profileResult, setProfileResult] = useState(null);
  const [scoreResult, setScoreResult] = useState(null);

  return (
    <div style={{ maxWidth: "700px", margin: "auto", padding: "2rem" }}>
      <h1>FraudSense AI</h1>
      <p>Check the authenticity of resumes and LinkedIn profiles.</p>

      <ResumeUploader setResumeResult={setResumeResult} setScoreResult={setScoreResult} />
      <hr />
      <ProfileInput setProfileResult={setProfileResult} setScoreResult={setScoreResult} />
      <hr />
      <ScoreDisplay resumeResult={resumeResult} profileResult={profileResult} scoreResult={scoreResult} />
      <hr />

      {/* ✅ Show Trust Graph only after profile is submitted */}
      {profileResult && (
        <>
          <h2>Trust Graph Visualization</h2>
          <TrustGraph profileData={profileResult} />
        </>
      )}
    </div>
  );
}

export default Home;
