from sqlalchemy import JSON, Column, DateTime, Float, Integer, String
from sqlalchemy.sql import func

from app.db import Base


class PredictionLog(Base):
    __tablename__ = "prediction_logs"

    id = Column(Integer, primary_key=True, index=True)
    model_version = Column(String(50), nullable=False)
    request_payload = Column(JSON, nullable=False)
    response_payload = Column(JSON, nullable=False)
    prediction = Column(String(50), nullable=False)
    score = Column(Float, nullable=False)
    inference_ms = Column(Float, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
