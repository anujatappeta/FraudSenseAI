# 🔍 FraudSense AI

FraudSense AI is an advanced AI-powered verification system designed to detect fake resumes, fraudulent internships, and suspicious job offers in real-time. It empowers students, job seekers, and recruiters with intelligent tools to assess the **authenticity of resumes and company profiles** before making critical career decisions.

---

## ❗ The Problem

Every year, thousands of individuals fall victim to fake internships, fraudulent job offers, and falsified candidate profiles. These scams not only waste time and resources but also cause emotional and financial damage to early-career professionals.

There is no widely available, AI-powered tool that provides a **trustworthy assessment of candidate profiles or internship/company legitimacy**—until now.

---

## ✅ Why Use FraudSense AI?

- 🔎 **Resume Realness Scoring**  
  AI-driven scoring system detects inconsistencies, unnatural patterns, and fabricated sections in resumes using transformer-based NLP models.

- 🔐 **Company/Internship Authenticity Check**  
  Verifies employer data using semantic search and web presence validation (via FAISS vector DB and Ollama Mistral LLM-based analysis).

- 📊 **Trust Graph Visualization**  
  Shows how different sources, resume content, and online footprints interconnect to assess credibility in a user-friendly graph.

- 🧠 **LLM + Embedding-Driven Validation**  
  Uses locally hosted Mistral model via Ollama to provide explainable insights with privacy and speed.

- ⚡ **Real-Time Results**  
  All evaluations are returned instantly with user-uploaded inputs—no external scraping or third-party APIs required.

- 🔧 **Modular and Scalable Architecture**  
  Easy to plug into hiring platforms, LMS systems, and resume portals.

---

## 🚀 Features

- Upload and analyze resumes in real-time  
- Enter LinkedIn/GitHub or other profile data  
- Get an AI-generated “Realness Score”  
- View flagged inconsistencies and warnings  
- Explore verification trust graph  
- Frontend built with clean and intuitive UX (React.js)  
- Backend logic powered by FastAPI + Torch + Transformers

---

## 🧰 Tech Stack

| Layer         | Tools Used                                                                 |
|---------------|-----------------------------------------------------------------------------|
| **Frontend**  | React.js, HTML5, CSS3, JavaScript, JSX                                      |
| **Backend**   | FastAPI, Uvicorn, Python, Pydantic                                          |
| **AI/ML**     | Hugging Face Transformers, FAISS, Ollama (Mistral model), Torch             |
| **Parsing**   | pdfplumber for resume extraction                                            |
| **Visualization** | D3.js or react-force-graph (planned)                                   |
| **IDE & Tools** | VS Code, Git                                                              |

---

## 📐 System Architecture (High-Level Overview)

```plaintext
[User Uploads Resume/Profile] ---> [FastAPI Backend]
                                   |
                      ┌────────────┼────────────┐
                      ▼                         ▼
        [Resume Parser + NLP Analysis]     [LLM-based Reasoning (Mistral)]
                      ▼                         ▼
                  [Scoring Engine]       [Verification Graph Generator]
                      ▼                         ▼
           [Realness Score + Warnings] --> [React.js Frontend Display]

🛣️ Future Development Roadmap

🔗 LinkedIn & GitHub Deep Integration
Automatically verify claimed skills and experience via APIs.

🧾 Certificate Verification
Scan and validate educational or internship certificates using OCR and LLM-powered consistency checks.

🔍 Crowdsourced Trust Layer
Allow users to upvote/downvote internship listings or employers and contribute to a shared reputation system.

🔒 Privacy-First LLM Hosting
Full deployment of Ollama-based Mistral on secure edge servers to ensure data never leaves the local machine.

📡 Browser Extension
Chrome plugin to detect fake internship/job listings directly on job boards and career platforms.

Built With ❤️ by me.

FraudSense AI is crafted with precision, purpose, and passion to make the digital hiring ecosystem safer, smarter, and more trustworthy. Whether you’re a student navigating early career paths or a recruiter filtering thousands of profiles, this tool is built for you.
