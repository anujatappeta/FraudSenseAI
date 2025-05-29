import React, { useEffect, useState } from "react";
import axios from "axios";
import "./ScoreDisplay.css";

function ScoreDisplay({ resumeResult, profileResult, scoreResult }) {
  const [score, setScore] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    async function fetchScore() {
      setLoading(true);
      try {
        let params = {};

        if (resumeResult && Array.isArray(resumeResult.flags) && resumeResult.flags.length > 0) {
          params.resume_text = resumeResult.flags.join(" ");
        }

        if (profileResult) {
          params.profile_data = JSON.stringify(profileResult);
        }

        if (!params.resume_text && !params.profile_data) {
          setScore(null);
          setLoading(false);
          return;
        }

        const res = await axios.get("http://localhost:8000/score/", { params });
        setScore(res.data);
      } catch (error) {
        alert("Failed to calculate realness score.");
      } finally {
        setLoading(false);
      }
    }

    fetchScore();
  }, [resumeResult, profileResult]);

  if (loading) return <p className="score-container">Calculating realness score...</p>;
  if (!score) return <p className="score-container">Upload a resume or analyze a profile to get the Realness Score.</p>;

  const details = score.details || {};

  return (
    <div className="score-container">
      <h2 className="score-title">🎯 Realness Score</h2>
      <p className="score-value">{score.realness_score} / 100</p>

      <h3 className="score-subtitle">📊 Breakdown:</h3>
      <ul className="score-list">
        {"experience_score" in details && (
          <li>Experience Score: {details.experience_score} (Years: {details.experience_years})</li>
        )}
        {"education_score" in details && <li>Education Score: {details.education_score}</li>}
        {"skill_score" in details && (
          <li>
            Skills Score: {details.skill_score} <br />
            Matched Skills: {details.matched_skills?.join(", ") || "None"}
          </li>
        )}
        {"resume_ai_score" in details && (
          <li>
            Resume AI Likelihood Score: {details.resume_ai_score}
            <br />
            Flags: {details.resume_flags?.join(", ") || "None"}
          </li>
        )}
      </ul>
    </div>
  );
}

export default ScoreDisplay;
