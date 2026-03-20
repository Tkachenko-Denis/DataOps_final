FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir \
    mlflow==2.22.0 \
    psycopg2-binary==2.9.10

COPY entrypoint.sh /app/entrypoint.sh

EXPOSE 5000

CMD ["sh", "/app/entrypoint.sh"]
