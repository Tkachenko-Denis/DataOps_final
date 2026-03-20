from prometheus_client import CONTENT_TYPE_LATEST, Counter, Histogram, generate_latest
from starlette.responses import Response


PREDICTION_REQUESTS_TOTAL = Counter(
    "ml_service_prediction_requests_total",
    "Total prediction requests",
)

PREDICTION_ERRORS_TOTAL = Counter(
    "ml_service_prediction_errors_total",
    "Total prediction errors",
)

PREDICTION_LATENCY_SECONDS = Histogram(
    "ml_service_prediction_latency_seconds",
    "Prediction request latency",
    buckets=(0.01, 0.05, 0.1, 0.3, 0.5, 1.0, 3.0, 5.0),
)


def metrics_response() -> Response:
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)
