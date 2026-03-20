#!/bin/sh
set -e

until nc -z "$POSTGRES_HOST" "$POSTGRES_PORT"; do
  echo "Waiting for PostgreSQL..."
  sleep 2
done

exec mlflow server \
  --host 0.0.0.0 \
  --port 5000 \
  --backend-store-uri "$MLFLOW_BACKEND_STORE_URI" \
  --default-artifact-root "$MLFLOW_ARTIFACT_ROOT"
