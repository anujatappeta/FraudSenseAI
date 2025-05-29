import React, { useState } from "react";
import axios from "axios";
import "./ProfileInput.css";

export default function ProfileInput({ setProfileResult, setScoreResult }) {
  const [name, setName] = useState("");
  const [experience, setExperience] = useState([{ role: "", company: "", years: 0 }]);
  const [education, setEducation] = useState([{ degree: "", university: "", year: 2023 }]);
  const [skills, setSkills] = useState("");
  const [scoreResult, localSetScoreResult] = useState(null); // Local score result
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);

    const payload = {
      name,
      experience,
      education,
      skills: skills.split(",").map((skill) => skill.trim()),
    };

    try {
     const res = await axios.post("http://localhost:8000/profile/score", payload);
      setProfileResult && setProfileResult(res.data);
      setScoreResult && setScoreResult(null); // Reset parent score
      localSetScoreResult(res.data); // Show local score
    } catch (error) {
      alert("Error analyzing profile: " + (error.response?.data?.detail || error.message));
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container">
      <h2 className="heading">Enter Profile Data</h2>
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label className="label">Name:</label>
          <input
            className="input"
            value={name}
            onChange={(e) => setName(e.target.value)}
            required
          />
        </div>

        <div className="form-group">
          <label className="label">Experience (role, company, years):</label>
          {experience.map((exp, idx) => (
            <div key={idx} className="grid-three-columns">
              <input
                placeholder="Role"
                value={exp.role}
                onChange={(e) => {
                  const newExp = [...experience];
                  newExp[idx].role = e.target.value;
                  setExperience(newExp);
                }}
                required
                className="input"
              />
              <input
                placeholder="Company"
                value={exp.company}
                onChange={(e) => {
                  const newExp = [...experience];
                  newExp[idx].company = e.target.value;
                  setExperience(newExp);
                }}
                required
                className="input"
              />
              <input
                type="number"
                placeholder="Years"
                value={exp.years}
                onChange={(e) => {
                  const newExp = [...experience];
                  newExp[idx].years = Number(e.target.value);
                  setExperience(newExp);
                }}
                required
                className="input-number"
              />
            </div>
          ))}
          <button
            type="button"
            onClick={() =>
              setExperience([...experience, { role: "", company: "", years: 0 }])
            }
            className="button-add"
          >
            + Add Experience
          </button>
        </div>

        <div className="form-group">
          <label className="label">Education (degree, university, year):</label>
          {education.map((edu, idx) => (
            <div key={idx} className="grid-three-columns">
              <input
                placeholder="Degree"
                value={edu.degree}
                onChange={(e) => {
                  const newEdu = [...education];
                  newEdu[idx].degree = e.target.value;
                  setEducation(newEdu);
                }}
                required
                className="input"
              />
              <input
                placeholder="University"
                value={edu.university}
                onChange={(e) => {
                  const newEdu = [...education];
                  newEdu[idx].university = e.target.value;
                  setEducation(newEdu);
                }}
                required
                className="input"
              />
              <input
                type="number"
                placeholder="Year"
                value={edu.year}
                onChange={(e) => {
                  const newEdu = [...education];
                  newEdu[idx].year = Number(e.target.value);
                  setEducation(newEdu);
                }}
                required
                className="input-number"
              />
            </div>
          ))}
          <button
            type="button"
            onClick={() =>
              setEducation([...education, { degree: "", university: "", year: 2023 }])
            }
            className="button-add"
          >
            + Add Education
          </button>
        </div>

        <div className="form-group">
          <label className="label">Skills (comma separated):</label>
          <input
            className="input"
            value={skills}
            onChange={(e) => setSkills(e.target.value)}
            placeholder="Python, Machine Learning, FastAPI"
            required
          />
        </div>

        <button type="submit" className="button-submit" disabled={loading}>
          {loading ? "Analyzing..." : "Get Score"}
        </button>
      </form>

      {scoreResult && (
        <div className="score-result">
          <h3>
            Realness Score: <strong>{scoreResult.realness_score}</strong>
          </h3>
          <pre>{JSON.stringify(scoreResult.details, null, 2)}</pre>
        </div>
      )}
    </div>
  );
}
