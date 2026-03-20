from app.schemas import PredictionRequest


def score_request(payload: PredictionRequest) -> float:
    score = 0.0
    score += min(payload.support_tickets_last_30d * 0.12, 0.36)
    score += 0.18 if payload.transactions_last_30d < 5 else 0.02
    score += 0.14 if payload.avg_session_minutes < 10 else 0.03
    score += 0.12 if payload.income < 40000 else 0.01
    score += 0.08 if payload.age < 25 else 0.02
    return round(min(score, 0.99), 4)


def label_from_score(score: float) -> str:
    return "churn" if score >= 0.5 else "retain"
