from pydantic import BaseModel, Field


class PredictionRequest(BaseModel):
    age: int = Field(..., ge=18, le=100)
    income: float = Field(..., ge=0)
    transactions_last_30d: int = Field(..., ge=0)
    support_tickets_last_30d: int = Field(..., ge=0)
    avg_session_minutes: float = Field(..., ge=0)


class PredictionResponse(BaseModel):
    model_version: str
    churn_probability: float
    prediction: str
    inference_ms: float
