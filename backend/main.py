from __future__ import annotations

from typing import Literal

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

try:
    from backend.model import ensure_model_exists, predict_profile
except ModuleNotFoundError:  # pragma: no cover - direct script execution fallback
    from model import ensure_model_exists, predict_profile

app = FastAPI(title="Career Recommendation API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class StudentProfile(BaseModel):
    interested_field: Literal["AI/ML", "Data Science", "Software Development", "Cybersecurity", "Web Development", "General"]
    python_skill: int = Field(..., ge=1, le=10)
    ml_skill: int = Field(..., ge=1, le=10)
    sql_skill: int = Field(..., ge=1, le=10)
    deep_learning_skill: int = Field(..., ge=1, le=10)
    web_dev_skill: int = Field(..., ge=1, le=10)
    cybersecurity_skill: int = Field(..., ge=1, le=10)
    statistics_skill: int = Field(..., ge=1, le=10)
    communication_skill: int = Field(..., ge=1, le=10)
    problem_solving_skill: int = Field(..., ge=1, le=10)
    cgpa: float = Field(..., ge=0.0, le=10.0)
    ai_interest: int = Field(..., ge=1, le=10)
    data_interest: int = Field(..., ge=1, le=10)


@app.get("/")
def root():
    return {"message": "Career prediction API is running."}


@app.post("/predict")
def predict(profile: StudentProfile):
    try:
        ensure_model_exists()
        payload = profile.model_dump()
        result = predict_profile(payload)
        return result
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:  # pragma: no cover - defensive fallback for runtime issues
        raise HTTPException(status_code=500, detail=f"Prediction failed: {exc}") from exc


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=False)
