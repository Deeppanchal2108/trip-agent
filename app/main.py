from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import trip_routes
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

app = FastAPI(
    title="TripTrek API",
    description="AI-powered travel planning API",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(trip_routes.router)

@app.get("/")
def read_root():
    return {
        "message": "Welcome to TripTrek API 🚀",
        "docs": "/docs",
        "health": "/trip/health"
    }

@app.get("/ping")
def ping():
    return {"message": "pong"}
