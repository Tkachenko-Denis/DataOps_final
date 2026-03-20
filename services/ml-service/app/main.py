import logging
import os
import time
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from sqlalchemy.exc import SQLAlchemyError

from app.db import Base, SessionLocal, engine
from app.logging_config import configure_logging
from app.metrics import (
    PREDICTION_ERRORS_TOTAL,
    PREDICTION_LATENCY_SECONDS,
    PREDICTION_REQUESTS_TOTAL,
    metrics_response,
)
from app.models import PredictionLog
from app.schemas import PredictionRequest, PredictionResponse
from app.service import label_from_score, score_request


configure_logging()
logger = logging.getLogger("ml-service")
MODEL_VERSION = os.getenv("MODEL_VERSION", "1.0.0")
SERVICE_NAME = os.getenv("SERVICE_NAME", "customer-churn-api")
startup_completed = False


@asynccontextmanager
async def lifespan(_: FastAPI):
    global startup_completed
    Base.metadata.create_all(bind=engine)
    startup_completed = True
    yield


app = FastAPI(title=SERVICE_NAME, version=MODEL_VERSION, lifespan=lifespan)


@app.middleware("http")
async def log_requests(request: Request, call_next):
    started = time.perf_counter()
    response = await call_next(request)
    elapsed_ms = round((time.perf_counter() - started) * 1000, 2)
    logger.info(
        "request_completed",
        extra={
            "extra_data": {
                "path": request.url.path,
                "method": request.method,
                "status_code": response.status_code,
                "duration_ms": elapsed_ms,
            }
        },
    )
    return response


@app.get("/health/live")
def live() -> dict[str, str]:
    return {"status": "live"}


@app.get("/health/ready")
def ready() -> dict[str, str]:
    with engine.connect():
        pass
    return {"status": "ready"}


@app.get("/health/startup")
def startup() -> dict[str, str]:
    return {"status": "started" if startup_completed else "starting"}


@app.get("/metrics")
def metrics():
    return metrics_response()


@app.post("/api/v1/predict", response_model=PredictionResponse)
def predict(payload: PredictionRequest) -> PredictionResponse:
    PREDICTION_REQUESTS_TOTAL.inc()
    started = time.perf_counter()
    score = score_request(payload)
    prediction = label_from_score(score)
    inference_ms = round((time.perf_counter() - started) * 1000, 2)

    response_payload = {
        "model_version": MODEL_VERSION,
        "churn_probability": score,
        "prediction": prediction,
        "inference_ms": inference_ms,
    }

    try:
        with PREDICTION_LATENCY_SECONDS.time():
            db = SessionLocal()
            try:
                db.add(
                    PredictionLog(
                        model_version=MODEL_VERSION,
                        request_payload=payload.model_dump(),
                        response_payload=response_payload,
                        prediction=prediction,
                        score=score,
                        inference_ms=inference_ms,
                    )
                )
                db.commit()
            finally:
                db.close()
    except SQLAlchemyError:
        PREDICTION_ERRORS_TOTAL.inc()
        logger.exception(
            "prediction_persist_failed",
            extra={"extra_data": {"model_version": MODEL_VERSION}},
        )
        raise

    logger.info(
        "prediction_completed",
        extra={
            "extra_data": {
                "model_version": MODEL_VERSION,
                "input": payload.model_dump(),
                "output": response_payload,
            }
        },
    )

    return PredictionResponse(**response_payload)
