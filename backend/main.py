"""
FastAPI Backend Application for Automobile Service Diagnosis Assistant.
Provides RESTful APIs for health checks, symptom diagnosis, and history retrieval.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Dict, Any
from contextlib import asynccontextmanager

from backend.database import init_db, save_diagnosis, get_history
from backend.diagnosis import diagnose_symptom


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initializes the database on startup."""
    init_db()
    yield


app = FastAPI(
    title="Automobile Service Diagnosis API",
    description="Backend API for preliminary vehicle problem diagnosis",
    version="1.0.0",
    lifespan=lifespan
)

# Enable CORS for seamless interaction
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class DiagnosisRequest(BaseModel):
    vehicle: str = Field(..., example="Car", description="Type of vehicle, e.g. Car, Bike, SUV, Van")
    symptom: str = Field(..., example="Engine is overheating and smoke is coming from hood", description="Observed symptom or issue")


class DiagnosisResponse(BaseModel):
    vehicle: str
    symptom: str
    problem: str
    possible_cause: str
    severity: str
    basic_checks: List[str]
    recommended_action: str
    disclaimer: str


class HistoryRecord(BaseModel):
    id: int
    date: str
    vehicle: str
    symptom: str
    diagnosis: str
    severity: str


@app.get("/api/health", summary="Health Check Endpoint")
def health_check() -> Dict[str, str]:
    """Returns the health status of the backend API."""
    return {"status": "running"}


@app.post("/api/diagnose", response_model=DiagnosisResponse, summary="Diagnose Vehicle Problem")
def diagnose(request: DiagnosisRequest):
    """
    Analyzes the vehicle symptom using the diagnosis engine,
    persists the diagnosis in the SQLite database, and returns the result.
    """
    if not request.symptom or not request.symptom.strip():
        raise HTTPException(status_code=400, detail="Symptom description cannot be empty.")

    vehicle = request.vehicle.strip() if request.vehicle else "Car"
    symptom = request.symptom.strip()

    # Perform diagnosis
    result = diagnose_symptom(vehicle=vehicle, symptom=symptom)

    # Save to SQLite database
    save_diagnosis(
        vehicle=result["vehicle"],
        symptom=result["symptom"],
        diagnosis=result["problem"],
        severity=result["severity"]
    )

    return result


@app.get("/api/history", response_model=List[HistoryRecord], summary="Get Diagnosis History")
def history():
    """Retrieves all past diagnosis records stored in the database."""
    records = get_history()
    return records


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host="127.0.0.1", port=8000, reload=True)
