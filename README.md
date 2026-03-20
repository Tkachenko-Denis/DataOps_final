# DataOps Final Project

Репозиторий содержит файлы для полного цикла развёртывания учебного ML-сервиса:

- `MLflow` + `PostgreSQL`
- `Airflow` + `PostgreSQL`
- `LakeFS` + `PostgreSQL` + `MinIO`
- `JupyterHub`
- `FastAPI` ML-сервис + `PostgreSQL`
- `Prometheus` + `Grafana`
- `Kubernetes` manifests
- `Helm chart`

## Структура проекта

- `infrastructure/mlflow`
- `infrastructure/airflow`
- `infrastructure/lakefs`
- `infrastructure/jupyterhub`
- `services/ml-service`
- `monitoring`
- `k8s`
- `helm/ml-service`
- `prompts`
- `docs`

## Требования

- Docker Desktop
- Docker Compose
- Git
- Kubernetes и Helm для этапов 7-8

## Сводка сервисов

| Сервис | URL | Учётные данные |
|---|---|---|
| MLflow | `http://localhost:5000` | не требуются |
| Airflow | `http://localhost:8080` | `admin / admin` |
| LakeFS | `http://localhost:8001` | создаются при первом входе |
| MinIO Console | `http://localhost:9001` | `minioadmin / minioadmin123` |
| JupyterHub | `http://localhost:8002` | `admin / admin` |
| ML-service API | `http://localhost:8003/docs` | не требуются |
| Prometheus | `http://localhost:9090` | не требуются |
| Grafana | `http://localhost:3000` | `admin / admin` |

## Быстрый порядок запуска

1. MLflow
2. Airflow
3. LakeFS
4. JupyterHub
5. ML-service
6. Prometheus и Grafana
7. Kubernetes manifests
8. Helm chart
9. Prompt Storage в MLflow

## 1. MLflow

```powershell
cd C:\Users\denvt\DataOps_final\infrastructure\mlflow
Copy-Item .env.example .env
docker compose up -d --build
docker compose ps
```

Файл `.env`:

```env
POSTGRES_DB=mlflow
POSTGRES_USER=mlflow
POSTGRES_PASSWORD=mlflow
```

Проверка:

- открыть `http://localhost:5000`
- создать эксперимент `final-project`
- создать `run`
- приложить любой артефакт

Если `MLflow` не поднимается после неудачной миграции:

```powershell
docker compose down -v --remove-orphans
docker compose up -d --build
```

## 2. Airflow

```powershell
cd C:\Users\denvt\DataOps_final\infrastructure\airflow
Copy-Item .env.example .env
docker compose up airflow-init
docker compose up -d
docker compose ps
```

Учётные данные:

- логин: `admin`
- пароль: `admin`

Проверка:

- открыть `http://localhost:8080`
- включить DAG `demo_pipeline`
- запустить DAG вручную

## 3. LakeFS

```powershell
cd C:\Users\denvt\DataOps_final\infrastructure\lakefs
Copy-Item .env.example .env
docker compose up -d
docker compose ps
```

Рабочий `.env`:

```env
POSTGRES_DB=lakefs
POSTGRES_USER=lakefs
POSTGRES_PASSWORD=lakefs
MINIO_ROOT_USER=minioadmin
MINIO_ROOT_PASSWORD=minioadmin123
MINIO_BUCKET=lakefs-storage
LAKEFS_SECRET_KEY=supersecretkey1234567890123456
LAKEFS_ACCESS_KEY_ID=lakefsadmin
LAKEFS_SECRET_ACCESS_KEY=lakefsadmin123
```

Учётные данные:

- MinIO:
  - логин `minioadmin`
  - пароль `minioadmin123`
- LakeFS:
  - первый вход через `http://localhost:8001`
  - далее использовать созданные в интерфейсе данные

Проверка:

- открыть `http://localhost:9001` и убедиться, что bucket `lakefs-storage` существует
- открыть `http://localhost:8001`
- создать репозиторий `training-data`
- создать branch `feature/demo`
- загрузить файл
- выполнить commit

Если `LakeFS` работает нестабильно после неудачной первичной настройки:

```powershell
docker compose down -v --remove-orphans
docker compose up -d
```

## 4. JupyterHub

```powershell
cd C:\Users\denvt\DataOps_final\infrastructure\jupyterhub
Copy-Item .env.example .env
docker compose up -d --build
docker compose ps
```

Учётные данные:

- логин: `admin`
- пароль: `admin`

Проверка:

- открыть `http://localhost:8002`
- войти под `admin`
- дождаться запуска окружения
- открыть JupyterLab
- создать notebook

## 5. ML-service

```powershell
cd C:\Users\denvt\DataOps_final\services\ml-service
Copy-Item .env.example .env
docker compose up -d --build
docker compose ps
```

Проверка:

- открыть `http://localhost:8003/docs`
- выполнить запрос `POST /api/v1/predict`

Пример запроса:

```powershell
Invoke-RestMethod `
  -Method Post `
  -Uri "http://localhost:8003/api/v1/predict" `
  -ContentType "application/json" `
  -Body '{"age":34,"income":72000,"transactions_last_30d":14,"support_tickets_last_30d":1,"avg_session_minutes":22}'
```

Метрики:

- `http://localhost:8003/metrics`

## 6. Monitoring

```powershell
cd C:\Users\denvt\DataOps_final\monitoring
docker compose up -d --build
docker compose ps
```

Учётные данные Grafana:

- логин: `admin`
- пароль: `admin`

Проверка:

- открыть `http://localhost:9090`
- открыть `http://localhost:3000`
- в Grafana открыть дашборд `ML Service Overview`
- выполнить несколько запросов в ML-сервис
- убедиться, что метрики появились

## 7. Kubernetes

Файлы:

- `k8s/deployment.yaml`
- `k8s/service.yaml`
- `k8s/ingress.yaml`

Применение:

```powershell
cd C:\Users\denvt\DataOps_final
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
kubectl apply -f k8s/ingress.yaml
```

## 8. Helm

Установка:

```powershell
cd C:\Users\denvt\DataOps_final
helm install ml-service ./helm/ml-service
```

Изменение версии образа:

```powershell
helm upgrade ml-service ./helm/ml-service --set image.tag=1.0.1
```

## 9. Prompt Storage MLflow

Файлы с версиями промптов:

- `prompts/v1.txt`
- `prompts/v2.txt`
- `prompts/v3.txt`

Их нужно занести в Prompt Storage MLflow вручную через интерфейс.

## Что приложить к сдаче

- ссылка на репозиторий
- скриншот MLflow с экспериментом и run
- скриншот Airflow с DAG
- скриншот LakeFS с репозиторием, branch и commit
- скриншот JupyterHub с открытым JupyterLab
- скриншот успешного запроса к `POST /api/v1/predict`
- скриншот Grafana с метриками
- скриншот Prompt Storage с несколькими версиями

## Дополнительные файлы

- [Чек-лист проверки](C:/Users/denvt/DataOps_final/docs/checklist.md)
- [Что показывать на защите](C:/Users/denvt/DataOps_final/docs/evidence.md)
