from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import resume, profile, score

app = FastAPI(title="FraudSense AI")

# Define allowed origins for CORS (frontend URLs)
origins = [
    "http://localhost:3000",  # React frontend local dev server
]

# Add CORS middleware to allow cross-origin requests from frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],   # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],   # Allow all headers
)

# Include API routers with prefixes and tags for organization
app.include_router(resume.router, prefix="/resume", tags=["Resume"])
app.include_router(profile.router, prefix="/profile", tags=["Profile"])
app.include_router(score.router, prefix="/score", tags=["Score"])

# Root endpoint for a simple welcome message
@app.get("/")
def read_root():
    return {"message": "Welcome to FraudSense AI API"}
